from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
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
from app.problems import AppError
from app.travel_services import admin, hotel_admin
from app.travel_services.schemas import CatalogConfig, ConfigInput, HotelConfigPatch

NOW = datetime.now(UTC)
ALLeZ = {"enabled": True, "aid": "mokaair", "enabled_providers": ["booking"]}


def actor(*roles: str) -> User:
    user = User(id=uuid4(), email="stay22-operator@example.test", is_admin=False)
    user.__dict__["_admin_roles_cache"] = frozenset(roles)
    return user


@pytest.fixture
async def session(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite://")

    @event.listens_for(engine.sync_engine, "connect")
    def advisory_stub(connection: Any, _record: Any) -> None:
        connection.create_function("pg_advisory_xact_lock", 1, lambda _key: 0)

    tables = [
        model.__table__
        for model in (
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
    ]
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    monkeypatch.setattr(admin, "load_runtime_settings", AsyncMock(return_value=Settings()))
    async with async_sessionmaker(engine, expire_on_commit=False)() as database:
        yield database
    await engine.dispose()


def hotel(key: str = "hotel", *, old: bool = False, query: bool = False) -> TravelServiceProduct:
    product = TravelServiceProduct(
        id=uuid4(),
        source_key=key,
        kind="hotel",
        title=key,
        destination_id="tokyo",
        status="approved",
        facts={},
        names_json={},
        source_url="https://hotel.example.com/",
        hotel_options=[],
    )
    product.hotel_options.append(
        HotelBookingOption(
            id=uuid4(),
            provider="booking",
            url=f"https://www.booking.com/hotel/jp/{key}.html"
            + ("?checkin=2027-01-01" if query else ""),
            evidence_url="https://hotel.example.com/location",
            identity_note="Verified same property",
            status="approved",
            discovery_status="found",
            verified_at=NOW - timedelta(days=31) if old else NOW,
            health_status="healthy",
            version=1,
        )
    )
    return product


def config() -> CatalogConfig:
    return CatalogConfig(
        public_enabled=True, enabled_kinds=["hotel"], enabled_destinations=["tokyo"]
    )


@pytest.mark.parametrize(
    "roles,fields,allowed",
    [
        (("content",), {"stay22": ALLeZ}, False),
        (("viewer",), {"stay22": ALLeZ}, False),
        (("operations",), {"stay22": ALLeZ}, True),
        (("owner",), {"stay22": ALLeZ}, True),
        (("operations",), {"stay22": ALLeZ, "hotel_enabled": True}, False),
        (("content", "operations"), {"stay22": ALLeZ, "hotel_enabled": True}, True),
        (("content",), {"hotel_enabled": True}, True),
    ],
)
async def test_field_scoped_capability_boundary(roles, fields, allowed) -> None:
    payload = HotelConfigPatch(version=0, **fields)
    if allowed:
        assert await hotel_admin.hotel_config_user(payload, actor(*roles))
    else:
        with pytest.raises(AppError) as denied:
            await hotel_admin.hotel_config_user(payload, actor(*roles))
        assert denied.value.status == 403
        assert denied.value.code == "admin_capability_required"


async def test_route_dependency_enforces_stay22_before_database(session: AsyncSession) -> None:
    application = FastAPI()
    application.include_router(hotel_admin.router)
    user = actor("content")
    application.dependency_overrides[current_user] = lambda: user
    application.dependency_overrides[get_session] = lambda: session

    @application.exception_handler(AppError)
    async def app_error(_request, error):
        from fastapi.responses import JSONResponse

        return JSONResponse({"code": error.code}, status_code=error.status)

    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        response = await client.patch("/admin/hotels/config", json={"version": 0, "stay22": ALLeZ})
        assert response.status_code == 403
        assert await session.get(TravelServiceConfig, 1) is None
        user.__dict__["_admin_roles_cache"] = frozenset({"operations"})
        response = await client.patch("/admin/hotels/config", json={"version": 0, "stay22": ALLeZ})
        assert response.status_code == 200
        assert response.json() == {"version": 1}


async def test_stay22_patch_is_versioned_audited_and_preserves_catalog(
    session: AsyncSession,
) -> None:
    row = TravelServiceConfig(id=1, version=5, data={**config().model_dump(), "future": "keep"})
    session.add(row)
    await session.commit()
    await hotel_admin.patch_config(
        HotelConfigPatch(version=5, stay22=ALLeZ), actor("operations"), session
    )
    assert row.data["stay22"] == ALLeZ
    assert row.data["future"] == "keep"
    assert row.data["enabled_kinds"] == ["hotel"]
    log = await session.scalar(select(AdminAuditLog))
    assert log is not None and log.metadata_json == {"fields": ["stay22"]}
    with pytest.raises(AppError) as stale:
        await hotel_admin.patch_config(
            HotelConfigPatch(version=5, stay22=ALLeZ), actor("owner"), session
        )
    assert stale.value.code == "service_version_conflict"


async def test_older_forms_preserve_stay22_and_cannot_replace_without_capability(
    session: AsyncSession,
) -> None:
    row = TravelServiceConfig(id=1, version=1, data={**config().model_dump(), "stay22": ALLeZ})
    session.add(row)
    await session.commit()
    await hotel_admin.patch_config(
        HotelConfigPatch(version=1, hotel_enabled=False), actor("content"), session
    )
    await admin.put_config(
        ConfigInput(version=2, enabled_kinds=["hotel"]), actor("content"), session
    )
    assert row.data["stay22"] == ALLeZ
    with pytest.raises(AppError) as denied:
        await admin.put_config(
            ConfigInput(version=3, stay22={"enabled": False}), actor("content"), session
        )
    assert denied.value.status == 403
    assert row.version == 3


def test_readiness_is_potential_not_tracking_or_global_enabled() -> None:
    product = hotel()
    assert not config().stay22.enabled
    assert (
        admin.stay22_readiness_state(product, "booking", config(), NOW, set()) == "stay22_capable"
    )
    assert admin.stay22_readiness_state(product, "agoda", config(), NOW, set()) == "missing_link"
    target = product.hotel_options[0].url
    assert target
    assert (
        admin.stay22_readiness_state(product, "booking", config(), NOW, {("booking", target)})
        == "existing_affiliate"
    )
    assert (
        admin.stay22_readiness_state(hotel(old=True), "booking", config(), NOW, set())
        == "review_expired"
    )
    assert (
        admin.stay22_readiness_state(hotel(query=True), "booking", config(), NOW, set())
        == "blocked"
    )


async def test_readiness_counts_not_paginated_and_filter_matches_actual_products(
    session: AsyncSession,
) -> None:
    # Keep the UTC-aware fixture objects in the identity map: SQLite discards
    # tzinfo when loading rows, unlike the production PostgreSQL timestamptz.
    products = [hotel("ready"), hotel("expired", old=True), hotel("tracking", query=True)]
    session.add_all(products)
    session.add(TravelServiceConfig(id=1, version=1, data=config().model_dump()))
    await session.commit()
    response = await hotel_admin.overview(
        actor("content"),
        session,
        offset=0,
        limit=1,
        booking_provider="booking",
        booking_readiness="stay22_capable",
    )
    assert [product["title"] for product in response["products"]] == ["ready"]
    counts = response["stay22_readiness"][0]
    assert counts == {
        "provider": "booking",
        "existing_affiliate": 0,
        "stay22_capable": 1,
        "missing_link": 0,
        "review_expired": 1,
        "blocked": 1,
    }
    assert response["can_manage_stay22"] is False
    response = await hotel_admin.overview(
        actor("owner"),
        session,
        offset=0,
        limit=1,
        booking_provider="agoda",
        booking_readiness="missing_link",
    )
    assert len(response["products"]) == 1
    assert response["stay22_readiness"][1]["missing_link"] == 3
    assert response["can_manage_stay22"] is True
    assert response["config"]["stay22"]["enabled"] is False
