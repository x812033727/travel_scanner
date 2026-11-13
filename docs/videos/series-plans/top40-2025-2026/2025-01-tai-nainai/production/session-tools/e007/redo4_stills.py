#!/usr/bin/env python3
"""第 7 集首格第四輪（2026-11-10）：最後的小修圖 -> stills-redo4.json。

第三輪定 c07、c09、c22、c26、c27；c25 選 G 當底（下一步加前景背影、拿掉燈）、c29 從 c27 的 F 修。
c01 上輪把月棠也刪了：這輪只說「刪掉坐著的乘客」；c12 從第三輪 H 只改頭髮、領帶、奶茶；c15 一次只改一件事（拿掉杯蓋）。
`ST:` st/、`ST3:` st3/、`PICK:` pick/。
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills-redo4.json"
NOTEXT = "No subtitles, no captions, no text, numbers, signs, LED displays or screens anywhere in the picture."
KEEP = "Keep everything else exactly the same: the place, the light, the camera angle, faces, hair and clothes. No other change. "
S = []


def edit(shot, ref, prompt):
    S.append({"shot": shot, "shares_with": [], "refs": [ref], "prompt": prompt + " " + KEEP + NOTEXT, "latent": "image1"})


edit("c01", "ST:c01-a.png", "Edit image 1. Remove ONLY the passengers who are sitting in the seats, leaving those seats empty. KEEP the young woman in the "
     "moon-white top standing at the front door, and KEEP the schoolgirl walking in the aisle; both stay exactly where they are.")
edit("c12", "ST3:c12-h.png", "Edit image 1. The girl on the RIGHT: remove her bangs, her long straight light-brown hair is parted in the middle with her "
     "forehead showing; her bow becomes a navy necktie; her clear lidless cup is filled with pale milk tea, with one straw.")
edit("c15", "ST:c15-a.png", "Edit image 1. Remove the lid of the plastic cup, leaving its open round rim with one straw standing in the milk tea.")
edit("c25", "ST3:c25-g.png", "Edit image 1. Add in the RIGHT foreground, close to the camera and softly out of focus, the back view of a slim young woman seen "
     "from behind, from the waist up, cut by the right edge of the frame and filling only the right fifth of the picture: a moon-white cotton top with a high "
     "stand-up collar and long narrow sleeves, glossy black hair in one long braid hanging over her right shoulder, her left hand down at her side holding a "
     "plain navy school bag low at the bottom edge. Only the back of her head is visible: no face, no ear, no cheek, no earring. She does not cover the woman "
     "in wine-red or her arms. Also remove every hanging lamp and every floor lantern in the courtyard, leaving only warm yellow light glowing on the veranda "
     "walls. The woman in wine-red keeps her face in three-quarter profile toward screen right, lips closed, still holding the folded white robe against her chest.")
edit("c29", "PICK:c27", "Edit image 1. Add at the far RIGHT edge, in the foreground and heavily out of focus, a narrow slice of a young woman seen from "
     "behind her left shoulder: a moon-white high stand-up collar on her left shoulder and the back of her plain glossy black hair, cut by the right edge of "
     "the frame; no face, no ear, no cheek, no earring. The woman in wine-red now glares at her: eyebrows raised high, eyes wide open staring toward screen "
     "right at that shoulder, the corners of her red lips pulled down, lips closed, chin pushed forward, not smiling. She still holds the white robe up by its "
     "shoulders, held out toward screen right, and is NOT wearing it. Her necklace is a strand of round white pearls. No lanterns anywhere.")

if __name__ == "__main__":
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S))
