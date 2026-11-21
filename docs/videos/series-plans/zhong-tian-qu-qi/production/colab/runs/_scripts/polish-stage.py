#!/usr/bin/env python3
"""polish-stage.py N REFINED_DIR : put the 2026-11-21 polish retakes of live episode N into the cut, as stage.py does.

For each shot in ~/mokaair-work/videos/_live-e9NN/zhong-tian-qu-qi-e9NN-dh/runpod/polish/picks.json (polish-refine.py):
the refined picture REFINED_DIR/e9NN-sNN.mp4 (1312x736, silent) gets the audio of the picked draft (the lips follow
that voice, owner 2026-11-07) and the pick's trim (start@S / end-before@E, applied to both), and is written as
clips/sNN-t5.mp4. assemble-v4.mjs takes the highest take number, so t5 replaces t1 and any free-fix trim t2 of the old
clip without deleting either (delete t5 to go back). A shot not refined yet is reported and left alone.
"""
import json
import subprocess
import sys
from pathlib import Path

N = int(sys.argv[1])
EP = 900 + N
REFINED = Path(sys.argv[2])
E = Path.home() / "mokaair-work" / "videos" / f"_live-e{EP}" / f"zhong-tian-qu-qi-e{EP}-dh"
picks = json.loads((E / "runpod" / "polish" / "picks.json").read_text(encoding="utf-8"))
done, missing = [], []
for shot, p in sorted(picks.items()):
    pic = REFINED / f"e{EP}-{shot}.mp4"
    if not pic.exists():
        missing.append(shot)
        continue
    start = p["trim"].get("start", 0.0)
    cut = ["-to", f"{p['trim']['end-before']:.3f}"] if "end-before" in p["trim"] else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", *cut, "-i", str(pic),
                    "-ss", f"{start:.3f}", *cut, "-i", p["draft"],
                    "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", str(E / "clips" / f"{shot}-t5.mp4")], check=True)
    done.append(shot)
print(f"e{EP}: staged {' '.join(done) or 'none'}; not refined: {' '.join(missing) or 'none'}")
