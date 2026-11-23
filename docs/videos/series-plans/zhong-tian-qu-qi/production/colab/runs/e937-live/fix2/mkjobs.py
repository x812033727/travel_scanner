"""e937 fix2 (coordinator 2026-11-23): s27 and s27b again, seeds 9371221/9371222, 4 jobs, 22 s. Why in ../fix1/plan.md
(還要重拍的) and plan.md here.

s27: base = the fix1 9371211 job and prompt as sent (profile two-shot, face to face, powder, static; its pictures = d1's, the
spear prop last): the result is now written as the first frame - the saber already in the air an arm's length above his empty
hand, flying up and out of the top edge, never coming back.
s27b: base = the d1 job and prompt as sent (the geometry of d1 1102 worked; pictures as d1, the spear prop last): she stands two
long steps away with her right arm straight, the spearhead held still a hand's breadth before his throat, the gap visible; his
face caked grey-white with lime; static.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e937-dh/runpod/live/fix2
"""
import hashlib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[8]
assert (ROOT / "AGENTS.md").is_file(), ROOT
out = pathlib.Path(sys.argv[1]).resolve()
LIVE = out.parent
SEEDS = [9371221, 9371222]
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC = "The camera holds a static shot."
POWDER = ("his face, his brows and his hair caked thick and grey-white with lime powder, the pale powder plain on his cheeks "
          "and forehead")
SABER = "one long single-edged saber with a broad, gently curved back, widening toward the tip, a plain round iron disc at the hilt"

BASE = {"s27": ("fix1", "s27-9371211"), "s27b": ("d1", "s27b-9371101")}
REPL = {
    "s27": [
        ["its spearhead pointing low at the ground a step short of him, well apart from his saber,",
         "its spearhead raised high above the two of them, just come up from a quick upward stroke,"],
        [f"{SABER} already raised to shoulder height in his right hand and halfway into a downward cut from the first frame,",
         f"his right hand empty above his shoulder from the first frame, the fingers spread, and his saber, {SABER}, already "
         "flying free in the air from the first frame an arm's length above his empty hand, spinning upward,"],
        ["In one quick stroke Qin Shuang's spearhead flicks up under the saber, and the saber flies spinning out of his hand up "
         "out of the top of the frame; his right hand is left empty above his shoulder, the fingers spread, and the two of them "
         "stay face to face, still;",
         "The spinning saber keeps flying upward, away from his empty hand, and leaves the frame through the top edge within "
         "the first second, and it stays out of the frame to the last frame; Diao Qi's right hand stays empty above his "
         "shoulder, the fingers spread, and he stares at her, while Qin Shuang holds her spearhead up, the two of them face to "
         "face, still;"],
    ],
    "s27b": [
        ["medium close-up on the long ridge of dug earth:",
         "medium shot on the long ridge of dug earth, both of them framed from the waist up, the whole spear inside the frame:"],
        ["framed from the chest up, one long spear:",
         "standing two long steps away from him, her right arm stretched straight out toward him, one long spear:"],
        ["held level in her right hand, its small iron head already resting still a hand's breadth before his throat from the "
         "first frame,",
         "held level along her straight right arm, its small iron head already held still in the air a full hand's breadth in "
         "front of his throat from the first frame, a clear gap of dark air between the spearhead and his throat to the last "
         "frame,"],
        ["calm and cold, not smiling:", f"calm and cold, {NOSMILE}:"],
        ["a thick coat of white powder over his face,", POWDER + ","],
        ["framed from the chest up, his chin lifted away from the spearhead,",
         "framed from the waist up, his chin lifted away from the spearhead,"],
        ["stunned, not smiling, his lips closed;", f"stunned, his lips closed, {NOSMILE};"],
        ["Qin Shuang holds the spearhead perfectly still at his throat as she speaks,",
         "Qin Shuang holds the spearhead perfectly still a hand's breadth from his throat, her arm straight, as she speaks,"],
        [PUSH, STATIC],
    ],
}
MUST = {"s27": ["already flying free in the air from the first frame", "stays out of the frame to the last frame",
                "medium two-shot in profile", "caked thick and grey-white", STATIC, NOSMILE],
        "s27b": ["two long steps away", "a full hand's breadth in front of his throat", "caked thick and grey-white", STATIC,
                 NOSMILE, "speaks a short Mandarin line, 「刀放下了。再動一下，槍頭就進你喉嚨」"]}
GONE = {"s27": ["halfway into a downward cut", "flicks", PUSH], "s27b": ["resting still", "at his throat as", PUSH]}
hits, jobs = [], []
(out / "prompts").mkdir(parents=True, exist_ok=True)
for sid, (src, bid) in BASE.items():
    base = {j["id"]: j for j in json.loads((LIVE / src / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}[bid]
    t = (LIVE / src / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(t.encode()).hexdigest() != base["prompt_sha256"]:
        sys.exit(f"{sid}: {src} prompt not the one sent")
    for old, new in REPL[sid]:
        if t.count(old) != 1:
            sys.exit(f"{sid}: not once: {old[:70]!r}")
        t = t.replace(old, new)
    names = [pathlib.Path(r).name for r in base["reference_images"]]
    n = len(names)
    if names[-1] != "prop-changqiang-l1.png" or f"The long spear shown in <Picture {n}> is the one spear in this shot" not in t:
        hits.append(f"{sid}: spear prop not last with its sentence")
    if not t.startswith("For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are"):
        hits.append(f"{sid}: header")
    for s in MUST[sid]:
        if s not in t:
            hits.append(f"{sid}: missing {s[:60]}")
    for s in GONE[sid]:
        if s in t:
            hits.append(f"{sid}: still has {s}")
    for w in ("cinema camera", "beard", "sword", "fog", "pool", "open", "hang", "hung"):
        if re.search(rf"\b{w}", t, re.I):
            hits.append(f"{sid}: '{w}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", t.replace(NOSMILE, ""), re.I):
        hits.append(f"{sid}: {m.group(0)}")
    for m in re.finditer(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+)", re.sub(
            r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text|smile at any)\b", "", t), re.I):
        if m.group(2).lower() not in {"one", "other", "more", "the", "at", "even", "until"}:
            hits.append(f"{sid}: '{m.group(0)}'")
    if t.count("never the mood. ") != 1 or t.count("One continuous shot.") != 1:
        hits.append(f"{sid}: separators")
    for seed in SEEDS:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(t, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": base["title"].replace(" fix1", "") + " fix2", "prompt_file": f"prompts/{pf.name}",
                    "prompt_sha256": hashlib.sha256(t.encode()).hexdigest(), "seed": seed,
                    "output_name": f"{sid}-{seed}.mp4", "output_path": str(out / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))
(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for j in jobs:
    print(j["id"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]])
print(len(jobs), "jobs, scan 0")
