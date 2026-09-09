"""First-party HTTP clickouts with real storage, no external affiliate requests."""

from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import Settings
from app.db import Base, get_session
from app.models import (
    AffiliateClick,
    HotelBookingClick,
    HotelBookingOption,
    TravelServiceBrand,
    TravelServiceOffer,
    TravelServiceProduct,
)
from app.problems import AppError, app_error_handler
from app.travel_services import hotel_options, router
from app.travel_services.schemas import CatalogConfig, Stay22Config
from app.travel_services.stay22 import BOOKING_PLACEMENTS


@pytest.fixture
async def click_api(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[tuple]:
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = [
        TravelServiceProduct.__table__,
        HotelBookingOption.__table__,
        HotelBookingClick.__table__,
        AffiliateClick.__table__,
        TravelServiceBrand.__table__,
        TravelServiceOffer.__table__,
    ]
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    try:
        async with async_sessionmaker(engine, expire_on_commit=False)() as session:
            option = HotelBookingOption(
                id=uuid4(),
                provider="booking",
                url="https://www.booking.com/hotel/jp/fixture.html",
                evidence_url="https://www.booking.com/hotel/jp/fixture.html",
                property_id="reviewed-fixture",
                identity_note="Same hotel manually reviewed",
                status="approved",
                discovery_status="found",
                health_status="healthy",
                verified_at=datetime.now(UTC),
                version=1,
            )
            product = TravelServiceProduct(
                id=uuid4(),
                source_key=uuid4().hex,
                kind="hotel",
                destination_id="tokyo",
                title="Reviewed hotel",
                source_url="https://hotel.example.test/",
                status="approved",
                verified_at=datetime.now(UTC),
                hotel_options=[option],
            )
            session.add(product)
            await session.commit()
            config = CatalogConfig(
                public_enabled=True,
                enabled_kinds=["hotel"],
                enabled_destinations=["tokyo"],
                direct_hotel_links_enabled=True,
                stay22=Stay22Config(enabled=True, aid="fixture-aid", enabled_providers=["booking"]),
            )
            monkeypatch.setattr(router, "catalog_config", AsyncMock(return_value=(config, None)))
            monkeypatch.setattr(router, "load_runtime_settings", AsyncMock(return_value=Settings()))
            monkeypatch.setattr(router, "enforce_named_rate_limit", AsyncMock())
            monkeypatch.setattr(router, "get_redis", lambda: None)
            monkeypatch.setattr(hotel_options, "matching_offer", AsyncMock(return_value=None))
            # DNS only is stubbed; review, exact identity, channel, serialization and
            # click records go through the actual service implementation.
            monkeypatch.setattr(
                hotel_options, "safe_click_target", AsyncMock(side_effect=lambda opt: opt.url)
            )
            app = FastAPI()
            app.add_exception_handler(AppError, app_error_handler)
            app.include_router(router.router, prefix="/api/v1")
            app.dependency_overrides[get_session] = lambda: session
            async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
                yield client, session, product, option, config
    finally:
        await engine.dispose()


def endpoint(product, option) -> str:
    return (
        f"/api/v1/travel-services/{product.id}/booking-options/{option.id}/clickout?placement=trip"
    )


async def test_http_form_full_dates_and_minimal_persisted_click(click_api) -> None:
    client, session, product, option, _ = click_api
    original = (option.url, option.version, product.version, option.identity_note)
    result = await client.post(
        endpoint(product, option),
        data={
            "check_in": "2030-11-01",
            "check_out": "2030-11-30",
            "adults": "2",
            "children": "1",
        },
    )
    assert result.status_code == 303, result.text
    url = urlsplit(result.headers["location"])
    assert url.netloc == "www.stay22.com"
    assert url.path == "/allez/booking"
    query = parse_qs(url.query)
    assert query["checkout"] == ["2030-11-30"]
    assert query["link"] == [option.url]
    assert query["adults"] == ["2"] and query["children"] == ["1"]
    assert set(query) == {
        "aid",
        "link",
        "campaign",
        "lang",
        "currency",
        "checkin",
        "checkout",
        "adults",
        "children",
    }
    assert result.headers["cache-control"] == "no-store"
    assert result.headers["referrer-policy"] == "no-referrer"
    click = await session.scalar(select(AffiliateClick))
    assert click.partner == "stay22" and click.brand == "booking" and click.status == "redirected"
    assert click.user_id is click.trip_id is click.search_id is None
    assert str(product.id) not in query["campaign"][0]
    booking_click = await session.scalar(select(HotelBookingClick))
    assert booking_click.mode == "affiliate" and not booking_click.fallback
    assert original == (option.url, option.version, product.version, option.identity_note)


@pytest.mark.parametrize("headers", [{"dnt": "1"}, {"sec-gpc": "1"}])
async def test_privacy_signal_direct_fallback_without_affiliate_audit(click_api, headers) -> None:
    client, session, product, option, _ = click_api
    response = await client.post(endpoint(product, option), headers=headers)
    assert response.status_code == 303
    assert response.headers["location"] == option.url
    assert await session.scalar(select(AffiliateClick)) is None
    assert (await session.scalar(select(HotelBookingClick))).mode == "direct"


async def test_click_rechecks_feature_and_direct_switches(click_api) -> None:
    client, _, product, option, config = click_api
    config.stay22.enabled = False
    config.direct_hotel_links_enabled = False
    response = await client.post(endpoint(product, option))
    assert response.status_code == 503
    config.stay22.enabled = True
    assert (await client.post(endpoint(product, option))).status_code == 303


async def test_existing_affiliate_failure_never_changes_commission_channel(
    click_api, monkeypatch
) -> None:
    client, session, product, option, _ = click_api
    brand = TravelServiceBrand(
        id=uuid4(), code="booking", channel="travelpayouts", project_id="fixture"
    )
    session.add(brand)
    await session.commit()
    offer = TravelServiceOffer(id=uuid4(), brand_id=brand.id, version=1)
    monkeypatch.setattr(hotel_options, "matching_offer", AsyncMock(return_value=offer))
    resolver = AsyncMock(side_effect=TimeoutError())
    monkeypatch.setattr(router, "resolve_offer_target", resolver)
    response = await client.post(endpoint(product, option))
    assert response.status_code == 303
    assert response.headers["location"] == option.url
    assert await session.scalar(select(AffiliateClick)) is None
    assert (await session.scalar(select(HotelBookingClick))).fallback is True
    resolver.return_value = "https://tp.st/fixture"
    resolver.side_effect = None
    response = await client.post(endpoint(product, option))
    assert response.headers["location"] == "https://tp.st/fixture"
    assert (await session.scalar(select(AffiliateClick))).partner == "travelpayouts"


@pytest.mark.parametrize(
    "body",
    [
        {"check_in": "2030-11-01"},
        {"check_in": "2030-11-03", "check_out": "2030-11-01"},
        {"check_in": "2000-11-01", "check_out": "2000-11-02"},
        {"adults": True},
        {"adults": 0},
        {"adults": "2"},
        {"children": -1},
        {"adults": 10},
        {"link": "https://evil.test"},
        {"aid": "attacker"},
        {"channel": "stay22"},
        {"rooms": 2},
        {"children_ages": [7]},
        [],
    ],
)
async def test_invalid_context_never_clicks_or_mutates(click_api, body) -> None:
    client, session, product, option, _ = click_api
    response = await client.post(endpoint(product, option), json=body)
    assert response.status_code == 422, response.text
    assert response.json()["code"] == "hotel_booking_context_invalid"
    assert await session.scalar(select(HotelBookingClick)) is None


@pytest.mark.parametrize(
    "raw,content_type",
    [
        ("adults=1&adults=2", "application/x-www-form-urlencoded"),
        ('{"adults":1,"adults":2}', "application/json"),
        ("adults=2", "text/plain"),
    ],
)
async def test_duplicates_and_nonforms_rejected(click_api, raw, content_type) -> None:
    client, _, product, option, _ = click_api
    response = await client.post(
        endpoint(product, option), content=raw, headers={"content-type": content_type}
    )
    assert response.status_code == 422


async def test_body_cap_and_stale_review(click_api) -> None:
    client, session, product, option, _ = click_api
    assert (await client.post(endpoint(product, option), content="x" * 4097)).status_code == 413
    option.verified_at = datetime.now(UTC) - timedelta(days=31)
    await session.commit()
    assert (await client.post(endpoint(product, option))).status_code == 404
    assert await session.scalar(select(HotelBookingClick)) is None


async def test_legacy_empty_body_omits_context(click_api) -> None:
    client, _, product, option, _ = click_api
    response = await client.post(endpoint(product, option))
    assert response.status_code == 303
    query = parse_qs(urlsplit(response.headers["location"]).query)
    assert "checkin" not in query and "adults" not in query


@pytest.mark.parametrize("placement", sorted(BOOKING_PLACEMENTS))
@pytest.mark.parametrize("provider", ["official", "booking"])
async def test_all_public_placements_redirect_on_the_first_post(
    click_api, placement, provider
) -> None:
    client, session, product, option, _ = click_api
    if provider == "official":
        option.provider = "official"
        option.url = option.evidence_url = "https://hotel.example.test/"
        await session.commit()
    original = (option.url, option.version, product.version, option.identity_note)
    response = await client.post(
        endpoint(product, option).replace("placement=trip", f"placement={placement}"),
        data={"check_in": "2030-11-01", "check_out": "2030-11-30", "adults": "2"},
    )
    assert response.status_code == 303, response.text
    click = await session.scalar(select(HotelBookingClick))
    assert click.placement == placement
    if provider == "official":
        assert response.headers["location"] == option.url
        assert click.mode == "direct"
        assert await session.scalar(select(AffiliateClick)) is None
    else:
        query = parse_qs(urlsplit(response.headers["location"]).query)
        assert query["campaign"] == [f"mokaair_tokyo_booking_zh_TW_{placement}"]
        assert query["link"] == [option.url]
        assert query["checkout"] == ["2030-11-30"]
        assert query["adults"] == ["2"]
        affiliate = await session.scalar(select(AffiliateClick))
        assert affiliate.partner == "stay22" and affiliate.placement == placement
        assert affiliate.user_id is affiliate.trip_id is affiliate.search_id is None
        assert str(product.id) not in query["campaign"][0]
        assert str(option.id) not in query["campaign"][0]
    assert original == (option.url, option.version, product.version, option.identity_note)


@pytest.mark.parametrize("placement", ["unknown", "https://evil.test", "trip_private-user-id", ""])
@pytest.mark.parametrize("path_kind", ["booking", "service_offer"])
async def test_unknown_or_private_placements_are_rejected_before_click(
    click_api, placement, path_kind
) -> None:
    client, session, product, option, _ = click_api
    path = (
        endpoint(product, option).split("?", 1)[0]
        if path_kind == "booking"
        else f"/api/v1/affiliates/offers/{uuid4()}/clickout"
    )
    response = await client.post(path, params={"placement": placement})
    assert response.status_code == 422, response.text
    assert await session.scalar(select(HotelBookingClick)) is None
    assert await session.scalar(select(AffiliateClick)) is None


async def test_discovery_preserves_existing_affiliate_priority(click_api, monkeypatch) -> None:
    client, session, product, option, _ = click_api
    brand = TravelServiceBrand(
        id=uuid4(), code="booking", channel="travelpayouts", project_id="fixture"
    )
    session.add(brand)
    await session.commit()
    offer = TravelServiceOffer(id=uuid4(), brand_id=brand.id, version=1)
    monkeypatch.setattr(hotel_options, "matching_offer", AsyncMock(return_value=offer))
    resolver = AsyncMock(return_value="https://tp.st/fixture")
    monkeypatch.setattr(router, "resolve_offer_target", resolver)
    response = await client.post(
        endpoint(product, option).replace("placement=trip", "placement=discovery")
    )
    assert response.status_code == 303, response.text
    assert response.headers["location"] == "https://tp.st/fixture"
    assert resolver.call_args.args[4] == "svc_hotel_tokyo_zh-TW_discovery"
    affiliate = await session.scalar(select(AffiliateClick))
    assert affiliate.partner == "travelpayouts" and affiliate.placement == "discovery"
    assert (await session.scalar(select(HotelBookingClick))).placement == "discovery"


async def test_discovery_nearby_offer_redirects_without_dropping_placement(
    click_api, monkeypatch
) -> None:
    client, session, product, _, _ = click_api
    brand = TravelServiceBrand(
        id=uuid4(), code="booking", channel="travelpayouts", project_id="fixture"
    )
    offer = TravelServiceOffer(
        id=uuid4(), product_id=product.id, brand_id=brand.id,
        target_url="https://www.booking.com/city/jp/tokyo.html", scope="destination",
    )
    session.add_all([brand, offer])
    await session.commit()
    monkeypatch.setattr(router, "ready_offer", lambda *args: True)
    resolver = AsyncMock(return_value="https://tp.st/fixture")
    monkeypatch.setattr(router, "resolve_offer_target", resolver)
    response = await client.post(
        f"/api/v1/affiliates/offers/{offer.id}/clickout?placement=discovery"
    )
    assert response.status_code == 303, response.text
    assert response.headers["location"] == "https://tp.st/fixture"
    assert resolver.call_args.args[4] == "svc_hotel_tokyo_zh-TW_discovery"
    affiliate = await session.scalar(select(AffiliateClick))
    assert affiliate.partner == "travelpayouts" and affiliate.placement == "discovery"
    assert affiliate.user_id is affiliate.trip_id is affiliate.search_id is None
    assert await session.scalar(select(HotelBookingClick)) is None


async def test_privacy_without_direct_permission_is_unavailable(click_api) -> None:
    client, session, product, option, config = click_api
    config.direct_hotel_links_enabled = False
    response = await client.post(endpoint(product, option), headers={"sec-gpc": "1"})
    assert response.status_code == 503
    assert await session.scalar(select(AffiliateClick)) is None
    assert await session.scalar(select(HotelBookingClick)) is None


async def test_query_context_is_not_wrapped_and_foreign_option_is_rejected(click_api) -> None:
    client, session, product, option, _ = click_api
    option.url += "?checkin=2030-01-01"
    option.evidence_url = option.url
    await session.commit()
    response = await client.post(endpoint(product, option))
    assert response.status_code == 303
    assert response.headers["location"] == option.url
    assert await session.scalar(select(AffiliateClick)) is None
    foreign = await client.post(endpoint(product, option).replace(str(option.id), str(uuid4())))
    assert foreign.status_code == 404


@pytest.mark.parametrize(
    "headers,allowed", [({}, True), ({"dnt": "1"}, False), ({"sec-gpc": "1"}, False)]
)
async def test_public_catalog_channel_metadata_respects_privacy(
    click_api, monkeypatch, headers, allowed
) -> None:
    client, _, _, _, _ = click_api
    recommend = AsyncMock(return_value={"items": []})
    monkeypatch.setattr(router, "recommendations", recommend)
    response = await client.get(
        "/api/v1/travel-services?destination_id=tokyo&type=hotel", headers=headers
    )
    assert response.status_code == 200, response.text
    assert recommend.call_args.kwargs["tracking_allowed"] is allowed
    assert response.json()["booking_context"] is None
