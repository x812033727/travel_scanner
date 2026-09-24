"""Claude Code status line command that records the plan usage the admin page shows.

Claude Code has no documented way to read a subscription's usage outside a session, but
the JSON it pipes to a status line command carries ``rate_limits.five_hour`` and
``rate_limits.seven_day`` for Pro and Max accounts once a session has had its first API
response. This command writes the latest of those next to the account's config
(``$CLAUDE_CONFIG_DIR/mokaair-usage.json``), then prints the status line: the owner's own
command when one was configured before (kept in ``mokaair-statusline-chain.json``), or a
short default.

The status line command names its account (``statusline-record claude-b``) so the
snapshot lands in the right place however the session was started. The host runs this
file directly (``python3 -I statusline.py``), so it imports nothing from the package; the
agent imports the helpers.
"""

import json
import os
import subprocess
import sys
import tempfile
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, BinaryIO, TextIO

# Kept equal to ai_accounts_agent.config by a test; this file cannot import the package.
RECORDER_PATH = "/usr/local/lib/mokaair-ai-accounts/statusline-record"
STATE_ROOT = Path("/var/lib/mokaair-ai-accounts")
RECORDED_SLOTS = tuple(f"claude-{slot}" for slot in "abcde")
SNAPSHOT_NAME = "mokaair-usage.json"
CHAIN_NAME = "mokaair-statusline-chain.json"
MAX_INPUT_BYTES = 1_000_000
CHAIN_TIMEOUT_SECONDS = 5.0
# The status line redraws every few seconds while Claude works; rewrite an unchanged
# snapshot only this often, just to move its timestamp.
UNCHANGED_REWRITE_SECONDS = 60
# Status line window keys and the length each one stands for.
WINDOW_MINUTES = {"five_hour": 300, "seven_day": 10_080}


def atomic_write_text(path: Path, text: str, mode: int = 0o600) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value)


def windows_from_rate_limits(rate_limits: Any) -> list[dict[str, Any]]:
    if not isinstance(rate_limits, Mapping):
        return []
    windows: list[dict[str, Any]] = []
    for key, minutes in WINDOW_MINUTES.items():
        window = rate_limits.get(key)
        if not isinstance(window, Mapping):
            continue
        used = _number(window.get("used_percentage"))
        if used is None:
            continue
        resets_at = _number(window.get("resets_at"))
        windows.append(
            {
                "window_minutes": minutes,
                "used_percent": max(0.0, min(100.0, used)),
                "resets_at": int(resets_at) if resets_at is not None else None,
            }
        )
    return windows


def record_snapshot(config_dir: Path, payload: Any, now: float | None = None) -> bool:
    """Keep the newest usage windows; a payload without them leaves the last snapshot."""
    if not isinstance(payload, Mapping):
        return False
    windows = windows_from_rate_limits(payload.get("rate_limits"))
    if not windows:
        return False
    recorded_at = int(time.time() if now is None else now)
    previous = read_snapshot(config_dir)
    if (
        previous is not None
        and previous["windows"] == windows
        and recorded_at - previous["recorded_at"] < UNCHANGED_REWRITE_SECONDS
    ):
        return False
    snapshot = {"recorded_at": recorded_at, "windows": windows}
    atomic_write_text(config_dir / SNAPSHOT_NAME, json.dumps(snapshot, separators=(",", ":")))
    return True


def read_snapshot(config_dir: Path) -> dict[str, Any] | None:
    try:
        data = json.loads((config_dir / SNAPSHOT_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, Mapping):
        return None
    recorded_at = _number(data.get("recorded_at"))
    windows = data.get("windows")
    if recorded_at is None or not isinstance(windows, list):
        return None
    cleaned: list[dict[str, Any]] = []
    for window in windows:
        if not isinstance(window, Mapping):
            continue
        used = _number(window.get("used_percent"))
        minutes = _number(window.get("window_minutes"))
        resets_at = _number(window.get("resets_at"))
        if used is None:
            continue
        cleaned.append(
            {
                "window_minutes": int(minutes) if minutes is not None else None,
                "used_percent": max(0.0, min(100.0, used)),
                "resets_at": int(resets_at) if resets_at is not None else None,
            }
        )
    return {"recorded_at": int(recorded_at), "windows": cleaned}


def is_recorder(command: object) -> bool:
    return isinstance(command, str) and command.split(" ", 1)[0] == RECORDER_PATH


def _read_settings(config_dir: Path) -> dict[str, Any] | None:
    path = config_dir / "settings.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def recorder_installed(config_dir: Path, command: str) -> bool:
    settings = _read_settings(config_dir)
    if not settings:
        return False
    current = settings.get("statusLine")
    return isinstance(current, Mapping) and current.get("command") == command


def ensure_statusline(config_dir: Path, command: str) -> bool:
    """Point the account's status line at the recorder, keeping any earlier command.

    Returns True when settings.json changed. A recorder for another account (settings
    copied from slot A) is replaced, never chained, or the status line would call itself.
    A settings file that is not a JSON object is left alone: rewriting it would throw away
    whatever the owner put there.
    """
    settings = _read_settings(config_dir)
    if settings is None:
        return False
    current = settings.get("statusLine")
    if isinstance(current, Mapping) and current.get("command") == command:
        return False
    replacement: dict[str, Any] = {"type": "command", "command": command}
    if isinstance(current, Mapping):
        previous = current.get("command")
        if isinstance(previous, str) and previous.strip() and not is_recorder(previous):
            atomic_write_text(
                config_dir / CHAIN_NAME, json.dumps({"command": previous}, ensure_ascii=False)
            )
        padding = current.get("padding")
        if isinstance(padding, int) and not isinstance(padding, bool):
            replacement["padding"] = padding
    settings["statusLine"] = replacement
    path = config_dir / "settings.json"
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    atomic_write_text(path, json.dumps(settings, indent=2, ensure_ascii=False) + "\n", mode)
    return True


def _chained_command(config_dir: Path) -> str | None:
    try:
        data = json.loads((config_dir / CHAIN_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    command = data.get("command") if isinstance(data, Mapping) else None
    if not isinstance(command, str) or not command.strip() or is_recorder(command):
        return None
    return command


def default_line(payload: Any) -> str:
    parts: list[str] = []
    if isinstance(payload, Mapping):
        model = payload.get("model")
        if isinstance(model, Mapping) and isinstance(model.get("display_name"), str):
            parts.append(model["display_name"])
        for window in windows_from_rate_limits(payload.get("rate_limits")):
            label = "5h" if window["window_minutes"] == 300 else "7d"
            parts.append(f"{label} {round(window['used_percent'])}%")
    return " | ".join(parts)


def config_dir_for(
    argv: Sequence[str], environ: Mapping[str, str], state_root: Path = STATE_ROOT
) -> Path | None:
    if len(argv) > 1:
        return state_root / argv[1] if argv[1] in RECORDED_SLOTS else None
    value = environ.get("CLAUDE_CONFIG_DIR")
    return Path(value) if value else None


def main(
    argv: Sequence[str],
    stdin: BinaryIO,
    stdout: TextIO,
    environ: Mapping[str, str],
    state_root: Path = STATE_ROOT,
) -> int:
    raw = stdin.read(MAX_INPUT_BYTES)
    try:
        payload: Any = json.loads(raw)
    except ValueError:
        payload = None
    config_dir = config_dir_for(argv, environ, state_root)
    if config_dir is not None:
        try:
            record_snapshot(config_dir, payload)
        except OSError:
            pass  # A status line must never fail because the snapshot could not be written.
        chained = _chained_command(config_dir)
        if chained is not None:
            try:
                result = subprocess.run(  # noqa: S602 - the owner's own statusLine command
                    chained,
                    shell=True,
                    input=raw,
                    capture_output=True,
                    timeout=CHAIN_TIMEOUT_SECONDS,
                    check=False,
                )
            except (OSError, subprocess.SubprocessError):
                return 0
            stdout.write(result.stdout.decode("utf-8", errors="replace"))
            return 0
    stdout.write(default_line(payload) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv, sys.stdin.buffer, sys.stdout, os.environ))
