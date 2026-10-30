#!/usr/bin/env python3
"""Paint first frames on Colab with Qwen-Image-Edit-2509, one reusable session for a batch.

The upstream H3 runner only makes video. This drives this skill's own notebook
(`assets/qwen_image_edit.ipynb`) the same way: upload the reference pictures and the prompt,
`colab exec` the notebook with the job's settings as environment variables, download the PNG,
write `progress.json` as it goes. Same Colab CLI, same session names, so a batch can share the
session the H3 clips use afterwards (`--session NAME`).

  images.py batch --manifest ff.json --output-dir out/ [--progress out/progress.json]
                  [--session NAME] [--new-session] [--stop-on-complete] [--gpu A100] [--no-high-mem]
                  [--timeout 1800] [--only s01,s02]
  images.py start --session NAME [--gpu A100] [--no-high-mem]
  images.py stop --session NAME

Manifest: {"jobs": [{"id", "title", "reference_images": [1-3 paths], "prompt_file" | "prompt",
  "negative_file"?, "width" (1312), "height" (736), "seed"?, "steps"?, "cfg"?, "lora"? (true),
  "latent"? ("empty" | "image1"), "output_name" ("<id>.png")}]}
Relative paths resolve against the manifest's directory. `scripts/check_images_manifest.py`
checks all of it offline first (`h3.sh images` runs it before this).

Without --session a session is created and stopped at the end; with --session an existing one is
reused and left running unless --stop-on-complete (or --new-session, which creates it under that
name and owns it). An exec timeout stops nothing on the remote: look at progress.json and rerun
only the jobs that are not `completed` (--only), or every job is paid for again.
Standard library only. Contains no credentials; the Colab CLI reads its own token.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Callable

SKILL_DIR = Path(__file__).resolve().parents[1]
NOTEBOOK = SKILL_DIR / "assets" / "qwen_image_edit.ipynb"
AUTH = os.environ.get("COLAB_AUTH", "oauth2")
ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
SAFE_RE = re.compile(r"[^A-Za-z0-9_-]+")
MAX_AREA = 1920 * 1088  # the H3 canvas cap; a first frame may be as large as the clip
MAX_JOBS = 40


class ColabError(RuntimeError):
    pass


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def write_progress(path: Path | None, state: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def call_colab(arguments: list[str], *, label: str, timeout: float, on_line: Callable[[str], None] | None = None) -> list[str]:
    colab = shutil.which("colab")
    if not colab:
        raise ColabError("Colab CLI is not on PATH; run bootstrap.sh install")
    command = [colab, f"--auth={AUTH}", *arguments]
    child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, encoding="utf-8", errors="replace", bufsize=1)
    lines: list[str] = []
    deadline = time.monotonic() + timeout
    assert child.stdout is not None
    try:
        for raw in child.stdout:
            line = ANSI_RE.sub("", raw).replace("\r", "").rstrip("\n")
            lines.append(line)
            if on_line and line:
                on_line(line)
            if time.monotonic() > deadline:
                child.kill()
                raise ColabError(f"{label} timed out after {timeout:.0f}s (the remote may still be running)")
        child.wait(timeout=60)
    finally:
        if child.poll() is None:
            child.kill()
    if child.returncode != 0:
        tail = "\n".join(line for line in lines[-12:] if line)
        raise ColabError(f"{label} failed (exit {child.returncode})" + (f":\n{tail}" if tail else ""))
    return lines


# Accelerators with a single machine shape: Colab rejects G4 outright when --high-mem is asked for
# ("Backend rejected accelerator 'G4'", 2026-10-30), and ignores it for L4.
SINGLE_SHAPE_GPUS = frozenset({"G4", "L4"})


def start_session(session: str, gpu: str, high_mem: bool, on_line: Callable[[str], None] | None = None) -> None:
    args = ["new", "--session", session, "--gpu", gpu]
    if high_mem and gpu.upper() not in SINGLE_SHAPE_GPUS:
        args.append("--high-mem")
    call_colab(args, label=f"create Colab session {session}", timeout=900, on_line=on_line)


def stop_session(session: str, on_line: Callable[[str], None] | None = None) -> None:
    call_colab(["stop", "--session", session], label=f"stop Colab session {session}", timeout=300, on_line=on_line)


def resolve_path(base: Path, value: Any) -> Path:
    path = Path(str(value)).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def resolve_jobs(manifest_path: Path, output_dir: Path, only: set[str] | None) -> list[dict[str, Any]]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    jobs = data.get("jobs") if isinstance(data, dict) else None
    if not isinstance(jobs, list) or not jobs:
        raise ValueError("Manifest must contain a non-empty jobs list.")
    if len(jobs) > MAX_JOBS:
        raise ValueError(f"A single batch may contain at most {MAX_JOBS} images; split the manifest.")
    base = manifest_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    resolved: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_outputs: set[Path] = set()
    for index, raw in enumerate(jobs, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"Job {index} must be an object.")
        job_id = SAFE_RE.sub("-", str(raw.get("id") or "")).strip("-")[:64]
        if not job_id:
            raise ValueError(f"Job {index} needs an id.")
        if job_id in seen_ids:
            raise ValueError(f"Job {index} duplicates job id {job_id!r}.")
        seen_ids.add(job_id)
        if only is not None and job_id not in only:
            continue
        refs = raw.get("reference_images")
        if not isinstance(refs, list) or not 1 <= len(refs) <= 3:
            raise ValueError(f"Job {job_id} must have 1-3 reference images.")
        images = []
        for ref in refs:
            path = resolve_path(base, ref)
            if not path.is_file() or path.stat().st_size == 0:
                raise ValueError(f"Job {job_id}: reference image missing or empty: {path}")
            images.append(path)
        width = int(raw.get("width", 1312))
        height = int(raw.get("height", 736))
        if width <= 0 or height <= 0 or width % 16 or height % 16 or width * height > MAX_AREA:
            raise ValueError(f"Job {job_id}: {width}x{height} must be multiples of 16 within the 1920x1088 area.")
        if raw.get("prompt_file"):
            prompt_path = resolve_path(base, raw["prompt_file"])
            prompt = prompt_path.read_text(encoding="utf-8")
        else:
            prompt = str(raw.get("prompt", ""))
        if not prompt.strip():
            raise ValueError(f"Job {job_id} needs a non-empty prompt.")
        negative = resolve_path(base, raw["negative_file"]).read_text(encoding="utf-8") if raw.get("negative_file") else str(raw.get("negative", ""))
        seed = raw.get("seed")
        if seed not in (None, "") and not 0 <= int(seed) < 2**53:
            raise ValueError(f"Job {job_id}: seed must be between 0 and 2^53-1.")
        latent = str(raw.get("latent", "empty"))
        if latent not in {"empty", "image1"}:
            raise ValueError(f"Job {job_id}: latent must be empty or image1.")
        stem = SAFE_RE.sub("-", re.sub(r"\.png$", "", str(raw.get("output_name") or job_id), flags=re.IGNORECASE)).strip("-") or job_id
        output = (output_dir / f"{stem}.png").resolve()
        if output in seen_outputs:
            raise ValueError(f"Multiple jobs target the same output: {output}")
        seen_outputs.add(output)
        resolved.append({
            "id": job_id,
            "title": str(raw.get("title") or job_id)[:120],
            "reference_images": images,
            "prompt": prompt,
            "negative": negative,
            "width": width,
            "height": height,
            "seed": None if seed in (None, "") else int(seed),
            "steps": raw.get("steps"),
            "cfg": raw.get("cfg"),
            "lora": raw.get("lora", True),
            "latent": latent,
            "output_path": output,
        })
    if not resolved:
        raise ValueError("No job matched --only.")
    return resolved


def verify_png(path: Path, width: int, height: int) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        raise ColabError(f"downloaded file is missing or empty: {path}")
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ColabError(f"downloaded file is not a PNG: {path}")
    got = (int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big"))
    if got != (width, height):
        raise ColabError(f"{path.name} is {got[0]}x{got[1]}, not the {width}x{height} canvas")


def run_batch(args: argparse.Namespace) -> dict[str, Any]:
    if not NOTEBOOK.is_file():
        raise FileNotFoundError(f"notebook not found: {NOTEBOOK}")
    manifest_path = args.manifest.expanduser().resolve()
    only = {s.strip() for s in args.only.split(",") if s.strip()} if args.only else None
    jobs = resolve_jobs(manifest_path, args.output_dir.expanduser().resolve(), only)
    session = args.session or f"qie-{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}-{uuid.uuid4().hex[:6]}"
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", session):
        raise ValueError("Invalid Colab session name.")
    owns_session = args.session is None or args.new_session
    progress_path = args.progress.expanduser().resolve() if args.progress else None
    progress: dict[str, Any] = {
        "task": "images",
        "status": "starting",
        "session": session,
        "gpu": args.gpu,
        "notebook": NOTEBOOK.name,
        "jobs": [{"id": j["id"], "title": j["title"], "status": "queued", "output": str(j["output_path"])} for j in jobs],
        "log_tail": [],
        "updated_at": now_iso(),
    }
    write_progress(progress_path, progress)

    def log_line(line: str) -> None:
        if len(line) > 320:
            line = line[:317] + "..."
        progress["log_tail"] = (progress["log_tail"] + [line])[-30:]
        progress["updated_at"] = now_iso()
        write_progress(progress_path, progress)

    def save(status: str | None = None) -> None:
        if status:
            progress["status"] = status
        progress["updated_at"] = now_iso()
        write_progress(progress_path, progress)

    work_root = manifest_path.parent / f"work_{uuid.uuid4().hex[:8]}"
    work_root.mkdir(parents=True, exist_ok=True)
    error: str | None = None
    try:
        if owns_session:
            start_session(session, args.gpu, not args.no_high_mem, log_line)
        save("running")
        for index, job in enumerate(jobs):
            current = progress["jobs"][index]
            current.update({"status": "uploading", "started_at": now_iso()})
            progress["current_job"] = job["id"]
            save()
            remote_prefix = f"/content/qie_{job['id']}"
            remote_refs = []
            for n, image in enumerate(job["reference_images"], start=1):
                remote = f"{remote_prefix}_reference_{n}.img"
                call_colab(["upload", "--session", session, str(image), remote], label=f"upload reference {n} for {job['title']}", timeout=600, on_line=log_line)
                remote_refs.append(remote)
            prompt_path = work_root / f"{job['id']}.txt"
            prompt_path.write_text(job["prompt"], encoding="utf-8")
            remote_prompt = f"{remote_prefix}_prompt.txt"
            call_colab(["upload", "--session", session, str(prompt_path), remote_prompt], label=f"upload prompt for {job['title']}", timeout=120, on_line=log_line)
            env = [
                f"QIE_WIDTH={job['width']}",
                f"QIE_HEIGHT={job['height']}",
                f"QIE_PROMPT_FILE={remote_prompt}",
                "QIE_REFERENCE_IMAGES=" + json.dumps(remote_refs, separators=(",", ":")),
                f"QIE_OUTPUT_PATH={remote_prefix}_output.png",
                f"QIE_OUTPUT_PREFIX=qie_{job['id'][:20]}",
                f"QIE_LATENT={job['latent']}",
                f"QIE_LORA={'on' if job['lora'] else 'off'}",
                f"QIE_JOB_TIMEOUT_SECONDS={min(args.timeout, 7200):.0f}",
            ]
            if job["negative"].strip():
                negative_path = work_root / f"{job['id']}.neg.txt"
                negative_path.write_text(job["negative"], encoding="utf-8")
                remote_negative = f"{remote_prefix}_negative.txt"
                call_colab(["upload", "--session", session, str(negative_path), remote_negative], label=f"upload negative prompt for {job['title']}", timeout=120, on_line=log_line)
                env.append(f"QIE_NEGATIVE_FILE={remote_negative}")
            if job["seed"] is not None:
                env.append(f"QIE_SEED={job['seed']}")
            if job["steps"] is not None:
                env.append(f"QIE_STEPS={int(job['steps'])}")
            if job["cfg"] is not None:
                env.append(f"QIE_CFG={float(job['cfg'])}")
            exec_args = ["exec", "--session", session, "--timeout", str(int(args.timeout))]
            for value in env:
                exec_args.extend(["--env", value])
            notebook_copy = work_root / job["id"] / NOTEBOOK.name
            notebook_copy.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(NOTEBOOK, notebook_copy)
            exec_args.extend(["--file", str(notebook_copy)])
            current.update({"status": "generating", "seed": job["seed"], "size": f"{job['width']}x{job['height']}"})
            save()
            lines = call_colab(exec_args, label=f"paint {job['title']}", timeout=args.timeout + 60, on_line=log_line)
            for line in lines:
                if line.startswith("QIE_SEED_USED:"):
                    current["seed"] = int(line.split(":", 1)[1].strip())
            current["status"] = "downloading"
            save()
            call_colab(["download", "--session", session, f"{remote_prefix}_output.png", str(job["output_path"])], label=f"download {job['title']}", timeout=600, on_line=log_line)
            verify_png(job["output_path"], job["width"], job["height"])
            current.update({"status": "completed", "finished_at": now_iso(), "bytes": job["output_path"].stat().st_size})
            save()
    except (ColabError, ValueError, OSError) as exc:
        error = str(exc)
        for item in progress["jobs"]:
            if item["id"] == progress.get("current_job") and item["status"] not in {"completed", "failed"}:
                item.update({"status": "failed", "error": error, "finished_at": now_iso()})
            elif item["status"] == "queued":
                item["status"] = "cancelled"
    finally:
        if owns_session or args.stop_on_complete:
            save("stopping_session")
            try:
                stop_session(session, log_line)
                progress["session_status"] = "stopped"
            except ColabError as exc:
                progress["session_status"] = "stop_failed"
                progress["cleanup_error"] = str(exc)
        else:
            progress["session_status"] = "active"
    completed = sum(item["status"] == "completed" for item in progress["jobs"])
    failed = sum(item["status"] == "failed" for item in progress["jobs"])
    progress.update({"completed": completed, "failed": failed, "error": error, "status": "completed" if error is None and failed == 0 else "failed"})
    save()
    return progress


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = parser.add_subparsers(dest="command", required=True)
    start = sub.add_parser("start")
    start.add_argument("--session", required=True)
    start.add_argument("--gpu", default=os.environ.get("COLAB_GPU", "A100"))
    start.add_argument("--no-high-mem", action="store_true")
    stop = sub.add_parser("stop")
    stop.add_argument("--session", required=True)
    batch = sub.add_parser("batch")
    batch.add_argument("--manifest", type=Path, required=True)
    batch.add_argument("--output-dir", type=Path, default=Path("output"))
    batch.add_argument("--progress", type=Path)
    batch.add_argument("--session")
    batch.add_argument("--new-session", action="store_true", help="create --session instead of reusing it (and own it)")
    batch.add_argument("--stop-on-complete", action="store_true")
    batch.add_argument("--gpu", default=os.environ.get("COLAB_GPU", "A100"))
    batch.add_argument("--no-high-mem", action="store_true")
    batch.add_argument("--timeout", type=float, default=float(os.environ.get("QIE_EXEC_TIMEOUT", "1800")))
    batch.add_argument("--only", help="comma-separated job ids to run (the rest are skipped)")
    args = parser.parse_args(argv)
    try:
        if args.command == "start":
            start_session(args.session, args.gpu, not args.no_high_mem, print)
            return 0
        if args.command == "stop":
            stop_session(args.session, print)
            return 0
        progress = run_batch(args)
    except (ColabError, ValueError, OSError) as exc:
        print(f"[images] {exc}", file=sys.stderr)
        return 1
    print(json.dumps(progress, ensure_ascii=False))
    return 0 if progress["status"] == "completed" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
