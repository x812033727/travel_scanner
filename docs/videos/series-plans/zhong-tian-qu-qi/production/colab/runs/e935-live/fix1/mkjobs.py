"""e935 fix1: spec.json -> <out>/prompts/ref-sNN-SEED.txt, <out>/retake.json and <out>/colab-jobs.json (5 shots x seeds
9351211/9351212 = 10 jobs, 76 s). Copied from e934-live/fix1/mkjobs.py: the base of each job is the d1 9351101 job and prompt
exactly as sent (sha256 checked), every d1 edit of ../spec.json for these shots asserted to be in the base (PREP.md section 6),
the fix1 replaces applied once each, picture paths made absolute under this checkout and checked to exist.

Scans (exit 1 on a hit), as e934 fix1: negative nouns, weapon words, the two separators once, words that grow writing or open
something, hung/locked things, smile words beyond NOSMILE, people named who are not in the frame, pool words in the field shots
(s17b, s23), the d1 clean-air sentence once; e935 fix1's own MUST / GONE lists, no line in any of the five (all silent),
static camera in all five, pictures, seconds, seeds.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/runpod/live/fix1
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
assert SEEDS == [9351211, 9351212], SEEDS
FIELD = {"s17b", "s23"}
CLEAR = "a clean natural film image"


def here(r: str) -> str:
    p = ROOT / r[r.index("docs/"):]
    if not p.is_file():
        sys.exit(f"no such picture {p}")
    return str(p)


hits = []
(out / "prompts").mkdir(parents=True, exist_ok=True)
jobs = []
for sid, sp in spec["shots"].items():
    base = d1jobs[f"{sid}-9351101"]
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
HUNG_OK = {}
PEOPLE = {"Xu Yan": r"Xu Yan", "Qin Shuang": r"Qin Shuang", "A-ling": r"A-ling|Aling", "Xiaohe": r"Xiaohe",
          "Elder Han": r"Elder Han", "Carpenter Shi": r"Carpenter Shi", "Qian Yuanwai": r"Qian Yuanwai|Yuanwai",
          "Tang Xiaotang": r"Xiaotang"}
IN_FRAME = {"s01": {"Xu Yan"}, "s17b": set(), "s23": {"Qian Yuanwai"}, "s30": {"Xu Yan"}, "s34": {"Xu Yan", "A-ling"}}
PICS = {"s01": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-xujia-wu-ye-table-l1.png"],
        "s17b": ["set-hantian-yang-zong2-shui-l1.png"],
        "s23": ["qianyuanwai-portrait-l1.png", "qianyuanwai-angle-a-l1.png", "set-hantian-yang-chen2-liu-l1.png"],
        "s30": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-cunkou-zha2-kong-l1.png"],
        "s34": ["xuyan-portrait-l1.png", "aling-portrait-l1.png", "set-cunkou-zha2-men-l1.png"]}
DUR = {"s01": 8, "s17b": 6, "s23": 8, "s30": 10, "s34": 6}
LINE = {}
SILENT = {"s01", "s17b", "s23", "s30", "s34"}
PUSH = "The camera pushes in with small amplitude at slow speed."
STATIC_S = "The camera holds a static shot."
STATIC = {"s01", "s17b", "s23", "s30", "s34"}
MUST = {
    "s01": ["the small window high in the back wall at the upper left of the frame behind him",
            "in the first frame his head is already turned back over his left shoulder",
            "each speck smaller than a fingertip", "He says nothing in this shot", NOSMILE, STATIC_S],
    "s17b": ["all six whole in the frame", "for the first two seconds the six ducks face different ways",
             "all six ducks snap their heads up", STATIC_S],
    "s23": ["with the look of a feature film.", "small narrow eyes under heavy brows", "every strand wound up inside the two buns",
            "his face slowly going slack and sour", "three white farm ducks with white feathers and orange bills",
            "his jaw still, no talking", NOSMILE, STATIC_S],
    "s30": ["gives only the colour of the background", "under the wide evening sky;", "standing out under the wide sky",
            "clear sky all around his head and shoulders", "He says nothing in this shot", NOSMILE, STATIC_S],
    "s34": ["the two round-log gate leaves stay shut from the first frame to the last", "he stops one step before it",
            "at the right edge of the trio", "behind his left shoulder", "standing still one at each end of the crossbar",
            "through the narrow gaps between the gate's logs", NOSMILE, STATIC_S],
}
GONE = {
    "s01": ["small dark shapes", "thumps", "thumping", PUSH],
    "s17b": ["close-up low over the water", "every which way", "hold still", PUSH],
    "s23": ["cinema camera", "shrewd", "smug", PUSH],
    "s30": ["by the gate", "keeping its layout", PUSH],
    "s34": ["stepping aside", "beyond the gate's logs", PUSH],
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
if len(jobs) != 10 or set(DUR) != set(spec["shots"]):
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
      "NOSMILE, lines, static/push, pictures, seconds, seeds 9351211/9351212")
