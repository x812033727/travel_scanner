"""e931 fix3: s23 once more, from the d1 pick (picks-merged.tsv: s23 9311102). Both cut reviews: the bowl in s23 is a white
heap with three upright sprouts stuck in it, like cooked rice with incense sticks (cut-review.md 輕微 3, cut-review-2.md
中等 2), while s21 and s22 (fix2 9311301) show golden-brown seeds with short white sprouts lying on them. Owner 2026-11-18:
quality first, retake s23. Written 2026-11-18, NOT run (paid Colab; the send script is the scratchpad's e931f3.sh, session
zt-live2).
Same steps as fix1/fix2: retake.py from live/st1, with the d1 edits of s23 applied first, unchanged from ../spec.json (this
script checks that they rebuild d1's 9311102 prompt byte for byte, pictures renumbered), then the fix3 edits below. Seeds
9311401/9311402 (fix<N> = 9311(N+1)xx), bought at the d1 length (6 s).

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix3 spec.json
    python3 -I mkjobs.py <live>/fix3
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix3/colab-jobs.json
    bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix3/colab-jobs.json

Why (frames of d1 9311102, its refine, s21 9311101, s22 fix2 9311301 and s24 9311102 checked 2026-11-18, scratchpad
e931f3/*.jpg, bowls.jpg):
- d1 wrote the bowl as "holding a layer of rice grains, each grain with one tiny white sprout": "rice grains" without
  "unhusked" or a colour reads as cooked white rice, and "each grain with one sprout" as sprouts standing in it. Both seeds of
  d1 drew a white mound with three upright sprouts. Now the bowl is fix2 s22's sentence, the one its 9311301 take proved
  (golden-brown unhusked seeds filled level to just below the rim, about ten thread-thin white sprouts each one grain long
  lying flat on the seeds, the surface flat from rim to rim), kept in s23's own hold (left hand, bottom of the frame) and
  tilted a little toward us so the flat golden top shows; the action sentence adds s22's "lie still and flat ... keeping its
  one-grain length from the first frame to the last". No negated noun; no leaf, seedling, shoot, stem, green or grow word.
- The wet cloth: s21 lifts it, s22 has it over his left wrist (bowl uncovered), s24 has it back over the bowl (an accepted
  continuity slip, cut-review 2 item 2/7). s23 sits between s22 and s24 and is cut hard after s22, whose prompt already
  says "the wet cloth over his left wrist": s23 takes the same words, bowl uncovered.
- The face: d1 did not smile (both pickers), but "not smiling" is a smile word the season stopped writing (fix2): now
  "sobering and grave" plus the corners of his mouth level. Everything else of d1 stays: the one man, medium close-up,
  his eyes lifting from the bowl to the cracked earth beyond the right edge (the one action), the line 「芽是醒了，可田裡
  沒水，插下去也活不了」 spoken on camera (its own voice is used, as d1's was; recording a22 is the fallback), the slow push
  (it kept the bowl in frame in d1), the pictures (portrait, angle-a, -han-wu-l1).
"""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
LIVE = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e931-dh/runpod/live")
ST1, D1DIR = LIVE / "st1", LIVE / "d1"
D1 = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
PICK = {"s23": 9311102}  # picks-merged.tsv
SHOTS = ("s23",)


def norm(t):
    return re.sub(r"(<Picture \d+>(, | and )?)+( \(the same [^)]*\))?", "<P>", t)


def d1text(sid):
    text = (ST1 / "prompts" / f"ref-{sid}.txt").read_text(encoding="utf-8")
    for old, new in D1[sid]["replace"]:
        assert old in text, (sid, old[:60])
        text = text.replace(old, new)
    picked = (D1DIR / "prompts" / f"ref-{sid}-{PICK[sid]}.txt").read_text(encoding="utf-8")
    # retake.py renumbers the pictures after drop_pictures; everything else must be d1's prompt byte for byte (mkjobs.py
    # checks the built fix3 prompt against d1's file exactly, with the fix3 edits undone)
    assert norm(text) == norm(picked), f"{sid}: st1 + d1 edits do not rebuild d1's {PICK[sid]} prompt"
    return text


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:60])
    return s


S = {sid: json.loads(json.dumps(D1[sid])) for sid in SHOTS}
for sid in SHOTS:
    S[sid]["replace"] = [list(p) for p in D1[sid]["replace"]]

# --- s23: the bowl as fix2 s22 wrote it (proved by 9311301), in s23's left-hand hold; the cloth as in s22 --------------------
S["s23"]["replace"] += [
    [once("s23", "one red clay bowl holding a layer of rice grains, each grain with one tiny white sprout held in his left hand "
                 "at the bottom of the frame,"),
     "one red clay bowl filled level to just below its rim with plump golden-brown unhusked rice seeds, held in his left hand "
     "at the bottom of the frame and tilted a little toward us so that the flat golden top of the seeds shows, about ten short "
     "thin pure-white sprouts scattered evenly over the seeds, each sprout as long as one rice grain and as thin as a thread, "
     "lying flat on the seeds against its own grain, the surface of the seeds flat and level from rim to rim, the wet cloth "
     "over his left wrist,"],
    # the face without a smile word (fix2's lesson); d1's concrete parts kept
    [once("s23", "sobering, not smiling: the warmth leaving his eyes, brows drawing together, lips moving evenly between words;"),
     "sobering and grave: the warmth leaving his eyes, brows drawing together, the corners of his mouth level, lips moving "
     "evenly between words;"],
    # the seeds and sprouts keep still and keep their size (s22's sentence)
    [once("s23", "Xu Yan's eyes lift from the bowl to the cracked earth beyond the right edge of the frame as he speaks, his "
                 "brows drawing together, and the hazy hot afternoon light stays unchanged."),
     "Xu Yan's eyes lift from the bowl to the cracked earth beyond the right edge of the frame as he speaks, his brows drawing "
     "together; the bowl stays in his left hand at the bottom of the frame, its golden seeds and their short white sprouts "
     "lying still and flat, each sprout keeping its one-grain length from the first frame to the last; the hazy hot afternoon "
     "light stays unchanged."],
]

DUR = {"s23": 6}  # the d1 length
for sid in S:
    S[sid]["duration_seconds"] = DUR[sid]
    text = d1text(sid)
    for old, new in S[sid]["replace"][len(D1[sid]["replace"]):]:
        assert text.count(old) == 1, (sid, old[:60])
        text = text.replace(old, new)

(HERE / "spec.json").write_text(json.dumps({"seeds": [9311401, 9311402], "base": {k: f"d1 {v}" for k, v in PICK.items()},
                                            "shots": S}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(S), "shot ->", HERE / "spec.json")
