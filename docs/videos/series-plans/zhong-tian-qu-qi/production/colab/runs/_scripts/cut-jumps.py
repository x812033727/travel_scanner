#!/usr/bin/env python3
"""cut-jumps.py CUT_DIR : hard cuts inside a shot of a finished cut (a flash of another picture at a shot's start or end).

A Ref2VA clip sometimes opens on a different picture for a few frames (the set picture, a wide shot) before it jumps to the
shot, or jumps away in its last frames. One frame from the middle of each shot never shows it; it shows up in the cut as a
flash (e002-r2 s35/s36, e003-r2 s01/s14, found 2026-11-07). This scans every frame of each shot (scaled to 160x90, grey)
and reports any frame-to-frame jump much bigger than the shot's own motion, with its time inside the shot.
Fix: `stage-clips.sh NN sNN@SECS` starts the shot after the jump, or `headtrim.sh`; a jump at the end is trimmed by the cut
only if the shot runs short of it, so retake it or buy it longer. Exit 1 when anything is found.
"""
import re
import statistics
import subprocess
import sys
from pathlib import Path

cut = Path(sys.argv[1])
log = (cut / "final.log").read_text(encoding="utf-8")
shots = [(s, float(a), float(d)) for s, a, d in re.findall(r"^(s\d+[a-z]?) ([\d.]+) \+([\d.]+)s ", log, re.M)]
mp4 = next(p for p in cut.glob("*.mp4") if not p.name.endswith("-phone.mp4"))
w, h = 160, 90
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-vf", f"scale={w}:{h}:flags=area,format=gray", "-f", "rawvideo", "-"],
                     capture_output=True).stdout
fps = 24
n = len(raw) // (w * h)
frame = lambda i: raw[i * w * h:(i + 1) * w * h]
bad = 0
for sid, a, d in shots:
    i0, i1 = int(round(a * fps)) + 1, int(round((a + d) * fps)) - 1  # skip the cut into and out of the shot
    diffs = []
    for i in range(i0 + 1, min(i1, n)):
        x, y = frame(i - 1), frame(i)
        diffs.append((sum(abs(p - q) for p, q in zip(x, y)) / (w * h), i))
    if len(diffs) < 4:
        continue
    med = statistics.median(v for v, _ in diffs)
    for v, i in diffs:
        if v > max(25, 6 * med):
            t = (i - i0) / fps
            where = "start" if t < 0.8 else ("end" if (i1 - i) / fps < 0.8 else "middle")
            print(f"JUMP {sid} at {t:.2f} s into the shot ({where}), diff {v:.0f} vs median {med:.1f}")
            bad += 1
print(f"{cut}: {bad} jump(s)")
sys.exit(1 if bad else 0)
