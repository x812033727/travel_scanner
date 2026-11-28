#!/usr/bin/env python3
"""crowd-murmur.py N [SECONDS] [OUT.wav] : an unintelligible crowd bed made from the episode's own Chinese recordings.

Owner 2026-11-21: 「用倒放錄音做人群聲」. The Pixabay crowd and market beds carry readable English and Persian words
(whisper heard "Sorry!", "Please, stop.", "green tea"), so every crowd murmur in episodes 1-30 is made the e929/e930 way:
the recordings in ~/mokaair-work/videos/zhong-tian-qu-qi-e9NN-dh/audio/zq9NNa*.wav (orig/ copies preferred) are reversed,
sped up a little, laid over each other 0.53 s apart (several passes, alternating pan) until SECONDS are filled,
band-limited to 250-1800 Hz, given two short echoes and leveled to -19 LUFS. Reversed speech keeps a Chinese voice
texture with no readable word. Default 12 s, written to zhong-tian-qu-qi-e9NN-dh/sfx/murmurNN.wav (the edit table's
episode sfx dir), 48 kHz stereo.

    python3 -I crowd-murmur.py 30 12
"""
import random
import subprocess
import sys
from pathlib import Path

N = int(sys.argv[1])
SECS = float(sys.argv[2]) if len(sys.argv) > 2 else 12.0
EP = 900 + N
DH = Path.home() / "mokaair-work" / "videos" / f"zhong-tian-qu-qi-e{EP}-dh"
OUT = Path(sys.argv[3]) if len(sys.argv) > 3 else DH / "sfx" / f"murmur{N:02d}.wav"
OUT.parent.mkdir(parents=True, exist_ok=True)
src = {}
for p in sorted((DH / "audio").glob(f"zq{EP}a*.wav")) + sorted((DH / "audio" / "orig").glob(f"zq{EP}a*.wav")):
    src[p.stem.split("-")[0]] = p  # orig/ (the untouched recording) wins over a leveled or spliced one
files = [src[k] for k in sorted(src)]
if len(files) < 6:
    sys.exit(f"e{EP}: only {len(files)} recordings under {DH / 'audio'}")
rng = random.Random(EP)
picks, t, layers = [], 0.0, []
while t < SECS + 2:
    f = rng.choice(files)
    picks.append((f, round(t, 2), rng.choice([-0.6, -0.3, 0.3, 0.6]), round(rng.uniform(1.05, 1.15), 3)))
    t += 0.53
inputs, filters = [], []
for i, (f, at, pan, tempo) in enumerate(picks):
    inputs += ["-i", str(f)]
    left, right = (1 - pan) / 2, (1 + pan) / 2
    filters.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=mono,areverse,atempo={tempo},volume=0.55,"
                   f"pan=stereo|c0={left:.2f}*c0|c1={right:.2f}*c0,adelay={int(at * 1000)}|{int(at * 1000)}[l{i}]")
mix = "".join(f"[l{i}]" for i in range(len(picks)))
filters.append(f"{mix}amix=inputs={len(picks)}:normalize=0,highpass=f=250,lowpass=f=1800,"
               f"aecho=0.8:0.6:60|110:0.35|0.22,atrim=0:{SECS},afade=t=in:d=0.6,afade=t=out:st={SECS - 0.8}:d=0.8,"
               f"loudnorm=I=-19:TP=-6:LRA=7,aresample=48000[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[out]", "-ac", "2",
                "-ar", "48000", str(OUT)], check=True)
print(f"e{EP}: {OUT} ({SECS:.1f} s, {len(picks)} reversed takes from {len(files)} recordings)")
