"""Structured verification probe (RQ5): prompt builder and answer parser.

The model is asked, in one answer, to box the two participants by their role phrases and then to say which of two
captions is correct. `parse_verify` reads the answer letter and one box per role key from the generated JSON, with a
positional fallback (boxes in order of appearance) for models that do not keep the keys.
"""

from __future__ import annotations

import re

from .models.base import ANY_BOX_RE

ANSWER_RE = re.compile(r'"answer"\s*:\s*"?\s*([AB])\b')
ANSWER_FALLBACK_RE = re.compile(r"(?i)\banswer\b\W{0,6}([AB])\b")


def verify_prompt(a: str, b: str, roles: list[tuple[str, str]]) -> str:
    """`roles`: two (role_key, role_phrase) pairs, e.g. ("agent", "the one who is biting (the agent)")."""
    (r1, p1), (r2, p2) = roles
    return (
        "Two captions are proposed for this image.\n"
        f"A: {a}\nB: {b}\n"
        f"Before deciding, locate the participants: output the bounding box of {p1} under the key \"{r1}\" "
        f"and the bounding box of {p2} under the key \"{r2}\". Then decide which caption is correct.\n"
        "Answer only with a JSON object of the form "
        f"{{\"{r1}\": {{\"name\": \"...\", \"bbox_2d\": [x1, y1, x2, y2]}}, "
        f"\"{r2}\": {{\"name\": \"...\", \"bbox_2d\": [x1, y1, x2, y2]}}, \"answer\": \"A\"}} "
        "where \"answer\" is \"A\" or \"B\"."
    )


def jointbox_prompt(roles: list[tuple[str, str]]) -> str:
    """Both role phrases in one request, no captions and no judgement (the joint-box control)."""
    (r1, p1), (r2, p2) = roles
    return (
        "Locate the two participants of the action in this image: output the bounding box of "
        f"{p1} under the key \"{r1}\" and the bounding box of {p2} under the key \"{r2}\". "
        "Answer only with a JSON object of the form "
        f"{{\"{r1}\": {{\"bbox_2d\": [x1, y1, x2, y2]}}, \"{r2}\": {{\"bbox_2d\": [x1, y1, x2, y2]}}}}."
    )


def parse_verify(raw: str, roles: list[str]) -> dict:
    """Return {"answer": "A" | "B" | None, "boxes": {role: [x1, y1, x2, y2] | None}}."""
    m = ANSWER_RE.search(raw) or ANSWER_FALLBACK_RE.search(raw)
    answer = m.group(1).upper() if m else None
    boxes: dict[str, list[float] | None] = {}
    for role in roles:
        rm = re.search(
            r'"' + re.escape(role) + r'"\s*:\s*\{[^{}]*?"bbox_2d"\s*:\s*\[\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\]',
            raw,
        )
        boxes[role] = [float(v) for v in rm.groups()] if rm else None
    if all(v is None for v in boxes.values()):
        found = [[float(v) for v in g] for g in ANY_BOX_RE.findall(raw)]
        for role, box in zip(roles, found):
            boxes[role] = box
    return {"answer": answer, "boxes": boxes}
