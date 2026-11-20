"""e936 fix1: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (9 shots x seeds
9361211/9361212 = 18 jobs, 124 s). Copied from e935-live/fix1/mkjobs.py (and e935 fix4 for the whole-written s04): the base of
each job is the d1 9361101 job and prompt exactly as sent (sha256 checked), every d1 edit of ../spec.json for the shot asserted
to be in the base (PREP.md section 3), the fix1 replaces applied once each; s04's prompt is spec.json's text with the d1 job.

Scans (exit 1 on a hit): negative nouns, weapon words, the two separators once, words that grow writing or open something,
hung/locked things, smile words beyond NOSMILE, people named who are not in the frame, pool words on the channel, 'cinema
camera', fix1's own MUST / GONE lists, s04 has no name / face / mouth / spoken line, the lines of the speaking shots, static
camera in all nine, pictures, seconds, seeds.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/runpod/live/fix1
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
assert SEEDS == [9361211, 9361212], SEEDS
CHANNEL = {"s18", "s20", "s26", "s28"}

hits = []
(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec["shots"].items():
    base = d1jobs[f"{sid}-9361101"]
    d1t = (D1 / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(d1t.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
        hits.append(f"{sid}: the d1 prompt file is not the one sent (sha256)")
    if "text" in sp:
        text = sp["text"]
        refs = [str(ROOT / p) for p in sp["pictures"]]
    else:
        text = d1t
        for old, new in d1spec[sid].get("replace", []):  # the d1 edits are carried
            if new and new not in text:
                hits.append(f"{sid}: a d1 edit is missing from the base: '{new[:70]}'")
        for old, new in sp["replace"]:
            if text.count(old) != 1:
                sys.exit(f"{sid}: not once in the d1 prompt: {old[:60]!r}")
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
GROWS_TEXT = re.compile(r"\b(open(?!\s+(flat|bare|field|ground))\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|book\w*|ledger\w*)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|hangs|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?|stalls?|awnings?|"
                  r"pavilions?|torch\w*)\b", re.I)
HUNG_OK = {"s01": ["torches", "burning pine torch", "the torch flames"]}
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "A-ling": r"A-ling|Aling", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai",
          "Tang Xiaotang": r"Xiaotang"}
IN_FRAME = {"s01": {"Xu Yan", "A-ling"}, "s04": set(), "s11b": {"Xu Yan"}, "s12b": {"Xu Yan"}, "s18": {"A-ling"},
            "s20": {"Xu Yan", "A-ling"}, "s26": {"Qian Yuanwai"}, "s28": set(), "s31": {"Qin Shuang"}}
PICS = {"s01": ["xuyan-portrait-l1.png", "aling-portrait-l1.png", "set-cunkou-zha2-men-l1.png"],
        "s04": ["set-cunkou-zha2-ding2-l1.png"],
        "s11b": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-cunkou-zha2-kong-l1.png"],
        "s12b": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-cunkou-zha2-wai2-l1.png"],
        "s18": ["aling-portrait-l1.png", "aling-angle-a-l1.png", "set-shanjiao-qu-zhuo2-l1.png"],
        "s20": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "aling-portrait-l1.png", "aling-angle-a-l1.png",
                "set-shanjiao-qu-zhuo2-l1.png"],
        "s26": ["qianyuanwai-portrait-l1.png", "qianyuanwai-angle-a-l1.png", "set-shanjiao-qu-zhuo2-l1.png"],
        "s28": ["set-shanjiao-qu-zhuo2-l1.png"],
        "s31": ["qinshuang-portrait-l1.png", "set-xujia-yuan-ye-dong2-l1.png"]}
DUR = {"s01": 6, "s04": 8, "s11b": 6, "s12b": 6, "s18": 6, "s20": 6, "s26": 10, "s28": 8, "s31": 6}
LINE = {"s12b": "「好，明早天一亮，記名、發鋤頭、開工」", "s20": "「是好字。妳不想說，我就不問」",
        "s26": "「一斗都沒人買？我錢家的米，一夜跌了一半！」"}
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
MUST = {
    "s01": ["shut tight from the first frame to the last", "his feet planted", "wound up inside just two round buns",
            "has lifted the whole thick crossbar clear up out of its iron fitting", "shut tight to the last frame", NOSMILE],
    "s04": ["his broad back square to the camera from the first frame", "he is the only person in the frame",
            "sweeps his flat right hand out from the left across to the right"],
    "s11b": ["gives only the colour of the background", "under the wide evening sky;", "clear sky all around his head", NOSMILE],
    "s12b": ["staying at the right edge of the frame from the first frame to the last", "three-quarter profile", NOSMILE],
    "s18": ["seated in the exact centre of the frame from the first frame to the last",
            "the abacus staying under her right hand the whole shot", "her hands holding only the brush",
            "the only young woman with two high round buns in the frame", NOSMILE],
    "s20": ["one single sheet of blank plain white paper the only things on the bare tabletop", "his eyes on her face", NOSMILE],
    "s26": ["with one loud slam", "bounce up and fall back", NOSMILE],
    "s28": ["exactly one person in the frame", "both his hands empty", "standing empty with nobody at them",
            "much smaller, alone, still walking away"],
    "s31": ["facing the wall, only their backs and the backs of their heads toward us",
            "the three mats in the middle of the row clearly visible, flat and bare",
            "the round stone well stands alone in the front right"],
}
GONE = {
    "s01": ["while the two gate leaves stay closed", PUSH],
    "s04": ["Qian", "face", "mouth", "lips", "speaks", "Mandarin", PUSH],
    "s11b": ["just inside the gate", "keeping its layout", "light of torches", PUSH],
    "s12b": ["toward us the whole shot;", PUSH],
    "s18": ["medium shot from close behind", PUSH],
    "s20": ["a faint easy look", "soft at the lower edge", PUSH],
    "s26": ["slams his flat right hand", PUSH],
    "s28": [PUSH],
    "s31": ["running behind the well", "with their backs to us", PUSH],
}
d1_texts = [p.read_text(encoding="utf-8") for p in sorted((D1 / "prompts").glob("ref-*.txt"))]
for job in jobs:
    jid = job["id"]
    sid = jid.rsplit("-", 1)[0]
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{jid}: '{m.group(0)}'")
    for word in ("axe", "sword", "spear", "scabbard", "weapon", "dagger", "knife", "pickaxe", "mattock", "sickle"):
        if re.search(rf"\b{word}s?\b", text, re.I):
            hits.append(f"{jid}: names '{word}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{jid}: {sep!r} occurs {text.count(sep)} times, not once")
    for m in GROWS_TEXT.finditer(text):
        hits.append(f"{jid}: a word that grows writing or opens something: '{m.group(0)}'")
    t2 = text
    for ok in HUNG_OK.get(sid, []):
        t2 = t2.replace(ok, "")
    for m in HUNG.finditer(t2):
        hits.append(f"{jid}: something hung up, locked, a stall or a torch: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    if "cinema camera" in text:
        hits.append(f"{jid}: 'cinema camera'")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame: {who}")
    if sid in CHANNEL and re.search(r"\b(pools?|ponds?)\b", text, re.I):
        hits.append(f"{jid}: a pool word on the channel")
    for s in MUST[sid]:
        if text.count(s) < 1:
            hits.append(f"{jid}: not there: '{s[:70]}'")
    for old, new in spec["shots"][sid].get("replace", []):
        if text.count(new) != 1:
            hits.append(f"{jid}: the fix1 sentence is not there once: '{new[:70]}'")
        if new != STATIC_S and any(new in t for t in d1_texts):
            hits.append(f"{jid}: the fix1 sentence is already in a d1 prompt: '{new[:70]}'")
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
    if names != PICS[sid] or job["duration_seconds"] != DUR[sid] or job["seed"] not in SEEDS:
        hits.append(f"{jid}: pictures {names}, {job['duration_seconds']} s or seed {job['seed']} wrong")
    n = len(names)
    want = ("For the target video, <Picture 1> is referenced throughout." if n == 1 else
            "For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are "
            "referenced throughout.")
    if not text.startswith(want):
        hits.append(f"{jid}: the header is not {n} pictures")
    if max(int(x) for x in re.findall(r"<Picture (\d+)>", text)) != n:
        hits.append(f"{jid}: a <Picture N> beyond the {n} sent, or one missing")
    if not all(r.startswith(str(ROOT) + "/") for r in job["reference_images"]) or not job["output_path"].startswith("/"):
        hits.append(f"{jid}: a path is not absolute or not under this checkout")
if len(jobs) != 18 or set(DUR) != set(spec["shots"]):
    hits.append(f"{len(jobs)} jobs, shots {sorted(spec['shots'])}")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["seed"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]],
          len((out / j["prompt_file"]).read_text(encoding="utf-8").split()), "words")
print("scan 0")
