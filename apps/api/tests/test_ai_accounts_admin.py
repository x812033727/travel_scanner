"""The /admin/ai-accounts routes: owner only, relayed to the host agent, audited once."""

import hashlib
import hmac
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from uuid import uuid4

import httpx
import pytest
from httpx import ASGITransport, AsyncClient

import app.admin_ai_accounts.router as router_module
from app.admin_ai_accounts.agent import AiAccountsAgentClient
from app.auth.service import current_user
from app.config import get_settings
from app.db import get_session
from app.main import app
from app.models import AdminAuditLog, User

KEY = "ai-accounts-key-with-at-least-32-chars"
BASE = "/api/v1/admin/ai-accounts"
LOGIN_ID = "0123456789abcdef0123456789abcdef"


def slot(tool: str, letter: str, **values: Any) -> dict[str, Any]:
    return {
        "tool": tool,
        "slot": letter,
        "is_default": letter == "a",
        "logged_in": False,
        "auth_method": None,
        "email": None,
        "organization": None,
        "plan": None,
        "email_allowed": None,
        "usage": None,
        "usage_error": None,
        "recorder_installed": None,
        "checked_at": 1790000000,
        "error": None,
        "login": None,
        **values,
    }


def login(status: str = "pending", **values: Any) -> dict[str, Any]:
    return {
        "id": LOGIN_ID,
        "tool": "codex",
        "slot": "b",
        "kind": "device_code",
        "status": status,
        "url": "https://auth.openai.com/codex/device" if status == "pending" else None,
        "user_code": "ABCD-EFGH" if status == "pending" else None,
        "error": None,
        "expires_at": 1790000900,
        **values,
    }


class AuditSession:
    """Just enough of AsyncSession for the audit rows."""

    def __init__(self) -> None:
        self.added: list[Any] = []
        self.commits = 0
        self.existing: Any = None

    async def scalar(self, statement: Any) -> Any:
        return self.existing

    def add(self, row: Any) -> None:
        self.added.append(row)

    async def commit(self) -> None:
        self.commits += 1

    def audits(self) -> list[AdminAuditLog]:
        return [row for row in self.added if isinstance(row, AdminAuditLog)]


class Agent:
    """Answers signed requests the way the host agent would, and checks the signatures."""

    def __init__(self) -> None:
        self.routes: dict[tuple[str, str], tuple[int, Any]] = {}
        self.calls: list[tuple[str, str, Any]] = []
        self.unreachable = False

    def handler(self, request: httpx.Request) -> httpx.Response:
        if self.unreachable:
            raise httpx.ConnectError("no socket", request=request)
        body = request.content
        path = request.url.raw_path.decode()
        timestamp = request.headers["X-Agent-Timestamp"]
        nonce = request.headers["X-Agent-Nonce"]
        digest = hashlib.sha256(body).hexdigest()
        message = f"{timestamp}\n{nonce}\n{request.method}\n{path}\n{digest}".encode()
        expected = hmac.new(KEY.encode(), message, hashlib.sha256).hexdigest()
        assert request.headers["X-Agent-Signature"] == expected
        self.calls.append((request.method, path, json.loads(body) if body else None))
        status, payload = self.routes.get((request.method, path), (404, {"code": "not_found"}))
        return httpx.Response(status, json=payload)


@pytest.fixture
def ai_app(monkeypatch: pytest.MonkeyPatch) -> Iterator[dict[str, Any]]:
    settings = get_settings()
    monkeypatch.setattr(settings, "admin_emails", "owner@example.com")
    monkeypatch.setattr(settings, "ai_accounts_enabled", True)
    monkeypatch.setattr(settings, "ai_accounts_agent_hmac_key", KEY)
    agent = Agent()
    session = AuditSession()
    state: dict[str, Any] = {"agent": agent, "session": session, "limits": []}

    async def count_limit(namespace: str, identifier: str, **_: Any) -> None:
        state["limits"].append(namespace)

    monkeypatch.setattr(router_module, "enforce_named_rate_limit", count_limit)
    monkeypatch.setattr(
        AiAccountsAgentClient, "_transport", lambda self: httpx.MockTransport(agent.handler)
    )
    previous = app.dependency_overrides.copy()
    state["actor"] = User(id=uuid4(), email="owner@example.com", is_admin=True)
    app.dependency_overrides[current_user] = lambda: state["actor"]
    app.dependency_overrides[get_session] = lambda: session
    yield state
    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous)


def _client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_only_the_owner_reaches_the_page(ai_app: dict[str, Any]) -> None:
    ai_app["actor"] = User(id=uuid4(), email="staff@example.com", is_admin=True)
    async with _client() as client:
        for method, path in (("GET", BASE), ("POST", f"{BASE}/codex/b/login")):
            response = await client.request(method, path)
            assert response.status_code == 403, path
    assert ai_app["agent"].calls == []


@pytest.mark.asyncio
async def test_disabled_page_reports_it_and_refuses_changes(
    ai_app: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(get_settings(), "ai_accounts_enabled", False)
    async with _client() as client:
        overview = await client.get(BASE)
        assert overview.status_code == 200
        assert overview.json()["enabled"] is False
        started = await client.post(f"{BASE}/codex/b/login")
        assert (started.status_code, started.json()["code"]) == (503, "ai_accounts_disabled")
    assert ai_app["agent"].calls == []


@pytest.mark.asyncio
async def test_overview_relays_the_agent_and_drops_fields_it_does_not_know(
    ai_app: dict[str, Any],
) -> None:
    usage = {
        "source": "live",
        "windows": [{"window_minutes": 10080, "used_percent": 100, "resets_at": 1790451041}],
    }
    codex_a = slot(
        "codex", "a", logged_in=True, email="owner@example.com", plan="pro", usage=usage,
        access_token="must-not-leak",
    )
    ai_app["agent"].routes[("GET", "/v1/accounts?fresh=1")] = (
        200,
        {
            "slots": [codex_a, slot("codex", "b")],
            "defaults": {"claude": "a", "codex": "a"},
            "allowlist_configured": True,
            "refresh_token": "must-not-leak",
        },
    )
    async with _client() as client:
        response = await client.get(BASE, params={"fresh": "true"})
    assert response.status_code == 200
    body = response.json()
    assert (body["enabled"], body["agent_reachable"], body["allowlist_configured"]) == (
        True,
        True,
        True,
    )
    assert body["slots"][0]["usage"]["windows"][0]["used_percent"] == 100
    assert "must-not-leak" not in response.text


@pytest.mark.asyncio
async def test_unreachable_agent_is_a_state_of_the_page(ai_app: dict[str, Any]) -> None:
    ai_app["agent"].unreachable = True
    async with _client() as client:
        response = await client.get(BASE)
    body = response.json()
    assert response.status_code == 200
    assert (body["enabled"], body["agent_reachable"]) == (True, False)
    assert "mokaair-ai-accounts" in body["agent_error"]


@pytest.mark.asyncio
async def test_login_is_audited_when_it_starts_and_once_when_it_ends(
    ai_app: dict[str, Any],
) -> None:
    agent, session = ai_app["agent"], ai_app["session"]
    agent.routes[("POST", "/v1/accounts/codex/b/login")] = (201, login())
    agent.routes[("GET", f"/v1/logins/{LOGIN_ID}")] = (200, login("succeeded"))
    async with _client() as client:
        started = await client.post(f"{BASE}/codex/b/login")
        assert started.status_code == 201
        assert started.json()["user_code"] == "ABCD-EFGH"
        finished = await client.get(f"{BASE}/logins/{LOGIN_ID}")
        assert finished.json()["status"] == "succeeded"
        session.existing = uuid4()  # The first poll's row is there now.
        await client.get(f"{BASE}/logins/{LOGIN_ID}")
    actions = [(row.action, row.target) for row in session.audits()]
    assert actions == [
        ("ai_account.login_started", f"ai-login:{LOGIN_ID}"),
        ("ai_account.login_succeeded", f"ai-login:{LOGIN_ID}"),
    ]
    assert ai_app["limits"] == ["ai-account-login"]


@pytest.mark.asyncio
async def test_pasted_code_is_trimmed_forwarded_and_never_recorded(
    ai_app: dict[str, Any],
) -> None:
    agent, session = ai_app["agent"], ai_app["session"]
    code = "AbC_-123.~#state-Part"
    agent.routes[("POST", f"/v1/logins/{LOGIN_ID}/code")] = (
        202,
        login("verifying", tool="claude", kind="paste_code"),
    )
    async with _client() as client:
        response = await client.post(f"{BASE}/logins/{LOGIN_ID}/code", json={"code": f"  {code} "})
        assert response.status_code == 202
        rejected = await client.post(
            f"{BASE}/logins/{LOGIN_ID}/code", json={"code": "abc def\r\nghij"}
        )
        assert rejected.status_code == 422
    assert agent.calls == [("POST", f"/v1/logins/{LOGIN_ID}/code", {"code": code})]
    assert all(code not in json.dumps(row.metadata_json) for row in session.audits())
    assert session.audits() == []


@pytest.mark.asyncio
async def test_antigravity_logins_take_a_google_code_and_labelled_windows(
    ai_app: dict[str, Any],
) -> None:
    agent = ai_app["agent"]
    google = "https://accounts.google.com/o/oauth2/auth?client_id=x"
    agent.routes[("POST", "/v1/accounts/agy/a/login")] = (
        201,
        login(tool="agy", slot="a", kind="paste_code", url=google, user_code=None),
    )
    agent.routes[("POST", f"/v1/logins/{LOGIN_ID}/code")] = (
        202,
        login("verifying", tool="agy", slot="a", kind="paste_code"),
    )
    usage = {
        "source": "snapshot",
        "recorded_at": 1790000000,
        "windows": [{"label": "Gemini Models", "window_minutes": 300, "used_percent": 20}],
    }
    agent.routes[("GET", "/v1/accounts")] = (
        200,
        {
            "slots": [slot("agy", "a", logged_in=True, auth_method="google", usage=usage)],
            "defaults": {"claude": "a", "codex": "a", "agy": "a"},
            "allowlist_configured": True,
        },
    )
    async with _client() as client:
        started = await client.post(f"{BASE}/agy/a/login")
        assert (started.status_code, started.json()["url"]) == (201, google)
        code = await client.post(
            f"{BASE}/logins/{LOGIN_ID}/code", json={"code": " 4/0AVGzR1Bq-example_code "}
        )
        assert code.status_code == 202
        overview = (await client.get(BASE)).json()
    assert agent.calls[1] == (
        "POST",
        f"/v1/logins/{LOGIN_ID}/code",
        {"code": "4/0AVGzR1Bq-example_code"},
    )
    assert overview["defaults"]["agy"] == "a"
    assert overview["slots"][0]["usage"]["windows"][0]["label"] == "Gemini Models"


@pytest.mark.asyncio
async def test_agent_refusals_keep_their_status_and_code(ai_app: dict[str, Any]) -> None:
    ai_app["agent"].routes[("POST", f"/v1/logins/{LOGIN_ID}/code")] = (
        409,
        {"code": "login_code_not_expected", "detail": "this login takes no code"},
    )
    async with _client() as client:
        response = await client.post(
            f"{BASE}/logins/{LOGIN_ID}/code", json={"code": "abcdefghijk"}
        )
    assert response.status_code == 409
    assert response.json()["code"] == "login_code_not_expected"


@pytest.mark.asyncio
async def test_paths_outside_the_fixed_set_never_reach_the_agent(ai_app: dict[str, Any]) -> None:
    async with _client() as client:
        assert (await client.post(f"{BASE}/codex/f/login")).status_code == 422
        assert (await client.post(f"{BASE}/gemini/a/login")).status_code == 422
        assert (await client.get(f"{BASE}/logins/not-an-id")).status_code == 422
        assert (
            await client.put(f"{BASE}/defaults/claude", json={"slot": "z"})
        ).status_code == 422
    assert ai_app["agent"].calls == []


@pytest.mark.asyncio
async def test_default_change_and_logout_are_audited(ai_app: dict[str, Any]) -> None:
    agent, session = ai_app["agent"], ai_app["session"]
    agent.routes[("PUT", "/v1/defaults/claude")] = (
        200,
        {"defaults": {"claude": "c", "codex": "a"}},
    )
    agent.routes[("POST", "/v1/accounts/claude/b/logout")] = (
        200,
        {"tool": "claude", "slot": "b", "logged_in": False},
    )
    async with _client() as client:
        changed = await client.put(f"{BASE}/defaults/claude", json={"slot": "c"})
        assert changed.json() == {"defaults": {"claude": "c", "codex": "a"}}
        signed_out = await client.post(f"{BASE}/claude/b/logout")
        assert signed_out.json()["logged_in"] is False
    assert [row.action for row in session.audits()] == [
        "ai_account.default_changed",
        "ai_account.logout",
    ]
    assert agent.calls[0] == ("PUT", "/v1/defaults/claude", {"slot": "c"})


def test_compose_mounts_the_socket_the_settings_expect() -> None:
    repository = Path(__file__).resolve().parents[3]
    compose = (repository / "docker-compose.prod.yml").read_text(encoding="utf-8")
    socket_dir = Path(get_settings().ai_accounts_agent_socket).parent.as_posix()
    assert f"{socket_dir}:{socket_dir}:ro" in compose


def test_the_workers_that_run_claude_reach_the_agent_and_nothing_else_on_the_host() -> None:
    repository = Path(__file__).resolve().parents[3]
    compose = (repository / "docker-compose.prod.yml").read_text(encoding="utf-8")
    socket_dir = Path(get_settings().ai_accounts_agent_socket).parent.as_posix()
    for service in ("worker", "news-worker"):
        block = compose.split(f"\n  {service}:\n", 1)[1].split("\n\n", 1)[0]
        assert f"{socket_dir}:{socket_dir}:ro" in block, service
        assert "group_add:" in block, service
        assert "travel-scanner-deployer" not in block, f"{service} must not reach the deployer"
