"""Tests for the video-tool-token authenticated Flow & Flow Music MCP proxy."""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import Settings
from app.db import get_session
from app.models import AdminAuditLog, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_flow_mcp import router as flow_mcp_router
from app.video_speech import admin_api as speech_api

SECRET = "a" * 48


def _token(*, flow_access: bool = True) -> VideoToolToken:
    return VideoToolToken(
        id=uuid4(),
        name="配對：雲端工作站",
        token_hash="h" * 64,
        token_prefix="mkv_flow12",
        created_by_user_id=uuid4(),
        colab_access=False,
        runpod_access=False,
        flow_access=flow_access,
    )


class FakeSession:
    def __init__(self) -> None:
        self.added: list[Any] = []
        self.commits = 0

    def add(self, item: Any) -> None:
        self.added.append(item)

    async def commit(self) -> None:
        self.commits += 1

    def audits(self) -> list[AdminAuditLog]:
        return [item for item in self.added if isinstance(item, AdminAuditLog)]


def _client(token: VideoToolToken, session: FakeSession) -> TestClient:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(flow_mcp_router.router, prefix="/api/v1")

    async def fake_session() -> Any:
        yield session

    async def fake_token() -> VideoToolToken:
        return token

    app.dependency_overrides[get_session] = fake_session
    app.dependency_overrides[speech_api.video_tool] = fake_token
    return TestClient(app)


def test_flow_mcp_refuses_token_without_flow_access(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(
        flow_mcp_router,
        "get_settings",
        lambda: Settings(
            flow_mcp_gateway_enabled=True,
            flow_mcp_gateway_url="http://127.0.0.1:8792",
            flow_mcp_gateway_secret=SECRET,
        ),
    )
    client = _client(_token(flow_access=False), session)
    res = client.post(
        "/api/v1/video/mcp/flow",
        json={"jsonrpc": "2.0", "id": 1, "method": "ping"},
    )
    assert res.status_code == 403
    assert res.json()["code"] == "video_tool_token_no_flow"


def test_flow_mcp_signs_forwards_and_audits_tool_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession()
    monkeypatch.setattr(
        flow_mcp_router,
        "get_settings",
        lambda: Settings(
            flow_mcp_gateway_enabled=True,
            flow_mcp_gateway_url="http://127.0.0.1:8792",
            flow_mcp_gateway_secret=SECRET,
        ),
    )

    async def fake_rate_limit(*_args: Any, **_kwargs: Any) -> None:
        return None

    monkeypatch.setattr(flow_mcp_router, "enforce_named_rate_limit", fake_rate_limit)

    seen_requests: list[httpx.Request] = []

    def handler(req: httpx.Request) -> httpx.Response:
        seen_requests.append(req)
        ts = req.headers["X-Mokaair-Timestamp"]
        nonce = req.headers["X-Mokaair-Nonce"]
        sig = req.headers["X-Mokaair-Signature"]
        digest = hashlib.sha256(req.content).hexdigest()
        expected = hmac.new(
            SECRET.encode("utf-8"),
            f"{ts}\n{nonce}\n{req.method}\n{req.url.path}\n{digest}".encode(),
            hashlib.sha256,
        ).hexdigest()
        assert sig == expected
        if req.url.path == "/health":
            return httpx.Response(
                200,
                json={"ok": True, "services": ["flow", "flow-music"], "uptimeSec": 12},
            )
        return httpx.Response(
            200,
            json={
                "jsonrpc": "2.0",
                "id": 5,
                "result": {"content": [{"type": "text", "text": "{}"}]},
            },
        )

    transport = httpx.MockTransport(handler)
    real_async_client = httpx.AsyncClient

    def patched_client(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
        kwargs["transport"] = transport
        return real_async_client(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", patched_client)

    client = _client(_token(flow_access=True), session)

    health = client.get("/api/v1/video/mcp/health")
    assert health.status_code == 200
    assert health.json()["ok"] is True
    assert health.json()["services"] == ["flow", "flow-music"]

    body = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {"name": "music_status", "arguments": {"profile": "default"}},
    }
    res = client.post("/api/v1/video/mcp/flow-music", content=json.dumps(body))
    assert res.status_code == 200
    assert res.headers["cache-control"] == "no-store"
    assert res.json()["id"] == 5

    audits = session.audits()
    assert len(audits) == 1
    assert audits[0].action == "video_flow_mcp.tool_call"
    assert audits[0].target == "flow-mcp:flow-music"
    assert flow_mcp_router.MCP_CALLS_PER_HOUR >= 1200
    assert audits[0].metadata_json == {
        "token": "mkv_flow12",
        "service": "flow-music",
        "tool": "music_status",
    }

    write_body = {
        "jsonrpc": "2.0",
        "id": 7,
        "method": "tools/call",
        "params": {
            "name": "flow_write_file",
            "arguments": {
                "slug": "sothatswhy-g790-dehumidifier-winter",
                "relPath": "stills/B38.jpg",
                "contentBase64": "ZmFrZS1pbWFnZS1ieXRlcw==",
            },
        },
    }
    write_res = client.post("/api/v1/video/mcp/flow", content=json.dumps(write_body))
    assert write_res.status_code == 200
    assert len(session.audits()) == 2
    assert session.audits()[1].metadata_json == {
        "token": "mkv_flow12",
        "service": "flow",
        "tool": "flow_write_file",
    }

    bad_method = client.post(
        "/api/v1/video/mcp/flow",
        json={"jsonrpc": "2.0", "id": 6, "method": "admin/shutdown"},
    )
    assert bad_method.status_code == 400
    assert bad_method.json()["code"] == "flow_mcp_method_not_allowed"


def test_flow_mcp_uses_unix_socket_transport_when_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FakeSession()
    settings = Settings(
        flow_mcp_gateway_enabled=True,
        flow_mcp_gateway_socket="/run/mokaair-flow-gateway/gateway.sock",
        flow_mcp_gateway_secret=SECRET,
    )
    assert settings.flow_mcp_gateway_configured is True
    monkeypatch.setattr(flow_mcp_router, "get_settings", lambda: settings)

    captured: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        captured["url"] = str(req.url)
        return httpx.Response(
            200,
            json={"ok": True, "services": ["flow", "flow-music"], "uptimeSec": 3},
        )

    real_async_client = httpx.AsyncClient
    real_transport = httpx.AsyncHTTPTransport

    def patched_transport(*args: Any, **kwargs: Any) -> Any:
        captured["uds"] = kwargs.get("uds")
        return httpx.MockTransport(handler)

    monkeypatch.setattr(httpx, "AsyncHTTPTransport", patched_transport)
    monkeypatch.setattr(httpx, "AsyncClient", real_async_client)
    try:
        client = _client(_token(flow_access=True), session)
        health = client.get("/api/v1/video/mcp/health")
        assert health.status_code == 200
        assert health.json()["ok"] is True
        assert captured["uds"] == "/run/mokaair-flow-gateway/gateway.sock"
        assert captured["url"] == "http://flow-gateway.local/health"
    finally:
        monkeypatch.setattr(httpx, "AsyncHTTPTransport", real_transport)
