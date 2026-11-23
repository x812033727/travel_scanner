#!/usr/bin/env python3
"""Write docs/videos/tai-nainai-e007/shots-en.json for the 2026-11-10 種田 rewrite (29 shots).

Each shot's English body is bound to its script.md row by zh_sha256 (compile.py --check). Re-run after editing a row:
  python3 -I e007-gen-en.py
"""
import json
import sys
from pathlib import Path

ROOT = Path("/home/user/travel_scanner")
sys.path.insert(0, str(ROOT / "docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools"))
import parse_script  # noqa: E402

# ---- people (same sentence every shot) ----
YT = ("Shen Yuetang in her moon-white high-collared cotton shirt with frog buttons fastened to the throat, ankle-length navy cotton skirt and black cloth shoes, "
      "one thick braid over her right shoulder")
YT_UP = ("Shen Yuetang in her moon-white high-collared cotton shirt with frog buttons fastened to the throat and long narrow sleeves, "
         "one thick braid over her right shoulder")
RING = "the thick old silver ring only on her left ring finger, her right hand bare with no ring"
XM = ("Shen Xiaoman, a high-school girl with straight blunt bangs and a high ponytail, in a navy school blazer one size too big over a white shirt with a navy ribbon tie, "
      "a navy pleated skirt below the knee, white socks and black school shoes")
XM_UP = ("Shen Xiaoman, a high-school girl with straight blunt bangs and a high ponytail, in a navy school blazer one size too big over a white shirt with a navy ribbon tie")
BUDS = "small white wireless earbuds with no logo in her ears"
PBAG = "a plain white paper bag of schoolbooks with nothing printed on it hugged to her chest in both arms, no school bag"
LD = ("Director Lin, a thin man of thirty-five in a black baseball cap with no logo, an olive utility jacket over a grey T-shirt, a black camera with no logo on a strap "
      "around his neck")
STICK = ("a black selfie stick in his right hand with a phone on its tip; the phone's plain black back faces the camera, no logo")
HXY = ("He Xiaoyang, a polished high-school girl with long straight light-brown hair worn loose and no bangs, in a slim-tailored navy school blazer over a white shirt with a navy "
       "necktie, a navy pleated skirt below the knee, white socks and black school shoes")
HXY_UP = ("He Xiaoyang, a polished high-school girl with long straight light-brown hair worn loose and no bangs, in a slim-tailored navy school blazer over a white shirt "
          "with a navy necktie")
SBAG = "Xiaoman's plain navy school bag with nothing written on it, its main zip open"
BELLS = "the little brass bells on a faded red cord clipped to the zip pull of its front pocket"
TEA = "a clear plastic cup with no lid and one straw, full of pale brown milk tea, no logo and nothing printed on it"
MF = ("Lin Meifeng with big glossy dark chestnut shoulder-length curls, a pearl necklace, red nails and a fitted wine-red long-sleeved knit dress with a high round neckline")
MF_FULL = MF + ", black low heels"
ROBE = ("a plain off-white cotton burial robe with a high stand-up collar, no V-neck, a side frog-button fastening, long sleeves, mid-calf length with slits at both "
        "sides, no embroidery and nothing written on it")
FOLDED = "the same plain off-white cotton burial robe, high stand-up collar and side frog-button fastening, folded neatly"
DRIVER = "the bus driver in a plain light-blue work shirt with no lettering, only the back of his head and his shoulder seen, his face never in the frame"

NOSMILE = "no smile, lips together, no teeth showing"
OPEN = "her lips are closed until she starts, and she starts within the first second"
OPEN_M = "his lips are closed until he starts, and he starts within the first second"
MCU = "a medium close-up from the chest up, {who} filling about half of the frame"

# ---- places ----
BUS = "Inside a city bus in the early morning, clear and cold"
BUS_WIDE = ("seen from the middle of the bus toward the front as in the bus picture: rows of blue seats on both sides, yellow poles and a row of hanging straps; at the front "
            "the big windshield with the morning street beyond; at the front right the steps of the front door with a tall grey coin box beside them; a small grey box fixed "
            "to a yellow pole near the front, its face turned away; the driver's seat at the front left behind a yellow rail; every seat in view is empty; the small signs "
            "and stickers are blank")
BUS_FRONT = "behind her only the out-of-focus windshield and soft early morning light"
BUS_BACK = "behind her only the out-of-focus rear window of the bus and the early morning street"
SCHOOL = "Outside the front gate of a high school on a clear, cold morning"
SCHOOL_WIDE = ("seen from the sidewalk toward the gate as in the school-gate picture: on the left half a wide closed iron bar gate, to its right a small white guard booth "
               "with a rounded roof, then a long cream wall with a dark red base running right; bare trees and one dark green cypress behind the wall; the school building "
               "behind the gate out of focus with nothing written on it; grey paving stones of the sidewalk in the foreground; nobody else on the sidewalk")
WALL = "behind her only the out-of-focus cream school wall and bare branches"
STREET = "behind her only the out-of-focus street and cold morning light"
LANE = "A narrow old lane at dusk, just after dark"
LANE_WIDE = ("seen from the lane looking north at the street front of the old Shen house as in the lane picture: two low old houses with grey tiled roofs; on the left an old "
             "shopfront with a dark brown wooden double door, two small windows and a few stone steps, an old street lamp lit beside it; on the right a black-lacquered "
             "double gate with two brass ring knockers; deep blue sky; stone paving in the foreground; nobody else in the lane")
YARD = "The inner stone courtyard of the old Shen house at dusk, just after dark"
YARD_WIDE = ("seen from the back door of the main hall looking north as in the courtyard picture: a round stone table with a few stone stools in the middle on the sunken "
             "stone floor; an old well with a small wooden roof on the left; bamboo drying poles leaning on the right; covered corridors with dark red pillars on both "
             "sides, warm yellow lamplight on their walls; at the far end the ancestral hall's dark lattice doors above stone steps; "
             "deep blue sky")
Y_MF = "behind her only the out-of-focus corridor pillars and warm yellow lamplight"
Y_YT = "behind her only the out-of-focus door frame and warm yellow light from the hall"

YT_RFG = "her right shoulder, moon-white collar and the thick black braid lying over it soft at the left frame edge, her face unseen"
YT_LFG = "her left shoulder, moon-white collar and the back of her black hair soft at the right frame edge, her face unseen; her braid is on the far side, out of the frame"
XM_RFG = "her right shoulder in the navy blazer and her high black ponytail soft at the left frame edge, her face unseen"
LD_FG = "his left shoulder in the olive utility jacket and the back of his black cap soft at the right frame edge, his face unseen"
HXY_FG = "her left shoulder in the navy blazer and her long light-brown hair soft at the right frame edge, her face unseen"

S = {}
B1 = dict(set="gongche")
B2 = dict(set="gaozhong-xiaomen")
B3L = dict(set="shenjia-jiewai")
B3 = dict(set="shenjia-yuanzi")


def shot(sid, base, **kw):
    e = dict(base)
    e.update(kw)
    S[sid] = e


# ---- 第一場：公車 ----
shot("c01", B1, camera="Wide shot, slow push in", characters=["xiaoman", "yuetang-18"], action_seconds=2, prompt=(
    f"{BUS}, {BUS_WIDE}; one out-of-focus yellow pole in the foreground. Exactly three people in the whole frame, two faces. In the middle of the aisle, {XM}, {BUDS}, "
    f"{PBAG}, walking head down toward the camera, her eyes on the paper bag. At the back right, at the top of the front-door steps, {YT}, {RING}, a single coin pinched "
    f"in her right hand, just stepped up onto the bus floor. At the back left, out of focus behind the rail, {DRIVER}. Early light through the windows. Shen Xiaoman: brows "
    f"pressed down, eyes lowered to the bag, lips pressed tight, chin tucked, {NOSMILE}. Shen Yuetang: brows slightly drawn, eyes fixed on the girl's back, lips closed, "
    "slow breath, no smile. In the first frame the girl is already halfway down the aisle; from the first second she walks on, head down, never looking back, while Shen "
    "Yuetang settles her weight and stands, slow and steady, her eyes following the girl. Everyone's lips stay closed. End: the girl halfway past the pole."),
    motion="Xiaoman walks down the aisle head down as Yuetang steps on behind her, watching.")
shot("c02", B1, camera="Point-of-view medium shot, locked", characters=["xiaoman"], no_set=True, action_seconds=2, prompt=(
    f"{BUS}; {BUS_BACK}; an out-of-focus yellow pole and blue seat backs in the foreground. Exactly one person in the whole frame: {XM_UP}, {BUDS}, sitting in a blue window "
    f"seat at the back of the bus, {PBAG}; early light through the window on half her face. Brows pressed down, eyes lowered to the bag, lips pressed tight, chin sunk "
    f"into her ribbon tie, shallow breath, {NOSMILE}. In the first frame she is already seated; in the first second she hugs the bag tighter and lowers her head further, "
    "her forehead leaning toward the window; she never looks up. Her lips stay closed. The camera holds a static shot. End: forehead near the glass, head down."),
    motion="At the back of the bus Xiaoman hugs her paper bag and sinks her head toward the window.")
shot("c03", B1, camera="Medium close-up, slow push in to a medium close-up", characters=["yuetang-18"], no_set=True, clip_seconds=5, prompt=(
    f"{BUS}; {BUS_FRONT}; the camera halfway down the aisle, to her front left. Exactly one person in the whole frame, a medium close-up from the chest up: {YT_UP}, standing "
    "by a yellow pole at the front, her hands below the bottom edge of the frame; early light from screen right on half her face. Eyes fixed far off to the left of the "
    f"lens toward the back of the bus, brows slightly drawn, lips closed, chin tucked, a slow breath in, {NOSMILE}; the same face from the first frame to the last. In the "
    "first second the bus sways and her body sways gently with it, then she straightens her back again, her eyes never leaving the back of the bus and never going to the "
    "camera. Her lips stay closed. End: standing straight, watching."),
    motion="The bus sways; Yuetang sways with it and straightens, her eyes on the back of the bus.")
shot("c04", B1, camera="Medium shot, locked", characters=["yuetang-18"], no_set=True, action_seconds=3, prompt=(
    f"{BUS}; behind her only the out-of-focus glass of the front door and the morning street. Exactly one person in the whole frame, seen side-on from the waist up: {YT_UP}, "
    "standing at the front of the bus; in the first frame one coin already lies flat on top of a small plain grey box fixed to a yellow "
    "pole, the face of the box turned away from the camera, her bare right hand with no ring resting beside the coin; her left hand out of the frame. Brows lifted a little, eyes looking down at the coin, lips closed, chin tucked, "
    f"{NOSMILE}. In the first second she waits and tilts her head slightly, her hand still; nothing happens. Her lips stay closed. "
    "End: halfway through the head tilt."),
    motion="She lays the coin on the card reader, presses it and waits, puzzled.")
shot("c05", B1, camera="Medium shot, locked", characters=["yuetang-18"], no_set=True, action_seconds=5, prompt=(
    f"{BUS}; the camera behind the driver's seat to its right, looking toward the front door; the glass of the front door and the morning street behind her. Exactly two "
    f"people in the whole frame, one face. In the left foreground, out of focus, {DRIVER}, sitting at the big steering wheel with both hands on it. On screen right, standing "
    f"by a yellow pole at the top of the front-door steps, {YT_UP}, in three-quarter profile toward the driver at screen left. Shen Yuetang: brows raised, eyes fixed on "
    f"the back of his head, lips closed, chin slightly tucked, {NOSMILE}. In the first second the driver lifts his right hand off the wheel and jabs a finger toward screen "
    "right across the aisle, then slaps the hand back on the wheel; his head stays facing the windshield, his face never in the frame; she glances "
    "at his pointing finger and back to his head. Her lips stay closed. The camera holds a static shot. End: his hand back on the wheel, her eyes on him."),
    motion="The driver jabs a finger toward the coin box without turning round; she looks from his finger back to him.")
shot("c06", B1, camera="Low-angle medium close-up, slow push in to a medium close-up", characters=["yuetang-18"], no_set=True, clip_seconds=10,
     addressee="the driver below and beyond the left edge of the frame, well off to the left of the lens", prompt=(
    f"{BUS}; seen from low beside the driver's seat looking up, behind her only the out-of-focus bus ceiling and a row of hanging straps. Exactly one person in the whole "
    f"frame, a medium close-up from the chest up: {YT_UP}, standing at the front, both hands out of the frame below the bottom edge; early light "
    "slanting from screen right across half her face. Back very straight, chin lifted a little, eyes clear and fixed on the driver far below to the left, brows level, lips "
    f"pressing together between the place names, steady breath, {NOSMILE}; the same face from the first frame to the last. {OPEN.capitalize()}. Shen Yuetang, turned toward "
    "him in three-quarter profile, speaks a short Mandarin line, slowly, her voice falling at the end, her lips, jaw and cheeks moving clearly with every syllable, giving "
    "one small nod of the chin at each place name. End: her eyes still on him."),
    motion="Looking down at the driver, she names the old stops of the horse-cart road one by one.")
shot("c07", B1, camera="Medium close-up, slow push in", characters=["lindao"], no_set=True, clip_seconds=8,
     addressee="the phone on his selfie stick at screen left", prompt=(
    f"{BUS}; behind him only the out-of-focus bus windows and early morning light; the camera in the aisle to his front right. Exactly one person in the whole frame, a "
    f"medium close-up from the chest up: {LD}, standing in the aisle, {STICK}, held out in front of his face at screen left. Brows shot up high, eyes wide and bright on "
    f"the phone, mouth corners stretched up, quick excited breaths. {OPEN_M.capitalize()}. Director Lin, in profile toward the phone, speaks a short Mandarin line, in an "
    "excited half-whisper, his lips, jaw and cheeks moving clearly with every syllable, and points his left hand toward screen left where she stands out of the frame; the phone's cool light falls faintly on his face. "
    "End: his eyes on the phone, his left hand pointing."),
    motion="The live-streamer whispers excitedly into his phone, pointing at the girl off screen.")
shot("c08", B1, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "lindao"], ref_characters=["yuetang-18", "lindao"], no_set=True,
     clip_seconds=9, prompt=(
    f"{BUS}; {BUS_FRONT}. Exactly two people in the whole frame. Over Director Lin's left shoulder: {LD_FG}. On screen left, {MCU.format(who='she')}: {YT_UP}, "
    f"both hands out of the frame; early light from screen right on her face. Brows lifted slightly, eyes curious on the phone he holds just beyond the right edge of the frame, lips pressing "
    f"together between phrases, chin pushed forward a little, {NOSMILE}. In the first second she leans forward a little; {OPEN}. Shen Yuetang, turned to Director Lin at "
    "screen right in three-quarter profile, speaks a short Mandarin line, earnestly, her lips, jaw and cheeks moving clearly with every syllable. Director Lin's lips stay "
    "closed. End: leaning in, her eyes on the phone."),
    motion="Leaning in, she earnestly asks whether his glowing board is an abacus.")
shot("c09", B1, camera="Over-the-shoulder medium close-up, locked", characters=["lindao", "yuetang-18"], ref_characters=["lindao", "yuetang-18"], no_set=True,
     clip_seconds=8, prompt=(
    f"{BUS}; behind him only the out-of-focus bus windows and hanging straps. Exactly two people in the whole frame. Over Shen Yuetang's right shoulder: {YT_RFG}. On screen "
    f"right, {MCU.format(who='he')}: {LD}, the selfie stick in his right hand raised high, the phone above the top edge of the frame. Laughing hard from the first frame: "
    "eyes squeezed into two slits, brows up, mouth open in a big laugh, shoulders shaking. In the first second, still laughing, Director Lin, turned to Shen Yuetang at "
    "screen left in three-quarter profile, speaks a short Mandarin line, laughing out loud, his lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang's "
    "lips stay closed. The camera holds a static shot. End: still laughing, his eyes on her."),
    motion="Laughing so hard his shoulders shake, he tells her it is a live stream and everyone is watching.")
shot("c10", B1, camera="Point-of-view medium shot, locked", characters=["xiaoman"], no_set=True, action_seconds=3, prompt=(
    f"{BUS}; {BUS_BACK}; an out-of-focus yellow pole and blue seat backs in the foreground. Exactly one person in the whole frame: {XM_UP}, {BUDS}, in the first frame still "
    f"sitting in the blue window seat at the back, {PBAG}; the street outside the window slowing down. Brows pressed down, eyes lowered, lips pressed tight, chin tucked, "
    f"{NOSMILE}. In the first second the bus brakes and she stands up with the bag and turns to walk toward the rear door at screen left, never looking toward the front. "
    "Her lips stay closed. The camera holds a static shot. End: halfway through turning to walk."),
    motion="As the bus brakes, Xiaoman gets up with her bag and heads for the rear door.")
shot("c11", B1, camera="Medium close-up, locked", characters=["yuetang-18"], no_set=True, action_seconds=4, prompt=(
    f"{BUS}; {BUS_FRONT}. Exactly one person in the whole frame, a medium close-up from the chest up: {YT_UP}, standing by a yellow pole at the front. In the first frame her eyes are on the girl "
    f"far off to the left of the lens, brows level, lips closed, chin slightly tucked, steady breath, {NOSMILE}; the same face from the first frame to the last. In the "
    "first second her head turns to screen right and she is about to set off: her weight shifts to the right and one foot is just lifting. Her lips stay closed. The camera holds a "
    "static shot. End: just setting off, weight on the right."),
    motion="Her eyes on the girl, she takes a slow step after her toward the rear door.")

# ---- 第二場：校門口 ----
shot("c12", B2, camera="Wide shot, slow push in", characters=["hexiaoyang", "xiaoman"], action_seconds=3, prompt=(
    f"{SCHOOL}, {SCHOOL_WIDE}. Exactly two people in the whole frame. On screen right, standing in front of the cream wall, {HXY}, holding {SBAG} by its handle in her right "
    f"hand and {TEA} in her left. On screen left, just walking in from the left edge of the frame, {XM}, {PBAG}. Cold morning light. He Xiaoyang: one brow raised, eyes "
    "half-lidded on the other girl, one mouth corner curled up, lips closed, no teeth showing. Shen Xiaoman: brows pushed up and together, eyes wide on the school bag, lips "
    f"pressed tight, {NOSMILE}. In the first second Shen Xiaoman walks into the frame and stops dead, hugging her bag tighter; He Xiaoyang lifts the school bag a little. "
    "Everyone's lips stay closed. End: Xiaoman stopped, staring at her bag."),
    motion="Xiaoman walks up to the gate and stops dead when she sees her bag in the other girl's hand.")
shot("c13", B2, camera="Over-the-shoulder medium close-up, slow push in", characters=["hexiaoyang", "xiaoman"], ref_characters=["hexiaoyang", "xiaoman"], no_set=True,
     clip_seconds=8, prompt=(
    f"{SCHOOL}; behind her only the out-of-focus cream school wall and bare branches. Exactly two people in the whole frame. Over Shen Xiaoman's right shoulder: {XM_RFG}. On "
    f"screen right, {MCU.format(who='she')}: {HXY_UP}, holding {SBAG} up at her chest in her right hand, {BELLS}; her left hand with the milk tea below the bottom edge of "
    "the frame. One brow raised, eyes half-lidded on the other girl, one mouth corner curled up with no teeth showing, chin raised. In the first second she gives the bag a "
    "small shake and the bells ring once; her lips are closed until she starts, and she starts within the first second. He Xiaoyang, turned to Shen Xiaoman at screen left "
    "in three-quarter profile, speaks a short Mandarin line, sweetly with a sting at the end, her lips, jaw and cheeks moving clearly with every syllable. Shen Xiaoman's "
    "lips stay closed. End: the bag held up, her eyes on the girl."),
    motion="Shaking the bag so the bells ring, she tells Xiaoman the bag spent the night with her.")
shot("c14", B2, camera="Medium close-up, locked", characters=["xiaoman"], no_set=True, action_seconds=3, prompt=(
    f"{SCHOOL}; behind her only the out-of-focus street and cold morning light. Exactly one person in the whole frame, a medium close-up from the chest up: {XM_UP}, the white "
    "paper bag hugged to her chest at the bottom edge of the frame. Brows pushed up and together, eyes glistening with tears, no redness, no red marks, lips pressed tight and trembling, chin pulled in, tight "
    f"breath, {NOSMILE}; the same face from the first frame to the last. In the first second she hugs the bag harder to her chest and shrinks back half a step, her eyes "
    "fixed on the other girl far off to the right of the lens. Her lips stay closed. The camera holds a static shot. End: shrunk back, hugging the bag."),
    motion="Xiaoman hugs her paper bag and shrinks back, near tears.")
shot("c15", B2, camera="Medium close-up, slow push in", characters=["hexiaoyang"], no_set=True, clip_seconds=8,
     addressee="Shen Xiaoman beyond the left edge of the frame, well off to the left of the lens", prompt=(
    f"{SCHOOL}; behind her only the out-of-focus white rounded roof of the guard booth and the cream wall. Exactly one person in the whole frame, a medium close-up from the "
    f"chest up: {HXY_UP}, her right hand holding {SBAG} mouth-up at the bottom edge of the frame, her left hand holding {TEA} raised just above the open bag. Brows raised, "
    "eyes sliding sideways to the girl at screen left, one mouth corner curled up with no teeth showing, chin raised. Her lips are closed until she starts, and she starts "
    "within the first second. He Xiaoyang, turned toward the girl in three-quarter profile, speaks a short Mandarin line, sweetly, her lips, jaw and cheeks moving clearly "
    "with every syllable; the cup stays poised above the bag and is not tipped. End: the cup held over the open bag."),
    motion="Holding the milk tea over the open bag, she sweetly says the bag deserves a drink too.")
shot("c16", B2, camera="Medium shot, locked", characters=["hexiaoyang"], no_set=True, action_seconds=3, prompt=(
    f"{SCHOOL}; behind her only the out-of-focus cream school wall. Exactly one person in the whole frame, seen side-on from the waist up in profile facing screen left: "
    f"{HXY_UP}, her right hand holding the handle of {SBAG}, mouth up; in the first frame the lidless cup in her left hand is already tipped over the opening and pale brown milk "
    "tea is pouring into the bag. Eyes looking down into the bag, one mouth corner curled up, lips closed with no teeth showing, chin raised. In the first second the tea "
    "pours in and the cup runs empty, and she flicks the empty cup down. Her lips stay closed. The camera holds a static shot. End: halfway through the flick."),
    motion="She pours the whole cup of milk tea into the open school bag and flicks the empty cup.")
shot("c17", B2, camera="Low-angle medium close-up, slow push in to a medium close-up", characters=["yuetang-18"], no_set=True, action_seconds=5, prompt=(
    f"{SCHOOL}; seen from low on the sidewalk looking up, behind her only out-of-focus bare branches and the pale grey morning sky. Exactly one person in the whole frame, a "
    f"medium close-up from the chest up: {YT_UP}, standing on the sidewalk a few steps behind the girl, her hands folded at her waist below the bottom edge of the frame; the "
    "wind lifts the end of her braid; cold morning light. Eyes darkened and fixed on the girl with the cup far off to the right of the lens, brows pressed down, lips "
    f"pressed tight, jaw set, a slow breath in through the nose, {NOSMILE}; the same face from the first frame to the last. In the first second she takes half a step "
    "forward and stops herself, her shoulders drawing in, her back straightening. Her lips stay closed. End: standing still, watching."),
    motion="She starts forward half a step, stops herself and stands very straight, watching.")
shot("c18", B2, camera="Over-the-shoulder medium close-up, locked", characters=["hexiaoyang", "xiaoman"], ref_characters=["hexiaoyang", "xiaoman"], no_set=True,
     clip_seconds=8, prompt=(
    f"{SCHOOL}; behind her only the out-of-focus cream school wall and bare branches. Exactly two people in the whole frame. Over Shen Xiaoman's right shoulder: {XM_RFG}. On "
    f"screen right, {MCU.format(who='she')}: {HXY_UP}, the wet navy school bag hanging from her right hand in front of her, milk tea dripping from its bottom; her left hand "
    "with the empty cup below the bottom edge of the frame. Brows raised, eyes cool on the other girl, one mouth corner curled up with no teeth showing, chin raised high. "
    "In the first second her right hand lets go and the bag drops out of the bottom of the frame toward the girl's feet; her lips are closed until she starts, and she "
    "starts within the first second. He Xiaoyang, turned to Shen Xiaoman at screen left in three-quarter profile, speaks a short Mandarin line, sweetly with a sting at the "
    "end, her lips, jaw and cheeks moving clearly with every syllable. Shen Xiaoman's lips stay closed. The camera holds a static shot. End: her hand empty, her eyes on the girl."),
    motion="She drops the dripping bag at Xiaoman's feet and tells her to keep her mouth shut at home.")
shot("c19", B2, camera="Over-the-shoulder medium close-up, slow push in", characters=["xiaoman", "yuetang-18"], ref_characters=["xiaoman", "yuetang-18"], no_set=True,
     clip_seconds=8, prompt=(
    f"{SCHOOL}; behind her only the out-of-focus cream school wall and the iron gate. Exactly two people in the whole frame. Over Shen Yuetang's right shoulder: {YT_RFG}. On "
    f"screen right, {MCU.format(who='she')}: {XM_UP}, the white paper bag hugged to her chest, in the first frame already turned round to face Shen Yuetang. Pale and "
    "frightened from the first frame: brows pushed up and together, eyes wide and glistening with tears, no redness, no red marks, lips trembling, chin pulled in, no smile, no teeth showing; the same frightened face "
    "to the last frame. In the first second she backs off half a step; her lips are closed until she starts, and she starts within the first second. Shen Xiaoman, turned "
    "to Shen Yuetang at screen left in three-quarter profile, speaks a short Mandarin line, low and shaking, her lips, jaw and cheeks moving clearly with every syllable. "
    "Shen Yuetang's lips stay closed. End: her frightened eyes on Shen Yuetang."),
    motion="Turning to find Yuetang behind her, Xiaoman backs off and begs her not to tell the family.")
shot("c20", B2, camera="Medium close-up, locked", characters=["yuetang-18"], no_set=True, action_seconds=3, prompt=(
    f"{SCHOOL}; {STREET}. Exactly one person in the whole frame, a medium close-up from the chest up: {YT_UP}, her hands folded at her waist below the bottom edge of the "
    "frame. Brows drawn gently up and together, eyes soft and fixed on the girl's face far off to the right of the lens, lips closed, chin tucked, a slow breath out, "
    f"{NOSMILE}; the same face from the first frame to the last. In the first second she nods slowly once, her eyes never leaving the girl. Her lips stay closed. The camera "
    "holds a static shot. End: halfway through the nod."),
    motion="She nods once, slowly: she will not tell.")
shot("c21", B2, camera="Medium shot, slow push in", characters=["yuetang-18"], no_set=True, action_seconds=3, prompt=(
    f"{SCHOOL}; seen side-on from low on the sidewalk, behind her only the out-of-focus cream school wall. Exactly one person in the whole frame: {YT}, {RING}; in the first "
    "frame she is already crouched low and steady on the sidewalk, her skirt tucked to cover her ankles, her left hand already gripping the handle of the wet navy school "
    f"bag on the ground, {BELLS}; a puddle of pale brown milk tea on the paving. Brows pressed down, eyes on the bag, lips pressed tight, slow breath, {NOSMILE}. In the "
    "first second she rises slowly with the bag, the bells ring once and milk tea drips from its bottom. Her lips stay closed. End: halfway up, the bag hanging from her left hand."),
    motion="Crouched by the soaked bag, she lifts it by the handle and slowly stands, tea dripping.")
shot("c22", B2, camera="Over-the-shoulder medium close-up, locked", characters=["hexiaoyang", "yuetang-18"], ref_characters=["hexiaoyang", "yuetang-18"], no_set=True,
     clip_seconds=8, prompt=(
    f"{SCHOOL}; behind her only the out-of-focus cream school wall and the guard booth. Exactly two people in the whole frame. Over Shen Yuetang's right shoulder: {YT_RFG}. "
    f"On screen right, {MCU.format(who='she')}: {HXY_UP}, the empty lidless clear plastic cup with its straw in her left hand at the bottom edge of the frame. One brow raised, eyes running down "
    "Shen Yuetang's clothes from head to foot, mouth corners pulled down, chin raised, no smile, no teeth showing. In the first second her eyes look Shen Yuetang up and "
    "down; her lips are closed until she starts, and she starts within the first second. He Xiaoyang, turned to Shen Yuetang at screen left in three-quarter profile, speaks "
    "a short Mandarin line, with contempt, her lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang's lips stay closed. The camera holds a static shot. "
    "End: her eyes on Shen Yuetang."),
    motion="Looking her up and down, the girl asks what she is to Xiaoman's family, dressed like that.")
shot("c23", B2, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "hexiaoyang"], ref_characters=["yuetang-18", "hexiaoyang"], no_set=True,
     clip_seconds=9, prompt=(
    f"{SCHOOL}; {STREET}. Exactly two people in the whole frame. Over He Xiaoyang's left shoulder: {HXY_FG}. On screen left, {MCU.format(who='she')}: {YT_UP}, both "
    "hands below the bottom edge of the frame, the wet school bag in her left hand. Back very straight, eyes on the girl's eyes and then dropping once to the empty cup in her hand, "
    f"brows level, lips pressing together between the two sentences, chin lifted slightly, steady breath, {NOSMILE}; the same face from the first frame to the last. "
    f"{OPEN.capitalize()}. Shen Yuetang, turned to He Xiaoyang at screen right in three-quarter profile, speaks a short Mandarin line, low and slow, word by word, her lips, "
    "jaw and cheeks moving clearly with every syllable. He Xiaoyang's lips stay closed. End: her eyes on the girl."),
    motion="Holding the soaked bag, she says she is the Shen family's nanny and will take it home to wash.")

# ---- 第三場：沈家巷到院子 ----
shot("c24", B3L, camera="Wide shot, slow push in", characters=["yuetang-18"], action_seconds=4, prompt=(
    f"{LANE}, {LANE_WIDE}. Exactly one person in the whole frame: {YT}, the navy school bag hanging from her left hand with a dried dark milk-tea stain on it, her right hand "
    "empty, dust on her black cloth shoes. Eyelids a little heavy, brows level, lips closed, breathing a little hard but back straight, no smile, no teeth showing. In the "
    "first frame she is already in the lane on screen right, walking upright toward the black-lacquered gate; from the first second she walks slowly up to it and stops, lifting "
    "her eyes to it. Her lips stay closed. End: halfway through looking up at the gate."),
    motion="Tired but upright, she walks up the lane to the black gate and stops.")
shot("c25", B3, camera="Wide shot, slow push in", characters=["meifeng", "yuetang-18"], action_seconds=3, prompt=(
    f"{YARD}, {YARD_WIDE}. Exactly two people in the whole frame, one face. In the right foreground, seen only from behind, {YT}, the navy school bag hanging from her left "
    f"hand, her face unseen. In the middle, standing by the round stone table, {MF_FULL}, holding {FOLDED} in both hands. Lin Meifeng: "
    "one brow arched, eyes lifting to fix on the woman in the doorway, red lips curled up at one corner with no teeth showing, chin raised. In the first frame Shen Yuetang "
    "has just stopped in the doorway; in the first second Lin Meifeng looks up at her and lifts the folded white garment to her chest. Everyone's lips stay closed. "
    "End: the garment held up at her chest."),
    motion="Lin Meifeng looks up from the stone table and lifts the folded white garment as Yuetang comes in.")
shot("c26", B3, camera="Over-the-shoulder medium close-up, locked", characters=["meifeng", "yuetang-18"], ref_characters=["meifeng", "yuetang-18"], no_set=True,
     clip_seconds=8, prompt=(
    f"{YARD}; {Y_MF}. Exactly two people in the whole frame. Over Shen Yuetang's left shoulder: {YT_LFG}. On screen left, {MCU.format(who='she')}: {MF}, holding "
    f"{FOLDED} at her chest in both hands. Mouth corners pulled up into a fake smile with no teeth showing, eyes not smiling and coldly fixed on "
    "Shen Yuetang, brows arched high, chin raised. Her lips are closed until she starts, and she starts within the first second. Lin Meifeng, turned to Shen Yuetang at "
    "screen right in three-quarter profile, speaks a short Mandarin line, drawling the end, her lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang's lips "
    "stay closed. The camera holds a static shot. End: the fake smile, her eyes on Shen Yuetang."),
    motion="With a fake smile she says she found something in Yuetang's wooden box.")
shot("c27", B3, camera="Medium shot, slow push in to a medium close-up", characters=["meifeng"], no_set=True, clip_seconds=8,
     addressee="Shen Yuetang beyond the right edge of the frame, well off to the right of the lens", prompt=(
    f"{YARD}; behind her only out-of-focus corridor pillars and a dark wall. Exactly one person in the whole frame: {MF}; in the first frame she is already holding {ROBE} "
    "by its shoulders in both hands, shaken open and hanging down in front of her; warm yellow corridor light from screen left on her face and the white cloth. Brows arched "
    "high, eyes narrowed at the woman far off to the right, red lips twisted coldly to one side with no teeth showing, chin raised high. In the first second she lifts the "
    "open robe toward screen right to chest height; her lips are closed until she starts, and she starts within the first second. Lin Meifeng, turned toward her in "
    "three-quarter profile, speaks a short Mandarin line, with a sharp cold sneer, her lips, jaw and cheeks moving clearly with every syllable. End: the robe held up toward her."),
    motion="Holding the burial robe up by its shoulders, she sneers that it is the old lady's own burial robe.")
shot("c28", B3, camera="Low-angle medium close-up, locked", characters=["yuetang-18"], no_set=True, action_seconds=5, prompt=(
    f"{YARD}; seen from stone-table height looking up, {Y_YT}. Exactly one person in the whole frame, a medium close-up from the chest up: {YT_UP}, standing in the doorway, "
    "the school bag in her left hand below the bottom edge of the frame. Eyes fixed on the robe far off to the left of the lens, brows drawn together, lips pressed tight, "
    f"jaw tightening, a slow breath in, {NOSMILE}; the same face from the first frame to the last. In the first second her bare right hand with no ring slowly lowers from "
    "her waist to hang at her side; she keeps her back straight and does not step back. Her lips stay closed. The camera holds a static shot. End: standing her ground, eyes on the robe."),
    motion="Eyes on the burial robe, she lowers her right hand and stands her ground.")
shot("c29", B3, camera="Over-the-shoulder medium shot, slow push in from a medium shot to a medium close-up", characters=["meifeng", "yuetang-18"],
     ref_characters=["meifeng", "yuetang-18"], no_set=True, clip_seconds=8, prompt=(
    f"{YARD}; behind her only the out-of-focus round stone table and corridor pillars; warm yellow corridor light. Exactly two people in the whole frame. Over Shen Yuetang's "
    f"left shoulder: {YT_LFG}. On screen left: {MF}, in the first frame already standing still by the round stone table, gripping {ROBE} by "
    "its shoulders, shaken open and held out toward Shen Yuetang. Brows shot up, eyes glaring at Shen Yuetang, mouth corners pulled down as she talks, chin thrust forward, no smile. In the first second she gives the robe "
    "one shake at her, without stepping; her lips are closed until she starts, and she starts within the first second. Lin Meifeng, turned to Shen Yuetang at screen right "
    "in three-quarter profile, speaks a short Mandarin line, her voice rising high, her lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang in the "
    "foreground does not move; her lips stay closed. End: the robe held out at her, her eyes on Shen Yuetang."),
    motion="Shaking the robe at her, Lin Meifeng demands where she got the old lady's burial robe.")

ORDER = ["camera", "characters", "looks", "ref_characters", "set", "set_variant", "no_set", "lamp", "lamp_in_frame", "lamp_quiet", "no_face",
         "action_seconds", "clip_seconds", "addressee", "prompt", "motion"]


def main():
    parsed = parse_script.parse(ROOT / "docs/videos/tai-nainai-e007/script.md")
    rows = {s["id"]: s for sc in parsed["scenes"] for s in sc["shots"]}
    assert set(rows) == set(S), (set(rows) ^ set(S))
    shots = {}
    for sid in rows:
        e = S[sid]
        out = {"zh_sha256": rows[sid]["row_sha256"]}
        for k in ORDER:
            if k in e:
                out[k] = e[k]
        shots[sid] = out
    doc = {
        "episode": 7,
        "music": ("a light, playful comedy cue of plucked strings and soft woodwinds on the morning bus with one half-beat stop after she names the old stops, then a cold, "
                  "restrained tension cue of muted low strings at the school gate with one accent when the girl sees her, then a slow suspense cue of low drones and a "
                  "few soft piano notes at dusk in the lane and the courtyard, one accent on the last question; restrained, no vocals"),
        "thumbnail": {"headline": "沈家的保母", "shot": "c23"},
        "speaker_overrides": {},
        "shots": shots,
    }
    p = ROOT / "docs/videos/tai-nainai-e007/shots-en.json"
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(p, len(shots))


if __name__ == "__main__":
    main()
