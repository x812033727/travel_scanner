#!/usr/bin/env python3
"""First-frame still prompts for tai-nainai e006 (2026-11-10 種田 rewrite) -> stills.json, same format as e005ff/stills.json.

Rules (lessons.md 2026-11-09/10): no foreground person's name, no dialogue, first-frame pose only, MEDIUM CLOSE-UP chest up for speakers,
"the woman/man from image 1, alone", blurred-shoulder foreground with costume colours in caps, closing exactly-N-people sentence,
"no subtitles, no captions, no text anywhere", three-quarter face with eyes clearly to the left/right.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "stills.json"
PRE = "A single still frame, photographic live-action, realistic skin and fabric, keeping the look of image 1."
NOTEXT = "No subtitles, no captions, no text anywhere in the picture."
ONE_F = "There is exactly one person in the picture; no second person, no reflection of her anywhere. " + NOTEXT
ONE_M = "There is exactly one person in the picture; no second person, no reflection of him anywhere. " + NOTEXT
OTS = "There are exactly two people in the picture: one clear person and one blurred shoulder at the edge; no other head, shoulder or person anywhere. " + NOTEXT
MCU = "a MEDIUM CLOSE-UP, chest up, filling half the frame"

YT_P = "yuetang-18-portrait-t1.png"
JMB_P = "jiangmubai-portrait-t1.png"
FB_P = "fubo-portrait-t1.png"
ZY_P = "zhiyuan-portrait-t1.png"
MF_P = "meifeng-portrait-t1.png"
XM_P = "xiaoman-damp-t1.png"
HALL_SET = "set-shenjia-zhengting-day-t1.png"
KIT_SET = "set-shenjia-chufang-day-t1.png"
DIN_SET = "set-shenjia-fanting-t1.png"

YT = ("in a moon-white high-collared cotton shirt with fabric frog buttons fastened to the throat, one thick black braid over her right shoulder, "
      "a thick old silver ring only on her left ring finger, her right hand bare")
JMB = "in gold-rimmed glasses on his nose, neatly side-parted black hair, a navy suit, a light blue shirt and a burgundy tie"
FB = "a very old man with very short white hair, in a neatly ironed LIGHT BLUE-GREY Chinese-style jacket with fabric frog buttons, a silver watch chain at a button"
ZY = "with short neat black hair, a white pharmacist's coat worn open over a dark navy shirt, the white coat sleeves pushed up to mid-forearm"
MF = "with big glossy dark chestnut curls, a pearl necklace, red nails and a fitted WINE-RED long-sleeved knit dress with a high round neckline"
XM = ("a high-school girl with straight blunt bangs and a high ponytail, in a navy school blazer one size too big over a white shirt with a navy ribbon tie, "
      "her bangs and the shoulders of her blazer damp, her face clean, no school bag")

HALL = "A clear cold morning inside the main hall of an old Chinese family house, the lamps off"
HALL_HER = "behind her only a cream plaster wall and the dark wooden side of a tall grandfather clock, its face out of the picture; no window, no lantern"
HALL_RIGHT = "behind {w} only a plain wooden door and tall wooden lattice doors with soft morning sunlight; no lantern, no second table"
KIT = "A clear morning inside an old house kitchen, no lamp on"
KIT_HER = "behind her only an out-of-focus window over a white sink and white wall tiles"
KIT_FB = "behind him only an out-of-focus open door in the wall with a sunlit stone-paved courtyard path beyond it"
DIN = "Night in the dining room of an old Chinese family house"
DIN_HER = "behind her only a cream wall and one black night window; no lantern, no second lamp"
DIN_DOOR = "behind {w} only a dark open doorway and the edge of one dark wooden cupboard; no lit lamp beyond the doorway"
LAMP = "warm light from one pendant lamp above"

FG_YT_R = "At the LEFT edge of the frame: a young woman's right shoulder in a MOON-WHITE high stand-up collar with one thick BLACK braid lying over it, very close to the lens, soft and out of focus, no face."
FG_YT_L = "At the RIGHT edge of the frame: a young woman's left shoulder in a MOON-WHITE high stand-up collar and the back of her glossy BLACK hair, very close to the lens, soft and out of focus, no face."
FG_JMB = "At the RIGHT edge of the frame: a seated man's left shoulder in a NAVY suit and the back of his side-parted BLACK hair, very close to the lens, soft and out of focus, no face."
FG_FB_L = "At the RIGHT edge of the frame: an old man's left shoulder in a LIGHT BLUE-GREY Chinese-style jacket and very short WHITE hair, very close to the lens, soft and out of focus, no face."
FG_FB_R = "At the LEFT edge of the frame: an old man's right shoulder in a LIGHT BLUE-GREY Chinese-style jacket and very short WHITE hair, very close to the lens, soft and out of focus, no face."
FG_ZY = "At the RIGHT edge of the frame: a man's left shoulder in a WHITE pharmacist's coat and short BLACK hair, very close to the lens, soft and out of focus, no face."
FG_XM = "At the RIGHT edge of the frame: a girl's left shoulder in a damp NAVY school blazer and a high BLACK ponytail, very close to the lens, soft and out of focus, no face."

FACE_L = "face in three-quarter profile turned toward screen left, eyes clearly to the left"
FACE_R = "face in three-quarter profile turned toward screen right, eyes clearly to the right"

S = []


def still(shot, refs, prompt, shares=()):
    S.append({"shot": shot, "shares_with": list(shares), "refs": refs, "prompt": prompt})


# ---- 第一場：正廳（白天） ----
still("c01", [FB_P, YT_P, HALL_SET], (
    f"{PRE} {HALL}, seen from just inside the front door as in image 3: one long red-wood table running back into the hall with red-wood chairs along it, a long narrow "
    "side table against the back wall under one blank empty frame, a tall grandfather clock on the left wall with its face turned away into shadow, a wooden staircase and a "
    "door at the back left, tall lattice doors on the right wall letting in slanting morning sunlight, both ceiling lanterns unlit; there is only this one long table. "
    "The edge of the front door frame in the foreground. In the middle foreground, seen only from behind: a man's back in a NAVY suit with side-parted BLACK hair, a dark "
    "brown leather folder with a brass clasp under his left arm, no face. Half a step ahead of him on screen right: the old man from image 1, " + FB + ", walking, his head "
    "turned back toward the man behind him, eyes respectful, lips closed. At the back left, coming out of the door beside the staircase: the young woman from image 2, " + YT +
    ", a navy ankle-length skirt, carrying a plain light wooden tray with one small purple-clay teapot and three small white teacups in both hands, brows slightly drawn, "
    "eyes on the man in the suit, lips closed. There are exactly three people in the picture: the man seen from behind, the old man and the young woman; no other person "
    "anywhere. " + NOTEXT))
still("c04", [FB_P], (
    f"{PRE} {HALL}; {HALL_RIGHT.format(w='him')}. A medium close-up, chest up: the old man from image 1, alone, {FB}, standing beside a plain wooden door, half turned "
    f"back, his right hand lifted toward the door; soft morning sunlight from screen right on half his face. His {FACE_L}, toward someone far off to the left of the lens; "
    "brows level, eyes respectful, mouth corners drawn down, chin slightly tucked, lips closed, not smiling, never looking at the camera. " + ONE_M))
still("c05", [YT_P], (
    f"{PRE} {HALL}; {HALL_HER}. {FG_JMB} On screen left, {MCU}: the young woman from image 1, alone, {YT}, both hands already folded at her waist at the bottom edge of the frame, one small white teacup already on the table in front of the blurred man at the bottom edge; "
    f"soft morning sunlight from screen right on her shoulder. Her {FACE_R}, eyes on the blurred man, brows level, chin slightly tucked, lips closed, calm and serious, not "
    "smiling, never looking at the camera. " + OTS), shares=["c11"])
still("c06", [JMB_P], (
    f"{PRE} {HALL}; {HALL_RIGHT.format(w='him')}. {FG_YT_R} On screen right, {MCU}: the man from image 1, alone, {JMB}, seated on a red-wood chair, a closed dark brown "
    "leather folder with a brass clasp clamped under his left arm; the edge of a red-wood table and one small white teacup at the bottom edge of the frame. His "
    f"{FACE_L}, eyes cool behind his lenses and on the blurred woman, lips pressed into a thin polite line, brows still, chin raised a little, not smiling, never looking at "
    "the camera. " + OTS), shares=["c08"])
still("c07", [YT_P], (
    f"{PRE} {HALL}; {HALL_HER}. A MEDIUM CLOSE-UP, chest up, filling half the frame: the young woman from image 1, alone, {YT}; soft morning sunlight from screen right on her shoulder and half her face. "
    f"Her {FACE_R}, eyes steady on someone far off to the right of the lens, brows slightly drawn, lips closed, chin tucked, not smiling, never looking at the camera. " + ONE_F))
still("c09", [YT_P], (
    f"{PRE} {HALL}; seen from table height looking up, behind her only an out-of-focus cream upper wall and dark wooden ceiling beams. A low-angle MEDIUM CLOSE-UP, chest up, filling half the frame: the "
    f"young woman from image 1, alone, {YT}, back very straight, both hands folded at her waist at the bottom edge of the frame; morning sunlight slanting from screen right "
    f"across her shoulder and half her face. Her {FACE_R}, eyes clear and fixed on someone far off to the right of the lens, brows level, chin lifted slightly, lips closed, "
    "not smiling, never looking at the camera. " + ONE_F))
still("c10", [JMB_P], (
    f"{PRE} {HALL}; {HALL_RIGHT.format(w='him')}. A close-up, chest up: the man from image 1, alone, {JMB}, seated; morning sunlight from screen right glinting on his "
    f"glasses, which have slid halfway down his nose. His {FACE_L}, eyes caught and frozen behind the lenses on someone far off to the left of the lens, brows raised, lips pressed tight, chin pulled in, not "
    "smiling, never looking at the camera. " + ONE_M))
still("c14", [JMB_P], (
    f"{PRE} {HALL}; {HALL_RIGHT.format(w='him')}. {FG_YT_R} On screen right, {MCU}, with room above his head: the man from image 1, alone, {JMB}, standing, a closed black "
    "hard-cover folder and a dark brown leather folder stacked under his left arm, his right hand at his jacket button. His "
    f"{FACE_L}, eyes narrowed behind his lenses on the blurred woman, brows pulled low, lips tight, chin raised, not smiling, never looking at the camera. " + OTS))
still("c15", [YT_P], (
    f"{PRE} {HALL}; {HALL_HER}. {FG_FB_L} On screen left, {MCU}: the young woman from image 1, alone, {YT}, her bare right hand setting a small white teacup on a plain "
    "light wooden tray with a small purple-clay teapot at the bottom edge of the frame; soft morning sunlight from screen right on her shoulder. Her "
    f"{FACE_R}, eyes on the blurred old man, brows pressed low, lips closed, chin tucked, not smiling, never looking at the camera. " + OTS))

# ---- 第二場：廚房（白天） ----
still("c16", [YT_P, FB_P, KIT_SET], (
    f"{PRE} {KIT}, seen from the front of the room toward the back wall as in image 3: an open door in the left wall with a sunlit stone path beyond, a white sink under a "
    "window in the middle of the back wall, an old white gas stove with two pots on the right, a doorway to a laundry room in the right wall, one square wooden table with "
    "four stools in the middle; there is only this one table. A corner of the table along the bottom edge. On screen right, side-on at the sink: the young woman from "
    f"image 1, {YT}, a navy ankle-length skirt, cuffs folded back to the wrist, rinsing a small white teacup, a plain light wooden tray with a small purple-clay teapot and "
    "small white teacups on the counter beside her; brows slightly drawn, eyes lowered to her hands, lips pressed. On screen left, stepping in through the open door: the old "
    f"man from image 2, {FB}, hands empty, eyes on her, lips closed. There are exactly two people in the picture; no other person anywhere. " + NOTEXT))
still("c18", [YT_P], (
    f"{PRE} {KIT}; {KIT_HER}. {FG_FB_R} On screen right, {MCU}: the young woman from image 1, alone, {YT}, cuffs folded back to the wrist, both hands at her waist at the "
    f"bottom edge of the frame; morning light from the window behind her rims her outline. Her {FACE_L}, eyes on the blurred old man, brows knitted, mouth corners turned "
    "down, lips closed, not smiling, never looking at the camera. " + OTS), shares=["c22"])
still("c19", [FB_P], (
    f"{PRE} {KIT}; {KIT_FB}. {FG_YT_L} On screen left, {MCU}: the old man from image 1, alone, {FB}, leaning in a little. His {FACE_R}, eyes on the blurred young woman, "
    "brows drawn together, lips pressed, chin slightly tucked, not smiling, never looking at the camera. " + OTS), shares=["c23"])
still("c21", [YT_P], (
    f"{PRE} {KIT}; behind her only out-of-focus white wall tiles and a corner of a window frame. A close-up, chest up: the young woman from image 1, alone, {YT}, cuffs "
    "folded back, head bowed, her hands below the bottom edge of the frame; morning light from screen right on half her face. Her face in three-quarter profile turned "
    "toward screen left, eyes lowered to the lower left, eyes a little wet at the rims, brows drawn gently up and together, lips closed, not smiling, never looking at the "
    "camera. " + ONE_F))
still("c24", [YT_P], (
    f"{PRE} {KIT}; behind her only out-of-focus white wall tiles and a corner of a window frame. A MEDIUM CLOSE-UP, chest up, filling half the frame: the young woman from image 1, alone, {YT}, cuffs "
    "folded back, both hands folded at her waist at the bottom edge of the frame with the ringed left hand underneath; morning light from screen right on her face. Her "
    f"{FACE_L}, eyes clear and fixed on someone far off to the left of the lens, brows smooth, chin lifted slightly, lips closed, not smiling, never looking at the camera. " + ONE_F))

# ---- 第三場：飯廳（夜） ----
still("c25", [YT_P, MF_P, DIN_SET], (
    f"{PRE} {DIN}, seen from a corner of the room as in image 3: one long dark wooden table running back into the room with a row of empty high-backed wooden chairs on both "
    "sides and blue-and-white bowls and chopsticks at every place; two windows in the left wall, black at night; one white pendant lamp lit above the table, the only lamp; "
    "an open doorway at the back right, dark beyond, and one dark wooden cupboard beside it; only this one cupboard. A stack of blue-and-white bowls at the bottom edge. "
    f"Middle left, seated at the window side of the table, head bowed: the woman from image 2, {MF}, a phone in her left hand with its back to the camera, brows arched, "
    f"eyes lowered to the phone, red lips pressed. At the far end of the table by the doorway, standing: the young woman from image 1, {YT}, a navy ankle-length skirt, a "
    "long-handled ladle in her bare right hand, her left hand on a lidded white porcelain soup pot that is steaming, brows drawn tight, eyes on an empty bowl at an empty "
    "chair, lips closed. There are exactly two people in the picture; no other person anywhere. " + NOTEXT))
still("c26", [YT_P], (
    f"{PRE} {DIN}; {DIN_HER}. {FG_FB_L} On screen left, {MCU}: the young woman from image 1, alone, {YT}, both hands folded at her waist at the bottom edge of the frame; "
    f"{LAMP} on her face. Her {FACE_R}, eyes on the blurred old man, brows squeezed together, mouth corners turned down, lips closed, not smiling, never looking at the "
    "camera. " + OTS))
still("c27", [FB_P], (
    f"{PRE} {DIN}; {DIN_DOOR.format(w='him')}. {FG_YT_R} On screen right, {MCU}: the old man from image 1, alone, {FB}; {LAMP}. His {FACE_L}, eyes on the blurred young "
    "woman, brows knitted, lips tight, not smiling, never looking at the camera. " + OTS))
still("c28", [FB_P], (
    f"{PRE} {DIN}; behind him only an out-of-focus dark wooden cupboard and a cream wall; no doorway in the picture. A medium close-up, chest up: the old man from image 1, "
    f"alone, {FB}; {LAMP} from screen left on his face. His face in profile turned toward screen right, eyes clearly to the right, toward something beyond the right edge "
    "of the frame, brows raised, lips slightly parted, not smiling, never looking at the camera. " + ONE_M))
still("c29", [ZY_P], (
    f"{PRE} {DIN}; the edge of a doorway frame along the right edge of the picture, the dark open doorway behind him, the only doorway in view; {LAMP}. A medium shot, "
    f"waist up: the man from image 1, alone, {ZY}, just stepped in through the doorway and striding toward screen left, a folded white sheet of paper in his right hand "
    "with its blank back to the camera. His face in three-quarter profile turned toward screen left, eyes clearly to the left, brows pulled down hard, jaw clenched, lips "
    "pressed, not smiling, never looking at the camera. " + ONE_M))
still("c31", [ZY_P], (
    f"{PRE} {DIN}; seen from table height looking up, behind him only a dark ceiling and an out-of-focus dark doorway. A low-angle medium close-up, chest up: the man from "
    f"image 1, alone, {ZY}, standing at a dark wooden table, leaning forward over it, his right hand holding a folded white sheet at the bottom edge of the frame, its "
    f"blank back to the camera; {LAMP}. His face in three-quarter profile turned down toward screen left, eyes clearly to the left and down, on someone well off to the left of the lens, brows pulled low, jaw clenched, lips "
    "pressed thin, not smiling, never looking at the camera. " + ONE_M))
still("c32", [MF_P, ZY_P], (
    f"{PRE} {DIN}; seen at eye level from across a dark wooden table, behind them only a cream wall and one black night window. In the left foreground, seated: the woman "
    f"from image 1, {MF}, head bowed, her face in three-quarter profile turned toward screen right, a phone in her left hand with its back to the camera, a porcelain spoon in her right hand over a blue-and-white bowl; eyes down on the "
    "phone, one brow arched, one corner of her red lips pulled sideways. At the back right, standing at the corner of the table: the man from image 2, "
    f"{ZY}, his right hand pressed on a folded white sheet on the table, his face turned down toward her at screen left, eyes clearly to the left on her bowed head, brows "
    f"pulled low, jaw clenched, lips pressed thin, not smiling; {LAMP}. Neither looks at the camera. There are exactly two people in the picture; no other person anywhere. " + NOTEXT))
still("c34", [YT_P], (
    f"{PRE} {DIN}; {DIN_HER}. {FG_ZY} On screen left, {MCU}: the young woman from image 1, alone, {YT}, both hands folded at her waist at the bottom edge of the frame; "
    f"{LAMP} on her face. Her {FACE_R}, eyes on the blurred man, brows smooth and level, chin slightly tucked, lips closed, not smiling, never looking at the camera. " + OTS))
still("c35", [ZY_P], (
    f"{PRE} {DIN}; {DIN_DOOR.format(w='him')}. {FG_YT_R} On screen right, {MCU}: the man from image 1, alone, {ZY}, his right hand stopped above a small white saucer of red "
    f"goji berries at the bottom edge of the frame; {LAMP}. His {FACE_L}, eyes wide and fixed on the blurred young woman, straight brows knitted and lifting, lips slightly "
    "parted, surprised, not smiling, never looking at the camera. " + OTS))
still("c36", [YT_P], (
    f"{PRE} {DIN}; {DIN_HER}. A MEDIUM CLOSE-UP, chest up, filling half the frame: the young woman from image 1, alone, {YT}, both hands folded at her waist at the bottom edge of the frame; {LAMP} on "
    f"her face. Her {FACE_R}, eyes gentle and fixed on someone far off to the right of the lens, brows smooth, chin slightly tucked, lips closed, not smiling, never looking "
    "at the camera. " + ONE_F))
still("c38", [YT_P, XM_P], (
    f"{PRE} {DIN}; seen side-on at the doorway end of the room, the open doorway dark beyond; in the lower left foreground a corner of a dark wooden table and a lidded white "
    f"porcelain soup pot with no steam; {LAMP}. On screen right, standing in the doorway with her head bowed: the girl from image 2, {XM}, a navy pleated skirt below the "
    "knee, both hands empty at her sides, eyes lowered, lips pressed tight, chin trembling. On screen left, two steps from her at the end of the table: the young woman from "
    f"image 1, {YT}, a navy ankle-length skirt, her face in three-quarter profile toward screen right, brows squeezed together, eyes on the girl, lips closed. Neither looks "
    "at the camera. There are exactly two people in the picture; no other person anywhere. " + NOTEXT))
still("c39", [YT_P], (
    f"{PRE} {DIN}; {DIN_HER}. {FG_XM} On screen left, {MCU}: the young woman from image 1, alone, {YT}, bending a little toward the blurred girl; {LAMP} on her face. Her "
    f"{FACE_R}, eyes on the blurred girl, brows drawn up and together, mouth corners turned down, lips closed, not smiling, never looking at the camera. " + OTS))
still("c40", [XM_P], (
    f"{PRE} {DIN}; {DIN_DOOR.format(w='her')}. {FG_YT_R} On screen right, {MCU}: the girl from image 1, alone, {XM}; {LAMP}. Her {FACE_L}, eyes wet and red-rimmed on the "
    "blurred young woman, brows pushed up and together, mouth corners forced up into a shaky smile that is not a happy one, chin trembling, never looking at the camera. " + OTS))
still("c41", [YT_P, XM_P], (
    f"{PRE} {DIN}; seen side-on, behind them only an out-of-focus dark doorway and the edge of one dark wooden cupboard; {LAMP}. Two people facing each other side-on, not "
    f"toward the camera: on screen left the young woman from image 1, {YT}, both hands resting on the girl's shoulders, her face in profile toward screen right, brows drawn "
    f"up and together, eyes on the girl's face, lips pressed; on screen right the girl from image 2, {XM}, crying, her face in profile toward screen left, head bowing, brows "
    "crumpled, tears on her cheeks, mouth corners pulled down, lips trembling. There are exactly two people in the picture; no other person anywhere. " + NOTEXT))


def main():
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    covered = [s["shot"] for s in S] + [x for s in S for x in s["shares_with"]]
    print(OUT, len(S), "stills covering", len(covered), "shots")


if __name__ == "__main__":
    main()
