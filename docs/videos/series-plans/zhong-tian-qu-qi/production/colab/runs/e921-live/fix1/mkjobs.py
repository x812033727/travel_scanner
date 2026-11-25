"""e921 fix1: retake.json -> colab-jobs.json, as e920-live/fix1/mkjobs.py (duration_seconds and swap_pictures from spec.json,
every reference_images entry an absolute path under /home/user/zt-work/ and checked to exist, an absolute output_path, the
bible 拍法 18 negative-noun scan, exit 1 on a hit). e921's own checks replace e920's: refine-prep.py's two separators
("never the mood. ", "One continuous shot.") occur exactly once in each prompt; s28 never opens or flicks the fan and names
no fan face, painting, writing or calligraphy; s36 sends no picture of Wei Shaoqing, names him nowhere and writes the
gathered topknot; s37 sends only Wei Shaoqing's portrait (no set picture) and writes the raised threshold from below.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e921-dh/runpod/live/fix1
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
    if sid == "s28" and re.search(r"\b(opens?|opening|flicks?|unfold\w*|fan face|face of the fan|leaf|leaves|paint\w*|writing|"
                                  r"calligraph\w*|characters?|inscri\w*|poem)\b", text, re.I):
        hits.append(f"{job['id']}: a word that opens the fan or draws on it is back")
    if sid == "s36" and ("Wei Shaoqing" in text or any(n.startswith("weishaoqing-") for n in names) or
                         "topknot high on the crown" not in text):
        hits.append(f"{job['id']}: Wei Shaoqing is named or pictured, or the gathered topknot is missing")
    if sid == "s37" and (names != ["weishaoqing-portrait-l1.png"] or "raised dark wooden threshold" not in text or
                         "tall dark wooden shelves" in text):
        hits.append(f"{job['id']}: a set picture or the shop interior is back, or the threshold framing is missing")
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
