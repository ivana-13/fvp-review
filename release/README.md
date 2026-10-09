# Foils versus pointing: the balanced-and-boxed item files

Companion data for an ARR submission on caption-foil benchmarks and role pointing. Two JSON-lines files, one
item per line, that let a caption-foil evaluation be paired with a role-localisation probe on the same items.

| file | items | source |
|---|---|---|
| `swaps.jsonl` | 933 VALSE actant swaps joined to SWiG | images: SWiG (imSitu) |
| `aro_relations.jsonl` | 1143 distinct ARO VG-Relation swaps (at most 150 per relation; the paper's 1,228 records also count second phrasings of the same image-relation pair) | images: Visual Genome |

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

Write one JSON line per item: `{"valse_id": ..., "boxes": {"<word>": [x1, y1, x2, y2], ...}, "foil_pass": true}`
(boxes in original pixels, one per participant word; `foil_pass` optional) and run

    python scripts/score_release.py predictions.jsonl --items release/swaps.jsonl

It prints the share of items with both participants located by role, on all items, on the balanced stratum and on
the gold-verified items, and, when `foil_pass` is given, P(located | foil passed) and the odds ratio between the two.

Built by `scripts/make_release.py` from the repository's outputs on 2026-10-09.
