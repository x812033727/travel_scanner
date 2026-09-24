import contextlib
import json
import os
import re
import select
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from ai_accounts_agent.config import AgentConfig
from ai_accounts_agent.runner import (
    CliError,
    cli_environment,
    parse_json_object,
    run_cli,
    text_or_none,
)
from ai_accounts_agent.security import sanitize
from ai_accounts_agent.sessions import (
    CANCELLED,
    FAILED,
    NOT_SIGNED_IN,
    PENDING,
    SUCCEEDED,
    VERIFYING,
    Finalizer,
    LoginError,
)
from ai_accounts_agent.statusline import (
    SNAPSHOT_NAME,
    atomic_write_text,
    read_snapshot,
    recorder_installed,
)

AUTHORIZE_HOSTS = ("claude.com", "claude.ai", "anthropic.com")
# Screens a probe may meet before the prompt, matched with whitespace removed: the TUI
# spaces words with cursor moves, so the screen reads "Yes,Itrustthisfolder". Each gets
# answered once. The trust prompt defaults to "No, exit", so it needs Down first; the
# theme picker and notice pages keep their defaults.
_FIRST_RUN_SCREENS: tuple[tuple[str, re.Pattern[str], tuple[bytes, ...]], ...] = (
    ("trust", re.compile(r"trustthisfolder", re.IGNORECASE), (b"\x1b[B", b"\r")),
    ("theme", re.compile(r"syntaxtheme|choosethetextstyle", re.IGNORECASE), (b"\r",)),
    ("notice", re.compile(r"entertocontinue", re.IGNORECASE), (b"\r",)),
)
# The TUI's own login picker: seen when a config directory has credentials but never
# finished onboarding. A probe gives up rather than start a sign-in.
_LOGIN_PROMPT = re.compile(r"selectloginmethod|claudeaccountwithsubscription", re.IGNORECASE)
SCREEN_SETTLE_SECONDS = 0.8
# Only sent when the status line has not reported usage on its own; a one-word answer from
# the smallest model is the cheapest request that yields an API response.
PROBE_MESSAGE = "Reply with the single word: ok"
# `claude auth login` prints the authorize URL as an OSC 8 hyperlink; its target survives
# any wrapping of the visible text, so read it from there first.
_OSC8_TARGET = re.compile(r"\x1b\]8;[^;\x07\x1b]*;(https://[^\x07\x1b]+)(?:\x07|\x1b\\)")
_TERMINAL_ESCAPES = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")
_PLAIN_URL = re.compile(r"https://[^\s\x1b\x07\"'<>]+")
# What the callback page hands the owner to paste: base64url pieces joined by `#`. No
# whitespace or control characters, so nothing typed into the terminal can be a keystroke.
CODE_PATTERN = re.compile(r"[A-Za-z0-9._~#-]{10,1024}")
MAX_OUTPUT_BYTES = 262_144
# Wide enough that the CLI never wraps the URL it prints.
TERMINAL_COLUMNS = 400
TERMINAL_ROWS = 50


def is_authorize_url(url: str) -> bool:
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    return (
        parts.scheme == "https"
        and any(host == allowed or host.endswith(f".{allowed}") for allowed in AUTHORIZE_HOSTS)
        and "oauth" in parts.path
    )


def extract_authorize_url(output: str) -> str | None:
    for match in _OSC8_TARGET.finditer(output):
        if is_authorize_url(match.group(1)):
            return match.group(1)
    for match in _PLAIN_URL.finditer(_TERMINAL_ESCAPES.sub("", output)):
        if is_authorize_url(match.group(0)):
            return match.group(0)
    return None


def _open_terminal() -> tuple[int, int]:
    if sys.platform == "win32":
        raise LoginError("the Claude login needs a POSIX terminal")
    import fcntl
    import struct
    import termios

    controller, terminal = os.openpty()
    fcntl.ioctl(
        terminal,
        termios.TIOCSWINSZ,
        struct.pack("HHHH", TERMINAL_ROWS, TERMINAL_COLUMNS, 0, 0),
    )
    return controller, terminal


def mark_onboarding_done(config_dir: Path) -> bool:
    """Record first-run setup as done for an account signed in with `claude auth login`.

    That command saves the login but leaves `hasCompletedOnboarding` unset, so the next
    interactive start shows the login picker as if nobody were signed in (seen on the
    host, 2026-09-24). Only these two keys change; returns True when the file did.
    """
    path = config_dir / ".claude.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        mode = path.stat().st_mode & 0o777
    except (OSError, ValueError):
        return False
    if not isinstance(data, dict) or data.get("hasCompletedOnboarding") is True:
        return False
    data["hasCompletedOnboarding"] = True
    version = data.get("firstStartVersion")
    if isinstance(version, str):
        data.setdefault("lastOnboardingVersion", version)
    atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n", mode)
    return True


def _stop_session(process: subprocess.Popen[bytes]) -> None:
    """End a CLI started in its own session, and everything it started."""
    if process.poll() is not None:
        return
    if sys.platform == "win32":
        process.kill()
        return
    for signum in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, signum)
        except ProcessLookupError:
            return
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.wait(3)
            return


class ClaudeLogin:
    """Drives `claude auth login` in a pseudo-terminal.

    The CLI prints the authorize URL and then waits at "Paste code here if prompted" for
    the code the callback page shows. The page hands the URL to the owner; the code comes
    back through `submit_code`, and a thread waits for the CLI to exchange it.
    """

    kind = "paste_code"

    def __init__(
        self,
        command: Sequence[str],
        environment: Mapping[str, str],
        *,
        url_timeout: float,
        exchange_timeout: float,
        finalize: Finalizer,
    ) -> None:
        self.user_code: str | None = None
        self._exchange_timeout = exchange_timeout
        self._finalize = finalize
        self._lock = threading.Lock()
        self._output = bytearray()
        self._url_found = threading.Event()
        self._closed = False
        self._status = PENDING
        self._error: str | None = None
        self._submitted: str | None = None
        self._url: str | None = None
        controller, terminal = _open_terminal()
        try:
            self._process = subprocess.Popen(  # noqa: S603 - fixed argv, shell=False
                [*command, "auth", "login", "--claudeai"],
                stdin=terminal,
                stdout=terminal,
                stderr=terminal,
                env=dict(environment),
                start_new_session=True,
                close_fds=True,
            )
        except OSError as exc:
            os.close(controller)
            raise LoginError(f"cannot start claude: {exc.strerror}") from exc
        finally:
            os.close(terminal)
        self._controller = controller
        threading.Thread(target=self._read, daemon=True).start()
        if not self._url_found.wait(url_timeout) or self._url is None:
            self.cancel()
            raise LoginError("claude did not print a sign-in URL")
        self.url: str = self._url

    def _read(self) -> None:
        # Reading continuously keeps the CLI from blocking on a full terminal buffer. Only
        # this thread closes the descriptor, once the CLI side is gone: closing it from
        # another thread could let the number be reused under a read still in progress.
        try:
            while True:
                try:
                    chunk = os.read(self._controller, 4096)
                except OSError:
                    break
                if not chunk:
                    break
                with self._lock:
                    self._output.extend(chunk)
                    del self._output[:-MAX_OUTPUT_BYTES]
                    if self._url is None:
                        text = self._output.decode("utf-8", errors="replace")
                        self._url = extract_authorize_url(text)
                        if self._url is not None:
                            self._url_found.set()
        finally:
            with self._lock:
                self._closed = True
                os.close(self._controller)
            self._url_found.set()

    def state(self) -> tuple[str, str | None]:
        with self._lock:
            return self._status, self._error

    def submit_code(self, code: str) -> None:
        if not CODE_PATTERN.fullmatch(code):
            raise LoginError("the code does not look like a Claude sign-in code")
        with self._lock:
            if self._status != PENDING:
                raise LoginError("this login is no longer waiting for a code")
            # Written under the lock, which the reader holds while it closes the descriptor.
            if self._closed or self._process.poll() is not None:
                self._status, self._error = FAILED, "claude exited before the code arrived"
                raise LoginError(self._error)
            try:
                os.write(self._controller, code.encode("ascii") + b"\r")
            except OSError as exc:
                self._status, self._error = FAILED, "claude stopped listening for the code"
                raise LoginError(self._error) from exc
            self._status = VERIFYING
            self._submitted = code
        threading.Thread(target=self._finish, daemon=True).start()

    def _finish(self) -> None:
        try:
            self._process.wait(self._exchange_timeout)
        except subprocess.TimeoutExpired:
            self._stop()
        # The CLI can leave a prompt open after saving the login, so the saved login decides.
        rejection = self._finalize()
        with self._lock:
            if self._status == VERIFYING:
                if rejection is None:
                    self._status, self._error = SUCCEEDED, None
                elif rejection == NOT_SIGNED_IN:
                    self._status, self._error = FAILED, self._failure_detail()
                else:
                    self._status, self._error = FAILED, rejection
        self._stop()

    def _failure_detail(self) -> str:
        text = _TERMINAL_ESCAPES.sub("", self._output.decode("utf-8", errors="replace"))
        if self._submitted:
            # The terminal echoes what was typed; the code must not travel back.
            text = text.replace(self._submitted, "***")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        detail = sanitize(lines[-1], 200) if lines else ""
        return detail or "claude did not accept the code"

    def cancel(self) -> None:
        with self._lock:
            if self._status in (PENDING, VERIFYING):
                self._status, self._error = CANCELLED, None
        self._stop()

    def _stop(self) -> None:
        """End the CLI; its side of the terminal closing lets the reader finish."""
        _stop_session(self._process)


class ClaudeAccounts:
    def __init__(self, config: AgentConfig) -> None:
        self.config = config

    def environment(self, slot: str) -> dict[str, str]:
        return cli_environment(
            self.config, {"CLAUDE_CONFIG_DIR": str(self.config.slot_path("claude", slot))}
        )

    def status(self, slot: str) -> dict[str, Any]:
        result = run_cli(
            [*self.config.claude_command, "auth", "status", "--json"],
            self.environment(slot),
            self.config.command_timeout_seconds,
        )
        payload = parse_json_object(result.stdout)
        if payload is None:
            raise CliError(sanitize(result.stderr or result.stdout) or "claude auth status failed")
        logged_in = payload.get("loggedIn") is True
        return {
            "logged_in": logged_in,
            "auth_method": text_or_none(payload.get("authMethod")) if logged_in else None,
            "email": text_or_none(payload.get("email")) if logged_in else None,
            "organization": text_or_none(payload.get("orgName")) if logged_in else None,
            "plan": text_or_none(payload.get("subscriptionType")) if logged_in else None,
        }

    def has_credentials(self, slot: str) -> bool:
        return (self.config.slot_path("claude", slot) / ".credentials.json").exists()

    def details(self, slot: str) -> dict[str, Any]:
        """The usage snapshot the status line recorder left, read fresh on every call."""
        path = self.config.slot_path("claude", slot)
        snapshot = read_snapshot(path)
        return {
            "usage": {"source": "snapshot", **snapshot} if snapshot is not None else None,
            "recorder_installed": recorder_installed(path, self.config.recorder_for(slot)),
        }

    def refresh_usage(self, slot: str) -> bool:
        """Open Claude Code once so its status line records this account's plan usage.

        Claude Code reports usage only to the status line of an interactive session. On
        the host it arrives within a couple of seconds of start, before any message, so
        this usually costs nothing; a one-word request is the fallback. `--restricted`
        leaves out the owner's settings (hooks, push notifications, Remote Control) and
        the tools that run code; the recorder comes in through `--settings`. Returns True
        when a new snapshot was written.
        """
        if sys.platform == "win32":
            return False
        config_dir = self.config.slot_path("claude", slot)
        snapshot = config_dir / SNAPSHOT_NAME

        def stamp() -> int | None:
            try:
                return snapshot.stat().st_mtime_ns
            except OSError:
                return None

        before = stamp()
        mark_onboarding_done(config_dir)
        probe_dir = self.config.usage_probe_path
        probe_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        settings = json.dumps(
            {"statusLine": {"type": "command", "command": self.config.recorder_for(slot)}}
        )
        command = [
            *self.config.claude_command,
            "--restricted",
            "--strict-mcp-config",
            "--model",
            "haiku",
            "--settings",
            settings,
        ]
        environment = {**self.environment(slot), "TERM": "xterm-256color"}
        controller, terminal = _open_terminal()
        try:
            process = subprocess.Popen(  # noqa: S603 - fixed argv, shell=False
                command,
                stdin=terminal,
                stdout=terminal,
                stderr=terminal,
                cwd=probe_dir,
                env=environment,
                start_new_session=True,
                close_fds=True,
            )
        except OSError as exc:
            os.close(controller)
            raise CliError(f"cannot start claude: {exc.strerror}") from exc
        finally:
            os.close(terminal)
        output = bytearray()
        answered: set[str] = set()
        started = last_output = time.monotonic()
        message_at = started + self.config.claude_usage_quiet_seconds
        give_up_at = message_at + self.config.claude_usage_message_seconds
        messaged = False
        try:
            while True:
                if stamp() != before:
                    return True
                now = time.monotonic()
                if process.poll() is not None or now >= give_up_at:
                    return False
                if not messaged and now >= message_at:
                    messaged = True
                    os.write(controller, PROBE_MESSAGE.encode())
                    time.sleep(0.5)  # The TUI reads a burst ending in Enter as a paste.
                    os.write(controller, b"\r")
                    output.clear()
                ready, _, _ = select.select([controller], [], [], 0.25)
                if ready:
                    try:
                        chunk = os.read(controller, 65536)
                    except OSError:
                        return stamp() != before
                    output.extend(chunk)
                    del output[:-MAX_OUTPUT_BYTES]
                    last_output = time.monotonic()
                    continue
                # Read a screen only once it has settled; the TUI draws in bursts.
                if not output or time.monotonic() - last_output < SCREEN_SETTLE_SECONDS:
                    continue
                screen = "".join(
                    _TERMINAL_ESCAPES.sub("", output.decode("utf-8", errors="replace")).split()
                )
                output.clear()
                if _LOGIN_PROMPT.search(screen):
                    return False  # Not really signed in; a probe must never start a login.
                for name, pattern, keys in _FIRST_RUN_SCREENS:
                    if name not in answered and pattern.search(screen):
                        answered.add(name)
                        for key in keys:
                            os.write(controller, key)
                            time.sleep(0.3)
                        break
        finally:
            _stop_session(process)
            os.close(controller)

    def start_login(self, slot: str, finalize: Finalizer) -> ClaudeLogin:
        return ClaudeLogin(
            self.config.claude_command,
            self.environment(slot),
            url_timeout=self.config.url_timeout_seconds,
            exchange_timeout=self.config.code_exchange_timeout_seconds,
            finalize=finalize,
        )

    def logout(self, slot: str) -> None:
        result = run_cli(
            [*self.config.claude_command, "auth", "logout"],
            self.environment(slot),
            self.config.command_timeout_seconds,
        )
        if result.returncode != 0:
            raise CliError(sanitize(result.stderr or result.stdout) or "claude auth logout failed")
