#!/usr/bin/env python3
"""Write docs/videos/tai-nainai-e006/shots-en.json for the 2026-11-10 種田 rewrite (41 shots)."""
import json
import sys
from pathlib import Path

ROOT = Path("/home/user/travel_scanner")
sys.path.insert(0, str(ROOT / "docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools"))
import parse_script  # noqa: E402

YT = ("Shen Yuetang in her moon-white high-collared cotton shirt with frog buttons fastened to the throat, ankle-length navy cotton skirt and black cloth shoes, "
      "one thick braid over her right shoulder")
RING = "the thick old silver ring only on her left ring finger, her right hand bare with no ring"
JMB = "Jiang Mubai in gold-rimmed glasses, neatly side-parted black hair, a navy suit, a light blue shirt and a burgundy tie"
BROWN = "a closed dark brown leather document folder about A4 size with a brass clasp and a blank cover"
BLACK = "a closed black hard-cover document folder about A4 size with a blank cover, the metal clips inside unseen"
TRAY = ("a plain light wooden tray about the size of a magazine holding one small purple-clay teapot and three small white porcelain teacups of pale amber tea")
FB = ("Fu Bo, a very old man with very short white hair, in his neatly ironed light blue-grey Chinese-style jacket with frog buttons, black trousers and black cloth shoes, "
      "the silver chain of a pocket watch at a button")
ZY = ("Shen Zhiyuan with short neat black hair, a white pharmacist's coat worn open over a dark navy shirt, the white coat sleeves pushed up to mid-forearm, "
      "dark grey trousers and black sneakers")
ZY_UP = ("Shen Zhiyuan with short neat black hair, a white pharmacist's coat worn open over a dark navy shirt, the white coat sleeves pushed up to mid-forearm")
YT_UP = ("Shen Yuetang in her moon-white high-collared cotton shirt with frog buttons fastened to the throat and long narrow sleeves, "
         "one thick braid over her right shoulder")
FB_UP = ("Fu Bo, a very old man with very short white hair, in his neatly ironed light blue-grey Chinese-style jacket with frog buttons, "
         "the silver chain of a pocket watch at a button")
MF = ("Lin Meifeng with big glossy dark chestnut shoulder-length curls, a pearl necklace, red nails and a fitted wine-red long-sleeved knit dress with a high round neckline")
XM = ("Shen Xiaoman, a high-school girl with straight blunt bangs and a high ponytail, in a navy school blazer one size too big over a white shirt with a navy ribbon tie "
      "and a navy pleated skirt below the knee; her bangs and the shoulders of her blazer are damp, her face clean, both hands empty, no school bag")
MCU = "a medium close-up from the chest up, {who} filling about half of the frame"

HALL = "The main hall of the old Shen house on a clear, cold morning, the lamps off"
HALL_WIDE = ("seen from just inside the front door as in the hall picture: one long red-wood table running back into the hall with red-wood chairs along it; a long narrow side "
             "table against the back wall under one blank empty frame; on the left wall a tall grandfather clock with its face turned away into shadow, a wooden staircase and "
             "the door to the dining room; on the right wall a row of tall lattice doors letting in slanting morning sunlight and, further back, a plain wooden door to the study; "
             "both lantern-shaped ceiling lamps unlit; there is only this one long table in the hall")
HALL_HER = "behind her only the cream plaster wall and the dark wooden side of the tall clock, its face out of the frame"
HALL_RIGHT = "behind {who} only a plain wooden door and the tall lattice doors of the right wall with soft morning sunlight"
MORNING_R = "soft morning sunlight from screen right falls on her shoulder"

KITCHEN = "The kitchen of the old Shen house at about ten on a clear morning, no lamp on"
KITCHEN_WIDE = ("seen from the front of the room toward the back wall as in the kitchen picture: on the left wall an open door with a sunlit stone-paved courtyard path beyond "
                "it; in the middle of the back wall a white sink under a window; on the right of the back wall an old white gas stove with two pots; on the right wall an open "
                "doorway to a small laundry room; in the middle one square wooden table with four wooden stools; there is only this one table in the kitchen")
K_HER = "behind her only the out-of-focus window over the sink and white wall tiles"
K_FB = "behind him only the out-of-focus open door in the left wall and the sunlit stone path beyond it"

DINING = "The dining room of the old Shen house at night"
DINING_WIDE = ("seen from a corner of the room as in the dining-room picture: one long dark wooden table running back into the room with a row of empty high-backed wooden "
               "chairs on both sides and blue-and-white bowls and chopsticks set at every place; two windows in the left wall, black at night; one white pendant lamp lit above "
               "the table, the only lamp in the room; at the back right an open doorway, dark beyond; one dark wooden cupboard beside it")
D_HER = "behind her only a cream wall and one black night window"
D_DOOR = "behind {who} only the dark open doorway and the edge of a dark wooden cupboard"
LAMPLIGHT = "warm light from the pendant lamp above"

YT_RFG = "her right shoulder, moon-white collar and the thick black braid lying over it soft at the left frame edge, her face unseen"
YT_LFG = "her left shoulder, moon-white collar and the back of her black hair soft at the right frame edge, her face unseen"
JMB_FG = "his left shoulder in the navy suit and the back of his side-parted black hair soft at the right frame edge as he sits, his face unseen"
FB_LFG = "his left shoulder in the light blue-grey jacket and his very short white hair soft at the right frame edge, his face unseen"
FB_RFG = "his right shoulder in the light blue-grey jacket and his very short white hair soft at the left frame edge, his face unseen"
ZY_FG = "his left shoulder in the white pharmacist's coat and his short black hair soft at the right frame edge, his face unseen"
XM_FG = "her left shoulder in the damp navy blazer and her high black ponytail soft at the right frame edge, her face unseen"

S = {}
D1 = dict(set="shenjia-zhengting", set_variant="day")
D2 = dict(set="shenjia-chufang", set_variant="day")
D3 = dict(set="shenjia-fanting")


def shot(sid, base, **kw):
    e = dict(base)
    e.update(kw)
    S[sid] = e


# ---- 第一場：正廳（白天） ----
shot("c01", D1, camera="Wide shot, tracking behind Jiang Mubai toward the table", characters=["fubo", "yuetang-18", "jiangmubai"], action_seconds=3, prompt=(
    f"{HALL}, {HALL_WIDE}; the edge of the front door frame in the foreground. Exactly three people in the whole frame. In the middle foreground, seen only from behind, "
    f"Jiang Mubai: navy suit, side-parted black hair, black leather shoes, {BROWN} clamped under his left arm, his face never in the frame. Half a step ahead of him on "
    f"screen right, {FB}, leading the way, his head turned back toward him. At the back left, coming out of the dining-room door beside the staircase, {YT}, carrying {TRAY} "
    "in both hands. Fu Bo: brows level, eyes respectfully on the guest, lips closed, chin slightly tucked. Shen Yuetang: brows slightly drawn, eyes on the guest's face and then "
    "on his left arm, lips closed. In the first frame Jiang Mubai has just stepped over the threshold; from the first second he walks toward the table while Fu Bo gestures "
    "toward it with an open hand, and she carries the tray out, slow and steady. Everyone's lips stay closed. End: Jiang Mubai halfway to the table."),
    motion="The lawyer walks into the hall behind Fu Bo as she carries the tea out.")
shot("c04", D1, camera="Medium close-up, slow push in", characters=["fubo"], no_set=True, clip_seconds=8,
     addressee="Shen Yuetang beyond the left edge of the frame, well off to the left of the lens", prompt=(
    f"{HALL}; {HALL_RIGHT.format(who='him')}. Exactly one person in the whole frame: {FB_UP}, seen from the chest up in three-quarter profile from her side of the table, "
    "in the first frame already stopped beside the study door and half turned back; soft morning sunlight from screen right on half his face. Brows level, eyes respectful, "
    "mouth corners drawn down, chin slightly tucked, steady breath, no smile. In the first second he gestures with his right hand toward the study door beside him; "
    "Fu Bo speaks a short Mandarin line, respectfully, his lips, jaw and cheeks moving clearly with every syllable; then he turns and puts out his hand to push the study door. "
    "End: halfway into pushing the door."),
    motion="Fu Bo gestures at the study door, tells her why the lawyer has come, and turns to fetch the contract.")
shot("c05", D1, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "jiangmubai"], ref_characters=["yuetang-18", "jiangmubai"],
     no_set=True, clip_seconds=8, prompt=(
    f"{HALL}; {HALL_HER}. Exactly two people in the whole frame. Over Jiang Mubai's left shoulder: {JMB_FG}. On screen left, {MCU.format(who='she')}: {YT_UP}, {RING}, "
    "standing at the west side of the long red-wood table, both hands already folded at her waist in the first frame; one small white porcelain teacup already stands on the "
    f"table in front of him at the bottom edge of the frame; {MORNING_R}. Eyes fixed on his face, flicking down once to the folder under his left arm and back up, brows level, mouth corners still, "
    "chin slightly tucked, slow breath, no smile. In the first second she inclines her head a little; Shen Yuetang, turned to Jiang Mubai "
    "at screen right in three-quarter profile, speaks a short Mandarin line, evenly, her lips, jaw and cheeks moving clearly with every syllable. Jiang Mubai's lips stay "
    "closed. End: her hands folded at her waist, her eyes on him."),
    motion="His tea already served, she folds her hands and asks him where the third attachment is.")
shot("c06", D1, camera="Over-the-shoulder medium close-up, locked", characters=["jiangmubai", "yuetang-18"], ref_characters=["jiangmubai", "yuetang-18"],
     no_set=True, prompt=(
    f"{HALL}; {HALL_RIGHT.format(who='him')}. Exactly two people in the whole frame. Over Shen Yuetang's right shoulder: {YT_RFG}. On screen right, "
    f"{MCU.format(who='he')}: {JMB}, seated on a red-wood chair at the east side of the table, {BROWN} clamped under his left arm against his side; the table edge and one "
    "small white teacup at the bottom edge of the frame. Lips pressed into a thin polite line, eyes cool behind his lenses and fixed on her face, brows still, chin raised a "
    "little, no smile at any moment, not even at the end of the shot. In the first second he pushes the teacup aside an inch with two fingers of his right hand without "
    "drinking; Jiang Mubai, turned to Shen Yuetang at screen left in three-quarter profile, speaks a short Mandarin line, politely and coolly, his lips, jaw and cheeks moving "
    "clearly with every syllable. Shen Yuetang's lips stay closed. End: the cup pushed aside, his eyes on her."),
    motion="He pushes the tea aside untouched and tells her it is none of a nanny's business.")
shot("c07", D1, camera="Medium close-up, gentle push in to a medium close-up", characters=["yuetang-18"], no_set=True, clip_seconds=8,
     addressee="Jiang Mubai beyond the right edge of the frame, well off to the right of the lens", prompt=(
    f"{HALL}; {HALL_HER}; the camera on his side, to his left. Exactly one person in the whole frame, a medium close-up from the chest up: {YT_UP}, {RING}, both hands folded at her waist below the bottom edge "
    "of the frame; soft morning sunlight from screen right on her shoulder and half her face. Eyes steady and fixed on him far off to the right, brows slightly drawn, lips "
    "pressing together between phrases, chin tucked, slow breath, no smile. In the first second she takes half a step forward and leans in a little; Shen Yuetang, turned "
    "toward him in three-quarter profile, speaks a short Mandarin line, slowly and evenly, her lips, jaw and cheeks moving clearly with every syllable. End: her eyes still on him."),
    motion="Stepping closer, she tells him the index lists three attachments but only two are in the folder.")
shot("c08", D1, camera="Over-the-shoulder medium close-up, slow push in", characters=["jiangmubai", "yuetang-18"], ref_characters=["jiangmubai", "yuetang-18"],
     no_set=True, clip_seconds=8, prompt=(
    f"{HALL}; {HALL_RIGHT.format(who='him')}. Exactly two people in the whole frame. Over Shen Yuetang's right shoulder: {YT_RFG}. On screen right, "
    f"{MCU.format(who='he')}: {JMB}, seated, {BROWN} under his left arm; the table edge at the bottom of the frame. One brow cocked, eyes half-lidded behind his lenses, "
    "lips held in a thin polite line, chin raised, no smile at any moment, not even at the end of the shot. In the first second he leans back in the chair and taps the table "
    "edge once with his right forefinger; Jiang Mubai, turned to Shen Yuetang at screen left in three-quarter profile, speaks a short Mandarin line, slowly and smoothly, his "
    "lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang's lips stay closed. End: leaning back, his eyes on her."),
    motion="Leaning back, he waves the attachments off as standard forms the firm will add.")
shot("c09", D1, camera="Low-angle medium close-up, gentle push in to a medium close-up", characters=["yuetang-18"], no_set=True, clip_seconds=10,
     addressee="Jiang Mubai beyond the right edge of the frame, well off to the right of the lens", prompt=(
    f"{HALL}; seen from table height looking up, behind her only the out-of-focus upper cream wall and the dark wooden ceiling beams. Exactly one person in the whole frame, a medium close-up from the chest up: "
    f"{YT_UP}, {RING}, standing at the west side of the table, both hands folded at her waist at the bottom edge of the frame; morning sunlight slants from screen right across "
    "her shoulder and half her face. Back very straight, chin lifted slightly, eyes clear and fixed on him far off to the right, brows level, lips pressing together between "
    "the items, steady breath, no smile. In the first second she straightens her back; Shen Yuetang, turned toward him in three-quarter profile, speaks a short Mandarin line, "
    "slowly and firmly, her lips, jaw and cheeks moving clearly with every syllable, giving one small nod of the chin at each item. "
    "End: her hands folded, her eyes on him."),
    motion="Back straight, she lists the three things an old shop contract must attach.")
shot("c10", D1, camera="Close-up, locked", characters=["jiangmubai"], no_set=True, action_seconds=3, prompt=(
    f"{HALL}; {HALL_RIGHT.format(who='him')}. Exactly one person in the whole frame: {JMB}, seated, seen in three-quarter profile from her side; morning sunlight from "
    "screen right glints on his gold-rimmed glasses, which have already slid halfway down his nose in the first frame. From the first frame to the last the same caught-out face: brows raised, eyes frozen behind the lenses and fixed on her "
    "far off to the left of the lens, lips pressed tight, chin pulled in, no smile. In the first second he pushes his glasses back up his nose "
    "with his right middle finger; his eyes never leave her and never go to the camera. His lips stay closed. End: his finger leaving the frame of his glasses."),
    motion="Caught out, he pushes his slipped glasses back up his nose.")
shot("c11", D1, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "jiangmubai"], ref_characters=["yuetang-18", "jiangmubai"],
     no_set=True, clip_seconds=10, prompt=(
    f"{HALL}; {HALL_HER}. Exactly two people in the whole frame. Over Jiang Mubai's left shoulder: {JMB_FG}. On screen left, {MCU.format(who='she')}: {YT_UP}, {RING}, "
    f"both hands folded at her waist at the bottom edge of the frame; {MORNING_R}. Eyes fixed on his face, brows pressed down a little, lips pressing together between "
    "phrases, chin tucked, a quiet breath in through the nose, no smile. In the first second she draws her folded hands in and straightens her back; Shen Yuetang, turned to "
    "Jiang Mubai at screen right in three-quarter profile, speaks a short Mandarin line, calmly, her lips, jaw and cheeks moving clearly with every syllable; at the end her "
    "eyes drop once to his left arm. Jiang Mubai's lips stay closed. End: her eyes on his left arm."),
    motion="She tells him what is sold, when, and who guarantees it are all in the attachments, nothing standard.")
shot("c12", D1, camera="Point-of-view insert, close-up, locked", characters=["jiangmubai"], ref_characters=[], no_set=True, no_face=True, action_seconds=2, prompt=(
    f"{HALL}. Seen from across the table, the first frame is already tight on a seated man's left arm and side: the navy suit sleeve, a light blue shirt cuff, his left "
    f"hand pressed on {BROWN} under the arm; behind it the out-of-focus back of a red-wood chair and soft morning light. In the first second his arm clamps the folder hard "
    "against his body and the knuckles of his left hand whiten; he holds it there the whole shot. Only this one arm is in the frame, no face. End: the folder clamped tight."),
    motion="His left arm clamps the leather folder hard against his side.")
shot("c14", D1, camera="Over-the-shoulder medium close-up, slow push in", characters=["jiangmubai", "yuetang-18"], ref_characters=["jiangmubai", "yuetang-18"],
     no_set=True, clip_seconds=8, prompt=(
    f"{HALL}; {HALL_RIGHT.format(who='him')}. Exactly two people in the whole frame. Over Shen Yuetang's right shoulder: {YT_RFG}. On screen right, "
    f"{MCU.format(who='he')}, with room above his head: {JMB}, standing at the east side of the table, {BLACK} and {BROWN} already stacked together under his left arm. Brows pulled low, "
    "eyes narrowed behind his lenses and fixed on her, lips tight between words, chin raised, no smile at any moment, not even at the end of the shot. In the first second he "
    "fastens his jacket button with his right hand; Jiang Mubai, turned to Shen Yuetang at screen left in three-quarter profile, speaks a short Mandarin line, politely with a "
    "warning under it, his lips, jaw and cheeks moving clearly with every syllable; then he turns away toward the front door beyond the right edge of the frame. Shen "
    "Yuetang's lips stay closed. End: halfway through his turn, his whole head still in the frame."),
    motion="Buttoning his jacket, he warns her to mind the tea and turns to leave with the contract.")
shot("c15", D1, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "fubo"], ref_characters=["yuetang-18", "fubo"],
     no_set=True, clip_seconds=8, prompt=(
    f"{HALL}; {HALL_HER}. Exactly two people in the whole frame. Over Fu Bo's left shoulder: {FB_LFG}. On screen left, {MCU.format(who='she')}: {YT_UP}, {RING}, standing at "
    f"the west side of the table, the tray at the bottom edge of the frame; {MORNING_R}. Eyes fixed on his face, brows pressed low, lips pressing together between phrases, "
    "chin tucked, voice held low, no smile. In the first second her bare right hand sets the untouched teacup back on the tray at the bottom edge of the frame and she folds "
    "her hands at her waist; Shen Yuetang, turned to Fu Bo at screen right in three-quarter profile, speaks a short Mandarin line, low and certain, her lips, jaw and cheeks "
    "moving clearly with every syllable. Fu Bo's lips stay closed. End: her hands folded, her eyes on him."),
    motion="Clearing the untouched cup, she tells Fu Bo the third attachment is in the lawyer's leather folder.")

# ---- 第二場：廚房（白天） ----
shot("c16", D2, camera="Wide shot, slow push in", characters=["yuetang-18", "fubo"], action_seconds=3, prompt=(
    f"{KITCHEN}, {KITCHEN_WIDE}; a corner of the square table along the bottom edge of the frame. Exactly two people in the whole frame. On screen right {YT}, {RING}, her "
    f"cuffs folded back to the wrist, standing side-on at the sink, {TRAY.replace(' of pale amber tea', ', empty,')} on the counter beside the sink; on screen left {FB}, "
    "stepping in through the open door in the left wall, hands empty. Morning sun comes in through the open door and the window. Shen Yuetang: brows slightly drawn, eyes "
    "lowered to her hands, lips pressed. Fu Bo: brows level, eyes on her, lips closed. In the first second she rinses one small white teacup in the sink and sets it on the "
    "tray, while he steps over the threshold and walks two paces toward her. Everyone's lips stay closed. End: he stops a few paces from her."),
    motion="She rinses a teacup at the sink as Fu Bo steps into the kitchen.")
shot("c17", D2, camera="Insert, close-up, locked", characters=["yuetang-18"], ref_characters=[], no_set=True, no_face=True, action_seconds=3, prompt=(
    f"{KITCHEN}. The first frame is already tight on a young woman's soapy left hand in the centre of the frame, back of the hand up, a narrow moon-white cuff folded back "
    "to the wrist; the thick old silver ring is only on her left ring finger, its seal face turned to the palm and unseen. Only the fingertips of her bare right thumb and "
    "forefinger, with no ring, reach in from the right edge of the frame and pinch the ring; a white sink far out of focus behind. In the first second the fingertips twist "
    "the ring and pull; it does not move at all, the fingertips slip off and withdraw past the right edge. The ring stays only on her left ring finger the whole shot. Only "
    "her hands are in the frame, no face. End: her left hand alone in the centre, the ring still on its ring finger."),
    motion="Her fingertips twist and pull at the ring; it will not move.")
shot("c18", D2, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "fubo"], ref_characters=["yuetang-18", "fubo"],
     no_set=True, clip_seconds=8, prompt=(
    f"{KITCHEN}; {K_HER}. Exactly two people in the whole frame. Over Fu Bo's right shoulder: {FB_RFG}. On screen right, {MCU.format(who='she')}: {YT_UP}, {RING}, cuffs "
    "folded back to the wrist, standing at the sink; morning light from the window behind her rims her outline. Brows knitted, eyes going from her left hand up to his face, "
    "mouth corners turned down, a soft breath out, no smile. In the first second she raises her left hand to her chest, the back of the hand toward him; Shen Yuetang, "
    "turned to Fu Bo at screen left in three-quarter profile, speaks a short Mandarin line, low and puzzled, her lips, jaw and cheeks moving clearly with every syllable. "
    "Fu Bo's lips stay closed. End: her left hand still raised, her eyes on him."),
    motion="Raising her left hand, she asks him why the ring that used to turn now will not move.")
shot("c19", D2, camera="Over-the-shoulder medium close-up, locked", characters=["fubo", "yuetang-18"], ref_characters=["fubo", "yuetang-18"],
     no_set=True, clip_seconds=10, prompt=(
    f"{KITCHEN}; {K_FB}. Exactly two people in the whole frame. Over Shen Yuetang's left shoulder: {YT_LFG}. On screen left, {MCU.format(who='he')}: {FB_UP}. Eyes darting "
    "once to the open door at screen left and back to her face, brows drawn together, lips pressed between words, chin slightly tucked, no smile. In the first second he "
    "leans half a step closer and glances out of the door; Fu Bo, turned to Shen Yuetang at screen right in three-quarter profile, speaks a short Mandarin line, very low, his "
    "lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang's lips stay closed. End: leaning close, his eyes on her."),
    motion="Leaning close, Fu Bo whispers that the ring was made from one of Zuofu's three silver seals.")
shot("c20", D2, camera="Point-of-view insert, close-up, slow push in to the ring band", characters=["yuetang-18"], ref_characters=[], no_set=True, no_face=True, prompt=(
    f"{KITCHEN}. Looking down at her hands, the first frame is already tight on a young woman's open left palm facing up, narrow moon-white cuffs folded back to the "
    "wrist, the thick old silver ring on her left ring finger with its square seal face on the palm side, covered from the first frame by the thumb of her bare right hand, "
    "which has no ring; soap foam on the band; a white sink far out of focus behind. In the first second the right thumb, still covering the seal face, slowly wipes the foam "
    "off along the band, and the fingers of her left hand curl in gently. The thumb stays over the seal face the whole shot. Only her hands are in the frame, no face. "
    "End: the clean silver band, the seal face hidden under her thumb."),
    motion="Her thumb wipes the foam from the ring, covering its seal face.")
shot("c21", D2, camera="Close-up, locked", characters=["yuetang-18"], no_set=True, action_seconds=3, prompt=(
    f"{KITCHEN}; {K_HER.replace('the out-of-focus window', 'out-of-focus white wall tiles and a corner of the window frame').replace(' over the sink and white wall tiles', '')}; "
    f"the camera on Fu Bo's side. Exactly one person in the whole frame: {YT_UP}, head bowed, her hands below the bottom edge of the frame; morning light from the window at "
    "screen right on half her face. Her face in three-quarter profile turned toward screen left, eyes lowered to the lower left; the same face from the first frame to the last: eyes a little warm and wet at the rims, brows drawn gently up and together, lips closed, "
    "a slow breath in, no smile. In the first frame she is looking down to the left at her hand; from the first second she slowly lifts her eyes toward Fu Bo far off to the left of the "
    "lens, never at the camera. Her lips stay together the whole shot. End: her eyes on him."),
    motion="She slowly lifts her eyes from the ring to Fu Bo.")
shot("c22", D2, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "fubo"], ref_characters=["yuetang-18", "fubo"],
     no_set=True, clip_seconds=8, prompt=(
    f"{KITCHEN}; {K_HER}. Exactly two people in the whole frame. Over Fu Bo's right shoulder: {FB_RFG}. On screen right, {MCU.format(who='she')}: {YT_UP}, {RING}, cuffs "
    "folded back to the wrist, both hands folded at her waist at the bottom edge of the frame. Eyes darkening and steady on his face, brows "
    "pressed low, lips pressing together between phrases, chin tucked, no smile. In the first second she draws her folded hands in and "
    "straightens her back; Shen Yuetang, turned to Fu Bo at screen left in three-quarter profile, speaks a short Mandarin line, slowly, her lips, jaw and cheeks moving clearly "
    "with every syllable. Fu Bo's lips stay closed. End: her hands folded, her eyes on him."),
    motion="Hands folded, she asks where Zuofu's other two seals are now.")
shot("c23", D2, camera="Over-the-shoulder medium close-up, locked", characters=["fubo", "yuetang-18"], ref_characters=["fubo", "yuetang-18"],
     no_set=True, clip_seconds=8, prompt=(
    f"{KITCHEN}; {K_FB}. Exactly two people in the whole frame. Over Shen Yuetang's left shoulder: {YT_LFG}. On screen left, {MCU.format(who='he')}: {FB_UP}. Brows drawn "
    "together, eyes lowering and then lifting to her face, mouth corners pressed down, voice even lower, no smile. In the first second he points briefly with his right hand "
    "out of the open door at screen left, toward the ancestral hall, and drops the hand to his side; Fu Bo, turned to Shen Yuetang at screen right in three-quarter profile, "
    "speaks a short Mandarin line, low, his lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang's lips stay closed. End: his hand at his side, his eyes on her."),
    motion="Pointing toward the ancestral hall, Fu Bo says one seal is in a little box there and one is lost.")
shot("c24", D2, camera="Medium close-up, gentle push in to a medium close-up", characters=["yuetang-18"], no_set=True, clip_seconds=8,
     addressee="Fu Bo beyond the left edge of the frame, well off to the left of the lens", prompt=(
    f"{KITCHEN}; behind her only out-of-focus white wall tiles and a corner of the window frame; the camera on Fu Bo's side. Exactly one person in the whole frame, a medium close-up from the chest up: {YT_UP}, "
    f"{RING}, both hands folded at her waist with the ringed left hand underneath, at the bottom edge of the frame; morning light from screen right on her face. Eyes clear "
    "and fixed on him far off to the left, brows smooth, chin lifted slightly, mouth corners still, steady breath, no smile. In the first second she tucks her left hand "
    "under her right and settles them at her waist, chin lifting; Shen Yuetang, turned toward him in three-quarter profile, speaks a short Mandarin line, calmly and "
    "certainly, her lips, jaw and cheeks moving clearly with every syllable. End: her hands folded over the ring, her eyes on him."),
    motion="Folding her hand over the ring, she says she will wear it; she never meant to leave.")

# ---- 第三場：飯廳（夜） ----
shot("c25", D3, camera="Wide shot, slow push in to a medium wide", characters=["yuetang-18", "meifeng"], action_seconds=3, prompt=(
    f"{DINING}, {DINING_WIDE}; a stack of blue-and-white bowls at the near end of the table along the bottom edge of the frame. Exactly two people in the whole frame. "
    f"Middle left, seated at the window side of the table, {MF}, head bowed, a phone in her left hand with its back to the camera. At the far end of the table by the doorway, "
    f"{YT}, standing, a long-handled ladle in her bare right hand, her left hand on a lidded two-handled white porcelain soup pot that is steaming. Lin Meifeng: brows arched, "
    "eyes lowered to the phone, red lips pressed. Shen Yuetang: brows drawn tight, eyes on an empty bowl at an empty chair, lips closed. In the first second she ladles soup "
    "into one bowl and puts the ladle down, her eyes going to the empty place; Lin Meifeng's thumb swipes once on the phone. Everyone's lips stay closed. End: the ladle "
    "down, her eyes on the empty chair."),
    motion="She ladles soup, her eyes on Xiaoman's empty place, while Lin Meifeng scrolls her phone.")
shot("c26", D3, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "fubo"], ref_characters=["yuetang-18", "fubo"],
     no_set=True, clip_seconds=8, prompt=(
    f"{DINING}; {D_HER}. Exactly two people in the whole frame. Over Fu Bo's left shoulder: {FB_LFG}. On screen left, {MCU.format(who='she')}: {YT_UP}, {RING}, standing at "
    f"the far end of the table; {LAMPLIGHT} on her face. Brows squeezed together, eyes dropping once to the empty bowl below the frame and lifting to his face, mouth "
    "corners turned down, breath tight, no smile. In the first second she folds her hands at her waist; Shen Yuetang, turned to Fu Bo at screen right in three-quarter "
    "profile, speaks a short Mandarin line, low and worried, her lips, jaw and cheeks moving clearly with every syllable. Fu Bo's lips stay closed. End: her eyes on him."),
    motion="Worried, she asks Fu Bo what time Xiaoman's classes end.")
shot("c27", D3, camera="Over-the-shoulder medium close-up, locked", characters=["fubo", "yuetang-18"], ref_characters=["fubo", "yuetang-18"],
     no_set=True, clip_seconds=10, prompt=(
    f"{DINING}; {D_DOOR.format(who='him')}. Exactly two people in the whole frame. Over Shen Yuetang's right shoulder: {YT_RFG}. On screen right, {MCU.format(who='he')}: "
    f"{FB_UP}, standing by the doorway; {LAMPLIGHT}. Brows knitted, eyes dropping to the empty chair and lifting back to her face, lips tight between words, no smile. In the "
    "first second he shakes his head once; Fu Bo, turned to Shen Yuetang at screen left in three-quarter profile, speaks a short Mandarin line, worried, his lips, jaw and "
    "cheeks moving clearly with every syllable. Shen Yuetang's lips stay closed. End: his eyes on her."),
    motion="Shaking his head, Fu Bo says there is no evening class and nobody answers the phone.")
shot("c28", D3, camera="Medium close-up, locked", characters=["fubo"], no_set=True, clip_seconds=8,
     addressee="the doorway beyond the right edge of the frame, in profile", prompt=(
    f"{DINING}; behind him only an out-of-focus dark wooden cupboard and a cream wall, the doorway beyond the right edge of the frame; the camera on her side, at his left front. Exactly one person in the whole frame: {FB_UP}, standing by the doorway; {LAMPLIGHT} from "
    "screen left on his face. The same face the whole shot: brows raised, eyes turned to the doorway beyond the right edge of the frame, lips slightly parted, breath caught, no smile. In the "
    "first frame his head is already turned to the doorway off screen right; in the first second he takes one step toward it; Fu Bo speaks a short Mandarin line, his lips, jaw and cheeks "
    "moving clearly with every syllable. End: his profile toward the doorway."),
    motion="Hearing footsteps, Fu Bo steps toward the door and says Zhiyuan is back.")
shot("c29", D3, camera="Medium shot, tracking with Shen Zhiyuan from the doorway toward the table", characters=["zhiyuan"], no_set=True, action_seconds=3, prompt=(
    f"{DINING}; the edge of the doorway frame along the right edge of the picture, the dark open doorway behind him, the only doorway in view; {LAMPLIGHT}. Exactly one "
    f"person in the whole frame: {ZY_UP}, a folded white A4 sheet in his right hand with its blank back to the camera, nothing written visible. Brows pulled down hard, eyes "
    "fixed on the table toward screen left, jaw clenched, a sharp breath out through the nose, no smile. In the first frame he has just stepped through the doorway; from the "
    "first second he strides quickly toward screen left. His lips stay closed. End: halfway to the table."),
    motion="Zhiyuan strides in from the doorway with a folded sheet of paper.")
shot("c31", D3, camera="Low-angle medium close-up, slow push in", characters=["zhiyuan"], no_set=True,
     addressee="Lin Meifeng seated beyond the lower left edge of the frame, well off to the left of the lens", prompt=(
    f"{DINING}; seen from table height on Lin Meifeng's side looking up, {D_DOOR.format(who='him').replace('behind him only ', 'behind him only the dark ceiling, ')}. "
    f"Exactly one person in the whole frame: {ZY_UP}, standing at the table, a folded white sheet in his right hand at the bottom edge of the frame; {LAMPLIGHT}. Brows pulled low, "
    "eyes fixed down at her, well off to the left of the lens and below it, jaw clenched, lips tight between words, no smile. In the first second he slaps the folded sheet down on the table, blank back up, nothing written visible, presses it flat with his palm and leans forward over the table; Shen Zhiyuan, "
    "turned toward her in three-quarter profile, speaks a short Mandarin line, low and holding his anger, his lips, jaw and cheeks moving clearly with every syllable. "
    "End: leaning over the table, his eyes on her."),
    motion="Slapping the notice down, Zhiyuan tells Lin Meifeng the pharmacy will be torn down next month.")
shot("c32", D3, camera="Medium two-shot, slow push in", characters=["meifeng", "zhiyuan"], ref_characters=["meifeng", "zhiyuan"], no_set=True, clip_seconds=8,
     addressee="the phone in her left hand, her head bowed, while she answers Shen Zhiyuan who stands at the back right", prompt=(
    f"{DINING}; seen at eye level from across the table, behind them only a cream wall and one black night window. Exactly two people in the whole frame. In the left "
    f"foreground, seated at the table, {MF}, a phone in her left hand with its back to the camera, the screen unseen, a porcelain spoon in her right hand. At the back right, "
    f"standing at the corner of the table, {ZY_UP}, his right hand pressed on a folded white sheet on the table, glaring down at her; {LAMPLIGHT}. Lin Meifeng: face in three-quarter profile turned toward screen right, eyes kept down "
    "on the phone, one brow arched, one corner of her red lips pulled sideways, chin up, head never lifting. Shen Zhiyuan: brows pulled low, eyes fixed on her bowed head, "
    "jaw clenched, lips pressed thin, no smile. In the first second she stirs the spoon once in her bowl; Lin Meifeng speaks a short Mandarin line, drawling, her lips, jaw "
    "and cheeks moving clearly with every syllable, while his hand presses the sheet harder. Shen Zhiyuan's lips stay closed. End: her eyes still on the phone, his on her."),
    motion="Without looking up from her phone, Lin Meifeng says a little pharmacy can go, don't spoil dinner.")
shot("c33", D3, camera="Point-of-view insert, high-angle close-up, locked", characters=["zhiyuan"], ref_characters=[], no_set=True, no_face=True, action_seconds=3, prompt=(
    f"{DINING}. Seen from where she stands, the first frame is already tight on a man's right hand in a white coat sleeve pushed up to mid-forearm, above a "
    "small white porcelain saucer holding a little heap of red goji berries on the dark table; a blue-and-white bowl far out of focus. In the first second the hand grabs a "
    "pinch of goji berries and bounces it once at the wrist, the web between thumb and forefinger left loose, and a few berries drop back through it into the saucer. "
    "Only this one hand is in the frame, no face. End: the hand holding the pinch above the saucer."),
    motion="His loose grip lets a few goji berries slip back into the saucer.")
shot("c34", D3, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "zhiyuan"], ref_characters=["yuetang-18", "zhiyuan"],
     no_set=True, clip_seconds=8, prompt=(
    f"{DINING}; {D_HER}. Exactly two people in the whole frame. Over Shen Zhiyuan's left shoulder: {ZY_FG}. On screen left, {MCU.format(who='she')}: {YT_UP}, {RING}, "
    f"standing at the corner of the table; {LAMPLIGHT}. Eyes going from his hand up to his eyes, brows smooth and level, mouth corners still, chin slightly tucked, slow "
    "breath, no smile. In the first second she takes one step closer to the table corner and folds her hands at her waist; Shen Yuetang, turned to Shen Zhiyuan at screen "
    "right in three-quarter profile, speaks a short Mandarin line, calmly, her lips, jaw and cheeks moving clearly with every syllable. Shen Zhiyuan's lips stay closed. "
    "End: her eyes on him."),
    motion="She steps closer and tells him his grip is loose; a dose would lose a gram.")
shot("c35", D3, camera="Over-the-shoulder medium close-up, slow push in", characters=["zhiyuan", "yuetang-18"], ref_characters=["zhiyuan", "yuetang-18"],
     no_set=True, clip_seconds=8, prompt=(
    f"{DINING}; {D_DOOR.format(who='him')}. Exactly two people in the whole frame. Over Shen Yuetang's right shoulder: {YT_RFG}. On screen right, {MCU.format(who='he')}: "
    f"{ZY_UP}; in the first frame his right hand is stopped above the saucer at the bottom edge of the frame and he is already looking up at her; {LAMPLIGHT}. The same "
    "surprised face the whole shot: straight brows knitted and lifting, eyes wide and fixed on her face, lips parted between words, breath caught, no smile. In the first "
    "second he draws his hand back from the saucer and looks her up and down once; Shen Zhiyuan, turned to Shen Yuetang at screen left in three-quarter profile, speaks a "
    "short Mandarin line, low and surprised, his lips, jaw and cheeks moving clearly with every syllable. Shen Yuetang's lips stay closed. End: his eyes on her face."),
    motion="Looking at her properly for the first time, he asks how a new nanny can read his hands.")
shot("c36", D3, camera="Medium close-up, gentle push in to a medium close-up", characters=["yuetang-18"], no_set=True, clip_seconds=10,
     addressee="Shen Zhiyuan beyond the right edge of the frame, well off to the right of the lens", prompt=(
    f"{DINING}; {D_HER}; the camera on his side. Exactly one person in the whole frame, a medium close-up from the chest up: {YT_UP}, {RING}; {LAMPLIGHT} on her face. Eyes gentle and fixed on him far off to the "
    "right, brows smooth, mouth corners still, chin slightly tucked, slow breath, like teaching a child, no smile. In the first second her bare right hand, at the bottom edge "
    "of the frame below her chest, closes the web between thumb and forefinger into a tight grip and makes one pinch in the air, then folds back over her left hand at her "
    "waist; Shen Yuetang, turned toward him in three-quarter profile, speaks a short Mandarin line, slowly, her lips, jaw and cheeks moving clearly with every syllable. "
    "End: her hands folded, her eyes on him."),
    motion="Showing a tight grip in the air, she says an old hand taught her to close the web of the hand first.")
shot("c37", D3, camera="Insert, high-angle close-up, locked", characters=["zhiyuan"], ref_characters=[], no_set=True, no_face=True, action_seconds=2, prompt=(
    f"{DINING}. The first frame is already tight on a man's right hand in a white coat sleeve pushed up to mid-forearm, above the small white saucer of "
    "red goji berries, the web between thumb and forefinger already closed tight. In the first second he grabs a pinch of berries and bounces it once at the wrist; not one "
    "berry falls; the hand stays still. Only this one hand is in the frame, no face. End: the tight pinch held above the saucer."),
    motion="With the web of his hand closed, he grabs goji berries and none fall.")
shot("c38", D3, camera="Medium two-shot, locked", characters=["yuetang-18", "xiaoman"], looks={"xiaoman": "damp"}, no_set=True, action_seconds=3, prompt=(
    f"{DINING}, half an hour later; seen side-on at the doorway end of the room; in the lower left foreground a corner of the table and the lidded white porcelain soup pot, "
    f"no longer steaming; beyond the doorway it is dark; {LAMPLIGHT}. Exactly two people in the whole frame; everyone else is out of the frame to the left. On screen right, "
    f"in the first frame already standing in the doorway with her head bowed, {XM}. On screen left, in the first frame already at the doorway end of the table two steps "
    f"from her, {YT}. Shen Xiaoman: eyes lowered, lips pressed tight, chin trembling, no smile. Shen Yuetang: brows squeezed together, eyes on the girl's face and then on "
    "her empty hands and shoulders, lips closed. In the first second Shen Yuetang takes two slow, steady steps and stops in front of her; the girl's shoulders draw in. "
    "Everyone's lips stay closed. End: the two of them face to face."),
    motion="Xiaoman stands in the doorway, head bowed; Yuetang steps up and stops in front of her.")
shot("c39", D3, camera="Over-the-shoulder medium close-up, slow push in", characters=["yuetang-18", "xiaoman"], looks={"xiaoman": "damp"},
     ref_characters=["yuetang-18", "xiaoman"], no_set=True, clip_seconds=8, prompt=(
    f"{DINING}; {D_HER}. Exactly two people in the whole frame. Over Shen Xiaoman's left shoulder: {XM_FG}. On screen left, {MCU.format(who='she')}: {YT_UP}, {RING}; "
    f"{LAMPLIGHT} on her face. Brows drawn up and together, eyes on the girl's eyes and then down to her empty shoulder, mouth corners turned down, breath softened, no "
    "smile. In the first second she bends a little and brings her face closer to the girl's; Shen Yuetang, turned to Shen Xiaoman at screen right in three-quarter profile, "
    "speaks a short Mandarin line, very gently, her lips, jaw and cheeks moving clearly with every syllable. Shen Xiaoman's lips stay closed. End: her eyes on the girl."),
    motion="Bending close, she gently asks Xiaoman where her school bag is.")
shot("c40", D3, camera="Over-the-shoulder medium close-up, slow push in", characters=["xiaoman", "yuetang-18"], looks={"xiaoman": "damp"},
     ref_characters=["xiaoman", "yuetang-18"], no_set=True, prompt=(
    f"{DINING}; {D_DOOR.format(who='her')}. Exactly two people in the whole frame. Over Shen Yuetang's right shoulder: {YT_RFG}. On screen right, "
    f"{MCU.format(who='she')}: {XM}; {LAMPLIGHT}. The same face from the first frame to the last: mouth corners forced up into a shaky smile that is not a happy one, chin "
    "trembling, eyes wet and red-rimmed, brows pushed up and together. In the first frame she has just lifted her head; in the first second she looks into Shen Yuetang's eyes; "
    "Shen Xiaoman, turned to Shen Yuetang at screen left in three-quarter profile, speaks a very short Mandarin line, her voice shaking at the end, her lips, jaw and cheeks "
    "moving clearly. Shen Yuetang's lips stay closed. End: the shaky forced smile, her eyes on Shen Yuetang."),
    motion="Forcing a shaky smile, Xiaoman says the bag got lost.")
shot("c41", D3, camera="Medium two-shot, slow push in to a medium close shot", characters=["yuetang-18", "xiaoman"], looks={"xiaoman": "damp"}, no_set=True,
     action_seconds=4, prompt=(
    f"{DINING}; seen side-on, behind them only the out-of-focus dark doorway and the edge of a dark wooden cupboard; {LAMPLIGHT}. Exactly two people in the whole frame, "
    f"facing each other side-on: on screen left {YT_UP}, {RING}; on screen right {XM}. Shen Xiaoman is crying from the first frame: brows crumpled together, tears sliding from "
    "the corners of her eyes, mouth corners pulled down, lips trembling, shoulders jerking with sobs, no words. Shen Yuetang: brows drawn up and together, eyes fixed on the "
    "girl's face, lips pressed, a slow breath in, no smile. From the first frame both of Shen Yuetang's hands already rest on the girl's shoulders; in the first second the girl bows her head "
    "and sobs aloud; Shen Yuetang does not let go. Nobody speaks. End: both of her hands on the girl's shoulders, the girl crying."),
    motion="Yuetang holds Xiaoman by the shoulders as the girl breaks down crying.")

ORDER = ["camera", "characters", "looks", "ref_characters", "set", "set_variant", "no_set", "lamp", "lamp_in_frame", "lamp_quiet", "no_face",
         "action_seconds", "clip_seconds", "addressee", "prompt", "motion"]


def main():
    parsed = parse_script.parse(ROOT / "docs/videos/tai-nainai-e006/script.md")
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
        "episode": 6,
        "music": ("a low, light tension cue of muted plucked strings over a soft low drone in the morning main hall with one accent as she lists the three items, then a "
                  "gentle solo guzheng in the kitchen with one soft accent on the ring, then a warm acoustic guitar and erhu kept low and a little cold at the dinner table, "
                  "one accent on the demolition notice, falling away to silence when the girl starts to cry; restrained, no vocals"),
        "thumbnail": {"headline": "拔不下的戒指", "shot": "c24"},
        "speaker_overrides": {},
        "shots": shots,
    }
    p = ROOT / "docs/videos/tai-nainai-e006/shots-en.json"
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(p, len(shots))


if __name__ == "__main__":
    main()
