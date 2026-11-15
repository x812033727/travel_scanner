"""e912 fix2: retake.json -> colab-jobs.json (output_path added, as e912 fix1), plus the per-shot duration_seconds of
spec.json (retake.py copies st1's duration; e912 fix2 s22 is bought at 10 s, as st1).

    python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e912-dh/runpod/live/fix2
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
out = pathlib.Path(sys.argv[1])
shots = json.loads((HERE / "spec.json").read_text(encoding="utf-8"))["shots"]
retake = json.loads((out / "retake.json").read_text(encoding="utf-8"))
for job in retake["jobs"]:
    dur = shots[job["id"].split("-")[0]].get("duration_seconds")
    if dur:
        job["duration_seconds"] = dur
(out / "retake.json").write_text(json.dumps(retake, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
jobs = [dict(job, output_path=str(out / "out" / job["output_name"])) for job in retake["jobs"]]
(out / "colab-jobs.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "colab-jobs.json", {j["id"]: j["duration_seconds"] for j in jobs})
