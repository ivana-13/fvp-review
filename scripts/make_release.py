"""Build the released "balanced-and-boxed" item files: every actant-swap and ARO relation item with its caption, foil,
role phrases, gold boxes and the flags a role-binding probe needs, plus every open model's outcomes on it.

    uv run python scripts/make_release.py

Writes release/swaps.jsonl (VALSE actant swaps on SWiG), release/aro_relations.jsonl (ARO VG-Relation swaps) and
release/README.md. Images are not included: SWiG and Visual Genome images are redistributed by their own projects, and
the files carry the image file names. Score your own boxes with scripts/score_release.py.

Fields per item: valse_id, image_file, width, height, caption, foil, verb (SWiG verb or ARO relation), participants
(one per swapped word: word, role, role_phrase = the phrasing-A prompt of the paper, gold_box [x1, y1, x2, y2] in
pixels), flags (nested_pair; swaps only: gold_detector_ok, gold_human_confirmed), text_lm (per external text-only
language model: margin in nats, stratum balanced / text-solvable / foil-preferred at one nat), models (per open model:
foil_pass (pairwise, with image), blind_ab, own_lm_margin, both_noun, both_role, role_iou per word).
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from analyze import BAL, HIT, load_jsonl  # noqa: E402
from make_paper_assets import APPENDIX_ONLY, POINTING_MODELS, nested_pair  # noqa: E402
from run_probes import role_phrase  # noqa: E402

DATA, OUT, REL = ROOT / "data", ROOT / "outputs", ROOT / "release"
EXT_LMS = ["olmo2-7b", "mistral-7b"]
MODELS = [(k, n) for k, n in POINTING_MODELS if k not in APPENDIX_ONLY]


def stratum(m: float) -> str:
    return "text-solvable" if m > BAL else ("foil-preferred" if m < -BAL else "balanced")


def gold_sets() -> tuple[set, set]:
    """(detector-verified items, detector-or-human-verified items); the same rules as scripts/make_paper_assets.py."""
    gc = load_jsonl(DATA / "gold_check.jsonl")
    gold_ok = {r["valse_id"] for r in gc if all(w["flag"] == "ok" for w in r["words"].values())}
    human_ok, human_bad = set(), set()
    csvp = OUT / "gold_flagged.csv"
    if csvp.exists():
        by_item: dict[str, list] = {}
        for row in csv.DictReader(open(csvp, encoding="utf-8-sig")):
            v = (row.get("verdict") or "").strip().lower()
            by_item.setdefault(row["valse_id"], []).append((row["flag"], {"o": "ok", "s": "swapped"}.get(v, v)))
        for vid, fv in by_item.items():
            if all(v for _, v in fv):
                (human_ok if all(p in {("ok", "ok"), ("swapped", "swapped")} for p in fv) else human_bad).add(vid)
    return gold_ok, (gold_ok | human_ok) - human_bad


def build(subset: str, out: Path, gold: tuple[set, set] | None) -> int:
    items = load_jsonl(DATA / "joined" / f"{subset}.valid.jsonl")
    ext = {lm: {r["valse_id"]: r["margin"] for r in load_jsonl(OUT / f"blindll_{lm}_{subset}.jsonl")} for lm in EXT_LMS}
    probes = {}
    for key, _ in MODELS:
        recs = [r for r in load_jsonl(OUT / f"probes_{key}_{subset}.jsonl") if "pointing" in r and r.get("foil")]
        if len(recs) >= len(items) - 100:  # complete runs only (the joined ARO file lists a few ids twice)
            probes[key] = {r["valse_id"]: r for r in recs}
    own_ll = {key: {r["valse_id"]: r["margin"] for r in load_jsonl(OUT / f"blindll_{key}_{subset}.jsonl")} for key, _ in MODELS}
    n = 0
    seen = set()
    with open(out, "w", encoding="utf-8") as f:
        for it in items:
            vid = it["valse_id"]
            if vid in seen:
                continue
            seen.add(vid)
            words = [w for w in it["targets"] if w != "__agent__"]
            parts = [{"word": w, "role": it["targets"][w]["role"],
                      "role_phrase": role_phrase(it["targets"][w]["role"], it["targets"][w].get("def", ""), it["verb"]),
                      "gold_box": it["targets"][w]["bbox"]} for w in words]
            rec = {"valse_id": vid, "image_file": it["image_file"], "width": it["width"], "height": it["height"],
                   "caption": it["caption"], "foil": it["foil"], "verb": it["verb"], "participants": parts,
                   "flags": {"nested_pair": nested_pair(parts[0]["gold_box"], parts[1]["gold_box"]) if len(parts) == 2 else None},
                   "text_lm": {lm: {"margin": round(ext[lm][vid], 3), "stratum": stratum(ext[lm][vid])} for lm in EXT_LMS if vid in ext[lm]},
                   "models": {}}
            if gold is not None:
                rec["flags"]["gold_detector_ok"] = vid in gold[0]
                rec["flags"]["gold_human_confirmed"] = vid in gold[1]
            for key, _ in MODELS:
                r = probes.get(key, {}).get(vid)
                if not r:
                    continue
                pt = r["pointing"]
                rec["models"][key] = {
                    "foil_pass": bool(r["foil"]["pair_correct"]), "blind_ab": bool(r["foil"].get("blind_correct", False)),
                    "own_lm_margin": round(own_ll[key][vid], 3) if vid in own_ll[key] else None,
                    "both_noun": all(p["noun_prompt"]["iou"] >= HIT for p in pt.values()),
                    "both_role": all(p["role_prompt"]["iou"] >= HIT for p in pt.values()),
                    "role_iou": {w: round(p["role_prompt"]["iou"], 3) for w, p in pt.items()},
                    "noun_iou": {w: round(p["noun_prompt"]["iou"], 3) for w, p in pt.items()}}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    return n


README = """# Foils versus pointing: the balanced-and-boxed item files

Companion data for an ARR submission on caption-foil benchmarks and role pointing. Two JSON-lines files, one
item per line, that let a caption-foil evaluation be paired with a role-localisation probe on the same items.

| file | items | source |
|---|---|---|
| `swaps.jsonl` | {n_swap} VALSE actant swaps joined to SWiG | images: SWiG (imSitu) |
| `aro_relations.jsonl` | {n_aro} distinct ARO VG-Relation swaps (at most 150 per relation; the paper's 1,228 records also count second phrasings of the same image-relation pair) | images: Visual Genome |

Images are not included; `image_file` names the SWiG or Visual Genome image. Captions and foils come from VALSE and
ARO, boxes from SWiG and Visual Genome, all under their own licences.

## Fields

- `caption`, `foil`: the true caption and its participant-swapped foil; `verb`: the SWiG verb or the ARO relation.
- `participants`: the two swapped words, each with its semantic `role`, the `role_phrase` used as the pointing prompt
  (phrasing A of the paper; it names the role, never the noun) and the `gold_box` `[x1, y1, x2, y2]` in pixels.
- `flags.nested_pair`: the two gold boxes overlap at IoU >= 0.5 or one lies 90% inside the other (such pairs are
  excluded from the discriminative criterion in the paper). Swaps only: `gold_detector_ok` (an open-vocabulary detector
  agreed with both SWiG boxes) and `gold_human_confirmed` (detector-verified or confirmed by a manual check).
- `text_lm`: for two external text-only language models (OLMo-2-7B, Mistral-7B), the log-likelihood margin
  caption minus foil in nats and the stratum at one nat: `balanced` (|margin| <= 1: the text alone cannot decide),
  `text-solvable` (> 1) or `foil-preferred` (< -1). Report swap results on the balanced stratum.
- `models`: per open model of the paper, `foil_pass` (pairwise choice with the image), `blind_ab` (the same without
  the image), `own_lm_margin` (the model's own language model), `both_noun` / `both_role` (both participants located,
  IoU >= 0.5, with noun prompts / with the role phrases; Molmo: point in box) and the per-word IoUs.

## Scoring your own model

Write one JSON line per item: `{{"valse_id": ..., "boxes": {{"<word>": [x1, y1, x2, y2], ...}}, "foil_pass": true}}`
(boxes in original pixels, one per participant word; `foil_pass` optional) and run

    python scripts/score_release.py predictions.jsonl --items release/swaps.jsonl

It prints the share of items with both participants located by role, on all items, on the balanced stratum and on
the gold-verified items, and, when `foil_pass` is given, P(located | foil passed) and the odds ratio between the two.

Built by `scripts/make_release.py` from the repository's outputs on {date}.
"""


def main() -> None:
    import datetime
    REL.mkdir(exist_ok=True)
    gold = gold_sets()
    n_swap = build("actant-swap", REL / "swaps.jsonl", gold)
    n_aro = build("aro-relation", REL / "aro_relations.jsonl", None)
    (REL / "README.md").write_text(README.format(n_swap=n_swap, n_aro=n_aro, date=datetime.date.today().isoformat()), encoding="utf-8")
    print(f"release/swaps.jsonl: {n_swap} items; release/aro_relations.jsonl: {n_aro} items; README written")


if __name__ == "__main__":
    main()
