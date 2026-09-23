from __future__ import annotations

from typing import cast
from uuid import uuid4

import pytest
from sqlalchemy import Table, func, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db import Base
from app.guides import admin_service, search
from app.guides.models import (
    GuideArticle,
    GuideArticleAlias,
    GuideArticleLink,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideSearchEntry,
)
from app.guides.schemas import GuideDocument
from app.i18n import Locale
from app.models import AdminAuditLog
from app.problems import AppError

LOCALES: tuple[Locale, ...] = ("en", "ja", "ko", "zh-TW", "zh-CN")


def document(locale: Locale) -> GuideDocument:
    return GuideDocument.model_validate(
        {
            "title": f"Atomic news {locale}",
            "description": f"Complete publication test for {locale}",
            "blocks": [{"type": "paragraph", "text": "Verified body."}],
            "sources": [
                {
                    "title": "Official",
                    "url": "https://example.com/release",
                    "checked_on": "2026-09-23",
                },
                {
                    "title": "Regulator",
                    "url": "https://regulator.example/notice",
                    "checked_on": "2026-09-23",
                },
            ],
        }
    )


async def database() -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = cast(
        list[Table],
        [
            GuideArticle.__table__,
            GuideArticleLocale.__table__,
            GuideArticleRevision.__table__,
            GuideArticleAlias.__table__,
            GuideSearchEntry.__table__,
            GuideArticleLink.__table__,
            AdminAuditLog.__table__,
        ],
    )
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    return engine, async_sessionmaker(engine, expire_on_commit=False)


async def seed(
    factory: async_sessionmaker[AsyncSession],
) -> tuple[GuideArticle, dict[Locale, int]]:
    article = GuideArticle(id=uuid4(), slug="ai-news-atomic-test-20260923", kind="life")
    async with factory() as session:
        session.add(article)
        for locale in LOCALES:
            session.add(
                GuideArticleLocale(
                    id=uuid4(),
                    article_id=article.id,
                    locale=locale,
                    version=1,
                    draft_json=document(locale).model_dump(mode="json"),
                )
            )
        await session.commit()
    return article, {locale: 1 for locale in LOCALES}


@pytest.mark.asyncio
async def test_publish_bundle_commits_five_locales_revisions_index_and_system_audit() -> None:
    engine, factory = await database()
    article, versions = await seed(factory)
    async with factory() as session:
        result = await admin_service.publish_bundle(
            session,
            None,
            article.id,
            {locale: document(locale) for locale in LOCALES},
            versions,
            reason="automated approval",
            automation_metadata={"candidate_id": "candidate-1"},
        )
        rows = list(
            await session.scalars(
                select(GuideArticleLocale).where(GuideArticleLocale.article_id == article.id)
            )
        )
        revisions = int(
            await session.scalar(select(func.count()).select_from(GuideArticleRevision)) or 0
        )
        indexed = int(await session.scalar(select(func.count()).select_from(GuideSearchEntry)) or 0)
        audits = list(await session.scalars(select(AdminAuditLog)))
    assert set(result) == set(LOCALES)
    assert all(row.published_version == 2 for row in rows)
    assert revisions == indexed == len(LOCALES)
    assert len(audits) == len(LOCALES)
    assert all(
        item.actor_user_id is None and item.metadata_json["atomic_bundle"] for item in audits
    )
    await engine.dispose()


@pytest.mark.asyncio
async def test_publish_bundle_rolls_back_every_locale_when_indexing_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    article, versions = await seed(factory)
    original = search.index_locale
    calls = 0

    async def fail_third(*args: object, **kwargs: object) -> object:
        nonlocal calls
        calls += 1
        if calls == 3:
            raise RuntimeError("index failed")
        return await original(*args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(search, "index_locale", fail_third)
    async with factory() as session:
        with pytest.raises(RuntimeError, match="index failed"):
            await admin_service.publish_bundle(
                session,
                None,
                article.id,
                {locale: document(locale) for locale in LOCALES},
                versions,
                reason="automated approval",
            )
    async with factory() as session:
        rows = list(
            await session.scalars(
                select(GuideArticleLocale).where(GuideArticleLocale.article_id == article.id)
            )
        )
        assert all(row.version == 1 and row.published_version is None for row in rows)
        assert await session.scalar(select(func.count()).select_from(GuideArticleRevision)) == 0
        assert await session.scalar(select(func.count()).select_from(GuideSearchEntry)) == 0
        assert await session.scalar(select(func.count()).select_from(AdminAuditLog)) == 0
    await engine.dispose()


@pytest.mark.asyncio
async def test_publish_bundle_rolls_back_every_locale_on_one_version_conflict() -> None:
    engine, factory = await database()
    article, versions = await seed(factory)
    versions["ja"] = 0
    async with factory() as session:
        with pytest.raises(AppError) as conflict:
            await admin_service.publish_bundle(
                session,
                None,
                article.id,
                {locale: document(locale) for locale in LOCALES},
                versions,
                reason="automated approval",
            )
    assert conflict.value.code == "guide_version_conflict"
    async with factory() as session:
        rows = list(
            await session.scalars(
                select(GuideArticleLocale).where(GuideArticleLocale.article_id == article.id)
            )
        )
        assert all(row.version == 1 and row.published_version is None for row in rows)
        assert await session.scalar(select(func.count()).select_from(GuideArticleRevision)) == 0
        assert await session.scalar(select(func.count()).select_from(GuideSearchEntry)) == 0
        assert await session.scalar(select(func.count()).select_from(AdminAuditLog)) == 0
    await engine.dispose()
