"""e934 fix1: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (4 shots x seeds
9341211/9341212 = 8 jobs, 64 s). As e933 fix1: the base of each job is the d1 9341101 job and prompt exactly as sent, the
fix1 replaces applied once each, swap_pictures by file name (s37: set-hantian-hui-tian-l1 -> set-hantian-hui-kong-l1), the
picture paths made absolute under this checkout and checked to exist.

PREP.md section 6 (independent review 建議 6): before anything is replaced, every d1 edit of ../spec.json for these shots is
asserted to be in the base (its new words there, its old words gone): POOLMARK out of the field shots s28, s32, s37, the staff
out of Elder Han's s28 sentence, the GAZE_REFINE sentences, the 'only' sentences, the capitals; and no pool or pond word is in
a field shot after the fix1 replaces (the prep check 「田裡沒有潭字」). None of the four is a clear-air (s01-s03, s34, s38,
s40) or shoes (s12, s19) shot; the scan checks that their clear sentence is the d1 one.

Scans (exit 1 on a hit), kept from e933 fix1: the bible 拍法 18 negative-noun scan; no weapon word; the two separators of
refine-prep.py once each; no word that grows writing or opens something ("open" included); nothing hung or locked (Xiaohe's
"red string" pigtails allowed); no smile word beyond NOSMILE; nobody named who is not in the frame; header and <Picture N>
match the pictures sent; absolute paths that exist. e934 fix1's own: every fix1 sentence there once and none of them in any
d1 prompt; the d1 words they replace gone ("lets out one long breath", "kind face", "warm but firm", "brows lifted",
"shrewd", "gritted teeth", the far hills and the grassy ridge of s37); NOSMILE in all four; the d1 line of every speaking
shot and no line in s09; static camera in s09, s28, s32, the slow push in s37; pictures, seconds and seeds.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live/fix1
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
assert SEEDS == [9341211, 9341212], SEEDS
FIELD = {"s28", "s32", "s37"}
CLEAR = "the air is clear and still, a clean natural film image"


def here(r: str) -> str:
    p = ROOT / r[r.index("docs/"):]
    if not p.is_file():
        sys.exit(f"no such picture {p}")
    return str(p)


hits = []
(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec["shots"].items():
    base = d1jobs[f"{sid}-9341101"]
    text = (D1 / base["prompt_file"]).read_text(encoding="utf-8")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != base["prompt_sha256"]:
        hits.append(f"{sid}: the d1 prompt file is not the one sent (sha256)")
    for old, new in d1spec[sid].get("replace", []):  # PREP.md section 6: the d1 edits are carried
        if new and new not in text:
            hits.append(f"{sid}: a d1 edit is missing from the base: '{new[:70]}'")
        if old and old not in new and old in text:
            hits.append(f"{sid}: d1 words that d1 replaced are back in the base: '{old[:70]}'")
    for old, new in sp["replace"]:
        if text.count(old) != 1:
            sys.exit(f"{sid}: not once in the d1 prompt: {old[:60]!r}")
        text = text.replace(old, new)
    swap = dict(sp.get("swap_pictures", {}))
    refs = []
    for r in base["reference_images"]:
        name = pathlib.Path(r).name
        refs.append(here(swap.pop(name) if name in swap else r))
    if swap:
        sys.exit(f"{sid}: not among its pictures: {sorted(swap)}")
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
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|hangs|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?|stalls?|awnings?)\b",
                  re.I)
HUNG_OK = {"s37": ["tied with red string"]}  # Xiaohe's pigtails (cast sentence since e930)
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "A-ling": r"A-ling|Aling", "Xiaohe": r"Xiaohe",
          "Elder Han": r"Elder Han", "Carpenter Shi": r"Carpenter Shi", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai",
          "Tang Xiaotang": r"Xiaotang"}
IN_FRAME = {"s09": {"Xu Yan"}, "s28": {"Elder Han"}, "s32": {"Qian Yuanwai"}, "s37": {"Xiaohe"}}
PICS = {"s09": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-shentan-bian-l3.png"],
        "s28": ["hanbo-portrait-l1.png", "set-hantian-tian-l1.png"],
        "s32": ["qianyuanwai-portrait-l1.png", "qianyuanwai-angle-a-l1.png", "set-hantian-liu-l1.png"],
        "s37": ["xiaohe-portrait-l1.png", "set-hantian-hui-kong-l1.png"]}
DUR = {"s09": 10, "s28": 8, "s32": 8, "s37": 6}
LINE = {"s28": "「許先生，老頭子替全村，給您磕個頭」", "s32": "「哼，有水算什麼。田裡長不出糧，一樣得求我」",
        "s37": "「哥……北邊的天，怎麼一下子黑了？」"}
SILENT = {"s09"}
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
STATIC = {"s09", "s28", "s32"}
MUST = {
    "s09": ["He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still",
            "Xu Yan shuts his eyes for a moment, then turns his face slowly toward the big grey boulder",
            "the corners of his mouth press down;", "lips pressed together in one flat line", NOSMILE, STATIC_S],
    "s28": ["grave steady eyes", "framed from his knees up", "the corners of his mouth turned down",
            "his lips staying turned down on every word", "By the last word Elder Han has bowed low",
            "his two hands slid forward off his knees onto the grass", "all of him still in the frame", NOSMILE, STATIC_S],
    "s32": ["small narrow eyes under heavy brows", "already walking away toward the right edge of the frame from the first frame",
            "his back three-quarter to the camera", "his eyes on the field beyond the lower left edge of the frame, looking back",
            "By the last word Qian Yuanwai has walked on into the right third of the frame",
            "in the first second he gives his right sleeve one sharp shake", "the corners of his mouth pulled down", NOSMILE,
            STATIC_S],
    "s37": ["the darkening grey sky shown in <Picture 2> gives only the colour of the background",
            "seen from far below, sitting up high",
            "the darkening grey sky filling the whole frame behind her from the top edge to the bottom edge",
            "her left hand below the bottom edge of the frame holding the little paper pinwheel down there",
            "her eyes on the upper right corner of the frame, never the lens",
            "By the middle of the line Little Xiaohe's right arm is stretched out straight toward the upper right corner",
            NOSMILE, PUSH],
}
GONE = {
    "s09": ["lets out one long breath", "breath", PUSH],
    "s28": ["kind face", "warm but firm", "brows lifted", "medium close-up", "framed from the waist up",
            "bends slowly forward from the waist toward the ground to bow", "walking staff", PUSH],
    "s32": ["shrewd", "gritted teeth", "already turning away", "gives his sleeve one sharp shake, walks away", PUSH],
    "s37": ["far hills", "grassy ridge", "cracked furrows", "is the set, keeping its layout", "already lowered in her left hand",
            "its vanes still", "stretches her flat right hand out"],
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
        hits.append(f"{jid}: something hung up, locked or a stall: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text.replace(NOSMILE, ""), re.I):
        hits.append(f"{jid}: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{jid}: names someone not in the frame: {who}")
    if sid in FIELD and re.search(r"\b(pools?|ponds?)\b", text, re.I):
        hits.append(f"{jid}: a pool word in a field shot (PREP.md section 6)")
    if text.count(CLEAR) != 1:
        hits.append(f"{jid}: the d1 clear sentence is not there once")
    for s in MUST[sid]:
        if text.count(s) != 1:
            hits.append(f"{jid}: not there once: '{s[:70]}'")
    for old, new in spec["shots"][sid]["replace"]:
        if text.count(new) != 1:
            hits.append(f"{jid}: the fix1 sentence is not there once: '{new[:70]}'")
        if new != STATIC_S and any(new in t for t in d1_texts):
            hits.append(f"{jid}: the fix1 sentence is already in a d1 prompt: '{new[:70]}'")
    for s in GONE[sid]:
        if s in text:
            hits.append(f"{jid}: d1 words still there: '{s}'")
    if sid in LINE and f"speaks a short Mandarin line, {LINE[sid]}" not in text:
        hits.append(f"{jid}: the line {LINE[sid]} is not there")
    if sid in SILENT and "speaks a short Mandarin line" in text:
        hits.append(f"{jid}: a speaking sentence in a silent shot")
    if text.count(PUSH) != (0 if sid in STATIC else 1) or text.count(STATIC_S) != (1 if sid in STATIC else 0):
        hits.append(f"{jid}: the camera is not as planned")
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
if len(jobs) != 8 or set(DUR) != set(spec["shots"]):
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
print("scan 0: d1 edits carried (PREP 6), no pool word in the field, negative nouns, weapons, separators, text-growing (open), "
      "hung/lock, smile words, people not in frame, headers, paths; fix1 sentences once and not in d1, replaced d1 words gone, "
      "NOSMILE, lines, static/push, pictures, seconds, seeds 9341211/9341212")
