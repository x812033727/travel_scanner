"""e938 fix3: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (2 shots x seeds
9381501/9381502 = 4 jobs, 24 s). Copied from ../fix1/mkjobs.py: the base of each job is the d1 9381101 job and prompt exactly as
sent (sha256 checked; its reference_images, the appended horse / captain pictures included), every d1 edit of ../spec.json for the
shot asserted to be in the base, the fix3 replaces applied once each; the set crop swapped for -zhahou (s25) / -zhamen (s26).

Scans as fix1 (exit 1 on a hit). The full per-shot assertions of check938.py, rewritten for these shots, are in
<scratchpad>/tools/check938f3.py (run it after this).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live/fix3
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
D1 = out.parent / "d1"
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
d1spec = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
d1jobs = {j["id"]: j for j in json.loads((D1 / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
SEEDS = spec["seeds"]
assert SEEDS == [9381501, 9381502], SEEDS
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
DUR = {"s25": 6, "s26": 6}
OUTSIDE = {"s25", "s26"}
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "Tang Xiaotang": r"Xiaotang", "A-ling": r"A-ling|Aling",
          "Xiaohe": r"Xiaohe|Xiao He", "captain": r"guard captain"}
IN_FRAME = {"s25": {"A-ling"}, "s26": {"captain"}}
LINE = {"s25": "「家裡的妹妹燒了一整天，讓開」", "s26": "「再往前一步，就當流寇拿下！」"}
MUST = {
    "s25": ["running across the whole bottom of the frame in front of us", "nearer to the camera than the horse",
            "the top rail of the barrier passing in front of the horse's chest", "beyond the barrier the whole shot",
            "close behind the horse", "toward someone out of sight beyond the left edge of the frame", NOSMILE],
    "s26": ["running across the whole bottom of the frame in front of him", "nearer to the camera than he is",
            "standing on the side-door side of the barrier, just behind its stakes", "the swung-out small side door of studded planks at the left",
            "toward someone out of sight beyond the right edge of the frame", NOSMILE],
}
GONE = {
    "s25": ["the road back the way she came", "torchlit barrier", "not smiling", PUSH],
    "s26": ["the tops of the crossed stakes soft along the bottom", "standing behind the barrier,", "not smiling", PUSH],
}
APPENDED = {"prop-changqiang-l1.png": "The long spear shown in <Picture {n}> is the one spear in this shot",
            "prop-zaohongma-l1.png": "The horse shown in <Picture {n}> is the one horse in this shot",
            "duizhang-portrait-l1.png": "The guard captain looks exactly like <Picture {n}>"}

hits = []
(out / "prompts").mkdir(parents=True, exist_ok=True)
(out / "out").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec["shots"].items():
    base = d1jobs[f"{sid}-9381101"]
    d1t = (D1 / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(d1t.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
        hits.append(f"{sid}: the d1 prompt file is not the one sent (sha256)")
    text = d1t
    for old, new in d1spec[sid].get("replace", []):
        if new and new not in text:
            hits.append(f"{sid}: a d1 edit is missing from the base: '{new[:70]}'")
    for pic, sent in d1spec[sid].get("append_pictures", []):
        if not any(r.endswith("/" + pic) for r in base["reference_images"]):
            hits.append(f"{sid}: the appended picture {pic} was not sent in d1")
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the prompt: {old[:60]!r}")
        text = text.replace(old, new)
    refs = list(base["reference_images"])
    for k, v in sp.get("swap_pictures", {}).items():
        hit = [i for i, r in enumerate(refs) if r.rsplit("/", 1)[1] == k]
        assert len(hit) == 1, (sid, k)
        refs[hit[0]] = str(L / v)
    if "pictures" in sp:
        refs = [str(L / n) for n in sp["pictures"]]
    for r in refs:
        if not pathlib.Path(r).is_file():
            sys.exit(f"no such picture {r}")
    for seed in SEEDS:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": f"{base['title']} fix3", "reference_images": refs,
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
    t3 = text.replace("a short black beard", "").replace("short black beard", "") if sid == "s26" else text  # the captain's
    for w in ("beard", "stubble", "moustache", "mustache", "shaven", "cinema camera", "fog", "chopper", "sword", "blade",
              "table", "lamp"):
        if re.search(rf"\b{w}", t3, re.I):
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
    for old, new in spec["shots"][sid]["replace"]:
        if len(new) > 3 and new != STATIC_S and text.count(new) != 1:
            hits.append(f"{jid}: the fix3 sentence is not there once: '{new[:70]}'")
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
    want_names = spec["shots"][sid].get("pictures") or [
        spec["shots"][sid].get("swap_pictures", {}).get(x, x) for x in
        (pathlib.Path(r).name for r in d1jobs[f"{sid}-9381101"]["reference_images"])]
    if names != want_names:
        hits.append(f"{jid}: pictures {names} are not {want_names}")
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
if len(jobs) != 4 or set(DUR) != set(spec["shots"]):
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
