"""Analyse probe outputs: foil accuracy, blind accuracy, pointing hit rates with chance
baselines, foil-versus-pointing agreement (four-cell tables, kappa), and a logistic
regression of foil success on pointing success and blind success.

Usage:
    uv run python scripts/analyze.py --model qwen3vl-2b
Reads outputs/probes_<model>_{actant-swap,action-replacement}.jsonl and, if present,
data/gold_check.jsonl (to report a clean-gold subset). Writes outputs/summary_<model>.md.
"""

from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from fvp.data import SUBSETS
from fvp.geometry import box_center, iou, point_in_box

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
HIT = 0.5


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in open(p, encoding="utf-8")] if p.exists() else []


def mean(xs) -> float:
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float("nan")


def pct(k: int, n: int) -> str:
    return f"{k}/{n} ({100.0 * k / n:.1f}%)" if n else "n/a"


def kappa(a: list[bool], b: list[bool]) -> float:
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def four_cell(foil: list[bool], point: list[bool]) -> dict:
    c = Counter((f, p) for f, p in zip(foil, point))
    return {"foil+point+": c[(True, True)], "foil+point-": c[(True, False)],
            "foil-point+": c[(False, True)], "foil-point-": c[(False, False)]}


def logistic(y: list[bool], X: list[list[float]], names: list[str]) -> str:
    try:
        import numpy as np
        from sklearn.linear_model import LogisticRegression
    except Exception:
        return "sklearn not installed"
    if len(set(y)) < 2:
        return "degenerate outcome"
    Xa, ya = np.array(X, dtype=float), np.array(y, dtype=int)
    m = LogisticRegression(max_iter=1000).fit(Xa, ya)
    acc = m.score(Xa, ya)
    base = max(ya.mean(), 1 - ya.mean())
    terms = ", ".join(f"{n}={c:+.2f}" for n, c in zip(names, m.coef_[0]))
    return f"coef: {terms}; intercept={m.intercept_[0]:+.2f}; fit acc {acc:.3f} vs majority {base:.3f}"


def chance_baselines(items_by_id: dict, recs: list[dict], seed=0, target: str = "all") -> dict:
    """Pointing baselines computed from gold boxes only. target: all | agent | other."""
    rng = random.Random(seed)
    full = center = largest = rand = other = 0
    n = 0
    for r in recs:
        it = items_by_id[(r["subset"], r["valse_id"])]
        W, H = it["width"], it["height"]
        roles = {w: r["pointing"][w]["gold"] for w in r["pointing"]}
        for w, gold in roles.items():
            is_agent = r["pointing"][w]["role"] == "agent"
            if (target == "agent" and not is_agent) or (target == "other" and is_agent):
                continue
            n += 1
            full += iou([0, 0, W, H], gold) >= HIT
            center += point_in_box((W / 2, H / 2), gold)
            big = max(roles.values(), key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
            largest += iou(big, gold) >= HIT
            oth = [b for k, b in roles.items() if k != w]
            other += any(iou(b, gold) >= HIT for b in oth)
            hits = 0
            for _ in range(20):
                x1, x2 = sorted(rng.uniform(0, W) for _ in range(2))
                y1, y2 = sorted(rng.uniform(0, H) for _ in range(2))
                hits += iou([x1, y1, x2, y2], gold) >= HIT
            rand += hits / 20
    return {"n_targets": n, "full_image_box": full / n, "image_center_point": center / n,
            "largest_role_box": largest / n, "other_actant_box": other / n, "random_box": rand / n} if n else {}


def verb_match(answer: str, gold: str) -> tuple[bool, bool]:
    """(strict stem match, WordNet-synonym match)."""
    a = answer.lower().strip().strip(".").split()[0] if answer.strip() else ""
    stem = gold[:-3] if gold.endswith("ing") else gold
    strict = bool(a) and (a.startswith(stem[:4]) or stem.startswith(a[:4]))
    syn = strict
    try:
        import nltk
        nltk.data.path.append(r'C:' + chr(92) + 'tmp' + chr(92) + 'nltk_data')
        from nltk.corpus import wordnet as wn
        lem = wn.morphy(a, wn.VERB) or a
        glem = wn.morphy(gold, wn.VERB) or stem
        lemmas = {l.name().lower() for s in wn.synsets(glem, pos=wn.VERB) for l in s.lemmas()}
        syn = strict or (lem in lemmas)
    except Exception:
        pass
    return strict, syn


def analyse_swap(model: str, recs: list[dict], items_by_id: dict, gold_ok: set | None, title: str = "actant-swap") -> list[str]:
    L = [f"## {title} ({len(recs)} items)\n"]
    f = [r["foil"] for r in recs if r.get("foil")]
    n = len(f)
    L.append("| foil probe | correct |\n|---|---|")
    L.append(f"| P(yes) caption > P(yes) foil | {pct(sum(x['yes_correct'] for x in f), n)} |")
    L.append(f"| pairwise, order-debiased | {pct(sum(x['pair_correct'] for x in f), n)} |")
    L.append(f"| blind pairwise (no image) | {pct(sum(x['blind_correct'] for x in f), n)} |")
    L.append(f"| mean P(yes) caption / foil | {mean(x['p_yes_caption'] for x in f):.3f} / {mean(x['p_yes_foil'] for x in f):.3f} |")
    L.append(f"| yes-rate (P(yes)>0.5) caption / foil | {mean(x['p_yes_caption'] > 0.5 for x in f):.3f} / {mean(x['p_yes_foil'] > 0.5 for x in f):.3f} |")
    crop = [r["foil_crop"] for r in recs if "foil_crop" in r]
    if crop:
        L.append(f"| pairwise on the benchmark crop | {pct(sum(x['pair_correct'] for x in crop), len(crop))} |")
    L.append("")

    # verb probe
    vm = [verb_match(r["verb_probe"]["answer"], r["verb_probe"]["gold"]) for r in recs if "verb_probe" in r]
    if vm:
        L.append(f"Verb naming: strict {pct(sum(s for s, _ in vm), len(vm))}, WordNet-synonym {pct(sum(y for _, y in vm), len(vm))}\n")

    # pointing
    recs_p = [r for r in recs if "pointing" in r]
    if recs_p:
        by = defaultdict(list)
        for r in recs_p:
            for w, p in r["pointing"].items():
                kind = "agent" if p["role"] == "agent" else "other-actant"
                for pk in ["role_prompt", "noun_prompt"]:
                    by[(kind, pk)].append(p[pk])
        L.append("| pointing target | prompt | IoU>=0.5 | centre-in-box | mean IoU | no box |\n|---|---|---|---|---|---|")
        for (kind, pk), xs in sorted(by.items()):
            L.append(f"| {kind} | {pk} | {pct(sum(x['iou'] >= HIT for x in xs), len(xs))} | {pct(sum(x['center_hit'] for x in xs), len(xs))} | {mean(x['iou'] for x in xs):.3f} | {sum(not x['boxes_px'] for x in xs)} |")
        L.append("")
        for tgt in ["all", "agent", "other"]:
            cb = chance_baselines(items_by_id, recs_p, target=tgt)
            L.append(f"Chance baselines for pointing, targets={tgt} (IoU>=0.5 hit rate unless noted): " +
                     ", ".join(f"{k} {v:.3f}" if isinstance(v, float) else f"{k} {v}" for k, v in cb.items()))
        L.append("")

        # role-pair breakdown (role prompt, both actants hit)
        pair_hits = Counter()
        pair_n = Counter()
        for r in recs_p:
            pr = tuple(sorted(p["role"] for p in r["pointing"].values()))
            pair_n[pr] += 1
            pair_hits[pr] += all(p["role_prompt"]["iou"] >= HIT for p in r["pointing"].values())
        L.append("Both actants hit with role prompts, by role pair (top 8): " +
                 "; ".join(f"{'-'.join(k)} {pair_hits[k]}/{v}" for k, v in pair_n.most_common(8)) + "\n")

        # agreement
        def agreement_block(subset: list[dict], title: str, outcome: str = "pair_correct") -> None:
            subset = [r for r in subset if r.get("foil")]
            if not subset:
                return
            title = f"{title}, foil outcome = {outcome}"
            foil_ok = [r["foil"][outcome] for r in subset]
            blind_ok = [r["foil"]["blind_correct"] for r in subset]
            both_role = [all(p["role_prompt"]["iou"] >= HIT for p in r["pointing"].values()) for r in subset]
            agent_role = [any(p["role"] == "agent" and p["role_prompt"]["iou"] >= HIT for p in r["pointing"].values()) for r in subset]
            both_noun = [all(p["noun_prompt"]["iou"] >= HIT for p in r["pointing"].values()) for r in subset]
            L.append(f"### Agreement, {title} (n={len(subset)})\n")
            for name, pt in [("both actants, role prompt", both_role), ("agent only, role prompt", agent_role), ("both actants, noun prompt", both_noun)]:
                fc = four_cell(foil_ok, pt)
                L.append(f"- pointing = {name}: pointing hit {pct(sum(pt), len(pt))}; kappa(foil, pointing) = {kappa(foil_ok, pt):.3f}; cells {fc}")
            L.append(f"- kappa(foil, blind) = {kappa(foil_ok, blind_ok):.3f}; cells {four_cell(foil_ok, blind_ok)}")
            L.append("- logistic: foil_correct ~ pointing(both,role) + blind: " +
                     logistic(foil_ok, [[float(p), float(b)] for p, b in zip(both_role, blind_ok)], ["pointing", "blind"]))
            L.append("- logistic: foil_correct ~ pointing(agent,role) + blind: " +
                     logistic(foil_ok, [[float(p), float(b)] for p, b in zip(agent_role, blind_ok)], ["pointing", "blind"]) + "\n")

        for outcome in ["pair_correct", "yes_correct"]:
            agreement_block(recs_p, "all items", outcome)
            if gold_ok is not None:
                clean = [r for r in recs_p if r["valse_id"] in gold_ok]
                if len(clean) >= 20:
                    agreement_block(clean, "detector-verified gold only", outcome)
    return L


def analyse_replace(model: str, recs: list[dict]) -> list[str]:
    L = [f"## action-replacement ({len(recs)} items)\n"]
    recs = [r for r in recs if r.get("foil")]
    f = [r["foil"] for r in recs]
    n = len(recs)
    L.append("| foil probe | correct |\n|---|---|")
    L.append(f"| P(yes) caption > P(yes) foil | {pct(sum(x['yes_correct'] for x in f), n)} |")
    L.append(f"| pairwise, order-debiased | {pct(sum(x['pair_correct'] for x in f), n)} |")
    L.append(f"| blind pairwise (no image) | {pct(sum(x['blind_correct'] for x in f), n)} |")
    L.append(f"| mean P(yes) caption / foil | {mean(x['p_yes_caption'] for x in f):.3f} / {mean(x['p_yes_foil'] for x in f):.3f} |\n")
    recs_p = [r for r in recs if "pointing" in r]
    if recs_p:
        for pk in ["role_prompt", "noun_prompt"]:
            xs = [r["pointing"]["__agent__"][pk] for r in recs_p]
            L.append(f"- agent pointing, {pk}: IoU>=0.5 {pct(sum(x['iou'] >= HIT for x in xs), len(xs))}, mean IoU {mean(x['iou'] for x in xs):.3f}")
        foil_ok = [r["foil"]["pair_correct"] for r in recs_p]
        blind_ok = [r["foil"]["blind_correct"] for r in recs_p]
        pt = [r["pointing"]["__agent__"]["role_prompt"]["iou"] >= HIT for r in recs_p]
        L.append(f"- kappa(foil, agent pointing) = {kappa(foil_ok, pt):.3f}; cells {four_cell(foil_ok, pt)}")
        L.append(f"- kappa(foil, blind) = {kappa(foil_ok, blind_ok):.3f}; cells {four_cell(foil_ok, blind_ok)}")
        L.append("- logistic: foil_correct ~ pointing + blind: " +
                 logistic(foil_ok, [[float(p), float(b)] for p, b in zip(pt, blind_ok)], ["pointing", "blind"]) + "\n")
    return L


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3vl-2b")
    args = ap.parse_args()
    items_by_id = {}
    for subset in SUBSETS:
        for it in load_jsonl(DATA / "joined" / f"{subset}.valid.jsonl"):
            items_by_id[(subset, it["valse_id"])] = it
    gold_ok = None
    gc = load_jsonl(DATA / "gold_check.jsonl")
    if gc:
        gold_ok = {r["valse_id"] for r in gc if all(w["flag"] == "ok" for w in r["words"].values())}
    lines = [f"# Summary for {args.model}\n"]
    if gold_ok is not None:
        lines.append(f"Gold check available: {len(gold_ok)} of {len(gc)} checked actant-swap items have both actant boxes confirmed by Grounding DINO.\n")
    swap = load_jsonl(OUT / f"probes_{args.model}_actant-swap.jsonl")
    rep = load_jsonl(OUT / f"probes_{args.model}_action-replacement.jsonl")
    if swap:
        lines += analyse_swap(args.model, swap, items_by_id, gold_ok)
    if rep:
        lines += analyse_replace(args.model, rep)
    for subset in ["aro-relation", "aro-spatial"]:
        recs = load_jsonl(OUT / f"probes_{args.model}_{subset}.jsonl")
        if recs:
            lines += analyse_swap(args.model, recs, items_by_id, None, title=subset)
    text = "\n".join(lines) + "\n"
    (OUT / f"summary_{args.model}.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Controls (scripts/run_controls.py): text-only role resolution, conditioned and conflict pointing
# ---------------------------------------------------------------------------
POINT_TAG = re.compile(r'x\d*="([\d.]+)"\s+y\d*="([\d.]+)"')


def rescore_control_points(recs: list[dict], subset: str) -> None:
    """Point-output models (Molmo): controls written before scripts/run_controls.py scored points carry the answer
    only in "raw" (percent coordinates) and no boxes. Re-score in place as the pointing probe does: a hit is a point
    inside the gold box, recorded as iou 1.0/0.0."""
    def unscored(e: dict) -> bool:
        return not e.get("boxes_px") and "points_px" not in e and bool(POINT_TAG.search(e.get("raw") or ""))
    if not any(unscored(d[k]) for r in recs for d in r["words"].values() for k in ("conditioned", "conflict")):
        return
    from PIL import Image
    from fvp.data import image_path
    items = {it["valse_id"]: it for it in load_jsonl(DATA / "joined" / f"{subset}.valid.jsonl")}
    for r in recs:
        it = items.get(r["valse_id"])
        if it is None:
            continue
        W, H = (it["width"], it["height"]) if it.get("width") else Image.open(image_path(it)).size
        for d in r["words"].values():
            for k in ("conditioned", "conflict"):
                e = d[k]
                if not unscored(e):
                    continue
                pts = [(float(x) / 100.0 * W, float(y) / 100.0 * H) for x, y in POINT_TAG.findall(e["raw"])]
                e["points_px"] = pts
                g = any(point_in_box(p, d["gold"]) for p in pts)
                o = any(point_in_box(p, d["gold_other"]) for p in pts)
                e["iou_gold"], e["iou_other"] = float(g), float(o)
                if k == "conditioned":
                    e["hit"] = g
                else:
                    e["class"] = {(True, False): "image", (False, True): "text", (True, True): "both"}.get((g, o), "neither")


def controls_stats(model: str, probes: list[dict] | None = None, subset: str = "actant-swap") -> dict | None:
    recs = load_jsonl(OUT / f"controls_{model}_{subset}.jsonl")
    if not recs:
        return None
    rescore_control_points(recs, subset)
    probe_by_id = {r["valse_id"]: r for r in (probes or []) if "pointing" in r}
    st = {"n_items": len(recs), "n_words": 0, "text_correct": 0, "text_correct_agent": 0, "n_agent": 0,
          "text_correct_other": 0, "n_other": 0,
          "cond_hit": 0, "cond_hit_agent": 0, "cond_hit_other": 0,
          "uncond_hit": 0, "noun_hit": 0, "n_with_probe": 0,
          "conflict": Counter(), "n_conflict_eval": 0, "n_nested": 0,
          "text_ok_uncond_fail": 0, "text_ok": 0,
          "cond_both": 0, "uncond_both": 0, "n_items_with_probe": 0}
    for r in recs:
        pr = probe_by_id.get(r["valse_id"])
        if pr:
            st["n_items_with_probe"] += 1
            st["uncond_both"] += all(p["role_prompt"]["iou"] >= HIT for p in pr["pointing"].values())
        st["cond_both"] += all(d["conditioned"]["hit"] for d in r["words"].values())
        for w, d in r["words"].items():
            st["n_words"] += 1
            is_agent = d["role"] == "agent"
            st["n_agent" if is_agent else "n_other"] += 1
            tc = d["text_resolution"]["correct"]
            st["text_correct"] += tc
            st["text_correct_agent" if is_agent else "text_correct_other"] += tc
            st["cond_hit"] += d["conditioned"]["hit"]
            st["cond_hit_agent" if is_agent else "cond_hit_other"] += d["conditioned"]["hit"]
            nested = iou(d["gold"], d["gold_other"]) >= HIT
            if nested:
                st["n_nested"] += 1
            else:
                st["n_conflict_eval"] += 1
                st["conflict"][d["conflict"]["class"]] += 1
            if pr and w in pr["pointing"]:
                st["n_with_probe"] += 1
                u = pr["pointing"][w]["role_prompt"]["iou"] >= HIT
                st["uncond_hit"] += u
                st["noun_hit"] += pr["pointing"][w]["noun_prompt"]["iou"] >= HIT
                if tc:
                    st["text_ok"] += 1
                    st["text_ok_uncond_fail"] += (not u)
    return st


def analyse_controls(model: str, probes: list[dict], subset: str = "actant-swap") -> list[str]:
    st = controls_stats(model, probes, subset)
    if not st:
        return []
    L = [f"## controls, {subset} ({st['n_items']} items, {st['n_words']} role targets)\n"]
    L.append(f"- text-only role resolution correct: {pct(st['text_correct'], st['n_words'])} "
             f"(agent {pct(st['text_correct_agent'], st['n_agent'])}, other {pct(st['text_correct_other'], st['n_other'])})")
    L.append(f"- pointing hit, role prompt: unconditioned {pct(st['uncond_hit'], st['n_with_probe'])} | "
             f"caption-conditioned {pct(st['cond_hit'], st['n_words'])} | noun prompt {pct(st['noun_hit'], st['n_with_probe'])}")
    L.append(f"- caption-conditioned by target: agent {pct(st['cond_hit_agent'], st['n_agent'])}, other {pct(st['cond_hit_other'], st['n_other'])}")
    L.append(f"- both participants by role: unconditioned {pct(st['uncond_both'], st['n_items_with_probe'])} | conditioned {pct(st['cond_both'], st['n_items'])}")
    L.append(f"- text resolved correctly but unconditioned pointing failed: {pct(st['text_ok_uncond_fail'], st['text_ok'])} of text-correct targets")
    c = st["conflict"]
    n = st["n_conflict_eval"]
    L.append(f"- conflict pointing (foil caption in prompt), non-nested targets n={n}: image-consistent {pct(c['image'], n)}, "
             f"text-following {pct(c['text'], n)}, both {pct(c['both'], n)}, neither {pct(c['neither'], n)}; nested pairs excluded: {st['n_nested']}\n")
    return L


def _main_with_controls():
    import sys as _sys
    argv = _sys.argv[1:]
    model = "qwen3vl-2b"
    if "--model" in argv:
        model = argv[argv.index("--model") + 1]
    lines = []
    for subset in SUBSETS:
        if subset == "action-replacement":
            continue
        lines += analyse_controls(model, load_jsonl(OUT / f"probes_{model}_{subset}.jsonl"), subset)
    if lines:
        p = OUT / f"summary_{model}.md"
        txt = p.read_text(encoding="utf-8") if p.exists() else ""
        txt = txt.split("\n## controls")[0].rstrip("\n") + "\n\n" + "\n".join(lines) + "\n"
        p.write_text(txt, encoding="utf-8")
        print("\n".join(lines))


if __name__ == "__main__":
    _main_with_controls()


# ---------------------------------------------------------------------------
# Likelihood blind baseline (scripts/run_blind_ll.py) and stratified agreement
# ---------------------------------------------------------------------------
BAL = 1.0  # |margin| <= BAL nats counts as 'balanced' (neither caption clearly more likely as text)


def _stratum(margin: float, t: float) -> str:
    return "solvable" if margin > t else ("foil_preferred" if margin < -t else "balanced")


def _token_counts(model: str, subset: str) -> dict[str, tuple[int, int]]:
    """valse_id -> (caption tokens, foil tokens) from scripts/token_counts.py; empty when not computed for this model."""
    return {r["valse_id"]: (r["n_caption"], r["n_foil"]) for r in load_jsonl(OUT / f"tokens_{model}.jsonl") if r["subset"] == subset}


def blindll_stats(model: str, probes: list[dict], subset: str = "actant-swap") -> dict | None:
    bl = load_jsonl(OUT / f"blindll_{model}_{subset}.jsonl")
    if not bl:
        return None
    by = {r["valse_id"]: r for r in bl}
    n = len(bl)
    st = {"n": n, "acc": sum(r["blind_ll_correct"] for r in bl) / n,
          "solvable": sum(r["margin"] > BAL for r in bl) / n,
          "foil_preferred": sum(r["margin"] < -BAL for r in bl) / n,
          "balanced": sum(abs(r["margin"]) <= BAL for r in bl) / n}
    # Length-normalised margin (mean log-probability per token): the summed margin favours the shorter string when the
    # caption and the foil differ in token count (about a fifth of the swap pairs differ by one token). The one-nat
    # threshold is carried over per token at the mean caption length (BAL / mean tokens).
    toks = _token_counts(model, subset)
    tok_margin: dict[str, float] = {}
    bal_tok = float("nan")
    if toks and all(v in toks for v in by):
        tok_margin = {v: r["ll_caption"] / toks[v][0] - r["ll_foil"] / toks[v][1] for v, r in by.items()}
        bal_tok = BAL / (sum(toks[v][0] for v in by) / n)
        st["acc_tok"] = sum(m > 0 for m in tok_margin.values()) / n
        st["bal_tok"] = bal_tok
        st["solvable_tok"] = sum(m > bal_tok for m in tok_margin.values()) / n
        st["moved_tok"] = sum(_stratum(by[v]["margin"], BAL) != _stratum(tok_margin[v], bal_tok) for v in by) / n
    # stratified agreement on items with two pointing targets
    if subset != "action-replacement":
        strata = {"solvable": [], "balanced": [], "foil_preferred": []}
        strata_tok = {"solvable": [], "balanced": [], "foil_preferred": []}
        for r in probes:
            if "pointing" not in r or r["valse_id"] not in by or not r.get("foil"):
                continue
            strata[_stratum(by[r["valse_id"]]["margin"], BAL)].append(r)
            if tok_margin:
                strata_tok[_stratum(tok_margin[r["valse_id"]], bal_tok)].append(r)
        for tag, groups in (("", strata), ("_tok", strata_tok)):
            for key, recs in groups.items():
                if not recs:
                    st[key + tag + "_n"] = 0
                    continue
                foil_ok = [r["foil"]["pair_correct"] for r in recs]
                both = [all(p["role_prompt"]["iou"] >= HIT for p in r["pointing"].values()) for r in recs]
                fc = four_cell(foil_ok, both)
                npass = fc["foil+point+"] + fc["foil+point-"]
                st[key + tag + "_n"] = len(recs)
                st[key + tag + "_foil_pass"] = sum(foil_ok) / len(recs)
                st[key + tag + "_point_both"] = sum(both) / len(recs)
                st[key + tag + "_cond"] = fc["foil+point+"] / npass if npass else float("nan")
                st[key + tag + "_cells"] = fc
    return st


def analyse_blindll(model: str, probes: list[dict] | None = None) -> list[str]:
    L = []
    for subset in SUBSETS:
        st = blindll_stats(model, load_jsonl(OUT / f"probes_{model}_{subset}.jsonl"), subset)
        if not st:
            continue
        L.append(f"## blind likelihood baseline, {subset} ({st['n']} items)\n")
        L.append(f"- caption more likely than foil (text only): {100*st['acc']:.1f}% | clearly text-solvable (margin > {BAL} nat): {100*st['solvable']:.1f}% | balanced: {100*st['balanced']:.1f}% | foil preferred: {100*st['foil_preferred']:.1f}%")
        if subset != "action-replacement":
            for key in ["solvable", "balanced", "foil_preferred"]:
                if st.get(key + "_n"):
                    L.append(f"- stratum {key} (n={st[key+'_n']}): foil pass {100*st[key+'_foil_pass']:.1f}%, both-by-role {100*st[key+'_point_both']:.1f}%, P(point | foil pass) {100*st[key+'_cond']:.1f}%, cells {st[key+'_cells']}")
        L.append("")
    return L


def _main_with_blindll():
    import sys as _sys
    argv = _sys.argv[1:]
    model = argv[argv.index("--model") + 1] if "--model" in argv else "qwen3vl-2b"
    probes = load_jsonl(OUT / f"probes_{model}_actant-swap.jsonl")
    lines = analyse_blindll(model, probes)
    if lines:
        p = OUT / f"summary_{model}.md"
        txt = p.read_text(encoding="utf-8") if p.exists() else ""
        txt = txt.split("\n## blind likelihood baseline")[0].rstrip("\n") + "\n\n" + "\n".join(lines) + "\n"
        p.write_text(txt, encoding="utf-8")
        print("\n".join(lines))


if __name__ == "__main__":
    _main_with_blindll()


# ---------------------------------------------------------------------------
# Bootstrap confidence intervals: item-level resampling, percentile method (95%)
# ---------------------------------------------------------------------------
N_BOOT = 2000


def boot_ci(rows, stat, n_boot: int = N_BOOT, seed: int = 0) -> tuple[float, float]:
    """`rows`: one entry per item (a number or a tuple of numbers); `stat(arr)` maps an (n, k) array to a float.
    Returns the 2.5 and 97.5 percentiles of `stat` over `n_boot` resamples of the items."""
    import numpy as np

    arr = np.asarray(rows, dtype=float)
    if arr.ndim == 1:
        arr = arr[:, None]
    n = len(arr)
    if n == 0:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    stats = np.array([stat(arr[i]) for i in idx], dtype=float)
    return float(np.nanpercentile(stats, 2.5)), float(np.nanpercentile(stats, 97.5))


def stat_rate(a) -> float:
    return float(a[:, 0].mean())


def stat_cond(a) -> float:
    """P(column 1 | column 0)."""
    m = a[:, 0] > 0
    return float(a[m, 1].mean()) if m.any() else float("nan")


def stat_kappa(a) -> float:
    x, y = a[:, 0] > 0, a[:, 1] > 0
    po = float((x == y).mean())
    px, py = float(x.mean()), float(y.mean())
    pe = px * py + (1 - px) * (1 - py)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def ci_pct(rows, stat=stat_rate, scale: float = 100.0, digits: int = 1) -> str:
    lo, hi = boot_ci(rows, stat)
    if lo != lo:
        return "--"
    return f"[{scale * lo:.{digits}f}, {scale * hi:.{digits}f}]"
