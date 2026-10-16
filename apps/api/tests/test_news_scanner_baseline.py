"""A source's first scan is its baseline, even when the first attempt fails.

Kept apart from test_news_automation.py, which an open draft extends heavily.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.db import Base
from app.news_automation.fetch import UnsafeNewsUrl
from app.news_automation.models import (
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsSource,
)
from app.news_automation.scanner import BASELINE, scan_source
from app.news_automation.schemas import FetchResult

LISTING_URL = "https://blog.example/engineering"
# An HTML listing carries no dates, so nothing but the baseline keeps its old entries out.
NAMES = [f"post-{index}" for index in range(5)]
LISTING = "".join(
    f'<a href="/engineering/{name}">Engineering post {name}</a>' for name in NAMES
).encode()


class FlakyListing:
    """Refuses the listing `failures` times (robots.txt answering 403), then serves it."""

    def __init__(self, failures: int) -> None:
        self.failures = failures
        self.requested: list[str] = []

    async def fetch(self, url: str, **_kwargs: object) -> FetchResult:
        self.requested.append(url)
        if url == LISTING_URL:
            if self.failures:
                self.failures -= 1
                raise UnsafeNewsUrl("robots.txt could not be read (HTTP 403)")
            return FetchResult(url=url, status_code=200, content_type="text/html", body=LISTING)
        body = f"<html><main>{url}: {'The whole post. ' * 30}</main></html>".encode()
        return FetchResult(url=url, status_code=200, content_type="text/html", body=body)

    async def close(self) -> None:
        return None


async def _database() -> tuple[AsyncEngine, async_sessionmaker]:  # type: ignore[type-arg]
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: Base.metadata.create_all(
                sync,
                tables=[
                    NewsAutomationSettings.__table__,
                    NewsSource.__table__,
                    NewsCandidate.__table__,
                    NewsEvidence.__table__,
                ],
            )
        )
    return engine, async_sessionmaker(engine, expire_on_commit=False)


def _source(**fields: object) -> NewsSource:
    return NewsSource(
        name="Engineering blog",
        url=LISTING_URL,
        format="html",
        role="evidence",
        vertical="tech",
        enabled=True,
        is_first_party=True,
        config_json={"include_path_prefixes": ["/engineering/"]},
        **fields,
    )


@pytest.mark.asyncio
async def test_a_first_scan_that_fails_leaves_the_baseline_to_the_next_scan() -> None:
    engine, factory = await _database()
    source = _source()
    fetcher = FlakyListing(failures=1)
    queued: list[UUID] = []

    async def enqueue(candidate_id: UUID) -> None:
        queued.append(candidate_id)

    async with factory() as session:
        session.add(NewsAutomationSettings(id=1, enabled=True))
        session.add(source)
        await session.commit()
        with pytest.raises(UnsafeNewsUrl):
            await scan_source(session, source.id, enqueue, fetcher=fetcher)  # type: ignore[arg-type]
        await session.refresh(source)
        failed = (source.last_scanned_at, source.last_status, source.consecutive_failures)

        fetcher.requested.clear()
        created = await scan_source(session, source.id, enqueue, fetcher=fetcher)  # type: ignore[arg-type]
        await session.refresh(source)
        rows = {
            row.canonical_url.rsplit("/", 1)[-1]: (row.status, row.error_code)
            for row in await session.scalars(select(NewsCandidate))
        }
        scanned = (source.last_scanned_at is not None, source.last_status)
    # The failure is recorded, but the source is still owed its baseline.
    assert failed == (None, "failed", 1)
    # The retry is the first scan: the listing is read, no page is fetched, nothing is queued.
    assert created == 0 and queued == []
    assert fetcher.requested == [LISTING_URL]
    assert rows == {name: ("rejected", BASELINE) for name in NAMES}
    assert scanned == (True, "succeeded")
    await engine.dispose()


@pytest.mark.asyncio
async def test_a_later_scan_that_fails_still_records_when_it_ran() -> None:
    engine, factory = await _database()
    before = datetime.now(UTC) - timedelta(hours=1)
    source = _source(last_scanned_at=before)

    async def enqueue(_candidate_id: UUID) -> None:
        return None

    async with factory() as session:
        session.add(NewsAutomationSettings(id=1, enabled=True))
        session.add(source)
        await session.commit()
        with pytest.raises(UnsafeNewsUrl):
            await scan_source(session, source.id, enqueue, fetcher=FlakyListing(failures=1))  # type: ignore[arg-type]
        await session.refresh(source)
        last = source.last_scanned_at
    assert last is not None and last.replace(tzinfo=UTC) > before
    await engine.dispose()
