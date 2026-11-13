#!/usr/bin/env python3
"""第 8 集首格第三輪（2026-11-11）-> stills-redo3.json。

第二輪定 c04、c08、c13、c26、c27。拿掉 c05、c19（沒有台詞的全景，兩輪都失敗；c06、c20、c21 交代得到）。
這輪：c07、c21、c25 從第二輪最接近的那張只改一件事；c14 改從頭畫（兩輪修圖都做不出抱腰）；第二批 c09、c10、c12、c29 從已挑定的首格修（stills.json 的 batch 2）。
`ST2:` 是 $TN_WORK/e008ff/st2/，`PICK:` 是 pick/。
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills-redo3.json"
BASE = {s["shot"]: s for s in json.loads((HERE / "stills.json").read_text(encoding="utf-8"))}
NOTEXT = "No subtitles, no text anywhere; no screen anywhere."
KEEP = "Keep everything else exactly the same: faces, hair, clothes, positions, expressions, the place, the light and the camera angle. "
S = []


def edit(shot, refs, prompt):
    S.append({"shot": shot, "shares_with": [], "refs": refs, "prompt": prompt + " " + KEEP + NOTEXT, "latent": "image1"})


edit("c07", ["ST2:c07-d.png", "PICK:c04"],
     "Edit image 1. Only one change: the flat white board in her arms becomes the folded off-white robe exactly as the young woman holds it in image 2: folded "
     "into a soft square with its high stand-up collar and one fabric frog button on top. Also remove the two small ceiling lights under the eave.")
edit("c21", ["ST2:c21-c.png"],
     "Edit image 1. Only one change: her bare right hand comes up from below and cups the three little brass bells on the bag's flap, holding them still; her "
     "left hand moves to the bag's handle at chest height.")
edit("c25", ["ST2:c25-c.png"],
     "Edit image 1. Only one change: her bare RIGHT hand is closed tight around the three little brass bells on the flap, the bells hidden inside her fist; "
     "only her left hand holds the handle.")
b = BASE["c14"]
S.append({"shot": "c14", "shares_with": b["shares_with"], "refs": b["refs"],
          "prompt": "FIRST FRAME ALREADY HUGGING: the old woman in the wheelchair has both arms wrapped tight around the young woman's waist, her cheek pressed "
                    "against her side, crying with clear tears, no redness, NOT smiling; the young woman stands beside the wheelchair in long narrow moon-white "
                    "sleeves and a navy ankle-length skirt, her bare right hand on the old woman's back, looking down at her. " + b["prompt"],
          **({"latent": b["latent"]} if b.get("latent") else {})})
for shot in ("c09", "c10", "c12", "c29"):
    b = BASE[shot]
    S.append({"shot": shot, "shares_with": b["shares_with"], "refs": b["refs"], "prompt": b["prompt"], **({"latent": b["latent"]} if b.get("latent") else {})})

if __name__ == "__main__":
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S), [(s["shot"], s["refs"][:1]) for s in S])
