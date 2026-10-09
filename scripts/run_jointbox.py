"""Joint-box control: both role phrases in one prompt, no captions, no judgement.

The structured verification (scripts/run_verify.py) locates both participants far more often than the separate role
prompts do, but it shows the captions, so the gain could come from the nouns being in view or from the two boxes
being assigned together. This probe asks for the two boxes in one JSON answer with the role phrases only, so the
difference to the separate probe isolates joint assignment, and the difference to the structured probe isolates the
captions.

Usage:
    uv run python scripts/run_jointbox.py --model qwen3vl-2b [--subset actant-swap] [--limit N] [--device cpu]
Resumable. Output: outputs/jointbox_<model>_<subset>.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from fvp.data import SUBSETS, image_path, set_cache_default  # noqa: E402

set_cache_default()

from PIL import Image  # noqa: E402

from fvp.geometry import iou, normalized_1000_to_abs  # noqa: E402
from fvp.models import load_model  # noqa: E402
from fvp.verify import jointbox_prompt, parse_verify  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
sys.path.insert(0, str(ROOT / "scripts"))
from run_probes import role_phrase  # noqa: E402

HIT = 0.5


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3vl-2b")
    ap.add_argument("--subset", choices=SUBSETS, default="actant-swap")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    items = [json.loads(l) for l in open(DATA / "joined" / f"{args.subset}.valid.jsonl", encoding="utf-8")]
    if args.limit:
        items = items[: args.limit]
    OUT.mkdir(exist_ok=True)
    out_path = OUT / f"jointbox_{args.model}_{args.subset}.jsonl"
    done = {json.loads(l)["valse_id"] for l in open(out_path, encoding="utf-8")} if out_path.exists() else set()
    todo = [it for it in items if it["valse_id"] not in done]
    print(f"jointbox {args.model} {args.subset}: {len(items)} items, {len(done)} done, {len(todo)} to run")
    if not todo:
        return
    t0 = time.time()
    kw = {"device": args.device}
    if args.device == "cpu":
        import torch
        kw["dtype"] = torch.float32
    model = load_model(args.model, **kw)
    if getattr(model, "supports_points", False) or not getattr(model, "supports_pointing", True):
        print("joint-box control needs a box-output model; not applicable to", args.model)
        return
    grid = model.coord_convention == "norm1000"
    print(f"loaded in {time.time() - t0:.0f}s")

    with open(out_path, "a", encoding="utf-8") as fout:
        for i, it in enumerate(todo, 1):
            img = Image.open(image_path(it)).convert("RGB")
            W, H = img.size
            words = [it["classes"], it["classes_foil"]]
            roles = [(it["targets"][w]["role"], role_phrase(it["targets"][w]["role"], it["targets"][w]["def"], it["verb"])) for w in words]
            gold = {it["targets"][w]["role"]: it["targets"][w]["bbox"] for w in words}
            raw = model.generate(img, jointbox_prompt(roles), 160)
            parsed = parse_verify(raw, [r for r, _ in roles])
            boxes = {}
            for r, box in parsed["boxes"].items():
                if box is None:
                    boxes[r] = {"box_px": None, "iou": 0.0}
                else:
                    bp = normalized_1000_to_abs(box, (W, H)) if grid else list(box)
                    boxes[r] = {"box_px": bp, "iou": iou(bp, gold[r])}
            rec = {"valse_id": it["valse_id"], "image_file": it["image_file"], "verb": it["verb"], "subset": args.subset,
                   "model": args.model, "raw": raw,
                   "words": {w: {"role": it["targets"][w]["role"], "gold": it["targets"][w]["bbox"]} for w in words},
                   "boxes": boxes,
                   "both_hit": len(boxes) == 2 and all(v["iou"] >= HIT for v in boxes.values()),
                   "hits": {r: v["iou"] >= HIT for r, v in boxes.items()}}
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fout.flush()
            if i % 20 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"  {i}/{len(todo)}  {el / i:.1f}s per item, elapsed {el / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
