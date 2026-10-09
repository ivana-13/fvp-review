"""Structured verification probe (RQ5): locate both participants by role, then judge the captions, in one answer.

For each actant-swap item the model sees the image and both captions (as A and B), is told to first give a bounding
box for each of the two role phrases used in the pointing probe, and then to say which caption is correct, all in one
JSON object. Each item is run twice with the caption order swapped. We record the boxes (IoU with the gold role
boxes) and the answer under both orders, so the foil decision can be crossed with the localisation made in the same
response.

Usage:
    uv run python scripts/run_verify.py --model qwen3vl-2b [--limit N] [--device cpu]
Resumable. Output: outputs/verify_<model>_actant-swap.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from fvp.data import SUBSETS, image_path, set_cache_default  # noqa: E402

set_cache_default()

from PIL import Image  # noqa: E402

from fvp.geometry import iou, normalized_1000_to_abs  # noqa: E402
from fvp.models import load_model  # noqa: E402
from fvp.verify import parse_verify, verify_prompt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
sys.path.insert(0, str(ROOT / "scripts"))
from run_probes import role_phrase  # noqa: E402

HIT = 0.5
MAX_NEW_TOKENS = 200


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3vl-2b")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--subset", choices=SUBSETS, default="actant-swap")
    args = ap.parse_args()

    items = [json.loads(l) for l in open(DATA / "joined" / f"{args.subset}.valid.jsonl", encoding="utf-8")]
    if args.limit:
        items = items[: args.limit]
    OUT.mkdir(exist_ok=True)
    out_path = OUT / f"verify_{args.model}_{args.subset}.jsonl"
    done = {json.loads(l)["valse_id"] for l in open(out_path, encoding="utf-8")} if out_path.exists() else set()
    todo = [it for it in items if it["valse_id"] not in done]
    print(f"verify {args.model}: {len(items)} items, {len(done)} done, {len(todo)} to run")
    if not todo:
        return
    t0 = time.time()
    kw = {"device": args.device}
    if args.device == "cpu":
        import torch
        kw["dtype"] = torch.float32
    model = load_model(args.model, **kw)
    if getattr(model, "supports_points", False) or not getattr(model, "supports_foil", True):
        print("structured verification needs a box-and-chat model; not applicable to", args.model)
        return
    grid = model.coord_convention == "norm1000"  # otherwise the model answers in pixels
    print(f"loaded in {time.time() - t0:.0f}s")

    with open(out_path, "a", encoding="utf-8") as fout:
        for i, it in enumerate(todo, 1):
            img = Image.open(image_path(it)).convert("RGB")
            W, H = img.size
            words = [it["classes"], it["classes_foil"]]
            roles = [(it["targets"][w]["role"], role_phrase(it["targets"][w]["role"], it["targets"][w]["def"], it["verb"])) for w in words]
            gold = {it["targets"][w]["role"]: it["targets"][w]["bbox"] for w in words}
            rec = {"valse_id": it["valse_id"], "image_file": it["image_file"], "verb": it["verb"], "subset": args.subset,
                   "model": args.model, "caption": it["caption"], "foil": it["foil"],
                   "words": {w: {"role": it["targets"][w]["role"], "gold": it["targets"][w]["bbox"]} for w in words},
                   "orders": {}}
            for order, (a, b) in [("cap_first", (it["caption"], it["foil"])), ("foil_first", (it["foil"], it["caption"]))]:
                raw = model.generate(img, verify_prompt(a, b, roles), MAX_NEW_TOKENS)
                parsed = parse_verify(raw, [r for r, _ in roles])
                chose = None if parsed["answer"] is None else parsed["answer"] == ("A" if order == "cap_first" else "B")
                boxes = {}
                for r, box in parsed["boxes"].items():
                    if box is None:
                        boxes[r] = {"box_px": None, "iou": 0.0}
                    else:
                        bp = normalized_1000_to_abs(box, (W, H)) if grid else list(box)
                        boxes[r] = {"box_px": bp, "iou": iou(bp, gold[r])}
                rec["orders"][order] = {"raw": raw, "answer": parsed["answer"], "chose_caption": chose, "boxes": boxes}
            o1, o2 = rec["orders"]["cap_first"], rec["orders"]["foil_first"]
            rec["first_correct"] = bool(o1["chose_caption"])
            rec["strict_correct"] = bool(o1["chose_caption"]) and bool(o2["chose_caption"])
            rec["either_correct"] = bool(o1["chose_caption"]) or bool(o2["chose_caption"])
            rec["consistent"] = o1["chose_caption"] is not None and o1["chose_caption"] == o2["chose_caption"]
            rec["parsed"] = o1["answer"] is not None and o2["answer"] is not None
            rec["both_hit_first"] = len(o1["boxes"]) == 2 and all(v["iou"] >= HIT for v in o1["boxes"].values())
            rec["both_hit_either"] = rec["both_hit_first"] or (
                len(o2["boxes"]) == 2 and all(v["iou"] >= HIT for v in o2["boxes"].values()))
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fout.flush()
            if i % 20 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"  {i}/{len(todo)}  {el / i:.1f}s per item, elapsed {el / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
