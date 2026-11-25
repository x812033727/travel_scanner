"""e934 fix3: s15 s17 (A-ling cold), s30 s32 (Qian Yuanwai NOSMILE), s33 (Xu Yan clean-shaven). Why in plan.md.

    python3 -I mkspec.py                       # -> spec.json (5 shots, seeds 93414xx, two per shot)
    python3 -I mkjobs.py <live>/fix3           # -> <live>/fix3/prompts/*.txt, retake.json, colab-jobs.json (10 jobs, 84 s)

The base of each shot is the job and prompt exactly as sent for the take now in the cut (sha256 checked by mkjobs.py):
s15 d1 9341101, s17 d1 9341101, s30 d1 9341102, s32 fix1 9341211, s33 d1 9341101. So the d1 edits of ../mkspec.py
(PREP.md section 6: POOLMARK out of the field shots s30 s32 s33, the 'only' sentences, the GAZE_REFINE sentences) and s32's
fix1 staging are already in it. Each fix3 replace is asserted to be in its base exactly once.

What the earlier rounds taught (fix1/fix2 review-picks.tsv, both cut reviews):
- The expression must also be written in the MOTION part (after "never the mood. "), because refine-prep.py carries only
  that part into the refine prompt; a no-smile written only in the composition is lost at the refine (s32 fix1).
- "lips, jaw and cheeks moving clearly" invites a wide mouth and lifted cheeks; written here as small mouth shapes with the
  cheeks still (fix2 s28's wording, which held the teeth covered better than 'clearly').
- s30: "his mouth stuck in a stiff frozen stretch" is a smile shape; "fans himself with one wide sleeve" is a relaxed,
  pleased gesture; "small shrewd eyes" (fix1 lesson). Written instead as a concrete stunned face: wide staring eyes, brows
  raised and drawn together, jaw slack, mouth corners sagging, pale; arms slack at his sides.
- s32: fix2 got the face (sulk) but lost the staging when it asked to show "only the side of his face" and moved the gaze;
  so here 1211's staging and gaze are kept word for word, only the face is fix2's sulk, and it is also written in the motion.
- s15 s17: "cool and even, not smiling" still drew a soft smile when she hands over food; a concrete cold face by parts plus
  NOSMILE, also in the motion; the generic gaze "the person she is speaking to" becomes the buns in the nearer man's hand.
- s33: d1 wrote "a short dark stubble on his jaw" (the bible's 33-34 stubble) and the model drew a moustache and goatee that
  no other shot has; the face is written clean-shaven like the pictures (xuyan-portrait-l1 is clean-shaven); "lets out one
  long slow breath" goes (fix1 s09: the breath opens the mouth; d1 1102 opened it).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
LIVE = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
BASE = {"s15": ("d1", 9341101), "s17": ("d1", 9341101), "s30": ("d1", 9341102), "s32": ("fix1", 9341211),
        "s33": ("d1", 9341101)}
SEEDS = {"s15": [9341411, 9341412], "s17": [9341413, 9341414], "s30": [9341415, 9341416], "s32": [9341417, 9341418],
         "s33": [9341419, 9341420]}
DUR = {"s15": 8, "s17": 8, "s30": 8, "s32": 8, "s33": 10}  # the lengths bought before


def basetext(sid):
    src, seed = BASE[sid]
    return (LIVE / src / "prompts" / f"ref-{sid}-{seed}.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert basetext(sid).count(s) == 1, (sid, s[:70])
    return s


ALING_FACE = ("her face cold and still: brows level and unmoving, eyes cool and half-lidded, the corners of her mouth flat "
              "and level, her cheeks still")
S = {sid: {"base": f"{BASE[sid][0]} {sid}-{BASE[sid][1]}", "seeds": SEEDS[sid], "duration_seconds": DUR[sid],
           "replace": []} for sid in BASE}

S["s15"]["replace"] = [
    [once("s15", "cool and even, not smiling: brows level, lips moving calmly between words;"),
     f"{ALING_FACE}, her lips moving only a little between words, {NOSMILE};"],
    [once("s15", "her lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, turned toward "
                 "the person she is speaking to, face in profile or three-quarter profile, eyes on that person, never looking "
                 "at the camera;"),
     f"her lips moving evenly with every syllable in small natural talking mouth shapes, {ALING_FACE} the whole time, {NOSMILE}, "
     "her face three-quarter to screen right toward the nearer man, her eyes on the buns in his hand, never looking at the "
     "camera;"],
    [once("s15", "A-ling puts the two buns into the nearer man's hand as she speaks;"),
     "A-ling puts the two buns into the nearer man's hand as she speaks, her face staying just as cold;"],
]
S["s17"]["replace"] = [
    [once("s17", "cold and flat, not smiling: brows level, eyes cool, lips moving evenly between words;"),
     f"{ALING_FACE}, her lips moving only a little between words, {NOSMILE};"],
    [once("s17", "her lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, her face "
                 "three-quarter to screen right toward the wheel at the right"),
     f"her lips moving evenly with every syllable in small natural talking mouth shapes, {ALING_FACE} the whole time, {NOSMILE}, "
     "her face three-quarter to screen right toward the wheel at the right"],
]
S["s30"]["replace"] = [
    [once("s30", "small shrewd eyes,"), "small narrow eyes under heavy brows,"],
    [once("s30", "his mouth stuck in a stiff frozen stretch, eyes staring, his face drained pale, not smiling; lips moving "
                 "stiffly between words;"),
     "stunned and shaken: his eyes wide and staring at the water, his brows raised and drawn together, his jaw slack, the "
     f"corners of his mouth sagging down, his face drained pale, {NOSMILE};"],
    [once("s30", "his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, his face "
                 "three-quarter to screen left"),
     "his lips moving slowly with every syllable in small natural talking mouth shapes, his jaw slack, the corners of his "
     f"mouth sagging down, his eyes wide and his face stunned and pale the whole time, {NOSMILE}, his face three-quarter "
     "to screen left"],
    [once("s30", "Qian Yuanwai fans himself with one wide sleeve as he speaks;"),
     "Qian Yuanwai's arms stay slack at his sides and he stares at the water in the furrows as he speaks;"],
]
S["s32"]["replace"] = [
    [once("s32", "sour and dark: his face fallen, brows pulled down hard, the corners of his mouth pulled down, jaw clenched, "
                 f"lips tight and moving hard between words, {NOSMILE};"),
     "sulking and sour: his lower lip pushed out in a sulk, the corners of his mouth dragged down hard, his eyes narrowed "
     "under the heavy brows, his cheeks heavy and flat, his nostrils flared, his lips tight and moving hard between "
     f"words, {NOSMILE};"],
    [once("s32", "his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, his head turned "
                 "back over his right shoulder"),
     "his lips tight and moving hard with every syllable in small talking mouth shapes, his lower lip pushed out and the "
     f"corners of his mouth dragged down the whole time, {NOSMILE}, his head turned back over his right shoulder"],
    [once("s32", "his eyes on the field beyond the lower left edge of the frame, looking back down to the lower left, never "
                 "looking at the camera;"),
     "his eyes on the dry cracked field beyond the lower left edge of the frame, looking back down to the lower left, never "
     "looking at the camera;"],
]
S["s33"]["replace"] = [
    [once("s33", "dark shadows under his eyes and a short dark stubble on his jaw after seven short nights,"),
     "dark shadows under his eyes after seven short nights, his jaw, chin and upper lip clean-shaven and smooth exactly as "
     "in the pictures,"],
    [once("s33", "Xu Yan lets out one long slow breath and lifts his eyes again toward the field;"),
     "Xu Yan, his face clean-shaven and smooth, closes his eyes for a moment, then slowly lifts his eyes again toward the "
     "field;"],
]

spec = {"base": "the take now in the cut, job and prompt as sent: " + ", ".join(f"{k} {v[0]} {v[1]}" for k, v in BASE.items()),
        "shots": S}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR[k] * len(v['seeds']) for k, v in S.items())} s)")
