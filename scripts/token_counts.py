"""Token counts of every caption and foil under a model's tokenizer, for the length-normalised blind likelihood.

    uv run python scripts/token_counts.py --models qwen3vl-2b internvl35-2b
    uv run python scripts/token_counts.py --all          # every model with a blind-LL file in outputs/

Writes outputs/tokens_<model>.jsonl, one line per item (valse_id, subset, n_caption, n_foil), for every subset that has
a blind-LL file. Only the tokenizer is loaded (CPU, no weights). The count is len(tok.encode(text,
add_special_tokens=False)): exactly the tokens whose log-probabilities scripts/run_blind_ll.py sums, so ll / n is the
mean log-probability per token and ll_caption / n_caption - ll_foil / n_foil the length-normalised margin.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fvp.data import SUBSETS, set_cache_default  # noqa: E402

set_cache_default()

from fvp.models import REGISTRY  # noqa: E402

OUT = ROOT / "outputs"


def tokenizer_for(key: str):
    from transformers import AutoProcessor, AutoTokenizer
    model_id = REGISTRY[key][2]["model_id"]
    try:
        return AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    except Exception:  # a processor with remote code (Molmo) may register its tokenizer only through the processor
        return AutoProcessor.from_pretrained(model_id, trust_remote_code=True).tokenizer


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=[])
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    keys = args.models or ([k for k in REGISTRY if (OUT / f"blindll_{k}_actant-swap.jsonl").exists()] if args.all else [])
    for key in keys:
        tok = tokenizer_for(key)
        lines = []
        for subset in SUBSETS:
            f = OUT / f"blindll_{key}_{subset}.jsonl"
            if not f.exists():
                continue
            for line in open(f, encoding="utf-8"):
                r = json.loads(line)
                lines.append({"valse_id": r["valse_id"], "subset": subset,
                              "n_caption": len(tok.encode(r["caption"], add_special_tokens=False)),
                              "n_foil": len(tok.encode(r["foil"], add_special_tokens=False))})
        (OUT / f"tokens_{key}.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines), encoding="utf-8")
        same = sum(x["n_caption"] == x["n_foil"] for x in lines)
        print(f"{key}: {len(lines)} items, same token length {same} ({100 * same / max(1, len(lines)):.1f}%)")


if __name__ == "__main__":
    main()
