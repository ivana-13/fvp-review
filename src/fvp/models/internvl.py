"""InternVL3.5 (HF-format checkpoints) wrapper. Grounding follows the InternVL convention:
prompt '<ref>target</ref>', answer '<box>[[x1, y1, x2, y2]]</box>' on a 0-1000 grid."""

from __future__ import annotations

import re

from .base import GroundResult, HFChatVLM  # noqa: F401

BOX_RE = re.compile(r"<box>\s*\[\s*\[\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\]\s*\]\s*</box>")


class InternVL(HFChatVLM):
    coord_convention = "norm1000"

    def __init__(self, model_id: str = "OpenGVLab/InternVL3_5-2B-HF", **kw):
        super().__init__(model_id, **kw)

    def grounding_prompt(self, target: str) -> str:
        return f"Please provide the bounding box coordinate of the region this sentence describes: <ref>{target}</ref>"

    def parse_boxes(self, raw: str):
        boxes = [[float(v) for v in m] for m in BOX_RE.findall(raw)]
        return boxes or super().parse_boxes(raw)
