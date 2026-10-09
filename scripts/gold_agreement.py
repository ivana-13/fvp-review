"""Agreement between two annotators on the detector-flagged gold items.

    uv run python scripts/gold_agreement.py outputs/gold_flagged.csv annotation/gold_flagged_annotator2.csv

Both files have one row per flagged word (columns sheet, tile, valse_id, image_file, caption, word, role, flag,
iou_own, iou_other, verdict); the verdict judges the red detector box of that word: ok = on the right participant,
swapped = on the other participant of the pair, other = anything else. Prints the row-level agreement on the verdict
with Cohen's kappa and the confusion table, and the item-level agreement on whether the SWiG boxes count as confirmed
under the rule of scripts/make_paper_assets.py (every word's verdict matches its detector flag: ok on an ok flag,
swapped on a swapped flag).
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

LABELS = ("ok", "swapped", "other")


def read(path: str) -> dict[tuple[str, str], dict]:
    rows = {}
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        v = (r.get("verdict") or "").strip().lower()
        r["verdict"] = {"o": "ok", "s": "swapped", "sw": "swapped", "x": "other"}.get(v, v)
        rows[(r["valse_id"], r["word"])] = r
    return rows


def kappa(pairs: list[tuple[str, str]]) -> float:
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[l] * cb[l] for l in set(ca) | set(cb)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def confirmed(rows: dict, by_item: dict[str, list[tuple[str, str]]]) -> set[str]:
    return {vid for vid, fv in by_item.items() if all(p in {("ok", "ok"), ("swapped", "swapped")} for p in fv)}


def main() -> None:
    a, b = read(sys.argv[1]), read(sys.argv[2])
    keys = sorted(k for k in a if k in b and a[k]["verdict"] and b[k]["verdict"])
    missing = [k for k in a if k not in b], [k for k in a if k in b and not b[k]["verdict"]]
    print(f"rows compared: {len(keys)} of {len(a)} (not in second file: {len(missing[0])}, no verdict in second file: {len(missing[1])})")
    pairs = [(a[k]["verdict"], b[k]["verdict"]) for k in keys]
    print(f"row-level agreement on the verdict: {100 * sum(x == y for x, y in pairs) / len(pairs):.1f}%, Cohen's kappa {kappa(pairs):.2f}")
    print("confusion (rows = annotator 1, columns = annotator 2):")
    conf = Counter(pairs)
    print("           " + "".join(f"{l:>9s}" for l in LABELS))
    for l1 in LABELS:
        print(f"{l1:>10s} " + "".join(f"{conf[(l1, l2)]:9d}" for l2 in LABELS))
    for flag in ("ok", "swapped", "mismatch"):
        sub = [(a[k]["verdict"], b[k]["verdict"]) for k in keys if a[k]["flag"] == flag]
        if sub:
            print(f"  flag {flag:>8s}: {len(sub)} rows, agreement {100 * sum(x == y for x, y in sub) / len(sub):.1f}%")
    items_a: dict[str, list] = {}
    items_b: dict[str, list] = {}
    for k in keys:
        items_a.setdefault(k[0], []).append((a[k]["flag"], a[k]["verdict"]))
        items_b.setdefault(k[0], []).append((b[k]["flag"], b[k]["verdict"]))
    complete = {vid for vid in items_a if len(items_a[vid]) == sum(1 for kk in a if kk[0] == vid)}
    ca, cb = confirmed(a, items_a) & complete, confirmed(b, items_b) & complete
    ipairs = [(vid in ca, vid in cb) for vid in sorted(complete)]
    print(f"items with every row judged by both: {len(complete)}; confirmed by annotator 1: {len(ca)}, by annotator 2: {len(cb)}, "
          f"by both: {len(ca & cb)}, by neither: {sum(1 for x, y in ipairs if not x and not y)}")
    print(f"item-level agreement on 'confirmed': {100 * sum(x == y for x, y in ipairs) / len(ipairs):.1f}%, "
          f"kappa {kappa([(str(x), str(y)) for x, y in ipairs]):.2f}")


if __name__ == "__main__":
    main()
