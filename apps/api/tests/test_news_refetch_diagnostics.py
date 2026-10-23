"""A source that cannot be read again says why: an HTTP status, a robots refusal, or nothing more.

Kept apart from test_news_automation.py, which an open draft extends heavily.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import httpx
import pytest

from app.news_automation.fetch import UnsafeNewsUrl
from app.news_automation.models import NewsEvidence, NewsSource
from app.news_automation.schemas import FetchResult
from app.news_automation.validation import refresh_evidence, revalidate_evidence

URL = "https://www.cftc.gov/PressRoom/PressReleases/9999-26"


def _status(code: int) -> httpx.HTTPStatusError:
    request = httpx.Request("GET", URL)
    response = httpx.Response(code, request=request, headers={"cf-ray": "abc", "set-cookie": "s=1"})
    return httpx.HTTPStatusError(f"Client error '{code}'", request=request, response=response)


def _source() -> NewsSource:
    return NewsSource(
        last_scanned_at=datetime.now(UTC) - timedelta(days=1),
        name="CFTC press releases",
        url="https://www.cftc.gov/PressRoom/PressReleases",
        format="html",
        role="evidence",
        vertical="crypto",
        is_first_party=True,
        enabled=True,
    )


def _evidence() -> NewsEvidence:
    return NewsEvidence(
        candidate_id=uuid4(),
        role="evidence",
        is_first_party=True,
        url=URL,
        title="CFTC release",
        content_hash="old",
        excerpt="Old text.",
    )


def _session() -> AsyncMock:
    session = AsyncMock()
    session.scalars.return_value = [_source()]
    return session


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("error", "reason"),
    [
        (_status(403), f"source_refetch_failed:{URL}:HTTPStatusError:article:http_403"),
        (_status(503), f"source_refetch_failed:{URL}:HTTPStatusError:article:http_503"),
        (
            UnsafeNewsUrl("robots.txt did not permit this fetch"),
            f"source_refetch_failed:{URL}:UnsafeNewsUrl:article:robots_refused",
        ),
        (
            UnsafeNewsUrl("unsupported content type: application/pdf"),
            f"source_refetch_failed:{URL}:UnsafeNewsUrl:article:content_type",
        ),
        (
            UnsafeNewsUrl("news source resolved to a non-public address"),
            f"source_refetch_failed:{URL}:UnsafeNewsUrl:article:unsafe_url",
        ),
        # Nothing more is known: the reason keeps its earlier form.
        (TimeoutError(), f"source_refetch_failed:{URL}:TimeoutError"),
    ],
)
async def test_a_refetch_failure_names_the_stage_and_upstream_status(
    error: BaseException, reason: str
) -> None:
    for check in (revalidate_evidence, refresh_evidence):
        fetcher = AsyncMock()
        fetcher.fetch.side_effect = error
        _, reasons = await check(_session(), [_evidence()], fetcher=fetcher)  # type: ignore[operator]
        assert reasons == [reason], check.__name__
        # Bounded and safe: no response headers or cookies, whatever the upstream sent.
        assert "cf-ray" not in reasons[0] and "set-cookie" not in reasons[0]


@pytest.mark.asyncio
async def test_a_page_that_reads_but_says_something_else_is_still_changed_content() -> None:
    fetcher = AsyncMock()
    fetcher.fetch.return_value = FetchResult(
        url=URL,
        status_code=200,
        content_type="text/html",
        body=f"<html><main>{'A different release altogether. ' * 20}</main></html>".encode(),
    )
    still, reasons = await revalidate_evidence(_session(), [_evidence()], fetcher=fetcher)
    assert still is False
    assert reasons == [f"source_content_changed:{URL}"]
