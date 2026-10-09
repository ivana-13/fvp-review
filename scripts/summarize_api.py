"""Compare an API model (scripts/run_api.py) with the open models on the same 200-item actant-swap sample.

    uv run python scripts/summarize_api.py --tag gemini31pro [--name "Gemini 3.1 Pro"]

Writes paper/tables/tab_api.tex and prints the rows. Every open model's numbers are recomputed on exactly the sampled
items, so the columns are comparable; the API model's foil pass is the strict two-order generated choice.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from analyze import HIT, load_jsonl, rescore_control_points  # noqa: E402
from run_wording import sample_items  # noqa: E402
from make_paper_assets import FOOTER, grouped, header  # noqa: E402

OUT, TAB = ROOT / "outputs", ROOT / "paper" / "tables"
OPEN = [("qwen3vl-2b", "Qwen3-VL-2B"), ("qwen3vl-4b", "Qwen3-VL-4B"), ("qwen3vl-8b", "Qwen3-VL-8B"), ("qwen3vl-32b", "Qwen3-VL-32B"),
        ("qwen3vl-235b", "Qwen3-VL-235B"),
        ("internvl35-2b", "InternVL3.5-2B"), ("internvl35-8b", "InternVL3.5-8B"), ("molmo-7b-d", "Molmo-7B-D (points)"),
        ("paligemma2-10b", "PaliGemma 2 10B")]


def pct(k, n):
    return f"{100 * k / n:.1f}" if n else "--"


def both(r, ph):
    return all(p[ph]["iou"] >= HIT for p in r["pointing"].values())


def row(key, name, ids):
    recs = [r for r in load_jsonl(OUT / f"probes_{key}_actant-swap.jsonl") if r["valse_id"] in ids and r.get("pointing")]
    if not recs:
        return None, {}
    passed = [r for r in recs if r["foil"]["pair_correct"]]
    loc = [r for r in passed if both(r, "noun_prompt")]
    st = {"n": len(recs), "pair": pct(len(passed), len(recs)),
          "blind": pct(sum(bool(r["foil"].get("blind_correct")) for r in recs), len(recs)),
          "yes": pct(sum(r["foil"]["yes_correct"] for r in recs), len(recs)),
          "bothNoun": pct(sum(both(r, "noun_prompt") for r in recs), len(recs)),
          "bothRole": pct(sum(both(r, "role_prompt") for r in recs), len(recs)),
          "cond": pct(sum(both(r, "role_prompt") for r in passed), len(passed)),
          "condLoc": pct(sum(both(r, "role_prompt") for r in loc), len(loc))}
    ctl = [c for c in load_jsonl(OUT / f"controls_{key}_actant-swap.jsonl") if c["valse_id"] in ids] if (OUT / f"controls_{key}_actant-swap.jsonl").exists() else []
    if ctl:
        rescore_control_points(ctl, "actant-swap")
        words = [d for c in ctl for d in c["words"].values()]
        conf = [d["conflict"]["class"] for d in words if d["conflict"].get("class")]
        st.update({"text": pct(sum(d["text_resolution"]["correct"] for d in words), len(words)),
                   "cond_hit": pct(sum(d["conditioned"]["hit"] for d in words), len(words)),
                   "confImage": pct(conf.count("image"), len(conf)), "confText": pct(conf.count("text"), len(conf))})
    else:
        st.update({"text": "--", "cond_hit": "--", "confImage": "--", "confText": "--"})
    cells = [name, st["pair"], st["blind"], st["bothNoun"], st["bothRole"], st["cond"], st["condLoc"], st["text"], st["cond_hit"], st["confImage"], st["confText"]]
    return " & ".join(cells) + " \\\\", st


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="gemini31pro")
    ap.add_argument("--name", default="Gemini 3.1 Pro (API)")
    ap.add_argument("--more", nargs="*", default=[], help="further API models as tag=name, e.g. claudeopus55='Claude Opus 5.5 (API)'")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    items = [json.loads(l) for l in open(ROOT / "data/joined/actant-swap.valid.jsonl", encoding="utf-8")]
    ids = {it["valse_id"] for it in sample_items(items, args.n, args.seed)}
    rows, stats = [], {}
    for key, name in OPEN + [(args.tag, args.name)] + [tuple(m.split("=", 1)) for m in args.more]:
        line, st = row(key, name, ids)
        if line:
            rows.append((key, line)); stats[key] = st
            print(line)
    head = header("@{}lFFNRRRrrrr@{}",
                  " & \\multicolumn{2}{c}{Foil passed} & \\multicolumn{2}{c}{Both located} & \\multicolumn{2}{c}{$P(\\mathrm{loc}\\mid\\mathrm{pass})$} & "
                  "\\multicolumn{2}{c}{Controls} & \\multicolumn{2}{c}{Conflict} \\\\",
                  "\\cmidrule(lr){2-3}\\cmidrule(lr){4-5}\\cmidrule(lr){6-7}\\cmidrule(lr){8-9}\\cmidrule(lr){10-11}",
                  "Model & image & blind & noun & role & all & localisable & \\thead{Text\\\\resolved} & +caption & image & text \\\\")
    TAB.mkdir(exist_ok=True)
    (TAB / "tab_api.tex").write_text(head + grouped(rows) + FOOTER, encoding="utf-8")
    (OUT / f"summary_api_{args.tag}.json").write_text(json.dumps(stats, indent=1), encoding="utf-8")
    print("written paper/tables/tab_api.tex")


if __name__ == "__main__":
    main()
