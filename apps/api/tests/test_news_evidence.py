from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.ai.jev import NoulAnswer, estimate_tokens
from app.config import get_settings
from app.db import Base
from app.guides.schemas import GuideDocument
from app.news_automation import ai
from app.news_automation.evidence import MAX_EVIDENCE_CHARACTERS, NewsInputTooLarge
from app.news_automation.feeds import read_article
from app.news_automation.models import (
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsSource,
)
from app.news_automation.scanner import scan_source
from app.news_automation.schemas import EditorialDraft, FetchResult, VerificationResult
from app.news_automation.validation import refresh_evidence

# Sources in these tests have been scanned before: a first scan only records its listing
# as seen (scanner.BASELINE), which test_a_new_source_s_first_scan_files_only_fresh_entries covers.
SCANNED_BEFORE = datetime(2026, 1, 1, tzinfo=UTC)


def document() -> GuideDocument:
    return GuideDocument.model_validate(
        {
            "title": "The completed rollout",
            "description": "What is available and where.",
            "blocks": [{"type": "paragraph", "text": "The official rollout has limits."}],
        }
    )


def evidence(text: str, number: int = 0) -> NewsEvidence:
    return NewsEvidence(
        candidate_id=uuid4(),
        role="evidence",
        is_first_party=True,
        url=f"https://official.example/update-{number}",
        title="Official rollout",
        content_hash="a" * 64,
        retrieved_at=datetime.now(UTC),
        excerpt=text,
    )


@pytest.mark.asyncio
async def test_long_primary_and_linked_pages_reach_factcheck_and_refresh_without_shortening(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Exercise fetching -> extraction -> persisted rows -> actual verification payload.

    Both facts used to fall beyond the scanner's 8k cut. A refresh of the exact same page
    must keep them, and an old 8k row must expand even when its full-page hash is unchanged.
    """
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
    factory = async_sessionmaker(engine, expire_on_commit=False)
    primary_url = "https://press.example/story"
    linked_url = "https://official.example/rollout"
    late_facts = {
        primary_url: "Since June 2026 the site runs on 100% CSS Modules.",
        linked_url: "Enterprise access is coming soon; voice replication is unavailable in Texas.",
    }
    lead = "The organisation explained the background to this update. " * 200
    bodies = {
        url: (
            f"<html><main><p>{lead}</p><p>{fact}</p>"
            + (f'<a href="{linked_url}">Official rollout</a>' if url == primary_url else "")
            + "</main></html>"
        ).encode()
        for url, fact in late_facts.items()
    }
    listing = (
        "<rss><channel><item><title>Official rollout</title>"
        f"<link>{primary_url}</link></item></channel></rss>"
    ).encode()
    sources = [
        NewsSource(
            last_scanned_at=SCANNED_BEFORE,
            name=host,
            url=f"https://{host}/feed",
            format="rss",
            role="evidence",
            vertical="tech",
            is_first_party=True,
            enabled=True,
            allowed_redirect_hosts_json=[],
            config_json={},
        )
        for host in ("press.example", "official.example")
    ]
    fetcher = AsyncMock()

    async def fetch(url: str, **_kwargs: object) -> FetchResult:
        return FetchResult(
            url=url,
            status_code=200,
            content_type="application/rss+xml" if url.endswith("/feed") else "text/html",
            body=listing if url.endswith("/feed") else bodies[url],
        )

    fetcher.fetch.side_effect = fetch
    enqueued: list[UUID] = []

    async def enqueue(candidate_id: UUID) -> None:
        enqueued.append(candidate_id)

    provider = SimpleNamespace(
        model="offline-fixture",
        structured=AsyncMock(return_value=(VerificationResult(verdict="pass"), {})),
        close=AsyncMock(),
    )
    monkeypatch.setattr(ai, "research_provider", Mock(return_value=provider))
    try:
        async with factory() as session:
            settings = NewsAutomationSettings(id=1, enabled=True)
            session.add(settings)
            session.add_all(sources)
            await session.commit()
            assert await scan_source(session, sources[0].id, enqueue, fetcher=fetcher) == 1
            rows = list(await session.scalars(select(NewsEvidence)))
            assert len(rows) == 2 and len(enqueued) == 1
            stored = {row.url: row.excerpt for row in rows}
            for row in rows:
                assert 8_000 < len(row.excerpt) <= MAX_EVIDENCE_CHARACTERS
                assert late_facts[row.url] in row.excerpt
                assert late_facts[row.url] not in row.excerpt[:8_000]

            candidate = await session.get(NewsCandidate, enqueued[0])
            assert candidate is not None
            provider.structured.return_value = (
                EditorialDraft.model_validate(
                    {
                        "eligible": True,
                        "vertical": "tech",
                        "event_date": "2026-09-29",
                        "slug": "tech-news-rollout-20260929",
                        "topics": ["tech"],
                        "claims": [
                            {"claim": late_facts[primary_url], "source_urls": [primary_url]}
                        ],
                        "document": document(),
                    }
                ),
                {},
            )
            await ai.draft_article(get_settings(), settings, candidate, rows)
            payload = provider.structured.await_args.args[-1]
            assert {row["url"]: row["excerpt"] for row in payload["evidence"]} == stored
            provider.structured.return_value = (VerificationResult(verdict="pass"), {})

            for legacy in (False, True):
                if legacy:
                    for row in rows:
                        row.excerpt = row.excerpt[:8_000]
                assert await refresh_evidence(session, rows, fetcher=fetcher) == ([], [])
                assert {row.url: row.excerpt for row in rows} == stored
                await ai.verify_article(get_settings(), settings, document(), rows)
                payload = provider.structured.await_args.args[-1]
                assert {row["url"]: row["excerpt"] for row in payload["evidence"]} == stored
                await ai.final_edit(
                    get_settings(), settings, document(), "en", document(), rows
                )
                payload = provider.structured.await_args.args[-1]
                assert {row["url"]: row["excerpt"] for row in payload["evidence"]} == stored
    finally:
        await engine.dispose()


def test_evidence_storage_keeps_the_existing_extractor_ceiling() -> None:
    lead = "a" * (MAX_EVIDENCE_CHARACTERS - 40)
    tail = "Release remains restricted."
    page = f"<main>{lead}{tail}{'b' * 10_000}</main>".encode()
    extracted = read_article(page, "https://official.example/update")
    assert len(extracted.text) == MAX_EVIDENCE_CHARACTERS
    assert tail in extracted.text


@pytest.mark.asyncio
async def test_full_english_evidence_fits_without_reslicing_at_the_model_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The scanner permits one primary and four linked sources. Keep all five complete.
    rows = [evidence("a" * 39_960 + f" Tail fact from source {i}.", i) for i in range(5)]
    provider = SimpleNamespace(
        model="offline-fixture",
        structured=AsyncMock(return_value=(VerificationResult(verdict="pass"), {})),
        close=AsyncMock(),
    )
    monkeypatch.setattr(ai, "research_provider", Mock(return_value=provider))
    await ai.verify_article(get_settings(), NewsAutomationSettings(id=1), document(), rows)
    payload = provider.structured.await_args.args[-1]
    assert [item["excerpt"] for item in payload["evidence"]] == [row.excerpt for row in rows]
    provider.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_large_cjk_bundle_is_held_before_model_creation_instead_of_cutting_sources(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider_factory = Mock()
    monkeypatch.setattr(ai, "research_provider", provider_factory)
    rows = [evidence("字" * MAX_EVIDENCE_CHARACTERS, i) for i in range(2)]
    with pytest.raises(NewsInputTooLarge, match="Evidence was not truncated"):
        await ai.verify_article(get_settings(), NewsAutomationSettings(id=1), document(), rows)
    provider_factory.assert_not_called()
    assert all(len(row.excerpt) == MAX_EVIDENCE_CHARACTERS for row in rows)


@pytest.mark.asyncio
async def test_input_budget_includes_instructions_and_reply_schema(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider_factory = Mock()
    monkeypatch.setattr(ai, "research_provider", provider_factory)
    payload = {"evidence": "Short evidence."}
    monkeypatch.setattr(ai, "STAGE_MAX_INPUT_TOKENS", estimate_tokens(payload) + 1)
    with pytest.raises(NewsInputTooLarge):
        await ai._structured(
            get_settings(), "openai", None, VerificationResult, "check", "Verify it.", payload
        )
    provider_factory.assert_not_called()


@pytest.mark.asyncio
async def test_duplicate_check_reads_the_fact_after_the_old_six_thousand_cut(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    text = "Background to the product launch. " * 300 + "A later independent rollout in June."
    consumed = AsyncMock(return_value=True)
    client = SimpleNamespace(
        ask=AsyncMock(return_value=({"duplicate": NoulAnswer(type="noul", noul=0.01)}, {})),
        close=AsyncMock(),
    )
    monkeypatch.setattr(ai, "consume_jev_call", consumed)
    monkeypatch.setattr(ai, "jev_client", Mock(return_value=client))
    result = await ai.jev_duplicate_check(
        AsyncMock(), get_settings(), "The June rollout", text, ["Product announced in May"]
    )
    assert result == ("distinct", 0.01, [])
    assert client.ask.await_args.args[0]["new_event"]["excerpt"] == text
    assert "June" not in text[:6_000]
    consumed.assert_awaited_once()
    client.close.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("limited_setting", ["jev_max_state_tokens", "jev_max_request_tokens"])
async def test_duplicate_over_either_budget_is_manual_without_spending_a_call(
    monkeypatch: pytest.MonkeyPatch, limited_setting: str
) -> None:
    consumed = AsyncMock(return_value=True)
    client_factory = Mock()
    monkeypatch.setattr(ai, "consume_jev_call", consumed)
    monkeypatch.setattr(ai, "jev_client", client_factory)
    environment = get_settings().model_copy(update={limited_setting: 2_000})
    result = await ai.jev_duplicate_check(
        AsyncMock(), environment, "New rollout", "字" * 9_000, ["Earlier announcement"]
    )
    assert result == ("manual", None, ["JevRequestTooLarge"])
    consumed.assert_not_awaited()
    client_factory.assert_not_called()


@pytest.mark.asyncio
async def test_oversized_pipeline_input_preserves_saved_drafts_and_evidence_for_the_editor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.news_automation import pipeline
    from app.news_automation.models import NewsPipelineRun
    from tests.test_news_pipeline import database, seed_single_source_candidate

    engine, factory = await database()
    original_draft = {"zh-TW": document().model_dump(mode="json")}
    provider_factory = Mock()
    monkeypatch.setattr(ai, "research_provider", provider_factory)
    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    try:
        async with factory() as session:
            candidate = await seed_single_source_candidate(session)
            candidate_id = candidate.id
            candidate.draft_bundle_json = original_draft
            first = await session.scalar(select(NewsEvidence))
            assert first is not None
            first.excerpt = "字" * MAX_EVIDENCE_CHARACTERS
            second = evidence("文" * MAX_EVIDENCE_CHARACTERS)
            second.candidate_id = candidate_id
            session.add(second)
            await session.commit()
            original_evidence = {
                row.url: (row.content_hash, row.excerpt)
                for row in await session.scalars(select(NewsEvidence))
            }

        async with factory() as session:
            with pytest.raises(NewsInputTooLarge):
                await pipeline.process_candidate(
                    session, Mock(), get_settings(), candidate_id
                )
            stored = await session.get(NewsCandidate, candidate_id)
            assert stored is not None
            assert stored.status == "failed" and stored.error_code == "NewsInputTooLarge"
            assert "Evidence was not truncated" in (stored.error_detail or "")
            assert stored.draft_bundle_json == original_draft
            assert {
                row.url: (row.content_hash, row.excerpt)
                for row in await session.scalars(select(NewsEvidence))
            } == original_evidence
            run = await session.scalar(select(NewsPipelineRun))
            assert run is not None and run.status == "failed"
            assert run.error_code == "NewsInputTooLarge"
        provider_factory.assert_not_called()
    finally:
        await engine.dispose()


def test_oversized_input_does_not_escape_the_job_or_queue_an_automatic_retry(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    from app.news_automation import jobs
    from tests.test_news_pipeline import FakeSessionFactory

    process = AsyncMock(side_effect=NewsInputTooLarge("Evidence was not truncated."))
    queue_factory = Mock()
    monkeypatch.setattr(jobs, "SessionFactory", FakeSessionFactory)
    monkeypatch.setattr(jobs, "load_runtime_settings", AsyncMock(return_value=get_settings()))
    monkeypatch.setattr(jobs, "process_candidate", process)
    monkeypatch.setattr(jobs, "get_redis", Mock())
    monkeypatch.setattr(jobs, "_close_resources", AsyncMock())
    monkeypatch.setattr(jobs, "_queue", queue_factory)
    jobs.run_candidate(str(uuid4()))
    process.assert_awaited_once()
    queue_factory.assert_not_called()
    assert "failed without retry: NewsInputTooLarge" in caplog.text
