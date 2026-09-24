import contextlib
import json
import re
import socketserver
import threading
import time
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from concurrent.futures import wait as wait_for
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from typing import Any, Protocol
from urllib.parse import parse_qs, urlsplit

from ai_accounts_agent.claude import ClaudeAccounts, mark_onboarding_done
from ai_accounts_agent.codex import CodexAccounts
from ai_accounts_agent.config import SLOTS, TOOLS, AgentConfig
from ai_accounts_agent.runner import CliError
from ai_accounts_agent.security import (
    NONCE_HEADER,
    SIGNATURE_HEADER,
    TIMESTAMP_HEADER,
    NonceCache,
    sanitize,
    verify_request,
)
from ai_accounts_agent.sessions import (
    NOT_SIGNED_IN,
    Finalizer,
    LoginError,
    LoginHandle,
    LoginRegistry,
)
from ai_accounts_agent.statusline import atomic_write_text, ensure_statusline

Response = tuple[int, dict[str, Any]]

_TOOL_SLOT = r"(claude|codex)/([a-e])"
_LOGIN_ID = r"([0-9a-f]{32})"
# A slow CLI turns into "still checking" for its card instead of a timeout for the page;
# the check keeps running and fills the cache for the next read.
OVERVIEW_DEADLINE_SECONDS = 12.0
ERROR_CACHE_SECONDS = 10.0


class Accounts(Protocol):
    def status(self, slot: str) -> dict[str, Any]: ...

    def start_login(self, slot: str, finalize: Finalizer) -> LoginHandle: ...

    def logout(self, slot: str) -> None: ...

    def details(self, slot: str) -> dict[str, Any]: ...

    def has_credentials(self, slot: str) -> bool: ...

    def refresh_usage(self, slot: str) -> bool: ...


def _problem(status: int, code: str, detail: str) -> Response:
    return status, {"code": code, "detail": detail}


class StatusCache:
    """One CLI check per account at a time; readers of a fresh entry skip the CLI."""

    def __init__(self, clock: Callable[[], float]) -> None:
        self._clock = clock
        self._entries: dict[tuple[str, str], tuple[float, dict[str, Any]]] = {}
        self._locks: dict[tuple[str, str], threading.Lock] = {}
        self._guard = threading.Lock()

    def _lock_for(self, key: tuple[str, str]) -> threading.Lock:
        with self._guard:
            return self._locks.setdefault(key, threading.Lock())

    def cached(self, key: tuple[str, str]) -> dict[str, Any] | None:
        with self._guard:
            entry = self._entries.get(key)
        if entry is None or entry[0] <= self._clock():
            return None
        return entry[1]

    def get(
        self,
        key: tuple[str, str],
        compute: Callable[[], dict[str, Any]],
        ttl: float,
        *,
        fresh: bool = False,
    ) -> dict[str, Any]:
        with self._lock_for(key):
            if not fresh:
                cached = self.cached(key)
                if cached is not None:
                    return cached
            value = compute()
            lifetime = ERROR_CACHE_SECONDS if value.get("error") else ttl
            with self._guard:
                self._entries[key] = (self._clock() + lifetime, value)
            return value

    def put(self, key: tuple[str, str], value: dict[str, Any], ttl: float) -> None:
        with self._guard:
            self._entries[key] = (self._clock() + ttl, value)

    def invalidate(self, key: tuple[str, str]) -> None:
        with self._guard:
            self._entries.pop(key, None)


class AgentApplication:
    def __init__(
        self,
        config: AgentConfig,
        *,
        claude: Accounts | None = None,
        codex: Accounts | None = None,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self.config = config
        self.clock = clock
        self.nonces = NonceCache()
        self.accounts: dict[str, Accounts] = {
            "claude": claude or ClaudeAccounts(config),
            "codex": codex or CodexAccounts(config),
        }
        self.logins = LoginRegistry(config.login_ttl_seconds, clock)
        self.cache = StatusCache(clock)
        self.executor = ThreadPoolExecutor(max_workers=len(TOOLS) * len(SLOTS) * 2)
        self._usage_lock = threading.Lock()
        self._usage_running: set[str] = set()
        self._usage_attempts: dict[str, float] = {}
        self._prepare_state()

    def _prepare_state(self) -> None:
        self.config.state_root.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.config.home_path.mkdir(mode=0o700, exist_ok=True)
        for tool in TOOLS:
            for slot in SLOTS:
                self.config.slot_path(tool, slot).mkdir(mode=0o700, exist_ok=True)
        for slot in SLOTS:
            # Idempotent; also repairs a status line that /statusline replaced.
            with contextlib.suppress(OSError):
                ensure_statusline(
                    self.config.slot_path("claude", slot), self.config.recorder_for(slot)
                )

    # --- account state -------------------------------------------------------------

    def ttl_for(self, tool: str) -> float:
        return (
            self.config.claude_cache_seconds
            if tool == "claude"
            else self.config.codex_cache_seconds
        )

    def check(self, tool: str, slot: str) -> dict[str, Any]:
        signed_out: dict[str, Any] = {
            "logged_in": False,
            "auth_method": None,
            "email": None,
            "organization": None,
            "plan": None,
            "error": None,
            "checked_at": int(self.clock()),
        }
        # Most slots are empty; skip starting a CLI just to hear that.
        if not self.accounts[tool].has_credentials(slot):
            return signed_out
        try:
            status = dict(self.accounts[tool].status(slot))
        except CliError as exc:
            return {
                "logged_in": None,
                "auth_method": None,
                "email": None,
                "organization": None,
                "plan": None,
                "error": str(exc),
            }
        status.setdefault("error", None)
        status["checked_at"] = int(self.clock())
        return status

    def status(self, tool: str, slot: str, *, fresh: bool = False) -> dict[str, Any]:
        return self.cache.get(
            (tool, slot), lambda: self.check(tool, slot), self.ttl_for(tool), fresh=fresh
        )

    def default_slot(self, tool: str) -> str:
        try:
            value = self.config.default_path(tool).read_text(encoding="utf-8").strip()
        except OSError:
            return SLOTS[0]
        return value if value in SLOTS else SLOTS[0]

    def email_allowed(self, email: str | None) -> bool | None:
        if not self.config.allowed_emails or not email:
            return None
        return email.lower() in self.config.allowed_emails

    def slot_view(self, tool: str, slot: str, status: dict[str, Any]) -> dict[str, Any]:
        now = self.clock()
        session = self.logins.active_for(tool, slot)
        view: dict[str, Any] = {
            "tool": tool,
            "slot": slot,
            "is_default": self.default_slot(tool) == slot,
            "logged_in": status.get("logged_in"),
            "auth_method": status.get("auth_method"),
            "email": status.get("email"),
            "organization": status.get("organization"),
            "plan": status.get("plan"),
            "email_allowed": self.email_allowed(status.get("email")),
            "usage": status.get("usage"),
            "usage_error": status.get("usage_error"),
            "recorder_installed": None,
            "checked_at": status.get("checked_at"),
            "error": status.get("error"),
            "login": session.view(now) if session is not None else None,
        }
        view.update(self.accounts[tool].details(slot))
        view["usage_refreshing"] = tool == "claude" and self.usage_refreshing(slot)
        return view

    # --- Claude usage ----------------------------------------------------------------

    def usage_refreshing(self, slot: str) -> bool:
        with self._usage_lock:
            return slot in self._usage_running

    def maybe_refresh_usage(
        self, slot: str, status: dict[str, Any], *, force: bool, after_login: bool = False
    ) -> bool:
        """Start a background usage probe for a signed-in Claude subscription when due.

        A page view starts one when the snapshot is missing or older than max_age; the
        refresh button and a finished login start one regardless, but no account is
        probed more than once per min_interval, and a page view does not retry a probe
        that found nothing for retry seconds. Returns whether a probe is running.
        """
        if status.get("logged_in") is not True or status.get("auth_method") != "claude.ai":
            return False
        if not after_login and self.logins.active_for("claude", slot) is not None:
            return False  # A probe and `claude auth login` must not share the directory.
        now = self.clock()
        with self._usage_lock:
            if slot in self._usage_running:
                return True
            last = self._usage_attempts.get(slot)
            if last is not None and now - last < self.config.claude_usage_min_interval_seconds:
                return False
            if not force:
                usage = self.accounts["claude"].details(slot).get("usage")
                recorded = usage.get("recorded_at") if isinstance(usage, dict) else None
                if (
                    isinstance(recorded, int | float)
                    and now - recorded < self.config.claude_usage_max_age_seconds
                ):
                    return False
                if last is not None and now - last < self.config.claude_usage_retry_seconds:
                    return False
            self._usage_running.add(slot)
            self._usage_attempts[slot] = now
        self.executor.submit(self._refresh_usage, slot)
        return True

    def _refresh_usage(self, slot: str) -> None:
        try:
            # Whatever breaks, the page shows the last snapshot and its age.
            with contextlib.suppress(Exception):
                self.accounts["claude"].refresh_usage(slot)
        finally:
            with self._usage_lock:
                self._usage_running.discard(slot)

    def overview(self, fresh: bool) -> dict[str, Any]:
        keys = [(tool, slot) for tool in TOOLS for slot in SLOTS]
        futures: dict[tuple[str, str], Future[dict[str, Any]]] = {
            key: self.executor.submit(self.status, key[0], key[1], fresh=fresh) for key in keys
        }
        wait_for(futures.values(), timeout=OVERVIEW_DEADLINE_SECONDS)
        slots = []
        for key in keys:
            future = futures[key]
            if future.done():
                status = future.result()
            else:
                status = self.cache.cached(key) or {
                    "logged_in": None,
                    "error": "still checking this account; refresh in a moment",
                }
            if key[0] == "claude":
                self.maybe_refresh_usage(key[1], status, force=fresh)
            slots.append(self.slot_view(key[0], key[1], status))
        return {
            "slots": slots,
            "defaults": {tool: self.default_slot(tool) for tool in TOOLS},
            "allowlist_configured": bool(self.config.allowed_emails),
        }

    # --- logins --------------------------------------------------------------------

    def finalize(self, tool: str, slot: str) -> str | None:
        """Accept a finished login, or undo it when the account is not on the list."""
        key = (tool, slot)
        self.cache.invalidate(key)
        status = self.check(tool, slot)
        if status.get("error"):
            return str(status["error"])
        if not status.get("logged_in"):
            return NOT_SIGNED_IN
        if self.email_allowed(status.get("email")) is False:
            with contextlib.suppress(CliError):
                self.accounts[tool].logout(slot)
            self.cache.invalidate(key)
            return (
                f"{status.get('email')} is not in AI_ACCOUNTS_ALLOWED_EMAILS on the host, "
                "so it was signed out again"
            )
        if tool == "claude":
            with contextlib.suppress(OSError):
                ensure_statusline(self.config.slot_path(tool, slot), self.config.recorder_for(slot))
            with contextlib.suppress(OSError):
                mark_onboarding_done(self.config.slot_path(tool, slot))
        self.cache.put(key, status, self.ttl_for(tool))
        if tool == "claude":
            self.maybe_refresh_usage(slot, status, force=True, after_login=True)
        return None

    def start_login(self, tool: str, slot: str) -> Response:
        accounts = self.accounts[tool]

        def factory() -> LoginHandle:
            return accounts.start_login(slot, lambda: self.finalize(tool, slot))

        try:
            session, created = self.logins.start(tool, slot, factory)
        except (LoginError, CliError) as exc:
            return _problem(HTTPStatus.BAD_GATEWAY, "login_start_failed", str(exc))
        status = HTTPStatus.CREATED if created else HTTPStatus.OK
        return status, session.view(self.clock())

    def submit_code(self, session_id: str, body: bytes) -> Response:
        session = self.logins.get(session_id)
        if session is None:
            return _problem(HTTPStatus.NOT_FOUND, "login_not_found", "login not found")
        payload = _json_object(body)
        code = payload.get("code") if payload is not None else None
        if not isinstance(code, str):
            return _problem(HTTPStatus.UNPROCESSABLE_ENTITY, "login_code_invalid", "code missing")
        if session.handle.kind != "paste_code":
            return _problem(
                HTTPStatus.CONFLICT, "login_code_not_expected", "this login takes no code"
            )
        try:
            session.handle.submit_code(code.strip())
        except LoginError as exc:
            return _problem(HTTPStatus.UNPROCESSABLE_ENTITY, "login_code_rejected", str(exc))
        return HTTPStatus.ACCEPTED, session.view(self.clock())

    def logout(self, tool: str, slot: str) -> Response:
        self.logins.cancel_slot(tool, slot)
        try:
            self.accounts[tool].logout(slot)
        except CliError as exc:
            return _problem(HTTPStatus.BAD_GATEWAY, "logout_failed", str(exc))
        finally:
            self.cache.invalidate((tool, slot))
        return HTTPStatus.OK, {"tool": tool, "slot": slot, "logged_in": False}

    def set_default(self, tool: str, body: bytes) -> Response:
        payload = _json_object(body)
        slot = payload.get("slot") if payload is not None else None
        if slot not in SLOTS:
            return _problem(HTTPStatus.UNPROCESSABLE_ENTITY, "slot_invalid", "unknown slot")
        atomic_write_text(self.config.default_path(tool), f"{slot}\n", 0o600)
        return HTTPStatus.OK, {"defaults": {name: self.default_slot(name) for name in TOOLS}}

    # --- routing -------------------------------------------------------------------

    def handle(self, method: str, path: str, body: bytes, headers: Any) -> Response:
        if not verify_request(
            self.nonces,
            self.config.hmac_key,
            method,
            path,
            body,
            headers.get(TIMESTAMP_HEADER),
            headers.get(NONCE_HEADER),
            headers.get(SIGNATURE_HEADER),
        ):
            return _problem(
                HTTPStatus.UNAUTHORIZED, "ai_accounts_agent_auth_failed", "authentication failed"
            )
        parts = urlsplit(path)
        route = parts.path
        try:
            if method == "GET" and route == "/v1/accounts":
                fresh = parse_qs(parts.query).get("fresh") == ["1"]
                return HTTPStatus.OK, self.overview(fresh)
            if match := re.fullmatch(rf"/v1/accounts/{_TOOL_SLOT}/login", route):
                if method == "POST":
                    return self.start_login(match.group(1), match.group(2))
            elif match := re.fullmatch(rf"/v1/accounts/{_TOOL_SLOT}/logout", route):
                if method == "POST":
                    return self.logout(match.group(1), match.group(2))
            elif match := re.fullmatch(rf"/v1/logins/{_LOGIN_ID}", route):
                if method == "GET":
                    session = self.logins.get(match.group(1))
                    if session is None:
                        return _problem(HTTPStatus.NOT_FOUND, "login_not_found", "login not found")
                    return HTTPStatus.OK, session.view(self.clock())
            elif match := re.fullmatch(rf"/v1/logins/{_LOGIN_ID}/code", route):
                if method == "POST":
                    return self.submit_code(match.group(1), body)
            elif match := re.fullmatch(rf"/v1/logins/{_LOGIN_ID}/cancel", route):
                if method == "POST":
                    session = self.logins.cancel(match.group(1))
                    if session is None:
                        return _problem(HTTPStatus.NOT_FOUND, "login_not_found", "login not found")
                    return HTTPStatus.OK, session.view(self.clock())
            elif match := re.fullmatch(r"/v1/defaults/(claude|codex)", route):
                if method == "PUT":
                    return self.set_default(match.group(1), body)
            return _problem(HTTPStatus.NOT_FOUND, "not_found", "endpoint not found")
        except Exception as exc:  # The socket must answer, whatever broke underneath.
            return _problem(
                HTTPStatus.SERVICE_UNAVAILABLE,
                "ai_accounts_agent_error",
                sanitize(str(exc)) or "agent operation failed",
            )


def _json_object(body: bytes) -> dict[str, Any] | None:
    try:
        value = json.loads(body or b"{}")
    except ValueError:
        return None
    return value if isinstance(value, dict) else None


_UnixStreamServer = getattr(socketserver, "UnixStreamServer", socketserver.TCPServer)


class UnixHTTPServer(socketserver.ThreadingMixIn, _UnixStreamServer):  # type: ignore[misc,valid-type]
    daemon_threads = True


MAX_BODY_BYTES = 16_384


def make_handler(application: AgentApplication) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        # Drop half-open connections instead of holding a worker thread forever.
        timeout = 30

        def _handle(self) -> None:
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = -1
            if length < 0:
                self._respond(*_problem(400, "invalid_content_length", "bad Content-Length"))
                return
            if length > MAX_BODY_BYTES:
                self._respond(*_problem(413, "request_too_large", "request body too large"))
                return
            body = self.rfile.read(length) if length else b""
            self._respond(*application.handle(self.command, self.path, body, self.headers))

        def _respond(self, status: int, payload: dict[str, Any]) -> None:
            encoded = json.dumps(payload, separators=(",", ":")).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        do_GET = _handle
        do_POST = _handle
        do_PUT = _handle

        def log_message(self, format: str, *args: object) -> None:
            return

    return Handler


def serve(config: AgentConfig) -> None:
    if not hasattr(socketserver, "UnixStreamServer"):
        raise RuntimeError("the AI accounts agent requires Unix-domain sockets")
    config.socket_path.parent.mkdir(parents=True, exist_ok=True)
    if config.socket_path.exists():
        config.socket_path.unlink()
    application = AgentApplication(config)
    with UnixHTTPServer(str(config.socket_path), make_handler(application)) as server:
        config.socket_path.chmod(0o660)
        try:
            server.serve_forever()
        finally:
            application.logins.close_all()
