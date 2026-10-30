"""The daily AI and tech news brief (app/video_automation/daily_briefs.py): when a day is filed
and from which articles, when it is skipped or goes stale, how the worker starts and finishes
it, its settings, its outline pick, and the two steps in which the server gives its video
languages (app/video_reviews/admin_service.py _decide_daily_brief_locales). The rows live in
an in-memory SQLite database; the routes are exercised with the service mocked, as the slides
requests' are."""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, date, datetime, timedelta
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.db import Base, get_session
from app.guides.models import (
    GuideArticle,
    GuideArticleLocale,
    GuideArticleTopic,
    GuideSearchEntry,
    GuideTopic,
)
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api
from app.video_automation import daily_briefs as service
from app.video_automation import settings as settings_service
from app.video_automation.models import (
    DEFAULT_DAILY_BRIEF_LOCALES,
    VideoAutomationSettings,
    VideoDailyBriefRequest,
)
from app.video_automation.requests import RequestRefused
from app.video_automation.schemas import (
    CAPTION_LOCALES,
    DailyBriefRequestOut,
    DailyBriefSettings,
    DailyBriefStory,
    SettingsSave,
    SettingsWrite,
)
from app.video_reviews import admin_service
from app.video_reviews.schemas import DUB_LOCALES
from app.video_speech import admin_api as speech_api
from app.video_youtube import sync as youtube_sync

TABLES = (
    VideoToolToken,
    VideoProject,
    VideoReview,
    VideoAutomationSettings,
    VideoDailyBriefRequest,
    AdminAuditLog,
    GuideArticle,
    GuideArticleLocale,
    GuideArticleTopic,
    GuideSearchEntry,
    GuideTopic,
)
NEWS_DAY = date(2026, 10, 28)
SLUG = "daily-ai-20261028"
# 09:00 in Asia/Taipei on 2026-10-29 is 01:00 UTC.
AT_NINE = datetime(2026, 10, 29, 1, 0, tzinfo=UTC)
BEFORE_NINE = AT_NINE - timedelta(minutes=1)


@pytest.fixture
async def db() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: Base.metadata.create_all(
                sync, tables=[model.__table__ for model in TABLES]
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        settings = await settings_service.settings_row(session)
        settings.enabled = True
        settings.daily_brief_enabled = True
        ai = GuideTopic(slug="ai-news", section="life")
        tech = GuideTopic(slug="tech-news", section="life")
        session.add_all([ai, tech, GuideTopic(slug="crypto", section="life")])
        await session.flush()
        session.add(GuideTopic(slug="ai-news-models", section="life", parent_id=ai.id))
        await session.commit()
    try:
        yield factory
    finally:
        await engine.dispose()


async def _article(
    session: AsyncSession,
    slug: str,
    *,
    topic: str = "ai-news",
    news_date: date = NEWS_DAY,
    minute: int = 0,
    published: bool = True,
    kind: str = "life",
) -> None:
    """A zh-TW article as the site serves it once published: the locale's published version
    and the search entry built from that version."""
    article = GuideArticle(slug=slug, kind=kind, news_date=news_date)
    session.add(article)
    await session.flush()
    stamp = datetime(2026, 10, 28, 12, minute, tzinfo=UTC)
    session.add(
        GuideArticleLocale(
            article_id=article.id,
            locale="zh-TW",
            version=1,
            draft_json={},
            published_version=1 if published else None,
            published_at=stamp if published else None,
        )
    )
    if published:
        session.add(
            GuideSearchEntry(
                article_id=article.id,
                locale="zh-TW",
                revision_version=1,
                title=f"標題 {slug}",
                description=f"摘要 {slug}",
                title_norm=slug,
                description_norm=slug,
                headings_norm="",
                aliases_norm="",
                body_text="",
                search_text=slug,
                published_at=stamp,
            )
        )
    topic_id = await session.scalar(select(GuideTopic.id).where(GuideTopic.slug == topic))
    assert topic_id is not None
    session.add(GuideArticleTopic(article_id=article.id, topic_id=topic_id))
    await session.flush()


async def _five_stories(session: AsyncSession) -> None:
    kinds = ("ai-news", "tech-news", "ai-news-models", "ai-news", "tech-news")
    for index, topic in enumerate(kinds):
        await _article(session, f"story-{index}", topic=topic, minute=index)
    await session.commit()


def _token() -> VideoToolToken:
    return VideoToolToken(id=uuid4(), name="worker", token_hash=uuid4().hex, token_prefix="mkv_w")


# --- filing a day --------------------------------------------------------------------------------


async def test_the_day_is_filed_from_the_hour_in_taipei_and_not_before(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        await _five_stories(session)
        # Off-topic, another day, unpublished, or not a lifestyle article: never in the brief.
        await _article(session, "crypto-story", topic="crypto", minute=30)
        await _article(session, "older-story", news_date=NEWS_DAY - timedelta(days=1))
        await _article(session, "draft-story", published=False)
        await _article(session, "intel-story", kind="intel", minute=40)
        await session.commit()
        assert await service.next_request(session, BEFORE_NINE) is None
        assert (await session.scalars(select(VideoDailyBriefRequest))).all() == []
        brief = await service.next_request(session, AT_NINE)
    assert brief is not None
    assert (brief.news_date, brief.slug, brief.status) == (NEWS_DAY, SLUG, "queued")
    # Newest first, the sub-topic of ai-news included.
    assert brief.source_guides == [f"story-{index}" for index in (4, 3, 2, 1, 0)]
    first = brief.stories[0]
    assert (first.slug, first.title, first.description, first.news_date) == (
        "story-4",
        "標題 story-4",
        "摘要 story-4",
        NEWS_DAY,
    )
    assert first.url == "https://mokaair.com/zh-TW/life/story-4"


async def test_yesterday_is_taipei_s_yesterday_whatever_the_utc_date(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        row = await settings_service.settings_row(session)
        row.daily_brief_hour = 0
        await session.commit()
        # 2026-10-28 16:30 UTC is already 00:30 on 2026-10-29 in Taipei.
        await _five_stories(session)
        brief = await service.next_request(session, datetime(2026, 10, 28, 16, 30, tzinfo=UTC))
    assert brief is not None and brief.news_date == NEWS_DAY


async def test_at_most_twelve_stories_are_handed_to_the_writer(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        for index in range(15):
            await _article(session, f"many-{index:02d}", minute=index)
        await session.commit()
        brief = await service.next_request(session, AT_NINE)
    assert brief is not None and len(brief.source_guides) == service.MAX_STORIES
    assert brief.source_guides[0] == "many-14"


async def test_a_day_with_too_few_stories_is_skipped_with_the_reason_once(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        for index in range(3):
            await _article(session, f"few-{index}", minute=index)
        await session.commit()
        assert await service.next_request(session, AT_NINE) is None
        assert await service.next_request(session, AT_NINE + timedelta(hours=2)) is None
        rows = (await session.scalars(select(VideoDailyBriefRequest))).all()
        audits = (
            await session.scalars(
                select(AdminAuditLog).where(AdminAuditLog.action == "video_daily_brief_skipped")
            )
        ).all()
    [row] = rows
    assert (row.status, row.slug, row.news_date) == ("skipped", SLUG, NEWS_DAY)
    assert row.skip_reason is not None and "3" in row.skip_reason and "5" in row.skip_reason
    [audit] = audits
    assert audit.actor_user_id is None and audit.target == f"video-daily-brief:{row.id}"
    assert audit.metadata_json == {"news_date": "2026-10-28", "stories": 3, "min_stories": 5}


async def test_next_files_one_row_a_day_and_keeps_handing_it_out_until_started(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        await _five_stories(session)
        first = await service.next_request(session, AT_NINE)
        again = await service.next_request(session, AT_NINE + timedelta(hours=3))
        # The next morning, before the hour: yesterday's unstarted day is still the one.
        morning = await service.next_request(session, AT_NINE + timedelta(hours=23))
        rows = (await session.scalars(select(VideoDailyBriefRequest))).all()
    assert first is not None and again is not None and morning is not None
    assert first.id == again.id == morning.id and len(rows) == 1


async def test_a_second_row_for_one_day_is_refused_by_the_database(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        for slug in (SLUG, "daily-ai-x"):
            session.add(
                VideoDailyBriefRequest(news_date=NEWS_DAY, slug=slug, source_guides=[])
            )
        with pytest.raises(IntegrityError):
            await session.commit()


async def test_two_lanes_filing_one_day_take_turns_on_postgres() -> None:
    """The advisory lock is what makes the second lane find the first lane's row."""
    session = MagicMock()
    session.get_bind.return_value.dialect.name = "postgresql"
    session.execute = AsyncMock()
    await service._lock_day(session, NEWS_DAY)
    [statement] = [call.args[0] for call in session.execute.await_args_list]
    assert "pg_advisory_xact_lock" in str(statement)
    session.get_bind.return_value.dialect.name = "sqlite"
    await service._lock_day(session, NEWS_DAY)
    assert session.execute.await_count == 1


@pytest.mark.parametrize("switch", ["enabled", "daily_brief_enabled"])
async def test_nothing_is_filed_or_handed_out_while_switched_off(
    db: async_sessionmaker[AsyncSession], switch: str
) -> None:
    async with db() as session:
        await _five_stories(session)
        row = await settings_service.settings_row(session)
        setattr(row, switch, False)
        await session.commit()
        assert await service.next_request(session, AT_NINE) is None
        assert (await session.scalars(select(VideoDailyBriefRequest))).all() == []


async def test_a_queued_day_more_than_two_days_old_is_cancelled_as_stale(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        await _five_stories(session)
        for day in (date(2026, 10, 25), date(2026, 10, 27)):
            session.add(
                VideoDailyBriefRequest(
                    news_date=day, slug=service.slug_for(day), source_guides=[], status="queued"
                )
            )
        await session.commit()
        brief = await service.next_request(session, AT_NINE)
        rows = {
            row.news_date: row for row in (await session.scalars(select(VideoDailyBriefRequest)))
        }
    old = rows[date(2026, 10, 25)]
    assert (old.status, old.skip_reason) == ("cancelled", "stale")
    assert old.cancelled_at is not None
    # The day before yesterday is not stale yet, and the oldest queued day comes first.
    assert brief is not None and brief.news_date == date(2026, 10, 27)
    assert rows[NEWS_DAY].status == "queued"


async def test_a_day_that_is_a_video_already_is_skipped_and_holds_nothing_behind_it(
    db: async_sessionmaker[AsyncSession],
) -> None:
    # The first brief was made by hand under its day's slug before the worker took over: the
    # worker leaves that day alone, so queued it would stand first in line every round.
    made = date(2026, 10, 27)
    async with db() as session:
        await _five_stories(session)
        session.add(VideoProject(slug=service.slug_for(made), title="快報", stage="final"))
        session.add(
            VideoDailyBriefRequest(
                news_date=made, slug=service.slug_for(made), source_guides=[], status="queued"
            )
        )
        await session.commit()
        brief = await service.next_request(session, AT_NINE)
        row = await session.scalar(
            select(VideoDailyBriefRequest).where(VideoDailyBriefRequest.news_date == made)
        )
    assert brief is not None and brief.news_date == NEWS_DAY
    assert row is not None and row.status == "skipped"
    assert row.skip_reason == f"{service.slug_for(made)} 已經是一支影片，這天不再做快報"


# --- starting and finishing ----------------------------------------------------------------------


async def test_the_worker_starts_a_day_under_its_own_slug_once_and_finishes_it(
    db: async_sessionmaker[AsyncSession],
) -> None:
    token, other = _token(), _token()
    async with db() as session:
        session.add_all([token, other])
        await _five_stories(session)
        brief = await service.next_request(session, AT_NINE)
        assert brief is not None
        with pytest.raises(RequestRefused) as early:
            await service.finish_request(session, brief.id)
        assert (early.value.status, early.value.code) == (409, "video_daily_brief_not_started")
        with pytest.raises(RequestRefused) as wrong:
            await service.start_request(session, token, brief.id, "daily-ai-20261027")
        assert (wrong.value.status, wrong.value.code) == (409, "video_daily_brief_slug_mismatch")
        started = await service.start_request(session, token, brief.id, SLUG)
        assert started.status == "started" and started.started_at is not None
        # The same claim again (a lost answer) is answered as the first.
        assert (await service.start_request(session, token, brief.id, SLUG)).status == "started"
        with pytest.raises(RequestRefused) as taken:
            await service.start_request(session, other, brief.id, SLUG)
        assert (taken.value.status, taken.value.code) == (409, "video_daily_brief_not_queued")
        # Started, it is no longer handed out.
        assert await service.next_request(session, AT_NINE + timedelta(hours=1)) is None
        done = await service.finish_request(session, brief.id)
        assert done.status == "done" and done.finished_at is not None
        assert (await service.finish_request(session, brief.id)).status == "done"
        with pytest.raises(RequestRefused) as missing:
            await service.start_request(session, token, uuid4(), SLUG)
        assert (missing.value.status, missing.value.code) == (404, "video_daily_brief_not_found")


async def test_the_list_is_newest_first_with_what_became_of_each_video(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        for offset, status in enumerate(("started", "started", "skipped")):
            day = NEWS_DAY - timedelta(days=offset)
            session.add(
                VideoDailyBriefRequest(
                    news_date=day, slug=service.slug_for(day), source_guides=[], status=status
                )
            )
        session.add(
            VideoProject(slug=SLUG, title="快報", stage="on YouTube", youtube_video_id="a" * 11)
        )
        session.add(
            VideoProject(
                slug="daily-ai-20261027",
                title="快報",
                stage="final",
                dropped_at=datetime(2026, 10, 28, tzinfo=UTC),
            )
        )
        await session.commit()
        listed = await service.list_requests(session)
    assert [(row.news_date.day, row.status) for row in listed] == [
        (28, "done"),
        (27, "dropped"),
        (26, "skipped"),
    ]


# --- the routes ----------------------------------------------------------------------------------


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


ADMIN = "/api/v1/admin/video-automation/daily-briefs"
TOOL = "/api/v1/video/automation/daily-briefs"


def _view(**changes: Any) -> Any:
    row = VideoDailyBriefRequest(
        id=uuid4(),
        news_date=NEWS_DAY,
        slug=SLUG,
        source_guides=["story-1"],
        status="queued",
        created_at=AT_NINE,
        updated_at=AT_NINE,
    )
    for key, value in changes.items():
        setattr(row, key, value)
    return DailyBriefRequestOut(
        id=row.id,
        news_date=row.news_date,
        slug=row.slug,
        status=changes.get("status", "queued"),
        skip_reason=row.skip_reason,
        source_guides=list(row.source_guides),
        stories=[
            DailyBriefStory(
                slug="story-1",
                title="標題",
                description="摘要",
                url="https://mokaair.com/zh-TW/life/story-1",
                news_date=NEWS_DAY,
            )
        ],
        created_at=AT_NINE,
        started_at=None,
        finished_at=None,
        cancelled_at=None,
    )


async def test_a_viewer_reads_the_days_and_the_worker_routes_need_a_tool_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    monkeypatch.setattr(service, "list_requests", AsyncMock(return_value=[_view()]))
    start = AsyncMock()
    monkeypatch.setattr(service, "start_request", start)
    async with AsyncClient(transport=ASGITransport(app=_app(viewer)), base_url="http://t") as c:
        read = await c.get(ADMIN)
        nobody = await c.get(f"{TOOL}/next")
        no_claim = await c.post(f"{TOOL}/{uuid4()}/start", json={"slug": SLUG})
        no_done = await c.post(f"{TOOL}/{uuid4()}/done")
    assert read.status_code == 200
    [listed] = read.json()["requests"]
    assert (listed["slug"], listed["status"], listed["news_date"]) == (SLUG, "queued", "2026-10-28")
    assert listed["stories"][0]["url"] == "https://mokaair.com/zh-TW/life/story-1"
    assert {nobody.status_code, no_claim.status_code, no_done.status_code} == {401}
    start.assert_not_awaited()


async def test_the_worker_takes_the_next_day_starts_it_and_reports_it_done(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    token = _token()
    view = _view()
    limits = AsyncMock()
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", limits)
    monkeypatch.setattr(service, "next_request", AsyncMock(side_effect=[view, None]))
    start = AsyncMock(
        side_effect=[
            _view(id=view.id, status="started"),
            RequestRefused(409, "video_daily_brief_slug_mismatch", "只能用 daily-ai-20261028"),
        ]
    )
    monkeypatch.setattr(service, "start_request", start)
    finish = AsyncMock(
        side_effect=[
            _view(id=view.id, status="done"),
            RequestRefused(404, "video_daily_brief_not_found", "找不到"),
        ]
    )
    monkeypatch.setattr(service, "finish_request", finish)
    async with AsyncClient(
        transport=ASGITransport(app=_app(token=token)), base_url="http://t"
    ) as c:
        nxt = await c.get(f"{TOOL}/next")
        empty = await c.get(f"{TOOL}/next")
        claimed = await c.post(f"{TOOL}/{view.id}/start", json={"slug": SLUG})
        mismatch = await c.post(f"{TOOL}/{view.id}/start", json={"slug": "daily-ai-20261027"})
        bad_slug = await c.post(f"{TOOL}/{view.id}/start", json={"slug": "Bad Slug"})
        done = await c.post(f"{TOOL}/{view.id}/done")
        missing = await c.post(f"{TOOL}/{uuid4()}/done")
    assert nxt.status_code == 200
    request = nxt.json()["request"]
    assert (request["id"], request["slug"], request["source_guides"]) == (
        str(view.id),
        SLUG,
        ["story-1"],
    )
    assert set(request["stories"][0]) == {"slug", "title", "description", "url", "news_date"}
    assert empty.status_code == 200 and empty.json() == {"request": None}
    assert claimed.status_code == 200 and claimed.json()["status"] == "started"
    assert start.await_args_list[0].args[1:] == (token, view.id, SLUG)
    assert mismatch.status_code == 409
    assert mismatch.json()["code"] == "video_daily_brief_slug_mismatch"
    assert bad_slug.status_code == 422 and start.await_count == 2
    assert done.status_code == 200 and done.json()["status"] == "done"
    assert missing.status_code == 404
    assert {call.args[0] for call in limits.await_args_list} == {"video_daily_briefs"}


# --- settings ------------------------------------------------------------------------------------


def test_the_settings_default_to_off_at_nine_five_stories_and_all_eight_languages() -> None:
    assert CAPTION_LOCALES == DUB_LOCALES, "the brief's languages are the videos' languages"
    brief = DailyBriefSettings()
    assert (brief.daily_brief_enabled, brief.daily_brief_hour, brief.daily_brief_min_stories) == (
        False,
        9,
        5,
    )
    assert list(brief.daily_brief_locales) == list(DUB_LOCALES)
    assert {
        locale: parts.model_dump() for locale, parts in brief.daily_brief_locales.items()
    } == DEFAULT_DAILY_BRIEF_LOCALES
    row = VideoAutomationSettings(id=1)
    assert settings_service.daily_brief_values(row) == brief, "a row from before 0143"
    row.daily_brief_locales = {"zh-CN": {"metadata": True}, "th": {"metadata": True}}
    assert list(settings_service.daily_brief_values(row).daily_brief_locales) == ["th"]
    for bad in (
        {"daily_brief_hour": 24},
        {"daily_brief_hour": -1},
        {"daily_brief_min_stories": 0},
        {"daily_brief_min_stories": 21},
        {"daily_brief_locales": {"fr": {"metadata": True}}},
        {"daily_brief_locales": {"en": {"captions": False, "dub": True}}},
        {"daily_brief_zone": "UTC"},
    ):
        with pytest.raises(ValidationError):
            DailyBriefSettings(**bad)


async def test_a_save_merges_the_brief_field_by_field_and_spreads_it_onto_columns(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        row = await settings_service.settings_row(session)
        current = settings_service.settings_values(row).model_dump()
    merged = SettingsSave.model_validate(
        {"daily_brief": {"daily_brief_enabled": True}}
    ).merged_over(current)
    written = SettingsWrite.model_validate(merged)
    assert written.daily_brief.daily_brief_enabled is True
    assert written.daily_brief.daily_brief_hour == 9
    flat = settings_service._flat(written.model_dump(mode="json"))
    assert flat["daily_brief_enabled"] is True and flat["daily_brief_min_stories"] == 5
    assert "daily_brief" not in flat
    assert SettingsSave().merged_over(current)["daily_brief"] == current["daily_brief"]


# --- the outline pick ----------------------------------------------------------------------------


def _pick(demo: float = 0.17) -> dict[str, Any]:
    return {
        "options": [{"key": "A"}, {"key": "B"}],
        "pick": {
            "choice": "A",
            "probabilities": {"A": 1.0, "B": 0.0},
            "options": {"A": {"stance": 0.92, "demo": demo}, "B": {"stance": 0.7, "demo": 0.2}},
            "advice": 0.02,
        },
    }


async def test_a_brief_s_outline_is_picked_without_a_demonstration_whatever_its_category(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        row = await settings_service.settings_row(session)
        row.channel_stance = "只講查得到出處的事。"
        row.auto_pick_outline = True
        await session.commit()
        assert await settings_service.auto_picks_outline(session, _pick(), "tutorial", SLUG)
        assert not await settings_service.auto_picks_outline(
            session, _pick(), "tutorial", "hands-on-mcp"
        )
        assert not await settings_service.auto_picks_outline(session, _pick(), "tutorial")
    assert not settings_service.outline_demo_wanted("tutorial", SLUG)
    assert settings_service.outline_demo_wanted(None, "hands-on-mcp")
    assert not settings_service.outline_demo_wanted("explainer")


# --- the languages -------------------------------------------------------------------------------


async def _brief_project(
    session: AsyncSession, slug: str = SLUG, final: str = "approved"
) -> VideoProject:
    project = VideoProject(slug=slug, title="快報", stage="final", format="slides")
    session.add(project)
    await session.flush()
    session.add(
        VideoReview(
            project_id=project.id,
            gate="final",
            content_sha256="a" * 64,
            summary="成片",
            status=final,
        )
    )
    await session.flush()
    return project


async def _locale_audits(session: AsyncSession) -> list[dict[str, Any]]:
    rows = await session.scalars(
        select(AdminAuditLog)
        .where(AdminAuditLog.action == "video_locales_set")
        .order_by(AdminAuditLog.created_at)
    )
    return [row.metadata_json for row in rows]


CAPTIONS_ONLY = {"metadata": True, "captions": True, "dub": False}
WITH_DUB = {"metadata": True, "captions": True, "dub": True}


async def test_an_approved_brief_gets_its_titles_and_captions_without_a_dub(
    db: async_sessionmaker[AsyncSession],
) -> None:
    now = AT_NINE
    async with db() as session:
        pending = await _brief_project(session, "daily-ai-20261027", final="pending")
        other = await _brief_project(session, "hands-on-mcp")
        project = await _brief_project(session)
        for each in (pending, other, project):
            await admin_service._decide_daily_brief_locales(session, each, now)
        assert pending.locales_decided_at is None and other.locales_decided_at is None
        assert project.locales_decided_at == now
        assert project.locales == {locale: CAPTIONS_ONLY for locale in DUB_LOCALES}
        [audit] = await _locale_audits(session)
        assert audit["decided_by"] == "server" and audit["phase"] == "captions"
        # Such a batch never waits for the owner, so the upload is not held back.
        made = {locale: {"metadata": "ready", "captions": "ready"} for locale in DUB_LOCALES}
        assert not admin_service.languages_need_owner({"locales": made})
        # Decided once: a later report does not write over the owner's change.
        project.locales = {"en": CAPTIONS_ONLY}
        await admin_service._decide_daily_brief_locales(session, project, now)
        assert project.locales == {"en": CAPTIONS_ONLY}


async def test_the_dubs_go_on_once_the_site_s_send_to_youtube_has_finished(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        row = await settings_service.settings_row(session)
        row.daily_brief_locales = {
            **DEFAULT_DAILY_BRIEF_LOCALES,
            "th": {"metadata": True, "captions": True, "dub": False},
        }
        project = await _brief_project(session)
        await admin_service._decide_daily_brief_locales(session, project, AT_NINE)
        await session.commit()
        # No YouTube id, or a send still running: nothing changes, the batch is still read.
        await admin_service.decide_daily_brief_dubs(session, SLUG)
        project.youtube_video_id = "a" * 11
        project.youtube_sync = {"status": "running"}
        await session.commit()
        await admin_service.decide_daily_brief_dubs(session, SLUG)
        assert not any(parts["dub"] for parts in project.locales.values())
        project.youtube_sync = {"status": "done"}
        await session.commit()
        await admin_service.decide_daily_brief_dubs(session, SLUG)
        assert project.locales == {
            locale: (CAPTIONS_ONLY if locale == "th" else WITH_DUB) for locale in DUB_LOCALES
        }
        assert list(project.locales) == list(DUB_LOCALES)
        audits = await _locale_audits(session)
        assert [audit["phase"] for audit in audits] == ["captions", "dubs"]
        # The owner unticks a dub afterwards: no later report or send ticks it again.
        project.locales = {**project.locales, "ja": CAPTIONS_ONLY}
        await session.commit()
        await admin_service.decide_daily_brief_dubs(session, SLUG)
        project.last_synced_at = AT_NINE
        await admin_service._decide_daily_brief_locales(session, project, AT_NINE)
        assert project.locales["ja"] == CAPTIONS_ONLY
        assert len(await _locale_audits(session)) == 2


async def test_a_brief_pasted_without_the_site_s_send_keeps_its_captions_only(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        project = await _brief_project(session)
        await admin_service._decide_daily_brief_locales(session, project, AT_NINE)
        project.youtube_video_id = "b" * 11
        await admin_service._decide_daily_brief_locales(session, project, AT_NINE)
    assert not any(parts["dub"] for parts in project.locales.values())


async def test_the_send_to_youtube_asks_about_the_dubs_only_when_it_ended_well(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = VideoProject(slug=SLUG, youtube_sync={"run": "t", "status": "running"})
    session = MagicMock()
    session.scalar = AsyncMock(return_value=project)
    session.commit = AsyncMock()

    class Opened:
        async def __aenter__(self) -> Any:
            return session

        async def __aexit__(self, *_: Any) -> None:
            return None

    decide = AsyncMock(side_effect=RuntimeError("database away"))
    monkeypatch.setattr(admin_service, "decide_daily_brief_dubs", decide)
    await youtube_sync._finish(lambda: Opened(), SLUG, "t", "details", "YouTube 不接受")  # type: ignore[arg-type]
    decide.assert_not_awaited()
    project.youtube_sync = {"run": "t", "status": "running"}
    # A failure deciding the dubs does not make the finished send read as failed.
    await youtube_sync._finish(lambda: Opened(), SLUG, "t", None, None)  # type: ignore[arg-type]
    decide.assert_awaited_once()
    assert project.youtube_sync["status"] == "done"
