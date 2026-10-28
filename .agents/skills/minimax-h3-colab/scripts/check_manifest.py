#!/usr/bin/env python3
"""Check an H3 Colab batch manifest before any compute unit is spent.

The upstream runner validates the shape (1-9 images, 4-15 seconds, multiples of 32) only when
the batch starts, and the notebook warns about short clips only on the GPU. This runs offline:

  errors (exit 1): missing or duplicate ids, unknown inference_mode, a first_frame job without
    exactly one image, a reference image file that is missing or empty, no prompt, `<Picture N>`
    beyond the images given, duration outside 4-15 s, width/height not multiples of 32 or over
    the 1344x768 area, a `prompt_sha256` that does not match the prompt file, duplicate outputs.
  warnings (exit 0): duration under 5 s (fewer than the 124 frames H3 was trained on: 4 s is
    107 frames), a first frame whose aspect ratio differs from the canvas by more than 0.01 (the
    notebook stretches it; run fit_first_frame.sh), `[Shot 2]` or ` then the camera ` in the
    prompt (the model cuts), a prompt without `<Picture 1>` in first_frame mode, ffprobe missing.

  check_manifest.py <manifest.json> [--quiet]
Standard library only; ffprobe is used when present.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

MODES = {"reference", "first_frame"}
MAX_AREA = 1344 * 768
TRAINED_MIN_FRAMES = 124
PICTURE = re.compile(r"<Picture\s+(\d+)>")


def frames_for(seconds: float) -> int:
    requested = max(5, round(seconds * 24))
    return requested + (5 - requested % 17) % 17


def image_size(path: Path) -> tuple[int, int] | None:
    if not shutil.which("ffprobe"):
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, timeout=30, check=False,
        ).stdout.strip()
        width, height = (int(v) for v in out.split(",")[:2])
        return width, height
    except (ValueError, subprocess.SubprocessError, OSError):
        return None


def check(manifest_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"{manifest_path}: cannot read as JSON ({exc})"], warnings
    jobs = data.get("jobs") if isinstance(data, dict) else None
    if not isinstance(jobs, list) or not jobs:
        return [f"{manifest_path}: expected an object with a non-empty `jobs` array"], warnings
    base = manifest_path.parent
    seen_ids: set[str] = set()
    seen_out: set[str] = set()
    if not shutil.which("ffprobe"):
        warnings.append("ffprobe is not on PATH: first-frame aspect ratios are not checked")

    for index, job in enumerate(jobs):
        if not isinstance(job, dict):
            errors.append(f"jobs[{index}] is not an object")
            continue
        job_id = str(job.get("id") or f"jobs[{index}]")
        tag = f"{job_id}:"
        if not job.get("id"):
            errors.append(f"{tag} missing id")
        elif job_id in seen_ids:
            errors.append(f"{tag} duplicate id")
        seen_ids.add(job_id)

        mode = str(job.get("inference_mode") or "reference")
        if mode not in MODES:
            errors.append(f"{tag} inference_mode {mode!r} is not reference or first_frame")

        images = job.get("reference_images")
        if not isinstance(images, list) or not images:
            errors.append(f"{tag} reference_images must list 1-9 images")
            images = []
        elif len(images) > 9:
            errors.append(f"{tag} {len(images)} reference images; the limit is 9")
        if mode == "first_frame" and len(images) != 1:
            errors.append(f"{tag} first_frame needs exactly one image, got {len(images)}")
        image_paths = []
        for image in images:
            path = (base / str(image)).resolve() if not Path(str(image)).is_absolute() else Path(str(image))
            if not path.is_file() or path.stat().st_size == 0:
                errors.append(f"{tag} reference image missing or empty: {image}")
            else:
                image_paths.append(path)

        width = job.get("width", 1344)
        height = job.get("height", 768)
        for name, value in (("width", width), ("height", height)):
            if not isinstance(value, int) or value <= 0 or value % 32:
                errors.append(f"{tag} {name}={value!r} must be a positive multiple of 32")
        if isinstance(width, int) and isinstance(height, int) and width > 0 and height > 0:
            if width * height > MAX_AREA:
                errors.append(f"{tag} {width}x{height} exceeds the 1344x768 area the notebook accepts")
            if mode == "first_frame" and image_paths:
                size = image_size(image_paths[0])
                if size and abs(size[0] / size[1] - width / height) > 0.01:
                    warnings.append(
                        f"{tag} first frame {size[0]}x{size[1]} ({size[0] / size[1]:.3f}) does not match the {width}x{height} "
                        f"canvas ({width / height:.3f}); the notebook will stretch it. Run fit_first_frame.sh, or use the 1312x736 canvas for a 16:9 frame."
                    )

        duration = job.get("duration_seconds", 12)
        if not isinstance(duration, (int, float)) or isinstance(duration, bool) or not (4 <= float(duration) <= 15):
            errors.append(f"{tag} duration_seconds={duration!r} must be 4-15")
        elif frames_for(float(duration)) < TRAINED_MIN_FRAMES:
            warnings.append(
                f"{tag} {duration} s is {frames_for(float(duration))} frames, under the {TRAINED_MIN_FRAMES}-frame range H3 was trained on; "
                "buy 5 s (124 frames, 5.17 s) or more and trim in the cut"
            )

        prompt_text = None
        if job.get("prompt_file"):
            prompt_path = (base / str(job["prompt_file"])).resolve() if not Path(str(job["prompt_file"])).is_absolute() else Path(str(job["prompt_file"]))
            try:
                prompt_bytes = prompt_path.read_bytes()
                prompt_text = prompt_bytes.decode("utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                errors.append(f"{tag} prompt_file unreadable as UTF-8: {job['prompt_file']} ({exc})")
            else:
                if prompt_text.startswith("﻿"):
                    warnings.append(f"{tag} prompt_file starts with a UTF-8 BOM, which leaks into the prompt")
                expected = job.get("prompt_sha256")
                if expected:
                    actual = hashlib.sha256(prompt_bytes).hexdigest()
                    if str(expected).lower() != actual:
                        errors.append(f"{tag} prompt_sha256 {str(expected)[:12]}… does not match the prompt file ({actual[:12]}…): the lock and the file disagree")
        elif job.get("prompt"):
            prompt_text = str(job["prompt"])
        else:
            errors.append(f"{tag} needs prompt_file or prompt")

        if prompt_text is not None:
            if not prompt_text.strip():
                errors.append(f"{tag} the prompt is empty")
            cited = [int(n) for n in PICTURE.findall(prompt_text)]
            for n in cited:
                if n < 1 or n > len(images):
                    errors.append(f"{tag} prompt cites <Picture {n}> but the job has {len(images)} image(s)")
            if mode == "first_frame" and 1 not in cited:
                warnings.append(f"{tag} first_frame prompt never cites <Picture 1>: add the official alignment line and the anchor sentence")
            if re.search(r"\[Shot\s*[2-9]\]", prompt_text):
                warnings.append(f"{tag} prompt has [Shot 2]: the model will cut inside the clip; one shot per clip")
            if re.search(r"\bthen the camera\b", prompt_text, re.IGNORECASE):
                warnings.append(f"{tag} prompt chains camera moves with 'then': H3 turns that into cuts; one move per clip")

        out = job.get("output_name")
        if out:
            if out in seen_out:
                errors.append(f"{tag} duplicate output_name {out}")
            seen_out.add(str(out))
    return errors, warnings


def main(argv: list[str]) -> int:
    quiet = "--quiet" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if len(paths) != 1:
        print(__doc__.strip())
        return 2
    errors, warnings = check(Path(paths[0]))
    for line in warnings:
        print(f"[check_manifest] warning: {line}")
    for line in errors:
        print(f"[check_manifest] error: {line}", file=sys.stderr)
    if not quiet or errors:
        print(f"[check_manifest] {paths[0]}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
