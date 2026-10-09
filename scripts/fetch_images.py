"""Fetch individual SWiG images from the 13 GB images_512.zip on S3 using HTTP range requests.

Usage:
    uv run python scripts/fetch_images.py                 # images in data/trial_sample.jsonl
    uv run python scripts/fetch_images.py --names a.jpg b.jpg

Only the zip's central directory and the requested members are downloaded.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from remotezip import RemoteZip

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "data" / "swig" / "images"
ZIP_URL = "https://swig-data-weights.s3.us-east-2.amazonaws.com/images_512.zip"


def fetch(names: list[str]) -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    todo = [n for n in names if not (IMG_DIR / n).exists()]
    if not todo:
        print("all images already present")
        return
    with RemoteZip(ZIP_URL) as rz:
        members = {Path(m).name: m for m in rz.namelist() if m.lower().endswith(".jpg")}
        print(f"zip lists {len(members)} jpg members")
        for n in todo:
            m = members.get(n)
            if m is None:
                print("  MISSING in zip:", n)
                continue
            data = rz.read(m)
            (IMG_DIR / n).write_bytes(data)
            print(f"  fetched {n} ({len(data)//1024} KB)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--names", nargs="*")
    ap.add_argument("--sample", default=str(ROOT / "data" / "trial_sample.jsonl"))
    args = ap.parse_args()
    if args.names:
        names = args.names
    else:
        names = [json.loads(l)["image_file"] for l in open(args.sample, encoding="utf-8")]
    fetch(names)


if __name__ == "__main__":
    main()
