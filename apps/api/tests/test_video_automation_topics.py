from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.news_automation import sources_cli
from app.news_automation.models import NewsCandidate, NewsEvidence, NewsSource
from app.news_automation.policy import JEV_FINAL_HOLD
from app.video_automation import topics
from app.video_automation.schemas import TopicView

NOW = datetime(2026, 10, 10, 12, 0, tzinfo=UTC)
PAGE = "https://claude.dev/blog/claude-code-in-the-cloud/"


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: Base.metadata.create_all(
                sync,
                tables=[NewsSource.__table__, NewsCandidate.__table__, NewsEvidence.__table__],
            )
        )
    async with async_sessionmaker(engine, expire_on_commit=False)() as opened:
        yield opened
    await engine.dispose()


async def _source(session: AsyncSession, name: str, **changes: Any) -> NewsSource:
    values: dict[str, Any] = {
        "name": name,
        "url": f"https://{name.casefold().replace(' ', '-')}.example/feed.xml",
        "format": "rss",
        "role": "evidence",
        "vertical": "ai",
        "is_first_party": True,
        "enabled": True,
        "config_json": {"video_topics": True},
    }
    source = NewsSource(**{**values, **changes})
    session.add(source)
    await session.commit()
    return source


async def _candidate(
    session: AsyncSession, source: NewsSource, url: str, **changes: Any
) -> NewsCandidate:
    values: dict[str, Any] = {
        "source_id": source.id,
        "vertical": "ai",
        "status": "rejected",
        "error_code": "news_not_eligible",
        "canonical_url": url,
        "source_title": "Claude Code in the cloud: a field guide to cloud sessions",
        "content_hash": url[-40:],
        "idempotency_key": url,
        "created_at": NOW - timedelta(days=2),
    }
    candidate = NewsCandidate(**{**values, **changes})
    session.add(candidate)
    await session.commit()
    return candidate


async def _evidence(session: AsyncSession, candidate_id: UUID, url: str, excerpt: str) -> None:
    session.add(
        NewsEvidence(
            candidate_id=candidate_id,
            role="evidence",
            is_first_party=True,
            url=url,
            title="A page",
            content_hash=url[-40:],
            excerpt=excerpt,
        )
    )
    await session.commit()


@pytest.mark.asyncio
async def test_a_first_party_page_the_writer_declined_is_offered_as_an_official_topic(
    session: AsyncSession,
) -> None:
    source = await _source(session, "Claude developer blog")
    candidate = await _candidate(
        session, source, PAGE, source_published_at=datetime(2026, 10, 6, 15, 0, tzinfo=UTC)
    )
    await _evidence(
        session,
        candidate.id,
        PAGE,
        "You probably run Claude Code in a terminal\n  on your own laptop. " + "x" * 600,
    )
    # A second page the scanner attached to the same candidate is not the page's own excerpt.
    await _evidence(session, candidate.id, "https://www.anthropic.com/news/other", "Elsewhere.")

    found, notes = await topics.official_topics(session, now=NOW)

    assert notes == []
    assert len(found) == 1
    topic = found[0]
    assert topic.source == "official"
    assert topic.title == (
        "Claude developer blog｜Claude Code in the cloud: a field guide to cloud sessions"
    )
    assert topic.url == PAGE
    assert topic.slug is None
    assert topic.date == "2026-10-06"
    assert topic.summary.startswith("You probably run Claude Code in a terminal on your own lap")
    assert len(topic.summary) == 500


@pytest.mark.asyncio
async def test_a_page_without_stored_evidence_or_a_date_is_still_offered(
    session: AsyncSession,
) -> None:
    source = await _source(session, "Claude developer blog")
    await _candidate(session, source, PAGE)

    found, _ = await topics.official_topics(session, now=NOW)

    # No date of its own: the day the scanner first saw it is not sent in its place.
    assert [(topic.summary, topic.date) for topic in found] == [("", None)]


@pytest.mark.asyncio
async def test_only_the_writers_own_refusal_from_an_opted_in_source_counts(
    session: AsyncSession,
) -> None:
    opted_in = await _source(session, "Opted in")
    kept = await _candidate(session, opted_in, "https://opted-in.example/kept")
    # Each row is the kept one with one field changed, or a state the pipeline really
    # leaves a candidate in (those change status and error_code together).
    not_offered: dict[str, dict[str, Any]] = {
        # The first scan's back catalogue, never read.
        "baseline": {"error_code": "news_baseline"},
        # Reported: it is a site article and comes through site_topics.
        "published": {"status": "published", "error_code": None},
        "duplicate": {"status": "duplicate", "error_code": None},
        # Rejected for another reason than the writer's "not newsworthy".
        "other-refusal": {"error_code": "news_hard_checks_failed"},
        "in-flight": {"status": "discovered", "error_code": None},
        "held": {"status": "manual_review", "error_code": JEV_FINAL_HOLD},
        # The judge asked for a rewrite and the writer then declined the story: the same
        # error code as the kept row, waiting for the owner. Only the status keeps it out.
        "handed-back": {"status": "needs_redraft"},
        # The writer declined it and the owner then rejected it by hand.
        "owner-rejected": {"human_decision": "reject"},
        "old": {"created_at": NOW - timedelta(days=15)},
    }
    for slug, changes in not_offered.items():
        await _candidate(session, opted_in, f"https://opted-in.example/{slug}", **changes)
    not_opted_in: dict[str, dict[str, Any]] = {
        "No key": {"config_json": {}},
        # Only the boolean opts in; a string from a hand-edited config does not.
        "Key as text": {"config_json": {"video_topics": "true"}},
        "Switched off": {"enabled": False},
        "Press": {"is_first_party": False},
    }
    for name, changes in not_opted_in.items():
        other = await _source(session, name, **changes)
        await _candidate(session, other, f"{other.url}/story")

    found, notes = await topics.official_topics(session, now=NOW)

    assert [topic.url for topic in found] == [kept.canonical_url]
    assert notes == []


@pytest.mark.asyncio
async def test_a_source_read_from_its_feed_summary_is_named_and_left_out(
    session: AsyncSession,
) -> None:
    changelog = await _source(
        session,
        "Claude Code changelog",
        config_json={"video_topics": True, "evidence_from_feed_summary": True},
    )
    await _candidate(session, changelog, "https://code.claude.com/docs/en/changelog#2-1-296")

    found, notes = await topics.official_topics(session, now=NOW)

    assert found == []
    assert len(notes) == 1 and "Claude Code changelog" in notes[0]


@pytest.mark.asyncio
async def test_official_topics_are_newest_first_and_capped(session: AsyncSession) -> None:
    source = await _source(session, "Busy")
    # Oldest inserted first: without an ORDER BY the rows come back in insertion order
    # on SQLite, which would be oldest first and fail the assertions below.
    for index in reversed(range(topics.OFFICIAL_LIMIT + 3)):
        await _candidate(
            session,
            source,
            f"https://busy.example/{index:02d}",
            created_at=NOW - timedelta(hours=index + 1),
        )

    found, _ = await topics.official_topics(session, now=NOW)

    assert len(found) == topics.OFFICIAL_LIMIT
    assert found[0].url == "https://busy.example/00"
    assert found[-1].url == f"https://busy.example/{topics.OFFICIAL_LIMIT - 1:02d}"


def test_every_source_the_file_opts_in_can_give_topics() -> None:
    # A row that carries the key but is skipped by official_topics would look switched on
    # and never give a topic: not first-party, off, or read from its feed summary.
    opted_in = [
        row
        for row in sources_cli.load_file(sources_cli.DEFAULT_FILE)
        if topics.OFFICIAL_KEY in row.config
    ]
    assert [row.name for row in opted_in] == [
        "Claude blog",
        "Claude developer blog",
        "Anthropic engineering",
        "GitHub Changelog",
        "Cursor changelog",
    ]
    for row in opted_in:
        assert row.config[topics.OFFICIAL_KEY] is True, row.name
        assert row.enabled and row.is_first_party, row.name
        assert not row.config.get("evidence_from_feed_summary"), row.name


def _stub_other_sources(monkeypatch: pytest.MonkeyPatch, search: list[TopicView]) -> None:
    async def site_topics(session: AsyncSession) -> list[TopicView]:
        return [
            TopicView(
                source="site",
                title="站上的新聞",
                summary="",
                url="https://mokaair.com/zh-TW/life/a-story",
                slug="a-story",
            )
        ]

    async def search_topics(*args: Any, **kwargs: Any) -> tuple[list[TopicView], list[str]]:
        return search, []

    monkeypatch.setattr(topics, "site_topics", site_topics)
    monkeypatch.setattr(topics, "search_topics", search_topics)


@pytest.mark.asyncio
async def test_gather_puts_official_pages_between_the_site_and_the_search(
    session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = await _source(session, "Claude developer blog")
    # gather_topics reads the clock itself, so this candidate is dated from the real one.
    await _candidate(session, source, PAGE, created_at=datetime.now(UTC) - timedelta(hours=3))
    # A source the owner opted in although it is read from its feed summary: its entry is
    # not a topic, and the reason reaches the endpoint's notes beside the other topics.
    changelog = await _source(
        session,
        "Claude Code changelog",
        config_json={"video_topics": True, "evidence_from_feed_summary": True},
    )
    await _candidate(
        session,
        changelog,
        "https://code.claude.com/docs/en/changelog#2-1-296",
        created_at=datetime.now(UTC) - timedelta(hours=2),
    )
    search = [
        TopicView(source="search", title="The same page, found again", summary="", url=PAGE),
        TopicView(source="search", title="Another page", summary="", url="https://other.example/a"),
    ]
    _stub_other_sources(monkeypatch, search)
    row: Any = SimpleNamespace(topic_from_site=True, topic_from_search=True, topic_scope=["AI"])

    out = await topics.gather_topics(session, SimpleNamespace(), SimpleNamespace(), row)  # type: ignore[arg-type]

    assert [(topic.source, topic.url) for topic in out.topics] == [
        ("site", "https://mokaair.com/zh-TW/life/a-story"),
        ("official", PAGE),
        ("search", "https://other.example/a"),
    ]
    assert len(out.notes) == 1 and "Claude Code changelog" in out.notes[0]


@pytest.mark.asyncio
async def test_gather_is_unchanged_while_no_source_opts_in(
    session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    # As shipped: sources.json may carry the key, but nothing does on the host until it is
    # loaded there, and until then the planner must get exactly what it got before.
    source = await _source(session, "Not opted in", config_json={})
    await _candidate(session, source, PAGE, created_at=datetime.now(UTC) - timedelta(hours=3))
    search = [TopicView(source="search", title="A page", summary="", url=PAGE)]
    _stub_other_sources(monkeypatch, search)
    row: Any = SimpleNamespace(topic_from_site=True, topic_from_search=True, topic_scope=["AI"])

    out = await topics.gather_topics(session, SimpleNamespace(), SimpleNamespace(), row)  # type: ignore[arg-type]

    assert [topic.source for topic in out.topics] == ["site", "search"]
    assert out.notes == []
