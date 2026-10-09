"""Download the Visual Genome images needed by the ARO subsets (URLs from image_data.json) into data/aro/images/.

Usage:
    uv run python scripts/fetch_aro_images.py [--workers 8]
Resumable: existing, readable images are skipped.
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ARO = DATA / "aro"
IMG = ARO / "images"


def ok(p: Path) -> bool:
    try:
        Image.open(p).verify()
        return True
    except Exception:
        return False


def fetch(url: str, dest: Path) -> str:
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=60)
            if r.status_code == 200 and r.content:
                dest.write_bytes(r.content)
                if ok(dest):
                    return "ok"
                dest.unlink(missing_ok=True)
        except Exception:
            pass
    return "failed"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    IMG.mkdir(parents=True, exist_ok=True)
    urls: dict[str, str] = {}
    for name in ["aro-relation", "aro-spatial"]:
        p = DATA / "joined" / f"{name}.valid.jsonl"
        if p.exists():
            for l in open(p, encoding="utf-8"):
                r = json.loads(l)
                if r.get("url"):
                    urls[r["image_file"]] = r["url"]
    todo = {f: u for f, u in urls.items() if not (IMG / f).exists() or not ok(IMG / f)}
    print(f"{len(urls)} images needed, {len(urls) - len(todo)} present, {len(todo)} to fetch")
    failed = []
    with ThreadPoolExecutor(args.workers) as ex:
        futs = {ex.submit(fetch, u, IMG / f): f for f, u in todo.items()}
        for i, fut in enumerate(as_completed(futs), 1):
            if fut.result() != "ok":
                failed.append(futs[fut])
            if i % 200 == 0:
                print(f"  {i}/{len(todo)}", flush=True)
    print(f"done; failed: {len(failed)}")
    (ARO / "fetch_done.txt").write_text(f"{len(urls) - len(failed)} of {len(urls)} images present\n", encoding="utf-8")
    if failed:
        (ARO / "failed_images.txt").write_text("\n".join(failed), encoding="utf-8")


if __name__ == "__main__":
    main()
