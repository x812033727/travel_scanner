"""Catalogue/booking boundaries reject unsafe stays before DNS, providers or writes."""

import json
from datetime import UTC, date, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from starlette.requests import Request
from starlette.responses import Response

from app.config import Settings
from app.models import (
    AffiliateClick,
    HotelBookingClick,
    HotelBookingOption,
    TravelServiceProduct,
    TripPlan,
)
from app.problems import AppError, app_error_handler
from app.travel_services import hotel_options, hotel_quotes, router, service, stay22_script
from app.travel_services.hotel_quotes import HotelQuoteRequest
from app.travel_services.schemas import CatalogConfig, Facts, SelectInput, Stay22Config

NOW = datetime(2026, 9, 11, 5, tzinfo=UTC)
POLICY = {"unavailable_stays": [{
    "start_date": "2027-01-14", "end_date": "2027-01-16", "reason": "Maintenance nights",
    "source_url": "https://hotel.example.org/maintenance",
}]}


def hotel(rules=POLICY):
    return TravelServiceProduct(
        id=uuid4(), kind="hotel", title="Reviewed hotel", names_json={}, source_key=str(uuid4()),
        source_url="https://hotel.example.org/", destination_id="kyoto", status="approved",
        verified_at=NOW,
        facts=Facts(
            latitude=35.0116, longitude=135.7681,
            coordinate_source_url="https://hotel.example.org/location",
        ).model_dump(mode="json") | {"hotel_operating_rules": rules},
        hotel_options=[HotelBookingOption(
            id=uuid4(), provider="booking", url="https://www.booking.com/hotel/jp/example.html",
            evidence_url="https://hotel.example.org/", identity_note="Exact hotel checked",
            status="approved", discovery_status="found", health_status="healthy",
            verified_at=NOW, version=1,
        )],
    )


def config():
    return CatalogConfig(
        public_enabled=True, enabled_kinds=["hotel"], enabled_destinations=["kyoto"],
        direct_hotel_links_enabled=True,
        stay22=Stay22Config(enabled=True, integration_mode="script", lma_id="a" * 24),
    )


def request(context=None):
    body = json.dumps(context).encode() if context is not None else b""

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    return Request({
        "type": "http", "method": "POST", "path": "/", "query_string": b"",
        "headers": [(b"content-type", b"application/json")],
    }, receive)


@pytest.fixture
def boundaries(monkeypatch):
    class FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return NOW.astimezone(tz) if tz else NOW.replace(tzinfo=None)

    monkeypatch.setattr(router, "datetime", FixedDateTime)
    monkeypatch.setattr(hotel_quotes, "datetime", FixedDateTime)
    monkeypatch.setattr(service, "datetime", FixedDateTime)
    monkeypatch.setattr(router, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(router, "catalog_config", AsyncMock(return_value=(config(), 1)))
    monkeypatch.setattr(service, "catalog_config", AsyncMock(return_value=(config(), 1)))
    monkeypatch.setattr(router, "load_runtime_settings", AsyncMock(return_value=Settings()))
    dns = AsyncMock(return_value="https://www.booking.com/hotel/jp/example.html")
    monkeypatch.setattr(hotel_options, "safe_click_target", dns)
    monkeypatch.setattr(stay22_script, "safe_click_target", dns)
    return dns


@pytest.mark.parametrize("context", [
    None, {}, {"adults": 2},
    {"check_in": "2027-01-14", "check_out": "2027-01-15"},
    {"check_in": "2027-01-13", "check_out": "2027-01-17"},
])
async def test_new_clickout_blocks_missing_or_overlapping_stay_before_target(boundaries, context):
    product = hotel()
    session = AsyncMock()
    session.get.return_value = product
    with pytest.raises(AppError) as caught:
        await router.booking_option_clickout(
            product.id, product.hotel_options[0].id, session, request(context), "zh-TW"
        )
    assert caught.value.code in {"hotel_operating_dates_required", "hotel_operating_unavailable"}
    boundaries.assert_not_called()
    session.commit.assert_not_called()


@pytest.mark.parametrize("context", [
    {"check_in": "2027-01-12", "check_out": "2027-01-14"},
    {"check_in": "2027-01-16", "check_out": "2027-01-17"},
])
async def test_new_clickout_allows_boundary_stays(boundaries, monkeypatch, context):
    product = hotel()
    session = AsyncMock()
    session.get.return_value = product
    session.add = Mock()
    monkeypatch.setattr(hotel_options, "matching_offer", AsyncMock(return_value=None))
    response = await router.booking_option_clickout(
        product.id, product.hotel_options[0].id, session, request(context), "zh-TW"
    )
    assert response.status_code == 303
    assert response.headers["location"] == product.hotel_options[0].url
    boundaries.assert_awaited_once()
    session.commit.assert_awaited_once()


async def test_legacy_and_script_original_links_cannot_bypass_dates(boundaries):
    product = hotel()
    session = AsyncMock()
    session.get.return_value = product
    assert service.ready_hotel_links(product, config(), NOW) == []
    with pytest.raises(AppError) as legacy:
        await router.hotel_clickout(product.id, "booking", session, request())
    assert legacy.value.code == "hotel_operating_dates_required"
    with pytest.raises(AppError) as script:
        await stay22_script.script_options(product, config(), NOW, locale="en")
    assert script.value.code == "hotel_operating_dates_required"
    with pytest.raises(AppError):
        await router.public_stay22_script_options(product.id, session, request(), Response(), "en")
    boundaries.assert_not_called()


async def test_affiliate_product_offer_cannot_bypass_dates(boundaries, monkeypatch):
    product = hotel()
    session = AsyncMock()
    session.execute.return_value = Mock(first=Mock(return_value=(Mock(), Mock(), product)))
    resolve = AsyncMock()
    monkeypatch.setattr(router, "resolve_offer_target", resolve)
    with pytest.raises(AppError) as caught:
        await router.offer_clickout(uuid4(), session, "en", request())
    assert caught.value.code == "hotel_operating_dates_required"
    resolve.assert_not_called()
    session.commit.assert_not_called()


async def test_selection_rejects_overlap_before_hydrating_or_writing_trip(boundaries, monkeypatch):
    product = hotel()
    trip = TripPlan(id=uuid4(), start_date=date(2027, 1, 14), end_date=date(2027, 1, 16), version=2)
    session = AsyncMock()
    session.scalar.return_value = None
    session.get.return_value = product
    monkeypatch.setattr(router, "locked_trip", AsyncMock(return_value=trip))
    load_items = AsyncMock()
    monkeypatch.setattr(router, "load_items", load_items)
    with pytest.raises(AppError) as caught:
        await router.select_service(
            trip.id, SelectInput(product_id=product.id, version=2), "operation-1",
            SimpleNamespace(id=uuid4()), session,
        )
    assert caught.value.code == "hotel_operating_unavailable"
    load_items.assert_not_called()
    session.flush.assert_not_called()
    session.commit.assert_not_called()


async def test_quote_route_and_worker_gate_before_quota_or_provider(boundaries, monkeypatch):
    product = hotel()
    query = HotelQuoteRequest(
        check_in="2027-01-14", check_out="2027-01-15", rooms=[{"adults": 2}],
        currency="TWD", booker_country="TW",
    )
    session = AsyncMock()
    session.get.return_value = product
    redis = AsyncMock()
    reserve = AsyncMock()
    monkeypatch.setattr(hotel_quotes, "reserve_calls", reserve)
    with pytest.raises(AppError, match="暫停住宿"):
        await hotel_quotes.search_quotes(product, query, "en", config(), redis)
    search = AsyncMock()
    monkeypatch.setattr(router, "search_quotes", search)
    with pytest.raises(AppError, match="暫停住宿"):
        await router.hotel_quotes(product.id, query, session, request(), "en", Response())
    reserve.assert_not_called()
    search.assert_not_called()
    boundaries.assert_not_called()


async def test_public_and_trip_recommendations_filter_rules_without_provider_calls(boundaries):
    restricted, ordinary, malformed = hotel(), hotel(None), hotel({"bad": True})
    ended = hotel({
        "last_checkout_date": "2026-09-11", "last_checkout_reason": "Closed",
        "last_checkout_source_url": "https://hotel.example.org/closed",
    })
    session = AsyncMock()
    session.scalars.return_value = [restricted, ordinary, malformed, ended]
    session.execute.return_value = Mock(all=Mock(return_value=[]))
    public = await service.recommendations(session, Settings(), "en", city="kyoto")
    assert {p["id"] for p in public["items"]} == {str(restricted.id), str(ordinary.id)}
    trip = TripPlan(
        start_date=date(2027, 1, 14), end_date=date(2027, 1, 16),
        destination_name="Kyoto", data={},
    )
    planned = await service.recommendations(
        session, Settings(), "en", city="kyoto", trip=trip, rows=[]
    )
    assert [p["id"] for p in planned["items"]] == [str(ordinary.id)]
    boundaries.assert_not_called()


@pytest.mark.parametrize("rules", [{"bad": True}, {"unavailable_stays": [None]}])
async def test_malformed_stored_policy_never_reaches_direct_target(boundaries, rules):
    product = hotel(rules)
    session = AsyncMock()
    session.get.return_value = product
    with pytest.raises(AppError):
        await router.booking_option_clickout(
            product.id, product.hotel_options[0].id, session,
            request({"check_in": "2027-01-01", "check_out": "2027-01-02"}), "en",
        )
    boundaries.assert_not_called()


@pytest.mark.parametrize("body,expected", [
    ("", 422),
    ("adults=2", 422),
    ("check_in=2027-01-14&check_out=2027-01-15", 409),
    ("check_in=2027-01-12&check_out=2027-01-14", 303),
])
async def test_browser_post_form_cannot_bypass_rule(boundaries, monkeypatch, body, expected):
    product = hotel()
    session = AsyncMock()
    session.get.return_value = product
    session.add = Mock()
    monkeypatch.setattr(hotel_options, "matching_offer", AsyncMock(return_value=None))
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)
    app.include_router(router.router, prefix="/api/v1")
    app.dependency_overrides[router.get_session] = lambda: session
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        response = await client.post(
            f"/api/v1/travel-services/{product.id}/booking-options/"
            f"{product.hotel_options[0].id}/clickout",
            content=body, headers={"content-type": "application/x-www-form-urlencoded"},
            follow_redirects=False,
        )
    assert response.status_code == expected
    if expected == 303:
        assert response.headers["location"] == product.hotel_options[0].url
        boundaries.assert_awaited_once()
    else:
        assert response.json()["code"] in {
            "hotel_operating_dates_required", "hotel_operating_unavailable",
        }
        boundaries.assert_not_called()
        session.commit.assert_not_called()


def test_import_retains_valid_operating_policy_and_rejects_bad_policy():
    import csv
    import io

    from app.travel_services.imports import parse_csv

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "source_key", "kind", "destination_id", "title", "source_url", "facts",
    ])
    writer.writeheader()
    for index, rules in enumerate((POLICY, {"last_checkout_date": "2027-05-09"})):
        writer.writerow({
            "source_key": f"operating-import-{index}", "kind": "hotel",
            "destination_id": "kyoto", "title": "Reviewed hotel",
            "source_url": "https://hotel.example.org/",
            "facts": json.dumps({"hotel_operating_rules": rules}),
        })
    result = parse_csv(output.getvalue())
    assert result[0]["product"]["facts"]["hotel_operating_rules"]["unavailable_stays"] == (
        POLICY["unavailable_stays"]
    )
    assert result[1]["error"] == "service_csv_invalid"


async def browser_click(session, path, body="check_in=2027-01-12&check_out=2027-01-14"):
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)
    app.include_router(router.router, prefix="/api/v1")
    app.dependency_overrides[router.get_session] = lambda: session
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        return await client.post(
            f"/api/v1/{path}", content=body,
            headers={"content-type": "application/x-www-form-urlencoded"}, follow_redirects=False,
        )


@pytest.mark.parametrize("query", [
    "checkin=2027-01-14&checkout=2027-01-15", "arrival=2027-01-14", "property_id=123",
])
async def test_valid_caller_dates_cannot_override_opaque_saved_query(
    boundaries, monkeypatch, query
):
    product = hotel()
    option = product.hotel_options[0]
    original = f"{option.url}?{query}"
    option.url = original
    session = AsyncMock()
    session.get.return_value = product
    session.add = Mock()
    matching, resolve = AsyncMock(), AsyncMock()
    monkeypatch.setattr(hotel_options, "matching_offer", matching)
    monkeypatch.setattr(router, "resolve_offer_target", resolve)
    response = await browser_click(
        session, f"travel-services/{product.id}/booking-options/{option.id}/clickout"
    )
    assert response.status_code == 409
    assert response.json()["code"] == "hotel_operating_rules_invalid"
    assert option.url == original  # No query stripping that could switch hotel identity.
    boundaries.assert_not_called()
    matching.assert_not_called()
    resolve.assert_not_called()
    session.add.assert_not_called()
    session.commit.assert_not_called()


async def test_unrestricted_saved_query_keeps_existing_behavior(boundaries, monkeypatch):
    product = hotel(None)
    option = product.hotel_options[0]
    option.url += "?checkin=2027-01-14&property_id=123"
    boundaries.return_value = option.url
    session = AsyncMock()
    session.get.return_value = product
    session.add = Mock()
    monkeypatch.setattr(hotel_options, "matching_offer", AsyncMock(return_value=None))
    response = await browser_click(
        session, f"travel-services/{product.id}/booking-options/{option.id}/clickout", body=""
    )
    assert response.status_code == 303
    assert response.headers["location"] == option.url
    boundaries.assert_awaited_once()


@pytest.mark.parametrize("dirty_field", ["target_url", "static_url"])
@pytest.mark.parametrize("allow_direct", [True, False])
async def test_opaque_saved_affiliate_only_falls_back_to_clean_direct(
    boundaries, monkeypatch, dirty_field, allow_direct,
):
    product = hotel()
    option = product.hotel_options[0]
    saved = SimpleNamespace(target_url=option.url, static_url=None, brand_id=uuid4())
    setattr(saved, dirty_field, f"{option.url}?checkin=2027-01-14")
    session = AsyncMock()
    session.get.return_value = product
    session.add = Mock()
    settings = config().model_copy(update={"direct_hotel_links_enabled": allow_direct})
    settings.stay22.enabled_providers = ["booking"]
    monkeypatch.setattr(router, "catalog_config", AsyncMock(return_value=(settings, 1)))
    monkeypatch.setattr(hotel_options, "matching_offer", AsyncMock(return_value=saved))
    resolve, wrap = AsyncMock(), Mock()
    monkeypatch.setattr(router, "resolve_offer_target", resolve)
    monkeypatch.setattr("app.travel_services.stay22.build_stay22_url", wrap)
    response = await browser_click(
        session, f"travel-services/{product.id}/booking-options/{option.id}/clickout"
    )
    resolve.assert_not_called()
    wrap.assert_not_called()
    if allow_direct:
        assert response.status_code == 303
        assert response.headers["location"] == option.url
        boundaries.assert_awaited_once()
        added = [call.args[0] for call in session.add.call_args_list]
        assert len(added) == 1 and isinstance(added[0], HotelBookingClick)
        assert added[0].mode == "direct" and added[0].fallback
        assert not any(isinstance(row, AffiliateClick) for row in added)
    else:
        assert response.status_code == 409
        assert response.json()["code"] == "hotel_operating_rules_invalid"
        boundaries.assert_not_called()
        session.add.assert_not_called()
        session.commit.assert_not_called()


@pytest.mark.parametrize("dirty_field", ["target_url", "static_url"])
async def test_legacy_affiliate_saved_query_blocks_before_resolution(
    boundaries, monkeypatch, dirty_field,
):
    product = hotel()
    saved = SimpleNamespace(target_url=product.hotel_options[0].url, static_url=None)
    setattr(saved, dirty_field, f"{saved.target_url}?checkout=2027-01-15")
    session = AsyncMock()
    session.execute.return_value = Mock(first=Mock(return_value=(saved, Mock(), product)))
    session.add = Mock()
    resolve = AsyncMock()
    monkeypatch.setattr(router, "resolve_offer_target", resolve)
    response = await browser_click(session, f"affiliates/offers/{uuid4()}/clickout")
    assert response.status_code == 409
    assert response.json()["code"] == "hotel_operating_rules_invalid"
    resolve.assert_not_called()
    boundaries.assert_not_called()
    session.add.assert_not_called()
    session.commit.assert_not_called()


async def browser_booking_details(session, product_id):
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)
    app.include_router(router.router, prefix="/api/v1")
    app.dependency_overrides[router.get_session] = lambda: session
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        return await client.get(f"/api/v1/travel-services/{product_id}/booking-details")


@pytest.mark.parametrize("rules", [None, POLICY])
async def test_booking_details_are_public_without_discovery_or_external_calls(
    boundaries, monkeypatch, rules,
):
    product = hotel(rules)
    session = AsyncMock()
    session.get.return_value = product
    session.scalars.return_value = [product]
    session.execute.return_value = Mock(all=Mock(return_value=[]))
    session.add = Mock()
    settings = Settings(discovery_enabled=False)
    monkeypatch.setattr(router, "load_runtime_settings", AsyncMock(return_value=settings))
    resolve, quotes = AsyncMock(), AsyncMock()
    monkeypatch.setattr(router, "resolve_offer_target", resolve)
    monkeypatch.setattr(router, "search_quotes", quotes)
    response = await browser_booking_details(session, product.id)
    assert response.status_code == 200
    detail = response.json()
    assert detail["id"] == str(product.id) and detail["kind"] == "hotel"
    assert detail["destination_id"] == "kyoto"
    assert detail["booking_options"][0]["id"] == str(product.hotel_options[0].id)
    assert "url" not in detail["booking_options"][0]
    if rules:
        assert detail["facts"]["hotel_operating_rules"]["unavailable_stays"] == (
            rules["unavailable_stays"]
        )
    assert response.headers["cache-control"] == "no-store"
    boundaries.assert_not_called()
    resolve.assert_not_called()
    quotes.assert_not_called()
    session.add.assert_not_called()
    session.flush.assert_not_called()
    session.commit.assert_not_called()


@pytest.mark.parametrize("hidden", [
    "missing", "nonhotel", "pending", "rejected", "public_disabled", "hotel_disabled",
    "destination_disabled", "unknown_destination", "closed", "malformed_rules", "malformed_facts",
])
async def test_booking_details_never_expose_unapproved_or_disabled_hotels(
    boundaries, monkeypatch, hidden,
):
    product = hotel()
    product_id = product.id
    settings = config()
    if hidden == "missing":
        product = None
    elif hidden == "nonhotel":
        product.kind = "tour"
    elif hidden in {"pending", "rejected"}:
        product.status = hidden
    elif hidden == "public_disabled":
        settings.public_enabled = False
    elif hidden == "hotel_disabled":
        settings.enabled_kinds = []
    elif hidden == "destination_disabled":
        settings.enabled_destinations = []
    elif hidden == "unknown_destination":
        product.destination_id = "unknown"
    elif hidden == "closed":
        product.facts["hotel_operating_rules"] = {
            "last_checkout_date": "2026-09-11", "last_checkout_reason": "Closed",
            "last_checkout_source_url": "https://hotel.example.org/closed",
        }
    elif hidden == "malformed_rules":
        product.facts["hotel_operating_rules"] = {"bad": True}
    elif hidden == "malformed_facts":
        product.facts["latitude"] = "not a coordinate"
    session = AsyncMock()
    session.get.return_value = product
    session.add = Mock()
    monkeypatch.setattr(router, "catalog_config", AsyncMock(return_value=(settings, 1)))
    monkeypatch.setattr(service, "catalog_config", AsyncMock(return_value=(settings, 1)))
    response = await browser_booking_details(session, product_id)
    assert response.status_code == 404
    assert response.json()["code"] == "service_unavailable"
    session.scalars.assert_not_called()
    boundaries.assert_not_called()
    session.add.assert_not_called()
    session.commit.assert_not_called()


async def test_booking_details_filter_product_id_in_sql_before_catalog_limit(boundaries):
    # The requested hotel is beyond the list cap; the database must select only its ID.
    catalogue = [hotel(None) for _ in range(130)]
    product = catalogue[-1]
    session = AsyncMock()
    session.get.return_value = product

    async def select_product(statement):
        compiled = statement.compile()
        assert "travel_service_products.id = :id_1" in str(compiled)
        assert compiled.params["id_1"] == product.id
        assert "approved" in compiled.params.values()
        return [entry for entry in catalogue if entry.id == compiled.params["id_1"]]

    session.scalars.side_effect = select_product
    session.execute.return_value = Mock(all=Mock(return_value=[]))
    response = await browser_booking_details(session, product.id)
    assert response.status_code == 200
    assert response.json()["id"] == str(product.id)
    session.scalars.assert_awaited_once()
    boundaries.assert_not_called()
