"""Score human role-pointing annotations against the SWiG boxes and against the models on the same targets.

    uv run python scripts/score_annotations.py annotation/human_ceiling_annotations.json [--second other.json]

Prints the human hit rate (IoU >= 0.5 and centre-in-box) per role group, the share of 'cannot tell' answers, the
agreement with a second annotator's file when given, and the models' role-prompt hit rates on exactly the same targets.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fvp.geometry import box_center, iou, point_in_box  # noqa: E402

MODELS = ["qwen3vl-2b", "qwen3vl-4b", "qwen3vl-8b", "qwen3vl-32b", "qwen3vl-235b", "internvl35-2b", "internvl35-8b", "molmo-7b-d", "paligemma2-10b"]


def load_ann(path: Path) -> dict:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return d.get("annotations", d)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--second", default=None)
    ap.add_argument("--targets", default="annotation/human_ceiling_targets.json")
    args = ap.parse_args()
    targets = {t["id"]: t for t in json.loads((ROOT / args.targets).read_text(encoding="utf-8"))}
    ann = load_ann(ROOT / args.file)
    done = {k: v for k, v in ann.items() if k in targets}
    answered = {k: v for k, v in done.items() if v.get("box")}
    print(f"targets {len(targets)}, annotated {len(done)}, with a box {len(answered)}, cannot tell {len(done) - len(answered)}")
    for group, keys in (("all", list(answered)), ("agent", [k for k in answered if targets[k]["role"] == "agent"]),
                        ("other", [k for k in answered if targets[k]["role"] != "agent"])):
        if not keys:
            continue
        hit = sum(iou(answered[k]["box"], targets[k]["gold"]) >= 0.5 for k in keys)
        cen = sum(point_in_box(box_center(answered[k]["box"]), targets[k]["gold"]) for k in keys)
        print(f"  human {group:5s}: IoU>=0.5 {100 * hit / len(keys):.1f}%  centre-in-box {100 * cen / len(keys):.1f}%  (n={len(keys)})")
    if args.second:
        ann2 = load_ann(ROOT / args.second)
        both = [k for k in answered if ann2.get(k, {}).get("box")]
        if both:
            agree = sum(iou(answered[k]["box"], ann2[k]["box"]) >= 0.5 for k in both)
            print(f"  two annotators agree (IoU>=0.5) on {100 * agree / len(both):.1f}% of {len(both)} shared targets")
    # models on the same targets
    by_item: dict[str, dict] = {}
    for k in done:
        vid, word = k.split("::")
        by_item.setdefault(vid, {})[word] = k
    for m in MODELS:
        p = ROOT / "outputs" / f"probes_{m}_actant-swap.jsonl"
        if not p.exists():
            continue
        hits, n = 0, 0
        for line in open(p, encoding="utf-8"):
            r = json.loads(line)
            for word, k in by_item.get(r["valse_id"], {}).items():
                if word in r.get("pointing", {}):
                    hits += r["pointing"][word]["role_prompt"]["iou"] >= 0.5; n += 1
        if n:
            print(f"  {m:16s} role-prompt hits on the same {n} targets: {100 * hits / n:.1f}%")


if __name__ == "__main__":
    main()
