"""e934 fix3: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json, <out>/colab-jobs.json (10 jobs, 84 s).

Base of each job: the job and prompt exactly as sent for the take now in the cut (sha256 checked against that round's
colab-jobs.json), each fix3 replace applied once, the pictures and size as in the base, paths absolute and checked.

Scans (exit 1 on a hit), as fix1/fix2: negative nouns (bible 拍法 18), weapon words, the two refine-prep.py separators once
each, words that grow writing or open something, hung/locked things, smile-bringing words beyond NOSMILE (the base's own
"not smiling" is gone in every shot here), people named who are not in the frame, pool words in the field shots (PREP.md
section 6: s30 s32 s33), the d1 clear sentence once, header and <Picture N>; fix3's own: every fix3 sentence once and in no
earlier prompt, the replaced words gone, the expression (or the clean-shaven face) present AFTER "never the mood. " so that
refine-prep.py carries it into the refine, the line, the camera as in the base, seconds and seeds.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live/fix3
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
CLEAR = "the air is clear and still, a clean natural film image"
SEP = "never the mood. "
FIELD = {"s30", "s32", "s33"}
IN_FRAME = {"s15": {"A-ling", "Xiaohe"}, "s17": {"A-ling"}, "s30": {"Qian Yuanwai"}, "s32": {"Qian Yuanwai"},
            "s33": {"Xu Yan"}}
LINE = {"s15": "「先給下水的人，他們冷。妳拿兩個給哥哥」", "s17": "「妳數慢了。第八片已經上架了，剩四片」",
        "s30": "「我的壩……白守了十天，就這樣沒用了？」", "s32": "「哼，有水算什麼。田裡長不出糧，一樣得求我」", "s33": None}
MOTION_MUST = {"s15": ["her face cold and still", NOSMILE], "s17": ["her face cold and still", NOSMILE],
               "s30": ["the corners of his mouth sagging down", "his face stunned and pale the whole time", NOSMILE],
               "s32": ["his lower lip pushed out and the corners of his mouth dragged down the whole time", NOSMILE],
               "s33": ["his face clean-shaven and smooth", "his lips stay pressed together from the first frame to the last"]}
GONE = {"s15": ["moving clearly", "the person she is speaking to", "not smiling"],
        "s17": ["moving clearly", "not smiling"],
        "s30": ["moving clearly", "shrewd", "frozen stretch", "fans himself", "not smiling"],
        "s32": ["moving clearly", "sour and dark", "his face fallen"],
        "s33": ["stubble", "breath"]}


def here(r: str) -> str:
    p = ROOT / r[r.index("docs/"):]
    if not p.is_file():
        sys.exit(f"no such picture {p}")
    return str(p)


hits, jobs = [], []
(out / "prompts").mkdir(parents=True, exist_ok=True)
for sid, sp in spec["shots"].items():
    src, bseed = sp["base"].split()[0], int(sp["base"].split("-")[-1])
    bjobs = {j["id"]: j for j in json.loads((LIVE / src / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}
    base = bjobs[f"{sid}-{bseed}"]
    text = (LIVE / src / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
        hits.append(f"{sid}: the {src} prompt file is not the one sent (sha256)")
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the base prompt: {old[:60]!r}")
        text = text.replace(old, new)
    refs = [here(r) for r in base["reference_images"]]
    for seed in sp["seeds"]:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": f"zhong-tian-qu-qi-e934 {sid} ref2va fix3", "reference_images": refs,
                    "prompt_file": f"prompts/{pf.name}", "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "seed": seed, "duration_seconds": sp["duration_seconds"], "output_name": f"{sid}-{seed}.mp4",
                    "output_path": str(out / "out" / f"{sid}-{seed}.mp4"), "_base": sp["base"]})
        jobs.append(job)

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"smile", "one", "other", "at", "even", "until", "the"}
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|written(?! above)|inscri\w*|"
                        r"ink|characters?|letters?|poem|scroll\w*)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|tablets?|lanterns?|hanging|hung|hangs|tassels?|"
                  r"curtains?|locks?|padlocks?|chains?|stalls?|awnings?)\b", re.I)
SMILEY = re.compile(r"\b(smil\w*|grin\w*|laugh\w*|smirk\w*|smug\w*|sneer\w*|cheer\w*|pleased|kind|warm(?! golden)|shrewd|"
                    r"gleeful|amused|gritted|relieved)\b", re.I)
SMILE_OK = {"s33": ["relieved, not smiling"]}  # d1 s33's mood (mouth shut, picked: no smile seen), kept as sent
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "A-ling": r"A-ling|Aling", "Xiaohe": r"Xiaohe",
          "Elder Han": r"Elder Han", "Carpenter Shi": r"Carpenter Shi", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai",
          "Tang Xiaotang": r"Xiaotang"}
REUSED = {"small narrow eyes under heavy brows,"}  # fix1 s32's identity words, reused on purpose for s30
old_texts = [p.read_text(encoding="utf-8") for d in ("d1", "fix1", "fix2") for p in sorted((LIVE / d / "prompts").glob("ref-*.txt"))]
for job in jobs:
    jid = job["id"]
    sid = jid.rsplit("-", 1)[0]
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        if m.group(1).lower() == "no" and m.group(2).split()[0].lower() in NOT_NOUNS:
            continue
        if m.group(0).lower().startswith("not smiling") and sid in SMILE_OK:
            continue
        if m.group(0).lower().startswith(("never the", "never looking")):
            continue
        hits.append(f"{jid}: '{m.group(0)}'")
    for w in ("axe", "sword", "spear", "weapon", "dagger", "knife", "sickle"):
        if re.search(rf"\b{w}s?\b", text, re.I):
            hits.append(f"{jid}: names '{w}'")
    for sep in (SEP, "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{jid}: {sep!r} x{text.count(sep)}")
    for m in GROWS_TEXT.finditer(text):
        hits.append(f"{jid}: grows writing or opens something: '{m.group(0)}'")
    for m in HUNG.finditer(text):
        hits.append(f"{jid}: hung/locked: '{m.group(0)}'")
    t2 = text.replace(NOSMILE, "")
    for ok in SMILE_OK.get(sid, []):
        t2 = t2.replace(ok, "")
    for m in SMILEY.finditer(t2):
        hits.append(f"{jid}: a word that brings a smile: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame: {who}")
    if sid in FIELD and re.search(r"\b(pools?|ponds?)\b", text, re.I):
        hits.append(f"{jid}: a pool word in a field shot (PREP.md section 6)")
    if text.count(CLEAR) != 1:
        hits.append(f"{jid}: the d1 clear sentence is not there once")
    motion = text.split(SEP)[1].split("One continuous shot.")[0]
    for s in MOTION_MUST[sid]:
        if s not in motion:
            hits.append(f"{jid}: not in the motion part (refine would lose it): '{s}'")
    for old, new in spec["shots"][sid]["replace"]:
        if new not in text:
            hits.append(f"{jid}: fix3 sentence missing: '{new[:60]}'")
        if new not in REUSED and any(new in t for t in old_texts):
            hits.append(f"{jid}: fix3 sentence already in an earlier prompt: '{new[:60]}'")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{jid}: old words still there: '{s}'")
    if LINE[sid] and f"speaks a short Mandarin line, {LINE[sid]}" not in text:
        hits.append(f"{jid}: the line is not there")
    if LINE[sid] is None and "says nothing in this shot" not in text:
        hits.append(f"{jid}: the silent shot lost 'says nothing'")
    n = len(job["reference_images"])
    want = ("For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are "
            "referenced throughout.")
    if not text.startswith(want) or max(int(x) for x in re.findall(r"<Picture (\d+)>", text)) != n:
        hits.append(f"{jid}: header / <Picture N> does not match the {n} pictures")
if len(jobs) != 10 or len({j['seed'] for j in jobs}) != 10:
    hits.append(f"{len(jobs)} jobs / seeds not unique")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))
for j in jobs:
    j.pop("_base")
(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]])
print("scan 0")
