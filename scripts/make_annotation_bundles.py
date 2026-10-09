"""Portable annotation packages, so that annotators do not need this repository or the SWiG images.

    uv run python scripts/make_annotation_bundles.py

Writes annotation/human_ceiling_bundle.zip (the role-pointing page with its 100 images, self-contained) and
annotation/gold_check_bundle.zip (the six contact sheets of the detector-flagged items and a CSV with the verdict
column emptied, for an independent second annotator). Each zip carries a README with the instructions.
"""

from __future__ import annotations

import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fvp.data import image_path  # noqa: E402

ANN = ROOT / "annotation"

CEILING_README = """Role pointing: human annotation
================================

Open human_ceiling.html in a browser (Chrome, Edge or Firefox; no internet needed).
Each screen shows one image and one phrase such as "the one who is biting (the agent)".
Drag with the mouse to draw a box around the thing the phrase refers to. Draw again to replace it.
If the phrase cannot be answered on that image, click "Cannot tell".
200 screens in all; your progress is saved in the browser, so you can close and come back.
When you reach the end, click "Download annotations" and send the file human_ceiling_annotations.json back.
Please do not look up the images or captions elsewhere: the point is what a person can do from the phrase alone.
"""

GOLD_README = """Gold-box check: second annotator
=================================

The sheets gold_flagged_sheet_1.png to _6.png show images in which an object detector disagreed with the
annotated boxes. Each tile is numbered (#1, #2, ...) and shows the caption, the two annotated role boxes in GREEN
("gold <role>: <noun>") and, for each noun, the detector's box in RED ("det: <noun> [...]"; the word in brackets is
the detector's own flag, ignore it).

gold_flagged.csv has one row per noun (columns sheet, tile, valse_id, image_file, caption, word, role, ...).
For each row, look at the RED box of that noun and fill the "verdict" column with one of:
  ok       the red box is on the right object for that noun (the detector agrees with the green box)
  swapped  the red box is on the OTHER participant of the pair (e.g. the red "man" box sits on the woman)
  other    anything else: the red box is on neither, covers both, or you cannot tell
Judge the red box only; do not try to decide whether the green boxes are right, that is derived afterwards.
Please work from the sheets alone, without consulting anyone's earlier judgements, and send the CSV back.
"""


def main() -> None:
    # 1. human ceiling: page + images
    targets = json.loads((ANN / "human_ceiling_targets.json").read_text(encoding="utf-8"))
    out = ANN / "human_ceiling_bundle"
    shutil.rmtree(out, ignore_errors=True)
    (out / "images").mkdir(parents=True)
    copied = set()
    for t in targets:
        if t["image"] in copied:
            continue
        shutil.copy(image_path({"image_file": t["image"]}), out / "images" / t["image"])
        copied.add(t["image"])
    html = (ANN / "human_ceiling.html").read_text(encoding="utf-8").replace("../data/swig/images/", "images/")
    (out / "human_ceiling.html").write_text(html, encoding="utf-8")
    (out / "README.txt").write_text(CEILING_README, encoding="utf-8")
    z = shutil.make_archive(str(ANN / "human_ceiling_bundle"), "zip", out)
    print(f"{z}: {len(copied)} images, {len(targets)} targets, {Path(z).stat().st_size / 1e6:.1f} MB")

    # 2. gold check: sheets + blank CSV
    out = ANN / "gold_check_bundle"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    sheets = sorted((ROOT / "outputs").glob("gold_flagged_sheet_*.png"))
    for sh in sheets:
        shutil.copy(sh, out / sh.name)
    with open(ROOT / "outputs" / "gold_flagged.csv", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = list(reader.fieldnames or [])
    with open(out / "gold_flagged.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            r = dict(r)
            for k in r:
                if k.lower().startswith("verdict") or k.lower().startswith("note"):
                    r[k] = ""
            w.writerow(r)
    (out / "README.txt").write_text(GOLD_README, encoding="utf-8")
    z = shutil.make_archive(str(ANN / "gold_check_bundle"), "zip", out)
    print(f"{z}: {len(sheets)} sheets, {len(rows)} items, columns {fields}, {Path(z).stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
