"""e939 fix4: spec.json -> <out>/prompts/ref-s40b-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (s40b x seeds
9391601/9391602 = 2 jobs, 10 s). As ../fix3/mkjobs.py: the job's fields come from the d1 s35 job (sha256 of its prompt checked),
the whole text from spec.json, the pictures spec.json lists (Xu Yan's portrait and angle-a from the base job, the whole
barn-front picture from refs-live).

Scans here (exit 1 on a hit): negative nouns, the two separators once, beard / stubble / cinema camera / fog / chopper / sword /
blade / table / lamp / hat / villagers / crowd / open, smile words beyond NOSMILE / not smiling, the pool words, people named who
are not in the frame, the grey coat (on A-ling since s23), the MUST / GONE lists, the static camera, seconds, seeds, header count.
The full assertions of check939.py, rewritten for this shot, are in <scratchpad>/tools/check939f4.py (run it after this).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live/fix4
"""
import hashlib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[8]
assert (ROOT / "AGENTS.md").is_file(), ROOT
L = HERE.parents[3] / "assets" / "refs-live"
out = pathlib.Path(sys.argv[1]).resolve()
LIVE = out.parent
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
SEEDS = spec["seeds"]
assert SEEDS == [9391601, 9391602], SEEDS
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
CAMERA = {"s40b": STATIC_S}
DUR = {"s40b": 5}
NJOBS = 2 * len(DUR)
OUTSIDE = {"s40b"}
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "A-ling": r"A-ling|Aling", "Xiaohe": r"Xiaohe|Xiao He",
          "captain": r"guard captain", "Doctor Bai": r"Doctor Bai", "Qian Yuanwai": r"Qian Yuanwai", "Diao Qi": r"Diao Qi",
          "Elder Han": r"Elder Han", "Wang Erniu": r"Erniu"}
IN_FRAME = {"s40b": {"Xu Yan"}}
LINE = {}
MUST = {
    "s40b": ["exactly seven people, the six people of the village seen only from behind",
             "Only Xu Yan and the six people of the village seen from behind are in the frame",
             "all six turn their heads together toward the right edge of the frame, clearly and at the same moment",
             "every one of them still turned away from the camera",
             "comes into the frame from the right edge along the strip of trampled earth",
             "stops a few paces from them in the right part of the frame", "his face three-quarter to screen left", NOSMILE,
             "pale white lime powder dusted over the lower half of the robe", "Xu Yan says nothing in this shot",
             "never the mood. ", "dark doorway"],
}
GONE = {"s40b": ["outer coat", "speaks a short Mandarin line", PUSH]}
APPENDED = {}

hits = []
(out / "prompts").mkdir(parents=True, exist_ok=True)
(out / "out").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec["shots"].items():
    rnd, bsid, bseed = sp["base"]
    base = {j["id"]: j for j in json.loads((LIVE / rnd / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}[f"{bsid}-{bseed}"]
    bt = (LIVE / rnd / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(bt.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
        hits.append(f"{sid}: the base prompt file {rnd} {bsid}-{bseed} is not the one sent (sha256)")
    if "text" in sp:
        text = sp["text"]
    else:
        text = bt
        for old, new in sp["replace"]:
            if text.count(old) != 1:
                sys.exit(f"{sid}: not once in the prompt: {old[:60]!r}")
            text = text.replace(old, new)
    refs = list(base["reference_images"])
    if "pictures" in sp:
        byname = {r.rsplit("/", 1)[1]: r for r in base["reference_images"]}
        refs = [byname.get(n, str(L / n)) for n in sp["pictures"]]
    for r in refs:
        if not pathlib.Path(r).is_file():
            sys.exit(f"no such picture {r}")
    for seed in SEEDS:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        title = base["title"].replace(f" {bsid} ", f" {sid} ").replace(" fix1", "")
        job.update({"id": f"{sid}-{seed}", "title": f"{title} fix4", "reference_images": refs,
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
    for w in ("beard", "stubble", "moustache", "mustache", "shaven", "cinema camera", "fog", "chopper", "sword", "blade",
              "table", "lamp", "hat", "villagers", "crowds?", "open"):
        if re.search(rf"\b{w}\b", text, re.I):
            hits.append(f"{jid}: '{w}'")
    if "with the look of a feature film." not in text:
        hits.append(f"{jid}: the style sentence")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, "").replace("not smiling", ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    if sid in OUTSIDE and re.search(r"\b(pools?|ponds?|deep pool)\b", text, re.I):
        hits.append(f"{jid}: a pool word outdoors")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame: {who}")
    for s in MUST[sid]:
        if s not in text:
            hits.append(f"{jid}: not there: '{s[:70]}'")
    for old, new in spec["shots"][sid].get("replace", []):
        if text.count(new) != 1:
            hits.append(f"{jid}: the fix4 sentence is not there once: '{new[:70]}'")
    for s in GONE[sid]:
        if re.search(rf"\b{re.escape(s)}\b", text):
            hits.append(f"{jid}: words that should be gone are there: '{s}'")
    if sid in LINE and f"speaks a short Mandarin line, {LINE[sid]}" not in text:
        hits.append(f"{jid}: the line {LINE[sid]} is not there")
    if sid not in LINE and "speaks a short Mandarin line" in text:
        hits.append(f"{jid}: a speaking sentence in a silent shot")
    other = PUSH if CAMERA[sid] == STATIC_S else STATIC_S
    if text.count(CAMERA[sid]) != 1 or text.count(other) != 0:
        hits.append(f"{jid}: the camera is not {CAMERA[sid]!r} once")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    n = len(names)
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
if len(jobs) != NJOBS or set(DUR) != set(spec["shots"]):
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
