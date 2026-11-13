#!/usr/bin/env python3
"""第 6 集首格第二輪：獨立挑圖（2026-11-10）兩張都不行的 11 鏡，照審稿意見改寫 -> stills-redo.json（與 stills.json 同格式）。

審稿抓到的整集問題：
- 飯廳的燈一半畫成紅流蘇中式燈籠：每一鏡飯廳都寫白燈罩吊燈、不要燈籠、牆上沒有字畫。
- 落地鐘的鐘面數字入鏡：要鐘的鏡不再寫鐘。
- 月棠臉偏正面：寫鼻子指向哪一邊、看得到哪一邊臉頰。
- 黑窗會映出人影：飯廳近景不寫窗，改成牆或拉上的深色窗簾。
- 眼淚畫成紅色像血：寫透明的淚、臉上沒有紅痕。
"""
import json
from pathlib import Path

import make_stills as m

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills-redo.json"

DLAMP = ("one plain white dome-shaded pendant lamp is the only lamp, no Chinese lantern, no red tassel anywhere; "
         "no paintings, scrolls or calligraphy on the walls")
DIN = f"Night in the dining room of an old Chinese family house; {DLAMP}"
TURN_L = ("her head turned well to screen left, her nose pointing to the left of the lens, we see more of her right cheek than her left, "
          "eyes clearly to the left")
FG_FB_R_HEAVY = ("At the LEFT edge of the frame: an old man's right shoulder in a LIGHT BLUE-GREY Chinese-style jacket and very short WHITE hair, "
                 "very close to the lens, heavily blurred, no face, no glasses.")
FOLDERS = ("under his LEFT arm, pressed against his side: two folders stacked, a black hard-cover folder on top of a dark brown leather folder "
           "with a brass clasp; his right hand empty at his jacket button")
TEARS = "clear transparent tears on her cheeks, no red marks anywhere on her face"

S = []


def still(shot, refs, prompt):
    S.append({"shot": shot, "shares_with": [], "refs": refs, "prompt": prompt})


still("c01", [m.FB_P, m.YT_P, m.HALL_SET], (
    f"{m.PRE} A clear cold morning inside the main hall of an old Chinese family house, the lamps off, seen from just inside the front door as in image 3. "
    "In the near foreground, filling the lower left third of the frame, seen only from behind: the back of a man in a NAVY suit with side-parted BLACK hair, "
    "a dark brown leather folder with a brass clasp under his left arm, no face. Half a step ahead of him on screen right: the old man from image 1, "
    f"{m.FB}, walking, his head turned back toward the man behind him, eyes respectful, lips closed. At the back left, coming out of the door beside the "
    f"staircase: the young woman from image 2, {m.YT}, a navy ankle-length skirt, carrying in both hands a plain light wooden tray with one small "
    "reddish-brown purple-clay teapot and three small white teacups, brows slightly drawn, eyes on the man in the suit, lips closed. Behind them one long "
    "red-wood table running back into the hall, tall lattice doors on the right wall letting in slanting morning sunlight, both ceiling lanterns unlit; "
    "no clock face visible anywhere. There are exactly three people in the picture: the man seen from behind, the old man and the young woman; "
    "no other person anywhere. " + m.NOTEXT))
still("c14", [m.JMB_P, m.YT_P], (
    f"{m.PRE} A clear cold morning inside the main hall of an old Chinese family house, the lamps off; behind him only a plain wooden door and tall "
    "wooden lattice doors with soft morning sunlight; no lantern, no lamp lit, no second table. At the LEFT edge of the frame: the right shoulder of the "
    "young woman from image 2 in a MOON-WHITE high stand-up collar with her one thick BLACK braid lying over it, very close to the lens, heavily "
    f"blurred, no face. On screen right, {m.MCU}, with room above his head: the man from image 1, alone, {m.JMB}, standing, {FOLDERS}. His face in "
    "three-quarter profile turned toward screen left, eyes clearly to the left, eyes narrowed behind his lenses on the blurred woman, brows pulled low, "
    "lips tight, chin raised, not smiling, never looking at the camera. " + m.OTS))
still("c16", [m.YT_P, m.FB_P], (
    f"{m.PRE} Two people in an old house kitchen on a clear morning, no lamp on. On screen right, side-on at a white sink under a window: the young "
    f"woman from image 1, {m.YT}, a navy ankle-length skirt, cuffs folded back to the wrist, rinsing a small white teacup, a plain light wooden tray "
    "with a small reddish-brown purple-clay teapot and small white teacups on the counter beside her; brows slightly drawn, eyes lowered to her hands, "
    f"lips pressed. On screen left, stepping in through an open door with a sunlit stone path beyond: the old man from image 2, {m.FB}, hands empty, "
    "eyes on her, lips closed. White wall tiles, an old white gas stove at the right edge, a corner of a square wooden table along the bottom edge. "
    "There are exactly two people in the picture; no other person anywhere. " + m.NOTEXT))
still("c18", [m.YT_P], (
    f"{m.PRE} A clear morning inside an old house kitchen, no lamp on; {m.KIT_HER}. {FG_FB_R_HEAVY} On screen right, {m.MCU}: the young woman from "
    f"image 1, alone, {m.YT}, cuffs folded back to the wrist, both hands at her waist at the bottom edge of the frame; morning light from the window "
    f"behind her rims her outline. {TURN_L}, on the blurred old man, brows knitted, mouth corners turned down, lips closed, not smiling, never "
    "looking at the camera. " + m.OTS))
still("c25", [m.YT_P, m.MF_P], (
    f"{m.PRE} {DIN}; seen from a corner of the room: one long dark wooden table running back into the room, empty high-backed wooden chairs on both "
    "sides, blue-and-white bowls and chopsticks at every place, all bowls empty; a dark open doorway at the back right and one dark wooden cupboard "
    "beside it; the left wall plain cream plaster. ONLY ONE woman in a wine-red dress: in the MIDDLE LEFT of the frame, seated sideways at the "
    f"near half of the table, head bowed, the woman from image 2, {m.MF}, a phone in her left hand with its back to the camera, eyes lowered to the "
    "phone, red lips pressed, her face in three-quarter profile toward screen left. ONLY ONE woman in moon-white: at the FAR END of the table by the "
    f"doorway, standing, small in the frame, the young woman from image 1, {m.YT}, a navy ankle-length skirt, a long-handled ladle in her bare right "
    "hand, her left hand on a lidded white porcelain soup pot, brows drawn tight, eyes on an empty bowl at an empty chair, lips closed. There are "
    "exactly two people in the picture; no other person anywhere. " + m.NOTEXT))
still("c28", [m.FB_P], (
    f"{m.PRE} {DIN}; behind him only an out-of-focus dark wooden cupboard and a cream wall; no doorway, no window in the picture. A medium "
    f"close-up, chest up: the old man from image 1, alone, {m.FB}; warm lamp light from screen right on the right side of his face. His face in "
    "profile turned toward screen right, his nose pointing to screen right, the back of his head toward screen left, eyes clearly to the right, "
    "toward something beyond the right edge of the frame, brows raised, lips slightly parted, not smiling, never looking at the camera. " + m.ONE_M))
still("c29", [m.ZY_P], (
    f"{m.PRE} {DIN}; the edge of a doorway frame along the right edge of the picture, the dark open doorway behind him, the only doorway in view; "
    f"no window in view. A medium shot, waist up: the man from image 1, alone, {m.ZY}, just stepped in through the doorway and striding toward screen "
    "left, ONE folded white sheet of paper in his right hand with its blank back to the camera. His face in three-quarter profile turned toward screen "
    "left, eyes clearly to the left, brows pulled down hard, jaw clenched, lips pressed, not smiling, never looking at the camera. " + m.ONE_M))
still("c31", [m.ZY_P], (
    f"{m.PRE} {DIN}; the camera at table-top height, very close to him and looking up; behind him only a dark ceiling and an out-of-focus dark "
    f"doorway. A low-angle MEDIUM CLOSE-UP: the man from image 1, alone, {m.ZY}, his face and chest fill the right half of the frame, leaning forward "
    "over a dark wooden table, only one corner of a folded white sheet showing at the bottom edge of the frame under his right hand. His face in "
    "three-quarter profile turned toward screen left, eyes clearly to the left and level, on someone far off to the left of the lens, NOT looking down "
    "at the table, brows pulled low, jaw clenched, lips pressed thin, not smiling, never looking at the camera. " + m.ONE_M))
still("c32", [m.MF_P, m.ZY_P], (
    f"{m.PRE} {DIN}; seen at eye level from across a dark wooden table, behind them only a plain cream wall and a closed dark curtain; no window "
    f"glass, no reflection anywhere. In the left foreground, seated: the woman from image 1, {m.MF}, head bowed, her face in three-quarter profile "
    "turned toward screen right, a phone in her left hand with its back to the camera, a porcelain spoon in her right hand over a blue-and-white bowl; "
    "eyes down on the phone, one brow arched, one corner of her red lips pulled sideways. At the back right, standing at the corner of the table: the "
    f"man from image 2, {m.ZY}, his right hand pressed on a folded white sheet on the table, his face turned down toward her at screen left, eyes "
    "clearly to the left on her bowed head, brows pulled low, jaw clenched, lips pressed thin, not smiling. Neither looks at the camera. There are "
    "exactly two people in the picture; no other person anywhere. " + m.NOTEXT))
still("c40", [m.XM_P, m.YT_P], (
    f"{m.PRE} {DIN}; behind her only a dark open doorway and the edge of one dark wooden cupboard. At the LEFT edge of the frame: the right shoulder "
    "of the young woman from image 2 in her MOON-WHITE high stand-up collar with her one thick BLACK braid lying over it, very close to the lens, "
    f"heavily blurred, no face. On screen right, {m.MCU}: ONLY ONE girl, the girl from image 1, {m.XM}; warm lamp light from above. Her face in "
    f"three-quarter profile turned toward screen left, eyes clearly to the left, eyes wet and slightly red-rimmed on the blurred young woman, {TEARS}, "
    "brows pushed up and together, mouth corners forced up into a shaky smile that is not a happy one, chin trembling, never looking at the camera. "
    + m.OTS))
still("c41", [m.YT_P, m.XM_P], (
    f"{m.PRE} {DIN}; seen side-on, behind them only an out-of-focus dark doorway and the edge of one dark wooden cupboard. Two people standing close, "
    f"an arm's length apart, facing each other side-on, not toward the camera: on screen left the young woman from image 1, {m.YT}, her two hands "
    "resting on the girl's two shoulders, her face in profile toward screen right, brows drawn up and together, eyes on the girl's face, lips "
    f"pressed; on screen right ONLY ONE girl, the girl from image 2, {m.XM}, crying, her face in profile toward screen left, head bowing, brows "
    f"crumpled, {TEARS.replace('her', 'the girl’s', 1)}, mouth corners pulled down, lips trembling. There are exactly two people in the picture; "
    "no other person anywhere. " + m.NOTEXT))


def main():
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S), "redo stills")


if __name__ == "__main__":
    main()
