"""e915 fix1: retake.json -> colab-jobs.json (output_path added, as e914 fix1), plus from spec.json the per-shot
duration_seconds (retake.py copies st1's) and swap_pictures (s08: the shed set picture -> xuyan-angle-a-l1; s26: the
ridged field set picture -> qinshuang-portrait-l1; retake.py cannot add a picture and a job may not go to zero; the prompt
already names the new picture, so prompt_sha256 is unchanged). See mkspec.py.

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e915-dh/runpod/live/fix1
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
out = pathlib.Path(sys.argv[1])
shots = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))["shots"]
retake = json.loads((out / "retake.json").read_text(encoding="utf-8"))
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
                sys.exit(f"{job['id']}: no such picture {new}")
            r = new
        refs.append(r)
    if swap:
        sys.exit(f"{job['id']}: not among its pictures: {sorted(swap)}")
    job["reference_images"] = refs
(out / "retake.json").write_text(json.dumps(retake, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
jobs = [dict(job, output_path=str(out / "out" / job["output_name"])) for job in retake["jobs"]]
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json",
      {j["id"]: (j["duration_seconds"], [pathlib.Path(r).name for r in j["reference_images"]]) for j in jobs})
