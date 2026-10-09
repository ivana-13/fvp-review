"""Foil probe for contrastive encoders (SigLIP2, CLIP): caption vs foil by cosine similarity.

Usage:
    uv run python scripts/run_encoder_foils.py --model siglip2-base --subset actant-swap --device cpu
Writes outputs/probes_<model>_<subset>.jsonl with the same 'foil' block layout as run_probes.py
(pair_correct = sim(caption) > sim(foil); no yes-prob, no blind, no pointing).
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from fvp.data import SUBSETS, image_path, set_cache_default  # noqa: E402

set_cache_default()

import torch  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"

ENCODERS = {
    "siglip2-base": "google/siglip2-base-patch16-256",
    "clip-vit-l": "openai/clip-vit-large-patch14",
    "siglip2-so400m": "google/siglip2-so400m-patch14-384",  # larger encoder for the VM
}


class Encoder:
    def __init__(self, model_id: str, device: str):
        from transformers import AutoModel, AutoProcessor

        self.device = device
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModel.from_pretrained(model_id).to(device).eval()
        self.is_siglip = "siglip" in model_id

    @torch.no_grad()
    def sims(self, image: Image.Image, texts: list[str]) -> list[float]:
        kw = {"padding": "max_length", "max_length": 64} if self.is_siglip else {"padding": True}
        inputs = self.processor(images=image, text=texts, return_tensors="pt", truncation=True, **kw).to(self.device)
        out = self.model(**inputs)
        img = out.image_embeds / out.image_embeds.norm(dim=-1, keepdim=True)
        txt = out.text_embeds / out.text_embeds.norm(dim=-1, keepdim=True)
        return (txt @ img.T).squeeze(-1).tolist()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=sorted(ENCODERS), default="siglip2-base")
    ap.add_argument("--subset", choices=SUBSETS, default="actant-swap")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    items = [json.loads(l) for l in open(DATA / "joined" / f"{args.subset}.valid.jsonl", encoding="utf-8")]
    if args.limit:
        items = items[: args.limit]
    OUT.mkdir(exist_ok=True)
    out_path = OUT / f"probes_{args.model}_{args.subset}.jsonl"
    enc = Encoder(ENCODERS[args.model], args.device)
    t0 = time.time()
    correct = 0
    with open(out_path, "w", encoding="utf-8") as fout:
        for i, it in enumerate(items, 1):
            img = Image.open(image_path(it)).convert("RGB")
            s_cap, s_foil = enc.sims(img, [it["caption"], it["foil"]])
            ok = s_cap > s_foil
            correct += ok
            rec = {"valse_id": it["valse_id"], "image_file": it["image_file"], "verb": it["verb"],
                   "subset": args.subset, "model": args.model,
                   "foil": {"caption": it["caption"], "foil": it["foil"], "sim_caption": s_cap, "sim_foil": s_foil,
                            "pair_correct": ok, "yes_correct": ok, "blind_correct": None}}
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if i % 100 == 0:
                print(f"  {i}/{len(items)}  acc so far {correct/i:.3f}  {(time.time()-t0)/i:.2f}s per item")
    print(f"{args.model} {args.subset}: {correct}/{len(items)} = {correct/len(items):.3f}  -> {out_path}")


if __name__ == "__main__":
    main()
