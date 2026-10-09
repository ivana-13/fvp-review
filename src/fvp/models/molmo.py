"""Molmo (allenai/Molmo-7B-D-0924) wrapper: a native point-output model.

Molmo answers "Point to X" with <point x="52.3" y="61.0" alt="X">X</point> (or <points x1="..." y1="..." x2="..."
y2="..." ...> for several targets); coordinates are percentages of the image width and height. The pointing probe
therefore scores a point-in-box hit instead of IoU (recorded as iou 1.0/0.0 so the rest of the pipeline is unchanged;
see scripts/run_probes.py). Yes/no and A/B probes read next-token logits as for the other models.

Molmo ships its own modelling code (trust_remote_code); the processor API is processor.process(images=[...],
text=...) and generation goes through model.generate_from_batch. Written for the VM and not run here: run
`bash scripts/vm_smoke.sh molmo-7b-d` first.
"""

from __future__ import annotations

import re

import torch
from PIL import Image

from .base import GroundResult, HFChatVLM

POINT_RE = re.compile(r'x\d*="([\d.]+)"\s+y\d*="([\d.]+)"')


def parse_points(raw: str, wh: tuple[int, int]) -> list[list[float]]:
    """Molmo point tags (percent coordinates) -> pixel points [[x, y], ...]."""
    W, H = wh
    return [[float(x) / 100.0 * W, float(y) / 100.0 * H] for x, y in POINT_RE.findall(raw)]


class Molmo(HFChatVLM):
    coord_convention = "points"
    supports_points = True

    def __init__(self, model_id: str = "allenai/Molmo-7B-D-0924", device: str = "cuda", dtype=torch.bfloat16,
                 device_map: str | None = None, **kw):
        from transformers import AutoModelForCausalLM, AutoProcessor

        self.model_id = model_id
        self.device = device
        self.dtype = dtype
        self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True, torch_dtype=dtype, device_map=device)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype=dtype,
                                                          device_map=device_map or device)
        self.model.eval()
        self.quantization = None
        self.tok = self.processor.tokenizer
        self._ids = {w: self._single_token_id(w) for w in [*self.yes_no_words, *self.ab_words]}

    # ---------- inputs ----------
    def _inputs(self, image: Image.Image | None, text: str):
        images = [image] if image is not None else None  # the processor treats [] as a real (empty) image list
        inputs = self.processor.process(images=images, text=text)
        out = {}
        for k, v in inputs.items():
            v = v.to(self.model.device)
            if v.is_floating_point():  # the processor emits float32 image tensors whatever dtype the model runs in
                v = v.to(self.dtype)
            elif k == "input_ids":  # int32 for text-only prompts; generation appends int64 tokens
                v = v.long()
            out[k] = v.unsqueeze(0)
        return out

    @torch.no_grad()
    def _next_logits(self, image, text) -> torch.Tensor:
        inputs = self._inputs(image, text)
        return self.model(**inputs).logits[0, -1].float()

    @torch.no_grad()
    def generate(self, image: Image.Image | None, prompt: str, max_new_tokens: int = 64) -> str:
        from transformers import GenerationConfig

        inputs = self._inputs(image, prompt)
        out = self.model.generate_from_batch(
            inputs, GenerationConfig(max_new_tokens=max_new_tokens, do_sample=False, stop_strings="<|endoftext|>"),
            tokenizer=self.tok)
        gen = out[0, inputs["input_ids"].size(1):]
        return self.tok.decode(gen, skip_special_tokens=True).strip()

    # ---------- pointing ----------
    def grounding_prompt(self, target: str) -> str:
        return f"Point to {target}."

    @torch.no_grad()
    def ground(self, image: Image.Image, target: str, max_new_tokens: int = 96, context: str | None = None) -> GroundResult:
        prompt = self.grounding_prompt(target)
        if context:
            prompt = f"{context}\n{prompt}"
        raw = self.generate(image, prompt, max_new_tokens)
        return GroundResult(raw=raw, boxes_norm1000=[], boxes_abs_input=[], input_wh=(0, 0), convention="points",
                            points_px=parse_points(raw, image.size))
