"""Join VALSE action items with SWiG role boxes and pick a trial sample.

Usage:
    uv run python scripts/prepare_valse_swig.py --sample 10 --seed 0

Writes data/joined/{actant-swap,action-replacement}.jsonl and data/trial_sample.jsonl,
and prints coverage statistics (how many items have both swapped words mapped to
grounded, distinct SWiG roles).
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path

from fvp.swig import SwigSpace, join_valse_with_swig, load_swig_annotations, mturk_valid

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def both_targets_grounded(item) -> bool:
    words = [item.classes, item.classes_foil]
    tg = [item.targets.get(w) for w in words]
    if any(t is None for t in tg):
        return False
    if any(not _valid(t["bbox"]) for t in tg):
        return False
    return tg[0]["role"] != tg[1]["role"]


def _valid(box) -> bool:
    return box is not None and len(box) == 4 and all(v >= 0 for v in box) and box[2] > box[0] and box[3] > box[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=10)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--min-caption-votes", type=int, default=2)
    args = ap.parse_args()

    space = SwigSpace.load(DATA / "swig" / "imsitu_space.json")
    swig = load_swig_annotations(DATA / "swig")
    print(f"SWiG images loaded: {len(swig)}")

    (DATA / "joined").mkdir(exist_ok=True)
    joined = {}
    for subset in ["actant-swap", "action-replacement"]:
        items = join_valse_with_swig(DATA / "valse" / f"{subset}.json", subset, swig, space)
        joined[subset] = items
        with open(DATA / "joined" / f"{subset}.jsonl", "w", encoding="utf-8") as f:
            for it in items:
                f.write(json.dumps(it.to_json(), ensure_ascii=False) + "\n")
        n = len(items)
        n_valid = sum(mturk_valid(it, args.min_caption_votes) for it in items)
        print(f"\n[{subset}] items joined to SWiG: {n}  | mturk caption>={args.min_caption_votes}: {n_valid}")
        if subset == "actant-swap":
            mapped = sum(all(w in it.targets for w in [it.classes, it.classes_foil]) for it in items)
            grounded = sum(both_targets_grounded(it) for it in items)
            grounded_valid = sum(both_targets_grounded(it) and mturk_valid(it, args.min_caption_votes) for it in items)
            print(f"  both swapped words mapped to a role: {mapped}")
            print(f"  both mapped roles grounded and distinct: {grounded}")
            print(f"  ... and mturk-valid: {grounded_valid}")
            role_pairs = Counter(
                tuple(sorted([it.targets[it.classes]["role"], it.targets[it.classes_foil]["role"]]))
                for it in items if both_targets_grounded(it)
            )
            print("  most common role pairs:", role_pairs.most_common(8))
        else:
            agent_grounded = sum(_valid(it.targets.get("__agent__", {}).get("bbox")) for it in items)
            print(f"  agent box grounded: {agent_grounded}")

    # Trial sample: actant-swap items that are mturk-valid, both targets grounded and distinct,
    # and whose image also has an action-replacement item (so both foil types share the image).
    by_image_ar = {}
    for it in joined["action-replacement"]:
        if mturk_valid(it, args.min_caption_votes):
            by_image_ar.setdefault(it.image_file, it)
    pool = [
        it for it in joined["actant-swap"]
        if mturk_valid(it, args.min_caption_votes) and both_targets_grounded(it) and it.image_file in by_image_ar
    ]
    print(f"\nTrial pool (actant-swap with paired action-replacement on same image): {len(pool)}")
    rng = random.Random(args.seed)
    rng.shuffle(pool)
    sample = pool[: args.sample]
    with open(DATA / "trial_sample.jsonl", "w", encoding="utf-8") as f:
        for it in sample:
            rec = it.to_json()
            rec["action_replacement"] = by_image_ar[it.image_file].to_json()
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Wrote {len(sample)} items to data/trial_sample.jsonl")
    for it in sample:
        t1, t2 = it.targets[it.classes], it.targets[it.classes_foil]
        print(f"  {it.image_file:28s} verb={it.verb:12s} '{it.caption}' | foil: '{it.foil}'")
        print(f"      {it.classes} -> {t1['role']} {t1['bbox']} | {it.classes_foil} -> {t2['role']} {t2['bbox']}")


if __name__ == "__main__":
    main()
