"""The review judge (judge.py): which holds it answers, what each answer does to the row,
and that a person, a switch and a refusing check all win over it.

Every case runs the judge through ``judged``, which also asserts what the judge must never
do: write one of the three columns that record a person's decision, or sign an assessment
as ``human``.

The last part is what surrounds it (jobs.py, worker.py): the job that asks the judge, the
candidate job that queues it when a story comes to rest in a hold, and the worker start that
sends a cut-off hold back.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import re
from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import fakeredis
import pytest
from pydantic import BaseModel, ValidationError
from redis.exceptions import ConnectionError as RedisConnectionError
from rq import Queue
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.ai.subscription import QUEUE_SECONDS, run_seconds
from app.config import get_settings
from app.db import Base
from app.guides.models import GuideArticle, GuideArticleLocale
from app.guides.schemas import GuideDocument
from app.models import AdminAuditLog, User
from app.news_automation import ai, jobs, judge, pipeline, service, worker
from app.news_automation.duplicates import DUPLICATE_UNCERTAIN, cleared_by_editor
from app.news_automation.evidence import NewsInputTooLarge
from app.news_automation.models import (
    LOCALES,
    NewsAssessment,
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsPipelineRun,
    NewsSource,
)
from app.news_automation.policy import (
    FINAL_EDIT_HOLD,
    JEV_FINAL_HOLD,
    READY_TO_PUBLISH,
    ZH_DRAFT_READY,
    document_fingerprint,
    for_review,
)
from app.news_automation.schemas import (
    CandidateAction,
    Claim,
    DuplicateJudgement,
    LocaleReviewResult,
    RedraftJudgement,
    ReviewJudgement,
    VerificationResult,
)
from app.problems import AppError
from tests.test_news_pipeline import (
    EVENT_DAY,
    FIRST_PARTY_URL,
    JUDGE_DIRECTIONS,
    JUDGE_REASONS,
    LEAD_URL,
    NEWS_TABLES,
    SEEDED_EVIDENCE_HASH,
    SLUG,
    TODAY,
    FakeSessionFactory,
    every_account_full,
    judge_row,
    news_document,
    reverify,
    seed_candidate,
    seed_judge_approved_draft,
    seed_owner,
    seed_published_news,
    seed_single_source_candidate,
    stage_one_mocks,
    stage_two_mocks,
)
from tests.test_news_review_actions import held_for_changed_evidence

Factory = async_sessionmaker[AsyncSession]
# A person's words already on the row. The judge writes none of its own over them.
OWNER_NOTE = "The owner's note from an earlier retry"
# Not the configured model name: the row records the model that answered.
JUDGE_MODEL = "claude-opus-5-5-20261001"
USAGE = {"input_tokens": 1200, "output_tokens": 80}
COMMON_KEYS = {"today", "hold", "candidate", "evidence", "sources", "allowed_decisions"}
QUESTIONS: dict[str, tuple[str, type[BaseModel]]] = {
    "zh_draft": ("judge_review", ReviewJudgement),
    "final": ("judge_review", ReviewJudgement),
    "duplicate": ("judge_duplicate", DuplicateJudgement),
    "redraft": ("judge_redraft", RedraftJudgement),
}
SWITCHES_OFF = [
    ("enabled", False),
    ("mode", "shadow"),
    ("auto_publish_ai", False),
    ("judge_enabled", False),
]


@pytest.fixture
async def factory(tmp_path: Path) -> AsyncIterator[Factory]:
    """A database file, not memory. In memory every session shares one connection; here a
    second session is a second connection, which is what a person pressing a button while
    the judge is asking amounts to."""

    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'news.db'}")
    tables = cast(list[Table], [model.__table__ for model in NEWS_TABLES])
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


async def judge_on(session: AsyncSession) -> None:
    """All four switches the judge needs; seed_single_source_candidate set ``enabled``."""

    settings = await session.get(NewsAutomationSettings, 1)
    assert settings is not None
    settings.mode, settings.auto_publish_ai, settings.judge_enabled = "automatic", True, True


async def not_first_party(session: AsyncSession) -> None:
    """The story's one page is a newsroom's, not the company's own: with every switch on,
    stage one still cannot send it out by itself, so it reaches the review queue."""

    for row in await session.scalars(select(NewsEvidence).where(NewsEvidence.role == "evidence")):
        row.is_first_party = False


async def seed_hold(
    session: AsyncSession, status: str, hold: str | None, **changes: Any
) -> NewsCandidate:
    """A candidate put straight into a hold, for what depends on the row alone."""

    candidate = await seed_single_source_candidate(session)
    await judge_on(session)
    candidate.status, candidate.error_code = status, hold
    candidate.error_detail = "Why the pipeline stopped here."
    candidate.evidence_hash = SEEDED_EVIDENCE_HASH
    candidate.human_reason = OWNER_NOTE
    for name, value in changes.items():
        setattr(candidate, name, value)
    await session.commit()
    return candidate


async def held_draft(factory: Factory, monkeypatch: pytest.MonkeyPatch) -> UUID:
    """Stage one's outcome: a verified Traditional Chinese draft in the review queue."""

    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        await judge_on(session)
        await not_first_party(session)
        candidate.human_reason = OWNER_NOTE
        await session.commit()
        candidate_id = candidate.id
    stage_one_mocks(monkeypatch)
    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    async with factory() as session:
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "manual_review"
    return candidate_id


async def held_duplicate(factory: Factory, monkeypatch: pytest.MonkeyPatch) -> UUID:
    """A story Jev could not tell from the known ones, stopped before any draft."""

    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        await judge_on(session)
        await not_first_party(session)
        candidate.human_reason = OWNER_NOTE
        await session.commit()
        candidate_id = candidate.id
    stage_one_mocks(monkeypatch)
    monkeypatch.setattr(
        ai,
        "jev_duplicate_check",
        AsyncMock(return_value=("manual", 0.5, ["semantic_duplicate_uncertain"])),
    )
    async with factory() as session:
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "manual_review"
    return candidate_id


async def edit_saved_locale(factory: Factory, locale: str, title: str) -> None:
    """An editor's change to one saved locale, which no review on record describes."""

    async with factory() as session:
        row = await session.scalar(
            select(GuideArticleLocale).where(GuideArticleLocale.locale == locale)
        )
        assert row is not None
        row.draft_json = {**row.draft_json, "title": title}
        await session.commit()


async def rechecked(factory: Factory, candidate_id: UUID, locale: str) -> None:
    """The owner edits one saved locale and presses 重新查核. The fact check and the locale
    reviews pass the edited article; nobody confirmed it, so it waits for the publish button.
    Neither the final editor nor Jev's last call reads it again."""

    await edit_saved_locale(factory, locale, f"Release {locale}, edited by the owner")
    async with factory() as session:
        owner_id = await seed_owner(session)
    await reverify(factory, candidate_id, owner_id)
    async with factory() as session:
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "manual_review"
        stored = await session.get(NewsCandidate, candidate_id)
        assert stored is not None and stored.error_code == READY_TO_PUBLISH


async def held_article(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, hold: str = JEV_FINAL_HOLD
) -> UUID:
    """A saved five-locale article one of the last checks held: Jev's last call on the
    Japanese, the final editor on the Korean, or nothing but the publish button. That last
    one is the Jev-held article after the owner edited its Japanese and had it re-checked."""

    candidate_id, _mocks, _translated = await seed_judge_approved_draft(factory, monkeypatch)

    async def final_edit(*args: Any, **_kwargs: Any) -> tuple[LocaleReviewResult, dict, str]:
        if args[3] == "ko":
            issues = ["The launch date is not in the evidence."]
            return LocaleReviewResult(verdict="manual", issues=issues), {}, "editor"
        return LocaleReviewResult(verdict="pass"), {}, "editor"

    async def last_call(*_args: Any, **kwargs: Any) -> list[ai.JevLocaleDecision]:
        return [
            ai.JevLocaleDecision(locale, "confirm", 0.62, [], {})
            if locale == "ja"
            else ai.JevLocaleDecision(locale, "act", 0.97, [], {})
            for locale in kwargs.get("locales", LOCALES)
        ]

    if hold == FINAL_EDIT_HOLD:
        monkeypatch.setattr(ai, "final_edit", final_edit)
    else:
        monkeypatch.setattr(ai, "jev_assessments", last_call)
    async with factory() as session:
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "manual_review"
        stored = await session.get(NewsCandidate, candidate_id)
        assert stored is not None and stored.guide_article_id is not None
        assert stored.error_code == (FINAL_EDIT_HOLD if hold == FINAL_EDIT_HOLD else JEV_FINAL_HOLD)
        # Every saved article has its five locales on the candidate too. That is not the old
        # flow's stored text, which had no article.
        assert set(stored.draft_bundle_json) >= set(LOCALES) and not judge.legacy_bundle(stored)
        stored.human_reason = OWNER_NOTE
        await session.commit()
    if hold == READY_TO_PUBLISH:
        await rechecked(factory, candidate_id, "ja")
    return candidate_id


async def stopped_draft(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, stop: str = "news_verification_failed"
) -> UUID:
    """A story in the redraft list, stopped by the named check of the pipeline itself."""

    if stop == "news_locale_review_failed":
        # Only stage two translates. The reviewer corrects the first translation once and
        # then refuses its own correction too.
        candidate_id, _mocks, _translated = await seed_judge_approved_draft(factory, monkeypatch)
        corrected = news_document("Corrected zh-CN")
        monkeypatch.setattr(
            ai,
            "review_locale",
            AsyncMock(
                side_effect=[
                    (
                        LocaleReviewResult(
                            verdict="revise",
                            issues=["The second paragraph drops the price."],
                            corrected_document=corrected,
                        ),
                        {},
                        "checker",
                    ),
                    (
                        LocaleReviewResult(
                            verdict="manual", issues=["The correction still drops the price."]
                        ),
                        {},
                        "checker",
                    ),
                ]
            ),
        )
    else:
        async with factory() as session:
            candidate = await seed_single_source_candidate(session)
            await judge_on(session)
            session.add(
                NewsEvidence(
                    candidate_id=candidate.id,
                    role="lead_only",
                    is_first_party=False,
                    url=LEAD_URL,
                    title="A lead",
                    source_date=EVENT_DAY,
                    content_hash="e" * 64,
                    excerpt="An aggregator's summary of the release.",
                )
            )
            await session.commit()
            candidate_id = candidate.id
        mocks = stage_one_mocks(monkeypatch)
        monkeypatch.setattr(
            ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
        )
        draft, usage, model = mocks["draft"].return_value
        if stop == "news_verification_failed":
            monkeypatch.setattr(
                ai,
                "verify_article",
                AsyncMock(
                    side_effect=[
                        (
                            VerificationResult(
                                verdict="revise",
                                issues=["The launch date is not in the evidence."],
                                corrected_document=news_document("模型發布（修正）"),
                            ),
                            {},
                            "checker",
                        ),
                        (
                            VerificationResult(
                                verdict="manual", issues=["The benchmark figure has no source."]
                            ),
                            {},
                            "checker",
                        ),
                    ]
                ),
            )
        elif stop == "news_claim_source_invalid":
            cited = ["https://elsewhere.example/blog", LEAD_URL, FIRST_PARTY_URL]
            claims = [Claim(claim="The model shipped.", source_urls=cited)]
            declined = draft.model_copy(update={"claims": claims})
            mocks["draft"].return_value = (declined, usage, model)
        else:
            assert stop == "news_event_date_invalid"
            dated = {"event_date": TODAY, "slug": f"ai-news-model-release-{TODAY:%Y%m%d}"}
            mocks["draft"].return_value = (draft.model_copy(update=dated), usage, model)
    async with factory() as session:
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "needs_redraft"
        stored = await session.get(NewsCandidate, candidate_id)
        assert stored is not None and stored.error_code == stop
        stored.human_reason = OWNER_NOTE
        await session.commit()
    return candidate_id


SEEDS = {
    "zh_draft": held_draft,
    "duplicate": held_duplicate,
    "final": held_article,
    "redraft": stopped_draft,
}


def reply_of(stage: str, decision: str, reasons: list[str] | None = None) -> tuple[Any, dict, str]:
    """What the judge's call for ``stage`` returns: the reply, its usage and the model."""

    reply = QUESTIONS[stage][1].model_validate(
        {"decision": decision, "reasons": list(JUDGE_REASONS if reasons is None else reasons)}
    )
    return reply, dict(USAGE), JUDGE_MODEL


def judge_answers(
    monkeypatch: pytest.MonkeyPatch, stage: str, decision: str, reasons: list[str] | None = None
) -> AsyncMock:
    """Stand in for the judge's call for ``stage``; its other two questions must not be
    asked."""

    name = QUESTIONS[stage][0]
    for other in {"judge_review", "judge_duplicate", "judge_redraft"} - {name}:
        monkeypatch.setattr(ai, other, AsyncMock(side_effect=AssertionError(f"{other} asked")))
    asked = AsyncMock(return_value=reply_of(stage, decision, reasons))
    monkeypatch.setattr(ai, name, asked)
    return asked


def payload_of(asked: AsyncMock) -> dict[str, Any]:
    asked.assert_awaited_once()
    assert asked.await_args is not None
    return cast(dict[str, Any], asked.await_args.args[2])


@dataclass
class Left:
    """What one run of the judge left behind."""

    outcome: judge.JudgeOutcome
    candidate: NewsCandidate
    verdicts: list[NewsAssessment]
    audits: list[AdminAuditLog]
    runs: list[NewsPipelineRun]


async def human_rows(session: AsyncSession, candidate_id: UUID) -> int:
    return len(
        list(
            await session.scalars(
                select(NewsAssessment.id).where(
                    NewsAssessment.candidate_id == candidate_id,
                    NewsAssessment.assessment_type == "human",
                )
            )
        )
    )


async def judged(
    factory: Factory,
    candidate_id: UUID,
    *,
    person: tuple[str | None, str | None, bool] | None = None,
    signed_by_a_person: int = 0,
) -> Left:
    """Run the judge once and return the rows it added.

    ``person`` and ``signed_by_a_person`` say what a person did while the judge was asking,
    in the tests where one does. In every other case the three human columns must be exactly
    as they were, and no assessment may be signed ``human``.
    """

    async with factory() as session:
        before = await session.get(NewsCandidate, candidate_id)
        assert before is not None
        belongs_to_a_person = person or (
            before.human_decision,
            before.human_reason,
            before.human_major_error,
        )
        signed = await human_rows(session, candidate_id)
        known_verdicts = set(
            await session.scalars(
                select(NewsAssessment.id).where(NewsAssessment.assessment_type == "judge")
            )
        )
        known_audits = set(await session.scalars(select(AdminAuditLog.id)))
    async with factory() as session:
        outcome = await judge.judge_candidate(session, Mock(), get_settings(), candidate_id)
    async with factory() as session:
        after = await session.get(NewsCandidate, candidate_id)
        assert after is not None
        verdicts = [
            row
            for row in await session.scalars(
                select(NewsAssessment)
                .where(
                    NewsAssessment.candidate_id == candidate_id,
                    NewsAssessment.assessment_type == "judge",
                )
                .order_by(NewsAssessment.created_at)
            )
            if row.id not in known_verdicts
        ]
        audits = [
            row
            for row in await session.scalars(
                select(AdminAuditLog).order_by(AdminAuditLog.created_at)
            )
            if row.id not in known_audits
        ]
        runs = list(
            await session.scalars(
                select(NewsPipelineRun)
                .where(
                    NewsPipelineRun.candidate_id == candidate_id,
                    NewsPipelineRun.stage.startswith("judge-"),
                )
                .order_by(NewsPipelineRun.attempt)
            )
        )
        signed_after = await human_rows(session, candidate_id)
    assert (
        after.human_decision,
        after.human_reason,
        after.human_major_error,
    ) == belongs_to_a_person
    assert signed_after == signed + signed_by_a_person
    return Left(outcome, after, verdicts, audits, runs)


async def stored(factory: Factory, candidate_id: UUID) -> NewsCandidate:
    async with factory() as session:
        row = await session.get(NewsCandidate, candidate_id)
        assert row is not None
        return row


async def published_versions(factory: Factory) -> list[int | None]:
    async with factory() as session:
        return [row.published_version for row in await session.scalars(select(GuideArticleLocale))]


def test_the_holds_the_judge_answers_are_the_ones_the_owner_named() -> None:
    assert dict(judge.REVIEW_HOLDS) == {
        "news_zh_draft_ready": "zh_draft",
        "news_duplicate_uncertain": "duplicate",
        "news_jev_final_hold": "final",
        "news_final_edit_hold": "final",
        "news_ready_to_publish": "final",
    }
    assert judge.REDRAFT_HOLDS == {
        "news_verification_failed",
        "news_claim_source_invalid",
        "news_event_date_invalid",
        "news_locale_review_failed",
    }
    assert judge.MAX_JUDGE_REWRITES == 2
    assert dict(judge.RUN_STAGES) == {
        "zh_draft": "judge-zh-draft",
        "duplicate": "judge-duplicate",
        "final": "judge-final",
        "redraft": "judge-redraft",
    }
    # NewsPipelineRun.stage is String(32).
    assert all(len(name) <= 32 for name in judge.RUN_STAGES.values())
    # The writer declined a rewrite the judge ordered: that one is the owner's to settle.
    assert "news_not_eligible" not in judge.REDRAFT_HOLDS
    # The two markers are how the judge sends a story back, never a hold it answers.
    assert not {pipeline.JUDGE_APPROVED_MARKER, pipeline.JUDGE_REDRAFT_MARKER} & (
        set(judge.REVIEW_HOLDS) | judge.REDRAFT_HOLDS
    )
    # The retention job and the judge mean the same excerpt by "expired".
    assert f'"{judge.EXPIRED_EXCERPT}"' in inspect.getsource(jobs.cleanup_retention)


def test_the_reasons_the_code_writes_are_sentences_for_the_owner() -> None:
    written = [
        judge.NO_VERIFIED_DRAFT,
        judge.NO_SAVED_ARTICLE,
        judge.REWRITES_SPENT,
        judge.CALL_UNUSABLE,
        judge.CALL_KEEPS_FAILING,
        judge.PERSON_CONFIRMED,
        judge.FINAL_EDITOR_HELD,
        judge.NO_DIRECTIONS,
        judge.DIRECTIONS_TOO_LONG,
        judge.LEGACY_BUNDLE,
        judge.LEGACY_REWRITE,
        judge.CONFIRMED_DRAFT,
        judge.EVIDENCE_MOVED,
        judge.REFUSED,
    ]
    for sentence in written:
        assert any("一" <= character <= "鿿" for character in sentence), sentence
        assert len(sentence) < judge.MAX_REASON_CHARACTERS


def test_a_judge_job_is_given_longer_than_the_call_it_wraps_can_take() -> None:
    # On a subscription account one question is two rounds at most. The agent client waits
    # for each as long as the run and the queue may take, and a minute more
    # (AiAccountsAgentClient.run_prompt).
    one_round = run_seconds(ai.STAGE_TIMEOUT_SECONDS) + QUEUE_SECONDS + 60
    assert one_round == 480
    assert judge.JOB_TIMEOUT_SECONDS == 1_800
    # What both rounds leave is for the evidence pages a publication fetches again.
    assert judge.JOB_TIMEOUT_SECONDS - 2 * one_round >= 600
    # A run counts as a job still asking for a minute past the limit RQ ends that job at.
    assert judge.LIVE_RUN == timedelta(seconds=judge.JOB_TIMEOUT_SECONDS + 60)


@pytest.mark.parametrize(
    ("stage", "hold", "confirmed", "allowed"),
    [
        ("zh_draft", ZH_DRAFT_READY, False, ["publish", "reject", "manual"]),
        ("zh_draft", ZH_DRAFT_READY, True, ["publish", "manual"]),
        ("final", JEV_FINAL_HOLD, False, ["publish", "reject", "manual"]),
        ("final", READY_TO_PUBLISH, True, ["publish", "manual"]),
        ("final", FINAL_EDIT_HOLD, False, ["reject", "manual"]),
        ("final", FINAL_EDIT_HOLD, True, ["manual"]),
        ("duplicate", DUPLICATE_UNCERTAIN, False, ["distinct", "duplicate", "manual"]),
        ("duplicate", DUPLICATE_UNCERTAIN, True, ["distinct", "manual"]),
        ("redraft", "news_verification_failed", False, ["rewrite", "reject", "manual"]),
    ],
)
def test_what_the_judge_may_choose_from(
    stage: judge.Stage, hold: str, confirmed: bool, allowed: list[str]
) -> None:
    assert judge.allowed_decisions(stage, hold, confirmed=confirmed) == allowed


HELD = [
    ("manual_review", "news_zh_draft_ready", "zh_draft"),
    ("manual_review", "news_duplicate_uncertain", "duplicate"),
    ("manual_review", "news_jev_final_hold", "final"),
    ("manual_review", "news_final_edit_hold", "final"),
    ("manual_review", "news_ready_to_publish", "final"),
    ("needs_redraft", "news_verification_failed", "redraft"),
    ("needs_redraft", "news_claim_source_invalid", "redraft"),
    ("needs_redraft", "news_event_date_invalid", "redraft"),
    ("needs_redraft", "news_locale_review_failed", "redraft"),
    # Holds that need work stay with the owner: an article to fix, pages to re-check.
    ("manual_review", "news_hard_checks_failed", None),
    ("manual_review", "news_evidence_changed", None),
    ("manual_review", "news_locale_review_failed", None),
    ("manual_review", "news_verification_failed", None),
    ("manual_review", None, None),
    ("needs_redraft", "news_not_eligible", None),
    ("needs_redraft", "news_zh_draft_ready", None),
    # The same codes outside the two lists are not holds.
    ("failed", "news_verification_failed", None),
    ("shadow_review", "news_zh_draft_ready", None),
    ("discovered", "news_judge_redraft", None),
    ("rejected", "news_zh_draft_ready", None),
    ("duplicate", "news_duplicate_uncertain", None),
    ("published", "news_jev_final_hold", None),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(("status", "hold", "stage"), HELD)
async def test_the_judge_wants_exactly_the_holds_of_its_two_lists(
    factory: Factory, status: str, hold: str | None, stage: str | None
) -> None:
    async with factory() as session:
        candidate = await seed_hold(session, status, hold)
        assert judge.stage_of(candidate) == stage
        assert await judge.wanted(session, candidate) is (stage is not None)
        assert await judge.exclusion(session, candidate) == (None if stage else "not_held")


@pytest.mark.asyncio
@pytest.mark.parametrize(("switch", "off"), SWITCHES_OFF)
@pytest.mark.parametrize(
    ("status", "hold", "stage"),
    [
        ("manual_review", ZH_DRAFT_READY, "zh_draft"),
        ("needs_redraft", "news_verification_failed", "redraft"),
    ],
)
async def test_the_judge_acts_only_while_all_four_switches_are_on(
    factory: Factory,
    monkeypatch: pytest.MonkeyPatch,
    switch: str,
    off: object,
    status: str,
    hold: str,
    stage: str,
) -> None:
    async with factory() as session:
        candidate = await seed_hold(session, status, hold)
        assert await judge.wanted(session, candidate)
        settings = await session.get(NewsAutomationSettings, 1)
        assert settings is not None
        setattr(settings, switch, off)
        await session.commit()
        assert await judge.exclusion(session, candidate) == "gate_off"
        assert not await judge.wanted(session, candidate)
    asked = judge_answers(monkeypatch, stage, "manual")

    left = await judged(factory, candidate.id)

    assert left.outcome == judge.JudgeOutcome("nothing")
    asked.assert_not_awaited()
    assert (left.verdicts, left.audits, left.runs) == ([], [], [])
    assert (left.candidate.judge_decision, left.candidate.judge_hold) == (None, None)


@pytest.mark.asyncio
async def test_the_switch_that_counts_is_the_candidates_own_vertical(factory: Factory) -> None:
    async with factory() as session:
        candidate = await seed_hold(session, "manual_review", ZH_DRAFT_READY, vertical="tech")
        # Automatic publication is on for AI news only.
        assert await judge.exclusion(session, candidate) == "gate_off"
        settings = await session.get(NewsAutomationSettings, 1)
        assert settings is not None
        settings.auto_publish_tech, settings.auto_publish_ai = True, False
        await session.commit()
        assert await judge.wanted(session, candidate)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("answered", "wanted"),
    [(None, True), (ZH_DRAFT_READY, False), ("news_duplicate_uncertain", True)],
    ids=["never", "this-hold", "an-earlier-hold"],
)
async def test_a_hold_is_judged_once(factory: Factory, answered: str | None, wanted: bool) -> None:
    async with factory() as session:
        candidate = await seed_hold(
            session, "manual_review", ZH_DRAFT_READY, judge_hold=answered, judge_decision="manual"
        )
        assert await judge.wanted(session, candidate) is wanted
        assert await judge.exclusion(session, candidate) == (None if wanted else "answered")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("change", "why"),
    [
        ("nothing", None),
        ("article", "has_article"),
        ("confirmed", "person_decided"),
        ("rejected-by-a-person", "person_decided"),
        ("expired-evidence", "evidence_expired"),
        ("expired-lead", None),
    ],
)
async def test_a_redraft_is_judged_only_for_a_story_that_has_nothing_but_live_evidence(
    factory: Factory, change: str, why: str | None
) -> None:
    async with factory() as session:
        candidate = await seed_hold(session, "needs_redraft", "news_verification_failed")
        if change == "article":
            article = GuideArticle(slug=SLUG, kind="life", news_date=EVENT_DAY)
            session.add(article)
            await session.flush()
            candidate.guide_article_id = article.id
        elif change == "confirmed":
            candidate.human_decision = "publish"
        elif change == "rejected-by-a-person":
            candidate.human_decision = "reject"
        elif change == "expired-evidence":
            for row in await session.scalars(select(NewsEvidence)):
                row.excerpt = judge.EXPIRED_EXCERPT
        elif change == "expired-lead":
            # Nothing is cited from a lead-only page, so its excerpt is not needed.
            session.add(
                NewsEvidence(
                    candidate_id=candidate.id,
                    role="lead_only",
                    url=LEAD_URL,
                    title="A lead",
                    content_hash="e" * 64,
                    excerpt=judge.EXPIRED_EXCERPT,
                )
            )
        await session.commit()
        assert await judge.exclusion(session, candidate) == why
        assert await judge.wanted(session, candidate) is (why is None)


@pytest.mark.asyncio
async def test_a_review_hold_a_person_confirmed_is_still_the_judges_to_read(
    factory: Factory,
) -> None:
    async with factory() as session:
        candidate = await seed_hold(
            session, "manual_review", JEV_FINAL_HOLD, human_decision="publish"
        )
        assert await judge.wanted(session, candidate)


@pytest.mark.asyncio
async def test_a_hold_that_leaves_the_judge_nothing_to_decide_is_not_put_to_it(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The final editor held a locale of a story a person confirmed. The judge may not
    publish the one and may not close the other, so all it could do is hand the story back."""

    candidate_id = await held_article(factory, monkeypatch, FINAL_EDIT_HOLD)
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None and await judge.wanted(session, candidate)
        candidate.human_decision = "publish"
        await session.commit()
        assert judge.allowed_decisions("final", FINAL_EDIT_HOLD, confirmed=True) == ["manual"]
        assert await judge.exclusion(session, candidate) == "person_decided"
        assert not await judge.wanted(session, candidate)
    asked = judge_answers(monkeypatch, "final", "manual")

    left = await judged(factory, candidate_id)

    assert left.outcome == judge.JudgeOutcome("nothing")
    asked.assert_not_awaited()
    # No call, no verdict and no badge: it waits for the owner as it would with AI review off.
    assert (left.verdicts, left.audits, left.runs) == ([], [], [])
    assert (left.candidate.judge_decision, left.candidate.judge_hold) == (None, None)


@pytest.mark.asyncio
@pytest.mark.parametrize("expired", ["evidence", "lead"])
@pytest.mark.parametrize(
    ("status", "hold"), [(status, hold) for status, hold, stage in HELD if stage is not None]
)
async def test_no_hold_is_judged_once_the_retention_cleanup_has_emptied_its_evidence(
    factory: Factory, status: str, hold: str, expired: str
) -> None:
    """A draft or an article is read against the excerpts, and "not a duplicate" sends the
    story on to be drafted or checked from them. A lead-only page is cited by nothing."""

    async with factory() as session:
        candidate = await seed_hold(session, status, hold)
        if expired == "evidence":
            for row in await session.scalars(select(NewsEvidence)):
                row.excerpt = judge.EXPIRED_EXCERPT
        else:
            session.add(
                NewsEvidence(
                    candidate_id=candidate.id,
                    role="lead_only",
                    url=LEAD_URL,
                    title="A lead",
                    content_hash="e" * 64,
                    excerpt=judge.EXPIRED_EXCERPT,
                )
            )
        await session.commit()
        why = "evidence_expired" if expired == "evidence" else None
        assert await judge.exclusion(session, candidate) == why
        assert await judge.wanted(session, candidate) is (why is None)


UNSURE = "news_duplicate_uncertain"
UNVERIFIED = "news_verification_failed"
VERDICTS = [
    # stage, the model's decision, stored verdict, status, error_code, judge_decision, action
    ("zh_draft", "publish", "publish", "discovered", "news_judge_approved", "publish", "requeue"),
    ("zh_draft", "reject", "reject", "rejected", "news_zh_draft_ready", "reject", "nothing"),
    ("zh_draft", "manual", "manual", "manual_review", "news_zh_draft_ready", "manual", "nothing"),
    ("duplicate", "distinct", "pass", "discovered", None, None, "requeue"),
    ("duplicate", "duplicate", "duplicate", "duplicate", UNSURE, "duplicate", "nothing"),
    ("duplicate", "manual", "manual", "manual_review", UNSURE, "manual", "nothing"),
    ("final", "publish", "publish", "published", "news_jev_final_hold", "publish", "nothing"),
    ("final", "reject", "reject", "rejected", "news_jev_final_hold", "reject", "nothing"),
    ("final", "manual", "manual", "manual_review", "news_jev_final_hold", "manual", "nothing"),
    ("redraft", "rewrite", "revise", "discovered", "news_judge_redraft", None, "requeue"),
    ("redraft", "reject", "reject", "rejected", UNVERIFIED, "reject", "nothing"),
    ("redraft", "manual", "manual", "needs_redraft", UNVERIFIED, "manual", "nothing"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("stage", "decision", "verdict", "status", "error_code", "judge_decision", "action"),
    VERDICTS,
    ids=[f"{row[0]}-{row[1]}" for row in VERDICTS],
)
async def test_each_decision_is_recorded_and_applied_in_one_step(
    factory: Factory,
    monkeypatch: pytest.MonkeyPatch,
    stage: str,
    decision: str,
    verdict: str,
    status: str,
    error_code: str | None,
    judge_decision: str | None,
    action: str,
) -> None:
    candidate_id = await SEEDS[stage](factory, monkeypatch)
    before = await stored(factory, candidate_id)
    hold = before.error_code
    assert hold is not None and before.error_detail
    asked = judge_answers(monkeypatch, stage, decision)

    left = await judged(factory, candidate_id)

    requeued = action == "requeue"
    after = left.candidate
    assert left.outcome == judge.JudgeOutcome(
        cast(Any, action),
        hold=hold,
        retry_count=before.retry_count + 1 if requeued else None,
        verdict=verdict,
    )
    assert (after.status, after.error_code) == (status, error_code)
    assert (after.judge_decision, after.judge_hold) == (judge_decision, hold)
    assert after.retry_count == before.retry_count + (1 if requeued else 0)
    # A story the judge closes or hands back keeps the hold's own explanation; one that goes
    # back to the pipeline starts clean.
    assert after.error_detail == (None if requeued else before.error_detail)
    assert after.human_decision is None

    [row] = left.verdicts
    assert (row.assessment_type, row.verdict, row.locale) == ("judge", verdict, None)
    assert (row.provider, row.model) == ("anthropic", JUDGE_MODEL)
    assert row.reasons_json == JUDGE_REASONS
    assert row.details_json == {"stage": stage, "hold": hold}
    assert (row.evidence_hash, row.prompt_version) == (before.evidence_hash, "news-v1")
    assert row.created_by_user_id is None

    [recorded] = [item for item in left.audits if item.action == "news_candidate_judged"]
    assert recorded.actor_user_id is None
    assert recorded.target == f"news-candidate:{candidate_id}"
    assert recorded.metadata_json == {
        "system_actor": True,
        "stage": stage,
        "hold": hold,
        "verdict": verdict,
        "provider": "anthropic",
        "model": JUDGE_MODEL,
    }

    [run] = left.runs
    assert (run.stage, run.status, run.provider, run.model) == (
        judge.RUN_STAGES[cast(judge.Stage, stage)],
        "succeeded",
        "anthropic",
        JUDGE_MODEL,
    )
    assert (run.input_tokens, run.output_tokens) == (1200, 80)
    assert run.metadata_json == {"verdict": verdict}
    assert run.finished_at is not None

    # One verdict per hold: the same job arriving again asks nothing.
    again = await judged(factory, candidate_id)
    assert again.outcome == judge.JudgeOutcome("nothing")
    assert again.verdicts == []
    asked.assert_awaited_once()


@pytest.mark.asyncio
async def test_a_draft_the_judge_approves_is_published_by_the_pipeline(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The row the judge writes is the approval the pipeline looks for."""

    candidate_id = await held_draft(factory, monkeypatch)
    translated = stage_two_mocks(monkeypatch)
    judge_answers(monkeypatch, "zh_draft", "publish")

    left = await judged(factory, candidate_id)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        after = await session.get(NewsCandidate, candidate_id)
        audits = list(await session.scalars(select(AdminAuditLog)))

    assert left.outcome.action == "requeue"
    assert result == "published"
    assert translated == ["zh-CN", "en", "ja", "ko"]
    assert after is not None
    assert (after.status, after.human_decision, after.human_reason) == (
        "published",
        None,
        OWNER_NOTE,
    )
    assert all(version is not None for version in await published_versions(factory))
    publications = [row for row in audits if row.action == "guide_article_published"]
    assert len(publications) == 5
    for row in publications:
        assert row.metadata_json["judge_model"] == JUDGE_MODEL
        assert row.metadata_json["judged_stage"] == "zh_draft"
        assert row.metadata_json["reason"] == " ".join(JUDGE_REASONS)


@pytest.mark.asyncio
async def test_a_rewrite_reaches_the_writer_with_the_directions_as_stored(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch)
    # More and longer than is kept, with blanks: the writer gets what the row holds.
    wordy = ["  ", *[f"第 {number} 項：" + "刪" * 500 for number in range(1, 11)]]
    judge_answers(monkeypatch, "redraft", "rewrite", wordy)

    left = await judged(factory, candidate_id)
    mocks = stage_one_mocks(monkeypatch)
    async with factory() as session:
        await not_first_party(session)
        await session.commit()
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        draft_runs = list(
            await session.scalars(
                select(NewsPipelineRun)
                .where(NewsPipelineRun.stage == "draft")
                .order_by(NewsPipelineRun.attempt)
            )
        )

    [row] = left.verdicts
    assert len(row.reasons_json) == judge.MAX_REASONS == 8
    assert all(len(reason) == judge.MAX_REASON_CHARACTERS == 400 for reason in row.reasons_json)
    assert row.reasons_json[0].startswith("第 1 項：")
    assert mocks["draft"].await_args is not None
    assert mocks["draft"].await_args.kwargs == {"notes": row.reasons_json}
    assert draft_runs[-1].metadata_json == {"slug": SLUG, "judge_notes": str(row.id)}
    # The rewrite met every check again and is a verified draft in the review queue.
    assert result == "manual_review"
    after = await stored(factory, candidate_id)
    assert (after.status, after.error_code) == ("manual_review", ZH_DRAFT_READY)
    # A new hold: the claim cleared the answer to the old one.
    async with factory() as session:
        assert await judge.wanted(session, after)


@pytest.mark.asyncio
async def test_a_story_the_judge_calls_distinct_is_drafted_without_asking_jev_again(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await held_duplicate(factory, monkeypatch)
    judge_answers(monkeypatch, "duplicate", "distinct")

    await judged(factory, candidate_id)
    duplicate_check = AsyncMock(return_value=("manual", 0.5, ["semantic_duplicate_uncertain"]))
    monkeypatch.setattr(ai, "jev_duplicate_check", duplicate_check)
    mocks = stage_one_mocks(monkeypatch)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)

    duplicate_check.assert_not_awaited()
    mocks["draft"].assert_awaited_once()
    # An ordinary draft: only a rewrite carries the judge's notes.
    assert mocks["draft"].await_args is not None and mocks["draft"].await_args.kwargs == {}
    after = await stored(factory, candidate_id)
    assert (result, after.error_code) == ("manual_review", ZH_DRAFT_READY)


UNCERTAIN = ("manual", 0.5, ["semantic_duplicate_uncertain"])


@pytest.mark.asyncio
async def test_a_rewrite_an_uncertain_duplicate_check_stopped_is_still_written_with_its_directions(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch)
    judge_answers(monkeypatch, "redraft", "rewrite")
    [directions] = (await judged(factory, candidate_id)).verdicts

    # The rewrite's own run asks Jev about duplicates first, and this time Jev cannot tell:
    # the story is held before anything is drafted, and the hold replaces the marker.
    mocks = stage_one_mocks(monkeypatch)
    monkeypatch.setattr(ai, "jev_duplicate_check", AsyncMock(return_value=UNCERTAIN))
    async with factory() as session:
        await not_first_party(session)
        await session.commit()
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "manual_review"
    mocks["draft"].assert_not_awaited()
    assert (await stored(factory, candidate_id)).error_code == DUPLICATE_UNCERTAIN

    judge_answers(monkeypatch, "duplicate", "distinct")
    left = await judged(factory, candidate_id)
    assert left.outcome.action == "requeue"
    assert left.candidate.error_code == pipeline.JUDGE_REDRAFT_MARKER
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)

    # The "not a duplicate" is the judge's newest word and does not take the rewrite back.
    assert mocks["draft"].await_args is not None
    assert mocks["draft"].await_args.kwargs == {"notes": directions.reasons_json}
    after = await stored(factory, candidate_id)
    assert (result, after.error_code) == ("manual_review", ZH_DRAFT_READY)


@pytest.mark.asyncio
@pytest.mark.parametrize("paused_at", ["draft", "verification"])
async def test_a_rewrite_that_was_interrupted_before_the_duplicate_hold_still_owes_its_directions(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, paused_at: str
) -> None:
    """The rewrite's first run reached the writer, or got past it, and then had to wait for
    a subscription account. A draft run is on record either way, and no draft was kept."""

    candidate_id = await stopped_draft(factory, monkeypatch)
    judge_answers(monkeypatch, "redraft", "rewrite")
    [directions] = (await judged(factory, candidate_id)).verdicts

    mocks = stage_one_mocks(monkeypatch)
    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    if paused_at == "draft":
        mocks["draft"].side_effect = every_account_full()
    else:
        monkeypatch.setattr(ai, "verify_article", AsyncMock(side_effect=every_account_full()))
    async with factory() as session:
        await not_first_party(session)
        await session.commit()
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "paused"
    waiting = await stored(factory, candidate_id)
    assert (waiting.status, waiting.error_code) == ("discovered", pipeline.JUDGE_REDRAFT_MARKER)

    # The rerun asks Jev about duplicates again, and this time Jev cannot tell.
    mocks = stage_one_mocks(monkeypatch)
    monkeypatch.setattr(ai, "jev_duplicate_check", AsyncMock(return_value=UNCERTAIN))
    async with factory() as session:
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "manual_review"
    mocks["draft"].assert_not_awaited()

    judge_answers(monkeypatch, "duplicate", "distinct")
    left = await judged(factory, candidate_id)
    assert left.outcome.action == "requeue"
    assert left.candidate.error_code == pipeline.JUDGE_REDRAFT_MARKER
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)

    assert mocks["draft"].await_args is not None
    assert mocks["draft"].await_args.kwargs == {"notes": directions.reasons_json}
    after = await stored(factory, candidate_id)
    assert (result, after.error_code) == ("manual_review", ZH_DRAFT_READY)


@pytest.mark.asyncio
async def test_directions_a_draft_already_used_do_not_steer_a_later_one(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch)
    judge_answers(monkeypatch, "redraft", "rewrite")
    await judged(factory, candidate_id)

    # The rewrite is drafted with the directions and the writer declines the story.
    mocks = stage_one_mocks(monkeypatch)
    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    draft, usage, model = mocks["draft"].return_value
    declined = draft.model_copy(update={"eligible": False, "exclusion_reason": "Not news."})
    mocks["draft"].return_value = (declined, usage, model)
    async with factory() as session:
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "needs_redraft"
    # The owner asks for a draft of their own, and that run stops at the duplicate check.
    async with factory() as session:
        row = await session.get(NewsCandidate, candidate_id)
        assert row is not None and row.error_code == "news_not_eligible"
        service._queue_new_draft(row, OWNER_NOTE)
        await session.commit()
    monkeypatch.setattr(ai, "jev_duplicate_check", AsyncMock(return_value=UNCERTAIN))
    async with factory() as session:
        assert await pipeline.process_candidate(
            session, Mock(), get_settings(), candidate_id
        ) == "manual_review"

    judge_answers(monkeypatch, "duplicate", "distinct")
    left = await judged(factory, candidate_id)

    # An ordinary draft follows: the directions were for the one the writer declined.
    assert left.outcome.action == "requeue"
    assert left.candidate.error_code is None


@pytest.mark.asyncio
async def test_a_distinct_story_that_has_its_article_is_checked_again_not_redrafted(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await held_article(factory, monkeypatch)
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None
        candidate.error_code = DUPLICATE_UNCERTAIN
        candidate.draft_bundle_json = {}
        await session.commit()
    judge_answers(monkeypatch, "duplicate", "distinct")

    left = await judged(factory, candidate_id)

    after = left.candidate
    assert left.outcome.action == "requeue"
    assert (after.status, after.error_code) == ("discovered", pipeline.REVERIFY_MARKER)
    # The saved article's five locales are what the pipeline re-checks.
    assert set(after.draft_bundle_json) == set(LOCALES)
    assert [row.verdict for row in left.verdicts] == ["pass"]


@pytest.mark.asyncio
async def test_an_article_the_judge_approves_goes_out_through_the_publish_buttons_checks(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await held_article(factory, monkeypatch)
    publication = AsyncMock(side_effect=service.publication_bundle)
    monkeypatch.setattr(service, "publication_bundle", publication)
    judge_answers(monkeypatch, "final", "publish")

    left = await judged(factory, candidate_id)

    publication.assert_awaited_once()
    assert left.candidate.status == "published"
    assert left.candidate.published_at is not None
    assert all(version is not None for version in await published_versions(factory))
    [verdict] = left.verdicts
    [announced] = [
        row for row in left.audits if row.action == "news_candidate_judge_published"
    ]
    assert announced.actor_user_id is None
    assert announced.metadata_json == {
        "system_actor": True,
        "candidate_id": str(candidate_id),
        "article_id": str(left.candidate.guide_article_id),
        "judged_stage": "final",
        "judge_provider": "anthropic",
        "judge_model": JUDGE_MODEL,
        "assessment_id": str(verdict.id),
        "prompt_version": "news-v1",
        "evidence_sha256": left.candidate.evidence_hash,
    }
    publications = [row for row in left.audits if row.action == "guide_article_published"]
    assert len(publications) == 5
    for row in publications:
        metadata = row.metadata_json
        assert row.actor_user_id is None
        assert "human_override" not in metadata
        assert {
            key: metadata[key] for key in ("judge", "judge_provider", "judge_model", "judged_stage")
        } == {
            "judge": True,
            "judge_provider": "anthropic",
            "judge_model": JUDGE_MODEL,
            "judged_stage": "final",
        }
        assert metadata["reason"] == " ".join(JUDGE_REASONS)
        assert metadata["system_actor"] is True
    assert "news_candidate_auto_published" not in [row.action for row in left.audits]


DOWNGRADES = [
    # seed, changes to the row, the model's decision, what may be chosen, the code's reason
    ("final-edit", {}, "publish", ["reject", "manual"], judge.FINAL_EDITOR_HELD),
    (
        "final",
        {"human_decision": "publish"},
        "reject",
        ["publish", "manual"],
        judge.PERSON_CONFIRMED.format(decision="退件"),
    ),
    (
        "zh_draft",
        {"human_decision": "publish"},
        "reject",
        ["publish", "manual"],
        judge.PERSON_CONFIRMED.format(decision="退件"),
    ),
    (
        "duplicate",
        {"human_decision": "publish"},
        "duplicate",
        ["distinct", "manual"],
        judge.PERSON_CONFIRMED.format(decision="重複新聞"),
    ),
    (
        "duplicate",
        {"draft_bundle_json": "five-locales"},
        "distinct",
        ["distinct", "duplicate", "manual"],
        judge.LEGACY_BUNDLE,
    ),
    # No article yet, so "distinct" would mean a new draft in place of the confirmed one. The
    # same answer from a person clears their confirmation; the judge may not touch it.
    (
        "duplicate",
        {"human_decision": "publish"},
        "distinct",
        ["distinct", "manual"],
        judge.CONFIRMED_DRAFT,
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("seed", "changes", "decision", "allowed", "reason"),
    DOWNGRADES,
    ids=[
        "final-edit-publish",
        "confirmed-article-reject",
        "confirmed-draft-reject",
        "confirmed-duplicate",
        "legacy-bundle-distinct",
        "confirmed-draft-distinct",
    ],
)
async def test_a_decision_a_rule_forbids_becomes_a_hand_back(
    factory: Factory,
    monkeypatch: pytest.MonkeyPatch,
    seed: str,
    changes: dict[str, Any],
    decision: str,
    allowed: list[str],
    reason: str,
) -> None:
    if seed == "final-edit":
        stage = "final"
        candidate_id = await held_article(factory, monkeypatch, FINAL_EDIT_HOLD)
    else:
        stage = seed
        candidate_id = await SEEDS[seed](factory, monkeypatch)
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None
        for name, value in changes.items():
            if value == "five-locales":
                encoded = news_document("A story stored before articles were saved")
                value = {locale: encoded.model_dump(mode="json") for locale in LOCALES}
            setattr(candidate, name, value)
        await session.commit()
    before = await stored(factory, candidate_id)
    asked = judge_answers(monkeypatch, stage, decision)

    left = await judged(factory, candidate_id)

    assert payload_of(asked)["allowed_decisions"] == allowed
    after = left.candidate
    assert left.outcome == judge.JudgeOutcome("nothing", hold=before.error_code, verdict="manual")
    # Nothing is closed, queued or published: the row rests where it was, answered.
    assert (after.status, after.error_code, after.retry_count) == (
        "manual_review",
        before.error_code,
        before.retry_count,
    )
    assert (after.judge_decision, after.judge_hold) == ("manual", before.error_code)
    assert after.draft_bundle_json == before.draft_bundle_json
    [row] = left.verdicts
    assert row.verdict == "manual"
    assert row.details_json == {
        "stage": stage,
        "hold": before.error_code,
        "downgraded_from": decision,
    }
    # The code says why first; what the model wrote follows.
    assert row.reasons_json == [reason, *JUDGE_REASONS]
    assert [item.action for item in left.audits] == ["news_candidate_judged"]
    assert await published_versions(factory) in ([], [None] * 5)
    async with factory() as session:
        assert not await judge.wanted(session, after)


@pytest.mark.asyncio
@pytest.mark.parametrize("reasons", [[], ["   ", ""]], ids=["none", "blank"])
async def test_a_rewrite_without_directions_is_handed_back(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, reasons: list[str]
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch)
    judge_answers(monkeypatch, "redraft", "rewrite", reasons)

    left = await judged(factory, candidate_id)

    [row] = left.verdicts
    assert (row.verdict, row.reasons_json) == ("manual", [judge.NO_DIRECTIONS])
    assert row.details_json["downgraded_from"] == "rewrite"
    assert (left.candidate.status, left.candidate.error_code, left.candidate.retry_count) == (
        "needs_redraft",
        "news_verification_failed",
        0,
    )
    # A hand-back is not a rewrite: nothing was spent from the story's two.
    async with factory() as session:
        assert await judge.rewrites_used(session, left.candidate) == 0


@pytest.mark.asyncio
async def test_a_rewrite_is_not_ordered_over_five_locales_stored_without_an_article(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch)
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None
        encoded = news_document("A story stored before articles were saved")
        candidate.draft_bundle_json = {
            locale: encoded.model_dump(mode="json") for locale in LOCALES
        }
        await session.commit()
        assert judge.legacy_bundle(candidate)
    judge_answers(monkeypatch, "redraft", "rewrite", JUDGE_DIRECTIONS)

    left = await judged(factory, candidate_id)

    [row] = left.verdicts
    assert (row.verdict, row.reasons_json) == (
        "manual",
        [judge.LEGACY_REWRITE, *JUDGE_DIRECTIONS],
    )
    assert row.details_json["downgraded_from"] == "rewrite"
    # A new draft would have replaced the only copy of those five locales.
    assert (left.candidate.status, left.candidate.retry_count) == ("needs_redraft", 0)
    assert set(left.candidate.draft_bundle_json) == set(LOCALES)


@pytest.mark.asyncio
@pytest.mark.parametrize("fits", [False, True])
async def test_directions_that_would_overflow_the_writers_input_are_handed_back(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, fits: bool
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch)
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None
        evidence = list(
            await session.scalars(
                select(NewsEvidence).order_by(
                    NewsEvidence.is_first_party.desc(), NewsEvidence.retrieved_at
                )
            )
        )
        # Both pages, as the writer is given them: the lead-only one counts toward the size.
        assert len(evidence) == 2
        without_notes = ai.draft_input_tokens(candidate, evidence)
        with_notes = ai.draft_input_tokens(candidate, evidence, JUDGE_DIRECTIONS)
    assert with_notes > without_notes
    # One token decides it: the limit is what the writer's whole input comes to, or one less.
    monkeypatch.setattr(ai, "STAGE_MAX_INPUT_TOKENS", with_notes if fits else with_notes - 1)
    judge_answers(monkeypatch, "redraft", "rewrite", JUDGE_DIRECTIONS)

    left = await judged(factory, candidate_id)

    [row] = left.verdicts
    if fits:
        assert (row.verdict, row.reasons_json) == ("revise", JUDGE_DIRECTIONS)
        assert left.candidate.error_code == pipeline.JUDGE_REDRAFT_MARKER
    else:
        assert row.verdict == "manual"
        assert row.reasons_json == [judge.DIRECTIONS_TOO_LONG, *JUDGE_DIRECTIONS]
        assert row.details_json["downgraded_from"] == "rewrite"
        assert (left.candidate.status, left.candidate.retry_count) == ("needs_redraft", 0)


SNAPSHOT: dict[str, dict[str, Any]] = {
    "status": {"status": "failed"},
    # Another hold the judge answers, and an answer to give it: still not this verdict's.
    "error_code": {"error_code": READY_TO_PUBLISH},
    "evidence_hash": {"evidence_hash": "0" * 64},
    # A retry that ran and stopped at the very same hold again, on a new draft.
    "retry_count": {"retry_count": 7},
    "human_decision": {"human_decision": "publish"},
    "judge_hold": {"judge_hold": DUPLICATE_UNCERTAIN},
}


@pytest.mark.asyncio
@pytest.mark.parametrize("decision", ["publish", "reject"])
@pytest.mark.parametrize("touched", list(SNAPSHOT))
async def test_a_row_touched_while_the_judge_was_asking_gets_no_verdict(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, touched: str, decision: str
) -> None:
    """SQLite has no row lock to wait on, so the other session acts inside the model call:
    after the judge read the row, before it locks it. Each case changes one thing only.
    That the judge asks for the lock at all is the next test's.

    Both decisions, because an approval is checked once more against the verified draft
    and a rejection is not: for a rejection this comparison is all there is.
    """

    candidate_id = await held_draft(factory, monkeypatch)
    change = SNAPSHOT[touched]

    async def meanwhile(*_args: Any, **_kwargs: Any) -> tuple[Any, dict, str]:
        async with factory() as other:
            row = await other.get(NewsCandidate, candidate_id)
            assert row is not None
            for name, value in change.items():
                setattr(row, name, value)
            await other.commit()
        return reply_of("zh_draft", decision)

    asked = AsyncMock(side_effect=meanwhile)
    monkeypatch.setattr(ai, "judge_review", asked)
    before = await stored(factory, candidate_id)

    left = await judged(
        factory,
        candidate_id,
        person=("publish", OWNER_NOTE, False) if touched == "human_decision" else None,
    )

    asked.assert_awaited_once()
    assert left.outcome == judge.JudgeOutcome("nothing", hold=ZH_DRAFT_READY)
    assert (left.verdicts, left.audits) == ([], [])
    after = left.candidate
    expected = {
        "status": before.status,
        "error_code": before.error_code,
        "evidence_hash": before.evidence_hash,
        "retry_count": before.retry_count,
        "human_decision": None,
        "judge_hold": None,
        **change,
    }
    assert {name: getattr(after, name) for name in expected} == expected
    assert after.judge_decision is None
    assert after.error_detail == before.error_detail
    # The call ran and was paid for; that much is on record.
    [run] = left.runs
    assert (run.status, run.input_tokens, run.model) == ("succeeded", 1200, JUDGE_MODEL)
    assert run.metadata_json == {"dropped": True}


def session_log(monkeypatch: pytest.MonkeyPatch) -> list[tuple[AsyncSession, str]]:
    """Every re-read of a candidate, every commit and every rollback from here on, in order,
    with the session that made it. A re-read is "locked" when it asked for the row lock."""

    log: list[tuple[AsyncSession, str]] = []
    refresh, commit, rollback = AsyncSession.refresh, AsyncSession.commit, AsyncSession.rollback

    async def refreshed(
        self: AsyncSession,
        instance: object,
        attribute_names: Any = None,
        with_for_update: Any = None,
    ) -> None:
        if isinstance(instance, NewsCandidate):
            log.append((self, "locked re-read" if with_for_update else "re-read"))
        await refresh(self, instance, attribute_names, with_for_update)

    async def committed(self: AsyncSession) -> None:
        await commit(self)
        log.append((self, "commit"))

    async def rolled_back(self: AsyncSession) -> None:
        await rollback(self)
        log.append((self, "rollback"))

    monkeypatch.setattr(AsyncSession, "refresh", refreshed)
    monkeypatch.setattr(AsyncSession, "commit", committed)
    monkeypatch.setattr(AsyncSession, "rollback", rolled_back)
    return log


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path",
    ["verdict", "publication", "nothing-to-read", "unusable-reply", "refused-publication"],
)
async def test_every_verdict_is_committed_under_the_row_lock_its_row_was_checked_under(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, path: str
) -> None:
    """What makes "a person wins" true on PostgreSQL. Every action of the owner takes the
    candidate's row lock, so between the judge's locked re-read and its commit nobody can
    press a button; without the lock the owner's approval could land in that gap and the
    judge's rejection be written over it. SQLite ignores FOR UPDATE, so no other test would
    notice the lock missing, or a commit or rollback that gave it up before the verdict.
    """

    if path == "verdict":
        candidate_id = await held_draft(factory, monkeypatch)
        judge_answers(monkeypatch, "zh_draft", "reject")
    elif path == "nothing-to-read":
        async with factory() as session:
            candidate_id = (await seed_hold(session, "manual_review", JEV_FINAL_HOLD)).id
        judge_answers(monkeypatch, "final", "publish")
    elif path == "unusable-reply":
        candidate_id = await stopped_draft(factory, monkeypatch)
        incomplete = ValueError("The provider returned an incomplete reply.")
        monkeypatch.setattr(ai, "judge_redraft", AsyncMock(side_effect=incomplete))
    else:
        candidate_id = await held_article(factory, monkeypatch)
        if path == "refused-publication":
            # No locale review covers the edited Japanese, so the publication is refused.
            await edit_saved_locale(factory, "ja", "Edited after its review")
        judge_answers(monkeypatch, "final", "publish")
    log = session_log(monkeypatch)

    async with factory() as session:
        outcome = await judge.judge_candidate(session, Mock(), get_settings(), candidate_id)
        mine = [event for owner, event in log if owner is session]

    assert outcome.verdict == {"verdict": "reject", "publication": "publish"}.get(path, "manual")
    rereads = [event for event in mine if event.endswith("re-read")]
    assert rereads and set(rereads) == {"locked re-read"}
    # A refused publication rolls back what the judge had written and takes the lock anew.
    assert len(rereads) == (2 if path == "refused-publication" else 1)
    last = len(mine) - 1 - mine[::-1].index("locked re-read")
    assert mine[last + 1 :] == ["commit"]


@pytest.mark.asyncio
async def test_the_judge_starts_from_the_row_as_it_is_not_as_its_session_last_saw_it(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await held_draft(factory, monkeypatch)
    asked = judge_answers(monkeypatch, "zh_draft", "publish")

    async with factory() as session:
        loaded = await session.get(NewsCandidate, candidate_id)
        assert loaded is not None and await judge.wanted(session, loaded)
        # Another job answers the hold after this session loaded the row.
        async with factory() as other:
            row = await other.get(NewsCandidate, candidate_id)
            assert row is not None
            row.judge_decision, row.judge_hold = "manual", ZH_DRAFT_READY
            await other.commit()
        outcome = await judge.judge_candidate(session, Mock(), get_settings(), candidate_id)

    # Not a call paid for and then dropped: the answered hold is seen before asking.
    assert outcome == judge.JudgeOutcome("nothing")
    asked.assert_not_awaited()
    after = await stored(factory, candidate_id)
    assert (after.status, after.judge_decision, after.human_reason) == (
        "manual_review",
        "manual",
        OWNER_NOTE,
    )


@pytest.mark.asyncio
async def test_the_owners_rejection_during_the_call_stands(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await held_article(factory, monkeypatch)
    async with factory() as session:
        owner_id = await seed_owner(session)

    async def meanwhile(*_args: Any, **_kwargs: Any) -> tuple[Any, dict, str]:
        async with factory() as other:
            owner = await other.get(User, owner_id)
            assert owner is not None
            await service.reject_candidate(
                other, owner, candidate_id, CandidateAction(reason="Not for us")
            )
        return reply_of("final", "publish")

    monkeypatch.setattr(ai, "judge_review", AsyncMock(side_effect=meanwhile))

    left = await judged(
        factory, candidate_id, person=("reject", "Not for us", False), signed_by_a_person=1
    )

    assert left.outcome == judge.JudgeOutcome("nothing", hold=JEV_FINAL_HOLD)
    assert left.verdicts == []
    assert (left.candidate.status, left.candidate.judge_decision) == ("rejected", None)
    assert await published_versions(factory) == [None] * 5
    assert [row.action for row in left.audits] == ["news_candidate_rejected"]


@pytest.mark.asyncio
@pytest.mark.parametrize(("switch", "off"), SWITCHES_OFF)
async def test_a_switch_turned_off_while_the_judge_was_asking_keeps_its_answer_from_applying(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, switch: str, off: object
) -> None:
    candidate_id = await held_article(factory, monkeypatch)

    async def meanwhile(*_args: Any, **_kwargs: Any) -> tuple[Any, dict, str]:
        async with factory() as other:
            row = await other.get(NewsAutomationSettings, 1)
            assert row is not None
            setattr(row, switch, off)
            await other.commit()
        return reply_of("final", "publish")

    asked = AsyncMock(side_effect=meanwhile)
    monkeypatch.setattr(ai, "judge_review", asked)

    left = await judged(factory, candidate_id)

    asked.assert_awaited_once()
    assert left.outcome == judge.JudgeOutcome("nothing", hold=JEV_FINAL_HOLD)
    assert (left.verdicts, left.audits) == ([], [])
    assert (left.candidate.status, left.candidate.error_code) == ("manual_review", JEV_FINAL_HOLD)
    assert (left.candidate.judge_decision, left.candidate.judge_hold) == (None, None)
    assert await published_versions(factory) == [None] * 5
    assert [run.metadata_json for run in left.runs] == [{"dropped": True}]


@pytest.mark.asyncio
@pytest.mark.parametrize(("switch", "off"), SWITCHES_OFF)
async def test_a_switch_turned_off_while_the_evidence_was_fetched_again_stops_the_publication(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, switch: str, off: object
) -> None:
    """After the answer, the publish button's checks fetch every evidence page again, which
    takes seconds to minutes. The switches are read once more when that is done."""

    candidate_id = await held_article(factory, monkeypatch)
    checks = service.publication_bundle

    async def slow_checks(*args: Any, **kwargs: Any) -> Any:
        # Before the checks rather than after: they leave the judge's session holding
        # SQLite's write lock, and the owner's save could not commit.
        async with factory() as other:
            row = await other.get(NewsAutomationSettings, 1)
            assert row is not None
            setattr(row, switch, off)
            await other.commit()
        return await checks(*args, **kwargs)

    monkeypatch.setattr(service, "publication_bundle", slow_checks)
    judge_answers(monkeypatch, "final", "publish")

    left = await judged(factory, candidate_id)

    assert left.outcome == judge.JudgeOutcome("nothing", hold=JEV_FINAL_HOLD)
    assert (left.verdicts, left.audits) == ([], [])
    assert (left.candidate.status, left.candidate.error_code) == ("manual_review", JEV_FINAL_HOLD)
    assert (left.candidate.judge_decision, left.candidate.judge_hold) == (None, None)
    assert await published_versions(factory) == [None] * 5
    assert [run.metadata_json for run in left.runs] == [{"dropped": True}]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "refusal", ["news_locale_review_required", "guide_article_inactive", "news_evidence_changed"]
)
async def test_a_publication_a_check_refuses_is_handed_back_and_not_asked_about_again(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, refusal: str
) -> None:
    candidate_id = await held_article(factory, monkeypatch)
    before = await stored(factory, candidate_id)
    if refusal == "news_locale_review_required":
        # The judge reads the edited Japanese and approves it; no locale review covers it.
        await edit_saved_locale(factory, "ja", "Edited after its review")
    elif refusal == "guide_article_inactive":
        # Refused inside publish_bundle, after the candidate was already marked published
        # in the session and without publish_bundle rolling anything back.
        async with factory() as session:
            article = await session.get(GuideArticle, before.guide_article_id)
            assert article is not None
            article.is_active = False
            await session.commit()
    else:
        monkeypatch.setattr(
            service,
            "revalidate_evidence",
            AsyncMock(return_value=(False, [f"source_content_changed:{FIRST_PARTY_URL}"])),
        )
    asked = judge_answers(monkeypatch, "final", "publish")

    left = await judged(factory, candidate_id)

    after = left.candidate
    assert left.outcome == judge.JudgeOutcome("nothing", hold=JEV_FINAL_HOLD, verdict="manual")
    assert await published_versions(factory) == [None] * 5
    assert after.published_at is None
    # Exactly one verdict, and it is the hand-back: the approval was never stored.
    [row] = left.verdicts
    assert row.verdict == "manual"
    assert row.details_json == {
        "stage": "final",
        "hold": JEV_FINAL_HOLD,
        "downgraded_from": "publish",
        "failure": refusal,
    }
    assert (row.model, row.reasons_json[1:]) == (JUDGE_MODEL, JUDGE_REASONS)
    assert (after.judge_decision, after.judge_hold) == ("manual", JEV_FINAL_HOLD)
    if refusal == "news_evidence_changed":
        # Held for changed evidence, as the publish button holds it, so the re-check is offered.
        assert (after.status, after.error_code) == ("manual_review", "news_evidence_changed")
        assert FIRST_PARTY_URL in (after.error_detail or "")
        assert row.reasons_json[0] == judge.EVIDENCE_MOVED
    else:
        assert (after.status, after.error_code, after.error_detail) == (
            "manual_review",
            JEV_FINAL_HOLD,
            before.error_detail,
        )
        assert refusal in row.reasons_json[0]
    assert [item.action for item in left.audits] == ["news_candidate_judged"]
    [run] = left.runs
    assert (run.status, run.input_tokens) == ("succeeded", 1200)
    assert run.metadata_json["failure"] == refusal

    async with factory() as session:
        assert not await judge.wanted(session, after)
    again = await judged(factory, candidate_id)
    assert again.outcome == judge.JudgeOutcome("nothing")
    assert again.verdicts == []
    asked.assert_awaited_once()


@pytest.mark.asyncio
async def test_an_article_that_is_not_the_one_the_judge_read_is_not_published(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The publication checks can pass on text the judge never saw: an edit made and
    reviewed again while the judge was asking. Its approval is of the earlier text."""

    candidate_id = await held_article(factory, monkeypatch)

    async def meanwhile(*_args: Any, **_kwargs: Any) -> tuple[Any, dict, str]:
        await edit_saved_locale(factory, "ja", "Edited and reviewed during the call")
        async with factory() as other:
            edited = await other.scalar(
                select(GuideArticleLocale).where(GuideArticleLocale.locale == "ja")
            )
            assert edited is not None
            for review in await other.scalars(
                select(NewsAssessment).where(
                    NewsAssessment.assessment_type == "locale_review",
                    NewsAssessment.locale == "ja",
                    NewsAssessment.verdict == "pass",
                )
            ):
                review.details_json = {
                    **review.details_json,
                    "document_sha256": document_fingerprint(
                        GuideDocument.model_validate(edited.draft_json)
                    ),
                }
            await other.commit()
        return reply_of("final", "publish")

    monkeypatch.setattr(ai, "judge_review", AsyncMock(side_effect=meanwhile))

    left = await judged(factory, candidate_id)

    assert left.outcome == judge.JudgeOutcome("nothing", hold=JEV_FINAL_HOLD)
    assert (left.verdicts, left.audits) == ([], [])
    assert (left.candidate.status, left.candidate.judge_hold) == ("manual_review", None)
    assert await published_versions(factory) == [None] * 5
    assert [run.metadata_json for run in left.runs] == [{"dropped": True}]
    # Unanswered, so the next job reads the article as it is now.
    async with factory() as session:
        assert await judge.wanted(session, left.candidate)


@pytest.mark.asyncio
async def test_a_draft_that_is_not_the_one_the_judge_read_is_not_approved(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await held_draft(factory, monkeypatch)

    async def meanwhile(*_args: Any, **_kwargs: Any) -> tuple[Any, dict, str]:
        # Another verified draft takes the place of the one in the payload, and nothing else
        # on the row moves.
        async with factory() as other:
            row = await other.get(NewsCandidate, candidate_id)
            assert row is not None
            replaced = news_document("Not the draft that was judged")
            row.draft_bundle_json = {"zh-TW": replaced.model_dump(mode="json")}
            other.add(
                NewsAssessment(
                    candidate_id=candidate_id,
                    assessment_type="verification",
                    verdict="pass",
                    details_json={"document_sha256": document_fingerprint(replaced)},
                    evidence_hash=row.evidence_hash,
                    prompt_version="news-v1",
                    created_at=datetime.now(UTC) + timedelta(seconds=5),
                )
            )
            await other.commit()
            assert await service.verified_zh_draft(other, row) is not None
        return reply_of("zh_draft", "publish")

    monkeypatch.setattr(ai, "judge_review", AsyncMock(side_effect=meanwhile))

    left = await judged(factory, candidate_id)

    assert left.outcome == judge.JudgeOutcome("nothing", hold=ZH_DRAFT_READY)
    assert (left.verdicts, left.audits) == ([], [])
    assert (left.candidate.status, left.candidate.error_code, left.candidate.judge_hold) == (
        "manual_review",
        ZH_DRAFT_READY,
        None,
    )
    assert [run.metadata_json for run in left.runs] == [{"dropped": True}]


def a_reply_that_fails_validation() -> ValidationError:
    try:
        RedraftJudgement.model_validate({"decision": "approve"})
    except ValidationError as error:
        return error
    raise AssertionError("the reply should not have validated")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "error",
    [
        a_reply_that_fails_validation(),
        NewsInputTooLarge("news_judge_redraft input is about 70000 tokens; the limit is 64000."),
        ValueError("The provider returned an incomplete reply."),
    ],
    ids=["ValidationError", "NewsInputTooLarge", "ValueError"],
)
async def test_a_call_that_would_fail_the_same_way_again_is_handed_back_at_once(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, error: Exception
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch)
    asked = AsyncMock(side_effect=error)
    monkeypatch.setattr(ai, "judge_redraft", asked)
    code = type(error).__name__

    left = await judged(factory, candidate_id)

    assert left.outcome == judge.JudgeOutcome(
        "nothing", hold="news_verification_failed", verdict="manual"
    )
    [row] = left.verdicts
    assert (row.verdict, row.model) == ("manual", None)
    assert row.details_json == {
        "stage": "redraft",
        "hold": "news_verification_failed",
        "failure": code,
    }
    assert row.reasons_json == [judge.CALL_UNUSABLE.format(code=code)]
    assert (left.candidate.status, left.candidate.judge_decision) == ("needs_redraft", "manual")
    [run] = left.runs
    assert (run.status, run.error_code) == ("failed", code)
    again = await judged(factory, candidate_id)
    assert again.outcome == judge.JudgeOutcome("nothing")
    asked.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("moved", ["the-owner-retried", "the-judge-was-switched-off"])
async def test_a_failure_is_not_handed_back_on_a_row_that_moved_meanwhile(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, moved: str
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch)
    async with factory() as session:
        owner_id = await seed_owner(session)

    async def meanwhile(*_args: Any, **_kwargs: Any) -> tuple[Any, dict, str]:
        async with factory() as other:
            if moved == "the-owner-retried":
                owner = await other.get(User, owner_id)
                assert owner is not None
                await service.retry_candidate(
                    other, owner, candidate_id, CandidateAction(reason="Try it again")
                )
            else:
                settings = await other.get(NewsAutomationSettings, 1)
                assert settings is not None
                settings.judge_enabled = False
                await other.commit()
        raise ValueError("The provider returned an incomplete reply.")

    monkeypatch.setattr(ai, "judge_redraft", AsyncMock(side_effect=meanwhile))

    retried = moved == "the-owner-retried"
    left = await judged(
        factory, candidate_id, person=(None, "Try it again", False) if retried else None
    )

    # A hand-back is a verdict like any other: it answers the hold the judge read, and that
    # hold is gone or no longer the judge's.
    assert left.outcome == judge.JudgeOutcome("nothing", hold="news_verification_failed")
    assert left.verdicts == []
    assert (left.candidate.judge_decision, left.candidate.judge_hold) == (None, None)
    assert left.candidate.status == ("discovered" if retried else "needs_redraft")
    assert [(run.status, run.error_code) for run in left.runs] == [("failed", "ValueError")]


@pytest.mark.asyncio
async def test_a_second_job_for_a_hold_that_is_being_judged_steps_aside_without_a_call(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await held_draft(factory, monkeypatch)
    calls = 0
    second: list[judge.JudgeOutcome] = []

    async def asked(*_args: Any, **_kwargs: Any) -> tuple[Any, dict, str]:
        nonlocal calls
        calls += 1
        if calls > 1:
            return reply_of("zh_draft", "manual")
        # A second job for the same hold (a backfill batch, say) starts while the first is
        # still asking, and finds the first one's run.
        async with factory() as other:
            second.append(
                await judge.judge_candidate(other, Mock(), get_settings(), candidate_id)
            )
        return reply_of("zh_draft", "publish")

    monkeypatch.setattr(ai, "judge_review", asked)

    left = await judged(factory, candidate_id)

    assert calls == 1
    assert second == [judge.JudgeOutcome("nothing", hold=ZH_DRAFT_READY)]
    # The first job's answer is the one applied, and its run was left alone.
    assert left.outcome.verdict == "publish"
    assert [row.verdict for row in left.verdicts] == ["publish"]
    assert (left.candidate.status, left.candidate.error_code) == (
        "discovered",
        pipeline.JUDGE_APPROVED_MARKER,
    )
    assert [(run.attempt, run.status, run.error_code, run.metadata_json) for run in left.runs] == [
        (1, "succeeded", None, {"verdict": "publish"}),
    ]
    assert [run.input_tokens for run in left.runs] == [1200]


@pytest.mark.asyncio
async def test_a_run_from_before_the_story_ran_again_does_not_keep_its_new_hold_from_the_judge(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The owner retries during the call and the story comes to rest in a hold again. The
    first job's run is minutes old, but what it read is gone and its answer will be dropped:
    stepping aside for it would leave the new hold with no judge at all."""

    candidate_id = await held_draft(factory, monkeypatch)
    async with factory() as session:
        owner_id = await seed_owner(session)
    calls = 0
    second: list[judge.JudgeOutcome] = []

    async def asked(*_args: Any, **_kwargs: Any) -> tuple[Any, dict, str]:
        nonlocal calls
        calls += 1
        if calls > 1:
            return reply_of("zh_draft", "manual")
        async with factory() as other:
            owner = await other.get(User, owner_id)
            assert owner is not None
            await service.retry_candidate(
                other, owner, candidate_id, CandidateAction(reason="Try it again")
            )
        async with factory() as other:
            assert await pipeline.process_candidate(
                other, Mock(), get_settings(), candidate_id
            ) == "manual_review"
        async with factory() as other:
            second.append(
                await judge.judge_candidate(other, Mock(), get_settings(), candidate_id)
            )
        return reply_of("zh_draft", "publish")

    monkeypatch.setattr(ai, "judge_review", asked)

    left = await judged(factory, candidate_id, person=(None, "Try it again", False))

    assert calls == 2
    assert second == [judge.JudgeOutcome("nothing", hold=ZH_DRAFT_READY, verdict="manual")]
    # The first job's approval was of the draft the retry replaced.
    assert left.outcome == judge.JudgeOutcome("nothing", hold=ZH_DRAFT_READY)
    assert [row.verdict for row in left.verdicts] == ["manual"]
    assert (left.candidate.status, left.candidate.judge_decision, left.candidate.retry_count) == (
        "manual_review",
        "manual",
        1,
    )
    # The new job took the first one's run for a stopped worker's; the first finished it.
    assert [(run.attempt, run.status, run.error_code, run.metadata_json) for run in left.runs] == [
        (1, "succeeded", None, {"dropped": True}),
        (2, "succeeded", None, {"verdict": "manual"}),
    ]
    assert [run.input_tokens for run in left.runs] == [1200, 1200]


@pytest.mark.asyncio
async def test_a_call_that_keeps_failing_is_tried_three_times_and_waiting_does_not_count(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch)
    hold = "news_verification_failed"
    later = judge.JudgeOutcome("retry_later", hold=hold, retry_count=0)
    outage = AppError(502, "ai_provider_unavailable", "The provider did not answer.")
    asked = AsyncMock(side_effect=outage)
    monkeypatch.setattr(ai, "judge_redraft", asked)

    first = await judged(factory, candidate_id)
    # Every subscription account is full, four times over: nothing ran, so nothing counts.
    asked.side_effect = every_account_full()
    waits = [await judged(factory, candidate_id) for _ in range(4)]
    # A job cut off long ago left its run marked running: that says nothing about the call
    # either.
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None
        cut_off = await pipeline._start_run(
            session, candidate, "judge-redraft", provider="anthropic"
        )
        cut_off.started_at = datetime.now(UTC) - judge.LIVE_RUN - timedelta(minutes=1)
        await session.commit()
    asked.side_effect = TimeoutError("read timed out")
    second = await judged(factory, candidate_id)
    still_wanted = await stored(factory, candidate_id)
    async with factory() as session:
        assert await judge.wanted(session, still_wanted)
    third = await judged(factory, candidate_id)

    assert [item.outcome for item in (first, *waits, second)] == [later] * 6
    assert [item.verdicts for item in (first, *waits, second)] == [[]] * 6
    assert second.candidate.judge_hold is None
    assert third.outcome == judge.JudgeOutcome("nothing", hold=hold, verdict="manual")
    [row] = third.verdicts
    assert row.details_json == {"stage": "redraft", "hold": hold, "failure": "TimeoutError"}
    assert row.reasons_json == [judge.CALL_KEEPS_FAILING.format(count=3, code="TimeoutError")]
    assert (third.candidate.status, third.candidate.judge_decision, third.candidate.judge_hold) == (
        "needs_redraft",
        "manual",
        hold,
    )
    assert [(run.status, run.error_code) for run in third.runs] == [
        ("failed", "ai_provider_unavailable"),
        *[("failed", "subscription_quota_paused")] * 4,
        ("failed", "news_processing_stale"),
        ("failed", "TimeoutError"),
        ("failed", "TimeoutError"),
    ]
    assert third.runs[0].error_detail == "The provider did not answer."
    assert asked.await_count == 7


@pytest.mark.asyncio
@pytest.mark.parametrize("since_known", [True, False])
async def test_only_the_failures_of_this_hold_count_toward_the_three(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, since_known: bool
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch)
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None and candidate.processing_started_at is not None
        # Two failures from before the run that produced this hold.
        for attempt in (1, 2):
            session.add(
                NewsPipelineRun(
                    candidate_id=candidate_id,
                    stage="judge-redraft",
                    status="failed",
                    attempt=attempt,
                    idempotency_key=f"{candidate_id}:judge-redraft:{attempt}",
                    error_code="TimeoutError",
                    started_at=candidate.processing_started_at - timedelta(hours=1),
                )
            )
        if not since_known:
            # A row that never recorded when it last ran: every failure is this hold's.
            candidate.processing_started_at = None
        await session.commit()
    monkeypatch.setattr(ai, "judge_redraft", AsyncMock(side_effect=TimeoutError("timed out")))

    left = await judged(factory, candidate_id)

    if since_known:
        assert left.outcome.action == "retry_later"
        assert left.verdicts == []
    else:
        assert left.outcome.verdict == "manual"
        assert [row.details_json["failure"] for row in left.verdicts] == ["TimeoutError"]


@pytest.mark.asyncio
@pytest.mark.parametrize("ordered", [1, 2, 3])
async def test_the_third_rewrite_is_refused_without_asking_the_model(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, ordered: int
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch)
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None
        for number in range(ordered):
            # On any evidence, at any time: the limit is for the story's whole life.
            session.add(
                judge_row(
                    candidate,
                    "revise",
                    "redraft",
                    "news_verification_failed",
                    reasons_json=[f"Direction {number + 1}"],
                    evidence_hash=f"{number}" * 64,
                    created_at=datetime.now(UTC) - timedelta(days=3 - number),
                )
            )
        await session.commit()
    asked = judge_answers(monkeypatch, "redraft", "manual")

    left = await judged(factory, candidate_id)

    [row] = left.verdicts
    if ordered < judge.MAX_JUDGE_REWRITES:
        payload = payload_of(asked)
        assert (payload["rewrites_used"], payload["rewrites_limit"]) == (1, 2)
        assert payload["earlier_directions"] == ["Direction 1"]
        assert "capped" not in row.details_json
        return
    asked.assert_not_awaited()
    assert left.outcome == judge.JudgeOutcome(
        "nothing", hold="news_verification_failed", verdict="manual"
    )
    assert (row.verdict, row.model, row.provider) == ("manual", None, "anthropic")
    assert row.details_json == {
        "stage": "redraft",
        "hold": "news_verification_failed",
        "capped": True,
    }
    assert row.reasons_json == [judge.REWRITES_SPENT.format(used=ordered, limit=2)]
    assert left.runs == []
    assert (left.candidate.status, left.candidate.judge_decision) == ("needs_redraft", "manual")
    assert [item.action for item in left.audits] == ["news_candidate_judged"]


@pytest.mark.asyncio
@pytest.mark.parametrize("missing", ["verified-draft", "article"])
async def test_a_hold_with_nothing_to_read_is_handed_back_without_a_call(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, missing: str
) -> None:
    if missing == "verified-draft":
        candidate_id = await held_draft(factory, monkeypatch)
        async with factory() as session:
            candidate = await session.get(NewsCandidate, candidate_id)
            assert candidate is not None
            # Not the text the passing verification describes any more.
            edited = news_document("Edited since it was verified")
            candidate.draft_bundle_json = {"zh-TW": edited.model_dump(mode="json")}
            await session.commit()
        stage, hold, reason = "zh_draft", ZH_DRAFT_READY, judge.NO_VERIFIED_DRAFT
    else:
        async with factory() as session:
            candidate_id = (await seed_hold(session, "manual_review", JEV_FINAL_HOLD)).id
        stage, hold, reason = "final", JEV_FINAL_HOLD, judge.NO_SAVED_ARTICLE
    asked = judge_answers(monkeypatch, stage, "publish")

    left = await judged(factory, candidate_id)

    asked.assert_not_awaited()
    [row] = left.verdicts
    assert (row.verdict, row.model, row.reasons_json) == ("manual", None, [reason])
    assert row.details_json == {"stage": stage, "hold": hold}
    assert (left.candidate.status, left.candidate.judge_decision, left.candidate.judge_hold) == (
        "manual_review",
        "manual",
        hold,
    )
    assert left.runs == []


@pytest.mark.asyncio
@pytest.mark.parametrize("cut_off", [True, False], ids=["past-the-job-limit", "within-it"])
async def test_a_run_left_running_is_failed_only_once_its_job_cannot_still_be_asking(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, cut_off: bool
) -> None:
    candidate_id = await held_draft(factory, monkeypatch)
    minute = timedelta(minutes=1)
    age = judge.LIVE_RUN + minute if cut_off else judge.LIVE_RUN - minute
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None
        # The story has rested in this hold since before that run began.
        candidate.processing_started_at = datetime.now(UTC) - age - minute
        earlier = await pipeline._start_run(
            session, candidate, "judge-zh-draft", provider="anthropic"
        )
        earlier.started_at = datetime.now(UTC) - age
        await session.commit()
    asked = judge_answers(monkeypatch, "zh_draft", "manual")

    left = await judged(factory, candidate_id)

    if not cut_off:
        # RQ may not have ended that job yet, and the hold is its to answer.
        assert left.outcome == judge.JudgeOutcome("nothing", hold=ZH_DRAFT_READY)
        asked.assert_not_awaited()
        assert [(run.attempt, run.status) for run in left.runs] == [(1, "running")]
        assert left.candidate.judge_hold is None
        return
    assert [(run.attempt, run.status, run.error_code) for run in left.runs] == [
        (1, "failed", "news_processing_stale"),
        (2, "succeeded", None),
    ]
    assert left.runs[0].finished_at is not None


@pytest.mark.asyncio
async def test_interrupted_judge_runs_are_found_for_every_candidate_and_no_other_run_is_touched(
    factory: Factory,
) -> None:
    async with factory() as session:
        first = await seed_hold(session, "manual_review", ZH_DRAFT_READY)
        second = await seed_candidate(session, status="needs_redraft")
        await pipeline._start_run(session, first, "judge-zh-draft")
        await pipeline._start_run(session, second, "judge-redraft")
        drafting = await pipeline._start_run(session, second, "draft")
        finished = await pipeline._start_run(session, first, "judge-final")
        await pipeline._finish_run(session, finished)

        interrupted = await judge.fail_interrupted_runs(session)
        await session.commit()
        runs = {
            run.stage: (run.status, run.error_code)
            for run in await session.scalars(select(NewsPipelineRun))
        }

    assert sorted(interrupted, key=str) == sorted([first.id, second.id], key=str)
    assert runs == {
        "judge-zh-draft": ("failed", "news_processing_stale"),
        "judge-redraft": ("failed", "news_processing_stale"),
        "judge-final": ("succeeded", None),
        "draft": ("running", None),
    }
    assert drafting.status == "running"


@pytest.mark.asyncio
async def test_a_second_job_that_starts_the_same_attempt_steps_aside(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await held_draft(factory, monkeypatch)
    async with factory() as session:
        # The key the judge's first attempt takes, already taken: what the unique constraint
        # answers to the second of two jobs that started in the same instant.
        session.add(
            NewsPipelineRun(
                candidate_id=candidate_id,
                stage="another-stage",
                status="succeeded",
                idempotency_key=f"{candidate_id}:judge-zh-draft:1",
            )
        )
        await session.commit()
    asked = judge_answers(monkeypatch, "zh_draft", "publish")

    left = await judged(factory, candidate_id)

    assert left.outcome == judge.JudgeOutcome("nothing", hold=ZH_DRAFT_READY)
    asked.assert_not_awaited()
    assert (left.verdicts, left.audits, left.runs) == ([], [], [])
    assert (left.candidate.status, left.candidate.judge_hold) == ("manual_review", None)


# Of the keys every payload has, the ones the review instructions explain. Those of the
# other two questions explain allowed_decisions alone; none says what today or candidate is.
REVIEW_EXPLAINS = {"hold", "sources", "allowed_decisions"}


def named(instructions: str, keys: set[str]) -> None:
    """Each of these payload keys is a word of the instructions that are sent with it, and
    not a part of another word: "stop" is not "stopped" and "hold" is not "holds"."""

    for key in sorted(keys):
        assert re.search(rf"(?<![\w.]){re.escape(key)}(?!\w)", instructions), key


@pytest.mark.asyncio
@pytest.mark.parametrize("sources", ["one-site", "first-party", "trusted", "two-sites"])
async def test_the_judge_is_shown_a_draft_as_the_owner_sees_it(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, sources: str
) -> None:
    candidate_id = await held_draft(factory, monkeypatch)
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None
        draft = GuideDocument.model_validate(candidate.draft_bundle_json["zh-TW"])
        # A lead-only page is shown as what it is and never counts as a website.
        session.add(
            NewsEvidence(
                candidate_id=candidate_id,
                role="lead_only",
                url=LEAD_URL,
                title="A lead",
                content_hash="e" * 64,
                excerpt="An aggregator's summary.",
            )
        )
        trusting = {"auto_publish_alone": True}
        session.add(
            NewsSource(
                name="The site of the evidence page: trusted alone only while it is enabled",
                url="https://official.example/feed",
                format="rss",
                role="evidence",
                vertical="ai",
                enabled=sources == "trusted",
                config_json=trusting,
            )
        )
        # Trusting the site of a lead-only page says nothing about the evidence.
        session.add(
            NewsSource(
                name="The site of the lead-only page",
                url="https://lead.example/feed",
                format="rss",
                role="lead_only",
                vertical="ai",
                enabled=True,
                config_json=trusting,
            )
        )
        if sources == "first-party":
            for row in await session.scalars(
                select(NewsEvidence).where(NewsEvidence.role == "evidence")
            ):
                row.is_first_party = True
        elif sources == "two-sites":
            session.add(
                NewsEvidence(
                    candidate_id=candidate_id,
                    role="evidence",
                    url="https://newsroom.example/report",
                    title="A report",
                    content_hash="d" * 64,
                    excerpt="A newsroom's report of the release.",
                )
            )
        await session.commit()
    asked = judge_answers(monkeypatch, "zh_draft", "manual")

    await judged(factory, candidate_id)

    payload = payload_of(asked)
    assert set(payload) == COMMON_KEYS | {"claims", "article", "checks"}
    named(ai.JUDGE_REVIEW_INSTRUCTIONS, set(payload) - COMMON_KEYS | REVIEW_EXPLAINS)
    assert payload["today"] == datetime.now(UTC).date().isoformat()
    assert payload["hold"] == {
        "code": ZH_DRAFT_READY,
        "detail": "A verified Traditional Chinese draft is waiting for the owner's decision.",
    }
    assert payload["candidate"] == {
        "title": "Model release",
        "url": candidate.canonical_url,
        "vertical": "ai",
        "event_date": EVENT_DAY.isoformat(),
        "published_at": None,
    }
    assert payload["allowed_decisions"] == ["publish", "reject", "manual"]
    assert payload["sources"] == {
        "websites": 2 if sources == "two-sites" else 1,
        "first_party": sources == "first-party",
        "trusted_alone": sources == "trusted",
    }
    roles = {item["url"]: item["role"] for item in payload["evidence"]}
    assert roles[FIRST_PARTY_URL] == "evidence" and roles[LEAD_URL] == "lead_only"
    assert payload["evidence"][0].keys() >= {"excerpt", "first_party", "source_date", "title"}
    assert payload["claims"] == [{"claim": "The model shipped.", "source_urls": [FIRST_PARTY_URL]}]
    assert payload["article"] == for_review(draft)
    assert payload["article"]["title"] == "模型發布"
    assert payload["checks"] == {
        "verification": {"verdict": "pass", "issues": []},
        "jev": {"tier": "act", "confidence": 0.97, "reasons": []},
    }
    # Sent as it is: the size check counts every evidence page, uncut.
    json.dumps(payload, ensure_ascii=False)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("hold", "held", "allowed"),
    [
        (JEV_FINAL_HOLD, ["ja"], ["publish", "reject", "manual"]),
        (FINAL_EDIT_HOLD, ["ko"], ["reject", "manual"]),
        (READY_TO_PUBLISH, [], ["publish", "reject", "manual"]),
    ],
)
async def test_the_judge_is_shown_a_finished_article_and_only_the_locales_a_check_held(
    factory: Factory,
    monkeypatch: pytest.MonkeyPatch,
    hold: str,
    held: list[str],
    allowed: list[str],
) -> None:
    candidate_id = await held_article(factory, monkeypatch, hold)
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None
        # What would be published is the saved article, not the copy on the candidate.
        candidate.draft_bundle_json = {
            locale: news_document("A stale copy on the candidate").model_dump(mode="json")
            for locale in LOCALES
        }
        candidate.lint_json = {"en": ["news_faq: an FAQ block is required"]}
        saved = {
            row.locale: GuideDocument.model_validate(row.draft_json)
            for row in await session.scalars(select(GuideArticleLocale))
        }
        await session.commit()
    asked = judge_answers(monkeypatch, "final", "manual")

    await judged(factory, candidate_id)

    payload = payload_of(asked)
    assert set(payload) == COMMON_KEYS | {"verified_zh_tw", "held", "checks"}
    named(ai.JUDGE_REVIEW_INSTRUCTIONS, set(payload) - COMMON_KEYS | REVIEW_EXPLAINS)
    assert payload["hold"]["code"] == hold
    assert payload["allowed_decisions"] == allowed
    assert payload["verified_zh_tw"] == for_review(saved["zh-TW"])
    assert payload["held"] == {locale: for_review(saved[locale]) for locale in held}
    assert "A stale copy on the candidate" not in json.dumps(payload)
    checks = payload["checks"]
    assert list(checks) == list(LOCALES)
    assert all(set(record) == {"jev", "final_edit", "lint"} for record in checks.values())
    assert checks["en"]["lint"] == ["news_faq: an FAQ block is required"]
    assert checks["ja"]["lint"] == []
    passed = {"verdict": "pass", "issues": []}
    if hold == FINAL_EDIT_HOLD:
        # Jev is not asked about an article the final editor held.
        assert checks["ko"] == {
            "jev": None,
            "final_edit": {
                "verdict": "manual",
                "issues": ["The launch date is not in the evidence."],
            },
            "lint": [],
        }
        assert checks["en"]["final_edit"] == passed
    elif hold == JEV_FINAL_HOLD:
        assert checks["ja"]["jev"] == {"tier": "confirm", "confidence": 0.62, "reasons": []}
        assert checks["en"]["jev"] == {"tier": "act", "confidence": 0.97, "reasons": []}
        assert checks["ja"]["final_edit"] == passed
    else:
        # The owner rewrote the Japanese and had the article checked again. What the final
        # editor and Jev said of the Japanese was about text that is gone, and Jev's answers
        # for the other locales came before their newest review. None of it is sent.
        assert checks["ja"] == {"jev": None, "final_edit": None, "lint": []}
        assert [record["jev"] for record in checks.values()] == [None] * 5
        # The final editor's pass still describes the text of a locale nobody touched.
        assert checks["en"]["final_edit"] == checks["zh-TW"]["final_edit"] == passed


@pytest.mark.asyncio
async def test_the_final_editors_hold_on_text_an_edit_replaced_is_not_shown_to_the_judge(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await held_article(factory, monkeypatch, FINAL_EDIT_HOLD)
    await rechecked(factory, candidate_id, "ko")
    asked = judge_answers(monkeypatch, "final", "manual")

    await judged(factory, candidate_id)

    payload = payload_of(asked)
    assert payload["hold"]["code"] == READY_TO_PUBLISH
    # The objection was to a sentence the owner has since rewritten; the judge may publish.
    assert payload["allowed_decisions"] == ["publish", "reject", "manual"]
    assert payload["held"] == {}
    assert payload["checks"]["ko"] == {"jev": None, "final_edit": None, "lint": []}
    assert "The launch date is not in the evidence." not in json.dumps(payload)
    assert payload["checks"]["en"]["final_edit"] == {"verdict": "pass", "issues": []}


@pytest.mark.asyncio
@pytest.mark.parametrize("edited", ["en", "ko"], ids=["a-passed-locale", "the-held-locale"])
async def test_a_locale_edited_since_the_final_editor_read_it_is_shown_as_held(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, edited: str
) -> None:
    """Edited in the guide editor and not checked again: the hold is still the final
    editor's, and its record of that locale describes the text before the edit."""

    candidate_id = await held_article(factory, monkeypatch, FINAL_EDIT_HOLD)
    await edit_saved_locale(factory, edited, f"Release {edited}, edited by the owner")
    asked = judge_answers(monkeypatch, "final", "manual")

    await judged(factory, candidate_id)

    payload = payload_of(asked)
    assert payload["hold"]["code"] == FINAL_EDIT_HOLD
    assert set(payload["held"]) == {"ko", edited}
    assert payload["held"][edited]["title"] == f"Release {edited}, edited by the owner"
    assert payload["checks"][edited]["final_edit"] is None
    assert payload["checks"]["ja"]["final_edit"] == {"verdict": "pass", "issues": []}


@pytest.mark.asyncio
async def test_the_judge_is_shown_the_ten_closest_known_stories_for_a_duplicate(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await held_duplicate(factory, monkeypatch)
    async with factory() as session:
        for number in range(12):
            await seed_published_news(
                session,
                f"ai-news-story-{number}-{EVENT_DAY:%Y%m%d}",
                EVENT_DAY,
                {"en": f"Weather satellite launch number {number}"},
            )
        await seed_published_news(
            session, f"ai-news-the-same-{EVENT_DAY:%Y%m%d}", EVENT_DAY, {"en": "Model released"}
        )
    asked = judge_answers(monkeypatch, "duplicate", "manual")

    await judged(factory, candidate_id)

    payload = payload_of(asked)
    assert set(payload) == COMMON_KEYS | {"title", "known_stories"}
    named(ai.JUDGE_DUPLICATE_INSTRUCTIONS, set(payload) - COMMON_KEYS | {"allowed_decisions"})
    assert payload["title"] == "Model release"
    assert payload["hold"]["code"] == DUPLICATE_UNCERTAIN
    assert payload["allowed_decisions"] == ["distinct", "duplicate", "manual"]
    assert len(payload["known_stories"]) == 10
    assert payload["known_stories"][0] == "Model released"
    assert payload["sources"] == {"websites": 1, "first_party": False, "trusted_alone": False}


REDRAFT_KEYS = COMMON_KEYS | {
    "stop",
    "rewrites_used",
    "rewrites_limit",
    "earlier_directions",
    "claims",
    "checks",
}
OLDER_DRAFT = "An older draft that a retry left on the candidate"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "stop", ["news_verification_failed", "news_claim_source_invalid", "news_event_date_invalid"]
)
async def test_a_stopped_draft_is_judged_on_this_attempts_records_and_never_on_stored_text(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, stop: str
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch, stop)
    async with factory() as session:
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None and candidate.processing_started_at is not None
        # An earlier attempt got as far as a verified draft; a retry then failed sooner.
        # Its text and its passing verification are still there, on the same evidence.
        older = news_document(OLDER_DRAFT)
        candidate.draft_bundle_json = {"zh-TW": older.model_dump(mode="json")}
        session.add(
            NewsAssessment(
                candidate_id=candidate_id,
                assessment_type="verification",
                verdict="pass",
                reasons_json=["An issue recorded for the older draft"],
                details_json={"round": 1, "document_sha256": document_fingerprint(older)},
                evidence_hash=candidate.evidence_hash,
                prompt_version="news-v1",
                created_at=candidate.processing_started_at - timedelta(hours=2),
            )
        )
        # And a record of this attempt's time, about other evidence.
        session.add(
            NewsAssessment(
                candidate_id=candidate_id,
                assessment_type="verification",
                verdict="manual",
                reasons_json=["An issue recorded on other evidence"],
                details_json={"round": 1},
                evidence_hash="0" * 64,
                prompt_version="news-v1",
            )
        )
        await session.commit()
        assert await service.verified_zh_draft(session, candidate) is not None
    asked = judge_answers(monkeypatch, "redraft", "manual")

    await judged(factory, candidate_id)

    payload = payload_of(asked)
    facts = set() if stop == "news_verification_failed" else {"facts"}
    assert set(payload) == REDRAFT_KEYS | facts
    named(ai.JUDGE_REDRAFT_INSTRUCTIONS, set(payload) - COMMON_KEYS | {"allowed_decisions"})
    sent = json.dumps(payload, ensure_ascii=False)
    assert OLDER_DRAFT not in sent
    assert "older draft" not in sent and "other evidence" not in sent
    assert payload["stop"] == payload["hold"]
    assert payload["stop"]["code"] == stop and payload["stop"]["detail"]
    assert (payload["rewrites_used"], payload["rewrites_limit"]) == (0, 2)
    assert payload["earlier_directions"] == []
    assert payload["allowed_decisions"] == ["rewrite", "reject", "manual"]
    assert payload["sources"] == {"websites": 1, "first_party": True, "trusted_alone": False}
    assert [item["role"] for item in payload["evidence"]] == ["evidence", "lead_only"]
    if stop == "news_verification_failed":
        assert payload["checks"] == {
            "verification": [
                {
                    "round": 1,
                    "verdict": "revise",
                    "issues": ["The launch date is not in the evidence."],
                },
                {
                    "round": 2,
                    "verdict": "manual",
                    "issues": ["The benchmark figure has no source."],
                },
            ]
        }
        assert payload["claims"] == [
            {"claim": "The model shipped.", "source_urls": [FIRST_PARTY_URL]}
        ]
    elif stop == "news_claim_source_invalid":
        assert payload["checks"] == {"verification": []}
        # A lead-only page is not evidence, however it is listed beside the evidence.
        assert payload["facts"] == {
            "cited_urls_not_evidence": sorted(["https://elsewhere.example/blog", LEAD_URL]),
            "allowed_urls": [FIRST_PARTY_URL],
        }
        assert payload["claims"][0]["source_urls"][0] == "https://elsewhere.example/blog"
    else:
        assert payload["checks"] == {"verification": []}
        assert payload["facts"] == {
            "event_date": TODAY.isoformat(),
            "slug": f"ai-news-model-release-{TODAY:%Y%m%d}",
            "today": datetime.now(UTC).date().isoformat(),
            "newest_evidence_date": EVENT_DAY.isoformat(),
        }


@pytest.mark.asyncio
async def test_a_translation_a_reviewer_refused_is_shown_with_its_source_and_both_reviews(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate_id = await stopped_draft(factory, monkeypatch, "news_locale_review_failed")
    before = await stored(factory, candidate_id)
    assert set(before.draft_bundle_json) == {"zh-TW", "zh-CN"}
    asked = judge_answers(monkeypatch, "redraft", "manual")

    await judged(factory, candidate_id)

    payload = payload_of(asked)
    assert set(payload) == REDRAFT_KEYS | {"verified_zh_tw", "held"}
    named(ai.JUDGE_REDRAFT_INSTRUCTIONS, set(payload) - COMMON_KEYS | {"allowed_decisions"})
    # The verification rounds are covered by "checks"; the record of the refused translation
    # is singled out by its place under it.
    singled_out = {f"checks.{key}" for key in payload["checks"]} - {"checks.verification"}
    assert singled_out == {"checks.locale_review"}
    named(ai.JUDGE_REDRAFT_INSTRUCTIONS, singled_out)
    assert payload["stop"] == {
        "code": "news_locale_review_failed",
        "detail": "zh-CN review did not pass.",
    }
    assert payload["checks"]["locale_review"] == {
        "locale": "zh-CN",
        "verdict": "manual",
        "issues": ["The second paragraph drops the price."],
        "discarded_correction_issues": ["The correction still drops the price."],
    }
    assert payload["verified_zh_tw"] == for_review(
        GuideDocument.model_validate(before.draft_bundle_json["zh-TW"])
    )
    # The translation as it was reviewed, not the correction that was thrown away.
    assert payload["held"] == {
        "zh-CN": for_review(GuideDocument.model_validate(before.draft_bundle_json["zh-CN"]))
    }
    assert payload["held"]["zh-CN"]["title"] == "Release zh-CN"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("stage", "decision", "restored"),
    [
        ("zh_draft", "reject", "manual_review"),
        ("final", "reject", "manual_review"),
        ("duplicate", "duplicate", "manual_review"),
        ("redraft", "reject", "needs_redraft"),
    ],
)
async def test_a_story_the_judge_closed_can_be_taken_back_and_is_not_judged_again(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, stage: str, decision: str, restored: str
) -> None:
    candidate_id = await SEEDS[stage](factory, monkeypatch)
    async with factory() as session:
        owner_id = await seed_owner(session)
    asked = judge_answers(monkeypatch, stage, decision)
    closed = await judged(factory, candidate_id)
    hold = closed.outcome.hold
    assert closed.candidate.status in {"rejected", "duplicate"}

    async with factory() as session:
        owner = await session.get(User, owner_id)
        assert owner is not None
        detail = await service.reopen_candidate(
            session, owner, candidate_id, CandidateAction(reason="I want to read this one")
        )
        reopened = await session.get(NewsCandidate, candidate_id)
        assert reopened is not None
        assert not await judge.wanted(session, reopened)
        assert await judge.exclusion(session, reopened) == "answered"
    again = await judged(factory, candidate_id)

    assert (detail.status, detail.error_code, detail.judge_decision) == (restored, hold, "manual")
    assert (detail.human_decision, detail.human_reason) == (None, OWNER_NOTE)
    assert reopened.judge_hold == hold
    assert again.outcome == judge.JudgeOutcome("nothing")
    assert again.verdicts == []
    asked.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("verdict", ["pass", "manual"])
async def test_refreshed_evidence_keeps_a_story_the_judge_called_distinct(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, verdict: str
) -> None:
    async def refresh(_session: Any, evidence: list[NewsEvidence], **_kwargs: Any) -> Any:
        for row in evidence:
            if row.url == FIRST_PARTY_URL:
                row.content_hash = "a" * 64
        return [FIRST_PARTY_URL], []

    monkeypatch.setattr(service, "refresh_evidence", refresh)
    async with factory() as session:
        owner_id = await seed_owner(session)
        candidate = await held_for_changed_evidence(session)
        # The answer on record for the old evidence is the judge's, not Jev's.
        answer = await session.scalar(
            select(NewsAssessment).where(NewsAssessment.assessment_type == "duplicate")
        )
        assert answer is not None
        answer.assessment_type, answer.provider, answer.verdict = "judge", "anthropic", verdict
        answer.details_json = {"stage": "duplicate", "hold": DUPLICATE_UNCERTAIN}
        await session.commit()
        owner = await session.get(User, owner_id)
        assert owner is not None

        await service.refresh_candidate_evidence(
            session, owner, candidate.id, CandidateAction(reason="Checked by hand")
        )
        refreshed = await session.get(NewsCandidate, candidate.id)
        assert refreshed is not None
        carried = list(
            await session.scalars(
                select(NewsAssessment.evidence_hash).where(
                    NewsAssessment.assessment_type == "duplicate",
                    NewsAssessment.provider == "human",
                )
            )
        )
        cleared = await cleared_by_editor(session, refreshed)

    # "pass" is the judge's "not a duplicate"; a hand-back answered nothing to carry.
    assert carried == ([refreshed.evidence_hash] if verdict == "pass" else [])
    assert cleared is (verdict == "pass")


def rq_queue(monkeypatch: pytest.MonkeyPatch) -> Queue:
    """RQ itself on an in-memory Redis. Unlike a Mock it refuses a job id it cannot store
    and keeps the ones it has, which is what queueing a hold once depends on."""

    queue = Queue("news", connection=fakeredis.FakeStrictRedis())
    # jobs.py closes the connection it is handed after each use; this one has to stay open.
    monkeypatch.setattr(jobs, "_queue", lambda: (Mock(), queue))
    return queue


def test_a_hold_is_queued_for_the_judge_once_and_a_tag_asks_again(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    queue = rq_queue(monkeypatch)
    candidate_id = uuid4()
    plain = f"news-judge-{candidate_id}-2-news_zh_draft_ready"
    tagged = f"{plain}-backfill-489000"
    rerun = f"news-judge-{candidate_id}-3-news_jev_final_hold"

    assert jobs.enqueue_judge_once(candidate_id, 2, ZH_DRAFT_READY) == plain
    assert jobs.enqueue_judge_once(candidate_id, 2, ZH_DRAFT_READY) is None
    # Off the queue, as after it ran: RQ still keeps the job, so the id stays taken.
    queue.remove(plain)
    assert jobs.enqueue_judge_once(candidate_id, 2, ZH_DRAFT_READY) is None
    assert jobs.enqueue_judge_once(candidate_id, 2, ZH_DRAFT_READY, tag="backfill-489000") == tagged
    assert jobs.enqueue_judge_once(candidate_id, 2, ZH_DRAFT_READY, tag="backfill-489000") is None
    # A rerun raises the count; what stops the story next is a hold of its own.
    assert jobs.enqueue_judge_once(candidate_id, 3, JEV_FINAL_HOLD) == rerun
    assert queue.job_ids == [tagged, rerun]

    job = queue.fetch_job(tagged)
    assert job is not None
    assert (job.func_name, job.args) == ("app.news_automation.jobs.run_judge", (str(candidate_id),))
    assert (job.timeout, job.result_ttl, job.failure_ttl) == (1_800, 86_400, 604_800)
    # No Retry: the judge counts its own failed calls and asks for the next try itself.
    assert (job.retries_left, job.retry_intervals) == (None, None)


def test_every_hold_the_judge_answers_makes_a_job_id_rq_accepts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    queue = rq_queue(monkeypatch)
    holds = sorted({*judge.REVIEW_HOLDS, *judge.REDRAFT_HOLDS})
    for hold in holds:
        # RQ takes letters, digits, underscores and dashes, and raises on anything else.
        assert jobs.enqueue_judge_once(uuid4(), 0, hold, tag="restarted-1791000000") is not None
    assert queue.count == len(holds) == 9


def job_doubles(monkeypatch: pytest.MonkeyPatch) -> Mock:
    """Stand-ins for everything a job opens, as the candidate job's own tests use them;
    returns the queue."""

    queue = Mock()
    monkeypatch.setattr(jobs, "SessionFactory", FakeSessionFactory)
    monkeypatch.setattr(jobs, "load_runtime_settings", AsyncMock(return_value=get_settings()))
    monkeypatch.setattr(jobs, "get_redis", Mock())
    monkeypatch.setattr(jobs, "_close_resources", AsyncMock())
    monkeypatch.setattr(jobs, "_queue", lambda: (Mock(), queue))
    return queue


RESULTS = [
    ("manual_review", True),
    ("needs_redraft", True),
    ("skipped", True),
    ("published", False),
    ("rejected", False),
    ("duplicate", False),
    ("needs_evidence", False),
    ("shadow_review", False),
    ("jev_paused", False),
    ("disabled", False),
    ("paused", False),
    ("deferred", False),
]


@pytest.mark.parametrize(("result", "offered"), RESULTS)
def test_a_candidates_run_offers_the_story_to_the_judge_only_where_it_may_rest_in_a_hold(
    monkeypatch: pytest.MonkeyPatch, result: str, offered: bool
) -> None:
    queue = job_doubles(monkeypatch)
    offer = AsyncMock()
    monkeypatch.setattr(jobs, "process_candidate", AsyncMock(return_value=result))
    monkeypatch.setattr(jobs, "_offer_to_judge", offer)
    candidate_id = uuid4()

    jobs.run_candidate(str(candidate_id))

    assert offer.await_count == int(offered)
    if offered:
        assert offer.await_args is not None and offer.await_args.args[1] == candidate_id
    # The candidate's own two waits are as they were.
    assert queue.enqueue_in.call_count == int(result in {"paused", "deferred"})
    queue.enqueue.assert_not_called()


def test_a_run_whose_reply_failed_validation_offers_nothing_to_the_judge(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    job_doubles(monkeypatch)
    offer = AsyncMock()
    failed = AsyncMock(side_effect=ValueError("The reply came back incomplete."))
    monkeypatch.setattr(jobs, "process_candidate", failed)
    monkeypatch.setattr(jobs, "_offer_to_judge", offer)

    # Returns, as before: the candidate is marked failed and RQ is given nothing to retry.
    jobs.run_candidate(str(uuid4()))

    failed.assert_awaited_once()
    offer.assert_not_awaited()


OFFERS: list[tuple[str, str | None, dict[str, Any], bool]] = [
    ("manual_review", ZH_DRAFT_READY, {"retry_count": 3}, True),
    ("needs_redraft", "news_verification_failed", {}, True),
    (
        "manual_review",
        ZH_DRAFT_READY,
        {"judge_hold": ZH_DRAFT_READY, "judge_decision": "manual"},
        False,
    ),
    ("manual_review", "news_hard_checks_failed", {}, False),
    ("needs_redraft", "news_not_eligible", {}, False),
    # Held by the final editor after a person confirmed it: the judge could only hand it back.
    ("manual_review", FINAL_EDIT_HOLD, {"human_decision": "publish"}, False),
    ("drafting", None, {}, False),
    ("published", None, {}, False),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status", "hold", "changes", "queued"),
    OFFERS,
    ids=[
        "review",
        "redraft",
        "answered",
        "owners-work",
        "writer-declined",
        "nothing-to-decide",
        "running",
        "out",
    ],
)
async def test_the_trigger_queues_the_judge_only_for_a_hold_it_would_answer(
    factory: Factory,
    monkeypatch: pytest.MonkeyPatch,
    status: str,
    hold: str | None,
    changes: dict[str, Any],
    queued: bool,
) -> None:
    queue = rq_queue(monkeypatch)
    async with factory() as session:
        candidate = await seed_hold(session, status, hold, **changes)
        candidate_id, retry_count = candidate.id, candidate.retry_count

    async with factory() as session:
        await jobs._offer_to_judge(session, candidate_id)
        await jobs._offer_to_judge(session, uuid4())

    wanted = [f"news-judge-{candidate_id}-{retry_count}-{hold}"] if queued else []
    assert queue.job_ids == wanted


@pytest.mark.asyncio
@pytest.mark.parametrize(("switch", "off"), SWITCHES_OFF)
async def test_the_trigger_queues_nothing_while_one_of_the_four_switches_is_off(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, switch: str, off: Any
) -> None:
    queue = rq_queue(monkeypatch)
    async with factory() as session:
        candidate = await seed_hold(session, "manual_review", ZH_DRAFT_READY)
        settings = await session.get(NewsAutomationSettings, 1)
        assert settings is not None
        on = getattr(settings, switch)
        setattr(settings, switch, off)
        await session.commit()
        candidate_id = candidate.id

    async with factory() as session:
        await jobs._offer_to_judge(session, candidate_id)
        assert queue.job_ids == []
        # Switched back on, the next job that finds the story resting there queues it.
        settings = await session.get(NewsAutomationSettings, 1)
        assert settings is not None
        setattr(settings, switch, on)
        await session.commit()
        await jobs._offer_to_judge(session, candidate_id)

    assert queue.job_ids == [f"news-judge-{candidate_id}-0-{ZH_DRAFT_READY}"]


@pytest.mark.asyncio
async def test_the_trigger_goes_by_the_stored_row_not_by_what_its_session_holds(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    queue = rq_queue(monkeypatch)
    async with factory() as session:
        candidate_id = (await seed_hold(session, "manual_review", ZH_DRAFT_READY)).id

    async with factory() as session:
        held = await session.get(NewsCandidate, candidate_id)
        assert held is not None and await judge.wanted(session, held)
        await session.commit()
        async with factory() as owner:
            # The owner rejects it before the candidate's job gets as far as the judge.
            row = await owner.get(NewsCandidate, candidate_id)
            assert row is not None
            row.status, row.human_decision = "rejected", "reject"
            await owner.commit()
        await jobs._offer_to_judge(session, candidate_id)

    assert queue.job_ids == []


@pytest.mark.asyncio
async def test_a_queue_that_is_down_is_logged_and_never_raised_into_the_candidates_job(
    factory: Factory, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    def down() -> tuple[Mock, Queue]:
        raise RedisConnectionError("Redis is not answering.")

    monkeypatch.setattr(jobs, "_queue", down)
    async with factory() as session:
        candidate_id = (await seed_hold(session, "manual_review", ZH_DRAFT_READY)).id

    async with factory() as session:
        await jobs._offer_to_judge(session, candidate_id)

    assert f"news candidate {candidate_id} could not be queued for the review judge" in caplog.text
    assert "Redis is not answering." in caplog.text


def job_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Factory:
    """The database a job runs against, with the job's other resources stood in for.

    A job is its own ``asyncio.run``, as under RQ, so nothing is pooled: a connection must
    not outlive the event loop that opened it.
    """

    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'jobs.db'}", poolclass=NullPool)
    tables = cast(list[Table], [model.__table__ for model in NEWS_TABLES])

    async def create() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))

    asyncio.run(create())
    made = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(jobs, "SessionFactory", made)
    monkeypatch.setattr(jobs, "load_runtime_settings", AsyncMock(return_value=get_settings()))
    monkeypatch.setattr(jobs, "get_redis", Mock())
    monkeypatch.setattr(jobs, "_close_resources", AsyncMock())
    return made


async def seed_newsroom_story(made: Factory) -> UUID:
    """A story no run has touched yet, which stage one cannot send out by itself."""

    async with made() as session:
        candidate = await seed_single_source_candidate(session)
        await judge_on(session)
        await not_first_party(session)
        await session.commit()
        return candidate.id


def test_a_story_goes_from_its_hold_to_the_judge_and_from_its_approval_to_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    made = job_database(tmp_path, monkeypatch)
    queue = rq_queue(monkeypatch)
    candidate_id = asyncio.run(seed_newsroom_story(made))
    stage_one_mocks(monkeypatch)
    monkeypatch.setattr(ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, [])))
    stage_two_mocks(monkeypatch)
    judge_job = f"news-judge-{candidate_id}-0-{ZH_DRAFT_READY}"
    rerun_job = f"news-candidate-{candidate_id}-1"

    jobs.run_candidate(str(candidate_id))
    held = asyncio.run(stored(made, candidate_id))
    assert (held.status, held.error_code) == ("manual_review", ZH_DRAFT_READY)
    assert queue.job_ids == [judge_job]

    # A second job for the candidate (RQ's retry, a sweep) is skipped, finds the story
    # resting in the same hold, and does not pay for a second judge.
    jobs.run_candidate(str(candidate_id))
    assert queue.job_ids == [judge_job]

    asked = judge_answers(monkeypatch, "zh_draft", "publish")
    jobs.run_judge(str(candidate_id))
    approved = asyncio.run(stored(made, candidate_id))
    asked.assert_awaited_once()
    assert (approved.status, approved.error_code, approved.retry_count) == (
        "discovered",
        pipeline.JUDGE_APPROVED_MARKER,
        1,
    )
    assert queue.job_ids == [judge_job, rerun_job]

    jobs.run_candidate(str(candidate_id))
    published = asyncio.run(stored(made, candidate_id))
    assert (published.status, published.human_decision) == ("published", None)
    # Published is not a hold: nothing more is queued for the judge.
    assert queue.job_ids == [judge_job, rerun_job]


def test_a_queue_that_is_down_when_a_story_reaches_its_hold_does_not_fail_the_candidates_job(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    def down() -> tuple[Mock, Queue]:
        raise RedisConnectionError("Redis is not answering.")

    made = job_database(tmp_path, monkeypatch)
    monkeypatch.setattr(jobs, "_queue", down)
    candidate_id = asyncio.run(seed_newsroom_story(made))
    stage_one_mocks(monkeypatch)
    monkeypatch.setattr(ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, [])))

    # RQ would run a failed job again, for a draft that is already written and saved.
    jobs.run_candidate(str(candidate_id))

    held = asyncio.run(stored(made, candidate_id))
    assert (held.status, held.error_code) == ("manual_review", ZH_DRAFT_READY)
    assert "could not be queued for the review judge" in caplog.text


OUTCOMES = {
    "nothing": judge.JudgeOutcome("nothing", hold=ZH_DRAFT_READY, verdict="manual"),
    "requeue": judge.JudgeOutcome("requeue", hold=ZH_DRAFT_READY, retry_count=4, verdict="publish"),
    "retry_later": judge.JudgeOutcome("retry_later", hold=ZH_DRAFT_READY, retry_count=3),
}


@pytest.mark.parametrize("action", list(OUTCOMES))
def test_the_judge_job_queues_what_the_judges_outcome_calls_for(
    monkeypatch: pytest.MonkeyPatch, action: str
) -> None:
    job_doubles(monkeypatch)
    runtime = get_settings().model_copy()
    monkeypatch.setattr(jobs, "load_runtime_settings", AsyncMock(return_value=runtime))
    queue = rq_queue(monkeypatch)
    asked = AsyncMock(return_value=OUTCOMES[action])
    monkeypatch.setattr(judge, "judge_candidate", asked)
    candidate_id = uuid4()
    before = datetime.now(UTC)

    jobs.run_judge(str(candidate_id))

    asked.assert_awaited_once()
    assert asked.await_args is not None
    # The judge's vendor key and model are admin AI settings, read as the pipeline's are.
    assert asked.await_args.args[2] is runtime
    assert asked.await_args.args[3] == candidate_id
    waiting = queue.scheduled_job_registry.get_job_ids()
    if action == "nothing":
        assert (queue.job_ids, waiting) == ([], [])
    elif action == "requeue":
        # The candidate's own job, under the count the verdict raised it to.
        assert (queue.job_ids, waiting) == ([f"news-candidate-{candidate_id}-4"], [])
        rerun = queue.fetch_job(queue.job_ids[0])
        assert rerun is not None
        assert (rerun.func_name, rerun.args, rerun.retries_left) == (
            "app.news_automation.jobs.run_candidate",
            (str(candidate_id),),
            2,
        )
    else:
        slots = {int(moment.timestamp() // 1800) for moment in (before, datetime.now(UTC))}
        assert queue.job_ids == [] and len(waiting) == 1
        assert waiting[0] in {
            f"news-judge-{candidate_id}-3-{ZH_DRAFT_READY}-later-{slot}" for slot in slots
        }
        later = queue.fetch_job(waiting[0])
        assert later is not None
        assert (later.func_name, later.args, later.timeout) == (
            "app.news_automation.jobs.run_judge",
            (str(candidate_id),),
            1_800,
        )
        due = queue.scheduled_job_registry.get_scheduled_time(later)
        assert timedelta(minutes=29) < due - before < timedelta(minutes=31)


@pytest.mark.asyncio
async def test_a_restarting_worker_fails_the_judges_cut_off_runs_and_names_the_holds_to_ask_again(
    factory: Factory, monkeypatch: pytest.MonkeyPatch
) -> None:
    async with factory() as session:
        cut_off = await seed_hold(session, "manual_review", ZH_DRAFT_READY, retry_count=2)
        # The owner rejected this one while the judge was still asking.
        decided = await seed_candidate(session, status="rejected")
        decided.error_code, decided.human_decision = DUPLICATE_UNCERTAIN, "reject"
        # Auto-publish is off for its vertical, so the judge may not act on it now.
        closed = await seed_candidate(session, status="needs_redraft", vertical="crypto")
        closed.error_code = "news_verification_failed"
        # Held and wanted, but no judge run of its own was cut off.
        waiting = await seed_candidate(session, status="manual_review")
        waiting.error_code = ZH_DRAFT_READY
        drafting = await seed_candidate(session, status="drafting")
        await session.commit()
        await pipeline._start_run(session, cut_off, "judge-zh-draft")
        await pipeline._start_run(session, decided, "judge-duplicate")
        await pipeline._start_run(session, closed, "judge-redraft")
        await pipeline._start_run(session, drafting, "draft")
        assert await judge.wanted(session, waiting)
        before = {
            row.id: (row.status, row.error_code, row.judge_hold)
            for row in await session.scalars(select(NewsCandidate))
        }
        cut_off_id = cut_off.id
    monkeypatch.setattr(worker, "SessionFactory", factory)
    monkeypatch.setattr(worker, "engine", factory.kw["bind"])

    again = await worker.recover_interrupted_judging()

    async with factory() as session:
        runs = {
            run.stage: (run.status, run.error_code)
            for run in await session.scalars(select(NewsPipelineRun))
        }
        after = {
            row.id: (row.status, row.error_code, row.judge_hold)
            for row in await session.scalars(select(NewsCandidate))
        }
    assert again == [(cut_off_id, 2, ZH_DRAFT_READY)]
    assert runs == {
        "judge-zh-draft": ("failed", "news_processing_stale"),
        "judge-duplicate": ("failed", "news_processing_stale"),
        "judge-redraft": ("failed", "news_processing_stale"),
        # A candidate cut off mid-pipeline is recover_interrupted's, not this function's.
        "draft": ("running", None),
    }
    assert after == before


def test_a_restarting_worker_sends_cut_off_holds_back_to_the_judge_before_the_pool_starts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[object] = []
    tags: list[str] = []
    stalled, held = uuid4(), uuid4()

    async def recover() -> list[UUID]:
        events.append("candidates")
        return [stalled]

    async def recover_judging() -> list[tuple[UUID, int, str]]:
        events.append("judging")
        return [(held, 2, ZH_DRAFT_READY)]

    def rerun(candidate_id: UUID, reason: str) -> str:
        events.append(("candidate", candidate_id, reason))
        return "job"

    def judge_again(candidate_id: UUID, retry_count: int, hold: str, *, tag: str) -> str:
        events.append(("judge", candidate_id, retry_count, hold))
        tags.append(tag)
        return "job"

    class Pool:
        def __init__(self, _queues: list[str], **_kwargs: object) -> None:
            events.append("pool")

        def start(self) -> None:
            events.append("start")

    monkeypatch.setattr(worker, "recover_interrupted", recover)
    monkeypatch.setattr(worker, "recover_interrupted_judging", recover_judging)
    monkeypatch.setattr(worker, "enqueue_candidate_once", rerun)
    monkeypatch.setattr(worker, "enqueue_judge_once", judge_again)
    monkeypatch.setattr(worker, "WorkerPool", Pool)
    monkeypatch.setattr(worker, "pool_size", lambda configured: configured)
    monkeypatch.setattr("app.news_automation.worker.Redis", Mock())
    monkeypatch.setattr(
        worker, "get_settings", lambda: Mock(redis_url="redis://x", news_worker_processes=2)
    )
    started = int(datetime.now(UTC).timestamp())

    worker.main()

    assert events == [
        "candidates",
        ("candidate", stalled, "restarted"),
        "judging",
        ("judge", held, 2, ZH_DRAFT_READY),
        "pool",
        "start",
    ]
    # The job the restart cut off still holds the plain id in RQ; the tag makes a new one.
    word, _, second = tags[0].partition("-")
    assert word == "restarted"
    assert started <= int(second) <= int(datetime.now(UTC).timestamp())
