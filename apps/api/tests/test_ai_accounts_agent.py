import hashlib
import hmac
import io
import json
import sys
import textwrap
import threading
import time
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

import ai_accounts_agent.__main__  # noqa: F401 - imported so mypy reads the entry point
from ai_accounts_agent import client, statusline
from ai_accounts_agent.claude import (
    CODE_PATTERN,
    ClaudeAccounts,
    ClaudeLogin,
    extract_authorize_url,
    is_authorize_url,
)
from ai_accounts_agent.codex import CodexAccounts, is_verification_url, usage_windows
from ai_accounts_agent.config import STATUSLINE_RECORDER, AgentConfig, parse_emails
from ai_accounts_agent.runner import CliError
from ai_accounts_agent.security import NonceCache, sanitize, signature_for, verify_request
from ai_accounts_agent.server import AgentApplication, UnixHTTPServer, make_handler
from ai_accounts_agent.sessions import (
    CANCELLED,
    EXPIRED,
    FAILED,
    NOT_SIGNED_IN,
    PENDING,
    SUCCEEDED,
    Finalizer,
    LoginHandle,
    LoginRegistry,
)

KEY = "ai-accounts-key-with-at-least-32-chars"
posix_only = pytest.mark.skipif(sys.platform == "win32", reason="needs a POSIX terminal")

FAKE_CODEX = textwrap.dedent(
    """
    import json, os, sys, threading, time
    home = os.environ["CODEX_HOME"]
    auth = os.path.join(home, "auth.json")
    lock = threading.Lock()

    def send(message):
        with lock:
            sys.stdout.write(json.dumps(message) + "\\n")
            sys.stdout.flush()

    def finish_login():
        time.sleep(0.2)
        control = os.path.join(home, "fake-login")
        outcome = json.load(open(control)) if os.path.exists(control) else {}
        if outcome.get("email"):
            json.dump({"email": outcome["email"]}, open(auth, "w"))
            send({"method": "account/login/completed",
                  "params": {"loginId": "L1", "success": True, "error": None}})
        elif outcome.get("error"):
            send({"method": "account/login/completed",
                  "params": {"loginId": "L1", "success": False, "error": outcome["error"]}})

    for line in sys.stdin:
        message = json.loads(line)
        method, ident = message.get("method"), message.get("id")
        if ident is None:
            continue
        signed_in = os.path.exists(auth)
        if method == "initialize":
            send({"id": ident, "result": {"userAgent": "fake", "codexHome": home}})
        elif method == "account/read":
            account = None
            if signed_in:
                email = json.load(open(auth))["email"]
                account = {"type": "chatgpt", "email": email, "planType": "pro"}
            send({"id": ident, "result": {"account": account, "requiresOpenaiAuth": True}})
        elif method == "account/rateLimits/read":
            if not signed_in:
                send({"id": ident, "error": {"code": -32600,
                      "message": "authentication required"}})
                continue
            send({"id": ident, "result": {"rateLimits": {
                "primary": {"usedPercent": 100, "windowDurationMins": 10080,
                            "resetsAt": 1790451041},
                "secondary": None}, "rateLimitsByLimitId": None}})
        elif method == "account/login/start":
            send({"id": ident, "result": {"type": "chatgptDeviceCode", "loginId": "L1",
                  "verificationUrl": "https://auth.openai.com/codex/device",
                  "userCode": "ABCD-EFGH"}})
            threading.Thread(target=finish_login, daemon=True).start()
        elif method in ("account/login/cancel", "account/logout"):
            if method == "account/logout" and signed_in:
                os.remove(auth)
            send({"id": ident, "result": {}})
        else:
            send({"id": ident, "error": {"code": -32601, "message": "unknown"}})
    """
)

FAKE_CLAUDE = textwrap.dedent(
    """
    import json, os, sys
    home = os.environ["CLAUDE_CONFIG_DIR"]
    credentials = os.path.join(home, ".credentials.json")
    command = sys.argv[1:3]
    if command == ["auth", "status"]:
        if os.path.exists(credentials):
            email = json.load(open(credentials))["email"]
            print(json.dumps({"loggedIn": True, "authMethod": "claude.ai", "email": email,
                              "orgName": "Org", "subscriptionType": "max"}))
        else:
            print(json.dumps({"loggedIn": False}))
    elif command == ["auth", "logout"]:
        if os.path.exists(credentials):
            os.remove(credentials)
        print("Successfully logged out")
    elif command == ["auth", "login"]:
        url = "https://claude.com/cai/oauth/authorize?code=true&state=secret-state"
        sys.stdout.write("Opening browser to sign in...\\r\\n")
        sys.stdout.write("If the browser didn't open, visit: \\x1b]8;;" + url + "\\x07"
                         + url + "\\x1b]8;;\\x07\\r\\n")
        sys.stdout.write("Paste code here if prompted > ")
        sys.stdout.flush()
        code = sys.stdin.readline().strip()
        if code.startswith("good"):
            control = os.path.join(home, "fake-login-email")
            email = open(control).read().strip() if os.path.exists(control) else "a@x.test"
            json.dump({"email": email}, open(credentials, "w"))
            sys.stdout.write("Login successful.\\r\\n")
            sys.exit(0)
        sys.stdout.write("OAuth error: Invalid code\\r\\n")
        sys.exit(1)
    """
)


def make_config(tmp_path: Path, **overrides: Any) -> AgentConfig:
    codex = tmp_path / "fake_codex.py"
    claude = tmp_path / "fake_claude.py"
    codex.write_text(FAKE_CODEX, encoding="utf-8")
    claude.write_text(FAKE_CLAUDE, encoding="utf-8")
    values: dict[str, Any] = {
        "hmac_key": KEY,
        "socket_path": tmp_path / "agent.sock",
        "state_root": tmp_path / "state",
        "claude_command": (sys.executable, str(claude)),
        "codex_command": (sys.executable, str(codex)),
        "url_timeout_seconds": 10.0,
        "command_timeout_seconds": 10.0,
        "code_exchange_timeout_seconds": 10.0,
    }
    values.update(overrides)
    return AgentConfig(**values)


def signed(
    application: AgentApplication,
    method: str,
    path: str,
    payload: Mapping[str, object] | None = None,
) -> tuple[int, dict[str, Any]]:
    body = json.dumps(payload).encode() if payload is not None else b""
    timestamp, nonce = str(int(time.time())), uuid4().hex
    headers = {
        "X-Agent-Timestamp": timestamp,
        "X-Agent-Nonce": nonce,
        "X-Agent-Signature": signature_for(KEY, timestamp, nonce, method, path, body),
    }
    return application.handle(method, path, body, headers)


def wait_until(check: Callable[[], bool], seconds: float = 10.0) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if check():
            return
        time.sleep(0.05)
    raise AssertionError("condition not met in time")


def slot_of(overview: dict[str, Any], tool: str, slot: str) -> dict[str, Any]:
    return next(item for item in overview["slots"] if (item["tool"], item["slot"]) == (tool, slot))


# --- signing ------------------------------------------------------------------------


def test_signature_accepts_once_and_rejects_replay_skew_and_tampering() -> None:
    nonces = NonceCache()
    now = 1_790_000_000
    nonce = uuid4().hex
    body = b'{"slot":"b"}'
    signature = signature_for(KEY, str(now), nonce, "PUT", "/v1/defaults/claude", body)
    arguments = (KEY, "PUT", "/v1/defaults/claude")
    assert verify_request(nonces, *arguments, body, str(now), nonce, signature, now=now)
    assert not verify_request(nonces, *arguments, body, str(now), nonce, signature, now=now)
    fresh = uuid4().hex
    fresh_signature = signature_for(KEY, str(now), fresh, "PUT", "/v1/defaults/claude", body)
    assert not verify_request(
        nonces, *arguments, b'{"slot":"a"}', str(now), fresh, fresh_signature, now=now
    )
    assert not verify_request(
        nonces, *arguments, body, str(now), fresh, fresh_signature, now=now + 61
    )
    assert not verify_request(nonces, *arguments, body, str(now), "short", fresh_signature)


def test_unsigned_requests_are_refused(tmp_path: Path) -> None:
    application = AgentApplication(make_config(tmp_path))
    status, payload = application.handle("GET", "/v1/accounts", b"", {})
    assert status == 401
    assert payload["code"] == "ai_accounts_agent_auth_failed"


def test_sanitize_removes_codes_tokens_and_escapes() -> None:
    text = (
        "visit https://claude.com/x?code=abc123&state=zzz then Bearer "
        "eyJhbGciOi.eyJzdWIiOi.sig token=sk-ant-oat01-abcdefghijklmnopqrstuvwx\x1b[31m"
    )
    cleaned = sanitize(text)
    for secret in ("abc123", "zzz", "eyJhbGciOi", "abcdefghijklmnop", "\x1b"):
        assert secret not in cleaned
    assert "exit code: 1" in sanitize("exit code: 1")


# --- config -------------------------------------------------------------------------


def test_config_from_env_requires_a_key_and_fixed_paths(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AI_ACCOUNTS_AGENT_HMAC_KEY", "short")
    with pytest.raises(RuntimeError, match="32 characters"):
        AgentConfig.from_env()
    monkeypatch.setenv("AI_ACCOUNTS_AGENT_HMAC_KEY", KEY)
    monkeypatch.setenv("AI_ACCOUNTS_AGENT_SOCKET", "/tmp/elsewhere.sock")
    with pytest.raises(RuntimeError, match="fixed by systemd"):
        AgentConfig.from_env()
    monkeypatch.delenv("AI_ACCOUNTS_AGENT_SOCKET")
    monkeypatch.setenv("AI_ACCOUNTS_ALLOWED_EMAILS", " Owner@Example.com, b@x.test ,")
    config = AgentConfig.from_env()
    assert config.allowed_emails == {"owner@example.com", "b@x.test"}
    assert parse_emails("") == frozenset()


def test_statusline_recorder_path_matches_the_config() -> None:
    assert statusline.RECORDER_PATH == STATUSLINE_RECORDER


# --- routing ------------------------------------------------------------------------


def test_overview_lists_every_slot_without_starting_clis_for_empty_ones(
    tmp_path: Path,
) -> None:
    config = make_config(tmp_path, claude_command=("/missing/claude",))
    application = AgentApplication(config)
    status, overview = signed(application, "GET", "/v1/accounts")
    assert status == 200
    assert len(overview["slots"]) == 10
    assert overview["defaults"] == {"claude": "a", "codex": "a"}
    assert overview["allowlist_configured"] is False
    claude_a = slot_of(overview, "claude", "a")
    # The missing binary was never run: an empty slot is signed out without a CLI call.
    assert claude_a["logged_in"] is False
    assert claude_a["error"] is None
    assert claude_a["recorder_installed"] is True


def test_routes_reject_unknown_slots_methods_and_logins(tmp_path: Path) -> None:
    application = AgentApplication(make_config(tmp_path))
    assert signed(application, "POST", "/v1/accounts/claude/f/login")[0] == 404
    assert signed(application, "GET", "/v1/accounts/claude/a/login")[0] == 404
    assert signed(application, "POST", "/v1/accounts/gemini/a/login")[0] == 404
    assert signed(application, "GET", f"/v1/logins/{uuid4().hex}")[0] == 404
    status, payload = signed(application, "POST", f"/v1/logins/{uuid4().hex}/code", {"code": "x"})
    assert (status, payload["code"]) == (404, "login_not_found")


def test_default_slot_is_written_for_the_shell_to_read(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    application = AgentApplication(config)
    status, payload = signed(application, "PUT", "/v1/defaults/codex", {"slot": "c"})
    assert status == 200
    assert payload["defaults"] == {"claude": "a", "codex": "c"}
    assert config.default_path("codex").read_text(encoding="utf-8") == "c\n"
    assert signed(application, "PUT", "/v1/defaults/codex", {"slot": "z"})[0] == 422
    overview = signed(application, "GET", "/v1/accounts")[1]
    assert slot_of(overview, "codex", "c")["is_default"] is True


# --- codex --------------------------------------------------------------------------


def test_codex_device_login_signs_in_and_reports_live_usage(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    application = AgentApplication(config)
    (config.slot_path("codex", "b") / "fake-login").write_text(
        json.dumps({"email": "second@x.test"}), encoding="utf-8"
    )
    status, login = signed(application, "POST", "/v1/accounts/codex/b/login")
    assert status == 201
    assert login["kind"] == "device_code"
    assert login["url"] == "https://auth.openai.com/codex/device"
    assert login["user_code"] == "ABCD-EFGH"
    # A second click returns the login already open for the slot.
    again = signed(application, "POST", "/v1/accounts/codex/b/login")
    assert (again[0], again[1]["id"]) == (200, login["id"])

    def finished() -> bool:
        view = signed(application, "GET", f"/v1/logins/{login['id']}")[1]
        return bool(view["status"] == SUCCEEDED)

    wait_until(finished)
    view = signed(application, "GET", f"/v1/logins/{login['id']}")[1]
    assert view["url"] is None and view["user_code"] is None
    codex_b = slot_of(signed(application, "GET", "/v1/accounts")[1], "codex", "b")
    assert codex_b["logged_in"] is True
    assert codex_b["email"] == "second@x.test"
    assert codex_b["plan"] == "pro"
    assert codex_b["usage"] == {
        "source": "live",
        "windows": [{"window_minutes": 10080, "used_percent": 100.0, "resets_at": 1790451041}],
    }


def test_codex_login_outside_the_allowlist_is_signed_out_again(tmp_path: Path) -> None:
    config = make_config(tmp_path, allowed_emails=frozenset({"owner@x.test"}))
    application = AgentApplication(config)
    home = config.slot_path("codex", "a")
    (home / "fake-login").write_text(json.dumps({"email": "intruder@x.test"}), "utf-8")
    login = signed(application, "POST", "/v1/accounts/codex/a/login")[1]

    def failed() -> bool:
        view = signed(application, "GET", f"/v1/logins/{login['id']}")[1]
        return bool(view["status"] == FAILED)

    wait_until(failed)
    view = signed(application, "GET", f"/v1/logins/{login['id']}")[1]
    assert "intruder@x.test is not in AI_ACCOUNTS_ALLOWED_EMAILS" in view["error"]
    assert not (home / "auth.json").exists()


def test_codex_login_failure_and_cancel(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    application = AgentApplication(config)
    (config.slot_path("codex", "a") / "fake-login").write_text(
        json.dumps({"error": "device code authorization is disabled"}), "utf-8"
    )
    failing = signed(application, "POST", "/v1/accounts/codex/a/login")[1]
    wait_until(
        lambda: signed(application, "GET", f"/v1/logins/{failing['id']}")[1]["status"] == FAILED
    )
    view = signed(application, "GET", f"/v1/logins/{failing['id']}")[1]
    assert view["error"] == "device code authorization is disabled"

    pending = signed(application, "POST", "/v1/accounts/codex/c/login")[1]
    status, cancelled = signed(application, "POST", f"/v1/logins/{pending['id']}/cancel")
    assert (status, cancelled["status"]) == (200, CANCELLED)
    code_status, problem = signed(
        application, "POST", f"/v1/logins/{pending['id']}/code", {"code": "whatever-code"}
    )
    assert (code_status, problem["code"]) == (409, "login_code_not_expected")


def test_codex_logout_clears_the_slot(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    application = AgentApplication(config)
    home = config.slot_path("codex", "a")
    (home / "auth.json").write_text(json.dumps({"email": "a@x.test"}), "utf-8")
    assert slot_of(signed(application, "GET", "/v1/accounts")[1], "codex", "a")["logged_in"]
    status, payload = signed(application, "POST", "/v1/accounts/codex/a/logout")
    assert (status, payload["logged_in"]) == (200, False)
    assert not (home / "auth.json").exists()
    assert slot_of(signed(application, "GET", "/v1/accounts")[1], "codex", "a")[
        "logged_in"
    ] is False


def test_codex_usage_windows_prefer_the_codex_bucket_and_convert_milliseconds() -> None:
    limits = {
        "rateLimits": {"primary": {"usedPercent": 1, "windowDurationMins": 300}},
        "rateLimitsByLimitId": {
            "codex": {
                "primary": {"usedPercent": 23.5, "windowDurationMins": 300, "resetsAt": 1790000000},
                "secondary": {
                    "usedPercent": 140,
                    "windowDurationMins": 10080,
                    "resetsAt": 1790451041000,
                },
            }
        },
    }
    assert usage_windows(limits) == [
        {"window_minutes": 300, "used_percent": 23.5, "resets_at": 1790000000},
        {"window_minutes": 10080, "used_percent": 100.0, "resets_at": 1790451041},
    ]
    assert usage_windows(None) == []
    assert is_verification_url("https://auth.openai.com/codex/device")
    assert not is_verification_url("https://auth.openai.com.evil.test/codex/device")


def test_codex_status_reports_a_cli_that_cannot_start(tmp_path: Path) -> None:
    config = make_config(tmp_path, codex_command=(str(tmp_path / "missing-codex"),))
    (config.state_root / "codex-a").mkdir(parents=True)
    (config.slot_path("codex", "a") / "auth.json").write_text("{}", "utf-8")
    with pytest.raises(CliError, match="cannot start"):
        CodexAccounts(config).status("a")


# --- claude -------------------------------------------------------------------------


def test_claude_status_reads_the_cli_and_the_usage_snapshot(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    application = AgentApplication(config)
    home = config.slot_path("claude", "a")
    (home / ".credentials.json").write_text(json.dumps({"email": "a@x.test"}), "utf-8")
    statusline.record_snapshot(
        home,
        {"rate_limits": {"five_hour": {"used_percentage": 23.5, "resets_at": 1790000000}}},
        now=1_789_990_000,
    )
    claude_a = slot_of(signed(application, "GET", "/v1/accounts")[1], "claude", "a")
    assert claude_a["logged_in"] is True
    assert (claude_a["email"], claude_a["plan"], claude_a["auth_method"]) == (
        "a@x.test",
        "max",
        "claude.ai",
    )
    assert claude_a["usage"] == {
        "source": "snapshot",
        "recorded_at": 1_789_990_000,
        "windows": [{"window_minutes": 300, "used_percent": 23.5, "resets_at": 1790000000}],
    }
    assert ClaudeAccounts(config).status("b") == {
        "logged_in": False,
        "auth_method": None,
        "email": None,
        "organization": None,
        "plan": None,
    }


def test_authorize_url_is_read_from_the_hyperlink_and_checked() -> None:
    url = "https://claude.com/cai/oauth/authorize?code=true&state=s"
    wrapped = f"visit: \x1b]8;;{url}\x07{url[:30]}\r\n{url[30:]}\x1b]8;;\x07"
    assert extract_authorize_url(wrapped) == url
    assert extract_authorize_url(f"\x1b[1mvisit {url}\x1b[0m") == url
    assert extract_authorize_url("visit https://evil.test/oauth/authorize") is None
    assert not is_authorize_url("https://claude.com.evil.test/oauth/authorize")
    assert not is_authorize_url("http://claude.com/oauth/authorize")
    assert CODE_PATTERN.fullmatch("AbC_-123.~#state-Part")
    assert not CODE_PATTERN.fullmatch("abc def ghij")
    assert not CODE_PATTERN.fullmatch("abcdefghij\x1b[A")


@posix_only
def test_claude_paste_code_login_signs_in(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    application = AgentApplication(config)
    status, login = signed(application, "POST", "/v1/accounts/claude/b/login")
    assert status == 201
    assert login["kind"] == "paste_code"
    assert login["url"] == "https://claude.com/cai/oauth/authorize?code=true&state=secret-state"
    code_status, view = signed(
        application, "POST", f"/v1/logins/{login['id']}/code", {"code": "  good-code#s  "}
    )
    assert (code_status, view["status"]) == (202, "verifying")
    wait_until(
        lambda: signed(application, "GET", f"/v1/logins/{login['id']}")[1]["status"] == SUCCEEDED
    )
    home = config.slot_path("claude", "b")
    assert statusline.recorder_installed(home, config.recorder_for("b"))
    claude_b = slot_of(signed(application, "GET", "/v1/accounts")[1], "claude", "b")
    assert (claude_b["logged_in"], claude_b["email"]) == (True, "a@x.test")


@posix_only
def test_claude_rejected_code_fails_without_echoing_it(tmp_path: Path) -> None:
    application = AgentApplication(make_config(tmp_path))
    login = signed(application, "POST", "/v1/accounts/claude/a/login")[1]
    assert signed(
        application, "POST", f"/v1/logins/{login['id']}/code", {"code": "bad\ncode-value"}
    )[0] == 422
    signed(application, "POST", f"/v1/logins/{login['id']}/code", {"code": "wrong-code-value"})
    wait_until(
        lambda: signed(application, "GET", f"/v1/logins/{login['id']}")[1]["status"] == FAILED
    )
    view = signed(application, "GET", f"/v1/logins/{login['id']}")[1]
    assert "wrong-code-value" not in json.dumps(view)
    assert "Invalid code" in view["error"]


@posix_only
def test_claude_login_cancel_stops_the_cli(tmp_path: Path) -> None:
    application = AgentApplication(make_config(tmp_path))
    login = signed(application, "POST", "/v1/accounts/claude/c/login")[1]
    session = application.logins.get(login["id"])
    assert session is not None
    status, view = signed(application, "POST", f"/v1/logins/{login['id']}/cancel")
    assert (status, view["status"]) == (200, CANCELLED)
    assert isinstance(session.handle, ClaudeLogin)
    process = session.handle._process
    wait_until(lambda: process.poll() is not None)


# --- sessions -----------------------------------------------------------------------


class FakeHandle:
    kind = "device_code"
    url = "https://auth.openai.com/codex/device"
    user_code: str | None = "CODE-1234"

    def __init__(self) -> None:
        self.cancelled = False

    def state(self) -> tuple[str, str | None]:
        return (CANCELLED, None) if self.cancelled else (PENDING, None)

    def submit_code(self, code: str) -> None:
        raise AssertionError("not used")

    def cancel(self) -> None:
        self.cancelled = True


def test_login_sessions_expire_and_stop_the_cli() -> None:
    now = [1000.0]
    registry = LoginRegistry(900, clock=lambda: now[0])
    handle = FakeHandle()
    session, created = registry.start("codex", "a", lambda: handle)
    assert created
    assert registry.start("codex", "a", FakeHandle)[0] is session
    now[0] += 901
    assert session.view(now[0])["status"] == EXPIRED
    assert handle.cancelled
    assert registry.active_for("codex", "a") is None


class RecordingAccounts:
    """An Accounts stand-in whose logins finish as soon as the test says so."""

    def __init__(self, email: str) -> None:
        self.email = email
        self.signed_in = False
        self.logouts = 0
        self.finalize: Finalizer | None = None

    def status(self, slot: str) -> dict[str, Any]:
        return {"logged_in": self.signed_in, "email": self.email if self.signed_in else None}

    def start_login(self, slot: str, finalize: Finalizer) -> LoginHandle:
        self.finalize = finalize
        return FakeHandle()

    def logout(self, slot: str) -> None:
        self.logouts += 1
        self.signed_in = False

    def details(self, slot: str) -> dict[str, Any]:
        return {}

    def has_credentials(self, slot: str) -> bool:
        return self.signed_in


def test_finalize_accepts_listed_accounts_and_undoes_others(tmp_path: Path) -> None:
    config = make_config(tmp_path, allowed_emails=frozenset({"owner@x.test"}))
    owner, stranger = RecordingAccounts("Owner@x.test"), RecordingAccounts("stranger@x.test")
    application = AgentApplication(config, claude=owner, codex=stranger)
    owner.signed_in = stranger.signed_in = True
    assert application.finalize("claude", "a") is None
    rejection = application.finalize("codex", "a")
    assert rejection is not None and "stranger@x.test" in rejection
    assert stranger.logouts == 1
    owner.signed_in = False
    assert application.finalize("claude", "b") == NOT_SIGNED_IN


# --- status line --------------------------------------------------------------------


def test_snapshot_keeps_the_last_numbers_and_skips_unchanged_rewrites(tmp_path: Path) -> None:
    payload = {
        "rate_limits": {
            "five_hour": {"used_percentage": 12.5, "resets_at": 1790000000},
            "seven_day": {"used_percentage": 40, "resets_at": 1790400000},
        }
    }
    assert statusline.record_snapshot(tmp_path, payload, now=100)
    assert not statusline.record_snapshot(tmp_path, payload, now=130)
    assert not statusline.record_snapshot(tmp_path, {"model": {}}, now=140)
    assert statusline.record_snapshot(tmp_path, payload, now=200)
    snapshot = statusline.read_snapshot(tmp_path)
    assert snapshot is not None and snapshot["recorded_at"] == 200
    assert [window["window_minutes"] for window in snapshot["windows"]] == [300, 10080]


def test_ensure_statusline_chains_the_owners_command_but_never_itself(tmp_path: Path) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text(
        json.dumps({"theme": "dark", "statusLine": {"type": "command", "command": "mine.sh"}}),
        "utf-8",
    )
    command_b = f"{STATUSLINE_RECORDER} claude-b"
    assert statusline.ensure_statusline(tmp_path, command_b)
    written = json.loads(settings.read_text("utf-8"))
    assert written["theme"] == "dark"
    assert written["statusLine"] == {"type": "command", "command": command_b}
    chain = json.loads((tmp_path / statusline.CHAIN_NAME).read_text("utf-8"))
    assert chain == {"command": "mine.sh"}
    assert not statusline.ensure_statusline(tmp_path, command_b)
    # Settings copied from another slot carry that slot's recorder: replaced, not chained.
    assert statusline.ensure_statusline(tmp_path, f"{STATUSLINE_RECORDER} claude-c")
    chain = json.loads((tmp_path / statusline.CHAIN_NAME).read_text("utf-8"))
    assert chain == {"command": "mine.sh"}
    broken = tmp_path / "broken"
    broken.mkdir()
    (broken / "settings.json").write_text("[1, 2]", "utf-8")
    assert not statusline.ensure_statusline(broken, command_b)


def test_status_line_main_records_for_the_named_slot_and_prints(tmp_path: Path) -> None:
    (tmp_path / "claude-b").mkdir()
    payload = {
        "model": {"display_name": "Opus"},
        "rate_limits": {"five_hour": {"used_percentage": 23.4, "resets_at": 1790000000}},
    }
    output = io.StringIO()
    code = statusline.main(
        ["statusline-record", "claude-b"],
        io.BytesIO(json.dumps(payload).encode()),
        output,
        {},
        state_root=tmp_path,
    )
    assert code == 0
    assert output.getvalue() == "Opus | 5h 23%\n"
    assert statusline.read_snapshot(tmp_path / "claude-b") is not None
    assert statusline.config_dir_for(["x", "../etc"], {}, tmp_path) is None
    assert statusline.config_dir_for(["x"], {"CLAUDE_CONFIG_DIR": "/c"}, tmp_path) == Path("/c")


def test_status_line_main_runs_the_chained_command(tmp_path: Path) -> None:
    slot = tmp_path / "claude-a"
    slot.mkdir()
    command = f'"{sys.executable}" -c "import sys; sys.stdout.write(sys.stdin.read()[:5])"'
    (slot / statusline.CHAIN_NAME).write_text(json.dumps({"command": command}), "utf-8")
    output = io.StringIO()
    statusline.main(
        ["statusline-record", "claude-a"], io.BytesIO(b"hello world"), output, {}, tmp_path
    )
    assert output.getvalue() == "hello"
    garbage = io.StringIO()
    statusline.main(["statusline-record"], io.BytesIO(b"not json"), garbage, {}, tmp_path)
    assert garbage.getvalue() == "\n"


@posix_only
def test_socket_server_and_host_client_talk(tmp_path: Path) -> None:
    config = make_config(tmp_path)
    application = AgentApplication(config)
    (config.slot_path("codex", "a") / "auth.json").write_text(
        json.dumps({"email": "owner@example.com"}), "utf-8"
    )
    socket_path = str(config.socket_path)
    server = UnixHTTPServer(socket_path, make_handler(application))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        status, answer = client.request(KEY, "GET", "/v1/accounts", socket_path=socket_path)
        assert status == 200
        assert slot_of(answer, "codex", "a")["email"] == "owner@example.com"
        wrong_key = "wrong-key-" * 4
        assert client.request(wrong_key, "GET", "/v1/accounts", socket_path=socket_path)[0] == 401
    finally:
        server.shutdown()
        server.server_close()
    assert client._EMAIL.sub(r"\1***@\2", "owner@example.com") == "ow***@example.com"


def test_host_client_needs_a_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AI_ACCOUNTS_AGENT_HMAC_KEY", raising=False)
    assert client.main(["client", "GET", "/v1/accounts"]) == 2
    assert client.main(["client"]) == 2


def test_signature_helper_matches_the_documented_message_format() -> None:
    body = b"{}"
    digest = hashlib.sha256(body).hexdigest()
    message = f"1\n{'0' * 32}\nPOST\n/v1/x\n{digest}".encode()
    expected = hmac.new(KEY.encode(), message, hashlib.sha256).hexdigest()
    assert signature_for(KEY, "1", "0" * 32, "post", "/v1/x", body) == expected
