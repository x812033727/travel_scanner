"""What an editor can do with a news candidate in each state, and where the pipeline
parks a candidate that stopped before its five-locale article existed."""

from __future__ import annotations

from datetime import timedelta
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.guides.models import GuideArticle, GuideArticleLocale
from app.models import AdminAuditLog, User
from app.news_automation import ai, pipeline, service
from app.news_automation.duplicates import DUPLICATE_UNCERTAIN, closest_titles
from app.news_automation.models import (
    LOCALES,
    NewsAssessment,
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
)
from app.news_automation.policy import ZH_DRAFT_READY, document_fingerprint
from app.news_automation.schemas import (
    CandidateAction,
    EditorialDraft,
    SettingsWrite,
    VerificationResult,
)
from app.problems import AppError
from tests.test_news_pipeline import (
    EVENT_DAY,
    FIRST_PARTY_URL,
    LEAD_URL,
    SLUG,
    TODAY,
    database,
    news_document,
    seed_candidate,
    seed_published_news,
)

EDITOR = User(id=uuid4(), email="editor@example.com", password_hash="unused")
ACTION = CandidateAction(reason="Checked by hand")
STATUSES = (
    "discovered",
    "drafting",
    "shadow_review",
    "manual_review",
    "needs_evidence",
    "needs_redraft",
    "published",
    "duplicate",
    "rejected",
    "failed",
)
RETRYABLE = {"manual_review", "shadow_review", "needs_evidence", "needs_redraft", "failed"}
REJECTABLE = RETRYABLE | {"duplicate"}


async def add_evidence(session: AsyncSession, candidate: NewsCandidate) -> None:
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
    await session.commit()


async def add_article(session: AsyncSession, candidate: NewsCandidate) -> None:
    article = GuideArticle(id=uuid4(), slug=SLUG, kind="life", news_date=EVENT_DAY)
    session.add(article)
    for locale in LOCALES:
        session.add(
            GuideArticleLocale(
                article_id=article.id,
                locale=locale,
                draft_json=news_document(f"Edited {locale}").model_dump(mode="json"),
            )
        )
    candidate.guide_article_id = article.id
    await session.commit()


def eligible_draft() -> EditorialDraft:
    return EditorialDraft.model_validate(
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


@pytest.mark.parametrize("status", STATUSES)
@pytest.mark.asyncio
async def test_retry_and_reject_accept_exactly_the_statuses_a_person_can_act_on(
    status: str,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        retried = (await seed_candidate(session, status=status)).id
        rejected = (await seed_candidate(session, status=status)).id
        outcomes: dict[str, str] = {}
        for name, action, candidate_id in (
            ("retry", service.retry_candidate, retried),
            ("reject", service.reject_candidate, rejected),
        ):
            try:
                detail = await action(session, EDITOR, candidate_id, ACTION)
                outcomes[name] = detail.status
            except AppError as problem:
                await session.rollback()
                assert problem.status == 409
                outcomes[name] = "refused"
    await engine.dispose()
    assert outcomes["retry"] == ("discovered" if status in RETRYABLE else "refused")
    assert outcomes["reject"] == ("rejected" if status in REJECTABLE else "refused")


@pytest.mark.parametrize(
    ("status", "error_code"),
    [
        ("manual_review", "news_jev_manual"),
        ("manual_review", "news_evidence_changed"),
        ("needs_redraft", "news_verification_failed"),
        ("shadow_review", None),
        ("failed", DUPLICATE_UNCERTAIN),
    ],
)
@pytest.mark.asyncio
async def test_not_a_duplicate_only_answers_an_uncertain_duplicate_check(
    status: str, error_code: str | None
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_candidate(session, status=status)
        candidate.error_code = error_code
        await session.commit()
        with pytest.raises(AppError) as refused:
            await service.clear_duplicate_candidate(session, EDITOR, candidate.id, ACTION)
    await engine.dispose()
    assert refused.value.code == "news_candidate_not_duplicate_uncertain"


@pytest.mark.asyncio
async def test_not_a_duplicate_without_an_article_starts_a_new_draft() -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_candidate(session, status="manual_review")
        candidate.error_code = DUPLICATE_UNCERTAIN
        candidate.evidence_hash = "a" * 64
        await session.commit()

        detail = await service.clear_duplicate_candidate(session, EDITOR, candidate.id, ACTION)
        answers = list(
            await session.scalars(
                select(NewsAssessment).where(NewsAssessment.candidate_id == candidate.id)
            )
        )
        actions = list(await session.scalars(select(AdminAuditLog.action)))
    await engine.dispose()
    assert (detail.status, detail.error_code) == ("discovered", None)
    assert [
        (row.assessment_type, row.provider, row.verdict, row.evidence_hash, row.reasons_json)
        for row in answers
    ] == [("duplicate", "human", "pass", "a" * 64, ["Checked by hand"])]
    assert actions == ["news_candidate_duplicate_cleared"]


@pytest.mark.asyncio
async def test_not_a_duplicate_with_an_article_reverifies_the_edited_drafts() -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_candidate(session, status="manual_review")
        candidate.error_code = DUPLICATE_UNCERTAIN
        await add_article(session, candidate)

        detail = await service.clear_duplicate_candidate(session, EDITOR, candidate.id, ACTION)
        stored = await session.get(NewsCandidate, candidate.id)
    await engine.dispose()
    assert detail.status == "discovered"
    assert detail.error_code == pipeline.REVERIFY_MARKER
    assert stored is not None
    assert set(stored.draft_bundle_json) == set(LOCALES)
    assert stored.draft_bundle_json["en"]["title"] == "Edited en"


@pytest.mark.asyncio
async def test_an_uncertain_duplicate_cleared_by_an_editor_is_not_sent_to_jev_again(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    async with factory() as session:
        session.add(NewsAutomationSettings(id=1, enabled=True))
        candidate = await seed_candidate(session)
        await add_evidence(session, candidate)
        # Something to compare with, or the check is skipped as trivially distinct.
        await seed_published_news(
            session, "ai-news-earlier-release-20260901", TODAY, {"en": "An earlier release"}
        )
        candidate_id = candidate.id

    duplicate_check = AsyncMock(return_value=("manual", 0.5, ["semantic_duplicate_uncertain"]))
    draft = AsyncMock(return_value=(eligible_draft(), {}, "writer"))
    monkeypatch.setattr(ai, "jev_duplicate_check", duplicate_check)
    monkeypatch.setattr(ai, "draft_article", draft)
    monkeypatch.setattr(
        ai,
        "verify_article",
        AsyncMock(return_value=(VerificationResult(verdict="manual"), {}, "checker")),
    )

    async with factory() as session:
        first = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        held = await session.get(NewsCandidate, candidate_id)
        assert held is not None
        assert (first, held.error_code) == ("manual_review", DUPLICATE_UNCERTAIN)
        await service.clear_duplicate_candidate(session, EDITOR, candidate_id, ACTION)
    async with factory() as session:
        second = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
    await engine.dispose()

    duplicate_check.assert_awaited_once()
    draft.assert_awaited_once()
    # It went on to the draft and stopped at verification, which has no article yet.
    assert second == "needs_redraft"


@pytest.mark.parametrize(
    ("has_article", "expected"), [(False, "needs_redraft"), (True, "manual_review")]
)
@pytest.mark.asyncio
async def test_a_verifier_rejection_waits_for_a_redraft_unless_an_article_can_be_fixed(
    monkeypatch: pytest.MonkeyPatch, has_article: bool, expected: str
) -> None:
    engine, factory = await database()
    async with factory() as session:
        session.add(NewsAutomationSettings(id=1, enabled=True))
        candidate = await seed_candidate(session)
        await add_evidence(session, candidate)
        if has_article:
            await add_article(session, candidate)
        candidate_id = candidate.id

    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.0, []))
    )
    monkeypatch.setattr(
        ai, "draft_article", AsyncMock(return_value=(eligible_draft(), {}, "writer"))
    )
    monkeypatch.setattr(
        ai,
        "verify_article",
        AsyncMock(return_value=(VerificationResult(verdict="manual"), {}, "checker")),
    )
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
    await engine.dispose()
    assert result == expected
    assert stored is not None
    assert (stored.status, stored.error_code) == (expected, "news_verification_failed")


@pytest.mark.asyncio
async def test_the_detail_lists_the_closest_titles_only_while_a_duplicate_is_uncertain() -> None:
    engine, factory = await database()
    async with factory() as session:
        yesterday = TODAY - timedelta(days=1)
        for index, title in enumerate(
            ("Chip maker opens a factory", "Model release notes", "Weather satellite launch")
        ):
            await seed_published_news(
                session, f"ai-news-story-{index}-{yesterday:%Y%m%d}", yesterday, {"en": title}
            )
        waiting = await seed_candidate(session, status="manual_review")
        waiting.error_code = DUPLICATE_UNCERTAIN
        held = await seed_candidate(session, status="manual_review")
        held.error_code = "news_jev_manual"
        await session.commit()

        waiting_detail = await service.candidate_detail(session, waiting.id)
        held_detail = await service.candidate_detail(session, held.id)
    await engine.dispose()
    # seed_candidate titles every candidate "Model release", the held one included.
    assert waiting_detail.similar_titles[:2] == ["Model release", "Model release notes"]
    assert held_detail.similar_titles == []


def test_closest_titles_rank_by_likeness_and_ignore_case() -> None:
    titles = ["Weather report", "OPENAI SHIPS A NEW MODEL", "OpenAI ships new models to Europe"]
    assert closest_titles("OpenAI ships a new model", titles, limit=2) == [
        "OPENAI SHIPS A NEW MODEL",
        "OpenAI ships new models to Europe",
    ]


async def verified_zh_draft(session: AsyncSession, candidate: NewsCandidate) -> None:
    """Give a candidate a stored zh-TW draft and the passing verification that matches it."""

    document = news_document("模型發布")
    candidate.draft_bundle_json = {"zh-TW": document.model_dump(mode="json")}
    candidate.evidence_hash = "a" * 64
    session.add(
        NewsAssessment(
            candidate_id=candidate.id,
            assessment_type="verification",
            verdict="pass",
            details_json={"document_sha256": document_fingerprint(document)},
            evidence_hash="a" * 64,
            prompt_version="news-v1",
        )
    )
    await session.commit()


@pytest.mark.asyncio
async def test_confirming_a_verified_chinese_draft_queues_the_translations() -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_candidate(session, status="manual_review")
        candidate.error_code = ZH_DRAFT_READY
        await verified_zh_draft(session, candidate)

        detail = await service.approve_candidate(session, EDITOR, candidate.id, ACTION)
        human = list(
            await session.scalars(
                select(NewsAssessment).where(
                    NewsAssessment.candidate_id == candidate.id,
                    NewsAssessment.assessment_type == "human",
                )
            )
        )
        actions = list(await session.scalars(select(AdminAuditLog.action)))
    await engine.dispose()
    assert (detail.status, detail.human_decision, detail.error_code) == (
        "discovered",
        "publish",
        None,
    )
    assert [(row.verdict, row.created_by_user_id) for row in human] == [("publish", EDITOR.id)]
    assert actions == ["news_candidate_publish_confirmed"]


@pytest.mark.parametrize(
    ("status", "error_code", "decision", "verified"),
    [
        ("manual_review", ZH_DRAFT_READY, None, False),
        ("manual_review", "news_jev_manual", None, True),
        ("manual_review", DUPLICATE_UNCERTAIN, None, True),
        ("manual_review", "news_evidence_changed", "publish", True),
        ("needs_redraft", "news_verification_failed", None, True),
        ("published", None, "publish", True),
    ],
)
@pytest.mark.asyncio
async def test_confirmation_needs_a_chinese_draft_waiting_for_it(
    status: str, error_code: str | None, decision: str | None, verified: bool
) -> None:
    engine, factory = await database()
    async with factory() as session:
        candidate = await seed_candidate(session, status=status)
        candidate.error_code = error_code
        candidate.human_decision = decision
        if verified:
            await verified_zh_draft(session, candidate)
        else:
            await session.commit()
        with pytest.raises(AppError) as refused:
            await service.approve_candidate(session, EDITOR, candidate.id, ACTION)
    await engine.dispose()
    assert refused.value.code == "news_candidate_not_approvable"


@pytest.mark.asyncio
async def test_a_confirmed_draft_that_failed_can_be_confirmed_again_and_retry_forgets_it() -> (
    None
):
    engine, factory = await database()
    async with factory() as session:
        stalled = await seed_candidate(session, status="failed")
        stalled.human_decision = "publish"
        await verified_zh_draft(session, stalled)
        again = await service.approve_candidate(session, EDITOR, stalled.id, ACTION)

        redraft = await seed_candidate(session, status="manual_review")
        redraft.error_code = ZH_DRAFT_READY
        redraft.human_decision = "publish"
        await session.commit()
        retried = await service.retry_candidate(session, EDITOR, redraft.id, ACTION)
    await engine.dispose()
    assert (again.status, again.human_decision) == ("discovered", "publish")
    assert (retried.status, retried.human_decision) == ("discovered", None)


def _settings_write(**changes: object) -> SettingsWrite:
    values: dict[str, object] = {
        "enabled": True,
        "mode": "automatic",
        "writer_provider": "minimax",
        "verifier_provider": "minimax",
        "global_concurrency": 2,
        "per_vertical_concurrency": 1,
        "min_shadow_days": 14,
        "min_shadow_candidates": 50,
        "min_human_agreement": 0.95,
        "jev_act_confidence": 0.9,
        "auto_publish_ai": True,
        "auto_publish_tech": True,
        "auto_publish_crypto": True,
        "prompt_version": "news-v1",
        "policy_version": "news-policy-v1",
    }
    values.update(changes)
    return SettingsWrite.model_validate(values)


@pytest.mark.asyncio
async def test_auto_publish_needs_automatic_mode_but_no_shadow_gate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    monkeypatch.setattr(service, "settings_view", AsyncMock(return_value="view"))
    async with factory() as session:
        session.add(NewsAutomationSettings(id=1))
        owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
        session.add(owner)
        await session.commit()
        # Nobody has labelled a single candidate, and auto-publish still switches on.
        assert await service.update_settings(session, owner, _settings_write()) == "view"
        row = await session.get(NewsAutomationSettings, 1)
        assert row is not None
        assert (row.auto_publish_ai, row.editor_provider, row.editor_model) == (
            True,
            "anthropic",
            "claude-opus-5-5",
        )
        started = row.shadow_started_at_ai
        # Choosing another editor restarts the agreement figures but leaves autopilot on.
        await service.update_settings(
            session, owner, _settings_write(editor_provider="minimax", editor_model=None)
        )
        await session.refresh(row)
        assert (row.mode, row.auto_publish_ai, row.editor_provider) == (
            "automatic",
            True,
            "minimax",
        )
        assert row.shadow_started_at_ai >= started
        with pytest.raises(AppError) as shadow:
            await service.update_settings(session, owner, _settings_write(mode="shadow"))
    await engine.dispose()
    assert shadow.value.code == "news_mode_shadow"


async def held_for_changed_evidence(session: AsyncSession) -> NewsCandidate:
    candidate = await seed_candidate(session, status="manual_review")
    candidate.error_code = "news_evidence_changed"
    candidate.evidence_hash = "stale"
    await add_evidence(session, candidate)
    await add_article(session, candidate)
    session.add(
        NewsAssessment(
            candidate_id=candidate.id,
            assessment_type="duplicate",
            verdict="pass",
            provider="jev",
            reasons_json=[],
            details_json={},
            evidence_hash="stale",
            prompt_version="news-v1",
        )
    )
    await session.commit()
    return candidate


@pytest.mark.asyncio
async def test_refreshing_changed_evidence_takes_the_current_pages_and_rechecks_the_article(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()

    async def refresh(_session: Any, evidence: list[NewsEvidence], **_kwargs: Any) -> Any:
        for row in evidence:
            if row.url == FIRST_PARTY_URL:
                row.content_hash = "a" * 64
                row.excerpt = "The model shipped today, and the page now says more."
        return [FIRST_PARTY_URL], []

    monkeypatch.setattr(service, "refresh_evidence", refresh)
    async with factory() as session:
        candidate = await held_for_changed_evidence(session)
        detail = await service.refresh_candidate_evidence(session, EDITOR, candidate.id, ACTION)
        stored = await session.get(NewsCandidate, candidate.id)
        carried = list(
            await session.scalars(
                select(NewsAssessment).where(
                    NewsAssessment.candidate_id == candidate.id,
                    NewsAssessment.assessment_type == "duplicate",
                    NewsAssessment.provider == "human",
                )
            )
        )
        audits = list(await session.scalars(select(AdminAuditLog)))
    await engine.dispose()

    assert (detail.status, detail.error_code) == ("discovered", "news_evidence_refreshed")
    assert stored is not None and stored.evidence_hash not in {None, "stale"}
    assert set(stored.draft_bundle_json) == set(LOCALES), "the saved article is re-checked"
    assert [row.evidence_hash for row in carried] == [stored.evidence_hash], (
        "a story already judged distinct stays distinct on the new evidence"
    )
    refreshed = next(row for row in audits if row.action == "news_candidate_evidence_refreshed")
    assert refreshed.metadata_json["changed_urls"] == [FIRST_PARTY_URL]


@pytest.mark.asyncio
async def test_only_a_changed_evidence_hold_is_refreshed_and_an_unreadable_page_changes_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine, factory = await database()
    monkeypatch.setattr(
        service,
        "refresh_evidence",
        AsyncMock(return_value=([], [f"source_refetch_failed:{FIRST_PARTY_URL}:TimeoutError"])),
    )
    async with factory() as session:
        candidate = await held_for_changed_evidence(session)
        other = await seed_candidate(session, status="manual_review")
        other.error_code = "news_jev_final_hold"
        await session.commit()
        candidate_id, other_id = candidate.id, other.id
        with pytest.raises(AppError) as wrong_state:
            await service.refresh_candidate_evidence(session, EDITOR, other_id, ACTION)
        with pytest.raises(AppError) as unreadable:
            await service.refresh_candidate_evidence(session, EDITOR, candidate_id, ACTION)
    async with factory() as session:
        stored = await session.get(NewsCandidate, candidate_id)
    await engine.dispose()

    assert wrong_state.value.code == "news_candidate_not_refreshable"
    assert unreadable.value.code == "news_evidence_refresh_failed"
    assert "TimeoutError" in unreadable.value.detail
    assert stored is not None
    assert (stored.error_code, stored.evidence_hash) == ("news_evidence_changed", "stale")
