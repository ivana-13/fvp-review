"""Two-box role probe: a recognition test of role binding matched to the foil test's two-way format.

The two gold boxes of an actant-swap item are drawn on the image and labelled A and B; the model is asked which box
contains the role phrase ("the one who is biting (the agent)") and we read P(A) vs P(B) from the next-token logits,
in both labellings (A/B swapped), so letter bias cancels. Chance is 50% per target and 25% for both targets. The same
question with the noun ("the dog") checks that the model can read the labels at all.

    uv run python scripts/run_twobox.py --model qwen3vl-2b [--limit N] [--device cpu]

Writes outputs/twobox_<model>_actant-swap.jsonl (resumable), one record per item with, per target, the order-averaged
probability of the right box for the role phrase and for the noun, and whether the gold pair is nested.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from fvp.data import image_path  # noqa: E402
from fvp.geometry import iou  # noqa: E402
from fvp.models import load_model  # noqa: E402
from run_probes import role_phrase  # noqa: E402

DATA, OUT = ROOT / "data", ROOT / "outputs"
PROMPT = "Two boxes are drawn on the image and labelled A and B. Which box contains {target}? Answer with A or B only."


def nested(ga: list, gb: list) -> bool:
    inter = max(0.0, min(ga[2], gb[2]) - max(ga[0], gb[0])) * max(0.0, min(ga[3], gb[3]) - max(ga[1], gb[1]))
    small = min((ga[2] - ga[0]) * (ga[3] - ga[1]), (gb[2] - gb[0]) * (gb[3] - gb[1]))
    return iou(ga, gb) >= 0.5 or (small > 0 and inter / small >= 0.9)


_font_cache: dict = {}


def draw_labelled(img: Image.Image, boxes: list[list], letters: list[str]) -> Image.Image:
    """Both boxes in the same colour, each with its letter in a filled tag at the top-left corner (inside the box)."""
    out = img.copy()
    d = ImageDraw.Draw(out)
    W, H = out.size
    size = max(22, W // 16)
    if size not in _font_cache:
        try:
            _font_cache[size] = ImageFont.truetype("arialbd.ttf", size)
        except OSError:
            try:
                _font_cache[size] = ImageFont.truetype("DejaVuSans-Bold.ttf", size)
            except OSError:
                _font_cache[size] = ImageFont.load_default()
    font = _font_cache[size]
    lw = max(4, W // 120)
    colour = (230, 30, 30)
    for b, letter in zip(boxes, letters):
        d.rectangle(b, outline=colour, width=lw)
        bb = d.textbbox((0, 0), letter, font=font)
        tw, th = bb[2] - bb[0] + 12, bb[3] - bb[1] + 8
        x0, y0 = min(max(0, b[0] + lw), W - tw), min(max(0, b[1] + lw), H - th)
        d.rectangle([x0, y0, x0 + tw, y0 + th], fill=colour)
        d.text((x0 + 6, y0 + 2), letter, fill="white", font=font)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3vl-2b")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--save-examples", type=int, default=0, help="save the first N labelled images to outputs/twobox_examples/")
    args = ap.parse_args()
    items = [json.loads(l) for l in open(DATA / "joined" / "actant-swap.valid.jsonl", encoding="utf-8")]
    if args.limit:
        items = items[: args.limit]
    OUT.mkdir(exist_ok=True)
    out_path = OUT / f"twobox_{args.model}_actant-swap.jsonl"
    done = {json.loads(l)["valse_id"] for l in open(out_path, encoding="utf-8")} if out_path.exists() else set()
    todo = [it for it in items if it["valse_id"] not in done]
    print(f"two-box {args.model}: {len(items)} items, {len(done)} done, {len(todo)} to run", flush=True)
    if not todo:
        return
    t0 = time.time()
    kw = {"device": args.device}
    if args.device == "cpu":
        import torch
        kw["dtype"] = torch.float32
    model = load_model(args.model, **kw)
    print(f"model {args.model} loaded in {time.time() - t0:.0f}s", flush=True)
    if args.save_examples:
        (OUT / "twobox_examples").mkdir(exist_ok=True)
    t0 = time.time()
    with open(out_path, "a", encoding="utf-8") as fout:
        for i, it in enumerate(todo, 1):
            img = Image.open(image_path(it)).convert("RGB")
            words = [it["classes"], it["classes_foil"]]
            golds = [it["targets"][w]["bbox"] for w in words]
            img_ab = draw_labelled(img, golds, ["A", "B"])   # word 0 = A, word 1 = B
            img_ba = draw_labelled(img, golds, ["B", "A"])   # word 0 = B, word 1 = A
            if args.save_examples and i <= args.save_examples:
                img_ab.save(OUT / "twobox_examples" / f"{Path(it['image_file']).stem}_AB.png")
            rec = {"valse_id": it["valse_id"], "image_file": it["image_file"], "verb": it["verb"], "subset": "actant-swap",
                   "model": args.model, "nested": nested(golds[0], golds[1]), "targets": {}}
            for j, w in enumerate(words):
                tg = it["targets"][w]
                for kind, target in (("role", role_phrase(tg["role"], tg["def"], it["verb"])), ("noun", f"the {w}")):
                    prompt = PROMPT.format(target=target)
                    p_ab = model.choose_ab(img_ab, prompt)            # P(A) when this word is A (j == 0) or B (j == 1)
                    p_ba = model.choose_ab(img_ba, prompt)            # P(A) when this word is B (j == 0) or A (j == 1)
                    p_own = ((p_ab + (1 - p_ba)) / 2) if j == 0 else (((1 - p_ab) + p_ba) / 2)
                    rec["targets"].setdefault(w, {"role": tg["role"], "gold": tg["bbox"]})
                    rec["targets"][w][f"{kind}_prompt"] = target
                    rec["targets"][w][f"p_{kind}"] = p_own
                    rec["targets"][w][f"{kind}_correct"] = p_own > 0.5
            rec["both_role"] = all(t["role_correct"] for t in rec["targets"].values())
            rec["both_noun"] = all(t["noun_correct"] for t in rec["targets"].values())
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fout.flush()
            if i % 25 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"  {i}/{len(todo)}  {el / i:.1f}s per item, elapsed {el / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
