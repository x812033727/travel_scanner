#!/usr/bin/env python3
"""Gate 1 of the finished-cut QA (QA.md): automatic checks on one episode's final cut.

  python3 qa_check.py <slug> [--work /root/mokaair-work/videos] [--out DIR]

Checks the cut against the Shorts profile (1080x1920, 30 fps, 48 kHz audio, 9-20 s, -15..-13 LUFS),
finds hard scene changes that are not shot boundaries of edit/plan.json (the model cutting away
inside a clip), and writes a contact sheet (3 frames a second, timestamped) for the reviewer.
Writes <out>/<slug>.qa.json and <out>/<slug>.jpg. Exit 0 = gate passed, 1 = a check failed.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

PROFILE = {"width": 1080, "height": 1920, "fps": "30/1", "sample_rate": "48000", "min_s": 9.0, "max_s": 20.0, "lufs": (-15.0, -13.0)}
CUT_THRESHOLD = 0.4
BOUNDARY_SLACK = 0.12


def probe(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,sample_rate:format=duration",
                        "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(p.stdout)


def loudness(path):
    err = subprocess.run(["ffmpeg", "-v", "info", "-i", str(path), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    lines = [l for l in err.splitlines() if l.strip().startswith("I:")]
    return float(lines[-1].split()[1]) if lines else None


def scene_cuts(path):
    err = subprocess.run(["ffmpeg", "-v", "info", "-i", str(path), "-vf", f"select='gt(scene,{CUT_THRESHOLD})',showinfo", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return [float(l.split("pts_time:")[1].split()[0]) for l in err.splitlines() if "pts_time:" in l]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--work", default="/root/mokaair-work/videos")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    ep = Path(a.work) / a.slug
    final = ep / "edit" / "final.mp4"
    out = Path(a.out or ep / "qa")
    out.mkdir(parents=True, exist_ok=True)
    problems, notes = [], []
    if not final.exists():
        print(f"{a.slug}: no edit/final.mp4"); return 1
    info = probe(final)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    au = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"])
    if (v["width"], v["height"]) != (PROFILE["width"], PROFILE["height"]):
        problems.append(f"size {v['width']}x{v['height']}, want 1080x1920")
    if v["r_frame_rate"] != PROFILE["fps"]:
        problems.append(f"frame rate {v['r_frame_rate']}, want 30/1")
    if not au or au.get("sample_rate") != PROFILE["sample_rate"]:
        problems.append("audio missing or not 48 kHz")
    if not PROFILE["min_s"] <= dur <= PROFILE["max_s"]:
        problems.append(f"length {dur:.1f} s, want {PROFILE['min_s']}-{PROFILE['max_s']} s")
    lufs = loudness(final)
    if lufs is None or not PROFILE["lufs"][0] <= lufs <= PROFILE["lufs"][1]:
        problems.append(f"loudness {lufs} LUFS, want {PROFILE['lufs'][0]}..{PROFILE['lufs'][1]}")
    # Shot boundaries from the parts edit.py actually cut (its auto-trim is not written back to plan.json).
    lst = ep / "edit" / "parts" / "list.txt"
    parts = [ep / "edit" / "parts" / l.split("'")[1] for l in lst.read_text().splitlines()] if lst.exists() else []
    bounds, t = [], 0.0
    for part in parts[:-1]:
        t += float(probe(part)["format"]["duration"])
        bounds.append(t)
    stray = [c for c in scene_cuts(final) if all(abs(c - b) > BOUNDARY_SLACK for b in bounds)]
    if stray:
        notes.append(f"hard scene changes inside a shot at {', '.join(f'{c:.2f}' for c in stray)} s (check: model cut away? plan durations may also differ from the cut after auto-trim)")
    sheet = out / f"{a.slug}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(final), "-vf",
                    "fps=3,scale=180:-1,drawtext=text='%{pts\\:hms}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=9x7",
                    "-frames:v", "1", str(sheet)], check=True)
    report = {"slug": a.slug, "duration_s": round(dur, 2), "lufs": lufs, "problems": problems, "notes": notes, "contact_sheet": str(sheet),
              "passed": not problems}
    (out / f"{a.slug}.qa.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(f"{a.slug}: {'PASS' if not problems else 'FAIL'} {dur:.1f}s {lufs} LUFS" + "".join(f"\n  FAIL {p}" for p in problems) + "".join(f"\n  note {n}" for n in notes))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
