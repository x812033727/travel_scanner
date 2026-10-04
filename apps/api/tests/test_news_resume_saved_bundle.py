"""Resuming the five-locale articles a retired hard check stopped (2026-10-04).

From 2026-10-01 until #1201 every automatic article failed the hard checks for a process
figure the pipeline no longer drew. Before #1136 such an article was kept only on the
candidate as ``needs_redraft``; 38 of them waited in production with their translations,
locale reviews and final edits on record. ``backfill_cli --resume-saved-bundles`` runs them
again from the hard checks without drafting or translating anything.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest
from sqlalchemy import Table, delete, select
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
)
from app.guides.schemas import GuideDocument
from app.models import AdminAuditLog, User
from app.news_automation import ai, backfill_cli, jobs, pipeline, service
from app.news_automation.models import NewsAutomationSettings, NewsCandidate, NewsPipelineRun
from app.news_automation.schemas import LocaleReviewResult
from tests.test_news_pipeline import (
    NEWS_TABLES,
    news_document,
    seed_candidate,
    seed_single_source_candidate,
    stage_one_mocks,
    stage_two_mocks,
)

FIVE_LOCALES = ("zh-TW", "zh-CN", "en", "ja", "ko")
PUBLISHED = datetime(2026, 10, 1, 12, tzinfo=UTC)


def retired_diagram(*_args: Any, **_kwargs: Any) -> list[str]:
    """The figure every locale was refused for until #1201."""

    return ["news_diagram: a diagram is required"]


def no_problems(*_args: Any, **_kwargs: Any) -> list[str]:
    return []


async def file_database(
    tmp_path: Path,
) -> tuple[str, AsyncEngine, async_sessionmaker[AsyncSession]]:
    """A file database: the CLI disposes its engine, which would drop an in-memory one."""

    url = f"sqlite+aiosqlite:///{tmp_path / 'news.db'}"
    engine = create_async_engine(url)
    tables = cast(list[Table], [model.__table__ for model in NEWS_TABLES])
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    return url, engine, async_sessionmaker(engine, expire_on_commit=False)


async def seed_automatic_story(factory: async_sessionmaker[AsyncSession]) -> UUID:
    async with factory() as session:
        candidate = await seed_single_source_candidate(session)
        settings = await session.get(NewsAutomationSettings, 1)
        assert settings is not None
        settings.mode, settings.auto_publish_ai = "automatic", True
        candidate.source_published_at = PUBLISHED
        session.add(User(email="owner@example.com", password_hash="unused", is_admin=True))
        await session.commit()
        return candidate.id


async def seed_second_candidate(session: AsyncSession) -> NewsCandidate:
    """A second candidate in a database whose settings and topic already exist."""

    candidate = await seed_candidate(session)
    candidate.source_published_at = PUBLISHED
    await session.commit()
    return candidate


async def stopped_before_1136(
    factory: async_sessionmaker[AsyncSession], candidate_id: UUID
) -> None:
    """Run the story to the retired check, then leave it as the code before #1136 did:
    five locales on the candidate, no saved article, ``needs_redraft``."""

    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        assert result == "manual_review"
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None and candidate.guide_article_id is not None
        assert candidate.error_code == "news_hard_checks_failed"
        article_id = candidate.guide_article_id
        locale_ids = list(
            await session.scalars(
                select(GuideArticleLocale.id).where(GuideArticleLocale.article_id == article_id)
            )
        )
        candidate.guide_article_id = None
        candidate.status = "needs_redraft"
        await session.execute(
            delete(GuideArticleRevision).where(
                GuideArticleRevision.article_locale_id.in_(locale_ids)
            )
        )
        await session.execute(
            delete(GuideArticleLocale).where(GuideArticleLocale.article_id == article_id)
        )
        await session.execute(
            delete(GuideArticleTopic).where(GuideArticleTopic.article_id == article_id)
        )
        await session.execute(delete(GuideArticle).where(GuideArticle.id == article_id))
        await session.commit()
        assert set(candidate.draft_bundle_json) == set(FIVE_LOCALES)


async def resume_with_cli(
    monkeypatch: pytest.MonkeyPatch, url: str, *, apply: bool, limit: int | None = None
) -> tuple[dict[str, Any], list[tuple[UUID, int]]]:
    engine = create_async_engine(url)
    queued: list[tuple[UUID, int]] = []
    monkeypatch.setattr(backfill_cli, "SessionFactory", async_sessionmaker(engine))
    monkeypatch.setattr(backfill_cli, "engine", engine)
    monkeypatch.setattr(
        jobs,
        "enqueue_candidate",
        lambda candidate_id, retry_count=0: queued.append((candidate_id, retry_count)) or "job",
    )
    report = await backfill_cli.run(
        since=datetime(2026, 9, 28).date(),
        limit=limit,
        apply=apply,
        actor_email="owner@example.com" if apply else None,
        reason="Resume after #1201",
        saved_bundles=True,
    )
    return report, queued


def fixed_checks(monkeypatch: pytest.MonkeyPatch, check: Any = no_problems) -> None:
    """The checks after #1201, in every module that runs them."""

    for module in (pipeline, service, backfill_cli):
        monkeypatch.setattr(module, "hard_policy_problems", check)


async def stages_of(session: AsyncSession, candidate_id: UUID) -> list[str]:
    return [
        run.stage
        for run in await session.scalars(
            select(NewsPipelineRun)
            .where(NewsPipelineRun.candidate_id == candidate_id)
            .order_by(NewsPipelineRun.started_at)
        )
    ]


@pytest.mark.asyncio
async def test_a_stored_bundle_resumes_at_the_hard_checks_and_goes_out_on_jevs_last_call(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    url, engine, factory = await file_database(tmp_path)
    candidate_id = await seed_automatic_story(factory)
    duplicate_check = AsyncMock(return_value=("distinct", 0.01, []))
    monkeypatch.setattr(ai, "jev_duplicate_check", duplicate_check)
    mocks = stage_one_mocks(monkeypatch)
    translated = stage_two_mocks(monkeypatch)

    async def final_edit(*args: Any) -> tuple[LocaleReviewResult, dict[str, int], str]:
        # The editor's zh-TW text is what publication must find a verification for.
        if args[3] == "zh-TW":
            corrected = news_document("Clearer zh-TW")
            return LocaleReviewResult(verdict="revise", corrected_document=corrected), {}, "e"
        return LocaleReviewResult(verdict="pass"), {}, "editor"

    final_edits = AsyncMock(side_effect=final_edit)
    monkeypatch.setattr(ai, "final_edit", final_edits)
    monkeypatch.setattr(pipeline, "hard_policy_problems", retired_diagram)
    await stopped_before_1136(factory, candidate_id)
    async with factory() as session:
        # One with only its zh-TW draft cannot resume: there is nothing to finish.
        incomplete = await seed_second_candidate(session)
        incomplete.status, incomplete.error_code = "needs_redraft", "news_hard_checks_failed"
        incomplete.draft_bundle_json = {"zh-TW": news_document("Half").model_dump(mode="json")}
        await session.commit()
    edits_before, translations_before = final_edits.await_count, list(translated)

    fixed_checks(monkeypatch)
    listed, queued = await resume_with_cli(monkeypatch, url, apply=False)
    assert (listed["candidates"], listed["still_failing"], listed["applied"]) == (1, 0, False)
    assert listed["sample"][0]["id"] == str(candidate_id)
    assert listed["sample"][0]["hard_checks"] == {}
    assert queued == []

    applied, queued = await resume_with_cli(monkeypatch, url, apply=True)
    assert applied["applied"] is True
    assert queued == [(candidate_id, 1)]
    async with factory() as session:
        waiting = await session.get(NewsCandidate, candidate_id)
        assert waiting is not None
        assert (waiting.status, waiting.error_code) == ("discovered", pipeline.RESUME_MARKER)

        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        stages = await stages_of(session, candidate_id)
        saved = list(await session.scalars(select(GuideArticleLocale)))
        audits = [row.action for row in await session.scalars(select(AdminAuditLog))]
    await engine.dispose()

    assert result == "published"
    assert stored is not None and (stored.status, stored.error_code) == ("published", None)
    # Nothing was written again: one draft, the same translations and final edits.
    mocks["draft"].assert_awaited_once()
    assert translated == translations_before
    assert final_edits.await_count == edits_before
    assert stages[-1] == "jev-final" and stages.count("draft") == 1
    # Two days later the story is checked against what was published meanwhile.
    assert duplicate_check.await_count == 2
    assert mocks["jev_locales"][-1] == FIVE_LOCALES
    assert len(saved) == 5 and all(row.published_version is not None for row in saved)
    assert {row.locale: row.draft_json["title"] for row in saved}["zh-TW"] == "Clearer zh-TW"
    assert audits.count("news_candidate_resumed") == 1
    assert "news_candidate_auto_published" in audits


@pytest.mark.asyncio
async def test_a_resumed_bundle_keeps_the_final_editors_hold_and_waits_for_a_person(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    url, engine, factory = await file_database(tmp_path)
    candidate_id = await seed_automatic_story(factory)
    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    mocks = stage_one_mocks(monkeypatch)
    stage_two_mocks(monkeypatch)

    async def final_edit(*args: Any) -> tuple[LocaleReviewResult, dict[str, int], str]:
        if args[3] == "ko":
            return LocaleReviewResult(verdict="manual", issues=["Date not in evidence"]), {}, "e"
        return LocaleReviewResult(verdict="pass"), {}, "editor"

    monkeypatch.setattr(ai, "final_edit", final_edit)
    monkeypatch.setattr(pipeline, "hard_policy_problems", retired_diagram)
    await stopped_before_1136(factory, candidate_id)

    fixed_checks(monkeypatch)
    await resume_with_cli(monkeypatch, url, apply=True)
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


def japanese_punctuation(
    document: GuideDocument, _vertical: Any, locale: str, **_kwargs: Any
) -> list[str]:
    """A check the stored Japanese text still fails after #1201."""

    return ["news_punctuation: half-width colon next to CJK"] if locale == "ja" else []


@pytest.mark.asyncio
async def test_a_stored_bundle_a_check_still_refuses_is_listed_last_and_saved_for_the_editor(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    url, engine, factory = await file_database(tmp_path)
    candidate_id = await seed_automatic_story(factory)
    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    mocks = stage_one_mocks(monkeypatch)
    stage_two_mocks(monkeypatch)
    monkeypatch.setattr(pipeline, "hard_policy_problems", retired_diagram)
    await stopped_before_1136(factory, candidate_id)

    fixed_checks(monkeypatch, japanese_punctuation)
    listed, _queued = await resume_with_cli(monkeypatch, url, apply=False)
    assert listed["still_failing"] == 1
    assert listed["sample"][0]["hard_checks"] == {
        "ja": ["news_punctuation: half-width colon next to CJK"]
    }

    await resume_with_cli(monkeypatch, url, apply=True)
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        saved = list(await session.scalars(select(GuideArticleLocale)))
    await engine.dispose()

    assert result == "manual_review"
    assert stored is not None and stored.error_code == "news_hard_checks_failed"
    # Now an article the guide editor can fix and re-verify, not a candidate-only draft.
    assert len(saved) == 5 and all(row.published_version is None for row in saved)
    assert mocks["jev_locales"] == [("zh-TW",)]
    mocks["draft"].assert_awaited_once()


@pytest.mark.asyncio
async def test_the_resume_marker_survives_a_crash_and_a_stall_and_never_redrafts(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    url, engine, factory = await file_database(tmp_path)
    candidate_id = await seed_automatic_story(factory)
    monkeypatch.setattr(
        ai, "jev_duplicate_check", AsyncMock(return_value=("distinct", 0.01, []))
    )
    mocks = stage_one_mocks(monkeypatch)
    stage_two_mocks(monkeypatch)
    monkeypatch.setattr(pipeline, "hard_policy_problems", retired_diagram)
    await stopped_before_1136(factory, candidate_id)
    fixed_checks(monkeypatch)
    await resume_with_cli(monkeypatch, url, apply=True)

    working_jev = ai.jev_assessments
    monkeypatch.setattr(ai, "jev_assessments", AsyncMock(side_effect=RuntimeError("Jev down")))
    async with factory() as session:
        with pytest.raises(RuntimeError):
            await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        crashed = await session.get(NewsCandidate, candidate_id)
        assert crashed is not None
        assert (crashed.status, crashed.error_code) == ("failed", pipeline.RESUME_MARKER)

        # A worker killed mid-run: the stall sweep keeps the marker too.
        crashed.status = "jev_review"
        crashed.processing_started_at = datetime(2026, 10, 1, tzinfo=UTC)
        await session.commit()
        assert await pipeline.recover_stalled_candidates(session) == [candidate_id]
        stalled = await session.get(NewsCandidate, candidate_id)
        assert stalled is not None and stalled.error_code == pipeline.RESUME_MARKER

        monkeypatch.setattr(ai, "jev_assessments", working_jev)
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
    await engine.dispose()

    assert result == "published"
    mocks["draft"].assert_awaited_once()


@pytest.mark.asyncio
async def test_a_resumed_story_published_meanwhile_is_a_duplicate_and_stays_unpublished(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    url, engine, factory = await file_database(tmp_path)
    candidate_id = await seed_automatic_story(factory)
    duplicate_check = AsyncMock(return_value=("distinct", 0.01, []))
    monkeypatch.setattr(ai, "jev_duplicate_check", duplicate_check)
    mocks = stage_one_mocks(monkeypatch)
    stage_two_mocks(monkeypatch)
    monkeypatch.setattr(pipeline, "hard_policy_problems", retired_diagram)
    await stopped_before_1136(factory, candidate_id)
    fixed_checks(monkeypatch)
    await resume_with_cli(monkeypatch, url, apply=True)

    duplicate_check.return_value = ("duplicate", 0.97, [])
    async with factory() as session:
        result = await pipeline.process_candidate(session, Mock(), get_settings(), candidate_id)
        stored = await session.get(NewsCandidate, candidate_id)
        saved = list(await session.scalars(select(GuideArticleLocale)))
    await engine.dispose()

    assert result == "duplicate"
    assert stored is not None and (stored.status, stored.error_code) == ("duplicate", None)
    assert saved == []
    assert mocks["jev_locales"] == [("zh-TW",)]

