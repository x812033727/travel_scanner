"""e938 fix4: the retakes of REVIEW 3 (../review3-plan.md, B) -- s09 (the bed behind them empty), s17 (Qin Shuang smiles),
s22 (the barrier runs through the horse). Why, shot by shot, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (3 shots, seeds 9381601/9381602)
    python3 -I mkjobs.py <live>/fix4           # -> <live>/fix4/prompts/*.txt, retake.json, colab-jobs.json (6 jobs, 38 s)
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix4/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix4/colab-jobs.json

As fix1-fix3: the base of each job is the job and prompt exactly as sent for the take now in the cut (mkjobs.py checks the
sha256; its reference_images ride along unchanged, so the appended spear / horse pictures and their sentences stay, last):
s09 d1 9381102, s17 d1 9381102, s22 fix2 9381401 (the first take with the gate's geometry right). Each replace is asserted to
be in that prompt exactly once. Bought at the base length. The base camera move is kept (s09 / s17 a slow push as d1, s22 static
as fix2). Not smiling.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
LIVE = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9381601, 9381602]
BASE = {"s09": ("d1", 9381102), "s17": ("d1", 9381102), "s22": ("fix2", 9381401)}
DUR = {"s09": 8, "s17": 6, "s22": 5}  # = the base jobs


def text(sid):
    r, seed = BASE[sid]
    return (LIVE / r / "prompts" / f"ref-{sid}-{seed}.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert text(sid).count(s) == 1, (sid, s[:80])
    return s


S = {sid: {"base": list(BASE[sid]), "duration_seconds": DUR[sid], "replace": []} for sid in DUR}

# s09: both d1 seeds show only the bare foot of the bed between them (Xiaohe out of frame at the pillow end): read as "the girl
# is gone" (review 2 M1). She is written into the bed behind them the way fix1 s12 9381302 got her (soft, asleep, under the quilt).
S["s09"]["replace"] = [
    [once("s09", "behind them, soft, the cracked plaster wall in the warm orange light;"),
     "behind them, soft, the cracked plaster wall in the warm orange light, and between them and behind Xu Yan, soft and out of "
     "focus, the bed with the pink quilt drawn over the small shape of the little girl asleep in it, her head on the pillow, "
     "in plain view from the first frame to the last;"],
    [once("s09", "exactly two people. Only these 2 people are in the frame;"),
     "exactly two people standing in the room, Qin Shuang and Xu Yan, with the little girl asleep in the bed behind them, soft. "
     "Only Qin Shuang and Xu Yan stand in the frame, with the little girl asleep under the quilt in the bed behind them;"],
]

# s17: d1 1102 smiles at c0.25 / c1.75 / c3.3 (review 1 該改 3): she is reading A-ling's mount, wary.
S["s17"]["replace"] = [
    [once("s17", "seeing it clearly, not smiling: eyes narrowing, brows level, lips moving quietly between words;"),
     f"seeing it clearly, serious and wary: eyes narrowed, brows level, lips moving quietly between words, the corners of her "
     f"mouth level and still, {NOSMILE};"],
]

# s22: fix2 1401 has the geometry right (camera, barrier, horse, wall) but the rails cross the horse's body and legs (review 2 M2):
# the horse moves two body-lengths further off, a strip of bare paving between the stakes and its hooves.
S["s22"]["replace"] = [
    [once("s22", "the barrier's top rail passing in front of its chest and the crossed stakes standing in front of all four of "
                 "its legs,"),
     "two full body-lengths beyond the far side of the barrier, the whole barrier between the camera and the horse with a clear "
     "strip of bare paving between the foot of the stakes and the horse's hooves, every rail and stake standing in front of the "
     "horse and none of them touching it,"],
    [once("s22", "Besides her, only the one horse is in the frame, the horse beyond the barrier and the side door on our side of "
                 "it;"),
     "Besides her, only the one horse is in the frame, the horse well beyond the barrier, apart from it, and the side door on our "
     "side of it;"],
]

(HERE / "spec.json").write_text(json.dumps({"seeds": SEEDS, "shots": S}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR.values())} s per seed, {2 * sum(DUR.values())} s)")
