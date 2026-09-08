"""Real PostgreSQL transactions; all provider traffic is stubbed, never a paid booking."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import fakeredis.aioredis
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.affiliates import router as affiliate_router
from app.auth.service import current_user
from app.config import Settings
from app.db import engine, get_session
from app.models import (
    AdminAuditLog,
    AffiliateClick,
    HotelBookingClick,
    HotelBookingOption,
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
    for module in (router, admin, affiliate_router):
        monkeypatch.setattr(module, "load_runtime_settings", AsyncMock(return_value=settings))
        monkeypatch.setattr(module, "get_redis", lambda: redis)
    monkeypatch.setattr(router, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(affiliate_router, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr("app.trips.router.get_redis", lambda: redis)
    monkeypatch.setattr("app.trips.router.load_runtime_settings", AsyncMock(return_value=settings))
    # Hotel mutation reuses the real routing/serialization path with paid routing disabled.
    application = FastAPI()
    application.add_exception_handler(AppError, app_error_handler)
    application.include_router(router.router)
    application.include_router(admin.router)
    application.include_router(affiliate_router.router)
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
        "enabled_destinations": [*CITIES, "taichung"],
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


async def test_destination_offer_admin_public_and_clickout(
    client, session, actor, monkeypatch
):
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
    await session.commit()
    created = await client.post(
        "/admin/travel-services/destination-offers",
        json={
            "brand_id": str(brand.id),
            "destination_id": "taichung",
            "module": "activities",
            "target_url": "https://www.klook.com/city/152-taichung/",
        },
    )
    assert created.status_code == 201
    pending = created.json()
    assert pending["status"] == "pending"
    monkeypatch.setattr(
        "app.travel_services.admin.TravelpayoutsLinkClient.create",
        AsyncMock(return_value="https://klook.tp.st/fixture"),
    )
    monkeypatch.setattr("app.travel_services.admin.verify_link", AsyncMock(return_value=True))
    reviewed = await client.post(
        f"/admin/travel-services/destination-offers/{pending['id']}/review",
        json={"version": pending["version"], "status": "approved"},
    )
    assert reviewed.status_code == 200
    public = await client.get(
        "/affiliates/destination-offers",
        params={"destination_id": "taichung", "module": "activities"},
        headers={"x-travel-locale": "en"},
    )
    assert public.status_code == 200
    assert public.json()["options"][0]["display_name"] == "Klook"
    assert "target_url" not in public.text
    monkeypatch.setattr(
        "app.affiliates.router.TravelpayoutsLinkClient.create",
        AsyncMock(return_value="https://klook.tp.st/fixture"),
    )
    clickout = await client.post(public.json()["options"][0]["clickout_url"])
    assert clickout.status_code == 303
    click = await session.scalar(
        select(AffiliateClick).where(AffiliateClick.offer_id == UUID(pending["id"]))
    )
    assert click and click.brand == "klook" and click.destination_id == "taichung"


async def option_fixture(session, client, monkeypatch):
    config = await session.get(TravelServiceConfig, 1)
    config.data = {**config.data, "direct_hotel_links_enabled": True}
    item = await product(
        session,
        kind="hotel",
        area_code="shinjuku",
        latitude=35.69,
        longitude=139.70,
        google_place_id="ChIJ_fixture_only",
        map_verified=True,
        coordinate_source_url="https://official.example.com/access",
    )
    link = HotelBookingOption(
        provider="booking",
        product_id=item.id,
        url="https://www.booking.com/hotel/jp/fixture.html",
        evidence_url=item.source_url,
        property_id="fixture-123",
        identity_note="Exact test identity",
        status="approved",
        discovery_status="found",
        verified_at=datetime.now(UTC),
        health_status="healthy",
        version=1,
    )
    item.hotel_options.append(link)
    await session.commit()
    monkeypatch.setattr(
        "app.catalog_review.evidence.public_request_target",
        AsyncMock(return_value=("https://1.1.1.1/", "www.booking.com")),
    )
    return item, link


async def test_unified_option_no_credentials_and_no_page_fetch(client, session, monkeypatch):
    item, link = await option_fixture(session, client, monkeypatch)
    before_clicks = await session.scalar(select(func.count()).select_from(AffiliateClick))
    before_selections = await session.scalar(select(func.count()).select_from(TripServiceSelection))
    monkeypatch.setattr(
        router, "load_runtime_settings", AsyncMock(return_value=Settings(_env_file=None))
    )
    checker = AsyncMock(side_effect=AssertionError("clickouts must not fetch hotel pages"))
    monkeypatch.setattr("app.travel_services.network.check_hotel_link", checker)
    endpoint = f"/travel-services/{item.id}/booking-options/{link.id}/clickout"
    result = await client.post(endpoint + "?url=https://evil.example.com")
    assert result.status_code == 303
    assert result.headers["location"] == link.url
    checker.assert_not_called()
    click = await session.scalar(
        select(HotelBookingClick).where(HotelBookingClick.option_id == link.id)
    )
    assert click.mode == "direct" and not click.fallback
    assert await session.scalar(select(func.count()).select_from(AffiliateClick)) == before_clicks
    assert (
        await session.scalar(select(func.count()).select_from(TripServiceSelection))
        == before_selections
    )
    assert (
        await client.post(f"/travel-services/{item.id}/booking-options/{uuid4()}/clickout")
    ).status_code == 404
    link.status = "pending"
    await session.flush()
    assert (await client.post(endpoint)).status_code == 404


async def test_unified_affiliate_same_hotel_fallback_and_project_isolation(
    client, session, monkeypatch
):
    item, option = await option_fixture(session, client, monkeypatch)
    before_clicks = await session.scalar(select(func.count()).select_from(AffiliateClick))
    affiliate, brand = await offer(session, item)
    brand.code = "booking"
    affiliate.target_url = option.url
    # The existing approval context binds credentials, brand version and exact target.
    settings = await router.load_runtime_settings(session)
    affiliate.verification_context = link_context(settings)
    await session.commit()
    create = AsyncMock(return_value="https://tp.st/fixture")
    monkeypatch.setattr(router.TravelpayoutsLinkClient, "create", create)
    endpoint = f"/travel-services/{item.id}/booking-options/{option.id}/clickout"
    result = await client.post(endpoint, headers={"X-Travel-Locale": "ja"})
    assert result.status_code == 303 and result.headers["location"] == "https://tp.st/fixture"
    assert str(brand.version) in create.call_args.kwargs["cache_context"]
    create.side_effect = TimeoutError()
    fallback = await client.post(endpoint)
    assert fallback.status_code == 303 and fallback.headers["location"] == option.url
    clicks = list(
        await session.scalars(
            select(HotelBookingClick)
            .where(HotelBookingClick.option_id == option.id)
            .order_by(HotelBookingClick.created_at)
        )
    )
    assert [(c.mode, c.fallback) for c in clicks] == [("affiliate", False), ("direct", True)]
    assert (
        await session.scalar(select(func.count()).select_from(AffiliateClick)) == before_clicks + 1
    )
    config = await session.get(TravelServiceConfig, 1)
    config.data = {**config.data, "direct_hotel_links_enabled": False}
    await session.commit()
    assert (await client.post(endpoint)).status_code == 503
    config.data = {**config.data, "direct_hotel_links_enabled": True}
    settings.travelpayouts_project_id = "different-project"
    create.reset_mock()
    await session.commit()
    assert (await client.post(endpoint)).headers["location"] == option.url
    create.assert_not_called()


async def test_option_review_reminder_is_independent_from_product_review(
    client, session, monkeypatch
):
    item, option = await option_fixture(session, client, monkeypatch)
    initial = (await client.get("/admin/travel-services")).json()
    assert item.verified_at > datetime.now(UTC) - timedelta(days=1)
    option.verified_at = datetime.now(UTC) - timedelta(days=31)
    await session.flush()
    overview = (await client.get("/admin/travel-services")).json()
    assert overview["review_due"] == initial["review_due"]
    assert overview["hotel_option_review_due"] == initial["hotel_option_review_due"] + 1


async def test_legacy_removal_refreshes_option_version_before_disabling(
    client, session, monkeypatch
):
    from app.travel_services.imports import upsert_product
    from app.travel_services.schemas import ProductInput
    from app.travel_services.service import product_input

    item, option = await option_fixture(session, client, monkeypatch)
    data = product_input(item).model_dump(mode="json")
    data["facts"]["hotel_links"] = []
    # Simulate a completed review after this request loaded the relationship.
    # Keep the identity map deliberately stale, as with a concurrent transaction.
    await session.execute(
        update(HotelBookingOption)
        .where(HotelBookingOption.id == option.id)
        .values(version=7)
        .execution_options(synchronize_session=False)
    )
    assert option.version != 7
    await upsert_product(session, ProductInput.model_validate(data))
    await session.flush()
    assert option.status == "disabled" and option.version == 8


async def test_option_versions_duplicate_identity_and_independent_review(
    client, session, monkeypatch
):
    item, option = await option_fixture(session, client, monkeypatch)
    endpoint = f"/admin/travel-services/products/{item.id}/booking-options"
    body = {
        "provider": "trip_com",
        "version": 0,
        "url": "https://www.trip.com/hotels/tokyo-hotel-detail-123/fixture/",
        "evidence_url": item.source_url,
        "identity_note": "Name and address checked",
    }
    response = await client.put(endpoint, json=body)
    assert response.status_code == 200 and response.json()["status"] == "pending"
    assert item.status == "approved" and option.status == "approved"
    assert (await client.put(endpoint, json=body)).status_code == 409
    other = await product(session, kind="hotel")
    assert (
        await client.put(f"/admin/travel-services/products/{other.id}/booking-options", json=body)
    ).status_code == 409
    added = response.json()
    review = {
        "version": added["version"],
        "status": "approved",
        "identity_note": "Browser verified exact address",
    }
    monkeypatch.setattr(
        "app.travel_services.network.check_hotel_link", AsyncMock(return_value="unconfirmed")
    )
    path = endpoint + f"/{added['id']}/review"
    assert (await client.post(path, json=review)).status_code == 422
    assert (await client.post(path, json={**review, "browser_verified": True})).status_code == 200


async def test_csv_without_legacy_links_preserves_reviewed_options(client, session, monkeypatch):
    import csv
    import io
    import json

    from app.travel_services.imports import parse_csv, upsert_product
    from app.travel_services.schemas import ProductInput

    item, option = await option_fixture(session, client, monkeypatch)
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "source_key",
            "kind",
            "destination_id",
            "title",
            "source_url",
            "facts",
            "names_json",
        ],
    )
    writer.writeheader()
    writer.writerow(
        {
            "source_key": item.source_key,
            "kind": "hotel",
            "destination_id": "tokyo",
            "title": item.title,
            "source_url": item.source_url,
            "facts": json.dumps({k: v for k, v in item.facts.items() if k != "hotel_links"}),
            "names_json": json.dumps(item.names_json),
        }
    )
    parsed = parse_csv(output.getvalue())
    assert "hotel_links" not in parsed[0]["product"]["facts"]
    same, changed = await upsert_product(session, ProductInput.model_validate(parsed[0]["product"]))
    assert same.id == item.id and not changed and option.status == "approved"


async def test_quotes_disabled_are_honest_uncached_and_do_not_expose_policies(
    client, session, monkeypatch
):
    item, _ = await option_fixture(session, client, monkeypatch)
    response = await client.post(
        f"/travel-services/{item.id}/hotel-quotes",
        json={
            "check_in": "2027-11-11",
            "check_out": "2027-11-13",
            "rooms": [{"adults": 2}],
            "currency": "TWD",
            "booker_country": "TW",
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "not_configured" and response.json()["quotes"] == []
    assert response.headers["cache-control"] == "no-store"
    assert "hotel_quote_policies" not in (await client.get("/travel-services/config")).json()


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


@pytest.mark.parametrize("unsafe", [False, True])
async def test_link_maintenance_rotates_outages_but_disables_unsafe_redirects(
    session, monkeypatch, unsafe
):
    from app.travel_services import jobs

    item = await product(session)
    link, _ = await offer(session, item)
    old = datetime(2020, 1, 1, tzinfo=UTC)
    link.updated_at = old
    await session.commit()

    @asynccontextmanager
    async def same_session():
        yield session

    monkeypatch.setattr(jobs, "SessionFactory", same_session)
    monkeypatch.setattr(
        jobs, "verify_link", AsyncMock(side_effect=ValueError() if unsafe else TimeoutError())
    )
    await jobs.maintain_links()
    await session.refresh(link)
    assert link.updated_at > old
    assert link.status == ("disabled" if unsafe else "approved")


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


async def test_transfer_requires_flight_before_scheduling_and_never_auto_books(
    client, session, actor
):
    journey = await trip(session, actor)
    transfer = await product(session, "transfer", airport="NRT", direction="arrival", passengers=4)
    path = f"/trips/{journey.id}/travel-services"
    payload = {
        "product_id": str(transfer.id),
        "version": 1,
        "day_date": "2026-11-11",
        "start_time": "2026-11-11T10:00:00+09:00",
        "end_time": "2026-11-11T11:00:00+09:00",
        "airport": "NRT",
        "direction": "arrival",
        "passengers": 2,
    }
    missing = await client.post(path, json=payload, headers={"Idempotency-Key": "flight-fixture"})
    assert missing.status_code == 422
    payload["flight_number"] = "BR198"
    response = await client.post(path, json=payload, headers={"Idempotency-Key": "flight-fixture"})
    assert response.status_code == 200, response.text
    selection = await session.get(TripServiceSelection, response.json()["id"])
    assert selection.status == "planned"
    assert selection.details["flight_number"] == "BR198"
    item = await session.get(TripPlanItem, selection.item_id)
    assert item.item_type == "activity" and item.data["service_kind"] == "transfer"


async def test_hotel_no_quote_preserves_locked_anchor_and_syncs_others(
    client, session, actor, monkeypatch
):
    # Selecting a reviewed hotel must not depend on any affiliate/network enrollment.
    monkeypatch.setattr(
        router,
        "load_runtime_settings",
        AsyncMock(
            return_value=Settings(
                _env_file=None,
                travelpayouts_enabled=False,
                travelpayouts_project_id=None,
                travelpayouts_api_token=None,
                travelpayouts_marker=None,
            )
        ),
    )
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


async def test_direct_hotel_import_review_and_guest_click_without_network(
    client, session, actor, monkeypatch
):
    import csv
    import io
    import json

    settings = Settings(
        _env_file=None,
        travelpayouts_enabled=False,
        travelpayouts_project_id=None,
        travelpayouts_api_token=None,
        travelpayouts_marker=None,
    )
    for module in (router, admin):
        monkeypatch.setattr(module, "load_runtime_settings", AsyncMock(return_value=settings))
    checker = AsyncMock(return_value=("https://93.184.216.34/stay", "hotel.example.com"))
    monkeypatch.setattr("app.catalog_review.evidence.public_request_target", checker)
    monkeypatch.setattr(
        "app.travel_services.network.check_hotel_link", AsyncMock(return_value="healthy")
    )
    affiliate = AsyncMock(side_effect=AssertionError("No affiliate API for ordinary links"))
    monkeypatch.setattr(router.TravelpayoutsLinkClient, "create", affiliate)
    config = await session.get(TravelServiceConfig, 1)
    config.data = {**config.data, "direct_hotel_links_enabled": True}
    link = {
        "provider": "official",
        "url": "https://hotel.example.com/stay",
        "evidence_url": "https://hotel.example.com/location",
    }
    facts = dict(
        latitude=35.6812,
        longitude=139.7671,
        coordinate_source_url="https://hotel.example.com/location",
        google_place_id="ChIJfixture",
        map_verified=True,
        area_code="marunouchi",
        hotel_links=[link],
    )
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["source_key", "kind", "destination_id", "title", "source_url", "facts"])
    writer.writerow(
        [
            uuid4().hex,
            "hotel",
            "tokyo",
            "Direct hotel fixture",
            "https://hotel.example.com/",
            json.dumps(facts),
        ]
    )
    preview = await client.post(
        "/admin/travel-services/imports/preview", json={"csv": out.getvalue()}
    )
    assert preview.status_code == 200, preview.text
    run_id = preview.json()["id"]
    imported = await client.post(f"/admin/travel-services/imports/{run_id}/commit")
    assert imported.status_code == 200, imported.text
    assert (
        await client.post(f"/admin/travel-services/imports/{run_id}/commit")
    ).json() == imported.json()
    hotel = await session.scalar(
        select(TravelServiceProduct).where(TravelServiceProduct.title == "Direct hotel fixture")
    )
    assert hotel.status == "pending"
    path = f"/travel-services/{hotel.id}/hotel-links/official/clickout"
    assert (await client.post(path)).status_code == 404
    approved = await client.post(
        f"/admin/travel-services/products/{hotel.id}/review",
        json={"version": hotel.version, "status": "approved"},
    )
    assert approved.status_code == 200, approved.text
    option = hotel.hotel_options[0]
    option_review = await client.post(
        f"/admin/travel-services/products/{hotel.id}/booking-options/{option.id}/review",
        json={
            "version": option.version,
            "status": "approved",
            "identity_note": "Confirmed official hotel name and address",
        },
    )
    assert option_review.status_code == 200, option_review.text
    results = (await client.get("/travel-services?destination_id=tokyo&type=hotel")).json()
    item = next(p for p in results["items"] if p["id"] == str(hotel.id))
    assert item["offers"] == []
    assert item["direct_links"] == [{"provider": "official", "name": None}]
    assert "hotel_links" not in item["facts"]
    click_count = await session.scalar(select(func.count()).select_from(AffiliateClick))
    # Guest requires no auth; caller-supplied URLs cannot replace the saved destination.
    client._transport.app.dependency_overrides[current_user] = lambda: None
    response = await client.post(path + "?url=https://evil.example.com/")
    assert response.status_code == 303 and response.headers["location"] == link["url"]
    assert response.headers["referrer-policy"] == "no-referrer"
    assert await session.scalar(select(func.count()).select_from(AffiliateClick)) == click_count
    affiliate.assert_not_called()
    checker.return_value = None
    assert (await client.post(path)).status_code == 503
    checker.return_value = ("https://93.184.216.34/stay", "hotel.example.com")
    config.data = {**config.data, "direct_hotel_links_enabled": False}
    assert (await client.post(path)).status_code == 404
    client._transport.app.dependency_overrides[current_user] = lambda: actor
    config.data = {**config.data, "direct_hotel_links_enabled": True}
    from app.travel_services.service import product_input

    payload = product_input(hotel).model_dump(mode="json")
    payload["facts"]["hotel_links"][0]["url"] = "https://hotel.example.com/new-stay"
    edited = await client.put(
        f"/admin/travel-services/products/{hotel.id}?version={hotel.version}", json=payload
    )
    assert edited.status_code == 200 and edited.json()["status"] == "approved"
    assert (
        hotel.hotel_options[0].status == "pending"
    )  # Link-only edits do not revoke hotel approval.
    assert (await client.post(path)).status_code == 404


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
    assert (await client.put(path)).status_code == 201
    assert (await client.put(path)).status_code == 201
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
    assert (await client.delete(path)).status_code == 204


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
