#!/usr/bin/env python3
"""Pair the Colab CLI with a Google account from a shell that has no browser.

`colab --auth=oauth2 usage` prints a Google sign-in URL and then blocks on stdin for the
authorization code the person copies from Google's landing page. In a Claude Code cloud
session the agent runs commands one at a time, so the process that printed the URL would be
gone before the person comes back with the code. This helper keeps that process alive in the
background and feeds it the code later:

    pair.py start            spawn the CLI, print the URL to open, keep waiting for the code
    pair.py code 4/0AX...    hand the code to the waiting CLI and report whether it paired
    pair.py status           what the pairing is doing right now
    pair.py export           the saved token as one base64 line, for an environment secret
    pair.py clear            forget a stuck or finished pairing (the token itself stays)

Only the Python standard library is used. The token the CLI writes stays where the CLI keeps
it (its own config directory); nothing here prints it except `export`, which the person asks
for on purpose. The state directory holds the URL, the code for a few seconds, and the log.
"""

from __future__ import annotations

import base64
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("COLAB_CLI_CONFIG_DIR") or Path.home() / ".config" / "colab-cli")
TOKEN_PATH = CONFIG_DIR / "token.json"
STATE_DIR = Path(os.environ.get("COLAB_PAIR_STATE") or CONFIG_DIR / "pair")
URL_FILE = STATE_DIR / "url.txt"
CODE_FILE = STATE_DIR / "code.txt"
RESULT_FILE = STATE_DIR / "result.json"
FEEDER_PID_FILE = STATE_DIR / "feeder.pid"
LOG_FILE = STATE_DIR / "colab.log"
AUTH_URL_MARK = "accounts.google.com/o/oauth2"
URL_WAIT_SECONDS = 90
CODE_WAIT_SECONDS = 30 * 60
RESULT_WAIT_SECONDS = 180


def colab_binary() -> str:
    path = os.environ.get("COLAB_BIN") or shutil.which("colab")
    if not path:
        sys.exit("colab is not on PATH. Run bootstrap.sh install first.")
    return path


def read_result() -> dict | None:
    if not RESULT_FILE.is_file():
        return None
    try:
        return json.loads(RESULT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def feeder_alive() -> bool:
    if not FEEDER_PID_FILE.is_file():
        return False
    try:
        pid = int(FEEDER_PID_FILE.read_text().strip())
        os.kill(pid, 0)
    except (ValueError, ProcessLookupError, PermissionError):
        return False
    return True


def write_result(payload: dict) -> None:
    tmp = RESULT_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, RESULT_FILE)


def feeder() -> int:
    """Own the CLI process: capture its URL, wait for the code file, feed it, record the exit."""
    FEEDER_PID_FILE.write_text(str(os.getpid()))
    child = subprocess.Popen(
        [colab_binary(), "--auth=oauth2", "usage"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )
    assert child.stdin is not None and child.stdout is not None
    # The CLI prints its prompt without a newline, so read in small pieces, not lines.
    pieces: queue.Queue[str | None] = queue.Queue()

    def collect() -> None:
        assert child.stdout is not None
        while True:
            piece = child.stdout.read(1)
            if not piece:
                break
            pieces.put(piece)
        pieces.put(None)

    threading.Thread(target=collect, daemon=True).start()
    lines: list[str] = []
    pending = ""
    url_seen = False
    code_sent = False
    eof = False
    started = time.monotonic()

    def take(line: str) -> None:
        nonlocal url_seen
        lines.append(line)
        print(line, flush=True)
        if not url_seen and AUTH_URL_MARK in line:
            URL_FILE.write_text(line.strip() + "\n", encoding="utf-8")
            url_seen = True

    while not (eof and child.poll() is not None):
        try:
            piece = pieces.get(timeout=0.2)
        except queue.Empty:
            piece = ""
        if piece is None:
            eof = True
        elif piece:
            pending += piece
            while "\n" in pending:
                line, pending = pending.split("\n", 1)
                take(line.rstrip())
        if url_seen and not code_sent and CODE_FILE.is_file():
            value = CODE_FILE.read_text(encoding="utf-8").strip()
            CODE_FILE.unlink(missing_ok=True)
            if value:
                try:
                    child.stdin.write(value + "\n")
                    child.stdin.flush()
                    child.stdin.close()
                except (BrokenPipeError, OSError):
                    pass
                code_sent = True
        if not code_sent and time.monotonic() - started > CODE_WAIT_SECONDS:
            child.terminate()
            take("pair.py: no authorization code arrived in time; the CLI was stopped.")
            break
    exit_code = child.wait()
    if pending.strip():
        take(pending.strip())
    paired = exit_code == 0 and code_sent and TOKEN_PATH.is_file()
    write_result({
        "exit": exit_code,
        "code_sent": code_sent,
        "paired": paired,
        "token_path": str(TOKEN_PATH),
        "tail": [line for line in lines[-12:] if line],
    })
    FEEDER_PID_FILE.unlink(missing_ok=True)
    return 0


def start() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.chmod(0o700)
    if feeder_alive():
        if URL_FILE.is_file():
            print("A pairing is already waiting for its code. Open this URL, then run: pair.py code <CODE>")
            print(URL_FILE.read_text(encoding="utf-8").strip())
            return 0
        print("A pairing is already starting; try `pair.py status` in a few seconds.")
        return 0
    for stale in (URL_FILE, CODE_FILE, RESULT_FILE, LOG_FILE):
        stale.unlink(missing_ok=True)
    colab_binary()
    log = LOG_FILE.open("a", encoding="utf-8")
    subprocess.Popen(
        [sys.executable, os.path.abspath(__file__), "_feeder"],
        stdin=subprocess.DEVNULL,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
        close_fds=True,
    )
    deadline = time.monotonic() + URL_WAIT_SECONDS
    while time.monotonic() < deadline:
        if URL_FILE.is_file():
            print("Open this URL in any browser, sign in with the Google account that owns the Colab plan,")
            print("approve, copy the authorization code Google shows, then run: pair.py code <CODE>")
            print()
            print(URL_FILE.read_text(encoding="utf-8").strip())
            print()
            print(f"The CLI waits up to {CODE_WAIT_SECONDS // 60} minutes for the code.")
            return 0
        result = read_result()
        if result is not None:
            if result.get("exit") == 0 and not result.get("code_sent"):
                print("The CLI did not ask for a code: it is already paired (a token exists and refreshed).")
                return 0
            print("The CLI ended before printing a sign-in URL:")
            print("\n".join(result.get("tail", [])))
            return 1
        time.sleep(0.3)
    print(f"No sign-in URL after {URL_WAIT_SECONDS} seconds; see {LOG_FILE}", file=sys.stderr)
    return 1


def code(value: str) -> int:
    if not URL_FILE.is_file() or not feeder_alive():
        print("No pairing is waiting for a code. Run `pair.py start` first.", file=sys.stderr)
        return 2
    value = value.strip()
    if not value:
        print("The authorization code is empty.", file=sys.stderr)
        return 2
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = CODE_FILE.with_suffix(".tmp")
    tmp.write_text(value + "\n", encoding="utf-8")
    tmp.chmod(0o600)
    os.replace(tmp, CODE_FILE)
    deadline = time.monotonic() + RESULT_WAIT_SECONDS
    while time.monotonic() < deadline:
        result = read_result()
        if result is not None:
            return report(result)
        time.sleep(0.3)
    print(f"Still waiting on Google after {RESULT_WAIT_SECONDS} seconds; run `pair.py status` later.", file=sys.stderr)
    return 1


def report(result: dict) -> int:
    if result.get("paired"):
        print(f"Paired. The Colab CLI saved its token at {result['token_path']}.")
        print("Usage, as the CLI printed it:")
        print("\n".join(line for line in result.get("tail", []) if "balance" in line.lower() or "rate" in line.lower() or "assignments" in line.lower()))
        print("To keep this pairing across cloud sessions, run `pair.py export` and store the line as the COLAB_CLI_TOKEN_JSON secret.")
        return 0
    print("Pairing did not complete:")
    print("\n".join(result.get("tail", [])))
    return 1


def status() -> int:
    result = read_result()
    if feeder_alive():
        if URL_FILE.is_file():
            print("waiting_for_code")
            print(URL_FILE.read_text(encoding="utf-8").strip())
        else:
            print("starting")
        return 0
    if result is not None:
        print("paired" if result.get("paired") else "failed")
        print("\n".join(result.get("tail", [])))
        return 0 if result.get("paired") else 1
    print("paired_token_present" if TOKEN_PATH.is_file() else "not_paired")
    return 0 if TOKEN_PATH.is_file() else 1


def export() -> int:
    if not TOKEN_PATH.is_file():
        print(f"No token at {TOKEN_PATH}; pair first.", file=sys.stderr)
        return 1
    raw = TOKEN_PATH.read_bytes()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("The token file is not JSON; pair again.", file=sys.stderr)
        return 1
    if not data.get("refresh_token"):
        print("The token has no refresh_token, so it would die within the hour; pair again.", file=sys.stderr)
        return 1
    print("# Store the next line as the environment secret COLAB_CLI_TOKEN_JSON (it is a Google refresh token: treat it like a password).", file=sys.stderr)
    print(base64.b64encode(json.dumps(data, separators=(",", ":")).encode("utf-8")).decode("ascii"))
    return 0


def clear() -> int:
    if feeder_alive():
        try:
            os.kill(int(FEEDER_PID_FILE.read_text().strip()), 15)
        except (ValueError, ProcessLookupError, PermissionError):
            pass
    for item in (URL_FILE, CODE_FILE, RESULT_FILE, FEEDER_PID_FILE, LOG_FILE):
        item.unlink(missing_ok=True)
    print("Pairing state cleared; the saved token, if any, was left alone.")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print(__doc__.strip())
        return 0 if len(argv) >= 2 else 2
    command = argv[1]
    if command == "_feeder":
        return feeder()
    if command == "start":
        return start()
    if command == "code":
        if len(argv) < 3:
            print("usage: pair.py code <CODE>", file=sys.stderr)
            return 2
        return code(argv[2])
    if command == "status":
        return status()
    if command == "export":
        return export()
    if command == "clear":
        return clear()
    print(__doc__.strip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
