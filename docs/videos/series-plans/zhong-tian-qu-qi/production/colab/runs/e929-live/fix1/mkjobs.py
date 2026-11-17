"""e929 fix1: retake.json -> colab-jobs.json, as e928-live/fix1/mkjobs.py (duration_seconds and swap_pictures from
spec.json, every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute
output_path, the bible 拍法 18 negative-noun scan, exit 1 on a hit). Kept from e922-e928: the two separators of
refine-prep.py ("never the mood. ", "One continuous shot.") occur exactly once in each prompt; no word that grows writing
or opens a fan or a paper (no "open" at all); nothing hung up or locked (no lantern, flag, sign, stall word); no smile,
grin or laugh word; no weapon word; no prompt names anyone, since nobody is in either insert. e929's own checks: each
insert sends only its own paper prop picture (s10 prop-liuye-zhi-xin-l1, s11 prop-huangzhi-l1), 6 s; the picture is
named as the prop, not as a set; nothing of the d1 text that invented a place is left (town square, the set layout,
cold clear winter day, real actors, each person, the "shown in <Picture 1> is the set" clause); the sheet fills the
frame from the first frame and reaches past all four edges; no person, hand, finger, snow, market or crowd word. The
fix1 sentences must not be in d1.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e929-dh/runpod/live/fix1
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("/home/user/zt-work")
REFS = ROOT / "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
out = pathlib.Path(sys.argv[1]).resolve()
D1 = out.parent / "d1"
shots = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))["shots"]
retake = json.loads((out / "retake.json").read_text(encoding="utf-8"))


def absolute(r: str, job_id: str) -> str:
    p = pathlib.Path(r)
    if not p.is_absolute():
        p = ROOT / p if r.startswith("docs/") else REFS / p  # a bare name or angles/... is under refs-live
    if not p.is_file():
        sys.exit(f"{job_id}: no such picture {p}")
    return str(p)


for job in retake["jobs"]:
    spec = shots[job["id"].split("-")[0]]
    if spec.get("duration_seconds"):
        job["duration_seconds"] = spec["duration_seconds"]
    swap = dict(spec.get("swap_pictures", {}))
    refs = [absolute(r, job["id"]) for r in spec.get("prepend_pictures", [])]
    for r in job["reference_images"]:
        name = pathlib.Path(r).name
        if name in swap:
            r = swap.pop(name)
        refs.append(absolute(r, job["id"]))
    if swap:
        sys.exit(f"{job['id']}: not among its pictures: {sorted(swap)}")
    if not refs:
        sys.exit(f"{job['id']}: no picture left")
    job["reference_images"] = refs

# bible 拍法 18: a negated object noun gets drawn
ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
NOT_NOUNS = {"bigger", "more", "longer", "larger", "smaller", "one", "other", "at", "even", "until", "the", "smile", "teeth"}
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hanging|hung|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?|stalls?|awnings?)\b", re.I)
PLACE = re.compile(r"\b(town square|square|market\w*|snow\w*|street|courtyard|yard|palace|hall|roofs?|eaves|crowd|people|"
                   r"person|actors?|hands?|fingers?|fingertips?|sleeves?|villagers?|townsfolk|cold clear|set layout|"
                   r"is the set)\b", re.I)
PICS = {"s10": ["prop-liuye-zhi-xin-l1.png"], "s11": ["prop-huangzhi-l1.png"]}
DUR = {"s10": 6, "s11": 6}
PEOPLE = {"Xu Yan": r"Xu Yan", "A-ling": r"A-ling", "Lai San": r"Lai San", "Tang Xiaotang": r"Tang Xiaotang|two buns|pink ribbon",
          "Magistrate Hu": r"Magistrate|\bHu\b", "Sun Zhanggui": r"\bSun\b|Zhanggui|shopkeeper", "Zhao Butou": r"Zhao|constable",
          "Wei Shaoqing": r"Wei Shaoqing|\bWei\b", "Tang Wanjin": r"Tang Wanjin", "Zheng Bo": r"Zheng", "Xiaohe": r"Xiaohe",
          "Qin Shuang": r"Qin Shuang", "Wang Erniu": r"Erniu"}
d1_texts = [p.read_text(encoding="utf-8") for p in sorted((D1 / "prompts").glob("ref-*.txt"))]
if not d1_texts:
    sys.exit(f"no d1 prompts under {D1}")
COMMON = ["The sheet of paper shown in <Picture 1> is the prop, keeping its look.",
          "Initial composition: Against the low slanting winter sun: insert close-up, the very first frame is already "
          "filled edge to edge by one sheet of",
          "the sheet reaches past all four edges of the frame from the first frame to the last",
          "behind the sheet only the bright glow of the low sun shows through the paper itself",
          "The picture fixes the paper only, never the mood.",
          "Natural, realistic motion of the paper in the light: the sheet keeps the look of its reference picture."]
FIX1_SENTENCES = {
    "s10": COMMON + ["so the whole picture is the glowing white paper"],
    "s11": COMMON + ["so the whole picture is the dull yellowish paper"],
}
ACTION = {"s10": "The faint willow-leaf shape in the middle of the sheet shows a little clearer in the light coming through, "
                 "its thin veins showing one by one",
          "s11": "The yellowish sheet trembles a little in the light, the soft lumps and specks showing and nothing else"}
hits = []
for job in retake["jobs"]:
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    sid = job["id"].split("-")[0]
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{job['id']}: '{m.group(0)}'")
    for word in ("blade", "axe", "sword", "spear", "scabbard", "weapon", "dagger", "knife"):
        if re.search(rf"\b{word}s?\b", text, re.I):
            hits.append(f"{job['id']}: names '{word}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{job['id']}: {sep!r} occurs {text.count(sep)} times, not once")
    for m in GROWS_TEXT.finditer(text):
        hits.append(f"{job['id']}: a word that grows writing or opens the paper: '{m.group(0)}'")
    for m in HUNG.finditer(text):
        hits.append(f"{job['id']}: something hung up, locked or a stall: '{m.group(0)}'")
    for m in PLACE.finditer(text):
        hits.append(f"{job['id']}: a place, person or hand word that invents a scene behind the paper: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text, re.I):
        hits.append(f"{job['id']}: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if re.search(pat, text):
            hits.append(f"{job['id']}: names someone not in the frame: {who}")
    for s in FIX1_SENTENCES[sid]:
        if text.count(s) != 1:
            hits.append(f"{job['id']}: the fix1 sentence is not there once: '{s}'")
        if any(s in t for t in d1_texts):
            hits.append(f"{job['id']}: the fix1 sentence leaked into d1: '{s}'")
    if ACTION[sid] not in text or "The camera pushes in with small amplitude at slow speed." not in text:
        hits.append(f"{job['id']}: the d1 action or the slow push is not kept")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS[sid] or job["duration_seconds"] != DUR[sid]:
        hits.append(f"{job['id']}: pictures {names} or {job['duration_seconds']} s are wrong")
    if not text.startswith("For the target video, <Picture 1> is referenced throughout."):
        hits.append(f"{job['id']}: the header is not one picture")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps(retake, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
jobs = [dict(job, output_path=str(out / "out" / job["output_name"])) for job in retake["jobs"]]
bad = [(j["id"], r) for j in jobs for r in j["reference_images"] if not r.startswith(str(ROOT) + "/")]
bad += [(j["id"], j["output_path"]) for j in jobs if not j["output_path"].startswith("/")]
if bad:
    sys.exit(f"not absolute: {bad}")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json")
for j in jobs:
    print(" ", j["id"], j["seed"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]])
print("negative-noun scan: 0; weapon words: 0; text-growing words (open included): 0; hung-up, lock or stall words: 0; "
      "place, person or hand words: 0; smile words: 0; people named: 0; fix1 sentences in d1: 0")
