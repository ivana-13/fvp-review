"""Role-prompt wording check on a fixed random sample of actant-swap items.

Phrasing A is the one used in the main runs (scripts/run_probes.py): agent "the one who is <verb> (the agent)",
other roles: the SWiG role definition. Phrasing B names the role instead of describing it: agent "the agent of the
<verb> action", other roles "the <role> of the <verb> action". Both phrasings are run here on the same items (A is
re-run so the comparison does not depend on the main run); the noun-prompt results for the same items come from the
probes file at analysis time.

Usage:
    uv run python scripts/run_wording.py --model qwen3vl-2b [--n 200] [--seed 0] [--limit N] [--device cpu]
Resumable. Output: outputs/wording_<model>_actant-swap.jsonl

--set extra runs the meaning-preserving paraphrases C and D (outputs/wording_cd_<model>_<subset>.jsonl).
--set noun runs the length-matched noun controls (outputs/wording_noun_<model>_<subset>.jsonl): E names the noun in a
descriptive phrase as long as a role phrase ("the dog that can be seen in this picture"), F puts the noun into the frame
of the agent phrase ("the one that is the dog"). If these score like the plain noun prompt, the role deficit is not an
effect of phrase length or form.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from pathlib import Path

from fvp.data import SUBSETS, image_path, set_cache_default  # noqa: E402

set_cache_default()

from PIL import Image  # noqa: E402

from fvp.models import load_model  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
sys.path.insert(0, str(ROOT / "scripts"))
from run_probes import pointing_record, role_phrase  # noqa: E402

READABLE_ROLE = {"agentpart": "body part of the agent", "agentparts": "body parts of the agent", "coagent": "co-agent"}


def phrase_b(role: str, role_def: str, verb: str) -> str:
    name = READABLE_ROLE.get(role, role)
    return f"the {name} of the {verb} action"


PHRASINGS = {"A": role_phrase, "B": phrase_b}


def phrase_c(role: str, role_def: str, verb: str) -> str:
    """Phrasing A without the parenthetical on the agent: 'the one who is biting'."""
    return f"the one who is {verb}" if role == "agent" else role_phrase(role, role_def, verb)


def phrase_d(role: str, role_def: str, verb: str) -> str:
    """Phrasing A with a locative tail: 'the item that is being bitten in this picture'."""
    return role_phrase(role, role_def, verb) + " in this picture"


# meaning-preserving paraphrases, run as a second set (--set extra) to put a noise ceiling on item-level flips
PHRASINGS_EXTRA = {"C": phrase_c, "D": phrase_d}

# length- and frame-matched noun controls (--set noun): the noun is named, the phrase is as long or as framed as a role phrase
PHRASINGS_NOUN = {"E": lambda word: f"the {word} that can be seen in this picture", "F": lambda word: f"the one that is the {word}"}
SET_PREFIX = {"main": "", "extra": "cd_", "noun": "noun_"}


def sample_items(items: list[dict], n: int, seed: int) -> list[dict]:
    """Deterministic sample of n items, returned in file order."""
    ids = {it["valse_id"] for it in random.Random(seed).sample(items, min(n, len(items)))}
    return [it for it in items if it["valse_id"] in ids]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3vl-2b")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--set", choices=["main", "extra", "noun"], default="main", help="main = phrasings A and B; extra = C and D; noun = E and F")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--subset", choices=SUBSETS, default="actant-swap")
    args = ap.parse_args()

    items = [json.loads(l) for l in open(DATA / "joined" / f"{args.subset}.valid.jsonl", encoding="utf-8")]
    items = sample_items(items, args.n, args.seed)
    if args.limit:
        items = items[: args.limit]
    OUT.mkdir(exist_ok=True)
    out_path = OUT / ("wording_" + SET_PREFIX[args.set] + f"{args.model}_{args.subset}.jsonl")
    done = {json.loads(l)["valse_id"] for l in open(out_path, encoding="utf-8")} if out_path.exists() else set()
    todo = [it for it in items if it["valse_id"] not in done]
    print(f"wording {args.model}: {len(items)} sampled items, {len(done)} done, {len(todo)} to run")
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
            rec = {"valse_id": it["valse_id"], "image_file": it["image_file"], "verb": it["verb"], "subset": args.subset,
                   "model": args.model, "seed": args.seed, "words": {}}
            for w in [it["classes"], it["classes_foil"]]:
                tg = it["targets"][w]
                entry = {"role": tg["role"], "gold": tg["bbox"]}
                if args.set == "noun":
                    for key, fn in PHRASINGS_NOUN.items():
                        entry[key] = pointing_record(model, img, fn(w), tg["bbox"])
                else:
                    for key, fn in (PHRASINGS if args.set == "main" else PHRASINGS_EXTRA).items():
                        entry[key] = pointing_record(model, img, fn(tg["role"], tg["def"], it["verb"]), tg["bbox"])
                rec["words"][w] = entry
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fout.flush()
            if i % 20 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"  {i}/{len(todo)}  {el / i:.1f}s per item, elapsed {el / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
