"""e920 fix1: retake.json -> colab-jobs.json, as e919-live/fix1/mkjobs.py (duration_seconds and swap_pictures from spec.json,
every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute output_path, the
bible 拍法 18 negative-noun scan, exit 1 on a hit). e920's own checks replace e919's: refine-prep.py's two separators
("never the mood. ", "One continuous shot.") occur exactly once in each prompt; s23 names no book, volume, cover, slip or
title; s33 names A-ling nowhere and sends no A-ling picture; s37b carries no palm-sized or five-rod abacus and sends the
prop picture prop-jinsuanpan-l1 (and no set picture).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e920-dh/runpod/live/fix1
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
        p = ROOT / p if r.startswith("docs/") else REFS / p  # a bare name or angles/... is under refs-live (e919 d1 swaps)
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
    # e920 fix1: refine-prep.py's separators, and the words that drew the faults in d1 must be gone
    for sep in ("never the mood. ", "One continuous shot."):
        if text.count(sep) != 1:
            hits.append(f"{job['id']}: {sep!r} occurs {text.count(sep)} times, not once")
    sid = job["id"].split("-")[0]
    names = [pathlib.Path(r).name for r in job["reference_images"]]
    if sid == "s23" and re.search(r"\b(books?|volumes?|covers?|slips?|titles?|labels?|thread-bound|stitch\w*|pages?)\b", text, re.I):
        hits.append(f"{job['id']}: a book word is back")
    if sid == "s33" and ("A-ling" in text or any(n.startswith("aling-") for n in names)):
        hits.append(f"{job['id']}: A-ling is named or pictured")
    if sid == "s37b" and (re.search(r"size of her palm|five thin gold rods|two looped buns", text) or
                          "prop-jinsuanpan-l1.png" not in names or any(n.startswith("set-") for n in names)):
        hits.append(f"{job['id']}: the small abacus or the long ribbons are back, or the prop picture is missing")
if hits:
    sys.exit("negative-noun scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps(retake, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
jobs = [dict(job, output_path=str(out / "out" / job["output_name"])) for job in retake["jobs"]]
bad = [(j["id"], r) for j in jobs for r in j["reference_images"] if not r.startswith(str(ROOT) + "/")]
bad += [(j["id"], j["output_path"]) for j in jobs if not j["output_path"].startswith("/")]
if bad:
    sys.exit(f"not absolute: {bad}")
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json")
for j in jobs:
    print(" ", j["id"], j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]])
print("negative-noun scan: 0")
