"""Build a one-page, offline tool for the second annotator of the gold check (the detector-flagged items).

    uv run python scripts/make_gold_tool.py

One flagged item per screen: the image with the SWiG boxes in green ("gold <role>: <noun>") and the detector's box for
each noun in red ("det: <noun>"), the caption, and for each noun three buttons: the red box is on the right object
(ok), on the other participant (swapped), or neither / both / cannot tell (other). This is the protocol of the first
annotator (outputs/gold_flagged.csv), so the two files compare row by row with scripts/gold_agreement.py. Progress is
kept in the browser; "Download CSV" writes gold_flagged.csv with the verdict column filled, in the original row order.
Writes annotation/gold_check_tool/ (gold_check.html, images/, README.txt) and annotation/gold_check_tool.zip.
"""

from __future__ import annotations

import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fvp.data import image_path  # noqa: E402

ANN, OUT, DATA = ROOT / "annotation", ROOT / "outputs", ROOT / "data"

HTML = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Gold-box check: second annotator</title>
<style>
 body{font-family:Segoe UI,Arial,sans-serif;margin:16px;background:#fafafa;color:#222;max-width:1200px}
 #cap{font-size:20px;font-weight:600;margin:6px 0}
 #wrap{display:inline-block;border:1px solid #999;background:#000}
 canvas{display:block}
 .word{margin:8px 0;padding:8px 10px;border:1px solid #ddd;border-radius:6px;background:#fff}
 .word:hover{border-color:#d33}
 .word b{font-size:17px}
 button{font-size:15px;padding:6px 12px;margin-right:6px;cursor:pointer}
 button.sel{background:#2a6;color:#fff;border-color:#2a6}
 .muted{color:#666}
 .legend span{display:inline-block;padding:1px 8px;margin-right:8px;border:3px solid}
 kbd{background:#eee;border:1px solid #bbb;border-radius:3px;padding:0 4px;font-size:13px}
</style></head><body>
<h2>Gold-box check: is the <span style="color:#c00">red</span> detector box on the right object?</h2>
<p class="muted">For each noun below, look at the <b>red</b> box labelled <b>det: &lt;noun&gt;</b>. Choose <b>ok</b> if it sits on the right object for that noun,
<b>swapped</b> if it sits on the <i>other</i> participant of the pair, <b>other</b> if it is on neither, covers both, or you cannot tell.
Judge the red box only; the green boxes are the dataset's own annotation. Keys: <kbd>1</kbd>/<kbd>2</kbd>/<kbd>3</kbd> answer the first open noun, <kbd>&larr;</kbd>/<kbd>&rarr;</kbd> move, <kbd>z</kbd> zooms. Progress is saved in this browser; download the CSV at the end.</p>
<div class="legend"><span style="border-color:#0c0">green: annotated (gold) boxes</span><span style="border-color:#e22">red: detector boxes to judge</span></div>
<div id="cap"></div>
<div id="wrap"><canvas id="c"></canvas></div>
<div id="words"></div>
<div style="margin-top:10px">
 <button id="prev">Previous</button><button id="next">Next</button><button id="zoom">Zoom</button>
 <span id="status" class="muted"></span>
 <button id="dl" style="float:right">Download CSV</button>
</div>
<script>
const ITEMS = __ITEMS__;
const COLS = __COLS__;
const ROWS = __ROWS__;
const KEY = "gold_check_verdicts_v1";
let ann = JSON.parse(localStorage.getItem(KEY) || "{}");
let i = 0; while (i < ITEMS.length - 1 && ITEMS[i].words.every(w => ann[w.key])) i++;
let zoom = 1, img = new Image(), scale = 1, hot = null;
const cv = document.getElementById("c"), ctx = cv.getContext("2d");
function load(){
  const it = ITEMS[i];
  document.getElementById("cap").textContent = "#" + (i+1) + "  " + it.caption;
  img = new Image();
  img.onload = () => { scale = Math.min(1, 1000 / img.width, 700 / img.height) * zoom; cv.width = img.width*scale; cv.height = img.height*scale; draw(); };
  img.src = it.src;
  const box = document.getElementById("words"); box.innerHTML = "";
  it.words.forEach((w, k) => {
    const d = document.createElement("div"); d.className = "word";
    d.onmouseenter = () => { hot = k; draw(); }; d.onmouseleave = () => { hot = null; draw(); };
    d.innerHTML = `<b>${w.word}</b> <span class="muted">(${w.role})</span> &nbsp; red box <b>det: ${w.word}</b>${w.det ? "" : " &mdash; <i>no detector box: choose other</i>"} &nbsp; `;
    ["ok", "swapped", "other"].forEach(v => { const b = document.createElement("button"); b.textContent = v; if (ann[w.key] === v) b.className = "sel";
      b.onclick = () => { ann[w.key] = v; save(); load(); if (it.words.every(x => ann[x.key]) && i < ITEMS.length-1) { i++; load(); } }; d.appendChild(b); });
    box.appendChild(d);
  });
  status();
}
function status(){ const n = Object.keys(ann).length; document.getElementById("status").textContent = "item " + (i+1) + " / " + ITEMS.length + "   (" + n + " of " + ROWS.length + " nouns judged)"; }
function label(x, y, text, fill, above){ ctx.font = "bold 15px Segoe UI, Arial"; const w = ctx.measureText(text).width + 8;
  const yy = above ? y - 20 : y; ctx.fillStyle = fill; ctx.fillRect(x, Math.max(0, yy), w, 20); ctx.fillStyle = "#fff"; ctx.fillText(text, x + 4, Math.max(0, yy) + 15); }
function draw(){
  ctx.drawImage(img, 0, 0, cv.width, cv.height);
  const it = ITEMS[i];
  it.words.forEach(w => { const g = w.gold.map(v => v*scale); ctx.lineWidth = 3; ctx.strokeStyle = "#0c0"; ctx.strokeRect(g[0], g[1], g[2]-g[0], g[3]-g[1]); label(g[0], g[1], "gold " + w.role + ": " + w.word, "#0a0", false); });
  it.words.forEach((w, k) => { if (!w.det) return; const d = w.det.map(v => v*scale); ctx.lineWidth = (hot === null || hot === k) ? 4 : 2; ctx.strokeStyle = (hot === null || hot === k) ? "#e22" : "rgba(230,34,34,0.45)";
    ctx.strokeRect(d[0], d[1], d[2]-d[0], d[3]-d[1]); label(d[0], d[3], "det: " + w.word, "#c00", true); });
}
function save(){ localStorage.setItem(KEY, JSON.stringify(ann)); status(); }
function csvq(v){ v = (v === undefined || v === null) ? "" : String(v); return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
document.getElementById("next").onclick = () => { if (i < ITEMS.length-1){ i++; load(); } };
document.getElementById("prev").onclick = () => { if (i > 0){ i--; load(); } };
document.getElementById("zoom").onclick = () => { zoom = zoom === 1 ? 1.6 : 1; load(); };
document.getElementById("dl").onclick = () => {
  const lines = [COLS.map(csvq).join(",")];
  ROWS.forEach(r => { const row = Object.assign({}, r); row.verdict = ann[r.valse_id + "::" + r.word] || ""; lines.push(COLS.map(c => csvq(row[c])).join(",")); });
  const blob = new Blob([lines.join("\r\n") + "\r\n"], {type: "text/csv"});
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "gold_flagged.csv"; a.click(); };
document.addEventListener("keydown", e => {
  if (e.key === "ArrowRight") document.getElementById("next").click();
  if (e.key === "ArrowLeft") document.getElementById("prev").click();
  if (e.key === "z") document.getElementById("zoom").click();
  if (["1", "2", "3"].includes(e.key)) { const it = ITEMS[i]; const w = it.words.find(x => !ann[x.key]) || it.words[it.words.length-1];
    ann[w.key] = ["ok", "swapped", "other"][Number(e.key)-1]; save(); if (it.words.every(x => ann[x.key]) && i < ITEMS.length-1) i++; load(); }
});
load();
</script></body></html>
"""

README = """Gold-box check: second annotator
=================================

Open gold_check.html in a browser (Chrome, Edge or Firefox; no internet needed).
Each screen shows one image with the dataset's annotated boxes in GREEN ("gold <role>: <noun>") and, for each of the
two nouns, the box an object detector found in RED ("det: <noun>"). The caption is shown above the image.
For each noun, decide where its RED box sits and click one of the three buttons:
  ok       on the right object for that noun
  swapped  on the OTHER participant of the pair (e.g. the red "man" box sits on the woman)
  other    on neither, on both, or you cannot tell
Judge the red box only. Keys 1/2/3 answer the first open noun, arrows move between items, z zooms.
116 items (232 nouns); progress is saved in the browser, so you can close and come back.
At the end click "Download CSV" and send the file gold_flagged.csv back.
Please work from this page alone, without consulting anyone's earlier judgements.
"""


def main() -> None:
    with open(OUT / "gold_flagged.csv", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = list(reader.fieldnames or [])
    gc = {r["valse_id"]: r for r in map(json.loads, open(DATA / "gold_check.jsonl", encoding="utf-8"))}
    items_j = {it["valse_id"]: it for it in map(json.loads, open(DATA / "joined" / "actant-swap.valid.jsonl", encoding="utf-8"))}
    out = ANN / "gold_check_tool"
    shutil.rmtree(out, ignore_errors=True)
    (out / "images").mkdir(parents=True)
    items, seen = [], {}
    for r in rows:
        vid, word = r["valse_id"], r["word"]
        if vid not in seen:
            it = items_j[vid]
            seen[vid] = {"valse_id": vid, "image": it["image_file"], "src": f"images/{it['image_file']}", "caption": it["caption"], "words": []}
            items.append(seen[vid])
            shutil.copy(image_path(it), out / "images" / it["image_file"])
        det = gc[vid]["words"].get(word, {}).get("top_box")
        seen[vid]["words"].append({"key": f"{vid}::{word}", "word": word, "role": r["role"], "flag": r["flag"],
                                   "gold": items_j[vid]["targets"][word]["bbox"], "det": [round(v) for v in det] if det else None})
    public_rows = [{c: ("" if c.lower().startswith(("verdict", "note")) else r[c]) for c in cols} for r in rows]
    html = (HTML.replace("__ITEMS__", json.dumps(items, ensure_ascii=False)).replace("__COLS__", json.dumps(cols))
            .replace("__ROWS__", json.dumps(public_rows, ensure_ascii=False)))
    (out / "gold_check.html").write_text(html, encoding="utf-8")
    (out / "README.txt").write_text(README, encoding="utf-8")
    z = shutil.make_archive(str(ANN / "gold_check_tool"), "zip", out)
    print(f"{z}: {len(items)} items, {len(rows)} nouns, {len(list((out / 'images').iterdir()))} images, {Path(z).stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
