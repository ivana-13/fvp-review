"""Florence-2 wrapper: a grounding specialist used as a pointing ceiling.

Uses the native transformers implementation (Florence2ForConditionalGeneration, transformers >= 4.56) with the
converted checkpoint florence-community/Florence-2-large; the original microsoft/Florence-2-large repository relies on
remote code that no longer loads under transformers 5. Florence-2 has no chat interface, so it takes the pointing
probe only (supports_foil = False; run_probes.py skips the foil, blind and verb probes). Grounding uses the
<CAPTION_TO_PHRASE_GROUNDING> task with the target phrase as text; the processor's post-processing returns boxes in
pixels of the original image.
"""

from __future__ import annotations

import torch
from PIL import Image

from .base import GroundResult

TASK = "<CAPTION_TO_PHRASE_GROUNDING>"


class Florence2:
    coord_convention = "pixels"
    supports_foil = False
    supports_pointing = True

    def __init__(self, model_id: str = "florence-community/Florence-2-large", device: str = "cuda", dtype=torch.float16,
                 device_map: str | None = None, **kw):
        from transformers import Florence2ForConditionalGeneration, Florence2Processor

        self.model_id = model_id
        self.device = device
        self.dtype = dtype if device != "cpu" else torch.float32
        self.processor = Florence2Processor.from_pretrained(model_id)
        self.model = Florence2ForConditionalGeneration.from_pretrained(model_id, dtype=self.dtype, device_map=device_map or device)
        self.model.eval()
        self.tok = self.processor.tokenizer
        self.quantization = None

    def yes_prob(self, image, caption):  # not a chat model
        raise NotImplementedError("Florence-2 takes the pointing probe only")

    choose = choose_sym = yes_prob

    def generate(self, image, prompt, max_new_tokens=64):
        raise NotImplementedError("Florence-2 takes the pointing probe only")

    @torch.no_grad()
    def ground(self, image: Image.Image, target: str, max_new_tokens: int = 96, context: str | None = None) -> GroundResult:
        text = f"{context} {target}" if context else target
        inputs = self.processor(text=TASK + text, images=image, return_tensors="pt").to(self.model.device, self.dtype)
        out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, num_beams=3, do_sample=False)
        raw = self.processor.batch_decode(out, skip_special_tokens=False)[0]
        parsed = self.processor.post_process_generation(raw, task=TASK, image_size=image.size)
        boxes = [[float(v) for v in b] for b in (parsed.get(TASK) or {}).get("bboxes", [])]
        return GroundResult(raw=raw.strip(), boxes_norm1000=boxes, boxes_abs_input=boxes, input_wh=(0, 0), convention="norm1000")
