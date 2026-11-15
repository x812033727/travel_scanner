"""e915 fix2: retake.json -> colab-jobs.json (output_path added), as fix1/mkjobs.py: duration_seconds and swap_pictures from
spec.json (s21: set-qiutian-l2 -> the prop picture; s26: Tang's portrait slot -> the prop picture, the set slot -> Qin's
portrait as in fix1; retake.py cannot add a picture). The prop picture refs-live/prop-quyuanli-l1.png may not exist yet
when this runs (the coordinator copies the screen-test pick in before the Colab run): it is then reported, not refused,
and q-e915fix2.sh refuses to start without it. Every other swapped picture must exist.

Also the bible 拍法 18 scan: no prompt may negate an object noun ("no blade", "not a sword", "without a scabbard" ...).
The allowed negations are the fixed sentences every prompt carries (no talking, no mouthing words, no second copy of
anyone, no subtitles, captions or text). Exit 1 on a hit.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e915-dh/runpod/live/fix2
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
out = pathlib.Path(sys.argv[1])
shots = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))["shots"]
retake = json.loads((out / "retake.json").read_text(encoding="utf-8"))
PROP_NAME = "prop-quyuanli-l1.png"
missing_prop = []
for job in retake["jobs"]:
    spec = shots[job["id"].split("-")[0]]
    if spec.get("duration_seconds"):
        job["duration_seconds"] = spec["duration_seconds"]
    swap = dict(spec.get("swap_pictures", {}))
    refs = []
    for r in job["reference_images"]:
        name = pathlib.Path(r).name
        if name in swap:
            new = swap.pop(name)
            if not pathlib.Path(new).is_file():
                if pathlib.Path(new).name != PROP_NAME:
                    sys.exit(f"{job['id']}: no such picture {new}")
                missing_prop.append(job["id"])
            r = new
        refs.append(r)
    if swap:
        sys.exit(f"{job['id']}: not among its pictures: {sorted(swap)}")
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
    for word in ("blade", "axe", "sword", "knife", "spear", "scabbard", "weapon", "crescent", "sickle", "ploughshare"):
        if re.search(rf"\b{word}s?\b", text, re.I):
            hits.append(f"{job['id']}: names '{word}'")
if hits:
    sys.exit("negative-noun scan:\n  " + "\n  ".join(hits))

(out / "retake.json").write_text(json.dumps(retake, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
jobs = [dict(job, output_path=str(out / "out" / job["output_name"])) for job in retake["jobs"]]
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json",
      {j["id"]: (j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]]) for j in jobs})
print("negative-noun scan: 0")
if missing_prop:
    print(f"NOTE: refs-live/{PROP_NAME} is not there yet ({', '.join(missing_prop)}); copy the screen-test pick in before the run")
