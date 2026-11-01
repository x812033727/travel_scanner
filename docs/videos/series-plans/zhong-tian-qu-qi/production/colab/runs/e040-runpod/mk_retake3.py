"""Third e040 retake after reviewing the 1080p finals: s14, s24, s50, s54, rebuilt by ref2manifest, two seeds each."""
import glob, json, os, subprocess, sys
repo, mk = sys.argv[1], sys.argv[2]
A = os.path.dirname(os.path.abspath(__file__)); R = f"{A}/retake3"; os.makedirs(R, exist_ok=True)
H = f"{repo}/docs/videos/series-plans/zhong-tian-qu-qi/production"
ff = json.load(open(f"{H}/hailuo/ff-dh-e040.json", encoding="utf8"))
SWAP = {
 # Boots and a floor-planted spear in the composition force the full body the shot must not show.
 "s14": [("the spear butt planted on the floor beside her boot", "her hand gripping the upright spear shaft beside her shoulder")],
 # The pinned man and the big villager were unnamed, so the model drew one seated stranger.
 "s24": [("the big villager", "Wang Erniu"), ("the big villager's", "Wang Erniu's")],
 # A named woman brings her face and a second copy of her; the shot is only hands.
 "s54": [("A-ling's slender hands", "a woman's slender hands")],
}
for f in ff:
    for old, new in SWAP.get(f["id"], []):
        f["prompt"] = f["prompt"].replace(old, new)
    if f["id"] in ("s14", "s50"):
        f["refs"] = [r for r in f["refs"] if "set-" not in r]
    if f["id"] == "s24":
        f["refs"] = [r for r in f["refs"] if "set-" not in r] + ["dh-erniu-portrait-t1.png"] + [r for r in f["refs"] if "set-" in r]
    if f["id"] == "s54":
        f["refs"] = [r for r in f["refs"] if "set-" in r]
ff_path = f"{R}/ff.json"
json.dump(ff, open(ff_path, "w", encoding="utf8"), ensure_ascii=False)
env = {**os.environ, "VIDEO_WORKDIR": R}
subprocess.run(["node", mk, f"{H}/hailuo/clips-dh-e040.json", ff_path, "40", R, "--refs", f"{H}/assets/refs-dh", "--only", "s14,s24,s50,s54", "--seed", "400000", "--width", "960", "--height", "544"], check=True, env=env)
FIX = {
 "s14": "The framing stays a medium close-up from the waist up, her face and shoulders large on screen right; her legs and boots are never in the frame; static shot from the first frame to the last.",
 "s24": "The grey-jacketed man lies face down in the dirt with Wang Erniu's knee on his back for the whole shot; Wang Erniu never sits against the wall.",
 "s50": "The framing stays a close-up of his scarred face, head and shoulders filling the frame, from the first frame to the last; his legs and the floor are never in the frame.",
 "s54": "The shot opens directly on this close view: from the first frame to the last the frame holds only two hands, the sleeves and the tea bowl, very large; no face and no whole person is ever in the frame, near or far.",
}
jobs = []
for path in sorted(glob.glob(f"{R}/ref-e040-part*.json")):
    for job in json.load(open(path, encoding="utf8"))["jobs"]:
        sid = job["id"]
        file = f"{R}/{job['prompt_file']}"
        text = open(file, encoding="utf8").read()
        for old, new in SWAP.get(sid, []):
            if old not in text and new not in text:
                sys.exit(f"{sid}: swap did not land: {old}")
        at = text.find("overall_soundscape")
        head = text[:at].rstrip()
        text = head + " " + FIX[sid] + text[len(head):]
        open(file, "w", encoding="utf8", newline="\n").write(text)
        print(sid, [os.path.basename(x.replace(chr(92), "/")) for x in job["reference_images"]])
        for seed in (400000, 400001):
            item = {k: v for k, v in job.items() if k not in ("output_path", "output_name", "prompt_sha256")}
            item.update(id=f"{sid}-{seed}", seed=seed, output_name=f"{sid}-{seed}.mp4")
            jobs.append(item)
json.dump({"jobs": jobs}, open(f"{R}/retake.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(jobs), "jobs")
