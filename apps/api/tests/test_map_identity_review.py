import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from decimal import Decimal
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import fakeredis.aioredis
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.config import Settings
from app.db import get_session
from app.locations import map_identity_review as review_module
from app.locations import map_identity_router as router_module
from app.locations import map_identity_tasks as tasks_module
from app.locations.map_identity import (
    catalog_google_place_id,
    catalog_map_identities,
    identity_metadata,
    set_identity_metadata,
)
from app.locations.map_identity_review import (
    CatalogReference,
    IdentityReviewRequest,
    candidate_snapshot,
    canonical_values,
    collect_candidates,
    comparison_key,
    review_identity,
    snapshot_key,
)
from app.locations.map_identity_router import IdentityBatchRequest, list_identities
from app.locations.map_identity_tasks import batch_key
from app.models import AdminAuditLog, Base, FoodMerchant, TravelHotspot, TravelServiceProduct, User
from app.problems import AppError, app_error_handler
from app.travel_services.imports import upsert_product
from app.travel_services.schemas import Facts, ProductInput


@pytest_asyncio.fixture
async def database() -> AsyncIterator[tuple[AsyncSession, User]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with async_sessionmaker(engine, expire_on_commit=False)() as session:
        user = User(id=uuid4(), email="identity-admin@example.test")
        user.__dict__["_admin_roles_cache"] = frozenset({"content"})
        session.add(user)
        await session.commit()
        yield session, user
    await engine.dispose()


async def add_place(session, kind="merchant", **changes):
    shared = dict(
        id=uuid4(),
        destination_id="seoul",
        latitude=Decimal("37.570000"),
        longitude=Decimal("126.980000"),
        google_place_id=None,
        naver_map_url="https://map.naver.com/p/entry/place/" + str(uuid4().int),
        map_match_status="verified",
        coordinate_source_type="merchant_official",
        coordinate_source_url="https://editorial.example/location",
        review_status="approved",
        is_active=True,
    )
    if kind == "hotel":
        row = TravelServiceProduct(
            id=shared["id"],
            kind="hotel",
            destination_id="seoul",
            source_key=uuid4().hex,
            title="서울호텔",
            names_json={"ko": "서울호텔"},
            status="approved",
            version=1,
            source_url="https://editorial.example/hotel",
            facts={
                "google_place_id": None,
                "naver_map_url": shared["naver_map_url"],
                "latitude": 37.57,
                "longitude": 126.98,
                "coordinate_source_url": shared["coordinate_source_url"],
                "map_verified": True,
            },
        )
    elif kind == "hotspot":
        row = TravelHotspot(
            **{
                **shared,
                "country_code": "KR",
                "country_name": "韓國",
                "name": "서울공원",
                "slug": uuid4().hex,
                "city_code": "ICN",
                "city_name": "首爾",
                "category": "park",
                "search_text": "서울공원",
                "metadata_json": {"local_name": "서울공원"},
                **changes,
            }
        )
    else:
        row = FoodMerchant(
            **{
                **shared,
                "country_code": "KR",
                "name": "서울식당",
                "local_name": "서울식당",
                "slug": uuid4().hex,
                "address": "서울 종로구 1",
                "map_identity_metadata": {},
                **changes,
            }
        )
    session.add(row)
    await session.commit()
    return row


@pytest.fixture
def providers(monkeypatch):
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    service = AsyncMock()
    service.configured = True
    service.search_place_candidates.return_value = [
        {
            "place_id": "ChIJcandidate",
            "name": "GOOGLE_TEMP_NAME",
            "address": "GOOGLE_TEMP_ADDRESS",
            "country_code": "KR",
            "latitude": 37.571234,
            "longitude": 126.981234,
            "google_maps_url": "https://www.google.com/maps/place/?q=place_id:ChIJcandidate",
        }
    ]
    monkeypatch.setattr(review_module, "automatic_refresh_allowed", AsyncMock(return_value=True))
    monkeypatch.setattr(review_module, "GoogleTravelService", lambda *args, **kwargs: service)
    return redis, service


async def snapshot_for(session, redis, row, user, kind="merchant"):
    return await candidate_snapshot(
        session,
        redis,
        Settings(google_maps_api_key="test-key"),
        CatalogReference(kind=kind, id=row.id),
        user.id,
    )


def decision(snapshot, **changes):
    return IdentityReviewRequest(
        **{
            "action": "confirm",
            "expected_revision": snapshot["item"]["revision"],
            "expected_fingerprint": snapshot["item"]["canonical_fingerprint"],
            "snapshot_id": snapshot["snapshot_id"],
            "place_id": "ChIJcandidate",
            "note": "Compared Korean branch name and full address with the canonical NAVER place.",
            **changes,
        }
    )


@pytest.mark.parametrize("kind", ["merchant", "hotspot", "hotel"])
async def test_candidates_are_transient_and_confirm_only_adds_identity(database, providers, kind):
    session, user = database
    redis, _ = providers
    row = await add_place(session, kind)
    before = canonical_values(row)
    naver_review = {
        "provider": "naver_maps",
        "map_url": before["naver_map_url"],
        "status": "verified",
        "verified_at": "2026-08-01T00:00:00Z",
        "verified_by_user_id": str(user.id),
        "evidence_url": "https://editorial.example/naver-review",
    }
    set_identity_metadata(
        row, {**identity_metadata(row), "map_identities": {"naver_maps": naver_review}}
    )
    await session.commit()
    snapshot = await snapshot_for(session, redis, row, user, kind)
    assert catalog_google_place_id(row) is None
    persisted = json.dumps(identity_metadata(row))
    assert "GOOGLE_TEMP" not in persisted and "37.571234" not in persisted
    assert 0 < await redis.ttl(comparison_key(CatalogReference(kind=kind, id=row.id))) <= 900
    result = await review_identity(
        session,
        redis,
        CatalogReference(kind=kind, id=row.id),
        decision(snapshot),
        user.id,
    )
    assert result["map_identities"]["google_places"]["status"] == "verified"
    assert result["map_identities"]["naver_maps"]["verified_at"] == naver_review["verified_at"]
    assert "evidence_url" not in result["map_identities"]["naver_maps"]
    metadata = identity_metadata(row)
    assert metadata["map_identities"]["naver_maps"] == naver_review
    google_review = dict(result["map_identities"]["google_places"])
    # Changing one provider's own review timestamp cannot reset the other provider.
    metadata["map_identities"]["naver_maps"] = {
        **naver_review, "verified_at": "2026-08-02T00:00:00Z",
    }
    set_identity_metadata(row, metadata)
    assert catalog_map_identities(row)["google_places"] == google_review
    assert canonical_values(row) == {**before, "google_place_id": "ChIJcandidate"}
    assert (row.status if kind == "hotel" else row.review_status) == "approved"
    audits = (await session.scalars(select(AdminAuditLog))).all()
    assert [audit.action for audit in audits] == [
        "map_identity.candidates_collected",
        "map_identity.confirm",
    ]
    assert all("GOOGLE_TEMP" not in json.dumps(audit.metadata_json) for audit in audits)


async def test_confirm_never_publishes_unreviewed_merchant(database, providers):
    session, user = database
    redis, _ = providers
    row = await add_place(
        session,
        review_status="pending",
        is_active=False,
        map_match_status="unverified",
        naver_map_url=None,
    )
    snapshot = await snapshot_for(session, redis, row, user)
    await review_identity(
        session, redis, CatalogReference(kind="merchant", id=row.id), decision(snapshot), user.id
    )
    assert row.review_status == "pending" and row.is_active is False
    assert row.map_match_status == "unverified" and row.naver_map_url is None


async def test_stale_canonical_record_or_revision_rejects_confirmation(database, providers):
    session, user = database
    redis, _ = providers
    row = await add_place(session)
    snapshot = await snapshot_for(session, redis, row, user)
    row.address = "Different branch address"
    await session.commit()
    with pytest.raises(AppError) as failure:
        await review_identity(
            session,
            redis,
            CatalogReference(kind="merchant", id=row.id),
            decision(snapshot),
            user.id,
        )
    assert failure.value.code == "map_identity_changed"
    assert row.google_place_id is None


@pytest.mark.parametrize("change", ["expired", "actor", "unknown_candidate"])
async def test_snapshot_is_actor_bound_and_exact_candidate_bound(database, providers, change):
    session, user = database
    redis, _ = providers
    row = await add_place(session)
    snapshot = await snapshot_for(session, redis, row, user)
    if change == "expired":
        await redis.delete(snapshot_key(UUID(snapshot["snapshot_id"])))
    payload = decision(
        snapshot, **({"place_id": "ChIJunseen"} if change == "unknown_candidate" else {})
    )
    with pytest.raises(AppError) as failure:
        await review_identity(
            session,
            redis,
            CatalogReference(kind="merchant", id=row.id),
            payload,
            uuid4() if change == "actor" else user.id,
        )
    assert failure.value.code == "map_identity_snapshot_expired"


async def test_duplicate_google_id_and_replayed_confirmation_are_rejected(database, providers):
    session, user = database
    redis, _ = providers
    row = await add_place(session)
    snapshot = await snapshot_for(session, redis, row, user)
    owner = await add_place(session, google_place_id="ChIJcandidate")
    with pytest.raises(AppError) as failure:
        await review_identity(
            session,
            redis,
            CatalogReference(kind="merchant", id=row.id),
            decision(snapshot),
            user.id,
        )
    assert failure.value.code == "map_identity_duplicate"
    owner.google_place_id = None
    await session.commit()
    await review_identity(
        session, redis, CatalogReference(kind="merchant", id=row.id), decision(snapshot), user.id
    )
    with pytest.raises(AppError):
        await review_identity(
            session,
            redis,
            CatalogReference(kind="merchant", id=row.id),
            decision(snapshot),
            user.id,
        )


async def test_rejection_does_not_overwrite_current_identity(database, providers):
    session, user = database
    redis, _ = providers
    row = await add_place(session, google_place_id="ChIJexisting")
    snapshot = await snapshot_for(session, redis, row, user)
    result = await review_identity(
        session,
        redis,
        CatalogReference(kind="merchant", id=row.id),
        decision(snapshot, action="reject"),
        user.id,
    )
    assert row.google_place_id == "ChIJexisting"
    assert result["review"]["status"] == "rejected"


async def test_collecting_again_does_not_downgrade_confirmed_identity(database, providers):
    session, user = database
    redis, _ = providers
    row = await add_place(session)
    snapshot = await snapshot_for(session, redis, row, user)
    await review_identity(
        session, redis, CatalogReference(kind="merchant", id=row.id), decision(snapshot), user.id
    )
    snapshot = await snapshot_for(session, redis, row, user)
    assert snapshot["item"]["review"]["status"] == "pending"
    assert catalog_map_identities(row)["google_places"]["status"] == "verified"


@pytest.mark.parametrize("other_kind", ["hotspot", "hotel"])
async def test_google_identity_cannot_be_confirmed_for_a_different_catalog_kind(
    database, providers, other_kind
):
    session, user = database
    redis, _ = providers
    row = await add_place(session)
    snapshot = await snapshot_for(session, redis, row, user)
    owner = await add_place(session, other_kind)
    if other_kind == "hotel":
        owner.facts = {**owner.facts, "google_place_id": "ChIJcandidate"}
    else:
        owner.google_place_id = "ChIJcandidate"
    await session.commit()
    with pytest.raises(AppError) as failure:
        await review_identity(
            session,
            redis,
            CatalogReference(kind="merchant", id=row.id),
            decision(snapshot),
            user.id,
        )
    assert failure.value.code == "map_identity_duplicate"


async def test_country_mismatch_is_not_saved_as_korean_candidate(database, providers):
    session, user = database
    redis, service = providers
    row = await add_place(session)
    service.search_place_candidates.return_value[0]["country_code"] = "JP"
    result = await collect_candidates(
        session, redis, Settings(), CatalogReference(kind="merchant", id=row.id), user.id
    )
    assert result["candidates"] == []
    assert result["item"]["review"]["candidate_place_ids"] == []


def test_batch_is_explicit_bounded_and_unique():
    with pytest.raises(ValidationError):
        IdentityBatchRequest(targets=[{"kind": "merchant", "id": uuid4()} for _ in range(51)])
    target = {"kind": "merchant", "id": uuid4()}
    with pytest.raises(ValidationError):
        IdentityBatchRequest(targets=[target, target])


async def test_list_filters_pending_and_confirmed_in_sql(database, providers, monkeypatch):
    session, user = database
    redis, _ = providers
    monkeypatch.setattr(router_module, "load_runtime_settings", AsyncMock(return_value=Settings()))
    row = await add_place(session)
    snapshot = await snapshot_for(session, redis, row, user)
    pending = await list_identities(user, session, "merchant", None, "pending", 0, 50)
    assert pending["total"] == 1
    await review_identity(
        session, redis, CatalogReference(kind="merchant", id=row.id), decision(snapshot), user.id
    )
    confirmed = await list_identities(user, session, "merchant", None, "confirmed", 0, 50)
    assert confirmed["total"] == 1
    missing = await list_identities(user, session, "merchant", None, "missing", 0, 50)
    assert missing["total"] == 0


async def test_hotel_identity_list_includes_korean_extension_destinations(database, monkeypatch):
    session, user = database
    monkeypatch.setattr(router_module, "load_runtime_settings", AsyncMock(return_value=Settings()))
    row = await add_place(session, "hotel")
    row.destination_id = "gyeongju"
    await session.commit()
    result = await list_identities(user, session, "hotel", "gyeongju", "all", 0, 50)
    assert result["total"] == 1
    assert result["items"][0]["country_code"] == "KR"


async def test_generic_hotel_import_cannot_certify_or_erase_review_facts(database):
    session, _ = database
    row = await add_place(session, "hotel")
    server_identity = {"provider": "google_places", "place_id": "ChIJserver", "status": "verified"}
    row.facts = {
        **row.facts,
        "map_identities": {"google_places": server_identity},
        "map_identity_review": {"revision": 4},
    }
    await session.commit()
    payload = ProductInput(
        source_key=row.source_key,
        kind="hotel",
        destination_id="seoul",
        title=row.title,
        names_json=row.names_json,
        source_url=row.source_url,
        facts=Facts.model_validate({**row.facts, "map_identities": {}}),
    )
    updated, _ = await upsert_product(session, payload)
    assert updated.facts["map_identities"]["google_places"] == server_identity
    assert updated.facts["map_identity_review"] == {"revision": 4}


async def test_new_admin_endpoints_require_content_capabilities(database, monkeypatch):
    session, user = database
    user.__dict__["_admin_roles_cache"] = frozenset({"support"})
    app = FastAPI()
    app.include_router(router_module.router)
    app.add_exception_handler(AppError, app_error_handler)
    app.dependency_overrides[current_user] = lambda: user
    app.dependency_overrides[get_session] = lambda: session
    monkeypatch.setattr(router_module, "load_runtime_settings", AsyncMock(return_value=Settings()))
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/admin/map-identities/batches",
            headers={"Idempotency-Key": "test-key-123"},
            json={"targets": [{"kind": "merchant", "id": str(uuid4())}]},
        )
        assert response.status_code == 403

        response = await client.get(f"/admin/map-identities/merchant/{uuid4()}/candidates")
        assert response.status_code == 403


async def test_batch_creation_is_idempotent_and_does_not_enqueue_more_than_once(
    database, providers, monkeypatch
):
    session, user = database
    redis, _ = providers
    row = await add_place(session)
    monkeypatch.setattr(router_module, "get_redis", lambda: redis)
    monkeypatch.setattr(router_module, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(
        router_module,
        "load_runtime_settings",
        AsyncMock(return_value=Settings(google_maps_api_key="test-key")),
    )
    enqueue = Mock()
    monkeypatch.setattr(router_module, "enqueue_identity_batch", enqueue)
    payload = IdentityBatchRequest(targets=[CatalogReference(kind="merchant", id=row.id)])
    first = await router_module.create_identity_batch(payload, user, session, "test-batch-key")
    replay = await router_module.create_identity_batch(payload, user, session, "test-batch-key")
    assert first == replay and first["status"] == "queued"
    assert enqueue.call_count == 1
    assert 0 < await redis.ttl(batch_key(first["id"])) <= 7 * 86_400
    other = IdentityBatchRequest(targets=[CatalogReference(kind="merchant", id=uuid4())])
    with pytest.raises(AppError) as failure:
        await router_module.create_identity_batch(other, user, session, "test-batch-key")
    assert failure.value.code == "idempotency_conflict"


async def test_dead_worker_is_reported_as_failed_instead_of_running(
    database, providers, monkeypatch
):
    _, user = database
    redis, _ = providers
    batch_id = uuid4()
    await redis.set(
        batch_key(batch_id),
        json.dumps(
            {
                "id": str(batch_id),
                "status": "running",
                "total": 2,
                "processed": 1,
                "results": [],
            }
        ),
    )
    monkeypatch.setattr(router_module, "get_redis", lambda: redis)
    monkeypatch.setattr(router_module, "identity_batch_job_status", lambda _: "failed")
    result = await router_module.identity_batch_status(batch_id, user)
    assert result["status"] == "failed" and result["processed"] == 1


async def test_worker_reports_partial_and_stops_when_usage_guard_refuses(
    database, providers, monkeypatch
):
    session, user = database
    redis, _ = providers
    batch_id = uuid4()
    targets = [{"kind": "merchant", "id": str(uuid4())} for _ in range(3)]
    state = {"id": str(batch_id), "status": "queued", "total": 3, "processed": 0, "results": []}
    await redis.set(batch_key(batch_id), json.dumps(state))

    @asynccontextmanager
    async def session_factory():
        yield session

    monkeypatch.setattr(tasks_module, "SessionFactory", session_factory)
    monkeypatch.setattr(tasks_module, "get_redis", lambda: redis)
    monkeypatch.setattr(tasks_module, "load_runtime_settings", AsyncMock(return_value=Settings()))
    collect = AsyncMock(
        side_effect=[
            {"candidates": [{"place_id": "ChIJpending"}]},
            AppError(429, "google_maps_usage_guard", "budget"),
        ]
    )
    monkeypatch.setattr(tasks_module, "collect_candidates", collect)
    await tasks_module._run_batch(batch_id, user.id, targets)
    final = json.loads(await redis.get(batch_key(batch_id)))
    assert final["status"] == "partial" and final["processed"] == 2
    assert [row["outcome"] for row in final["results"]] == ["pending", "google_maps_usage_guard"]
    assert collect.call_count == 2
    audit = await session.scalar(
        select(AdminAuditLog).where(AdminAuditLog.action == "map_identity.batch_completed")
    )
    assert audit.metadata_json["processed"] == 2
    await tasks_module._run_batch(batch_id, user.id, targets)
    assert collect.call_count == 2
