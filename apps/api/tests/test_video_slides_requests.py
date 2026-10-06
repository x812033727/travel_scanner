"""The owner's requests for a slides video of a chosen site article: what they accept, how they
move, what the page and the worker read of them, and who may call what."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy.dialects import postgresql

from app.auth.service import current_user
from app.db import get_session
from app.models import AdminAuditLog, User, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api, topics
from app.video_automation import settings as settings_service
from app.video_automation import slides_requests as service
from app.video_automation.models import VideoAutomationSettings, VideoSlidesRequest
from app.video_automation.requests import RequestRefused
from app.video_automation.schemas import SlidesRequestIn, SlidesRequestOut, TopicView
from app.video_speech import admin_api as speech_api

NOW = datetime(2026, 10, 5, 8, 0, tzinfo=UTC)
GUIDE = "ai-freelance-getting-started"
URL = f"https://mokaair.com/zh-TW/life/{GUIDE}"


def _row(**changes: Any) -> VideoSlidesRequest:
    values: dict[str, Any] = {
        "id": uuid4(),
        "source_guide": GUIDE,
        "title": "AI 接案入門",
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
    return VideoSlidesRequest(**values)


def _article(slug: str = GUIDE) -> TopicView:
    return TopicView(
        source="site",
        title="AI 接案入門",
        summary="報價怎麼算",
        url=f"{topics.SITE_URL}/{slug}",
        slug=slug,
        date="2026-10-01",
    )


class FakeSession:
    """Just enough of AsyncSession: scalar answers in order, the statements asked, add, commit.
    ``executed`` keeps each statement run for no answer (the article lock) with how many
    ``scalar`` lookups came before it."""

    def __init__(self, *scalars: Any) -> None:
        self.scalars = list(scalars)
        self.statements: list[Any] = []
        self.executed: list[tuple[int, Any]] = []
        self.added: list[Any] = []
        self.commits = 0

    async def scalar(self, statement: Any) -> Any:
        self.statements.append(statement)
        return self.scalars.pop(0)

    async def execute(self, statement: Any) -> None:
        self.executed.append((len(self.statements), statement))

    def add(self, row: Any) -> None:
        self.added.append(row)

    async def commit(self) -> None:
        self.commits += 1


def _sql(statement: Any) -> str:
    return str(
        statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
    ).lower()


def _owner() -> User:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    return owner


def _token() -> VideoToolToken:
    return VideoToolToken(id=uuid4(), name="worker", token_hash="h", token_prefix="mkv_w")


def test_a_request_names_a_guide_slug_and_an_optional_trimmed_note() -> None:
    plain = SlidesRequestIn(source_guide=GUIDE)
    assert (plain.source_guide, plain.note) == (GUIDE, None)
    noted = SlidesRequestIn(source_guide=GUIDE, note="  只講制度與風險，不給投資建議  ")
    assert noted.note == "只講制度與風險，不給投資建議"
    for bad in (
        {},
        {"source_guide": ""},
        {"source_guide": "a"},
        {"source_guide": "Not A Slug"},
        {"source_guide": f"{GUIDE}-"},
        {"source_guide": "x" * 121},
        {"source_guide": GUIDE, "note": ""},
        {"source_guide": GUIDE, "note": "   "},
        {"source_guide": GUIDE, "note": "x" * 2001},
        {"source_guide": GUIDE, "premise": "a drama field"},
    ):
        with pytest.raises(ValidationError):
            SlidesRequestIn(**bad)


def test_the_view_says_done_on_youtube_and_dropped_once_its_video_is_dropped() -> None:
    started = _row(status="started", slug="slides-1a2b3c4d", started_at=NOW)
    out = service.request_view(started)
    assert isinstance(out, SlidesRequestOut)
    assert (out.status, out.slug, out.url, out.title) == (
        "started",
        "slides-1a2b3c4d",
        URL,
        "AI 接案入門",
    )
    assert service.request_view(started, "dQw4w9WgXcQ").status == "done"
    assert service.request_view(started, None, NOW).status == "dropped"
    assert service.request_view(started, "dQw4w9WgXcQ", NOW).status == "done", (
        "a video already on YouTube answered the request"
    )
    assert service.request_view(_row(), "dQw4w9WgXcQ", NOW).status == "queued", (
        "only a started request is done or dropped by its video"
    )
    assert service.request_view(_row(status="cancelled"), None, NOW).status == "cancelled"
    assert service.request_view(_row(status="done"), None, NOW).status == "done"


@pytest.mark.asyncio
async def test_a_new_request_needs_a_published_life_article_not_queued_or_already_a_video(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = _owner()
    found: dict[str, TopicView | None] = {"article": None}
    asked: list[str] = []

    async def site_article(_session: Any, slug: str) -> TopicView | None:
        asked.append(slug)
        return found["article"]

    monkeypatch.setattr(topics, "site_article", site_article)
    payload = SlidesRequestIn(source_guide=GUIDE, note="結尾照文章加免責說明")

    unpublished = FakeSession()
    with pytest.raises(RequestRefused) as missing:
        await service.create_request(unpublished, owner, payload)  # type: ignore[arg-type]
    assert (missing.value.status, missing.value.code) == (
        422,
        "video_slides_request_article_not_found",
    )
    assert asked == [GUIDE] and unpublished.added == [] and unpublished.commits == 0

    found["article"] = _article()
    queued = FakeSession(uuid4())
    with pytest.raises(RequestRefused) as duplicate:
        await service.create_request(queued, owner, payload)  # type: ignore[arg-type]
    assert (duplicate.value.status, duplicate.value.code) == (409, "video_slides_request_duplicate")
    lookup = _sql(queued.statements[0])
    assert "video_projects" in lookup and "dropped_at is null" in lookup, (
        "a started request whose video was dropped no longer holds the article"
    )
    assert "'queued'" in lookup and "'started'" in lookup
    assert queued.added == [] and queued.commits == 0

    retold = FakeSession(None, "older-ai-freelance-video")
    with pytest.raises(RequestRefused) as used:
        await service.create_request(retold, owner, payload)  # type: ignore[arg-type]
    assert (used.value.status, used.value.code) == (409, "video_slides_request_article_used")
    assert "older-ai-freelance-video" in used.value.detail, "the refusal names the video"
    video_lookup = _sql(retold.statements[1])
    assert "format = 'slides'" in video_lookup and "dropped_at is null" in video_lookup
    assert retold.added == [] and retold.commits == 0

    session = FakeSession(None, None)
    out = await service.create_request(session, owner, payload)  # type: ignore[arg-type]
    assert isinstance(out.id, UUID) and out.status == "queued" and out.slug is None
    assert (out.source_guide, out.title, out.url) == (GUIDE, "AI 接案入門", URL)
    assert out.note == "結尾照文章加免責說明" and out.created_by_user_id == owner.id
    row, audit = session.added
    assert isinstance(row, VideoSlidesRequest) and row.id == out.id and row.status == "queued"
    assert isinstance(audit, AdminAuditLog)
    assert (audit.actor_user_id, audit.action, audit.target) == (
        owner.id,
        "video_slides_request_created",
        f"video-slides-request:{out.id}",
    )
    assert audit.metadata_json == {"source_guide": GUIDE}
    assert session.commits == 1
    assert unpublished.executed == [], "an article the site does not serve locks nothing"


@pytest.mark.asyncio
async def test_two_requests_for_one_article_filed_at_once_take_turns(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def site_article(_session: Any, slug: str) -> TopicView:
        return _article(slug)

    monkeypatch.setattr(topics, "site_article", site_article)

    async def lock_for(guide: str) -> str:
        session = FakeSession(None, None)
        await service.create_request(session, _owner(), SlidesRequestIn(source_guide=guide))  # type: ignore[arg-type]
        [(lookups_before, lock)] = session.executed
        assert lookups_before == 0, "the lock is held before the duplicate check reads anything"
        return _sql(lock)

    first, second, other = (
        await lock_for(GUIDE),
        await lock_for(GUIDE),
        await lock_for("ai-trading-bot-claims"),
    )
    assert "pg_advisory_xact_lock" in first, "held until the insert commits, not released early"
    assert first == second, "the same article takes the same lock, so the second waits"
    assert other != first, "another article does not wait"


@pytest.mark.asyncio
async def test_only_a_queued_request_can_be_cancelled_or_started_and_a_started_one_done() -> None:
    owner = _owner()
    queued = _row()
    session = FakeSession(queued)
    cancelled = await service.cancel_request(session, owner, queued.id)  # type: ignore[arg-type]
    assert cancelled.status == "cancelled" and queued.cancelled_at is not None
    [audit] = session.added
    assert (audit.action, audit.target, audit.metadata_json) == (
        "video_slides_request_cancelled",
        f"video-slides-request:{queued.id}",
        {"source_guide": GUIDE},
    )
    assert "for update" in _sql(session.statements[0]), "the row is locked while it changes"

    started = _row(status="started", slug="v")
    with pytest.raises(RequestRefused) as refused:
        await service.cancel_request(FakeSession(started), owner, started.id)  # type: ignore[arg-type]
    assert (refused.value.status, refused.value.code) == (409, "video_slides_request_not_queued")
    with pytest.raises(RequestRefused) as missing:
        await service.cancel_request(FakeSession(None), owner, uuid4())  # type: ignore[arg-type]
    assert (missing.value.status, missing.value.code) == (404, "video_slides_request_not_found")

    token = _token()
    fresh = _row()
    # The slug lookup finds no other request, so the claim goes through.
    claimed = await service.start_request(
        FakeSession(fresh, None),  # type: ignore[arg-type]
        token,
        fresh.id,
        "slides-1a2b3c4d",
    )
    assert claimed.status == "started" and claimed.slug == "slides-1a2b3c4d"
    assert fresh.started_by_token_id == token.id and fresh.started_at is not None
    # The first answer was lost (a reset, a 502) and the worker sends the same claim again.
    claimed_at = fresh.started_at
    resent = FakeSession(fresh)
    again_ok = await service.start_request(resent, token, fresh.id, "slides-1a2b3c4d")  # type: ignore[arg-type]
    assert (again_ok.status, again_ok.slug, again_ok.id) == ("started", "slides-1a2b3c4d", fresh.id)
    assert fresh.started_at == claimed_at and resent.commits == 0, "the claim is not made twice"
    with pytest.raises(RequestRefused) as again:
        await service.start_request(FakeSession(fresh), token, fresh.id, "another")  # type: ignore[arg-type]
    assert again.value.code == "video_slides_request_not_queued"
    with pytest.raises(RequestRefused) as someone_else:
        await service.start_request(
            FakeSession(fresh),  # type: ignore[arg-type]
            _token(),
            fresh.id,
            "slides-1a2b3c4d",
        )
    assert someone_else.value.code == "video_slides_request_not_queued", (
        "only the token that claimed it gets the claim back"
    )
    other = _row()
    with pytest.raises(RequestRefused) as taken:
        await service.start_request(
            FakeSession(other, uuid4()),  # type: ignore[arg-type]
            token,
            other.id,
            "slides-1a2b3c4d",
        )
    assert (taken.value.status, taken.value.code) == (409, "video_slides_request_slug_taken")
    assert other.status == "queued", "a refused claim changes nothing"
    with pytest.raises(RequestRefused) as gone:
        await service.start_request(FakeSession(None), token, uuid4(), "v")  # type: ignore[arg-type]
    assert gone.value.status == 404

    done = await service.finish_request(FakeSession(fresh), fresh.id)  # type: ignore[arg-type]
    assert done.status == "done" and fresh.finished_at is not None
    with pytest.raises(RequestRefused) as after_done:
        await service.start_request(FakeSession(fresh), token, fresh.id, "slides-1a2b3c4d")  # type: ignore[arg-type]
    assert after_done.value.code == "video_slides_request_not_queued", (
        "a finished request is not started again, even under its own slug"
    )
    for closed in (_row(status="cancelled"), _row(status="cancelled", slug="slides-1a2b3c4d")):
        closed.started_by_token_id = token.id
        with pytest.raises(RequestRefused) as refused_closed:
            await service.start_request(FakeSession(closed), token, closed.id, "slides-1a2b3c4d")  # type: ignore[arg-type]
        assert refused_closed.value.code == "video_slides_request_not_queued"
    with pytest.raises(RequestRefused) as not_started:
        await service.finish_request(FakeSession(_row()), uuid4())  # type: ignore[arg-type]
    assert (not_started.value.status, not_started.value.code) == (
        409,
        "video_slides_request_not_started",
    )


@pytest.mark.asyncio
async def test_next_is_the_oldest_queued_request_whose_article_is_still_published() -> None:
    oldest = _row(note="只講資訊")
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=oldest)
    out = await service.next_request(session)
    assert out is not None and (out.id, out.url, out.note) == (oldest.id, URL, "只講資訊")
    statement = _sql(session.scalar.await_args.args[0])
    assert "status = 'queued'" in statement
    assert "source_guide in (select guide_articles.slug" in statement, (
        "a request whose article was unpublished since does not stall the queue"
    )
    assert "kind = 'life'" in statement and "'zh-tw'" in statement
    assert "published_version = guide_search_entries.revision_version" in statement
    assert "order by video_slides_requests.created_at asc" in statement
    assert await service.next_request(FakeSession(None)) is None  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_listing_joins_each_request_with_what_became_of_its_video() -> None:
    youtube = _row(status="started", slug="a")
    dropped = _row(status="started", slug="b")
    rows = MagicMock()
    rows.all.return_value = [
        (youtube, "dQw4w9WgXcQ", None),
        (dropped, None, NOW),
        (_row(), None, None),
    ]
    session = AsyncMock()
    session.execute = AsyncMock(return_value=rows)
    listed = await service.list_requests(session)
    assert [item.status for item in listed] == ["done", "dropped", "queued"]
    statement = _sql(session.execute.await_args.args[0])
    assert "left outer join video_projects" in statement
    assert "created_at desc" in statement and "limit 100" in statement


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


ADMIN = "/api/v1/admin/video-automation/slides-requests"
TOOL = "/api/v1/video/automation/slides-requests"


@pytest.mark.asyncio
async def test_a_viewer_reads_the_queue_and_only_a_content_manager_files_or_cancels(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    monkeypatch.setattr(
        service, "list_requests", AsyncMock(return_value=[service.request_view(_row())])
    )
    create = AsyncMock()
    cancel = AsyncMock()
    monkeypatch.setattr(service, "create_request", create)
    monkeypatch.setattr(service, "cancel_request", cancel)
    async with AsyncClient(
        transport=ASGITransport(app=_app(viewer)), base_url="http://t"
    ) as client:
        read = await client.get(ADMIN)
        refused = await client.post(ADMIN, json={"source_guide": GUIDE})
        not_cancelled = await client.delete(f"{ADMIN}/{uuid4()}")
        nobody = await client.get(f"{TOOL}/next")
        no_claim = await client.post(f"{TOOL}/{uuid4()}/start", json={"slug": "v"})
    assert read.status_code == 200
    [listed] = read.json()["requests"]
    assert (listed["status"], listed["source_guide"], listed["url"]) == ("queued", GUIDE, URL)
    assert refused.status_code == 403 and not_cancelled.status_code == 403
    assert nobody.status_code == 401 and no_claim.status_code == 401, (
        "the worker's routes need a video tool token"
    )
    create.assert_not_awaited()
    cancel.assert_not_awaited()


@pytest.mark.asyncio
async def test_the_owner_files_a_request_only_while_automation_is_on(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = _owner()
    settings_row = AsyncMock(return_value=VideoAutomationSettings(id=1, enabled=False))
    monkeypatch.setattr(settings_service, "settings_row", settings_row)
    filed_row = _row(created_by_user_id=owner.id, note="不給投資建議")
    create = AsyncMock(
        side_effect=[
            service.request_view(filed_row),
            RequestRefused(409, "video_slides_request_duplicate", "已經在排隊"),
        ]
    )
    monkeypatch.setattr(service, "create_request", create)
    cancel = AsyncMock(
        side_effect=RequestRefused(409, "video_slides_request_not_queued", "工人已經開始做這支了")
    )
    monkeypatch.setattr(service, "cancel_request", cancel)
    async with AsyncClient(transport=ASGITransport(app=_app(owner)), base_url="http://t") as client:
        off = await client.post(ADMIN, json={"source_guide": GUIDE})
        settings_row.return_value = VideoAutomationSettings(id=1, enabled=True)
        filed = await client.post(ADMIN, json={"source_guide": GUIDE, "note": " 不給投資建議 "})
        again = await client.post(ADMIN, json={"source_guide": GUIDE})
        bad_slug = await client.post(ADMIN, json={"source_guide": "Not A Slug"})
        extra = await client.post(ADMIN, json={"source_guide": GUIDE, "style_preset": "anime-2d"})
        too_late = await client.delete(f"{ADMIN}/{uuid4()}")
        not_an_id = await client.delete(f"{ADMIN}/not-a-uuid")
    assert off.status_code == 409 and off.json()["code"] == "video_automation_disabled"
    assert create.await_count == 2, "nothing reaches the service while automation is off"
    assert filed.status_code == 201, filed.text
    assert (filed.json()["status"], filed.json()["url"]) == ("queued", URL)
    first = create.await_args_list[0].args
    assert first[1] is owner and (first[2].source_guide, first[2].note) == (GUIDE, "不給投資建議")
    assert again.status_code == 409 and again.json()["code"] == "video_slides_request_duplicate"
    assert bad_slug.status_code == 422 and extra.status_code == 422
    assert too_late.status_code == 409
    assert too_late.json()["code"] == "video_slides_request_not_queued"
    assert not_an_id.status_code == 422 and cancel.await_count == 1


@pytest.mark.asyncio
async def test_the_worker_takes_the_next_request_starts_it_and_reports_it_done(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    token = _token()
    row = _row(note="只講資訊")
    limits = AsyncMock()
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", limits)
    monkeypatch.setattr(
        service, "next_request", AsyncMock(side_effect=[service.request_view(row), None])
    )
    started = _row(id=row.id, status="started", slug="slides-1a2b3c4d", started_at=NOW)
    start = AsyncMock(return_value=service.request_view(started))
    monkeypatch.setattr(service, "start_request", start)
    finished = _row(id=row.id, status="done", slug="slides-1a2b3c4d", finished_at=NOW)
    finish = AsyncMock(
        side_effect=[
            service.request_view(finished),
            RequestRefused(409, "video_slides_request_not_started", "這個請求還沒開始做"),
        ]
    )
    monkeypatch.setattr(service, "finish_request", finish)
    async with AsyncClient(
        transport=ASGITransport(app=_app(token=token)), base_url="http://t"
    ) as client:
        nxt = await client.get(f"{TOOL}/next")
        empty = await client.get(f"{TOOL}/next")
        claimed = await client.post(f"{TOOL}/{row.id}/start", json={"slug": "slides-1a2b3c4d"})
        bad_slug = await client.post(f"{TOOL}/{row.id}/start", json={"slug": "Bad Slug"})
        done = await client.post(f"{TOOL}/{row.id}/done")
        not_done = await client.post(f"{TOOL}/{uuid4()}/done")
    assert nxt.status_code == 200
    request = nxt.json()["request"]
    assert (request["id"], request["source_guide"], request["url"], request["note"]) == (
        str(row.id),
        GUIDE,
        URL,
        "只講資訊",
    )
    assert empty.status_code == 200 and empty.json() == {"request": None}
    assert claimed.status_code == 200 and claimed.json()["status"] == "started"
    assert start.await_args.args[1] is token and start.await_args.args[2] == row.id
    assert start.await_args.args[3] == "slides-1a2b3c4d"
    assert bad_slug.status_code == 422 and start.await_count == 1
    assert done.status_code == 200 and done.json()["status"] == "done"
    assert not_done.status_code == 409
    assert not_done.json()["code"] == "video_slides_request_not_started"
    assert {call.args[0] for call in limits.await_args_list} == {"video_slides_requests"}
