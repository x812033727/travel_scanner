from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from types import TracebackType
from typing import Any, cast
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel, ValidationError
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings
from app.db import Base
from app.guides.models import (
    GuideArticle,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideArticleTopic,
    GuideSearchEntry,
    GuideTopic,
)
from app.guides.schemas import GuideDocument
from app.i18n import Locale
from app.models import AdminAuditLog
from app.news_automation import ai, jobs, pipeline, scheduler, service
from app.news_automation.models import (
    NewsAssessment,
    NewsAsset,
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsPipelineRun,
    NewsSource,
)
from app.news_automation.provider_schema import portable_json_schema
from app.news_automation.schemas import (
    EditorialDraft,
    LocaleReviewResult,
    LocalizedDocument,
    SettingsWrite,
    VerificationResult,
)
from app.news_automation.worker import QUEUE_NAME
from app.worker import QUEUE_NAMES

REPLY_MODELS: tuple[type[BaseModel], ...] = (
    EditorialDraft,
    VerificationResult,
    LocalizedDocument,
    LocaleReviewResult,
)
# Keywords OpenAI strict mode or Anthropic structured outputs reject over raw HTTP.
REJECTED_KEYWORDS = {
    "oneOf",
    "discriminator",
    "const",
    "minLength",
    "maxLength",
    "pattern",
    "minimum",
    "maximum",
    "exclusiveMinimum",
    "exclusiveMaximum",
    "multipleOf",
    "minItems",
    "maxItems",
    "uniqueItems",
    "propertyNames",
    "default",
}
TODAY = datetime.now(UTC).date()
EVENT_DAY = TODAY - timedelta(days=1)
SLUG = f"ai-news-model-release-{EVENT_DAY:%Y%m%d}"
FIRST_PARTY_URL = "https://official.example/release"
LEAD_URL = "https://lead.example/story"


def schema_nodes(node: Any, path: str = "$") -> list[tuple[str, dict[str, Any]]]:
    found: list[tuple[str, dict[str, Any]]] = []
    if isinstance(node, dict):
        found.append((path, node))
        for key, value in node.items():
            if key in {"properties", "$defs"}:
                for name, child in value.items():
                    found.extend(schema_nodes(child, f"{path}.{key}.{name}"))
            else:
                found.extend(schema_nodes(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(schema_nodes(value, f"{path}[{index}]"))
    return found


@pytest.mark.parametrize("model", REPLY_MODELS, ids=lambda model: model.__name__)
def test_every_news_reply_schema_is_accepted_by_strict_providers(
    model: type[BaseModel],
) -> None:
    schema = model.model_json_schema()
    for path, node in schema_nodes(schema):
        assert not REJECTED_KEYWORDS & set(node), path
        if "$ref" in node:
            assert set(node) == {"$ref"}, path
        if node.get("type") == "object" or "properties" in node:
            assert node["additionalProperties"] is False, path
            assert node["required"] == list(node.get("properties", {})), path
        if "format" in node:
            assert node["format"] in {"date", "date-time", "time"}, path


def test_dropped_bounds_stay_visible_to_the_model_and_enforced_by_pydantic() -> None:
    schema = LocalizedDocument.model_json_schema()
    heading = schema["$defs"]["HeadingBlock"]["properties"]["text"]
    assert "maxLength=200" in heading["description"]
    blocks = schema["$defs"]["GuideDocument"]["properties"]["blocks"]["items"]
    assert "anyOf" in blocks and len(blocks["anyOf"]) > 5
    with pytest.raises(ValidationError):
        LocalizedDocument.model_validate(
            {
                "document": {
                    "title": "Title",
                    "description": "Description",
                    "blocks": [{"type": "heading", "text": "x" * 201, "level": 2}],
                    "hero": None,
                    "sources": [],
                }
            }
        )
    with pytest.raises(ValueError, match="map-typed"):
        portable_json_schema({"type": "object", "additionalProperties": {"type": "string"}})


def test_model_ids_are_held_to_the_catalog_pattern() -> None:
    values: dict[str, Any] = {
        "enabled": False,
        "writer_provider": "gemini",
        "verifier_provider": "anthropic",
        "global_concurrency": 2,
        "per_vertical_concurrency": 1,
        "min_shadow_days": 14,
        "min_shadow_candidates": 50,
        "min_human_agreement": 0.95,
        "jev_act_confidence": 0.9,
        "prompt_version": "news-v1",
        "policy_version": "news-policy-v1",
    }
    written = SettingsWrite.model_validate(
        {**values, "writer_model": " gemini-3.8-flash ", "verifier_model": "  "}
    )
    assert written.writer_model == "gemini-3.8-flash"
    assert written.verifier_model is None
    with pytest.raises(ValidationError):
        SettingsWrite.model_validate({**values, "writer_model": "../v1beta/models/x"})


NEWS_TABLES = (
    NewsAutomationSettings,
    NewsSource,
    NewsCandidate,
    NewsEvidence,
    NewsPipelineRun,
    NewsAssessment,
    NewsAsset,
    GuideArticle,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideTopic,
    GuideArticleTopic,
    GuideSearchEntry,
    AdminAuditLog,
)


async def database() -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = cast(list[Table], [model.__table__ for model in NEWS_TABLES])
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    return engine, async_sessionmaker(engine, expire_on_commit=False)


def news_document(title: str) -> GuideDocument:
    return GuideDocument.model_validate(
        {
            "title": title,
            "description": "What changed and why it matters.",
            "blocks": [{"type": "paragraph", "text": "Verified body."}],
            "sources": [],
        }
    )


async def seed_candidate(
    session: AsyncSession,
    *,
    status: str = "discovered",
    vertical: str = "ai",
    processing_started_at: datetime | None = None,
) -> NewsCandidate:
    source = NewsSource(
        name=f"Source {uuid4()}",
        url=f"https://{uuid4().hex}.example/feed",
        format="rss",
        role="evidence",
        vertical=vertical,
        is_first_party=True,
        enabled=True,
    )
    session.add(source)
    await session.flush()
    marker = uuid4().hex
    candidate = NewsCandidate(
        source_id=source.id,
        vertical=vertical,
        status=status,
        canonical_url=f"{FIRST_PARTY_URL}/{marker}",
        source_title="Model release",
        normalized_title=f"model release {marker}",
        content_hash=marker * 2,
        idempotency_key=marker * 2,
        processing_started_at=processing_started_at,
    )
    session.add(candidate)
    await session.commit()
    return candidate


async def seed_published_news(
    session: AsyncSession, slug: str, news_date: date, titles: dict[str, str]
) -> None:
    article = GuideArticle(id=uuid4(), slug=slug, kind="life", news_date=news_date)
    session.add(article)
    for locale, title in titles.items():
        session.add(
            GuideSearchEntry(
                article_id=article.id,
                locale=locale,
                revision_version=1,
                title=title,
                description="",
                title_norm=title.casefold(),
                description_norm="",
                headings_norm="",
                aliases_norm="",
                body_text="",
                search_text=title.casefold(),
                published_at=datetime.now(UTC),
            )
        )
    await session.commit()


@pytest.mark.asyncio
async def test_pipeline_translates_each_locale_and_checks_published_news_for_duplicates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        session.add(NewsAutomationSettings(id=1, enabled=True))
        session.add(
            GuideTopic(slug="ai-news", section="life", names_json={"zh-TW": "AI 新聞"})
        )
        candidate = await seed_candidate(session)
        for url, first_party in ((FIRST_PARTY_URL, True), (LEAD_URL, False)):
            session.add(
                NewsEvidence(
                    candidate_id=candidate.id,
                    role="evidence",
                    is_first_party=first_party,
                    url=url,
                    title="Release",
                    source_date=EVENT_DAY,
                    content_hash=("f" if first_party else "e") * 64,
                    excerpt="The model shipped today.",
                )
            )
        await seed_published_news(
            session,
            "ai-news-manual-story-20260920",
            TODAY - timedelta(days=4),
            {"zh-TW": "手寫的 AI 新聞", "en": "A hand-written AI story"},
        )
        await seed_published_news(
            session, "tech-news-other-vertical", TODAY, {"en": "A technology story"}
        )
        await seed_published_news(
            session, "ai-news-too-old", TODAY - timedelta(days=45), {"en": "An old AI story"}
        )
        await session.commit()

    compared: list[list[str]] = []

    async def duplicate_check(*args: Any) -> tuple[str, float, list[str]]:
        compared.append(list(args[4]))
        return "distinct", 0.01, []

    draft = EditorialDraft.model_validate(
        {
            "eligible": True,
            "exclusion_reason": "",
            "vertical": "ai",
            "event_date": EVENT_DAY.isoformat(),
            "slug": SLUG,
            "topics": ["ai-news"],
            "claims": [{"claim": "The model shipped.", "source_urls": [FIRST_PARTY_URL]}],
            "document": news_document("模型發布").model_dump(mode="json"),
        }
    )
    translated: list[Locale] = []

    async def translate(*args: Any) -> tuple[LocalizedDocument, dict[str, int], str]:
        locale = cast(Locale, args[3])
        translated.append(locale)
        document = news_document(f"Release {locale}")
        return LocalizedDocument(document=document), {"output_tokens": 10}, "writer-model"

    async def identity_assets(_session: Any, _candidate: Any, documents: Any) -> Any:
        return documents

    monkeypatch.setattr(ai, "jev_duplicate_check", duplicate_check)
    monkeypatch.setattr(ai, "draft_article", AsyncMock(return_value=(draft, {}, "writer-model")))
    monkeypatch.setattr(
        ai,
        "verify_article",
        AsyncMock(return_value=(VerificationResult(verdict="pass"), {}, "checker")),
    )
    monkeypatch.setattr(ai, "translate_article", translate)
    monkeypatch.setattr(
        ai,
        "review_locale",
        AsyncMock(return_value=(LocaleReviewResult(verdict="pass"), {}, "checker")),
    )
    monkeypatch.setattr(
        ai,
        "jev_assessments",
        AsyncMock(
            return_value=[
                ai.JevLocaleDecision(locale, "act", 0.97, [], {})
                for locale in ("zh-TW", "zh-CN", "en", "ja", "ko")
            ]
        ),
    )
    monkeypatch.setattr(pipeline, "ensure_assets", identity_assets)
    monkeypatch.setattr(pipeline, "hard_policy_problems", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(pipeline, "revalidate_evidence", AsyncMock(return_value=(True, [])))

    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate.id)
        stored = await session.get(NewsCandidate, candidate.id)
        stages = list(
            await session.scalars(
                select(NewsPipelineRun.stage).where(NewsPipelineRun.candidate_id == candidate.id)
            )
        )
        locales = set(await session.scalars(select(GuideArticleLocale.locale)))

    assert result == "shadow_review"
    assert stored is not None and stored.would_publish is True
    assert translated == ["zh-CN", "en", "ja", "ko"]
    assert [stage for stage in stages if stage.startswith("translation")] == [
        "translation-zh-CN",
        "translation-en",
        "translation-ja",
        "translation-ko",
    ]
    assert locales == {"zh-TW", "zh-CN", "en", "ja", "ko"}
    assert compared == [["A hand-written AI story"]]
    await engine.dispose()


@pytest.mark.asyncio
async def test_claim_distinguishes_disabled_finished_and_full_capacity() -> None:
    engine, factory = await database()
    async with factory() as session:
        configuration = NewsAutomationSettings(id=1, enabled=False, per_vertical_concurrency=1)
        session.add(configuration)
        waiting = (await seed_candidate(session)).id
        finished = (await seed_candidate(session, status="manual_review")).id
        await seed_candidate(session, status="drafting", processing_started_at=datetime.now(UTC))

        outcomes = [
            await pipeline.process_candidate(session, Mock(), get_settings(), waiting)
        ]
        configuration = await service.settings_row(session)
        configuration.enabled = True
        await session.commit()
        for candidate_id in (finished, waiting):
            outcomes.append(
                await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
            )
        statuses = {
            row.id: row.status
            for row in await session.scalars(
                select(NewsCandidate).where(NewsCandidate.id.in_((waiting, finished)))
            )
        }
    assert outcomes == ["disabled", "skipped", "deferred"]
    assert statuses == {waiting: "discovered", finished: "manual_review"}
    await engine.dispose()


@pytest.mark.asyncio
async def test_stalled_candidates_release_capacity_and_rerun_a_bounded_number_of_times() -> None:
    engine, factory = await database()
    now = datetime.now(UTC)
    async with factory() as session:
        stalled = await seed_candidate(
            session, status="verifying", processing_started_at=now - timedelta(hours=2)
        )
        reverify = await seed_candidate(
            session, status="locale_review", processing_started_at=now - timedelta(hours=2)
        )
        reverify.error_code = "news_reverify_requested"
        fresh = await seed_candidate(
            session, status="drafting", processing_started_at=now - timedelta(minutes=10)
        )
        session.add(
            NewsPipelineRun(
                candidate_id=stalled.id,
                stage="verification-1",
                idempotency_key=f"{stalled.id}:verification-1:1",
            )
        )
        await session.commit()

        assert set(await pipeline.recover_stalled_candidates(session, now=now)) == {
            stalled.id,
            reverify.id,
        }
        await session.refresh(stalled)
        await session.refresh(reverify)
        await session.refresh(fresh)
        run = await session.scalar(
            select(NewsPipelineRun).where(NewsPipelineRun.stage == "verification-1")
        )
        assert stalled.status == "failed"
        assert stalled.error_code == "news_processing_stale"
        assert reverify.error_code == "news_reverify_requested"
        assert fresh.status == "drafting"
        assert run is not None and run.status == "failed"

        reruns: list[list[UUID]] = []
        for _ in range(2):
            stalled.status = "drafting"
            await session.commit()
            reruns.append(await pipeline.recover_stalled_candidates(session, now=now))
    assert reruns == [[stalled.id], []]
    await engine.dispose()


@pytest.mark.asyncio
async def test_orphaned_discovered_candidates_are_swept_only_while_enabled() -> None:
    engine, factory = await database()
    now = datetime.now(UTC)
    async with factory() as session:
        configuration = NewsAutomationSettings(id=1, enabled=False)
        session.add(configuration)
        orphan = await seed_candidate(session)
        orphan.updated_at = now - timedelta(hours=3)
        await session.commit()
        orphan_id = orphan.id
        await seed_candidate(session)
        disabled = await pipeline.orphaned_candidates(session, now=now)
        configuration = await service.settings_row(session)
        configuration.enabled = True
        await session.commit()
        enabled = await pipeline.orphaned_candidates(session, now=now)
    assert disabled == []
    assert enabled == [orphan_id]
    await engine.dispose()


@pytest.mark.asyncio
async def test_settings_offer_catalog_models_and_the_resolved_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    runtime = get_settings().model_copy(
        update={"hotspot_guide_ai_anthropic_model": "", "anthropic_model": "claude-sonnet-5"}
    )
    monkeypatch.setattr(service, "load_runtime_settings", AsyncMock(return_value=runtime))
    async with factory() as session:
        view = await service.settings_view(session)
    offered = {
        provider: [option.value for option in options]
        for provider, options in view.model_options.items()
    }
    assert "claude-sonnet-5" in offered["anthropic"]
    assert not any(value.startswith("jev") for values in offered.values() for value in values)
    assert view.default_models["anthropic"] == "claude-sonnet-5"
    assert set(view.model_options) == {"openai", "anthropic", "minimax", "gemini"}
    await engine.dispose()


class FakeSessionFactory:
    async def __aenter__(self) -> object:
        return object()

    async def __aexit__(
        self,
        _type: type[BaseException] | None,
        _error: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        return None


def test_candidate_job_reads_admin_ai_settings_and_requeues_only_full_capacity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = get_settings().model_copy()
    outcomes = iter(["disabled", "skipped", "deferred", "shadow_review"])
    environments: list[object] = []

    async def process(_session: object, _redis: object, environment: object, _id: UUID) -> str:
        environments.append(environment)
        return next(outcomes)

    queue = Mock()
    monkeypatch.setattr(jobs, "SessionFactory", FakeSessionFactory)
    monkeypatch.setattr(jobs, "load_runtime_settings", AsyncMock(return_value=runtime))
    monkeypatch.setattr(jobs, "process_candidate", process)
    monkeypatch.setattr(jobs, "get_redis", Mock())
    monkeypatch.setattr(jobs, "_close_resources", AsyncMock())
    monkeypatch.setattr(jobs, "_queue", lambda: (Mock(), queue))
    for _ in range(4):
        jobs.run_candidate(str(uuid4()))
    assert environments == [runtime] * 4
    assert queue.enqueue_in.call_count == 1


def test_scheduler_requeues_a_candidate_once_per_reason_and_hour(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    queue = Mock()
    queue.fetch_job.return_value = None
    monkeypatch.setattr(jobs, "_queue", lambda: (Mock(), queue))
    candidate_id = uuid4()
    assert jobs.enqueue_candidate_once(candidate_id, "recovered") is not None
    queue.fetch_job.return_value = Mock()
    assert jobs.enqueue_candidate_once(candidate_id, "recovered") is None
    assert queue.enqueue.call_count == 1
    job_id = queue.enqueue.call_args.kwargs["job_id"]
    assert job_id.startswith(f"news-candidate-{candidate_id}-recovered-")


def test_the_news_queue_has_its_own_worker_in_the_news_profile() -> None:
    assert QUEUE_NAME == "news"
    assert "news" not in QUEUE_NAMES
    root = Path(__file__).resolve().parents[3]
    for name in ("docker-compose.yml", "docker-compose.prod.yml"):
        compose = (root / name).read_text(encoding="utf-8")
        service_block = compose.split("  news-worker:", 1)[1].split("\n\n", 1)[0]
        assert 'profiles: ["news"]' in service_block, name
        assert '"app.news_automation.worker"' in service_block, name


@pytest.mark.asyncio
async def test_a_failed_reverification_keeps_its_marker_so_the_rerun_does_not_redraft(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        session.add(NewsAutomationSettings(id=1, enabled=True))
        candidate = await seed_candidate(session)
        candidate.error_code = pipeline.REVERIFY_MARKER
        # Only zh-TW is present, so the re-verification raises inside the pipeline.
        candidate.draft_bundle_json = {"zh-TW": news_document("Edited").model_dump(mode="json")}
        for url, first_party in ((FIRST_PARTY_URL, True), (LEAD_URL, False)):
            session.add(
                NewsEvidence(
                    candidate_id=candidate.id,
                    role="evidence",
                    is_first_party=first_party,
                    url=url,
                    title="Release",
                    content_hash=("f" if first_party else "e") * 64,
                    excerpt="The model shipped.",
                )
            )
        await session.commit()
        candidate_id = candidate.id
    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.0, []))
    )
    draft = AsyncMock()
    monkeypatch.setattr(ai, "draft_article", draft)
    async with factory() as session:
        with pytest.raises(Exception, match="五個語言"):
            await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
    assert stored is not None
    assert stored.status == "failed"
    assert stored.error_code == pipeline.REVERIFY_MARKER
    draft.assert_not_awaited()
    await engine.dispose()


@pytest.mark.asyncio
async def test_scheduler_queues_claimed_scans_even_when_the_sweep_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_id = uuid4()
    queued: list[UUID] = []
    monkeypatch.setattr(scheduler, "SessionFactory", FakeSessionFactory)
    monkeypatch.setattr(scheduler, "claim_due_sources", AsyncMock(return_value=[source_id]))
    monkeypatch.setattr(
        scheduler, "recover_stalled_candidates", AsyncMock(side_effect=RuntimeError("db blip"))
    )
    monkeypatch.setattr(scheduler, "enqueue_source_scan", queued.append)
    monkeypatch.setattr(scheduler, "enqueue_candidate_once", Mock())
    assert await scheduler.tick() == 1
    assert queued == [source_id]
