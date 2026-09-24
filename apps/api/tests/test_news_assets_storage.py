from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import cast
from unittest.mock import Mock

import pytest
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.guides.schemas import GuideDocument
from app.i18n import Locale
from app.news_automation import assets, jobs
from app.news_automation.models import NewsAsset, NewsCandidate, NewsEvidence, NewsSource
from app.problems import AppError

LOCALES: tuple[Locale, ...] = ("zh-TW", "zh-CN", "en", "ja", "ko")


def no_object_storage() -> None:
    raise AppError(503, "community_storage_unavailable", "community_storage_unavailable")


async def database() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = cast(
        list[Table],
        [
            NewsSource.__table__,
            NewsCandidate.__table__,
            NewsEvidence.__table__,
            NewsAsset.__table__,
        ],
    )
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    return async_sessionmaker(engine, expire_on_commit=False)


async def seed_candidate(session: AsyncSession) -> NewsCandidate:
    source = NewsSource(
        name="Official",
        url="https://example.com/feed",
        format="rss",
        role="evidence",
        vertical="ai",
    )
    session.add(source)
    await session.flush()
    candidate = NewsCandidate(
        source_id=source.id,
        vertical="ai",
        canonical_url="https://example.com/a",
        source_title="Release",
        content_hash="a" * 64,
        idempotency_key="b" * 64,
    )
    session.add(candidate)
    await session.commit()
    return candidate


def documents() -> dict[Locale, GuideDocument]:
    return {
        locale: GuideDocument.model_validate(
            {
                "title": f"Release {locale}",
                "description": "What changed.",
                "blocks": [{"type": "paragraph", "text": "Body."}],
                "sources": [],
            }
        )
        for locale in LOCALES
    }


@pytest.mark.asyncio
async def test_without_object_storage_images_live_in_the_row_and_are_served_from_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    factory = await database()
    monkeypatch.setattr(assets, "storage", no_object_storage)
    async with factory() as session:
        candidate = await seed_candidate(session)
        rendered = await assets.ensure_assets(session, candidate, documents())
        await session.commit()
        rows = list(await session.scalars(select(NewsAsset)))
        assert len(rows) == 7
        assert all(row.content for row in rows)
        diagram_src = next(
            block.src
            for block in rendered["en"].blocks
            if getattr(block, "type", "") == "image"
        )
        filename = diagram_src.rsplit("/", 1)[-1]
        with pytest.raises(AppError):
            await assets.public_asset(session, filename)
        await assets.mark_assets_public(session, candidate.id)
        await session.commit()
        body, content_type, _ = await assets.public_asset(session, filename)
    assert content_type == "image/svg+xml"
    assert body.startswith(b"<svg")


@pytest.mark.asyncio
async def test_with_object_storage_images_go_to_s3_and_not_the_row(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    factory = await database()
    client = Mock()
    monkeypatch.setattr(assets, "storage", lambda: client)
    async with factory() as session:
        candidate = await seed_candidate(session)
        await assets.ensure_assets(session, candidate, documents())
        await session.commit()
        rows = list(await session.scalars(select(NewsAsset)))
    assert client.put_object.call_count == 7
    assert all(row.content is None for row in rows)


@pytest.mark.asyncio
async def test_retention_clears_row_images_without_needing_object_storage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    factory = await database()
    monkeypatch.setattr(assets, "storage", no_object_storage)
    monkeypatch.setattr(jobs, "SessionFactory", factory)
    async with factory() as session:
        candidate = await seed_candidate(session)
        await assets.ensure_assets(session, candidate, documents())
        for row in await session.scalars(select(NewsAsset)):
            row.created_at = datetime.now(UTC) - timedelta(days=120)
        await session.commit()
        candidate_id = candidate.id
    result = await jobs.cleanup_retention()
    async with factory() as session:
        rows = list(
            await session.scalars(select(NewsAsset).where(NewsAsset.candidate_id == candidate_id))
        )
    assert result["deleted_assets"] == 7
    assert all(row.content is None and row.deleted_at is not None for row in rows)
