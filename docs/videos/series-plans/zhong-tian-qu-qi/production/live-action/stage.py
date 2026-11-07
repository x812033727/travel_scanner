#!/usr/bin/env python3
"""stage.py N : put a live-action episode's refined shots where assemble-v4.mjs reads them, with the model's own voice.

For each shot in ~/mokaair-work/videos/_live-e90N/zhong-tian-qu-qi-e90N-dh/picks.json (written by refine-prep.py):
the refined picture (…/runpod/a/st2/refined/sNN.mp4, silent) gets the audio of the draft it was refined from (the
lips follow that voice, owner 2026-11-07), and the pick's trim (start@S / end-before@E, applied to both) is cut in.
Writes ~/mokaair-work/videos/_live-e90N/zhong-tian-qu-qi-e90N-dh/clips/sNN-t1.mp4, and links the episode's recorded
audio/ (system, off-screen and inner lines) and music/ next to it, so the live cut is assembled in that folder with
VIDEO_WORKDIR=~/mokaair-work/videos/_live-e90N and clip_voice: true.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

N = int(sys.argv[1])
V = Path.home() / "mokaair-work" / "videos"
E = V / f"_live-e90{N}" / f"zhong-tian-qu-qi-e90{N}-dh"
CG = V / f"zhong-tian-qu-qi-e90{N}-dh"
picks = json.loads((E / "picks.json").read_text(encoding="utf-8"))
(E / "clips").mkdir(exist_ok=True)
for name in ("audio", "music"):
    if not (E / name).exists():
        os.symlink(CG / name, E / name)
done = missing = 0
for shot, p in sorted(picks.items()):
    pic = E / "runpod" / "a" / "st2" / "refined" / f"{shot}.mp4"
    if not pic.exists():
        print(f"{shot}: not refined yet"); missing += 1; continue
    start = p["trim"].get("start", 0.0)
    cut = ["-to", f"{p['trim']['end-before']:.3f}"] if "end-before" in p["trim"] else []
    # a crop from the pick is given on the 960x544 draft; the refined picture is 1312x736, so it is scaled to match
    vf = []
    if p.get("crop"):
        w, h, x, y = (int(v) for v in p["crop"].split(":")); k = 1312 / 960
        vf = ["-vf", f"crop={round(w * k)}:{round(h * k)}:{round(x * k)}:{round(y * k)},scale=1312:736:flags=lanczos,setsar=1"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", *cut, "-i", str(pic),
                    "-ss", f"{start:.3f}", *cut, "-i", p["draft"],
                    "-map", "0:v", "-map", "1:a?", *vf, "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", str(E / "clips" / f"{shot}-t1.mp4")], check=True)
    done += 1
print(f"staged {done}, not refined {missing} -> {E / 'clips'}")
