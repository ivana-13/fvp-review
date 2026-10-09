"""Gemma 3 wrapper (google/gemma-3-12b-it): a chat VLM without native grounding, used for the foil probes only.

It takes the yes/no, pairwise and blind probes through the shared chat-template code; the pointing probe is skipped
(supports_pointing = False). Gated on the Hub: accept the licence and set HF_TOKEN. Written for the VM.
"""

from __future__ import annotations

from .base import HFChatVLM


class Gemma3(HFChatVLM):
    supports_pointing = False

    def __init__(self, model_id: str = "google/gemma-3-12b-it", **kw):
        super().__init__(model_id, **kw)

    def grounding_prompt(self, target: str) -> str:  # never used: pointing is skipped for this model
        return f"Give the bounding box of {target} as [x1, y1, x2, y2] on a 0-1000 grid."
