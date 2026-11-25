"""e919 fix1: the retakes of picks-merged.tsv (s09, s16, s34), merged from review-picks-a/b by the coordinator's picker.
Same steps as e918 fix1: retake.py from live/st1 (the d1 edits of e919-live/spec.json are applied first), mkjobs.py for
the duration, the absolute picture paths, output_path and the bible 拍法 18 negative-noun scan, then preflight-prompts.py.
Seeds 9191201/9191202. Written under bible 拍法 15-18: what is in the frame written as what is there, no negative nouns;
hands and props placed in the first-frame composition; no smile written as concrete actions.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

Why each shot (frames checked by the coordinator's picker, 2026-11-16):
- s09 (picks-a and picks-b both RETAKE): in both takes white, clean fingers show in the gap between his joined sleeves
  (1101 0-5.2 s, 1102 the whole shot). The line is 「老夫的手，憑什麼給你看？」 and his hands are already red (s12), so
  white fingers break both the plot and s12; the line sits in the middle, nothing can be cut away. d1 wrote "framed from
  the chest up ... his joined sleeves below the bottom edge of the frame" and the model framed to the belly anyway: the
  sleeves-joined sentence drew them. So: framed from the upper chest up, the bottom edge across his chest well above the
  elbows, the frame's contents listed (face, neck, white inner collar, the top of the robe, the cap), "the only skin in
  the frame is his face and neck"; the sleeves-and-hands clauses are gone from the identity and the composition; the
  sleeve tug becomes a shoulder hunch. Pictures as d1 (portrait + angle-a: s15, s17, s19 kept a smooth cap with them).
- s16 (picks-a 1102 / picks-b 1101; the coordinator retakes it): both takes draw a whole clean round cage on a big
  brass dish; the evidence in court has to be the burnt broken ring with the thumbnail-sized square-holed copper plate
  that e917 s39/s40 showed. d1 already wrote "one charred lantern frame: a ring of blackened bamboo ribs ...": the word
  lantern and the ribs drew a cage. So the word lantern is gone from the English (the spoken line keeps 燈籠骨架), the
  prop is written as one flat broken hoop of charred bamboo strips split open at one side with the small plate nailed at
  its bottom. 1101's head left the frame when he stood up at 5.7 s and the last words were only legs: now he stays on
  one knee to the last frame, holds the hoop up at chest height for the line, the camera holds still.
- s34 (picks-b RETAKE, picks-a kept 1102): both takes open the mouth from the first frame and speak 「鴨子治蝗」 at
  1.45-4.35 s, under the system's a34 (0-3.84 s); the system voice would sit on his moving lips and cannot be cut
  apart. Checked 1102: mouth open 0-5 s, speaking from 1.45 s, so B is right. So: the back of his right hand over his
  mouth from the first frame to the last, silent laughter in the eyes and shaking shoulders; his line plays from the
  recording a35 (the bible allows the laugh in this shot). s35 opens with his fist at his mouth, so the hand carries over.

Not retaken (judged, see picks-merged.tsv):
- s04: 1101's long black band behind the cap shows 0-2.0 s only (the man then turns out of the right edge); the line
  starts at 3.0 s, so start@2.250 drops it and keeps 4.33 s for a04 (4.24 s).
- s27: the red pole with the gold tip stands in the background through the whole take; a crop that removes it either
  loses the pink hand's tug or cuts the top of his head (tried 1.26x at three heights). It is soft and a court-hall
  ceremonial pole is in period, so it stays; post may paint it out. The round skin disc on his chest (s27, s33, s34) comes
  from the d1 pouch sentence and the reference pictures' shoulder hole: a retake would keep both; post.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]


def shot(sid, extra, dur, keep=("drop_pictures", "drop_set", "swap_pictures")):
    s = {k: v for k, v in D1SPEC[sid].items() if k in keep}
    s["replace"] = D1SPEC[sid].get("replace", []) + extra
    s["duration_seconds"] = dur
    return s


CAMERA_PUSH = "The camera pushes in with small amplitude at slow speed."

S = {
 "s09": shot("s09", [
   [", long wide sleeves, his hands hidden inside them; the location shown in <Picture 3>",
    "; the location shown in <Picture 3>"],
   ["close-up of Qian Yuanwai, in his dark gold silk round-collared robe with roundel patterns and long wide sleeves, a white "
    "inner collar at his neck, and his tall round smooth black cap, plain and smooth all the way round down to its rim, "
    "kneeling, framed from the chest up with space above his cap, both his hands pushed deep inside his long wide dark gold "
    "sleeves, the cuffs hanging well past his fingertips, the two sleeves joined in front of his belly, his hands hidden "
    "inside them the whole time, his joined sleeves below the bottom edge of the frame, his face three-quarter to screen "
    "left toward Xu Yan off screen left, never the lens;",
    "close-up of Qian Yuanwai framed from the upper chest up with space above his cap, the bottom edge of the frame cutting "
    "straight across his chest well above his elbows from the first frame to the last, so both his arms stay below the "
    "frame for the whole shot; in the frame only his round face, his neck, the white inner collar, the top of his dark gold "
    "silk round-collared robe with roundel patterns across his shoulders and upper chest, and his tall round smooth black "
    "cap, plain and smooth all the way round down to its rim; the only skin in the frame is his face and neck; his face "
    "three-quarter to screen left toward Xu Yan off screen left, never the lens;"],
   ["then his chin jerks up and he pulls his joined sleeves tighter in against his belly below the frame;",
    "then his chin jerks up and he draws both shoulders up and in toward his neck in one quick hunch, as if pulling his "
    "sleeves in tighter below the frame, the bottom edge of the frame staying across his upper chest;"],
 ], 6),
 "s16": shot("s16", [
   ["crouching on screen left, framed full length with clear space above his head,",
    "kneeling on one knee on screen left, framed full length with clear space above his head, his head in the upper part of "
    "the frame,"],
   ["Xu Yan opens the blue cloth and lifts out with both hands one charred lantern frame: a ring of blackened bamboo ribs two "
    "hands wide, its paper burnt away to a few brown scorched edges, and at its base one small plain copper plate the size of "
    "a thumbnail, far smaller than his palm, a raised ring round a small square hole, smooth and plain; he sets it down on "
    "the stone floor in the middle of the frame and stands up beside it, speaking; after the last word he stands still "
    "beside it, his eyes toward screen right,",
    "Xu Yan opens the blue cloth and lifts out with both hands what is left after the fire: one single flat hoop of charred "
    "bamboo strips two hands wide, thin like a bracelet, burnt black, split open at one side where the fire ate through it, a "
    "few scorched brown paper edges clinging to it, and nailed to the bottom of the hoop one small plain copper plate the "
    "size of his thumbnail, much smaller than his palm, with a small square hole in its middle; still on one knee, he holds "
    "the broken hoop up at chest height in front of him in both hands, the small copper plate turned toward screen right, "
    "speaking; after the last word he stays on one knee holding it up, his head in the upper part of the frame, his eyes "
    "toward screen right,"],
   [CAMERA_PUSH, "The camera holds still on this framing from the first frame to the last."],
 ], 8),
 "s34": shot("s34", [
   ["his eyes on a point in the air in front of him, never the lens; amazed: eyes wide, brows high, lips closed;",
    "his eyes on a point in the air in front of him, never the lens; the back of his right hand already pressed flat over "
    "his mouth from the first frame, his right elbow bent in front of his chest, his fingers resting on his left cheek; "
    "amazed: eyes wide, brows high above his hand;"],
   ["Xu Yan speaks a short Mandarin line, 「鴨子……治蝗？鴨子能吃蝗蟲？」, his lips, jaw and cheeks moving clearly with every "
    "syllable in natural talking mouth shapes, his face three-quarter to screen left, his eyes on a point in the air in front "
    "of him, never looking at the camera; For the first four seconds Xu Yan's lips stay pressed together while his eyes grow "
    "wider; from the fourth to the eighth second he bursts out laughing and speaks the line through the laugh; from the "
    "eighth second he claps the back of his right hand over his mouth and keeps it there to the last frame, his eyes still "
    "creased,",
    "Xu Yan keeps the back of his right hand pressed over his mouth from the first frame to the last, his face three-quarter "
    "to screen left, his eyes on a point in the air in front of him, never looking at the camera; for the first three "
    "seconds his eyes grow wider and wider above his hand; then his eyes crease with laughter and his shoulders begin to "
    "shake with silent laughter behind his hand, harder and harder, his head dipping once toward his hand; to the last frame "
    "his hand stays over his mouth, his eyes creased, his shoulders shaking; he says nothing aloud in this shot: his mouth "
    "stays behind his hand the whole time, no talking, no mouthing words,"],
 ], 10),
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9191201, 9191202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
