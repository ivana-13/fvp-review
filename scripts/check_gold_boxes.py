"""Sanity-check SWiG role boxes with an open-vocabulary detector (Grounding DINO tiny).

For every valid actant-swap item and each of its two actant words, detect the word in the
image and compare the top detection with the SWiG box of the role the word was mapped to,
and with the box of the other role. Flags:
    ok          top detection overlaps own role box (IoU >= 0.5)
    swapped     overlaps the other role's box (IoU >= 0.5) but not its own -> gold roles likely swapped
    mismatch    overlaps neither -> gold box or detector unreliable for this word
    nodet       nothing detected above threshold

Usage:
    uv run python scripts/check_gold_boxes.py --device cuda      (or --device cpu)
Writes data/gold_check.jsonl and prints a summary.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from fvp.data import image_path, set_cache_default  # noqa: E402

set_cache_default()

import torch  # noqa: E402
from PIL import Image  # noqa: E402

from fvp.geometry import iou  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


class Detector:
    def __init__(self, model_id="IDEA-Research/grounding-dino-tiny", device="cuda"):
        from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

        self.device = device
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(device).eval()

    @torch.no_grad()
    def detect(self, image: Image.Image, phrase: str, threshold=0.25, text_threshold=0.25):
        text = phrase.lower().strip().rstrip(".") + "."
        inputs = self.processor(images=image, text=text, return_tensors="pt").to(self.device)
        outputs = self.model(**inputs)
        sizes = [image.size[::-1]]
        try:
            res = self.processor.post_process_grounded_object_detection(
                outputs, inputs["input_ids"], threshold=threshold, text_threshold=text_threshold, target_sizes=sizes)
        except TypeError:
            res = self.processor.post_process_grounded_object_detection(
                outputs, threshold=threshold, text_threshold=text_threshold, target_sizes=sizes)
        r = res[0]
        boxes = r["boxes"].tolist()
        scores = r["scores"].tolist()
        return sorted(zip(scores, boxes), key=lambda x: -x[0])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    items = [json.loads(l) for l in open(DATA / "joined" / "actant-swap.valid.jsonl", encoding="utf-8")]
    if args.limit:
        items = items[: args.limit]
    out_path = DATA / "gold_check.jsonl"
    done = {}
    if out_path.exists():
        for l in open(out_path, encoding="utf-8"):
            r = json.loads(l)
            done[r["valse_id"]] = r
    det = Detector(device=args.device)
    t0 = time.time()
    flags = {"ok": 0, "swapped": 0, "mismatch": 0, "nodet": 0}
    with open(out_path, "a", encoding="utf-8") as fout:
        for i, it in enumerate(items, 1):
            if it["valse_id"] in done:
                for w in done[it["valse_id"]]["words"].values():
                    flags[w["flag"]] += 1
                continue
            path = image_path(it)
            if not path.exists():
                continue
            img = Image.open(path).convert("RGB")
            words = [it["classes"], it["classes_foil"]]
            rec = {"valse_id": it["valse_id"], "image_file": it["image_file"], "words": {}}
            for j, w in enumerate(words):
                own = it["targets"][w]["bbox"]
                other = it["targets"][words[1 - j]]["bbox"]
                dets = det.detect(img, w)
                if not dets:
                    flag, top, iou_own, iou_other = "nodet", None, 0.0, 0.0
                else:
                    score, top = dets[0]
                    iou_own, iou_other = iou(top, own), iou(top, other)
                    if iou_own >= 0.5:
                        flag = "ok"
                    elif iou_other >= 0.5:
                        flag = "swapped"
                    else:
                        flag = "mismatch"
                rec["words"][w] = {"role": it["targets"][w]["role"], "flag": flag, "top_box": top,
                                   "iou_own": iou_own, "iou_other": iou_other, "n_det": len(dets)}
                flags[flag] += 1
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fout.flush()
            if i % 50 == 0:
                print(f"  {i}/{len(items)}  {(time.time()-t0)/i:.2f}s per item  {flags}")
    n_words = sum(flags.values())
    print(f"\nwords checked: {n_words}  flags: {flags}")
    both_ok = swapped_items = 0
    for l in open(out_path, encoding="utf-8"):
        r = json.loads(l)
        fl = [w["flag"] for w in r["words"].values()]
        both_ok += all(f == "ok" for f in fl)
        swapped_items += any(f == "swapped" for f in fl)
    print(f"items with both actants ok: {both_ok} | items with a likely role swap: {swapped_items}")


if __name__ == "__main__":
    main()
