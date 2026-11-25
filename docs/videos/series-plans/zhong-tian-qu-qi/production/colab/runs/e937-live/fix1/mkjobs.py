"""e937 fix1: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (10 shots x seeds
9371211/9371212 = 20 jobs, 118 s). Copied from e936-live/fix1/mkjobs.py: the base of each job is the d1 9371101 job and prompt
exactly as sent (sha256 checked; its reference_images, the appended spear prop included, unchanged), every d1 edit of
../spec.json for the shot asserted to be in the base, the fix1 replaces applied once each.

Scans (exit 1 on a hit): negative nouns, the two separators once, beard words, 'cinema camera', 'fog', smile words beyond
NOSMILE (s37 may smile: the script's tired smile), pool words on the channel, people named who are not in the frame, fix1's
MUST / GONE lists, the spear prop last with its sentence in s26 s27 s27b s36, the line of the speaking shots, static camera
once, pictures = d1, seconds, seeds, header count.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e937-dh/runpod/live/fix1
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
D1 = out.parent / "d1"
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
d1spec = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
d1jobs = {j["id"]: j for j in json.loads((D1 / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = spec["seeds"]
assert SEEDS == [9371211, 9371212], SEEDS
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
SPEAR = "The long spear shown in <Picture"
SPEARSHOTS = {"s26", "s27", "s27b", "s36"}
CHANNEL = {"s10", "s14", "s16b", "s21", "s26", "s27", "s27b", "s36", "s37"}
DUR = {"s09b": 5, "s10": 6, "s14": 6, "s16b": 6, "s21": 5, "s26": 6, "s27": 5, "s27b": 6, "s36": 6, "s37": 8}
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "Diao Qi": r"Diao Qi", "Tang Xiaotang": r"Xiaotang",
          "Erniu": r"Erniu|Er Niu", "A-ling": r"A-ling|Aling", "Xiaohe": r"Xiaohe|Xiao He"}
IN_FRAME = {"s09b": {"Xu Yan"}, "s10": {"Xu Yan"}, "s14": {"Qin Shuang"}, "s16b": {"Xu Yan"}, "s21": set(),
            "s26": {"Qin Shuang"}, "s27": {"Qin Shuang", "Diao Qi"}, "s27b": {"Qin Shuang", "Diao Qi"},
            "s36": {"Qin Shuang"}, "s37": {"Xu Yan"}}
LINE = {"s10": "「糖坊剩的石灰，三步埋一袋，袋口朝上」", "s14": "「你下去，站到後頭，這裡會死人」",
        "s27b": "「刀放下了。再動一下，槍頭就進你喉嚨」", "s36": "「你一個字都沒改我的陣，也一步都沒退」",
        "s37": "「陣是妳排的，我只負責站著別跑」"}
MUST = {
    "s09b": ["its clear left half plain to see the whole shot", "already at the gateway from the first frame",
             "in one single file", "only the last two men are still in the yard"],
    "s10": ["squatting low on his heels from the first frame to the last", "palm down and all five fingers together", NOSMILE],
    "s14": ["his dark hair cropped short at the nape", "staying at the right edge of the frame from the first frame to the last",
            NOSMILE],
    "s16b": ["already clenched into tight fists from the first frame", "his hands staying inside the frame to the last frame",
             NOSMILE],
    "s21": ["already sunk to the waist in two shallow pits", "a heavy white bank rolling outward along the ground"],
    "s26": ["already turned side-on to him from the first frame", "one spear in the frame",
            "clear deep blue night sky full of small stars", "falls forward face down out of the bottom of the frame", NOSMILE],
    "s27": ["medium two-shot in profile", "face to face", "already raised to shoulder height",
            "flies spinning out of his hand up out of the top of the frame", "caked thick and grey-white with lime powder",
            NOSMILE],
    "s27b": ["a full hand's breadth in front of his throat", "caked thick and grey-white with lime powder", NOSMILE],
    "s36": ["his dark hair cropped short at the nape", "staying at the left edge of the frame from the first frame to the last",
            "grey-white lime powder plain across her cheek", NOSMILE],
    "s37": ["filling the whole background to every edge of the frame", "in one breath", "only after the line ends"],
}
GONE = {
    "s09b": ["halfway across the yard", PUSH], "s10": ["already crouching", PUSH],
    "s14": ["toward us the whole shot", PUSH], "s16b": ["at his sides and loosen again", PUSH],
    "s21": ["billow up one after another", PUSH], "s26": ["lunging", "twists aside", "thrust", PUSH],
    "s27": ["knocks it out", PUSH], "s27b": ["at his throat as she speaks", PUSH],
    "s36": ["toward us the whole shot", PUSH], "s37": ["as he speaks, then his lips close", PUSH],
}

hits = []
(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec["shots"].items():
    base = d1jobs[f"{sid}-9371101"]
    d1t = (D1 / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(d1t.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
        hits.append(f"{sid}: the d1 prompt file is not the one sent (sha256)")
    text = d1t
    for old, new in d1spec[sid].get("replace", []):
        if new and new not in text:
            hits.append(f"{sid}: a d1 edit is missing from the base: '{new[:70]}'")
    for pic, sent in d1spec[sid].get("append_pictures", []):
        if not any(r.endswith("/" + pic) for r in base["reference_images"]) or not base["reference_images"][-1].endswith(pic):
            hits.append(f"{sid}: the appended picture {pic} is not the last one sent in d1")
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the prompt: {old[:60]!r}")
        text = text.replace(old, new)
    refs = list(base["reference_images"])
    for r in refs:
        if not pathlib.Path(r).is_file():
            sys.exit(f"no such picture {r}")
    for seed in SEEDS:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": f"{base['title']} fix1", "reference_images": refs,
                    "prompt_file": f"prompts/{pf.name}", "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "seed": seed, "duration_seconds": sp["duration_seconds"], "output_name": f"{sid}-{seed}.mp4",
                    "output_path": str(out / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the", "smile", "teeth"}
for job in jobs:
    jid = job["id"]
    sid = jid.rsplit("-", 1)[0]
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{jid}: '{m.group(0)}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{jid}: {sep!r} occurs {text.count(sep)} times, not once")
    t3 = text.replace("an older man with a short grey beard", "") if sid == "s09b" else text  # d1's extra, not Xu Yan
    for w in ("beard", "stubble", "moustache", "mustache", "shaven", "cinema camera", "fog", "chopper", "sword"):
        if re.search(rf"\b{w}", t3, re.I):
            hits.append(f"{jid}: '{w}'")
    if sid != "s37":
        for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, ""), re.I):
            hits.append(f"{jid}: '{m.group(0)}'")
    if sid in CHANNEL and re.search(r"\b(pools?|ponds?|causeway)\b", text, re.I):
        hits.append(f"{jid}: a pool word on the channel")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame: {who}")
    for s in MUST[sid]:
        if s not in text:
            hits.append(f"{jid}: not there: '{s[:70]}'")
    for old, new in spec["shots"][sid]["replace"]:
        if len(new) > 3 and new != STATIC_S and text.count(new) != 1:
            hits.append(f"{jid}: the fix1 sentence is not there once: '{new[:70]}'")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{jid}: words that should be gone are there: '{s}'")
    if sid in LINE and f"speaks a short Mandarin line, {LINE[sid]}" not in text:
        hits.append(f"{jid}: the line {LINE[sid]} is not there")
    if sid not in LINE and "speaks a short Mandarin line" in text:
        hits.append(f"{jid}: a speaking sentence in a silent shot")
    if text.count(PUSH) != 0 or text.count(STATIC_S) != 1:
        hits.append(f"{jid}: the camera is not static once")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    n = len(names)
    if sid in SPEARSHOTS:
        if names[-1] != "prop-changqiang-l1.png" or f"{SPEAR} {n}> is the one spear in this shot" not in text:
            hits.append(f"{jid}: the spear prop is not the last picture with its sentence")
    elif "prop-changqiang-l1.png" in names:
        hits.append(f"{jid}: a spear picture in a shot without the spear")
    if names != [pathlib.Path(r).name for r in d1jobs[f"{sid}-9371101"]["reference_images"]]:
        hits.append(f"{jid}: pictures differ from d1")
    if job["duration_seconds"] != DUR[sid] or job["seed"] not in SEEDS:
        hits.append(f"{jid}: {job['duration_seconds']} s or seed {job['seed']} wrong")
    want = ("For the target video, <Picture 1> is referenced throughout." if n == 1 else
            "For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are "
            "referenced throughout.")
    if not text.startswith(want):
        hits.append(f"{jid}: the header is not {n} pictures")
    if max(int(x) for x in re.findall(r"<Picture (\d+)>", text)) != n:
        hits.append(f"{jid}: a <Picture N> beyond the {n} sent, or one missing")
if len(jobs) != 20 or set(DUR) != set(spec["shots"]):
    hits.append(f"{len(jobs)} jobs, shots {sorted(spec['shots'])}")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]],
          len((out / j["prompt_file"]).read_text(encoding="utf-8").split()), "words")
print("scan 0")
