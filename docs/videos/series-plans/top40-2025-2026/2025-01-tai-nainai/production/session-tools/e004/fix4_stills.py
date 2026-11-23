#!/usr/bin/env python3
"""第 4 集重拍首格第三輪（2026-11-10）：修最接近的那張 -> fix4-stills.json。

兩輪重畫都失敗（c30 帽與袋上有字、臉被畫成面罩；c36 四張都不生氣），改成修圖（latent image1）：
- c30：第二輪 E（構圖、院牆、兩手捧袋都對）拿掉帽上的字、帽簷壓低遮眼、前景的女子轉成只露後腦與辮子。
- c36：成片 c33 精修片段的第 1 秒（同一刻、同一身造型）拿掉前景的月棠，林美鳳改成生氣、右手抓珍珠。
refs 的 `ST3:` 是 $TN_WORK/e004fix2/st3/，`CUT:` 是 $TN_WORK/e004fix2/refs/。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "e006"))
import make_stills as m  # noqa: E402

OUT = Path(__file__).resolve().parent / "fix4-stills.json"
KEEP = "Keep everything else exactly the same: the place, the light, the camera angle, faces, hair and clothes. No other change. "
S = []


def still(shot, refs, prompt):
    S.append({"shot": shot, "shares_with": [], "refs": refs, "prompt": prompt, "latent": "image1"})


still("c30", ["ST3:c30-e.png"], (
    "Edit image 1. Remove every letter and logo from the white helmet and from the delivery bag, leaving them plain. Pull the helmet brim lower so "
    "its shadow covers the man's eyes; only his mouth and chin stay visible, mouth corners pulled down, lips pressed. The blurred young woman at the "
    "right edge turns her head away from the camera: only the back of her head, her black braid and her moon-white collar show, no ear, no cheek, no "
    "face. " + KEEP + m.NOTEXT))
still("c36", ["CUT:clip-c33.png"], (
    "Edit image 1. Remove the young woman with the braid in the foreground completely, leaving only the kitchen behind. The woman in the wine-red "
    "dress is now ALONE, seen in a close-up from the chest up, straightened up, half a step back; her expression becomes FURIOUS: cheeks flushed red, "
    "brows knitted up and together, eyes wide and glaring toward screen right, lips pressed tight, NOT smiling, no teeth showing; her RIGHT hand "
    "clutches the pearl strand at her throat. She does not look at the camera. " + KEEP + "There is exactly one person in the picture. " + m.NOTEXT))


if __name__ == "__main__":
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S))
