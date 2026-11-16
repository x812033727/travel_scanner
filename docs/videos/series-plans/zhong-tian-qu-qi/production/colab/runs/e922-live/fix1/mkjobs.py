"""e922 fix1: retake.json -> colab-jobs.json, as e921-live/fix1/mkjobs.py (duration_seconds and swap_pictures from spec.json,
every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute output_path, the
bible 拍法 18 negative-noun scan, exit 1 on a hit). e922's own checks: refine-prep.py's two separators ("never the mood. ",
"One continuous shot.") occur exactly once in each prompt; no prompt carries a word that grows writing or opens a fan or a
paper (open/flick/unfold/paint/calligraphy/writing/ink/characters/letter/poem/scroll; s32's "the open door" and the
boilerplate "the emotion written above" are the only ones let through); s09 sends only Wei Shaoqing's portrait, never names
Tang Xiaotang, writes him out of focus and drops the "question" cue; s32 sends Qin Shuang's portrait and A-ling's two angles
(no set), keeps the paper folded shut with its plain back to the camera, puts Qin Shuang in the left half, and names no
candle, curtain, bead, string, bulb or lantern (the oil lamp is the one light).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e922-dh/runpod/live/fix1
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
GROWS_TEXT = re.compile(r"\b(open(s|ed|ing)?(?! door)|flick\w*|unfold\w*|paint\w*|calligraph\w*|writ(e|es|ing)|"
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
    if sid == "s09" and (names != ["weishaoqing-portrait-l1.png"] or "Tang Xiaotang" in text or "out of focus" not in text
                         or "question" in text or "appears only once" not in text):
        hits.append(f"{job['id']}: her picture or name is back, he is in focus, the question cue is back or 'only once' "
                    "is gone")
    if sid == "s32" and (names != ["qinshuang-portrait-l1.png", "aling-angle-a-l1.png", "aling-angle-b-l1.png"]
                         or "folded shut, its plain back toward the camera" not in text
                         or "in the left half of the frame Qin Shuang" not in text
                         or re.search(r"\b(candle\w*|curtains?|beads?|strings?|bulbs?|lanterns?)\b", text, re.I)):
        hits.append(f"{job['id']}: a set picture, a second light, an unfolded paper or the left-right placing is wrong")
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
