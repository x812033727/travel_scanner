"""Scope boundaries use real SQL locally and PostgreSQL in integration CI."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
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
