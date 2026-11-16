"""e922 fix1: the retakes of picks-merged.tsv (s09, s32), merged from review-picks-a/b by the coordinator's picker.
Same steps as e921 fix1: retake.py from live/st1 (the d1 edits of e922-live/spec.json are applied first), mkjobs.py for the
duration, the absolute picture paths, output_path and the scans, then preflight-prompts.py. Seeds 9221201/9221202, both 6 s
(158 frames = 6.583 s; s09 carries a07 3.36 s from behind, s32 a28 4.28 s lip-synced).

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json
    python3 -I mkjobs.py <live>/fix1
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json

refine-prep.py carries a fix shot's motion text from "never the mood. " to "One continuous shot." into its refine prompt,
so both separators stay exactly once (mkjobs.py checks it) and the motion part repeats what the refine pass must keep
(s09: one back, his lips pressed together; s32: the paper folded shut, the lamplight).

Why each shot (frames checked by the coordinator's picker, 2026-11-16):
- s32 (coordinator's must; A 1101, B RETAKE): in both takes the paper in Xu Yan's hand at the lower right shows clear rows
  of fake writing for the whole shot, and 1102 also hangs a bead curtain and string lights and swaps the two women. Now the
  first frame writes everything: the door frame soft in the left foreground, Qin Shuang in the left half against it, A-ling
  in the middle a step behind her right shoulder (script c32 and the room picture: the door is in the left wall), the dark
  corridor behind them, and at the right edge only a young man's hand holding one sheet of thick opaque plain paper folded
  in three and folded shut, its plain back to the camera (bible 拍法 7, 17, 27; unnamed, no picture, 拍法 2). The night is
  lit only by the script's oil lamp (c29 put it on her little table, off screen right): every "candlelight" is gone, and the
  background is written as what is there (拍法 18), so nothing invites the curtain or the bulbs.
- s09 (A 1102 cut from 2.500, B RETAKE): 1101 has two Tang Xiaotangs (one at each side; a crop cannot keep Wei Shaoqing and
  lose the second); 1102 cut from 2.500 does hold a07 (4.083 s for 2.79 s of speech) but Wei Shaoqing, sharp and facing us,
  opens his lips again at 4.3-4.6 s and 5.4 s with the take's own babble (4.39-4.86, 5.50-6.19 s), right under her line,
  so he reads as the speaker; and her hair grows two extra braids. Retaken: one back only, every strand gathered into the two
  buns, her right fist on the pouch neck at the lower right; Wei Shaoqing smaller, beyond her in the left half, out of focus
  in a shallow depth of field, lips pressed together; "he lets the question hang" (a cue to speak) is gone. Tang's three
  pictures stay dropped and her identity sentence stays out (d1, bible 拍法 3; e918 fix2's back-shot way); Wei Shaoqing keeps
  his portrait (he is in the frame, facing us).

Not retaken (picks-merged.tsv): s19 (the long abacus is the series prop, bible 拍法 20 corrected), s33 (cut from 1.708 past
the pink half face, a29 fits), and everything the coordinator accepted.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]


def d1(sid):
    return json.loads(json.dumps({k: v for k, v in D1SPEC[sid].items()
                                  if k in ("drop_pictures", "drop_set", "swap_pictures", "replace")}))


PAPER = ("one sheet of thick opaque plain paper folded in three and folded shut, its plain back toward the camera, a smooth "
         "empty cream surface")
S = {}

S["s09"] = d1("s09")
S["s09"]["replace"] += [
    ["close over-the-shoulder shot from close behind one young woman seen only from behind, appearing only once: the back of "
     "her head with all of her black hair gathered up into two round buns set high on her head, a short pink silk ribbon "
     "wrapped around each bun, the nape of her neck bare above a pink inner collar,",
     "from the first frame, a close over-the-shoulder shot from close behind one young woman seen only from behind, appearing "
     "only once, the focus sharp on her, her back filling the right half of the frame: the back of her head with every strand "
     "of her black hair combed smooth and gathered up into just two round buns set high on her head, a short pink silk ribbon "
     "wrapped tight around each bun, the nape and the back of her neck bare and smooth above a pink inner collar,"],
    ["facing us beyond her shoulder, soft, Wei Shaoqing,",
     "facing us beyond her shoulder in the left half of the frame, smaller, softly blurred and out of focus in the shallow "
     "depth of field, Wei Shaoqing,"],
    ["sitting back on the bench under the window, framed from the chest up,",
     "sitting back on the bench under the window, framed from the waist up,"],
    ["waiting: eyes half closed, lips closed;",
     "patient and silent: eyes half closed, his lips pressed together in one still line;"],
    ["he lets the question hang, unmoving,",
     "he sits back perfectly still and silent, out of focus, watching her with his lips pressed together,"],
]
S["s09"]["duration_seconds"] = 6

S["s32"] = d1("s32")
S["s32"]["replace"] += [
    ["In the first bedroom of the Xu farmhouse late at night, dim warm candlelight against rough plaster walls: medium shot at "
     "the open door in the left wall, the dark edge of the door frame in the soft left foreground: Qin Shuang,",
     "In the first bedroom of the Xu farmhouse late at night, the room lit only by one small clay oil lamp burning on a low "
     "table off screen right, its low warm glow on rough plaster walls: from the first frame, a medium shot at the open door "
     "in the left wall, the dark edge of the wooden door frame in the soft left foreground, behind the two women the dark "
     "corridor beyond the doorway, its plain plaster wall and dark wooden beams deep in shadow: in the left half of the frame "
     "Qin Shuang,"],
    ["just behind her shoulder A-ling,",
     "in the middle of the frame, a step behind her right shoulder, A-ling,"],
    ["warm candlelight on both faces; their hands hold only what is described here; exactly two people.",
     "the warm light of the oil lamp off screen right on both faces; at the right edge of the frame, close to the camera and "
     "soft, one young man's hand in a faded blue-grey cotton sleeve holds up " + PAPER + " from the first frame to the last; "
     "their hands hold only what is described here; exactly two faces, the two women."],
    ["Only these 2 people are in the frame; no second copy of anyone appears.",
     "Only these 2 people are in the frame, and at the right edge only the young man's hand with the folded paper; no second "
     "copy of anyone appears."],
    ["Qin Shuang glances at the paper in his hands beyond the right edge of the frame,",
     "Qin Shuang glances at the folded paper in the young man's hand at the right edge of the frame,"],
    ["and the low warm candlelight stays unchanged.",
     "the paper stays folded shut in his hand with its plain back toward the camera, and the low warm lamplight stays "
     "unchanged."],
]
S["s32"]["duration_seconds"] = 6

(HERE / "spec.json").write_text(json.dumps({"seeds": [9221201, 9221202], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json")
