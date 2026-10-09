"""Shared probe logic for chat-style vision-language models in transformers.

Subclasses set the grounding prompt and the box parser. Coordinates are assumed to be on a
0-1000 grid unless `coord_convention` is overridden; `ground` records both readings so a
calibration script can check which one matches gold boxes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import torch
from PIL import Image

from ..geometry import normalized_1000_to_abs, scale_box

ANY_BOX_RE = re.compile(r"\[\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\]")


@dataclass
class GroundResult:
    raw: str
    boxes_norm1000: list[list[float]]
    boxes_abs_input: list[list[float]]
    input_wh: tuple[int, int]
    convention: str = "norm1000"
    points_px: list[list[float]] = field(default_factory=list)  # point-output models (Molmo)

    @property
    def boxes_px(self) -> list[list[float]]:
        return self.boxes_norm1000 if self.convention == "norm1000" else self.boxes_abs_input


class HFChatVLM:
    coord_convention = "norm1000"
    yes_no_words = ("Yes", "No")
    ab_words = ("A", "B")
    supports_foil = True      # yes/no, pairwise, blind and likelihood probes
    supports_pointing = True  # box or point output for a described target
    supports_points = False   # True when `ground` returns points instead of boxes

    def __init__(self, model_id: str, device: str = "cuda", dtype=torch.bfloat16, quantization: str | None = None,
                 offload_gpu_gib: float | None = None, max_pixels: int | None = None, device_map: str | None = None,
                 **load_kwargs):
        """quantization: None | 'nf4' | 'int8' (bitsandbytes, vision tower and lm_head kept in bf16).
        offload_gpu_gib: if set, load in bf16 with device_map='auto' and this much GPU memory, rest on CPU.
        max_pixels: cap on image pixels fed to the processor (fewer visual tokens, less activation memory).
        device_map: e.g. 'auto' to spread a large model over the GPU and CPU (32B/38B on one card)."""
        from transformers import AutoModelForImageTextToText, AutoProcessor

        self.model_id = model_id
        self.device = device
        proc_kwargs = {"max_pixels": max_pixels} if max_pixels else {}
        self.processor = AutoProcessor.from_pretrained(model_id, **proc_kwargs)
        if quantization in ("nf4", "int8"):
            from transformers import BitsAndBytesConfig

            if quantization == "nf4":
                qcfg = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=dtype,
                                          bnb_4bit_use_double_quant=True, llm_int8_skip_modules=["visual", "lm_head"])
            else:
                qcfg = BitsAndBytesConfig(load_in_8bit=True, llm_int8_skip_modules=["visual", "lm_head"])
            self.model = AutoModelForImageTextToText.from_pretrained(
                model_id, dtype=dtype, device_map=device_map or device, quantization_config=qcfg, **load_kwargs)
        elif offload_gpu_gib:
            self.model = AutoModelForImageTextToText.from_pretrained(
                model_id, dtype=dtype, device_map="auto",
                max_memory={0: f"{offload_gpu_gib}GiB", "cpu": "48GiB"}, **load_kwargs)
        else:
            self.model = AutoModelForImageTextToText.from_pretrained(model_id, dtype=dtype, device_map=device_map or device, **load_kwargs)
        self.model.eval()
        self.quantization = quantization
        self.tok = self.processor.tokenizer
        self._ids = {w: self._single_token_id(w) for w in [*self.yes_no_words, *self.ab_words]}

    def _single_token_id(self, word: str) -> int:
        ids = self.tok.encode(word, add_special_tokens=False)
        if len(ids) != 1:
            raise ValueError(f"{word!r} is not a single token for {self.model_id}: {ids}")
        return ids[0]

    # ---------- inputs ----------
    def _inputs(self, image: Image.Image | None, text: str):
        content = []
        if image is not None:
            content.append({"type": "image", "image": image})
        content.append({"type": "text", "text": text})
        messages = [{"role": "user", "content": content}]
        inputs = self.processor.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_dict=True, return_tensors="pt"
        )
        return inputs.to(self.device)

    def input_wh(self, inputs) -> tuple[int, int]:
        return (0, 0)

    # ---------- probes ----------
    @torch.no_grad()
    def _next_logits(self, image, text) -> torch.Tensor:
        inputs = self._inputs(image, text)
        return self.model(**inputs).logits[0, -1].float()

    def yes_prob(self, image: Image.Image | None, caption: str) -> float:
        prompt = f"Does this caption correctly describe the image? Caption: \"{caption}\"\nAnswer with Yes or No only."
        logits = self._next_logits(image, prompt)
        y, n = self.yes_no_words
        two = torch.stack([logits[self._ids[y]], logits[self._ids[n]]])
        return torch.softmax(two, dim=0)[0].item()

    def choose(self, image: Image.Image | None, a: str, b: str) -> float:
        where = "this image" if image is not None else "a photograph you cannot see"
        prompt = f"Which caption describes {where} better?\nA: {a}\nB: {b}\nAnswer with A or B only."
        logits = self._next_logits(image, prompt)
        wa, wb = self.ab_words
        two = torch.stack([logits[self._ids[wa]], logits[self._ids[wb]]])
        return torch.softmax(two, dim=0)[0].item()

    def choose_sym(self, image, a: str, b: str) -> float:
        p1 = self.choose(image, a, b)
        p2 = 1.0 - self.choose(image, b, a)
        return (p1 + p2) / 2.0

    def choose_ab(self, image: Image.Image | None, prompt: str) -> float:
        """P(A) against P(B) as the next token after an arbitrary prompt that asks for A or B (two-box role probe)."""
        logits = self._next_logits(image, prompt)
        wa, wb = self.ab_words
        two = torch.stack([logits[self._ids[wa]], logits[self._ids[wb]]])
        return torch.softmax(two, dim=0)[0].item()

    @torch.no_grad()
    def generate(self, image: Image.Image | None, prompt: str, max_new_tokens: int = 64) -> str:
        inputs = self._inputs(image, prompt)
        out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        return self.tok.decode(out[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    # ---------- grounding: subclasses override the prompt and parser ----------
    def grounding_prompt(self, target: str) -> str:
        raise NotImplementedError

    def parse_boxes(self, raw: str) -> list[list[float]]:
        return [[float(v) for v in m] for m in ANY_BOX_RE.findall(raw)]

    @torch.no_grad()
    def ground(self, image: Image.Image, target: str, max_new_tokens: int = 96, context: str | None = None) -> GroundResult:
        """Box for `target`. If `context` is given (e.g. a caption), it is prepended to the grounding prompt."""
        prompt = self.grounding_prompt(target)
        if context:
            prompt = f"{context}\n{prompt}"
        inputs = self._inputs(image, prompt)
        in_wh = self.input_wh(inputs)
        out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        raw = self.tok.decode(out[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        boxes = self.parse_boxes(raw)
        W, H = image.size
        norm = [normalized_1000_to_abs(b, (W, H)) for b in boxes]
        absi = [scale_box(b, in_wh, (W, H)) if in_wh != (0, 0) else list(b) for b in boxes]
        return GroundResult(raw=raw, boxes_norm1000=norm, boxes_abs_input=absi, input_wh=in_wh,
                            convention=self.coord_convention)
