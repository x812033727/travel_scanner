#!/usr/bin/env python3
"""第 6 集首格第三輪（2026-11-10）：兩輪都不行的 6 鏡 -> stills-redo3.json。

第二輪獨立挑圖的結論：
- 模型把「前景虛焦的肩膀」「背影」放在句子後面就畫不出來：先寫畫面最前面的東西，再寫主角。
- 場景圖會把鐘面與第二個福伯帶進來（c01）：不給場景圖，正廳用文字寫、不提鐘。
- 一看到紙就往下看（c31）：機位與「眼睛平看」放在提示詞最前面，紙只露一角。
- 兩手扶肩（c41）畫不出來：從已定的 c38（同一個飯廳、同樣兩人側面相對）修圖，`latent image1`，refs 第一張是 pick/c38.png。
- 福伯的唐裝寫成「not dark grey, not charcoal」，跟 c19、c26 接得上。
"""
import json
from pathlib import Path

import make_stills as m
from redo_stills import DIN, FOLDERS, TEARS

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills-redo3.json"
FB = m.FB.replace("LIGHT BLUE-GREY", "LIGHT BLUE-GREY (pale, not dark grey, not charcoal)")
S = []


def still(shot, refs, prompt, latent=None):
    s = {"shot": shot, "shares_with": [], "refs": refs, "prompt": prompt}
    if latent:
        s["latent"] = latent
    S.append(s)


still("c01", [m.FB_P, m.YT_P], (
    f"{m.PRE} THREE people in the main hall of an old Chinese family house on a clear cold morning, the lamps off. "
    "FIRST, in the near foreground filling the lower left third of the frame, seen only from behind and slightly out of focus: the back of a "
    "man's head and shoulders in a NAVY suit, side-parted BLACK hair, a dark brown leather folder under his left arm, no face. "
    f"SECOND, half a step ahead of him on screen right, sharp: ONLY ONE old man, the old man from image 1, {FB}, walking, his head turned back "
    "over his shoulder toward the man behind him, eyes respectful, lips closed. "
    f"THIRD, small at the back left, coming out of a door beside a wooden staircase: the young woman from image 2, {m.YT}, a navy ankle-length "
    "skirt, holding in both hands in front of her a plain light wooden tray with one small reddish-brown clay teapot and three small white "
    "teacups, eyes on the man in the suit, lips closed. Between them one long red-wood table with chairs runs back into the hall; tall lattice "
    "doors on the right wall let in slanting morning sunlight; plain cream walls; no clock anywhere, no lantern lit. There are exactly three "
    "people in the picture; no other person anywhere. " + m.NOTEXT))
still("c14", [m.JMB_P], (
    f"{m.PRE} An over-the-shoulder shot. FIRST, filling the LEFT quarter of the frame, very close to the lens and heavily blurred: a young "
    "woman's right shoulder in a MOON-WHITE high stand-up collar with one thick BLACK braid lying over it, seen from behind, no face. "
    f"Then, on screen right, sharp, {m.MCU}: the man from image 1, {m.JMB}, standing, {FOLDERS}. His face in three-quarter profile turned "
    "toward screen left, toward the blurred woman, eyes clearly to the left, eyes narrowed behind his lenses, brows pulled low, lips tight, "
    "chin raised, cold, NOT smiling, never looking at the camera. A clear cold morning in an old Chinese house; behind him only a plain wooden "
    "door and tall wooden lattice doors with soft morning sunlight; no lantern. " + m.OTS))
still("c16", [m.YT_P, m.FB_P], (
    f"{m.PRE} Exactly two people in an old house kitchen on a clear morning, no lamp on, white wall tiles. On screen right, side-on at a white "
    f"sink under a window: the young woman from image 1, {m.YT}, a navy ankle-length skirt, cuffs folded back to the wrist, rinsing a small "
    "white teacup; ONE silver ring on her LEFT hand only, NO ring on her right hand; a plain light wooden tray with a small reddish-brown clay "
    "teapot and small white teacups on the counter beside her; brows slightly drawn, eyes lowered to her hands, lips pressed. On screen left, "
    f"stepping in through an open door with a sunlit stone path beyond: ONLY ONE old man, the old man from image 2, {FB}, hands empty, his face "
    "in three-quarter profile toward screen right, eyes on her, NOT looking at the camera, lips closed. There are exactly two people in the "
    "picture; no other person anywhere. " + m.NOTEXT))
still("c31", [m.ZY_P], (
    f"{m.PRE} LOW ANGLE: the camera sits at table-top height very close to him, looking UP at his face. EYES LEVEL: his eyes look straight "
    "ahead and level to screen left at someone far away across the room, NOT down. A MEDIUM CLOSE-UP, his face and chest fill the right half "
    f"of the frame: the man from image 1, alone, {m.ZY}, leaning forward with his right hand flat on a dark wooden table edge at the very bottom "
    "of the frame; no paper visible. His face in three-quarter profile toward screen left, brows pulled low, jaw clenched, lips pressed thin, "
    f"not smiling, never looking at the camera. Behind him only a dark ceiling and an out-of-focus dark doorway. {DIN}. " + m.ONE_M))
still("c40", [m.XM_P], (
    f"{m.PRE} ONLY ONE GIRL. A MEDIUM CLOSE-UP, chest up, filling the right half of the frame: the girl from image 1, {m.XM}; warm light from "
    f"above. Her face in three-quarter profile turned toward screen left, eyes clearly to the left on someone just out of the picture, {TEARS}, "
    "brows pushed up and together, mouth corners forced up into a small shaky smile that is not a happy one, chin trembling, never looking at "
    "the camera. At the very LEFT edge of the frame only a soft out-of-focus patch of moon-white fabric, no face, no second head. Behind her only "
    f"a dark open doorway and the edge of one dark wooden cupboard. {DIN}. " + m.ONE_F.replace("exactly one person", "exactly one clear person")))
still("c41", ["PICK:c38", m.XM_P], (
    "Edit image 1, keeping the room, the lamp, the light, the camera angle and both people's faces, hair and clothes exactly the same: "
    "the young woman in moon-white has stepped close to the girl, an arm's length apart, and rests BOTH of her hands on the girl's two "
    "shoulders, her face in profile toward screen right, brows drawn up and together, eyes on the girl's face, lips pressed. The girl, the girl "
    f"from image 2, is crying, head bowing, brows crumpled, {TEARS.replace('her', 'the girl’s', 1)}, mouth corners pulled down, lips trembling. "
    "No other change. There are exactly two people in the picture; no other person anywhere. " + m.NOTEXT), latent="image1")


def main():
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S), "redo stills")


if __name__ == "__main__":
    main()
