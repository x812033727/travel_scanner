"""e923 fix1: the retakes of picks-merged.tsv (s17, s31, s38), merged from review-picks-a/b by the coordinator's picker.
Same steps as e922 fix1: retake.py from live/st1 (the d1 edits of e923-live/spec.json are applied first), mkjobs.py for the
duration, the absolute picture paths, output_path and the scans, then preflight-prompts.py. Seeds 9231201/9231202, all 6 s
(158 frames = 6.583 s; s17 carries a15 4.60 s from behind, s31 a29 5.48 s from behind, s38 a36 5.52 s lip-synced).

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

refine-prep.py carries a fix shot's motion text from "never the mood. " to "One continuous shot." into its refine prompt, so
both separators stay exactly once (mkjobs.py checks it).

Why each shot (frames checked by the coordinator's picker, 2026-11-16):
- s38 (coordinator's must; A and B both RETAKE): in both takes the right third of the frame holds a second woman, sharp,
  side face with eye, nose and lips, long loose hair (1101) or a gold hairpin (1102), not the two buns; and both jump at
  5.0-5.7 s when he straightens up. Her name was in the composition ("toward Tang Xiaotang off screen right") and the gaze
  ("toward the young woman beyond the right edge"): both are gone. Now Wei Shaoqing is alone in the left two thirds, behind
  him only the plain dark wooden wall and the edge of one cream folding-screen panel, the right third plain empty wall; he is
  already leaning forward in the first frame and stays leaning the whole shot (the "lowers the fan and straightens up" beat
  is gone, so nothing invites the jump); the closed fan stays upright beside his cheek; the green jade at the front of his
  topknot and the deep sapphire-blue gold-woven robe as his portrait (the only picture; no set, as d1).
- s17 (A 1102, B RETAKE): 1102 was checked frame by frame at full size: its background is sharp, not soft: a dark wooden
  lattice door frame with paper panels at both sides of the frame for the whole shot and a hanging lantern, so it reads as a
  room opening onto the water, not a small boat in the fog; her two buns also carry one ribbon across the top of her head.
  d1 sent only the fog plate set-chuan-ye-wu-l1, a featureless blue gradient, so nothing told the model it was a boat. Now
  the set picture is the night boat itself, set-chuan-ye-l1 (a low bare wooden boat with one arched woven bamboo canopy and a
  lantern on a bamboo pole), the frame is written as what is there (拍法 18): just above her head one curved rib of dark
  split bamboo, on her left and right only drifting fog over flat dark water; her back facing straight away from us, her
  head still, every strand in just two buns. Tang's three pictures stay dropped and she stays unnamed (bible 拍法 2, 3; e918
  fix2's back-shot way).
- s31 (A 1101, B RETAKE): 1101 was checked every 0.25 s at Wei Shaoqing's face: his lips are parted in a talking smile from
  about 1.5 s to the end (the take's own babble 1.30-1.82, 2.20-2.92, 3.56-6.30 s); the longest closed-mouth stretch is
  0.0-1.25 s, and a29 needs 4.9 s of speech, so no cut holds her line without him reading as the speaker. 1102 swaps the two
  sides and shows her side face. Now Wei Shaoqing listens in silence with his lips pressed together, his eyes narrowing;
  "amused" and "his smile thins" (the cues to grin) are gone; she stays the back in the right foreground with both hands
  flat on the table, Xu Yan at her right shoulder, the folded paper folded shut with its plain blank back toward the camera.
  "worn open" (Xu Yan's coat) becomes "hanging unfastened" so the open-word scan stays clean.

Not retaken (picks-merged.tsv): every other shot has a take that a cut, an edge crop or a voice swap saves.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]


def d1(sid):
    return json.loads(json.dumps({k: v for k, v in D1SPEC[sid].items()
                                  if k in ("drop_pictures", "drop_set", "swap_pictures", "replace")}))


S = {}

S["s38"] = d1("s38")
S["s38"]["replace"] += [
    ["In the county inn guest room upstairs on a bright winter afternoon, warm light from the window on the left: medium "
     "close-up of Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread,",
     "In the county inn guest room upstairs on a bright winter afternoon, warm light from the window off screen left: from "
     "the first frame, a medium close-up of Wei Shaoqing alone, in the left two thirds of the frame, in his deep sapphire-blue "
     "brocade robe woven with gold thread,"],
    ["standing and leaning forward over the table toward Tang Xiaotang off screen right,",
     "his black hair in a neat topknot, standing and already leaning forward over the table toward the right edge of the "
     "frame, his upper body bent forward from the first frame to the last,"],
    ["his face three-quarter to screen right, close to her, never the lens;",
     "his face three-quarter to screen right, never the lens;"],
    ["behind him the bright window and the folding screen, soft.",
     "behind him only the plain dark wooden wall of the room and the edge of one plain cream folding-screen panel, soft; the "
     "right third of the frame is plain empty dark wooden wall."],
    ["He is the only person in the frame; no second copy of anyone appears.",
     "He is the only person in the frame, and the right third of the frame stays plain empty wall; no second copy of anyone "
     "appears."],
    ["his face three-quarter to screen right toward the young woman beyond the right edge of the frame, close, his eyes on her,",
     "his face three-quarter to screen right, his eyes on a point just beyond the right edge of the frame,"],
    ["after the last word he lowers the closed fan and straightens up to his full height, and the warm afternoon window light "
     "stays unchanged.",
     "after the last word he holds still, still leaning forward with the closed fan upright beside his cheek, and the warm "
     "afternoon light stays unchanged."],
]
S["s38"]["duration_seconds"] = 6

S["s17"] = d1("s17")
S["s17"]["swap_pictures"] = {"set-dukou-l2.png": "set-chuan-ye-l1.png"}
S["s17"]["replace"] += [
    ["On a small boat out on the water off the ferry landing of Liuxi at midnight, thick cold grey-blue fog all around: medium "
     "shot from close behind one young woman seen only from behind, appearing only once:",
     "On the small low wooden river boat with bare sides from the picture, out on the water off the ferry landing of Liuxi at "
     "midnight, thick cold grey-blue fog all around: from the first frame, a medium shot from close behind one young woman "
     "seen only from behind, appearing only once:"],
    ["the back of her head with all of her black hair gathered up into two round buns set high on her head,",
     "the back of her head with every strand of her black hair combed smooth and gathered up into just two round buns set "
     "high on her head, one bun on each side,"],
    ["sitting on the boards at the right side of the boat,",
     "sitting on the bare wooden boards of the boat, just above her head one curved rib of dark split bamboo at the edge of "
     "the boat's woven canopy,"],
    ["beyond her only the low wooden edge of the boat, the flat dark water and the thick grey fog.",
     "beyond her only the low wooden edge of the boat, the flat dark water and the thick grey fog, and on her left and on her "
     "right only drifting fog over the flat dark water."],
    ["keeps her head still, the back of her head toward us the whole shot;",
     "keeps her head still, facing straight away from us, the back of her head toward us the whole shot;"],
]
S["s17"]["duration_seconds"] = 6

S["s31"] = d1("s31")
S["s31"]["replace"] += [
    ["coat worn open over", "coat hanging unfastened over"],
    ["one sheet of thick smooth cream paper folded in half, its blank outside facing up, smooth and empty from the first "
     "frame,",
     "one sheet of thick opaque cream paper folded in half and folded shut, its plain blank back facing up toward the camera, "
     "smooth and empty from the first frame to the last,"],
    ["his face three-quarter to screen right looking up at her, never the lens; amused, weighing her: eyes narrowed, lips "
     "closed;",
     "his face three-quarter to screen right looking up at her, never the lens; listening in silence, weighing her: eyes "
     "narrowed, his lips pressed together in one still line;"],
    ["his smile thins, and the warm afternoon window light stays unchanged.",
     "Wei Shaoqing sits perfectly still and listens, his eyes slowly narrowing, his lips pressed together, and the warm "
     "afternoon window light stays unchanged."],
]
S["s31"]["duration_seconds"] = 6

(HERE / "spec.json").write_text(json.dumps({"seeds": [9231201, 9231202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
