"""Shared helpers for the run scripts: subsets, item image paths, and the cache-directory default.

Every joined item (data/joined/<subset>.valid.jsonl) carries `image_file` and, for non-SWiG sources, `image_dir`
relative to data/. `SUBSETS` lists the subsets the scripts accept; action-replacement has one target (the agent),
all others have two (the swapped participants), so scripts branch on `subset == "action-replacement"` only.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

SUBSETS = ["actant-swap", "action-replacement", "aro-relation", "aro-spatial"]


def image_path(item: dict) -> Path:
    return DATA / item.get("image_dir", "swig/images") / item["image_file"]


def set_cache_default() -> None:
    """On the Windows laptop the Hugging Face cache lives on an ASCII path (native libraries break on the
    non-ASCII user folder). Elsewhere HF_HOME is left to the environment. Call before importing transformers."""
    if sys.platform == "win32":
        os.environ.setdefault("HF_HOME", r"C:\tmp\hf")
