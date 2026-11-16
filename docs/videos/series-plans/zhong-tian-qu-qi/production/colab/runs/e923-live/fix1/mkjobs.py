"""e923 fix1: retake.json -> colab-jobs.json, as e922-live/fix1/mkjobs.py (duration_seconds and swap_pictures from spec.json,
every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute output_path, the
bible 拍法 18 negative-noun scan, exit 1 on a hit). Kept from e922: refine-prep.py's two separators ("never the mood. ",
"One continuous shot.") occur exactly once in each prompt; no prompt carries a word that grows writing or opens a fan or a
paper (open/flick/unfold/paint/calligraphy/writing/ink/characters/letter/poem/scroll; only the boilerplate "the emotion
written above" is let through). e923's own checks: s38 sends only Wei Shaoqing's portrait, names no young woman and no Tang
Xiaotang, keeps him leaning forward with no "straightens", and writes the right third as empty wall; s17 sends only the
night-boat set set-chuan-ye-l1 (no person), never names her, writes the bamboo rib, the fog on both sides, "facing straight
away from us" and "just two round buns", and names no door, window, lattice, wall, room, eave or stone lantern; s31 sends
Xu Yan's portrait and angle-a, Wei Shaoqing's portrait and the afternoon inn set, never names Tang Xiaotang, keeps the
paper folded shut with its plain back toward the camera, and carries no smile, amused, grin or laugh.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e923-dh/runpod/live/fix1
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
    if sid == "s38" and (names != ["weishaoqing-portrait-l1.png"] or re.search(r"Tang Xiaotang|young woman|straighten", text)
                         or "right third of the frame stays plain empty wall" not in text
                         or "leaning forward from the first frame" not in text and "bent forward from the first frame" not in text):
        hits.append(f"{job['id']}: a second picture, a woman named, the straightening beat or the empty right third is wrong")
    if sid == "s17" and (names != ["set-chuan-ye-l1.png"] or "Tang Xiaotang" in text
                         or any(s not in text for s in ("split bamboo", "facing straight away from us", "just two round buns",
                                                         "on her left and on her right only drifting fog"))
                         or re.search(r"\b(doors?|doorway|windows?|lattice|walls?|room|eaves?|stone lantern)\b", text, re.I)):
        hits.append(f"{job['id']}: her picture or name is back, an indoor word is in, or the boat clauses are missing")
    if sid == "s31" and (names != ["xuyan-portrait-l1.png", "xuyan-angle-a-l1.png", "weishaoqing-portrait-l1.png",
                                   "set-kezhan-pm-l1.png"]
                         or "Tang Xiaotang" in text
                         or "folded shut, its plain blank back facing up toward the camera" not in text
                         or re.search(r"\b(smil\w*|amused|grin\w*|laugh\w*)\b", text, re.I)):
        hits.append(f"{job['id']}: a picture, her name, the unfolded paper or a smile cue is wrong")
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
