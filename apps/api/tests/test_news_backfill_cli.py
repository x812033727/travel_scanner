"""Reopening earlier candidates that old rules or old models stopped (owner request, 2026-09-26)."""

from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, cast
from uuid import UUID, uuid4

import pytest
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db import Base
from app.models import AdminAuditLog, User
from app.news_automation import backfill_cli
from app.news_automation.models import NewsCandidate, NewsEvidence, NewsSource


def _candidate(
    source: NewsSource, status: str, error_code: str | None, published: datetime
) -> NewsCandidate:
    marker = uuid4().hex
    return NewsCandidate(
        source_id=source.id,
        vertical="ai",
        status=status,
        error_code=error_code,
        human_decision="reject" if status == "rejected" else None,
        canonical_url=f"https://news.example/{marker}",
        source_title=f"Story {status} {error_code} {published:%m-%d}",
        normalized_title=f"story {marker}",
        content_hash=marker * 2,
        idempotency_key=marker * 2,
        source_published_at=published,
    )


@pytest.mark.asyncio
async def test_the_backfill_reopens_only_stories_stopped_by_old_rules_best_first(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'news.db'}")
    tables = cast(
        list[Table],
        [
            User.__table__,
            NewsSource.__table__,
            NewsCandidate.__table__,
            NewsEvidence.__table__,
            AdminAuditLog.__table__,
        ],
    )
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    old, recent, newest = (
        datetime(2026, 9, 1, tzinfo=UTC),
        datetime(2026, 9, 20, tzinfo=UTC),
        datetime(2026, 9, 24, tzinfo=UTC),
    )
    async with factory() as session:
        session.add(User(email="owner@example.com", password_hash="unused", is_admin=True))
        source = NewsSource(
            name="Feed",
            url="https://news.example/feed",
            format="rss",
            role="evidence",
            vertical="ai",
        )
        session.add(source)
        await session.flush()
        official = _candidate(source, "rejected", "news_evidence_insufficient", recent)
        press = _candidate(source, "needs_redraft", "news_verification_failed", newest)
        too_old = _candidate(source, "rejected", "news_evidence_insufficient", old)
        editorial = _candidate(source, "rejected", "news_zh_draft_ready", newest)
        published = _candidate(source, "published", None, newest)
        session.add_all([official, press, too_old, editorial, published])
        await session.flush()
        session.add(
            NewsEvidence(
                candidate_id=official.id,
                role="evidence",
                is_first_party=True,
                url="https://official.example/post",
                title="Post",
                content_hash="h" * 64,
                excerpt="Text.",
            )
        )
        await session.commit()
        official_id, press_id = official.id, press.id

    queued: list[tuple[UUID, int]] = []
    monkeypatch.setattr(backfill_cli, "SessionFactory", factory)
    monkeypatch.setattr(backfill_cli, "engine", engine)
    monkeypatch.setattr(
        backfill_cli.jobs,
        "enqueue_candidate",
        lambda candidate_id, retry_count=0: queued.append((candidate_id, retry_count)) or "job",
    )

    listed: dict[str, Any] = await backfill_cli.run(
        since=date(2026, 9, 15), limit=None, apply=False, actor_email=None, reason="Backfill"
    )
    assert (listed["candidates"], listed["first_party"], listed["applied"]) == (2, 1, False)
    assert listed["sample"][0]["first_party"] is True, "an official story first"
    assert queued == []

    applied = await backfill_cli.run(
        since=date(2026, 9, 15),
        limit=None,
        apply=True,
        actor_email="owner@example.com",
        reason="Backfill",
    )
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'news.db'}")
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        rows = {row.id: row for row in await session.scalars(select(NewsCandidate))}
        audits = list(await session.scalars(select(AdminAuditLog.action)))
    await engine.dispose()

    assert applied["applied"] is True
    assert [candidate_id for candidate_id, _retry in queued] == [official_id, press_id]
    for candidate_id in (official_id, press_id):
        row = rows[candidate_id]
        assert (row.status, row.error_code, row.human_decision) == ("discovered", None, None)
        assert row.retry_count == 1
    untouched = {row.status for key, row in rows.items() if key not in {official_id, press_id}}
    assert untouched == {"rejected", "published"}
    assert audits == ["news_candidate_reopened", "news_candidate_reopened"]
