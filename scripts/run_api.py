"""The paper's probes through an OpenAI-compatible API (OpenRouter) for a closed or hosted model, on the fixed
200-item actant-swap sample of the wording check (same seed). Token probabilities are not available, so the foil
tests are generated answers: pairwise = A/B in both orders (pass when both orders choose the caption; pair_p_caption
is the share of orders that did), yes/no = generated Yes/No per sentence, blind A/B as in the paper. Pointing uses
Gemini's box convention ([ymin, xmin, ymax, xmax] on a 0-1000 grid); both readings are kept and the better one
(by noun-prompt IoU) is selected at the end of the run (--finalize), as the grid reading was for Qwen3-VL.

    uv run python scripts/run_api.py --model google/gemini-3.1-pro-preview --tag gemini31pro --limit 2   # smoke test
    uv run python scripts/run_api.py --model google/gemini-3.1-pro-preview --tag gemini31pro              # full sample
    uv run python scripts/run_api.py --tag gemini31pro --finalize                                          # pick the box reading

Writes outputs/probes_<tag>_actant-swap.jsonl and outputs/controls_<tag>_actant-swap.jsonl in the schema of
run_probes.py / run_controls.py, so analyze.py and make_paper_assets.py read them. The key is read from
OPENROUTER_API_KEY or C:/tmp/openrouter_key.txt(.txt). Resumable: items already written are skipped.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import random
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from fvp.data import image_path  # noqa: E402
from fvp.geometry import box_center, iou, point_in_box  # noqa: E402
from run_controls import mentions  # noqa: E402
from run_probes import role_phrase  # noqa: E402

DATA, OUT = ROOT / "data", ROOT / "outputs"
URL = "https://openrouter.ai/api/v1/chat/completions"
HIT = 0.5
BOX_PROMPT = ('Locate {target} in the image and output its bounding box in JSON format as '
              '[{{"box_2d": [ymin, xmin, ymax, xmax], "label": "..."}}], with coordinates on a 0-1000 scale.')
NUMS = re.compile(r"\[\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\]")
usage = {"prompt": 0, "completion": 0, "calls": 0, "errors": 0}
usage_lock = threading.Lock()


def read_key() -> str:
    k = os.environ.get("OPENROUTER_API_KEY")
    if k:
        return k.strip()
    for p in (Path("C:/tmp/openrouter_key.txt"), Path("C:/tmp/openrouter_key.txt.txt")):
        if p.exists():
            return p.read_text(encoding="utf-8").strip()
    raise SystemExit("no OpenRouter key: set OPENROUTER_API_KEY or create C:/tmp/openrouter_key.txt")


def data_url(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


class Client:
    def __init__(self, model: str, key: str, reasoning: str, timeout: float = 120.0):
        self.model, self.key, self.reasoning, self.timeout = model, key, reasoning, timeout
        self.session = requests.Session()

    def ask(self, prompt: str, img: Image.Image | None, max_tokens: int) -> str:
        content = [{"type": "text", "text": prompt}]
        if img is not None:
            content = [{"type": "image_url", "image_url": {"url": data_url(img)}}] + content
        body = {"model": self.model, "messages": [{"role": "user", "content": content}],
                "max_tokens": max_tokens, "temperature": 0}
        if self.reasoning:
            body["reasoning"] = {"effort": self.reasoning}
        last = ""
        for attempt in range(5):
            try:
                r = self.session.post(URL, headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json",
                                                    "HTTP-Referer": "https://anonymous.4open.science",
                                                    "X-Title": "foils-vs-pointing"},
                                      json=body, timeout=self.timeout)
                if r.status_code == 200:
                    j = r.json()
                    u = j.get("usage") or {}
                    with usage_lock:
                        usage["prompt"] += u.get("prompt_tokens", 0) or 0
                        usage["completion"] += u.get("completion_tokens", 0) or 0
                        usage["calls"] += 1
                    msg = j["choices"][0]["message"]
                    return (msg.get("content") or "").strip()
                last = f"HTTP {r.status_code}: {r.text[:200]}"
                if r.status_code in (400, 401, 402, 403):
                    break
            except Exception as e:  # noqa: BLE001
                last = repr(e)
            time.sleep(2 * (attempt + 1))
        with usage_lock:
            usage["errors"] += 1
        return f"<<error: {last}>>"


def parse_choice(text: str, letters=("A", "B")) -> str | None:
    m = re.search(r"\b([AB])\b", text.strip().upper()[:40])
    return m.group(1) if m and m.group(1) in letters else None


def parse_yes_no(text: str) -> bool | None:
    t = text.strip().lower()
    if t.startswith("yes"):
        return True
    if t.startswith("no"):
        return False
    m = re.search(r"\b(yes|no)\b", t)
    return None if not m else m.group(1) == "yes"


def parse_boxes(raw: str, W: int, H: int) -> tuple[list, list]:
    """Returns (boxes under the Gemini [ymin, xmin, ymax, xmax] reading, boxes under the [x1, y1, x2, y2] reading),
    both scaled from the 0-1000 grid to pixels."""
    gem, xyxy = [], []
    for m in NUMS.findall(raw):
        a, b, c, d = [float(v) for v in m]
        gem.append([b * W / 1000, a * H / 1000, d * W / 1000, c * H / 1000])
        xyxy.append([a * W / 1000, b * H / 1000, c * W / 1000, d * H / 1000])
    return gem, xyxy


def ground(cli: Client, img: Image.Image, target: str, gold: list, context: str | None = None) -> dict:
    prompt = BOX_PROMPT.format(target=target)
    if context:
        prompt = f"{context}\n{prompt}"
    raw = cli.ask(prompt, img, 200)
    W, H = img.size
    gem, xyxy = parse_boxes(raw, W, H)
    return {"prompt": target, "raw": raw, "boxes_px": gem, "boxes_px_xyxy": xyxy,
            "iou": max((iou(b, gold) for b in gem), default=0.0), "iou_xyxy": max((iou(b, gold) for b in xyxy), default=0.0),
            "center_hit": any(point_in_box(box_center(b), gold) for b in gem)}


def foil_record(cli: Client, img: Image.Image, caption: str, foil: str) -> dict:
    def pair(image, a, b):
        where = "this image" if image is not None else "a photograph you cannot see"
        t1 = cli.ask(f"Which caption describes {where} better?\nA: {a}\nB: {b}\nAnswer with A or B only.", image, 160)
        t2 = cli.ask(f"Which caption describes {where} better?\nA: {b}\nB: {a}\nAnswer with A or B only.", image, 160)
        c1, c2 = parse_choice(t1), parse_choice(t2)
        votes = [c1 == "A", c2 == "B"]  # True when the caption (a) was chosen
        return sum(votes) / 2, [t1, t2]

    yes_c = cli.ask(f"Does this caption correctly describe the image? Caption: \"{caption}\"\nAnswer with Yes or No only.", img, 160)
    yes_f = cli.ask(f"Does this caption correctly describe the image? Caption: \"{foil}\"\nAnswer with Yes or No only.", img, 160)
    yc, yf = parse_yes_no(yes_c), parse_yes_no(yes_f)
    p_cap, p_foil = (1.0 if yc else 0.0) if yc is not None else 0.5, (1.0 if yf else 0.0) if yf is not None else 0.5
    pair_p, pair_raw = pair(img, caption, foil)
    blind_p, blind_raw = pair(None, caption, foil)
    return {"caption": caption, "foil": foil,
            "p_yes_caption": p_cap, "p_yes_foil": p_foil, "yes_correct": p_cap > p_foil,
            "pair_p_caption": pair_p, "pair_correct": pair_p > 0.5, "pair_first_correct": pair_raw and parse_choice(pair_raw[0]) == "A",
            "blind_p_caption": blind_p, "blind_correct": blind_p > 0.5,
            "raw": {"yes_caption": yes_c, "yes_foil": yes_f, "pair": pair_raw, "blind": blind_raw}}


def controls_record(cli: Client, img: Image.Image, it: dict) -> dict:
    words = [it["classes"], it["classes_foil"]]
    rec = {"valse_id": it["valse_id"], "image_file": it["image_file"], "verb": it["verb"], "subset": "actant-swap",
           "model": cli.model, "caption": it["caption"], "foil": it["foil"], "words": {}}
    for j, w in enumerate(words):
        other = words[1 - j]
        tg = it["targets"][w]
        gold, gold_other = tg["bbox"], it["targets"][other]["bbox"]
        phrase = role_phrase(tg["role"], tg["def"], it["verb"])
        q = (f"Caption: \"{it['caption']}\"\nAccording to this caption only, who or what is {phrase}? "
             "Answer with the noun phrase from the caption, nothing else.")
        ans = cli.ask(q, None, 160)
        m_t, m_o = mentions(ans, w), mentions(ans, other)
        text_res = {"answer": ans, "mentions_target": m_t, "mentions_other": m_o, "correct": m_t and not m_o}
        cond = ground(cli, img, phrase, gold, context=f"The image shows: \"{it['caption']}\".")
        conf = ground(cli, img, phrase, gold, context=f"The image shows: \"{it['foil']}\".")
        for d in (cond, conf):
            d["iou_gold"] = d["iou"]
            d["iou_other"] = max((iou(b, gold_other) for b in d["boxes_px"]), default=0.0)
            d["iou_other_xyxy"] = max((iou(b, gold_other) for b in d["boxes_px_xyxy"]), default=0.0)
        cond["hit"] = cond["iou_gold"] >= HIT
        conf["class"] = classify(conf["iou_gold"], conf["iou_other"])
        rec["words"][w] = {"role": tg["role"], "phrase": phrase, "gold": gold, "gold_other": gold_other,
                           "text_resolution": text_res, "conditioned": cond, "conflict": conf}
    return rec


def classify(iou_gold: float, iou_other: float) -> str:
    if iou_gold >= HIT and iou_other < HIT:
        return "image"
    if iou_other >= HIT and iou_gold < HIT:
        return "text"
    if iou_gold >= HIT and iou_other >= HIT:
        return "both"
    return "neither"


def probes_record(cli: Client, img: Image.Image, it: dict) -> dict:
    rec = {"valse_id": it["valse_id"], "image_file": it["image_file"], "verb": it["verb"], "subset": "actant-swap",
           "model": cli.model, "foil": foil_record(cli, img, it["caption"], it["foil"]), "pointing": {}}
    for word in [it["classes"], it["classes_foil"]]:
        tg = it["targets"][word]
        rec["pointing"][word] = {"role": tg["role"], "gold": tg["bbox"],
                                 "role_prompt": ground(cli, img, role_phrase(tg["role"], tg["def"], it["verb"]), tg["bbox"]),
                                 "noun_prompt": ground(cli, img, f"the {word}", tg["bbox"])}
    return rec


def sample_items(items: list[dict], n: int, seed: int) -> list[dict]:
    ids = {it["valse_id"] for it in random.Random(seed).sample(items, min(n, len(items)))}
    return [it for it in items if it["valse_id"] in ids]


def finalize(tag: str) -> None:
    """Pick the box reading (Gemini [ymin, xmin, ymax, xmax] vs [x1, y1, x2, y2]) by the noun-prompt IoU and rewrite."""
    pp = OUT / f"probes_{tag}_actant-swap.jsonl"
    recs = [json.loads(l) for l in open(pp, encoding="utf-8")]
    gem = [p["noun_prompt"]["iou"] for r in recs for p in r["pointing"].values()]
    alt = [p["noun_prompt"]["iou_xyxy"] for r in recs for p in r["pointing"].values()]
    mg, ma = sum(gem) / max(1, len(gem)), sum(alt) / max(1, len(alt))
    print(f"noun-prompt mean IoU: Gemini reading {mg:.3f}, xyxy reading {ma:.3f}")
    if ma <= mg:
        print("keeping the Gemini reading")
        return
    print("switching to the xyxy reading")

    def swap(d, gold, gold_other=None):
        d["boxes_px"], d["boxes_px_xyxy"] = d["boxes_px_xyxy"], d["boxes_px"]
        d["iou"], d["iou_xyxy"] = d["iou_xyxy"], d["iou"]
        d["center_hit"] = any(point_in_box(box_center(b), gold) for b in d["boxes_px"])
        if gold_other is not None:
            d["iou_gold"] = d["iou"]
            d["iou_other"], d["iou_other_xyxy"] = d["iou_other_xyxy"], d["iou_other"]

    for r in recs:
        for p in r["pointing"].values():
            swap(p["role_prompt"], p["gold"]); swap(p["noun_prompt"], p["gold"])
    pp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs), encoding="utf-8")
    cp = OUT / f"controls_{tag}_actant-swap.jsonl"
    if cp.exists():
        crecs = [json.loads(l) for l in open(cp, encoding="utf-8")]
        for r in crecs:
            for d in r["words"].values():
                for k in ("conditioned", "conflict"):
                    swap(d[k], d["gold"], d["gold_other"])
                d["conditioned"]["hit"] = d["conditioned"]["iou_gold"] >= HIT
                d["conflict"]["class"] = classify(d["conflict"]["iou_gold"], d["conflict"]["iou_other"])
        cp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in crecs), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="google/gemini-3.1-pro-preview")
    ap.add_argument("--tag", default="gemini31pro", help="registry-like key used in the output file names")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--reasoning", default="low", help="OpenRouter reasoning effort: low, medium, high, or '' for the default")
    ap.add_argument("--finalize", action="store_true")
    ap.add_argument("--no-controls", action="store_true")
    args = ap.parse_args()
    if args.finalize:
        finalize(args.tag)
        return
    items = [json.loads(l) for l in open(DATA / "joined" / "actant-swap.valid.jsonl", encoding="utf-8")]
    items = sample_items(items, args.n, args.seed)
    if args.limit:
        items = items[: args.limit]
    OUT.mkdir(exist_ok=True)
    pp, cp = OUT / f"probes_{args.tag}_actant-swap.jsonl", OUT / f"controls_{args.tag}_actant-swap.jsonl"
    done_p = {json.loads(l)["valse_id"] for l in open(pp, encoding="utf-8")} if pp.exists() else set()
    done_c = {json.loads(l)["valse_id"] for l in open(cp, encoding="utf-8")} if cp.exists() else set()
    cli = Client(args.model, read_key(), args.reasoning)
    lock = threading.Lock()
    todo = [it for it in items if it["valse_id"] not in done_p or (not args.no_controls and it["valse_id"] not in done_c)]
    print(f"{args.model}: {len(items)} sampled items, {len(todo)} to run, {args.workers} workers")
    t0 = time.time()
    n_done = [0]

    def work(it):
        img = Image.open(image_path(it)).convert("RGB")
        out = []
        if it["valse_id"] not in done_p:
            out.append((pp, probes_record(cli, img, it)))
        if not args.no_controls and it["valse_id"] not in done_c:
            out.append((cp, controls_record(cli, img, it)))
        with lock:
            for path, rec in out:
                with open(path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n_done[0] += 1
            if n_done[0] % 10 == 0 or n_done[0] == len(todo):
                el = time.time() - t0
                print(f"  {n_done[0]}/{len(todo)}  {el / n_done[0]:.1f}s per item, elapsed {el / 60:.1f} min, "
                      f"tokens in {usage['prompt']} out {usage['completion']}, errors {usage['errors']}", flush=True)

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        list(ex.map(work, todo))
    print(f"done: {usage['calls']} calls, {usage['prompt']} prompt tokens, {usage['completion']} completion tokens, {usage['errors']} errors")


if __name__ == "__main__":
    main()
