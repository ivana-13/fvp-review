"""Run the foil, blind, verb and pointing probes over a full VALSE subset with one model.

Usage:
    uv run python scripts/run_probes.py --model qwen3vl-2b --subset actant-swap
    uv run python scripts/run_probes.py --model qwen3vl-2b --subset action-replacement --limit 50

Resumable: items already present in the output file are skipped. Output:
    outputs/probes_<model>_<subset>.jsonl   one JSON record per item with raw outputs.

Probes per item
  actant-swap:        yes-prob for caption and foil; order-debiased pairwise; blind pairwise;
                      verb naming; pointing for both swapped actants (role prompt and noun prompt)
  action-replacement: yes-prob, pairwise, blind; pointing for the agent (role prompt and noun prompt)
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from fvp.data import SUBSETS, image_path, set_cache_default  # noqa: E402

set_cache_default()

from PIL import Image  # noqa: E402

from fvp.geometry import box_center, iou, point_in_box  # noqa: E402
from fvp.models import load_model  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"

VERB_PROMPT = "What is the main action happening in this image? Answer with one verb in the -ing form."


def role_phrase(role: str, role_def: str, verb: str) -> str:
    d = role_def.strip().rstrip(".")
    d = d[0].lower() + d[1:] if d else role
    if role == "agent":
        return f"the one who is {verb} (the agent)"
    return d


def pointing_record(model, img, phrase: str, gold: list) -> dict:
    g = model.ground(img, phrase)
    boxes = g.boxes_px
    rec = {
        "prompt": phrase,
        "raw": g.raw,
        "boxes_px": boxes,
        "iou": max((iou(b, gold) for b in boxes), default=0.0),
        "center_hit": any(point_in_box(box_center(b), gold) for b in boxes),
    }
    pts = getattr(g, "points_px", [])
    if pts:  # point-output models (Molmo): a hit is a point inside the gold box, recorded as iou 1/0
        rec["points_px"] = pts
        rec["center_hit"] = any(point_in_box(tuple(p), gold) for p in pts)
        rec["iou"] = 1.0 if rec["center_hit"] else 0.0
    return rec


def foil_record(model, img, caption: str, foil: str, blind: bool = True) -> dict:
    p_cap = model.yes_prob(img, caption)
    p_foil = model.yes_prob(img, foil)
    pair = model.choose_sym(img, caption, foil)
    blind_p = model.choose_sym(None, caption, foil) if blind else None
    return {
        "caption": caption, "foil": foil,
        "p_yes_caption": p_cap, "p_yes_foil": p_foil, "yes_correct": p_cap > p_foil,
        "pair_p_caption": pair, "pair_correct": pair > 0.5,
        "blind_p_caption": blind_p, "blind_correct": (blind_p > 0.5) if blind_p is not None else None,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3vl-2b")
    ap.add_argument("--subset", choices=SUBSETS, default="actant-swap")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-pointing", action="store_true")
    ap.add_argument("--device", default="cuda", help="cuda (default) or cpu (float32, for smoke tests)")
    args = ap.parse_args()

    items = [json.loads(l) for l in open(DATA / "joined" / f"{args.subset}.valid.jsonl", encoding="utf-8")]
    if args.limit:
        items = items[: args.limit]
    OUT.mkdir(exist_ok=True)
    out_path = OUT / f"probes_{args.model}_{args.subset}.jsonl"
    done = set()
    if out_path.exists():
        done = {json.loads(l)["valse_id"] for l in open(out_path, encoding="utf-8")}
    todo = [it for it in items if it["valse_id"] not in done]
    print(f"{args.subset}: {len(items)} items, {len(done)} done, {len(todo)} to run")
    if not todo:
        return

    t0 = time.time()
    kw = {"device": args.device}
    if args.device == "cpu":
        import torch
        kw["dtype"] = torch.float32
    model = load_model(args.model, **kw)
    print(f"model {args.model} loaded in {time.time() - t0:.0f}s")

    with open(out_path, "a", encoding="utf-8") as fout:
        for i, it in enumerate(todo, 1):
            path = image_path(it)
            if not path.exists():
                print("missing image, skipping:", it["image_file"])
                continue
            img = Image.open(path).convert("RGB")
            rec = {"valse_id": it["valse_id"], "image_file": it["image_file"], "verb": it["verb"],
                   "subset": args.subset, "model": args.model}
            can_foil = getattr(model, "supports_foil", True)
            can_point = getattr(model, "supports_pointing", True) and not args.no_pointing
            rec["foil"] = foil_record(model, img, it["caption"], it["foil"]) if can_foil else None
            crop = it.get("crop")
            if crop and can_foil:  # ARO items: the foil test is repeated on the benchmark's union crop (no blind run needed)
                W, H = img.size
                c = (max(0, crop[0]), max(0, crop[1]), min(W, crop[2]), min(H, crop[3]))
                if c[2] - c[0] >= 8 and c[3] - c[1] >= 8:
                    rec["foil_crop"] = foil_record(model, img.crop(c), it["caption"], it["foil"], blind=False)
            if args.subset != "action-replacement":
                if args.subset == "actant-swap" and can_foil:
                    rec["verb_probe"] = {"answer": model.generate(img, VERB_PROMPT, 8), "gold": it["verb"]}
                if can_point:
                    rec["pointing"] = {}
                    for word in [it["classes"], it["classes_foil"]]:
                        tg = it["targets"][word]
                        rec["pointing"][word] = {
                            "role": tg["role"], "gold": tg["bbox"],
                            "role_prompt": pointing_record(model, img, role_phrase(tg["role"], tg["def"], it["verb"]), tg["bbox"]),
                            "noun_prompt": pointing_record(model, img, f"the {word}", tg["bbox"]),
                        }
            else:
                if can_point:
                    tg = it["targets"]["__agent__"]
                    agent_word = it["caption"].split()[1] if len(it["caption"].split()) > 1 else "agent"
                    rec["pointing"] = {"__agent__": {
                        "role": "agent", "gold": tg["bbox"],
                        "role_prompt": pointing_record(model, img, role_phrase("agent", tg["def"], it["verb"]), tg["bbox"]),
                        "noun_prompt": pointing_record(model, img, f"the {agent_word}", tg["bbox"]),
                    }}
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fout.flush()
            if i % 20 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"  {i}/{len(todo)}  {el/ i:.1f}s per item, elapsed {el/60:.1f} min")


if __name__ == "__main__":
    main()
