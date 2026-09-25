"""Google's Antigravity CLI (`agy`) signed in to Google AI Pro/Ultra accounts.

What the host showed on 2026-09-25 (agy 1.2.11), and what this module relies on:

- A home without a login opens on "Select login method" with Google OAuth first. Enter picks
  it; the CLI then prints the authorize URL as an OSC 8 link and waits at "paste the
  authorization code below". Google's callback page (antigravity.google/oauth-callback)
  shows the code, which carries a `/` (`4/0A…`).
- The login is kept in the Secret Service keyring when one answers, otherwise in
  ``~/.gemini/antigravity-cli/jetski-standalone-oauth-token``. The keyring is shared by
  every account of a user, so the agent and the shell commands point the session bus at
  nothing: each account then always keeps its own file.
- The CLI has no switch for its data folder; ``~/.gemini/antigravity-cli`` follows HOME.
  Each account slot is therefore a HOME of its own.
- There is no status command. The language server logs "OAuth: authenticated successfully
  as <email>" to ``cli.log`` after a login, and the TUI header shows the email and plan.
- Quota lives on the TUI's "Models & Quota" page (`/usage`): groups of buckets, each with a
  remaining share and a refresh time. `agy -p /usage` was reported to send the text to the
  model as a prompt, so the probe opens the TUI instead.

The agent only drives the official binary; it never reads the token or calls Google with
it. Antigravity's terms forbid using the service with other products, and Google has
suspended paid accounts for exactly that.
"""

import contextlib
import json
import os
import re
import select
import subprocess
import sys
import threading
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from ai_accounts_agent.claude import (
    _OSC8_TARGET,
    _PLAIN_URL,
    _TERMINAL_ESCAPES,
    _open_terminal,
    _stop_session,
)
from ai_accounts_agent.config import AgentConfig
from ai_accounts_agent.runner import CliError, cli_environment
from ai_accounts_agent.screen import Screen
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
from ai_accounts_agent.statusline import SNAPSHOT_NAME, atomic_write_text

DATA_DIR = Path(".gemini") / "antigravity-cli"
TOKEN_NAME = "jetski-standalone-oauth-token"  # noqa: S105 - a file name
# The CLI keeps other per-account state next to the token with the same prefix (its user
# tier, when the keyring is away); signing out removes all of it.
TOKEN_PREFIX = "jetski-standalone-"  # noqa: S105 - a file name prefix
ACCOUNT_NAME = "mokaair-account.json"
# A session bus address that fails at once: the keyring lookup errors and the CLI falls
# back to the token file in this account's home. Also used by ops/ai-accounts.
NO_KEYRING_BUS = "unix:path=/dev/null/mokaair-no-keyring"
SUBSCRIPTION_METHOD = "google"
AUTHORIZE_HOST = "accounts.google.com"
# Google authorization codes: base64url pieces and a `/`. No whitespace or control
# characters, so nothing typed into the terminal can be a keystroke of its own.
CODE_PATTERN = re.compile(r"[A-Za-z0-9._~/+-]{10,1024}")
MAX_OUTPUT_BYTES = 262_144
TERMINAL_COLUMNS = 200
TERMINAL_ROWS = 60
SCREEN_SETTLE_SECONDS = 0.8
# The TUI reads a burst of keys that ends in Enter as a paste and keeps the Enter.
TYPE_PAUSE_SECONDS = 0.5
# How long after a finished login the email may take to reach the log.
EMAIL_WAIT_SECONDS = 5.0
LOG_TAIL_BYTES = 2_000_000
LOG_FILES_READ = 20

_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
_LOGGED_EMAIL = re.compile(r"authenticated successfully as (\S+@\S+)")
_PLAN = re.compile(r"\b(?:Google\s+AI\s+)?(Ultra|Pro|Free|Standard|Business|Enterprise)\b")
# Screens matched with whitespace removed and lower-cased (the TUI spaces words with
# cursor moves).
_LOGIN_PICKER = "selectloginmethod"
_CODE_PROMPT = "authorizationcode"
# First-run pages the probe will not answer for the owner (strings in agy 1.2.11: "Choose
# your color scheme:", "Terms and Privacy:", "Yes, I agree to help improve …"): accepting
# terms is theirs to do, once, over SSH.
_SETUP_SCREENS = (
    "termsofservice",
    "termsandprivacy",
    "acceptterms",
    "colorscheme",
    "helpimprove",
    "getstarted",
)
# "Do you trust the contents of this project?" is asked per folder. The probe's folder is
# its own and empty, so the probe answers it; the owner never sees that folder.
_TRUST_PROMPT = "doyoutrustthecontentsofthisproject"
_TRUST_CHOICE = re.compile(r"yes,?\s*i\s*trust\s*this\s*folder", re.IGNORECASE)
_SELECTED = re.compile(r"^\s*[>❯›▶●]")
TRUST_MOVES = 3
_EXCHANGE_FAILED = re.compile(r"failed to exchange|invalid_grant|invalid code|error", re.I)

_PERCENT = re.compile(r"(\d{1,3}(?:\.\d+)?)\s*%")
_REFRESH = re.compile(r"(?:refreshes|resets?|renews?)\s+in\s+((?:\d+\s*[a-z]+\s*)+)", re.IGNORECASE)
_DURATION_PART = re.compile(r"(\d+)\s*([dhms])[a-z]*", re.IGNORECASE)
_DURATION_SECONDS = {"d": 86_400, "h": 3_600, "m": 60, "s": 1}
# Progress bars, box drawing and the like, which carry no words.
_GLYPHS = re.compile(r"[─-◿⠀-⣿|·•:\[\]()]+")


def is_authorize_url(url: str) -> bool:
    parts = urlsplit(url)
    return (
        parts.scheme == "https"
        and (parts.hostname or "").lower() == AUTHORIZE_HOST
        and parts.path.startswith("/o/oauth2/")
    )


def extract_authorize_url(output: str) -> str | None:
    for match in _OSC8_TARGET.finditer(output):
        if is_authorize_url(match.group(1)):
            return match.group(1)
    for match in _PLAIN_URL.finditer(_TERMINAL_ESCAPES.sub("", output)):
        if is_authorize_url(match.group(0)):
            return match.group(0)
    return None


def _flat(text: str) -> str:
    return "".join(text.split()).lower()


def mask_emails(text: str) -> str:
    return _EMAIL.sub(lambda match: "***@" + match.group(0).split("@", 1)[1], text)


def _duration_seconds(text: str) -> int | None:
    parts = _DURATION_PART.findall(text)
    if not parts:
        return None
    return sum(int(amount) * _DURATION_SECONDS[unit.lower()] for amount, unit in parts)


def _window_minutes(text: str) -> int | None:
    lowered = text.lower()
    if re.search(r"\b(?:5|five)\s*-?\s*h(?:ou)?r?s?\b", lowered):
        return 300
    if re.search(r"week|\b7\s*-?\s*d(?:ay)?s?\b", lowered):
        return 10_080
    if re.search(r"\bdaily\b|\bday\b|\b24\s*-?\s*h", lowered):
        return 1_440
    if re.search(r"\bmonth", lowered):
        return 43_200
    return None


def _words(text: str) -> str:
    return " ".join(_GLYPHS.sub(" ", text).split())


def parse_quota(lines: Sequence[str], now: float) -> list[dict[str, Any]]:
    """Read the quota windows off the rendered "Models & Quota" page.

    Every row with a percentage is a window. Its label is the row's own words when it
    names something beyond the window length, otherwise the nearest heading above it (a
    model group). A row that says "used" is taken as used; anything else as the remaining
    share, which is what the CLI's quota service reports (``remaining_fraction``).
    """
    windows: list[dict[str, Any]] = []
    heading: str | None = None
    for line in lines:
        percent = _PERCENT.search(line)
        disabled = re.search(r"\bdisabled\b", line, re.IGNORECASE) is not None
        if percent is None:
            words = _words(line)
            # A row without a figure ("Weekly limit  Disabled") is not a group heading.
            if (
                words
                and len(words) <= 60
                and not disabled
                and not _REFRESH.search(line)
                and _window_minutes(words) is None
            ):
                heading = words
            continue
        if disabled:
            continue
        value = max(0.0, min(100.0, float(percent.group(1))))
        lowered = line.lower()
        used = value if re.search(r"\bused\b", lowered) else 100.0 - value
        refresh = _REFRESH.search(line)
        seconds = _duration_seconds(refresh.group(1)) if refresh else None
        before = line[: percent.start()]
        if refresh is not None and refresh.start() < percent.start():
            before = line[: refresh.start()]
        own = _words(re.sub(r"(?i)\b(?:used|remaining|left|available|quota|usage)\b", " ", before))
        minutes = _window_minutes(line) or (_window_minutes(heading) if heading else None)
        # The row names a model group unless all it says is how long its window is.
        label = own if own and _window_minutes(own) is None else heading
        key = (label, minutes)
        if any((window["label"], window["window_minutes"]) == key for window in windows):
            continue
        windows.append(
            {
                "label": label[:80] if label else None,
                "window_minutes": minutes,
                "used_percent": round(used, 1),
                "resets_at": int(now + seconds) if seconds is not None else None,
            }
        )
    return windows


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _clean_windows(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    cleaned: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, Mapping):
            continue
        used = item.get("used_percent")
        if isinstance(used, bool) or not isinstance(used, int | float):
            continue
        minutes, resets, label = (
            item.get("window_minutes"),
            item.get("resets_at"),
            item.get("label"),
        )
        cleaned.append(
            {
                "label": label if isinstance(label, str) and label else None,
                "window_minutes": minutes if isinstance(minutes, int) else None,
                "used_percent": max(0.0, min(100.0, float(used))),
                "resets_at": resets if isinstance(resets, int) else None,
            }
        )
    return cleaned


def email_from_logs(data_dir: Path) -> str | None:
    """The account the CLI last reported signing in, newest log first."""
    candidates = [data_dir / "cli.log"]
    with contextlib.suppress(OSError):
        candidates.extend((data_dir / "log").glob("*.log"))
    existing: list[tuple[float, Path]] = []
    for path in candidates:
        with contextlib.suppress(OSError):
            existing.append((path.stat().st_mtime, path))
    for _, path in sorted(existing, reverse=True)[:LOG_FILES_READ]:
        try:
            with path.open("rb") as handle:
                handle.seek(max(0, path.stat().st_size - LOG_TAIL_BYTES))
                text = handle.read().decode("utf-8", errors="replace")
        except OSError:
            continue
        matches = _LOGGED_EMAIL.findall(text)
        if matches:
            email = matches[-1].strip().rstrip(".,;")
            return email if _EMAIL.fullmatch(email) else None
    return None


def _header_account(lines: Sequence[str]) -> tuple[str | None, str | None]:
    """The email and plan tier the TUI header shows, when it shows them."""
    for line in lines[:15]:
        match = _EMAIL.search(line)
        if match is None:
            continue
        plan = _PLAN.search(line[match.end() :]) or _PLAN.search(line[: match.start()])
        return match.group(0), plan.group(1) if plan else None
    return None, None


class AntigravityLogin:
    """Drives `agy`'s own sign-in in a pseudo-terminal.

    The TUI stays open after the login is saved, so the saved token decides the outcome:
    once it appears the CLI is stopped and the finalizer checks the account.
    """

    kind = "paste_code"

    def __init__(
        self,
        command: Sequence[str],
        environment: Mapping[str, str],
        home: Path,
        *,
        url_timeout: float,
        exchange_timeout: float,
        finalize: Finalizer,
    ) -> None:
        self.user_code: str | None = None
        self._home = home
        self._token = home / DATA_DIR / TOKEN_NAME
        self._exchange_timeout = exchange_timeout
        self._finalize = finalize
        self._lock = threading.Lock()
        self._output = bytearray()
        self._screen = Screen(TERMINAL_COLUMNS, TERMINAL_ROWS)
        self._url_found = threading.Event()
        self._picked = False
        self._closed = False
        self._status = PENDING
        self._error: str | None = None
        self._submitted: str | None = None
        self._url: str | None = None
        controller, terminal = _open_terminal()
        try:
            self._process = subprocess.Popen(  # noqa: S603 - fixed argv, shell=False
                list(command),
                stdin=terminal,
                stdout=terminal,
                stderr=terminal,
                cwd=home,
                env=dict(environment),
                start_new_session=True,
                close_fds=True,
            )
        except OSError as exc:
            os.close(controller)
            raise LoginError(f"cannot start agy: {exc.strerror}") from exc
        finally:
            os.close(terminal)
        self._controller = controller
        threading.Thread(target=self._read, daemon=True).start()
        if not self._url_found.wait(url_timeout) or self._url is None:
            self.cancel()
            raise LoginError("agy did not print a sign-in URL")
        self.url: str = self._url

    def _read(self) -> None:
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
                    self._screen.feed(chunk.decode("utf-8", errors="replace"))
                    if self._url is not None:
                        continue
                    text = self._output.decode("utf-8", errors="replace")
                    self._url = extract_authorize_url(text)
                    if self._url is not None:
                        self._url_found.set()
                    elif not self._picked and _LOGIN_PICKER in _flat(self._screen.text()):
                        # Google OAuth is the first choice and already highlighted.
                        self._picked = True
                        with contextlib.suppress(OSError):
                            os.write(self._controller, b"\r")
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
            raise LoginError("the code does not look like a Google authorization code")
        with self._lock:
            if self._status != PENDING:
                raise LoginError("this login is no longer waiting for a code")
            if self._closed or self._process.poll() is not None:
                self._status, self._error = FAILED, "agy exited before the code arrived"
                raise LoginError(self._error)
            try:
                os.write(self._controller, code.encode("ascii"))
            except OSError as exc:
                self._status, self._error = FAILED, "agy stopped listening for the code"
                raise LoginError(self._error) from exc
            self._status = VERIFYING
            self._submitted = code
            self._output.clear()
        threading.Thread(target=self._finish, daemon=True).start()

    def _press_enter(self) -> bool:
        with self._lock:
            if self._closed:
                return False
            try:
                os.write(self._controller, b"\r")
            except OSError:
                return False
            return True

    def _finish(self) -> None:
        time.sleep(TYPE_PAUSE_SECONDS)
        self._press_enter()
        deadline = time.monotonic() + self._exchange_timeout
        while time.monotonic() < deadline and not self._token.exists():
            if self._process.poll() is not None or self.state()[0] != VERIFYING:
                break
            time.sleep(0.25)
        if self._token.exists():
            email_deadline = time.monotonic() + EMAIL_WAIT_SECONDS
            data_dir = self._home / DATA_DIR
            while time.monotonic() < email_deadline and email_from_logs(data_dir) is None:
                time.sleep(0.25)
        # The account must not be checked, or probed, while this CLI still holds its home.
        self._stop()
        rejection = self._finalize()
        with self._lock:
            if self._status == VERIFYING:
                if rejection is None:
                    self._status, self._error = SUCCEEDED, None
                elif rejection == NOT_SIGNED_IN:
                    self._status, self._error = FAILED, self._failure_detail()
                else:
                    self._status, self._error = FAILED, rejection

    def _failure_detail(self) -> str:
        lines = self._screen.lines()
        if self._submitted:
            # The terminal echoes what was typed; the code must not travel back.
            lines = [line.replace(self._submitted, "***") for line in lines]
        for line in reversed(lines):
            if _EXCHANGE_FAILED.search(line):
                return sanitize(line, 200)
        return "agy did not accept the code"

    def cancel(self) -> None:
        with self._lock:
            if self._status in (PENDING, VERIFYING):
                self._status, self._error = CANCELLED, None
        self._stop()

    def _stop(self) -> None:
        _stop_session(self._process)


class AntigravityAccounts:
    def __init__(self, config: AgentConfig) -> None:
        self.config = config

    def home(self, slot: str) -> Path:
        return self.config.slot_path("agy", slot)

    def environment(self, slot: str) -> dict[str, str]:
        return cli_environment(
            self.config,
            {
                "HOME": str(self.home(slot)),
                "AGY_CLI_DISABLE_AUTO_UPDATE": "true",
                "DBUS_SESSION_BUS_ADDRESS": NO_KEYRING_BUS,
                "TERM": "xterm-256color",
            },
        )

    def has_credentials(self, slot: str) -> bool:
        return (self.home(slot) / DATA_DIR / TOKEN_NAME).exists()

    def _account(self, slot: str) -> dict[str, Any]:
        return read_json(self.home(slot) / ACCOUNT_NAME) or {}

    def _remember(self, slot: str, **values: Any) -> None:
        account = self._account(slot)
        changed = {
            key: value for key, value in values.items() if value and account.get(key) != value
        }
        if not changed:
            return
        account.update(changed, recorded_at=int(time.time()))
        with contextlib.suppress(OSError):
            atomic_write_text(self.home(slot) / ACCOUNT_NAME, json.dumps(account))

    def status(self, slot: str) -> dict[str, Any]:
        """Read from files only: the CLI has no status command, and starting its TUI to ask
        would cost a language server per page view."""
        if not self.has_credentials(slot):
            return {"logged_in": False, "auth_method": None, "email": None, "plan": None}
        account = self._account(slot)
        email = email_from_logs(self.home(slot) / DATA_DIR) or account.get("email")
        if isinstance(email, str) and email != account.get("email"):
            self._remember(slot, email=email)
        plan = account.get("plan")
        return {
            "logged_in": True,
            "auth_method": SUBSCRIPTION_METHOD,
            "email": email if isinstance(email, str) else None,
            "organization": None,
            "plan": plan if isinstance(plan, str) else None,
        }

    def details(self, slot: str) -> dict[str, Any]:
        snapshot = read_json(self.home(slot) / SNAPSHOT_NAME)
        if snapshot is None:
            return {"usage": None}
        recorded_at = snapshot.get("recorded_at")
        windows = _clean_windows(snapshot.get("windows"))
        error = snapshot.get("error")
        usage = (
            {"source": "snapshot", "recorded_at": recorded_at, "windows": windows}
            if isinstance(recorded_at, int) and windows
            else None
        )
        return {"usage": usage, "usage_error": error if isinstance(error, str) else None}

    def _record_usage(
        self, slot: str, windows: list[dict[str, Any]] | None, error: str | None
    ) -> None:
        path = self.home(slot) / SNAPSHOT_NAME
        previous = read_json(path) or {}
        snapshot = {
            "recorded_at": int(time.time()) if windows else previous.get("recorded_at"),
            "windows": windows if windows else previous.get("windows", []),
            "error": error,
        }
        with contextlib.suppress(OSError):
            atomic_write_text(path, json.dumps(snapshot, separators=(",", ":")))

    def refresh_usage(self, slot: str) -> bool:
        """Open the TUI once, show its quota page and record the windows on it.

        `/usage` is a local command: it asks Google for the quota and draws it, and no
        model is called. Returns True when new windows were recorded.
        """
        if sys.platform == "win32" or not self.has_credentials(slot):
            return False
        probe_dir = self.config.home_path / "agy-usage-probe"
        probe_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        controller, terminal = _open_terminal()
        try:
            process = subprocess.Popen(  # noqa: S603 - fixed argv, shell=False
                list(self.config.agy_command),
                stdin=terminal,
                stdout=terminal,
                stderr=terminal,
                cwd=probe_dir,
                env=self.environment(slot),
                start_new_session=True,
                close_fds=True,
            )
        except OSError as exc:
            os.close(controller)
            raise CliError(f"cannot start agy: {exc.strerror}") from exc
        finally:
            os.close(terminal)
        screen = Screen(TERMINAL_COLUMNS, TERMINAL_ROWS)
        started = last_output = time.monotonic()
        give_up_at = started + self.config.agy_usage_timeout_seconds
        asked_at: float | None = None
        read_at: float | None = None  # The output a settled screen was last read for.
        trusted = False
        trust_moves = 0
        try:
            while True:
                now = time.monotonic()
                if process.poll() is not None or now >= give_up_at:
                    break
                ready, _, _ = select.select([controller], [], [], 0.25)
                if ready:
                    try:
                        chunk = os.read(controller, 65536)
                    except OSError:
                        break
                    screen.feed(chunk.decode("utf-8", errors="replace"))
                    last_output = time.monotonic()
                    continue
                now = time.monotonic()
                if read_at == last_output or now - last_output < SCREEN_SETTLE_SECONDS:
                    continue
                # The page reloads the quota when it opens; until then the screen may still
                # show the status bar's own figures, so the page gets a moment first.
                if asked_at is not None and now - asked_at < self.config.agy_usage_page_seconds:
                    continue
                if asked_at is None and now - started < self.config.agy_usage_start_seconds:
                    continue
                read_at = last_output
                lines = screen.lines()
                flat = _flat("\n".join(lines))
                if _LOGIN_PICKER in flat or _CODE_PROMPT in flat:
                    self._record_usage(slot, None, "signed_out")
                    return False  # A probe must never start a sign-in.
                if any(marker in flat for marker in _SETUP_SCREENS):
                    self._record_usage(slot, None, "setup_needed")
                    return False
                if not trusted and _TRUST_PROMPT in flat:
                    choice = next((line for line in lines if _TRUST_CHOICE.search(line)), None)
                    if choice is not None and _SELECTED.match(choice):
                        trusted = True
                        os.write(controller, b"\r")
                    elif trust_moves < TRUST_MOVES:
                        trust_moves += 1
                        os.write(controller, b"\x1b[B")
                    else:
                        self._record_usage(slot, None, "setup_needed")
                        return False
                    continue
                email, plan = _header_account(lines)
                if email or plan:
                    self._remember(slot, email=email, plan=plan)
                if asked_at is None:
                    os.write(controller, b"/usage")
                    time.sleep(TYPE_PAUSE_SECONDS)
                    os.write(controller, b"\r")
                    asked_at = time.monotonic()
                    continue
                windows = parse_quota(lines, time.time())
                if windows:
                    self._record_usage(slot, windows, None)
                    return True
            self._record_usage(slot, None, "unreadable")
            if asked_at is not None:
                # The page's layout is only known from the binary's strings; show what it
                # drew so the parser can follow. No codes appear there; emails are masked.
                shown = "\n".join(sanitize(mask_emails(line), 200) for line in screen.lines())
                print(f"agy usage probe {slot}: no quota rows found on:\n{shown}", file=sys.stderr)
            return False
        finally:
            _stop_session(process)
            os.close(controller)

    def start_login(self, slot: str, finalize: Finalizer) -> AntigravityLogin:
        home = self.home(slot)
        home.mkdir(mode=0o700, parents=True, exist_ok=True)
        return AntigravityLogin(
            self.config.agy_command,
            self.environment(slot),
            home,
            url_timeout=self.config.agy_start_timeout_seconds,
            exchange_timeout=self.config.code_exchange_timeout_seconds,
            finalize=finalize,
        )

    def logout(self, slot: str) -> None:
        """Forget the account on this host. The CLI's own `/logout` needs its TUI; removing
        the saved login is what it does locally."""
        home = self.home(slot)
        try:
            for path in (home / DATA_DIR).glob(f"{TOKEN_PREFIX}*"):
                path.unlink(missing_ok=True)
            (home / ACCOUNT_NAME).unlink(missing_ok=True)
            (home / SNAPSHOT_NAME).unlink(missing_ok=True)
        except OSError as exc:
            raise CliError(f"cannot sign agy out: {exc.strerror}") from exc
