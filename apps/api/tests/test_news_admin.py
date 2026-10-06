from __future__ import annotations

import hashlib
import io
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.auth.service import current_user
from app.db import get_session
from app.models import User
from app.news_automation import assets, jobs, router, service
from app.news_automation.models import NewsAsset, NewsAutomationSettings, NewsCandidate
from app.news_automation.schemas import CandidateAction, StatsView
from app.problems import AppError, app_error_handler


@pytest.mark.asyncio
async def test_news_admin_routes_require_content_capabilities(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    holder = {"user": User(id=uuid4(), email="viewer@example.com", password_hash="unused")}

    async def user() -> User:
        return holder["user"]

    async def session() -> object:
        yield AsyncMock()

    stats = AsyncMock(
        return_value=StatsView(pending_review=2, failed=1, published=3, queue_by_status={})
    )
    monkeypatch.setattr(service, "stats", stats)
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(router.admin_router, prefix="/api/v1")
    app.dependency_overrides[current_user] = user
    app.dependency_overrides[get_session] = session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        forbidden = await client.get("/api/v1/admin/news/stats")
        holder["user"]._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
        allowed = await client.get("/api/v1/admin/news/stats")
    assert forbidden.status_code == 403
    assert allowed.status_code == 200
    assert allowed.json()["pending_review"] == 2


@pytest.mark.asyncio
async def test_public_asset_refuses_invalid_or_unpublished_ids_and_verifies_bytes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = AsyncMock()
    with pytest.raises(AppError) as invalid:
        await assets.public_asset(session, "../secret.webp")
    assert invalid.value.status == 404
    session.scalar.return_value = None
    with pytest.raises(AppError) as unpublished:
        await assets.public_asset(session, "a" * 32 + "-hero.webp")
    assert unpublished.value.status == 404

    body = b"safe-webp"
    row = NewsAsset(
        candidate_id=uuid4(),
        variant="hero",
        locale=None,
        storage_key="news/key",
        public_filename="a" * 32 + "-hero.webp",
        content_type="image/webp",
        sha256=hashlib.sha256(body).hexdigest(),
        size=len(body),
        width=1600,
        height=900,
        is_public=True,
    )
    session.scalar.return_value = row
    stream = io.BytesIO(body)
    client = Mock()
    client.get_object.return_value = {"ContentLength": len(body), "Body": stream}
    monkeypatch.setattr(assets, "storage", lambda: client)
    result, content_type, digest = await assets.public_asset(session, row.public_filename)
    assert result == body
    assert content_type == "image/webp"
    assert digest == row.sha256


@pytest.mark.asyncio
async def test_post_publication_major_error_disables_vertical_autopilot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = User(id=uuid4(), email="editor@example.com", password_hash="unused")
    candidate = NewsCandidate(
        id=uuid4(),
        source_id=uuid4(),
        vertical="ai",
        status="published",
        canonical_url="https://example.com/release",
        source_title="Release",
        normalized_title="release",
        content_hash="a" * 64,
        evidence_hash="b" * 64,
        idempotency_key="c" * 64,
        prompt_version="news-v1",
        policy_version="news-policy-v1",
    )
    configuration = NewsAutomationSettings(id=1, auto_publish_ai=True)
    session = AsyncMock()
    session.add = Mock()
    session.get.return_value = candidate
    monkeypatch.setattr(service, "settings_row", AsyncMock(return_value=configuration))
    expected = Mock()
    monkeypatch.setattr(service, "candidate_detail", AsyncMock(return_value=expected))

    result = await service.report_major_error(
        session,
        actor,
        candidate.id,
        CandidateAction(reason="Material licensing error", major_error=True),
    )

    assert result is expected
    assert configuration.auto_publish_ai is False
    assert configuration.updated_by_user_id == actor.id
    assert candidate.status == "published"
    assert candidate.human_decision == "reject"
    assert candidate.human_major_error is True
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_the_detail_names_the_saved_articles_address_for_its_public_link() -> None:
    from app.guides.models import GuideArticle
    from tests.test_news_pipeline import EVENT_DAY, SLUG, database, seed_candidate

    engine, factory = await database()
    async with factory() as session:
        published = await seed_candidate(session, status="published")
        article = GuideArticle(slug=SLUG, kind="life", news_date=EVENT_DAY)
        session.add(article)
        await session.flush()
        published.guide_article_id = article.id
        unwritten = await seed_candidate(session, status="discovered")
        await session.commit()

        with_article = await service.candidate_detail(session, published.id)
        without_article = await service.candidate_detail(session, unwritten.id)
    await engine.dispose()
    assert (with_article.article_slug, with_article.article_kind) == (SLUG, "life")
    assert with_article.model_dump(mode="json")["article_slug"] == SLUG
    assert (without_article.article_slug, without_article.article_kind) == (None, None)


@pytest.mark.asyncio
async def test_the_judges_answer_is_listed_and_the_stats_count_its_redraft_hand_backs() -> None:
    from tests.test_news_pipeline import database, seed_candidate

    engine, factory = await database()
    async with factory() as session:
        # The count is of redraft rows the judge handed back, and of nothing else it answered.
        for status, decision in (
            ("needs_redraft", "manual"),
            ("needs_redraft", "manual"),
            ("needs_redraft", None),
            ("manual_review", "manual"),
            ("rejected", "reject"),
            ("duplicate", "duplicate"),
        ):
            row = await seed_candidate(session, status=status)
            row.judge_decision = decision
        await session.commit()

        listed = await service.list_candidates(session, page=1, limit=20)
        rejected = next(row for row in listed.candidates if row.status == "rejected")
        detail = await service.candidate_detail(session, rejected.id)
        totals = await service.stats(session)
    await engine.dispose()

    assert sorted((row.status, row.judge_decision or "") for row in listed.candidates) == [
        ("duplicate", "duplicate"),
        ("manual_review", "manual"),
        ("needs_redraft", ""),
        ("needs_redraft", "manual"),
        ("needs_redraft", "manual"),
        ("rejected", "reject"),
    ]
    assert detail.model_dump(mode="json")["judge_decision"] == "reject"
    assert totals.judge_handed_back == 2
    assert totals.queue_by_status["needs_redraft"] == 3


@pytest.mark.asyncio
async def test_candidate_list_takes_repeated_statuses_and_refuses_unknown_ones(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.news_automation.schemas import CandidatePage

    async def user() -> User:
        viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
        viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
        return viewer

    async def session() -> object:
        yield AsyncMock()

    listing = AsyncMock(return_value=CandidatePage(candidates=[], total=0, page=1, pages=1))
    monkeypatch.setattr(service, "list_candidates", listing)
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(router.admin_router, prefix="/api/v1")
    app.dependency_overrides[current_user] = user
    app.dependency_overrides[get_session] = session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        listed = await client.get(
            "/api/v1/admin/news/candidates",
            params=[("status", "manual_review"), ("status", "needs_evidence")],
        )
        refused = await client.get("/api/v1/admin/news/candidates", params={"status": "bogus"})
    assert listed.status_code == 200
    assert listing.await_args is not None
    assert listing.await_args.kwargs["status"] == ["manual_review", "needs_evidence"]
    assert refused.status_code == 422


@pytest.mark.asyncio
async def test_not_a_duplicate_needs_content_manage_and_queues_the_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from datetime import UTC, datetime

    from app.news_automation.schemas import CandidateDetail

    holder = {"roles": frozenset({"viewer"})}
    candidate_id = uuid4()

    async def user() -> User:
        editor = User(id=uuid4(), email="editor@example.com", password_hash="unused")
        editor._admin_roles_cache = holder["roles"]  # type: ignore[attr-defined]
        return editor

    database = AsyncMock()
    database.get.return_value = NewsCandidate(id=candidate_id, retry_count=3)

    async def session() -> object:
        yield database

    now = datetime.now(UTC)
    detail = CandidateDetail(
        id=candidate_id,
        vertical="ai",
        status="discovered",
        source_title="Model release",
        canonical_url="https://official.example/release",
        event_date=None,
        would_publish=None,
        human_decision=None,
        error_code=None,
        error_detail=None,
        guide_article_id=None,
        created_at=now,
        updated_at=now,
        evidence=[],
        assessments=[],
        runs=[],
        documents={},
        claim_ledger=[],
        lint={},
        human_reason=None,
        human_major_error=False,
    )
    cleared = AsyncMock(return_value=detail)
    enqueue = Mock(return_value="job")
    monkeypatch.setattr(service, "clear_duplicate_candidate", cleared)
    monkeypatch.setattr(jobs, "enqueue_candidate", enqueue)
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(router.admin_router, prefix="/api/v1")
    app.dependency_overrides[current_user] = user
    app.dependency_overrides[get_session] = session
    url = f"/api/v1/admin/news/candidates/{candidate_id}/not-duplicate"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        forbidden = await client.post(url, json={"reason": "Different event"})
        holder["roles"] = frozenset({"content"})
        allowed = await client.post(url, json={"reason": "Different event"})
    assert forbidden.status_code == 403
    assert allowed.status_code == 200
    assert allowed.json()["similar_titles"] == []
    cleared.assert_awaited_once()
    assert cleared.await_args is not None
    assert cleared.await_args.args[2] == candidate_id
    assert cleared.await_args.args[3].reason == "Different event"
    enqueue.assert_called_once_with(candidate_id, retry_count=3)


@pytest.mark.asyncio
async def test_taking_back_a_story_the_judge_closed_needs_content_manage_and_queues_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from datetime import UTC, datetime

    from app.news_automation.schemas import CandidateDetail

    holder = {"roles": frozenset({"viewer"})}
    candidate_id = uuid4()

    async def user() -> User:
        editor = User(id=uuid4(), email="editor@example.com", password_hash="unused")
        editor._admin_roles_cache = holder["roles"]  # type: ignore[attr-defined]
        return editor

    async def session() -> object:
        yield AsyncMock()

    now = datetime.now(UTC)
    detail = CandidateDetail(
        id=candidate_id,
        vertical="ai",
        status="manual_review",
        source_title="Model release",
        canonical_url="https://official.example/release",
        event_date=None,
        would_publish=None,
        human_decision=None,
        judge_decision="manual",
        error_code="news_zh_draft_ready",
        error_detail=None,
        guide_article_id=None,
        created_at=now,
        updated_at=now,
        evidence=[],
        assessments=[],
        runs=[],
        documents={},
        claim_ledger=[],
        lint={},
        human_reason=None,
        human_major_error=False,
    )
    reopened = AsyncMock(return_value=detail)
    enqueue = Mock(return_value="job")
    monkeypatch.setattr(service, "reopen_candidate", reopened)
    # The story goes back to the owner's list, not to the pipeline.
    monkeypatch.setattr(jobs, "enqueue_candidate", enqueue)
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(router.admin_router, prefix="/api/v1")
    app.dependency_overrides[current_user] = user
    app.dependency_overrides[get_session] = session
    url = f"/api/v1/admin/news/candidates/{candidate_id}/reopen"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        forbidden = await client.post(url, json={"reason": "I want to read this one"})
        holder["roles"] = frozenset({"content"})
        unexplained = await client.post(url, json={})
        allowed = await client.post(url, json={"reason": "I want to read this one"})
    assert forbidden.status_code == 403
    assert unexplained.status_code == 422
    assert allowed.status_code == 200
    assert (allowed.json()["status"], allowed.json()["judge_decision"]) == (
        "manual_review",
        "manual",
    )
    reopened.assert_awaited_once()
    assert reopened.await_args is not None
    assert reopened.await_args.args[2] == candidate_id
    assert reopened.await_args.args[3].reason == "I want to read this one"
    enqueue.assert_not_called()
