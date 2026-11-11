from __future__ import annotations

from datetime import UTC, datetime
from typing import cast
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.news_automation.fetch import SafeNewsFetcher
from app.news_automation.freshness import MAX_EVIDENCE, check_evidence, run_checks
from app.news_automation.models import NewsEvidence
from app.news_automation.scheduler import enqueue_freshness


def evidence(index: int = 0) -> NewsEvidence:
    return NewsEvidence(
        id=uuid4(),
        candidate_id=uuid4(),
        role="evidence",
        is_first_party=True,
        url=f"https://official.example/story/{index}",
        title="Original title",
        retrieved_at=datetime(2026, 10, 1, tzinfo=UTC),
        source_date=None,
        etag="original-etag",
        last_modified="original-modified",
        content_hash="a" * 64,
        body_hash="body-v1:" + "b" * 64,
        excerpt="Original publication evidence",
    )


@pytest.mark.asyncio
async def test_advisory_revalidation_never_mutates_publication_evidence() -> None:
    original = evidence()
    before = {key: value for key, value in vars(original).items() if not key.startswith("_")}
    session = AsyncMock(spec=AsyncSession)
    fetcher = Mock(spec=SafeNewsFetcher)

    async def revalidate(actual_session, copies, **kwargs):  # type: ignore[no-untyped-def]
        assert actual_session is session
        assert kwargs["fetcher"] is fetcher
        assert copies[0] is not original
        copies[0].retrieved_at = datetime.now(UTC)
        copies[0].etag = "new"
        copies[0].content_hash = "different"
        copies[0].excerpt = "different"
        return True, []

    with patch("app.news_automation.freshness.revalidate_evidence", side_effect=revalidate):
        result = await check_evidence(session, [original], fetcher)
    assert result.status == "unchanged"
    assert before == {
        key: value for key, value in vars(original).items() if not key.startswith("_")
    }
    session.add.assert_not_called()
    session.commit.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "reason,expected",
    [
        ("source_content_changed", "changed"),
        ("source_disabled_or_unlisted", "unverified"),
        ("source_policy_changed", "unverified"),
        ("source_became_unreadable", "unverified"),
        ("source_refetch_failed", "unverified"),
    ],
)
async def test_source_failure_is_not_reported_as_expired(reason: str, expected: str) -> None:
    row = evidence()
    with patch(
        "app.news_automation.freshness.revalidate_evidence",
        new=AsyncMock(return_value=(False, [f"{reason}:{row.url}"])),
    ):
        result = await check_evidence(AsyncMock(), [row], Mock())
    assert result.status == expected
    assert result.changed_sources == int(expected == "changed")


@pytest.mark.asyncio
async def test_evidence_limit_does_not_claim_full_verification() -> None:
    rows = [evidence(i) for i in range(MAX_EVIDENCE + 1)]
    revalidate = AsyncMock(return_value=(True, []))
    with patch("app.news_automation.freshness.revalidate_evidence", new=revalidate):
        result = await check_evidence(AsyncMock(), rows, Mock())
    assert len(revalidate.call_args.args[1]) == MAX_EVIDENCE
    assert result.status == "unverified"
    assert result.total_sources == MAX_EVIDENCE + 1


@pytest.mark.asyncio
async def test_empty_evidence_and_timeout_are_unverified() -> None:
    revalidate = AsyncMock(side_effect=TimeoutError)
    with patch("app.news_automation.freshness.revalidate_evidence", new=revalidate):
        empty = await check_evidence(AsyncMock(), [], Mock())
        timed_out = await check_evidence(AsyncMock(), [evidence()], Mock())
    assert empty.status == timed_out.status == "unverified"
    assert timed_out.checked_sources == 0
    assert revalidate.await_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("settings", [None, Mock(enabled=False)])
async def test_disabled_automation_does_not_query_candidates_or_fetch(settings: object) -> None:
    session = AsyncMock(spec=AsyncSession)
    session.get.return_value = settings
    fetcher = Mock(spec=SafeNewsFetcher)
    assert await run_checks(cast(AsyncSession, session), fetcher) == 0
    session.scalars.assert_not_called()
    fetcher.fetch.assert_not_called()


def test_scheduler_has_daily_identity_and_no_retry() -> None:
    queue = Mock()
    queue.fetch_job.return_value = None
    enqueue_freshness(queue, "2026-11-10")
    queue.enqueue.assert_called_once_with(
        "app.news_automation.jobs.run_freshness",
        job_id="news-freshness-2026-11-10",
        job_timeout=900,
        result_ttl=86_400,
        failure_ttl=604_800,
    )
    queue.fetch_job.return_value = Mock()
    enqueue_freshness(queue, "2026-11-10")
    assert queue.enqueue.call_count == 1
