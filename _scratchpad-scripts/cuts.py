#!/usr/bin/env python3
"""Find the hard cuts a Ref2VA draft cut into itself and trim each draft to the last H3 length before the first one.

Ref2VA sometimes cuts to a second shot inside one clip (2026-11-07, 《恁祖媽今年18》 e001 c19: an extreme
close-up of the eyes jumps to a wide shot at 3.2 s of 5). Only the part before the cut is the shot that was
asked for, and stage 2 (refine.py) takes only H3 lengths of 17k+5 frames, so the draft is cut back to the
longest such length that ends before the cut.

  cuts.py --input-dir out/ --output-dir trimmed/ [--manifest jobs.json] [--threshold 0.15] [--json report.json]

Every draft is copied to --output-dir: unchanged when it has no cut, re-encoded to the trimmed length when it
has one. With --manifest (the stage-1 manifest), a trimmed draft shorter than its job's `min_seconds`, or than
`duration_seconds` minus 2 when there is no `min_seconds`, is reported as too short and the exit code is 3, so
that shot is bought again instead of being refined. ffmpeg and ffprobe must be on PATH.

The threshold is on ffmpeg's scene score. The cut in c19 scored 0.31 between two dark frames; ordinary motion
in the same pilot (hands sweeping across the face, a walk with a tracking camera) stayed below 0.04.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

def probe(path: Path) -> tuple[int, float]:
    """Frame count and frame rate of the first video stream."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                          "stream=nb_read_frames,r_frame_rate", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    stream = json.loads(out)["streams"][0]
    num, _, den = stream["r_frame_rate"].partition("/")
    return int(stream["nb_read_frames"]), float(num) / float(den or 1)


def scene_scores(path: Path) -> list[tuple[int, float]]:
    """(0-based frame index, scene score) for every frame; a cut's index is the new shot's first frame, so it equals the frames before it."""
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-vf", "select='gte(scene,0)',metadata=print:key=lavfi.scene_score",
                          "-an", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    scores = [float(m) for m in re.findall(r"lavfi\.scene_score=([0-9.]+)", out)]
    return list(enumerate(scores))


def h3_length_before(frame: int) -> int:
    """The longest 17k+5 frame count that fits in the `frame` frames before the cut (0 when even 22 do not)."""
    k = (frame - 5) // 17
    return 17 * k + 5 if k >= 1 else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--manifest", help="stage-1 manifest: report trimmed drafts too short for their shot")
    ap.add_argument("--threshold", type=float, default=0.15)
    ap.add_argument("--json", dest="report", help="write the report here as JSON")
    args = ap.parse_args(argv)
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        print("[cuts] ffmpeg and ffprobe must be on PATH", file=sys.stderr)
        return 2
    src, dst = Path(args.input_dir), Path(args.output_dir)
    dst.mkdir(parents=True, exist_ok=True)
    wanted: dict[str, float] = {}
    if args.manifest:
        for job in json.loads(Path(args.manifest).read_text(encoding="utf-8"))["jobs"]:
            name = Path(job.get("output_path") or job.get("output_name") or f"{job['id']}.mp4").name
            wanted[name] = float(job.get("min_seconds", max(1.0, float(job.get("duration_seconds", 5)) - 2)))
    report, short = [], 0
    for path in sorted(src.glob("*.mp4")):
        frames, fps = probe(path)
        cuts = [(i, s) for i, s in scene_scores(path) if s >= args.threshold]
        row = {"file": path.name, "frames": frames, "fps": fps, "cuts": [{"frame": i, "seconds": round(i / fps, 3), "score": s} for i, s in cuts]}
        out = dst / path.name
        if cuts:
            keep = h3_length_before(cuts[0][0])
            row["kept_frames"] = keep
            row["kept_seconds"] = round(keep / fps, 3)
            if keep:
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(path), "-frames:v", str(keep), "-an",
                                "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(out)], check=True)
        else:
            row["kept_frames"], row["kept_seconds"] = frames, round(frames / fps, 3)
            shutil.copyfile(path, out)
        need = wanted.get(path.name)
        if need is not None and row["kept_seconds"] < need:
            row["too_short"] = need
            short += 1
        report.append(row)
        cut = f"cut at {cuts[0][0]} ({cuts[0][1]:.2f}) -> {row['kept_frames']} frames, {row['kept_seconds']} s" if cuts else "no cut"
        print(f"[cuts] {path.name}: {frames} frames, {cut}" + (f"; TOO SHORT, needs {need:g} s: buy it again" if row.get("too_short") else ""))
    if args.report:
        Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 3 if short else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
