"""Generate LaTeX tables, number macros and example figures for paper/main.tex from the run outputs.

Usage:
    uv run python scripts/make_paper_assets.py
Writes paper/tables/*.tex, paper/numbers.tex and paper/figures/example_*.png.
Re-run after every analysis step; the paper picks up the new numbers on the next compile. Every macro the paper
may reference is emitted (as "--" when the run behind it has not finished), so the paper always compiles.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT, PAPER = ROOT / "data", ROOT / "outputs", ROOT / "paper"
TAB, FIG = PAPER / "tables", PAPER / "figures"
sys.path.insert(0, str(ROOT / "scripts"))
from fvp.data import SUBSETS  # noqa: E402
from fvp.geometry import box_center, iou, point_in_box  # noqa: E402
from analyze import (BAL, HIT, blindll_stats, chance_baselines, ci_pct, controls_stats, four_cell, kappa,  # noqa: E402
                     load_jsonl, stat_cond, stat_kappa, stat_rate, verb_match)

# Table order: one block per family, by size (rows appear once a run is complete).
POINTING_MODELS = [("qwen3vl-2b", "Qwen3-VL-2B"), ("qwen3vl-4b", "Qwen3-VL-4B"), ("qwen3vl-8b", "Qwen3-VL-8B"),
                   ("qwen3vl-32b-4bit", "Qwen3-VL-32B (nf4)"), ("qwen3vl-32b", "Qwen3-VL-32B"),
                   ("qwen3vl-235b", "Qwen3-VL-235B"),
                   ("internvl35-2b", "InternVL3.5-2B"), ("internvl35-8b", "InternVL3.5-8B"), ("internvl35-38b", "InternVL3.5-38B"),
                   ("molmo-7b-d", "Molmo-7B-D (points)"), ("paligemma2-10b", "PaliGemma 2 10B"),
                   ("florence2-large", "Florence-2-L"), ("gemma3-12b", "Gemma 3 12B (foil only)"),
                   # 4-bit runs of the 4B and 8B (laptop) and of the 32B (RTX 3090): macros only, compared with their
                   # bf16 runs in the appendix table tab_quant (the bf16 32B ran on an H200, 2026-10-07)
                   ("qwen3vl-4b-4bit", "Qwen3-VL-4B (nf4)"), ("qwen3vl-8b-4bit", "Qwen3-VL-8B (nf4)")]
APPENDIX_ONLY = {"qwen3vl-4b-4bit", "qwen3vl-8b-4bit", "qwen3vl-32b-4bit"}


def odds_ratio(fc: dict) -> str:
    """Odds ratio between a foil pass and both participants located, with a 95% Woolf interval ('2.4 [1.3, 4.3]');
    0.5 is added to every cell when one is empty."""
    import math
    a, b, c, d = fc["foil+point+"], fc["foil+point-"], fc["foil-point+"], fc["foil-point-"]
    if min(a, b, c, d) == 0:
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    orr = (a * d) / (b * c)
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    lo, hi = math.exp(math.log(orr) - 1.96 * se), math.exp(math.log(orr) + 1.96 * se)
    centre = f"{orr:.2f}" if orr < 1 else f"{orr:.1f}"
    return f"{centre} [{lo:.1f}, {hi:.1f}]"


def nz(text: str) -> str:
    """A kappa of -0.00 prints as 0.00."""
    return text.replace("-0.00", "0.00")


def shown(key: str) -> bool:
    """Whether a model gets rows in the result tables (the 4-bit 4B/8B/32B runs appear only in tab_quant)."""
    return key not in APPENDIX_ONLY
ENCODERS = [("siglip2-base", "SigLIP2-B/16"), ("clip-vit-l", "CLIP ViT-L/14")]

FOOTER = '\n\\bottomrule\n\\end{tabular}\n'

# Table style shared with the Overleaf project, whose layout.tex defines the colour wash `headerwash`, the washed column
# types F (foil scores), R (role localisation) and N (noun controls), \thead, \rolehead, \foilhead and \scoreci:
# washed header rows, a small gap between model families, sample counts in the captions rather than in the cells, and
# every "rate [lo, hi]" cell written as \scoreci{rate}{lo}{hi}. paper/layout.tex is a copy of that file.
FAMILY = {"siglip2-base": "encoder", "clip-vit-l": "encoder"}


def family(key: str) -> str:
    """The model family of a run key ('qwen3vl-32b-4bit' -> 'qwen3vl'); the two encoders share one group."""
    return FAMILY.get(key) or key.split("-")[0]


def grouped(rows, space: str = "2pt", by=family) -> str:
    """Join (key, row) pairs, inserting \\addlinespace where the group of the key changes."""
    out, prev = [], None
    for key, line in rows:
        g = by(key)
        if prev is not None and g != prev:
            out.append(f"\\addlinespace[{space}]")
        out.append(line)
        prev = g
    return "\n".join(out)


def header(colspec: str, *lines: str) -> str:
    """The opening of a tabular: colour-washed header rows (rule and spacing lines are left as they are)."""
    body = [ln if ln.startswith(("\\cmidrule", "\\addlinespace")) else "\\rowcolor{headerwash}\n" + ln for ln in lines]
    return f"\\begin{{tabular}}{{{colspec}}}\n\\toprule\n" + "\n".join(body) + "\n\\midrule\n"


def sc(text: str) -> str:
    """A 'rate [lo, hi]' cell as \\scoreci{rate}{lo}{hi}; any other cell unchanged."""
    m = re.fullmatch(r"(\S+) \[(\S+), (\S+)\]", text.strip())
    return f"\\scoreci{{{m[1]}}}{{{m[2]}}}{{{m[3]}}}" if m else text.strip()


CTL_HEADER = header("@{}lrRRNrrrrr@{}", " & & \\multicolumn{3}{c}{Pointing hit per target} & & \\multicolumn{4}{c}{Conflict pointing} \\\\",
                    "\\cmidrule(lr){3-5}\\cmidrule(lr){7-10}",
                    "Model & \\thead{Text\\\\resolved} & role & +caption & noun & \\thead{Text OK,\\\\point fails} & image & text & both & neither \\\\")
BLL_HEADER = header("@{}lrrrrr@{}", "\\multicolumn{6}{@{}l}{\\textit{(a) Text-only baselines}} \\\\", "\\addlinespace[2pt]",
                    " & \\multicolumn{3}{c}{Text only (swap)} & \\multicolumn{2}{c}{LL margin $>$1 nat} \\\\",
                    "\\cmidrule(lr){2-4}\\cmidrule(lr){5-6}", "Model & A/B & LL & LL/token & swap & replacement \\\\")
BLL_HEADER_B = header("@{}lrrrrrrrr@{}", "\\multicolumn{9}{@{}l}{\\textit{(b) Agreement within likelihood strata}} \\\\", "\\addlinespace[2pt]",
                      " & \\multicolumn{3}{c}{Balanced stratum} & \\multicolumn{2}{c}{Text-solvable stratum} & \\multicolumn{3}{c}{Text favours the foil} \\\\",
                      "\\cmidrule(lr){2-4}\\cmidrule(lr){5-6}\\cmidrule(lr){7-9}",
                      "Model & $n$ & \\thead{foil\\\\passed} & \\thead{$P(\\mathrm{loc}$\\\\$\\mid\\mathrm{pass})$} & \\thead{foil\\\\passed} & "
                      "\\thead{$P(\\mathrm{loc}$\\\\$\\mid\\mathrm{pass})$} & $n$ & \\thead{foil\\\\passed} & \\thead{$P(\\mathrm{loc}$\\\\$\\mid\\mathrm{pass})$} \\\\")
WORD_HEADER = header("@{}lRRRRRRRRNrrr@{}",
                     " & \\multicolumn{2}{c}{Agent by role} & \\multicolumn{2}{c}{Other by role} & \\multicolumn{5}{c}{Both located} & \\multicolumn{3}{c}{Item-level flips} \\\\",
                     "\\cmidrule(lr){2-3}\\cmidrule(lr){4-5}\\cmidrule(lr){6-10}\\cmidrule(lr){11-13}",
                     "Model & A & B & A & B & A & B & C & D & noun & A$\\neq$B & A$\\neq$C & A$\\neq$D \\\\")
VER_HEADER = header("@{}lrFFFFRRrR@{}", " & & & \\multicolumn{3}{c}{Structured foil} & & & & \\\\", "\\cmidrule(lr){4-6}",
                    "Model & parsed & \\thead{Pairwise\\\\foil} & first & strict & consist. & \\thead{Both\\\\located} & "
                    "\\thead{$P(\\mathrm{loc}$\\\\$\\mid\\mathrm{pass})$} & $\\kappa$ & \\thead{Independent\\\\$P(\\mathrm{loc}\\mid\\mathrm{pass})$} \\\\")

# Macro key templates emitted for every pointing model, so the paper compiles before a run has finished.
MODEL_KEYS = ["pair_", "blind_", "yes_", "yesrateFoil_", "yesrateCap_", "meanYesFoil_", "meanYesCap_", "pairRep_", "blindRep_",
              "yesRep_", "meanYesFoilRep_", "ptAgentRoleRep_", "pt_agent_role_", "pt_agent_noun_", "pt_other_role_", "pt_other_noun_",
              "ptOtherRoleCI_", "ptOtherNounCI_", "condBoth_", "condBothCI_", "cellPassNoPoint_", "cellPassPoint_", "kappa_", "kappaCI_",
              "ptBoth_", "ptBothNoun_", "ptBothRole_", "ptBothNounGold_", "ptBothRoleGold_", "condBothGold_", "nGoldSub_",
              "cellPassNoPointGold_", "cellPassPointGold_", "ctlText_", "ctlUncond_", "ctlCond_", "ctlNoun_", "ctlTextOkPointFail_",
              "ctlConfImage_", "ctlConfText_", "ctlConfNeither_", "ctlConfBoth_", "ctlNested_", "ctlCondBoth_", "ctlUncondBoth_", "blindLL_",
              "blindLLSolvable_", "blindLLSolvableRep_", "blindLLRep_", "balN_", "balFoil_", "balFoilCI_", "balCond_", "balCondCI_",
              "balPoint_", "solvN_", "solvFoil_", "solvCond_", "blindLLTok_", "strataMovedTok_", "balNTok_", "balFoilTok_",
              "balCondTok_", "fpN_", "fpFoil_", "fpCond_", "fpCondCI_", "wordN_",
              "sizeRoleS_", "sizeRoleM_", "sizeRoleL_", "sizeNounS_", "sizeNounM_", "sizeNounL_", "sizeRoleSmall_", "sizeRoleLarge_",
              "sizeCondSmall_", "sizeCondLarge_", "sizeNCondSmall_", "sizeNCondLarge_",
              "extSame_", "extBalFoil_", "extBalFoilCI_", "extBalCond_", "extBalCondCI_", "extSolvFoil_", "extSolvCond_", "extFpFoil_", "extFpCond_",
              "hcIoU_", "hcCentre_", "hcDiscr_", "hcSwap_", "hcBothIoU_", "hcBothCentre_",
              "nctlOtherNoun_", "nctlOtherE_", "nctlOtherF_", "nctlOtherA_", "nctlBothNoun_", "nctlBothE_", "nctlBothF_", "nctlBothA_", "nctlN_",
              "anchN_", "anchTarget_", "anchBoth_", "anchCond_", "anchCondCI_", "wordAgentA_", "wordAgentB_", "wordOtherA_", "wordOtherB_",
              "wordBothA_", "wordBothB_", "wordBothNoun_", "wordBothACI_", "wordBothBCI_", "wordFlip_", "verN_", "verParsed_",
              "wordBothC_", "wordBothD_", "wordFlipC_", "wordFlipD_", "wordOtherC_", "wordOtherD_",
              "tbN_", "tbNnn_", "tbBothRole_", "tbBothRoleNN_", "tbBothNoun_", "tbCond_", "tbCondLoc_", "tbTargetRole_", "tbTargetNoun_",
              "verPairSame_", "verFirst_", "verStrict_", "verEither_", "verCons_", "verBoth_", "verCond_", "verCondCI_", "verKappa_",
              "verIndepCond_", "verChanged_", "jointBoth_", "jointCond_", "jointCondCI_", "jointSep_",
              "condBothLoc_", "condBothLocCI_", "nLoc_", "verCondLoc_", "jointCondLoc_", "or_",
              "missHit_", "missSwap_", "missCollapse_", "missExtent_", "missElse_", "missNoBox_", "missExchanged_", "missSwapOfMiss_",
              "condBothHuman_", "nHumanSub_", "ptBothRoleHuman_", "ptBothNounHuman_",
              "sweepOtherRolethree_", "sweepOtherRolefive_", "sweepOtherRoleseven_", "sweepOtherRolecentre_",
              "sweepBoththree_", "sweepBothfive_", "sweepBothseven_", "sweepBothcentre_",
              "sweepCondthree_", "sweepCondfive_", "sweepCondseven_", "sweepCondcentre_",
              "sweepOtherRolediscr_", "sweepOtherRolediscrnn_", "sweepOtherNoundiscr_", "sweepOtherNoundiscrnn_",
              "sweepBothdiscr_", "sweepBothdiscrnn_", "sweepConddiscr_", "sweepConddiscrnn_", "sweepNdiscrnn_", "ptAgentNounRep_"]


def pct(k, n):
    return f"{100.0 * k / n:.1f}" if n else "--"


def tex_escape(s: str) -> str:
    return s.replace("&", "\\&").replace("%", "\\%").replace("_", "\\_")


def both_role(r: dict) -> bool:
    return all(p["role_prompt"]["iou"] >= HIT for p in r["pointing"].values())


def both_noun(r: dict) -> bool:
    return all(p["noun_prompt"]["iou"] >= HIT for p in r["pointing"].values())


def nested_pair(ga: list, gb: list) -> bool:
    """Two gold boxes count as nested when they overlap at IoU >= 0.5 or the smaller lies 90% inside the larger."""
    inter = max(0.0, min(ga[2], gb[2]) - max(ga[0], gb[0])) * max(0.0, min(ga[3], gb[3]) - max(ga[1], gb[1]))
    small = min((ga[2] - ga[0]) * (ga[3] - ga[1]), (gb[2] - gb[0]) * (gb[3] - gb[1]))
    return iou(ga, gb) >= 0.5 or (small > 0 and inter / small >= 0.9)


def _stratum_of(margin: float) -> str:
    return "solvable" if margin > BAL else ("foil_preferred" if margin < -BAL else "balanced")


def spearman(xs: list[float], ys: list[float]) -> float:
    """Rank correlation (ties broken by order; fine for a dozen values)."""
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0.0] * len(v)
        for k, i in enumerate(order):
            rk[i] = k
        return rk
    n = len(xs)
    if n < 3:
        return float("nan")
    ra, rb = ranks(xs), ranks(ys)
    return 1 - 6 * sum((a - b) ** 2 for a, b in zip(ra, rb)) / (n * (n * n - 1))


def strata_rows(key: str, probes_sw: list[dict]) -> dict[str, list[tuple[float, float]]]:
    """Per stratum of the likelihood margin: (pairwise foil ok, both located by role) per item."""
    bl = {r["valse_id"]: r for r in load_jsonl(OUT / f"blindll_{key}_actant-swap.jsonl")}
    out: dict[str, list] = {"solvable": [], "balanced": [], "foil_preferred": []}
    for r in probes_sw:
        if "pointing" not in r or r["valse_id"] not in bl or not r.get("foil"):
            continue
        m = bl[r["valse_id"]]["margin"]
        s = "solvable" if m > BAL else ("foil_preferred" if m < -BAL else "balanced")
        out[s].append((float(r["foil"]["pair_correct"]), float(both_role(r))))
    return out


def main() -> None:
    TAB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    items = {}
    for subset in SUBSETS:
        for it in load_jsonl(DATA / "joined" / f"{subset}.valid.jsonl"):
            items[(subset, it["valse_id"])] = it
    n_swap = len([1 for it in items.values() if it["subset"] == "actant-swap"])
    n_rep = len([1 for it in items.values() if it["subset"] == "action-replacement"])
    gc = load_jsonl(DATA / "gold_check.jsonl")
    gold_ok = {r["valse_id"] for r in gc if all(w["flag"] == "ok" for w in r["words"].values())}
    gold_swapped = {r["valse_id"] for r in gc if any(w["flag"] == "swapped" for w in r["words"].values())}
    # manual verdicts on the flagged items (outputs/gold_flagged.csv, column "verdict", one row per word). The verdict
    # judges the red DETECTOR box for that word: ok = on the right participant, swapped = on the other participant,
    # other = anything else. An item's SWiG boxes count as confirmed when every word's verdict agrees with the
    # geometry of the detector flag (ok on an "ok" flag, swapped on a "swapped" flag): the detector erred and the
    # green boxes are right. Any "other" verdict, or a verdict that contradicts the flag (a correct detector box on
    # the other gold box, as in a genuine SWiG swap, or a very large detector box), leaves the item unconfirmed.
    human_ok, human_bad = set(), set()
    csvp = OUT / "gold_flagged.csv"
    if csvp.exists():
        import csv
        by_item: dict[str, list[tuple[str, str]]] = {}
        for row in csv.DictReader(open(csvp, encoding="utf-8-sig")):
            v = (row.get("verdict") or "").strip().lower()
            v = {"o": "ok", "s": "swapped"}.get(v, v)
            by_item.setdefault(row["valse_id"], []).append((row["flag"], v))
        for vid, fv in by_item.items():
            if not all(v for _, v in fv):
                continue  # not checked yet
            if all(p in {("ok", "ok"), ("swapped", "swapped")} for p in fv):
                human_ok.add(vid)
            else:
                human_bad.add(vid)
    gold_ok_human = (gold_ok | human_ok) - human_bad

    runs = {}
    for key, _ in POINTING_MODELS + ENCODERS:
        for subset in ["actant-swap", "action-replacement"]:
            recs = load_jsonl(OUT / f"probes_{key}_{subset}.jsonl")
            if recs and len(recs) >= (n_swap if subset == "actant-swap" else n_rep):  # partial runs stay out
                runs[(key, subset)] = recs

    numbers = {"nSwap": n_swap, "nRep": n_rep, "nImages": len({it["image_file"] for it in items.values()}),
               "nGoldChecked": len(gc), "nGoldOk": len(gold_ok), "nGoldSwapped": len(gold_swapped),
               "nHumanChecked": len(human_ok | human_bad), "nHumanOk": len(human_ok), "nHumanBad": len(human_bad),
               "nGoldOkHuman": len(gold_ok_human)}

    # second annotator on the flagged items (annotation/gold_flagged_annotator2.csv, the browser tool of
    # scripts/make_gold_tool.py): row-level agreement, item-level agreement on "confirmed", and the joint subset
    ann2_p = ROOT / "annotation" / "gold_flagged_annotator2.csv"
    gold_ok_both = gold_ok_human
    if csvp.exists() and ann2_p.exists():
        from gold_agreement import confirmed as _confirmed, kappa as _kappa, read as _read
        a1, a2 = _read(str(csvp)), _read(str(ann2_p))
        keys = sorted(k for k in a1 if k in a2 and a1[k]["verdict"] and a2[k]["verdict"])
        pairs = [(a1[k]["verdict"], a2[k]["verdict"]) for k in keys]
        items1: dict[str, list] = {}
        items2: dict[str, list] = {}
        for k in keys:
            items1.setdefault(k[0], []).append((a1[k]["flag"], a1[k]["verdict"]))
            items2.setdefault(k[0], []).append((a2[k]["flag"], a2[k]["verdict"]))
        c1, c2 = _confirmed(a1, items1), _confirmed(a2, items2)
        numbers.update({"gaRows": len(keys), "gaAgree": pct(sum(x == y for x, y in pairs), len(pairs)), "gaKappa": f"{_kappa(pairs):.2f}",
                        "gaItems": len(items1), "gaConfOne": len(c1), "gaConfTwo": len(c2), "gaConfBoth": len(c1 & c2),
                        "gaConfNeither": len(set(items1) - c1 - c2),
                        "gaItemAgree": pct(sum((v in c1) == (v in c2) for v in items1), len(items1)),
                        "gaItemKappa": f"{_kappa([(str(v in c1), str(v in c2)) for v in items1]):.2f}"})
        gold_ok_both = gold_ok | (c1 & c2)
        numbers["nGoldOkBoth"] = len(gold_ok_both)

    # ---------------- Table 1: foil accuracies ----------------
    rows = []
    ci_half = []
    rep_rows = []
    for key, name in POINTING_MODELS + ENCODERS:
        if not any((key, s) in runs for s in ["actant-swap", "action-replacement"]):
            continue  # no complete run yet: no row
        cells = [name]
        for subset in ["actant-swap", "action-replacement"]:
            recs = runs.get((key, subset))
            if not recs:
                cells += ["--", "--", "--"]
                continue
            f = [r["foil"] for r in recs if r.get("foil")]
            if not f:
                cells += ["--", "--", "--"]
                continue
            n = len(f)
            is_enc = key in dict(ENCODERS)
            if is_enc:
                numbers[("pairSwap_" if subset == "actant-swap" else "pairRep_") + key] = pct(sum(x["pair_correct"] for x in f), n)
            cells.append("--" if is_enc else pct(sum(x["yes_correct"] for x in f), n))
            cells.append(pct(sum(x["pair_correct"] for x in f), n))
            cells.append("--" if is_enc else pct(sum(bool(x["blind_correct"]) for x in f), n))
            for col in (["pair_correct"] if is_enc else ["yes_correct", "pair_correct", "blind_correct"]):
                lo, hi = [float(v) for v in ci_pct([float(bool(x[col])) for x in f]).strip("[]").split(",")]
                ci_half.append((hi - lo) / 2)
            if not is_enc and subset == "actant-swap":
                numbers[f"pair_{key}"] = pct(sum(x["pair_correct"] for x in f), n)
                numbers[f"blind_{key}"] = pct(sum(bool(x["blind_correct"]) for x in f), n)
                numbers[f"yes_{key}"] = pct(sum(x["yes_correct"] for x in f), n)
                numbers[f"yesrateFoil_{key}"] = pct(sum(x["p_yes_foil"] > 0.5 for x in f), n)
                numbers[f"yesrateCap_{key}"] = pct(sum(x["p_yes_caption"] > 0.5 for x in f), n)
                numbers[f"meanYesFoil_{key}"] = f"{sum(x['p_yes_foil'] for x in f) / n:.2f}"
                numbers[f"meanYesCap_{key}"] = f"{sum(x['p_yes_caption'] for x in f) / n:.2f}"
            if not is_enc and subset == "action-replacement":
                numbers[f"pairRep_{key}"] = pct(sum(x["pair_correct"] for x in f), n)
                numbers[f"blindRep_{key}"] = pct(sum(bool(x["blind_correct"]) for x in f), n)
                numbers[f"yesRep_{key}"] = pct(sum(x["yes_correct"] for x in f), n)
                numbers[f"meanYesFoilRep_{key}"] = f"{sum(x['p_yes_foil'] for x in f) / n:.2f}"
                recs_p = [r for r in recs if "pointing" in r]
                if recs_p:
                    numbers[f"ptAgentRoleRep_{key}"] = pct(sum(r["pointing"]["__agent__"]["role_prompt"]["iou"] >= HIT for r in recs_p), len(recs_p))
                    numbers[f"ptAgentNounRep_{key}"] = pct(sum(r["pointing"]["__agent__"]["noun_prompt"]["iou"] >= HIT for r in recs_p), len(recs_p))
                    if shown(key):
                        rep_rows.append((name, len(recs_p), numbers[f"ptAgentRoleRep_{key}"], numbers[f"ptAgentNounRep_{key}"], key))
        if numbers.get(f"blind_{key}", "--") != "--" and float(numbers[f"blind_{key}"]) < 25:  # always answers B: degenerate
            cells = [c + "$^\\dagger$" if i in (3, 6) and c != "--" else c for i, c in enumerate(cells)]
        if shown(key) and any(c != "--" for c in cells[1:]): rows.append((key, " & ".join(cells) + " \\\\"))
    numbers["foilCImax"] = f"{max(ci_half):.1f}" if ci_half else "--"
    (TAB / "tab_foil.tex").write_text(
        header("@{}lrrrrrr@{}", " & \\multicolumn{3}{c}{Actant swap} & \\multicolumn{3}{c}{Action replacement} \\\\",
               "\\cmidrule(lr){2-4}\\cmidrule(lr){5-7}", "Model & Yes/no & Pairwise & Blind & Yes/no & Pairwise & Blind \\\\")
        + grouped(rows) + FOOTER, encoding="utf-8")

    # ---------------- Table 2: pointing with chance baselines (cells carry 95% CIs) ----------------
    rows = []
    for key, name in POINTING_MODELS:
        recs = [r for r in runs.get((key, "actant-swap"), []) if "pointing" in r]
        if not recs:
            continue
        by = {}
        for r in recs:
            for w, p in r["pointing"].items():
                kind = "agent" if p["role"] == "agent" else "other"
                for pk in ["role_prompt", "noun_prompt"]:
                    by.setdefault((kind, pk), []).append(p[pk]["iou"])
        cells = [name]
        for kind in ["agent", "other"]:
            for pk in ["noun_prompt", "role_prompt"]:  # column order: noun prompt, then role prompt
                xs = by.get((kind, pk), [])
                hits = [float(x >= HIT) for x in xs]
                rate = pct(sum(hits), len(xs))
                numbers[f"pt_{kind}_{pk.split('_')[0]}_{key}"] = rate
                cells.append(sc(f"{rate} {ci_pct(hits)}"))
                if kind == "other":
                    numbers[f"ptOther{'Role' if pk == 'role_prompt' else 'Noun'}CI_{key}"] = ci_pct(hits)
        if shown(key): rows.append((key, " & ".join(cells) + " \\\\"))
        if key == "qwen3vl-2b":
            for tgt in ["agent", "other"]:
                cb = chance_baselines(items, recs, target=tgt)
                numbers[f"chanceLargest_{tgt}"] = f"{100 * cb['largest_role_box']:.1f}"
                numbers[f"chanceFull_{tgt}"] = f"{100 * cb['full_image_box']:.1f}"
                numbers[f"chanceRandom_{tgt}"] = f"{100 * cb['random_box']:.1f}"
    base_rows = []
    if "chanceLargest_agent" in numbers:
        base_rows = [
            f"\\midrule\nLargest gold box & {numbers['chanceLargest_agent']} & {numbers['chanceLargest_agent']} & {numbers['chanceLargest_other']} & {numbers['chanceLargest_other']} \\\\",
            f"Whole-image box & {numbers['chanceFull_agent']} & {numbers['chanceFull_agent']} & {numbers['chanceFull_other']} & {numbers['chanceFull_other']} \\\\",
            f"Random box & {numbers['chanceRandom_agent']} & {numbers['chanceRandom_agent']} & {numbers['chanceRandom_other']} & {numbers['chanceRandom_other']} \\\\",
        ]
    (TAB / "tab_pointing.tex").write_text(
        header("@{}l NR NR@{}", " & \\multicolumn{2}{c}{Agent} & \\multicolumn{2}{c}{Other actant} \\\\",
               "\\cmidrule(lr){2-3}\\cmidrule(lr){4-5}",
               "Model & Noun prompt & \\rolehead{Role prompt} & Noun prompt & \\rolehead{Role prompt} \\\\")
        + grouped(rows) + "\n" + "\n".join(base_rows) + FOOTER, encoding="utf-8")

    # ---------------- Table 3: agreement (conditional rate and kappa with 95% CIs) ----------------
    rows = []
    for key, name in POINTING_MODELS:
        recs = [r for r in runs.get((key, "actant-swap"), []) if "pointing" in r and r.get("foil")]
        if not recs:
            continue
        subsets_agree = [("all", recs), ("gold", [r for r in recs if r["valse_id"] in gold_ok])]
        if human_ok or human_bad:
            subsets_agree.append(("gold+human", [r for r in recs if r["valse_id"] in gold_ok_human]))
        label = name  # printed on the model's first row only
        for subset_name, sub in subsets_agree:
            if len(sub) < 20:
                continue
            for outcome, olabel in [("pair_correct", "pairwise"), ("yes_correct", "yes/no")]:
                foil_ok = [r["foil"][outcome] for r in sub]
                both = [both_role(r) for r in sub]
                pairs = [(float(a), float(b)) for a, b in zip(foil_ok, both)]
                fc = four_cell(foil_ok, both)
                npass = fc["foil+point+"] + fc["foil+point-"]
                cond = pct(fc["foil+point+"], npass)
                cond_ci = ci_pct(pairs, stat_cond)
                k = kappa(foil_ok, both)
                k_ci = ci_pct(pairs, stat_kappa, scale=1.0, digits=2)
                if shown(key):
                    rows.append((key, f"{label} & {subset_name} & {olabel} & {len(sub)} & {fc['foil+point+']} & {fc['foil+point-']} & "
                                      f"{fc['foil-point+']} & {fc['foil-point-']} & {sc(f'{cond} {cond_ci}')} & {sc(nz(f'{k:.2f} {k_ci}'))} \\\\"))
                    label = ""
                if subset_name == "all" and outcome == "pair_correct":
                    numbers[f"condBoth_{key}"] = cond
                    numbers[f"condBothCI_{key}"] = cond_ci
                    numbers[f"cellPassNoPoint_{key}"] = fc["foil+point-"]
                    numbers[f"cellPassPoint_{key}"] = fc["foil+point+"]
                    numbers[f"kappa_{key}"] = f"{k:.2f}"
                    numbers[f"kappaCI_{key}"] = k_ci
                    numbers[f"ptBoth_{key}"] = pct(sum(both), len(both))
                if outcome == "pair_correct":
                    bn = [both_noun(r) for r in sub]
                    tag = {"all": "", "gold": "Gold", "gold+human": "Human"}[subset_name]
                    numbers[f"ptBothNoun{tag}_{key}"] = pct(sum(bn), len(bn))
                    numbers[f"ptBothRole{tag}_{key}"] = pct(sum(both), len(both))
                if subset_name == "gold+human" and outcome == "pair_correct":
                    numbers[f"condBothHuman_{key}"] = cond
                    numbers[f"nHumanSub_{key}"] = len(sub)
                    numbers[f"ptBothRoleHuman_{key}"] = pct(sum(both), len(both))
                    numbers[f"ptBothNounHuman_{key}"] = pct(sum(both_noun(r) for r in sub), len(sub))
                if subset_name == "gold" and outcome == "pair_correct":
                    numbers[f"condBothGold_{key}"] = cond
                    numbers[f"nGoldSub_{key}"] = len(sub)
                    numbers[f"cellPassNoPointGold_{key}"] = fc["foil+point-"]
                    numbers[f"cellPassPointGold_{key}"] = fc["foil+point+"]
    (TAB / "tab_agreement.tex").write_text(
        header("@{}l l l r rFrr R r@{}",
               "Model & Items & Foil test & $n$ & F$^+$P$^+$ & F$^+$P$^-$ & F$^-$P$^+$ & F$^-$P$^-$ & P(loc$\\mid$pass) & $\\kappa$ \\\\")
        + grouped(rows, "3pt", by=lambda k: k) + FOOTER, encoding="utf-8")

    # effect of restricting the gold+human subset to the items that both annotators confirm (reported in Appendix B)
    if "gaConfBoth" in numbers:
        md = 0.0
        for key, name in POINTING_MODELS:
            recs = [r for r in runs.get((key, "actant-swap"), []) if "pointing" in r and r.get("foil")]
            if not recs or not shown(key):
                continue
            vals = []
            for sub_ids in (gold_ok_human, gold_ok_both):
                sub = [r for r in recs if r["valse_id"] in sub_ids]
                foil_ok = [r["foil"]["pair_correct"] for r in sub]
                both = [both_role(r) for r in sub]
                fc = four_cell(foil_ok, both)
                npass = fc["foil+point+"] + fc["foil+point-"]
                vals.append((100 * fc["foil+point+"] / npass, 100 * sum(both) / len(sub), 100 * sum(both_noun(r) for r in sub) / len(sub)))
            md = max(md, max(abs(a - b) for a, b in zip(vals[0], vals[1])))
        numbers["gaMaxDiff"] = f"{md:.1f}"

    # ---------------- Table 4: role pairs ----------------
    rows = []
    pair_n = Counter()
    per_model = {}
    for key, name in POINTING_MODELS:
        recs = [r for r in runs.get((key, "actant-swap"), []) if "pointing" in r]
        hits, ns = Counter(), Counter()
        for r in recs:
            pr = tuple(sorted(p["role"] for p in r["pointing"].values()))
            ns[pr] += 1
            hits[pr] += both_role(r)
        per_model[key] = (hits, ns)
        pair_n.update(ns)
    top = [k for k, _ in pair_n.most_common(8)]
    for pr in top:
        n_pr = max((per_model[k][1][pr] for k, _ in POINTING_MODELS if k in per_model), default=0)
        cells = ["--".join(pr) + f" ({n_pr})"]
        for key, _ in POINTING_MODELS:
            hits, ns = per_model.get(key, (Counter(), Counter()))
            cells.append(pct(hits[pr], ns[pr]) if ns[pr] else "--")
        rows.append(" & ".join(cells) + " \\\\")
    # single-column table: group the header by model family so it fits (Qwen 2B, 4B, 8B, then InternVL 2B)
    order = ["qwen3vl-2b", "qwen3vl-4b", "qwen3vl-8b", "qwen3vl-32b", "qwen3vl-235b", "internvl35-2b", "internvl35-8b"]
    rows = []
    for pr in top:
        n_pr = max((per_model[k][1][pr] for k in order if k in per_model), default=0)
        cells = ["--".join(pr) + f" ({n_pr})"]
        for key in order:
            hits, ns = per_model.get(key, (Counter(), Counter()))
            cells.append(pct(hits[pr], ns[pr]) if ns[pr] else "--")
        rows.append(" & ".join(cells) + " \\\\")
    (TAB / "tab_rolepairs.tex").write_text(
        header("@{}lrrrrrrr@{}", " & \\multicolumn{5}{c}{Qwen3-VL} & \\multicolumn{2}{c}{InternVL3.5} \\\\",
               "\\cmidrule(lr){2-6}\\cmidrule(lr){7-8}", "Role pair ($n$) & 2B & 4B & 8B & 32B & 235B & 2B & 8B \\\\")
        + "\n".join(rows) + FOOTER, encoding="utf-8")

    # ---------------- Table 5: verb naming ----------------
    rows = []
    for key, name in POINTING_MODELS:
        recs = [r for r in runs.get((key, "actant-swap"), []) if "verb_probe" in r]
        if not recs:
            continue
        vm = [verb_match(r["verb_probe"]["answer"], r["verb_probe"]["gold"]) for r in recs]
        rows.append(f"{name} & {len(vm)} & {pct(sum(s for s, _ in vm), len(vm))} & {pct(sum(y for _, y in vm), len(vm))} \\\\")
    (TAB / "tab_verb.tex").write_text(
        "\\begin{tabular}{l r r r}\n\\toprule\nModel & $n$ & Strict & WordNet \\\\\n\\midrule\n"
        + "\n".join(rows) + FOOTER, encoding="utf-8")

    # ---------------- Table 6: controls ----------------
    rows = []
    for key, name in POINTING_MODELS:
        st = controls_stats(key, runs.get((key, "actant-swap"), []))
        if not st or st["n_items"] < n_swap:
            continue
        c, ncf = st["conflict"], st["n_conflict_eval"]
        if shown(key): rows.append((key, " & ".join([name, pct(st["text_correct"], st["n_words"]), pct(st["uncond_hit"], st["n_with_probe"]),
                                pct(st["cond_hit"], st["n_words"]), pct(st["noun_hit"], st["n_with_probe"]),
                                pct(st["text_ok_uncond_fail"], st["text_ok"]), pct(c["image"], ncf), pct(c["text"], ncf),
                                pct(c["both"], ncf), pct(c["neither"], ncf)]) + " \\\\"))
        numbers[f"ctlText_{key}"] = pct(st["text_correct"], st["n_words"])
        numbers[f"ctlUncond_{key}"] = pct(st["uncond_hit"], st["n_with_probe"])
        numbers[f"ctlCond_{key}"] = pct(st["cond_hit"], st["n_words"])
        numbers[f"ctlNoun_{key}"] = pct(st["noun_hit"], st["n_with_probe"])
        numbers[f"ctlTextOkPointFail_{key}"] = pct(st["text_ok_uncond_fail"], st["text_ok"])
        numbers[f"ctlConfImage_{key}"] = pct(c["image"], ncf)
        numbers[f"ctlConfText_{key}"] = pct(c["text"], ncf)
        numbers[f"ctlConfNeither_{key}"] = pct(c["neither"], ncf)
        numbers[f"ctlConfBoth_{key}"] = pct(c["both"], ncf)
        numbers[f"ctlNested_{key}"] = st["n_nested"]
        numbers[f"ctlCondBoth_{key}"] = pct(st["cond_both"], st["n_items"])
        numbers[f"ctlUncondBoth_{key}"] = pct(st["uncond_both"], st["n_items_with_probe"])
    (TAB / "tab_controls.tex").write_text(CTL_HEADER + grouped(rows) + FOOTER, encoding="utf-8")

    # ---------------- Table 7: likelihood blind baseline (panel a) and stratified agreement (panel b) ----------------
    rows = []
    rows_b = []
    for key, name in POINTING_MODELS:
        probes_sw = [r for r in runs.get((key, "actant-swap"), []) if r.get("foil")]
        st = blindll_stats(key, probes_sw, "actant-swap")
        if not st or not probes_sw or st["n"] < n_swap:
            continue
        st_rep = blindll_stats(key, [], "action-replacement") or {}
        strata = strata_rows(key, probes_sw)
        f = [r["foil"] for r in probes_sw]
        ab = pct(sum(bool(x["blind_correct"]) for x in f), len(f))
        if float(ab) < 25:  # always answers B: degenerate
            ab += "$^\\dagger$"

        def p100(v):
            return f"{100 * v:.1f}" if v == v else "--"

        bal = strata["balanced"]
        bal_foil_ci = ci_pct([b[0] for b in bal]) if bal else "--"
        bal_cond_ci = ci_pct(bal, stat_cond) if bal else "--"
        fp = strata["foil_preferred"]
        fp_cond_ci = ci_pct(fp, stat_cond) if fp else "--"
        if shown(key):
            rows.append((key, " & ".join([name, ab, p100(st["acc"]), p100(st.get("acc_tok", float("nan"))), p100(st["solvable"]),
                                          p100(st_rep.get("solvable", float("nan")))]) + " \\\\"))
            rows_b.append((key, " & ".join([name, str(st.get("balanced_n", 0)),
                                            sc(f"{p100(st.get('balanced_foil_pass', float('nan')))} {bal_foil_ci}"),
                                            sc(f"{p100(st.get('balanced_cond', float('nan')))} {bal_cond_ci}"),
                                            p100(st.get("solvable_foil_pass", float("nan"))), p100(st.get("solvable_cond", float("nan"))),
                                            str(st.get("foil_preferred_n", 0)), p100(st.get("foil_preferred_foil_pass", float("nan"))),
                                            p100(st.get("foil_preferred_cond", float("nan")))]) + " \\\\"))
        numbers[f"blindLL_{key}"] = p100(st["acc"])
        numbers[f"blindLLSolvable_{key}"] = p100(st["solvable"])
        numbers[f"blindLLSolvableRep_{key}"] = p100(st_rep.get("solvable", float("nan")))
        numbers[f"blindLLRep_{key}"] = p100(st_rep.get("acc", float("nan")))
        numbers[f"balN_{key}"] = st.get("balanced_n", 0)
        numbers[f"balFoil_{key}"] = p100(st.get("balanced_foil_pass", float("nan")))
        numbers[f"balFoilCI_{key}"] = bal_foil_ci
        numbers[f"balCond_{key}"] = p100(st.get("balanced_cond", float("nan")))
        numbers[f"balCondCI_{key}"] = bal_cond_ci
        numbers[f"balPoint_{key}"] = p100(st.get("balanced_point_both", float("nan")))
        numbers[f"solvN_{key}"] = st.get("solvable_n", 0)
        numbers[f"solvFoil_{key}"] = p100(st.get("solvable_foil_pass", float("nan")))
        numbers[f"solvCond_{key}"] = p100(st.get("solvable_cond", float("nan")))
        # length-normalised likelihood (scripts/token_counts.py) and the third stratum
        numbers[f"blindLLTok_{key}"] = p100(st.get("acc_tok", float("nan")))
        numbers[f"strataMovedTok_{key}"] = p100(st.get("moved_tok", float("nan")))
        numbers[f"balNTok_{key}"] = st.get("balanced_tok_n", 0)
        numbers[f"balFoilTok_{key}"] = p100(st.get("balanced_tok_foil_pass", float("nan")))
        numbers[f"balCondTok_{key}"] = p100(st.get("balanced_tok_cond", float("nan")))
        numbers[f"fpN_{key}"] = st.get("foil_preferred_n", 0)
        numbers[f"fpFoil_{key}"] = p100(st.get("foil_preferred_foil_pass", float("nan")))
        numbers[f"fpCond_{key}"] = p100(st.get("foil_preferred_cond", float("nan")))
        numbers[f"fpCondCI_{key}"] = fp_cond_ci
    (TAB / "tab_blindll.tex").write_text(BLL_HEADER + grouped(rows) + FOOTER + "\\par\\medskip\n" + BLL_HEADER_B + grouped(rows_b) + FOOTER,
                                         encoding="utf-8")

    # ---------------- Table 8: role-prompt wording check ----------------
    rows = []
    for key, name in POINTING_MODELS:
        wrec = load_jsonl(OUT / f"wording_{key}_actant-swap.jsonl")
        if len(wrec) < 200:
            continue
        probes = {r["valse_id"]: r for r in runs.get((key, "actant-swap"), []) if "pointing" in r}
        agent = {"A": [], "B": []}
        other = {"A": [], "B": []}
        both = {"A": [], "B": []}
        noun_both = []
        flips = []
        for r in wrec:
            for ph in ["A", "B"]:
                for w, d in r["words"].items():
                    (agent if d["role"] == "agent" else other)[ph].append(float(d[ph]["iou"] >= HIT))
                both[ph].append(float(all(d[ph]["iou"] >= HIT for d in r["words"].values())))
            flips.append(float(both["A"][-1] != both["B"][-1]))
            pr = probes.get(r["valse_id"])
            if pr:
                noun_both.append(float(both_noun(pr)))
        n = len(wrec)
        cells = [name, pct(sum(agent["A"]), len(agent["A"])), pct(sum(agent["B"]), len(agent["B"])),
                 pct(sum(other["A"]), len(other["A"])), pct(sum(other["B"]), len(other["B"])),
                 pct(sum(both["A"]), n), pct(sum(both["B"]), n), pct(sum(noun_both), len(noun_both)), pct(sum(flips), n)]
        numbers[f"wordAgentA_{key}"], numbers[f"wordAgentB_{key}"] = cells[1], cells[2]
        numbers[f"wordOtherA_{key}"], numbers[f"wordOtherB_{key}"] = cells[3], cells[4]
        numbers[f"wordBothA_{key}"], numbers[f"wordBothB_{key}"] = cells[5], cells[6]
        numbers[f"wordBothNoun_{key}"], numbers[f"wordFlip_{key}"] = cells[7], cells[8]
        # meaning-preserving paraphrases C and D (a second run set); flips are counted against phrasing A on shared items
        cd = {r["valse_id"]: r for r in load_jsonl(OUT / f"wording_cd_{key}_actant-swap.jsonl")}
        extra = {"C": "--", "D": "--"}; eflip = {"C": "--", "D": "--"}; eother = {"C": "--", "D": "--"}
        if len(cd) >= 200:
            a_both = {r["valse_id"]: all(d["A"]["iou"] >= HIT for d in r["words"].values()) for r in wrec}
            for ph in ("C", "D"):
                b = {vid: all(d[ph]["iou"] >= HIT for d in r["words"].values()) for vid, r in cd.items() if vid in a_both}
                oth = [float(d[ph]["iou"] >= HIT) for r in cd.values() for d in r["words"].values() if d["role"] != "agent"]
                extra[ph] = pct(sum(b.values()), len(b))
                eflip[ph] = pct(sum(b[v] != a_both[v] for v in b), len(b))
                eother[ph] = pct(sum(oth), len(oth))
        cells = cells[:7] + [extra["C"], extra["D"]] + cells[7:] + [eflip["C"], eflip["D"]]
        numbers[f"wordBothC_{key}"], numbers[f"wordBothD_{key}"] = extra["C"], extra["D"]
        numbers[f"wordFlipC_{key}"], numbers[f"wordFlipD_{key}"] = eflip["C"], eflip["D"]
        numbers[f"wordOtherC_{key}"], numbers[f"wordOtherD_{key}"] = eother["C"], eother["D"]
        if shown(key): rows.append((key, " & ".join(cells) + " \\\\"))
        numbers[f"wordN_{key}"] = n
        numbers[f"wordBothACI_{key}"] = ci_pct(both["A"])
        numbers[f"wordBothBCI_{key}"] = ci_pct(both["B"])
    (TAB / "tab_wording.tex").write_text(WORD_HEADER + grouped(rows) + FOOTER, encoding="utf-8")

    # ---------------- Table 9: structured verification ----------------
    rows = []
    for key, name in POINTING_MODELS:
        vrec = load_jsonl(OUT / f"verify_{key}_actant-swap.jsonl")
        if len(vrec) < n_swap:
            continue
        probes = {r["valse_id"]: r for r in runs.get((key, "actant-swap"), []) if "pointing" in r}
        n = len(vrec)
        parsed = sum(r["parsed"] for r in vrec)
        first = sum(r["first_correct"] for r in vrec)
        strict = sum(r["strict_correct"] for r in vrec)
        either = sum(r["either_correct"] for r in vrec)
        cons = sum(r["consistent"] for r in vrec)
        both_s = sum(r["both_hit_first"] for r in vrec)
        pairs = [(float(r["strict_correct"]), float(r["both_hit_first"])) for r in vrec]
        fc = four_cell([r["strict_correct"] for r in vrec], [r["both_hit_first"] for r in vrec])
        npass = fc["foil+point+"] + fc["foil+point-"]
        cond = pct(fc["foil+point+"], npass)
        cond_ci = ci_pct(pairs, stat_cond)
        k = kappa([r["strict_correct"] for r in vrec], [r["both_hit_first"] for r in vrec])
        same = [probes[r["valse_id"]] for r in vrec if r["valse_id"] in probes]
        pair_same = pct(sum(p["foil"]["pair_correct"] for p in same), len(same))
        ind = [(float(p["foil"]["pair_correct"]), float(both_role(p))) for p in same]
        ind_pass = sum(1 for a, _ in ind if a)
        ind_cond = pct(sum(1 for a, b in ind if a and b), ind_pass)
        changed = pct(sum(1 for r in vrec if r["valse_id"] in probes and probes[r["valse_id"]]["foil"]["pair_correct"] != r["strict_correct"]), len(same))
        loc_v = [r for r in vrec if r["strict_correct"] and r["valse_id"] in probes and both_noun(probes[r["valse_id"]])]
        numbers[f"verCondLoc_{key}"] = pct(sum(r["both_hit_first"] for r in loc_v), len(loc_v)) if loc_v else "--"
        if shown(key) and parsed: rows.append((key, " & ".join([name, pct(parsed, n), pair_same, pct(first, n), pct(strict, n), pct(cons, n), pct(both_s, n),
                                sc(f"{cond} {cond_ci}"), f"{k:.2f}", ind_cond]) + " \\\\"))
        numbers[f"verN_{key}"] = n
        numbers[f"verParsed_{key}"] = pct(parsed, n)
        numbers[f"verPairSame_{key}"] = pair_same
        numbers[f"verFirst_{key}"] = pct(first, n)
        numbers[f"verStrict_{key}"] = pct(strict, n)
        numbers[f"verEither_{key}"] = pct(either, n)
        numbers[f"verCons_{key}"] = pct(cons, n)
        numbers[f"verBoth_{key}"] = pct(both_s, n)
        numbers[f"verCond_{key}"] = cond
        numbers[f"verCondCI_{key}"] = cond_ci
        numbers[f"verKappa_{key}"] = f"{k:.2f}"
        numbers[f"verIndepCond_{key}"] = ind_cond
        numbers[f"verChanged_{key}"] = changed
    (TAB / "tab_verify.tex").write_text(VER_HEADER + grouped(rows) + FOOTER, encoding="utf-8")

    # ---------------- ARO table: same probes on ARO VG-Relation items ----------------
    aro_rows: dict[str, list] = {}
    n_subs: dict[str, int] = {}
    for subset, label in [("aro-relation", "ARO relations"), ("aro-spatial", "ARO left/right")]:
        n_sub = len([1 for it in items.values() if it["subset"] == subset])
        n_subs[subset] = n_sub
        aro_rows[subset] = []
        for key, name in POINTING_MODELS:
            recs = [r for r in load_jsonl(OUT / f"probes_{key}_{subset}.jsonl") if "pointing" in r and r.get("foil")]
            if not recs or len(recs) < n_sub:
                continue
            n_subs[subset] = len(recs)  # the count of scored records (the joined ARO file carries duplicate ids)
            foil_ok = [r["foil"]["pair_correct"] for r in recs]
            crop_ok = [r["foil_crop"]["pair_correct"] for r in recs if "foil_crop" in r]
            both = [both_role(r) for r in recs]
            bn = [both_noun(r) for r in recs]
            pairs = [(float(a), float(b)) for a, b in zip(foil_ok, both)]
            fc = four_cell(foil_ok, both)
            npass = fc["foil+point+"] + fc["foil+point-"]
            bl = blindll_stats(key, recs, subset)
            ll = f"{100 * bl['acc']:.1f}" if bl and bl["n"] >= n_sub else "--"
            cond, cond_ci, k = pct(fc["foil+point+"], npass), ci_pct(pairs, stat_cond), kappa(foil_ok, both)
            if shown(key): aro_rows[subset].append((key, " & ".join([name, pct(sum(foil_ok), len(recs)),
                                    pct(sum(crop_ok), len(crop_ok)) if crop_ok else "--", ll, pct(sum(bn), len(bn)),
                                    pct(sum(both), len(both))] + (["--", "--"] if subset == "aro-spatial" else [sc(f"{cond} {cond_ci}"), sc(odds_ratio(fc))])) + " \\\\"))
            tag = subset.replace("aro-", "aro")
            numbers[f"aroOR_{tag}_{key}"] = odds_ratio(fc)
            numbers[f"aroN_{tag}_{key}"] = len(recs)
            numbers[f"aroPair_{tag}_{key}"] = pct(sum(foil_ok), len(recs))
            numbers[f"aroCrop_{tag}_{key}"] = pct(sum(crop_ok), len(crop_ok)) if crop_ok else "--"
            numbers[f"aroLL_{tag}_{key}"] = ll
            numbers[f"aroBothNoun_{tag}_{key}"] = pct(sum(bn), len(bn))
            numbers[f"aroBothRole_{tag}_{key}"] = pct(sum(both), len(both))
            numbers[f"aroCond_{tag}_{key}"] = cond
            numbers[f"aroCondCI_{tag}_{key}"] = cond_ci
            numbers[f"aroKappa_{tag}_{key}"] = f"{k:.2f}"
            st = controls_stats(key, recs, subset)
            if st and st["n_items"] >= n_sub:
                c, ncf = st["conflict"], st["n_conflict_eval"]
                numbers[f"aroCtlText_{tag}_{key}"] = pct(st["text_correct"], st["n_words"])
                numbers[f"aroCtlUncond_{tag}_{key}"] = pct(st["uncond_hit"], st["n_with_probe"])
                numbers[f"aroCtlCond_{tag}_{key}"] = pct(st["cond_hit"], st["n_words"])
                numbers[f"aroCtlNoun_{tag}_{key}"] = pct(st["noun_hit"], st["n_with_probe"])
                numbers[f"aroCtlConfImage_{tag}_{key}"] = pct(c["image"], ncf)
                numbers[f"aroCtlConfText_{tag}_{key}"] = pct(c["text"], ncf)
    for tag in ["arorelation", "arospatial"]:
        for key, _ in POINTING_MODELS:
            for t in ["aroN_", "aroPair_", "aroCrop_", "aroLL_", "aroBothNoun_", "aroBothRole_", "aroCond_", "aroCondCI_", "aroKappa_", "aroOR_",
                      "aroCtlText_", "aroCtlUncond_", "aroCtlCond_", "aroCtlNoun_", "aroCtlConfImage_", "aroCtlConfText_"]:
                numbers.setdefault(f"{t}{tag}_{key}", "--")
    aro_blocks = [f"\\multicolumn{{8}}{{@{{}}l}}{{\\emph{{{label} ($n={n_subs[subset]}$)}}}} \\\\\n\\addlinespace[2pt]\n" + grouped(aro_rows[subset])
                  for subset, label in [("aro-relation", "ARO relations"), ("aro-spatial", "ARO left/right")]]
    (TAB / "tab_aro.tex").write_text(
        header("@{}l F F F N R R r@{}",
               " & \\multicolumn{2}{c}{\\foilhead{Foil pass}} & \\foilhead{\\thead{Text\\\\alone}} & \\multicolumn{2}{c}{Both located} & "
               "\\rolehead{$P(\\mathrm{loc}\\mid\\mathrm{pass})$} & \\thead{Odds\\\\ratio} \\\\",
               "\\cmidrule(lr){2-3}\\cmidrule(lr){5-6}", "Model & image & crop & LL & noun & \\rolehead{role} & all items & (OR) \\\\")
        + "\n\\midrule\n".join(aro_blocks) + FOOTER, encoding="utf-8")

    # ---------------- IoU threshold sweep and centre-in-box (appendix) ----------------
    def discr(p, og):
        """Closer to the right participant than to the other one: for boxes, IoU with the own gold box above the IoU with
        the other participant's box and above zero; for points, inside the own box."""
        if "points_px" in p:
            return p["iou"] >= 0.5
        boxes = p.get("boxes_px") or []
        if not boxes:
            return False
        b = boxes[0]
        return iou(b, p["gold"]) > 0 and iou(b, p["gold"]) > iou(b, og)

    def nested(r):
        ga, gb = [p["gold"] for p in r["pointing"].values()]
        inter = max(0.0, min(ga[2], gb[2]) - max(ga[0], gb[0])) * max(0.0, min(ga[3], gb[3]) - max(ga[1], gb[1]))
        small = min((ga[2] - ga[0]) * (ga[3] - ga[1]), (gb[2] - gb[0]) * (gb[3] - gb[1]))
        return iou(ga, gb) >= 0.5 or (small > 0 and inter / small >= 0.9)

    crits = [("three", "IoU $\\geq$ 0.3", lambda p, og: p["iou"] >= 0.3), ("five", "IoU $\\geq$ 0.5", lambda p, og: p["iou"] >= 0.5),
             ("seven", "IoU $\\geq$ 0.7", lambda p, og: p["iou"] >= 0.7), ("centre", "centre in box", lambda p, og: bool(p["center_hit"])),
             ("discr", "closer to own", discr), ("discrnn", "closer, non-nested", discr)]
    rows = []
    base = {}
    for key, name in POINTING_MODELS:
        recs = [r for r in runs.get((key, "actant-swap"), []) if "pointing" in r and r.get("foil")]
        if not recs:
            continue
        is_point_model = any("points_px" in p["role_prompt"] for r in recs[:50] for p in r["pointing"].values())
        for tag, clabel, fn in crits:
            use = [r for r in recs if not (tag == "discrnn" and nested(r))]

            def og(r, w):  # the other participant's gold box
                return [p["gold"] for v, p in r["pointing"].items() if v != w][0]

            def tgt(r, w, p):  # the target record with its own gold attached
                return dict(p, gold=r["pointing"][w]["gold"])

            other_role = [fn(tgt(r, w, p["role_prompt"]), og(r, w)) for r in use for w, p in r["pointing"].items() if p["role"] != "agent"]
            other_noun = [fn(tgt(r, w, p["noun_prompt"]), og(r, w)) for r in use for w, p in r["pointing"].items() if p["role"] != "agent"]
            both = [all(fn(tgt(r, w, p["role_prompt"]), og(r, w)) for w, p in r["pointing"].items()) for r in use]
            foil_ok = [r["foil"]["pair_correct"] for r in use]
            fc = four_cell(foil_ok, both)
            npass = fc["foil+point+"] + fc["foil+point-"]
            if shown(key) and not is_point_model: rows.append((key, f"{name if tag == 'three' else ''} & {clabel} & {pct(sum(other_role), len(other_role))} & {pct(sum(other_noun), len(other_noun))} & "
                        f"{pct(sum(both), len(use))} & {pct(fc['foil+point+'], npass)} \\\\"))
            numbers[f"sweepOtherRole{tag}_{key}"] = pct(sum(other_role), len(other_role))
            numbers[f"sweepOtherNoun{tag}_{key}"] = pct(sum(other_noun), len(other_noun))
            numbers[f"sweepBoth{tag}_{key}"] = pct(sum(both), len(use))
            numbers[f"sweepN{tag}_{key}"] = len(use)
            numbers[f"sweepCond{tag}_{key}"] = pct(fc["foil+point+"], npass)
        if key == "qwen3vl-2b":  # no-look baselines on the other participant under each criterion
            for tag, clabel, _ in crits:
                hits = []
                for r in recs:
                    it = items[("actant-swap", r["valse_id"])]
                    W, H = it["width"], it["height"]
                    golds = {w: p["gold"] for w, p in r["pointing"].items()}
                    big = max(golds.values(), key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
                    for w, p in r["pointing"].items():
                        if p["role"] == "agent":
                            continue
                        if tag in ("discr", "discrnn"):
                            other_g = [g for v, g in golds.items() if v != w][0]
                            hits.append(iou(big, p["gold"]) > iou(big, other_g))
                            continue
                        if tag == "centre":
                            hits.append(point_in_box((W / 2, H / 2), p["gold"]))
                        else:
                            hits.append(iou(big, p["gold"]) >= {"three": 0.3, "five": 0.5, "seven": 0.7}[tag])
                base[tag] = pct(sum(hits), len(hits))
                numbers[f"sweepBase{tag}"] = base[tag]
    base_rows = [f"{'No-look baseline' if i == 0 else ''} & {clabel} & {base.get(tag, '--')} & {base.get(tag, '--')} & -- & -- \\\\"
                 for i, (tag, clabel, _) in enumerate(crits)]
    (TAB / "tab_iou_sweep.tex").write_text(
        header("@{}l l R N R R@{}",
               "Model & Hit criterion & \\thead{Other\\\\role} & \\thead{Other\\\\noun} & \\thead{Both\\\\role} & $P(\\mathrm{loc}\\mid\\mathrm{pass})$ \\\\")
        + grouped(rows, "3pt", by=lambda k: k) + "\n\\midrule\n\\addlinespace[3pt]\n" + "\n".join(base_rows) + FOOTER, encoding="utf-8")

    # ---------------- Joint-box control (both roles in one answer, no captions) ----------------
    rows = []
    for key, name in POINTING_MODELS:
        jrec = load_jsonl(OUT / f"jointbox_{key}_actant-swap.jsonl")
        if len(jrec) < n_swap:
            continue
        probes = {r["valse_id"]: r for r in runs.get((key, "actant-swap"), []) if "pointing" in r and r.get("foil")}
        pairs_j = [(r["valse_id"], r["both_hit"]) for r in jrec if r["valse_id"] in probes]
        same = [probes[v] for v, _ in pairs_j]
        joint = [float(b) for _, b in pairs_j]
        sep = [float(both_role(p)) for p in same]
        noun = [float(both_noun(p)) for p in same]
        foil_ok = [float(p["foil"]["pair_correct"]) for p in same]
        fc = four_cell([bool(x) for x in foil_ok], [bool(x) for x in joint])
        npass = fc["foil+point+"] + fc["foil+point-"]
        st = controls_stats(key, list(probes.values()))
        cond_ctl = pct(st["cond_both"], st["n_items"]) if st and st["n_items"] >= n_swap else "--"
        vrec = load_jsonl(OUT / f"verify_{key}_actant-swap.jsonl")
        ver_both = pct(sum(r["both_hit_first"] for r in vrec), len(vrec)) if len(vrec) >= n_swap else "--"
        loc_j = [j for f, j, nn in zip(foil_ok, joint, noun) if f and nn]
        cond_loc = pct(sum(loc_j), len(loc_j)) if loc_j else "--"
        if shown(key) and sum(joint): rows.append((key, " & ".join([name, pct(sum(sep), len(sep)), pct(sum(joint), len(joint)), cond_ctl, ver_both, pct(sum(noun), len(noun)),
                                sc(f"{pct(fc['foil+point+'], npass)} {ci_pct([(f, j) for f, j in zip(foil_ok, joint)], stat_cond)}"), cond_loc]) + " \\\\"))
        numbers[f"jointBoth_{key}"] = pct(sum(joint), len(joint))
        numbers[f"jointCond_{key}"] = pct(fc["foil+point+"], npass)
        numbers[f"jointCondCI_{key}"] = ci_pct([(f, j) for f, j in zip(foil_ok, joint)], stat_cond)
        numbers[f"jointSep_{key}"] = pct(sum(sep), len(sep))
        numbers[f"jointCondLoc_{key}"] = cond_loc
    (TAB / "tab_jointbox.tex").write_text(
        header("@{}lRRRRNRR@{}",
               " & \\multicolumn{4}{c}{Both located by role} & & \\multicolumn{2}{c}{\\thead{$P(\\mathrm{loc}\\mid\\mathrm{pass})$\\\\Joint, no captions}} \\\\",
               "\\cmidrule(lr){2-5}\\cmidrule(lr){7-8}",
               "Model & separate & joint & \\thead{Separate\\\\+caption} & \\thead{Joint\\\\+captions} & \\thead{Both\\\\by noun} & all items & localisable \\\\")
        + grouped(rows) + FOOTER, encoding="utf-8")

    # ---------------- Headline table for the main text ----------------
    rows = []
    for key, name in POINTING_MODELS:
        recs = [r for r in runs.get((key, "actant-swap"), []) if "pointing" in r and r.get("foil")]
        if not recs:
            continue
        foil_ok = [r["foil"]["pair_correct"] for r in recs]
        both = [both_role(r) for r in recs]
        bn = [both_noun(r) for r in recs]
        pairs = [(float(a), float(b)) for a, b in zip(foil_ok, both)]
        fc = four_cell(foil_ok, both)
        npass = fc["foil+point+"] + fc["foil+point-"]
        bl = blindll_stats(key, recs, "actant-swap")
        ll = f"{100 * bl['acc']:.1f}" if bl and bl["n"] >= n_swap else "--"
        # localisable items: both participants found by noun; the binding deficit net of the localisation ceiling
        loc = [(float(a), float(b)) for a, b, c in zip(foil_ok, both, bn) if c]
        loc_pass = [b for a, b in loc if a]
        cond_loc = pct(sum(loc_pass), len(loc_pass)) if loc_pass else "--"
        cond_loc_ci = ci_pct(loc, stat_cond) if loc_pass else ""
        numbers[f"condBothLoc_{key}"] = cond_loc
        numbers[f"condBothLocCI_{key}"] = cond_loc_ci
        numbers[f"nLoc_{key}"] = len(loc_pass)
        if shown(key): rows.append((key, " & ".join([name, pct(sum(foil_ok), len(recs)), ll, pct(sum(bn), len(bn)), pct(sum(both), len(both)),
                                sc(f"{pct(fc['foil+point+'], npass)} {ci_pct(pairs, stat_cond)}"), sc(f"{cond_loc} {cond_loc_ci}"), sc(odds_ratio(fc))]) + " \\\\"))
        numbers[f"or_{key}"] = odds_ratio(fc)
    (TAB / "tab_headline.tex").write_text(
        header("@{}l F F N R R R r@{}",
               " & \\foilhead{\\thead{Foil\\\\pass}} & \\foilhead{\\thead{Text\\\\alone}} & \\multicolumn{2}{c}{Both located} & "
               "\\multicolumn{2}{c}{\\rolehead{$P(\\mathrm{loc}\\mid\\mathrm{pass})$}} & \\thead{Odds\\\\ratio} \\\\",
               "\\cmidrule(lr){4-5}\\cmidrule(lr){6-7}", "Model & image & LL & noun & \\rolehead{role} & all items & localisable & (OR) \\\\")
        + grouped(rows) + FOOTER, encoding="utf-8")


    # agent pointing on the verb-replacement items (no swap, same images and prompts) next to the actant-swap agent rates
    rep_lines = [(key, f"{name} & {role} & {noun} & {numbers.get(f'pt_agent_role_{key}', '--')} & {numbers.get(f'pt_agent_noun_{key}', '--')} \\\\")
                 for name, n_rep, role, noun, key in rep_rows]
    (TAB / "tab_replacement.tex").write_text(
        header("@{}lRNRN@{}", " & \\multicolumn{2}{c}{Action replacement} & \\multicolumn{2}{c}{Actant swap} \\\\",
               "\\cmidrule(lr){2-3}\\cmidrule(lr){4-5}", "Model & agent by role & agent by noun & agent by role & agent by noun \\\\")
        + grouped(rep_lines) + FOOTER, encoding="utf-8")


    # ---------------- Two-box role probe (recognition format matched to the foil): appendix table ----------------
    rows = []
    for key, name in POINTING_MODELS:
        tb = load_jsonl(OUT / f"twobox_{key}_actant-swap.jsonl")
        if len(tb) < n_swap:
            continue
        probes = {r["valse_id"]: r for r in runs.get((key, "actant-swap"), []) if "pointing" in r and r.get("foil")}
        tb = [r for r in tb if r["valse_id"] in probes]
        nn = [r for r in tb if not r["nested"]]
        targets = [t for r in tb for t in r["targets"].values()]
        passed = [r for r in tb if probes[r["valse_id"]]["foil"]["pair_correct"]]
        loc = [r for r in passed if r["both_noun"]]
        cells = [name, str(len(tb)), pct(sum(t["role_correct"] for t in targets), len(targets)), pct(sum(t["noun_correct"] for t in targets), len(targets)),
                 pct(sum(r["both_role"] for r in tb), len(tb)), pct(sum(r["both_role"] for r in nn), len(nn)) if nn else "--",
                 pct(sum(r["both_noun"] for r in tb), len(tb)),
                 pct(sum(r["both_role"] for r in passed), len(passed)) if passed else "--",
                 pct(sum(r["both_role"] for r in loc), len(loc)) if loc else "--",
                 numbers.get(f"condBoth_{key}", "--"), numbers.get(f"condBothLoc_{key}", "--")]
        if shown(key): rows.append((key, " & ".join(cells[:1] + cells[2:]) + " \\\\"))  # the count goes into the caption
        for k, v in zip(("tbN_", "tbTargetRole_", "tbTargetNoun_", "tbBothRole_", "tbBothRoleNN_", "tbBothNoun_", "tbCond_", "tbCondLoc_"), cells[1:9]):
            numbers[f"{k}{key}"] = v
        numbers[f"tbNnn_{key}"] = len(nn)
    (TAB / "tab_twobox.tex").write_text(
        header("@{}lRNRRNRRRR@{}",
               " & \\multicolumn{2}{c}{Per target} & \\multicolumn{3}{c}{Both participants} & "
               "\\multicolumn{2}{c}{\\thead{$P(\\mathrm{both\\ role}\\mid\\mathrm{pass})$\\\\Two-box probe}} & "
               "\\multicolumn{2}{c}{\\thead{$P(\\mathrm{loc}\\mid\\mathrm{pass})$\\\\Box probe}} \\\\",
               "\\cmidrule(lr){2-3}\\cmidrule(lr){4-6}\\cmidrule(lr){7-8}\\cmidrule(lr){9-10}",
               "Model & role & noun & role & \\thead{Role,\\\\non-nested} & noun & all & localisable & all & localisable \\\\")
        + grouped(rows) + FOOTER, encoding="utf-8")

    # ---------------- Role-miss decomposition (appendix): what a role box does when it is not a hit ----------------
    def decompose(r: dict) -> list[str]:
        """One label per role target: hit, swap (box on the other participant), collapse (the two role prompts got the
        same box), extent (overlaps its own participant but IoU below 0.5), else (box elsewhere), nobox."""
        words = list(r["pointing"])
        if len(words) != 2:
            return []
        boxes = {w: (r["pointing"][w]["role_prompt"].get("boxes_px") or [None])[0] for w in words}
        pts = {w: (r["pointing"][w]["role_prompt"].get("points_px") or [None])[0] for w in words}
        out = []
        for w in words:
            other = words[1] if w == words[0] else words[0]
            p = r["pointing"][w]["role_prompt"]
            gold, gold_other = r["pointing"][w]["gold"], r["pointing"][other]["gold"]
            if pts[w] is not None:  # point model: inside own box = hit, inside the other = swap, else = else
                own = point_in_box(tuple(pts[w]), gold); oth = point_in_box(tuple(pts[other]), gold_other) if pts[other] else False
                out.append("hit" if own else ("swap" if point_in_box(tuple(pts[w]), gold_other) else "else"))
                continue
            b = boxes[w]
            if b is None:
                out.append("nobox"); continue
            if p["iou"] >= HIT:
                out.append("hit"); continue
            if iou(b, gold_other) >= HIT:
                out.append("swap"); continue
            if boxes[other] is not None and iou(b, boxes[other]) >= 0.8:
                out.append("collapse"); continue
            cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
            gx, gy = (gold[0] + gold[2]) / 2, (gold[1] + gold[3]) / 2
            if iou(b, gold) > 0 and (point_in_box((cx, cy), gold) or point_in_box((gx, gy), b)):
                out.append("extent"); continue
            out.append("else")
        return out

    rows = []
    for key, name in POINTING_MODELS:
        recs = [r for r in runs.get((key, "actant-swap"), []) if "pointing" in r and r.get("foil")]
        if not recs:
            continue
        labels, exchanged = [], 0
        for r in recs:
            lab = decompose(r)
            labels += lab
            if len(lab) == 2 and lab == ["swap", "swap"]:
                exchanged += 1
        nt = len(labels)
        cnt = Counter(labels)
        misses = nt - cnt["hit"]
        cells = [pct(cnt[k], nt) for k in ("hit", "swap", "collapse", "extent", "else", "nobox")]
        for k, lab in zip(("Hit", "Swap", "Collapse", "Extent", "Else", "NoBox"), ("hit", "swap", "collapse", "extent", "else", "nobox")):
            numbers[f"miss{k}_{key}"] = pct(cnt[lab], nt)
        numbers[f"missExchanged_{key}"] = pct(exchanged, len(recs))
        numbers[f"missSwapOfMiss_{key}"] = pct(cnt["swap"], misses) if misses else "--"
        if shown(key): rows.append((key, " & ".join([name] + cells + [pct(cnt["swap"], misses) if misses else "--", pct(exchanged, len(recs))]) + " \\\\"))
    (TAB / "tab_misses.tex").write_text(
        header("@{}lRrrrrrrr@{}", " & \\multicolumn{6}{c}{Role-prompt outcome (\\pc{} of targets)} & & \\\\", "\\cmidrule(lr){2-7}",
               "Model & hit & swap & collapse & extent & elsewhere & no box & \\thead{Swap among\\\\misses} & \\thead{Roles\\\\exchanged} \\\\")
        + grouped(rows) + FOOTER, encoding="utf-8")

    # ---------------- Example figures (Qwen 2B, one per agreement cell) ----------------
    recs = [r for r in runs.get(("qwen3vl-2b", "actant-swap"), []) if "pointing" in r]
    chosen = {}
    prefer = {"agent-victim", "agent-listener", "agent-student", "agent-coagent", "agent-target", "agent-item"}
    for r in recs:
        it = items[("actant-swap", r["valse_id"])]
        cell = ("F+" if r["foil"]["pair_correct"] else "F-") + ("P+" if both_role(r) else "P-")
        pr = "-".join(sorted(p["role"] for p in r["pointing"].values()))
        score = (pr in prefer) + (r["image_file"] in {"biting_394.jpg", "scolding_30.jpg"})
        if cell not in chosen or score > chosen[cell][0]:
            chosen[cell] = (score, r, it)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
    ex_lines = []
    for cell in ["F+P+", "F+P-", "F-P+", "F-P-"]:
        if cell not in chosen:
            continue
        _, r, it = chosen[cell]
        img = Image.open(DATA / "swig" / "images" / it["image_file"]).convert("RGB")
        draw = ImageDraw.Draw(img)
        legend = []
        W, H = img.size
        BLUE, ORANGE = (0, 114, 178), (230, 159, 0)
        try:
            tag_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", max(22, W // 14))
        except OSError:
            tag_font = font
        lw = max(5, W // 120)
        placed = []

        def tag(x, y, text, colour, below=False):
            bb = draw.textbbox((0, 0), text, font=tag_font)
            tw, th = bb[2] - bb[0] + 10, bb[3] - bb[1] + 8
            y0 = y - th if below else y
            x0, y0 = min(max(0, x), W - tw), min(max(0, y0), H - th)
            step = -(th + 3) if below else (th + 3)
            for _ in range(10):
                rect = (x0, y0, x0 + tw, y0 + th)
                if not any(not (rect[2] <= q[0] or q[2] <= rect[0] or rect[3] <= q[1] or q[3] <= rect[1]) for q in placed):
                    break
                y0 = min(max(0, y0 + step), H - th)
            placed.append((x0, y0, x0 + tw, y0 + th))
            draw.rectangle([x0, y0, x0 + tw, y0 + th], fill=colour)
            draw.text((x0 + 5, y0 + 2), text, fill="white", font=tag_font)

        for w, p in r["pointing"].items():
            g = p["gold"]
            draw.rectangle(g, outline=BLUE, width=lw)
            tag(g[0] + 2, g[1] + 2, w, BLUE)
        for w, p in r["pointing"].items():
            for b in p["role_prompt"]["boxes_px"][:1]:
                draw.rectangle(b, outline=ORANGE, width=lw)
                tag(b[0] + 2, b[3] - 2, f"{p['role']}?", ORANGE, below=True)
                legend.append(f"{p['role']}: IoU {p['role_prompt']['iou']:.2f}")
        fname = f"example_{cell.replace('+', 'p').replace('-', 'm')}.png"
        img.save(FIG / fname)
        ex_lines.append(
            f"\\textbf{{{cell}}} (\\texttt{{{tex_escape(it['image_file'])}}}): caption ``{tex_escape(it['caption'])}'', "
            f"foil ``{tex_escape(it['foil'])}''. Pairwise P(caption)={r['foil']['pair_p_caption']:.2f}, blind={r['foil']['blind_p_caption']:.2f}. "
            f"Role pointing: {tex_escape('; '.join(legend))}.")
        numbers[f"exfile_{cell.replace('+', 'p').replace('-', 'm')}"] = fname
    (TAB / "examples.tex").write_text("\n\n".join(ex_lines) + "\n", encoding="utf-8")

    # ---------------- Quantisation check (appendix): 4-bit laptop runs against bf16 runs of the same models ----------------
    quant_cols = ["pair_", "blindLL_", "ptBothNoun_", "ptBoth_", "condBoth_", "pt_other_role_", "pt_other_noun_", "verBoth_", "jointBoth_"]
    rows = []
    for key, name in [("qwen3vl-4b-4bit", "Qwen3-VL-4B, nf4"), ("qwen3vl-4b", "Qwen3-VL-4B, bf16"),
                      ("qwen3vl-8b-4bit", "Qwen3-VL-8B, nf4"), ("qwen3vl-8b", "Qwen3-VL-8B, bf16"),
                      ("qwen3vl-32b-4bit", "Qwen3-VL-32B, nf4"), ("qwen3vl-32b", "Qwen3-VL-32B, bf16")]:
        if numbers.get(f"pair_{key}", "--") == "--":
            continue
        rows.append((key, " & ".join([name] + [str(numbers.get(c + key, "--")) for c in quant_cols]) + " \\\\"))
    (TAB / "tab_quant.tex").write_text(
        header("@{}lFFNRRRNRR@{}",
               " & & & \\multicolumn{2}{c}{Both located} & & \\multicolumn{2}{c}{Other participant} & \\multicolumn{2}{c}{Both by role} \\\\",
               "\\cmidrule(lr){4-5}\\cmidrule(lr){7-8}\\cmidrule(lr){9-10}",
               "Model & \\thead{Foil\\\\passed} & \\foilhead{\\thead{Text\\\\alone}} & noun & role & \\thead{$P(\\mathrm{loc}$\\\\$\\mid\\mathrm{pass})$} & role & noun & structured & joint \\\\")
        + grouped(rows, by=lambda k: k.replace("-4bit", "")) + FOOTER, encoding="utf-8")

    # ---------------- ARO relations: which relations carry the role-noun gap (appendix; means over the open models) ----------------
    n_rel_items = len([1 for it in items.values() if it["subset"] == "aro-relation"])
    rel_stats: dict[str, dict[str, list]] = {}
    rel_n: Counter = Counter()
    rel_nested: dict[str, float] = {}
    n_models_rel = 0
    for key, name in POINTING_MODELS:
        recs = [r for r in load_jsonl(OUT / f"probes_{key}_aro-relation.jsonl") if "pointing" in r and r.get("foil")]
        if not shown(key) or len(recs) < n_rel_items:
            continue
        n_models_rel += 1
        by_rel: dict[str, list] = {}
        for r in recs:
            by_rel.setdefault(r["verb"], []).append(r)
        for rel, rs in by_rel.items():
            d = rel_stats.setdefault(rel, {"foil": [], "noun": [], "role": []})
            d["foil"].append(sum(r["foil"]["pair_correct"] for r in rs) / len(rs))
            d["noun"].append(sum(both_noun(r) for r in rs) / len(rs))
            d["role"].append(sum(both_role(r) for r in rs) / len(rs))
            if rel not in rel_n:
                rel_n[rel] = len(rs)
                rel_nested[rel] = sum(nested_pair(*[p["gold"] for p in r["pointing"].values()]) for r in rs) / len(rs)

    def mean(v):
        return sum(v) / len(v)

    REL_MIN = 15
    big = sorted([rel for rel in rel_n if rel_n[rel] >= REL_MIN], key=lambda rel: -(mean(rel_stats[rel]["noun"]) - mean(rel_stats[rel]["role"])))
    rows = []
    for rel in big:
        d = rel_stats[rel]
        gap = 100 * (mean(d["noun"]) - mean(d["role"]))
        rows.append(f"{rel} & {rel_n[rel]} & {100 * rel_nested[rel]:.0f} & {100 * mean(d['foil']):.1f} & {100 * mean(d['noun']):.1f} & {100 * mean(d['role']):.1f} & {gap:.1f} \\\\")
        slug = "".join(ch for ch in rel if ch.isalpha())
        numbers[f"relN_{slug}"] = rel_n[rel]
        numbers[f"relNested_{slug}"] = f"{100 * rel_nested[rel]:.0f}"
        numbers[f"relNoun_{slug}"] = f"{100 * mean(d['noun']):.1f}"
        numbers[f"relRole_{slug}"] = f"{100 * mean(d['role']):.1f}"
        numbers[f"relGap_{slug}"] = f"{gap:.1f}"
    rest = [rel for rel in rel_n if rel_n[rel] < REL_MIN]
    if rest:
        tot = sum(rel_n[r] for r in rest)
        w = lambda k: 100 * sum(mean(rel_stats[r][k]) * rel_n[r] for r in rest) / tot  # noqa: E731
        nest_rest = 100 * sum(rel_nested[r] * rel_n[r] for r in rest) / tot
        rows.append(f"\\addlinespace[2pt]\nother ({len(rest)} relations) & {tot} & {nest_rest:.0f} & {w('foil'):.1f} & {w('noun'):.1f} & {w('role'):.1f} & {w('noun') - w('role'):.1f} \\\\")
        numbers["relRestK"], numbers["relRestN"], numbers["relRestGap"] = len(rest), tot, f"{w('noun') - w('role'):.1f}"
    if len(big) >= 3:
        numbers["relRho"] = f"{spearman([rel_nested[r] for r in big], [mean(rel_stats[r]['noun']) - mean(rel_stats[r]['role']) for r in big]):.2f}"
    numbers["relNBig"], numbers["relMinN"], numbers["relModels"] = len(big), REL_MIN, n_models_rel
    (TAB / "tab_aro_relations.tex").write_text(
        header("@{}lrrFNRr@{}", "Relation & $n$ & \\thead{Nested\\\\pairs (\\pc)} & \\thead{Foil\\\\passed} & \\thead{Both\\\\by noun} & \\thead{Both\\\\by role} & \\thead{Gap\\\\(noun$-$role)} \\\\")
        + "\n".join(rows) + FOOTER, encoding="utf-8")

    # ---------------- Target size: role and noun hits by relative gold-box area (appendix) ----------------
    def rel_area(b, it):
        return max(0.0, (b[2] - b[0]) * (b[3] - b[1])) / (it["width"] * it["height"])

    ref = [r for r in runs.get(("qwen3vl-2b", "actant-swap"), []) if "pointing" in r]
    areas = sorted(rel_area(p["gold"], items[("actant-swap", r["valse_id"])]) for r in ref for p in r["pointing"].values())
    rows = []
    if areas:
        t1, t2 = areas[len(areas) // 3], areas[2 * len(areas) // 3]  # pooled terciles, the same cut points for every model
        numbers["sizeTercOne"], numbers["sizeTercTwo"] = f"{100 * t1:.0f}", f"{100 * t2:.0f}"

        def terc(a):
            return 0 if a < t1 else (1 if a < t2 else 2)

        for key, name in POINTING_MODELS:
            recs = [r for r in runs.get((key, "actant-swap"), []) if "pointing" in r and r.get("foil")]
            if not recs:
                continue
            role = [[], [], []]
            noun = [[], [], []]
            small, large, cond_s, cond_n = [], [], [], []
            for r in recs:
                it = items[("actant-swap", r["valse_id"])]
                ps = list(r["pointing"].values())
                ar = [rel_area(p["gold"], it) for p in ps]
                for pp, a in zip(ps, ar):
                    role[terc(a)].append(pp["role_prompt"]["iou"] >= HIT)
                    noun[terc(a)].append(pp["noun_prompt"]["iou"] >= HIT)
                    (small if a <= min(ar) else large).append(pp["role_prompt"]["iou"] >= HIT)
                if r["foil"]["pair_correct"]:
                    (cond_s if terc(min(ar)) == 0 else cond_n).append(both_role(r))
            cells = [pct(sum(v), len(v)) for v in role] + [pct(sum(v), len(v)) for v in noun] + [
                pct(sum(small), len(small)), pct(sum(large), len(large)), pct(sum(cond_s), len(cond_s)), pct(sum(cond_n), len(cond_n))]
            for k, v in zip(("sizeRoleS_", "sizeRoleM_", "sizeRoleL_", "sizeNounS_", "sizeNounM_", "sizeNounL_",
                             "sizeRoleSmall_", "sizeRoleLarge_", "sizeCondSmall_", "sizeCondLarge_"), cells):
                numbers[k + key] = v
            numbers[f"sizeNCondSmall_{key}"], numbers[f"sizeNCondLarge_{key}"] = len(cond_s), len(cond_n)
            if shown(key):
                rows.append((key, " & ".join([name] + cells) + " \\\\"))
    (TAB / "tab_size.tex").write_text(
        header("@{}lRRRNNNRRRR@{}",
               " & \\multicolumn{3}{c}{Role hit by target size} & \\multicolumn{3}{c}{Noun hit by target size} & \\multicolumn{2}{c}{Role hit, target is the} & \\multicolumn{2}{c}{$P(\\mathrm{loc}\\mid\\mathrm{pass})$} \\\\",
               "\\cmidrule(lr){2-4}\\cmidrule(lr){5-7}\\cmidrule(lr){8-9}\\cmidrule(lr){10-11}",
               "Model & small & medium & large & small & medium & large & smaller & larger & \\thead{smaller box\\\\small} & other \\\\")
        + grouped(rows) + FOOTER, encoding="utf-8")

    # ---------------- External text-only LMs (reviewer check) and the common strata they define ----------------
    EXT_LMS = [("olmo2-7b", "OLMo-2-7B (text only)"), ("mistral-7b", "Mistral-7B (text only)")]
    SUBTAGS = [("actant-swap", "swap"), ("action-replacement", "rep"), ("aro-relation", "arorelation"), ("aro-spatial", "arospatial")]
    rows_a = []
    for key, name in POINTING_MODELS:  # the VLMs' own language models, from the macros computed above
        if not shown(key) or numbers.get(f"blindLL_{key}", "--") == "--":
            continue
        rows_a.append((key, " & ".join([name, numbers[f"blindLL_{key}"], str(numbers.get(f"blindLLTok_{key}", "--")), numbers[f"blindLLSolvable_{key}"],
                                        str(numbers.get(f"blindLLRep_{key}", "--")), str(numbers.get(f"aroLL_arorelation_{key}", "--")),
                                        str(numbers.get(f"aroLL_arospatial_{key}", "--"))]) + " \\\\"))
    ext_ref = None
    for lm, lname in EXT_LMS:
        cells = [lname]
        for subset, tag in SUBTAGS:
            st = blindll_stats(lm, [], subset)
            numbers[f"extLL_{lm}_{tag}"] = f"{100 * st['acc']:.1f}" if st else "--"
            numbers[f"extLLTok_{lm}_{tag}"] = f"{100 * st['acc_tok']:.1f}" if st and "acc_tok" in st else "--"
            numbers[f"extSolv_{lm}_{tag}"] = f"{100 * st['solvable']:.1f}" if st else "--"
            if subset == "actant-swap":
                cells += [numbers[f"extLL_{lm}_{tag}"], numbers[f"extLLTok_{lm}_{tag}"], numbers[f"extSolv_{lm}_{tag}"]]
            else:
                cells.append(numbers[f"extLL_{lm}_{tag}"])
        if numbers[f"extLL_{lm}_swap"] != "--":
            rows_a.append((lm, " & ".join(cells) + " \\\\"))
            ext_ref = ext_ref or (lm, lname)
    rows_b = []
    if ext_ref:
        lm, lname = ext_ref
        ext = {r["valse_id"]: r["margin"] for r in load_jsonl(OUT / f"blindll_{lm}_actant-swap.jsonl")}
        numbers["extRef"] = lname.replace(" (text only)", "")
        numbers["extBalN"] = sum(abs(m) <= BAL for m in ext.values())
        numbers["extSolvN"] = sum(m > BAL for m in ext.values())
        numbers["extFpN"] = sum(m < -BAL for m in ext.values())
        for key, name in POINTING_MODELS:
            recs = [r for r in runs.get((key, "actant-swap"), []) if "pointing" in r and r.get("foil") and r["valse_id"] in ext]
            if not recs:
                continue
            own = {r["valse_id"]: r["margin"] for r in load_jsonl(OUT / f"blindll_{key}_actant-swap.jsonl")}
            same = [_stratum_of(own[r["valse_id"]]) == _stratum_of(ext[r["valse_id"]]) for r in recs if r["valse_id"] in own]
            numbers[f"extSame_{key}"] = pct(sum(same), len(same))
            cells = [name]
            for sname, cond in (("Bal", lambda m: abs(m) <= BAL), ("Solv", lambda m: m > BAL), ("Fp", lambda m: m < -BAL)):
                rs = [r for r in recs if cond(ext[r["valse_id"]])]
                pairs = [(float(r["foil"]["pair_correct"]), float(both_role(r))) for r in rs]
                npass = sum(a for a, _ in pairs)
                foil = pct(npass, len(rs))
                condv = pct(sum(b for a, b in pairs if a), npass)
                numbers[f"ext{sname}Foil_{key}"], numbers[f"ext{sname}Cond_{key}"] = foil, condv
                if sname == "Bal":
                    foil_ci, cond_ci = (ci_pct([a for a, _ in pairs]), ci_pct(pairs, stat_cond)) if pairs else ("--", "--")
                    numbers[f"extBalFoilCI_{key}"], numbers[f"extBalCondCI_{key}"] = foil_ci, cond_ci
                    cells += [sc(f"{foil} {foil_ci}"), sc(f"{condv} {cond_ci}")]
                else:
                    cells += [foil, condv]
            cells.append(numbers[f"extSame_{key}"])
            if shown(key):
                rows_b.append((key, " & ".join(cells) + " \\\\"))
    (TAB / "tab_extlm.tex").write_text(
        header("@{}lrrrrrr@{}", "\\multicolumn{7}{@{}l}{\\textit{(a) Text-only preference for the caption, by language model}} \\\\", "\\addlinespace[2pt]",
               " & \\multicolumn{3}{c}{Actant swaps} & Replacements & ARO relations & Left/right \\\\", "\\cmidrule(lr){2-4}\\cmidrule(lr){5-5}\\cmidrule(lr){6-6}\\cmidrule(lr){7-7}",
               "Language model of & LL & LL/token & \\thead{margin\\\\$>$1 nat} & LL & LL & LL \\\\")
        + grouped(rows_a) + FOOTER + "\\par\\medskip\n"
        + header("@{}lrrrrrrr@{}", "\\multicolumn{8}{@{}l}{\\textit{(b) Agreement within the strata defined by the external language model}} \\\\", "\\addlinespace[2pt]",
                 " & \\multicolumn{2}{c}{Balanced} & \\multicolumn{2}{c}{Text-solvable} & \\multicolumn{2}{c}{Text favours the foil} & \\thead{Same stratum\\\\as own LM} \\\\",
                 "\\cmidrule(lr){2-3}\\cmidrule(lr){4-5}\\cmidrule(lr){6-7}",
                 "Model & \\thead{foil\\\\passed} & \\thead{$P(\\mathrm{loc}$\\\\$\\mid\\mathrm{pass})$} & \\thead{foil\\\\passed} & \\thead{$P(\\mathrm{loc}$\\\\$\\mid\\mathrm{pass})$} & "
                 "\\thead{foil\\\\passed} & \\thead{$P(\\mathrm{loc}$\\\\$\\mid\\mathrm{pass})$} & (\\pc) \\\\")
        + grouped(rows_b) + FOOTER, encoding="utf-8")

    # ---------------- Human ceiling on the role prompts: two annotators (an author; a colleague who is not), 200 targets of 100 items, blind to the gold ----------------
    ann_p, tgt_p = ROOT / "annotation" / "human_ceiling_annotations.json", ROOT / "annotation" / "human_ceiling_targets.json"
    rows = []
    human_row = ""
    if ann_p.exists() and tgt_p.exists():
        targets = {t["id"]: t for t in json.loads(tgt_p.read_text(encoding="utf-8"))}
        raw = json.loads(ann_p.read_text(encoding="utf-8"))
        ann = {k: v for k, v in raw.get("annotations", raw).items() if k in targets}
        hc_items: dict[str, dict] = {}
        for k, t in targets.items():
            hc_items.setdefault(k.split("::")[0], {})[k.split("::")[1]] = t
        keys = [k for k in targets if ann.get(k, {}).get("box")]  # targets the annotator boxed; the models are scored on the same ones
        items_hc = [vid for vid, ws in hc_items.items() if all(f"{vid}::{w}" in keys for w in ws)]

        def other_gold(k):
            vid, w = k.split("::")
            return [t["gold"] for ww, t in hc_items[vid].items() if ww != w][0]

        def hc_rates(get):
            """get(target id) -> ("box", box) | ("point", (x, y)) | None. Per-target rates and per-item both-located rates."""
            hit = cen = dis = swp = 0
            for k in keys:
                g, o = targets[k]["gold"], other_gold(k)
                r = get(k)
                if r is None:
                    continue
                kind, v = r
                if kind == "point":
                    i, io = point_in_box(v, g), point_in_box(v, o)
                    hit += i; cen += i; dis += i; swp += io and not i
                else:
                    ig, io, c = iou(v, g), iou(v, o), box_center(v)
                    hit += ig >= HIT; cen += point_in_box(c, g); dis += ig > 0 and ig > io
                    swp += ig < HIT and (io >= HIT or (point_in_box(c, o) and not point_in_box(c, g)))

            def both(crit):
                n_ok = 0
                for vid in items_hc:
                    ok = True
                    for w in hc_items[vid]:
                        k = f"{vid}::{w}"
                        r, g = get(k), targets[k]["gold"]
                        if r is None:
                            ok = False
                            break
                        kind, v = r
                        ok = ok and (point_in_box(v, g) if kind == "point" else (iou(v, g) >= HIT if crit == "iou" else point_in_box(box_center(v), g)))
                    n_ok += ok
                return pct(n_ok, len(items_hc))
            n = len(keys)
            return [pct(hit, n), pct(cen, n), pct(dis, n), pct(swp, n), both("iou"), both("centre")]

        hum = hc_rates(lambda k: ("box", ann[k]["box"]))
        for name, v in zip(("humanIoU", "humanCentre", "humanDiscr", "humanSwap", "humanBothIoU", "humanBothCentre"), hum):
            numbers[name] = v
        # second annotator, not an author, same tool and targets; a "cannot tell" or unannotated target counts as a miss,
        # as a model's missing box does, so every row of the table has the same denominator
        ann2_p = ROOT / "annotation" / "human_ceiling_annotations_annotator2.json"
        hum2 = None
        if ann2_p.exists():
            raw2 = json.loads(ann2_p.read_text(encoding="utf-8"))
            ann2 = {k: v for k, v in raw2.get("annotations", raw2).items() if k in targets}
            hum2 = hc_rates(lambda k: ("box", ann2[k]["box"]) if ann2.get(k, {}).get("box") else None)
            for name, v in zip(("humanTwoIoU", "humanTwoCentre", "humanTwoDiscr", "humanTwoSwap", "humanTwoBothIoU", "humanTwoBothCentre"), hum2):
                numbers[name] = v
            boxed2 = [k for k in keys if ann2.get(k, {}).get("box")]
            numbers["humanTwoBoxed"] = len(boxed2)
            numbers["humanTwoCannot"] = sum(1 for k in keys if k in ann2 and not ann2[k].get("box"))
            numbers["humanTwoMissing"] = sum(1 for k in keys if k not in ann2)
            numbers["humanTwoIoUBoxed"] = pct(sum(iou(ann2[k]["box"], targets[k]["gold"]) >= HIT for k in boxed2), len(boxed2))
            numbers["humanTwoCentreBoxed"] = pct(sum(point_in_box(box_center(ann2[k]["box"]), targets[k]["gold"]) for k in boxed2), len(boxed2))
            for role in ("agent", "other"):
                ks = [k for k in boxed2 if (targets[k]["role"] == "agent") == (role == "agent")]
                numbers[f"humanTwo{role.capitalize()}IoU"] = pct(sum(iou(ann2[k]["box"], targets[k]["gold"]) >= HIT for k in ks), len(ks))
            # agreement between the two annotators on the targets both boxed
            h1 = [iou(ann[k]["box"], targets[k]["gold"]) >= HIT for k in boxed2]
            h2 = [iou(ann2[k]["box"], targets[k]["gold"]) >= HIT for k in boxed2]
            c1 = [point_in_box(box_center(ann[k]["box"]), targets[k]["gold"]) for k in boxed2]
            c2 = [point_in_box(box_center(ann2[k]["box"]), targets[k]["gold"]) for k in boxed2]

            def _kappa(a, b):
                n = len(a)
                po = sum(x == y for x, y in zip(a, b)) / n
                pe = (sum(a) / n) * (sum(b) / n) + (1 - sum(a) / n) * (1 - sum(b) / n)
                return (po - pe) / (1 - pe) if pe < 1 else 1.0

            numbers["humanAgreeN"] = len(boxed2)
            numbers["humanAgreeBox"] = pct(sum(iou(ann[k]["box"], ann2[k]["box"]) >= HIT for k in boxed2), len(boxed2))
            numbers["humanMeanIoU"] = f"{sum(iou(ann[k]['box'], ann2[k]['box']) for k in boxed2) / len(boxed2):.2f}"
            numbers["humanAgreeHit"] = pct(sum(x == y for x, y in zip(h1, h2)), len(boxed2))
            numbers["humanKappaHit"] = f"{_kappa(h1, h2):.2f}"
            numbers["humanAgreeCentre"] = pct(sum(x == y for x, y in zip(c1, c2)), len(boxed2))
            numbers["humanKappaCentre"] = f"{_kappa(c1, c2):.2f}"
            # the same participant: both centres inside the same gold box (own or other)
            same = 0
            for k in boxed2:
                g, o = targets[k]["gold"], other_gold(k)
                p1, p2 = box_center(ann[k]["box"]), box_center(ann2[k]["box"])
                same += (point_in_box(p1, g) and point_in_box(p2, g)) or (point_in_box(p1, o) and point_in_box(p2, o) and not point_in_box(p1, g) and not point_in_box(p2, g))
            numbers["humanSameParticipant"] = pct(same, len(boxed2))
        numbers["humanN"], numbers["humanItems"] = len(keys), len(items_hc)
        numbers["humanCannot"] = sum(1 for k in targets if k in ann and not ann[k].get("box"))
        numbers["humanMissing"] = sum(1 for k in targets if k not in ann)
        for role in ("agent", "other"):
            ks = [k for k in keys if (targets[k]["role"] == "agent") == (role == "agent")]
            numbers[f"human{role.capitalize()}IoU"] = pct(sum(iou(ann[k]["box"], targets[k]["gold"]) >= HIT for k in ks), len(ks))
        human_row = "Human, author & " + " & ".join(hum) + " \\\\\n"
        if hum2 is not None:
            human_row += "Human, not an author & " + " & ".join(hum2) + " \\\\\n"
        human_row += "\\midrule\n"
        for key, name in POINTING_MODELS:
            P: dict[str, tuple | None] = {}
            for r in runs.get((key, "actant-swap"), []):
                if r["valse_id"] not in hc_items or "pointing" not in r:
                    continue
                for w, pp in r["pointing"].items():
                    rp = pp["role_prompt"]
                    if "points_px" in rp:
                        P[f"{r['valse_id']}::{w}"] = ("point", tuple(rp["points_px"][0])) if rp["points_px"] else None
                    else:
                        P[f"{r['valse_id']}::{w}"] = ("box", rp["boxes_px"][0]) if rp.get("boxes_px") else None
            if not P:
                continue
            vals = hc_rates(lambda k: P.get(k))
            for t, v in zip(("hcIoU_", "hcCentre_", "hcDiscr_", "hcSwap_", "hcBothIoU_", "hcBothCentre_"), vals):
                numbers[t + key] = v
            if shown(key):
                rows.append((key, " & ".join([name] + vals) + " \\\\"))
    (TAB / "tab_human.tex").write_text(
        header("@{}lRRRRRR@{}", " & \\multicolumn{4}{c}{Per target (\\pc)} & \\multicolumn{2}{c}{Both participants per item (\\pc)} \\\\",
               "\\cmidrule(lr){2-5}\\cmidrule(lr){6-7}",
               "Annotator or model & IoU $\\geq 0.5$ & \\thead{centre\\\\in box} & \\thead{closer to\\\\own} & \\thead{on the other\\\\participant} & IoU $\\geq 0.5$ & \\thead{centre\\\\in box} \\\\")
        + human_row + grouped(rows) + FOOTER, encoding="utf-8")

    # ---------------- Length-matched noun controls on the wording sample (scripts/run_wording.py --set noun) ----------------
    # E = "the <noun> that can be seen in this picture" (as long as a role phrase), F = "the one that is the <noun>" (the frame
    # of the agent phrase). Scored against the plain noun prompt of the main run and role phrasing A on the same items.
    rows = []
    for key, name in POINTING_MODELS:
        nrec = load_jsonl(OUT / f"wording_noun_{key}_actant-swap.jsonl")
        wrec = {r["valse_id"]: r for r in load_jsonl(OUT / f"wording_{key}_actant-swap.jsonl")}
        if len(nrec) < 200 or len(wrec) < 200:
            continue
        probes = {r["valse_id"]: r for r in runs.get((key, "actant-swap"), []) if "pointing" in r}
        other = {k: [] for k in ("noun", "E", "F", "A")}
        both = {k: [] for k in ("noun", "E", "F", "A")}
        for r in nrec:
            pr, wa = probes.get(r["valse_id"]), wrec.get(r["valse_id"])
            if not pr or not wa:
                continue
            for w, d in r["words"].items():
                if d["role"] != "agent":
                    other["E"].append(float(d["E"]["iou"] >= HIT))
                    other["F"].append(float(d["F"]["iou"] >= HIT))
                    other["noun"].append(float(pr["pointing"][w]["noun_prompt"]["iou"] >= HIT))
                    other["A"].append(float(wa["words"][w]["A"]["iou"] >= HIT))
            both["E"].append(float(all(d["E"]["iou"] >= HIT for d in r["words"].values())))
            both["F"].append(float(all(d["F"]["iou"] >= HIT for d in r["words"].values())))
            both["noun"].append(float(both_noun(pr)))
            both["A"].append(float(all(d["A"]["iou"] >= HIT for d in wa["words"].values())))
        vals = [pct(sum(other[k]), len(other[k])) for k in ("noun", "E", "F", "A")] + [pct(sum(both[k]), len(both[k])) for k in ("noun", "E", "F", "A")]
        for t, v in zip(("nctlOtherNoun_", "nctlOtherE_", "nctlOtherF_", "nctlOtherA_", "nctlBothNoun_", "nctlBothE_", "nctlBothF_", "nctlBothA_"), vals):
            numbers[t + key] = v
        numbers[f"nctlN_{key}"] = len(both["E"])
        if shown(key):
            rows.append((key, " & ".join([name] + vals) + " \\\\"))
    (TAB / "tab_nounctl.tex").write_text(
        header("@{}lNNNRNNNR@{}", " & \\multicolumn{4}{c}{Other participant hit} & \\multicolumn{4}{c}{Both participants located} \\\\",
               "\\cmidrule(lr){2-5}\\cmidrule(lr){6-9}",
               "Model & noun & \\thead{noun,\\\\long} & \\thead{noun,\\\\framed} & role & noun & \\thead{noun,\\\\long} & \\thead{noun,\\\\framed} & role \\\\")
        + grouped(rows) + FOOTER, encoding="utf-8")

    # ---------------- Anchored role prompts on the ARO left/right items (scripts/run_anchored.py) ----------------
    # "the one that is to the left of the <other noun>": the relation plus the other participant, never the target's own noun.
    rows = []
    n_spatial = len([1 for it in items.values() if it["subset"] == "aro-spatial"])
    for key, name in POINTING_MODELS:
        arec = load_jsonl(OUT / f"anchored_{key}_aro-spatial.jsonl")
        if len(arec) < n_spatial:
            continue
        probes = {r["valse_id"]: r for r in load_jsonl(OUT / f"probes_{key}_aro-spatial.jsonl") if "pointing" in r and r.get("foil")}
        hits, both, pairs = [], [], []
        for r in arec:
            pr = probes.get(r["valse_id"])
            if not pr:
                continue
            h = [d["anchored"]["iou"] >= HIT for d in r["words"].values()]
            hits += h
            both.append(all(h))
            pairs.append((float(pr["foil"]["pair_correct"]), float(all(h))))
        if not both:
            continue
        fc = four_cell([bool(a) for a, _ in pairs], [bool(b) for _, b in pairs])
        npass = fc["foil+point+"] + fc["foil+point-"]
        numbers[f"anchN_{key}"] = len(both)
        numbers[f"anchTarget_{key}"] = pct(sum(hits), len(hits))
        numbers[f"anchBoth_{key}"] = pct(sum(both), len(both))
        numbers[f"anchCond_{key}"] = pct(fc["foil+point+"], npass)
        numbers[f"anchCondCI_{key}"] = ci_pct(pairs, stat_cond)
        if shown(key):
            rows.append((key, " & ".join([name, str(numbers.get(f"aroBothNoun_arospatial_{key}", "--")), str(numbers.get(f"aroBothRole_arospatial_{key}", "--")),
                                           numbers[f"anchTarget_{key}"], numbers[f"anchBoth_{key}"],
                                           sc(f"{numbers[f'anchCond_{key}']} {numbers[f'anchCondCI_{key}']}")]) + " \\\\"))
    (TAB / "tab_anchored.tex").write_text(
        header("@{}lNRRRR@{}", " & \\multicolumn{2}{c}{Both located} & \\multicolumn{2}{c}{Anchored role phrase} & \\\\",
               "\\cmidrule(lr){2-3}\\cmidrule(lr){4-5}",
               "Model & by noun & \\thead{generic\\\\role phrase} & \\thead{per\\\\target} & \\thead{both\\\\located} & \\thead{$P(\\mathrm{loc}\\mid\\mathrm{pass})$\\\\anchored} \\\\")
        + grouped(rows) + FOOTER, encoding="utf-8")

    # ---------------- numbers.tex (every expected macro, "--" when not available) ----------------
    for key, _ in POINTING_MODELS:
        for t in MODEL_KEYS:
            numbers.setdefault(t + key, "--")
    for key, _ in ENCODERS:
        numbers.setdefault("pairSwap_" + key, "--")
        numbers.setdefault("pairRep_" + key, "--")
    for t in ["chanceLargest_agent", "chanceLargest_other", "chanceFull_agent", "chanceFull_other", "chanceRandom_agent", "chanceRandom_other",
              "sweepBasethree", "sweepBasefive", "sweepBaseseven", "sweepBasecentre", "sizeTercOne", "sizeTercTwo",
              "relRho", "relNBig", "relMinN", "relModels", "relRestK", "relRestN", "relRestGap", "extRef", "extBalN", "extSolvN", "extFpN",
              "humanIoU", "humanCentre", "humanDiscr", "humanSwap", "humanBothIoU", "humanBothCentre", "humanN", "humanItems", "humanCannot",
              "humanMissing", "humanAgentIoU", "humanOtherIoU", "gaRows", "gaAgree", "gaKappa", "gaItems", "gaConfOne", "gaConfTwo",
              "gaConfBoth", "gaConfNeither", "gaItemAgree", "gaItemKappa", "nGoldOkBoth", "gaMaxDiff"]:
        numbers.setdefault(t, "--")
    for lm in ("olmo2-7b", "mistral-7b"):
        for tag in ("swap", "rep", "arorelation", "arospatial"):
            for t in ("extLL_", "extLLTok_", "extSolv_"):
                numbers.setdefault(f"{t}{lm}_{tag}", "--")

    def macro(k):  # LaTeX macro names: letters only
        digits = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
        return "".join(ch if ch.isalpha() else digits.get(ch, "") for ch in k)
    lines = [f"\\newcommand{{\\{macro(k)}}}{{{v}}}" for k, v in numbers.items()]
    (PAPER / "numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("tables:", sorted(p.name for p in TAB.glob("*.tex")))
    print("figures:", sorted(p.name for p in FIG.glob("*.png")))
    print(f"numbers: {len(numbers)} macros")


if __name__ == "__main__":
    main()
