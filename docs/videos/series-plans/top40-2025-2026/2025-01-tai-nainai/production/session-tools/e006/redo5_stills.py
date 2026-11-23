#!/usr/bin/env python3
"""第 6 集首格第五輪（2026-11-10）-> stills-redo5.json。

四輪的教訓：模型「拿掉東西」比「加上東西」可靠；戒指的方形印面四輪都露出來。
- c01：第四輪 I 只錯在托盤（壺在桌上另一個托盤）：拿掉桌上那組，把壺放回她端的托盤。
- c14：第一輪 A（過肩、表情都對）右手拿著一本冊子：拿掉冊子，右手放到扣子上；皮夾夾在左臂由插鏡 c12 交代。
- c20：印面藏不住，改成左手輕輕握拳、右手整個蓋在拳上（劇本的「拇指蓋住印面」換成「手蓋住」）。
- c17 拿掉（三輪都露印面；c20 的心裡話交代得到）。
"""
import json
from pathlib import Path

import make_stills as m
from redo4_stills import KEEP, HANDS, RING

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills-redo5.json"
S = []


def still(shot, refs, prompt, latent=None):
    s = {"shot": shot, "shares_with": [], "refs": refs, "prompt": prompt}
    if latent:
        s["latent"] = latent
    S.append(s)


still("c01", ["ST:st4/c01-i.png"], (
    "Edit image 1. Remove the teapot and the second tray from the long table, leaving the table bare. On the plain light wooden tray the young "
    "woman in moon-white is carrying, put one small round reddish-purple clay teapot beside three small white teacups. There is only one tray "
    "and only one teapot in the whole picture. " + KEEP + m.NOTEXT), latent="image1")
still("c14", ["ST:st/c14-a.png"], (
    "Edit image 1. Remove the booklet from the man's right hand: his right hand is now empty and rests on the front button of his navy suit "
    "jacket. He holds nothing in his hands. " + KEEP + m.NOTEXT), latent="image1")
still("c20", [RING, m.YT_P], (
    f"{m.PRE.replace('image 1', 'image 2')} A close-up looking down, as if through her own eyes: a young woman's LEFT hand closed into a loose "
    "fist in the centre of the frame, knuckles up, and her bare RIGHT hand cupped over the fist, covering the fingers completely; only a thin "
    "sliver of the old silver band of image 1 shows between two knuckles, its face hidden inside the fist; no ring on the right hand; exactly "
    "two hands with five fingers each. " + HANDS + m.NOTEXT))


def main():
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S), "stills")


if __name__ == "__main__":
    main()
