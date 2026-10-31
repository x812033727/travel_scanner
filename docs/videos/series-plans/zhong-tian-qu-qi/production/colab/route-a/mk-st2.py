#!/usr/bin/env python3
"""mk-st2.py NN [sNN:path/to/draft.mp4:seed ...] : stage-2 manifests for episode NN.

Every shot of the episode's clips-dh list, with its stage-1 draft from st1/out/<id>.mp4 unless an
override names another draft (a retake) and its seed. Writes st2/ff/<id>.png (frame 0 cover-cropped to
1312x736), st2/prompts/<id>.txt (the first-frame body) and st2/st2-<k>.json, twenty jobs at most each.
Shots listed in st2/skip.txt (one id per line) are left out.
"""
import json, os, subprocess, sys
n = sys.argv[1]
ep = f"0{n}"
repo = os.environ.get("REPO") or subprocess.run(["git", "-C", os.path.dirname(os.path.abspath(__file__)), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
A = f"{os.environ.get('VIDEO_WORKDIR') or os.path.expanduser('~/mokaair-work/videos')}/zhong-tian-qu-qi-e{ep}-dh/colab/a"
clips = json.load(open(f"{repo}/docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/clips-dh-e{ep}.json"))
over = {}
for arg in sys.argv[2:]:
    sid, path, seed = arg.split(":")
    over[sid] = (path, int(seed))
os.makedirs(f"{A}/st2/ff", exist_ok=True)
os.makedirs(f"{A}/st2/prompts", exist_ok=True)
skip = set()
if os.path.exists(f"{A}/st2/skip.txt"):
    skip = {l.strip() for l in open(f"{A}/st2/skip.txt") if l.strip()}
jobs = []
for key, (text, _h, _sec) in clips.items():
    sid = key.split("-")[1]
    if sid in skip:
        continue
    draft, seed = over.get(sid, (f"{A}/st1/out/{sid}.mp4", 330000))
    if not os.path.exists(draft):
        sys.exit(f"missing draft {draft}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", draft, "-frames:v", "1", "-vf",
                    "scale=1312:736:force_original_aspect_ratio=increase:flags=lanczos,crop=1312:736", f"{A}/st2/ff/{sid}.png"], check=True)
    open(f"{A}/st2/prompts/{sid}.txt", "w").write(text)
    jobs.append({"id": sid, "input_video": draft, "first_frame": f"ff/{sid}.png", "prompt_file": f"prompts/{sid}.txt",
                 "output_name": f"{sid}.mp4", "sigma_start": 0.5, "steps": 10, "seed": seed, "guide": "none"})
for i in range(0, len(jobs), 20):
    json.dump({"jobs": jobs[i:i + 20]}, open(f"{A}/st2/st2-{i // 20 + 1}.json", "w"), indent=1)
print(len(jobs), "jobs in", (len(jobs) + 19) // 20, "manifests")
