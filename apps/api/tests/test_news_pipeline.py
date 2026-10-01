from __future__ import annotations

from collections.abc import AsyncIterator
from copy import deepcopy
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
    GuideArticleAlias,
    GuideArticleLink,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideArticleTopic,
    GuideSearchEntry,
    GuideTopic,
)
from app.guides.schemas import GuideDocument
from app.i18n import Locale
from app.models import AdminAuditLog, User
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
from app.news_automation.policy import (
    EVIDENCE_REFRESH_MARKER,
    document_fingerprint,
)
from app.news_automation.policy import (
    hard_policy_problems as actual_hard_policy_problems,
)
from app.news_automation.provider_schema import portable_json_schema
from app.news_automation.schemas import (
    CandidateAction,
    EditorialDraft,
    LocaleReviewResult,
    LocalizedDocument,
    SettingsWrite,
    VerificationResult,
)
from app.news_automation.worker import QUEUE_NAME
from app.problems import AppError
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
    GuideArticleAlias,
    GuideArticleLink,
    AdminAuditLog,
    User,
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


async def seed_single_source_candidate(session: AsyncSession) -> NewsCandidate:
    """A candidate whose only evidence is its own first-party page."""

    session.add(NewsAutomationSettings(id=1, enabled=True))
    session.add(GuideTopic(slug="ai-news", section="life", names_json={"zh-TW": "AI 新聞"}))
    candidate = await seed_candidate(session)
    session.add(
        NewsEvidence(
            candidate_id=candidate.id,
            role="evidence",
            is_first_party=True,
            url=FIRST_PARTY_URL,
            title="Release",
            source_date=EVENT_DAY,
            content_hash="f" * 64,
            excerpt="The model shipped today.",
        )
    )
    await session.commit()
    return candidate


def stage_one_mocks(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
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
    jev_locales: list[tuple[Locale, ...]] = []

    async def jev(*args: Any, **kwargs: Any) -> list[ai.JevLocaleDecision]:
        locales = kwargs.get("locales", ("zh-TW", "zh-CN", "en", "ja", "ko"))
        jev_locales.append(tuple(locales))
        return [ai.JevLocaleDecision(locale, "act", 0.97, [], {}) for locale in locales]

    mocks: dict[str, Any] = {
        "draft": AsyncMock(return_value=(draft, {}, "writer-model")),
        "translate": AsyncMock(),
        "jev_locales": jev_locales,
    }
    monkeypatch.setattr(ai, "draft_article", mocks["draft"])
    monkeypatch.setattr(
        ai,
        "verify_article",
        AsyncMock(return_value=(VerificationResult(verdict="pass"), {}, "checker")),
    )
    monkeypatch.setattr(ai, "translate_article", mocks["translate"])
    monkeypatch.setattr(ai, "jev_assessments", jev)
    mocks["final_edit"] = AsyncMock(return_value=(LocaleReviewResult(verdict="pass"), {}, "editor"))
    monkeypatch.setattr(ai, "final_edit", mocks["final_edit"])
    return mocks


def stage_two_mocks(monkeypatch: pytest.MonkeyPatch) -> list[Locale]:
    """Translations that pass review, no artwork, and evidence that has not changed."""

    translated: list[Locale] = []

    async def translate(*args: Any) -> tuple[LocalizedDocument, dict[str, int], str]:
        locale = cast(Locale, args[3])
        translated.append(locale)
        return LocalizedDocument(document=news_document(f"Release {locale}")), {}, "writer"

    async def identity_assets(_session: Any, _candidate: Any, documents: Any) -> Any:
        return documents

    monkeypatch.setattr(ai, "translate_article", translate)
    monkeypatch.setattr(
        ai,
        "review_locale",
        AsyncMock(return_value=(LocaleReviewResult(verdict="pass"), {}, "checker")),
    )
    monkeypatch.setattr(pipeline, "ensure_assets", identity_assets)
    monkeypatch.setattr(pipeline, "hard_policy_problems", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(service, "hard_policy_problems", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(service, "revalidate_evidence", AsyncMock(return_value=(True, [])))
    return translated


async def confirm(factory: Any, candidate_id: UUID, owner_id: UUID) -> None:
    """Run stage one, then press "confirm and translate" as the owner."""

    async with factory() as session:
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "manual_review"
        owner_row = await session.get(User, owner_id)
        assert owner_row is not None
        await service.approve_candidate(
            session, owner_row, candidate_id, CandidateAction(reason="Worth publishing")
        )


@pytest.mark.asyncio
async def test_stage_one_drafts_a_single_source_story_in_chinese_and_waits_for_the_owner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
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

    monkeypatch.setattr(ai, "jev_duplicate_check", duplicate_check)
    mocks = stage_one_mocks(monkeypatch)

    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate.id)
        stored = await session.get(NewsCandidate, candidate.id)
        draft_run = await session.scalar(
            select(NewsPipelineRun).where(
                NewsPipelineRun.candidate_id == candidate.id, NewsPipelineRun.stage == "draft"
            )
        )
        articles = list(await session.scalars(select(GuideArticle.slug)))
    await engine.dispose()

    assert result == "manual_review"
    assert stored is not None
    assert (stored.status, stored.error_code) == ("manual_review", "news_zh_draft_ready")
    assert set(stored.draft_bundle_json) == {"zh-TW"}
    assert stored.would_publish is True
    # One evidence website is enough to draft; nothing is translated before the owner says so.
    mocks["translate"].assert_not_awaited()
    assert mocks["jev_locales"] == [("zh-TW",)]
    assert draft_run is not None and draft_run.metadata_json == {"slug": SLUG}
    assert SLUG not in articles
    assert compared == [["A hand-written AI story"]]


@pytest.mark.asyncio
async def test_stage_two_translates_and_publishes_once_the_owner_confirms(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
        session.add(owner)
        await session.commit()
        candidate_id, owner_id = candidate.id, owner.id

    duplicate_check = AsyncMock(return_value=("distinct", 0.01, []))
    monkeypatch.setattr(ai, "jev_duplicate_check", duplicate_check)
    mocks = stage_one_mocks(monkeypatch)
    translated: list[Locale] = []

    async def translate(*args: Any) -> tuple[LocalizedDocument, dict[str, int], str]:
        locale = cast(Locale, args[3])
        translated.append(locale)
        return LocalizedDocument(document=news_document(f"Release {locale}")), {}, "writer"

    async def identity_assets(_session: Any, _candidate: Any, documents: Any) -> Any:
        return documents

    monkeypatch.setattr(ai, "translate_article", translate)
    monkeypatch.setattr(
        ai,
        "review_locale",
        AsyncMock(return_value=(LocaleReviewResult(verdict="pass"), {}, "checker")),
    )
    monkeypatch.setattr(pipeline, "ensure_assets", identity_assets)
    monkeypatch.setattr(pipeline, "hard_policy_problems", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(service, "hard_policy_problems", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(service, "revalidate_evidence", AsyncMock(return_value=(True, [])))

    async with factory() as session:
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "manual_review"
        owner_row = await session.get(User, owner_id)
        assert owner_row is not None
        await service.approve_candidate(
            session, owner_row, candidate_id, CandidateAction(reason="Worth publishing")
        )
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        published = {
            row.locale: row.published_version
            for row in await session.scalars(select(GuideArticleLocale))
        }
    await engine.dispose()

    assert result == "published"
    assert stored is not None
    assert (stored.status, stored.human_decision) == ("published", "publish")
    assert translated == ["zh-CN", "en", "ja", "ko"]
    assert set(published) == {"zh-TW", "zh-CN", "en", "ja", "ko"}
    assert all(version is not None for version in published.values())
    # Stage two neither checks for duplicates again nor redrafts, and Jev only saw zh-TW.
    duplicate_check.assert_awaited_once()
    mocks["draft"].assert_awaited_once()
    # Jev saw zh-TW in stage one, then all five locales as the last call.
    assert mocks["jev_locales"] == [("zh-TW",), ("zh-TW", "zh-CN", "en", "ja", "ko")]
    assert [call.args[3] for call in mocks["final_edit"].await_args_list] == [
        "zh-TW",
        "zh-CN",
        "en",
        "ja",
        "ko",
    ]


@pytest.mark.asyncio
async def test_a_confirmed_draft_whose_translation_fails_keeps_the_confirmation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
        session.add(owner)
        await session.commit()
        candidate_id, owner_id = candidate.id, owner.id

    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    stage_one_mocks(monkeypatch)
    monkeypatch.setattr(
        ai,
        "translate_article",
        AsyncMock(
            return_value=(LocalizedDocument(document=news_document("Release")), {}, "writer")
        ),
    )
    monkeypatch.setattr(
        ai,
        "review_locale",
        AsyncMock(return_value=(LocaleReviewResult(verdict="manual"), {}, "checker")),
    )

    async with factory() as session:
        await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        owner_row = await session.get(User, owner_id)
        assert owner_row is not None
        await service.approve_candidate(
            session, owner_row, candidate_id, CandidateAction(reason="Worth publishing")
        )
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        assert stored is not None
        held = (stored.error_code, stored.human_decision)
        # The same action may run stage two again.
        again = await service.approve_candidate(
            session, owner_row, candidate_id, CandidateAction(reason="Try the translation again")
        )
    await engine.dispose()

    assert result == "manual_review"
    assert held == ("news_locale_review_failed", "publish")
    assert again.status == "discovered"


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
async def test_a_spent_jev_budget_pauses_the_candidate_instead_of_holding_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        candidate_id = candidate.id
    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("manual", None, ["quota_unavailable"]))
    )
    writer = AsyncMock()
    monkeypatch.setattr(ai, "draft_article", writer)

    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        assessments = list(await session.scalars(select(NewsAssessment)))
    await engine.dispose()

    assert result == "jev_paused"
    assert stored is not None
    assert (stored.status, stored.error_code) == ("discovered", pipeline.JEV_QUOTA_PAUSED)
    assert assessments == [], "an unanswered check is not recorded as an uncertain one"
    writer.assert_not_awaited()


@pytest.mark.asyncio
async def test_candidates_paused_for_jev_wait_for_the_next_utc_day() -> None:
    engine, factory = await database()
    now = datetime(2026, 9, 27, 12, 0, tzinfo=UTC)
    async with factory() as session:
        session.add(NewsAutomationSettings(id=1, enabled=True))
        paused_today = await seed_candidate(session)
        paused_yesterday = await seed_candidate(session)
        plain = await seed_candidate(session)
        for row in (paused_today, paused_yesterday):
            row.error_code = pipeline.JEV_QUOTA_PAUSED
        paused_today.updated_at = now - timedelta(hours=3)
        paused_yesterday.updated_at = datetime(2026, 9, 26, 23, 0, tzinfo=UTC)
        plain.updated_at = now - timedelta(hours=3)
        await session.commit()
        expected = {paused_yesterday.id, plain.id}
        orphaned = set(await pipeline.orphaned_candidates(session, now=now))
    await engine.dispose()

    assert orphaned == expected


@pytest.mark.asyncio
async def test_candidates_paused_for_jev_run_now_when_the_budget_has_room() -> None:
    engine, factory = await database()
    now = datetime(2026, 9, 27, 12, 0, tzinfo=UTC)
    async with factory() as session:
        session.add(NewsAutomationSettings(id=1, enabled=True))
        paused_minutes_ago = await seed_candidate(session)
        paused_minutes_ago.error_code = pipeline.JEV_QUOTA_PAUSED
        paused_minutes_ago.updated_at = now - timedelta(minutes=5)
        recent = await seed_candidate(session)
        recent.updated_at = now - timedelta(minutes=5)
        await session.commit()
        paused_id = paused_minutes_ago.id
        spent = await pipeline.orphaned_candidates(session, now=now)
        room = await pipeline.orphaned_candidates(session, now=now, jev_budget_left=True)
    await engine.dispose()

    assert spent == []
    assert room == [paused_id], "a fresh candidate still waits for its own job"


def test_the_scheduler_reads_the_counter_jev_calls_spend(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    counted: list[str] = []

    class Spending:
        async def eval(self, _script: str, _keys: int, key: str, _budget: str) -> int:
            counted.append(key)
            return 1

    class Reading:
        def __init__(self, used: int | None) -> None:
            self.used = used
            self.read: list[str] = []

        def get(self, key: str) -> bytes | None:
            self.read.append(key)
            return None if self.used is None else str(self.used).encode()

        def close(self) -> None:
            pass

    import asyncio

    from app.ai.jev import consume_jev_call

    asyncio.run(consume_jev_call(Spending(), get_settings()))  # type: ignore[arg-type]
    for used, budget, expected in ((None, 200, True), (199, 200, True), (200, 200, False),
                                   (200, 5_000, True)):
        reader = Reading(used)
        monkeypatch.setattr(scheduler, "Redis", Mock(from_url=Mock(return_value=reader)))
        assert scheduler.jev_budget_left(budget) is expected
        assert reader.read == counted


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


def test_news_replies_drop_imagery_the_model_should_not_supply() -> None:
    draft = EditorialDraft.model_validate(
        {
            "eligible": True,
            "exclusion_reason": "",
            "vertical": "ai",
            "event_date": EVENT_DAY.isoformat(),
            "slug": SLUG,
            "topics": ["ai-news"],
            "claims": [{"claim": "Shipped.", "source_urls": [FIRST_PARTY_URL]}],
            # Also seen: sources repeated beside the document, and an unknown document key.
            "sources": [{"title": "Official", "url": FIRST_PARTY_URL}],
            "document": {
                "title": "Release",
                "description": "What changed.",
                "summary": "Not a GuideDocument field.",
                # As on the first production run: the source site's logo as the hero.
                "hero": {
                    "src": "https://blog.google/static/images/google-logo.svg",
                    "alt": "logo",
                    "width": 100,
                    "height": 100,
                },
                "blocks": [
                    {"type": "paragraph", "text": "Body."},
                    {
                        "type": "image",
                        "src": "https://example.com/photo.jpg",
                        "alt": "photo",
                        "width": 10,
                        "height": 10,
                    },
                ],
                "sources": [],
            },
        }
    )
    assert draft.document.hero is None
    assert [block.type for block in draft.document.blocks] == ["paragraph"]
    assert LocaleReviewResult.model_validate(
        {"verdict": "pass", "issues": [], "corrected_document": None}
    ).corrected_document is None


def test_a_reply_that_failed_validation_is_not_rerun_by_rq_but_outages_are(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import httpx

    def invalid() -> None:
        LocalizedDocument.model_validate({"document": None})

    errors: list[Exception] = []
    try:
        invalid()
    except ValidationError as error:
        errors.append(error)
    errors.append(httpx.ConnectError("provider unreachable"))
    raised: list[str] = []
    monkeypatch.setattr(jobs, "SessionFactory", FakeSessionFactory)
    monkeypatch.setattr(jobs, "load_runtime_settings", AsyncMock(return_value=get_settings()))
    monkeypatch.setattr(jobs, "get_redis", Mock())
    monkeypatch.setattr(jobs, "_close_resources", AsyncMock())
    for error in errors:
        monkeypatch.setattr(jobs, "process_candidate", AsyncMock(side_effect=error))
        try:
            jobs.run_candidate(str(uuid4()))
        except Exception as escaped:  # noqa: BLE001 - the test records what RQ would see
            raised.append(type(escaped).__name__)
    assert raised == ["ConnectError"]


@pytest.mark.asyncio
async def test_only_lead_only_pages_stop_at_the_evidence_gate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        session.add(NewsAutomationSettings(id=1, enabled=True))
        candidate = await seed_candidate(session)
        session.add(
            NewsEvidence(
                candidate_id=candidate.id,
                role="lead_only",
                is_first_party=False,
                url="https://lead.example/rumour",
                title="Rumour",
                content_hash="l" * 64,
                excerpt="Someone heard something.",
            )
        )
        await session.commit()
        candidate_id = candidate.id
    duplicate_check = AsyncMock()
    monkeypatch.setattr(ai, "jev_duplicate_check", duplicate_check)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
    await engine.dispose()
    assert result == "needs_evidence"
    assert stored is not None
    assert (stored.status, stored.error_code) == ("needs_evidence", "news_evidence_insufficient")
    # Nothing was spent on a candidate a draft could not cite.
    duplicate_check.assert_not_awaited()


@pytest.mark.asyncio
async def test_a_restarting_news_worker_recovers_every_in_flight_candidate_at_once(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from app.news_automation import worker

    # A file, not memory: recover_interrupted disposes the engine it is given.
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'news.db'}")
    tables = cast(list[Table], [model.__table__ for model in NEWS_TABLES])
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    now = datetime.now(UTC)
    async with factory() as session:
        # Cut off two minutes ago by a deploy: far younger than the scheduler's 70 minutes.
        interrupted = await seed_candidate(
            session, status="locale_review", processing_started_at=now - timedelta(minutes=2)
        )
        waiting = await seed_candidate(session)
        interrupted_id, waiting_id = interrupted.id, waiting.id
    monkeypatch.setattr(worker, "SessionFactory", factory)
    monkeypatch.setattr(worker, "engine", engine)

    recovered = await worker.recover_interrupted()

    async with factory() as session:
        statuses = {
            row.id: (row.status, row.error_code)
            for row in await session.scalars(select(NewsCandidate))
        }
    await engine.dispose()
    assert recovered == [interrupted_id]
    assert statuses[interrupted_id] == ("failed", "news_processing_stale")
    assert statuses[waiting_id] == ("discovered", None)


def test_the_news_worker_container_runs_a_pool_after_recovering_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.news_automation import worker

    events: list[object] = []

    async def recover() -> list[UUID]:
        events.append("recover")
        return []

    class Pool:
        def __init__(self, queues: list[str], **kwargs: object) -> None:
            events.append(("pool", queues, kwargs["num_workers"]))

        def start(self) -> None:
            events.append("start")

    monkeypatch.setattr(worker, "recover_interrupted", recover)
    monkeypatch.setattr(worker, "WorkerPool", Pool)
    pool_size = worker.pool_size
    monkeypatch.setattr(worker, "pool_size", lambda configured: configured)
    monkeypatch.setattr("app.news_automation.worker.Redis", Mock())
    monkeypatch.setattr(
        worker, "get_settings", lambda: Mock(redis_url="redis://x", news_worker_processes=3)
    )

    worker.main()

    # Recovery fails every in-flight candidate, so it runs once, before any worker exists.
    assert events == ["recover", ("pool", ["news"], 3), "start"]
    assert pool_size(3, os_name="posix") == 3
    assert pool_size(3, os_name="nt") == 1, "no fork on Windows"


def test_known_statuses_start_with_the_pipelines_in_flight_statuses() -> None:
    from app.news_automation.duplicates import KNOWN_STATUSES

    assert KNOWN_STATUSES[: len(pipeline.ACTIVE_STATUSES)] == pipeline.ACTIVE_STATUSES


@pytest.mark.asyncio
async def test_a_story_already_being_drafted_is_a_known_title() -> None:
    from app.news_automation.duplicates import known_titles

    engine, factory = await database()
    async with factory() as session:
        running = await seed_candidate(session, status="verifying")
        running.source_title = "OpenAI ships a new model"
        waiting = await seed_candidate(session, status="discovered")
        waiting.source_title = "Unrelated waiting story"
        await session.commit()
        fresh = await seed_candidate(session)
        titles = await known_titles(session, fresh)
    await engine.dispose()
    # Two news workers may run two outlets' versions of one story at once.
    assert "OpenAI ships a new model" in titles
    assert "Unrelated waiting story" not in titles


@pytest.mark.asyncio
async def test_the_review_list_asks_for_exactly_the_statuses_it_shows() -> None:
    engine, factory = await database()
    async with factory() as session:
        for status in ("manual_review", "needs_evidence", "needs_evidence", "failed", "published"):
            await seed_candidate(session, status=status)
        review = await service.list_candidates(
            session, page=1, limit=25, status=["manual_review", "shadow_review", "failed"]
        )
        evidence = await service.list_candidates(
            session, page=1, limit=25, status=["needs_evidence"]
        )
        everything = await service.list_candidates(session, page=1, limit=25)
    await engine.dispose()
    assert sorted(row.status for row in review.candidates) == ["failed", "manual_review"]
    assert evidence.total == 2
    assert everything.total == 5


async def seed_owner(session: AsyncSession) -> UUID:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    session.add(owner)
    await session.commit()
    return owner.id


@pytest.mark.asyncio
async def test_automatic_mode_publishes_through_the_final_editor_and_jevs_last_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No shadow gate: nobody has labelled anything, and a first-party page is enough."""

    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        settings = await session.get(NewsAutomationSettings, 1)
        assert settings is not None
        settings.mode, settings.auto_publish_ai = "automatic", True
        await session.commit()
        candidate_id = candidate.id

    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    mocks = stage_one_mocks(monkeypatch)
    translated = stage_two_mocks(monkeypatch)

    async def final_edit(*args: Any) -> tuple[LocaleReviewResult, dict[str, int], str]:
        locale = cast(Locale, args[3])
        if locale in {"zh-TW", "en"}:
            corrected = news_document(f"Clearer {locale}")
            return (
                LocaleReviewResult(verdict="revise", corrected_document=corrected),
                {"input_tokens": 5},
                "claude-opus-5-5",
            )
        return LocaleReviewResult(verdict="pass"), {}, "claude-opus-5-5"

    monkeypatch.setattr(ai, "final_edit", final_edit)

    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        stages = [
            run.stage
            for run in await session.scalars(
                select(NewsPipelineRun)
                .where(NewsPipelineRun.candidate_id == candidate_id)
                .order_by(NewsPipelineRun.started_at)
            )
        ]
        titles = {
            row.locale: row.draft_json["title"]
            for row in await session.scalars(select(GuideArticleLocale))
        }
        audits = [row.action for row in await session.scalars(select(AdminAuditLog))]
    await engine.dispose()

    assert result == "published"
    assert stored is not None and stored.human_decision is None
    assert translated == ["zh-CN", "en", "ja", "ko"]
    assert [stage for stage in stages if stage.startswith("final-edit")] == [
        "final-edit-zh-TW",
        "final-edit-zh-CN",
        "final-edit-en",
        "final-edit-ja",
        "final-edit-ko",
    ]
    assert stages[-1] == "jev-final"
    assert titles["zh-TW"] == "Clearer zh-TW" and titles["en"] == "Clearer en"
    assert titles["ja"] == "Release ja"
    assert "news_candidate_auto_published" in audits
    assert mocks["jev_locales"][-1] == ("zh-TW", "zh-CN", "en", "ja", "ko")


@pytest.mark.asyncio
async def test_jevs_last_call_holds_a_confirmed_article_until_the_owner_publishes_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        owner_id = await seed_owner(session)
        candidate_id = candidate.id

    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    mocks = stage_one_mocks(monkeypatch)
    stage_two_mocks(monkeypatch)

    async def jev(*args: Any, **kwargs: Any) -> list[ai.JevLocaleDecision]:
        locales = kwargs.get("locales", ("zh-TW", "zh-CN", "en", "ja", "ko"))
        mocks["jev_locales"].append(tuple(locales))
        return [
            ai.JevLocaleDecision(locale, "confirm" if locale == "ja" else "act", 0.8, [], {})
            for locale in locales
        ]

    monkeypatch.setattr(ai, "jev_assessments", jev)
    await confirm(factory, candidate_id, owner_id)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        assert stored is not None
        held = (stored.status, stored.error_code, stored.guide_article_id is not None)
        final_jev = [
            (row.locale, row.verdict)
            for row in await session.scalars(
                select(NewsAssessment).where(
                    NewsAssessment.candidate_id == candidate_id,
                    NewsAssessment.assessment_type == "jev",
                )
            )
            if row.details_json.get("stage") == "final"
        ]
        owner_row = await session.get(User, owner_id)
        assert owner_row is not None
        published = await service.publish_candidate(
            session, owner_row, candidate_id, CandidateAction(reason="Checked the Japanese")
        )
    await engine.dispose()

    assert result == "manual_review"
    assert held == ("manual_review", "news_jev_final_hold", True)
    assert ("ja", "manual") in final_jev and len(final_jev) == 5
    assert published.status == "published"


@pytest.mark.asyncio
async def test_the_final_editor_can_hold_a_locale_before_jev_is_asked(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        owner_id = await seed_owner(session)
        candidate_id = candidate.id

    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    mocks = stage_one_mocks(monkeypatch)
    stage_two_mocks(monkeypatch)

    async def final_edit(*args: Any) -> tuple[LocaleReviewResult, dict[str, int], str]:
        if args[3] == "ko":
            return (
                LocaleReviewResult(verdict="manual", issues=["The date is not in the evidence"]),
                {},
                "editor",
            )
        return LocaleReviewResult(verdict="pass"), {}, "editor"

    monkeypatch.setattr(ai, "final_edit", final_edit)
    await confirm(factory, candidate_id, owner_id)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
    await engine.dispose()

    assert result == "manual_review"
    assert stored is not None
    assert (stored.error_code, stored.guide_article_id is not None) == (
        "news_final_edit_hold",
        True,
    )
    assert "ko" in (stored.error_detail or "")
    assert mocks["jev_locales"] == [("zh-TW",)], "Jev is not asked about a held article"


@pytest.mark.asyncio
async def test_a_single_website_that_is_not_first_party_still_waits_for_the_owner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        settings = await session.get(NewsAutomationSettings, 1)
        assert settings is not None
        settings.mode, settings.auto_publish_ai = "automatic", True
        for row in await session.scalars(
            select(NewsEvidence).where(NewsEvidence.candidate_id == candidate.id)
        ):
            row.is_first_party = False
        await session.commit()
        candidate_id = candidate.id

    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    mocks = stage_one_mocks(monkeypatch)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
    await engine.dispose()

    assert result == "manual_review"
    assert stored is not None and stored.error_code == "news_zh_draft_ready"
    mocks["translate"].assert_not_awaited()


@pytest.mark.asyncio
async def test_a_translation_the_reviewer_corrected_gets_its_topic_link_back(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        owner_id = await seed_owner(session)
        candidate_id = candidate.id

    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    stage_one_mocks(monkeypatch)
    stage_two_mocks(monkeypatch)
    corrected: list[Locale] = []

    async def review(*args: Any) -> tuple[LocaleReviewResult, dict[str, int], str]:
        locale = cast(Locale, args[3])
        if locale == "en" and locale not in corrected:
            corrected.append(locale)
            fixed = news_document("Corrected en")
            return LocaleReviewResult(verdict="revise", corrected_document=fixed), {}, "checker"
        return LocaleReviewResult(verdict="pass"), {}, "checker"

    monkeypatch.setattr(ai, "review_locale", review)
    await confirm(factory, candidate_id, owner_id)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        english = next(
            row
            for row in await session.scalars(select(GuideArticleLocale))
            if row.locale == "en"
        )
    await engine.dispose()

    assert result == "published"
    assert english.draft_json["title"] == "Corrected en"
    assert "https://mokaair.com/en/life/topics/ai-news" in [
        block.get("url") for block in english.draft_json["blocks"]
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("saved_article", "second_verdict", "first_issues"),
    [
        pytest.param(False, "manual", ["Original wording is ambiguous"], id="new-manual"),
        pytest.param(False, "revise", ["Original wording is ambiguous"], id="new-revise"),
        pytest.param(True, "manual", ["Original wording is ambiguous"], id="saved-manual"),
        pytest.param(True, "revise", ["Original wording is ambiguous"], id="saved-revise"),
        pytest.param(True, None, ["Original needs an editor"], id="direct-manual"),
        pytest.param(True, "manual", [], id="empty-original-issues"),
    ],
)
async def test_held_locale_review_evidence_describes_the_previewed_original(
    monkeypatch: pytest.MonkeyPatch,
    saved_article: bool,
    second_verdict: str | None,
    first_issues: list[str],
) -> None:
    """A discarded correction's new mistakes must not become the editor's to-do list."""

    async def guide_state(session: AsyncSession) -> dict[str, list[dict[str, Any]]]:
        result = {}
        for model in (GuideArticle, GuideArticleLocale, GuideArticleRevision):
            table = cast(Table, model.__table__)
            rows = await session.execute(select(table).order_by(table.c.id))
            result[table.name] = [deepcopy(dict(row)) for row in rows.mappings()]
        return result

    engine, factory = await database()
    try:
        async with factory() as session:
            owner_id = await seed_owner(session)
            if saved_article:
                candidate_id = await seed_refreshed_candidate(session)
                candidate = await session.get(NewsCandidate, candidate_id)
                assert candidate is not None and candidate.guide_article_id is not None
                article = await session.get(GuideArticle, candidate.guide_article_id)
                assert article is not None
                article.version = 7
                for locale, encoded in candidate.draft_bundle_json.items():
                    localized = GuideArticleLocale(
                        id=uuid4(),
                        article_id=article.id,
                        locale=locale,
                        version=3,
                        draft_json=deepcopy(encoded),
                        published_version=2,
                        published_at=datetime(2026, 9, 1, tzinfo=UTC),
                    )
                    session.add(localized)
                    for version, action, document in (
                        (
                            2,
                            "published",
                            news_document(f"Published {locale}").model_dump(mode="json"),
                        ),
                        (3, "draft_saved", encoded),
                    ):
                        session.add(
                            GuideArticleRevision(
                                article_locale_id=localized.id,
                                version=version,
                                action=action,
                                document_json=deepcopy(document),
                                created_by_user_id=owner_id,
                            )
                        )
                await session.commit()
            else:
                candidate_id = (await seed_single_source_candidate(session)).id

        monkeypatch.setattr(
            ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
        )
        stage_one_mocks(monkeypatch)
        stage_two_mocks(monkeypatch)
        reviewed: list[GuideDocument] = []
        correction = news_document("Correction one introduces a different error")
        unwanted_correction = news_document("Correction two must never replace the preview")
        second_issues = ["The correction invented a quotation absent from the original"]

        async def review(*args: Any) -> tuple[LocaleReviewResult, dict[str, int], str]:
            if args[3] != "en":
                return LocaleReviewResult(verdict="pass"), {}, "other-locale-checker"
            reviewed.append(cast(GuideDocument, args[4]).model_copy(deep=True))
            if len(reviewed) == 1:
                return (
                    LocaleReviewResult(
                        verdict="manual" if second_verdict is None else "revise",
                        issues=first_issues,
                        corrected_document=None if second_verdict is None else correction,
                    ),
                    {"input_tokens": 11},
                    "original-reviewer",
                )
            assert len(reviewed) == 2, "Only one correction may be attempted"
            return (
                LocaleReviewResult(
                    verdict="manual" if second_verdict == "manual" else "revise",
                    issues=second_issues,
                    corrected_document=unwanted_correction if second_verdict == "revise" else None,
                ),
                {"input_tokens": 22},
                "correction-reviewer",
            )

        monkeypatch.setattr(ai, "review_locale", review)
        if not saved_article:
            await confirm(factory, candidate_id, owner_id)
        async with factory() as session:
            before = await service.candidate_detail(session, candidate_id)
            guides_before = await guide_state(session)
        async with factory() as session:
            result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        # Read committed public detail in another session, not the worker's identity map.
        async with factory() as session:
            detail = await service.candidate_detail(session, candidate_id)
            guides_after = await guide_state(session)

        assert result == "manual_review"
        assert detail.status == "manual_review"
        assert detail.error_code == "news_locale_review_failed"
        assert detail.guide_article_id == before.guide_article_id
        assert guides_after == guides_before, "No guide drafts, revisions or publication may move"
        for locale, document in before.documents.items():
            if locale != "en":
                assert detail.documents[locale] == document
        held = [
            item
            for item in detail.assessments
            if item.assessment_type == "locale_review" and item.locale == "en"
        ]
        assert len(held) == 1 and held[0].verdict == "manual"
        assessment = held[0]
        assert assessment.reasons == first_issues
        assert assessment.model == "original-reviewer"
        assert assessment.details["round"] == 1
        assert assessment.details["document_sha256"] == document_fingerprint(reviewed[0])
        assert detail.documents["en"] == reviewed[0]
        assert document_fingerprint(detail.documents["en"]) == document_fingerprint(reviewed[0])
        assert all(
            issue not in item.reasons for item in detail.assessments for issue in second_issues
        )
        if second_verdict is None:
            assert len(reviewed) == 1
            assert "discarded_correction" not in assessment.details
        else:
            assert len(reviewed) == 2
            assert reviewed[1].title == correction.title
            assert document_fingerprint(reviewed[0]) != document_fingerprint(reviewed[1])
            assert assessment.details["discarded_correction"] == {
                "round": 2,
                "verdict": second_verdict,
                "issues": second_issues,
                "model": "correction-reviewer",
                "document_sha256": document_fingerprint(reviewed[1]),
            }
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_an_edit_that_breaks_a_site_check_gets_one_fix_then_falls_back(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """On 2026-09-26 the final editor rewrote a crypto disclaimer out of its callout."""

    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        owner_id = await seed_owner(session)
        candidate_id = candidate.id

    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    stage_one_mocks(monkeypatch)
    stage_two_mocks(monkeypatch)

    def checks(document: GuideDocument, *_args: Any, **_kwargs: Any) -> list[str]:
        return ["crypto_disclaimer_block: broken"] if document.title == "Broken" else []

    monkeypatch.setattr(pipeline, "hard_policy_problems", checks)
    retries: dict[str, list[str]] = {}

    async def final_edit(
        *args: Any, problems: list[str] | None = None
    ) -> tuple[LocaleReviewResult, dict[str, int], str]:
        locale = cast(str, args[3])
        if locale not in {"ja", "ko"}:
            return LocaleReviewResult(verdict="pass"), {}, "editor"
        if problems:
            retries[locale] = problems
            title = "Fixed ko" if locale == "ko" else "Broken"
        else:
            title = "Broken"
        return (
            LocaleReviewResult(verdict="revise", corrected_document=news_document(title)),
            {},
            "editor",
        )

    monkeypatch.setattr(ai, "final_edit", final_edit)
    await confirm(factory, candidate_id, owner_id)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        titles = {
            row.locale: row.draft_json["title"]
            for row in await session.scalars(select(GuideArticleLocale))
        }
        notes = [
            reason
            for row in await session.scalars(
                select(NewsAssessment).where(NewsAssessment.locale == "ja")
            )
            if row.details_json.get("stage") == "final_edit"
            for reason in row.reasons_json
        ]
    await engine.dispose()

    assert result == "published"
    assert retries == {
        "ja": ["crypto_disclaimer_block: broken"],
        "ko": ["crypto_disclaimer_block: broken"],
    }
    assert titles["ko"] == "Fixed ko", "the second call fixed it, so the edit stays"
    assert titles["ja"] == "Release ja", "still broken, so the reviewed translation stays"
    assert any("was not kept" in note for note in notes)


async def seed_refreshed_candidate(session: AsyncSession) -> UUID:
    """A saved five-locale article whose evidence an editor just refreshed."""

    candidate = await seed_single_source_candidate(session)
    settings = await session.get(NewsAutomationSettings, 1)
    assert settings is not None
    settings.mode, settings.auto_publish_ai = "automatic", True
    article = GuideArticle(id=uuid4(), slug=SLUG, kind="life", news_date=EVENT_DAY)
    session.add(article)
    candidate.guide_article_id = article.id
    candidate.event_date = EVENT_DAY
    candidate.would_publish = True
    candidate.error_code = EVIDENCE_REFRESH_MARKER
    candidate.draft_bundle_json = {
        locale: news_document(f"Saved {locale}").model_dump(mode="json")
        for locale in ("zh-TW", "zh-CN", "en", "ja", "ko")
    }
    await session.commit()
    return candidate.id


@pytest.mark.asyncio
async def test_a_refreshed_article_is_rechecked_and_goes_out_only_on_jevs_last_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate_id = await seed_refreshed_candidate(session)

    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    mocks = stage_one_mocks(monkeypatch)
    stage_two_mocks(monkeypatch)
    verify = AsyncMock(return_value=(VerificationResult(verdict="pass"), {}, "checker"))
    monkeypatch.setattr(ai, "verify_article", verify)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
    await engine.dispose()

    assert result == "published"
    assert stored is not None and stored.error_code is None
    # The saved article is fact-checked against the new evidence, never drafted again.
    verify.assert_awaited()
    mocks["draft"].assert_not_awaited()
    mocks["final_edit"].assert_not_awaited()
    assert mocks["jev_locales"] == [("zh-TW", "zh-CN", "en", "ja", "ko")], "Jev's last call ran"


@pytest.mark.asyncio
async def test_a_refreshed_article_jev_holds_waits_for_the_owner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate_id = await seed_refreshed_candidate(session)

    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    stage_one_mocks(monkeypatch)
    stage_two_mocks(monkeypatch)

    async def jev(*args: Any, **kwargs: Any) -> list[ai.JevLocaleDecision]:
        locales = kwargs.get("locales", ("zh-TW", "zh-CN", "en", "ja", "ko"))
        return [ai.JevLocaleDecision(locale, "hold", 0.3, [], {}) for locale in locales]

    monkeypatch.setattr(ai, "jev_assessments", jev)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
    await engine.dispose()

    assert result == "manual_review"
    assert stored is not None and stored.error_code == "news_jev_final_hold"


def test_a_candidate_waiting_for_a_subscription_account_tries_again_in_half_an_hour(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    queue = Mock()
    monkeypatch.setattr(jobs, "SessionFactory", FakeSessionFactory)
    monkeypatch.setattr(jobs, "load_runtime_settings", AsyncMock(return_value=get_settings()))
    monkeypatch.setattr(jobs, "process_candidate", AsyncMock(return_value="paused"))
    monkeypatch.setattr(jobs, "get_redis", Mock())
    monkeypatch.setattr(jobs, "_close_resources", AsyncMock())
    monkeypatch.setattr(jobs, "_queue", lambda: (Mock(), queue))
    candidate_id = str(uuid4())
    jobs.run_candidate(candidate_id)
    assert queue.enqueue_in.call_count == 1
    delay, job, target = queue.enqueue_in.call_args.args
    assert (delay, job, target) == (
        timedelta(minutes=30),
        "app.news_automation.jobs.run_candidate",
        candidate_id,
    )
    assert "-paused-" in queue.enqueue_in.call_args.kwargs["job_id"]


@pytest.mark.asyncio
async def test_when_every_subscription_account_is_full_the_story_waits_instead_of_failing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        candidate_id = candidate.id

    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    stage_one_mocks(monkeypatch)
    full = AppError(429, "subscription_quota_paused", "every Claude account is at 100%")
    monkeypatch.setattr(ai, "draft_article", AsyncMock(side_effect=full))
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        draft_run = await session.scalar(
            select(NewsPipelineRun).where(
                NewsPipelineRun.candidate_id == candidate_id, NewsPipelineRun.stage == "draft"
            )
        )
    await engine.dispose()

    assert result == "paused"
    assert stored is not None
    assert (stored.status, stored.error_code) == ("discovered", "news_subscription_paused")
    assert draft_run is not None and draft_run.error_code == "subscription_quota_paused"


def _solar_document(factor: int, locale: str = "zh-TW", *, broken: bool = False) -> GuideDocument:
    document = news_document(f"Solar capacity {locale}").model_dump(mode="json")
    document["blocks"] = [
        {"type": "summary", "items": [f"Capacity can reach {factor} times.", "An official plan."]},
        {"type": "paragraph", "text": f"太陽能可達 {factor} 倍。" if locale == "zh-TW"
         else f"Capacity {factor} times."},
    ]
    if broken:
        document["blocks"] = document["blocks"][1:]
    return GuideDocument.model_validate(document)


def _solar_factor(document: GuideDocument) -> int:
    paragraph = next(block for block in document.blocks if block.type == "paragraph")
    return int(paragraph.text.split()[1])


async def _translate_solar(*args: Any) -> tuple[LocalizedDocument, dict[str, int], str]:
    # Read the actual input; a canned "8" would hide translation from the stale 4x source.
    source, locale = cast(GuideDocument, args[2]), cast(Locale, args[3])
    return LocalizedDocument(document=_solar_document(_solar_factor(source), locale)), {}, "writer"


SolarCandidate = tuple[async_sessionmaker[AsyncSession], UUID, UUID, dict[str, Any]]


@pytest.fixture
async def confirmed_solar_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncIterator[SolarCandidate]:
    engine, factory = await database()
    try:
        async with factory() as session:
            candidate = await seed_single_source_candidate(session)
            owner_id = await seed_owner(session)
            candidate_id = candidate.id
        monkeypatch.setattr(
            ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
        )
        mocks = stage_one_mocks(monkeypatch)
        draft, usage, model = mocks["draft"].return_value
        mocks["draft"].return_value = (
            draft.model_copy(update={"document": _solar_document(4)}), usage, model
        )
        stage_two_mocks(monkeypatch)
        mocks["solar_translate"] = AsyncMock(side_effect=_translate_solar)
        mocks["solar_review"] = AsyncMock(
            return_value=(LocaleReviewResult(verdict="pass"), {}, "checker")
        )
        monkeypatch.setattr(ai, "translate_article", mocks["solar_translate"])
        monkeypatch.setattr(ai, "review_locale", mocks["solar_review"])

        def summary_check(document: GuideDocument, *args: Any, **kwargs: Any) -> list[str]:
            # Exercise the real hard-check rejection while keeping this fixture independent
            # of generated artwork and the unrelated publication layout requirements.
            return [
                problem for problem in actual_hard_policy_problems(document, *args, **kwargs)
                if problem.startswith("news_summary:")
            ]

        monkeypatch.setattr(pipeline, "hard_policy_problems", summary_check)
        await confirm(factory, candidate_id, owner_id)
        yield factory, candidate_id, owner_id, mocks
    finally:
        await engine.dispose()


@pytest.mark.parametrize("english_edit_falls_back", [False, True])
@pytest.mark.asyncio
async def test_final_source_fact_reaches_translations_reviews_and_foreign_edit_fallback(
    monkeypatch: pytest.MonkeyPatch,
    confirmed_solar_candidate: SolarCandidate,
    english_edit_falls_back: bool,
) -> None:
    factory, candidate_id, _owner_id, mocks = confirmed_solar_candidate
    final_sources: list[tuple[str, int]] = []
    retried: list[str] = []

    async def final_edit(
        *args: Any, problems: list[str] | None = None
    ) -> tuple[LocaleReviewResult, dict[str, int], str]:
        locale = cast(Locale, args[3])
        final_sources.append((locale, _solar_factor(args[2])))
        if problems:
            retried.append(locale)
        if locale == "zh-TW":
            corrected = _solar_document(8)
        elif locale == "en" and english_edit_falls_back:
            corrected = _solar_document(64, "en", broken=True)
        else:
            return LocaleReviewResult(verdict="pass"), {}, "editor"
        return LocaleReviewResult(verdict="revise", corrected_document=corrected), {}, "editor"

    monkeypatch.setattr(ai, "final_edit", final_edit)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        assert stored is not None
        saved = {
            row.locale: GuideDocument.model_validate(row.draft_json)
            for row in await session.scalars(select(GuideArticleLocale))
        }
        assessments = list(await session.scalars(select(NewsAssessment)))
        stages = list(await session.scalars(
            select(NewsPipelineRun.stage).where(NewsPipelineRun.candidate_id == candidate_id)
            .order_by(NewsPipelineRun.started_at)
        ))
        assert _solar_factor(GuideDocument.model_validate(stored.draft_bundle_json["zh-TW"])) == 8
    assert result == "published"
    assert {locale: _solar_factor(doc) for locale, doc in saved.items()} == {
        "zh-TW": 8, "zh-CN": 8, "en": 8, "ja": 8, "ko": 8,
    }
    assert stages.index("final-edit-zh-TW") < stages.index("translation-zh-CN")
    assert [call.args[3] for call in mocks["solar_translate"].await_args_list] == [
        "zh-CN", "en", "ja", "ko"
    ]
    assert all(
        _solar_factor(call.args[2]) == 8 for call in mocks["solar_translate"].await_args_list
    )
    assert len(mocks["solar_review"].await_args_list) == 4
    assert all(
        (_solar_factor(call.args[2]), _solar_factor(call.args[4])) == (8, 8)
        for call in mocks["solar_review"].await_args_list
    )
    assert final_sources == [
        ("zh-TW", 4), ("zh-CN", 8), ("en", 8),
        *([("en", 8)] if english_edit_falls_back else []), ("ja", 8), ("ko", 8),
    ]
    assert retried == (["en"] if english_edit_falls_back else [])
    final_en = next(row for row in assessments
                    if row.locale == "en" and row.details_json.get("stage") == "final_edit")
    assert final_en.details_json["document_sha256"] == document_fingerprint(saved["en"])
    assert final_en.details_json["source_document_sha256"] == document_fingerprint(saved["zh-TW"])
    assert (
        any("was not kept" in reason for reason in final_en.reasons_json) == english_edit_falls_back
    )
    mocks["draft"].assert_awaited_once()


@pytest.mark.parametrize("second_edit_passes", [False, True])
@pytest.mark.asyncio
async def test_final_source_uses_only_the_accepted_zh_edit_after_hard_check_retry(
    monkeypatch: pytest.MonkeyPatch,
    confirmed_solar_candidate: SolarCandidate,
    second_edit_passes: bool,
) -> None:
    factory, candidate_id, _owner_id, mocks = confirmed_solar_candidate
    corrections: list[list[str] | None] = []

    async def final_edit(
        *args: Any, problems: list[str] | None = None
    ) -> tuple[LocaleReviewResult, dict[str, int], str]:
        if args[3] != "zh-TW":
            return LocaleReviewResult(verdict="pass"), {}, "editor"
        corrections.append(problems)
        corrected = _solar_document(8, broken=not (problems and second_edit_passes))
        return LocaleReviewResult(verdict="revise", corrected_document=corrected), {}, "editor"

    monkeypatch.setattr(ai, "final_edit", final_edit)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        assert stored is not None
        source = await service.verified_zh_draft(session, stored)
        factors = {
            row.locale: _solar_factor(GuideDocument.model_validate(row.draft_json))
            for row in await session.scalars(select(GuideArticleLocale))
        }
        zh_edits = [row for row in await session.scalars(select(NewsAssessment))
                    if row.locale == "zh-TW" and row.details_json.get("stage") == "final_edit"]
    expected = 8 if second_edit_passes else 4
    assert result == "published" and set(factors.values()) == {expected}
    assert source is not None and _solar_factor(source) == expected
    assert corrections == [None, ["news_summary: a summary block is required"]]
    assert len(zh_edits) == 1 and zh_edits[0].details_json["revised"] is second_edit_passes
    assert all(
        _solar_factor(call.args[2]) == expected for call in mocks["solar_translate"].await_args_list
    )
    assert mocks["solar_translate"].await_count == 4


@pytest.mark.asyncio
async def test_final_source_manual_hold_blocks_publication_and_jevs_last_call(
    monkeypatch: pytest.MonkeyPatch, confirmed_solar_candidate: SolarCandidate,
) -> None:
    factory, candidate_id, _owner_id, mocks = confirmed_solar_candidate

    async def final_edit(*args: Any) -> tuple[LocaleReviewResult, dict[str, int], str]:
        if args[3] == "zh-TW":
            return (
                LocaleReviewResult(verdict="manual", issues=["Check the capacity claim"]),
                {}, "editor",
            )
        return LocaleReviewResult(verdict="pass"), {}, "editor"

    monkeypatch.setattr(ai, "final_edit", final_edit)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        assert stored is not None
        assert (stored.status, stored.error_code, stored.human_decision) == (
            "manual_review", "news_final_edit_hold", "publish"
        )
        assert "zh-TW" in (stored.error_detail or "")
        locales = list(await session.scalars(select(GuideArticleLocale)))
        held = [row for row in await session.scalars(select(NewsAssessment))
                if row.locale == "zh-TW" and row.details_json.get("stage") == "final_edit"]
    assert result == "manual_review"
    assert len(locales) == 5 and all(row.published_version is None for row in locales)
    assert len(held) == 1 and held[0].verdict == "manual"
    assert held[0].reasons_json == ["Check the capacity claim"]
    assert mocks["jev_locales"] == [("zh-TW",)]


@pytest.mark.asyncio
async def test_final_source_and_verification_survive_translation_failure_and_owner_requeue(
    monkeypatch: pytest.MonkeyPatch, confirmed_solar_candidate: SolarCandidate,
) -> None:
    factory, candidate_id, owner_id, mocks = confirmed_solar_candidate
    final_edit = AsyncMock(return_value=(
        LocaleReviewResult(verdict="revise", corrected_document=_solar_document(8)), {}, "editor"
    ))
    monkeypatch.setattr(ai, "final_edit", final_edit)
    observed_before_failure: list[tuple[int, bool]] = []

    async def fail_translation(*args: Any) -> tuple[LocalizedDocument, dict[str, int], str]:
        async with factory() as persisted:
            stored = await persisted.get(NewsCandidate, candidate_id)
            assert stored is not None
            saved_source = GuideDocument.model_validate(stored.draft_bundle_json["zh-TW"])
            verified = await service.verified_zh_draft(persisted, stored)
            observed_before_failure.append((_solar_factor(saved_source), verified is not None))
        raise AppError(503, "test_translation_unavailable", "Translator temporarily unavailable")

    failed_translate = AsyncMock(side_effect=fail_translation)
    monkeypatch.setattr(ai, "translate_article", failed_translate)
    async with factory() as session:
        with pytest.raises(AppError, match="Translator temporarily unavailable"):
            await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
    assert observed_before_failure == [(8, True)], (
        "the source and verification commit before translation"
    )
    final_edit.assert_awaited_once()
    failed_translate.assert_awaited_once()
    async with factory() as session:
        stored = await session.get(NewsCandidate, candidate_id)
        owner = await session.get(User, owner_id)
        assert stored is not None and owner is not None
        assert (stored.status, stored.human_decision, stored.guide_article_id) == (
            "failed", "publish", None
        )
        source = GuideDocument.model_validate(stored.draft_bundle_json["zh-TW"])
        verification = await session.scalar(
            select(NewsAssessment).where(
                NewsAssessment.candidate_id == candidate_id,
                NewsAssessment.assessment_type == "verification",
            ).order_by(NewsAssessment.created_at.desc()).limit(1)
        )
        assert verification is not None
        assert verification.details_json["document_sha256"] == document_fingerprint(source)
        queued = await service.approve_candidate(
            session, owner, candidate_id, CandidateAction(reason="Retry the recovered translator")
        )
        assert queued.status == "discovered"
    monkeypatch.setattr(ai, "final_edit", AsyncMock(return_value=(
        LocaleReviewResult(verdict="pass"), {}, "editor"
    )))
    monkeypatch.setattr(ai, "translate_article", mocks["solar_translate"])
    async with factory() as session:
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "published"
        factors = [_solar_factor(GuideDocument.model_validate(row.draft_json))
                   for row in await session.scalars(select(GuideArticleLocale))]
    assert factors == [8] * 5
    mocks["draft"].assert_awaited_once()


@pytest.mark.asyncio
async def test_duplicate_question_tells_jev_a_new_model_version_is_a_new_event(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.ai.jev import NoulAnswer

    asked: list[dict[str, Any]] = []

    class Client:
        async def ask(self, state: dict[str, Any], questions: dict[str, Any]) -> tuple[dict, Any]:
            asked.append({"state": state, "questions": questions})
            return {"duplicate": NoulAnswer(type="noul", noul=0.1)}, None

        async def close(self) -> None:
            return None

    monkeypatch.setattr(ai, "consume_jev_call", AsyncMock(return_value=True))
    monkeypatch.setattr(ai, "jev_client", lambda _environment: Client())
    verdict, _probability, _reasons = await ai.jev_duplicate_check(
        cast(Any, None),
        get_settings(),
        "Introducing GPT-6.1 Sol",
        "GPT-6.1 Sol is the latest model family in the GPT-6 series.",
        ["GPT-6 Sol and Luna launch: API price cuts, available in Codex"],
    )
    instructions = asked[0]["questions"]["duplicate"].instructions
    # The pair that the check was likely to hold as "the same event" (task 2026-09-30).
    assert "new version or successor" in instructions
    assert "GPT-6.1 Sol after GPT-6 Sol" in instructions
    assert verdict == "distinct"
