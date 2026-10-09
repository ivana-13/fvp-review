"""Statistics quoted in the appendix paragraph on proprietary models (scripts/run_api.py outputs), for one API tag.

    uv run python scripts/api_stats.py --tag gemini31pro
    uv run python scripts/api_stats.py --tag claudeopus55

Prints, on the 200-item sample: foil pass with the image and blind, the pass rate with the image on the items the blind
choice gets wrong, both participants by noun and by role (IoU >= 0.5), P(loc | pass) on all and on localisable items,
the open models' range of passes without both boxes on the same localisable items, text-only role resolution, the share
of conflict targets that follow the text, centre-in-box both-roles rate, and per-target role and noun hits.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from analyze import HIT, load_jsonl, rescore_control_points  # noqa: E402
from summarize_api import OPEN  # noqa: E402

OUT = ROOT / "outputs"


def pct(k, n):
    return 100 * k / n if n else float("nan")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="claudeopus55")
    args = ap.parse_args()
    recs = [r for r in load_jsonl(OUT / f"probes_{args.tag}_actant-swap.jsonl") if r.get("pointing") and r.get("foil")]
    ids = {r["valse_id"] for r in recs}
    n = len(recs)
    both = lambda r, ph: all(p[ph]["iou"] >= HIT for p in r["pointing"].values())  # noqa: E731
    passed = [r for r in recs if r["foil"]["pair_correct"]]
    blind_wrong = [r for r in recs if not r["foil"]["blind_correct"]]
    loc = [r for r in passed if both(r, "noun_prompt")]
    targets = [p for r in recs for p in r["pointing"].values()]
    # center_hit is set at finalisation from the reading chosen for the model (Gemini-style box_2d or xyxy)
    centre_both = [all(p["role_prompt"]["center_hit"] for p in r["pointing"].values()) for r in recs]
    print(f"{args.tag}: n={n}")
    print(f"  foil pass with image {pct(len(passed), n):.1f}  blind {pct(sum(r['foil']['blind_correct'] for r in recs), n):.1f}  "
          f"yes/no {pct(sum(r['foil']['yes_correct'] for r in recs), n):.1f}")
    print(f"  blind wrong on {len(blind_wrong)} items; image pass among them {pct(sum(r['foil']['pair_correct'] for r in blind_wrong), len(blind_wrong)):.1f}")
    print(f"  both by noun {pct(sum(both(r, 'noun_prompt') for r in recs), n):.1f}  both by role {pct(sum(both(r, 'role_prompt') for r in recs), n):.1f}")
    print(f"  P(loc|pass) all {pct(sum(both(r, 'role_prompt') for r in passed), len(passed)):.1f}  localisable {pct(sum(both(r, 'role_prompt') for r in loc), len(loc)):.1f} (n loc {len(loc)})")
    print(f"  per-target role hit {pct(sum(p['role_prompt']['iou'] >= HIT for p in targets), len(targets)):.1f}  noun hit {pct(sum(p['noun_prompt']['iou'] >= HIT for p in targets), len(targets)):.1f}")
    print(f"  centre-in-box both roles {pct(sum(centre_both), n):.1f}  per-target role {pct(sum(p['role_prompt']['center_hit'] for p in targets), len(targets)):.1f}")
    ctl_p = OUT / f"controls_{args.tag}_actant-swap.jsonl"
    if ctl_p.exists():
        ctl = [c for c in load_jsonl(ctl_p) if c["valse_id"] in ids]
        rescore_control_points(ctl, "actant-swap")
        words = [d for c in ctl for d in c["words"].values()]
        conf = [d["conflict"]["class"] for d in words if d["conflict"].get("class")]
        print(f"  text-only role resolution {pct(sum(d['text_resolution']['correct'] for d in words), len(words)):.1f}  "
              f"conflict follows text {pct(conf.count('text'), len(conf)):.1f}  image {pct(conf.count('image'), len(conf)):.1f}")
    # open models on the same localisable items: passes without both boxes
    rng = []
    for key, name in OPEN:
        orec = [r for r in load_jsonl(OUT / f"probes_{key}_actant-swap.jsonl") if r["valse_id"] in ids and r.get("pointing") and r.get("foil")]
        if not orec:
            continue
        op = [r for r in orec if r["foil"]["pair_correct"] and both(r, "noun_prompt")]
        rng.append((name, 100 - pct(sum(both(r, "role_prompt") for r in op), len(op))))
    if rng:
        print("  open models, passes without both boxes on localisable items: " + ", ".join(f"{nm} {v:.1f}" for nm, v in rng))
        print(f"  range {min(v for _, v in rng):.0f} to {max(v for _, v in rng):.0f}")


if __name__ == "__main__":
    main()
