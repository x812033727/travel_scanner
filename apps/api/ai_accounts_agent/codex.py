import contextlib
import json
import os
import signal
import subprocess
import sys
import threading
from collections.abc import Callable, Mapping, Sequence
from typing import IO, Any
from urllib.parse import urlsplit

from ai_accounts_agent.config import AgentConfig
from ai_accounts_agent.runner import CliError, cli_environment, text_or_none
from ai_accounts_agent.security import sanitize
from ai_accounts_agent.sessions import (
    CANCELLED,
    FAILED,
    PENDING,
    SUCCEEDED,
    VERIFYING,
    Finalizer,
    LoginError,
)

CLIENT_INFO = {"name": "mokaair_ai_accounts", "title": "Mokaair AI accounts", "version": "1"}
VERIFICATION_HOSTS = ("openai.com", "chatgpt.com")
MAX_LINE_BYTES = 1_048_576

Notification = Callable[[str, Mapping[str, Any]], None]


class AppServer:
    """A `codex app-server` child spoken to in newline-delimited JSON-RPC over stdio.

    The protocol is JSON-RPC 2.0 without the "jsonrpc" member. Requests the server sends
    back (approvals and the like) never arise for account calls and are answered with an
    error so the server does not wait on them.
    """

    def __init__(
        self,
        command: Sequence[str],
        environment: Mapping[str, str],
        timeout: float,
        on_notification: Notification | None = None,
    ) -> None:
        self._timeout = timeout
        self._on_notification = on_notification
        self._lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._next_id = 0
        self._waiting: dict[int, threading.Event] = {}
        self._responses: dict[int, Mapping[str, Any]] = {}
        self._closed = threading.Event()
        try:
            self._process = subprocess.Popen(  # noqa: S603 - fixed argv, shell=False
                [*command, "app-server"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                env=dict(environment),
                start_new_session=True,
            )
        except OSError as exc:
            raise CliError(f"cannot start codex: {exc.strerror}") from exc
        assert self._process.stdin is not None and self._process.stdout is not None
        self._stdin: IO[bytes] = self._process.stdin
        threading.Thread(target=self._read, args=(self._process.stdout,), daemon=True).start()

    def __enter__(self) -> "AppServer":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _read(self, stream: IO[bytes]) -> None:
        for line in iter(lambda: stream.readline(MAX_LINE_BYTES), b""):
            try:
                message = json.loads(line)
            except ValueError:
                continue
            if not isinstance(message, dict):
                continue
            identifier = message.get("id")
            method = message.get("method")
            if isinstance(method, str):
                if identifier is not None:
                    with contextlib.suppress(CliError):
                        self._send(
                            {
                                "id": identifier,
                                "error": {
                                    "code": -32601,
                                    "message": "not supported by this client",
                                },
                            }
                        )
                elif self._on_notification is not None:
                    params = message.get("params")
                    self._on_notification(method, params if isinstance(params, dict) else {})
                continue
            if isinstance(identifier, int):
                with self._lock:
                    event = self._waiting.get(identifier)
                    self._responses[identifier] = message
                if event is not None:
                    event.set()
        self._closed.set()
        with self._lock:
            for event in self._waiting.values():
                event.set()

    def _send(self, message: Mapping[str, Any]) -> None:
        encoded = json.dumps(message, separators=(",", ":")).encode() + b"\n"
        with self._write_lock:
            try:
                self._stdin.write(encoded)
                self._stdin.flush()
            except (OSError, ValueError) as exc:
                raise CliError("codex app-server stopped") from exc

    def request(self, method: str, params: Mapping[str, Any] | None = None) -> Any:
        with self._lock:
            self._next_id += 1
            identifier = self._next_id
            event = threading.Event()
            self._waiting[identifier] = event
        message: dict[str, Any] = {"id": identifier, "method": method}
        if params is not None:
            message["params"] = params
        self._send(message)
        answered = event.wait(self._timeout)
        with self._lock:
            self._waiting.pop(identifier, None)
            response = self._responses.pop(identifier, None)
        if response is None:
            raise CliError(
                f"codex did not answer {method} in time"
                if not answered or not self._closed.is_set()
                else "codex app-server stopped"
            )
        error = response.get("error")
        if error is not None:
            detail = error.get("message") if isinstance(error, dict) else None
            raise CliError(sanitize(str(detail or f"codex refused {method}")))
        return response.get("result")

    def initialize(self) -> None:
        self.request("initialize", {"clientInfo": CLIENT_INFO, "capabilities": None})
        self._send({"method": "initialized"})

    def close(self) -> None:
        with contextlib.suppress(OSError):  # Gone already when the server exited first.
            self._stdin.close()
        try:
            self._process.wait(2)
        except subprocess.TimeoutExpired:
            self._terminate()

    def _terminate(self) -> None:
        if sys.platform == "win32":
            self._process.kill()
            self._process.wait(3)
            return
        # The npm entry point is a node wrapper around the native binary; signalling only
        # the wrapper can leave the binary running, so signal the whole session.
        for signum in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(self._process.pid, signum)
            except ProcessLookupError:
                return
            try:
                self._process.wait(3)
                return
            except subprocess.TimeoutExpired:
                continue


def _epoch_seconds(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    # Milliseconds would put the reset thousands of years out.
    return int(value / 1000) if value > 10_000_000_000 else int(value)


def usage_windows(limits: Any) -> list[dict[str, Any]]:
    if not isinstance(limits, Mapping):
        return []
    by_limit = limits.get("rateLimitsByLimitId")
    snapshot = by_limit.get("codex") if isinstance(by_limit, Mapping) else None
    if not isinstance(snapshot, Mapping):
        snapshot = limits.get("rateLimits")
    if not isinstance(snapshot, Mapping):
        return []
    windows: list[dict[str, Any]] = []
    for key in ("primary", "secondary"):
        window = snapshot.get(key)
        if not isinstance(window, Mapping):
            continue
        used = window.get("usedPercent")
        if isinstance(used, bool) or not isinstance(used, int | float):
            continue
        minutes = window.get("windowDurationMins")
        windows.append(
            {
                "window_minutes": minutes if isinstance(minutes, int) else None,
                "used_percent": max(0.0, min(100.0, float(used))),
                "resets_at": _epoch_seconds(window.get("resetsAt")),
            }
        )
    return windows


def is_verification_url(url: str) -> bool:
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    return parts.scheme == "https" and any(
        host == allowed or host.endswith(f".{allowed}") for allowed in VERIFICATION_HOSTS
    )


class CodexLogin:
    """A device-code login held open in its own app-server until it completes."""

    kind = "device_code"

    def __init__(
        self,
        command: Sequence[str],
        environment: Mapping[str, str],
        timeout: float,
        finalize: Finalizer,
    ) -> None:
        self._lock = threading.Lock()
        self._status = PENDING
        self._error: str | None = None
        self._finalize = finalize
        self._login_id: str | None = None
        self._server = AppServer(command, environment, timeout, self._notified)
        try:
            self._server.initialize()
            result = self._server.request("account/login/start", {"type": "chatgptDeviceCode"})
        except CliError as exc:
            self._server.close()
            raise LoginError(str(exc)) from exc
        url = result.get("verificationUrl") if isinstance(result, dict) else None
        code = result.get("userCode") if isinstance(result, dict) else None
        login_id = result.get("loginId") if isinstance(result, dict) else None
        if not isinstance(url, str) or not is_verification_url(url) or not isinstance(code, str):
            self._server.close()
            raise LoginError("codex did not return a device code")
        self._login_id = login_id if isinstance(login_id, str) else None
        self.url: str = url
        self.user_code: str | None = code

    def _notified(self, method: str, params: Mapping[str, Any]) -> None:
        if method != "account/login/completed":
            return
        login_id = params.get("loginId")
        if login_id is not None and self._login_id is not None and login_id != self._login_id:
            return
        with self._lock:
            if self._status != PENDING:
                return
            if params.get("success") is not True:
                reason = params.get("error")
                self._status = FAILED
                self._error = sanitize(str(reason)) if reason else "the sign-in did not finish"
            else:
                self._status = VERIFYING
        # This runs on the reader thread; checking the account starts another CLI, so do
        # it elsewhere and let the reader finish.
        threading.Thread(target=self._complete, daemon=True).start()

    def _complete(self) -> None:
        self._server.close()
        with self._lock:
            if self._status != VERIFYING:
                return
        rejection = self._finalize()
        with self._lock:
            if self._status == VERIFYING:
                if rejection is None:
                    self._status, self._error = SUCCEEDED, None
                else:
                    self._status, self._error = FAILED, rejection

    def state(self) -> tuple[str, str | None]:
        with self._lock:
            return self._status, self._error

    def submit_code(self, code: str) -> None:
        raise LoginError("a device-code login takes no code from this side")

    def cancel(self) -> None:
        with self._lock:
            if self._status not in (PENDING, VERIFYING):
                return
            self._status, self._error = CANCELLED, None
        if self._login_id is not None:
            # Closing the server below ends the login even if the cancel call fails.
            with contextlib.suppress(CliError):
                self._server.request("account/login/cancel", {"loginId": self._login_id})
        self._server.close()


class CodexAccounts:
    def __init__(self, config: AgentConfig) -> None:
        self.config = config

    def environment(self, slot: str) -> dict[str, str]:
        return cli_environment(
            self.config, {"CODEX_HOME": str(self.config.slot_path("codex", slot))}
        )

    def _server(self, slot: str) -> AppServer:
        return AppServer(
            self.config.codex_command, self.environment(slot), self.config.command_timeout_seconds
        )

    def status(self, slot: str) -> dict[str, Any]:
        with self._server(slot) as server:
            server.initialize()
            result = server.request("account/read", {"refreshToken": False})
            account = result.get("account") if isinstance(result, dict) else None
            if not isinstance(account, dict):
                return {
                    "logged_in": False,
                    "auth_method": None,
                    "email": None,
                    "organization": None,
                    "plan": None,
                }
            kind = account.get("type")
            status: dict[str, Any] = {
                "logged_in": True,
                "auth_method": "chatgpt" if kind == "chatgpt" else text_or_none(kind),
                "email": text_or_none(account.get("email")),
                "organization": None,
                "plan": text_or_none(account.get("planType")),
            }
            if kind != "chatgpt":
                return status
            try:
                limits = server.request("account/rateLimits/read")
            except CliError as exc:
                status["usage_error"] = str(exc)
            else:
                status["usage"] = {"source": "live", "windows": usage_windows(limits)}
            return status

    def start_login(self, slot: str, finalize: Finalizer) -> CodexLogin:
        return CodexLogin(
            self.config.codex_command,
            self.environment(slot),
            self.config.command_timeout_seconds,
            finalize,
        )

    def logout(self, slot: str) -> None:
        with self._server(slot) as server:
            server.initialize()
            server.request("account/logout")

    def has_credentials(self, slot: str) -> bool:
        return (self.config.slot_path("codex", slot) / "auth.json").exists()

    def details(self, slot: str) -> dict[str, Any]:
        return {}  # Codex usage is read live with the status.

    def refresh_usage(self, slot: str) -> bool:
        return False  # Nothing to refresh apart from the status itself.
