#!/usr/bin/env python3
"""refine-prep.py N PICKS.tsv [PICKS.tsv ...] : stage-2 (refine) jobs for a live-action episode, in its own work folder.

route_a_st23.sh reads the CG folders (runpod/a/st1/out and clips-dh-eNNN.json, whose refine prompts say 3D CG), so the
live episode is refined from ~/mokaair-work/videos/_live-e90N/zhong-tian-qu-qi-e90N-dh/runpod/a instead:
- each picked draft (a review-picks.tsv row whose choice is a seed; later files override earlier ones, so a retake's
  pick replaces the first pick) is copied to st1/out/sNN.mp4, and its source and trim are recorded in picks.json;
- clips-dh-e90N.json is copied with its two 3D CG style sentences turned into live action (the same text pilot.py uses);
- route_a_st2.py then writes st2/st2-*.json with each shot's own draft seed.
The draft files are looked up in runpod/live/{d1,fix1,fix2,...}/out. Prints the h3r.sh refine command to run.
"""
import glob
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[6]
N = int(sys.argv[1])
V = Path.home() / "mokaair-work" / "videos"
LIVE = V / f"zhong-tian-qu-qi-e90{N}-dh" / "runpod" / "live"
W = V / f"_live-e90{N}" / f"zhong-tian-qu-qi-e90{N}-dh" / "runpod" / "a"
(W / "st1" / "out").mkdir(parents=True, exist_ok=True)
picks = {}
for tsv in sys.argv[2:]:
    for line in Path(tsv).read_text(encoding="utf-8").splitlines()[1:]:
        shot, choice, reason = (line.split("\t") + ["", ""])[:3]
        if choice.isdigit():
            trim = dict(re.findall(r"(start|end-before)@([0-9.]+)", reason))
            picks[shot] = {"seed": int(choice), "trim": {k: float(v) for k, v in trim.items()}}
        elif choice == "RETAKE":
            picks.pop(shot, None)
for shot, p in picks.items():
    src = next((f for f in sorted(glob.glob(str(LIVE / "*" / "out" / f"{shot}-{p['seed']}.mp4")))), None)
    if not src:
        sys.exit(f"{shot}: no draft {shot}-{p['seed']}.mp4 under {LIVE}")
    p["draft"] = src
    shutil.copyfile(src, W / "st1" / "out" / f"{shot}.mp4")
(W.parent.parent / "picks.json").write_text(json.dumps(picks, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
STYLE = [("[Shot 1] 3D CG.", "[Shot 1] Photorealistic live-action film footage of real actors in an ancient Chinese (Song-dynasty) period drama, shot on a cinema camera."),
         ("Smooth, weighty 3D CG character animation; faces, hair and costumes stay as in the first frame.",
          "Natural, realistic human motion of real actors; faces, hair and costumes stay as in the first frame.")]
clips = json.loads((REPO / f"docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/clips-dh-e90{N}.json").read_text(encoding="utf-8"))
live = {}
for key, row in clips.items():
    if key.split("-")[1] not in picks:
        continue
    text = row[0]
    for a, b in STYLE:
        text = text.replace(a, b)
    if "3D" in text or "CG" in text:
        sys.exit(f"{key}: a 3D CG mention is left in the refine prompt")
    live[key] = [text] + row[1:]
clips_live = W.parent.parent / f"live-clips-e90{N}.json"
clips_live.write_text(json.dumps(live, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
skip = sorted({k.split("-")[1] for k in clips} - set(picks))
(W / "st2").mkdir(exist_ok=True)
(W / "st2" / "skip.txt").write_text(" ".join(skip) + "\n", encoding="utf-8")
seeds = [f"{s}:{p['seed']}" for s, p in sorted(picks.items())]
subprocess.run([sys.executable, "-I", str(REPO / ".agents/skills/minimax-h3-runpod/scripts/route_a_st2.py"), str(clips_live), str(W), "0", *seeds], check=True)
print(f"{len(picks)} picks staged; not picked yet: {' '.join(skip) or 'none'}")
for m in sorted((W / "st2").glob("st2-*.json")):
    print(f"bash {REPO}/.agents/skills/minimax-h3-runpod/scripts/h3r.sh refine --manifest {m} --output-dir {W}/st2/refined --progress {W}/st2/refined/progress-{m.name}")
