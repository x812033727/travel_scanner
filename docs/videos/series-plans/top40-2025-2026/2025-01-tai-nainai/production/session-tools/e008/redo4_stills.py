#!/usr/bin/env python3
"""第 8 集首格第四輪（2026-11-11）-> stills-redo4.json。

第三輪定 c21（h）、c29（g）。其餘六鏡照獨立挑圖的修法，每張從最接近的一張只改一兩件事：
- c07：第三輪把 PICK:c04 當 image 2，模型照抄成過肩構圖；改回只放 st2/c07-d 加壽衣定妝圖。
- c09：「eyes darken」被畫成煙燻妝；改從 PICK:c02 重跑並寫明不化妝。
- c12：不用 laugh 這個字（會畫成露齒真笑）。
`ST2:` 是 $TN_WORK/e008ff/st2/，`ST3:` 是 st3/，`PICK:` 是 pick/。
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills-redo4.json"
NOTEXT = "No subtitles, no text anywhere; no screen anywhere. No lanterns."
KEEP = "Keep everything else exactly the same: faces, hair, clothes, positions, the place, the light and the camera angle. "
S = []


def edit(shot, refs, prompt):
    S.append({"shot": shot, "shares_with": [], "refs": refs, "prompt": prompt + " " + KEEP + NOTEXT, "latent": "image1"})


edit("c07", ["ST2:c07-d.png", "prop-shouyi-t1.png"],
     "Edit image 1. Two changes only: the flat white board in her arms becomes the off-white robe of image 2 (only the robe, no trousers) folded into a soft "
     "neat square, its high stand-up collar and one fabric frog button showing on top, held against her chest in both hands; the strip of deep-blue sky at "
     "the top becomes dark roof eaves. There is only one person in the picture.")
edit("c25", ["ST3:c25-h.png"],
     "Edit image 1. Only change: her right hand leaves the handle and closes into a tight fist on the bag's flap with the brass bells hidden inside it, so no "
     "bell is visible anywhere; only her left hand holds the handle at chest height.")
edit("c14", ["ST3:c14-h.png"],
     "Edit image 1. The old woman lifts both arms from her lap and wraps them tight around the young woman's waist, face tilted up toward her with clear tears "
     "glistening on her lower lids, no redness, mouth corners turned down, not smiling; the young woman keeps only her right hand on the old woman's back, "
     "her left hand hangs down.")
edit("c09", ["PICK:c02"],
     "Edit image 1. Exactly two changes. One: at the bottom edge of the frame, the top of a neatly folded off-white robe held against her chest, its stand-up "
     "collar and one frog button showing. Two: her gaze turns heavy and serious, brows lowered a little, lips closed, not smiling, natural bare eyelids with "
     "no eye makeup or eyeshadow, the same face as image 1. Her face stays in three-quarter profile toward screen left.")
edit("c10", ["ST3:c10-h.png"],
     "Edit image 1. She straightens up most of the way, keeping only a slight stoop in her upper back, head raised so her face is in three-quarter profile "
     "toward screen left with eyelids half lowered, lips closed, not smiling; the folded off-white robe with its stand-up collar and frog button is held "
     "clearly in both hands in front of her waist, clearly separate from her clothes.")
edit("c12", ["PICK:c08"],
     "Edit image 1. Exactly two changes. One: the woman in wine-red unfolds her arms; her hands hang down at her sides. Two: her lips close into a tight, "
     "forced closed-mouth smirk with the corners pulled up, no teeth showing, eyes wide, cold and unsmiling, staring toward the young woman at screen right, "
     "face turned three-quarters to screen right as in image 1.")

if __name__ == "__main__":
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S))
