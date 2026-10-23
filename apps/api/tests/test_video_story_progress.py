"""Persisted preproduction counts stay separate from finished brand-story films."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.db import Base, get_session
from app.models import User, VideoProject, VideoReview
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api, stories, story_progress
from app.video_automation.models import VideoDramaEpisode, VideoDramaSeries

ROOT = Path(__file__).resolve().parents[3]
PLANS = ROOT / "docs/videos/brand-stories-everyday-reversals-20261020/stories.json"
NOW = datetime(2026, 10, 24, tzinfo=UTC)


@pytest_asyncio.fixture
async def db() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        yield factory
    finally:
        await engine.dispose()


def _plans() -> list[dict[str, object]]:
    document = json.loads(PLANS.read_text(encoding="utf-8"))
    return document["stories"]


async def _series(session: AsyncSession) -> VideoDramaSeries:
    row = VideoDramaSeries(
        id=uuid4(),
        slug=stories.EVERYDAY_REVERSALS_SLUG,
        kind="story",
        title="日用品的意外轉身",
        premise="已審企劃匯入後台供檢視",
        status="paused",
        planned_episodes=20,
        target_minutes=10,
        style_preset="custom",
        hands_off=True,
        visual_tier="stills",
        image_model="image-01",
        look={"preset": "cute-mystery"},
    )
    session.add(row)
    await session.flush()
    return row


def _episode(series: VideoDramaSeries, plan: dict[str, object]) -> VideoDramaEpisode:
    number = plan["number"]
    assert isinstance(number, int)
    return VideoDramaEpisode(
        id=uuid4(),
        series_id=series.id,
        number=number,
        chapter_number=1,
        title=str(plan["title"]),
        logline=str(plan["logline"]),
        slug=str(plan["slug"]),
        beats={key: value for key, value in plan.items() if key not in stories.COLUMN_KEYS},
        status="planned",
    )


def _project(episode: VideoDramaEpisode, *, dropped: bool = False) -> VideoProject:
    return VideoProject(
        id=uuid4(),
        slug=episode.slug,
        title=episode.title,
        format="drama",
        series_slug=stories.EVERYDAY_REVERSALS_SLUG,
        episode_number=episode.number,
        stage="script",
        dropped_at=NOW if dropped else None,
    )


def _review(
    project: VideoProject,
    *,
    status: str = "approved",
    source: str | None = None,
    submitted: datetime = NOW,
) -> VideoReview:
    return VideoReview(
        id=uuid4(),
        project_id=project.id,
        gate="script",
        status=status,
        content_sha256=sha256((source or "legacy source").encode("utf-8")).hexdigest(),
        payload={"source_md": source} if source is not None else {},
        summary="Script review",
        created_at=submitted,
    )


@pytest.mark.asyncio
async def test_absent_series_has_zero_stage_counts_without_inventing_finished_films(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        result = await story_progress.story_preproduction(session)
    assert result.model_dump() == {
        "series_slug": stories.EVERYDAY_REVERSALS_SLUG,
        "total_episodes": 20,
        "full_plans": 0,
        "scripts_approved": 0,
        "scripts_pending": 0,
        "source_markdown_verified": 0,
        "finished_films": 0,
        "episodes": [],
    }


@pytest.mark.asyncio
async def test_all_plans_and_current_review_cards_report_each_stage_separately(
    db: async_sessionmaker[AsyncSession],
) -> None:
    approved_numbers = {3, 4, 5, 6, 7, 8, 10, 11, 14, 15}
    async with db() as session:
        series = await _series(session)
        for plan in _plans():
            episode = _episode(series, plan)
            session.add(episode)
            if episode.number in approved_numbers | {19}:
                project = _project(episode)
                session.add(project)
                source = None if episode.number == 3 else f"# C{episode.number:02d}\n正文\n"
                session.add(
                    _review(
                        project,
                        status="pending" if episode.number == 19 else "approved",
                        source=source,
                    )
                )
        await session.commit()
    async with db() as session:
        result = await story_progress.story_preproduction(session)
    assert (result.total_episodes, result.full_plans, result.finished_films) == (20, 20, 0)
    assert (result.scripts_approved, result.scripts_pending) == (10, 1)
    assert result.source_markdown_verified == 10
    by_number = {episode.number: episode for episode in result.episodes}
    assert by_number[3].script_status == "approved"
    assert not by_number[3].source_markdown_verified  # legacy card has no Markdown bytes
    assert by_number[19].script_status == "pending"
    assert by_number[19].source_markdown_verified
    assert by_number[20].script_status is None


@pytest.mark.asyncio
async def test_partial_bad_identity_dropped_and_newer_rejected_are_not_counted(
    db: async_sessionmaker[AsyncSession],
) -> None:
    plans = _plans()
    async with db() as session:
        series = await _series(session)
        first = _episode(series, plans[0])
        first.status = "done"
        second = _episode(series, plans[1])
        second.beats = {**second.beats, "id": "C99"}
        third = _episode(series, plans[2])
        session.add_all([first, second, third])

        valid_project = _project(first)
        wrong_number = _project(second)
        wrong_number.episode_number = 20
        dropped_project = _project(third, dropped=True)
        session.add_all([valid_project, wrong_number, dropped_project])
        session.add_all(
            [
                _review(valid_project, source="# older\n", submitted=NOW),
                _review(
                    valid_project,
                    status="rejected",
                    source="# newer\n",
                    submitted=NOW + timedelta(minutes=1),
                ),
                _review(wrong_number, source="# wrong episode\n"),
                _review(dropped_project, source="# dropped\n"),
            ]
        )
        await session.commit()
    async with db() as session:
        result = await story_progress.story_preproduction(session)
    assert result.full_plans == 2
    assert result.finished_films == 1  # only the real finished-film state drives this count
    assert (result.scripts_approved, result.scripts_pending, result.source_markdown_verified) == (
        0,
        0,
        0,
    )
    assert [episode.full_plan for episode in result.episodes] == [True, False, True]


@pytest.mark.asyncio
async def test_source_hash_mismatch_and_subject_review_do_not_raise_intake_count(
    db: async_sessionmaker[AsyncSession],
) -> None:
    async with db() as session:
        series = await _series(session)
        first = _episode(series, _plans()[0])
        session.add(first)
        project = _project(first)
        session.add(project)
        current = _review(project, source="# Exact bytes\n")
        current.content_sha256 = "0" * 64
        character_review = _review(
            project, source="# character\n", submitted=NOW + timedelta(days=1)
        )
        character_review.subject = "character:host"
        session.add_all([current, character_review])
        await session.commit()
    async with db() as session:
        result = await story_progress.story_preproduction(session)
    assert (result.full_plans, result.scripts_approved, result.source_markdown_verified) == (
        1,
        1,
        0,
    )


@pytest.mark.asyncio
async def test_admin_endpoint_requires_content_read_and_returns_same_persisted_counts(
    db: async_sessionmaker[AsyncSession],
) -> None:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session_override() -> AsyncIterator[AsyncSession]:
        async with db() as session:
            yield session

    app.dependency_overrides[get_session] = session_override
    viewer = User(id=uuid4(), email="viewer@example.test", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    app.dependency_overrides[current_user] = lambda: viewer
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        response = await client.get("/api/v1/admin/video-automation/story-preproduction")
    assert response.status_code == 200
    assert response.json()["total_episodes"] == 20
    assert response.json()["finished_films"] == 0

    member = User(id=uuid4(), email="member@example.test", password_hash="unused")
    member._admin_roles_cache = frozenset()  # type: ignore[attr-defined]
    app.dependency_overrides[current_user] = lambda: member
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        refused = await client.get("/api/v1/admin/video-automation/story-preproduction")
    assert refused.status_code == 403
