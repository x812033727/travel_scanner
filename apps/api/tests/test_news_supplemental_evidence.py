"""Bounded official documentation adds detail, not another independent publisher."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import httpx
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db import Base
from app.news_automation.feeds import read_article
from app.news_automation.fetch import SafeNewsFetcher, UnsafeNewsUrl
from app.news_automation.models import (
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsSource,
)
from app.news_automation.policy import (
    auto_evidence_ok,
    body_fingerprint,
    content_fingerprint,
    evidence_site_count,
    evidence_sufficient,
)
from app.news_automation.scanner import NON_ARTICLE_SUFFIXES, scan_source
from app.news_automation.schemas import FetchResult
from app.news_automation.supplemental import is_supplemental_url, supplemental_urls

ORIGIN = "https://official.example"
LEAD = ORIGIN + "/news/release"
ONE = ORIGIN + "/support/one"
TWO = ORIGIN + "/support/two"
THREE = ORIGIN + "/support/three"
DEEP = ORIGIN + "/support/deep"


def _source(**changes: Any) -> NewsSource:
    fields = {
        "name": "Official",
        "url": ORIGIN + "/feed",
        "format": "rss",
        "role": "evidence",
        "vertical": "tech",
        "enabled": True,
        "is_first_party": True,
        "last_scanned_at": datetime(2026, 1, 1, tzinfo=UTC),
        "allowed_redirect_hosts_json": ["other.example"],
        "config_json": {"supplemental_paths": ["/support/"]},
    }
    return NewsSource(**{**fields, **changes})


@pytest.mark.parametrize(
    "value",
    [None, False, "/support/", [], ["/"], ["//support"], ["support"],
     ["/support?x=1"], ["/support#x"], ["/support/../private"],
     ["/support/%2e%2e/private"], ["/support/", 3], ["/support/"] * 9,
     ["/" + "x" * 256]],
)
def test_malformed_or_absent_config_never_enables_supplemental_fetch(value: object) -> None:
    source = _source(config_json={"supplemental_paths": value})
    assert supplemental_urls(source, LEAD, [ONE]) == ()
    assert supplemental_urls(_source(config_json={}), LEAD, [ONE]) == ()


@pytest.mark.parametrize(
    "changes",
    [{"enabled": False}, {"is_first_party": False}, {"role": "lead_only"},
     {"url": "https://other.example/feed"}],
)
def test_only_the_enabled_first_party_evidence_source_owns_supplemental_paths(
    changes: dict[str, Any],
) -> None:
    assert supplemental_urls(_source(**changes), LEAD, [ONE]) == ()
    assert supplemental_urls(None, LEAD, [ONE]) == ()


@pytest.mark.parametrize(
    "url",
    ["http://official.example/support/a", "https://other.example/support/a",
     "https://sub.official.example/support/a", "https://official.example.evil.test/support/a",
     "https://user@official.example/support/a", "https://official.example:444/support/a",
     "https://official.example:support/a", "https://official.example/supportive/a",
     "https://official.example/support/../private", "https://official.example/support/%2fprivate",
     "https://official.example/support/%252eprivate", "https://official.example/support/\\private",
     "https://official.example/support/one\n", LEAD + "?tracking=1#second"],
)
def test_link_scope_is_https_exact_host_and_a_path_boundary(url: str) -> None:
    assert not is_supplemental_url(_source(), LEAD, url)


def test_selection_is_two_distinct_paths_and_never_synthesizes_or_follows_links() -> None:
    first = ONE + "?language=en#usage"
    links = [ORIGIN + "/support/chart.JPG", first, ONE + "?tracking=1", TWO, THREE]
    assert supplemental_urls(
        _source(), LEAD, links, excluded_suffixes=NON_ARTICLE_SUFFIXES
    ) == (first, TWO)
    assert is_supplemental_url(_source(config_json={"supplemental_paths": ["/support"]}), LEAD, ONE)


def test_configured_origin_without_a_path_still_owns_its_document_host() -> None:
    assert supplemental_urls(_source(url=ORIGIN), LEAD, [ONE]) == (ONE,)


def test_a_non_mapping_legacy_config_is_disabled() -> None:
    assert supplemental_urls(_source(config_json="/support/"), LEAD, [ONE]) == ()


def _page(text: str, links: list[str] | None = None) -> bytes:
    anchors = "".join(f'<a href="{url}">Documentation</a>' for url in links or [])
    return f"<html><main><h1>Official details</h1><p>{text}</p>{anchors}</main></html>".encode()


DOCUMENT_TEXT = "Eligibility and monthly usage are described in these official terms. " * 12


class RecordingFetcher:
    def __init__(self, pages: dict[str, FetchResult | Exception]) -> None:
        self.pages = pages
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.closed = False

    async def fetch(self, url: str, **kwargs: Any) -> FetchResult:
        self.calls.append((url, kwargs))
        response = self.pages[url]
        if isinstance(response, Exception):
            raise response
        return response

    async def close(self) -> None:
        self.closed = True


def _result(url: str, body: bytes) -> FetchResult:
    return FetchResult(
        url=url, status_code=200, content_type="text/html", body=body,
        etag='"docs-v1"', last_modified="Mon, 09 Nov 2026 00:00:00 GMT",
    )


async def _scan(
    links: list[str],
    *,
    config: dict[str, Any] | None = None,
    replacements: dict[str, FetchResult | Exception] | None = None,
) -> tuple[RecordingFetcher, list[NewsEvidence], str, int]:
    engine = create_async_engine("sqlite+aiosqlite://")
    try:
        async with engine.begin() as connection:
            await connection.run_sync(
                lambda sync: Base.metadata.create_all(sync, tables=[
                    NewsAutomationSettings.__table__, NewsSource.__table__,
                    NewsCandidate.__table__, NewsEvidence.__table__,
                ])
            )
        source = _source(**({"config_json": config} if config is not None else {}))
        pages = {
            source.url: _result(source.url, (
                f"<rss><channel><item><title>Release</title><link>{LEAD}</link>"
                "</item></channel></rss>"
            ).encode()),
            LEAD: _result(LEAD, _page("A new feature changes usage.", links)),
            ONE: _result(ONE, _page(DOCUMENT_TEXT, [DEEP])),
            TWO: _result(TWO, _page(DOCUMENT_TEXT + "Second page.")),
        }
        fetcher = RecordingFetcher({**pages, **(replacements or {})})
        queued: list[UUID] = []

        async def enqueue(candidate_id: UUID) -> None:
            queued.append(candidate_id)

        factory = async_sessionmaker(engine, expire_on_commit=False)
        async with factory() as session:
            session.add_all([NewsAutomationSettings(id=1, enabled=True), source])
            await session.commit()
            created = await scan_source(session, source.id, enqueue, fetcher=fetcher)  # type: ignore[arg-type]
            rows = list(await session.scalars(select(NewsEvidence)))
            assert created == len(queued)
            return fetcher, rows, source.last_status, created
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_scanner_defaults_off_without_changing_the_original_fetch_path() -> None:
    fetcher, rows, status, created = await _scan([ONE, TWO], config={})
    assert [url for url, _ in fetcher.calls] == [ORIGIN + "/feed", LEAD]
    assert [row.url for row in rows] == [LEAD]
    assert status == "succeeded" and created == 1


@pytest.mark.asyncio
async def test_scanner_stores_two_documents_with_hashes_without_changing_evidence_gate() -> None:
    fetcher, rows, status, created = await _scan([ONE, ONE, TWO, THREE])
    assert [url for url, _ in fetcher.calls] == [ORIGIN + "/feed", LEAD, ONE, TWO]
    assert {row.url for row in rows} == {LEAD, ONE, TWO}
    assert DEEP not in [url for url, _ in fetcher.calls]
    for url, kwargs in fetcher.calls[2:]:
        assert kwargs == {"allowed_hosts": {"official.example"}, "allowed_redirect_hosts": set()}
        row = next(row for row in rows if row.url == url)
        response = fetcher.pages[url]
        assert isinstance(response, FetchResult)
        page = read_article(response.body, url)
        assert row.content_hash == content_fingerprint(page.text)
        assert row.body_hash == body_fingerprint(page) is not None
        assert row.excerpt == page.text and row.etag == '"docs-v1"'
    lead = [row for row in rows if row.url == LEAD]
    assert evidence_site_count(rows) == evidence_site_count(lead) == 1
    assert not evidence_sufficient(rows)
    assert auto_evidence_ok(rows) == auto_evidence_ok(lead)
    assert status == "succeeded" and created == 1 and not fetcher.closed


@pytest.mark.asyncio
async def test_failed_duplicate_link_uses_one_attempt_and_does_not_replace_with_a_third() -> None:
    error = httpx.HTTPStatusError(
        "refused", request=httpx.Request("GET", ONE), response=httpx.Response(403)
    )
    fetcher, rows, status, created = await _scan(
        [ONE, ONE, TWO, THREE], replacements={ONE: error}
    )
    assert [url for url, _ in fetcher.calls] == [ORIGIN + "/feed", LEAD, ONE, TWO]
    assert {row.url for row in rows} == {LEAD, TWO}
    assert status == "partial" and created == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("target", [LEAD, ORIGIN + "/private", "https://other.example/support/a"])
async def test_redirected_supplement_must_still_be_same_host_and_in_scope(target: str) -> None:
    _, rows, status, created = await _scan(
        [ONE], replacements={ONE: _result(target, _page(DOCUMENT_TEXT))}
    )
    assert [row.url for row in rows] == [LEAD]
    assert status == "partial" and created == 1


@pytest.mark.asyncio
async def test_a_help_shell_is_not_stored_as_an_official_document() -> None:
    _, rows, status, _ = await _scan(
        [ONE], replacements={ONE: _result(ONE, b"<main><h1>Help Center</h1></main>")}
    )
    assert [row.url for row in rows] == [LEAD]
    assert status == "partial"


@pytest.mark.asyncio
async def test_transient_document_failure_preserves_existing_deferred_scan_behavior() -> None:
    fetcher, rows, status, created = await _scan(
        [ONE, TWO], replacements={ONE: httpx.ReadTimeout("temporary")}
    )
    assert [url for url, _ in fetcher.calls] == [ORIGIN + "/feed", LEAD, ONE]
    assert rows == [] and created == 0 and status == "partial"


@pytest.mark.asyncio
async def test_same_fetcher_rejects_a_supplement_redirect_before_reading_another_host() -> None:
    requests: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        # SafeNewsFetcher pins the transport URL to the resolved public IP while
        # preserving the original Host/SNI; assert logical hosts, not the pinned URL.
        requests.append(request.headers["host"])
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /", request=request)
        return httpx.Response(
            302, headers={"location": "https://other.example/support/a"}, request=request
        )

    async def resolver(_host: str) -> tuple[str, ...]:
        return ("93.184.216.34",)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    fetcher = SafeNewsFetcher(client=client, resolver=resolver)
    try:
        with pytest.raises(UnsafeNewsUrl):
            await fetcher.fetch(
                ONE, allowed_hosts={"official.example"}, allowed_redirect_hosts=set()
            )
    finally:
        await fetcher.close()
    assert requests == ["official.example", "official.example"]
