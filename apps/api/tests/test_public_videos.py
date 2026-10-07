"""The public video library lists only what YouTube shows the public, newest first."""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from typing import cast

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base, get_session
from app.guides.models import GuideArticle
from app.models import User, VideoProject
from app.video_reviews.public_api import public_router

NOW = datetime.now(UTC)


def video(slug: str, **values: object) -> VideoProject:
    defaults: dict[str, object] = {
        "title": f"Title {slug}",
        "stage": "published",
        "checklist": [],
        "youtube_video_id": f"{slug:_<11}"[:11],
        "youtube_publish_at": NOW - timedelta(days=1),
    }
    return VideoProject(slug=slug, **{**defaults, **values})


@pytest.fixture
async def client() -> AsyncIterator[tuple[AsyncClient, async_sessionmaker[AsyncSession]]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = [cast(Table, model.__table__) for model in (User, VideoProject, GuideArticle)]
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async def session() -> AsyncIterator[AsyncSession]:
        async with factory() as value:
            yield value

    app = FastAPI()
    app.include_router(public_router, prefix="/api/v1")
    app.dependency_overrides[get_session] = session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
        yield http, factory
    await engine.dispose()


async def seed(
    factory: async_sessionmaker[AsyncSession], *rows: VideoProject | GuideArticle
) -> None:
    async with factory() as session:
        session.add_all(rows)
        await session.commit()


async def test_lists_only_published_videos_newest_first(
    client: tuple[AsyncClient, async_sessionmaker[AsyncSession]],
) -> None:
    http, factory = client
    await seed(
        factory,
        GuideArticle(slug="cursor-editor-guide", kind="life"),
        GuideArticle(slug="retired-guide", kind="life", is_active=False),
        video(
            "older",
            youtube_publish_at=NOW - timedelta(days=3),
            category="tutorial",
            source_guide="cursor-editor-guide",
        ),
        video(
            "newer",
            youtube_publish_at=NOW - timedelta(hours=2),
            category="comparison",
            source_guide="retired-guide",
        ),
        video("scheduled", youtube_publish_at=NOW + timedelta(days=1)),
        video("private", youtube_publish_at=None),
        video("unuploaded", youtube_video_id=None),
        video("dropped", dropped_at=NOW - timedelta(hours=1), dropped_note="no"),
        video("short", shorts_line="lab", youtube_publish_at=NOW - timedelta(days=2)),
    )
    response = await http.get("/api/v1/videos")
    assert response.status_code == 200
    body = response.json()
    assert [item["slug"] for item in body["videos"]] == ["newer", "short", "older"]
    assert body["next_cursor"] is None
    assert body["categories"] == ["tutorial", "comparison"]
    older = body["videos"][2]
    assert older["source_guide"] == "cursor-editor-guide"
    assert older["source_guide_kind"] == "life"
    # An article that is no longer live is not linked.
    assert body["videos"][0]["source_guide"] is None
    assert older["kind"] == "long"
    assert body["videos"][1]["kind"] == "shorts"
    # Nothing an operator sees on /admin/videos leaves through this door.
    assert set(older) == {
        "slug",
        "title",
        "youtube_video_id",
        "category",
        "kind",
        "source_guide",
        "source_guide_kind",
        "published_at",
    }


async def test_filters_and_pages(
    client: tuple[AsyncClient, async_sessionmaker[AsyncSession]],
) -> None:
    http, factory = client
    await seed(
        factory,
        *(
            video(f"v{index}", youtube_publish_at=NOW - timedelta(hours=index), category="tutorial")
            for index in range(5)
        ),
    )
    await seed(factory, video("s1", shorts_line="cut", category="explainer"))
    first = (await http.get("/api/v1/videos", params={"limit": 2, "kind": "long"})).json()
    assert [item["slug"] for item in first["videos"]] == ["v0", "v1"]
    second = (
        await http.get(
            "/api/v1/videos", params={"limit": 2, "kind": "long", "cursor": first["next_cursor"]}
        )
    ).json()
    assert [item["slug"] for item in second["videos"]] == ["v2", "v3"]
    shorts = (await http.get("/api/v1/videos", params={"kind": "shorts"})).json()
    assert [item["slug"] for item in shorts["videos"]] == ["s1"]
    explainers = (await http.get("/api/v1/videos", params={"category": "explainer"})).json()
    assert [item["slug"] for item in explainers["videos"]] == ["s1"]
    by_article = (await http.get("/api/v1/videos", params={"guide": "v-none"})).json()
    assert by_article["videos"] == []
    # A cursor the server cannot read starts from the top instead of failing.
    garbled = (await http.get("/api/v1/videos", params={"cursor": "not-a-cursor"})).json()
    assert garbled["videos"][0]["slug"] == "v0"
