"""Second retake round for e040: fixed pictures per shot, rebuilt by ref2manifest, two seeds each."""
import glob, json, os, subprocess, sys
repo, mk = sys.argv[1], sys.argv[2]
A = os.path.dirname(os.path.abspath(__file__)); R = f"{A}/retake2"; os.makedirs(R, exist_ok=True)
H = f"{repo}/docs/videos/series-plans/zhong-tian-qu-qi/production"
ff = json.load(open(f"{H}/hailuo/ff-dh-e040.json", encoding="utf8"))
for f in ff:
    if f["id"] in ("s13", "s14", "s47"):
        f["refs"] = [r for r in f["refs"] if "set-" not in r]
    if f["id"] == "s36":
        f["refs"] = [r for r in f["refs"] if "set-" not in r] + ["dh-tangxiaotang-portrait-t2.png"] + [r for r in f["refs"] if "set-" in r]
ff_path = f"{R}/ff.json"
json.dump(ff, open(ff_path, "w", encoding="utf8"), ensure_ascii=False)
env = {**os.environ, "VIDEO_WORKDIR": R}
subprocess.run(["node", mk, f"{H}/hailuo/clips-dh-e040.json", ff_path, "40", R, "--refs", f"{H}/assets/refs-dh", "--only", "s13,s14,s36,s47", "--seed", "400000", "--width", "960", "--height", "544"], check=True, env=env)
FIX = {
 "s13": "Both his hands stay bound behind his back; he kicks the bowl with one foot. The framing stays a close-up of his scarred face from the first frame to the last.",
 "s14": "The framing stays a medium close-up of her from the waist up, large in the frame, from the first frame to the last; static shot.",
 "s47": "Both his hands stay bound behind his back and the bowl stays on the floor below the frame, its steam drifting across his face. The framing stays a close-up of his face from the first frame to the last; static shot.",
}
jobs = []
for path in sorted(glob.glob(f"{R}/ref-e040-part*.json")):
    for job in json.load(open(path, encoding="utf8"))["jobs"]:
        sid = job["id"]
        file = f"{R}/{job['prompt_file']}"
        text = open(file, encoding="utf8").read()
        if sid in FIX:
            at = text.find("overall_soundscape")
            head = text[:at].rstrip()
            text = head + " " + FIX[sid] + text[len(head):]
            open(file, "w", encoding="utf8", newline="\n").write(text)
        print(sid, len(job["reference_images"]), [os.path.basename(x.replace(chr(92), "/")) for x in job["reference_images"]])
        for seed in (400000, 400001):
            item = {k: v for k, v in job.items() if k not in ("output_path", "output_name", "prompt_sha256")}
            item.update(id=f"{sid}-{seed}", seed=seed, output_name=f"{sid}-{seed}.mp4")
            jobs.append(item)
json.dump({"jobs": jobs}, open(f"{R}/retake.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(jobs), "jobs")
