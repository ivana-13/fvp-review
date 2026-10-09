"""Blind likelihood with an external text-only language model.

Reviewer check: is the text-only solvability of the foils idiosyncratic to the VLMs' own language models? The same
score as scripts/run_blind_ll.py (sum of token log-probabilities of the sentence as a plain continuation of
"Caption: ", no chat template; a BOS token is prepended when the tokenizer has one) from a language model that shares
no backbone with the VLMs in the paper.

    uv run python scripts/run_text_ll.py --lm olmo2-7b [--subsets actant-swap action-replacement aro-relation aro-spatial]

Writes outputs/blindll_<lm>_<subset>.jsonl in the blind-LL format (valse_id, caption, foil, ll_caption, ll_foil, margin,
blind_ll_correct) plus the token counts n_caption / n_foil, and outputs/tokens_<lm>.jsonl, so analyze.blindll_stats and
the per-token margin work unchanged. Resumable: items already in the output file are skipped.

    olmo2-7b     allenai/OLMo-2-1124-7B     Apache 2.0, open training data; no Qwen or Gemma backbone
    mistral-7b   mistralai/Mistral-7B-v0.3  Apache 2.0
    llama31-8b   meta-llama/Llama-3.1-8B    gated
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fvp.data import SUBSETS, set_cache_default  # noqa: E402

set_cache_default()

import torch  # noqa: E402

DATA, OUT = ROOT / "data", ROOT / "outputs"
LMS = {"olmo2-7b": "allenai/OLMo-2-1124-7B", "mistral-7b": "mistralai/Mistral-7B-v0.3", "llama31-8b": "meta-llama/Llama-3.1-8B"}


@torch.no_grad()
def sentence_logprob(model, tok, text: str, device) -> tuple[float, int]:
    """Sum of token log-probabilities of `text` after the prefix, and its token count."""
    prefix = ([tok.bos_token_id] if tok.bos_token_id is not None else []) + tok.encode("Caption: ", add_special_tokens=False)
    ids_text = tok.encode(text, add_special_tokens=False)
    ids = torch.tensor([prefix + ids_text], device=device)
    logits = model(input_ids=ids).logits[0].float()
    logp = torch.log_softmax(logits[:-1], dim=-1)
    tok_lp = logp.gather(1, ids[0, 1:].unsqueeze(1)).squeeze(1)
    return tok_lp[len(prefix) - 1:].sum().item(), len(ids_text)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lm", default="olmo2-7b", choices=sorted(LMS))
    ap.add_argument("--subsets", nargs="*", default=SUBSETS)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(LMS[args.lm])
    model = AutoModelForCausalLM.from_pretrained(LMS[args.lm], torch_dtype=torch.bfloat16, device_map="auto").eval()
    device = next(model.parameters()).device
    OUT.mkdir(exist_ok=True)
    token_lines = []
    for subset in args.subsets:
        items = [json.loads(l) for l in open(DATA / "joined" / f"{subset}.valid.jsonl", encoding="utf-8")]
        if args.limit:
            items = items[: args.limit]
        out = OUT / f"blindll_{args.lm}_{subset}.jsonl"
        done = {json.loads(l)["valse_id"] for l in open(out, encoding="utf-8")} if out.exists() else set()
        todo = [it for it in items if it["valse_id"] not in done]
        print(f"text-LL {args.lm} {subset}: {len(todo)} to run ({len(done)} done)")
        t0, correct = time.time(), 0
        with open(out, "a", encoding="utf-8") as f:
            for i, it in enumerate(todo, 1):
                lc, nc = sentence_logprob(model, tok, it["caption"], device)
                lf, nf = sentence_logprob(model, tok, it["foil"], device)
                ok = lc > lf
                correct += ok
                f.write(json.dumps({"valse_id": it["valse_id"], "image_file": it["image_file"], "subset": subset, "model": args.lm,
                                    "caption": it["caption"], "foil": it["foil"], "ll_caption": lc, "ll_foil": lf,
                                    "margin": lc - lf, "blind_ll_correct": ok, "n_caption": nc, "n_foil": nf}) + "\n")
                if i % 200 == 0:
                    print(f"  {i}/{len(todo)}  acc {correct / i:.3f}  {(time.time() - t0) / i:.2f}s/item", flush=True)
        for line in open(out, encoding="utf-8"):
            r = json.loads(line)
            token_lines.append({"valse_id": r["valse_id"], "subset": subset, "n_caption": r["n_caption"], "n_foil": r["n_foil"]})
        n_all = sum(1 for _ in open(out, encoding="utf-8"))
        acc = sum(json.loads(l)["blind_ll_correct"] for l in open(out, encoding="utf-8")) / n_all
        print(f"{args.lm} {subset}: caption more likely on {acc:.3f} of {n_all}")
    (OUT / f"tokens_{args.lm}.jsonl").write_text("".join(json.dumps(x) + "\n" for x in token_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
