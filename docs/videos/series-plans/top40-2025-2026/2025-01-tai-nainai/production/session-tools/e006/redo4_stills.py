#!/usr/bin/env python3
"""第 6 集首格第四輪（2026-11-10）-> stills-redo4.json。

第三輪獨立挑圖後：三輪都沒有一張全對的 c01、c14、c41 不能拿掉，改成「修最接近的那張」（latent image1，
refs 第一張是那張候選）；c38 吊燈修成白燈罩；c17、c20 參照路線讓印面入鏡，改走首格路線先畫手。
c16、c33、c37 拿掉（獨立審稿：前後鏡交代得到）。

refs 的寫法：`ST:<資料夾>/<檔名>` 是 $TN_WORK/e006ff/ 底下的候選圖，`PICK:<鏡>` 是 pick/<鏡>.png，其他是 refs/。
"""
import json
from pathlib import Path

import make_stills as m
from redo_stills import DIN, TEARS

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills-redo4.json"
KEEP = "Keep everything else exactly the same: the room, the light, the camera angle, every face, hair and costume. No other change. "
RING = "prop-yinjie-t1.png"
S = []


def still(shot, refs, prompt, latent=None):
    s = {"shot": shot, "shares_with": [], "refs": refs, "prompt": prompt}
    if latent:
        s["latent"] = latent
    S.append(s)


still("c01", ["ST:st3/c01-g.png", m.JMB_P], (
    "Edit image 1. The man seen from behind in the near foreground in the navy suit: his hair becomes neat side-parted glossy BLACK hair like the "
    "man in image 2, a younger man, no grey hair. Remove the man in the suit walking away outside the door on the left, leaving the doorway empty. "
    "The old man's Chinese-style jacket becomes a pale LIGHT BLUE-GREY. Remove the small red tassel hanging from the ceiling. " + KEEP + m.NOTEXT),
    latent="image1")
still("c14", ["ST:st/c14-a.png", m.JMB_P], (
    "Edit image 1. The folder the man holds becomes two folders tucked tight UNDER HIS LEFT ARM, pressed against his side: a black hard-cover "
    "folder on top and a dark brown leather folder with a brass clasp underneath, no label, no writing. His right hand is empty, resting at his "
    "suit jacket button. He keeps his gold-rimmed glasses, his cold narrowed eyes and his unsmiling mouth. " + KEEP + m.NOTEXT), latent="image1")
still("c41", ["ST:st3/c41-f.png"], (
    "Edit image 1. The young woman in moon-white lowers her eyes to look down at the crying girl's face in front of her, brows drawn up and "
    "together, lips pressed, her two hands still resting on the girl's shoulders. Make the pendant lamp a plain white dome-shaded lamp. " + KEEP
    + "There are exactly two people in the picture. " + m.NOTEXT), latent="image1")
still("c41n", [m.YT_P, m.XM_P], (
    f"{m.PRE} {DIN}. Seen exactly side-on at chest height, a two-shot of exactly two people standing face to face, an arm's length apart, both "
    "in profile: on screen LEFT, facing screen right, the young woman from image 1, "
    f"{m.YT}, her two arms reaching forward, BOTH of her hands resting on the two shoulders of the girl in front of her, brows drawn up and "
    "together, eyes looking down at the girl's face, lips pressed. On screen RIGHT, facing screen left, ONLY ONE girl, the girl from image 2, "
    f"{m.XM}, crying, head bowing, brows crumpled, {TEARS.replace('her', 'the girl’s', 1)}, mouth corners pulled down, lips trembling. Behind "
    "them only an out-of-focus dark doorway and the edge of one dark wooden cupboard. Nobody looks at the camera. There are exactly two people "
    "in the picture; no other person anywhere. " + m.NOTEXT))
still("c38", ["PICK:c38"], (
    "Edit image 1: replace the hanging lamp with one plain white dome-shaded pendant lamp giving the same warm light; no Chinese lantern, no "
    "bamboo shade, no tassel. " + KEEP + m.NOTEXT), latent="image1")
HANDS = ("her moon-white cotton cuffs folded back to the wrist, both hands wet with a little soap foam, behind them only an out-of-focus white "
         "sink; clear morning light. Only the hands; no face, no other person. ")
still("c17", [RING, m.YT_P], (
    f"{m.PRE.replace('image 1', 'image 2')} An extreme close-up, the camera fixed: in the centre of the frame a young woman's LEFT hand, back of "
    "the hand up, fingers slightly spread; on her left ring finger the thick old silver ring of image 1, turned so its square face is hidden "
    "against her palm and only the plain silver band shows on the back of the finger. From the right edge of the frame only the tips of her bare "
    "right thumb and forefinger reach in and pinch the silver band; no ring on the right hand. " + HANDS + m.NOTEXT))
still("c20", [RING, m.YT_P], (
    f"{m.PRE.replace('image 1', 'image 2')} A close-up looking down, as if through her own eyes: a young woman's LEFT hand open, palm up, in the "
    "centre of the frame; the thick old silver ring of image 1 on her left ring finger with its square face on the palm side, and her bare RIGHT "
    "THUMB pressed flat over that square face, covering it completely so none of it shows; only the silver band is visible; no ring on the right "
    "hand. " + HANDS + m.NOTEXT))


def main():
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S), "stills")


if __name__ == "__main__":
    main()
