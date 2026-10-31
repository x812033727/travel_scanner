#!/usr/bin/env python3
"""Run one notebook as a detached process on a Colab runtime and wait for it with short polls.

`colab exec` keeps one websocket open for the whole run. Colab's runtime proxy drains it every so
often (close code 1012) or the CLI stops receiving messages while the kernel keeps working, so a
refine or SeedVR2 batch of several minutes often fails or hangs although the GPU finished
(e033/e034, 2026-10-30: two silent hangs of 20 and 55 minutes, a watchdog kill every hour or so).
Here the notebook's code cells are joined into one script with its environment set at the top,
uploaded, and started with Popen(start_new_session=True), so it outlives the kernel and any dropped
tunnel. The local side polls with execs of a few seconds (each with its own timeout) and returns
once the script printed its done marker. A dropped tunnel costs one poll, not the run.

Used by refine.py and upscale.py with --detached; h3_detached.py does the same for the H3 notebook.
Standard library only.
"""
from __future__ import annotations

import json
import os
import random
import subprocess
import time
from pathlib import Path
from typing import Callable

DONE = "COLAB_DETACHED_DONE"


def colab(args: list[str], timeout: float) -> tuple[int, str]:
    try:
        auth = os.environ.get("COLAB_AUTH", "oauth2")
        p = subprocess.run(["colab", f"--auth={auth}", *args], capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired as exc:
        return 124, f"timeout after {timeout}s: {(exc.stdout or b'')[-300:]!r}"


def session_alive(name: str) -> bool:
    code, out = colab(["status", "--session", name], 60)
    return code == 0 and "Status:" in out


def notebook_script(notebook: Path, env: dict[str, str]) -> str:
    nb = json.loads(notebook.read_text(encoding="utf-8"))
    cells = ["".join(c["source"]) if isinstance(c["source"], list) else c["source"] for c in nb["cells"] if c.get("cell_type") == "code"]
    header = "import os\n" + "".join(f"os.environ[{k!r}] = {v!r}\n" for k, v in env.items()) + "os.chdir('/content')\n"
    return header + "\n\n# ---- next cell ----\n".join(cells) + f"\nprint({DONE!r}, flush=True)\n"


def _exec_code(session: str, code: str, timeout: float) -> tuple[int, str]:
    tmp = Path("/tmp") / f"cd_{os.getpid()}_{random.randrange(1 << 30)}.py"
    tmp.write_text(code, encoding="utf-8")
    try:
        return colab(["exec", "--session", session, "--file", str(tmp), "--timeout", str(int(timeout))], timeout + 60)
    finally:
        tmp.unlink(missing_ok=True)


def launch(session: str, notebook: Path, env: dict[str, str], prefix: str) -> None:
    """Upload <prefix>_job.py and start it; its output goes to <prefix>.log, its pid to <prefix>.pid."""
    local = Path("/tmp") / f"cd_job_{os.getpid()}_{random.randrange(1 << 30)}.py"
    local.write_text(notebook_script(notebook, env), encoding="utf-8")
    try:
        code, out = colab(["upload", "--session", session, str(local), f"{prefix}_job.py"], 600)
    finally:
        local.unlink(missing_ok=True)
    if code != 0:
        raise RuntimeError(f"upload {prefix}_job.py failed: {out[-300:]}")
    launcher = (
        "import subprocess\n"
        f"log = open('{prefix}.log', 'w')\n"
        f"p = subprocess.Popen(['python3', '-u', '{prefix}_job.py'], stdout=log, stderr=subprocess.STDOUT, cwd='/content', start_new_session=True)\n"
        f"open('{prefix}.pid', 'w').write(str(p.pid))\n"
        "print('CD_LAUNCHED', p.pid)\n"
    )
    code, out = _exec_code(session, launcher, 120)
    if code != 0 or "CD_LAUNCHED" not in out:
        raise RuntimeError(f"launch failed: {out[-400:]}")


def poll(session: str, prefix: str) -> tuple[str, str]:
    """(state, log): state is running, done, failed (the process ended without the marker) or lost (no answer)."""
    probe = (
        "import os\n"
        f"p = '{prefix}'\n"
        "try:\n"
        "    text = open(p + '.log', errors='replace').read()\n"
        "except Exception as exc:\n"
        "    text = '(no log: %s)' % exc\n"
        "alive = False\n"
        "try:\n"
        "    os.kill(int(open(p + '.pid').read()), 0); alive = True\n"
        "except Exception:\n"
        "    pass\n"
        "print('CD_PROBE', 'alive' if alive else 'dead')\n"
        "print(text[-20000:])\n"
    )
    code, out = _exec_code(session, probe, 90)
    if code != 0 or "CD_PROBE" not in out:
        return "lost", out[-300:]
    head, _, text = out.split("CD_PROBE", 1)[1].partition("\n")
    if DONE in text:
        return "done", text
    if "dead" in head:
        return "failed", text
    return "running", text


def run(session: str, notebook: Path, env: dict[str, str], prefix: str, *, poll_s: float = 30, max_wait: float = 3600,
        on_line: Callable[[str], None] = lambda line: None, alive: Callable[[], bool] = lambda: True) -> list[str]:
    """Launch and wait; returns the script's output lines. Raises RuntimeError on failure, timeout or a lost session."""
    launch(session, notebook, env, prefix)
    on_line(f"[detached] started {prefix}_job.py")
    t0 = time.monotonic()
    seen = 0
    lost = 0
    while time.monotonic() - t0 < max_wait:
        time.sleep(poll_s)
        state, text = poll(session, prefix)
        if state == "lost":
            lost += 1
            on_line(f"[detached] poll got no answer ({lost})")
            if lost >= 3 and not alive():
                raise RuntimeError("the Colab session is gone")
            continue
        lost = 0
        lines = text.splitlines()
        for line in lines[seen:]:
            on_line(line)
        seen = len(lines)
        if state == "done":
            return lines
        if state == "failed":
            raise RuntimeError("the detached run ended without finishing:\n" + "\n".join(lines[-15:]))
    raise RuntimeError(f"the detached run did not finish within {max_wait:.0f} s")
