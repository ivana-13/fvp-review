"""Join ARO VG-Relation items to Visual Genome object boxes and write them in the VALSE-join record format.

ARO's `visual_genome_relation.json` gives, per item, the true and swapped caption ("the man is holding the bag" /
"the bag is holding the man"), the subject object id (`primary_object_id`, with its noun) and the object id
(`relation_info.object`). Visual Genome's `objects.json` gives each object's box and names; `image_data.json` gives the
image size and download URL. Two subsets are written:

  aro-relation  non-spatial relations (wearing, holding, sitting on, ...), at most --cap items per relation
  aro-spatial   a --spatial sample of the "to the left of" / "to the right of" swaps, where both captions are equally
                plausible as text (the blind-solvable contrast is reversed here)

Each record has the same keys as the VALSE join (valse_id is the generic item id): image_file, image_dir, width,
height, verb (= relation), caption, foil, classes (subject noun), classes_foil (object noun), targets with a role
("subject"/"object"), a box and a role phrase (`def`), plus the ARO union crop as `crop`.

Usage:
    uv run python scripts/prepare_aro.py [--cap 150] [--spatial 300] [--seed 0]
Writes data/joined/aro-relation.valid.jsonl, data/joined/aro-spatial.valid.jsonl, data/aro/image_list.txt
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ARO = DATA / "aro"

SPATIAL = {"to the left of", "to the right of", "on", "in", "in front of", "behind", "above", "below", "under", "on top of",
           "next to", "beside", "near", "at", "inside", "by", "over", "between", "along", "against", "around", "across",
           "beneath", "underneath", "on the side of", "on the front of", "on the back of", "at the top of",
           "at the bottom of", "in the middle of", "on the left of", "on the right of", "to the side of", "attached to",
           "part of", "of", "with", "from", "for", "standing next to", "standing in", "standing on", "sitting in",
           "lying on", "lying in", "parked on", "hanging on", "hanging from", "leaning on", "leaning against",
           "laying on", "laying in"}
LEFT_RIGHT = {"to the left of", "to the right of"}


def role_defs(rel: str) -> dict[str, str]:
    """Role phrases that name the participant by its side of the relation without naming the noun."""
    return {"subject": f"The one that is {rel} something", "object": f"The thing that something is {rel}"}


def to_xyxy(o: dict, W: int, H: int) -> list[int] | None:
    x1, y1 = max(0, int(o["x"])), max(0, int(o["y"]))
    x2, y2 = min(W, int(o["x"] + o["w"])), min(H, int(o["y"] + o["h"]))
    return [x1, y1, x2, y2] if x2 - x1 >= 4 and y2 - y1 >= 4 else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=int, default=150, help="max items per non-spatial relation")
    ap.add_argument("--spatial", type=int, default=300, help="size of the left/right sample")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    items = json.load(open(ARO / "visual_genome_relation.json", encoding="utf-8"))
    meta = {str(m["image_id"]): m for m in json.load(open(ARO / "image_data.json", encoding="utf-8"))}
    needed = {str(it["image_id"]) for it in items}
    print(f"ARO items {len(items)}, images {len(needed)}; loading objects.json ...", flush=True)
    objects: dict[str, dict[str, dict]] = {}
    for entry in json.load(open(ARO / "objects.json", encoding="utf-8")):
        iid = str(entry["image_id"])
        if iid in needed:
            objects[iid] = {str(o["object_id"]): o for o in entry["objects"]}
    print(f"objects loaded for {len(objects)} of the needed images", flush=True)

    def build(it: dict, subset: str) -> dict | None:
        iid = str(it["image_id"])
        m, objs = meta.get(iid), objects.get(iid)
        if not m or not objs:
            return None
        W, H = int(m["width"]), int(m["height"])
        rel = it["relation_info"]["name"]
        s = objs.get(str(it["primary_object_id"]))
        o = objs.get(str(it["relation_info"]["object"]))
        if not s or not o:
            return None
        s_noun = (it.get("primary_object_name") or (s["names"][0] if s.get("names") else "")).strip().lower()
        o_noun = (o["names"][0] if o.get("names") else "").strip().lower()
        if not s_noun or not o_noun or s_noun == o_noun:
            return None
        sb, ob = to_xyxy(s, W, H), to_xyxy(o, W, H)
        if not sb or not ob:
            return None
        defs = role_defs(rel)
        crop = [it["bbox_x"], it["bbox_y"], it["bbox_x"] + it["bbox_w"], it["bbox_y"] + it["bbox_h"]]
        return {"valse_id": f"aro_{iid}_{it['primary_object_id']}_{it['relation_info']['object']}", "subset": subset,
                "image_file": f"{iid}.jpg", "image_dir": "aro/images", "split": "aro", "verb": rel,
                "width": W, "height": H, "caption": it["true_caption"], "foil": it["false_caption"],
                "classes": s_noun, "classes_foil": o_noun, "crop": crop, "url": m.get("url"),
                "targets": {s_noun: {"role": "subject", "bbox": sb, "def": defs["subject"]},
                            o_noun: {"role": "object", "bbox": ob, "def": defs["object"]}}}

    by_rel = defaultdict(list)
    for it in items:
        by_rel[it["relation_info"]["name"]].append(it)
    out_rel, dropped = [], Counter()
    for rel, its in sorted(by_rel.items()):
        if rel in SPATIAL:
            continue
        recs = [r for r in (build(it, "aro-relation") for it in its) if r]
        dropped[rel] += len(its) - len(recs)
        if len(recs) > args.cap:
            recs = rng.sample(recs, args.cap)
        out_rel += recs
    out_rel.sort(key=lambda r: r["valse_id"])
    lr = [it for rel in LEFT_RIGHT for it in by_rel.get(rel, [])]
    rng2 = random.Random(args.seed)
    rng2.shuffle(lr)
    out_sp = []
    for it in lr:
        r = build(it, "aro-spatial")
        if r:
            out_sp.append(r)
        if len(out_sp) >= args.spatial:
            break
    out_sp.sort(key=lambda r: r["valse_id"])

    (DATA / "joined").mkdir(exist_ok=True)
    for name, recs in [("aro-relation", out_rel), ("aro-spatial", out_sp)]:
        with open(DATA / "joined" / f"{name}.valid.jsonl", "w", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"{name}: {len(recs)} items, {len({r['image_file'] for r in recs})} images")
    print("non-spatial relations kept (top 12):", Counter(r["verb"] for r in out_rel).most_common(12))
    print("items dropped for missing boxes/nouns (top 5):", dropped.most_common(5))
    images = sorted({r["image_file"] for r in out_rel + out_sp})
    (ARO / "image_list.txt").write_text("\n".join(images) + "\n", encoding="utf-8")
    print(f"wrote data/aro/image_list.txt ({len(images)} images)")


if __name__ == "__main__":
    main()
