"""e934 fix2: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (s28 seeds
9341311/9341312 on fix1 9341212; s32 seeds 9341313/9341314 on fix1 9341211; 8 s each = 4 jobs, 32 s). The base of each job
is the fix1 job and prompt exactly as sent (sha256 checked against fix1/colab-jobs.json), each fix2 replace applied once,
the pictures as in fix1, paths absolute under this checkout and checked to exist.

PREP.md section 6 (independent review 建議 6): before anything is replaced, every d1 edit of ../spec.json and every fix1
replace of ../fix1/spec.json for these shots is asserted to be in the base (new words there, old words gone): POOLMARK out
(both are field shots), s28's staff out, the GAZE_REFINE and 'only' sentences, the capitals; and no pool or pond word after
the fix2 replaces (「田裡沒有潭字」). s26's XQ swap does not touch s28/s32; neither is a clear-air (s01-s03, s34, s38, s40) or
shoes (s12, s19) shot, so the scan checks that the clear sentence is the d1 one and no shoes sentence is there.

Scans (exit 1 on a hit), kept from fix1: the bible 拍法 18 negative-noun scan; no weapon word; the two refine-prep.py
separators once each; no word that grows writing or opens something; nothing hung or locked; no smile word beyond NOSMILE
(and no smug/sneer/grin/smirk/cheerful/pleased/kind/warm word); nobody named who is not in the frame; header and <Picture N>.
fix2's own: every fix2 sentence once and none of them in any d1 or fix1 prompt; the fix1 words they replace gone
("moving clearly", "By the last word Elder Han", "short and portly with a round face" in the composition, "his face in
profile", "his face fallen", "looking back down to the lower left"); the kept fix1 sentences still there (frame, static
camera, brows, the bow's result; s32's staging); in s28 the bow's result comes before the speaking-to-the-grass words;
lines, pictures, seconds and seeds.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live/fix2
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
FIX1 = out.parent / "fix1"
spec = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))
d1spec = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]
fix1spec = json.loads((HERE.parent / "fix1" / "spec.json").read_text(encoding="utf-8"))["shots"]
fix1jobs = {j["id"]: j for j in json.loads((FIX1 / "colab-jobs.json").read_text(encoding="utf-8"))["jobs"]}
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
BASE = {"s28": 9341212, "s32": 9341211}
SEEDS = {"s28": [9341311, 9341312], "s32": [9341313, 9341314]}
CLEAR = "the air is clear and still, a clean natural film image"


def here(r: str) -> str:
    p = ROOT / r[r.index("docs/"):]
    if not p.is_file():
        sys.exit(f"no such picture {p}")
    return str(p)


hits = []
(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
assert set(spec["shots"]) == set(BASE), sorted(spec["shots"])
for sid, sp in spec["shots"].items():
    assert sp["seeds"] == SEEDS[sid] and sp["duration_seconds"] == 8, (sid, sp["seeds"], sp["duration_seconds"])
    base = fix1jobs[f"{sid}-{BASE[sid]}"]
    text = (FIX1 / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
        hits.append(f"{sid}: the fix1 prompt file is not the one sent (sha256)")
    for label, edits in (("d1", d1spec[sid].get("replace", [])), ("fix1", fix1spec[sid]["replace"])):
        for old, new in edits:  # PREP.md section 6: the earlier edits are carried
            if new and new not in text and not (label == "d1" and any(new in o for o, _ in fix1spec[sid]["replace"])):
                hits.append(f"{sid}: a {label} edit is missing from the base: '{new[:70]}'")
            if old and old not in new and old in text:
                hits.append(f"{sid}: {label} words that {label} replaced are back in the base: '{old[:70]}'")
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the fix1 prompt: {old[:60]!r}")
        text = text.replace(old, new)
    refs = [here(r) for r in base["reference_images"]]
    for seed in sp["seeds"]:
        pf = out / "prompts" / f"ref-{sid}-{seed}.txt"
        pf.write_text(text, encoding="utf-8")
        job = {k: v for k, v in base.items() if k != "output_path"}
        job.update({"id": f"{sid}-{seed}", "title": base["title"].replace(" fix1", "") + " fix2", "reference_images": refs,
                    "prompt_file": f"prompts/{pf.name}", "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "seed": seed, "duration_seconds": 8, "output_name": f"{sid}-{seed}.mp4",
                    "output_path": str(out / "out" / f"{sid}-{seed}.mp4")})
        jobs.append(job)

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the", "smile", "teeth"}
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|hangs|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?|stalls?|awnings?)\b",
                  re.I)
HUNG_OK = {"s28": ["cheeks slack and hanging", "cheeks hanging"], "s32": ["cheeks hanging flat"]}  # fix2's slack cheeks
SMILEY = re.compile(r"\b(smil\w*|grin\w*|laugh\w*|smirk\w*|smug\w*|sneer\w*|cheer\w*|pleased|kind|warm(?! golden)|"
                    r"shrewd|gleeful|amused|gritted)\b", re.I)
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "A-ling": r"A-ling|Aling", "Xiaohe": r"Xiaohe",
          "Elder Han": r"Elder Han", "Carpenter Shi": r"Carpenter Shi", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai",
          "Tang Xiaotang": r"Xiaotang"}
IN_FRAME = {"s28": {"Elder Han"}, "s32": {"Qian Yuanwai"}}
PICS = {"s28": ["hanbo-portrait-l1.png", "set-hantian-tian-l1.png"],
        "s32": ["qianyuanwai-portrait-l1.png", "qianyuanwai-angle-a-l1.png", "set-hantian-liu-l1.png"]}
LINE = {"s28": "「許先生，老頭子替全村，給您磕個頭」", "s32": "「哼，有水算什麼。田裡長不出糧，一樣得求我」"}
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
MUST = {
    "s28": ["a worn, grieving old face", "grave steady eyes", "framed from his knees up",
            "brows drawn up together in the middle", "the corners of his mouth turned down",
            "his mouth parting only a little on each word under the white moustache", "his upper teeth covered",
            "his cheeks slack and hanging", "his lips trembling",
            "By the middle of the line Elder Han has already bowed low",
            "his two hands slid forward off his knees onto the grass", "all of him still in the frame",
            "he says the last words with his face turned down toward the grass", "eyes on the spot beyond the upper right",
            NOSMILE, STATIC_S],
    "s32": ["small narrow eyes under heavy brows", "round face",
            "already walking away toward the right edge of the frame from the first frame",
            "his back three-quarter to the camera",
            "we see only the side of his face past his right shoulder: his ear, his cheek and the tip of his moustache",
            "his lower lip pushed out in a sulk", "the corners of his mouth dragged down hard",
            "his eyes narrowed under the heavy brows", "his cheeks hanging flat and heavy", "his nostrils flared",
            "his eyes on the field below the lower left edge of the frame, cast down toward it",
            "By the last word Qian Yuanwai has walked on into the right third of the frame",
            "in the first second he gives his right sleeve one sharp shake", NOSMILE, STATIC_S],
}
GONE = {
    "s28": ["moving clearly", "By the last word Elder Han", "as he starts to bow", "kind face", "warm but firm",
            "brows lifted", "walking staff", "a deeply lined face", PUSH],
    "s32": ["short and portly with a round face and a thin eight-shaped moustache, in his",
            "his face in profile", "his face fallen", "sour and dark:", "looking back down to the lower left",
            "pulled down hard", "shrewd", "gritted teeth", PUSH],
}
old_texts = [p.read_text(encoding="utf-8") for d in (D1, FIX1) for p in sorted((d / "prompts").glob("ref-*.txt"))]
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
        hits.append(f"{jid}: something hung up, locked or a stall: '{m.group(0)}'")
    for m in SMILEY.finditer(text.replace(NOSMILE, "")):
        hits.append(f"{jid}: a word that brings a smile: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame: {who}")
    if re.search(r"\b(pools?|ponds?)\b", text, re.I):
        hits.append(f"{jid}: a pool word in a field shot (PREP.md section 6)")
    if text.count(CLEAR) != 1 or "cloth shoes" in text:
        hits.append(f"{jid}: the d1 clear sentence is not there once, or a shoes sentence is there")
    for s in MUST[sid]:
        if text.count(s) != 1:
            hits.append(f"{jid}: not there once: '{s[:70]}'")
    for old, new in spec["shots"][sid]["replace"]:
        if text.count(new) != 1:
            hits.append(f"{jid}: the fix2 sentence is not there once: '{new[:70]}'")
        if any(new in t for t in old_texts):
            hits.append(f"{jid}: the fix2 sentence is already in a d1 or fix1 prompt: '{new[:70]}'")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{jid}: old words still there: '{s}'")
    if sid == "s28" and text.index("has already bowed low") > text.index("he says the last words with his face turned down"):
        hits.append(f"{jid}: the bow's result is not before the last words")
    if f"speaks a short Mandarin line, {LINE[sid]}" not in text:
        hits.append(f"{jid}: the line {LINE[sid]} is not there")
    if text.count(STATIC_S) != 1 or PUSH in text:
        hits.append(f"{jid}: the camera is not static")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS[sid] or job["duration_seconds"] != 8 or job["seed"] not in SEEDS[sid]:
        hits.append(f"{jid}: pictures {names}, {job['duration_seconds']} s or seed {job['seed']} wrong")
    n = len(names)
    want = ("For the target video, " + ", ".join(f"<Picture {i}>" for i in range(1, n)) + f" and <Picture {n}> are "
            "referenced throughout.")
    if not text.startswith(want):
        hits.append(f"{jid}: the header is not {n} pictures")
    if max(int(x) for x in re.findall(r"<Picture (\d+)>", text)) != n:
        hits.append(f"{jid}: a <Picture N> beyond the {n} sent, or one missing")
    if not all(r.startswith(str(ROOT) + "/") for r in job["reference_images"]) or not job["output_path"].startswith("/"):
        hits.append(f"{jid}: a path is not absolute or not under this checkout")
if len(jobs) != 4:
    hits.append(f"{len(jobs)} jobs")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps({"jobs": [{k: v for k, v in j.items() if k != "output_path"} for j in jobs]},
                                            ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", f"({sum(j['duration_seconds'] for j in jobs)} s)")
for j in jobs:
    print(" ", j["id"], j["seed"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]],
          len((out / j["prompt_file"]).read_text(encoding="utf-8").split()), "words")
print("scan 0: d1 and fix1 edits carried (PREP 6), no pool word, clear sentence d1, negative nouns, weapons, separators, "
      "text-growing, hung/lock, smile-bringing words, people not in frame, headers, paths; fix2 sentences once and not in "
      "d1/fix1, replaced words gone, kept sentences there, s28 result first, NOSMILE, lines, static, pictures, 8 s, seeds "
      "9341311-9341314")
