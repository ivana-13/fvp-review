"""Anchored role prompts for the ARO left/right items: the phrase names the relation and the OTHER participant.

The generic role phrase ("the one that is to the left of something") cannot identify a participant of a symmetric spatial
relation. The anchored phrase can: for "the wall is to the right of the curtains" the subject prompt is "the one that is
to the right of the curtains" and the object prompt "the one that is to the left of the wall" (the relation inverted, so
both prompts have the same form and neither names its own target). This tests relation grounding with minimal anchoring.

    uv run python scripts/run_anchored.py --model qwen3vl-2b [--limit N] [--device cpu]
Resumable. Output: outputs/anchored_<model>_aro-spatial.jsonl (per word: role, gold, anchored pointing record).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from fvp.data import image_path, set_cache_default  # noqa: E402

set_cache_default()

from PIL import Image  # noqa: E402

from fvp.models import load_model  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "outputs"
sys.path.insert(0, str(ROOT / "scripts"))
from run_probes import pointing_record  # noqa: E402

INVERSE = {"to the left of": "to the right of", "to the right of": "to the left of"}


def anchored_phrases(it: dict) -> dict[str, str]:
    subj, obj, rel = it["classes"], it["classes_foil"], it["verb"]
    return {subj: f"the one that is {rel} the {obj}", obj: f"the one that is {INVERSE[rel]} the {subj}"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3vl-2b")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()
    items = [json.loads(l) for l in open(DATA / "joined" / "aro-spatial.valid.jsonl", encoding="utf-8")]
    if args.limit:
        items = items[: args.limit]
    OUT.mkdir(exist_ok=True)
    out_path = OUT / f"anchored_{args.model}_aro-spatial.jsonl"
    done = {json.loads(l)["valse_id"] for l in open(out_path, encoding="utf-8")} if out_path.exists() else set()
    todo = [it for it in items if it["valse_id"] not in done and it["verb"] in INVERSE]
    print(f"anchored {args.model}: {len(items)} items, {len(done)} done, {len(todo)} to run")
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
            phrases = anchored_phrases(it)
            rec = {"valse_id": it["valse_id"], "image_file": it["image_file"], "verb": it["verb"], "subset": "aro-spatial",
                   "model": args.model, "words": {}}
            for w, phrase in phrases.items():
                tg = it["targets"][w]
                rec["words"][w] = {"role": tg["role"], "gold": tg["bbox"], "anchored": pointing_record(model, img, phrase, tg["bbox"])}
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fout.flush()
            if i % 25 == 0 or i == len(todo):
                el = time.time() - t0
                print(f"  {i}/{len(todo)}  {el / i:.1f}s per item, elapsed {el / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
