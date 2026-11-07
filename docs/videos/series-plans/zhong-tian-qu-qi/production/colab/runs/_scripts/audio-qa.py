#!/usr/bin/env python3
"""audio-qa.py CUT_DIR VIDEO_JSON : check where every dubbed line landed in a finished cut.

The cut is reviewed from still frames, so nothing listened to it (owner 2026-11-07: "does the pipeline review the cut?").
This reads <stem>.lines.json (assemble-v4.mjs writes it) and final.log and checks what a viewer would hear wrong:
- spill:   a line runs past the end of its shot by more than 0.25 s, so a speaker on screen is heard over the next shot
           (lips moving in one shot, the voice in the next); an off-screen or system line spilling is only a note;
- overlap: two lines play at the same time;
- cut:     a line runs past the end of the video;
- quiet:   a line is not clearly louder than the music under it (its window is under -30 LUFS, or, where the second
           before it holds no other line, less than 3 dB above that second of music and effects) — the voice is buried;
- gap:     more than 4 s with no line at all (only a note: silence can be on purpose).
It cannot judge lip shapes or whether a voice suits a face; the owner still listens.
Prints one line per finding; exit 1 on spill/overlap/cut/quiet.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

cut = Path(sys.argv[1])
video = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
mp4 = next(p for p in cut.glob("*.mp4") if not p.name.endswith("-phone.mp4"))
lines = json.loads(mp4.with_suffix(".lines.json").read_text(encoding="utf-8"))
log = (cut / "final.log").read_text(encoding="utf-8")
shots = {s: (float(a), float(a) + float(d)) for s, a, d in re.findall(r"^([sc]\d+[a-z]?) ([\d.]+) \+([\d.]+)s ", log, re.M)}
total = float(re.search(r"^total ([\d.]+)s", log, re.M).group(1))
scene = {s["id"]: s for s in video["scenes"]}
onscreen = lambda l: l["speaker"] != "xitong" and l["speaker"] in scene[l["shot"]]["data"].get("characters", []) \
    and l["speaker"] not in scene[l["shot"]]["data"].get("nospeak", []) \
    and not re.search("嘴閉著|內心獨白|畫外", next((x.get("emotion", "") for x in scene[l["shot"]]["lines"] if x["id"] == l["id"]), ""))
bad = 0


def say(level, kind, text):
    global bad
    bad += level == "FAIL"
    print(f"{level:4} {kind:7} {text}")


def lufs(a, b):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{max(0, a):.2f}", "-t", f"{max(0.4, b - a):.2f}", "-i", str(mp4),
                          "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
    return float(m[-1]) if m else -70.0


lines.sort(key=lambda l: l["start"])
for i, l in enumerate(lines):
    end = l["start"] + l["len"]
    s0, s1 = shots[l["shot"]]
    if end > s1 + 0.25:
        level = "FAIL" if onscreen(l) else "note"
        say(level, "spill", f"{l['id']} {l['speaker']} ({l['shot']}) runs {end - s1:.2f} s into the next shot")
    if end > total + 0.05:
        say("FAIL", "cut", f"{l['id']} ends {end - total:.2f} s after the video")
    if i + 1 < len(lines) and lines[i + 1]["start"] < end - 0.05:
        say("FAIL", "overlap", f"{l['id']} and {lines[i + 1]['id']} overlap {end - lines[i + 1]['start']:.2f} s")
    here = lufs(l["start"] + 0.1, end - 0.1)
    free = l["start"] > 1.2 and not any(o is not l and o["start"] < l["start"] - 0.1 and o["start"] + o["len"] > l["start"] - 1.1 for o in lines)
    before = lufs(l["start"] - 1.1, l["start"] - 0.1) if free else -70.0  # music and effects only: no other line in that second
    if here < -30 or (before > -70 and here - before < 3 and before > -28):
        say("FAIL", "quiet", f"{l['id']} {l['speaker']} ({l['shot']}) {here:.1f} LUFS, the second before it {before:.1f}")
prev = 0.0
for l in lines:
    if l["start"] - prev > 4:
        say("note", "gap", f"{l['start'] - prev:.1f} s without a line before {l['id']} ({l['shot']})")
    prev = max(prev, l["start"] + l["len"])
print(f"{cut}: {len(lines)} lines, {bad} problem(s)")
sys.exit(1 if bad else 0)
