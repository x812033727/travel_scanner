"""The five selected MiniMax brand stories validate and keep their series look on import."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.video_automation import stories
from app.video_automation.models import (
    VideoAiRun,
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.schemas import SeriesIn
from app.video_media.models import VideoMediaJob

CUTE_LOOK = {"preset": "cute-mystery"}
TABLES = (
    User,
    AdminAuditLog,
    VideoToolToken,
    VideoProject,
    VideoReview,
    VideoMediaJob,
    VideoAiRun,
    VideoAutomationSettings,
    VideoDramaSeries,
    VideoDramaDoc,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaEpisode,
)


def _five_file() -> dict[str, Any]:
    folder = Path(__file__).resolve().parents[3] / "docs/videos/brand-stories-five-20261014"
    series = json.loads((folder / "series.json").read_text(encoding="utf-8"))
    episodes = sorted(
        (
            json.loads(file.read_text(encoding="utf-8"))
            for file in (folder / "episodes").glob("*.json")
        ),
        key=lambda episode: episode["number"],
    )
    return {"schema_version": 1, "series": series, "stories": episodes}


@pytest.fixture
async def db() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: Base.metadata.create_all(
                sync, tables=[model.__table__ for model in TABLES]
            )
        )
    try:
        yield async_sessionmaker(engine, expire_on_commit=False)
    finally:
        await engine.dispose()


def test_selected_five_episode_fixture_passes_api_schema_and_compiled_import_check() -> None:
    document = _five_file()
    series = document["series"]
    payload = SeriesIn.model_validate(
        {key: value for key, value in series.items() if key in SeriesIn.model_fields}
    )
    assert payload.model_dump()["look"] == CUTE_LOOK
    check = stories.check_story_file(document, series["slug"])
    assert check.problems == [] and check.refused == []
    assert [episode["number"] for episode in check.stories] == [1, 2, 3, 4, 5]


def test_compiled_story_accepts_only_the_matching_ten_minute_cute_route() -> None:
    document = _five_file()
    assert stories.series_problems(document["series"]) == []

    for changes, expected in (
        ({"target_minutes": 13}, "series.target_minutes must be 10"),
        ({"image_model": "gemini-3.1-flash-image"}, 'series.image_model must be "image-01"'),
        ({"style_preset": "cinematic-3d"}, 'series.style_preset must be "custom"'),
        ({"look": {"preset": "cute-mystery", "negative": "extra"}}, "series.look needs a style"),
        (
            {"look": {"preset": "cute-mystery", "style": "flat cartoon", "negative": "logos"}},
            "series.look needs a style",
        ),
        (
            {"look": {"style": "a custom look", "negative": "logos"}},
            "series.target_minutes must be 12 to 15",
        ),
    ):
        invalid = _five_file()
        invalid["series"].update(changes)
        assert expected in "\n".join(
            stories.check_story_file(invalid, invalid["series"]["slug"]).problems
        )


async def test_import_creates_the_cute_story_series_without_rewriting_look(
    db: async_sessionmaker[AsyncSession],
) -> None:
    document = _five_file()
    async with db() as session:
        report = await stories.import_story_rows(
            session, document, series_slug=document["series"]["slug"], apply=True, limit=1
        )
    assert report.problems == [] and report.written and report.series_created
    async with db() as session:
        series = await session.scalar(select(VideoDramaSeries))
        assert series is not None
        assert (series.target_minutes, series.image_model, series.style_preset) == (
            10,
            "image-01",
            "custom",
        )
        assert series.look == CUTE_LOOK
