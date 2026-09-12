"""HTTP, transactional import, and schema regressions for separate enrollments."""

import importlib.util
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import fakeredis.aioredis
import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.affiliates import router as affiliates
from app.auth.service import current_user, optional_current_user
from app.config import Settings
from app.db import Base, get_session
from app.models import (
    AdminAuditLog,
    AffiliateClick,
    DestinationAffiliateOffer,
    HotelBookingClick,
    HotelBookingOption,
    TravelServiceBrand,
    TravelServiceConfig,
    TravelServiceImport,
    TravelServiceOffer,
    TravelServiceProduct,
    TripServiceSelection,
    User,
)
from app.problems import AppError, app_error_handler
from app.travel_services import admin, hotel_admin, router
from app.travel_services.channels import channel_context
from app.travel_services.imports import commit_import, parse_csv
from app.travel_services.schemas import CatalogConfig, Facts

AID = "134379"
TARGET = "https://www.klook.com/zh-TW/activity/12345-test-fixture/"
HOTEL = "https://www.klook.com/zh-TW/hotels/285841"
NOW = datetime.now(UTC)


@pytest.fixture
async def fixture(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite://")
    models = (
        TravelServiceProduct,
        HotelBookingOption,
        TravelServiceBrand,
        TravelServiceOffer,
        DestinationAffiliateOffer,
        TravelServiceConfig,
        TravelServiceImport,
        AdminAuditLog,
        AffiliateClick,
        HotelBookingClick,
        TripServiceSelection,
    )

    @event.listens_for(engine.sync_engine, "connect")
    def sqlite_advisory(connection: Any, _record: Any):
        connection.create_function("pg_advisory_xact_lock", 1, lambda _key: 0)

    # SQLite drops timezone offsets; emulate PostgreSQL's aware DateTime result type.
    def restore_utc(target, _context):
        for column in target.__table__.columns:
            value = getattr(target, column.name)
            if isinstance(value, datetime) and value.tzinfo is None:
                setattr(target, column.name, value.replace(tzinfo=UTC))

    for model in models:
        event.listen(model, "load", restore_utc)
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: Base.metadata.create_all(
                sync, tables=[model.__table__ for model in models]
            )
        )
    config = Settings(
        klook_enabled=True,
        klook_affiliate_id=AID,
        travelpayouts_enabled=True,
        travelpayouts_project_id=AID,
        travelpayouts_marker="456",
        travelpayouts_api_token="fixture-token",
    )
    actor = User(id=uuid4(), email="fixture-admin@example.test", is_admin=True)
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    for module in (admin, hotel_admin, router, affiliates):
        monkeypatch.setattr(module, "load_runtime_settings", AsyncMock(return_value=config))
    for module in (admin, router, affiliates):
        monkeypatch.setattr(module, "get_redis", lambda: redis)
    monkeypatch.setattr(router, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(affiliates, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(
        "app.catalog_review.evidence.public_request_target",
        AsyncMock(return_value=("https://93.184.216.34/", "www.klook.com")),
    )
    monkeypatch.setattr(admin, "verify_link", AsyncMock(return_value=False))
    monkeypatch.setattr(
        admin.TravelpayoutsLinkClient,
        "create",
        AsyncMock(side_effect=AssertionError("Direct Klook must not request Travelpayouts links")),
    )
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)
    app.include_router(admin.router, prefix="/api/v1")
    app.include_router(hotel_admin.router, prefix="/api/v1")
    app.include_router(router.router, prefix="/api/v1")
    app.include_router(affiliates.router, prefix="/api/v1")
    app.dependency_overrides[current_user] = lambda: actor
    app.dependency_overrides[optional_current_user] = lambda: None
    try:
        async with async_sessionmaker(engine, expire_on_commit=False)() as session:
            app.dependency_overrides[get_session] = lambda: session
            session.add(
                TravelServiceConfig(
                    id=1,
                    data=CatalogConfig(
                        public_enabled=True,
                        enabled_kinds=["hotel", "tour", "transfer", "esim"],
                        enabled_destinations=["tokyo", "hiroshima"],
                    ).model_dump(),
                    version=1,
                )
            )
            await session.commit()
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                yield session, client, config, actor
    finally:
        for model in models:
            event.remove(model, "load", restore_utc)
        await redis.aclose()
        await engine.dispose()


async def create_brand(client, channel="klook_direct"):
    response = await client.put(
        "/api/v1/admin/travel-services/brands",
        json={
            "channel": channel,
            "code": "klook",
            "approval": "approved",
            "enabled": True,
            "evidence_url": "https://affiliate.klook.com/zh-TW/my_account"
            if channel == "klook_direct"
            else "https://app.travelpayouts.com/programs/fixture",
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


async def test_http_channels_same_numeric_id_are_separate_and_versioned(fixture):
    session, client, config, actor = fixture
    tp, direct = await create_brand(client, "travelpayouts"), await create_brand(client)
    assert tp["id"] != direct["id"]
    assert tp["project_id"] == direct["project_id"] == AID
    overview = await client.get("/api/v1/admin/travel-services")
    assert overview.status_code == 200, overview.text
    assert {row["channel"] for row in overview.json()["brands"]} == {
        "travelpayouts",
        "klook_direct",
    }
    assert overview.json()["channels"]["klook_direct"]["configured"]
    conflict = await client.put(
        "/api/v1/admin/travel-services/brands",
        json={
            "channel": "klook_direct",
            "code": "klook",
            "approval": "approved",
            "enabled": True,
            "evidence_url": "https://affiliate.klook.com/zh-TW/my_account",
            "version": 99,
        },
    )
    assert conflict.status_code == 409
    assert (await session.get(TravelServiceBrand, UUID(tp["id"]))).version == 1
    config.klook_affiliate_id = "2"
    hidden = await client.get("/api/v1/admin/travel-services")
    assert [row["id"] for row in hidden.json()["brands"]] == [tp["id"]]
    assert actor.is_admin


async def test_http_review_clickout_and_aid_rotation_without_price_or_booking(fixture):
    session, client, config, _actor = fixture
    brand = await create_brand(client)
    created = await client.post(
        "/api/v1/admin/travel-services/products",
        json={
            "source_key": "fixture:klook:12345",
            "kind": "tour",
            "destination_id": "tokyo",
            "title": "Test fixture day tour",
            "source_url": TARGET,
        },
    )
    assert created.status_code == 201, created.text
    product = created.json()
    approved = await client.post(
        f"/api/v1/admin/travel-services/products/{product['id']}/review",
        json={"version": 1, "status": "approved"},
    )
    assert approved.status_code == 200, approved.text
    offer_response = await client.post(
        "/api/v1/admin/travel-services/offers",
        json={
            "product_id": product["id"],
            "brand_id": brand["id"],
            "target_url": TARGET,
        },
    )
    assert offer_response.status_code == 201, offer_response.text
    offer = offer_response.json()
    path = f"/api/v1/admin/travel-services/offers/{offer['id']}/review"
    assert (await client.post(path, json={"version": 1, "status": "approved"})).status_code == 422
    assert (
        await client.post(
            path,
            json={
                "version": 1,
                "status": "approved",
                "browser_verified": True,
                "evidence_url": TARGET + "different/",
            },
        )
    ).status_code == 422
    assert (
        await client.post(
            path,
            json={
                "version": 1,
                "status": "approved",
                "browser_verified": True,
                "evidence_url": TARGET + "?aid=" + AID,
            },
        )
    ).status_code == 200
    catalog = await client.get("/api/v1/travel-services?destination_id=tokyo")
    assert catalog.status_code == 200, catalog.text
    public = catalog.json()["items"][0]
    assert public["facts"]["reference_price"] is None
    assert [entry["id"] for entry in public["offers"]] == [offer["id"]]
    click = await client.post(f"/api/v1/affiliates/offers/{offer['id']}/clickout?placement=trip")
    assert click.status_code == 303, click.text
    assert click.headers["location"] == TARGET + "?aid=" + AID
    assert click.headers["cache-control"] == "no-store"
    row = await session.scalar(select(AffiliateClick))
    assert (row.partner, row.brand, row.service_type, row.user_id) == (
        "klook",
        "klook",
        "tour",
        None,
    )
    assert row.sub_id == "svc_tour_tokyo_zh-TW_trip"
    assert await session.scalar(select(func.count()).select_from(TripServiceSelection)) == 0
    audit = await session.scalar(
        select(AdminAuditLog).where(AdminAuditLog.action == "travel_services.offer_review")
    )
    assert audit.metadata_json["method"] == "browser"
    config.klook_affiliate_id = "2"
    assert (
        await client.post(f"/api/v1/affiliates/offers/{offer['id']}/clickout")
    ).status_code == 404


async def test_destination_discovery_accepts_extended_city_but_not_a_product(fixture):
    _session, client, _config, _actor = fixture
    brand = await create_brand(client)
    target = "https://www.klook.com/zh-TW/search/?query=Hiroshima"
    created = await client.post(
        "/api/v1/admin/travel-services/destination-offers",
        json={
            "brand_id": brand["id"],
            "destination_id": "hiroshima",
            "module": "hotel",
            "target_url": target,
        },
    )
    assert created.status_code == 201, created.text
    identifier = created.json()["id"]
    review = await client.post(
        f"/api/v1/admin/travel-services/destination-offers/{identifier}/review",
        json={"version": 1, "status": "approved", "browser_verified": True, "evidence_url": target},
    )
    assert review.status_code == 200, review.text
    options = await client.get(
        "/api/v1/affiliates/destination-offers?destination_id=hiroshima&module=hotel"
    )
    assert len(options.json()["options"]) == 1
    assert options.json()["options"][0]["clickout_url"].endswith(
        f"/destination-offers/{identifier}/clickout?placement=destination"
    )
    click = await client.post(f"/api/v1/affiliates/destination-offers/{identifier}/clickout")
    assert click.status_code == 303, click.text
    assert click.headers["location"] == target + "&aid=" + AID


async def test_destination_offers_are_gated_and_labelled_per_surface(fixture):
    session, client, _config, _actor = fixture
    brand = await create_brand(client)
    target = "https://www.klook.com/zh-TW/search/?query=Hiroshima"
    created = await client.post(
        "/api/v1/admin/travel-services/destination-offers",
        json={
            "brand_id": brand["id"],
            "destination_id": "hiroshima",
            "module": "hotel",
            "target_url": target,
        },
    )
    identifier = created.json()["id"]
    review = await client.post(
        f"/api/v1/admin/travel-services/destination-offers/{identifier}/review",
        json={"version": 1, "status": "approved", "browser_verified": True, "evidence_url": target},
    )
    assert review.status_code == 200, review.text
    listing = "/api/v1/affiliates/destination-offers?destination_id=hiroshima&module=hotel"
    clickout = f"/api/v1/affiliates/destination-offers/{identifier}/clickout"

    # The content surfaces are off by default: the list is empty and the click refuses,
    # so a page that guessed the URL cannot route a click through a closed surface.
    assert (await client.get(listing + "&placement=guide")).json()["options"] == []
    assert (await client.post(clickout + "?placement=guide")).status_code == 404
    assert (await client.post(clickout + "?placement=evil")).status_code == 422
    assert await session.scalar(select(func.count()).select_from(AffiliateClick)) == 0

    row = await session.get(TravelServiceConfig, 1)
    row.data = {**row.data, "affiliate_placements": [*row.data["affiliate_placements"], "guide"]}
    await session.commit()

    options = (await client.get(listing + "&placement=guide")).json()["options"]
    assert [option["clickout_url"] for option in options] == [
        f"/api/travel/affiliates/destination-offers/{identifier}/clickout?placement=guide"
    ]
    click = await client.post(clickout + "?placement=guide")
    assert click.status_code == 303, click.text
    recorded = (await session.scalars(select(AffiliateClick))).one()
    assert recorded.placement == "guide"
    assert recorded.sub_id == "dst_hotel_hiroshima_zh-TW_guide"
    assert recorded.partner == "klook" and recorded.destination_id == "hiroshima"
    # Switching the surface off again also revokes the click, not only the listing.
    row.data = {**row.data, "affiliate_placements": ["destination"]}
    await session.commit()
    assert (await client.post(clickout + "?placement=guide")).status_code == 404


async def test_partner_offer_modules_follow_the_surface_switch(fixture):
    """A trip payload asks "which modules have something ready here?", never for the
    offers; the answer follows the same switch as the public list and the click."""
    from app.travel_services.service import partner_offer_modules

    session, client, config, _actor = fixture
    brand = await create_brand(client)
    for module, target in (
        ("transport", "https://www.klook.com/airport-transfers/city/28-tokyo-airport/"),
        ("activities", "https://www.klook.com/destination/c28-tokyo/1-things-to-do/"),
    ):
        created = await client.post(
            "/api/v1/admin/travel-services/destination-offers",
            json={
                "brand_id": brand["id"],
                "destination_id": "tokyo",
                "module": module,
                "target_url": target,
            },
        )
        review = await client.post(
            f"/api/v1/admin/travel-services/destination-offers/{created.json()['id']}/review",
            json={
                "version": 1,
                "status": "approved",
                "browser_verified": True,
                "evidence_url": target,
            },
        )
        assert review.status_code == 200, review.text
    # Canonical module order, not insertion order; `trip` is a legacy surface and on.
    assert await partner_offer_modules(session, config, "tokyo", "trip") == [
        "activities",
        "transport",
    ]
    # `share` is a content surface and off until an operator enables it.
    assert await partner_offer_modules(session, config, "tokyo", "share") == []
    assert await partner_offer_modules(session, config, None, "trip") == []
    assert await partner_offer_modules(session, config, "hiroshima", "trip") == []
    row = await session.get(TravelServiceConfig, 1)
    row.data = {**row.data, "affiliate_placements": [*row.data["affiliate_placements"], "share"]}
    await session.commit()
    assert await partner_offer_modules(session, config, "tokyo", "share") == [
        "activities",
        "transport",
    ]
    # The share page's clicks carry their own label once the surface is open.
    offers = (
        await client.get(
            "/api/v1/affiliates/destination-offers?destination_id=tokyo&module=transport"
            "&placement=share"
        )
    ).json()["options"]
    assert [offer["clickout_url"].rsplit("?", 1)[1] for offer in offers] == ["placement=share"]


async def test_direct_import_default_channel_and_replay_never_publish(fixture):
    session, client, config, _actor = fixture
    header = "source_key,kind,destination_id,title,source_url,brand,target_url,channel\n"
    csv = header + f"fixture:tour,tour,tokyo,Fixture,{TARGET},klook,{TARGET},klook_direct\n"
    preview = await client.post("/api/v1/admin/travel-services/imports/preview", json={"csv": csv})
    assert preview.status_code == 200, preview.text
    identifier = preview.json()["id"]
    applied = await client.post(f"/api/v1/admin/travel-services/imports/{identifier}/commit")
    assert applied.status_code == 200, applied.text
    replay = await client.post(f"/api/v1/admin/travel-services/imports/{identifier}/commit")
    assert replay.json() == applied.json()
    brand = await session.scalar(select(TravelServiceBrand))
    assert (brand.channel, brand.project_id, brand.approval, brand.enabled) == (
        "klook_direct",
        AID,
        "unknown",
        False,
    )
    product = await session.scalar(select(TravelServiceProduct))
    offer = await session.scalar(select(TravelServiceOffer))
    assert product.status == offer.status == "pending"
    assert await session.scalar(select(func.count()).select_from(TravelServiceOffer)) == 1
    legacy_csv = header + f"fixture:tour,tour,tokyo,Fixture,{TARGET},klook,{TARGET},\n"
    legacy = TravelServiceImport(source="csv", rows_json=parse_csv(legacy_csv), result_json={})
    session.add(legacy)
    await session.flush()
    await commit_import(
        session,
        legacy.id,
        config.travelpayouts_project_id,
        klook_affiliate_id=config.klook_affiliate_id,
    )
    assert await session.scalar(select(func.count()).select_from(TravelServiceBrand)) == 2
    assert await session.scalar(select(func.count()).select_from(TravelServiceOffer)) == 2


@pytest.mark.parametrize(
    "option_url,eligible",
    [
        (HOTEL, True),
        ("https://www.klook.com/zh-TW/hotels/detail/285841-hotel-gracery-shinjuku/", True),
        (HOTEL + "?check_in=2026-11-11", False),
        (HOTEL.replace("285841", "285842"), False),
    ],
)
async def test_hotel_booking_option_prefers_own_direct_channel_and_clicks_exact_identity(
    fixture, option_url, eligible
):
    session, client, config, _actor = fixture
    brand = TravelServiceBrand(
        channel="klook_direct",
        project_id=AID,
        code="klook",
        approval="approved",
        enabled=True,
        verified_at=NOW,
    )
    hotel = TravelServiceProduct(
        source_key="fixture:hotel",
        kind="hotel",
        destination_id="tokyo",
        title="Fixture hotel",
        source_url=HOTEL,
        names_json={},
        status="approved",
        verified_at=NOW,
        facts=Facts(latitude=35.6955, longitude=139.7019).model_dump(),
    )
    session.add_all([brand, hotel])
    await session.flush()
    option = HotelBookingOption(
        product_id=hotel.id,
        provider="klook",
        url=option_url,
        evidence_url=option_url,
        discovery_status="found",
        status="approved",
        verified_at=NOW,
        health_status="unconfirmed",
        identity_note="Browser fixture review",
    )
    offer = TravelServiceOffer(
        product_id=hotel.id,
        brand_id=brand.id,
        target_url="https://www.klook.com/zh-TW/hotels/detail/285841-hotel-gracery-shinjuku/",
        scope="product",
        status="approved",
        verified_at=NOW,
        verification_context=channel_context(config, "klook_direct"),
    )
    hotel.hotel_options.append(option)
    session.add(offer)
    await session.commit()
    public = await client.get("/api/v1/travel-services?destination_id=tokyo&type=hotel")
    assert public.status_code == 200, public.text
    if not eligible:
        assert public.json()["items"][0]["booking_options"] == []
        clicked = await client.post(
            f"/api/v1/travel-services/{hotel.id}/booking-options/{option.id}/clickout"
        )
        assert clicked.status_code == 503
        assert await session.scalar(select(func.count()).select_from(AffiliateClick)) == 0
        return
    assert public.json()["items"][0]["booking_options"][0]["mode"] == "affiliate"
    clicked = await client.post(
        f"/api/v1/travel-services/{hotel.id}/booking-options/{option.id}/clickout"
    )
    assert clicked.status_code == 303, clicked.text
    assert clicked.headers["location"] == offer.target_url + "?aid=" + AID
    assert (await session.scalar(select(AffiliateClick))).partner == "klook"
    assert (await session.scalar(select(HotelBookingClick))).mode == "affiliate"


def migration_module():
    path = Path(__file__).parents[1] / "migrations/versions/0064_klook_affiliate_channels.py"
    spec = importlib.util.spec_from_file_location("klook_channel_migration", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("fresh", [False, True])
def test_migration_guards_legacy_and_current_metadata(monkeypatch, fresh):
    module = migration_module()
    operations: list[str] = []

    class Inspector:
        def get_columns(self, _name):
            return [{"name": "channel"}] if fresh else []

        def get_unique_constraints(self, _name):
            return [
                {
                    "name": "uq_service_brand_channel_project"
                    if fresh
                    else "uq_service_brand_project"
                }
            ]

        def get_check_constraints(self, _name):
            return (
                [
                    {"name": value}
                    for value in ("ck_service_brand_channel", "ck_service_brand_direct_klook")
                ]
                if fresh
                else []
            )

    class Ops:
        def get_bind(self):
            return self

        def __getattr__(self, name):
            return lambda *_args, **_kwargs: operations.append(name)

    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    monkeypatch.setattr(module.sa, "inspect", lambda _bind: Inspector())
    monkeypatch.setattr(module, "op", Ops())
    module.upgrade()
    if fresh:
        assert operations == []
    else:
        assert operations == [
            "add_column",
            "drop_constraint",
            "create_unique_constraint",
            "create_check_constraint",
            "create_check_constraint",
        ]


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.parametrize("fresh", [False, True])
async def test_postgres_channel_migration_preserves_ids_and_refuses_unsafe_downgrade(
    monkeypatch, fresh
):
    from app.db import engine

    module = migration_module()
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)
    await engine.dispose(close=False)
    async with engine.connect() as connection, connection.begin():
        schema = "klook_channels_" + uuid4().hex
        await connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
        await connection.execute(sa.text(f'SET LOCAL search_path TO "{schema}"'))

        def verify(sync):
            if fresh:
                # This is the same current metadata path used by 0001_initial.
                TravelServiceBrand.__table__.create(sync)
            else:
                # Frozen 0063-era table: the column and new constraints do not exist.
                table = sa.Table(
                    "travel_service_brands",
                    sa.MetaData(),
                    sa.Column("id", sa.Uuid(), primary_key=True),
                    sa.Column("project_id", sa.String(32), nullable=False),
                    sa.Column("code", sa.String(64), nullable=False),
                    sa.Column("approval", sa.String(16), nullable=False),
                    sa.Column("enabled", sa.Boolean(), nullable=False),
                    sa.Column("version", sa.Integer(), nullable=False),
                    sa.Column("evidence_url", sa.String(2048)),
                    sa.Column("verified_at", sa.DateTime(timezone=True)),
                    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
                    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
                    sa.UniqueConstraint("project_id", "code", name="uq_service_brand_project"),
                    sa.CheckConstraint(
                        "approval IN ('unknown','pending','approved','rejected')",
                        name="ck_brand_approval",
                    ),
                )
                table.create(sync)
            table = sa.Table("travel_service_brands", sa.MetaData(), autoload_with=sync)
            identifier = uuid4()
            original = dict(
                id=identifier,
                project_id=AID,
                code="klook",
                approval="approved",
                enabled=True,
                version=7,
                evidence_url="https://app.travelpayouts.com/fixture",
                verified_at=NOW,
                created_at=NOW,
                updated_at=NOW,
            )
            sync.execute(table.insert().values(**original))
            with Operations.context(MigrationContext.configure(sync)):
                module.upgrade()
                module.upgrade()
                upgraded = sa.Table("travel_service_brands", sa.MetaData(), autoload_with=sync)
                row = (
                    sync.execute(sa.select(upgraded).where(upgraded.c.id == identifier))
                    .mappings()
                    .one()
                )
                assert row["channel"] == "travelpayouts"
                assert all(row[key] == value for key, value in original.items())
                direct_id = uuid4()
                sync.execute(
                    upgraded.insert().values(
                        **{
                            **original,
                            "id": direct_id,
                            "channel": "klook_direct",
                            "evidence_url": "https://affiliate.klook.com/zh-TW/my_account",
                        }
                    )
                )
                assert sync.scalar(sa.select(sa.func.count()).select_from(upgraded)) == 2
                with pytest.raises(RuntimeError, match="direct affiliate enrollments"):
                    module.downgrade()
                assert sync.scalar(sa.select(sa.func.count()).select_from(upgraded)) == 2
                # Remove only the fixture direct row before testing a lossless legacy downgrade.
                sync.execute(upgraded.delete().where(upgraded.c.id == direct_id))
                module.downgrade()
                legacy = sa.Table("travel_service_brands", sa.MetaData(), autoload_with=sync)
                assert "channel" not in legacy.c
                assert sync.scalar(sa.select(legacy.c.id)) == identifier

        await connection.run_sync(verify)
        await connection.rollback()  # The isolated schema and every fixture row are rolled back.
    await engine.dispose()
