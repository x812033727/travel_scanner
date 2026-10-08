"""The public video library lists only what YouTube shows the public, newest first."""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from typing import cast

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base, get_session
from app.guides.models import GuideArticle
from app.models import AdminAuditLog, User, VideoProject
from app.video_reviews import admin_service
from app.video_reviews.public_api import public_router
from tests.test_video_reviews_youtube import FakeYoutube, link_channel, youtube_item

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
    tables = [
        cast(Table, model.__table__)
        for model in (User, VideoProject, GuideArticle, AdminAuditLog)
    ]
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


async def test_a_video_the_owner_published_from_studio_is_listed_once_youtube_says_so(
    client: tuple[AsyncClient, async_sessionmaker[AsyncSession]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The eighteen videos of 2026-10-07: an id the owner pasted, no publish time (they went
    public in Studio, not through the site), so the library left them out. The backfill asks
    the linked channel and keeps the ones YouTube reports as public or scheduled."""
    http, factory = client
    await seed(
        factory,
        GuideArticle(slug="google-vids-guide", kind="life"),
        video(
            "studio-public",
            youtube_publish_at=None,
            source_guide="google-vids-guide",
            category="tutorial",
        ),
        video("studio-scheduled", youtube_publish_at=None),
        video("studio-private", youtube_publish_at=None),
        video("studio-unlisted", youtube_publish_at=None),
    )
    nothing = (await http.get("/api/v1/videos")).json()
    assert nothing["videos"] == [], "an id alone is not publication"
    by_article = (await http.get("/api/v1/videos", params={"guide": "google-vids-guide"})).json()
    assert by_article["videos"] == []

    link_channel(
        monkeypatch,
        FakeYoutube(
            youtube_item("studio-publ", published=NOW - timedelta(days=4)),
            youtube_item("studio-sche", privacy="private", scheduled=NOW + timedelta(days=1)),
            youtube_item("studio-priv", privacy="private"),
            youtube_item("studio-unli", privacy="unlisted"),
        ),
    )
    async with factory() as session:
        report = await admin_service.backfill_youtube_publish_times(session, apply=True)
    assert (report["checked"], report["filled"]) == (4, 2)

    listed = (await http.get("/api/v1/videos")).json()
    assert [item["slug"] for item in listed["videos"]] == ["studio-public"]
    assert listed["videos"][0]["published_at"].startswith(
        (NOW - timedelta(days=4)).isoformat()[:19]
    )
    assert listed["categories"] == ["tutorial"]
    by_article = (await http.get("/api/v1/videos", params={"guide": "google-vids-guide"})).json()
    assert [item["slug"] for item in by_article["videos"]] == ["studio-public"]
    # The scheduled one has a time now, in the future: listed once it has come, not before.
    async with factory() as session:
        stored = await session.scalars(select(VideoProject))
        rows = {row.slug: row.youtube_publish_at for row in stored}
    # SQLite hands the time back without its zone; it was written in UTC.
    scheduled = rows["studio-scheduled"]
    assert scheduled is not None and scheduled.replace(tzinfo=UTC) > NOW
    assert rows["studio-private"] is None and rows["studio-unlisted"] is None
