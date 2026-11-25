"""e938 fix2: the retakes of ../fix1/review-picks.tsv (fix2 prep agent, 2026-11-23). Why, shot by shot, in plan.md.

    python3 -I mkspec.py                       # -> spec.json (3 shots, seeds 9381401/9381402 for every shot)
    python3 -I mkjobs.py <live>/fix2           # -> <live>/fix2/prompts/*.txt, retake.json, colab-jobs.json (6 jobs, 32 s)
    python3 -I <scratchpad>/tools/check938f2.py <live>/fix2   # check938.py's assertions, rewritten for these three shots
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix2/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix2/colab-jobs.json

The base of every job is the fix1 9381301 job and prompt exactly as sent (mkjobs.py checks the sha256 and that every fix1 edit of
../fix1/spec.json is in it; fix1 itself was built on the d1 9381101 job, so the d1 appended pictures - the horse prop s22 s27, the
captain s27 - and every d1 edit ride along). Each fix2 replace is asserted to be in the fix1 prompt exactly once. Bought at the
d1 length (= r2.py BUY). Static camera as fix1. s22 s27 swap the fix1 gate crop -zha2 for the lower, closer free crop -zha3.

The coordinator's list from the fix1 picks: s01 (1301 a second Xu Yan sits behind the bed; 1302 the pillow at the left and no
cloth on her forehead in the first frame), s22 (the horse walks to the side door and the barrier runs through its body), s27 (1302
0-0.75 s right, then the whole leap; the captain never throws himself aside).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
F1 = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live/fix1")
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = [9381401, 9381402]
DUR = {"s01": 6, "s22": 5, "s27": 5}  # d1 = BUY


def f1text(sid):
    return (F1 / "prompts" / f"ref-{sid}-9381301.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert f1text(sid).count(s) == 1, (sid, s[:80])
    return s


S = {sid: {"duration_seconds": DUR[sid], "replace": []} for sid in DUR}

# s01: "kneeling at the pillow end at screen right" and "the pillow end at screen right" asked for one spot twice: 1302 moved her
# head to the left, 1301 put a second Xu Yan behind the bed. He kneels at the middle of the bed, just left of the pillow; the second
# cloth is gone (his palm is on the cloth already on her forehead); "the only man in the room" goes with the counts, twice.
# Not to be mirrored in the cut (the cross collar would close the wrong way).
S["s01"]["replace"] = [
    [once("s01", "the whole bed across the frame with its pillow end at screen right and its foot at screen left,"),
     "the whole bed across the frame with its pillow end at screen right and its foot at screen left, her head on the pillow at "
     "screen right and her feet toward screen left,"],
    [once("s01", "kneeling upright on the clear floor at the near side of the bed by its pillow end at screen right, Xu Yan,"),
     "kneeling upright on the clear floor at the near side of the bed, in the middle of the frame just left of the pillow, Xu Yan,"],
    [once("s01", "his right hand already holding a second folded damp white cloth, freshly wrung, a hand's breadth above her "
                 "forehead from the first frame,"),
     "his right palm already resting on the folded damp white cloth, freshly wrung, that lies across her forehead from the first "
     "frame, her head on the pillow at screen right in plain view beyond his hand,"],
    [once("s01", "exactly two people: Xu Yan kneeling and one little girl alone in the bed. Only these 2 people are in the frame, "
                 "Xu Yan kneeling on the floor and little Xiaohe, the only child, lying alone in the bed;"),
     "exactly two people: Xu Yan kneeling and one little girl alone in the bed; he is the only man in the room, and nobody sits "
     "on the bed or stands behind it. Only these 2 people are in the frame, Xu Yan kneeling on the floor, the only man in the "
     "room, and little Xiaohe, the only child, lying alone in the bed;"],
    [once("s01", "Xu Yan lays the fresh cloth gently on her forehead and smooths it down with his palm as he speaks, staying on "
                 "both knees to the last frame;"),
     "Xu Yan smooths the cloth on her forehead gently down with his palm as he speaks, staying on both knees in the same place "
     "to the last frame;"],
]

# s22 + s27, one camera, the lower crop -zha3 (the stakes large across the lower half on our side, the wall foot beyond them):
# both fix1 seeds of s22 walked the horse up to the side door with the barrier through its body; 1302 of s27 leapt at 0.875 s.
for sid in ("s22", "s27"):
    S[sid]["swap_pictures"] = {"set-chengmen-ye2-zha2-l1.png": "set-chengmen-ye2-zha3-l1.png"}
    S[sid]["replace"] = [
        [once(sid, "running across the middle of the frame from the foot of that torch out to the right edge, standing between the "
                   "horse and the side door;"),
         "running large across the lower half of the frame from the foot of that torch out to the right edge, nearer to the "
         "camera than the horse, standing between the horse and the side door;"],
    ]
S["s22"]["replace"] += [
    [once("s22", "wide shot at the barrier from the side-door side, like the picture:"),
     "wide shot from a low camera on the side-door side close to the barrier, like the picture:"],
    [once("s22", "already reined in hard three steps short of the barrier from the first frame, seen side-on with its head toward "
                 "the left, its legs seen through the crossed stakes,"),
     "standing in the right half of the frame, at least three horse-lengths from the side door at the left, already reined in "
     "to a standstill from the first frame, seen side-on with its head toward the left, the barrier's top rail passing in front "
     "of its chest and the crossed stakes standing in front of all four of its legs,"],
    [once("s22", "her face in profile to screen left toward the gate, never the lens, her lips closed, not smiling;"),
     f"her face in profile to screen left toward the gate, never the lens, cold and still, her lips pressed shut in one flat "
     f"line, {NOSMILE};"],
    [once("s22", "Beyond the barrier the horse tosses its head hard and stamps its forefeet on the spot,"),
     "Beyond the barrier the horse stays on the same spot from the first frame to the last and does not walk; it tosses its "
     "head hard and stamps its forefeet where it stands,"],
]
S["s27"]["replace"] += [
    [once("s27", "already at a flat-out gallop from the first frame, coming in from the right edge and charging toward the left "
                 "straight at the barrier where it meets the wall by the torch, seen side-on, its head toward the left, its legs "
                 "stretched long, its mane flying,"),
     "already at a flat-out gallop from the first frame, still small and far off at the right edge, a dozen strides from the "
     "stakes, charging toward the left at the barrier, seen side-on, its head toward the left, its mane flying, the crossed "
     "stakes in front of its legs,"],
    [once("s27", "framed full figure, small, already flinching back from the first frame, his face toward the horse,"),
     "framed full figure, small, already throwing himself to the left from the first frame, his face toward the horse,"],
    [once("s27", "The horse pounds flat out along the road straight at the barrier, its head low, its mane flying, closing in stride "
                 "by stride, still two strides short of the stakes with all four hooves on the ground as the shot ends, while the "
                 "guard captain throws himself aside toward the left;"),
     "The horse pounds flat out along the road toward the barrier, its head low, its mane flying, and in this shot it closes "
     "only half of that distance, still well short of the stakes with all four hooves on the ground as the shot ends; it never "
     "reaches or touches the barrier and its front hooves stay low, never higher than its knees, at every stride; the guard "
     "captain lands on the paving by the side door and lies sprawled on his side;"],
]

(HERE / "spec.json").write_text(json.dumps({"seeds": SEEDS, "shots": S}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR.values())} s per seed, {2 * sum(DUR.values())} s)")
