"""Contact sheets of the actant-swap items whose SWiG gold box the detector flags as swapped, for a manual check.

Each tile shows the image with the two SWiG role boxes (green, "gold <role>: <word>") and the detector's top box for
each word (red, "det: <word>"), plus the caption. Twenty tiles per page.

Usage:
    uv run python scripts/make_gold_contact_sheet.py [--flag swapped] [--cols 4] [--rows 5]
Writes outputs/gold_flagged_sheet_<k>.png and outputs/gold_flagged.csv (one row per flagged word, with an empty
"verdict" column to fill in per word, judging the red detector box: ok = on the right participant, swapped = on the
other participant, other = anything else; scripts/make_paper_assets.py turns these into item-level gold verdicts).
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "outputs"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--flag", default="swapped")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--rows", type=int, default=5)
    ap.add_argument("--tile", type=int, default=340)
    args = ap.parse_args()
    items = {json.loads(l)["valse_id"]: json.loads(l) for l in open(DATA / "joined" / "actant-swap.valid.jsonl", encoding="utf-8")}
    gc = [json.loads(l) for l in open(DATA / "gold_check.jsonl", encoding="utf-8")]
    flagged = [r for r in gc if any(w["flag"] == args.flag for w in r["words"].values()) and r["valse_id"] in items]
    print(f"{len(flagged)} items with a word flagged '{args.flag}'")
    try:
        font = ImageFont.truetype("arial.ttf", 13)
        small = ImageFont.truetype("arial.ttf", 11)
    except Exception:
        font = small = ImageFont.load_default()

    with open(OUT / "gold_flagged.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["sheet", "tile", "valse_id", "image_file", "caption", "word", "role", "flag", "iou_own", "iou_other", "verdict"])
        per_page = args.cols * args.rows
        T, cap_h = args.tile, 44
        for page in range(0, len(flagged), per_page):
            chunk = flagged[page: page + per_page]
            sheet = Image.new("RGB", (args.cols * T, args.rows * (T + cap_h)), "white")
            for k, r in enumerate(chunk):
                it = items[r["valse_id"]]
                img = Image.open(DATA / "swig" / "images" / it["image_file"]).convert("RGB")
                s = min(T / img.width, T / img.height)
                img = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))))
                d = ImageDraw.Draw(img)
                for word, tg in it["targets"].items():
                    if word == "__agent__":
                        continue
                    b = [v * s for v in tg["bbox"]]
                    d.rectangle(b, outline=(0, 190, 0), width=3)
                    d.text((b[0] + 3, b[1] + 2), f"gold {tg['role']}: {word}", fill=(0, 140, 0), font=small)
                for word, w in r["words"].items():
                    if w.get("top_box"):
                        b = [v * s for v in w["top_box"]]
                        d.rectangle(b, outline=(230, 30, 30), width=2)
                        d.text((b[0] + 3, max(0, b[3] - 14)), f"det: {word} [{w['flag']}]", fill=(200, 0, 0), font=small)
                x, y = (k % args.cols) * T, (k // args.cols) * (T + cap_h)
                sheet.paste(img, (x, y))
                sd = ImageDraw.Draw(sheet)
                idx = page + k + 1
                sd.text((x + 4, y + T + 2), f"#{idx} {it['image_file']}", fill=(0, 0, 0), font=font)
                sd.text((x + 4, y + T + 20), it["caption"][: 52], fill=(60, 60, 60), font=small)
                for word, w in r["words"].items():
                    wr.writerow([page // per_page + 1, idx, r["valse_id"], it["image_file"], it["caption"], word, w["role"],
                                 w["flag"], f"{w.get('iou_own', 0):.2f}", f"{w.get('iou_other', 0):.2f}", ""])
            out = OUT / f"gold_flagged_sheet_{page // per_page + 1}.png"
            sheet.save(out)
            print("wrote", out.name, f"({len(chunk)} tiles)")
    print("wrote outputs/gold_flagged.csv")


if __name__ == "__main__":
    main()
