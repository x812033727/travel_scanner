"""e938 fix1: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (10 shots x seeds
9381301/9381302 = 20 jobs, 118 s). Copied from e937-live/fix1/mkjobs.py: the base of each job is the d1 9381101 job and prompt
exactly as sent (sha256 checked; its reference_images, the appended spear / horse / captain pictures included), every d1 edit of
../spec.json for the shot asserted to be in the base, the fix1 replaces applied once each; s12 sends the pictures spec.json lists
(A-ling's portrait added as picture 2), s22 s27 swap the gate crop for -zha2.

Scans here (exit 1 on a hit): negative nouns, the two separators once, beard / stubble / cinema camera / fog / chopper / sword,
smile words beyond NOSMILE, the pool words outdoors, people named who are not in the frame, the MUST / GONE lists, appended
pictures last with their sentence, static camera once, seconds, seeds, header count. The full per-shot assertions of
check938.py, rewritten for these shots, are in <scratchpad>/tools/check938f1.py (run it after this).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live/fix1
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
assert SEEDS == [9381301, 9381302], SEEDS
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
DUR = {"s01": 6, "s05": 6, "s11": 6, "s12": 8, "s14": 6, "s15": 6, "s15b": 6, "s20": 5, "s22": 5, "s27": 5}
OUTSIDE = {"s20", "s22", "s27"}
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "Tang Xiaotang": r"Xiaotang", "A-ling": r"A-ling|Aling",
          "Xiaohe": r"Xiaohe|Xiao He", "captain": r"guard captain"}
IN_FRAME = {"s01": {"Xu Yan", "Xiaohe"}, "s05": {"Xiaohe"}, "s11": {"Xu Yan"}, "s12": {"Qin Shuang", "A-ling"},
            "s14": {"Xu Yan"}, "s15": {"Xu Yan"}, "s15b": {"Xu Yan"}, "s20": {"A-ling"}, "s22": {"A-ling"},
            "s27": {"A-ling", "captain"}}
LINE = {"s01": "「濕布換了三回，還是燙得嚇人」", "s05": "「哥哥……別下水……哥哥別下水……」",
        "s12": "「馬只有一匹。我不能走，山上還有散掉的流寇」", "s14": "「我不問妳會不會騎。我信妳，馬給妳」"}
GIRL = "a little girl of eight with two little pigtails asleep in it"
MUST = {
    "s01": ["its pillow end at screen right and its foot at screen left", "already lying across her forehead from the first frame",
            "both his knees and both his shins flat on the floorboards", "the only child in the bed", "lying alone in the bed",
            "its wick dark and cold", "framed full figure with both knees on the floor"],
    "s05": ["the pink pillow filling the space on both sides of her head", "the bare plaster wall"],
    "s11": [GIRL, "exactly two people", "Only these 2 people are in the frame"],
    "s12": ["by the shut plank door, A-ling", "exactly two people standing in the room",
            "Only Qin Shuang and A-ling stand in the frame", "the little girl asleep in the bed",
            "toward someone out of sight beyond the right edge of the frame"],
    "s14": [GIRL, NOSMILE, "stays empty to the last frame", "exactly three people"],
    "s15": [GIRL, "exactly two people", "Only these 2 people are in the frame", "shut plank door"],
    "s15b": [GIRL, NOSMILE, "exactly two people", "Only these 2 people are in the frame", "shut plank door"],
    "s20": ["already at a flat-out gallop from the first frame", "never slowing", "from right to left"],
    "s22": ["standing between the horse and the side door", "on the far side of the stakes from the side door",
            "the horse beyond the barrier and the side door on our side of it", "all four hooves staying on the paving"],
    "s27": ["standing between the horse and the side door", "on the far side of the stakes from the side door",
            "on our side of the barrier, at its near end by the torch and the side door",
            "still two strides short of the stakes with all four hooves on the ground", "already at a flat-out gallop"],
}
GONE = {
    "s01": ["soft in the lower foreground", "just above her forehead", PUSH],
    "s05": ["candle", PUSH], "s11": ["candle", "he is the only person in the frame", PUSH],
    "s12": ["over a shoulder", "a man in an old grey cloth outer coat", "the man at the right edge", "exactly three people", PUSH],
    "s14": ["not smiling", "exactly two people", PUSH],
    "s15": ["he is the only person in the frame", "only the plaster wall and the dark blue window", PUSH],
    "s15b": ["he is the only person in the frame", "only the plaster wall and the dark blue window", "not smiling", PUSH],
    "s20": ["already galloping in", PUSH],
    "s22": ["on the road side of the barrier", PUSH],
    "s27": ["on the road side of the barrier", "seen from behind and a little to the side", "beyond the barrier, by the side door",
            "lifting", "forelegs", PUSH],
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
    t3 = text.replace("a short black beard", "").replace("short black beard", "") if sid == "s27" else text  # the captain's
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
