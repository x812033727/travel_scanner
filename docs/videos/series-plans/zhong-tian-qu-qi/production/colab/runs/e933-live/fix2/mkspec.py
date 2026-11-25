"""e933 fix2: s34 only (the hook 「轉半圈」), two variants x two seeds, 8 s each. NOT RUN: written and checked (mkjobs.py,
preflight-prompts.py, check_manifest.py, h3r.sh check), nothing is sent. Why in plan.md.

    python3 -I mkspec.py                       # -> spec.json (s34, variants A and B)
    python3 -I mkjobs.py <live>/fix2           # -> <live>/fix2/prompts/*.txt, retake.json, colab-jobs.json (4 jobs, 32 s)

What fix1 taught (fix1/review-picks.tsv s34, measured with scratchpad e933/picks-a/rot6.py): this H3 route turns the wheel
about 40-70 degrees in a whole clip (1211: 38 degrees, stopped at 4.75 s; 1212: 66 degrees, stopped at 5.25 s), so "half a
turn" never happens, and the pale marker at the top (set-shentan-l4) only made the short turn plainer; the water went flat
after 4-4.5 s. The coordinator's decision: make "it turns, then stops dead" readable and stop chasing 180 degrees (nobody can
read the angle; 「就轉半圈」 in s39 is Qian Yuanwai's sneer and stays). So:

- the result is written first (where the wheel ends and that the last two seconds are dead still), then the path (five steady
  seconds down the left side, then a jolt and a dead stop), and the water as one white stream pouring from the left straight
  onto the lowest paddle, foaming white to the last frame; 8 s bought (d1 and fix1 bought 6); the camera static as before;
- the water's source is written into the first frame: set-shentan-l3 has no flume (stone steps and a plank landing at the
  left), so a short wooden chute at the end of s33's stone channel (fix1 s33 9331211, picked: the water rushes along a stone
  channel toward the wheel at the right) exists in the text only; risk in plan.md;
- A (9331311/9331312) on set-shentan-l5 (free: live-action/free-e031-e040/shentan_l5.py, the nine o'clock paddle pale):
  a quarter turn takes the pale paddle into the water, and 45-60 degrees already dips it at about seven to eight o'clock;
- B (9331313/9331314) on set-shentan-l3, no marker, the same path and water: e934 is sent on the l3 family (no pale paddle),
  so B cuts into e934's opening wheel shots without a continuity question.

The base is the d1 9331101 s34 job and prompt exactly as sent (as fix1); each replace is asserted to be there once.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e933-dh/runpod/live/d1")
REFS = "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live/"
D1TEXT = (D1 / "prompts" / "ref-s34-9331101.txt").read_text(encoding="utf-8")


def once(s):
    assert D1TEXT.count(s) == 1, s[:70]
    return s


WHEEL = once("and the big wooden water wheel exactly as in the picture, standing in the pond against the far stone edge, "
             "its twelve flat wooden paddles round its rim;")
WATER0 = once("a white surge of water already rushing along the stone edge from the left into the pond under the wheel;")
ONLY = once("only the wheel, its frames, the pond, the stone edge and the fields are in the frame.")
ACTION = once("In this shot the wheel turns only half a turn and then stops dead: the rushing water strikes the lowest "
              "paddles, the big wheel creaks and swings slowly round half a turn, slows, and stops, and stays still to the "
              "last frame while the water churns white under it,")

CHUTE = ("at the left edge of the frame the end of the narrow stone channel, with one short wooden chute laid from it over "
         "the stone edge toward the bottom of the wheel, and a thick white stream of water already pouring out of the chute "
         "straight onto the lowest paddle of the wheel and foaming white around it;")
ONLY_NEW = "only the wheel, its frames, the chute, the pond, the stone edge and the fields are in the frame."
STREAM = ("while the thick white stream keeps pouring from the chute at the left straight onto the lowest paddle, churning "
          "and foaming white around it to the very last frame,")

A = [
    [WHEEL,
     "and the big wooden water wheel exactly as in the picture, standing in the pond against the far stone edge, its twelve "
     "flat wooden paddles round its rim: eleven of dark weathered wood and one of pale fresh-cut wood, much lighter than all "
     "the others, sticking straight out from the left side of the wheel, level with the hub, in the first frame;"],
    [WATER0, CHUTE],
    [ONLY, ONLY_NEW],
    [ACTION,
     "In this shot the wheel ends with the pale paddle down at the very bottom of the wheel, sunk in the white water, and for "
     "the last two seconds nothing on the wheel moves at all: for the first five seconds the big wheel creaks and turns "
     "slowly and steadily, the pale paddle travelling down the left side of the wheel from beside the hub into the water; "
     "then with one jolt the wheel stops dead, the pale paddle at the bottom in the water, and it stays dead still to the "
     f"last frame, {STREAM}"],
]
B = [
    [WATER0, CHUTE],
    [ONLY, ONLY_NEW],
    [ACTION,
     "In this shot the wheel ends stopped dead, one paddle down at the very bottom of the wheel, sunk in the white water, and "
     "for the last two seconds nothing on the wheel moves at all: for the first five seconds the big wheel creaks and turns "
     "slowly and steadily, the paddles on the left side travelling down into the water one after another; then with one "
     f"jolt the wheel stops dead, and it stays dead still to the last frame, {STREAM}"],
]
spec = {"base": "d1 9331101 s34 prompt and job", "shot": "s34", "duration_seconds": 8, "variants": {
    "A": {"seeds": [9331311, 9331312], "picture": "set-shentan-l5.png",
          "swap_pictures": {"set-shentan-l3.png": REFS + "set-shentan-l5.png"}, "replace": A},
    "B": {"seeds": [9331313, 9331314], "picture": "set-shentan-l3.png", "swap_pictures": {}, "replace": B}}}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("s34 A+B ->", HERE / "spec.json")
