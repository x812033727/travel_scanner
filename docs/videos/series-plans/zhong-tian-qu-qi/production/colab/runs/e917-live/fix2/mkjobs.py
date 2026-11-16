"""e917 fix2: retake.json -> colab-jobs.json, as ../fix1/mkjobs.py (duration_seconds and swap_pictures from spec.json, every
reference_images entry an absolute path under /home/user/zt-work/, an absolute output_path), with two changes taken from
e915-live/fix2/mkjobs.py:
- the loose-hair picture refs-live/angles/aling-loose-angle-a-l1.png may not exist yet (the coordinator copies the screen-test
  pick in before the Colab run): it is then reported with a WARNING, not refused, and q-e917fix2.sh refuses to start without
  it. Every other picture must exist.
- the bible 拍法 18 scan: no prompt may negate an object noun ("no bun", "without a pin" ...); the allowed negations are the
  fixed sentences every prompt carries. Exit 1 on a hit.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e917-dh/runpod/live/fix2
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("/home/user/zt-work")
REFS = ROOT / "docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
LOOSE_NAME = "aling-loose-angle-a-l1.png"
out = pathlib.Path(sys.argv[1]).resolve()
shots = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))["shots"]
retake = json.loads((out / "retake.json").read_text(encoding="utf-8"))
missing_loose = []


def absolute(r: str, job_id: str) -> str:
    p = pathlib.Path(r)
    if not p.is_absolute():
        p = ROOT / p if "/" in r else REFS / p  # a bare file name is a refs-live picture
    if not p.is_file():
        if p.name != LOOSE_NAME:
            sys.exit(f"{job_id}: no such picture {p}")
        missing_loose.append(job_id)
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
    # A-ling's own clauses (each runs from "A-ling" to the next ";" or "."): her hair is written only as what is there
    for clause in re.findall(r"\bA-ling\b[^.;]*", text):
        for word in ("bun", "knot", "topknot", "hairpin", "pin", "hair stick", "ornament"):
            if re.search(rf"\b{word}s?\b", clause, re.I):
                hits.append(f"{job['id']}: A-ling's clause names '{word}'")
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
if missing_loose:
    print(f"WARNING: refs-live/angles/{LOOSE_NAME} is not there yet ({', '.join(missing_loose)}); "
          "copy the screen-test pick in before the run (q-e917fix2.sh stops without it)")
