#!/usr/bin/env python3
"""continuity-sheets.py CUT_DIR|PICKS_DIR VIDEO_JSON OUT_DIR : one contact sheet per scene, for the continuity review.

CUT_DIR is a finished cut (final.log + the mp4). PICKS_DIR is a folder of picked drafts named sNN.mp4 (runpod/a/st1/out):
the same sheets before anything is refined, for the pick-stage review (owner 2026-11-07: review after the picks too).

Every shot of a scene gets three frames (start, middle, end) in cut order, one row per shot, labelled with the shot id and
its first line, so a scene is read the way the viewer sees it. cut-qa.py checks one shot at a time; these sheets are for
what only shows across shots (owner, e004-r2: "the box grew and shrank", "the door and the wok moved", "he came out and the
figure was not there"):
- the same prop at the same size and shape in every shot of the scene;
- the same places at the same distance from each other (door, stove, table, gate);
- whoever looks at something: the thing is where they look, in the shot before or after;
- the time of day, the light and the clothes stay put within the scene.
Writes OUT_DIR/scene-NN.jpg and prints the paths.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

cut, video, out = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
PICKS = not (cut / "final.log").exists()
if PICKS:
    dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                         capture_output=True, text=True).stdout)
    times = {f.stem: (0.0, dur(f)) for f in cut.glob("[sc][0-9]*.mp4")}
else:
    log = (cut / "final.log").read_text(encoding="utf-8")
    times = {s: (float(a), float(d)) for s, a, d in re.findall(r"^([sc]\d+[a-z]?) ([\d.]+) \+([\d.]+)s ", log, re.M)}
FONT = next((str(p) for p in [Path("/usr/share/fonts/opentype/unifont/unifont.otf")] if p.exists()), None)
FONTARG = f":fontfile={FONT}" if FONT else ""
mp4 = None if PICKS else next(p for p in cut.glob("*.mp4") if not p.name.endswith("-phone.mp4"))
scenes, cur = [], None
for sc in video["scenes"]:
    if sc.get("chapter") or cur is None:
        cur = {"name": sc.get("chapter", ""), "shots": []}
        scenes.append(cur)
    cur["shots"].append(sc)
for n, scene in enumerate(scenes, 1):
    rows = []
    for sc in scene["shots"]:
        sid = sc["id"]
        if sid not in times:
            continue
        a, d = times[sid]
        line = (sc["lines"][0]["text"][:18] if sc.get("lines") else "—").replace("'", "").replace(":", " ")
        frames = []
        for k, t in enumerate((a + 0.15, a + d / 2, a + d - 0.15)):
            f = out / f".{sid}-{k}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(cut / f"{sid}.mp4") if PICKS else str(mp4), "-frames:v", "1", "-vf",
                            f"scale=420:-2,drawtext=text='{sid} {line}'{FONTARG}:x=6:y=6:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6" if k == 0 else "scale=420:-2",
                            str(f)], check=True)
            frames.append(f)
        row = out / f".{sid}-row.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *sum((["-i", str(f)] for f in frames), []), "-filter_complex", "hstack=inputs=3", str(row)], check=True)
        rows.append(row)
    if not rows:
        continue
    sheet = out / f"scene-{n:02d}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *sum((["-i", str(r)] for r in rows), []), "-filter_complex", f"vstack=inputs={len(rows)}", str(sheet)], check=True)
    for p in out.glob(".[sc][0-9]*.jpg"):
        p.unlink()
    print(f"{sheet}  ({scene['name']}, {len(rows)} shots)")
