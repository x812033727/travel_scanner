"""Real PostgreSQL transactions; all provider traffic is stubbed, never a paid booking."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from datetime import UTC, date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import fakeredis.aioredis
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import current_user
from app.config import Settings
from app.db import engine, get_session
from app.models import (
    AdminAuditLog,
    AffiliateClick,
    TravelServiceBrand,
    TravelServiceConfig,
    TravelServiceFavorite,
    TravelServiceOffer,
    TravelServiceProduct,
    TripPlan,
    TripPlanItem,
    TripServiceSelection,
    User,
)
from app.problems import AppError, app_error_handler
from app.saved.router import router as saved_router
from app.travel_services import admin, router
from app.travel_services.schemas import CITIES, KINDS, Facts
from app.travel_services.service import link_context

pytestmark = [
    pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"),
    pytest.mark.asyncio(loop_scope="module"),
]


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def database_lifecycle() -> AsyncIterator[None]:
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
                yield database
        finally:
            await transaction.rollback()


@pytest_asyncio.fixture(loop_scope="module")
async def actor(session):
    user = User(
        id=uuid4(),
        email=f"services-{uuid4()}@example.test",
        password_hash="unused",
        is_admin=True,
        is_active=True,
    )
    session.add(user)
    await session.flush()
    return user


@pytest_asyncio.fixture(loop_scope="module")
async def client(session, actor, monkeypatch):
    settings = Settings(
        _env_file=None,
        travelpayouts_enabled=True,
        travelpayouts_project_id="123",
        travelpayouts_marker="456",
        travelpayouts_api_token="fixture-not-a-live-key",
        google_maps_api_key=None,
        google_routes_api_key=None,
    )
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    for module in (router, admin):
        monkeypatch.setattr(module, "load_runtime_settings", AsyncMock(return_value=settings))
        monkeypatch.setattr(module, "get_redis", lambda: redis)
    monkeypatch.setattr(router, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr("app.trips.router.get_redis", lambda: redis)
    monkeypatch.setattr("app.trips.router.load_runtime_settings", AsyncMock(return_value=settings))
    # Hotel mutation reuses the real routing/serialization path with paid routing disabled.
    application = FastAPI()
    application.add_exception_handler(AppError, app_error_handler)
    application.include_router(router.router)
    application.include_router(admin.router)
    application.include_router(saved_router)
    application.dependency_overrides[get_session] = lambda: session
    application.dependency_overrides[current_user] = lambda: actor
    config = await session.get(TravelServiceConfig, 1)
    if config is None:
        config = TravelServiceConfig(id=1, version=1)
        session.add(config)
    config.data = {
        "public_enabled": True,
        "enabled_kinds": list(KINDS),
        "enabled_destinations": list(CITIES),
        "airalo_feed_enabled": False,
    }
    await session.commit()
    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="https://test"
    ) as http:
        yield http
    await redis.aclose()


async def product(session, kind="tour", city="tokyo", status="approved", **facts):
    row = TravelServiceProduct(
        id=uuid4(),
        source_key=uuid4().hex,
        kind=kind,
        destination_id=city,
        title="Verified fixture",
        names_json={"ja": "確認済みの例"},
        source_url="https://official.example.com/product",
        status=status,
        facts=Facts(**facts).model_dump(mode="json"),
        verified_at=datetime.now(UTC),
        version=1,
    )
    session.add(row)
    await session.flush()
    return row


async def trip(session, actor, city="tokyo"):
    row = TripPlan(
        id=uuid4(),
        user_id=actor.id,
        name=city,
        destination_name=city,
        mode="manual",
        total_price=Decimal("1200"),
        currency="TWD",
        version=1,
        start_date=date(2026, 11, 11),
        end_date=date(2026, 11, 13),
        timezone="Asia/Tokyo",
        data={"destination_id": city, "routing_defaults": {"auto_compute": False}},
    )
    session.add(row)
    await session.flush()
    return row


async def offer(session, item):
    now = datetime.now(UTC)
    brand = TravelServiceBrand(
        id=uuid4(),
        project_id="123",
        code="klook",
        enabled=True,
        approval="approved",
        verified_at=now,
    )
    session.add(brand)
    await session.flush()
    row = TravelServiceOffer(
        id=uuid4(),
        product_id=item.id,
        brand_id=brand.id,
        target_url="https://www.klook.com/activity/123-fixture/",
        status="approved",
        scope="product",
        verified_at=now,
        version=1,
    )
    session.add(row)
    await session.flush()
    return row, brand


async def test_catalog_only_exposes_reviewed_products_and_ready_offers(client, session):
    good = await product(session)
    pending = await product(session, status="pending")
    link, brand = await offer(session, good)
    result = await client.get(
        "/travel-services?destination_id=tokyo", headers={"X-Travel-Locale": "ja"}
    )
    assert result.status_code == 200
    rows = {r["id"]: r for r in result.json()["items"]}
    assert str(pending.id) not in rows
    assert rows[str(good.id)]["title"] == "確認済みの例"
    assert rows[str(good.id)]["offers"][0]["id"] == str(link.id)
    brand.approval = "pending"
    await session.flush()
    result = await client.get("/travel-services?destination_id=tokyo")
    assert next(r for r in result.json()["items"] if r["id"] == str(good.id))["offers"] == []


async def test_anonymous_clickout_is_303_and_never_books(client, session, monkeypatch):
    item = await product(session)
    link, _ = await offer(session, item)
    creator = AsyncMock(return_value="https://tp.st/verified-fixture")
    monkeypatch.setattr(router.TravelpayoutsLinkClient, "create", creator)
    response = await client.post(
        f"/affiliates/offers/{link.id}/clickout?placement=destination",
        headers={"X-Travel-Locale": "ko"},
    )
    assert response.status_code == 303
    assert response.headers["location"] == "https://tp.st/verified-fixture"
    assert response.headers["referrer-policy"] == "no-referrer"
    clicked = await session.scalar(
        select(AffiliateClick).where(AffiliateClick.sub_id == "svc_tour_tokyo_ko_destination")
    )
    assert clicked.user_id is None
    assert clicked.brand == "klook"
    assert not await session.scalar(
        select(TripServiceSelection.id).where(TripServiceSelection.product_id == item.id)
    )
    assert len(creator.await_args.args) == 2
    assert str(item.id) not in creator.await_args.args[1]
    assert (
        await client.post(f"/affiliates/offers/{uuid4()}/clickout?url=https://evil.com")
    ).status_code == 404


async def test_selection_is_idempotent_versioned_and_can_be_scheduled_later(client, session, actor):
    item = await product(session, duration_minutes=60)
    journey = await trip(session, actor)
    path = f"/trips/{journey.id}/travel-services"
    body = {"product_id": str(item.id), "version": 1}
    response = await client.post(path, json=body, headers={"Idempotency-Key": "add-fixture"})
    assert response.status_code == 200, response.text
    selected_id = response.json()["id"]
    assert response.json()["status"] == "planned"
    replay = await client.post(path, json=body, headers={"Idempotency-Key": "add-fixture"})
    assert replay.json()["replayed"]
    row = await session.scalar(
        select(TripServiceSelection).where(TripServiceSelection.product_id == item.id)
    )
    assert row.item_id is None
    other = await product(session)
    conflict = await client.post(
        path, json={**body, "product_id": str(other.id)}, headers={"Idempotency-Key": "add-fixture"}
    )
    assert conflict.status_code == 409
    body.update(
        version=response.json()["version"],
        day_date="2026-11-11",
        start_time="2026-11-11T10:00:00+09:00",
        end_time="2026-11-11T11:00:00+09:00",
    )
    scheduled = await client.post(path, json=body, headers={"Idempotency-Key": "schedule-fixture"})
    assert scheduled.status_code == 200, scheduled.text
    assert scheduled.json()["id"] == selected_id
    await session.refresh(row)
    assert row.item_id
    stop = await session.get(TripPlanItem, row.item_id)
    assert stop.fixed_time and stop.data["source_mode"] == "manual"
    assert (
        await session.scalar(
            select(func.count())
            .select_from(TripServiceSelection)
            .where(TripServiceSelection.trip_id == journey.id)
        )
        == 1
    )
    stale = await client.post(
        path,
        json={"product_id": str(other.id), "version": 1},
        headers={"Idempotency-Key": "other-fixture"},
    )
    assert stale.status_code == 409
    booked = await client.patch(
        f"{path}/{selected_id}", json={"version": scheduled.json()["version"], "status": "booked"}
    )
    assert booked.status_code == 200
    assert row.status == "booked"


async def test_time_conflict_and_other_owner_cannot_mutate(client, session, actor):
    journey = await trip(session, actor)
    item = await product(session)
    locked = TripPlanItem(
        trip_plan_id=journey.id,
        item_type="activity",
        day_date=journey.start_date,
        title="Do not change",
        locked=True,
        fixed_time=True,
        start_time=datetime(2026, 11, 11, 1, tzinfo=UTC),
        end_time=datetime(2026, 11, 11, 3, tzinfo=UTC),
        data={"source_mode": "manual"},
    )
    session.add(locked)
    await session.flush()
    response = await client.post(
        f"/trips/{journey.id}/travel-services",
        headers={"Idempotency-Key": "conflict-fixture"},
        json={
            "product_id": str(item.id),
            "version": 1,
            "day_date": "2026-11-11",
            "start_time": "2026-11-11T10:00:00+09:00",
            "end_time": "2026-11-11T11:00:00+09:00",
        },
    )
    assert response.status_code == 409
    assert locked.title == "Do not change" and locked.locked
    assert (await client.get(f"/trips/{uuid4()}/travel-services")).status_code == 404
    actor.is_admin = False
    assert (await client.get("/admin/travel-services")).status_code == 403


async def test_hotel_no_quote_preserves_locked_anchor_and_syncs_others(client, session, actor):
    journey = await trip(session, actor)
    hotel = await product(
        session,
        "hotel",
        latitude=35.6812,
        longitude=139.7671,
        coordinate_source_url="https://official.example.com/map",
        google_place_id="ChIJfixture",
        map_verified=True,
        area_code="marunouchi",
    )
    locked = TripPlanItem(
        trip_plan_id=journey.id,
        item_type="activity",
        system_role="hotel_start",
        day_date=journey.start_date,
        title="Locked stay",
        location_name="Locked stay",
        locked=True,
        fixed_time=True,
        latitude=Decimal("35.67"),
        longitude=Decimal("139.76"),
        data={},
    )
    session.add(locked)
    await session.flush()
    response = await client.post(
        f"/trips/{journey.id}/travel-services",
        headers={"Idempotency-Key": "hotel-fixture"},
        json={"product_id": str(hotel.id), "version": 1},
    )
    assert response.status_code == 200, response.text
    await session.refresh(journey)
    await session.refresh(locked)
    assert locked.title == "Locked stay"
    assert locked.latitude == Decimal("35.67")
    assert journey.data["primary_lodging"]["catalog_product_id"] == str(hotel.id)
    assert journey.data["prices_stale"] and journey.total_price == Decimal("1200")
    assert "price_snapshot" not in journey.data["primary_lodging"]
    assert await session.scalar(
        select(TripPlanItem.id).where(
            TripPlanItem.trip_plan_id == journey.id, TripPlanItem.provider_place_id == "ChIJfixture"
        )
    )


async def test_esim_multicity_dedup_no_timeline_and_country_gate(client, session, actor):
    journey = await trip(session, actor, "osaka")
    journey.destination_name = "Osaka Kyoto"
    esim = await product(session, "esim", country_codes=["JP"], validity_days=7)
    other = await product(session, "esim", country_codes=["KR"], validity_days=7)
    result = await client.get(f"/trips/{journey.id}/travel-services?type=esim")
    ids = [p["id"] for p in result.json()["items"]]
    assert ids.count(str(esim.id)) == 1 and str(other.id) not in ids
    response = await client.post(
        f"/trips/{journey.id}/travel-services",
        headers={"Idempotency-Key": "esim-fixture"},
        json={"product_id": str(esim.id), "version": 1},
    )
    assert response.status_code == 200, response.text
    selected = await session.scalar(
        select(TripServiceSelection).where(TripServiceSelection.product_id == esim.id)
    )
    assert selected.item_id is None
    invalid = await client.post(
        f"/trips/{journey.id}/travel-services",
        headers={"Idempotency-Key": "esim-wrong-country"},
        json={"product_id": str(other.id), "version": response.json()["version"]},
    )
    assert invalid.status_code == 422


async def test_import_preview_commit_replay_and_review_reset(client, session):
    csv = "source_key,kind,destination_id,title,source_url\nfixture-import,tour,tokyo,Official tour,https://official.example.com/tour"
    response = await client.post("/admin/travel-services/imports/preview", json={"csv": csv})
    assert response.status_code == 200
    identifier = response.json()["id"]
    assert not await session.scalar(
        select(TravelServiceProduct.id).where(TravelServiceProduct.source_key == "fixture-import")
    )
    committed = await client.post(f"/admin/travel-services/imports/{identifier}/commit")
    assert committed.status_code == 200
    assert (
        await client.post(f"/admin/travel-services/imports/{identifier}/commit")
    ).json() == committed.json()
    row = await session.scalar(
        select(TravelServiceProduct).where(TravelServiceProduct.source_key == "fixture-import")
    )
    assert row.status == "pending"
    assert (
        await client.post(
            f"/admin/travel-services/products/{row.id}/review",
            json={"status": "approved", "version": row.version},
        )
    ).status_code == 200
    changed = await client.put(
        f"/admin/travel-services/products/{row.id}?version={row.version}",
        json={
            "source_key": "fixture-import",
            "kind": "tour",
            "destination_id": "tokyo",
            "title": "New identity",
            "source_url": row.source_url,
            "facts": {},
            "names_json": {},
        },
    )
    assert changed.status_code == 200 and changed.json()["status"] == "pending"
    assert await session.scalar(
        select(AdminAuditLog.id).where(AdminAuditLog.action == "travel_services.import_commit")
    )


async def test_favorites_and_cascade_without_deleting_selected_history(client, session):
    item = await product(session)
    path = f"/saved-items/service/{item.id}"
    assert (await client.put(path)).status_code == 200
    assert (await client.put(path)).status_code == 200
    assert (
        await session.scalar(
            select(func.count())
            .select_from(TravelServiceFavorite)
            .where(TravelServiceFavorite.product_id == item.id)
        )
        == 1
    )
    item.status = "disabled"
    await session.flush()
    assert (await client.put(path)).status_code == 404
    assert (await client.delete(path)).status_code == 200


async def test_static_links_require_marker_project_verification(client, session, monkeypatch):
    item = await product(session)
    link, _ = await offer(session, item)
    link.status = "pending"
    link.static_url = "https://tp.st/fixture"
    verifier = AsyncMock(return_value=False)
    monkeypatch.setattr(admin, "verify_link", verifier)
    path = f"/admin/travel-services/offers/{link.id}/review"
    assert (await client.post(path, json={"version": 1, "status": "approved"})).status_code == 422
    assert verifier.await_args.kwargs == {"marker": "456", "project": "123"}
    verifier.return_value = True
    assert (await client.post(path, json={"version": 1, "status": "approved"})).status_code == 200
    assert link.verification_context == link_context(
        Settings(_env_file=None, travelpayouts_marker="456", travelpayouts_project_id="123")
    )
