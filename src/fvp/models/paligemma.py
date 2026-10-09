"""PaliGemma 2 wrapper (google/paligemma2-10b-mix-448): detection through location tokens.

The "mix" checkpoints answer "detect X" with "<loc0123><loc0456><loc0789><loc0012> X": four location tokens on a
0-1023 grid in the order y_min, x_min, y_max, x_max (each divided by 1024 and scaled by the image height or width).
PaliGemma has no chat template and always expects an image, so prompts are passed raw (prefixed with "answer en" for
the question probes) and the blind probes use a blank white image. The repository is gated on the Hub: accept the
licence and set HF_TOKEN before loading. Written for the VM and not run here: run
`bash scripts/vm_smoke.sh paligemma2-10b` first.
"""

from __future__ import annotations

import re

import torch
from PIL import Image

from .base import GroundResult, HFChatVLM

LOC_RE = re.compile(r"<loc(\d{4})><loc(\d{4})><loc(\d{4})><loc(\d{4})>")


def parse_locs(raw: str, wh: tuple[int, int]) -> list[list[float]]:
    """PaliGemma location tokens (y1, x1, y2, x2 on a 0-1023 grid) -> pixel boxes [x1, y1, x2, y2]."""
    W, H = wh
    return [[int(x1) / 1024 * W, int(y1) / 1024 * H, int(x2) / 1024 * W, int(y2) / 1024 * H]
            for y1, x1, y2, x2 in LOC_RE.findall(raw)]


class PaliGemma(HFChatVLM):
    coord_convention = "pixels"

    def __init__(self, model_id: str = "google/paligemma2-10b-mix-448", device: str = "cuda", dtype=torch.bfloat16,
                 device_map: str | None = None, **kw):
        from transformers import AutoProcessor, PaliGemmaForConditionalGeneration

        self.model_id = model_id
        self.device = device
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = PaliGemmaForConditionalGeneration.from_pretrained(model_id, dtype=dtype, device_map=device_map or device)
        self.model.eval()
        self.quantization = None
        self.tok = self.processor.tokenizer
        self._ids = {w: self._single_token_id(w) for w in [*self.yes_no_words, *self.ab_words]}
        self._blank = Image.new("RGB", (448, 448), "white")

    def _inputs(self, image: Image.Image | None, text: str):
        img = image if image is not None else self._blank
        inputs = self.processor(text=f"answer en {text}", images=img, return_tensors="pt")
        return inputs.to(self.model.device)

    @torch.no_grad()
    def generate(self, image: Image.Image | None, prompt: str, max_new_tokens: int = 64) -> str:
        inputs = self._inputs(image, prompt)
        out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        return self.tok.decode(out[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    # ---------- grounding ----------
    def grounding_prompt(self, target: str) -> str:
        # the mix checkpoints were trained on "detect <object>" without an article ("detect man", "detect dog")
        t = target.strip()
        for art in ("the ", "a ", "an "):
            if t.lower().startswith(art):
                t = t[len(art):]
                break
        return f"detect {t}"

    @torch.no_grad()
    def ground(self, image: Image.Image, target: str, max_new_tokens: int = 48, context: str | None = None) -> GroundResult:
        prompt = self.grounding_prompt(target)
        if context:
            prompt = f"{context} {prompt}"
        inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(self.model.device)
        out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        raw = self.tok.decode(out[0, inputs["input_ids"].shape[1]:], skip_special_tokens=False)
        boxes = parse_locs(raw, image.size)
        return GroundResult(raw=raw.strip(), boxes_norm1000=boxes, boxes_abs_input=boxes, input_wh=(0, 0), convention="norm1000")
