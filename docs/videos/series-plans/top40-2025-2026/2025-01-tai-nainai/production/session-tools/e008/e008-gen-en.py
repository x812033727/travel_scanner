#!/usr/bin/env python3
"""Write docs/videos/tai-nainai-e008/shots-en.json for the 2026-11-11 種田 rewrite (29 shots).

Each shot's English body is bound to its script.md row by zh_sha256 (compile.py --check). Re-run after editing a row:
  python3 -I e008-gen-en.py
"""
import json
import sys
from pathlib import Path

ROOT = Path("/home/user/travel_scanner")
sys.path.insert(0, str(ROOT / "docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools"))
import parse_script  # noqa: E402

# ---- people (same sentence every shot) ----
YT_UP = ("Shen Yuetang in her moon-white high-collared cotton shirt with frog buttons fastened to the throat and long narrow sleeves, one thick braid over her "
         "right shoulder, no earrings")
YT_FULL = YT_UP + ", an ankle-length navy cotton skirt and black cloth shoes"
MF = ("Lin Meifeng with big glossy dark chestnut shoulder-length curls, a pearl necklace, red nails and a fitted wine-red long-sleeved knit dress with a high "
      "round neckline")
NOTWEAR = "she is wearing her wine-red knit dress and is NOT wearing the white robe; the robe is only in her hands"
JY = ("Shen Jianye, a tall heavyset man with oiled black hair slicked back and one deep vertical line between his brows, in a tailored brown double-breasted "
      "suit with a cream shirt and a dark brown tie")
JB = ("Shen Jianbang with short black hair greying at the temples and thin black-framed glasses, in a slightly worn charcoal-grey suit with a white shirt "
      "buttoned to the top and no tie")
YQ = ("Shen Yuqin, an elderly woman with short silver-white hair, a navy wool cardigan over a light grey high-neck blouse and dark grey trousers, seated in a "
      "plain black-framed manual wheelchair")
FB = ("Fu Bo, a very old man with very short white hair, in his neatly ironed light blue-grey Chinese-style jacket with frog buttons, the silver chain of a "
      "pocket watch at a button")
FB_FULL = FB + ", black trousers and black cloth shoes"
KEYS = "an old bronze-coloured key ring in his right hand"
XM = ("Shen Xiaoman, a high-school girl with a high ponytail, in an oversized light grey hoodie and loose black track pants, her back to the door, her face "
      "never in the frame")

ROBE = ("a plain off-white cotton burial robe with a high stand-up collar, no V-neck, a frog-button fastening down the right side, long sleeves, mid-calf "
        "length with slits at both sides, only the robe and no trousers, no embroidery and nothing written on it")
FOLDED = "the same plain off-white cotton burial robe, high stand-up collar and side frog buttons, folded into a neat square"
BAG = ("Xiaoman's navy flap school bag with nothing written on it, a big round brass clasp in the middle of the flap and the little brass bells on a faded "
       "red cord hanging beside the clasp")
BAG_STAIN = BAG + ", dried pale brown milk-tea streaks on the flap"
BAG_WET = BAG + ", washed clean and still damp"

NOSMILE = "no smile, lips together, no teeth showing"
OPEN_F = "her lips are closed until she starts, and she starts within the first second"
OPEN_M = "his lips are closed until he starts, and he starts within the first second"
MCU = "a medium close-up from the chest up, {who} filling about half of the frame"

# ---- places ----
YARD = "The inner stone courtyard of the old Shen house at dusk, just after dark"
YARD_WIDE = ("seen from the back door of the main hall looking north as in the courtyard picture: a round stone table with a few stone stools in the middle on "
             "the sunken stone floor; an old well with a small wooden roof on the left; bamboo drying poles leaning on the right; covered corridors with dark red "
             "pillars on both sides, warm yellow light glowing on their walls; at the far end the ancestral hall's dark lattice doors above stone steps")
Y_LEFT = "behind {w} only out-of-focus dark red corridor pillars and warm yellow light glowing on a wall"
Y_YT = "behind her only out-of-focus corridor pillars and a dark wall"
KIT = "The kitchen of the old Shen house late at night"
KIT_WIDE = ("seen from the front of the room toward the back wall as in the kitchen picture: on the left wall an open door with the dark night beyond; in the "
            "middle of the back wall a white sink under a black window and white wall tiles; on the right an old white gas stove; on the right wall a doorway "
            "to a small laundry nook; in the middle one square wooden table with four wooden stools; one bare light bulb glowing under the ceiling; nothing "
            "hanging on the walls")
CORR = "The covered corridor of the old Shen house late at night"
CORR_WIDE = ("seen along the corridor as in the corridor picture: on the left wall a row of dark red wooden doors, dark red pillars and rolled-up bamboo blinds; "
             "on the right wall a long wooden bench; two small wall lamps with white shades, one far on the left and one on the right; at the far end an open doorway onto the dark courtyard; a green "
             "metal bin with a lid beside it, nothing written on it")
CRACK = "the near dark red wooden door on the left wall stands open a finger's width, flickering white light coming through the crack"

YT_LFG = "her left shoulder, moon-white collar and the back of her black hair soft at the right frame edge, only the back of her head, her face unseen"
MF_RFG = "her right shoulder in the wine-red knit sleeve and the back of her dark chestnut curls soft at the left frame edge, only the back of her head, her face unseen"

S = {}
Y = dict(set="shenjia-yuanzi")
K = dict(set="shenjia-chufang")
C = dict(set="shenjia-huilang")


def shot(sid, base, **kw):
    e = dict(base)
    e.update(kw)
    S[sid] = e


# ---- 第一場：院子 ----
shot("c01", Y, camera="Over-the-shoulder medium close-up, slow push in", characters=["meifeng", "yuetang-18"], ref_characters=["meifeng", "yuetang-18"], no_set=True,
     clip_seconds=10, prompt=(
    f"{YARD}; {Y_LEFT.format(w='her')}. Exactly two people in the whole frame. Over Shen Yuetang's shoulder: only the back of her head with glossy black hair "
    f"soft at the right frame edge, no face, no ear, no earring. On screen left, {MCU.format(who='she')}: {MF}; {NOTWEAR}. In the first frame she is "
    f"already standing still, both hands holding {ROBE} up in front of her chest toward Shen Yuetang, her lips closed. Brows shot up, eyes glaring at Shen "
    "Yuetang, mouth corners pulled down, chin thrust forward, chest heaving, no smile, no teeth. In the first second she gives the robe one hard shake toward "
    f"her; {OPEN_F}. Lin Meifeng, turned to Shen Yuetang at screen right in three-quarter profile, chin up, speaks a short Mandarin line, shouting for the whole "
    "house to hear, her lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang's lips stay closed. End: the robe held up, her eyes on Shen Yuetang."),
    motion="Shaking the burial robe at the nanny, Lin Meifeng shouts for the whole house to come and see the thief.")
shot("c02", Y, camera="Medium close-up, locked", characters=["yuetang-18"], no_set=True, action_seconds=2, prompt=(
    f"{YARD}; {Y_YT}; warm yellow wall light from screen left on half her face. Exactly one person in the whole frame, a medium close-up from the chest up: "
    f"{YT_UP}, her hands below the bottom edge of the frame. Eyes on the woman far off to the left of the lens, then moving down to the white robe in her hands, "
    f"brows drawing together, lips closed, chin tucked, a slow breath in, {NOSMILE}; the same face from the first frame to the last. In the first second she "
    "takes half a slow, steady step toward the woman, her eyes moving from the woman's face down to the robe and staying there. Her lips stay closed. The camera holds a static shot. End: her eyes on the robe."),
    motion="She steps half a step toward Lin Meifeng, her eyes going from her face down to the burial robe.")
shot("c03", Y, camera="Medium two-shot, locked", characters=["meifeng", "yuetang-18"], no_set=True, action_seconds=2, prompt=(
    f"{YARD}; seen side-on by the round stone table, {Y_LEFT.format(w='them')}. Exactly two people in the whole frame, facing each other side-on, never looking at "
    f"the camera. On screen left {MF}; {NOTWEAR}; her right hand still holds one shoulder of {ROBE}. On screen right {YT_UP}; in the first frame her bare right "
    "hand already holds the other shoulder of the robe; her left hand is out of the frame. Lin Meifeng: one brow raised, eyes narrowed, red lips twisted to one "
    f"side, no teeth. Shen Yuetang: brows level, eyes on Lin Meifeng's face, lips closed, chin tucked, {NOSMILE}. In the first second Shen Yuetang draws the robe "
    "toward herself, slow and steady, and Lin Meifeng's fingers slide off its shoulder. Everyone's lips stay closed. The camera holds a static shot. End: the "
    "moment her fingers slip off."),
    motion="Yuetang draws the robe to herself and Lin Meifeng's fingers slide off it.")
shot("c04", Y, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "meifeng"], ref_characters=["yuetang-18", "meifeng"], no_set=True,
     clip_seconds=9, prompt=(
    f"{YARD}; {Y_YT}. Exactly two people in the whole frame. Over Lin Meifeng's right shoulder: {MF_RFG}. On screen right, {MCU.format(who='she')}: {YT_UP}, "
    f"holding {FOLDED} against her chest with both hands. Brows level, eyes fixed on Lin Meifeng, lips pressing together between phrases, chin slightly tucked, "
    f"steady breath, {NOSMILE}; the same face from the first frame to the last. {OPEN_F.capitalize()}. Shen Yuetang, turned to Lin Meifeng at screen left in "
    "three-quarter profile, speaks a short Mandarin line, calmly, her voice falling at the end, her lips, jaw and cheeks moving clearly with every syllable, pressing "
    "the folded robe gently to her chest. Lin Meifeng's lips stay closed. End: the robe held to her chest, her eyes on Lin Meifeng."),
    motion="Holding the folded robe to her chest, she says the old lady gave it to her herself.")
shot("c05", Y, camera="Wide shot, slow push in", characters=["meifeng", "jianye"], action_seconds=3, prompt=(
    f"{YARD}, {YARD_WIDE}. Exactly three people in the whole frame, two faces. FIRST, at the right edge of the foreground, seen only from behind and out of focus: "
    "a young woman's back in a moon-white high-collared shirt and an ankle-length navy skirt, one thick black braid down her right shoulder, her face unseen. "
    f"In the middle, by the round stone table: {MF}, black low heels, her hands empty. On the left, in the first frame already stepping in from the left corridor: "
    f"{JY}, polished brown shoes. Shen Jianye: brows knitted, eyes fixed on the white robe in front of the young woman, lips pressed tight, {NOSMILE}. Lin Meifeng: "
    "one brow raised, one corner of her red lips curled up, no teeth, eyes on the young woman. In the first second he strides up behind Lin Meifeng with weighted "
    "steps and stops; she shifts half a step aside. Everyone's lips stay closed. End: he stops behind her."),
    motion="Jianye strides into the courtyard and stops behind Lin Meifeng.")
shot("c06", Y, camera="Over-the-shoulder medium close-up, locked", characters=["jianye", "yuetang-18"], ref_characters=["jianye", "yuetang-18"], no_set=True,
     clip_seconds=10, prompt=(
    f"{YARD}; {Y_LEFT.format(w='him')}. Exactly two people in the whole frame. Over Shen Yuetang's left shoulder: {YT_LFG}. On screen left, {MCU.format(who='he')}: "
    f"{JY}. Brows knitted hard, eyes impatient on the robe in her hands, mouth corners pulled down, chin raised, a snort through the nose, {NOSMILE}. In the first "
    f"second he jabs his right hand toward the robe at screen right; {OPEN_M}. Shen Jianye, turned to Shen Yuetang at screen right in three-quarter profile, speaks "
    "a short Mandarin line, impatiently, his lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang's lips stay closed. The camera holds a static "
    "shot. End: his eyes on her."),
    motion="Jianye jabs a finger at the robe: the dead woman's things are her estate.")
shot("c07", Y, camera="Low-angle medium shot, slow push in to a medium close-up", characters=["yuetang-18"], no_set=True, clip_seconds=10,
     addressee="Shen Jianye beyond the left edge of the frame, well off to the left of the lens", prompt=(
    f"{YARD}; seen from stone-table height looking up, behind her only out-of-focus corridor pillars and dark eaves. Exactly one person in the whole frame, "
    f"at first a medium shot from the waist up: {YT_UP}, holding {FOLDED} against her chest; warm yellow wall light from screen left on half her face. Back very "
    f"straight, chin lifted a little, eyes fixed on the man far off to the left, brows level, lips pressing together between words, steady breath, {NOSMILE}; the "
    f"same face from the first frame to the last. {OPEN_F.capitalize()}. Shen Yuetang, turned toward him in three-quarter profile, speaks a short Mandarin line, "
    "slowly, word by word, her lips, jaw and cheeks moving clearly with every syllable. End: her eyes still on him."),
    motion="Looking up at Jianye, she says that while the old lady lives, these are not a dead woman's clothes.")
shot("c08", Y, camera="Over-the-shoulder medium close-up, slow push in", characters=["meifeng", "yuetang-18"], ref_characters=["meifeng", "yuetang-18"], no_set=True,
     clip_seconds=10, prompt=(
    f"{YARD}; {Y_LEFT.format(w='her')}. Exactly two people in the whole frame. Over Shen Yuetang's left shoulder: {YT_LFG}. On screen left, {MCU.format(who='she')}: "
    f"{MF}, in the first frame her arms already folded across her chest, her hands empty. One brow cocked, eyes half-lidded, one corner of her red lips curled up "
    f"in a sneer, no teeth, chin raised high. In the first second she leans forward a little; {OPEN_F}. Lin Meifeng, turned to Shen Yuetang at screen right in "
    "three-quarter profile, speaks a short Mandarin line, sneering, her lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang's lips stay closed. "
    "End: arms folded, her eyes on Shen Yuetang."),
    motion="Arms folded, Lin Meifeng sneers: then tell us what the old lady said to you.")
shot("c09", Y, camera="Medium close-up, locked", characters=["yuetang-18"], no_set=True, clip_seconds=10,
     addressee="Lin Meifeng beyond the left edge of the frame, well off to the left of the lens", prompt=(
    f"{YARD}; {Y_YT}; warm yellow wall light from screen left on her face. Exactly one person in the whole frame, a medium close-up from the chest up: {YT_UP}, "
    "the folded white robe held at her chest at the bottom edge of the frame. Eyes darkened and fixed on the woman far off to the left, brows lowered a little, "
    f"lips pressing together between the two sentences, chin tucked, slow breath, {NOSMILE}; the same face from the first frame to the last. {OPEN_F.capitalize()}. "
    "Shen Yuetang, turned toward her in three-quarter profile, speaks a short Mandarin line in an old woman's voice, very slow and soft, her voice sinking at the "
    "end, her lips, jaw and cheeks moving clearly with every syllable. The camera holds a static shot. End: her eyes still on her."),
    motion="In the old lady's slow, soft voice, she repeats what was said at dinner that night.")
shot("c10", Y, camera="Medium shot over the shoulder, locked", characters=["yuetang-18", "meifeng"],
     ref_characters=["yuetang-18", "meifeng"], no_set=True, clip_seconds=12, prompt=(
    f"{YARD}; {Y_YT}. Exactly two people in the whole frame. Over Lin Meifeng's right shoulder: {MF_RFG}. On screen right, from the waist up: {YT_UP}; in the "
    f"first frame she is already stooping a little like an old woman, both hands holding {FOLDED} folded in front of her waist. Brows drooping, eyelids half "
    f"lowered, lips pressing together between phrases, chin pushed forward, slow breath, {NOSMILE}; the same face from the first frame to the last. "
    f"{OPEN_F.capitalize()}. Shen Yuetang, turned to Lin Meifeng at screen left in three-quarter profile, speaks a short Mandarin line in a deliberately slow, "
    "old-sounding drawl, her lips, jaw and cheeks moving clearly with every syllable, her back staying slightly stooped. Lin Meifeng's lips stay closed. The camera holds a static shot. End: "
    "still stooping, her eyes on Lin Meifeng."),
    motion="Stooping like an old woman, she mimics Lin Meifeng mimicking the old lady that night.")
shot("c11", Y, camera="Medium two-shot, locked", characters=["meifeng", "jianye"], no_set=True, action_seconds=2, prompt=(
    f"{YARD}; {Y_LEFT.format(w='them')}. Exactly two people in the whole frame, both facing screen right, never looking at the camera. In front on screen left: "
    f"{MF}, her arms folded across her chest; half a step behind her on her right: {JY}. Lin Meifeng: her sneer frozen on her face, eyes wide, brows up, mouth "
    "corners still curled but stiff, no teeth, breath held. Shen Jianye: brows raised, eyes wide, lips parted and then closed, a hard swallow, no smile, no teeth. "
    "In the first second Lin Meifeng's folded arms slowly loosen and drop; Shen Jianye pulls his chin back. Everyone's lips stay closed. The camera holds a static shot. End: halfway through her "
    "arms dropping."),
    motion="Lin Meifeng's sneer freezes and her folded arms drop; Jianye stares.")
shot("c12", Y, camera="Over-the-shoulder medium close-up, locked", characters=["meifeng", "yuetang-18"], ref_characters=["meifeng", "yuetang-18"], no_set=True,
     clip_seconds=10, prompt=(
    f"{YARD}; {Y_LEFT.format(w='her')}. Exactly two people in the whole frame. Over Shen Yuetang's left shoulder: {YT_LFG}. On screen left, {MCU.format(who='she')}: "
    f"{MF}, her hands at her sides. From the first frame a forced dry laugh: mouth corners yanked up, eyes not laughing and staring, brows arched high, chin "
    f"raised, no teeth. In the first second she gives one dry laugh and flicks her right hand outward; {OPEN_F}. Lin Meifeng, turned to Shen Yuetang at screen "
    "right in three-quarter profile, speaks a short Mandarin line, shrill, her lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang's lips stay "
    "closed. The camera holds a static shot. End: the forced smile, her eyes on Shen Yuetang."),
    motion="With a forced laugh she says anyone could make that up from one line overheard at the door.")
shot("c13", Y, camera="Wide shot, slow push in", characters=["yuqin"], action_seconds=4, prompt=(
    f"{YARD}, {YARD_WIDE}. Exactly two people in the whole frame, one face. FIRST, at the right edge of the foreground, seen only from behind and out of focus: a "
    "young woman's back in a moon-white high-collared shirt and an ankle-length navy skirt, one thick black braid down her right shoulder, her face unseen. On the "
    f"right, on the raised walkway of the right-hand corridor, not yet down the step: {YQ}, both hands on the wheels, coming toward the foreground. Brows pushed up "
    "and together, eyes bright and glistening with tears, no redness, no red marks, staring straight at the young woman, mouth open in a cry. In the first second "
    "she gives the wheels one hard push and the wheelchair rolls along the walkway toward the foreground; the young woman's back does not move. End: halfway "
    "through the push."),
    motion="Yuqin pushes her wheelchair along the corridor toward Yuetang, crying out.")
shot("c14", Y, camera="Medium two-shot, locked", characters=["yuqin", "yuetang-18"], no_set=True, clip_seconds=9, prompt=(
    f"{YARD}; seen side-on, {Y_LEFT.format(w='them')}. Exactly two people in the whole frame. On screen left {YQ}; in the first frame her arms are already wrapped "
    f"around the young woman's waist and her face is lifted from her side toward her, in three-quarter profile toward the upper right. On screen right {YT_UP}, "
    "standing and bending toward her, her bare right hand already resting on the old woman's back, her left hand down out of the frame. Shen Yuqin: "
    "brows pushed up and together, eyes glistening with tears, no redness, no red marks, certain and fixed on the young woman's face, mouth corners pulled down. "
    f"Shen Yuetang: brows drawn gently up and together, eyes looking down at her, lips closed, {NOSMILE}. {OPEN_F.capitalize()}. Shen Yuqin, turned to Shen "
    "Yuetang in three-quarter profile, speaks a short Mandarin line, crying and certain, her lips, jaw and cheeks moving clearly with every syllable; Shen Yuetang "
    "pats her back once. Shen Yuetang's lips stay closed. The camera holds a static shot. End: holding each other."),
    motion="Holding her round the waist, Yuqin cries: Mama, why did you take so long to come back?")
shot("c15", Y, camera="Medium close-up, slow push in", characters=["yuetang-18"], no_set=True, clip_seconds=9,
     addressee="Shen Yuqin below the lower left edge of the frame", prompt=(
    f"{YARD}; {Y_YT}; seen from slightly low. Exactly two people in the whole frame, one face. FIRST, at the lower left edge of the frame, very close to the lens "
    "and out of focus: the back of an old woman's short silver-white hair, only the back of her head, no face. On screen right, a medium close-up from the chest "
    f"up: {YT_UP}, bending toward her, her hands below the bottom edge of the frame; warm yellow wall light from screen left on her face. Brows drawn gently up "
    "and together, eyes soft and looking down at the old woman, a faint shine of tears with no redness, lips pressing together between phrases, a slow breath "
    f"out, {NOSMILE}; the same face from the first frame to the last. {OPEN_F.capitalize()}. Shen Yuetang, turned toward her in three-quarter profile, speaks a "
    "short Mandarin line, softly, her lips, jaw and cheeks moving clearly with every syllable, her body moving slightly with the patting hand out of the frame. "
    "End: her eyes on the old woman."),
    motion="Patting her back, she softly tells her not to cry: I am here.")
shot("c16", Y, camera="Medium close-up, locked", characters=["jianye"], no_set=True, clip_seconds=10,
     addressee="Shen Yuetang and Shen Yuqin beyond the right edge of the frame, well off to the right of the lens", prompt=(
    f"{YARD}; {Y_LEFT.format(w='him')}. Exactly one person in the whole frame, a medium close-up from the chest up: {JY}. From the first frame a covering dry "
    "smile: one mouth corner pulled sideways, eyes not smiling and shifting, the line between his brows deepening, chin pulled in, no teeth; the same face from "
    f"the first frame to the last. In the first second he spreads both hands; {OPEN_M}. Shen Jianye, turned toward them in three-quarter profile, speaks a short "
    "Mandarin line, with a dry covering laugh, his lips, jaw and cheeks moving clearly with every syllable. The camera holds a static shot. End: hands spread."),
    motion="With a dry laugh Jianye says his aunt is confused again, calling a nanny her mother.")
shot("c17", Y, camera="Medium close-up, slow push in", characters=["jianbang"], no_set=True, clip_seconds=10,
     addressee="the people in the courtyard beyond the left edge of the frame, well off to the left of the lens", prompt=(
    f"{YARD}; behind him only the out-of-focus door frame of the main hall and warm light inside. Exactly one person in the whole frame, a medium close-up from "
    f"the chest up: {JB}, standing in the doorway; in the first frame his right hand already holds a phone with no logo to his ear, its plain black back outward. "
    "Brows knitted tight, eyes staring behind his glasses, face pale, lips slightly parted, tight breath, no smile, no teeth; the same face from the first frame "
    f"to the last. In the first second he lowers the phone slowly from his ear; {OPEN_M}. Shen Jianbang, turned toward the courtyard in three-quarter profile, "
    "speaks a short Mandarin line, his voice dry and stunned, his lips, jaw and cheeks moving clearly with every syllable. End: the phone lowered, his eyes on the "
    "courtyard."),
    motion="Lowering his phone, Jianbang says the handover has been moved three days earlier.")
shot("c18", Y, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "meifeng"], ref_characters=["yuetang-18", "meifeng"], no_set=True,
     clip_seconds=10, prompt=(
    f"{YARD}; {Y_YT}. Exactly two people in the whole frame. Over Lin Meifeng's right shoulder: {MF_RFG}. On screen right, {MCU.format(who='she')}: {YT_UP}, "
    f"holding {FOLDED} against her chest with both hands. Eyes darkened and fixed on Lin Meifeng, brows pressed down, lips pressing together between phrases, jaw "
    f"set, steady breath, {NOSMILE}; the same face from the first frame to the last. {OPEN_F.capitalize()}. Shen Yuetang, turned to Lin Meifeng at screen left in "
    "three-quarter profile, speaks a short Mandarin line, low and steady, her lips, jaw and cheeks moving clearly with every syllable, and draws the robe closer "
    "to her chest. Lin Meifeng's lips stay closed. End: the robe held close, her eyes on Lin Meifeng."),
    motion="Holding the robe close, she says it goes back in the box and nobody touches the old lady's things again.")

# ---- 第二場：廚房到東迴廊 ----
shot("c19", K, camera="Wide shot, slow push in", characters=["yuetang-18", "fubo"], action_seconds=3, prompt=(
    f"{KIT}, {KIT_WIDE}; a corner of the wooden table in the lower foreground. Exactly two people in the whole frame. On screen right at the sink, side-on: "
    f"{YT_FULL}, her sleeves folded back to the wrists; in the first frame both hands already hold {BAG_WET} up above the sink, the bells hanging clear of the "
    f"water. On screen left, in the first frame already stepping in through the open door: {FB_FULL}, {KEYS}. Shen Yuetang: brows slightly drawn, eyes down on "
    f"the bag, lips closed, {NOSMILE}. Fu Bo: brows lifted, eyes on the bag in her hands, lips closed, no smile, no teeth. In the first second she presses her "
    "palm once on the flap of the bag; he takes one step toward her and stops. Everyone's lips stay closed. End: he stops."),
    motion="Late at night she holds the washed school bag over the sink as Fu Bo comes in with his keys.")
shot("c20", K, camera="Medium close-up, locked", characters=["fubo"], no_set=True, clip_seconds=10,
     addressee="Shen Yuetang beyond the right edge of the frame, well off to the right of the lens", prompt=(
    f"{KIT}; behind him only the out-of-focus open door in the left wall and the dark night beyond it. Exactly one person in the whole frame, a medium close-up "
    f"from the chest up: {FB}, {KEYS} held at his chest; light from the bare bulb from screen right on his face. Brows drawn up and together, eyes worried on the "
    "young woman and the bag far off to the right, mouth corners pulled down, chin slightly tucked, no smile, no teeth; the same face from the first frame to the "
    f"last. {OPEN_M.capitalize()}. Fu Bo, turned toward her in three-quarter profile, speaks a short Mandarin line, in a low voice, his lips, jaw and cheeks "
    "moving clearly with every syllable. The camera holds a static shot. End: his eyes on her."),
    motion="Fu Bo asks in a low voice why she is still washing Xiaoman's bag so late.")
shot("c21", K, camera="Medium close-up, slow push in", characters=["yuetang-18"], no_set=True, clip_seconds=10,
     addressee="Fu Bo beyond the left edge of the frame, well off to the left of the lens", prompt=(
    f"{KIT}; behind her only the out-of-focus black window and white wall tiles. Exactly one person in the whole frame, a medium close-up from the chest up: "
    f"{YT_UP}, her sleeves folded back to the wrists; her left hand holds {BAG_WET} up at chest height, and her bare right hand already cups the bells. Brows "
    f"level, eyes on the old man far off to the left, lips pressing together between phrases, chin slightly tucked, {NOSMILE}; the same face from the first frame "
    f"to the last. In the first second she lifts the bag a little; {OPEN_F}. Shen Yuetang, turned toward him in three-quarter profile, speaks a "
    "short Mandarin line, calmly and briefly, her lips, jaw and cheeks moving clearly with every syllable. End: the bag held up, her eyes on him."),
    motion="Holding up the washed bag, she says only that it got dirty and she is taking it back to her.")
shot("c22", K, camera="Medium close-up, locked", characters=["fubo"], no_set=True, clip_seconds=10,
     addressee="Shen Yuetang beyond the right edge of the frame, well off to the right of the lens", prompt=(
    f"{KIT}; behind him only the out-of-focus open door in the left wall and the dark night beyond it. Exactly one person in the whole frame, a medium close-up "
    f"from the chest up: {FB}, {KEYS} at his chest. Brows knitted, eyes flicking toward the corridor far right and back to her, mouth corners pulled down, lips "
    f"pressing between words, tight breath, no smile, no teeth; the same face from the first frame to the last. {OPEN_M.capitalize()}. Fu Bo, turned toward her "
    "in three-quarter profile, speaks a short Mandarin line, worried, his lips, jaw and cheeks moving clearly with every syllable; then he turns toward the door "
    "at screen left. The camera holds a static shot. End: halfway through turning."),
    motion="Fu Bo says Xiaoman skipped dinner and shut herself in, and turns to go.")
shot("c23", C, camera="Wide shot, slow push in", characters=["yuetang-18"], action_seconds=3, prompt=(
    f"{CORR}, {CORR_WIDE}; {CRACK}; one out-of-focus dark red pillar in the foreground. Exactly one person in the whole frame: {YT_FULL}, in the first frame "
    f"already halfway along the corridor walking toward the camera, {BAG_WET} hanging from her left hand. Brows slightly drawn, eyes on the crack of the door on "
    f"the left, lips closed, soft breath, {NOSMILE}. In the first second she walks on with quiet, light steps to the door and stops in front of it. Her lips stay "
    "closed. End: she stops at the door."),
    motion="She walks quietly along the dark corridor and stops at the door left open a crack.")
shot("c24", C, camera="Medium shot, locked", characters=["yuetang-18"], no_set=True, action_seconds=4, prompt=(
    f"{CORR}; seen side-on, behind her only out-of-focus dark red pillars and a dark wall. Exactly one person in the whole frame, from the waist up: {YT_UP}, "
    "standing before a dark red wooden door on screen left that stands open a finger's width, the bag in her left hand below the bottom edge of the frame; in the "
    "first frame her bare right hand is already raised before the door, about to knock; flickering white light from the crack on her face. Brows drawn up and "
    f"together, eyes fixed on the crack, lips lightly pressed, breath held, {NOSMILE}; the same face from the first frame to the last. In the first second her "
    "raised hand stops in mid-air and does not knock; she tilts her head a little toward the crack to listen. Her lips stay closed. The camera holds a static "
    "shot. End: her hand still raised."),
    motion="About to knock, she stops with her hand raised and leans in to listen at the crack.")
shot("c25", C, camera="Medium close-up, locked", characters=["yuetang-18"], no_set=True, action_seconds=2, prompt=(
    f"{CORR}; behind her only out-of-focus dark red pillars. Exactly one person in the whole frame, a medium close-up from the chest up: {YT_UP}; her left hand "
    f"holds {BAG_WET} up at her chest, and in the first frame her bare right hand has already closed around the bells; flickering white light from the left on "
    f"her face. Brows slowly drawing together, eyes fixed on the crack beyond the left edge of the frame, lips pressed tight, jaw set, {NOSMILE}; the same face "
    "from the first frame to the last. In the first second her right hand tightens around the bells and she draws the bag in against her chest. Her lips stay closed. The camera holds a static shot. "
    "End: the bells held silent in her fist."),
    motion="She clamps the bells in her fist and draws the bag to her chest so nothing rings.")
shot("c26", C, camera="Point-of-view medium shot, locked", characters=["xiaoman"], looks={"xiaoman": "home"}, set="shenjia-xiaomanfang", no_face=True, action_seconds=4, prompt=(
    "A teenage girl's small bedroom late at night as in the bedroom picture, seen from the doorway: a single bed, an empty hook on the wall above the bed head, "
    f"a desk with a lit desk lamp, nothing written anywhere. Exactly one person in the whole frame: {XM}, sitting at the foot of the bed with her back to the "
    "camera, only her back, shoulders and ponytail seen; both hands hold a phone at her chest, its screen facing her and never seen; faint white light from the "
    "phone on the wall. In the first second her shoulders start to heave and her head sinks. Her face is never in the frame. The camera holds a static shot. "
    "End: head bowed, shoulders shaking."),
    motion="Xiaoman sits on her bed with her back to the door, shoulders shaking as a video plays.")
shot("c27", C, camera="Close-up, slow push in", characters=["yuetang-18"], no_set=True, action_seconds=4, prompt=(
    f"{CORR}; behind her only the out-of-focus dark corridor. Exactly one person in the whole frame, a close-up of her face and shoulders: {YT_UP}, her hands "
    "below the bottom edge of the frame; white light from the crack flickering on her face from the left. Brows slowly drawing together, eyes fixed on the crack "
    f"beyond the left edge of the frame with a faint shine of tears and no redness, lips pressed, jaw set, slow breath, {NOSMILE}; the same face from the first "
    "frame to the last. In the first second her chin tucks in and she blinks once, her eyes never leaving the crack. Her lips stay closed. End: her eyes on the "
    "crack."),
    motion="Lit by the flicker from the crack, she understands what the girl is afraid of.")
shot("c28", C, camera="Point-of-view medium shot, locked", characters=["xiaoman"], looks={"xiaoman": "home"}, set="shenjia-xiaomanfang", no_face=True, action_seconds=3, prompt=(
    "A teenage girl's small bedroom late at night as in the bedroom picture, seen from the doorway: a single bed, an empty hook on the wall above the bed head, "
    f"a desk with a lit desk lamp, nothing written anywhere. Exactly one person in the whole frame: {XM}, sitting at the foot of the bed with her back to the "
    "camera; in the first frame both hands still hold the phone at her chest, its screen facing her and never seen. In the first second she lays the phone on "
    "her lap and buries her head in both hands; the phone's light falls on the backs of her hands. Her face is never in the frame. The camera holds a static "
    "shot. End: her head in her hands."),
    motion="Xiaoman puts the phone down on her lap and buries her head in her hands.")
shot("c29", C, camera="Close-up, slow push in", characters=["yuetang-18"], no_set=True, action_seconds=5, prompt=(
    f"{CORR}; behind her only the dark corridor. Exactly one person in the whole frame, a close-up of her face and shoulders: {YT_UP}, the bag and her "
    "clenched right hand below the bottom edge of the frame; the phone light from the crack flickering on her face from the left. Eyes wide and fixed on the crack "
    f"beyond the left edge of the frame, brows pressed down, lips pressed tight, jaw set, breath held, {NOSMILE}; the same face from the first frame to the last. "
    "In the first second her shoulders tighten as her hidden hand grips harder; her eyes never leave the crack. Her lips stay closed. End: frozen at the door."),
    motion="Frozen at the door, she hears the voice message threatening to upload the video.")

ORDER = ["camera", "characters", "looks", "ref_characters", "set", "set_variant", "no_set", "lamp", "lamp_in_frame", "lamp_quiet", "no_face",
         "action_seconds", "clip_seconds", "addressee", "prompt", "motion"]


def main():
    parsed = parse_script.parse(ROOT / "docs/videos/tai-nainai-e008/script.md")
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
        "episode": 8,
        "music": ("a low tension cue of muted plucked strings and a soft drone in the courtyard at dusk, one accent as she mimics the old voice, a one-beat drop "
                  "when the old woman cries out, crossfading into a gentle solo guzheng memory cue as she holds her, then a quiet, low suspense cue of soft "
                  "drones and sparse piano notes in the night kitchen and corridor, one accent after the voice message; restrained, no vocals"),
        "thumbnail": {"headline": "這個家要散了", "shot": "c10"},
        "speaker_overrides": {},
        "shots": shots,
    }
    p = ROOT / "docs/videos/tai-nainai-e008/shots-en.json"
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(p, len(shots))


if __name__ == "__main__":
    main()
