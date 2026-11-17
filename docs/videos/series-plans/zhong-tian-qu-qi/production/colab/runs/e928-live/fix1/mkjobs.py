"""e928 fix1: retake.json -> colab-jobs.json, as e926-live/fix1/mkjobs.py (duration_seconds and swap_pictures from
spec.json, every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute
output_path, the bible 拍法 18 negative-noun scan, exit 1 on a hit). Kept from e922-e926: the two separators of
refine-prep.py ("never the mood. ", "One continuous shot.") occur exactly once in each prompt; no word that grows writing
or opens a fan or a paper (no "open" at all); nothing that hangs on a post or a wall; no smile, grin or laugh word; no
prompt names anyone who is not in the frame. e928's own checks: the only weapon is A-ling's short knife "sheathed in plain
dark wood" (no blade, sword, scabbard or drawn knife); s07 names nobody, sends only the lane set, ties the man's crossed
wrists behind his back with grey-white sleeved hands from the upper edge; s26 sends the unlocked set-dalao-bi-l1 and keeps
Xu Yan on the near side of the bars, the left edge a dark wall; s03 keeps the stick in the man's fists and lands it one
arm's length to her right while she stands still; all three hold a static camera. The fix1 sentences must not be in d1.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e928-dh/runpod/live/fix1
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
                  r"hanging|hung|strings?|tassels?|curtains?|firecrackers?|locks?|padlocks?|chains?)\b", re.I)
PICS = {"s03": ["aling-veil-portrait-l1.png", "set-chouduan-ye-xiang-l2.png"],
        "s07": ["set-chouduan-ye-xiang-l2.png"],
        "s26": ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-dalao-bi-l1.png"]}
DUR = {"s03": 6, "s07": 6, "s26": 6}
PEOPLE = {"Xu Yan": r"Xu Yan", "A-ling": r"A-ling", "Lai San": r"Lai San", "Tang Xiaotang": r"Tang Xiaotang|two buns|pink ribbon",
          "Magistrate Hu": r"Magistrate|\bHu\b", "Sun Zhanggui": r"\bSun\b|Zhanggui|shopkeeper", "Zhao Butou": r"Zhao|constable",
          "Wei Shaoqing": r"Wei Shaoqing|\bWei\b", "Xiaohe": r"Xiaohe", "Qin Shuang": r"Qin Shuang", "Wang Erniu": r"Erniu"}
IN_FRAME = {"s03": {"A-ling"}, "s07": set(), "s26": {"Xu Yan"}}
d1_texts = [p.read_text(encoding="utf-8") for p in sorted((D1 / "prompts").glob("ref-*.txt"))]
if not d1_texts:
    sys.exit(f"no d1 prompts under {D1}")
FIX1_SENTENCES = {
    "s03": ["one step beyond her down the lane, right of centre", "the whole stick plain to see in his two fists",
            "bounces once in his hands", "A-ling stands still, her feet planted"],
    "s07": ["close shot from behind and a little above one thin man", "crossed behind his back at the small of his back",
            "reach down into the frame from its upper edge", "tie one tight knot round the man's crossed wrists"],
    "s26": ["wide shot from the cold dark side of the jail gate", "on the near side of the bars in the cold blue night",
            "from him to the left edge of the frame only the dark night wall",
            "he stays on the dark near side of the bars the whole shot"],
}
hits = []
for job in retake["jobs"]:
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    sid = job["id"].split("-")[0]
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{job['id']}: '{m.group(0)}'")
    for word in ("blade", "axe", "sword", "spear", "scabbard", "weapon", "unsheathed", "dagger", "drawn knife"):
        if re.search(rf"\b{word}s?\b", text, re.I):
            hits.append(f"{job['id']}: names '{word}'")
    for m in re.finditer(r"\bknife\b", text):
        if not text[m.start():].startswith("knife sheathed in plain dark wood"):
            hits.append(f"{job['id']}: a knife that is not sheathed: '{text[m.start():m.start() + 40]}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{job['id']}: {sep!r} occurs {text.count(sep)} times, not once")
    for m in GROWS_TEXT.finditer(text):
        hits.append(f"{job['id']}: a word that grows writing or opens the fan or paper: '{m.group(0)}'")
    for m in HUNG.finditer(text):
        hits.append(f"{job['id']}: something hung up or locked: '{m.group(0)}'")
    for m in re.finditer(r"\b(smil\w*|grin\w*|laugh\w*)\b", text, re.I):
        hits.append(f"{job['id']}: '{m.group(0)}'")
    for who, pat in PEOPLE.items():
        if who not in IN_FRAME[sid] and re.search(pat, text):
            hits.append(f"{job['id']}: names someone not in the frame: {who}")
    for s in FIX1_SENTENCES[sid]:
        if s not in text:
            hits.append(f"{job['id']}: the fix1 sentence is missing: '{s}'")
        if any(s in t for t in d1_texts):
            hits.append(f"{job['id']}: the fix1 sentence leaked into d1: '{s}'")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS[sid] or job["duration_seconds"] != DUR[sid]:
        hits.append(f"{job['id']}: pictures {names} or {job['duration_seconds']} s are wrong")
    if "The camera holds a static shot." not in text or "pushes in" in text:
        hits.append(f"{job['id']}: the camera is not static")
    if sid == "s07" and (not text.startswith("For the target video, <Picture 1> is referenced throughout.")
                         or "exactly one man seen from behind and two grey-white sleeved hands" not in text
                         or re.search(r"\b(she|her)\b", text, re.I)):
        hits.append(f"{job['id']}: the tied wrists, the hands or the count are wrong")
    if sid == "s26" and ("filling the frame from edge to edge" in text or "beyond the bars, Xu Yan" in text
                         or "never the lens" not in text):
        hits.append(f"{job['id']}: the gate or Xu Yan's side of it is wrong")
    if sid == "s03" and ("sways aside" in text or "two steps beyond her" in text or "nobody is hit" not in text
                         or "her back three-quarter to us from the first frame to the last" not in text):
        hits.append(f"{job['id']}: the stick, the distance or her back are wrong")
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
print("negative-noun scan: 0; weapon words: 0; text-growing words (open included): 0; hung-up or lock words: 0; "
      "smile words: 0; people not in the frame: 0; fix1 sentences in d1: 0")
