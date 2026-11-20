"""e933 fix3: s05 (the beam hook) and s30 (the wheel before the gate), two seeds each. NOT RUN: written and checked
(mkjobs.py, preflight-prompts.py, check_manifest.py, h3r.sh check), nothing is sent. Why in plan.md.

    python3 -I mkspec.py                       # -> spec.json (s05 on fix1 9331212, s30 on d1 9331101)
    python3 -I mkjobs.py <live>/fix3           # -> <live>/fix3/prompts/*.txt, retake.json, colab-jobs.json (4 jobs, 32 s)

The two cut reviews (../cut-review.md medium 2-3 and minor 2, ../cut-review-2.md medium 2 and minor 2):
- s05 (fix1 9331212, picked): Carpenter Shi stands with both feet on the altar table top between the censer and the tablets,
  the ladder beside him and nobody on it, while s07's very next line is 「別砸了供桌」; and the beam is a dark round log wound
  with hemp rope, where s07 (fix1 9331212) carries a pale squared timber. Base: the fix1 9331212 prompt exactly as sent.
  Kept: the whole beam in the frame, the rope wrapped on the beam, four on the rope, the rope apart from the ladder, the
  shouted line with NOSMILE. Changed: the beam written as s07's (one long squared beam of pale weathered light-brown wood,
  four flat sides), in the place sentence too (the set picture's beam is dark: risk in plan.md); Carpenter Shi standing with
  both feet on the flagstones just left of the altar table's left end, his raised arm pointing up at the coil; the ladder
  standing by itself; the table top holding only the tablets, the censer and the two candles; all seven on the flagstones.
- s30 (d1 9331101, picked): the wheel turns before the gate is opened (the rim moves about 340 px, the paddle carries his
  hand down), so s34's 「水推不動它」 makes no sense. Base: the d1 9331101 prompt exactly as sent. The result is written into
  the first sentence of the composition (the wheel dead still from the first frame to the last, every paddle, spoke and
  wedge in the same place), repeated at his hand, at the near rim and in the action; the slow push becomes a static camera
  (a push changes the wheel's perspective and reads as turning); his look and the closed mouth as before (silent clip:
  the system line a31 and the inner voice a32 are laid over it, about 7.7 s from c0.15).
Seconds as bought before: s05 6 s (d1 and fix1), s30 10 s (d1). Seeds 9331411/9331412 (s05), 9331413/9331414 (s30).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
LIVE = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e933-dh/runpod/live")
BASES = {"s05": ("fix1", 9331212), "s30": ("d1", 9331101)}
SEEDS = {"s05": [9331411, 9331412], "s30": [9331413, 9331414]}
DUR = {"s05": 6, "s30": 10}


def text(sid):
    run, seed = BASES[sid]
    return (LIVE / run / "prompts" / f"ref-{sid}-{seed}.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert text(sid).count(s) == 1, (sid, s[:70])
    return s


BEAM = "one long squared beam of pale weathered light-brown wood, its four flat sides plain and smooth, with square edges"

S05 = [
    [once("s05", "the thick dark main beam across the top of the back wall,"),
     f"the main beam across the top of the back wall, {BEAM},"],
    [once("s05", "low-angle wide shot from near the flagstones looking up, the whole thick dark main beam across the upper "
                 "part of the frame from the first frame to the last:"),
     "low-angle wide shot from near the flagstones looking up, the whole main beam across the upper part of the frame from "
     f"the first frame to the last, {BEAM}:"],
    [once("s05", "one plain wooden ladder leaning against the back wall under the right end of the beam, and near its top "
                 "Carpenter Shi, in his faded light tan cross-collared short work jacket with the sleeves rolled up and his "
                 "worn brown leather apron, one plain wooden stick through his grey topknot, framed full figure, already up "
                 "on the ladder from the first frame, both hands on a coil of one thick, soft hemp rope wrapped twice round "
                 "the right end of the beam just above his head, pulling its knot tight, his face turned down over his "
                 "shoulder toward the people below at the left, never the lens;"),
     "one plain wooden ladder leaning against the back wall under the right end of the beam, standing by itself; the long "
     "altar table against the back wall, its top holding only the five tablets, the bronze censer and the two candles; on "
     "the grey flagstones just to the left of the left end of the altar table Carpenter Shi, in his faded light tan "
     "cross-collared short work jacket with the sleeves rolled up and his worn brown leather apron, one plain wooden stick "
     "through his grey topknot, framed full figure, standing with both feet flat on the grey flagstones from the first frame "
     "to the last, his head well below the beam, his right arm raised and pointing up at a coil of one thick, soft hemp rope "
     "wrapped twice round the right end of the beam, his face turned toward the four men at the left, never the lens;"],
    [once("s05", "the rope runs from the beam itself, well apart from the ladder;"),
     "the rope runs from the coil on the beam itself, well apart from the ladder;"],
    [once("s05", "exactly seven people."),
     "exactly seven people, all seven standing on the grey flagstones with both feet from the first frame to the last."],
    [once("s05", "Carpenter Shi gives the knot one last hard pull and shouts down;"),
     "Carpenter Shi, both feet on the flagstones, jabs his raised hand up at the coil on the beam and shouts at the four on "
     "the rope;"],
]

S30 = [
    [once("s30", "standing in the pond against the far stone edge, its twelve flat wooden paddles round its rim;"),
     "standing in the pond against the far stone edge, its twelve flat wooden paddles round its rim, and the wheel stands "
     "dead still the whole shot: every paddle, spoke and pale wooden wedge of the wheel stays in exactly the same place from "
     "the first frame to the last, held fast before the water is let in, the pond water lying flat and calm under it;"],
    [once("s30", "his flat right hand already resting on one wet wooden paddle on the rim of the wheel at the right edge of "
                 "the frame from the first frame,"),
     "his flat right hand already resting on one wet wooden paddle on the rim of the wheel at the right edge of the frame "
     "from the first frame, his hand and that paddle staying at the same spot in the frame to the last frame,"],
    [once("s30", "beside him at the right, the near rim, spokes and paddles of the wheel;"),
     "beside him at the right, the near rim, spokes and paddles of the wheel, standing dead still;"],
    [once("s30", "Xu Yan's eyes travel slowly up the wheel and his hand stays pressed on the paddle;"),
     "Xu Yan's eyes travel slowly up the still wheel while his flat hand stays pressed on the same paddle at the same spot, "
     "and the whole wheel stays dead still, every paddle exactly where it was in the first frame;"],
    [once("s30", "The camera pushes in with small amplitude at slow speed."), "The camera holds a static shot."],
]

spec = {"shots": {
    sid: {"base": f"{BASES[sid][0]} {BASES[sid][1]} {sid} prompt and job", "base_run": BASES[sid][0],
          "base_seed": BASES[sid][1], "seeds": SEEDS[sid], "duration_seconds": DUR[sid], "replace": rep}
    for sid, rep in (("s05", S05), ("s30", S30))}}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("s05 s30 ->", HERE / "spec.json")
