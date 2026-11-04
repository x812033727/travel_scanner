#!/usr/bin/env python3
"""Cut one zero-dialogue Short: clips -> 1080x1920 30 fps, music bed, sfx at shot starts, -14 LUFS.

  python3 edit.py <plan.json> <out.mp4>

plan.json: {"music": path, "music_start": s, "music_gain_db": -14, "shots": [
  {"clip": path, "in": s, "dur": s, "sfx": [{"file": path, "at": s_from_shot_start, "gain_db": 0}]}
]}
Optional per shot: "hold": s (freeze the last frame that long; part of the shot's length),
"reverse": true, "push": [z0, z1] (slow zoom from z0 to z1 over the shot) with "anchor": [x, y]
(0..1 point the zoom closes in on), "lights_out": [s, ...] (each step darkens; black 0.4 s after
the last), "music_off": true (music silent during the shot), "box": [x, y, w, h, at] (0..1 of the frame: a
near-black patch from `at` seconds, e.g. a screen that goes dead), "keep_cuts": true.
A missing clip (or "clip": "black") is a black card.
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


def first_cut(clip, start, threshold=0.4):
    """Seconds into the clip of the first hard scene change after `start` (the model cutting away), or None."""
    p = subprocess.run(["ffmpeg", "-v", "info", "-ss", str(start), "-i", clip, "-vf", f"select='gt(scene,{threshold})',showinfo",
                        "-f", "null", "-"], capture_output=True, text=True)
    for line in p.stderr.splitlines():
        if "pts_time:" in line:
            return start + float(line.split("pts_time:")[1].split()[0])
    return None


def main():
    plan = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    work = out.parent / "parts"
    work.mkdir(parents=True, exist_ok=True)
    parts, t, cues, mutes = [], 0.0, [], []
    for i, shot in enumerate(plan["shots"]):
        part = work / f"{i:02d}.mp4"
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}"
        if shot.get("reverse"):
            vf = "reverse," + vf
        if shot.get("push"):
            z0, z1 = shot["push"]
            ax, ay = shot.get("anchor", [0.5, 0.5])
            d = shot["dur"]
            z = f"({z0}+({z1}-{z0})*t/{d})"
            vf += (f",scale=w='trunc({W}*{z}/2)*2':h='trunc({H}*{z}/2)*2':eval=frame,"
                   f"crop={W}:{H}:x='(in_w-{W})*{ax}':y='(in_h-{H})*{ay}'")
        for k, at in enumerate(shot.get("lights_out", [])):
            vf += f",eq=brightness=-0.2:contrast=0.8:saturation=0.7:enable='gte(t,{at})'"
        if shot.get("lights_out"):
            vf += f",drawbox=c=black:t=fill:enable='gte(t,{shot['lights_out'][-1] + 0.4})'"
        if shot.get("box"):
            bx, by, bw, bh, bat = shot["box"]
            vf += f",drawbox=x={int(bx * W)}:y={int(by * H)}:w={int(bw * W)}:h={int(bh * H)}:c=0x0b0d10:t=fill:enable='gte(t,{bat})'"
        hold = shot.get("hold", 0)
        if hold:
            vf += f",tpad=stop_mode=clone:stop_duration={hold}"
        vf += ",format=yuv420p"
        if Path(shot["clip"]).exists() and not shot.get("keep_cuts"):
            cut = first_cut(shot["clip"], shot["in"])
            if cut is not None and cut < shot["in"] + shot["dur"] - hold:
                new = max(0.8, round(cut - shot["in"] - 0.05, 2)) + hold
                print(f"  {Path(shot['clip']).name}: scene change at {cut:.2f}s, {shot['dur']}s -> {new}s")
                shot["dur"] = new
        if Path(shot["clip"]).exists():
            run(["ffmpeg", "-v", "error", "-y", "-ss", str(shot["in"]), "-t", str(round(shot["dur"] - hold, 3)), "-i", shot["clip"],
                 "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(part)])
        else:
            run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=black:s={W}x{H}:r={FPS}:d={shot['dur']}",
                 "-vf", "format=yuv420p", "-c:v", "libx264", str(part)])
        parts.append(part)
        if shot.get("music_off"):
            mutes.append((t, t + shot["dur"]))
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
            f"volume={plan.get('music_gain_db', -14)}dB,"
            + "".join(f"volume=0:enable='between(t,{a:.3f},{b:.3f})'," for a, b in mutes)
            + f"afade=t=out:st={max(total - 1.2, 0)}:d=1.2[m]"]
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
