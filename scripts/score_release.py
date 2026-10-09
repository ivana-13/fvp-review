"""Score role-pointing predictions against the released item files (release/swaps.jsonl, release/aro_relations.jsonl).

    python scripts/score_release.py predictions.jsonl [--items release/swaps.jsonl] [--lm olmo2-7b] [--iou 0.5]

predictions.jsonl: one JSON line per item, {"valse_id": ..., "boxes": {"<word>": [x1, y1, x2, y2], ...}} with the boxes
in original image pixels (one per participant word; a missing word counts as a miss), optionally "foil_pass": true/false
(the item's caption-foil outcome with the image). Prints the share of items with both participants located by role on
all items, on the balanced stratum of the external text LM and on the gold-verified items, and, when foil_pass is
given, the foil pass rate, P(located | foil passed) and the odds ratio with a Woolf 95% interval.
Needs only the standard library.
"""

from __future__ import annotations

import argparse
import json
import math


def iou(a, b) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / ua if ua > 0 else 0.0


def odds_ratio(a, b, c, d) -> str:
    if min(a, b, c, d) == 0:
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    orr = (a * d) / (b * c)
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return f"{orr:.2f} [{math.exp(math.log(orr) - 1.96 * se):.2f}, {math.exp(math.log(orr) + 1.96 * se):.2f}]"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("predictions")
    ap.add_argument("--items", default="release/swaps.jsonl")
    ap.add_argument("--lm", default="olmo2-7b", help="external text LM whose balanced stratum is reported")
    ap.add_argument("--iou", type=float, default=0.5)
    args = ap.parse_args()
    items = {r["valse_id"]: r for r in map(json.loads, open(args.items, encoding="utf-8"))}
    preds = {r["valse_id"]: r for r in map(json.loads, open(args.predictions, encoding="utf-8")) if r["valse_id"] in items}
    print(f"items {len(items)}, predictions for {len(preds)}")

    def located(vid) -> bool:
        boxes = preds[vid].get("boxes", {})
        return all(w["word"] in boxes and iou(boxes[w["word"]], w["gold_box"]) >= args.iou for w in items[vid]["participants"])

    subsets = {"all items": list(preds)}
    subsets[f"balanced ({args.lm})"] = [v for v in preds if items[v].get("text_lm", {}).get(args.lm, {}).get("stratum") == "balanced"]
    if any("gold_human_confirmed" in items[v]["flags"] for v in preds):
        subsets["gold-verified"] = [v for v in preds if items[v]["flags"].get("gold_human_confirmed")]
    subsets["non-nested pairs"] = [v for v in preds if not items[v]["flags"].get("nested_pair")]
    for name, vids in subsets.items():
        if not vids:
            continue
        loc = [located(v) for v in vids]
        line = f"{name:22s} n={len(vids):4d}  both located by role {100 * sum(loc) / len(vids):5.1f}%"
        fp = [preds[v].get("foil_pass") for v in vids]
        if all(x is not None for x in fp):
            a = sum(1 for p, l in zip(fp, loc) if p and l)
            b = sum(1 for p, l in zip(fp, loc) if p and not l)
            c = sum(1 for p, l in zip(fp, loc) if not p and l)
            d = sum(1 for p, l in zip(fp, loc) if not p and not l)
            line += f"  foil passed {100 * (a + b) / len(vids):5.1f}%  P(located | passed) {100 * a / max(1, a + b):5.1f}%  OR {odds_ratio(a, b, c, d)}"
        print(line)


if __name__ == "__main__":
    main()
