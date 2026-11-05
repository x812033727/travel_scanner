#!/usr/bin/env python3
"""Run H3 jobs on Colab with the notebook as a *detached* process on the runtime.

Why: the upstream runner keeps one `colab exec` websocket open for the whole clip (12 minutes at
1920x1088). Colab's runtime proxy drains that tunnel every so often (close code 1012,
server_draining: four times on 2026-10-28), the CLI then reports "Connection was lost", the runner
abandons the batch, and the runtime idles out half an hour later. Here the notebook's code cells
are joined into one script, started on the runtime with nohup (ComfyUI becomes its child, so it
survives kernel restarts), and the local side only polls with short execs and downloads the MP4.
A dropped tunnel costs one poll, not the clip.

  python3 -I scripts/h3_detached.py <jobs.json> --session NAME [--only s01,s02] [--poll 60] [--max-wait 2700] [--attempts 3]

jobs.json is the h3.sh/runner manifest shape (id, inference_mode, reference_images, prompt_file
or prompt, duration_seconds, width, height, seed, output_path). Each job: upload pictures and
prompt as the runner names them (/content/h3_<id>_reference_N.img, _prompt.txt), upload the
script, start it, poll /content/h3_<id>.log until H3_DETACHED_DONE or a traceback, download
/content/h3_<id>_output.mp4 to output_path, verify with ffprobe. A missing session is recreated
with h3.sh start. Progress goes to <jobs.json dir>/<id>.detached.json. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HOME = Path(os.environ.get("MINIMAX_H3_COLAB_HOME") or Path.home() / ".cache" / "minimax-h3-colab-skill")
NOTEBOOK = HOME / "assets" / "MiniMax_H3_Turbo_Colab.ipynb"
H3SH = Path(__file__).resolve().parent / "h3.sh"
DONE = "H3_DETACHED_DONE"


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    print(f"{datetime.now(timezone.utc).strftime('%H:%M:%S')} {msg}", flush=True)


def colab(args: list[str], timeout: float) -> tuple[int, str]:
    try:
        p = subprocess.run(["colab", *args], capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired as exc:
        return 124, f"timeout after {timeout}s: {(exc.stdout or b'')[-500:]!r}"


def session_alive(name: str) -> bool:
    code, out = colab(["status", "--session", name], 60)
    return code == 0 and "Status:" in out


def ensure_session(name: str) -> None:
    if session_alive(name):
        return
    log(f"session {name} missing; starting")
    p = subprocess.run(["bash", str(H3SH), "start", "--session", name], capture_output=True, text=True, timeout=900)
    log(p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr.strip()[-300:])
    if not session_alive(name):
        raise RuntimeError("could not start a Colab session")


def notebook_script() -> str:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    cells = [("".join(c["source"]) if isinstance(c["source"], list) else c["source"]) for c in nb["cells"] if c.get("cell_type") == "code"]
    body = "\n\n# ---- next cell ----\n".join(cells)
    return body


def exec_code(session: str, code: str, timeout: float) -> tuple[int, str]:
    tmp = Path("/tmp") / f"h3d_{os.getpid()}_{random.randrange(1 << 30)}.py"
    tmp.write_text(code, encoding="utf-8")
    try:
        return colab(["exec", "--session", session, "--file", str(tmp), "--timeout", str(int(timeout))], timeout + 60)
    finally:
        tmp.unlink(missing_ok=True)


def upload(session: str, local: Path, remote: str) -> None:
    code, out = colab(["upload", "--session", session, str(local), remote], 900)
    if code != 0:
        raise RuntimeError(f"upload {local.name} failed: {out[-300:]}")


def start_job(session: str, job: dict, base: Path) -> str:
    jid = job["id"]
    prefix = f"/content/h3_{jid}"
    remote_refs = []
    for i, image in enumerate(job["reference_images"], 1):
        p = Path(image) if Path(image).is_absolute() else base / image
        remote = f"{prefix}_reference_{i}.img"
        upload(session, p, remote)
        remote_refs.append(remote)
    prompt = job.get("prompt")
    if prompt is None:
        pf = Path(job["prompt_file"]) if Path(job["prompt_file"]).is_absolute() else base / job["prompt_file"]
        prompt = pf.read_text(encoding="utf-8")
    pl = Path("/tmp") / f"h3d_prompt_{jid}.txt"
    pl.write_text(prompt, encoding="utf-8")
    upload(session, pl, f"{prefix}_prompt.txt")
    pl.unlink(missing_ok=True)
    env = {
        "H3_INFERENCE_MODE": job["inference_mode"],
        "H3_WIDTH": str(job["width"]),
        "H3_HEIGHT": str(job["height"]),
        "H3_PROMPT_FILE": f"{prefix}_prompt.txt",
        "H3_DURATION_SECONDS": str(job["duration_seconds"]),
        "H3_SEED": str(job.get("seed") if job.get("seed") not in (None, "") else random.SystemRandom().randrange(0, 2**63)),
        "H3_OUTPUT_PREFIX": "MiniMax_H3_" + jid[:20],
        "H3_OUTPUT_PATH": f"{prefix}_output.mp4",
        "H3_JOB_TIMEOUT_SECONDS": "7200",
        "H3_FIRST_FRAME_MEGAPIXELS": str(round(job["width"] * job["height"] / 1e6, 3)),
    }
    if job["inference_mode"] == "reference":
        env["H3_REFERENCE_IMAGES"] = json.dumps(remote_refs, separators=(",", ":"))
    else:
        env["H3_INPUT_IMAGE"] = remote_refs[0]
    header = "import os\n" + "".join(f"os.environ[{k!r}] = {v!r}\n" for k, v in env.items()) + "os.chdir('/content')\n"
    script = header + notebook_script() + f"\nprint({DONE!r}, flush=True)\n"
    sl = Path("/tmp") / f"h3d_job_{jid}.py"
    sl.write_text(script, encoding="utf-8")
    upload(session, sl, f"{prefix}_job.py")
    sl.unlink(missing_ok=True)
    launcher = (
        "import subprocess, os\n"
        f"log = open('{prefix}.log', 'w')\n"
        f"p = subprocess.Popen(['python3', '-u', '{prefix}_job.py'], stdout=log, stderr=subprocess.STDOUT, cwd='/content', start_new_session=True)\n"
        f"open('{prefix}.pid', 'w').write(str(p.pid))\n"
        "print('launched', p.pid)\n"
    )
    code, out = exec_code(session, launcher, 120)
    if code != 0 or "launched" not in out:
        raise RuntimeError(f"launch failed: {out[-400:]}")
    return prefix


def poll(session: str, prefix: str) -> tuple[str, str]:
    """Returns (state, tail): state is running / done / failed / lost."""
    probe = (
        "import os\n"
        f"p='{prefix}'\n"
        "tail=''\n"
        "try:\n"
        "    tail=open(p+'.log',errors='replace').read()[-1500:]\n"
        "except Exception as e: tail='(no log: '+str(e)+')'\n"
        "alive=False\n"
        "try:\n"
        "    pid=int(open(p+'.pid').read()); os.kill(pid,0); alive=True\n"
        "except Exception: pass\n"
        "print('H3_PROBE', 'out' if os.path.exists(p+'_output.mp4') else 'noout', 'alive' if alive else 'dead')\n"
        "print(tail)\n"
    )
    code, out = exec_code(session, probe, 90)
    if code != 0 or "H3_PROBE" not in out:
        return "lost", out[-300:]
    flag = out.split("H3_PROBE", 1)[1].split("\n", 1)[0].split()
    tail = out.split("\n", 1)[1] if "\n" in out else ""
    if "out" in flag and DONE in tail:
        return "done", tail
    if "Traceback" in tail or "Error:" in tail.split(DONE)[0] and "dead" in flag:
        return "failed", tail
    if "dead" in flag and DONE not in tail:
        return "failed", tail
    return "running", tail


def download(session: str, prefix: str, out: Path) -> bool:
    out.parent.mkdir(parents=True, exist_ok=True)
    code, text = colab(["download", "--session", session, f"{prefix}_output.mp4", str(out)], 900)
    if code != 0 or not out.is_file() or out.stat().st_size == 0:
        return False
    if shutil.which("ffprobe"):
        p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=nb_frames", "-of", "csv=p=0", str(out)], capture_output=True, text=True)
        return p.returncode == 0 and p.stdout.strip().isdigit()
    return True


def run_job(session: str, job: dict, base: Path, poll_s: int, max_wait: int, attempts: int, progress: Path) -> bool:
    out = Path(job["output_path"])
    state = {"id": job["id"], "attempts": [], "output": str(out)}
    for attempt in range(1, attempts + 1):
        rec = {"n": attempt, "started_at": now(), "session": session}
        state["attempts"].append(rec)
        try:
            ensure_session(session)
            log(f"{job['id']} attempt {attempt}: uploading and launching")
            prefix = start_job(session, job, base)
            t0 = time.monotonic()
            last_line = ""
            while time.monotonic() - t0 < max_wait:
                time.sleep(poll_s)
                st, tail = poll(session, prefix)
                line = tail.strip().splitlines()[-1][:120] if tail.strip() else ""
                if line != last_line:
                    log(f"{job['id']} {st}: {line}")
                    last_line = line
                rec["state"] = st
                progress.write_text(json.dumps(state, ensure_ascii=False, indent=1))
                if st == "done":
                    if download(session, prefix, out):
                        rec["finished_at"] = now()
                        rec["result"] = "ok"
                        progress.write_text(json.dumps(state, ensure_ascii=False, indent=1))
                        log(f"{job['id']} done -> {out.name} ({(time.monotonic() - t0) / 60:.1f} min)")
                        return True
                    rec["result"] = "download failed"
                    break
                if st == "failed":
                    rec["result"] = "failed on runtime"
                    rec["tail"] = tail[-800:]
                    log(f"{job['id']} failed on the runtime:\n{tail[-600:]}")
                    break
                if st == "lost":
                    if not session_alive(session):
                        rec["result"] = "session lost"
                        log(f"{job['id']} session lost")
                        break
            else:
                rec["result"] = "timeout"
                log(f"{job['id']} exceeded {max_wait}s")
        except Exception as exc:  # noqa: BLE001
            rec["result"] = f"error: {exc}"[:300]
            log(f"{job['id']} attempt {attempt} error: {exc}")
        progress.write_text(json.dumps(state, ensure_ascii=False, indent=1))
    return False


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--session", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--poll", type=int, default=60)
    ap.add_argument("--max-wait", type=int, default=2700)
    ap.add_argument("--attempts", type=int, default=3)
    a = ap.parse_args(argv)
    mpath = Path(a.manifest).resolve()
    jobs = json.loads(mpath.read_text(encoding="utf-8"))["jobs"]
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    failed = []
    for job in jobs:
        if only and job["id"] not in only:
            continue
        out = Path(job["output_path"])
        if out.is_file() and out.stat().st_size > 0:
            log(f"{job['id']} already done")
            continue
        ok = run_job(a.session, job, mpath.parent, a.poll, a.max_wait, a.attempts, mpath.parent / f"{job['id']}.detached.json")
        if not ok:
            failed.append(job["id"])
            log(f"{job['id']} GAVE UP")
    log(f"run end; failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
