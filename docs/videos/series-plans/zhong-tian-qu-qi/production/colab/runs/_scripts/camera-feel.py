#!/usr/bin/env python3
"""camera-feel.py VIDEO [VIDEO ...] : the camera-feel-study-20261105 measures for a clip or a cut.

Every 0.25 s one frame, scaled to 96x54 grey, top 80 % only (burnt-in subtitles stay out), and the
mean absolute difference of neighbouring frames:
- cut: a difference >= CUT (25 for our renders, as in the study) is a hard cut, left out of the motion;
- in-shot motion: the median of the other differences (study target for e001-r2: >= 7);
- static frames: the share of differences < 3 (target <= 15 %).
Prints one line per file: motion, static %, cuts, frames.
"""
import statistics
import subprocess
import sys

W, H, FPS, CUT = 96, 54, 4, 25.0
TOP = int(H * 0.8)


def measure(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={FPS},scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"],
        capture_output=True, check=True).stdout
    n = len(raw) // (W * H)
    frames = [raw[i * W * H:(i * W * H) + W * TOP] for i in range(n)]
    diffs = [sum(abs(a - b) for a, b in zip(frames[i], frames[i - 1])) / (W * TOP) for i in range(1, n)]
    inner = [d for d in diffs if d < CUT]
    cuts = len(diffs) - len(inner)
    motion = statistics.median(inner) if inner else 0.0
    static = sum(1 for d in diffs if d < 3) / len(diffs) if diffs else 0.0
    return motion, static, cuts, n


if __name__ == "__main__":
    for p in sys.argv[1:]:
        m, s, c, n = measure(p)
        print(f"{p}\tmotion {m:.1f}\tstatic {s * 100:.0f}%\tcuts {c}\tframes {n}")
