#!/usr/bin/env python3
"""Stage 3 of the three-stage H3 route: SeedVR2 refined clips to exactly 1920x1080 on one Colab session.

Uploads every MP4 named on the command line (or found in --input-dir), runs
assets/seedvr2_upscale.ipynb (numz's SeedVR2 CLI at a pinned commit; the notebook trims the frames
`--prepend_frames` adds and checks that the frame count is unchanged), and unpacks
<name>_1080.mp4 into --output-dir. See references/three-stage.md.

  upscale.py --input-dir refined/ --output-dir final/ [--model 7b|3b] [--batch-size 81] [--session NAME]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tarfile
import time
import uuid
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from images import ColabError, call_colab, now_iso, start_session, stop_session, write_progress  # noqa: E402
import colab_detached  # noqa: E402
from colab_detached import session_alive  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parents[1]
NOTEBOOK = SKILL_DIR / "assets" / "seedvr2_upscale.ipynb"
MODELS = {"3b": "seedvr2_ema_3b_fp16.safetensors", "7b": "seedvr2_ema_7b_fp16.safetensors"}
NAME_RE = re.compile(r"^[A-Za-z0-9_-]{1,60}\.mp4$")
MAX_CLIPS = 20


def gather(inputs: list[Path], input_dir: Path | None) -> tuple[list[Path], list[str]]:
    clips = [path.expanduser().resolve() for path in inputs]
    if input_dir:
        clips += sorted(path.resolve() for path in input_dir.expanduser().glob("*.mp4"))
    errors = []
    if not clips:
        errors.append("no clips: name MP4 files or --input-dir")
    if len(clips) > MAX_CLIPS:
        errors.append(f"{len(clips)} clips; a batch takes at most {MAX_CLIPS}")
    names = set()
    for clip in clips:
        if not clip.is_file() or clip.stat().st_size == 0:
            errors.append(f"missing or empty: {clip}")
        if not NAME_RE.match(clip.name):
            errors.append(f"{clip.name}: name it with letters, digits, _ or - and .mp4")
        if clip.name in names:
            errors.append(f"{clip.name}: two clips share a name")
        names.add(clip.name)
    return clips, errors


def run(args: argparse.Namespace) -> dict[str, Any]:
    if not NOTEBOOK.is_file():
        raise FileNotFoundError(f"notebook not found: {NOTEBOOK}")
    if args.batch_size % 4 != 1:
        raise ValueError(f"--batch-size {args.batch_size}: SeedVR2 batches are 4n+1 frames")
    clips, errors = gather(args.clips, args.input_dir)
    if errors:
        raise ValueError("input problems:\n  " + "\n  ".join(errors))
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    session = args.session or f"s3-{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}-{uuid.uuid4().hex[:6]}"
    owns_session = args.session is None
    progress_path = args.progress.expanduser().resolve() if args.progress else None
    progress: dict[str, Any] = {"task": "upscale", "status": "starting", "session": session, "gpu": args.gpu,
                                "model": MODELS[args.model], "batch_size": args.batch_size,
                                "clips": [clip.name for clip in clips], "log_tail": [], "updated_at": now_iso()}
    write_progress(progress_path, progress)

    def log_line(line: str) -> None:
        progress["log_tail"] = (progress["log_tail"] + [line[:320]])[-30:]
        progress["updated_at"] = now_iso()
        write_progress(progress_path, progress)

    error: str | None = None
    try:
        if owns_session:
            progress["session_started_at"] = now_iso()
            start_session(session, args.gpu, not args.no_high_mem, log_line)
        progress["status"] = "uploading"
        write_progress(progress_path, progress)
        for clip in clips:
            # `colab upload` cannot create folders; the notebook moves these into its input folder.
            call_colab(["upload", "--session", session, str(clip), f"/content/s3in__{clip.name}"], label=f"upload {clip.name}", timeout=600, on_line=log_line)
        work = output_dir / f"work_{uuid.uuid4().hex[:8]}"
        work.mkdir()
        notebook_copy = work / NOTEBOOK.name
        notebook_copy.write_bytes(NOTEBOOK.read_bytes())
        progress["status"] = "upscaling"
        progress["exec_started_at"] = now_iso()
        write_progress(progress_path, progress)
        if args.detached:
            env = {"S3_DIT_MODEL": MODELS[args.model], "S3_BATCH_SIZE": str(args.batch_size)}
            lines = colab_detached.run(session, notebook_copy, env, "/content/s3_run", poll_s=args.poll, max_wait=args.timeout,
                                       on_line=log_line, alive=lambda: session_alive(session))
        else:
            lines = call_colab(["exec", "--session", session, "--timeout", str(int(args.timeout)),
                                "--env", f"S3_DIT_MODEL={MODELS[args.model]}", "--env", f"S3_BATCH_SIZE={args.batch_size}",
                                "--file", str(notebook_copy)], label="SeedVR2", timeout=args.timeout + 60, on_line=log_line)
        progress["exec_finished_at"] = now_iso()
        progress["seconds"] = {parts[1]: float(parts[2]) for parts in (line.split() for line in lines if line.startswith("SEEDVR2_SECONDS:")) if len(parts) == 3}
        tar_path = work / "s3_out.tar"
        call_colab(["download", "--session", session, "/content/s3_out.tar", str(tar_path)], label="download", timeout=900, on_line=log_line)
        with tarfile.open(tar_path) as archive:
            archive.extractall(output_dir, filter="data")
        missing = [clip.name for clip in clips if not (output_dir / f"{clip.stem}_1080.mp4").is_file()]
        if missing:
            raise ValueError(f"no 1080p output for: {', '.join(missing)}")
        progress["outputs"] = [str(output_dir / f"{clip.stem}_1080.mp4") for clip in clips]
    except (ColabError, ValueError, OSError, tarfile.TarError, RuntimeError) as exc:
        error = str(exc)
    finally:
        if owns_session:
            try:
                stop_session(session, log_line)
                progress["session_status"] = "stopped"
            except ColabError as exc:
                progress["session_status"] = "stop_failed"
                progress["cleanup_error"] = str(exc)
            progress["session_stopped_at"] = now_iso()
        else:
            progress["session_status"] = "active"
    progress.update({"status": "completed" if error is None else "failed", "error": error})
    write_progress(progress_path, progress)
    return progress


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("clips", nargs="*", type=Path)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("final"))
    parser.add_argument("--model", choices=sorted(MODELS), default="7b")
    parser.add_argument("--batch-size", type=int, default=81)
    parser.add_argument("--detached", action="store_true",
                        help="run SeedVR2 as a detached process on the runtime and poll it (colab_detached.py)")
    parser.add_argument("--poll", type=float, default=30, help="seconds between polls with --detached")
    parser.add_argument("--progress", type=Path)
    parser.add_argument("--session", help="reuse this running session and leave it up")
    # Not COLAB_GPU: h3.sh sets that to A100 for the draft runner; the stages default to G4.
    parser.add_argument("--gpu", default=os.environ.get("H3_STAGE_GPU", "G4"))
    parser.add_argument("--no-high-mem", action="store_true")
    parser.add_argument("--timeout", type=float, default=float(os.environ.get("H3_UPSCALE_EXEC_TIMEOUT", "5400")))
    args = parser.parse_args(argv)
    try:
        progress = run(args)
    except (ColabError, ValueError, OSError) as exc:
        print(f"[upscale] {exc}", file=sys.stderr)
        return 1
    print(json.dumps({k: progress.get(k) for k in ("status", "session", "seconds", "error")}, ensure_ascii=False))
    return 0 if progress["status"] == "completed" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
