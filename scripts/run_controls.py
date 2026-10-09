"""Two controls that separate linguistic from visual role binding (actant-swap items).

1. Text-only role resolution: given the caption alone, "who or what is <role phrase>?"
   If the model names the right noun from text, then a pointing failure is not a parsing failure.
2. Caption-conditioned and conflict pointing: the pointing prompt is preceded by
   'The image shows: "<caption>"' (conditioned) or 'The image shows: "<foil>"' (conflict).
   Under the foil, the role phrase maps textually to the OTHER participant. We record IoU with the
   true gold box (image-consistent) and with the other participant's box (text-following).

Usage:
    uv run python scripts/run_controls.py --model qwen3vl-2b [--limit N] [--device cpu]
Resumable. Output: outputs/controls_<model>_actant-swap.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

from fvp.data import SUBSETS, image_path, set_cache_default  # noqa: E402

set_cache_default()

from PIL import Image  # noqa: E402

from fvp.geometry import iou, point_in_box  # noqa: E402
from fvp.models import load_model  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
sys.path.insert(0, str(ROOT / "scripts"))
from run_probes import role_phrase  # noqa: E402

HIT = 0.5


def word_forms(w: str) -> set[str]:
    w = w.lower().strip()
    forms = {w}
    if w.endswith("s"):
        forms.add(w[:-1])
    forms.add(w + "s")
    forms |= {t for t in w.split() if len(t) > 2}  # multi-word: "male child" -> child, male
    return forms


def mentions(answer: str, word: str) -> bool:
    a = re.sub(r"[^a-z ]", " ", answer.lower())
    toks = set(a.split())
    return bool(word_forms(word) & toks) or word.lower() in a


def score_ground(g, gold: list, gold_other: list) -> dict:
    """IoU with the target's and the other participant's gold box; for point-output models (Molmo) a point inside
    the box, recorded as iou 1.0/0.0 as in scripts/run_probes.py."""
    rec = {"raw": g.raw, "boxes_px": g.boxes_px,
           "iou_gold": max((iou(b, gold) for b in g.boxes_px), default=0.0),
           "iou_other": max((iou(b, gold_other) for b in g.boxes_px), default=0.0)}
    pts = getattr(g, "points_px", [])
    if pts:
        rec["points_px"] = pts
        rec["iou_gold"] = float(any(point_in_box(tuple(p), gold) for p in pts))
        rec["iou_other"] = float(any(point_in_box(tuple(p), gold_other) for p in pts))
    return rec


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
    out_path = OUT / f"controls_{args.model}_{args.subset}.jsonl"
    done = {json.loads(l)["valse_id"] for l in open(out_path, encoding="utf-8")} if out_path.exists() else set()
    todo = [it for it in items if it["valse_id"] not in done]
    print(f"controls {args.model} {args.subset}: {len(items)} items, {len(done)} done, {len(todo)} to run")
    if not todo:
        return
    t0 = time.time()
    kw = {"device": args.device}
    if args.device == "cpu":
        import torch
        kw["dtype"] = torch.float32
    model = load_model(args.model, **kw)
    print(f"loaded in {time.time() - t0:.0f}s")

    with open(out_path, "a", encoding="utf-8") as fout:
        for i, it in enumerate(todo, 1):
            img = Image.open(image_path(it)).convert("RGB")
            words = [it["classes"], it["classes_foil"]]
            rec = {"valse_id": it["valse_id"], "image_file": it["image_file"], "verb": it["verb"],
                   "subset": args.subset, "model": args.model, "caption": it["caption"], "foil": it["foil"], "words": {}}
            for j, w in enumerate(words):
                other = words[1 - j]
                tg = it["targets"][w]
                gold, gold_other = tg["bbox"], it["targets"][other]["bbox"]
                phrase = role_phrase(tg["role"], tg["def"], it["verb"])
                # 1. text-only role resolution
                q = (f"Caption: \"{it['caption']}\"\nAccording to this caption only, who or what is {phrase}? "
                     "Answer with the noun phrase from the caption, nothing else.")
                ans = model.generate(None, q, 12)
                m_t, m_o = mentions(ans, w), mentions(ans, other)
                text_res = {"answer": ans, "mentions_target": m_t, "mentions_other": m_o, "correct": m_t and not m_o}
                # 2a. caption-conditioned pointing
                g_c = model.ground(img, phrase, context=f"The image shows: \"{it['caption']}\".")
                cond = score_ground(g_c, gold, gold_other)
                cond["hit"] = cond["iou_gold"] >= HIT
                # 2b. conflict pointing (foil caption: the role phrase now textually names the other word)
                g_f = model.ground(img, phrase, context=f"The image shows: \"{it['foil']}\".")
                conf = score_ground(g_f, gold, gold_other)
                if conf["iou_gold"] >= HIT and conf["iou_other"] < HIT:
                    conf["class"] = "image"
                elif conf["iou_other"] >= HIT and conf["iou_gold"] < HIT:
                    conf["class"] = "text"
                elif conf["iou_gold"] >= HIT and conf["iou_other"] >= HIT:
                    conf["class"] = "both"
                else:
                    conf["class"] = "neither"
                rec["words"][w] = {"role": tg["role"], "phrase": phrase, "gold": gold, "gold_other": gold_other,
                                   "text_resolution": text_res, "conditioned": cond, "conflict": conf}
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fout.flush()
            if i % 20 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"  {i}/{len(todo)}  {el / i:.1f}s per item, elapsed {el / 60:.1f} min")


if __name__ == "__main__":
    main()
