#!/usr/bin/env python3
"""First-frame still prompts for tai-nainai e007 (2026-11-10 種田 rewrite, after the pre-shoot review) -> stills.json,
same format as e006/stills.json: [{shot, shares_with, refs, prompt[, latent]}].

Every shot of e007 takes the first-frame route (script.md〈開拍路線建議〉). 27 stills cover 29 shots:
c02 also serves c10 (the girl at the back of the bus), c03 also serves c11 (her at the front pole).
Each still is drawn at 1312x736, two seeds (the manifest converter sets the size, as for e006).

refs: names under assets/refs/; `PICK:<shot>` is the picked first frame of that shot (pick/<shot>.png) — c18 is an edit of the c13 pick.
The four wides (c01, c12, c24, c25) put the people into the fixed set picture: the set is image 1 and `latent: image1`.
Close-ups and over-the-shoulders never get a set picture; behind the person only one or two things are named.

What e006's five rounds taught (handoff ticket 2026-11-10 notes, e006/redo*_stills.py):
- the blurred foreground shoulder or back goes FIRST in the prompt ("FIRST, at the LEFT edge ..."); written at the end it is not drawn;
  the foreground person is never named, only shoulder, costume colours in caps, "no face";
- "ONLY ONE <person>" against doubles; the people-count sentence goes last; "no subtitles, no captions, no text";
- no clock, no writing, no screens; whoever does not smile is "NOT smiling, no teeth";
- tears are "glistening, no redness, no red marks" (red tears read as blood);
- at most three reference pictures per still (portraits + a prop or the set);
- the pose is the FIRST frame of the clip (shots-en.json "Initial composition"), never the middle of the action.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "stills.json"
PRE = "A single still frame, photographic live-action, realistic skin and fabric, keeping the look of image 1."
NOTEXT = "No subtitles, no captions, no text, letters or signs anywhere in the picture; no screen anywhere."
ONE_F = "There is exactly one person in the picture; no second person, no reflection of her anywhere. " + NOTEXT
ONE_M = "There is exactly one person in the picture; no second person, no reflection of him anywhere. " + NOTEXT
OTS = ("There are exactly two people in the picture: one clear person and one blurred shoulder at the edge; no other head, shoulder or person anywhere. "
       + NOTEXT)
KEEP = "Keep everything else exactly the same: the place, the light, the camera angle, every face, hair and costume. No other change. "
MCU = "a MEDIUM CLOSE-UP, chest up, filling half the frame"
NOSMILE = "NOT smiling, lips together, no teeth showing"

YT_P = "yuetang-18-portrait-t1.png"
XM_P = "xiaoman-portrait-t1.png"
LD_P = "lindao-portrait-t1.png"
HXY_P = "hexiaoyang-portrait-t1.png"
MF_P = "meifeng-portrait-t1.png"
BELL_P = "prop-baoxinling-t1.png"
ROBE_P = "prop-shouyi-t1.png"
BUS_SET = "set-gongche-t1.png"
SCH_SET = "set-gaozhong-xiaomen-t1.png"
LANE_SET = "set-shenjia-jiewai-t1.png"
YARD_SET = "set-shenjia-yuanzi-t1.png"

YT = "in a MOON-WHITE high-collared cotton shirt with fabric frog buttons fastened to the throat, one thick BLACK braid over her right shoulder"
YT_FULL = YT + ", a NAVY ankle-length cotton skirt and black cloth shoes"
XM = ("a high-school girl with straight blunt bangs and a high ponytail, in a NAVY school blazer one size too big over a white shirt with a navy ribbon tie, "
      "small white wireless earbuds in her ears, hugging a plain white paper bag to her chest with both arms, no school bag")
XM_GATE = ("a high-school girl with straight blunt bangs and a high ponytail, in a NAVY school blazer one size too big over a white shirt with a navy ribbon tie, "
           "hugging a plain white paper bag to her chest with both arms, no school bag")
LD = ("a thin man of thirty-five in a black baseball cap with no logo, an OLIVE utility jacket over a grey T-shirt, a black camera with no logo on a strap "
      "around his neck")
HXY = ("a polished high-school girl with long straight LIGHT-BROWN hair worn loose and no bangs, in a slim-tailored NAVY school blazer over a white shirt "
       "with a navy necktie")
MF = "with big glossy dark chestnut curls, a pearl necklace, red nails and a fitted WINE-RED long-sleeved knit dress with a high round neckline"
SBAG = "a plain navy school bag with nothing written on it, its main zip open"
CUP = "a clear plastic cup with NO LID and one straw, pale brown milk tea inside, no logo, nothing printed on it"
ROBE_ONLY = "only the long robe, not the trousers"

BUS = "Early morning inside a city bus, clear and cold, warm slanting sunlight"
BUS_FRONT = "behind her only the out-of-focus windshield of the bus and soft morning light"
BUS_BACK = "behind her only the out-of-focus rear window of the bus and the morning street"
SCHOOL = "A clear cold morning on the sidewalk outside a high-school gate"
LANE = "Dusk just after dark"
YARD = "Dusk just after dark in the inner stone courtyard of an old Chinese family house"
Y_MF = "behind her only out-of-focus dark red wooden corridor pillars and warm yellow lamplight on a wall; no lantern, no candle"

FG_YT_R = ("FIRST, at the LEFT edge of the frame: a young woman's right shoulder in a MOON-WHITE high stand-up collar with one thick BLACK braid lying over it, "
           "very close to the lens, soft and out of focus, no face.")
FG_YT_L = ("FIRST, at the RIGHT edge of the frame: a young woman's left shoulder in a MOON-WHITE high stand-up collar and the back of her glossy BLACK hair, "
           "very close to the lens, soft and out of focus, no face.")
FG_XM_R = ("FIRST, at the LEFT edge of the frame: a girl's right shoulder in a NAVY school blazer and a high BLACK ponytail, very close to the lens, soft and "
           "out of focus, no face.")
FG_LD = ("FIRST, at the RIGHT edge of the frame: a man's left shoulder in an OLIVE utility jacket and the back of a BLACK baseball cap, very close to the lens, "
         "soft and out of focus, no face.")
FG_HXY = ("FIRST, at the RIGHT edge of the frame: a girl's left shoulder in a NAVY school blazer and long straight LIGHT-BROWN hair, very close to the lens, soft "
          "and out of focus, no face.")

FACE_L = "face in three-quarter profile turned toward screen left, eyes clearly to the left, never looking at the camera"
FACE_R = "face in three-quarter profile turned toward screen right, eyes clearly to the right, never looking at the camera"

S = []


def still(shot, refs, prompt, shares=(), latent=None):
    s = {"shot": shot, "shares_with": list(shares), "refs": refs, "prompt": prompt}
    if latent:
        s["latent"] = latent
    S.append(s)


# ---- 第一場：公車 ----
still("c01", [BUS_SET, XM_P, YT_P], (
    "Edit image 1: keep the bus interior exactly as it is (blue seats, yellow poles and hanging straps, the windshield and the morning street, the warm slanting "
    "sunlight, every seat empty, the small signs blank) and put people into it. "
    "FIRST, in the near foreground: one out-of-focus yellow pole. "
    f"In the middle of the aisle, walking head down toward the camera: ONLY ONE girl, the girl from image 2, {XM}, a navy pleated skirt below the knee, white "
    f"socks and black school shoes, her eyes lowered to the paper bag, brows pressed down, lips pressed tight, {NOSMILE}. "
    f"At the back right, at the top of the front-door steps beside the grey coin box: ONLY ONE young woman, the young woman from image 3, {YT_FULL}, standing "
    "upright, one small coin pinched in her right hand at her waist, her face toward the girl, brows slightly drawn, eyes on the girl's back, lips closed, NOT smiling. "
    "At the back left, behind the yellow rail of the driver's seat, out of focus: the back of a bus driver's head and one shoulder in a plain LIGHT BLUE work shirt, no face. "
    "There are exactly three people in the picture: the girl, the young woman and the driver seen from behind; no passengers, no other person anywhere. " + NOTEXT),
    latent="image1")
still("c02", [XM_P], (
    f"{PRE} {BUS}; {BUS_BACK}. FIRST, at the LEFT edge of the frame, very close to the lens and out of focus: a yellow pole and the top of a blue seat back. "
    f"A medium shot: the girl from image 1, alone, {XM}, sitting in a blue window seat at the back of the bus, her head bowed low over the bag, her face in "
    "three-quarter profile turned toward the window at screen right, eyes lowered to the bag, brows pressed down, lips pressed tight, chin sunk into her tie, "
    f"{NOSMILE}; morning light from the window on half her face. " + ONE_F), shares=["c10"])
still("c03", [YT_P], (
    f"{PRE} {BUS}; {BUS_FRONT}; one yellow pole beside her. {MCU}: the young woman from image 1, alone, {YT}, standing upright, both hands below the bottom "
    f"edge of the frame; morning light from screen right on half her face. Her {FACE_L}, toward the back of the bus far off to the left of the lens; brows slightly "
    f"drawn, chin tucked, {NOSMILE}. " + ONE_F), shares=["c11"])
still("c04", [YT_P], (
    f"{PRE} {BUS}; behind her only the out-of-focus glass of the bus's front door and the morning street. A medium shot from the waist up, seen side-on: the young "
    f"woman from image 1, alone, {YT}, standing at the front of the bus facing screen right. At chest height on screen right a small plain GREY box is fixed to a "
    "yellow pole, its front face turned away from the camera: no screen, no buttons, no lights, no writing. One small coin already lies flat on top of the box; her "
    "bare right hand with no ring rests beside the coin; her left hand is out of the frame. Her face in three-quarter profile toward screen right, eyes looking down "
    f"at the coin, brows lifted a little, head very slightly tilted, {NOSMILE}. " + ONE_F))
still("c05", [YT_P], (
    f"{PRE} {BUS}. FIRST, at the LEFT edge of the frame, very close to the lens and out of focus: the back of a middle-aged man's head with short greying hair and "
    "his right shoulder in a plain LIGHT BLUE work shirt, both hands on a big steering wheel, his head facing forward toward the windshield, no face. "
    f"On screen right, a medium shot from the waist up: the young woman from image 1, alone, {YT}, standing by a yellow pole at the top of the front-door steps, "
    f"the glass of the front door and the morning street behind her. Her {FACE_L}, eyes on the back of the man's head, brows raised, chin slightly tucked, "
    f"{NOSMILE}. There are exactly two people in the picture: the clear young woman and the blurred man seen from behind; no other person anywhere. " + NOTEXT))
still("c06", [YT_P], (
    f"{PRE} {BUS}; seen from low down looking up, behind her only the out-of-focus bus ceiling and a row of hanging straps. {MCU}: the young woman from image 1, "
    f"alone, {YT}, standing very straight, both hands out of the frame below the bottom edge; morning light slanting from screen right across half her face. "
    f"Her {FACE_L}, eyes looking down and to the left at someone far below the lens, chin lifted a little, brows level, {NOSMILE}. " + ONE_F))
still("c07", [LD_P], (
    f"{PRE} {BUS}; behind him only the out-of-focus bus windows and morning light. {MCU}: the man from image 1, alone, {LD}, standing in the aisle; in his right "
    "hand a black selfie stick held out in front of his face at screen left with a phone on its tip; the phone's plain black back faces the camera, no logo; the "
    "phone's cool light falls faintly on his face. His face in profile toward the phone at screen left, eyes on the phone, brows shot up high, eyes wide and "
    "bright, mouth corners pulled up, lips closed; his left hand down at his side. " + ONE_M))
still("c08", [YT_P], (
    f"{PRE} {BUS}. {FG_LD} On screen left, {MCU}: the young woman from image 1, alone, {YT}, both hands out of the frame; {BUS_FRONT}; morning light from "
    f"screen right on her face. Her {FACE_R}, eyes curious on something just beyond the right edge of the frame, brows lifted slightly, chin pushed forward a "
    f"little, {NOSMILE}. " + OTS))
still("c09", [LD_P], (
    f"{PRE} {BUS}. {FG_YT_R} On screen right, {MCU}: the man from image 1, alone, {LD}, the selfie stick raised high in his right hand, the phone above the top "
    "edge of the frame; behind him only the out-of-focus bus windows and hanging straps. He is laughing hard: eyes squeezed into two slits, brows up, mouth open in "
    f"a big laugh, shoulders hunched with laughter; his {FACE_L}, toward the blurred young woman. " + OTS))

# ---- 第二場：校門口 ----
still("c12", [SCH_SET, HXY_P, XM_P], (
    "Edit image 1: keep the school gate exactly as it is (the closed iron bar gate, the white guard booth with its small side door open a crack, the long cream "
    "wall with the dark red base, the bare trees and the cypress, the cold morning light, nothing written on the building) and put two girls on the sidewalk. "
    f"On screen right, standing in front of the cream wall to the right of the guard booth: ONLY ONE girl, the girl from image 2, {HXY}, a navy pleated skirt "
    f"below the knee, white socks and black school shoes, holding {SBAG} by its handle in her right hand and {CUP} in her left; her {FACE_L}, one brow raised, "
    "eyes half-lidded on the other girl, one mouth corner curled up, lips closed, no teeth. "
    f"On screen left, near the left edge, just stepped in: ONLY ONE girl, the girl from image 3, {XM_GATE}, a navy pleated skirt below the knee, white socks and "
    f"black school shoes; her {FACE_R}, brows pushed up and together, eyes wide on the school bag, lips pressed tight, {NOSMILE}. "
    "There are exactly two people in the picture; nobody else on the sidewalk, no students, no guard. " + NOTEXT), latent="image1")
still("c13", [HXY_P, BELL_P], (
    f"{PRE} {SCHOOL}. {FG_XM_R} On screen right, {MCU}: the girl from image 1, alone, {HXY}, holding {SBAG} up at her chest in her right hand, the little "
    "brass bells of image 2 on their faded red cord clipped to the zip pull of its front pocket; her left hand below the bottom edge of the frame; behind her only "
    f"the out-of-focus cream school wall and bare branches. Her {FACE_L}, one brow raised, eyes half-lidded on the blurred girl, one mouth corner curled up, lips "
    "closed, no teeth, chin raised. " + OTS))
still("c14", [XM_P], (
    f"{PRE} {SCHOOL}; behind her only the out-of-focus street and cold morning light. {MCU}: the girl from image 1, alone, {XM_GATE}, the paper bag at the "
    f"bottom edge of the frame. Her {FACE_R}, toward someone far off to the right of the lens; brows pushed up and together, eyes glistening with tears, no "
    f"redness, no red marks on her face, lips pressed tight and trembling, chin pulled in, {NOSMILE}. " + ONE_F))
still("c15", [HXY_P], (
    f"{PRE} {SCHOOL}; behind her only the out-of-focus white rounded roof of a small guard booth and a cream wall. {MCU}: the girl from image 1, alone, {HXY}; "
    f"her right hand holds {SBAG} mouth-up at the bottom edge of the frame; her left hand holds {CUP}, raised just above the open bag and NOT tipped. Her "
    "FACE in three-quarter profile turned toward screen left, eyes sliding to someone far off to the left, never looking at the camera; brows raised, one mouth "
    "corner curled up, lips closed, no teeth, chin raised. " + ONE_F))
still("c16", [HXY_P], (
    f"{PRE} {SCHOOL}; behind her only the out-of-focus cream school wall. A medium shot from the waist up, seen side-on: the girl from image 1, alone, {HXY}, her "
    f"face in profile facing screen left. Her right hand holds the handle of {SBAG}, mouth up, in front of her; in her left hand {CUP} is already tipped over the "
    "opening of the bag and pale brown milk tea is pouring from it into the bag in one stream. Her eyes look down into the bag, one mouth corner curled up, lips "
    "closed, no teeth, chin raised. " + ONE_F))
still("c17", [YT_P], (
    f"{PRE} {SCHOOL}; seen from low down looking up, behind her only out-of-focus bare branches and a pale grey morning sky. {MCU}: the young woman from image 1, "
    f"alone, {YT}, standing very straight, both hands below the bottom edge of the frame; the wind lifts the end of her braid. Her {FACE_R}, eyes darkened and "
    f"fixed on someone far off to the right, brows pressed down, lips pressed tight, jaw set, {NOSMILE}. " + ONE_F))
still("c18", ["PICK:c13"], (
    "Edit image 1. Only the navy school bag in the girl's right hand changes: it is soaked through, a darker wet navy with a sheen, pale brown milk tea dripping "
    "from its bottom corner, and it hangs lower in front of her at arm's length instead of being held up at her chest; the brass bells stay on its front pocket. "
    "No cup anywhere in the frame. " + KEEP + NOTEXT), latent="image1")
still("c19", [XM_P], (
    f"{PRE} {SCHOOL}. {FG_YT_R} On screen right, {MCU}: the girl from image 1, alone, {XM_GATE}, already turned round to face the blurred young woman; behind her "
    f"only the out-of-focus cream school wall and an iron bar gate. Her {FACE_L}; pale and frightened: brows pushed up and together, eyes wide and glistening "
    f"with tears, no redness, no red marks on her face, lips trembling, chin pulled in, {NOSMILE}. " + OTS))
still("c20", [YT_P], (
    f"{PRE} {SCHOOL}; behind her only the out-of-focus street and cold morning light. {MCU}: the young woman from image 1, alone, {YT}, both hands below the "
    f"bottom edge of the frame. Her {FACE_R}, eyes soft and fixed on a girl far off to the right of the lens, brows drawn gently up and together, chin tucked, "
    f"{NOSMILE}. " + ONE_F))
still("c21", [YT_P, BELL_P], (
    f"{PRE} {SCHOOL}; seen side-on from low on the sidewalk, behind her only the out-of-focus cream school wall. A medium shot: the young woman from image 1, "
    f"alone, {YT_FULL}, crouched low and steady on the grey paving, her skirt tucked to cover her ankles, her face in three-quarter profile toward screen right "
    "looking down at the bag; her left hand already grips the handle of a soaked dark navy school bag lying on the paving, the brass bells of image 2 on its front "
    "pocket, the old silver ring on her left ring finger turned toward the palm; her bare right hand rests on her knee; a small puddle of pale brown milk tea on "
    f"the paving. Brows pressed down, lips pressed tight, {NOSMILE}. " + ONE_F))
still("c22", [HXY_P], (
    f"{PRE} {SCHOOL}. {FG_YT_R} On screen right, {MCU}: the girl from image 1, alone, {HXY}, an empty clear plastic cup with no lid and one straw in her left "
    "hand at the bottom edge of the frame; behind her only the out-of-focus cream school wall and the guard booth. Her face in three-quarter profile turned toward "
    "screen left, eyes running down the blurred woman's clothes, never looking at the camera; one brow raised, mouth corners pulled down, chin raised, "
    f"{NOSMILE}. " + OTS))
still("c23", [YT_P], (
    f"{PRE} {SCHOOL}. {FG_HXY} On screen left, {MCU}: the young woman from image 1, alone, {YT}, standing very straight, both hands below the bottom edge of "
    f"the frame; behind her only the out-of-focus street and cold morning light. Her {FACE_R}, eyes on the blurred girl, brows level, chin lifted slightly, "
    f"{NOSMILE}. " + OTS))

# ---- 第三場：沈家巷到院子 ----
still("c24", [LANE_SET, YT_P], (
    "Edit image 1: keep the lane exactly as it is (the two low old houses with grey tiled roofs, the brown wooden double door and the lit street lamp on the "
    f"left, the black-lacquered double gate with brass ring knockers on the right, the deep blue dusk sky, the stone paving) and add ONLY ONE young woman, the "
    f"young woman from image 2, {YT_FULL}, on the stone paving in the right half of the picture, a few steps from the black gate, walking toward it: seen in "
    "three-quarter back view, her face turned toward the gate and away from the camera; a navy school bag with a dried dark stain hangs from her left hand, her "
    "right hand empty, dust on her black cloth shoes; she is full-length and small in the frame, the gate taller than her. There is exactly one person in the "
    "picture; nobody else in the lane. " + NOTEXT), latent="image1")
still("c25", [YARD_SET, MF_P, ROBE_P], (
    "Edit image 1: keep the courtyard exactly as it is (the round stone table and stools, the old well on the left, the bamboo poles on the right, the dark red "
    "corridor pillars, the ancestral hall's lattice doors dark at the far end) at dusk just after dark, a deep blue sky and warm yellow lamplight on the corridor "
    "walls, no candle glow anywhere. FIRST, in the right foreground, very close to the lens and slightly out of focus, seen only from behind: a young woman's back "
    "in a MOON-WHITE high-collared shirt and a NAVY ankle-length skirt, one thick BLACK braid down her right shoulder, a navy school bag hanging from her left hand, "
    f"no face. In the middle, standing by the round stone table: ONLY ONE woman, the woman from image 2, {MF}, black low heels, holding at her chest in both hands "
    f"the off-white robe of image 3 folded neatly ({ROBE_ONLY}); her face toward the young woman in the foreground, one brow arched, eyes fixed on her, red lips "
    "curled up at one corner, no teeth. There are exactly two people in the picture: the woman seen from behind and the woman by the table; no other person "
    "anywhere. " + NOTEXT), latent="image1")
still("c26", [MF_P, ROBE_P], (
    f"{PRE} {YARD}. {FG_YT_L} On screen left, {MCU}: the woman from image 1, alone, {MF}, holding at her chest in both hands the off-white robe of image 2 "
    f"folded neatly ({ROBE_ONLY}); {Y_MF}. Her {FACE_R}; a fake smile: mouth corners pulled up, lips closed, no teeth, eyes not smiling and coldly fixed on the "
    "blurred young woman, brows arched high, chin raised. " + OTS))
still("c27", [MF_P, ROBE_P], (
    f"{PRE} {YARD}; behind her only out-of-focus corridor pillars and a dark wall; warm yellow lamplight from screen left on her face and the white cloth. A medium "
    f"shot from the waist up: the woman from image 1, alone, {MF}, holding by its shoulders in both hands the off-white robe of image 2, shaken open and hanging "
    f"down in front of her: high stand-up collar, side frog-button fastening, long sleeves, mid-calf length with slits at both sides ({ROBE_ONLY}), no "
    f"embroidery, nothing written on it. Her {FACE_R}, eyes narrowed at someone far off to the right, brows arched high, red lips twisted coldly to one side, "
    "no teeth, chin raised high. " + ONE_F))
still("c28", [YT_P], (
    f"{PRE} {YARD}; seen from low down looking up, behind her only an out-of-focus door frame and warm yellow light from the room behind. {MCU}: the young woman "
    f"from image 1, alone, {YT}, standing very straight in a doorway, both hands below the bottom edge of the frame. Her {FACE_L}, eyes fixed on something far "
    f"off to the left of the lens, brows drawn together, lips pressed tight, jaw tight, {NOSMILE}. " + ONE_F))
still("c29", [MF_P, ROBE_P], (
    f"{PRE} {YARD}. {FG_YT_L} On screen left, a medium shot from the waist up: the woman from image 1, alone, {MF}, standing still beside the edge of a round "
    f"stone table, gripping by its shoulders the off-white robe of image 2, shaken open and held out toward the blurred young woman ({ROBE_ONLY}); {Y_MF}. Her "
    f"{FACE_R}; brows shot up, eyes glaring at the blurred young woman, mouth corners pulled down, lips closed, chin thrust forward, {NOSMILE}. " + OTS))


def main():
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    covered = [s["shot"] for s in S] + [x for s in S for x in s["shares_with"]]
    assert len(covered) == len(set(covered)) == 29, sorted(covered)
    for s in S:
        assert len(s["refs"]) <= 3, s["shot"]
        for r in s["refs"]:
            if not r.startswith("PICK:"):
                assert (Path(__file__).resolve().parents[2] / "assets" / "refs" / r).is_file(), r
    print(OUT, len(S), "stills covering", len(covered), "shots")


if __name__ == "__main__":
    main()
