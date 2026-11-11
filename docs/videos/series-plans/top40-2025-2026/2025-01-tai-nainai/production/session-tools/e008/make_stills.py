#!/usr/bin/env python3
"""First-frame still prompts for tai-nainai e008 (2026-11-11 種田 rewrite) -> stills.json, same format as e007/stills.json:
[{shot, shares_with, refs, prompt[, latent]}]. Each still is drawn at 1312x736, two seeds (the manifest converter sets the size).

26 stills cover 29 shots: c04 also serves c18 (her over Lin Meifeng's shoulder, robe at her chest), c20 also serves c22 (Fu Bo at the kitchen
door), c26 also serves c28 (the door-crack point of view).

refs: names under assets/refs/; `E7PICK:<shot>` is $TN_WORK/e007ff/pick/<shot>.png (episode 7's picked first frame); `PICK:<shot>` is
$TN_WORK/e008ff/pick/<shot>.png. `prop-shubao-t1.png` (the school bag, cut from E7PICK:c18 and cleaned) does not exist yet: the coordinator draws it first.

What episode 7's four rounds taught (handoff ticket, last section of 2026-11-11; e007/redo*_stills.py):
- redrawing a whole frame almost always fails; editing the closest picture usually works. So every wide (c05, c13, c19, c23) and the
  door-crack view (c26) is an EDIT of the set picture (`latent: image1`) that only puts people in; c01 is an edit of episode 7's c29 pick.
- close shots are kept simple: one clear person and at most one blurred shoulder or back of a head, written FIRST ("FIRST, at the RIGHT edge ...");
  the foreground person is never named and is "only the back of the head, no face, no ear, no earring".
- at most two visible faces; a third person is only a back at the frame edge. "ONLY ONE <person>" against doubles; the people count goes last.
- the courtyard has no lanterns or lamps in the text, only "warm yellow light glowing on the corridor walls".
- Lin Meifeng holding the robe ends up wearing it: "she wears her wine-red knit dress and is NOT wearing the white robe; the robe is in her hands".
- Shen Yuetang has no earrings (episode 7 c26, c29 got pearl earrings); NOT smiling, no teeth; no text, no screens, no clock.
- at most three reference pictures per still.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "stills.json"
PRE = "A single still frame, photographic live-action, realistic skin and fabric, keeping the look of image 1."
NOTEXT = "No subtitles, no captions, no text, letters, numbers or signs anywhere in the picture; no screen anywhere."
ONE_F = "There is exactly one person in the picture; no second person, no reflection of her anywhere. " + NOTEXT
ONE_M = "There is exactly one person in the picture; no second person, no reflection of him anywhere. " + NOTEXT
OTS = ("There are exactly two people in the picture: one clear person and one blurred back of a head at the edge; no other head, shoulder or person "
       "anywhere. " + NOTEXT)
KEEP = "Keep everything else exactly the same: the place, the light, the camera angle, faces, hair and clothes. No other change. "
MCU = "a MEDIUM CLOSE-UP, chest up, filling half the frame"
NOSMILE = "NOT smiling, lips together, no teeth showing"
NOLANTERN = "No lanterns, no hanging lamps, no candles anywhere."

YT_P = "yuetang-18-portrait-t1.png"
MF_P = "meifeng-portrait-t1.png"
JY_P = "jianye-portrait-t1.png"
JB_P = "jianbang-portrait-t1.png"
YQ_P = "yuqin-portrait-t1.png"
FB_P = "fubo-portrait-t1.png"
XM_P = "xiaoman-home-t1.png"
ROBE_P = "prop-shouyi-t1.png"
BAG_P = "prop-shubao-t1.png"  # to be drawn from E7PICK:c18
KEYS_P = "prop-fubo-yaoshichuan-t1.png"
YARD_SET = "set-shenjia-yuanzi-t1.png"
KIT_SET = "set-shenjia-chufang-t1.png"   # retouched first: no wall frames, a bare bulb instead of the lantern lamp
CORR_SET = "set-shenjia-huilang-t1.png"  # retouched first: no text on the bin, the near left door open a crack with white light
ROOM_SET = "set-shenjia-xiaomanfang-t1.png"

YT = ("in a MOON-WHITE high-collared cotton shirt with fabric frog buttons fastened to the throat, one thick BLACK braid over her right shoulder, "
      "no earrings")
YT_FULL = YT + ", a NAVY ankle-length cotton skirt and black cloth shoes"
MF = "with big glossy dark chestnut curls, a pearl necklace of round white pearls, red nails and a fitted WINE-RED long-sleeved knit dress with a high round neckline"
NOTWEAR = "She wears her wine-red knit dress and is NOT wearing the white robe; the robe is only in her hands."
JY = "a tall heavyset man with oiled black hair slicked back, in a tailored BROWN double-breasted suit with a cream shirt and a dark brown tie"
JB = "a man with short black hair greying at the temples and thin black-framed glasses, in a slightly worn CHARCOAL-GREY suit, a white shirt buttoned to the top, no tie"
YQ = "with short silver-white hair, a NAVY wool cardigan over a light grey high-neck blouse, seated in a plain black-framed manual wheelchair"
FB = ("a very old man with very short white hair, in a neatly ironed LIGHT BLUE-GREY (pale, not dark grey) Chinese-style jacket with fabric frog "
      "buttons, a silver watch chain at a button")
ROBE_FOLD = "the off-white robe of the robe picture folded into a neat square (only the robe, no trousers)"
YARD = ("Dusk just after dark in the inner stone courtyard of an old Chinese family house, warm yellow light glowing on the corridor walls, dark red "
        "wooden pillars")

FG_YT_L = ("FIRST, at the RIGHT edge of the frame: only the back of a young woman's head with glossy BLACK hair and her left shoulder in a MOON-WHITE high "
           "stand-up collar, very close to the lens, soft and out of focus; no face, no ear, no cheek, no earring.")
FG_MF_R = ("FIRST, at the LEFT edge of the frame: only the back of a woman's head with dark chestnut curls and her right shoulder in a WINE-RED knit "
           "sleeve, very close to the lens, soft and out of focus; no face, no ear, no cheek.")
FG_YQ = ("FIRST, at the LOWER LEFT edge of the frame: only the back of an old woman's head with short silver-white hair, very close to the lens, soft and "
         "out of focus; no face.")
FACE_L = "face in three-quarter profile turned toward screen left, eyes clearly to the left, never looking at the camera"
FACE_R = "face in three-quarter profile turned toward screen right, eyes clearly to the right, never looking at the camera"
YT_BACK_R = ("FIRST, at the RIGHT edge of the foreground, cut by the frame edge and softly out of focus, seen only from behind from the waist up: a slim "
             "young woman in a MOON-WHITE high-collared shirt, one long BLACK braid down her right shoulder; only the back of her head, no face, no ear, no "
             "earring.")

S = []


def still(shot, refs, prompt, shares=(), latent=None):
    s = {"shot": shot, "shares_with": list(shares), "refs": refs, "prompt": prompt}
    if latent:
        s["latent"] = latent
    S.append(s)


# ---- 第一場：院子 ----
still("c01", ["E7PICK:c29"], (
    "Edit image 1. Only change: the woman in wine-red lifts her chin a little higher and draws a breath as if about to shout, eyebrows still raised high, "
    "eyes still glaring toward screen right, lips still closed, not smiling. She still holds the white robe up by its shoulders, held out toward screen "
    "right, and is NOT wearing it. The blurred shoulder at the right edge shows only the back of the head: no ear, no earring. " + NOLANTERN + " " + KEEP
    + NOTEXT), latent="image1")
still("c02", [YT_P], (
    f"{PRE} {YARD}; behind her only out-of-focus corridor pillars and a dark wall. {MCU}: the young woman from image 1, alone, {YT}, her hands below the "
    "bottom edge of the frame; warm yellow light from screen left on half her face. Her face in three-quarter profile turned toward screen left, eyes "
    f"looking down and to the left, brows drawn together, chin tucked, {NOSMILE}. " + NOLANTERN + " " + ONE_F))
still("c03", [MF_P, YT_P, ROBE_P], (
    f"{PRE} {YARD}; seen side-on beside a round stone table, behind them only out-of-focus dark red pillars and warm yellow wall light. A medium "
    f"two-shot from the waist up, the two facing each other side-on, never looking at the camera. On screen left: ONLY ONE woman, the woman from image 1, "
    f"{MF}, her right hand gripping one shoulder of the off-white robe of image 3 (only the robe, no trousers). {NOTWEAR} On screen right: ONLY ONE young "
    f"woman, the young woman from image 2, {YT}; her bare right hand already holds the other shoulder of the robe, so the robe hangs open between them; "
    "her left hand down at her side. The woman in wine-red: one brow raised, eyes narrowed, red lips twisted to one side, no teeth. The young woman: brows "
    f"level, eyes on the other woman's face, chin tucked, {NOSMILE}. There are exactly two people in the picture. " + NOLANTERN + " " + NOTEXT))
still("c04", [YT_P, ROBE_P], (
    f"{PRE} {YARD}. {FG_MF_R} On screen right, {MCU}: the young woman from image 1, alone, {YT}, holding {ROBE_FOLD} against her chest with both hands; "
    f"behind her only out-of-focus corridor pillars and a dark wall. Her {FACE_L}, eyes on the blurred woman, brows level, chin slightly tucked, {NOSMILE}. "
    + NOLANTERN + " " + OTS), shares=["c18"])
still("c05", [YARD_SET, MF_P, JY_P], (
    "Edit image 1: keep the courtyard exactly as it is (the round stone table and stools, the old well on the left, the bamboo poles on the right, the dark "
    "red corridor pillars, the dark lattice doors at the far end, the deep blue dusk sky), with warm yellow light glowing on the corridor walls and no "
    f"lanterns, lamps or candles anywhere, and put people into it. {YT_BACK_R} In the middle, standing by the left side of the round stone table: ONLY ONE "
    f"woman, the woman from image 2, {MF}, black low heels, her hands empty, her face toward the young woman, one brow raised, one corner of her red lips "
    "curled up, no teeth. On the left, just stepping in from the left corridor toward her: ONLY ONE man, the man from image 3, " + JY + ", polished brown "
    f"shoes, his face toward screen right, brows knitted, eyes on the young woman, lips pressed tight, {NOSMILE}. There are exactly three people in the "
    "picture: the young woman seen from behind, the woman and the man; no other person anywhere. " + NOTEXT), latent="image1")
still("c06", [JY_P], (
    f"{PRE} {YARD}. {FG_YT_L} On screen left, {MCU}: the man from image 1, alone, {JY}; behind him only out-of-focus dark red pillars and warm yellow wall "
    f"light. His {FACE_R}, brows knitted hard, eyes impatient, mouth corners pulled down, chin raised, {NOSMILE}. " + NOLANTERN + " " + OTS))
still("c07", [YT_P, ROBE_P], (
    f"{PRE} {YARD}; seen from low down looking up, behind her only out-of-focus corridor pillars and the deep blue sky. {MCU}: the young woman from image 1, "
    f"alone, {YT}, holding {ROBE_FOLD} against her chest; warm yellow light from screen left on half her face. Her {FACE_L}, back very straight, chin "
    f"lifted a little, brows level, {NOSMILE}. " + NOLANTERN + " " + ONE_F))
still("c08", [MF_P], (
    f"{PRE} {YARD}. {FG_YT_L} On screen left, {MCU}: the woman from image 1, alone, {MF}, her arms folded across her chest, her hands empty; behind her only "
    "out-of-focus dark red pillars and warm yellow wall light. Her {face}, one brow cocked, eyes half-lidded, one corner of her red lips curled up in a sneer, "
    "no teeth, chin raised high. ".replace("{face}", FACE_R) + NOLANTERN + " " + OTS))
still("c09", [YT_P], (
    f"{PRE} {YARD}; behind her only out-of-focus corridor pillars and a dark wall. {MCU}: the young woman from image 1, alone, {YT}, the edge of a folded "
    f"white cloth at her chest at the bottom edge of the frame; warm yellow light from screen left on her face. Her {FACE_L}, eyes darkened, brows lowered "
    f"a little, chin tucked, {NOSMILE}. " + NOLANTERN + " " + ONE_F))
still("c10", [YT_P, ROBE_P], (
    f"{PRE} {YARD}. {FG_MF_R} On screen right, a MEDIUM SHOT from the waist up: the young woman from image 1, alone, {YT}, a navy ankle-length skirt, "
    f"stooping a little like an old woman, both hands holding {ROBE_FOLD} in front of her waist; behind her only out-of-focus corridor pillars and a dark "
    f"wall. Her {FACE_L}, brows drooping, eyelids half lowered, chin pushed forward, {NOSMILE}. " + NOLANTERN + " " + OTS))
still("c11", [MF_P, JY_P], (
    f"{PRE} {YARD}; behind them only out-of-focus dark red pillars and warm yellow wall light. A medium two-shot from the waist up, both facing screen "
    f"right, never looking at the camera: in front on screen left ONLY ONE woman, the woman from image 1, {MF}, her arms folded across her chest; half a "
    f"step behind her on her right ONLY ONE man, the man from image 2, {JY}. The woman: a frozen sneer, eyes wide, brows up, mouth corners stiffly curled, "
    "no teeth. The man: brows raised, eyes wide, lips closed, no smile, no teeth. There are exactly two people in the picture. " + NOLANTERN + " " + NOTEXT))
still("c12", [MF_P], (
    f"{PRE} {YARD}. {FG_YT_L} On screen left, {MCU}: the woman from image 1, alone, {MF}, her hands down at her sides; behind her only out-of-focus dark red "
    f"pillars and warm yellow wall light. Her {FACE_R}; a forced dry laugh: mouth corners yanked up, lips closed, no teeth, eyes not laughing and staring, "
    "brows arched high, chin raised. " + NOLANTERN + " " + OTS))
still("c13", [YARD_SET, YQ_P], (
    "Edit image 1: keep the courtyard exactly as it is (the round stone table and stools, the old well, the bamboo poles, the dark red corridor pillars, the "
    "dark lattice doors at the far end, the deep blue dusk sky), with warm yellow light glowing on the corridor walls and no lanterns, lamps or candles "
    f"anywhere, and put people into it. {YT_BACK_R} In the middle right, on the stone floor halfway between the right-hand corridor and the young woman: "
    f"ONLY ONE old woman, the old woman from image 2, {YQ}, both hands on the wheels, rolling toward the young woman; her face toward the young woman, brows "
    "pushed up and together, eyes glistening with tears, no redness, no red marks, mouth open in a cry. There are exactly two people in the picture: the "
    "young woman seen from behind and the old woman; no other person anywhere. " + NOTEXT), latent="image1")
still("c14", [YQ_P, YT_P], (
    f"{PRE} {YARD}; seen side-on, behind them only out-of-focus dark red pillars and warm yellow wall light. A medium two-shot: on screen left ONLY ONE "
    f"old woman, the old woman from image 1, {YQ}, her arms wrapped around the young woman's waist, her face lifted toward her in three-quarter profile "
    f"toward the upper right; on screen right ONLY ONE young woman, the young woman from image 2, {YT}, standing and bending toward her, her bare right hand "
    "resting on the old woman's back, a folded white cloth under her left arm. The old woman: brows pushed up and together, eyes glistening with tears, no "
    "redness, no red marks, mouth corners pulled down, lips closed. The young woman: brows drawn gently up and together, eyes looking down at her, "
    f"{NOSMILE}. Neither looks at the camera. There are exactly two people in the picture. " + NOLANTERN + " " + NOTEXT))
still("c15", [YT_P], (
    f"{PRE} {YARD}; seen from slightly low. {FG_YQ} On screen right, {MCU}: the young woman from image 1, alone, {YT}, bending toward the old woman, her "
    "hands below the bottom edge of the frame; behind her only out-of-focus corridor pillars and a dark wall; warm yellow light from screen left on her face. "
    "Her face in three-quarter profile turned toward the lower left, eyes soft and looking down at the old woman, a faint shine of tears with no redness, "
    f"brows drawn gently up and together, {NOSMILE}. " + NOLANTERN + " " + OTS))
still("c16", [JY_P], (
    f"{PRE} {YARD}; behind him only out-of-focus dark red pillars and warm yellow wall light. {MCU}: the man from image 1, alone, {JY}, both hands spread a "
    f"little at chest height. His {FACE_R}; a covering dry smile: one mouth corner pulled sideways, lips closed, no teeth, eyes not smiling and shifting, the "
    "line between his brows deep. " + NOLANTERN + " " + ONE_M))
still("c17", [JB_P], (
    f"{PRE} {YARD}; behind him only the out-of-focus wooden door frame of the main hall and warm light inside. {MCU}: the man from image 1, alone, {JB}, "
    "standing in the doorway, his right hand holding a phone with no logo to his ear, its plain black back outward. His {face}, brows knitted tight, eyes "
    "staring behind his glasses, face pale, lips slightly parted, not smiling, no teeth. ".replace("{face}", FACE_L) + ONE_M))

# ---- 第二場：廚房到東迴廊 ----
still("c19", [KIT_SET, YT_P, FB_P], (
    "Edit image 1: keep the kitchen exactly as it is (the open door in the left wall with the dark night beyond, the white sink under the black window, "
    "white tiles, the old gas stove, the doorway to the laundry nook, the square wooden table with stools, one bare light bulb, nothing on the walls) and "
    f"put two people into it. On screen right at the sink, side-on: ONLY ONE young woman, the young woman from image 2, {YT_FULL}, her sleeves folded back "
    "to the wrists, both hands holding a navy flap school bag with a big round brass clasp down in the sink, eyes down on the bag, brows slightly drawn, "
    f"{NOSMILE}. On screen left, just stepping in through the open door: ONLY ONE old man, the old man from image 3, {FB}, black trousers and black cloth "
    "shoes, an old bronze-coloured key ring in his right hand, his face toward her, brows lifted, eyes on the bag, lips closed, not smiling. There are "
    "exactly two people in the picture; no other person anywhere. " + NOTEXT), latent="image1")
still("c20", [FB_P, KEYS_P], (
    f"{PRE} Late at night in an old house kitchen; behind him only an out-of-focus open door and the dark night beyond it. {MCU}: the old man from image 1, "
    f"alone, {FB}, holding the key ring of image 2 at his chest in his right hand; light from a bare bulb on his face from screen right. His {FACE_R}, brows "
    "drawn up and together, eyes worried, mouth corners pulled down, chin slightly tucked, lips closed, not smiling. " + ONE_M), shares=["c22"])
still("c21", [YT_P, BAG_P], (
    f"{PRE} Late at night in an old house kitchen; behind her only an out-of-focus black window and white wall tiles. {MCU}: the young woman from image 1, "
    f"alone, {YT}, her sleeves folded back to the wrists; her left hand holds the navy flap school bag of image 2, washed and damp, up at her chest, and her "
    f"bare right hand cups the little brass bells hanging beside its clasp. Her {FACE_L}, brows level, eyes on someone far off to the left, chin slightly "
    f"tucked, {NOSMILE}. " + ONE_F))
still("c23", [CORR_SET, YT_P, BAG_P], (
    "Edit image 1: keep the corridor exactly as it is at night (the dark red doors, pillars and rolled-up bamboo blinds on the left, the wooden bench and "
    "the small white-shaded wall lamp on the right, the open doorway onto the dark courtyard at the far end, the green bin with nothing written on it, the "
    "near left door open a finger's width with flickering white light in the crack) and put ONLY ONE young woman into it: the young woman from image 2, "
    f"{YT_FULL}, halfway along the corridor walking toward the camera, the navy flap school bag of image 3 hanging from her left hand, her face turned "
    f"toward the crack of the door on the left, brows slightly drawn, {NOSMILE}, never looking at the camera. There is exactly one person in the picture; "
    "nobody else in the corridor. " + NOTEXT), latent="image1")
still("c24", [YT_P], (
    f"{PRE} Late at night in a covered corridor; seen side-on, behind her only out-of-focus dark red pillars and a dark wall. A MEDIUM SHOT from the waist "
    f"up: the young woman from image 1, alone, {YT}, standing before a dark red wooden door on screen left that stands open a finger's width; her bare "
    "right hand raised before the door, about to knock; flickering white light from the crack on her face. Her face in three-quarter profile toward the "
    f"crack on screen left, eyes fixed on it, brows drawn up and together, {NOSMILE}. " + ONE_F))
still("c25", [YT_P, BAG_P], (
    f"{PRE} Late at night in a covered corridor; behind her only out-of-focus dark red pillars. {MCU}: the young woman from image 1, alone, {YT}; her left "
    "hand holds the navy flap school bag of image 2 up at her chest, and her bare right hand is closed tight around the little brass bells beside its "
    f"clasp; flickering white light from screen left on her face. Her {FACE_L}, eyes fixed on something beyond the left edge, brows drawing together, lips "
    f"pressed tight, jaw set, {NOSMILE}. " + ONE_F))
still("c26", [ROOM_SET, XM_P], (
    "Edit image 1: keep the small bedroom exactly as it is late at night (the single bed, the empty hook on the wall above the bed head, the desk with the "
    "lit desk lamp, nothing written anywhere) and make it a view through a finger-wide crack of a door: the out-of-focus edges of a dark red wooden door "
    "fill the left and right of the frame. Through the crack: ONLY ONE girl, wearing the clothes of the girl in image 2 (an oversized light grey hoodie, "
    "loose black track pants, a high ponytail), sitting on the edge of the bed with her back to the door, head bowed, only her back, shoulders and ponytail "
    "seen, her face never in the frame; a phone in her hands, its screen facing her and never seen; faint white light from the phone on the wall. There is "
    "exactly one person in the picture. " + NOTEXT), shares=["c28"], latent="image1")
still("c27", [YT_P], (
    f"{PRE} Late at night in a dark covered corridor; behind her only darkness. A CLOSE-UP of her face and shoulders: the young woman from image 1, alone, "
    f"{YT}; cold white light from screen left on her face. Her {FACE_L}, eyes fixed on something beyond the left edge with a faint shine of tears and no "
    f"redness, brows drawing together, lips pressed, jaw set, {NOSMILE}. " + ONE_F))
still("c29", [YT_P], (
    f"{PRE} Late at night in a dark covered corridor; behind her only darkness. A tight CLOSE-UP of her face: the young woman from image 1, alone, {YT}; "
    f"flickering cold white light from screen left on her face. Her {FACE_L}, eyes wide and fixed on something beyond the left edge, brows pressed down, "
    f"lips pressed tight, jaw set, breath held, {NOSMILE}. " + ONE_F))


def main():
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    covered = [s["shot"] for s in S] + [x for s in S for x in s["shares_with"]]
    assert len(covered) == len(set(covered)) == 29, sorted(covered)
    refs_dir = Path(__file__).resolve().parents[2] / "assets" / "refs"
    missing = set()
    for s in S:
        assert len(s["refs"]) <= 3, s["shot"]
        for r in s["refs"]:
            if ":" not in r and not (refs_dir / r).is_file():
                missing.add(r)
    assert missing <= {BAG_P}, missing
    print(OUT, len(S), "stills covering", len(covered), "shots; still to draw:", ", ".join(sorted(missing)) or "none")


if __name__ == "__main__":
    main()
