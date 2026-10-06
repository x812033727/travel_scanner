"""Reopening earlier candidates that old rules or old models stopped (owner request, 2026-09-26).

The second half is the review judge's backlog (owner decision, 2026-10-06): the stories that
were already waiting in the review queue or the redraft list when AI review was switched on
are handed to the judge in batches, and nothing about them is reopened.
"""

from __future__ import annotations

import itertools
import json
import sys
from collections.abc import AsyncIterator
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import fakeredis
import pytest
from rq import Queue
from sqlalchemy import Table, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.models import AdminAuditLog, User
from app.news_automation import backfill_cli, jobs, judge
from app.news_automation.models import (
    LOCALES,
    NewsAssessment,
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsPipelineRun,
    NewsSource,
)
from app.news_automation.pipeline import JEV_QUOTA_PAUSED
from tests.test_news_pipeline import NEWS_TABLES


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
        jobs,
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


@pytest.mark.asyncio
async def test_jev_quota_holds_are_reopened_paused_and_not_queued(
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
            NewsAssessment.__table__,
            AdminAuditLog.__table__,
        ],
    )
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    published = datetime(2026, 9, 25, tzinfo=UTC)
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
        quota = _candidate(source, "manual_review", "news_duplicate_uncertain", published)
        uncertain = _candidate(source, "manual_review", "news_duplicate_uncertain", published)
        session.add_all([quota, uncertain])
        await session.flush()
        for row, reasons in (
            (quota, ["quota_unavailable"]),
            (uncertain, ["semantic_duplicate_uncertain"]),
        ):
            session.add(
                NewsAssessment(
                    candidate_id=row.id,
                    assessment_type="duplicate",
                    verdict="manual",
                    reasons_json=reasons,
                    prompt_version="v1",
                )
            )
        await session.commit()
        quota_id, uncertain_id = quota.id, uncertain.id

    queued: list[UUID] = []
    monkeypatch.setattr(backfill_cli, "SessionFactory", factory)
    monkeypatch.setattr(backfill_cli, "engine", engine)
    monkeypatch.setattr(
        jobs,
        "enqueue_candidate",
        lambda candidate_id, retry_count=0: queued.append(candidate_id) or "job",
    )

    report = await backfill_cli.run(
        since=date(2026, 9, 1),
        limit=None,
        apply=True,
        actor_email="owner@example.com",
        reason="Jev budget",
        jev_quota=True,
    )
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'news.db'}")
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        rows = {row.id: row for row in await session.scalars(select(NewsCandidate))}
    await engine.dispose()

    assert (report["candidates"], report["applied"], report["waits_for"]) == (1, True, "00:00 UTC")
    assert queued == [], "the orphan sweep runs them once the budget resets"
    assert (rows[quota_id].status, rows[quota_id].error_code) == ("discovered", JEV_QUOTA_PAUSED)
    assert rows[uncertain_id].status == "manual_review", (
        "a real uncertain check stays for an editor"
    )


@pytest.mark.asyncio
async def test_refetch_source_rereads_not_newsworthy_stories_and_queues_the_readable_ones(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """2026-09-28: the extractor kept only tag lists, so the writer rejected real stories."""
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
    published = datetime(2026, 9, 25, tzinfo=UTC)
    async with factory() as session:
        session.add(User(email="owner@example.com", password_hash="unused", is_admin=True))
        blog = NewsSource(
            name="Blog",
            url="https://blog.example/rss",
            format="rss",
            role="evidence",
            vertical="tech",
            is_first_party=True,
            enabled=True,
        )
        other = NewsSource(
            name="Other",
            url="https://other.example/rss",
            format="rss",
            role="evidence",
            vertical="tech",
            enabled=True,
        )
        session.add_all([blog, other])
        await session.flush()
        readable = _candidate(blog, "rejected", "news_not_eligible", published)
        gone = _candidate(blog, "rejected", "news_not_eligible", published)
        by_person = _candidate(blog, "rejected", "news_not_eligible", published)
        elsewhere = _candidate(other, "rejected", "news_not_eligible", published)
        for row in (readable, gone, elsewhere):
            row.human_decision = None
        session.add_all([readable, gone, by_person, elsewhere])
        await session.flush()
        for row, path in ((readable, "ok"), (gone, "gone")):
            session.add(
                NewsEvidence(
                    candidate_id=row.id,
                    role="evidence",
                    is_first_party=True,
                    url=f"https://blog.example/{path}",
                    title="Post",
                    content_hash="h" * 64,
                    excerpt="AI | Security | All tags",
                )
            )
        await session.commit()
        readable_id, gone_id = readable.id, gone.id

    async def refresh(
        session: Any, evidence: list[NewsEvidence], **_kwargs: Any
    ) -> tuple[list[str], list[str]]:
        if any(row.url.endswith("/gone") for row in evidence):
            return [], ["source_refetch_failed:https://blog.example/gone:HTTPStatusError"]
        for row in evidence:
            row.excerpt = "The story body."
        return [row.url for row in evidence], []

    queued: list[UUID] = []
    monkeypatch.setattr(backfill_cli, "SessionFactory", factory)
    monkeypatch.setattr(backfill_cli, "engine", engine)
    monkeypatch.setattr(backfill_cli, "refresh_evidence", refresh)
    monkeypatch.setattr(backfill_cli, "get_redis", lambda: None)
    monkeypatch.setattr(
        jobs,
        "enqueue_candidate",
        lambda candidate_id, retry_count=0: queued.append(candidate_id) or "job",
    )

    listed = await backfill_cli.run(
        since=date(2026, 9, 20),
        limit=None,
        apply=False,
        actor_email=None,
        reason="Refetch",
        refetch_sources=["Blog"],
    )
    assert listed["candidates"] == 2, "the person's rejection and the other source stay out"

    applied = await backfill_cli.run(
        since=date(2026, 9, 20),
        limit=None,
        apply=True,
        actor_email="owner@example.com",
        reason="Refetch",
        refetch_sources=["Blog"],
    )
    assert queued == [readable_id]
    assert applied["queued"] == 1
    assert list(applied["refetch_problems"]) == [str(gone_id)]
    async with factory() as session:
        rows = {row.id: row for row in await session.scalars(select(NewsCandidate))}
        excerpt = await session.scalar(
            select(NewsEvidence.excerpt).where(NewsEvidence.candidate_id == readable_id)
        )
    await engine.dispose()
    assert (rows[readable_id].status, rows[readable_id].error_code) == ("discovered", None)
    assert (rows[gone_id].status, rows[gone_id].error_code) == ("rejected", "news_not_eligible")
    assert excerpt == "The story body."


Factory = async_sessionmaker[AsyncSession]
SINCE = date(2026, 10, 1)
DRAFT_READY = "news_zh_draft_ready"
UNVERIFIED = "news_verification_failed"
# Text of the flow before articles were saved on a failed check: five locales, no article.
FIVE_LOCALES = {locale: {"title": locale} for locale in LOCALES}
# Each pool flag with the value it takes, if any.
POOL_FLAGS: dict[str, list[str]] = {
    "--jev-quota-holds": [],
    "--refetch-source": ["Blog"],
    "--resume-saved-bundles": [],
    "--judge-holds": [],
    "--judge-redrafts": [],
}


@pytest.mark.parametrize(("first", "second"), list(itertools.combinations(POOL_FLAGS, 2)))
def test_a_run_takes_one_pool(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], first: str, second: str
) -> None:
    run = AsyncMock(return_value={})
    monkeypatch.setattr(backfill_cli, "run", run)
    flags = [first, *POOL_FLAGS[first], second, *POOL_FLAGS[second]]
    monkeypatch.setattr(sys, "argv", ["backfill_cli", "--since", "2026-10-01", *flags])

    with pytest.raises(SystemExit) as refused:
        backfill_cli.main()

    assert refused.value.code == 2
    assert "not allowed with argument" in capsys.readouterr().err
    run.assert_not_called()


def test_one_pool_named_twice_is_still_one_pool(monkeypatch: pytest.MonkeyPatch) -> None:
    run = AsyncMock(return_value={})
    monkeypatch.setattr(backfill_cli, "run", run)
    sources = ["--refetch-source", "Blog", "--refetch-source", "Press"]
    monkeypatch.setattr(sys, "argv", ["backfill_cli", "--since", "2026-09-20", *sources])

    backfill_cli.main()

    assert run.call_args is not None
    assert run.call_args.kwargs["refetch_sources"] == ["Blog", "Press"]


@pytest.mark.parametrize(
    ("flags", "pool"),
    [([], None), (["--judge-holds"], "holds"), (["--judge-redrafts"], "redrafts")],
)
def test_the_command_line_names_the_judges_pool_and_asks_for_no_actor(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    flags: list[str],
    pool: str | None,
) -> None:
    run = AsyncMock(return_value={"applied": False})
    monkeypatch.setattr(backfill_cli, "run", run)
    typed = ["backfill_cli", "--since", "2026-10-01", "--limit", "5", "--apply", *flags]
    monkeypatch.setattr(sys, "argv", typed)

    backfill_cli.main()

    assert run.call_args is not None
    options = run.call_args.kwargs
    assert (options["judge_pool"], options["since"], options["limit"], options["apply"]) == (
        pool,
        SINCE,
        5,
        True,
    )
    assert options["actor_email"] is None
    assert (options["jev_quota"], options["refetch_sources"], options["saved_bundles"]) == (
        False,
        None,
        False,
    )
    assert json.loads(capsys.readouterr().out) == {"applied": False}


@pytest.fixture
async def news(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[Factory]:
    """Every news table, in a file: the CLI disposes the engine it is given.

    The judge's four switches are on for AI and technology; crypto may not publish on its
    own, so the judge does not act there.
    """

    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'news.db'}")
    tables = cast(list[Table], [model.__table__ for model in NEWS_TABLES])
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        session.add(
            NewsAutomationSettings(
                id=1,
                enabled=True,
                mode="automatic",
                auto_publish_ai=True,
                auto_publish_tech=True,
                judge_enabled=True,
            )
        )
        session.add(User(email="owner@example.com", password_hash="unused", is_admin=True))
        await session.commit()
    monkeypatch.setattr(backfill_cli, "SessionFactory", factory)
    monkeypatch.setattr(backfill_cli, "engine", engine)
    yield factory
    await engine.dispose()


async def feed(session: AsyncSession) -> NewsSource:
    source = NewsSource(
        name="Feed", url="https://news.example/feed", format="rss", role="evidence", vertical="ai"
    )
    session.add(source)
    await session.flush()
    return source


def held(source: NewsSource, status: str, hold: str, day: int, **changes: Any) -> NewsCandidate:
    """A candidate that came in on that day of October 2026 and rests in ``hold``."""

    row = _candidate(source, status, hold, datetime(2026, 10, day, tzinfo=UTC))
    row.human_decision = None
    row.created_at = datetime(2026, 10, day, 12, tzinfo=UTC)
    for name, value in changes.items():
        setattr(row, name, value)
    return row


def saved_article() -> dict[str, Any]:
    """What a finished article leaves on its candidate: the article, and the five locales
    there as well. The old flow's stored text is five locales without an article."""

    return {"guide_article_id": uuid4(), "draft_bundle_json": FIVE_LOCALES}


def judge_queue(monkeypatch: pytest.MonkeyPatch) -> Queue:
    """RQ on an in-memory Redis, so a job id queued twice is refused as in production. A
    candidate job would mean the story was reopened, which the judge's pools never do."""

    queue = Queue("news", connection=fakeredis.FakeStrictRedis())
    monkeypatch.setattr(jobs, "_queue", lambda: (Mock(), queue))
    reopened = Mock(side_effect=AssertionError("a candidate was queued to run again"))
    monkeypatch.setattr(jobs, "enqueue_candidate", reopened)
    return queue


async def everything(factory: Factory) -> dict[str, Any]:
    """Whatever a backfill could write: each candidate column by column, and how many
    audit rows, runs, assessments and settings rows there are."""

    columns = [attribute.key for attribute in inspect(NewsCandidate).column_attrs]
    counted: tuple[Any, ...] = (
        AdminAuditLog,
        NewsPipelineRun,
        NewsAssessment,
        NewsAutomationSettings,
    )
    async with factory() as session:
        stored: dict[str, Any] = {
            "candidates": {
                row.id: {name: getattr(row, name) for name in columns}
                for row in await session.scalars(select(NewsCandidate))
            }
        }
        for model in counted:
            stored[model.__name__] = len(list(await session.scalars(select(model.id))))
    return stored


async def listing(pool: str, limit: int | None = None, *, apply: bool = False) -> dict[str, Any]:
    return await backfill_cli.run(
        since=SINCE,
        limit=limit,
        apply=apply,
        actor_email=None,
        reason="Not used by the judge's pools",
        judge_pool=cast(Any, pool),
    )


@pytest.mark.asyncio
async def test_listing_the_review_queue_says_what_the_judge_would_be_asked_and_writes_nothing(
    news: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    queue = judge_queue(monkeypatch)
    async with news() as session:
        source = await feed(session)
        draft = held(source, "manual_review", DRAFT_READY, 5)
        unsure = held(source, "manual_review", "news_duplicate_uncertain", 4, vertical="tech")
        last_call = held(source, "manual_review", "news_jev_final_hold", 3, **saved_article())
        # A source that gives no publication date: the story waits in the list all the same.
        undated = held(source, "manual_review", "news_ready_to_publish", 2, **saved_article())
        undated.source_published_at = None
        answered = held(
            source, "manual_review", DRAFT_READY, 5, judge_hold=DRAFT_READY, judge_decision="manual"
        )
        crypto = held(source, "manual_review", DRAFT_READY, 5, vertical="crypto")
        legacy = held(
            source, "manual_review", "news_duplicate_uncertain", 4, draft_bundle_json=FIVE_LOCALES
        )
        # The final editor held it after a person confirmed it: nothing is left to decide.
        confirmed = held(
            source,
            "manual_review",
            "news_final_edit_hold",
            4,
            human_decision="publish",
            **saved_article(),
        )
        # The 90-day cleanup has emptied its evidence: nothing to read the draft against.
        expired = held(source, "manual_review", DRAFT_READY, 3)
        # Not this pool: holds that are the owner's work, the other list, and an older story.
        hard_checks = held(source, "manual_review", "news_hard_checks_failed", 5)
        changed = held(source, "manual_review", "news_evidence_changed", 5)
        stopped = held(source, "needs_redraft", UNVERIFIED, 5)
        older = held(source, "manual_review", DRAFT_READY, 1)
        older.created_at = datetime(2026, 9, 30, 23, tzinfo=UTC)
        session.add_all(
            [draft, unsure, last_call, undated, answered, crypto, legacy, confirmed, expired]
            + [hard_checks, changed, stopped, older]
        )
        await session.flush()
        session.add(
            NewsEvidence(
                candidate_id=expired.id,
                role="evidence",
                url="https://news.example/expired",
                title="Post",
                content_hash="h" * 64,
                excerpt=judge.EXPIRED_EXCERPT,
            )
        )
        await session.commit()
    before = await everything(news)

    listed = await listing("holds")
    first_two = await listing("holds", 2)

    assert (listed["pool"], listed["since"], listed["applied"]) == (
        "judge_holds",
        "2026-10-01",
        False,
    )
    assert (listed["held"], listed["eligible"], listed["candidates"]) == (9, 4, 4)
    # Newest first.
    assert [row["id"] for row in listed["rows"]] == [
        str(row.id) for row in (draft, unsure, last_call, undated)
    ]
    assert listed["rows"][0] == {
        "id": str(draft.id),
        "created": "2026-10-05",
        "vertical": "ai",
        "hold": DRAFT_READY,
        "title": draft.source_title,
    }
    assert listed["by_hold"] == {
        DRAFT_READY: 1,
        "news_duplicate_uncertain": 1,
        "news_jev_final_hold": 1,
        "news_ready_to_publish": 1,
    }
    assert listed["by_vertical"] == {"ai": 3, "tech": 1}
    assert listed["excluded"] == {
        "answered": {"ai": 1},
        "gate_off": {"crypto": 1},
        "legacy_bundle": {"ai": 1},
        "person_decided": {"ai": 1},
        "evidence_expired": {"ai": 1},
    }
    assert listed["switches"] == {
        "enabled": True,
        "automatic_mode": True,
        "judge_enabled": True,
        "auto_publish": {"ai": True, "tech": True, "crypto": False},
    }
    assert "warning" not in listed
    # A limit cuts the batch, not what is known about the list.
    assert (first_two["held"], first_two["eligible"], first_two["candidates"]) == (9, 4, 2)
    assert [row["id"] for row in first_two["rows"]] == [str(draft.id), str(unsure.id)]
    assert first_two["by_hold"] == {DRAFT_READY: 1, "news_duplicate_uncertain": 1}
    assert first_two["excluded"] == listed["excluded"]
    assert await everything(news) == before
    assert queue.job_ids == []


@pytest.mark.asyncio
async def test_listing_the_redraft_list_names_every_reason_a_story_is_left_to_the_owner(
    news: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    queue = judge_queue(monkeypatch)
    async with news() as session:
        source = await feed(session)
        stopped = held(source, "needs_redraft", UNVERIFIED, 5)
        dated = held(source, "needs_redraft", "news_event_date_invalid", 4, vertical="tech")
        saved = held(
            source, "needs_redraft", "news_locale_review_failed", 3, guide_article_id=uuid4()
        )
        confirmed = held(
            source, "needs_redraft", "news_claim_source_invalid", 3, human_decision="publish"
        )
        expired = held(source, "needs_redraft", UNVERIFIED, 3)
        capped = held(source, "needs_redraft", UNVERIFIED, 3)
        legacy = held(
            source, "needs_redraft", "news_locale_review_failed", 3, draft_bundle_json=FIVE_LOCALES
        )
        handed_back = held(
            source, "needs_redraft", UNVERIFIED, 3, judge_hold=UNVERIFIED, judge_decision="manual"
        )
        # Not this pool: the writer declined a rewrite the judge ordered, a stored article
        # for --resume-saved-bundles, and the review queue.
        declined = held(source, "needs_redraft", "news_not_eligible", 5)
        bundle = held(source, "needs_redraft", "news_hard_checks_failed", 5)
        review = held(source, "manual_review", DRAFT_READY, 5)
        session.add_all(
            [stopped, dated, saved, confirmed, expired, capped, legacy, handed_back]
            + [declined, bundle, review]
        )
        await session.flush()
        session.add(
            NewsEvidence(
                candidate_id=expired.id,
                role="evidence",
                url="https://news.example/expired",
                title="Post",
                content_hash="h" * 64,
                excerpt=judge.EXPIRED_EXCERPT,
            )
        )
        for _ in range(judge.MAX_JUDGE_REWRITES):
            session.add(
                NewsAssessment(
                    candidate_id=capped.id,
                    assessment_type="judge",
                    verdict="revise",
                    reasons_json=["Drop the launch date."],
                    prompt_version="v1",
                )
            )
        await session.commit()
    before = await everything(news)

    listed = await listing("redrafts")

    assert (listed["pool"], listed["held"], listed["eligible"]) == ("judge_redrafts", 8, 2)
    assert [row["id"] for row in listed["rows"]] == [str(stopped.id), str(dated.id)]
    assert listed["by_hold"] == {UNVERIFIED: 1, "news_event_date_invalid": 1}
    assert listed["by_vertical"] == {"ai": 1, "tech": 1}
    assert listed["excluded"] == {
        "has_article": {"ai": 1},
        "person_decided": {"ai": 1},
        "evidence_expired": {"ai": 1},
        "rewrite_cap": {"ai": 1},
        "legacy_bundle": {"ai": 1},
        "answered": {"ai": 1},
    }
    assert await everything(news) == before
    assert queue.job_ids == []


@pytest.mark.asyncio
@pytest.mark.parametrize("settings", ["switched-off", "never-saved"])
async def test_with_ai_review_off_the_listing_says_so_and_a_batch_queues_nothing(
    news: Factory, monkeypatch: pytest.MonkeyPatch, settings: str
) -> None:
    queue = judge_queue(monkeypatch)
    async with news() as session:
        row = await session.get(NewsAutomationSettings, 1)
        assert row is not None
        if settings == "switched-off":
            row.judge_enabled = False
        else:
            await session.delete(row)
        source = await feed(session)
        session.add_all(
            [
                held(source, "manual_review", DRAFT_READY, 5),
                held(source, "manual_review", DRAFT_READY, 4, vertical="tech"),
                # A reason no switch lifts is named ahead of the closed gate.
                held(
                    source,
                    "manual_review",
                    "news_duplicate_uncertain",
                    4,
                    draft_bundle_json=FIVE_LOCALES,
                ),
            ]
        )
        await session.commit()
    before = await everything(news)

    listed = await listing("holds")
    applied = await listing("holds", 5, apply=True)

    assert listed["switches"]["judge_enabled"] is False
    assert "judge_enabled is off" in listed["warning"]
    assert (listed["held"], listed["eligible"], listed["rows"]) == (3, 0, [])
    assert listed["excluded"] == {"gate_off": {"ai": 1, "tech": 1}, "legacy_bundle": {"ai": 1}}
    assert (applied["applied"], applied["candidates"]) == (False, 0)
    assert "queued" not in applied
    # Reading the switches does not save a settings row that was never there.
    assert before["NewsAutomationSettings"] == (1 if settings == "switched-off" else 0)
    assert await everything(news) == before
    assert queue.job_ids == []


@pytest.mark.asyncio
async def test_releasing_a_batch_only_queues_judge_jobs_and_needs_a_limit(
    news: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    queue = judge_queue(monkeypatch)
    # A fixed clock: the batch's tag is the hour, and two runs must not straddle one.
    now = datetime(2026, 10, 6, 9, 10, tzinfo=UTC)
    clock = Mock(side_effect=datetime)
    clock.now.return_value = now
    monkeypatch.setattr(backfill_cli, "datetime", clock)
    async with news() as session:
        source = await feed(session)
        newest = held(source, "manual_review", DRAFT_READY, 5)
        rerun = held(
            source, "manual_review", "news_jev_final_hold", 4, retry_count=2, **saved_article()
        )
        oldest = held(source, "manual_review", DRAFT_READY, 3)
        answered = held(
            source, "manual_review", DRAFT_READY, 5, judge_hold=DRAFT_READY, judge_decision="manual"
        )
        session.add_all([newest, rerun, oldest, answered])
        await session.commit()
    before = await everything(news)
    tag = f"backfill-{int(now.timestamp() // 3600)}"
    batch = [
        f"news-judge-{newest.id}-0-{DRAFT_READY}-{tag}",
        f"news-judge-{rerun.id}-2-news_jev_final_hold-{tag}",
    ]

    # The backlog goes out in batches the owner sized, never all at once.
    with pytest.raises(SystemExit, match="--limit is required with --apply"):
        await listing("holds", apply=True)
    with pytest.raises(SystemExit, match="at least 1"):
        await listing("holds", 0, apply=True)
    assert queue.job_ids == []

    applied = await listing("holds", 2, apply=True)
    again = await listing("holds", 2, apply=True)

    assert (applied["applied"], applied["candidates"]) == (True, 2)
    assert (applied["queued"], applied["already_queued"]) == (2, 0)
    assert queue.job_ids == batch
    job = queue.fetch_job(batch[0])
    assert job is not None and job.func_name == "app.news_automation.jobs.run_judge"
    # The same batch asked for again within the hour is not paid for twice.
    assert (again["applied"], again["queued"], again["already_queued"]) == (True, 0, 2)
    # No candidate row, audit row, run or assessment: nothing was reopened, and no
    # administrator was named.
    assert await everything(news) == before


@pytest.mark.asyncio
async def test_a_plain_backfill_leaves_what_the_judge_rejected_or_handed_back(
    news: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    published = datetime(2026, 10, 3, tzinfo=UTC)
    async with news() as session:
        source = await feed(session)
        unjudged = _candidate(source, "needs_redraft", UNVERIFIED, published)
        handed_back = _candidate(source, "needs_redraft", UNVERIFIED, published)
        handed_back.judge_decision, handed_back.judge_hold = "manual", UNVERIFIED
        closed = _candidate(source, "rejected", UNVERIFIED, published)
        closed.human_decision = None
        closed.judge_decision, closed.judge_hold = "reject", UNVERIFIED
        session.add_all([unjudged, handed_back, closed])
        await session.commit()
        unjudged_id, handed_back_id, closed_id = unjudged.id, handed_back.id, closed.id
    queued: list[UUID] = []
    monkeypatch.setattr(
        jobs,
        "enqueue_candidate",
        lambda candidate_id, retry_count=0: queued.append(candidate_id) or "job",
    )

    listed = await backfill_cli.run(
        since=SINCE, limit=None, apply=False, actor_email=None, reason="Backfill"
    )
    await backfill_cli.run(
        since=SINCE, limit=None, apply=True, actor_email="owner@example.com", reason="Backfill"
    )

    async with news() as session:
        rows = {row.id: row for row in await session.scalars(select(NewsCandidate))}
    assert listed["candidates"] == 1
    assert queued == [unjudged_id]
    assert rows[unjudged_id].status == "discovered"
    # Their stop code is one the backfill reopens; the judge's answer is what keeps them out.
    assert (rows[handed_back_id].status, rows[handed_back_id].judge_decision) == (
        "needs_redraft",
        "manual",
    )
    assert (rows[closed_id].status, rows[closed_id].judge_decision) == ("rejected", "reject")
