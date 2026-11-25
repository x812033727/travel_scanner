"""e930 fix3: retake.json -> colab-jobs.json for s07, as fix1/mkjobs.py (duration_seconds and swap_pictures from spec.json,
every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute output_path, the
bible 拍法 18 negative-noun scan, exit 1 on a hit). Kept from e922-e930: the two separators of refine-prep.py ("never the
mood. ", "One continuous shot.") occur exactly once; no word that grows writing or "open"; nothing hung up or locked (the one
costume phrase "a string of small gold keys" allowed); no smile, grin or laugh word; no weapon word; nobody named who is not
in the frame (only Qin Shuang and Tang Wanjin).
fix3's own checks (the cut-review 中等 1 fix): the pictures are the d1 three (her portrait, his portrait, -men2-l1), 6 s; no
word that puts a hand toward the other person (hold, clasp, grip, take, link, arm in arm, hand in hand, wrist, reach, held
out, across his way) and no "side by side", "shoulder to shoulder" or "facing us"; the fix3 sentences are there once and none
of them is in d1; the d1 sentences that failed ("held out across his way", "not smiling", "facing us") are gone; the line is the
script's sentence, said by her only; the camera holds still (no push).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e930-dh/runpod/live/fix3
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
        p = ROOT / p if r.startswith("docs/") else REFS / p
    if not p.is_file():
        sys.exit(f"{job_id}: no such picture {p}")
    return str(p)


for job in retake["jobs"]:
    spec = shots[job["id"].split("-")[0]]
    if spec.get("duration_seconds"):
        job["duration_seconds"] = spec["duration_seconds"]
    swap = dict(spec.get("swap_pictures", {}))
    refs = []
    for r in job["reference_images"]:
        name = pathlib.Path(r).name
        if name in swap:
            r = swap.pop(name)
        refs.append(absolute(r, job["id"]))
    if swap:
        sys.exit(f"{job['id']}: not among its pictures: {sorted(swap)}")
    job["reference_images"] = refs

ALLOWED = re.compile(r"\bno (talking|mouthing words|second copy of anyone|subtitles, captions or text)\b", re.I)
NEGATION = re.compile(r"\b(no|not an?|without|never an?|nor)\s+([a-z'-]+(?:\s+[a-z'-]+)?)", re.I)
GROWS_TEXT = re.compile(r"\b(open\w*|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|written(?! above)|inscri\w*|ink|"
                        r"characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
HUNG = re.compile(r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|"
                  r"hang\w*|hung|strings?|tassels?|curtains?|firecrackers?|locks?|locked|padlocks?|chains?|stalls?|awnings?)\b", re.I)
COSTUME_OK = "a string of small gold keys"
SMILE = re.compile(r"\b(smil\w*|grin\w*|laugh\w*|beam\w*)\b", re.I)
WEAPON = re.compile(r"\b(blade|axe|sword|spear|scabbard|weapon|dagger|knife|machete|hatchet|cleaver)s?\b", re.I)
TOUCH = re.compile(r"\b(hold(s|ing)? (his|her) (hand|wrist|arm)|clasp\w*|grip\w*|grasp\w*|takes? (his|her)|link\w*|arm in arm|"
                   r"hand in hand|wrists?|reach\w*|held out|across his way|side by side|shoulder to shoulder|facing us)\b", re.I)
PEOPLE = {"Xu Yan": r"Xu Yan", "A-ling": r"A-ling", "Lai San": r"Lai San", "Tang Xiaotang": r"Tang Xiaotang|Xiaotang",
          "Wei Shaoqing": r"Wei Shaoqing|\bWei\b", "Tang Wanjin": r"Tang Wanjin", "Zheng Bo": r"Zheng|steward",
          "Xiaohe": r"Xiaohe", "Qin Shuang": r"Qin Shuang", "Wang Erniu": r"Erniu"}
IN_FRAME = {"Qin Shuang", "Tang Wanjin"}
PICS = ["qinshuang-portrait-l1.png", "tangwanjin-portrait-l1.png", "set-xujia-yuan-dong-men2-l1.png"]
LINE = "Qin Shuang speaks a short Mandarin line, 「小棠，這位老爺是誰？一進門就東張西望」"
FIX3_SENTENCES = [
    "they stand face to face across one full step of bare packed earth",
    "a clear gap of low golden evening light between her shoulder and his from the first frame to the last",
    "her left palm pressed flat against the gatepost at the height of her shoulder",
    "her right fist planted on her hip at her belt",
    "her brows pressed low and drawn together, her eyes narrowed and hard, fixed on his face, her mouth pressed flat between "
    "words, her jaw firm",
    "both his arms straight down at his sides, his hands loose against his thighs",
    "her hands stay on the gatepost and on her hip, his hands stay at his sides",
    "her mouth pressing back into a tight flat line after the last word",
    "and his eyes settle on her face, his arms still at his sides",
    "The camera holds a static shot.",
]
D1_GONE = ["her left arm already held out across his way", "not smiling", "facing us",
           "half a step before him and a little to the side", "The camera pushes in"]
d1_texts = [p.read_text(encoding="utf-8") for p in sorted((D1 / "prompts").glob("ref-*.txt"))]
if not d1_texts:
    sys.exit(f"no d1 prompts under {D1}")
hits = []
for job in retake["jobs"]:
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    jid = job["id"]
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        hits.append(f"{jid}: a negated noun gets drawn (bible 拍法 18): '{m.group(0)}'")
    for rx, what in ((GROWS_TEXT, "a word that grows writing or 'open'"), (SMILE, "a smile word"), (WEAPON, "a weapon word"),
                     (TOUCH, "a word that puts a hand toward the other person or the two side by side")):
        hits += [f"{jid}: {what}: '{m.group(0)}'" for m in rx.finditer(text)]
    hits += [f"{jid}: something hung up, locked or a stall: '{m.group(0)}'" for m in HUNG.finditer(text.replace(COSTUME_OK, ""))]
    hits += [f"{jid}: names someone not in the frame: {who}" for who, pat in PEOPLE.items()
             if who not in IN_FRAME and re.search(pat, text)]
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{jid}: {sep!r} occurs {text.count(sep)} times, not once")
    for s in FIX3_SENTENCES:
        if text.count(s) != 1:
            hits.append(f"{jid}: the fix3 sentence is not there once: '{s}'")
        if any(s in t for t in d1_texts):
            hits.append(f"{jid}: the fix3 sentence is in d1 already: '{s}'")
    hits += [f"{jid}: the failed d1 wording is still there: '{s}'" for s in D1_GONE if s in text]
    if text.count(LINE) != 1 or len(re.findall(r"speaks a short Mandarin line", text)) != 1:
        hits.append(f"{jid}: the line is not Qin Shuang's script sentence once")
    if "Tang Wanjin says nothing in this shot" not in text:
        hits.append(f"{jid}: Tang Wanjin's closed-mouth sentence is missing")
    if re.search(r"\b(push\w*|pan\w*|dolly|zoom\w*|track\w*)\b", text, re.I):
        hits.append(f"{jid}: a camera move (fix3 holds a static shot)")
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if names != PICS or job["duration_seconds"] != 6 or (job["width"], job["height"]) != (960, 544):
        hits.append(f"{jid}: pictures {names}, {job['duration_seconds']} s or {job['width']}x{job['height']} are wrong")
    if not text.startswith("For the target video, <Picture 1>, <Picture 2> and <Picture 3> are referenced throughout."):
        hits.append(f"{jid}: the header is not 3 pictures")
    if max(int(x) for x in re.findall(r"<Picture (\d+)>", text)) != 3:
        hits.append(f"{jid}: a <Picture N> beyond the 3 sent")
if sorted(j["seed"] for j in retake["jobs"]) != [9301401, 9301402]:
    hits.append("seeds are not 9301401/9301402")
if hits:
    sys.exit("scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps(retake, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
jobs = [dict(job, output_path=str(out / "out" / job["output_name"])) for job in retake["jobs"]]
bad = [(j["id"], r) for j in jobs for r in j["reference_images"] if not r.startswith(str(ROOT) + "/")]
bad += [(j["id"], j["output_path"]) for j in jobs if not j["output_path"].startswith("/")]
if bad:
    sys.exit(f"not absolute: {bad}")
(out / "out").mkdir(exist_ok=True)
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json")
for j in jobs:
    print(" ", j["id"], j["seed"], j["duration_seconds"], f"{j['width']}x{j['height']}",
          [pathlib.Path(r).name for r in j["reference_images"]])
print("scan: 0 (negated nouns, open/text, hung-up, smile, weapon, hand-toward/side-by-side words, names not in frame; "
      "separators once; fix3 sentences once and not in d1; failed d1 wording gone; the line once; static camera)")
