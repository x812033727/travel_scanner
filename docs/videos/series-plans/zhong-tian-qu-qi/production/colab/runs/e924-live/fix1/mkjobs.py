"""e924 fix1: retake.json -> colab-jobs.json, as e923-live/fix1/mkjobs.py (duration_seconds and swap_pictures from spec.json,
every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute output_path, the
bible 拍法 18 negative-noun scan, exit 1 on a hit). Kept from e922/e923: refine-prep.py's two separators ("never the mood. ",
"One continuous shot.") occur exactly once in each prompt; no prompt carries a word that grows writing or opens a fan or a
paper (open/flick/unfold/paint/calligraphy/writing/ink/characters/letter/poem/scroll; only the boilerplate "the emotion
written above" is let through). e924's own checks: s17 and s34 send only Xu Yan's portrait, his angle-a and their street
set (no picture of her), never name Tang Xiaotang, write "facing straight away from us" and "just two round buns", and
name nothing that hangs on a post or a wall (sign, board, plaque, banner, flag, pennant, tablet, placard, couplet, lantern,
hanging); s17 keeps him listening with his lips pressed together; s34 writes the grip on his left sleeve and his glance
down at the pouch; s35 sends his two pictures and the Xu shop set, names no young woman, no buns and no "past her", writes
him as the only person, one bowl, and the right third as the soft plank door and the street.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e924-dh/runpod/live/fix1
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("/home/user/zt-work")
REFS = ROOT / "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
out = pathlib.Path(sys.argv[1]).resolve()
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
    refs = []
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
# words that open a fan or a paper, or draw strokes on anything (e921 s28 fan, e922 s30-s33 paper)
GROWS_TEXT = re.compile(r"\b(open(s|ed|ing)?|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
                        r"written(?! above)|inscri\w*|ink|characters?|letters?|poem|scroll\w*|fan face|face of the fan)\b", re.I)
hits = []
for job in retake["jobs"]:
    text = (out / job["prompt_file"]).read_text(encoding="utf-8")
    for m in NEGATION.finditer(ALLOWED.sub("", text)):
        word = m.group(2).split()[0].lower()
        if m.group(1).lower() == "no" and word in NOT_NOUNS:
            continue
        hits.append(f"{job['id']}: '{m.group(0)}'")
    for word in ("blade", "axe", "sword", "knife", "spear", "scabbard", "weapon"):
        if re.search(rf"\b{word}s?\b", text, re.I):
            hits.append(f"{job['id']}: names '{word}'")
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{job['id']}: {sep!r} occurs {text.count(sep)} times, not once")
    for m in GROWS_TEXT.finditer(text):
        hits.append(f"{job['id']}: a word that grows writing or opens the fan or paper: '{m.group(0)}'")
    sid = job["id"].split("-")[0]
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    HUNG = r"\b(signs?|signboards?|boards?|plaques?|banners?|flags?|pennants?|tablets?|placards?|couplets?|lanterns?|hanging|hung)\b"
    if sid in ("s17", "s34") and (names != ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png",
                                            "set-xianjie-shi-l1.png" if sid == "s17" else "set-xianjie-xuji-l1.png"]
                                  or "Tang Xiaotang" in text
                                  or any(s not in text for s in ("facing straight away from us", "just two round buns",
                                                                  "lips pressed together"))
                                  or re.search(HUNG, text, re.I)):
        hits.append(f"{job['id']}: a picture, her name, the back-of-head clauses or a word for something hung up is wrong")
    if sid == "s17" and ("listens to her" not in text or "smooth bare wooden posts" not in text):
        hits.append(f"{job['id']}: the listening or the bare posts are missing")
    if sid == "s34" and ("gripping the cuff of his left sleeve" not in text or "glances down at the cloth pouch" not in text):
        hits.append(f"{job['id']}: the sleeve grip or the glance at the pouch is missing")
    if sid == "s35" and (names != ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "set-xianjie-xuji-l1.png"]
                         or re.search(r"young woman|\bbuns?\b|past her|Tang Xiaotang", text)
                         or "He is the only person in the frame" not in text
                         or "the right third of the frame is only the soft out-of-focus pale plank door" not in text
                         or re.search(HUNG, text, re.I)):
        hits.append(f"{job['id']}: a picture, the young woman, the only-person sentence or the empty right third is wrong")
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
print("negative-noun scan: 0; text-growing words: 0")
