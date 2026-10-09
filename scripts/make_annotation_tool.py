"""Build a one-page, offline annotation tool for the human ceiling on role prompts.

    uv run python scripts/make_annotation_tool.py [--n 100] [--seed 1] [--out annotation/human_ceiling.html]

The page shows one target at a time: the image and the role phrase only (no caption, no gold box, no model box), in a
random order, and asks for one drag-drawn box. Progress is kept in the browser's localStorage; the "Download
annotations" button saves a JSON file with pixel boxes in the original image coordinates, which
scripts/score_annotations.py compares with the SWiG boxes. Open the page from this repository (it loads the images
from data/swig/images by relative path).
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_probes import role_phrase  # noqa: E402

HTML = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Role pointing: human annotation</title>
<style>
 body{font-family:Segoe UI,Arial,sans-serif;margin:16px;background:#fafafa;color:#222}
 #phrase{font-size:22px;font-weight:600;margin:8px 0}
 #wrap{position:relative;display:inline-block;border:1px solid #999;background:#000}
 canvas{display:block;cursor:crosshair}
 button{font-size:15px;padding:6px 12px;margin-right:6px}
 .muted{color:#666}
</style></head><body>
<h2>Where is it? Draw one box around the thing the phrase refers to.</h2>
<p class="muted">Drag with the mouse to draw a box. Draw a new box to replace it. If the phrase cannot be answered on this image, click <b>Cannot tell</b>. Your progress is saved in this browser; download the file at the end.</p>
<div id="phrase"></div>
<div id="wrap"><canvas id="c"></canvas></div>
<div style="margin-top:10px">
 <button id="prev">Previous</button><button id="next">Next</button><button id="skip">Cannot tell</button>
 <span id="status" class="muted"></span>
 <button id="dl" style="float:right">Download annotations</button>
</div>
<script>
const ITEMS = __ITEMS__;
const KEY = "role_pointing_annotations_v1";
let ann = JSON.parse(localStorage.getItem(KEY) || "{}");
let i = Math.min(Object.keys(ann).length, ITEMS.length - 1);
const cv = document.getElementById("c"), ctx = cv.getContext("2d");
let img = new Image(), scale = 1, drag = null, box = null;
function load(){
  const it = ITEMS[i];
  document.getElementById("phrase").textContent = it.phrase;
  document.getElementById("status").textContent = (i+1) + " / " + ITEMS.length + (ann[it.id] ? "   (answered)" : "");
  img = new Image();
  img.onload = () => { scale = Math.min(1, 900 / img.width, 650 / img.height); cv.width = img.width*scale; cv.height = img.height*scale;
                       box = ann[it.id] && ann[it.id].box ? ann[it.id].box.map(v => v*scale) : null; draw(); };
  img.src = it.src;
}
function draw(){ ctx.drawImage(img, 0, 0, cv.width, cv.height);
  if (box){ ctx.lineWidth = 3; ctx.strokeStyle = "#ff3030"; ctx.strokeRect(box[0], box[1], box[2]-box[0], box[3]-box[1]); } }
cv.addEventListener("mousedown", e => { const r = cv.getBoundingClientRect(); drag = [e.clientX - r.left, e.clientY - r.top]; });
cv.addEventListener("mousemove", e => { if (!drag) return; const r = cv.getBoundingClientRect();
  box = [Math.min(drag[0], e.clientX - r.left), Math.min(drag[1], e.clientY - r.top), Math.max(drag[0], e.clientX - r.left), Math.max(drag[1], e.clientY - r.top)]; draw(); });
cv.addEventListener("mouseup", e => { if (!drag) return; drag = null;
  if (box && (box[2]-box[0]) > 4 && (box[3]-box[1]) > 4){ const it = ITEMS[i];
    ann[it.id] = {box: box.map(v => Math.round(v/scale)), image: it.image, phrase: it.phrase, t: Date.now()}; save(); } });
function save(){ localStorage.setItem(KEY, JSON.stringify(ann)); document.getElementById("status").textContent = (i+1) + " / " + ITEMS.length + "   (answered)"; }
document.getElementById("next").onclick = () => { if (i < ITEMS.length-1){ i++; load(); } };
document.getElementById("prev").onclick = () => { if (i > 0){ i--; load(); } };
document.getElementById("skip").onclick = () => { const it = ITEMS[i]; ann[it.id] = {box: null, image: it.image, phrase: it.phrase, t: Date.now()}; save(); if (i < ITEMS.length-1){ i++; load(); } };
document.getElementById("dl").onclick = () => { const blob = new Blob([JSON.stringify({items: ITEMS.length, annotations: ann}, null, 1)], {type: "application/json"});
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "human_ceiling_annotations.json"; a.click(); };
document.addEventListener("keydown", e => { if (e.key === "ArrowRight") document.getElementById("next").click(); if (e.key === "ArrowLeft") document.getElementById("prev").click(); });
load();
</script></body></html>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default="annotation/human_ceiling.html")
    args = ap.parse_args()
    items = [json.loads(l) for l in open(ROOT / "data/joined/actant-swap.valid.jsonl", encoding="utf-8")]
    rng = random.Random(args.seed)
    chosen = rng.sample(items, args.n)
    targets = []
    for it in chosen:
        for w in (it["classes"], it["classes_foil"]):
            tg = it["targets"][w]
            targets.append({"id": f"{it['valse_id']}::{w}", "image": it["image_file"], "src": f"../data/swig/images/{it['image_file']}",
                            "phrase": role_phrase(tg["role"], tg["def"], it["verb"]), "role": tg["role"], "word": w, "gold": tg["bbox"]})
    rng.shuffle(targets)
    public = [{k: t[k] for k in ("id", "image", "src", "phrase")} for t in targets]  # the page never sees gold, roles or nouns
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HTML.replace("__ITEMS__", json.dumps(public, ensure_ascii=False)), encoding="utf-8")
    (out.parent / "human_ceiling_targets.json").write_text(json.dumps(targets, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out} with {len(public)} targets from {args.n} items (seed {args.seed}); gold kept in human_ceiling_targets.json")


if __name__ == "__main__":
    main()
