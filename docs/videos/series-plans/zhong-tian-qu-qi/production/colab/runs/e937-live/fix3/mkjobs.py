"""e937 fix3 (REVIEW 3, 2026-11-23): eight shots again, seeds 9371231/9371232, 16 jobs, 98 s. Why in plan.md here and in
../review3-plan.md (section B).

Batch A (zt-live3): s27 s27b s32 s18. Batch B (zt-live2): s09 s12 s19 s31. Batch C (added after A and B were sent): s28.

s27  base fix2 9371221 (profile two-shot, face to face): the first frame is now her spear held low, his saber held out at chest
     height; the action is one upward stroke that knocks the saber up out of his hand (fix2 1221: empty hand + spear appearing at
     c0.375; fix2 1222: he swings the saber off himself). Lighter lime powder (cut review 2: grey hair read as another man).
s27b base fix2 9371221: three long steps, the point stopped one palm before his throat, the gap against the sky (fix2: touching).
s32  base d1 9371101: she is in the left third, the raider in the right half four steps away (d1: the bucket turned translucent
     over his face, the water fountained up, he shrank away); a solid dark bucket; the water falls on him, he falls back; static.
s18  base d1 9371101: Diao Qi's scar as the bible writes it (left brow to left cheekbone, one continuous line), his face nearly
     frontal so the left side is seen; no smile.
s09 / s19: no smile in the tense beat (both seeds of d1 smiled). s12: the hoe as a hoe (d1: a pickaxe), no smile.
s28  base d1 9371101: the saber stuck in the earth is left out (cut review 2: it read as a katana; a 1.25 crop would cut his
     knees or keep the blade), lighter powder, the long scar, Diao Qi without a smile.
s31: A-ling's sheathed knife as dark bark-brown wood no longer than her hand, held against her thigh (d1: a pale long tube).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e937-dh/runpod/live/fix3
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
SEEDS = [9371231, 9371232]
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC = "The camera holds a static shot."
SABER = "one long single-edged saber with a broad, gently curved back, widening toward the tip, a plain round iron disc at the hilt"
SCAR_ID = ["a short pale old scar on his left cheekbone",
           "one long pale old scar running from his left eyebrow down to his left cheekbone, one continuous line"]
SCAR_C = ["the short pale old scar on his left cheekbone",
          "the long pale old scar running from his left eyebrow down to his left cheekbone plain on his face"]
POWDER = ("his face, his brows and his hair caked thick and grey-white with lime powder, the pale powder plain on his cheeks "
          "and forehead")
LIGHT = "a light dusting of grey-white lime powder on his cheeks and brows, his hair still black under it"
BATCH = {"a": ["s27", "s27b", "s32", "s18"], "b": ["s09", "s12", "s19", "s31"], "c": ["s28"]}
BASE = {"s27": ("fix2", "s27-9371221"), "s27b": ("fix2", "s27b-9371221"), "s32": ("d1", "s32-9371101"),
        "s18": ("d1", "s18-9371101"), "s09": ("d1", "s09-9371101"), "s12": ("d1", "s12-9371101"),
        "s19": ("d1", "s19-9371101"), "s31": ("d1", "s31-9371101"), "s28": ("d1", "s28-9371101")}
# [old, new]: old must be in the base prompt exactly once
REPL = {
    "s27": [
        SCAR_ID, SCAR_C, [POWDER, LIGHT],
        ["the shaft bare below the head held low in her right hand from the first frame, its spearhead raised high above the two "
         "of them, just come up from a quick upward stroke,",
         "the shaft bare below the head already gripped low in her right hand from the first frame, the spear angled down across "
         "her body, its spearhead low near the ground between them, a step short of his feet,"],
        [f"his right hand empty above his shoulder from the first frame, the fingers spread, and his saber, {SABER}, already "
         "flying free in the air from the first frame an arm's length above his empty hand, spinning upward,",
         f"his saber, {SABER}, gripped in his right hand from the first frame and held out level at chest height toward her, its "
         "blade in the air between them,"],
        ["The spinning saber keeps flying upward, away from his empty hand, and leaves the frame through the top edge within "
         "the first second, and it stays out of the frame to the last frame; Diao Qi's right hand stays empty above his "
         "shoulder, the fingers spread, and he stares at her, while Qin Shuang holds her spearhead up, the two of them face to "
         "face, still;",
         "Qin Shuang sweeps the spear up in one fast upward stroke: the iron spearhead rises from the ground and strikes the "
         "underside of his saber blade, and the saber is knocked up out of his hand and flies spinning upward out through the "
         "top edge of the frame, and it stays out of the frame to the last frame; his right hand is left empty and spread at "
         "chest height, and he stares at her, while Qin Shuang holds the spear raised, the spearhead high, the two of them face "
         "to face, still;"],
    ],
    "s27b": [
        SCAR_ID, [POWDER, LIGHT],
        ["the short pale old scar on his left cheekbone,", ""],
        ["medium shot on the long ridge of dug earth, both of them framed from the waist up, the whole spear inside the frame:",
         "medium shot on the long ridge of dug earth, both of them framed from the waist up, the whole spear inside the frame, "
         "the camera at the height of their throats and square to the line between them, the gap between the spearhead and his "
         "throat seen against the night sky:"],
        ["standing two long steps away from him, her right arm stretched straight out toward him,",
         "standing three long steps away from him, her right arm stretched straight out toward him,"],
        ["its small iron head already held still in the air a full hand's breadth in front of his throat from the first frame, "
         "a clear gap of dark air between the spearhead and his throat to the last frame,",
         "its small iron point already stopped still in the air one palm's width in front of his throat from the first frame, "
         "the point never touching him, a clear gap of night sky between the point and his skin, plain against the sky to the "
         "last frame,"],
        ["Qin Shuang holds the spearhead perfectly still a hand's breadth from his throat, her arm straight, as she speaks, and "
         "Diao Qi swallows, his chin pressed back;",
         "Qin Shuang holds the spearhead perfectly still one palm's width from his throat, the gap between them clear, her arm "
         "straight, as she speaks, and Diao Qi swallows, his chin pressed back, his body leaning back away from the point;"],
    ],
    "s32": [
        ["medium shot from close behind one young woman seen only from behind, appearing only once:",
         "medium-wide shot from behind and a little to the left of one young woman seen only from behind, appearing only once:"],
        ["the back of her head facing straight away from us the whole time, her head still, her ear the furthest round her head "
         "we ever see, standing in the doorway of the narrow plank door, looking out down the dark alley, in the middle of the "
         "frame, framed from the waist up, facing straight away from us;",
         "the back of her head turned away from us the whole time, her ear the furthest round her head we ever see, standing in "
         "the doorway of the narrow plank door in the left third of the frame, framed from the knees up, turned away from us "
         "toward the alley at the right;"],
        ["one wooden bucket bound with iron hoops, full of steaming hot water already swung back low in both her hands from the "
         "first frame, steam rising from it; beyond her, three steps down the dark alley, one raider in a ragged undyed homespun "
         "tunic and a cloth head wrap seen only as a dark shape with his face in shadow, already rushing at the doorway from the "
         "first frame; beyond him the dark alley along the stone wall in the moonlight; she stays in the middle of the frame the "
         "whole shot;",
         "one solid wooden bucket of dark brown planks bound with two iron hoops, heavy and full of steaming hot water, already "
         "swung back low beside her right hip in both her hands from the first frame, steam rising from it; in the right half of "
         "the frame, four steps away from her down the dark alley and well clear of her and the bucket, one raider in a ragged "
         "undyed homespun tunic and a cloth head wrap, his face in shadow, already rushing at the doorway from the first frame, "
         "framed full figure, the same size to the last frame; beyond him the dark alley along the stone wall in the moonlight; "
         "she stays in the left third of the frame the whole shot;"],
        ["exactly two people, the young woman in the middle seen only from behind, the raider only a dark shape.",
         "exactly two people, the young woman at the left seen only from behind, the raider at the right with his face in shadow."],
        ["the one raider as a dark shape the composition describes",
         "the one raider at the right the composition describes"],
        ["She swings the bucket forward with both arms and the hot water flies out in one steaming sheet over the raider, who "
         "reels back with his arms over his face, only her arms moving; the young woman with the two high round buns keeps her "
         "head still, facing straight away from us, the back of her head toward us the whole shot,",
         "She swings the heavy bucket forward and up toward the right with both arms, and the hot water leaves the bucket in one "
         "thick steaming sheet that travels across the alley and falls down onto the raider's chest and arms, splashing onto the "
         "ground around his feet; the raider throws both arms over his face, staggers two steps back and falls backward onto the "
         "ground of the alley; the bucket stays in her two hands, only her arms and shoulders moving; the young woman with the "
         "two high round buns keeps her head turned away from us, the back of her head toward us the whole shot,"],
        [PUSH, STATIC],
    ],
    "s18": [
        SCAR_ID, SCAR_C,
        ["already running toward the ridge at the right at full speed from the first frame, framed from the waist up, his face "
         "three-quarter to screen right toward the ridge, never the lens; savage, not smiling:",
         "already running at full speed from the first frame toward the ridge just to the right of the camera, coming almost "
         "straight toward us, framed from the waist up, his face nearly frontal and turned only slightly to screen right, the "
         f"left side of his face with the scar in the light and clear to the camera, never the lens; savage, {NOSMILE}:"],
        ["his face three-quarter to screen right, his eyes on the ridge ahead of him, never looking at the camera;",
         "his face nearly frontal, his eyes on the ridge just beside the camera, never looking at the camera;"],
    ],
    "s09": [
        ["resolved, not smiling: brows level, eyes steady, lips moving firmly between words;",
         f"resolved and grave, {NOSMILE}: brows drawn slightly together, jaw set, eyes steady, lips together between words, "
         "the corners of his mouth level;"],
    ],
    "s12": [
        ["calm, a faint easy look in his eyes, lips moving evenly between words;",
         f"calm and serious, {NOSMILE}: brows level, eyes steady, lips moving evenly between words;"],
        ["standing, one hoe with a plain wooden handle and a flat iron head planted upright beside him with both hands resting "
         "on top of its handle,",
         "standing, one hoe resting on his right shoulder: a long plain wooden handle with one broad flat iron blade fixed at a "
         "right angle at its far end, the blade wide, thin and squared-off like a spade's, held by the handle in his right hand,"],
        ["his lips closed, not smiling,", f"his lips closed, {NOSMILE},"],
    ],
    "s19": [
        ["utterly still and cold, not smiling: eyes narrowed, brows level, lips barely moving between words;",
         f"utterly still and cold, {NOSMILE}: jaw tight, eyes narrowed on the torchlight, brows drawn low, lips pressed thin "
         "between words, the corners of her mouth turned down;"],
    ],
    "s28": [
        SCAR_ID, SCAR_C, ["a thick coat of white powder over his face,", LIGHT + ","],
        ["wide shot on the long ridge of dug earth, one long single-edged saber with a broad, gently curved back, widening toward "
         "the tip, a plain round iron disc at the hilt standing stuck point-down in the earth soft in the lower foreground:",
         "wide shot on the long ridge of dug earth, the bare trodden earth soft in the lower foreground:"],
        ["his lips closed, not smiling, never the lens;", f"his lips closed, {NOSMILE}, never the lens;"],
        ["fierce and loud, not smiling:", "fierce and loud:"],
    ],
    "s31": [
        ["one short knife sheathed in plain dark wood, grip and sheath one closed piece of dark wood as long as her hand in her "
         "right hand,",
         "one short knife sheathed in plain dark wood, grip and sheath one closed piece of dark wood as long as her hand, the "
         "dark brown of tree bark, held low in her right hand against her thigh,"],
        ["cold, not smiling: eyes narrowed, lips moving short and low between words;",
         f"cold, {NOSMILE}: eyes narrowed, lips moving short and low between words;"],
    ],
}
MUST = {
    "s27": ["gripped low in her right hand from the first frame", "held out level at chest height toward her",
            "strikes the underside of his saber blade", "stays out of the frame to the last frame", "medium two-shot in profile",
            LIGHT, STATIC, NOSMILE, "left eyebrow down to his left cheekbone"],
    "s27b": ["three long steps away", "one palm's width in front of his throat", "a clear gap of night sky", LIGHT, STATIC,
             NOSMILE, "speaks a short Mandarin line, 「刀放下了。再動一下，槍頭就進你喉嚨」"],
    "s32": ["in the left third of the frame", "in the right half of the frame", "falls backward onto the ground", STATIC,
            "Only the young woman with the buns seen only from behind and the one raider at the right"],
    "s18": ["left eyebrow down to his left cheekbone, one continuous line", "plain on his face", "nearly frontal", NOSMILE,
            "speaks a short Mandarin line, 「衝過去！柳溪的糧，全是咱們的！」"],
    "s09": [NOSMILE, "speaks a short Mandarin line, 「我站渠頭。石灰是我的主意，我得在那裡」"],
    "s12": [NOSMILE, "fixed at a right angle", "speaks a short Mandarin line, 「不用深，夜裡衝過來的人，絆一跤就夠了」"],
    "s19": [NOSMILE, "speaks a short Mandarin line, 「等，讓他們踩上坑，再等三步」"],
    "s28": [LIGHT, "framed full figure with both knees on the ground", NOSMILE,
            "speaks a short Mandarin line, 「綁了！把刁七押去穀倉關起來！」"],
    "s31": [NOSMILE, "the dark brown of tree bark", "speaks a short Mandarin line, 「進來一個，我就放倒一個」"],
}
GONE = {"s27": ["halfway into a downward cut", "flicks", "flying free", PUSH, "caked thick", "short pale old scar"],
        "s27b": ["resting still", "hand's breadth", PUSH, "caked thick", "short pale old scar"],
        "s32": ["in the middle of the frame", "dark shape", PUSH, "reels back"],
        "s18": ["short pale old scar"], "s09": [], "s12": ["planted upright"], "s19": [], "s31": [], "s28": ["saber", "stuck point-down", "short pale old scar"]}
hits, jobs = [], []
(out / "prompts").mkdir(parents=True, exist_ok=True)
for sid, (src, bid) in BASE.items():
    base = {j["id"]: j for j in json.loads((LIVE / src / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}[bid]
    t = (LIVE / src / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(t.encode()).hexdigest() != base["prompt_sha256"]:
        sys.exit(f"{sid}: {src} prompt not the one sent")
    for old, new in REPL[sid]:
        if t.count(old) != 1:
            sys.exit(f"{sid}: not once ({t.count(old)}): {old[:70]!r}")
        t = t.replace(old, new)
    t = t.replace(" ,", ",").replace(",,", ",")
    names = [pathlib.Path(r).name for r in base["reference_images"]]
    n = len(names)
    if sid in ("s27", "s27b") and (names[-1] != "prop-changqiang-l1.png"
                                   or f"The long spear shown in <Picture {n}> is the one spear in this shot" not in t):
        hits.append(f"{sid}: spear prop not last with its sentence")
    if f"<Picture {n}>" not in t or f"<Picture {n + 1}>" in t:
        hits.append(f"{sid}: picture count")
    for s in MUST[sid]:
        if s not in t:
            hits.append(f"{sid}: missing {s[:60]}")
    for s in GONE[sid]:
        if s in t:
            hits.append(f"{sid}: still has {s}")
    for w in ("cinema camera", "beard", "stubble", "sword", "fog", "pool", "open", "hang", "hung", "flick", "pickaxe",
              "chopper", "tassel", "armour", "fountain"):
        if re.search(rf"\b{w}", t, re.I):
            hits.append(f"{sid}: '{w}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", t.replace(NOSMILE, ""), re.I):
        hits.append(f"{sid}: {m.group(0)}")
    for m in re.finditer(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+)", re.sub(
            r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text|smile at any)\b", "", t, flags=re.I), re.I):
        if m.group(2).lower() not in {"one", "other", "more", "the", "at", "even", "until"}:
            hits.append(f"{sid}: '{m.group(0)}'")
    if t.count("never the mood. ") != 1 or t.count("One continuous shot.") != 1:
        hits.append(f"{sid}: separators")
    for seed in SEEDS:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(t, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": re.sub(r" fix\d$", "", base["title"]) + " fix3", "prompt_file": f"prompts/{pf.name}",
                    "prompt_sha256": hashlib.sha256(t.encode()).hexdigest(), "seed": seed,
                    "output_name": f"{sid}-{seed}.mp4", "output_path": str(out / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)
used = set()
for d in ("d1", "fix1", "fix2"):
    used |= {j["seed"] for j in json.loads((LIVE / d / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}
if used & set(SEEDS):
    hits.append(f"seeds used before: {used & set(SEEDS)}")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))
(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for b, shots in BATCH.items():
    bj = [j for j in jobs if j["id"].split("-")[0] in shots]
    (out / f"colab-jobs-{b}.json").write_text(json.dumps({"jobs": bj}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for j in jobs:
    print(j["id"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]])
print(len(jobs), "jobs,", sum(j["duration_seconds"] for j in jobs), "s, scan 0")
