#!/usr/bin/env python3
"""Stage 2 of the three-stage H3 route: refine draft clips at the canvas size on one Colab session.

Each job uploads a stage-1 draft MP4, its first frame at the refine canvas and the prompt, runs
assets/h3_refine.ipynb (stretch the draft to the canvas, re-encode it, re-denoise only the low-noise
tail from `sigma_start` with the first frame as a keyframe) and downloads the refined MP4. Why the
tail starts at a sigma and not at "step 10 of 20", the pilot numbers and the receipts are in
references/three-stage.md.

  refine.py --manifest r.json --check
  refine.py --manifest r.json --output-dir out/ [--progress p.json] [--session NAME] [--only a,b]

Manifest `jobs[]`: id, input_video, first_frame, prompt_file (or prompt), output_name; optional
width/height (default 1312x736), sigma_start (default 0.5), steps (default 10), seed (default 0),
guide ("none" default, or "draft": the whole draft also anchors every frame), sigmas (an explicit
falling list ending in 0 that replaces sigma_start/steps) and sampler (default res_multistep).
Relative paths are relative to the manifest. Without --session the runner creates a session on
H3_STAGE_GPU (default G4) and stops it at the end; with --session it reuses that one and leaves it up.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from images import ColabError, call_colab, now_iso, resolve_path, start_session, stop_session, write_progress  # noqa: E402
import colab_detached  # noqa: E402
from colab_detached import session_alive  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parents[1]
NOTEBOOK = SKILL_DIR / "assets" / "h3_refine.ipynb"
MAX_AREA = 1344 * 768
MAX_JOBS = 20
ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,40}$")
SAMPLER_RE = re.compile(r"^[a-z0-9_]{1,40}$")


def load_jobs(manifest_path: Path, output_dir: Path | None, only: set[str] | None) -> tuple[list[dict[str, Any]], list[str]]:
    """The jobs to run and every problem that would waste a session; nothing is uploaded here."""
    errors: list[str] = []
    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [f"cannot read {manifest_path}: {exc}"]
    entries = raw.get("jobs") if isinstance(raw, dict) else None
    if not isinstance(entries, list) or not entries:
        return [], ["the manifest needs a non-empty jobs list"]
    if len(entries) > MAX_JOBS:
        errors.append(f"{len(entries)} jobs; a batch takes at most {MAX_JOBS}")
    base = manifest_path.parent
    jobs: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_outputs: set[str] = set()
    for index, entry in enumerate(entries):
        where = f"job {index + 1}"
        if not isinstance(entry, dict):
            errors.append(f"{where}: must be an object")
            continue
        job_id = str(entry.get("id", ""))
        if not ID_RE.match(job_id):
            errors.append(f"{where}: id must be 1-40 letters, digits, _ or -")
        where = job_id or where
        if job_id in seen_ids:
            errors.append(f"{where}: duplicate id")
        seen_ids.add(job_id)
        files: dict[str, Path] = {}
        for key in ("input_video", "first_frame"):
            value = entry.get(key)
            path = resolve_path(base, value) if value else None
            if path is None or not path.is_file() or path.stat().st_size == 0:
                errors.append(f"{where}: {key} missing or empty: {value}")
            else:
                files[key] = path
        prompt = entry.get("prompt")
        if entry.get("prompt_file"):
            prompt_path = resolve_path(base, entry["prompt_file"])
            prompt = prompt_path.read_text(encoding="utf-8") if prompt_path.is_file() else None
            if prompt is None:
                errors.append(f"{where}: prompt_file missing: {entry['prompt_file']}")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{where}: the prompt is empty")
        width, height = entry.get("width", 1312), entry.get("height", 736)
        for name, value in (("width", width), ("height", height)):
            if not isinstance(value, int) or value <= 0 or value % 32:
                errors.append(f"{where}: {name}={value} must be a positive multiple of 32")
        if isinstance(width, int) and isinstance(height, int) and width * height > MAX_AREA:
            errors.append(f"{where}: {width}x{height} exceeds the 1344x768 area H3 was trained on")
        sigma = entry.get("sigma_start", 0.5)
        if not isinstance(sigma, (int, float)) or not 0.05 <= sigma <= 0.95:
            errors.append(f"{where}: sigma_start={sigma} must be between 0.05 and 0.95")
        steps = entry.get("steps", 10)
        if not isinstance(steps, int) or not 1 <= steps <= 30:
            errors.append(f"{where}: steps={steps} must be an integer from 1 to 30")
        guide = entry.get("guide", "none")
        if guide not in {"none", "draft"}:
            errors.append(f"{where}: guide={guide!r} must be none or draft")
        sigmas = entry.get("sigmas")
        if sigmas is not None and not (
            isinstance(sigmas, list) and 2 <= len(sigmas) <= 31 and all(isinstance(v, (int, float)) for v in sigmas)
            and sigmas[0] < 1 and sigmas[-1] == 0 and all(a > b for a, b in zip(sigmas, sigmas[1:]))
        ):
            errors.append(f"{where}: sigmas must be 2-31 numbers falling from below 1 to 0")
        sampler = entry.get("sampler", "res_multistep")
        if not isinstance(sampler, str) or not SAMPLER_RE.match(sampler):
            errors.append(f"{where}: sampler={sampler!r} is not a sampler name")
        seed = entry.get("seed", 0)
        if not isinstance(seed, int) or seed < 0:
            errors.append(f"{where}: seed={seed} must be a non-negative integer")
        output_name = str(entry.get("output_name") or f"{job_id}.mp4")
        if not output_name.endswith(".mp4") or "/" in output_name or "\\" in output_name:
            errors.append(f"{where}: output_name must be a plain .mp4 file name")
        if output_name in seen_outputs:
            errors.append(f"{where}: duplicate output_name {output_name}")
        seen_outputs.add(output_name)
        if only and job_id not in only:
            continue
        jobs.append({
            "id": job_id, "title": entry.get("title") or job_id, "prompt": prompt, "width": width, "height": height,
            "sigma_start": sigma, "steps": steps, "seed": seed, "guide": guide, "sampler": sampler,
            "sigmas": ", ".join(str(v) for v in sigmas) if sigmas else "", **files,
            "output_path": (output_dir / output_name) if output_dir else None,
        })
    if only and not jobs and not errors:
        errors.append(f"--only matched no job: {sorted(only)}")
    return jobs, errors


def run_batch(args: argparse.Namespace) -> dict[str, Any]:
    if not NOTEBOOK.is_file():
        raise FileNotFoundError(f"notebook not found: {NOTEBOOK}")
    manifest_path = args.manifest.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    only = {s.strip() for s in args.only.split(",") if s.strip()} if args.only else None
    jobs, errors = load_jobs(manifest_path, output_dir, only)
    if errors:
        raise ValueError("manifest problems:\n  " + "\n  ".join(errors))
    output_dir.mkdir(parents=True, exist_ok=True)
    session = args.session or f"h3r-{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}-{uuid.uuid4().hex[:6]}"
    owns_session = args.session is None
    progress_path = args.progress.expanduser().resolve() if args.progress else None
    progress: dict[str, Any] = {
        "task": "refine", "status": "starting", "session": session, "gpu": args.gpu, "notebook": NOTEBOOK.name,
        "jobs": [{"id": j["id"], "title": j["title"], "status": "queued", "sigma_start": j["sigma_start"],
                  "steps": j["steps"], "seed": j["seed"], "guide": j["guide"], "sampler": j["sampler"],
                  "output": str(j["output_path"])} for j in jobs],
        "log_tail": [], "updated_at": now_iso(),
    }
    write_progress(progress_path, progress)

    def log_line(line: str) -> None:
        progress["log_tail"] = (progress["log_tail"] + [line[:320]])[-30:]
        progress["updated_at"] = now_iso()
        write_progress(progress_path, progress)

    work_root = output_dir / f"work_{uuid.uuid4().hex[:8]}"
    work_root.mkdir(parents=True, exist_ok=True)
    error: str | None = None
    try:
        if owns_session:
            progress["session_started_at"] = now_iso()
            start_session(session, args.gpu, not args.no_high_mem, log_line)
        progress["status"] = "running"
        for index, job in enumerate(jobs):
            current = progress["jobs"][index]
            current.update({"status": "uploading", "started_at": now_iso()})
            progress["current_job"] = job["id"]
            write_progress(progress_path, progress)
            remote = f"/content/h3r_{job['id']}"
            prompt_path = work_root / f"{job['id']}.txt"
            prompt_path.write_text(job["prompt"], encoding="utf-8")
            for local, target in ((job["input_video"], f"{remote}_draft.mp4"), (job["first_frame"], f"{remote}_first_frame.png"), (prompt_path, f"{remote}_prompt.txt")):
                call_colab(["upload", "--session", session, str(local), target], label=f"upload {Path(target).name}", timeout=600, on_line=log_line)
            env = {
                "R_INPUT_VIDEO": f"{remote}_draft.mp4", "R_FIRST_FRAME": f"{remote}_first_frame.png",
                "R_PROMPT_FILE": f"{remote}_prompt.txt", "R_WIDTH": str(job["width"]), "R_HEIGHT": str(job["height"]),
                "R_SIGMA_START": str(job["sigma_start"]), "R_STEPS": str(job["steps"]), "R_SEED": str(job["seed"]),
                "R_GUIDE": job["guide"], "R_SAMPLER": job["sampler"], "R_SIGMAS": job["sigmas"],
                "R_OUTPUT_PATH": f"{remote}_refined.mp4", "R_JOB_TIMEOUT_SECONDS": f"{min(args.timeout, 7200):.0f}",
            }
            exec_args = ["exec", "--session", session, "--timeout", str(int(args.timeout))]
            for key, value in env.items():
                exec_args.extend(["--env", f"{key}={value}"])
            notebook_copy = work_root / job["id"] / NOTEBOOK.name
            notebook_copy.parent.mkdir(parents=True, exist_ok=True)
            notebook_copy.write_bytes(NOTEBOOK.read_bytes())
            exec_args.extend(["--file", str(notebook_copy)])
            current["status"] = "refining"
            write_progress(progress_path, progress)
            if args.detached:
                lines = colab_detached.run(session, notebook_copy, env, remote, poll_s=args.poll, max_wait=args.timeout,
                                           on_line=log_line, alive=lambda: session_alive(session))
            else:
                lines = call_colab(exec_args, label=f"refine {job['title']}", timeout=args.timeout + 60, on_line=log_line)
            for line in lines:
                if line.startswith("REFINE_SECONDS:"):
                    current["graph_seconds"] = float(line.split(":", 1)[1])
                elif line.startswith("REFINE_FRAMES:"):
                    current["frames"] = int(line.split(":", 1)[1])
                elif line.startswith("REFINE_SIGMAS:"):
                    current["sigmas"] = line.split(":", 1)[1].strip()
            current["status"] = "downloading"
            write_progress(progress_path, progress)
            call_colab(["download", "--session", session, f"{remote}_refined.mp4", str(job["output_path"])], label=f"download {job['title']}", timeout=600, on_line=log_line)
            current.update({"status": "completed", "finished_at": now_iso(), "bytes": job["output_path"].stat().st_size})
            write_progress(progress_path, progress)
    except (ColabError, ValueError, OSError, RuntimeError) as exc:
        error = str(exc)
        for item in progress["jobs"]:
            if item["id"] == progress.get("current_job") and item["status"] not in {"completed", "failed"}:
                item.update({"status": "failed", "error": error, "finished_at": now_iso()})
            elif item["status"] == "queued":
                item["status"] = "cancelled"
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
    completed = sum(item["status"] == "completed" for item in progress["jobs"])
    progress.update({"completed": completed, "error": error, "status": "completed" if error is None else "failed"})
    write_progress(progress_path, progress)
    return progress


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--check", action="store_true", help="only check the manifest; no Colab call")
    parser.add_argument("--output-dir", type=Path, default=Path("refined"))
    parser.add_argument("--progress", type=Path)
    parser.add_argument("--session", help="reuse this running session and leave it up")
    # Not COLAB_GPU: h3.sh sets that to A100 for the draft runner; the stages default to G4.
    parser.add_argument("--gpu", default=os.environ.get("H3_STAGE_GPU", "G4"))
    parser.add_argument("--no-high-mem", action="store_true")
    parser.add_argument("--timeout", type=float, default=float(os.environ.get("H3_REFINE_EXEC_TIMEOUT", "3600")))
    parser.add_argument("--only", help="comma-separated job ids to run")
    parser.add_argument("--detached", action="store_true",
                        help="run each job as a detached process on the runtime and poll it (colab_detached.py)")
    parser.add_argument("--poll", type=float, default=30, help="seconds between polls with --detached")
    args = parser.parse_args(argv)
    if args.check:
        jobs, errors = load_jobs(args.manifest.expanduser().resolve(), None, None)
        for problem in errors:
            print(f"[refine] {problem}", file=sys.stderr)
        print(f"[refine] {args.manifest}: {len(jobs)} job(s), {len(errors)} error(s)")
        return 1 if errors else 0
    try:
        progress = run_batch(args)
    except (ColabError, ValueError, OSError) as exc:
        print(f"[refine] {exc}", file=sys.stderr)
        return 1
    print(json.dumps({k: progress.get(k) for k in ("status", "session", "completed", "error")}, ensure_ascii=False))
    return 0 if progress["status"] == "completed" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
