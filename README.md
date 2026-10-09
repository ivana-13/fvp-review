# Foils versus pointing: code and item files (anonymous review copy)

Companion code for an ARR submission that pairs caption-foil evaluation (VALSE actant swaps on SWiG, ARO VG-Relation
swaps on Visual Genome) with a role-localisation probe on the same items, for nine open vision-language models.

## Layout

| path | content |
|---|---|
| `src/fvp/` | model wrappers (Qwen3-VL, InternVL3.5, Molmo, PaliGemma 2, Florence-2, SigLIP2, CLIP), data access, geometry |
| `scripts/prepare_valse_swig.py`, `scripts/prepare_aro.py`, `scripts/fetch_*.py` | build the joined item files and fetch the images |
| `scripts/run_probes.py` | foil test (pairwise, yes/no), noun and role pointing, verb naming |
| `scripts/run_blind_ll.py`, `scripts/run_text_ll.py`, `scripts/token_counts.py` | text-only likelihood baselines (the VLM's own LM; external OLMo-2-7B and Mistral-7B); token counts for the per-token margin |
| `scripts/run_controls.py` | text-only role resolution, caption-in-prompt, foil-in-prompt (conflict) |
| `scripts/run_wording.py` | role-prompt phrasings A/B, paraphrases C/D (`--set extra`), length-matched noun controls E/F (`--set noun`) |
| `scripts/run_verify.py`, `scripts/run_jointbox.py`, `scripts/run_twobox.py` | structured verification, joint-box prompt, two-box recognition probe |
| `scripts/run_encoder_foils.py`, `scripts/run_api.py`, `scripts/summarize_api.py` | contrastive encoders; a proprietary model through an API on the 200-item sample |
| `scripts/check_gold_boxes.py`, `scripts/make_gold_contact_sheet.py`, `scripts/make_gold_tool.py`, `scripts/gold_agreement.py` | detector check of the SWiG boxes, annotation tools, inter-annotator agreement |
| `scripts/make_annotation_tool.py`, `scripts/score_annotations.py` | human ceiling on the role prompts |
| `scripts/analyze.py`, `scripts/make_paper_assets.py` | per-model summaries; every table and number macro of the paper |
| `scripts/make_release.py`, `scripts/score_release.py`, `release/` | the released item files and a scorer for new models |
| `scripts/run_anchored.py` | anchored role prompts on the ARO left/right items |
| `data/joined/*.valid.jsonl`, `data/gold_check.jsonl` | the joined items (captions, foils, roles, gold boxes) and the detector check |
| `outputs/summary_*.md` and small per-item files | summaries per model; external-LM likelihoods, token counts, noun controls, anchored left/right prompts, and the per-item outputs of the two API models (`gemini31pro`, `claudeopus55`), which are not in `release/` |
| `annotation/` | the human-ceiling page and annotations, the second annotator's gold-check verdicts |
| `tests/` | unit tests (`uv run pytest`) |

Per-item outputs of the open models (probes, controls, verification) are large and not included here; `release/*.jsonl`
carries every open model's per-item outcomes, and `outputs/summary_*.md` the aggregated results. The API models' per-item
files (`outputs/probes_*` and `outputs/controls_*` for `gemini31pro` and `claudeopus55`) are included, since they cannot
be regenerated offline.

## Setup

Python 3.12 with [uv](https://docs.astral.sh/uv/): `uv sync`. Images are not redistributed: SWiG images come from the
SWiG/imSitu release, Visual Genome images from their public URLs (`scripts/fetch_images.py`, `scripts/fetch_aro_images.py`);
VALSE and ARO annotation files from their repositories (`data/valse/`, `data/aro/`). `scripts/prepare_valse_swig.py` and
`scripts/prepare_aro.py` rebuild `data/joined/`. A 2B model runs on an 8 GB laptop GPU; the 32B needs about 70 GB in bf16;
the 235B a node with eight H200s. Every run script is resumable and writes JSON lines to `outputs/`.

## Reproducing the tables

`uv run python scripts/analyze.py --model <key>` writes `outputs/summary_<key>.md`;
`uv run python scripts/make_paper_assets.py` writes the tables and number macros (`paper/tables`, `paper/numbers.tex`)
from whatever runs are complete. Model keys are listed in `src/fvp/models/__init__.py`.

## Scoring your own model on the released items

See `release/README.md`: one JSON line per item with the predicted boxes, then
`python scripts/score_release.py predictions.jsonl --items release/swaps.jsonl`.
