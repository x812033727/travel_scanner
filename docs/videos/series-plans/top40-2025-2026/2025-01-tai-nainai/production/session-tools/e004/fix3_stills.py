#!/usr/bin/env python3
"""第 4 集重拍首格第二輪（2026-11-10）：c30、c36 -> fix3-stills.json。c29 第一輪 A 定案。

第一輪獨立挑圖：c30 三張照抄整張 c27 的遠景構圖、前景變成另一個人、戴墨鏡或口罩；c36 三張都在笑、背景是現代廚房與花園。
改法：外送員只給裁出來的上半身（ref-courier.png）；鏡位與表情放第一句；禁止笑、墨鏡、口罩；背景指名老屋門口、石板路、灰院牆。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "e006"))
import make_stills as m  # noqa: E402

OUT = Path(__file__).resolve().parent / "fix3-stills.json"
OUTSIDE = ("behind him only a bright sunlit stone-paved path and a plain grey courtyard wall; no kitchen, no table, no second doorway, no garden "
           "in the frame")
S = []


def still(shot, refs, prompt):
    S.append({"shot": shot, "shares_with": [], "refs": refs, "prompt": prompt})


still("c30", ["CUT:ref-courier.png"], (
    "A MEDIUM CLOSE-UP over-the-shoulder shot: the delivery man fills the LEFT half of the frame from the chest up. "
    f"{m.PRE} A bright clear noon outside the side door of an old house, seen from just inside the doorway looking out; {OUTSIDE}. "
    "At the RIGHT edge of the frame, very close to the lens and heavily blurred: the left shoulder of a young woman seen from BEHIND, a MOON-WHITE "
    "high collar and one long BLACK braid, no ear, no cheek, no face, and her two hands in moon-white cuffs holding a white porcelain bowl. "
    "On screen left: ONLY ONE man, the delivery man of image 1, in his plain GREY zip jacket and plain WHITE helmet with no writing, the helmet brim "
    "pulled low so its shadow covers his eyes; only his mouth and chin are visible; NO sunglasses, NO goggles, NO face mask. BOTH hands raise a plain "
    "dark box-shaped insulated delivery bag with no logo and no writing at chest height between them. Mouth corners pulled down, lips pressed, awkward. "
    "He does not look at the camera. " + m.OTS))
still("c36", [m.MF_P, "CUT:ref-c33.png", "CUT:ref-c28.png"], (
    "FURIOUS, NOT SMILING: cheeks flushed red, brows knitted up and together, eyes wide and glaring, lips pressed tight; no smile, no teeth showing. "
    "A TIGHT CLOSE-UP, head and shoulders. "
    f"{m.PRE} ONLY ONE woman: the woman from image 1, dressed exactly as in image 2: shoulder-length glossy AUBURN-brown wavy hair, a fitted WINE-RED "
    "knit dress with a high round neckline, a SINGLE long strand of pearls, red lips. Her RIGHT hand clutches the pearl strand at her throat. Her face "
    "in three-quarter profile turned toward screen right, glaring toward screen right, never looking at the camera. Behind her, out of focus: the open "
    "doorway of the old plain kitchen of image 3, and beyond it a bright stone-paved path and a grey courtyard wall; no garden, no flowers, no modern "
    "stove. " + m.ONE_F))


if __name__ == "__main__":
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S))
