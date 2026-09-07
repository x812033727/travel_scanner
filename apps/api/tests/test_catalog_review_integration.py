"""PostgreSQL catalog workflow tests; no Gemini, map, source or queue network calls.

Every test runs inside a rolled-back outer transaction. Service commits release nested
savepoints, so they exercise actual database behavior without leaking fixtures into the
other catalog integration modules or overwriting their seed decisions.
"""

from __future__ import annotations

import hashlib
import os
from collections.abc import AsyncIterator
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any, cast
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.auth.service import current_user
from app.catalog_review import jobs
from app.catalog_review.repository import (
    ENTITY_TYPES,
    duplicate_draft,
    entity_snapshot,
    import_draft,
    publication_gaps,
    row_data,
    source_urls,
    trusted_hosts,
)
from app.catalog_review.router import router
from app.catalog_review.schemas import (
    DiscoveryDraft,
    EvidenceCitation,
    EvidenceSource,
    ReviewAssessment,
)
from app.catalog_review.service import (
    ApplyRequest,
    StartRequest,
    apply_decisions,
    create_run,
    record_assessment,
    run_items,
    run_view,
)
from app.config import Settings
from app.db import engine, get_session
from app.foods import service as food_service
from app.foods.catalog import FOOD_SEEDS
from app.i18n import LOCALES
from app.models import (
    AdminAuditLog,
    CatalogReviewItem,
    CatalogReviewRun,
    FoodDestination,
    FoodLocalization,
    FoodMerchant,
    FoodMerchantSource,
    HotspotLocalization,
    TravelFood,
    TravelHotspot,
    User,
)
from app.problems import AppError, app_error_handler

pytestmark = [
    pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"),
    pytest.mark.asyncio(loop_scope="module"),
]
SOURCE = "https://www.japan.travel/en/spot/fixture/"
EXCERPT = "This independently checked official source identifies the exact test museum."


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


@pytest_asyncio.fixture(loop_scope="module")
async def session() -> AsyncIterator[AsyncSession]:
    async with engine.connect() as connection:
        transaction = await connection.begin()
        try:
            async with AsyncSession(
                bind=connection, expire_on_commit=False, join_transaction_mode="create_savepoint"
            ) as database:
                # Another module's historical run must not make this isolated test busy.
                # The outer rollback restores every prior value.
                await database.execute(update(CatalogReviewRun).values(status="completed"))
                await database.commit()
                yield database
        finally:
            await transaction.rollback()


@pytest_asyncio.fixture(loop_scope="module")
async def actor(session: AsyncSession) -> User:
    user = User(
        id=uuid4(),
        email=f"catalog-review-{uuid4()}@example.test",
        password_hash="unused-integration-fixture",
        is_admin=True,
        is_active=True,
    )
    session.add(user)
    await session.flush()
    return user


def configured() -> Settings:
    return Settings(_env_file=None, hotspot_guide_gemini_api_key="not-a-live-key")


def hotspot(*, verified: bool = False, **changes: Any) -> TravelHotspot:
    unique = uuid4().hex
    now = datetime.now(UTC)
    fields: dict[str, Any] = {
        "id": uuid4(),
        "slug": f"catalog-test-{unique}",
        "name": f"Museum {unique}",
        "city_code": "TYO",
        "city_name": "東京",
        "destination_id": "tokyo",
        "country_code": "JP",
        "country_name": "日本",
        "category": "culture",
        "search_text": f"Museum {unique}",
        "source_urls": [SOURCE],
        "review_status": "pending",
        "is_active": False,
        "map_match_status": "verified" if verified else "unverified",
        "metadata_json": {"local_name": f"資料館{unique}"},
    }
    if verified:
        fields.update(
            google_place_id=f"ChIJfixture{unique}",
            map_verified_at=now,
            wikidata_item_id=f"Q{int(unique[:12], 16)}",
            latitude=Decimal("35.710100"),
            longitude=Decimal("139.810700"),
            coordinate_source_type="official_tourism",
            coordinate_source_url=SOURCE,
            coordinate_verified_at=now,
        )
    return TravelHotspot(**(fields | changes))


def food(**changes: Any) -> TravelFood:
    unique = uuid4().hex
    return TravelFood(
        **(
            {
                "id": uuid4(),
                "slug": f"catalog-food-{unique}",
                "local_name": f"料理{unique}",
                "romanized_name": f"Dish {unique}",
                "country_code": "JP",
                "food_kind": "main",
                "meal_types": ["lunch", "dinner"],
                "search_text": f"Dish {unique}",
                "source_urls": [SOURCE],
                "review_status": "pending",
                "is_active": False,
                "source": "admin",
            }
            | changes
        )
    )


def merchant(**changes: Any) -> FoodMerchant:
    unique = uuid4().hex
    return FoodMerchant(
        **(
            {
                "id": uuid4(),
                "slug": f"catalog-merchant-{unique}",
                "name": f"Branch {unique}",
                "local_name": f"本店{unique}",
                "destination_id": "tokyo",
                "country_code": "JP",
                "review_status": "pending",
                "is_active": False,
                "map_match_status": "unverified",
            }
            | changes
        )
    )


async def new_run(session: AsyncSession, actor: User, **changes: Any) -> CatalogReviewRun:
    run, created = await create_run(
        session, configured(), actor.id, StartRequest(mode="review_pending", **changes), uuid4().hex
    )
    assert created
    return run


async def ready_run(
    session: AsyncSession,
    actor: User,
    row: TravelHotspot,
) -> tuple[CatalogReviewRun, CatalogReviewItem]:
    session.add(row)
    await session.flush()
    run = await new_run(session, actor)
    items = await run_items(session, run.id)
    item = next(entry for entry in items if entry.entity_id == row.id)
    source = EvidenceSource(
        url=SOURCE,
        text=EXCERPT,
        trusted=True,
        fetched=True,
        fingerprint=hashlib.sha256(EXCERPT.encode()).hexdigest(),
    )
    record_assessment(
        item,
        ReviewAssessment(
            candidate_id=str(item.id),
            decision="approve",
            confidence=0.99,
            reason="官方來源與既有獨立地圖驗證一致。",
            evidence=[EvidenceCitation(url=SOURCE, quote="identifies the exact test museum")],
        ),
        [source],
    )
    run.status = "completed"
    run.version += 1
    await session.commit()
    return run, item


async def audit_count(session: AsyncSession, target: str, action: str) -> int:
    return int(
        await session.scalar(
            select(func.count())
            .select_from(AdminAuditLog)
            .where(
                AdminAuditLog.target == target,
                AdminAuditLog.action == action,
            )
        )
        or 0
    )


async def test_create_snapshots_all_pending_types_and_idempotency_conflict(
    session: AsyncSession,
    actor: User,
) -> None:
    rows: list[TravelHotspot | TravelFood | FoodMerchant] = [hotspot(), food(), merchant()]
    ignored: list[TravelHotspot | TravelFood | FoodMerchant] = [
        hotspot(review_status="approved"),
        food(review_status="rejected"),
        merchant(review_status="disabled"),
    ]
    session.add_all([*rows, *ignored])
    await session.flush()
    expected = {
        (kind, row_id)
        for kind, model in ENTITY_TYPES.items()
        for row_id in (
            await session.scalars(
                select(model.id).where(
                    model.review_status == "pending",
                )
            )
        ).all()
    }
    payload = StartRequest(mode="review_pending")
    key = uuid4().hex
    run, created = await create_run(session, configured(), actor.id, payload, key)
    assert created
    items = await run_items(session, run.id)
    assert {(item.kind, item.entity_id) for item in items} == expected
    assert {row.id for row in rows} <= {item.entity_id for item in items}
    assert not {row.id for row in ignored} & {item.entity_id for item in items}
    assert all(item.status == "pending" and item.snapshot_hash for item in items)
    assert run.usage_json["calls"] == 0
    replay, created = await create_run(session, configured(), actor.id, payload, key)
    assert not created and replay.id == run.id
    assert len(await run_items(session, run.id)) == len(items)
    assert await audit_count(session, f"catalog-review:{run.id}", "catalog_review_requested") == 1
    with pytest.raises(AppError) as exc:
        await create_run(
            session, configured(), actor.id, StartRequest(mode="review_pending", max_calls=5), key
        )
    assert exc.value.status == 409 and exc.value.code == "idempotency_conflict"


async def test_discovery_requires_completed_pending_snapshot(
    session: AsyncSession,
    actor: User,
) -> None:
    with pytest.raises(AppError) as missing:
        await create_run(
            session, configured(), actor.id, StartRequest(mode="discover_new"), uuid4().hex
        )
    assert missing.value.code == "catalog_review_required"
    session.add(hotspot())
    await session.flush()
    prior = await new_run(session, actor)
    prior.status = "partial"
    await session.commit()
    discover = StartRequest(mode="discover_new", prior_review_run_id=prior.id)
    with pytest.raises(AppError) as incomplete:
        await create_run(session, configured(), actor.id, discover, uuid4().hex)
    assert incomplete.value.code == "catalog_review_incomplete"
    for item in await run_items(session, prior.id):
        item.status = "assessed"
        item.decision = "needs_review"
    prior.status = "completed"
    await session.commit()
    assert (await run_view(session, prior))["review_complete"]
    run, created = await create_run(session, configured(), actor.id, discover, uuid4().hex)
    assert created and run.mode == "discover_new"
    assert await run_items(session, run.id) == []


async def test_imported_dish_has_five_locales_and_all_new_pois_remain_pending_inactive(
    session: AsyncSession,
    actor: User,
) -> None:
    run = await new_run(session, actor)
    unique = uuid4().hex
    dish = DiscoveryDraft(
        kind="food",
        name=f"New Dish {unique}",
        local_name=f"新料理{unique}",
        destination_id="tokyo",
        slug=f"new-dish-{unique}",
        source_urls=[SOURCE],
        data={
            "romanized_name": f"New Dish {unique}",
            "food_kind": "main",
            "meal_types": ["lunch", "dinner"],
            "ingredient_tags": ["rice"],
            "dietary_notes": [],
            "localizations": [
                {
                    "locale": locale,
                    "name": f"Dish {locale} {unique}",
                    "summary": f"Original test summary ({locale})",
                }
                for locale in LOCALES
            ],
        },
    )
    imported = await import_draft(session, dish, actor.id, run.id)
    assert isinstance(imported, TravelFood)
    await session.commit()
    assert imported.review_status == "pending" and not imported.is_active
    assert imported.source == "admin"
    localizations = (
        await session.scalars(
            select(FoodLocalization).where(
                FoodLocalization.food_id == imported.id,
            )
        )
    ).all()
    assert {entry.locale for entry in localizations} == set(LOCALES)
    assert all(entry.name and entry.summary and entry.source == "admin" for entry in localizations)
    assert (
        await session.scalar(
            select(FoodDestination.destination_id).where(
                FoodDestination.food_id == imported.id,
            )
        )
        == "tokyo"
    )
    assert await import_draft(session, dish, actor.id, run.id) is None
    for kind in ("hotspot", "merchant"):
        poi = DiscoveryDraft(
            kind=kind,
            name=f"New {kind} {unique}",
            local_name=f"新{kind}{unique}",
            destination_id="tokyo",
            slug=f"new-{kind}-{unique}",
            source_urls=[SOURCE],
            data={
                "category": "culture",
                "latitude": 35.7,
                "longitude": 139.8,
                "google_place_id": "untrusted-generated-id",
                "map_match_status": "verified",
            },
        )
        created_poi = await import_draft(session, poi, actor.id, run.id)
        assert isinstance(created_poi, (TravelHotspot, FoodMerchant))
        await session.flush()
        assert created_poi.review_status == "pending" and not created_poi.is_active
        assert created_poi.map_match_status == "unverified"
        assert created_poi.google_place_id is None
        assert created_poi.latitude is None and created_poi.longitude is None
        assert publication_gaps(kind, await entity_snapshot(session, created_poi))
    assert await audit_count(session, f"food:{imported.id}", "catalog_candidate_imported") == 1


async def test_rejected_tombstones_block_new_slugs_local_names_and_localized_aliases(
    session: AsyncSession,
    actor: User,
) -> None:
    unique = uuid4().hex
    spot = hotspot(
        review_status="rejected",
        name=f"Rejected landmark {unique}",
        metadata_json={"local_name": f"既有地點{unique}"},
    )
    dish = food(review_status="rejected")
    branch = merchant(review_status="rejected")
    session.add_all([spot, dish, branch])
    await session.flush()
    alias = f"Existing translated alias {unique}"
    session.add(
        HotspotLocalization(
            hotspot_id=spot.id,
            locale="en",
            name=alias,
            aliases=[f"Alias {unique}"],
            search_terms=[],
        )
    )
    session.add(
        FoodLocalization(
            food_id=dish.id,
            locale="en",
            name=alias,
            summary="Existing rejected item",
            source="admin",
        )
    )
    await session.flush()
    pairs = [
        ("hotspot", f"既有地點{unique}"),
        ("hotspot", alias),
        ("hotspot", f"Alias {unique}"),
        ("food", alias),
        ("merchant", branch.local_name),
    ]
    for kind, local_name in pairs:
        proposal = DiscoveryDraft(
            kind=kind,
            name=f"Different name {uuid4().hex}",
            local_name=local_name,
            destination_id="tokyo",
            slug=f"different-{uuid4().hex}",
            source_urls=[SOURCE],
        )
        assert await duplicate_draft(session, proposal)


async def test_approved_verified_snapshot_applies_once_and_audits_without_saving_source_body(
    session: AsyncSession,
    actor: User,
) -> None:
    row = hotspot(verified=True)
    run, item = await ready_run(session, actor, row)
    assert item.decision == "approve" and item.gaps_json == []
    assert all("text" not in entry for entry in item.evidence_json)
    assert item.evidence_json[0]["fingerprint"]
    payload = ApplyRequest(item_ids=[item.id], action="approve", expected_version=run.version)
    key = uuid4().hex
    outcome = await apply_decisions(session, run.id, actor.id, payload, key)
    assert outcome["updated"] == 1
    await session.refresh(row)
    assert row.review_status == "approved" and row.is_active
    assert row.reviewed_by_user_id == actor.id
    assert row.google_place_id and row.coordinate_source_url == SOURCE
    target = f"hotspot:{row.id}"
    assert await audit_count(session, target, "catalog_review_applied") == 1
    previous_version = run.version
    replay = await apply_decisions(session, run.id, actor.id, payload, key)
    assert replay["outcomes"] == outcome["outcomes"]
    assert run.version == previous_version
    assert await audit_count(session, target, "catalog_review_applied") == 1
    with pytest.raises(AppError) as conflict:
        await apply_decisions(
            session,
            run.id,
            actor.id,
            ApplyRequest(
                item_ids=[item.id],
                action="keep_pending",
                expected_version=payload.expected_version,
            ),
            key,
        )
    assert conflict.value.code == "idempotency_conflict"


async def test_missing_map_cannot_be_approved_even_when_gemini_recommends_it(
    session: AsyncSession,
    actor: User,
) -> None:
    row = hotspot()
    run, item = await ready_run(session, actor, row)
    assert item.decision == "needs_review"
    assert "missing_exact_map_identity" in item.gaps_json
    result = await apply_decisions(
        session,
        run.id,
        actor.id,
        ApplyRequest(
            item_ids=[item.id],
            action="approve",
            expected_version=run.version,
        ),
        uuid4().hex,
    )
    assert result["updated"] == 0
    assert result["outcomes"][0]["reason"] == "action_not_allowed"
    await session.refresh(row)
    assert row.review_status == "pending" and not row.is_active
    assert await audit_count(session, f"hotspot:{row.id}", "catalog_review_applied") == 0


async def test_stale_run_version_and_changed_entity_never_overwrite_admin_edits(
    session: AsyncSession,
    actor: User,
) -> None:
    row = hotspot(verified=True)
    run, item = await ready_run(session, actor, row)
    with pytest.raises(AppError) as version:
        await apply_decisions(
            session,
            run.id,
            actor.id,
            ApplyRequest(
                item_ids=[item.id],
                action="approve",
                expected_version=run.version - 1,
            ),
            uuid4().hex,
        )
    assert version.value.code == "catalog_version_conflict"
    row.name = f"Administrator corrected {uuid4().hex}"
    await session.commit()
    edited_name = row.name
    result = await apply_decisions(
        session,
        run.id,
        actor.id,
        ApplyRequest(
            item_ids=[item.id],
            action="approve",
            expected_version=run.version,
        ),
        uuid4().hex,
    )
    assert result["updated"] == 0
    assert result["outcomes"][0]["reason"] == "candidate_changed"
    await session.refresh(row)
    assert row.name == edited_name and row.review_status == "pending" and not row.is_active


async def test_expired_assessment_and_wrong_run_item_are_rejected(
    session: AsyncSession,
    actor: User,
) -> None:
    run, item = await ready_run(session, actor, hotspot(verified=True))
    item.assessed_at = datetime.now(UTC) - timedelta(days=8)
    await session.commit()
    expired = await apply_decisions(
        session,
        run.id,
        actor.id,
        ApplyRequest(
            item_ids=[item.id],
            action="approve",
            expected_version=run.version,
        ),
        uuid4().hex,
    )
    assert expired["updated"] == 0 and expired["outcomes"][0]["reason"] == "assessment_expired"
    with pytest.raises(AppError) as wrong_item:
        await apply_decisions(
            session,
            run.id,
            actor.id,
            ApplyRequest(
                item_ids=[uuid4()],
                action="approve",
                expected_version=run.version,
            ),
            uuid4().hex,
        )
    assert wrong_item.value.code == "catalog_item_mismatch"


async def test_pending_official_website_cannot_extend_source_trust(
    session: AsyncSession,
    actor: User,
) -> None:
    hostname = f"merchant-{uuid4().hex}.example"
    row = merchant(
        official_website_url=f"https://{hostname}/",
        official_website_verified_at=datetime.now(UTC),
        map_match_status="verified",
    )
    session.add(row)
    await session.flush()
    assert hostname not in await trusted_hosts(session)
    row.review_status = "approved"
    row.is_active = True
    await session.flush()
    assert hostname in await trusted_hosts(session)


async def test_lease_and_per_run_budget_fail_closed_before_external_provider(
    session: AsyncSession,
    actor: User,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run = await new_run(session, actor, max_calls=1)
    connection = cast(AsyncConnection, session.bind)
    monkeypatch.setattr(
        jobs,
        "SessionFactory",
        lambda: AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        ),
    )
    consume = AsyncMock(return_value=True)
    monkeypatch.setattr(jobs, "consume_search_budget", consume)
    monkeypatch.setattr(jobs, "get_redis", lambda: object())
    claimed = await jobs._claim_run(run.id)
    assert claimed is not None and claimed.lease_token
    assert await jobs._claim_run(run.id) is None
    with pytest.raises(jobs.LeaseLost):
        await jobs.reserve_call(run.id, "another-worker-token", configured())
    assert consume.await_count == 0
    assert await jobs.reserve_call(run.id, claimed.lease_token, configured())
    with pytest.raises(jobs.BudgetStopped):
        await jobs.reserve_call(run.id, claimed.lease_token, configured())
    assert consume.await_count == 1
    await session.refresh(run)
    assert run.usage_json["calls"] == 1 and run.usage_json["member_charged"] is False


async def test_admin_http_auth_gates_do_not_enqueue_or_call_gemini(
    session: AsyncSession,
    actor: User,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    application = FastAPI()
    application.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    application.include_router(router, prefix="/api/v1")
    enqueue = AsyncMock()
    monkeypatch.setattr("app.catalog_review.router.enqueue_saved_run", enqueue)

    async def database() -> AsyncIterator[AsyncSession]:
        yield session

    application.dependency_overrides[get_session] = database
    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        anonymous = await client.get("/api/v1/admin/catalog-review")
        assert anonymous.status_code == 401
        assert anonymous.json()["code"] == "authentication_required"
        member = User(
            id=uuid4(),
            email=f"catalog-member-{uuid4()}@example.test",
            password_hash="unused",
            is_admin=False,
            is_active=True,
        )
        session.add(member)
        await session.flush()

        async def authenticated_member() -> User:
            return member

        application.dependency_overrides[current_user] = authenticated_member
        denied = await client.get("/api/v1/admin/catalog-review")
        assert denied.status_code == 403 and denied.json()["code"] == "admin_required"
    assert enqueue.await_count == 0


async def test_merchant_discovery_reference_does_not_claim_branch_verification(
    session: AsyncSession,
    actor: User,
) -> None:
    run = await new_run(session, actor)
    unique = uuid4().hex
    row = await import_draft(
        session,
        DiscoveryDraft(
            kind="merchant",
            name=f"New Branch {unique}",
            local_name=f"新分店{unique}",
            destination_id="tokyo",
            slug=f"new-branch-{unique}",
            source_urls=[SOURCE],
        ),
        actor.id,
        run.id,
    )
    assert isinstance(row, FoodMerchant)
    sources = (
        await session.scalars(
            select(FoodMerchantSource).where(
                FoodMerchantSource.merchant_id == row.id,
            )
        )
    ).all()
    assert sources == []
    snapshot = await entity_snapshot(session, row)
    assert snapshot["discovery_reference_urls"] == [SOURCE]
    assert source_urls(snapshot) == [SOURCE]
    assert row.verified_at is None and row.coordinate_verified_at is None
    assert "missing_direct_merchant_source" in publication_gaps("merchant", snapshot)


async def test_reviewed_seed_dish_and_all_reviewed_localizations_survive_reseed(
    session: AsyncSession,
    actor: User,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    row = food(source="seed")
    session.add(row)
    await session.flush()
    localizations = [
        FoodLocalization(
            food_id=row.id,
            locale=locale,
            name=f"Reviewed {locale} {row.local_name}",
            summary=f"Reviewed original explanation {locale}",
            source="seed",
        )
        for locale in LOCALES
    ]
    session.add_all(localizations)
    session.add(FoodDestination(food_id=row.id, destination_id="tokyo"))
    await session.flush()
    run = await new_run(session, actor)
    item = next(entry for entry in await run_items(session, run.id) if entry.entity_id == row.id)
    text = f"Official culinary source describes {row.local_name} and its original ingredients."
    record_assessment(
        item,
        ReviewAssessment(
            candidate_id=str(item.id),
            decision="approve",
            confidence=0.99,
            reason="官方資料支持料理及五語說明。",
            evidence=[EvidenceCitation(url=SOURCE, quote="and its original ingredients")],
        ),
        [
            EvidenceSource(
                url=SOURCE,
                text=text,
                fetched=True,
                trusted=True,
                fingerprint=hashlib.sha256(text.encode()).hexdigest(),
            )
        ],
    )
    assert item.decision == "approve" and item.gaps_json == []
    run.status = "completed"
    run.version += 1
    await session.commit()
    result = await apply_decisions(
        session,
        run.id,
        actor.id,
        ApplyRequest(
            item_ids=[item.id],
            action="approve",
            expected_version=run.version,
        ),
        uuid4().hex,
    )
    assert result["updated"] == 1
    await session.refresh(row)
    for localization in localizations:
        await session.refresh(localization)
    assert row.source == "admin" and all(entry.source == "admin" for entry in localizations)
    before = row_data(row), [row_data(entry) for entry in localizations]
    changed_seed = replace(
        FOOD_SEEDS[0],
        slug=row.slug,
        local_name="Later seed local name",
        romanized_name="Later seed English name",
        name="後來種子繁中名稱",
        simplified_name="后来种子简中名称",
        description="A later, unreviewed seed description",
        destination_ids=("tokyo",),
    )
    monkeypatch.setattr(food_service, "FOOD_SEEDS", (changed_seed,))
    monkeypatch.setattr(food_service, "MERCHANT_SEEDS", ())
    monkeypatch.setattr(food_service, "MERCHANT_DIRECT_SOURCE_SEEDS", ())
    monkeypatch.setattr(food_service, "CATEGORY_SEEDS", ())
    monkeypatch.setattr(food_service, "ALL_AREA_SEEDS", ())
    for _ in range(2):
        assert await food_service.seed_food_catalog(session) == 1
        await session.commit()
    await session.refresh(row)
    for localization in localizations:
        await session.refresh(localization)
    assert (row_data(row), [row_data(entry) for entry in localizations]) == before
    assert row.review_status == "approved" and row.is_active
    assert await audit_count(session, f"food:{row.id}", "catalog_review_applied") == 1
