"""The RunPod pod broker (ticket 2026-10-30-runpod-pod-broker).

RunPod is never called: every exchange goes through ``httpx.MockTransport``. The database is a
small fake that records what the service adds and commits; the queries it would run
(``running``, ``month_spend``) are replaced per test.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import Settings
from app.db import get_session
from app.models import AdminAuditLog, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_runpod import router as runpod_router
from app.video_runpod import service
from app.video_runpod.client import RunPodClient, RunPodError, proxy_url
from app.video_runpod.models import VideoRunpodSession
from app.video_speech import admin_api as speech_api

NOW = datetime(2026, 10, 30, 3, 0, tzinfo=UTC)
DIGEST = "ghcr.io/mokaair/runpod-h3@sha256:" + "b" * 64
READY = Settings(
    runpod_api_key="rp-key",
    runpod_data_center_id="EU-RO-1",
    runpod_network_volume_id="abc123xyz",
    runpod_image=DIGEST,
    runpod_monthly_usd_cap=50,
)


def _token(**changes: Any) -> VideoToolToken:
    return VideoToolToken(
        id=uuid4(),
        name="雲端 session",
        token_hash="h" * 64,
        token_prefix="mkv_abcd",
        created_by_user_id=uuid4(),
        colab_access=changes.get("colab_access", False),
        runpod_access=changes.get("runpod_access", True),
    )


class FakeSession:
    def __init__(self) -> None:
        self.added: list[Any] = []
        self.commits = 0
        self.executed: list[Any] = []

    def add(self, item: Any) -> None:
        self.added.append(item)

    async def commit(self) -> None:
        self.commits += 1

    async def execute(self, statement: Any) -> None:
        self.executed.append(statement)

    def audits(self) -> list[str]:
        return [item.action for item in self.added if isinstance(item, AdminAuditLog)]


def _runpod(seen: list[httpx.Request], *, create_status: int = 201, pod: Any = None):
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        assert request.headers["Authorization"] == "Bearer rp-key"
        assert request.url.host == "rest.runpod.io"
        if request.method == "POST" and request.url.path == "/v1/pods":
            if create_status != 201:
                return httpx.Response(create_status, json={"error": "no stock"})
            return httpx.Response(201, json={"id": "pod123", "costPerHr": 1.03})
        if request.method == "GET":
            if pod is None:
                return httpx.Response(404)
            return httpx.Response(200, json=pod)
        if request.method == "DELETE":
            return httpx.Response(204)
        raise AssertionError(request)

    def factory(settings: Settings) -> RunPodClient:
        return RunPodClient(settings, httpx.AsyncClient(transport=httpx.MockTransport(handler)))

    return factory


def _patch_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    rows: list[VideoRunpodSession] | None = None,
    spent: str = "0",
) -> None:
    monkeypatch.setattr(service, "running", AsyncMock(return_value=rows or []))
    monkeypatch.setattr(service, "month_spend", AsyncMock(return_value=Decimal(spent)))


def _row(**changes: Any) -> VideoRunpodSession:
    values: dict[str, Any] = {
        "id": uuid4(),
        "token_id": None,
        "pod_id": "pod123",
        "label": "e031 pilot",
        "slug": None,
        "gpu": "NVIDIA RTX 6000 Ada Generation",
        "cloud_type": "SECURE",
        "data_center_id": "EU-RO-1",
        "cost_per_hr": Decimal("1.0300"),
        "gate_token_hash": "g" * 64,
        "started_at": NOW - timedelta(minutes=30),
        "last_heartbeat_at": NOW - timedelta(minutes=1),
        "stopped_at": None,
        "stop_reason": None,
        "usd": None,
    }
    values.update(changes)
    return VideoRunpodSession(**values)


async def test_a_start_writes_the_row_first_then_asks_runpod(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_queries(monkeypatch)
    session = FakeSession()
    seen: list[httpx.Request] = []
    row, gate = await service.start_pod(
        session,  # type: ignore[arg-type]
        READY,
        _token(),
        label="e031 pilot",
        slug="zhong-tian-e031",
        client_factory=_runpod(seen),
        now=NOW,
    )
    assert session.executed, "the start takes the advisory lock"
    assert session.commits == 2, "the row is committed before RunPod is asked, then updated"
    assert row.pod_id == "pod123" and row.cost_per_hr == Decimal("1.0300")
    assert len(gate) > 30 and row.gate_token_hash != gate
    body = json.loads(seen[0].content)
    assert body["gpuTypeIds"] == ["NVIDIA RTX 6000 Ada Generation"]
    assert body["dataCenterIds"] == ["EU-RO-1"] and body["networkVolumeId"] == "abc123xyz"
    assert body["imageName"] == DIGEST and body["cloudType"] == "SECURE"
    assert body["ports"] == ["8188/http"] and body["interruptible"] is False
    assert body["env"]["GATE_TOKEN"] == gate
    assert body["name"].startswith(f"mokaair-{row.id.hex[:8]}-")
    assert session.audits() == ["runpod.pod_started"]
    assert service.base_url(row) == "https://pod123-8188.proxy.runpod.net"


@pytest.mark.parametrize(
    ("kwargs", "status", "code"),
    [
        ({"rows": [_row()]}, 409, "runpod_pod_running"),
        ({"spent": "50"}, 409, "runpod_cap_reached"),
    ],
)
async def test_a_start_is_refused_while_a_pod_runs_or_past_the_cap(
    monkeypatch: pytest.MonkeyPatch, kwargs: dict[str, Any], status: int, code: str
) -> None:
    _patch_queries(monkeypatch, **kwargs)
    seen: list[httpx.Request] = []
    with pytest.raises(AppError) as refused:
        await service.start_pod(
            FakeSession(),  # type: ignore[arg-type]
            READY,
            _token(),
            label="x",
            slug=None,
            client_factory=_runpod(seen),
            now=NOW,
        )
    assert (refused.value.status, refused.value.code) == (status, code)
    assert seen == [], "RunPod is never asked"


async def test_a_start_needs_the_card_filled_in(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_queries(monkeypatch)
    with pytest.raises(AppError) as refused:
        await service.start_pod(
            FakeSession(),  # type: ignore[arg-type]
            Settings(runpod_api_key="rp-key"),
            _token(),
            label="x",
            slug=None,
        )
    assert refused.value.status == 503 and "映像" in refused.value.detail


async def test_a_failed_create_settles_the_row_as_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_queries(monkeypatch)
    session = FakeSession()
    with pytest.raises(AppError) as refused:
        await service.start_pod(
            session,  # type: ignore[arg-type]
            READY,
            _token(),
            label="x",
            slug=None,
            client_factory=_runpod([], create_status=500),
            now=NOW,
        )
    assert refused.value.code == "runpod_create_failed"
    row = next(item for item in session.added if isinstance(item, VideoRunpodSession))
    assert (row.stop_reason, row.usd) == ("failed", Decimal(0))
    assert session.audits() == ["runpod.pod_failed"]


def test_cost_is_hourly_price_times_time_run() -> None:
    assert service.cost_so_far(_row(), NOW) == Decimal("0.5150")
    assert service.cost_so_far(_row(usd=Decimal("2.0000")), NOW) == Decimal("2.0000")
    assert service.cost_so_far(_row(pod_id=None), NOW) == Decimal(0)


@pytest.mark.parametrize(
    ("changes", "over_cap", "reason"),
    [
        ({}, False, None),
        ({"last_heartbeat_at": NOW - timedelta(minutes=16)}, False, "idle"),
        ({"started_at": NOW - timedelta(hours=4, minutes=1)}, False, "max_hours"),
        ({}, True, "cap"),
        ({"pod_id": None, "started_at": NOW - timedelta(minutes=11)}, False, "failed"),
        ({"pod_id": None, "started_at": NOW - timedelta(minutes=2)}, False, None),
    ],
)
def test_reap_reasons(changes: dict[str, Any], over_cap: bool, reason: str | None) -> None:
    assert service.reap_reason(_row(**changes), READY, NOW, over_cap) == reason


async def test_reap_stops_idle_pods_and_notices_ones_deleted_elsewhere(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    idle = _row(last_heartbeat_at=NOW - timedelta(minutes=20))
    gone = _row(pod_id="pod999")
    _patch_queries(monkeypatch, rows=[idle, gone])
    session = FakeSession()
    seen: list[httpx.Request] = []
    stopped = await service.reap(
        session,  # type: ignore[arg-type]
        READY,
        client_factory=_runpod(seen, pod=None),
        now=NOW,
    )
    assert [row.stop_reason for row in stopped] == ["idle", "gone"]
    assert [(request.method, request.url.path) for request in seen] == [
        ("DELETE", "/v1/pods/pod123"),
        ("GET", "/v1/pods/pod999"),
    ], "a pod RunPod no longer has is not deleted again"
    assert idle.usd == Decimal("0.5150") and idle.stopped_at == NOW
    assert session.audits() == ["runpod.pod_reaped", "runpod.pod_reaped"]


async def test_a_running_pod_is_left_alone(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_queries(monkeypatch, rows=[_row()])
    stopped = await service.reap(
        FakeSession(),  # type: ignore[arg-type]
        READY,
        client_factory=_runpod([], pod={"id": "pod123", "desiredStatus": "RUNNING"}),
        now=NOW,
    )
    assert stopped == []


async def test_stop_is_idempotent() -> None:
    row = _row(stopped_at=NOW, stop_reason="manual", usd=Decimal("1"))
    session = FakeSession()
    assert await service.stop_pod(session, READY, row, reason="manual", actor_id=None) is row  # type: ignore[arg-type]
    assert session.commits == 0


async def test_the_client_reads_runpod_errors() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401)

    client = RunPodClient(READY, httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    with pytest.raises(RunPodError, match="金鑰被拒"):
        await client.create_pod(name="x", env={})
    with pytest.raises(RunPodError, match="金鑰"):
        RunPodClient(Settings())
    assert proxy_url("abc") == "https://abc-8188.proxy.runpod.net"


@pytest.mark.parametrize(
    ("token", "settings", "canvas", "upscale", "recommended"),
    [
        ({"colab_access": True}, READY, "736p", False, "colab"),
        ({"colab_access": True}, READY, "1088p", False, "runpod"),
        ({"colab_access": True}, READY, "736p", True, "runpod"),
        ({"colab_access": True, "runpod_access": False}, READY, "1088p", False, None),
        ({"colab_access": False}, READY, "736p", False, "runpod"),
        ({"colab_access": True}, Settings(), "1088p", False, None),
        (
            {"colab_access": True},
            READY.model_copy(update={"gpu_route_default": "runpod"}),
            "736p",
            False,
            "runpod",
        ),
        (
            {"colab_access": True},
            READY.model_copy(update={"gpu_route_default": "colab"}),
            "1088p",
            False,
            None,
        ),
    ],
)
def test_gpu_routes_recommend_only_what_the_token_may_use(
    token: dict[str, Any],
    settings: Settings,
    canvas: Any,
    upscale: bool,
    recommended: str | None,
) -> None:
    routes = service.gpu_routes(
        settings,
        _token(**token),
        canvas=canvas,
        upscale=upscale,
        month_usd=Decimal(0),
        pod_running=False,
    )
    assert routes.recommended == recommended
    allowed = {item.route: item.allowed for item in routes.routes}
    assert allowed == {
        "colab": token.get("colab_access", False),
        "runpod": token.get("runpod_access", True),
    }


def test_gpu_routes_say_why_runpod_is_not_ready() -> None:
    routes = service.gpu_routes(
        READY,
        _token(),
        canvas="1088p",
        upscale=False,
        month_usd=Decimal(50),
        pod_running=False,
    )
    assert routes.recommended is None and "上限" in routes.reason


def _app(token: VideoToolToken) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(runpod_router.tool_router, prefix="/api/v1")
    app.include_router(runpod_router.routes_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[speech_api.video_tool] = lambda: token
    return app


def test_a_token_without_runpod_access_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(runpod_router, "enforce_named_rate_limit", AsyncMock())
    client = TestClient(_app(_token(runpod_access=False)))
    response = client.post("/api/v1/video/runpod/pods", json={"label": "x"})
    assert response.status_code == 403
    assert response.json()["code"] == "video_tool_token_no_runpod"


def test_the_routes_endpoint_answers_without_storing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(runpod_router, "load_runtime_settings", AsyncMock(return_value=READY))
    _patch_queries(monkeypatch)
    client = TestClient(_app(_token(colab_access=True)))
    response = client.get("/api/v1/video/gpu-routes", params={"canvas": "1088p"})
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.json()["recommended"] == "runpod"
