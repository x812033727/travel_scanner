"""e915 fix1: the retakes of picks-merged.tsv (s08, s10, s21, s25, s26, s41), the union of review-picks-a/b plus s10
(both takes laugh; the coordinator added it). Same steps as e914 fix1: retake.py from live/st1 (the d1 edits of
e915-live/spec.json are applied first), mkjobs.py for the duration, the picture swaps and output_path,
preflight-prompts.py. Seeds 9151201/9151202. Written under bible 拍法 18: backgrounds and props written as what is there,
no negative nouns; no smile written as concrete actions; hands and props placed in the first-frame composition.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

"swap_pictures" is read by mkjobs.py, not retake.py: it replaces a sent picture by file name after retake.py has
written the job (retake.py cannot add a picture, and a job may not be left with none: route-a.md, e908 fix1). The prompt
text already names the new picture, so prompt_sha256 does not change.

Why each shot:
- s08 (picks-b RETAKE, picks-a kept 1102 with start 0.750): both takes open on the empty work shed and hard-cut to the
  insert inside the clip (1101 at 1.75 s, 1102 at 0.71 s), and neither drew a plough (1101 an arrow, a straight bar and
  saw teeth; 1102 a bent-arrow sign). The shed set picture is what the model opened on, so it is not sent (owner: 不送工棚圖);
  a job needs one picture, so xuyan-angle-a-l1 (his serious side view, the blue-grey sleeve) takes its place, named only
  as the owner of the sleeve and hands. The shed description before the insert goes; the insert opens on the paper.
  The drawing is written as four strokes in order: the bow-curved beam, the flat sole, the small leaf-shaped share, the
  handle at the back. "draws a plough" (a noun the model drew as an arrow sign) is replaced by those shapes. Static
  camera (the push gave the model room to travel). 6 s (a10 5.48 s).
- s10 (coordinator; picks-a 1101 and picks-b 1102 both laugh with the teeth through the line; the script says one brow
  up, no smile): "amused" is the word that became the grin; the face is written as what it does (one brow raised high,
  eyes narrowed and steady, mouth corners level, lips pressed flat between words), and after the last word he holds a
  concrete beat (presses his lips flat, a short breath out through the nose, taps the paper tube once on his palm).
  The paper is a tight tube under his arm from the first frame (1101 opened a sheet of fake writing at 0-0.75 s, 1102
  grew the roll in his hand at 1.5 s). Kept at 6 s (a11 5.08 s; 5 s buys only 5.17 s of picture).
- s21 (both): the share came out as a saw-toothed axe blade or a crescent blade taller than a man, and they walked
  toward the lens. The plough is written whole as plain brown wood with one palm-sized smooth rounded leaf-shaped iron
  share fitted on the tip of the sole, "the only metal on the whole plough"; the camera is side-on and they walk in
  side view from screen right to screen left and set the sole flat on the earth. 8 s as st1 (several beats).
- s25 (picks-a RETAKE, picks-b kept 1101): in all four takes she walks beside the plough holding one handle like a cart
  (1101) or in front of it pulling (1102), and the whole field is already furrowed, so the before/after of the episode
  is gone. The set picture set-qiutian-l2 itself is a field of ridged rows (the rows read as furrows in s13 s19 s20 s24
  s25), so it is not sent here (drop_set; her portrait stays). The field is written as one flat level surface of hard
  dark earth with short pale stubble all over, the only turned soil one fresh furrow behind her; she walks directly
  behind the plough, both hands on its one handle at her waist, arms straight, pushing it ahead; the share bites and a
  thick wave of soil curls off it. 8 s.
- s26 (picks-b RETAKE, picks-a kept 1102): the far figure is pink with two buns (1102, reads as Tang Xiaotang) or there
  is an empty plough and nobody (1101). Qin Shuang's portrait replaces the ridged set picture (swap), and the far figure
  is written as her by costume: dark brown cross-collared jacket, black trousers and boots, high ponytail, alone behind
  the plough pushing, the only person out in the field. The foreground girl is "the young woman with the pink ribbons".
  6 s (a25 3.96 s).
- s41 (both): Lai San holds Tang Xiaotang's gold abacus in all four takes (reads as him taking her money), and in 1102
  the log is behind him. The abacus is written at her own waist under her own right hand for the whole shot; he stands
  behind the log that lies level between them at his waist, both forearms on it, both hands open and empty on the bark.
  "belts and waists plain" (it contradicted the abacus at her waist) goes. 6 s (a39 4.12 s).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
REFS = "/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"

PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC = "The camera holds a static shot."
FIELD_OLD = ("a wide harvested rice field, flat and level, hard dry dark earth never yet ploughed, short cut rice stubble "
             "standing in straight even rows on the flat ground,")
FIELD_NEW = ("a wide harvested rice field lying perfectly flat, one smooth level surface of hard dry dark earth with short pale "
             "cut rice stubble dotted evenly all over it like a close-cropped carpet,")
PLOUGH = ("one new curved-beam plough made of plain brown wood: one long smooth wooden beam bent in a gentle arc like a drawn "
          "bow, a short flat wooden sole at its low front end, one smooth polished wooden handle rising at the back, and "
          "fitted snugly on the sole's front tip one small leaf-shaped dark iron ploughshare no bigger than a man's palm, "
          "rounded and smooth all round like a leaf, the only metal on the whole plough")


def shot(sid, extra, dur=None, **more):
    s = {k: v for k, v in D1SPEC[sid].items() if k != "replace"}
    s["replace"] = D1SPEC[sid].get("replace", []) + extra
    if dur:
        s["duration_seconds"] = dur
    s.update(more)
    return s


S = {
 "s08": shot("s08", [
   ["the location shown in <Picture 1> is the set, keeping its layout and props. Initial composition: In the night work "
    "shed just before dawn, lit only by one short candle burnt down almost to a stub on the old table, its small yellow "
    "flame and the cold grey-blue sky in the open right side; the posts and the earthen walls bare, the middle timber post "
    "carrying only one sheet of plain paper pinned flat with one wooden peg, thick and opaque, completely blank; nothing "
    "leaning against the walls: insert close-up looking straight down, the shot opens directly on one torn-cornered sheet "
    "of plain scrap paper, blank and matte lying flat on the old wooden table from its very first frame, candlelight on it; "
    "one young man's right hand, his blue-grey sleeve tied back with a cloth strip, holding one short black stick of "
    "charcoal on the paper; only the hand, the sleeve, the paper and the wood are in the frame. the charcoal draws a plough "
    "seen from the side in a few thick black strokes: one long beam curved like a drawn bow, a short flat sole and a "
    "pointed share; only those few strokes are on the sheet, the rest of it plain and blank, and the one small candle "
    "flame and the cold grey-blue before-dawn light stay unchanged.",
    "the faded blue-grey cotton sleeve in this shot is the robe of the young man shown in <Picture 1>, seen only as his "
    "two hands and sleeves. Initial composition: insert close-up looking straight down at an old dark wooden tabletop lit "
    "by warm yellow candlelight from screen right; the shot opens directly on one torn-cornered sheet of plain scrap "
    "paper, blank and matte, lying flat and filling the middle of the frame from its very first frame; one young man's "
    "right hand reaches in from the bottom edge, his blue-grey sleeve tied back above the wrist with a cloth strip, "
    "holding one short black stick of charcoal with its tip on the paper, his left hand resting flat on the paper's lower "
    "left corner; the paper, his two hands, the sleeves and the dark wood fill the frame from the first frame to the "
    "last. The charcoal draws, in slow thick black strokes one after another from left to right, the side view of a farm "
    "plough: first one long wooden beam bending upward in a smooth gentle arc like a drawn bow, then under its low front "
    "end a short straight flat sole lying level, then at the sole's front tip one small leaf-shaped pointed share, then "
    "one short handle rising at the back of the sole; the drawing ends as those four simple outlines on the plain sheet, "
    "the rest of the paper blank and matte, and the warm candlelight from the right stays unchanged."],
   [PUSH, STATIC]], 6, swap_pictures={"set-gongpeng-ye-l2.png": f"{REFS}/angles/xuyan-angle-a-l1.png"}),
 "s10": shot("s10", [
   ["one torn-cornered sheet of plain paper rolled up loosely, its outside blank tucked under his left arm,",
    "one sheet of plain paper rolled into a tight tube as long as his forearm, its outside blank and matte, tucked under "
    "his left arm from the first frame,"],
   ["amused: one brow cocked, eyes narrowed, lips moving between words;",
    "dry and probing: one brow raised high, eyes narrowed and steady on her, the corners of his mouth held level, lips "
    "moving between words and pressed flat between them;"],
   ["Xu Yan takes a few steps onto the threshing ground and moves the rolled sheet from under his left arm into his right "
    "hand as he speaks;",
    "Xu Yan takes one step onto the threshing ground and stops, draws the rolled paper tube out from under his left arm "
    "into his right hand without unrolling it, and tips his chin once toward her as he speaks;"],
   ["after the last word the lips press flat and the jaw sets, the brows stay drawn, held to the last frame,",
    "after the last word he presses his lips flat, lets one short breath out through his nose and taps the paper tube "
    "once against his left palm, his raised brow staying up and his eyes steady on her to the last frame,"]], 6),
 "s21": shot("s21", [
   [FIELD_OLD, FIELD_NEW],
   ["wide shot following them from right to left past a hanging branch of yellow willow leaves in the foreground: coming "
    "down off the raised ridge on the right into the field, one behind the other,",
    "wide shot, the camera side-on to them and tracking with them from screen right to screen left past a hanging branch "
    "of yellow willow leaves in the foreground: in clean side view, walking from screen right toward screen left and "
    "stepping down off the raised ridge on the right into the field, one behind the other,"],
   ["carrying one new curved-beam plough: one wooden beam curved like a drawn bow, a short wooden sole, one new black iron "
    "ploughshare and one smooth polished wooden handle between them on their shoulders,",
    "carrying between them on their shoulders, level and seen side-on, " + PLOUGH + ","],
   ["the two of them step down off the ridge into the field and lower the plough onto the dark earth;",
    "the two of them walk on toward screen left, step down off the ridge into the field, lower the plough together and "
    "set its flat sole level on the dark earth, the small leaf-shaped iron tip resting on the soil;"]], 8),
 "s25": shot("s25", [
   [FIELD_OLD, FIELD_NEW],
   ["low-angle wide shot moving alongside the new furrow, the whole action kept in the frame:",
    "low-angle wide shot from the side, the camera low at the edge of the field tracking alongside her, the whole action "
    "kept in the frame: ahead of her on screen left the field lies flat and level, short pale stubble standing on hard "
    "dark earth; behind her on screen right runs one single fresh dark furrow she has just cut, the only turned soil in "
    "the whole field;"],
   ["behind one new curved-beam plough: one wooden beam curved like a drawn bow, a short wooden sole, one new black iron "
    "ploughshare and one smooth polished wooden handle, both bare hands gripping its polished wooden handle,",
    "walking directly behind one new curved-beam plough, the plough out in front of her body toward screen left: one long "
    "wooden beam curved like a drawn bow, a short flat wooden sole, one small smooth leaf-shaped dark iron share as big as "
    "a palm on the sole's tip sunk into the earth, and one smooth polished wooden handle rising at the back toward her; "
    "she leans her weight forward, both bare hands gripping that one handle at her waist, arms straight, pushing the "
    "plough ahead of her,"],
   ["in front of the plough only bare dark earth, she alone pushes it;",
    "in front of the plough the flat stubble field, short pale stalks on hard dark earth; she is the only one at the "
    "plough;"],
   ["Qin Shuang drives the plough forward; the black iron share bites into the dark earth and one long wave of soil rolls "
    "over beside it as she walks on step by step toward screen left;",
    "Qin Shuang pushes the plough forward with both hands on its handle; its small iron share bites into the hard earth "
    "and a thick wave of dark soil curls up off it and rolls over to the side in one long unbroken ribbon as she drives "
    "it on step by step toward screen left, the fresh furrow growing behind her;"]], 8, drop_set=True),
 "s26": shot("s26", [
   ["The location shown in <Picture 4> is the set, keeping its layout and props.",
    "Qin Shuang shown in <Picture 4> keeps exactly the same face, hair and costume as the picture: a tall athletic young "
    "woman, sleek high ponytail tied with black cord, a fitted dark brown cotton short jacket crossed at the collar and "
    "cinched with a wide leather belt over fitted black trousers and black leather boots; she appears only once, small "
    "and far off out in the field."],
   [FIELD_OLD, FIELD_NEW],
   ["below in the field far ahead on screen left, small, one young woman alone pushing one new curved-beam plough: one "
    "wooden beam curved like a drawn bow, a short wooden sole, one new black iron ploughshare and one smooth polished "
    "wooden handle along a long fresh furrow;",
    "below in the field far ahead on screen left, small but clear in the middle distance, Qin Shuang in her dark brown "
    "cross-collared short jacket, wide leather belt, black trousers and black leather boots, her long black high ponytail "
    "swinging, walks alone behind one new curved-beam plough with a long wooden beam curved like a drawn bow, both hands "
    "on its wooden handle, pushing it forward, a dark wave of fresh soil curling off its small iron share and one single "
    "long fresh furrow trailing behind her across the flat stubble; she is the only person out in the field;"],
   ["the young woman tugs the man's sleeve twice",
    "the young woman with the pink ribbons tugs the man's sleeve twice"]], 6,
   swap_pictures={"set-qiutian-l2.png": f"{REFS}/qinshuang-portrait-l1.png"}),
 "s41": shot("s41", [
   ["the small gold abacus hanging at her waist, standing in the left foreground, her right hand (on screen right) at the "
    "small gold abacus at her waist;",
    "standing in the left foreground, a small gold abacus hanging at her own waist on her right side, her own right hand "
    "(on screen right) resting on that abacus at her waist, the abacus and her hand staying at her waist the whole shot;"],
   ["facing us a few steps away, a little right of the middle, behind the thick log barrier, Lai San,",
    "facing us a few steps away, a little right of the middle, standing behind the thick rough log barrier, the log lying "
    "level across the frame between him and her at the height of his waist, Lai San,"],
   ["slouching with one shoulder dropped, framed from the waist up",
    "slouching with one shoulder dropped, both his forearms resting on top of the log and both his hands lying open and "
    "empty on the bark, fingers spread, framed from the waist up"],
   ["their hands hold only what is described here, belts and waists plain;",
    "his hands stay open and empty on the log the whole shot, and the abacus stays at her waist under her own hand;"],
   ["the young woman flicks two beads of the small gold abacus with her right hand (on screen right); Lai San's grin "
    "widens a little;",
    "the young woman flicks two beads of the abacus at her own waist with her right hand (on screen right); Lai San stays "
    "where he is behind the log, his hands flat on the bark, and his grin widens a little;"]], 6),
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9151201, 9151202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
