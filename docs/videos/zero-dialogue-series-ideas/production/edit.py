#!/usr/bin/env python3
"""Cut one zero-dialogue Short: clips -> 1080x1920 30 fps, music bed, sfx at shot starts, -14 LUFS.

  python3 edit.py <plan.json> <out.mp4>

plan.json: {"music": path, "music_start": s, "music_gain_db": -14, "shots": [
  {"clip": path, "in": s, "dur": s, "sfx": [{"file": path, "at": s_from_shot_start, "gain_db": 0}]}
]}
Missing clips are replaced by a black card with the shot id (so a draft cut still plays).
"""
import json
import subprocess
import sys
from pathlib import Path

W, H, FPS = 1080, 1920, 30


def run(args):
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode:
        sys.exit(p.stderr[-2000:])
    return p


def main():
    plan = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    work = out.parent / "parts"
    work.mkdir(parents=True, exist_ok=True)
    parts, t, cues = [], 0.0, []
    for i, shot in enumerate(plan["shots"]):
        part = work / f"{i:02d}.mp4"
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p"
        if Path(shot["clip"]).exists():
            run(["ffmpeg", "-v", "error", "-y", "-ss", str(shot["in"]), "-t", str(shot["dur"]), "-i", shot["clip"],
                 "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(part)])
        else:
            run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=black:s={W}x{H}:r={FPS}:d={shot['dur']}",
                 "-vf", "format=yuv420p", "-c:v", "libx264", str(part)])
        parts.append(part)
        for s in shot.get("sfx", []):
            cues.append((t + s.get("at", 0), s["file"], s.get("gain_db", 0)))
        t += shot["dur"]
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    video = work / "video.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(video)])
    total = t
    inputs = ["-i", plan["music"]]
    filt = [f"[0]atrim=start={plan.get('music_start', 0)}:duration={total},asetpts=PTS-STARTPTS,"
            f"volume={plan.get('music_gain_db', -14)}dB,afade=t=out:st={max(total - 1.2, 0)}:d=1.2[m]"]
    labels = ["[m]"]
    for k, (at, f, g) in enumerate(cues, 1):
        inputs += ["-i", f]
        ms = int(at * 1000)
        filt.append(f"[{k}]volume={g}dB,adelay={ms}|{ms}[s{k}]")
        labels.append(f"[s{k}]")
    filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{total},"
                f"aformat=sample_rates=48000:channel_layouts=stereo[mix]")
    mix = work / "mix.wav"
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[mix]", str(mix)])
    measured = run(["ffmpeg", "-v", "info", "-i", str(mix), "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
                    "-f", "null", "-"]).stderr
    m = json.loads(measured[measured.rindex("{"):measured.rindex("}") + 1])
    norm = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(mix), "-af", f"{norm},aresample=48000",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", str(out)])
    print(f"{out}: {total:.2f} s, {len(plan['shots'])} shots, {len(cues)} sfx")


if __name__ == "__main__":
    main()
