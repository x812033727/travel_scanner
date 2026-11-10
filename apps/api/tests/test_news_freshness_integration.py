"""Real PostgreSQL quota concurrency and advisory report pagination in a private schema."""

from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from typing import cast
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import pytest
from sqlalchemy import Table, func, select, text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import get_settings
from app.db import Base
from app.guides.models import GuideArticle
from app.news_automation import freshness
from app.news_automation.models import (
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsPipelineRun,
    NewsSource,
)
from tests.test_news_pipeline import NEWS_TABLES

NOW = datetime(2026, 11, 10, 12, tzinfo=UTC)


@pytest.fixture
async def database() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    if os.getenv("RUN_INTEGRATION_TESTS") != "1":
        pytest.skip("requires isolated local PostgreSQL")
    url = get_settings().database_url
    assert make_url(url).host in {"localhost", "127.0.0.1", "::1", "postgres", "db"}
    assert make_url(url).get_backend_name() == "postgresql"
    schema = f"news_freshness_test_{uuid4().hex}"
    engine = create_async_engine(
        url, poolclass=NullPool, execution_options={"schema_translate_map": {None: schema}}
    )
    tables = [cast(Table, model.__table__) for model in NEWS_TABLES]
    try:
        async with engine.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
            await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
        yield async_sessionmaker(engine, expire_on_commit=False)
    finally:
        async with engine.begin() as connection:
            await connection.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
        await engine.dispose()


async def seed(session: AsyncSession, count: int) -> list[UUID]:
    source = NewsSource(
        name="Official",
        url="https://example.com/feed",
        format="rss",
        vertical="tech",
        role="evidence",
        enabled=True,
        is_first_party=True,
    )
    session.add_all([source, NewsAutomationSettings(id=1, enabled=True)])
    await session.flush()
    ids = []
    for index in range(count):
        article = GuideArticle(slug=f"freshness-{uuid4().hex}", kind="life")
        session.add(article)
        await session.flush()
        candidate = NewsCandidate(
            source_id=source.id,
            vertical="tech",
            status="published",
            canonical_url=f"https://example.com/news/{index}",
            source_title=f"News {index}",
            content_hash="a" * 64,
            idempotency_key=uuid4().hex,
            guide_article_id=article.id,
            published_at=NOW - timedelta(days=10),
        )
        session.add(candidate)
        await session.flush()
        ids.append(candidate.id)
    await session.commit()
    return ids


@pytest.mark.asyncio
async def test_daily_quota_is_hard_across_parallel_workers_and_repeated_runs(database):  # type: ignore[no-untyped-def]
    async with database() as session:
        ids = await seed(session, 25)
        for candidate_id in ids[:19]:
            assert await freshness._reserve_check(session, candidate_id, NOW)

    async def reserve(candidate_id: UUID) -> UUID | None:
        async with database() as session:
            return await freshness._reserve_check(session, candidate_id, NOW)

    results = await asyncio.gather(*(reserve(candidate_id) for candidate_id in ids[19:]))
    assert sum(value is not None for value in results) == 1
    async with database() as session:
        assert await freshness.run_checks(session, Mock(), now=NOW, clock=lambda: NOW) == 0
        assert await session.scalar(select(func.count()).select_from(NewsPipelineRun)) == 20


@pytest.mark.asyncio
async def test_pagination_reaches_due_rows_and_one_bad_receipt_does_not_hide_others(database):  # type: ignore[no-untyped-def]
    async with database() as session:
        ids = await seed(session, 80)
        for index, candidate_id in enumerate(ids[:55]):
            session.add(
                NewsPipelineRun(
                    candidate_id=candidate_id,
                    stage=freshness.STAGE,
                    status="succeeded",
                    idempotency_key=f"receipt-{index}",
                    started_at=NOW - timedelta(days=1),
                    metadata_json={"status": "future-version" if index == 0 else "changed"},
                )
            )
        await session.commit()
        due = await freshness.report(session, now=NOW, view="due")
        assert due.eligible_count == 80 and due.due_count == 25
        assert due.total_count == 25 and due.pages == 1
        assert {row.candidate_id for row in due.items} == set(ids[55:])
        assert all(row.review_due and row.status == "pending" for row in due.items)
        pages = [await freshness.report(session, now=NOW, page=page) for page in range(1, 5)]
        flattened = [row for page in pages for row in page.items]
        assert len(flattened) == len({row.candidate_id for row in flattened}) == 80
        assert next(row for row in flattened if row.candidate_id == ids[0]).status == "unverified"
        assert (await freshness.report(session, now=NOW, view="changed")).total_count == 54


@pytest.mark.asyncio
async def test_background_check_only_writes_advisory_receipt(database, monkeypatch):  # type: ignore[no-untyped-def]
    async with database() as session:
        ids = await seed(session, 1)
        row = NewsEvidence(
            candidate_id=ids[0],
            role="evidence",
            is_first_party=True,
            url="https://example.com/source",
            title="Original",
            content_hash="a" * 64,
            excerpt="Original excerpt",
            retrieved_at=NOW - timedelta(days=40),
            etag="original",
        )
        session.add(row)
        await session.commit()
        evidence_id = row.id
        candidate = await session.get(NewsCandidate, ids[0])
        assert candidate is not None
        candidate_updated = candidate.updated_at
        article_id = candidate.guide_article_id
        article = await session.get(GuideArticle, article_id)
        assert article is not None
        article_updated = article.updated_at
        revalidate = AsyncMock(return_value=(False, [f"source_content_changed:{row.url}"]))
        monkeypatch.setattr(freshness, "revalidate_evidence", revalidate)
        assert await freshness.run_checks(session, Mock(), now=NOW, clock=lambda: NOW) == 1
        assert await freshness.run_checks(session, Mock(), now=NOW, clock=lambda: NOW) == 0
    async with database() as session:
        row = await session.get(NewsEvidence, evidence_id)
        assert row is not None
        assert row.retrieved_at == NOW - timedelta(days=40)
        assert row.etag == "original" and row.excerpt == "Original excerpt"
        candidate = await session.get(NewsCandidate, ids[0])
        article = await session.get(GuideArticle, article_id)
        assert candidate is not None and article is not None
        assert candidate.status == "published" and candidate.updated_at == candidate_updated
        assert article.updated_at == article_updated and article.is_active
        receipt = await session.scalar(select(NewsPipelineRun))
        assert receipt is not None and receipt.metadata_json["status"] == "changed"


@pytest.mark.asyncio
async def test_a_batch_crossing_midnight_reserves_each_attempt_on_its_actual_day(database):  # type: ignore[no-untyped-def]
    async with database() as session:
        await seed(session, 2)
        times = iter(
            [
                NOW.replace(hour=23, minute=59, second=59),
                (NOW + timedelta(days=1)).replace(hour=0, minute=0, second=1),
            ]
        )
        assert await freshness.run_checks(session, Mock(), now=NOW, clock=lambda: next(times)) == 2
        rows = list(
            await session.scalars(select(NewsPipelineRun).order_by(NewsPipelineRun.started_at))
        )
        assert [row.started_at.date() for row in rows] == [
            NOW.date(),
            (NOW + timedelta(days=1)).date(),
        ]
        assert all(row.started_at.date().isoformat() in row.idempotency_key for row in rows)


@pytest.mark.asyncio
async def test_stale_candidate_selection_cannot_repeat_an_attempt_after_midnight(database):  # type: ignore[no-untyped-def]
    async with database() as session:
        ids = await seed(session, 1)
        first = NOW.replace(hour=23, minute=59, second=59)
        assert await freshness._reserve_check(session, ids[0], first)
        assert await freshness._reserve_check(session, ids[0], first + timedelta(seconds=2)) is None
        assert await session.scalar(select(func.count()).select_from(NewsPipelineRun)) == 1


@pytest.mark.asyncio
async def test_reservation_samples_clock_after_acquiring_the_quota_lock(database):  # type: ignore[no-untyped-def]
    async with database() as seed_session:
        ids = await seed(seed_session, 1)
    clock = Mock(return_value=NOW + timedelta(days=1))
    async with database() as blocker, database() as contender:
        await blocker.execute(text("SELECT pg_advisory_xact_lock(184729, 11010)"))
        task = asyncio.create_task(freshness._reserve_check(contender, ids[0], clock=clock))
        try:
            await asyncio.sleep(0.05)
            assert not task.done()
            clock.assert_not_called()
        finally:
            await blocker.commit()
        run_id = await task
        assert run_id is not None
        row = await contender.get(NewsPipelineRun, run_id)
        assert row is not None and row.started_at == NOW + timedelta(days=1)
        clock.assert_called_once_with()
