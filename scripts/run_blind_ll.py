"""Likelihood-based blind baseline: log P(caption) vs log P(foil) under the model's language model, no image.

Unlike the A/B blind choice, this does not depend on instruction following and is the standard
text-only baseline for compositional benchmarks. An item is 'blind-solvable' when the caption is
more likely than the foil; the margin (nats) says how strongly.

Usage:
    uv run python scripts/run_blind_ll.py --model qwen3vl-2b --subset actant-swap
Output: outputs/blindll_<model>_<subset>.jsonl   (valse_id, ll_caption, ll_foil, margin, blind_ll_correct)
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from fvp.data import SUBSETS, set_cache_default  # noqa: E402

set_cache_default()

import torch  # noqa: E402

from fvp.models import load_model  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"


@torch.no_grad()
def sentence_logprob(model, text: str) -> float:
    """Sum of token log-probabilities of `text` as a plain continuation of a neutral prefix, no chat template."""
    tok = model.tok
    prefix = "Caption: "
    ids_prefix = tok.encode(prefix, add_special_tokens=False)
    ids_text = tok.encode(text, add_special_tokens=False)
    ids = torch.tensor([ids_prefix + ids_text], device=model.device)
    logits = model.model(input_ids=ids).logits[0].float()
    logp = torch.log_softmax(logits[:-1], dim=-1)
    targets = ids[0, 1:]
    tok_lp = logp.gather(1, targets.unsqueeze(1)).squeeze(1)
    return tok_lp[len(ids_prefix) - 1:].sum().item()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3vl-2b")
    ap.add_argument("--subset", choices=SUBSETS, default="actant-swap")
    args = ap.parse_args()
    items = [json.loads(l) for l in open(DATA / "joined" / f"{args.subset}.valid.jsonl", encoding="utf-8")]
    OUT.mkdir(exist_ok=True)
    out_path = OUT / f"blindll_{args.model}_{args.subset}.jsonl"
    done = {json.loads(l)["valse_id"] for l in open(out_path, encoding="utf-8")} if out_path.exists() else set()
    todo = [it for it in items if it["valse_id"] not in done]
    print(f"blind-LL {args.model} {args.subset}: {len(todo)} to run")
    if not todo:
        return
    t0 = time.time()
    model = load_model(args.model)
    if not getattr(model, "supports_foil", True):
        print("pointing-only model: no likelihood baseline")
        return
    correct = 0
    with open(out_path, "a", encoding="utf-8") as fout:
        for i, it in enumerate(todo, 1):
            lc, lf = sentence_logprob(model, it["caption"]), sentence_logprob(model, it["foil"])
            ok = lc > lf
            correct += ok
            fout.write(json.dumps({"valse_id": it["valse_id"], "image_file": it["image_file"], "subset": args.subset,
                                   "model": args.model, "caption": it["caption"], "foil": it["foil"],
                                   "ll_caption": lc, "ll_foil": lf, "margin": lc - lf, "blind_ll_correct": ok}) + "\n")
            if i % 100 == 0:
                print(f"  {i}/{len(todo)}  blind-LL acc {correct / i:.3f}  {(time.time() - t0) / i:.2f}s/item")
    print(f"{args.model} {args.subset}: blind-LL accuracy {correct}/{len(todo)} = {correct / len(todo):.3f}")


if __name__ == "__main__":
    main()
