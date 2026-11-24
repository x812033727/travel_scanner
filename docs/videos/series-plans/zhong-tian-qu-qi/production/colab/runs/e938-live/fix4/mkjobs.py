"""e938 fix4: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (3 shots x seeds
9381601/9381602 = 6 jobs, 38 s). Copied from ../fix3/mkjobs.py; the base of each job is the job and prompt exactly as sent for the
take now in the cut (spec "base": s09 / s17 d1 9381102, s22 fix2 9381401; sha256 checked; reference_images unchanged, the appended
spear / horse pictures included), each fix4 replace applied once.

Scans as fix1-fix3 (exit 1 on a hit): negation nouns, the separators once, forbidden words, smiles, pool words outdoors, people
named who are not in the frame, the sentences that must be there / must be gone, the line, the camera move of the base once,
pictures and their numbered sentences, the header.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live/fix4
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
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = spec["seeds"]
assert SEEDS == [9381601, 9381602], SEEDS
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
DUR = {"s09": 8, "s17": 6, "s22": 5}
CAM = {"s09": PUSH, "s17": PUSH, "s22": STATIC_S}
OUTSIDE = {"s22"}
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "Tang Xiaotang": r"Xiaotang", "A-ling": r"A-ling|Aling",
          "Xiaohe": r"Xiaohe|Xiao He", "captain": r"guard captain"}
IN_FRAME = {"s09": {"Qin Shuang", "Xu Yan"}, "s17": {"Qin Shuang"}, "s22": {"A-ling"}}
LINE = {"s09": "「縣城宵禁了。昨夜流寇下山，天一黑城門就關」", "s17": "「那是騎兵上馬的法子，不是剛學的」"}
MUST = {
    "s09": ["the pink quilt drawn over the small shape of the little girl asleep in it", "with the little girl asleep in the bed behind them, soft",
            "Only Qin Shuang and Xu Yan stand in the frame"],
    "s17": ["serious and wary: eyes narrowed", NOSMILE],
    "s22": ["two full body-lengths beyond the far side of the barrier", "the whole barrier between the camera and the horse",
            "none of them touching it", "nearer to the camera than the horse", NOSMILE],
}
GONE = {
    "s09": ["Only these 2 people are in the frame"],
    "s17": ["seeing it clearly, not smiling"],
    "s22": ["the barrier's top rail passing in front of its chest", "the crossed stakes standing in front of all four of its legs"],
}
APPENDED = {"prop-changqiang-l1.png": "The long spear shown in <Picture {n}> is the one spear in this shot",
            "prop-zaohongma-l1.png": "The horse shown in <Picture {n}> is the one horse in this shot",
            "duizhang-portrait-l1.png": "The guard captain looks exactly like <Picture {n}>"}

hits = []
(out / "prompts").mkdir(parents=True, exist_ok=True)
(out / "out").mkdir(parents=True, exist_ok=True)
jobs, bases = [], {}
for sid, sp in spec["shots"].items():
    r, bseed = sp["base"]
    bj = {j["id"]: j for j in json.loads((LIVE / r / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}[f"{sid}-{bseed}"]
    bases[sid] = bj
    bt = (LIVE / r / bj["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(bt.encode("utf-8")).hexdigest() != bj["prompt_sha256"]:
        hits.append(f"{sid}: the {r} {bseed} prompt file is not the one sent (sha256)")
    text = bt
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the prompt: {old[:60]!r}")
        text = text.replace(old, new)
    refs = list(bj["reference_images"])
    for x in refs:
        if not pathlib.Path(x).is_file():
            sys.exit(f"no such picture {x}")
    for seed in SEEDS:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in bj.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": f"{bj['title'].replace(' fix1', '').replace(' fix2', '')} fix4", "reference_images": refs,
                    "prompt_file": f"prompts/{pf.name}", "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "seed": seed, "duration_seconds": sp["duration_seconds"], "output_name": f"{sid}-{seed}.mp4",
                    "output_path": str(out / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone(?: or of the horse)?|subtitles, captions or text)\b", re.I)
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
    for w in ("beard", "stubble", "moustache", "mustache", "shaven", "cinema camera", "fog", "chopper", "sword", "blade",
              "table", "lamp", "leap", "jump", "rear"):
        if re.search(rf"\b{w}", text, re.I):
            hits.append(f"{jid}: '{w}'")
    if "with the look of a feature film." not in text:
        hits.append(f"{jid}: the style sentence")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, "").replace("not smiling", ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    if sid in OUTSIDE and re.search(r"\b(pools?|ponds?|deep pool)\b", text, re.I):
        hits.append(f"{jid}: a pool word outdoors")
    if sid not in OUTSIDE and re.search(r"\b(flame|lit candle)\b", text, re.I):
        hits.append(f"{jid}: a flame in the daytime sickroom")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame: {who}")
    for s in MUST[sid]:
        if s not in text:
            hits.append(f"{jid}: not there: '{s[:70]}'")
    for old, new in spec["shots"][sid]["replace"]:
        if text.count(new) != 1:
            hits.append(f"{jid}: the fix4 sentence is not there once: '{new[:70]}'")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{jid}: words that should be gone are there: '{s}'")
    if sid in LINE and f"speaks a short Mandarin line, {LINE[sid]}" not in text:
        hits.append(f"{jid}: the line {LINE[sid]} is not there")
    if sid not in LINE and "speaks a short Mandarin line" in text:
        hits.append(f"{jid}: a speaking sentence in a silent shot")
    other = PUSH if CAM[sid] == STATIC_S else STATIC_S
    if text.count(CAM[sid]) != 1 or other in text:
        hits.append(f"{jid}: the camera move is not the base's, once")
    names = [pathlib.Path(x).name for x in job["reference_images"]]
    n = len(names)
    if names != [pathlib.Path(x).name for x in bases[sid]["reference_images"]]:
        hits.append(f"{jid}: pictures {names} differ from the base")
    app = [x for x in names if x in APPENDED]
    if names[n - len(app):] != app:
        hits.append(f"{jid}: an appended picture is not last: {names}")
    for x in app:
        if APPENDED[x].format(n=names.index(x) + 1) not in text:
            hits.append(f"{jid}: the sentence of {x} is not there with its number")
    if job["duration_seconds"] != DUR[sid] or job["seed"] not in SEEDS:
        hits.append(f"{jid}: {job['duration_seconds']} s or seed {job['seed']} wrong")
    want = ("For the target video, <Picture 1> is referenced throughout." if n == 1 else
            "For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are "
            "referenced throughout.")
    if not text.startswith(want):
        hits.append(f"{jid}: the header is not {n} pictures")
    nums = [int(x) for x in re.findall(r"<Picture (\d+)>", text.split("\n", 1)[1])]
    if max(nums) != n or set(nums) != set(range(1, n + 1)):
        hits.append(f"{jid}: <Picture N> in the text are {sorted(set(nums))}, {n} sent")
if len(jobs) != 6 or set(DUR) != set(spec["shots"]):
    hits.append(f"{len(jobs)} jobs, shots {sorted(spec['shots'])}")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["duration_seconds"], [pathlib.Path(x).name for x in j["reference_images"]],
          len((out / j["prompt_file"]).read_text(encoding="utf-8").split()), "words")
print("scan 0")
