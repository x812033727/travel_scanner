"""Isolated script inputs use reviewed public data, never live affiliate traffic."""

from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db import Base, get_session
from app.models import (
    AdminAuditLog,
    HotelBookingOption,
    TravelServiceConfig,
    TravelServiceProduct,
    User,
)
from app.problems import AppError, app_error_handler
from app.travel_services import hotel_admin, router, stay22_script
from app.travel_services.schemas import CatalogConfig, HotelConfigPatch, Stay22Config

LMA_ID = "0123456789abcdef01234567"


def active_config() -> CatalogConfig:
    return CatalogConfig(
        public_enabled=True,
        direct_hotel_links_enabled=True,
        enabled_kinds=["hotel"],
        enabled_destinations=["tokyo"],
        stay22=Stay22Config(enabled=True, integration_mode="script", lma_id=LMA_ID),
    )


def test_legacy_config_keeps_allez_defaults_without_account_script_id() -> None:
    config = Stay22Config(enabled=True, aid="fixture", enabled_providers=["booking"])
    assert config.integration_mode == "allez"
    assert config.lma_id is None
    assert active_config().stay22.enabled_providers == []


@pytest.mark.parametrize("value", ["", "x" * 24, "ABCDEF012345678901234567", "a" * 23,
                                     "a" * 25, "<script>alert(1)</script>"])
def test_script_id_rejects_noncanonical_or_injected_values(value: str) -> None:
    with pytest.raises(ValidationError):
        Stay22Config(integration_mode="script", lma_id=value)


def test_enabled_script_requires_id_but_disabled_can_be_preconfigured() -> None:
    with pytest.raises(ValidationError):
        Stay22Config(enabled=True, integration_mode="script")
    assert Stay22Config(integration_mode="script").lma_id is None
    with pytest.raises(ValidationError):
        Stay22Config(integration_mode="arbitrary", lma_id=LMA_ID)
    with pytest.raises(ValidationError):
        Stay22Config(enabled="true", integration_mode="script", lma_id=LMA_ID)


@pytest.fixture
async def script_api(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[tuple]:
    engine = create_async_engine("sqlite+aiosqlite://")

    @event.listens_for(engine.sync_engine, "connect")
    def advisory_stub(connection: Any, _record: Any) -> None:
        connection.create_function("pg_advisory_xact_lock", 1, lambda _key: 0)

    tables = [model.__table__ for model in (
        TravelServiceProduct, HotelBookingOption, TravelServiceConfig, AdminAuditLog,
    )]
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    try:
        async with async_sessionmaker(engine, expire_on_commit=False)() as session:
            option = HotelBookingOption(
                id=uuid4(), provider="booking",
                url="https://www.booking.com/hotel/jp/fixture.html",
                evidence_url="https://www.booking.com/hotel/jp/fixture.html",
                property_id="internal-reviewed-identity", identity_note="Private reviewer notes",
                status="approved", discovery_status="found", health_status="healthy",
                verified_at=datetime.now(UTC), version=1,
            )
            product = TravelServiceProduct(
                id=uuid4(), source_key=uuid4().hex, kind="hotel", destination_id="tokyo",
                title="Reviewed hotel", names_json={"en": "Public English hotel"},
                source_url="https://hotel.example.test/", status="approved",
                verified_at=datetime.now(UTC), hotel_options=[option],
            )
            config = active_config()
            row = TravelServiceConfig(id=1, version=1, data=config.model_dump())
            session.add_all([product, row])
            await session.commit()
            limiter = AsyncMock()
            monkeypatch.setattr(router, "enforce_named_rate_limit", limiter)
            monkeypatch.setattr(router, "catalog_config", AsyncMock(return_value=(config, 1)))
            # DNS only is fixed; hotel identity and published/review gates are real.
            safe_target = AsyncMock(side_effect=lambda value: value.url)
            monkeypatch.setattr(stay22_script, "safe_click_target", safe_target)
            app = FastAPI()
            app.add_exception_handler(AppError, app_error_handler)
            app.include_router(router.router, prefix="/api/v1")
            app.dependency_overrides[get_session] = lambda: session
            async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
                yield client, session, product, option, config, safe_target, limiter
    finally:
        await engine.dispose()


def options_url(product: TravelServiceProduct) -> str:
    return f"/api/v1/travel-services/{product.id}/stay22-script-options"


async def test_config_only_reveals_public_identity_no_aid_or_raw_settings(script_api) -> None:
    client, _, _, _, config, *_ = script_api
    config.stay22.aid = "private-config-fixture"
    response = await client.get("/api/v1/travel-services/stay22-script-config")
    assert response.status_code == 200
    assert response.json() == {"enabled": True, "integration_mode": "script", "lma_id": LMA_ID}
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["referrer-policy"] == "no-referrer"
    ordinary_config = await client.get("/api/v1/travel-services/config")
    assert "stay22" not in ordinary_config.json()
    assert LMA_ID not in ordinary_config.text


@pytest.mark.parametrize("gate", ["public", "direct", "hotels", "master", "mode"])
async def test_inactive_config_never_reveals_id_or_hrefs(script_api, gate: str) -> None:
    client, _, product, _, config, safe_target, _ = script_api
    if gate == "public":
        config.public_enabled = False
    elif gate == "direct":
        config.direct_hotel_links_enabled = False
    elif gate == "hotels":
        config.enabled_kinds = []
    elif gate == "master":
        config.stay22.enabled = False
    else:
        config.stay22.integration_mode = "allez"
    response = await client.get("/api/v1/travel-services/stay22-script-config")
    assert response.json()["enabled"] is False
    assert response.json()["lma_id"] is None
    response = await client.get(options_url(product))
    assert response.status_code == 404
    assert "booking.com" not in response.text
    safe_target.assert_not_awaited()


def test_disabling_direct_links_does_not_disable_independent_native_allez() -> None:
    from app.travel_services.stay22 import booking_channel

    config = active_config()
    config.direct_hotel_links_enabled = False
    config.stay22.enabled_providers = ["booking"]
    option = HotelBookingOption(
        provider="booking", url="https://www.booking.com/hotel/jp/fixture.html"
    )
    assert not stay22_script.script_config(config, tracking_allowed=True)["enabled"]
    assert booking_channel(option, config, has_offer=False) == "stay22"


@pytest.mark.parametrize("headers", [{"dnt": "1"}, {"sec-gpc": "1"}])
async def test_privacy_disables_script_and_original_url_exposure(script_api, headers) -> None:
    client, _, product, _, _, safe_target, _ = script_api
    config = await client.get("/api/v1/travel-services/stay22-script-config", headers=headers)
    assert config.json() == {"enabled": False, "integration_mode": "script", "lma_id": None}
    response = await client.get(options_url(product), headers=headers)
    assert response.status_code == 404 and "booking.com" not in response.text
    safe_target.assert_not_awaited()


async def test_options_contain_only_safe_public_identity_and_do_not_mutate(script_api) -> None:
    client, session, product, option, _, safe_target, limiter = script_api
    old_version, old_url = product.version, option.url
    response = await client.get(options_url(product), headers={"x-travel-locale": "en"})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "title": "Public English hotel", "destination_id": "tokyo", "options": [{
            "id": str(option.id), "provider": "booking", "name": "Booking.com", "url": old_url,
        }],
    }
    assert "allez" not in response.text and "lma_id" not in response.text
    assert "Private reviewer" not in response.text and "internal-reviewed" not in response.text
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["referrer-policy"] == "no-referrer"
    safe_target.assert_awaited_once_with(option)
    limiter.assert_awaited_once()
    await session.refresh(product)
    assert product.version == old_version and option.url == old_url


@pytest.mark.parametrize("gate", ["destination", "product", "type", "missing"])
async def test_unpublished_products_never_reveal_hrefs(script_api, gate: str) -> None:
    client, session, product, _, config, safe_target, _ = script_api
    url = options_url(product)
    if gate == "destination":
        config.enabled_destinations = []
    elif gate == "product":
        product.status = "pending"
    elif gate == "type":
        product.kind = "tour"
    else:
        url = f"/api/v1/travel-services/{uuid4()}/stay22-script-options"
    await session.commit()
    response = await client.get(url)
    assert response.status_code == 404
    assert "booking.com" not in response.text
    safe_target.assert_not_awaited()


@pytest.mark.parametrize("field,value", [
    ("provider", "unregistered-platform"),
    ("status", "pending"), ("status", "disabled"),
    ("discovery_status", "unconfirmed"), ("health_status", "unsafe"),
    ("health_status", "unavailable"), ("verified_at", None),
    ("verified_at", datetime.now(UTC) - timedelta(days=31)),
    ("verified_at", datetime.now(UTC) + timedelta(days=1)),
    ("url", "https://attacker.example/hotel/jp/fixture.html"),
    ("url", "https://www.booking.com/searchresults.html"),
    ("url", "https://www.booking.com/hotel/jp/fixture.html?checkin=2030-01-01"),
    ("url", "https://www.booking.com/hotel/jp/fixture.html?sid=secret"),
    ("url", "https://www.booking.com/hotel/jp/fixture.html#private"),
    ("url", "http://www.booking.com/hotel/jp/fixture.html"),
])
async def test_review_identity_and_original_url_gates(script_api, field, value) -> None:
    client, session, product, option, _, safe_target, _ = script_api
    setattr(option, field, value)
    await session.commit()
    response = await client.get(options_url(product))
    assert response.status_code == 200, response.text
    assert response.json()["options"] == []
    safe_target.assert_not_awaited()


async def test_dns_failure_is_partial_and_official_stays_plain_original(script_api) -> None:
    client, session, product, option, _, safe_target, _ = script_api
    official = HotelBookingOption(
        id=uuid4(), provider="official", url="https://fixture-hotel.example/",
        evidence_url="https://fixture-hotel.example/about", identity_note="Reviewed official site",
        status="approved", discovery_status="found", health_status="healthy",
        verified_at=datetime.now(UTC), version=1,
    )
    product.hotel_options.append(official)
    await session.commit()

    def resolve(value):
        if value.id == option.id:
            raise AppError(503, "service_link_unavailable", "unavailable")
        return value.url

    safe_target.side_effect = resolve
    response = await client.get(options_url(product))
    assert response.json()["options"] == [{
        "id": str(official.id), "provider": "official", "name": "Official website",
        "url": official.url,
    }]


@pytest.mark.parametrize("url,property_id,exposed", [
    ("https://travel.rakuten.co.jp/HOTEL/187836/187836.html", "187836", False),
    ("https://travel.rakuten.com/usa/en-us/hotel_info_item/cnt_japan/sub_tokyo/"
     "cty_shinjuku_ward/10123456789012/", "10123456789012", True),
])
async def test_rakuten_japan_is_direct_only_while_global_script_behavior_is_preserved(
    script_api, url, property_id, exposed
) -> None:
    client, session, product, booking, config, safe_target, _ = script_api
    rakuten = HotelBookingOption(
        id=uuid4(), provider="rakuten", url=url, evidence_url=url,
        property_id=property_id, identity_note="Reviewed exact hotel",
        status="approved", discovery_status="found", health_status="healthy",
        verified_at=datetime.now(UTC), version=1,
    )
    product.hotel_options.append(rakuten)
    await session.commit()
    # The Japan option is ready for ordinary first-party booking, not rejected
    # merely because its platform namespace is excluded from the SDK document.
    assert stay22_script.ready_option(product, rakuten, config, datetime.now(UTC))
    response = await client.get(options_url(product))
    assert response.status_code == 200, response.text
    assert [item["provider"] for item in response.json()["options"]] == (
        ["booking", "rakuten"] if exposed else ["booking"]
    )
    assert (url in response.text) is exposed
    if exposed:
        assert safe_target.await_count == 2
    else:
        safe_target.assert_awaited_once_with(booking)


async def test_real_target_validator_checks_dns_without_fetching_booking_pages(
    script_api, monkeypatch
) -> None:
    from app.catalog_review import evidence
    from app.travel_services.hotel_options import safe_click_target

    client, _, product, option, _, *_ = script_api
    dns = AsyncMock(return_value=None)
    monkeypatch.setattr(stay22_script, "safe_click_target", safe_click_target)
    monkeypatch.setattr(evidence, "public_request_target", dns)
    response = await client.get(options_url(product))
    assert response.json()["options"] == []
    dns.assert_awaited_once_with(option.url)


def operator() -> User:
    user = User(id=uuid4(), email="operator@example.test", is_admin=False)
    user.__dict__["_admin_roles_cache"] = frozenset({"operations"})
    return user


async def test_legacy_nested_patch_preserves_script_fields_and_is_audited(script_api) -> None:
    _, session, _, _, _, *_ = script_api
    row = await session.get(TravelServiceConfig, 1)
    await hotel_admin.patch_config(HotelConfigPatch(version=1, stay22={
        "enabled": True, "aid": "new-fixture", "enabled_providers": ["booking"],
    }), operator(), session)
    assert row.data["stay22"] == {
        "enabled": True, "aid": "new-fixture", "enabled_providers": ["booking"],
        "integration_mode": "script", "lma_id": LMA_ID,
    }
    assert row.version == 2
    assert (await session.scalar(select(AdminAuditLog))).metadata_json == {"fields": ["stay22"]}
    assert row.data["public_enabled"] and row.data["enabled_destinations"] == ["tokyo"]


async def test_partial_patch_validates_merged_config_before_writing(script_api) -> None:
    _, session, _, _, _, *_ = script_api
    row = await session.get(TravelServiceConfig, 1)
    with pytest.raises(AppError) as error:
        await hotel_admin.patch_config(
            HotelConfigPatch(version=1, stay22={"lma_id": None}), operator(), session
        )
    assert error.value.code == "stay22_config_invalid"
    assert row.version == 1 and row.data["stay22"]["lma_id"] == LMA_ID
    assert await session.scalar(select(AdminAuditLog)) is None


async def test_disable_preserves_existing_channel_settings_and_script_identity(script_api) -> None:
    _, session, _, _, _, *_ = script_api
    row = await session.get(TravelServiceConfig, 1)
    await hotel_admin.patch_config(
        HotelConfigPatch(version=1, stay22={"enabled": False}), operator(), session
    )
    assert row.data["stay22"]["enabled"] is False
    assert row.data["stay22"]["lma_id"] == LMA_ID
    assert row.data["stay22"]["integration_mode"] == "script"
