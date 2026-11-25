"""e938 fix3: s25 and s26 turned to the gate's geometry that fix2 s22 found (fix3 prep agent, 2026-11-24). Why in plan.md.

    python3 -I mkspec.py                       # -> spec.json (2 shots, seeds 9381501/9381502)
    python3 -I mkjobs.py <live>/fix3           # -> <live>/fix3/prompts/*.txt, retake.json, colab-jobs.json (4 jobs, 24 s)
    python3 -I <scratchpad>/tools/check938f3.py <live>/fix3   # check938.py's assertions, rewritten for these two shots
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix3/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix3/colab-jobs.json

The geometry (fix2 s22 9381401, the first take that read right): the camera on the side-door side -> the barrier of crossed stakes
in the foreground -> the horse beyond it -> the long city wall. The d1 picks broke it: s25-9381102 has the barrier behind A-ling
and the wall behind the barrier (she stands on the far side from the wall); s26-9381101 has the barrier behind the captain, yet
seen from A-ling's side it must be in front of him, he being on the side-door side.

As fix1: the base of each job is the d1 9381101 job and prompt exactly as sent (sha256 checked by mkjobs.py, every d1 edit of
../spec.json in it), so the d1 appended pictures ride along (s25 the horse prop, s26 the captain's portrait, last, with their
sentence; the header unchanged since the count is unchanged); only the set crop is swapped for one of two new free crops of
set-chengmen-ye2-l1 (live-action/free-e031-e040/kong_e938.sh). Bought at the d1 length (6 s each = r2.py BUY; the recordings
a24 3.68 s and a25-p85 3.08 s fit). Static camera. Not smiling.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live/d1")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9381501, 9381502]
DUR = {"s25": 6, "s26": 6}  # d1 = BUY
STATIC = "The camera holds a static shot."
PUSH = "The camera pushes in with small amplitude at slow speed."


def d1text(sid):
    return (D1 / "prompts" / f"ref-{sid}-9381101.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert d1text(sid).count(s) == 1, (sid, s[:80])
    return s


S = {sid: {"duration_seconds": DUR[sid], "replace": []} for sid in DUR}

# s25: A-ling and the horse beyond the barrier, the stakes across the bottom of the frame in front of us, the wall close behind;
# the captain stays out of frame and unnamed (she speaks toward the left edge, as d1).
S["s25"]["swap_pictures"] = {"set-chengmen-ye2-lu-l1.png": "set-chengmen-ye2-zhahou-l1.png"}
S["s25"]["replace"] = [
    [once("s25", "medium shot on the road along the wall, side-on: A-ling,"),
     "medium shot from our side of the barrier, across it, side-on: the waist-high barrier of crossed wooden stakes running "
     "across the whole bottom of the frame in front of us, nearer to the camera than the horse; beyond it, on the road along "
     "the foot of the long city wall, A-ling,"],
    [once("s25", "framed from the waist up with the horse's head and neck before her, the horse's head toward the left,"),
     "framed from the waist up with the horse's head and neck before her, the horse's head toward the left, the top rail of the "
     "barrier passing in front of the horse's chest below her, the horse and A-ling beyond the barrier the whole shot,"],
    [once("s25", "that side of the frame is only the torchlit barrier of crossed stakes all the way to the edge,"),
     "that side of the frame is only the stakes and the dark wall all the way to the edge,"],
    [once("s25", "cold to the bone, not smiling: eyes narrowed, brows level, lips moving low and hard between words;"),
     f"cold to the bone: eyes narrowed, brows level, lips moving low and hard between words, {NOSMILE};"],
    [once("s25", "behind her, soft, the long dark wall and the road back the way she came under the moon;"),
     "behind her, soft, only the long dark city wall under the moon, close behind the horse;"],
    [once("s25", "Besides her, only the one horse is in the frame;"),
     "Besides her, only the one horse is in the frame, the two of them beyond the barrier and its stakes between them and us;"],
    [once("s25", PUSH), STATIC],
]

# s26: seen from A-ling's side across the barrier: the stakes in front of him along the bottom of the frame, the swung-out side
# door, its torch and the lit wall behind him; the same face and helmet (his portrait, from d1).
S["s26"]["swap_pictures"] = {"set-chengmen-ye2-qiang-l1.png": "set-chengmen-ye2-zhamen-l1.png"}
S["s26"]["replace"] = [
    [once("s26", "medium shot behind the barrier of crossed stakes, the tops of the crossed stakes soft along the bottom of the "
                 "frame:"),
     "medium shot from the road side, across the barrier: the waist-high barrier of crossed wooden stakes running across the "
     "whole bottom of the frame in front of him, nearer to the camera than he is, its stakes between him and us the whole shot:"],
    [once("s26", "standing behind the barrier, framed from the waist up,"),
     "standing on the side-door side of the barrier, just behind its stakes, the top rail across the frame at his waist, framed "
     "from the waist up,"],
    [once("s26", "hard and final, not smiling: brows down, eyes hard, lips moving hard between words;"),
     f"hard and final: brows down, eyes hard, lips moving hard between words, {NOSMILE};"],
    [once("s26", "behind him, soft, the lit brick wall and one torch fixed upright in an iron holder, nobody holding it, and at "
                 "the left edge the edge of the swung-out small side door;"),
     "behind him, soft, the swung-out small side door of studded planks at the left, the lit brick wall and one torch fixed "
     "upright in an iron holder, nobody holding it;"],
    [once("s26", PUSH), STATIC],
]

(HERE / "spec.json").write_text(json.dumps({"seeds": SEEDS, "shots": S}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR.values())} s per seed, {2 * sum(DUR.values())} s)")
