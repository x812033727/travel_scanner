#!/usr/bin/env python3
"""Drive first_frames_colab.py on a Colab session from a browserless shell (Colab CLI, OAuth2 token
already paired by .agents/skills/minimax-h3-colab/scripts/bootstrap.sh).

    python3 ff_runner.py --manifest manifest-pilot.json --out <dir> [--profile lightning|base]
                         [--gpu A100] [--no-high-mem] [--session NAME] [--timeout 7200] [--keep]

Steps: tar the manifest and its reference pictures → `colab new` (A100, high RAM) → `colab upload`
the tar → `colab exec` a one-cell notebook that runs first_frames_colab.py → `colab download` the
output tar → extract into --out (pictures + results.json) → `colab stop` (unless --keep).
progress.json in --out records each step. Nothing here prints or stores a credential.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "first_frames_colab.py"
AUTH = os.environ.get("COLAB_CLI_AUTH", "oauth2")


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def colab(args, *, timeout, log):
    command = [shutil.which("colab") or "colab", f"--auth={AUTH}", *args]
    log(f"$ colab {' '.join(args)}")
    child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1)
    output = []
    deadline = time.monotonic() + timeout
    assert child.stdout is not None
    for line in child.stdout:
        line = line.rstrip("\n")
        output.append(line)
        log(line)
        if time.monotonic() > deadline:
            child.kill()
            raise TimeoutError(f"colab {args[0]} exceeded {timeout} s")
    code = child.wait()
    if code != 0:
        raise RuntimeError(f"colab {args[0]} exited {code}: {output[-1] if output else ''}")
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--profile", default="lightning", choices=["lightning", "base"])
    parser.add_argument("--gpu", default="A100")
    parser.add_argument("--no-high-mem", action="store_true")
    parser.add_argument("--session", default=None)
    parser.add_argument("--timeout", type=int, default=7200)
    parser.add_argument("--keep", action="store_true", help="leave the session running (reuse it with --session)")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    progress_path = out / "progress.json"
    state = {"task": "first-frames", "status": "starting", "manifest": str(manifest_path), "jobs": [job["id"] for job in manifest["jobs"]], "log_tail": [], "started_at": now()}

    def save():
        state["updated_at"] = now()
        progress_path.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

    def log(line):
        print(line, flush=True)
        state["log_tail"] = (state["log_tail"] + [line])[-40:]
        save()

    # The bundle: manifest with reference paths rewritten to refs/<n>-<basename>, plus those files.
    bundle = out / "ff_bundle.tar"
    bundled = {"jobs": []}
    seen = {}
    with tarfile.open(bundle, "w") as tar:
        for job in manifest["jobs"]:
            refs = []
            for ref in job.get("references", []):
                src = Path(ref["file"])
                if not src.is_file():
                    raise FileNotFoundError(f"{job['id']}: reference {src} is missing")
                name = seen.get(str(src))
                if name is None:
                    name = f"refs/{len(seen) + 1:02d}-{src.name}"
                    seen[str(src)] = name
                    tar.add(src, arcname=name)
                refs.append({**ref, "file": name})
            bundled["jobs"].append({**job, "references": refs})
        manifest_copy = out / "manifest.bundled.json"
        manifest_copy.write_text(json.dumps(bundled, ensure_ascii=False), encoding="utf-8")
        tar.add(manifest_copy, arcname="manifest.json")
    log(f"bundle {bundle} ({bundle.stat().st_size // 1024} KiB, {len(seen)} reference pictures, {len(bundled['jobs'])} jobs)")

    session = args.session or f"ff-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", session):
        raise ValueError("bad session name")
    state["session"] = session
    new_session = not args.session
    try:
        if new_session:
            state["status"] = "creating"
            new_args = ["new", "--session", session, "--gpu", args.gpu]
            if not args.no_high_mem:
                new_args.append("--high-mem")
            colab(new_args, timeout=900, log=log)
        state["status"] = "uploading"
        colab(["upload", "--session", session, str(bundle), "/content/ff_bundle.tar"], timeout=1800, log=log)
        notebook = out / "first_frames.ipynb"
        notebook.write_text(json.dumps({
            "nbformat": 4, "nbformat_minor": 5, "metadata": {},
            "cells": [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": SCRIPT.read_text(encoding="utf-8")}],
        }), encoding="utf-8")
        state["status"] = "running"
        env = [f"FF_BUNDLE=/content/ff_bundle.tar", f"FF_OUT=/content/ff_out.tar", f"FF_PROFILE={args.profile}"]
        exec_args = ["exec", "--session", session, "--timeout", str(args.timeout)]
        for value in env:
            exec_args.extend(["--env", value])
        exec_args.extend(["--file", str(notebook)])
        colab(exec_args, timeout=args.timeout + 120, log=log)
        state["status"] = "downloading"
        result_tar = out / "ff_out.tar"
        colab(["download", "--session", session, "/content/ff_out.tar", str(result_tar)], timeout=1800, log=log)
        with tarfile.open(result_tar) as tar:
            tar.extractall(out, filter="data")
        results = json.loads((out / "results.json").read_text(encoding="utf-8"))
        state["results"] = results
        state["status"] = "completed" if all(r["status"] == "completed" for r in results["results"]) else "partial"
        log(f"{sum(r['status'] == 'completed' for r in results['results'])}/{len(results['results'])} pictures, {results['total_seconds']} s on {results.get('gpu')}, steps {results['steps']}, lora {results.get('lora')}")
    except Exception as exc:  # noqa: BLE001
        state["status"] = "failed"
        state["error"] = str(exc)
        save()
        raise
    finally:
        if not args.keep:
            try:
                colab(["stop", "--session", session], timeout=300, log=log)
                state["session_status"] = "stopped"
            except Exception as exc:  # noqa: BLE001
                state["session_status"] = f"stop failed: {exc}"
        save()
    return 0 if state["status"] == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
