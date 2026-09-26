"""The owner's drama requests: what they accept, how they move, who may call what, and the spend
each video shows on the list."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError

from app.auth.service import current_user
from app.db import get_session
from app.models import AdminAuditLog, User, VideoProject, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api
from app.video_automation import requests as service
from app.video_automation import settings as settings_service
from app.video_automation.models import VideoAutomationSettings, VideoDramaRequest
from app.video_automation.schemas import DramaRequestIn, DramaRequestOut
from app.video_media.meter import SlugSpend, spend_by_slug
from app.video_reviews import admin_service as reviews
from app.video_reviews.schemas import ProjectIn, ProjectSummary
from app.video_speech import admin_api as speech_api

NOW = datetime(2026, 9, 26, 6, 0, tzinfo=UTC)


def _row(**changes: Any) -> VideoDramaRequest:
    values: dict[str, Any] = {
        "id": uuid4(),
        "premise": "精衛填海：炎帝最小的女兒在東海溺水，化成一隻鳥。",
        "title": None,
        "source_guide": None,
        "style_preset": "cinematic-3d",
        "target_minutes": 3,
        "note": None,
        "status": "queued",
        "slug": None,
        "created_by_user_id": uuid4(),
        "created_at": NOW,
        "updated_at": NOW,
        "started_at": None,
        "finished_at": None,
        "cancelled_at": None,
    }
    values.update(changes)
    return VideoDramaRequest(**values)


class FakeSession:
    """Just enough of AsyncSession: scalar answers in order, add, commit."""

    def __init__(self, *scalars: Any) -> None:
        self.scalars = list(scalars)
        self.added: list[Any] = []
        self.commits = 0

    async def scalar(self, _statement: Any) -> Any:
        return self.scalars.pop(0)

    def add(self, row: Any) -> None:
        self.added.append(row)

    async def commit(self) -> None:
        self.commits += 1


def _owner() -> User:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    return owner


def _token() -> VideoToolToken:
    return VideoToolToken(id=uuid4(), name="worker", token_hash="h", token_prefix="mkv_w")


def test_a_request_needs_a_premise_and_keeps_to_the_presets_and_lengths() -> None:
    minimal = DramaRequestIn(premise="  夸父逐日  ")
    assert minimal.premise == "夸父逐日"
    assert (minimal.style_preset, minimal.target_minutes, minimal.source_guide) == (
        "cinematic-3d",
        3,
        None,
    )
    adapted = DramaRequestIn(
        premise="把這篇改成三幕的旅途故事",
        source_guide="tokyo-first-trip-guide",
        style_preset="ink-wash",
        target_minutes=4,
        title="第一次去東京",
        note="旁白慢一點",
    )
    assert adapted.source_guide == "tokyo-first-trip-guide"
    for bad in (
        {"premise": ""},
        {"premise": "   "},
        {"premise": "x" * 4001},
        {"premise": "p", "style_preset": "noir"},
        {"premise": "p", "target_minutes": 0},
        {"premise": "p", "target_minutes": 9},
        {"premise": "p", "source_guide": "Not A Slug"},
        {"premise": "p", "title": ""},
        {"premise": "p", "unknown": 1},
    ):
        with pytest.raises(ValidationError):
            DramaRequestIn(**bad)


def test_the_view_says_done_once_the_started_video_is_on_youtube() -> None:
    started = _row(status="started", slug="jingwei-fills-the-sea", started_at=NOW)
    assert service.request_view(started).status == "started"
    assert service.request_view(started, "dQw4w9WgXcQ").status == "done"
    assert service.request_view(_row(), "dQw4w9WgXcQ").status == "queued", (
        "only a started request is done by its video"
    )
    out = service.request_view(started)
    assert isinstance(out, DramaRequestOut) and out.slug == "jingwei-fills-the-sea"


@pytest.mark.asyncio
async def test_creating_a_request_queues_it_and_writes_an_audit_entry() -> None:
    session = FakeSession()
    owner = _owner()
    out = await service.create_request(
        session,  # type: ignore[arg-type]
        owner,
        DramaRequestIn(premise="精衛填海", source_guide="shanhaijing-birds", target_minutes=2),
    )
    assert out.status == "queued" and out.created_by_user_id == owner.id and out.slug is None
    assert isinstance(out.id, UUID)
    row, audit = session.added
    assert isinstance(row, VideoDramaRequest) and row.id == out.id and row.status == "queued"
    assert isinstance(audit, AdminAuditLog)
    assert audit.action == "video_drama_request_created"
    assert audit.target == f"video-drama-request:{out.id}"
    assert audit.metadata_json == {
        "style_preset": "cinematic-3d",
        "target_minutes": 2,
        "source_guide": "shanhaijing-birds",
    }
    assert session.commits == 1


@pytest.mark.asyncio
async def test_only_a_queued_request_can_be_cancelled_or_started() -> None:
    owner = _owner()
    queued = _row()
    session = FakeSession(queued)
    cancelled = await service.cancel_request(session, owner, queued.id)  # type: ignore[arg-type]
    assert cancelled.status == "cancelled" and queued.cancelled_at is not None
    assert session.added[0].action == "video_drama_request_cancelled"

    started = _row(status="started", slug="v")
    with pytest.raises(service.RequestRefused) as refused:
        await service.cancel_request(FakeSession(started), owner, started.id)  # type: ignore[arg-type]
    assert (refused.value.status, refused.value.code) == (409, "video_drama_request_not_queued")
    with pytest.raises(service.RequestRefused) as missing:
        await service.cancel_request(FakeSession(None), owner, uuid4())  # type: ignore[arg-type]
    assert missing.value.status == 404

    token = _token()
    fresh = _row()
    # The slug lookup finds no other request, so the claim goes through.
    claimed = await service.start_request(
        FakeSession(fresh, None),  # type: ignore[arg-type]
        token,
        fresh.id,
        "jingwei-fills-the-sea",
    )
    assert claimed.status == "started" and claimed.slug == "jingwei-fills-the-sea"
    assert fresh.started_by_token_id == token.id and fresh.started_at is not None
    with pytest.raises(service.RequestRefused) as again:
        await service.start_request(FakeSession(fresh), token, fresh.id, "another")  # type: ignore[arg-type]
    assert again.value.code == "video_drama_request_not_queued"
    other = _row()
    with pytest.raises(service.RequestRefused) as taken:
        await service.start_request(
            FakeSession(other, uuid4()),  # type: ignore[arg-type]
            token,
            other.id,
            "jingwei-fills-the-sea",
        )
    assert taken.value.code == "video_drama_request_slug_taken"
    assert other.status == "queued", "a refused claim changes nothing"

    done = await service.finish_request(FakeSession(fresh), fresh.id)  # type: ignore[arg-type]
    assert done.status == "done" and fresh.finished_at is not None
    with pytest.raises(service.RequestRefused) as not_started:
        await service.finish_request(FakeSession(_row()), uuid4())  # type: ignore[arg-type]
    assert not_started.value.code == "video_drama_request_not_started"


@pytest.mark.asyncio
async def test_next_is_the_oldest_queued_request_or_none() -> None:
    oldest = _row()
    assert (await service.next_request(FakeSession(oldest))).id == oldest.id  # type: ignore[arg-type, union-attr]
    assert await service.next_request(FakeSession(None)) is None  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_listing_joins_each_request_with_its_video() -> None:
    started = _row(status="started", slug="v")
    rows = MagicMock()
    rows.all.return_value = [(started, "dQw4w9WgXcQ"), (_row(), None)]
    session = AsyncMock()
    session.execute = AsyncMock(return_value=rows)
    listed = await service.list_requests(session)
    assert [item.status for item in listed] == ["done", "queued"]
    statement = str(session.execute.await_args.args[0]).lower()
    assert "video_projects" in statement and "desc" in statement
    await service.list_requests(session, active_only=True)
    active = str(session.execute.await_args.args[0]).lower()
    assert "asc" in active and "status" in active


def _app(user: User | None = None, token: VideoToolToken | None = None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.tool_router, prefix="/api/v1")
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    if user is not None:
        app.dependency_overrides[current_user] = lambda: user
    if token is not None:
        app.dependency_overrides[speech_api.video_tool] = lambda: token
    return app


ADMIN = "/api/v1/admin/video-automation/drama-requests"
TOOL = "/api/v1/video/automation/drama-requests"


@pytest.mark.asyncio
async def test_a_viewer_reads_the_queue_and_only_a_content_manager_files_or_cancels(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    listed = AsyncMock(return_value=[service.request_view(_row())])
    create = AsyncMock()
    cancel = AsyncMock()
    monkeypatch.setattr(service, "list_requests", listed)
    monkeypatch.setattr(service, "create_request", create)
    monkeypatch.setattr(service, "cancel_request", cancel)
    async with AsyncClient(
        transport=ASGITransport(app=_app(viewer)), base_url="http://t"
    ) as client:
        read = await client.get(ADMIN)
        refused = await client.post(ADMIN, json={"premise": "精衛填海"})
        not_cancelled = await client.delete(f"{ADMIN}/{uuid4()}")
        nobody = await client.get(TOOL)
    assert read.status_code == 200 and read.json()["requests"][0]["status"] == "queued"
    assert refused.status_code == 403 and not_cancelled.status_code == 403
    assert nobody.status_code == 401, "the worker's routes need a video tool token"
    create.assert_not_awaited()
    cancel.assert_not_awaited()


@pytest.mark.asyncio
async def test_the_owner_files_a_request_only_while_the_drama_route_is_on(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = _owner()
    settings_row = AsyncMock(return_value=VideoAutomationSettings(id=1, drama_enabled=False))
    monkeypatch.setattr(settings_service, "settings_row", settings_row)
    create = AsyncMock(return_value=service.request_view(_row(created_by_user_id=owner.id)))
    monkeypatch.setattr(service, "create_request", create)
    cancel = AsyncMock(
        side_effect=service.RequestRefused(
            409, "video_drama_request_not_queued", "工人已經開始做這支了"
        )
    )
    monkeypatch.setattr(service, "cancel_request", cancel)
    async with AsyncClient(transport=ASGITransport(app=_app(owner)), base_url="http://t") as client:
        off = await client.post(ADMIN, json={"premise": "精衛填海"})
        settings_row.return_value = VideoAutomationSettings(id=1, drama_enabled=True)
        filed = await client.post(
            ADMIN, json={"premise": "精衛填海", "style_preset": "ink-wash", "target_minutes": 2}
        )
        bad = await client.post(ADMIN, json={"premise": "p", "target_minutes": 20})
        too_late = await client.delete(f"{ADMIN}/{uuid4()}")
    assert off.status_code == 409 and off.json()["code"] == "video_drama_disabled"
    create.assert_awaited_once()
    assert filed.status_code == 201, filed.text
    assert filed.json()["status"] == "queued"
    payload = create.await_args.args[2]
    assert (payload.style_preset, payload.target_minutes) == ("ink-wash", 2)
    assert bad.status_code == 422
    assert too_late.status_code == 409
    assert too_late.json()["code"] == "video_drama_request_not_queued"


@pytest.mark.asyncio
async def test_the_worker_takes_the_next_request_starts_it_and_reports_it_done(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    token = _token()
    row = _row()
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(service, "next_request", AsyncMock(return_value=service.request_view(row)))
    listed = AsyncMock(return_value=[service.request_view(row)])
    monkeypatch.setattr(service, "list_requests", listed)
    started = _row(id=row.id, status="started", slug="jingwei-fills-the-sea", started_at=NOW)
    start = AsyncMock(return_value=service.request_view(started))
    monkeypatch.setattr(service, "start_request", start)
    finish = AsyncMock(
        side_effect=service.RequestRefused(
            409, "video_drama_request_not_started", "這個請求還沒開始做"
        )
    )
    monkeypatch.setattr(service, "finish_request", finish)
    async with AsyncClient(
        transport=ASGITransport(app=_app(token=token)), base_url="http://t"
    ) as client:
        queue = await client.get(TOOL)
        nxt = await client.get(f"{TOOL}/next")
        claimed = await client.post(
            f"{TOOL}/{row.id}/start", json={"slug": "jingwei-fills-the-sea"}
        )
        bad_slug = await client.post(f"{TOOL}/{row.id}/start", json={"slug": "Bad Slug"})
        not_done = await client.post(f"{TOOL}/{row.id}/done")
    assert queue.status_code == 200 and queue.json()["requests"][0]["id"] == str(row.id)
    assert listed.await_args.kwargs == {"active_only": True}
    assert nxt.status_code == 200 and nxt.json()["request"]["premise"] == row.premise
    assert claimed.status_code == 200 and claimed.json()["slug"] == "jingwei-fills-the-sea"
    assert start.await_args.args[1] is token and start.await_args.args[3] == "jingwei-fills-the-sea"
    assert bad_slug.status_code == 422
    assert not_done.status_code == 409
    assert not_done.json()["code"] == "video_drama_request_not_started"


@pytest.mark.asyncio
async def test_a_video_on_the_list_shows_its_format_and_media_spend() -> None:
    rows = MagicMock()
    rows.all.return_value = [("jingwei", Decimal("12.3456"), 96), ("other", 0, 0)]
    session = AsyncMock()
    session.execute = AsyncMock(return_value=rows)
    spend = await spend_by_slug(session, ["jingwei", "other", "none"])
    assert spend == {"jingwei": SlugSpend(usd=12.3456, clip_seconds=96), "other": SlugSpend(0.0, 0)}
    assert await spend_by_slug(session, []) == {}

    drama = VideoProject(
        id=uuid4(),
        slug="jingwei",
        title="精衛填海",
        format="drama",
        stage="clips",
        checklist=[],
        last_synced_at=NOW,
    )
    summary = ProjectSummary(**reviews._summary(drama, 1, spend["jingwei"]))
    assert (summary.format, summary.media_usd, summary.clip_seconds) == ("drama", 12.3456, 96)
    older = VideoProject(
        id=uuid4(), slug="older", title="t", stage="brief", checklist=[], last_synced_at=NOW
    )
    plain = ProjectSummary(**reviews._summary(older, 0))
    assert (plain.format, plain.media_usd, plain.clip_seconds) == ("slides", 0.0, 0)

    # The tool reports the format; an older tool leaves it out and the stored one stays.
    assert ProjectIn(title="t", stage="brief").format is None
    assert ProjectIn(title="t", stage="brief", format="drama").format == "drama"
    with pytest.raises(ValidationError):
        ProjectIn(title="t", stage="brief", format="opera")
