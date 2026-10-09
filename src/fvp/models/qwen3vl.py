"""Qwen3-VL wrapper. Grounding output is JSON with "bbox_2d" on a 0-1000 grid (verified in the trial:
mean IoU on noun prompts 0.77 under the grid reading vs 0.21 under the pixel reading)."""

from __future__ import annotations

import re

from .base import ANY_BOX_RE, GroundResult, HFChatVLM  # noqa: F401

BOX_RE = re.compile(r"\"bbox_2d\"\s*:\s*\[\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\]")


class Qwen3VL(HFChatVLM):
    coord_convention = "norm1000"

    def __init__(self, model_id: str = "Qwen/Qwen3-VL-2B-Instruct", **kw):
        super().__init__(model_id, **kw)
        self.patch = getattr(self.model.config.vision_config, "patch_size", 16)

    def input_wh(self, inputs):
        thw = inputs.get("image_grid_thw")
        if thw is None:
            return (0, 0)
        t, h, w = [int(x) for x in thw[0].tolist()]
        return (w * self.patch, h * self.patch)

    def grounding_prompt(self, target: str) -> str:
        return (f"Locate {target} in the image and output its bounding box in JSON format "
                "as [{\"bbox_2d\": [x1, y1, x2, y2], \"label\": \"...\"}].")

    def parse_boxes(self, raw: str):
        boxes = [[float(v) for v in m] for m in BOX_RE.findall(raw)]
        return boxes or super().parse_boxes(raw)
