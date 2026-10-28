#!/usr/bin/env python3
"""Check a first-frame (Qwen-Image-Edit) manifest before any compute unit is spent.

  errors (exit 1): missing or duplicate ids, not 1-3 reference images, a reference image file
    that is missing or empty, no prompt, width/height not multiples of 16 or over the 1344x768
    area, a prompt that names "image N" beyond the images given, a seed outside 0..2^53-1,
    `latent` other than empty or image1, duplicate outputs, more than 40 jobs.
  warnings (exit 0): a canvas that is not 16:9 within 0.01 (the H3 first-frame canvas is
    1312x736), `<Picture N>` tags (that is H3's notation; Qwen-Image-Edit reads "image 1"),
    a prompt without any "image N" mention (the references are then only a mood board),
    a prompt over 2,500 characters, a UTF-8 BOM.

  check_images_manifest.py <manifest.json> [--quiet]
Standard library only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MAX_AREA = 1344 * 768
MAX_JOBS = 40
IMAGE_REF = re.compile(r"\bimage\s+(\d+)\b", re.IGNORECASE)
PICTURE = re.compile(r"<Picture\s+\d+>")


def resolve(base: Path, value: object) -> Path:
    path = Path(str(value)).expanduser()
    return path if path.is_absolute() else (base / path)


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
    if len(jobs) > MAX_JOBS:
        errors.append(f"{len(jobs)} jobs; a batch takes at most {MAX_JOBS} (split the manifest)")
    base = manifest_path.parent
    seen_ids: set[str] = set()
    seen_out: set[str] = set()
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

        images = job.get("reference_images")
        if not isinstance(images, list) or not 1 <= len(images) <= 3:
            errors.append(f"{tag} reference_images must list 1-3 images (TextEncodeQwenImageEditPlus takes image1-image3)")
            images = images if isinstance(images, list) else []
        for image in images:
            path = resolve(base, image)
            if not path.is_file() or path.stat().st_size == 0:
                errors.append(f"{tag} reference image missing or empty: {image}")

        width = job.get("width", 1312)
        height = job.get("height", 736)
        for name, value in (("width", width), ("height", height)):
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0 or value % 16:
                errors.append(f"{tag} {name}={value!r} must be a positive multiple of 16")
        if isinstance(width, int) and isinstance(height, int) and width > 0 and height > 0:
            if width * height > MAX_AREA:
                errors.append(f"{tag} {width}x{height} exceeds the 1344x768 area (the first frame must fit the H3 canvas)")
            elif abs(width / height - 16 / 9) > 0.01:
                warnings.append(f"{tag} {width}x{height} is not 16:9; the H3 first-frame canvas is 1312x736")

        prompt_text = None
        if job.get("prompt_file"):
            try:
                prompt_text = resolve(base, job["prompt_file"]).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                errors.append(f"{tag} prompt_file unreadable as UTF-8: {job['prompt_file']} ({exc})")
        elif job.get("prompt"):
            prompt_text = str(job["prompt"])
        else:
            errors.append(f"{tag} needs prompt_file or prompt")
        if prompt_text is not None:
            if prompt_text.startswith("﻿"):
                warnings.append(f"{tag} prompt starts with a UTF-8 BOM, which leaks into the prompt")
            if not prompt_text.strip():
                errors.append(f"{tag} the prompt is empty")
            cited = [int(n) for n in IMAGE_REF.findall(prompt_text)]
            for n in cited:
                if n < 1 or n > len(images):
                    errors.append(f"{tag} prompt names image {n} but the job has {len(images)} image(s)")
            if not cited and images:
                warnings.append(f"{tag} prompt never says which image is which ('image 1 is ...'): the references act only as a mood board")
            if PICTURE.search(prompt_text):
                warnings.append(f"{tag} prompt uses <Picture N>: that is H3's tag; Qwen-Image-Edit reads 'image N'")
            if len(prompt_text) > 2500:
                warnings.append(f"{tag} prompt is {len(prompt_text)} characters; long prompts dilute the reference instructions")
        if job.get("negative_file"):
            path = resolve(base, job["negative_file"])
            if not path.is_file():
                errors.append(f"{tag} negative_file missing: {job['negative_file']}")

        seed = job.get("seed")
        if seed not in (None, "") and (not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed < 2**53):
            errors.append(f"{tag} seed={seed!r} must be an integer in 0..2^53-1")
        latent = job.get("latent", "empty")
        if latent not in {"empty", "image1"}:
            errors.append(f"{tag} latent={latent!r} must be empty or image1")
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
        print(f"[check_images_manifest] warning: {line}")
    for line in errors:
        print(f"[check_images_manifest] error: {line}", file=sys.stderr)
    if not quiet or errors:
        print(f"[check_images_manifest] {paths[0]}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
