"""Scope boundaries use real SQL locally and PostgreSQL in integration CI."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.catalog_review import jobs
from app.catalog_review.repository import fingerprint
from app.catalog_review.router import router
from app.catalog_review.schemas import AssessmentBatch, DiscoveryBatch, ReviewAssessment
from app.catalog_review.scope import SCOPE_KINDS, CatalogScope, request_scope, scope_counts
from app.catalog_review.service import (
    ApplyRequest,
    ResumeRequest,
    StartRequest,
    apply_decisions,
    create_run,
    get_run,
    overview,
    prepare_resume,
    run_items,
    run_view,
)
from app.config import Settings
from app.db import get_session
from app.models import (
    AdminAuditLog,
    Base,
    CatalogReviewItem,
    CatalogReviewRun,
    FoodMerchant,
    TravelFood,
    TravelHotspot,
    User,
)
from app.problems import AppError, app_error_handler


def configured() -> Settings:
    return Settings(_env_file=None, hotspot_guide_gemini_api_key="scope-fixture-not-a-key")


@pytest_asyncio.fixture(
    params=["sqlite"] + (["postgresql"] if os.getenv("RUN_INTEGRATION_TESTS") == "1" else [])
)
async def catalog(request: pytest.FixtureRequest) -> AsyncIterator[tuple[AsyncSession, User]]:
    schema = "catalog_scope_" + uuid4().hex
    administrator = None
    if request.param == "postgresql":
        from app.config import get_settings

        administrator = create_async_engine(get_settings().database_url)
        async with administrator.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = create_async_engine(
            get_settings().database_url, connect_args={"server_settings": {"search_path": schema}}
        )
    else:
        engine = create_async_engine("sqlite+aiosqlite://")
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        factory = async_sessionmaker(engine, expire_on_commit=False)
        async with factory() as session:
            user = User(
                id=uuid4(), email="catalog-scope@example.test", is_admin=True, is_active=True
            )
            session.add(user)
            session.add_all(
                [
                    TravelHotspot(
                        slug="scope-hotspot",
                        name="Scope attraction",
                        city_code="TYO",
                        city_name="Tokyo",
                        destination_id="tokyo",
                        country_code="JP",
                        country_name="Japan",
                        category="culture",
                        search_text="Scope attraction",
                        review_status="pending",
                        is_active=False,
                    ),
                    TravelFood(
                        slug="scope-food",
                        local_name="Scope dish",
                        romanized_name="Scope dish",
                        country_code="JP",
                        food_kind="main",
                        search_text="Scope dish",
                        review_status="pending",
                        is_active=False,
                    ),
                    FoodMerchant(
                        slug="scope-merchant",
                        name="Scope merchant",
                        local_name="Scope merchant",
                        destination_id="tokyo",
                        country_code="JP",
                        review_status="pending",
                        is_active=False,
                    ),
                ]
            )
            await session.commit()
            session.info["factory"] = factory
            yield session, user
    finally:
        await engine.dispose()
        if administrator is not None:
            async with administrator.begin() as connection:
                await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
            await administrator.dispose()


async def start(session: AsyncSession, user: User, scope: CatalogScope) -> CatalogReviewRun:
    run, created = await create_run(
        session,
        configured(),
        user.id,
        StartRequest(mode="review_pending", scope=scope),
        uuid4().hex,
    )
    assert created
    return run


async def complete(session: AsyncSession, run: CatalogReviewRun) -> None:
    for item in await run_items(session, run.id, scope=request_scope(run.request_json)):
        item.status = "assessed"
        item.decision = "needs_review"
        item.assessment_json = {"confidence": 0.5}
        item.assessed_at = datetime.now(UTC)
    run.status = "completed"
    await session.commit()


@pytest.mark.parametrize("scope", ["all", "hotspots", "foods"])
def test_scope_defaults_targets_and_worker_validation(scope: CatalogScope) -> None:
    payload = StartRequest(mode="discover_new", scope=scope)
    assert payload.requested_counts == scope_counts(scope)
    assert jobs._targets(payload.model_dump()) == scope_counts(scope)
    assert request_scope({}) == "all"
    if scope != "all":
        with pytest.raises(ValidationError):
            StartRequest(
                mode="discover_new",
                scope=scope,
                requested_counts={"hotspot": 40, "food": 20, "merchant": 40},
            )
        with pytest.raises(ValueError):
            jobs._targets(
                {"scope": scope, "requested_counts": {"hotspot": 40, "food": 20, "merchant": 40}}
            )
    with pytest.raises(ValidationError):
        StartRequest(mode="review_pending", scope="hotels")


@pytest.mark.asyncio
@pytest.mark.parametrize("scope", ["all", "hotspots", "foods"])
async def test_snapshot_counts_history_and_global_lock(
    catalog: tuple[AsyncSession, User], scope: CatalogScope
) -> None:
    session, user = catalog
    run = await start(session, user, scope)
    rows = await run_items(session, run.id)
    assert {item.kind for item in rows} == set(SCOPE_KINDS[scope])
    view = await overview(session, configured(), scope)
    assert view["pending_counts"]["total"] == len(SCOPE_KINDS[scope])
    assert {
        kind for kind, value in view["pending_counts"].items() if kind != "total" and value
    } == set(SCOPE_KINDS[scope])
    assert view["runs"][0]["scope"] == scope
    other = "foods" if scope == "hotspots" else "hotspots"
    blocked = await overview(session, configured(), other)
    assert blocked["runs"] == []
    assert blocked["active_run"] == {"id": str(run.id), "scope": scope, "status": "queued"}
    assert not blocked["can_start_review"]
    with pytest.raises(AppError, match="已有目錄審核"):
        await start(session, user, other)
    await complete(session, run)
    await start(session, user, other)
    assert len((await overview(session, configured()))["runs"]) == 2
    assert len((await overview(session, configured(), scope))["runs"]) == 1


@pytest.mark.asyncio
async def test_same_scope_prior_review_and_legacy_idempotency(
    catalog: tuple[AsyncSession, User],
) -> None:
    session, user = catalog
    # Persist the exact payload/hash produced before the scope field existed.
    payload = StartRequest(mode="review_pending")
    legacy = payload.model_dump(mode="json", exclude={"scope"})
    old = CatalogReviewRun(
        id=uuid4(),
        actor_user_id=user.id,
        idempotency_key="legacy-replay",
        request_hash=fingerprint(legacy),
        request_json=legacy,
        mode="review_pending",
        phase="review_pending",
        status="completed",
        version=1,
        model="fixture",
        result_json={},
        usage_json={},
    )
    session.add(old)
    await session.commit()
    for retry in [payload, StartRequest(mode="review_pending", scope="all")]:
        replay, created = await create_run(session, configured(), user.id, retry, "legacy-replay")
        assert replay.id == old.id and not created
        assert "scope" not in replay.request_json
    with pytest.raises(AppError) as conflict:
        await create_run(
            session,
            configured(),
            user.id,
            StartRequest(mode="review_pending", scope="foods"),
            "legacy-replay",
        )
    assert conflict.value.code == "idempotency_conflict"
    with pytest.raises(AppError) as mismatch:
        await create_run(
            session,
            configured(),
            user.id,
            StartRequest(mode="discover_new", scope="foods", prior_review_run_id=old.id),
            uuid4().hex,
        )
    assert mismatch.value.code == "catalog_scope_mismatch"
    scoped = await start(session, user, "foods")
    await complete(session, scoped)
    discovered, created = await create_run(
        session,
        configured(),
        user.id,
        StartRequest(mode="discover_new", scope="foods", prior_review_run_id=scoped.id),
        uuid4().hex,
    )
    assert created and discovered.request_json["requested_counts"] == scope_counts("foods")
    assert (await run_view(session, old))["scope"] == "all"


@pytest.mark.asyncio
@pytest.mark.parametrize("configured_limit", [1, 160, 1000])
async def test_omitted_budget_snapshots_runtime_setting_and_replay_ignores_later_setting_changes(
    catalog: tuple[AsyncSession, User], configured_limit: int
) -> None:
    session, user = catalog
    payload = StartRequest(mode="review_pending", scope="hotspots")
    settings = configured().model_copy(update={"catalog_review_max_calls": configured_limit})
    key = uuid4().hex
    run, created = await create_run(session, settings, user.id, payload, key)
    assert created and run.request_json["max_calls"] == configured_limit
    assert run.request_hash == fingerprint(
        {**payload.model_dump(mode="json"), "max_calls_source": "configured_default"}
    )
    assert run.request_json["max_calls_source"] == "configured_default"
    original_items = [row.id for row in await run_items(session, run.id)]
    audit = await session.scalar(
        select(AdminAuditLog).where(
            AdminAuditLog.target == f"catalog-review:{run.id}",
            AdminAuditLog.action == "catalog_review_requested",
        )
    )
    assert audit.metadata_json["max_calls"] == configured_limit
    settings.catalog_review_max_calls = 30
    replay, created = await create_run(session, settings, user.id, payload, key)
    assert not created and replay.id == run.id
    assert replay.request_json["max_calls"] == configured_limit
    assert [row.id for row in await run_items(session, run.id)] == original_items
    view = await overview(session, settings, "hotspots")
    assert view["run_call_limit"] == 30
    assert view["runs"][0]["max_calls"] == configured_limit
    assert not view["runs"][0]["can_extend_budget"]  # Queued work is never silently raised.


@pytest.mark.asyncio
async def test_explicit_start_budget_cannot_exceed_runtime_setting_but_lower_cap_is_preserved(
    catalog: tuple[AsyncSession, User],
) -> None:
    session, user = catalog
    settings = configured().model_copy(update={"catalog_review_max_calls": 160})
    with pytest.raises(AppError) as blocked:
        await create_run(
            session,
            settings,
            user.id,
            StartRequest(mode="review_pending", max_calls=161),
            uuid4().hex,
        )
    assert blocked.value.status == 422
    assert blocked.value.code == "validation_error"
    assert not (await session.scalars(select(CatalogReviewRun))).all()
    payload = StartRequest(mode="review_pending", max_calls=120)
    key = uuid4().hex
    run, created = await create_run(session, settings, user.id, payload, key)
    assert created and run.request_json["max_calls"] == 120
    settings.catalog_review_max_calls = 80
    replay, created = await create_run(session, settings, user.id, payload, key)
    assert not created and replay.id == run.id and replay.request_json["max_calls"] == 120
    with pytest.raises(AppError) as conflict:
        await create_run(
            session, settings, user.id, StartRequest(mode="review_pending", max_calls=80), key
        )
    assert conflict.value.code == "idempotency_conflict"


@pytest.mark.asyncio
@pytest.mark.parametrize("first_explicit", [False, True])
async def test_default_and_explicit_80_budget_are_distinct_idempotent_requests(
    catalog: tuple[AsyncSession, User], first_explicit: bool
) -> None:
    session, user = catalog
    omitted = StartRequest(mode="review_pending", scope="hotspots")
    explicit = StartRequest(mode="review_pending", scope="hotspots", max_calls=80)
    original, mixed = (explicit, omitted) if first_explicit else (omitted, explicit)
    settings = configured().model_copy(update={"catalog_review_max_calls": 160})
    key = uuid4().hex
    run, created = await create_run(session, settings, user.id, original, key)
    assert created and run.request_json["max_calls"] == (80 if first_explicit else 160)
    source = "explicit" if first_explicit else "configured_default"
    assert run.request_json["max_calls_source"] == source
    assert run.request_hash == fingerprint(
        {**original.model_dump(mode="json"), "max_calls_source": source}
    )
    with pytest.raises(AppError) as conflict:
        await create_run(session, settings, user.id, mixed, key)
    assert conflict.value.status == 409 and conflict.value.code == "idempotency_conflict"
    settings.catalog_review_max_calls = 120
    replay, created = await create_run(session, settings, user.id, original, key)
    assert not created and replay.id == run.id
    assert replay.request_json["max_calls"] == (80 if first_explicit else 160)


@pytest.mark.asyncio
@pytest.mark.parametrize("scope", ["all", "hotspots", "foods"])
async def test_legacy_scoped_hashes_replay_without_rewriting_the_saved_budget(
    catalog: tuple[AsyncSession, User], scope: CatalogScope
) -> None:
    session, user = catalog
    payload = StartRequest(mode="review_pending", scope=scope)
    legacy = payload.model_dump(mode="json")
    old = CatalogReviewRun(
        id=uuid4(),
        actor_user_id=user.id,
        idempotency_key="scoped-legacy-budget",
        request_hash=fingerprint(legacy),
        request_json=deepcopy(legacy),
        mode="review_pending",
        phase="review_pending",
        status="partial",
        version=4,
        model="fixture",
        result_json={},
        usage_json={"calls": 80},
    )
    session.add(old)
    await session.commit()
    settings = configured().model_copy(update={"catalog_review_max_calls": 160})
    for retry in [payload, StartRequest(mode="review_pending", scope=scope, max_calls=80)]:
        replay, created = await create_run(
            session, settings, user.id, retry, "scoped-legacy-budget"
        )
        assert not created and replay.id == old.id
        assert replay.request_json == legacy and replay.request_hash == fingerprint(legacy)
        assert replay.usage_json == {"calls": 80}


@pytest.mark.asyncio
async def test_explicit_budget_extension_preserves_progress_hash_and_audits_cumulative_calls(
    catalog: tuple[AsyncSession, User],
) -> None:
    session, user = catalog
    payload = StartRequest(mode="review_pending", scope="foods")
    key = uuid4().hex
    run, _ = await create_run(session, configured(), user.id, payload, key)
    rows = await run_items(session, run.id)
    reviewed, failed = rows
    reviewed.status = "assessed"
    reviewed.decision = "needs_review"
    reviewed.assessment_json = {"confidence": 0.5, "reason": "Keep independent review gates"}
    failed.status = "error"
    failed.assessment_json = {"code": "catalog_response_truncated"}
    failed.evidence_json = [{"url": "https://www.wikidata.org/wiki/Q123", "trusted": True}]
    run.status = "partial"
    run.error_code = "catalog_review_call_limit"
    run.usage_json = {
        "calls": 80,
        "input_tokens": 1200,
        "thought_tokens": 240,
        "member_charged": False,
    }
    run.result_json = {"apply_receipts": {"saved": {"updated": 0}}}
    await session.commit()
    original = deepcopy((run.request_hash, run.usage_json, run.result_json))
    snapshots = {row.id: (row.snapshot_hash, deepcopy(row.snapshot_json)) for row in rows}
    reviewed_before = deepcopy((reviewed.status, reviewed.decision, reviewed.assessment_json))
    version = run.version
    settings = configured().model_copy(update={"catalog_review_max_calls": 160})
    view = await overview(session, settings, "foods")
    assert view["runs"][0]["can_extend_budget"] and not view["runs"][0]["can_resume"]
    with pytest.raises(AppError) as bodyless:
        await prepare_resume(session, run.id, user.id, scope="foods", settings=settings)
    assert bodyless.value.code == "catalog_run_not_resumable"
    resumed = await prepare_resume(
        session,
        run.id,
        user.id,
        scope="foods",
        settings=settings,
        payload=ResumeRequest(expected_version=version, max_calls=160),
    )
    assert resumed.id == run.id and run.status == "queued" and run.version == version + 1
    assert run.request_json["max_calls"] == 160
    assert (run.request_hash, run.usage_json, run.result_json) == original
    assert {row.id: (row.snapshot_hash, row.snapshot_json) for row in rows} == snapshots
    assert (reviewed.status, reviewed.decision, reviewed.assessment_json) == reviewed_before
    assert failed.status == "pending" and failed.assessment_json == {}
    assert failed.evidence_json == [{"url": "https://www.wikidata.org/wiki/Q123", "trusted": True}]
    audit = await session.scalar(
        select(AdminAuditLog).where(
            AdminAuditLog.target == f"catalog-review:{run.id}",
            AdminAuditLog.action == "catalog_review_resumed",
        )
    )
    assert audit.metadata_json == {
        "retried_items": 1,
        "legacy_missing_items": 0,
        "stale_items": 0,
        "previous_max_calls": 80,
        "max_calls": 160,
        "calls": 80,
    }
    replay, created = await create_run(session, settings, user.id, payload, key)
    assert not created and replay.id == run.id and replay.request_json["max_calls"] == 160
    with pytest.raises(AppError) as retry:
        await prepare_resume(
            session,
            run.id,
            user.id,
            settings=settings,
            payload=ResumeRequest(expected_version=version, max_calls=160),
        )
    assert retry.value.code == "catalog_version_conflict"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,used_calls,maximum,config_limit,version_delta,expected_code",
    [
        ("partial", 80, 160, 120, 0, "validation_error"),
        ("partial", 80, 80, 160, 0, "catalog_run_not_resumable"),
        ("partial", 120, 100, 160, 0, "catalog_run_not_resumable"),
        ("partial", 80, 160, 160, -1, "catalog_version_conflict"),
        ("queued", 80, 160, 160, 0, "catalog_run_not_resumable"),
        ("running", 80, 160, 160, 0, "catalog_run_not_resumable"),
        ("completed", 80, 160, 160, 0, "catalog_run_not_resumable"),
        ("cancelled", 80, 160, 160, 0, "catalog_run_not_resumable"),
    ],
)
async def test_budget_extension_rejections_do_not_modify_saved_run(
    catalog: tuple[AsyncSession, User],
    status: str,
    used_calls: int,
    maximum: int,
    config_limit: int,
    version_delta: int,
    expected_code: str,
) -> None:
    session, user = catalog
    run = await start(session, user, "hotspots")
    run.status = status
    run.version = 4
    run.usage_json = {"calls": used_calls}
    run.lease_until = datetime.now(UTC) + timedelta(minutes=1)
    await session.commit()
    original = deepcopy((run.request_json, run.usage_json, run.status, run.version))
    settings = configured().model_copy(update={"catalog_review_max_calls": config_limit})
    with pytest.raises(AppError) as blocked:
        await prepare_resume(
            session,
            run.id,
            user.id,
            scope="hotspots",
            settings=settings,
            payload=ResumeRequest(expected_version=run.version + version_delta, max_calls=maximum),
        )
    assert blocked.value.code == expected_code
    assert (run.request_json, run.usage_json, run.status, run.version) == original
    assert not (
        await session.scalars(
            select(AdminAuditLog).where(AdminAuditLog.action == "catalog_review_resumed")
        )
    ).all()


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["running", "queued"])
async def test_expired_lease_with_exhausted_cap_can_explicitly_extend_without_resetting_usage(
    catalog: tuple[AsyncSession, User], status: str
) -> None:
    session, user = catalog
    run = await start(session, user, "hotspots")
    run.status = status
    run.usage_json = {"calls": 80, "input_tokens": 1234, "member_charged": False}
    run.lease_token = "expired-worker"
    run.lease_until = datetime.now(UTC) - timedelta(minutes=1)
    await session.commit()
    original_usage = deepcopy(run.usage_json)
    original_hash = run.request_hash
    settings = configured().model_copy(update={"catalog_review_max_calls": 160})
    view = await run_view(session, run, settings=settings)
    assert view["can_extend_budget"] and not view["can_resume"]
    resumed = await prepare_resume(
        session,
        run.id,
        user.id,
        scope="hotspots",
        settings=settings,
        payload=ResumeRequest(expected_version=run.version, max_calls=160),
    )
    assert resumed.status == "queued" and resumed.request_json["max_calls"] == 160
    assert resumed.usage_json == original_usage and resumed.request_hash == original_hash
    assert resumed.lease_token is None and resumed.lease_until is None


@pytest.mark.asyncio
async def test_budget_extension_preserves_cross_scope_single_active_run_lock(
    catalog: tuple[AsyncSession, User],
) -> None:
    session, user = catalog
    run = await start(session, user, "hotspots")
    run.status = "partial"
    run.usage_json = {"calls": 80}
    await session.commit()
    other = await start(session, user, "foods")
    settings = configured().model_copy(update={"catalog_review_max_calls": 160})
    with pytest.raises(AppError) as blocked:
        await prepare_resume(
            session,
            run.id,
            user.id,
            settings=settings,
            payload=ResumeRequest(expected_version=run.version, max_calls=160),
        )
    assert blocked.value.code == "catalog_run_in_progress"
    assert run.status == "partial" and run.request_json["max_calls"] == 80
    assert run.usage_json == {"calls": 80}
    assert other.status == "queued"


@pytest.mark.asyncio
async def test_bodyless_resume_keeps_previously_approved_cap_when_settings_are_lowered(
    catalog: tuple[AsyncSession, User],
) -> None:
    session, user = catalog
    run = await start(session, user, "hotspots")
    run.status = "partial"
    run.usage_json = {"calls": 40}
    await session.commit()
    settings = configured().model_copy(update={"catalog_review_max_calls": 20})
    resumed = await prepare_resume(session, run.id, user.id, settings=settings)
    assert resumed.status == "queued" and resumed.request_json["max_calls"] == 80
    assert resumed.usage_json == {"calls": 40}


@pytest.mark.asyncio
async def test_scope_mismatch_cannot_read_resume_or_apply_and_legacy_can_resume(
    catalog: tuple[AsyncSession, User],
) -> None:
    session, user = catalog
    run = await start(session, user, "hotspots")
    run.status = "partial"
    await session.commit()
    row = (await run_items(session, run.id))[0]
    apply = ApplyRequest(item_ids=[row.id], action="keep_pending", expected_version=run.version)
    for operation in [
        get_run(session, run.id, scope="foods"),
        prepare_resume(session, run.id, user.id, scope="foods"),
        apply_decisions(session, run.id, user.id, apply, "scope-apply", scope="foods"),
    ]:
        with pytest.raises(AppError) as exc:
            await operation
        assert exc.value.code == "catalog_scope_mismatch"
    assert run.status == "partial"
    # Missing scope remains the historical mixed domain and can still resume.
    run.request_json = {key: value for key, value in run.request_json.items() if key != "scope"}
    await session.commit()
    resumed = await prepare_resume(session, run.id, user.id, scope="all")
    assert resumed.status == "queued"


@pytest.mark.asyncio
async def test_scope_guards_items_resume_worker_and_apply_even_for_foreign_kind_injected_into_run(
    catalog: tuple[AsyncSession, User], monkeypatch: pytest.MonkeyPatch
) -> None:
    session, user = catalog
    run = await start(session, user, "hotspots")
    merchant = await session.scalar(select(FoodMerchant))
    foreign = CatalogReviewItem(
        id=uuid4(),
        run_id=run.id,
        kind="merchant",
        entity_id=merchant.id,
        name="Foreign row",
        phase="review_pending",
        status="error",
        snapshot_hash="x" * 64,
        snapshot_json={},
        assessment_json={},
        gaps_json=[],
        evidence_json=[],
    )
    session.add(foreign)
    run.status = "partial"
    await session.commit()
    assert (await run_view(session, run))["counts"]["total"] == 1
    await prepare_resume(session, run.id, user.id, scope="hotspots")
    assert foreign.status == "error"
    run.status = "completed"
    await session.commit()
    with pytest.raises(AppError) as exc:
        await apply_decisions(
            session,
            run.id,
            user.id,
            ApplyRequest(
                item_ids=[foreign.id], action="keep_pending", expected_version=run.version
            ),
            "injected-item",
            scope="hotspots",
        )
    assert exc.value.code == "catalog_item_mismatch"
    run.status = "running"
    run.lease_token = "scope-lease"
    run.lease_until = datetime.now(UTC) + timedelta(minutes=10)
    await session.commit()
    monkeypatch.setattr(jobs, "SessionFactory", session.info["factory"])
    monkeypatch.setattr(jobs, "fetch_sources", AsyncMock(return_value=[]))
    provider = AsyncMock()
    provider.usage = {}

    async def assess(candidates: list[Any]) -> AssessmentBatch:
        assert {candidate.kind for candidate in candidates} == {"hotspot"}
        return AssessmentBatch(
            items=[
                ReviewAssessment(
                    candidate_id=candidate.candidate_id,
                    decision="needs_review",
                    confidence=0.5,
                    reason="Fixture only",
                    evidence=[],
                )
                for candidate in candidates
            ]
        )

    provider.assess.side_effect = assess
    await jobs._review_items(run.id, "scope-lease", "review_pending", provider, set(), {})
    assert provider.assess.await_count == 1
    await session.refresh(foreign)
    assert foreign.status == "error"


@pytest.mark.asyncio
@pytest.mark.parametrize("scope", ["hotspots", "foods"])
async def test_discovery_worker_only_calls_allowed_kinds(
    catalog: tuple[AsyncSession, User], scope: CatalogScope, monkeypatch: pytest.MonkeyPatch
) -> None:
    session, user = catalog
    run = await start(session, user, scope)
    run.mode = "discover_new"
    run.status = "running"
    run.lease_token = "scope-lease"
    run.lease_until = datetime.now(UTC) + timedelta(minutes=10)
    await session.commit()
    monkeypatch.setattr(jobs, "SessionFactory", session.info["factory"])
    monkeypatch.setattr(jobs, "_discovery_context", AsyncMock(return_value=([], [])))
    provider = AsyncMock()
    provider.usage = {}
    provider.discovery_diagnostics = {}
    provider.discover.return_value = DiscoveryBatch(items=[])
    await jobs._discover_items(run.id, "scope-lease", provider, {})
    assert {call.args[0] for call in provider.discover.await_args_list} == set(SCOPE_KINDS[scope])
    assert provider.discover.await_count == 3 * len(SCOPE_KINDS[scope])


@pytest.mark.asyncio
async def test_http_scope_boundaries_and_foreign_item_pagination(
    catalog: tuple[AsyncSession, User], monkeypatch: pytest.MonkeyPatch
) -> None:
    import app.catalog_review.router as routes

    session, user = catalog
    run = await start(session, user, "foods")
    app = FastAPI()
    app.include_router(router)
    app.add_exception_handler(AppError, app_error_handler)
    app.dependency_overrides[current_user] = lambda: user

    async def database() -> AsyncIterator[AsyncSession]:
        yield session

    app.dependency_overrides[get_session] = database
    monkeypatch.setattr(routes, "load_runtime_settings", AsyncMock(return_value=configured()))
    monkeypatch.setattr(routes, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(routes, "enqueue_saved_run", AsyncMock())
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        result = await client.get("/admin/catalog-review?scope=foods")
        assert result.status_code == 200 and result.json()["pending_counts"]["total"] == 2
        result = await client.get(
            f"/admin/catalog-review/runs/{run.id}/items?scope=foods&page_size=1"
        )
        assert result.status_code == 200
        assert result.json()["total"] == 2 and result.json()["has_more"]
        for suffix in ["", "/items"]:
            result = await client.get(f"/admin/catalog-review/runs/{run.id}{suffix}?scope=hotspots")
            assert result.status_code == 409 and result.json()["code"] == "catalog_scope_mismatch"
        assert (await client.get("/admin/catalog-review?scope=hotels")).status_code == 422
        result = await client.post(f"/admin/catalog-review/runs/{run.id}/resume?scope=hotspots")
        assert result.status_code == 409
        assert not routes.enqueue_saved_run.called


@pytest.mark.asyncio
async def test_http_budget_extension_is_explicit_scoped_versioned_and_admin_only(
    catalog: tuple[AsyncSession, User], monkeypatch: pytest.MonkeyPatch
) -> None:
    import app.catalog_review.router as routes

    session, user = catalog
    run = await start(session, user, "hotspots")
    run.status = "partial"
    run.version = 4
    run.usage_json = {"calls": 80, "member_charged": False}
    await session.commit()
    settings = configured().model_copy(update={"catalog_review_max_calls": 160})
    app = FastAPI()
    app.include_router(router)
    app.add_exception_handler(AppError, app_error_handler)
    app.dependency_overrides[current_user] = lambda: user

    async def database() -> AsyncIterator[AsyncSession]:
        yield session

    app.dependency_overrides[get_session] = database
    monkeypatch.setattr(routes, "load_runtime_settings", AsyncMock(return_value=settings))
    monkeypatch.setattr(routes, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(routes, "enqueue_saved_run", AsyncMock())
    url = f"/admin/catalog-review/runs/{run.id}/resume?scope=hotspots"
    body = {"expected_version": 4, "max_calls": 160}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        overview_response = await client.get("/admin/catalog-review?scope=hotspots")
        assert overview_response.json()["run_call_limit"] == 160
        view = await client.get(f"/admin/catalog-review/runs/{run.id}?scope=hotspots")
        assert view.json()["max_calls"] == 80 and view.json()["can_extend_budget"]
        user.is_admin = False
        forbidden = await client.post(url, json=body)
        assert forbidden.status_code == 403
        user.is_admin = True
        for invalid in [
            {**body, "max_calls": True},
            {**body, "max_calls": 1001},
            {**body, "expected_version": "4"},
            {**body, "calls": 0},
        ]:
            assert (await client.post(url, json=invalid)).status_code == 422
        foreign = await client.post(url.replace("hotspots", "foods"), json=body)
        assert foreign.status_code == 409 and foreign.json()["code"] == "catalog_scope_mismatch"
        bodyless = await client.post(url)
        assert bodyless.status_code == 409
        assert bodyless.json()["code"] == "catalog_run_not_resumable"
        routes.enqueue_saved_run.assert_not_awaited()
        assert run.usage_json["calls"] == 80 and run.request_json["max_calls"] == 80
        response = await client.post(url, json=body)
        assert response.status_code == 202
        assert response.json()["max_calls"] == 160
        assert response.json()["usage"]["calls"] == 80
        assert response.json()["status"] == "queued" and response.json()["version"] == 5
        assert not response.json()["can_extend_budget"]
        routes.enqueue_saved_run.assert_awaited_once_with(session, run)
        duplicate = await client.post(url, json=body)
        assert duplicate.status_code == 409
        assert duplicate.json()["code"] == "catalog_version_conflict"
        assert routes.enqueue_saved_run.await_count == 1
