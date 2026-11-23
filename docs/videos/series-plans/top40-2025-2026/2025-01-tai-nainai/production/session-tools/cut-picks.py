#!/usr/bin/env python3
"""picks.txt（<鏡>=<片段>@<起>-<止>）→ 每鏡剪成 17k+5 格（精修的格數規則）、從選定的起點開始；寫 cut/<鏡>.mp4 與 cut/takes.json（給 voice.py：draft、from）。"""
import json, math, subprocess, sys
from pathlib import Path
picks, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
takes = {}
for line in picks.read_text().split():
    sid, rest = line.split("=", 1)
    if rest == "FAIL": continue
    path, win = rest.split("@"); a, b = map(float, win.split("-"))
    total = int(subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-count_frames","-show_entries","stream=nb_read_frames","-of","csv=p=0",path],capture_output=True,text=True).stdout.strip())
    need = math.ceil((b - a) * 24); k = max(1, math.ceil((need - 5) / 17)); n = 17 * k + 5
    while n > total: k -= 1; n = 17 * k + 5
    s = min(round(a * 24), total - n)
    subprocess.run(["ffmpeg","-v","error","-y","-i",path,"-vf",f"trim=start_frame={s}:end_frame={s+n},setpts=PTS-STARTPTS","-an","-c:v","libx264","-crf","12","-preset","slow",str(out/f"{sid}.mp4")],check=True)
    takes[sid] = {"draft": path, "from": round(s / 24, 4), "frames": n, "window": [a, b]}
    print(f"{sid}: {path.split('/')[-1]} from {s/24:.2f}s {n} frames ({n/24:.2f}s) window {a}-{b}")
(out/"takes.json").write_text(json.dumps(takes, indent=1))
