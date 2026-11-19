"""e934 fix2: s28 and s32 only, as fix1/review-picks.tsv's fix2 lines ask. NOT RUN: written and checked (mkjobs.py,
preflight-prompts.py, check_manifest.py, h3r.sh check), nothing is sent. Why in plan.md.

    python3 -I mkspec.py                       # -> spec.json (s28 seeds 9341311/9341312, s32 seeds 9341313/9341314, 8 s)
    python3 -I mkjobs.py <live>/fix2           # -> <live>/fix2/prompts/*.txt, retake.json, colab-jobs.json (4 jobs, 32 s)

The base of each shot is the fix1 job and prompt exactly as sent and picked as the stand-in (s28: fix1 9341212; s32: fix1
9341211), so the d1 edits of ../mkspec.py (PREP.md section 6: POOLMARK out of the field shots, the GAZE_REFINE sentences, the
'only' sentences, s28's staff out) and the fix1 replaces are already in it; mkjobs.py asserts both before anything is
replaced, and that no pool word is in either field shot. Each fix2 replace is asserted to be in that fix1 prompt once.

What fix1 taught (fix1/review-picks.tsv):
- s28: the frame, the static camera, the grieving brows and the bow all worked, but Elder Han still smiled while he spoke
  (1212: mouth wide, upper teeth bare, cheeks up at 「給您磕個頭」 5.5-6.75 s) and the bow only began after the line (7.0 s).
  So the result moves earlier (by the middle of the line he is already bent forward, hands on the grass, and says the last
  words with his face turned down toward the grass: the face that could smile is out of sight when the line ends); the
  mouth is written small and hidden ("clearly" goes: parting only a little on each word under the white moustache, upper teeth
  covered, cheeks slack and hanging, lips trembling); the identity gets "a worn, grieving old face". Kept: the knees-up frame,
  the static camera, the brows, the bow's result sentence (hands slid forward onto the grass, head lowered, all in the frame).
- s32: 1211 got the staging (back three-quarter from the first frame, head back over the right shoulder, sleeve in the first
  second, ends in the right third, static) but smiled smugly through the line, and looked level to the left, not down to the
  field. So less face (only his ear, cheek and the tip of his moustache past the right shoulder), a concrete sulking face
  (lower lip pushed out, mouth corners dragged down, eyes narrowed, cheeks hanging, nostrils flared) in place of "sour and
  dark", his eyes cast down to the field below the lower left edge; "short and portly with a round face and a thin
  eight-shaped moustache" is not said twice (the identity keeps it; the composition names only the robe and the action).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FIX1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live/fix1")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
BASE = {"s28": 9341212, "s32": 9341211}
SEEDS = {"s28": [9341311, 9341312], "s32": [9341313, 9341314]}


def fix1text(sid):
    return (FIX1 / "prompts" / f"ref-{sid}-{BASE[sid]}.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert fix1text(sid).count(s) == 1, (sid, s[:70])
    return s


S = {sid: {"base": f"fix1 {sid}-{BASE[sid]}", "seeds": SEEDS[sid], "duration_seconds": 8, "replace": []} for sid in BASE}

# s28: the bow by the middle of the line, the last words said to the grass; a small hidden mouth; a worn grieving face.
S["s28"]["replace"] = [
    [once("s28", "a deeply lined face, a long white beard down to his chest, white hair in a neat small topknot, grave steady "
                 "eyes,"),
     "a worn, grieving old face, deeply lined, a long white beard down to his chest, white hair in a neat small topknot, grave "
     "steady eyes,"],
    [once("s28", "his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, his face "
                 "three-quarter to screen right, his eyes on the spot beyond the upper right edge of the frame as he starts to "
                 "bow, never looking at the camera;"),
     "his lips moving with every syllable in small natural talking mouth shapes, his mouth parting only a little on each "
     "word under the white moustache, his upper teeth covered, his cheeks slack and hanging, his lips trembling, his face "
     "three-quarter to screen right, his eyes on the spot beyond the upper right edge of the frame for the first words and "
     "then on the grass in front of him as he goes down, never looking at the camera;"],
    [once("s28", "By the last word Elder Han has bowed low: his body bent forward from the waist, his two hands slid forward off "
                 "his knees onto the grass in front of him, his head lowered toward the ground, all of him still in the frame; "
                 "he starts to bend forward slowly with the first words and keeps going down as he speaks,"),
     "By the middle of the line Elder Han has already bowed low: his body bent forward from the waist, his two hands slid "
     "forward off his knees onto the grass in front of him, his head lowered toward the ground, all of him still in the "
     "frame, and he says the last words with his face turned down toward the grass, only his white topknot and brow toward "
     "the camera; he starts to bend forward with the first word and keeps going down as he speaks,"],
]

# s32: 1211's staging kept; less face; a concrete sulking face; eyes cast down to the field at the lower left.
S["s32"]["replace"] = [
    [once("s32", "Qian Yuanwai, short and portly with a round face and a thin eight-shaped moustache, in his dark gold silk "
                 "robe"),
     "Qian Yuanwai, in his dark gold silk robe"],
    [once("s32", "his head turned back over his right shoulder, his face in profile looking back down toward the field beyond "
                 "the lower left edge of the frame, never the lens;"),
     "his head turned back over his right shoulder, so that we see only the side of his face past his right shoulder: his "
     "ear, his cheek and the tip of his moustache, his eyes cast down toward the field below the lower left edge of the "
     "frame, never the lens;"],
    [once("s32", "sour and dark: his face fallen, brows pulled down hard, the corners of his mouth pulled down, jaw clenched, "
                 f"lips tight and moving hard between words, {NOSMILE};"),
     "sulking and sour: his lower lip pushed out in a sulk, the corners of his mouth dragged down hard, his eyes narrowed "
     "under the heavy brows, his cheeks hanging flat and heavy, his nostrils flared, his lips tight and moving hard between "
     f"words, {NOSMILE};"],
    [once("s32", "his head turned back over his right shoulder, his eyes on the field beyond the lower left edge of the frame, "
                 "looking back down to the lower left, never looking at the camera;"),
     "his head turned back over his right shoulder, his eyes on the field below the lower left edge of the frame, cast down "
     "toward it, never looking at the camera;"],
]

spec = {"base": "fix1 job and prompt as sent: s28 9341212, s32 9341211", "shots": S}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(8 * len(v['seeds']) for v in S.values())} s)")
