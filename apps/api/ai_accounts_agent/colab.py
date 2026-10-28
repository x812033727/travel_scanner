"""Google's Colab CLI (`colab`, the google-colab-cli package) signed in to Google accounts.

What google-colab-cli 0.7.5 does, read in its `auth.py` on 2026-10-27, and what this module
relies on:

- `colab --auth=oauth2 <command>` without a saved login prints an `accounts.google.com`
  authorization URL and waits on stdin for the code Google's landing page shows
  (`sdk.cloud.google.com/applicationdefaultauthcode.html`, the same copy-and-paste flow as
  `gcloud auth application-default login`). No browser, no local HTTP server: pipes are enough.
- The login is saved as `~/.config/colab-cli/token.json` (google-auth's `Credentials.to_json()`:
  access token, refresh token, client id and secret, scopes). The CLI refreshes the access token
  itself and rewrites the file; the refresh token stays. The path follows HOME and has no switch,
  so each account slot is a HOME of its own, like Antigravity's.
- `colab usage` prints the account's compute units: "Current balance: N compute units",
  "Usage rate: N / hr" and "Active assignments: N". With a saved login that no longer works it
  prints the sign-in URL again instead. There is no status or logout command, and nothing the
  CLI prints names the account, so the email comes from Google's userinfo endpoint with the
  access token (the login's `openid` and `userinfo.email` scopes), once, and is kept beside the
  slot.
- The token carries the `cloud-platform` scope. A paired cloud session is handed this file
  (`credentials`), so the owner pairs accounts that hold nothing but a Colab plan.
"""

import contextlib
import json
import os
import re
import subprocess
import threading
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from ai_accounts_agent.antigravity import CODE_PATTERN, extract_authorize_url, mask_emails
from ai_accounts_agent.claude import _stop_session
from ai_accounts_agent.config import AgentConfig
from ai_accounts_agent.runner import CliError, cli_environment, run_cli
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
from ai_accounts_agent.statusline import atomic_write_text

TOOL = "colab"
TOKEN_DIR = Path(".config") / "colab-cli"
TOKEN_NAME = "token.json"  # noqa: S105 - a file name
# A login moved aside while the account signs in again: with a working token the CLI would
# refresh it and never print a sign-in URL.
SET_ASIDE_SUFFIX = ".mokaair-previous"
ACCOUNT_NAME = "mokaair-account.json"
SUBSCRIPTION_METHOD = "google"
USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
USERINFO_TIMEOUT_SECONDS = 10.0
AUTH_URL_MARK = "accounts.google.com/o/oauth2"
MAX_OUTPUT_BYTES = 262_144
NOT_SIGNED_IN_DETAIL = "the saved sign-in no longer works; sign in again"

_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
_BALANCE = re.compile(r"Current balance:\s*([\d,]+(?:\.\d+)?)\s*compute units", re.IGNORECASE)
_RATE = re.compile(r"Usage rate:\s*([\d,]+(?:\.\d+)?)\s*/\s*hr", re.IGNORECASE)
_ASSIGNMENTS = re.compile(r"Active assignments:\s*(\d+)", re.IGNORECASE)
_EXCHANGE_FAILED = re.compile(r"invalid_grant|invalid|failed|error|denied", re.IGNORECASE)

Opener = Callable[..., Any]


def parse_usage(text: str) -> dict[str, Any] | None:
    """The compute-unit lines of `colab usage`, or None when the balance is not there."""
    balance = _BALANCE.search(text)
    if balance is None:
        return None
    rate = _RATE.search(text)
    assignments = _ASSIGNMENTS.search(text)
    return {
        "balance": float(balance.group(1).replace(",", "")),
        "rate_per_hour": float(rate.group(1).replace(",", "")) if rate else None,
        "active_assignments": int(assignments.group(1)) if assignments else None,
    }


def token_path(home: Path) -> Path:
    return home / TOKEN_DIR / TOKEN_NAME


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def saved_login(home: Path) -> bool:
    return token_path(home).is_file()


def set_aside_login(home: Path) -> None:
    path = token_path(home)
    if path.exists():
        os.replace(path, path.with_name(f"{TOKEN_NAME}{SET_ASIDE_SUFFIX}"))


def settle_set_aside_login(home: Path) -> None:
    """After a sign-in ends: a new login stands, or the one moved aside comes back."""
    aside = token_path(home).with_name(f"{TOKEN_NAME}{SET_ASIDE_SUFFIX}")
    with contextlib.suppress(OSError):
        if not aside.exists():
            return
        if saved_login(home):
            aside.unlink()
        else:
            os.replace(aside, token_path(home))


def fetch_email(
    access_token: str, *, timeout: float = USERINFO_TIMEOUT_SECONDS, opener: Opener | None = None
) -> str | None:
    """The signed-in account's email from Google's userinfo endpoint, or None."""
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    request = urllib.request.Request(USERINFO_URL, headers=headers)  # noqa: S310 - fixed https
    open_url = opener or urllib.request.urlopen
    try:
        with open_url(request, timeout=timeout) as response:  # noqa: S310 - see above
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except (OSError, ValueError, urllib.error.URLError):
        return None
    email = payload.get("email") if isinstance(payload, dict) else None
    return email if isinstance(email, str) and _EMAIL.fullmatch(email) else None


class ColabLogin:
    """Drives `colab --auth=oauth2 usage` over pipes until it has saved a login.

    The CLI prints the authorization URL, waits for the code on stdin, exchanges it, saves
    the token and prints the balance. The saved token decides the outcome; however it ends, a
    login moved aside for this sign-in is dropped or put back.
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
        self._exchange_timeout = exchange_timeout
        self._finalize = finalize
        self._lock = threading.Lock()
        self._output = bytearray()
        self._url_found = threading.Event()
        self._eof = threading.Event()
        self._closed = False
        self._status = PENDING
        self._error: str | None = None
        self._submitted: str | None = None
        self._url: str | None = None
        try:
            self._process = subprocess.Popen(  # noqa: S603 - fixed argv, shell=False
                [*command, "--auth=oauth2", "usage"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=home,
                env=dict(environment),
                start_new_session=True,
                close_fds=True,
            )
        except OSError as exc:
            raise LoginError(f"cannot start colab: {exc.strerror}") from exc
        threading.Thread(target=self._read, daemon=True).start()
        if not self._url_found.wait(url_timeout) or self._url is None:
            self.cancel()
            raise LoginError("colab did not print a sign-in URL")
        self.url: str = self._url

    def _read(self) -> None:
        stream = self._process.stdout
        assert stream is not None
        try:
            while True:
                chunk = stream.read1(4096) if hasattr(stream, "read1") else stream.read(1)
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
            self._url_found.set()
            self._eof.set()

    def state(self) -> tuple[str, str | None]:
        with self._lock:
            return self._status, self._error

    def submit_code(self, code: str) -> None:
        if not CODE_PATTERN.fullmatch(code):
            raise LoginError("the code does not look like a Google authorization code")
        with self._lock:
            if self._status != PENDING:
                raise LoginError("this login is no longer waiting for a code")
            stdin = self._process.stdin
            if self._closed or stdin is None or self._process.poll() is not None:
                self._status, self._error = FAILED, "colab exited before the code arrived"
                raise LoginError(self._error)
            try:
                stdin.write(code.encode("ascii") + b"\n")
                stdin.flush()
                stdin.close()
            except (OSError, ValueError) as exc:
                self._status, self._error = FAILED, "colab stopped listening for the code"
                raise LoginError(self._error) from exc
            self._status = VERIFYING
            self._submitted = code
        threading.Thread(target=self._finish, daemon=True).start()

    def _finish(self) -> None:
        try:
            self._process.wait(self._exchange_timeout)
        except subprocess.TimeoutExpired:
            self._stop()
        # The CLI's last words can still be in the pipe when it exits; the failure detail
        # below reads them, so give the reader a moment to drain it.
        self._eof.wait(2.0)
        rejection = self._finalize()
        settle_set_aside_login(self._home)
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
        text = self._output.decode("utf-8", errors="replace")
        if self._submitted:
            text = text.replace(self._submitted, "***")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in reversed(lines):
            # The CLI's last words follow its prompt on the same line: `input()` prints
            # "Enter the authorization code: " without a newline.
            _, _, tail = line.rpartition("authorization code:")
            candidate = (tail or line).strip()
            if not candidate or AUTH_URL_MARK in candidate:
                continue
            if _EXCHANGE_FAILED.search(candidate):
                return sanitize(mask_emails(candidate), 200)
        return "colab did not accept the code"

    def cancel(self) -> None:
        with self._lock:
            active = self._status in (PENDING, VERIFYING)
            if active:
                self._status, self._error = CANCELLED, None
        self._stop()
        if active:
            settle_set_aside_login(self._home)

    def _stop(self) -> None:
        with contextlib.suppress(OSError, ValueError):
            if self._process.stdin is not None:
                self._process.stdin.close()
        _stop_session(self._process)


class ColabAccounts:
    def __init__(self, config: AgentConfig, *, opener: Opener | None = None) -> None:
        self.config = config
        self._opener = opener
        self._account_lock = threading.Lock()

    def home(self, slot: str) -> Path:
        return self.config.slot_path(TOOL, slot)

    def environment(self, slot: str) -> dict[str, str]:
        return cli_environment(self.config, {"HOME": str(self.home(slot))})

    def has_credentials(self, slot: str) -> bool:
        return saved_login(self.home(slot))

    def _account(self, slot: str) -> dict[str, Any]:
        return read_json(self.home(slot) / ACCOUNT_NAME) or {}

    def _remember(self, slot: str, **values: Any) -> None:
        with self._account_lock:
            if not self.has_credentials(slot):
                return
            account = self._account(slot)
            changed = {
                key: value for key, value in values.items() if value and account.get(key) != value
            }
            if not changed:
                return
            account.update(changed, recorded_at=int(time.time()))
            with contextlib.suppress(OSError):
                atomic_write_text(self.home(slot) / ACCOUNT_NAME, json.dumps(account))

    def _email(self, slot: str) -> str | None:
        """The account's email: remembered, named in the token file, or asked of Google once."""
        remembered = self._account(slot).get("email")
        if isinstance(remembered, str) and _EMAIL.fullmatch(remembered):
            return remembered
        token = read_json(token_path(self.home(slot))) or {}
        named = token.get("account")
        email = named if isinstance(named, str) and _EMAIL.fullmatch(named) else None
        access = token.get("token")
        if email is None and isinstance(access, str) and access:
            email = fetch_email(access, opener=self._opener)
        if email:
            self._remember(slot, email=email)
        return email

    def status(self, slot: str) -> dict[str, Any]:
        """`colab usage`: the balance proves the login and is the usage in one call."""
        result = run_cli(
            [*self.config.colab_command, "--auth=oauth2", "usage"],
            self.environment(slot),
            self.config.colab_usage_timeout_seconds,
        )
        text = f"{result.stdout}\n{result.stderr}"
        signed_out: dict[str, Any] = {
            "logged_in": False,
            "auth_method": None,
            "email": None,
            "organization": None,
            "plan": None,
        }
        if AUTH_URL_MARK in text:
            # The refresh failed (revoked, or the account's password changed): the CLI asked
            # for a new sign-in and gave up at the closed stdin.
            return {**signed_out, "usage_error": NOT_SIGNED_IN_DETAIL}
        usage = parse_usage(text)
        if usage is None:
            detail = sanitize(mask_emails(result.stderr or result.stdout))
            raise CliError(detail or "colab usage failed")
        return {
            "logged_in": True,
            "auth_method": SUBSCRIPTION_METHOD,
            "email": self._email(slot),
            "organization": None,
            "plan": None,
            "usage": {"source": "live", "windows": [], "compute_units": usage},
        }

    def details(self, slot: str) -> dict[str, Any]:
        return {}  # The balance is read live with the status.

    def refresh_usage(self, slot: str) -> bool:
        return False

    def credentials(self, slot: str) -> dict[str, Any]:
        """The saved token file, for a paired session that runs the CLI elsewhere."""
        token = read_json(token_path(self.home(slot)))
        if token is None or not token.get("refresh_token"):
            raise CliError(f"colab-{slot} has no saved sign-in")
        return token

    def start_login(self, slot: str, finalize: Finalizer) -> ColabLogin:
        home = self.home(slot)
        (home / TOKEN_DIR).mkdir(mode=0o700, parents=True, exist_ok=True)
        set_aside_login(home)
        try:
            return ColabLogin(
                self.config.colab_command,
                self.environment(slot),
                home,
                url_timeout=self.config.url_timeout_seconds,
                exchange_timeout=self.config.code_exchange_timeout_seconds,
                finalize=finalize,
            )
        except LoginError:
            settle_set_aside_login(home)
            raise

    def logout(self, slot: str) -> None:
        """Forget the account on this host; the CLI has no logout of its own."""
        home = self.home(slot)
        try:
            token_path(home).unlink(missing_ok=True)
            with self._account_lock:
                (home / ACCOUNT_NAME).unlink(missing_ok=True)
        except OSError as exc:
            raise CliError(f"cannot sign colab out: {exc.strerror}") from exc
