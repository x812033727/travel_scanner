"""Public channel metadata uses the same eligibility decisions as clickout."""

from datetime import UTC, date, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from starlette.requests import Request

from app.config import Settings
from app.models import HotelBookingOption, TravelServiceProduct
from app.problems import AppError
from app.travel_services.hotel_options import public_options
from app.travel_services.schemas import CatalogConfig, Stay22Config

NOW = datetime(2026, 9, 9, 12, tzinfo=UTC)


def product():
    result = TravelServiceProduct(
        id=uuid4(), kind="hotel", destination_id="tokyo", status="approved", hotel_options=[],
    )
    result.hotel_options.append(HotelBookingOption(
        id=uuid4(), provider="booking", url="https://www.booking.com/hotel/jp/example.html",
        evidence_url="https://example.com/hotel-location", identity_note="Reviewed hotel",
        discovery_status="found", status="approved", verified_at=NOW, health_status="healthy",
    ))
    return result


def config(**updates):
    return CatalogConfig.model_validate({
        "enabled_kinds": ["hotel"], "enabled_destinations": ["tokyo"],
        "stay22": Stay22Config(enabled=True, enabled_providers=["booking"]), **updates,
    })


async def test_public_stay22_does_not_require_plain_links_or_disclose_aid_target():
    result = await public_options(AsyncMock(), product(), config(), Settings(), NOW, set())
    assert len(result) == 1
    assert result[0]["mode"] == "affiliate" and result[0]["affiliate_channel"] == "stay22"
    assert result[0]["provider"] == "booking" and result[0]["name"] == "Booking.com"
    assert not {"url", "aid", "target_url", "link", "property_id"} & result[0].keys()


async def test_existing_offer_has_priority_without_extra_database_queries():
    hotel = product()
    session = AsyncMock()
    result = await public_options(
        session, hotel, config(), Settings(), NOW, {("booking", hotel.hotel_options[0].url)}
    )
    assert result[0]["affiliate_channel"] == "existing"
    session.execute.assert_not_called()


async def test_another_hotel_or_platform_offer_does_not_count_as_matching():
    result = await public_options(AsyncMock(), product(), config(), Settings(), NOW, {
        ("booking", "https://www.booking.com/hotel/jp/another.html"),
        ("agoda", "https://www.booking.com/hotel/jp/example.html"),
    })
    assert result[0]["affiliate_channel"] == "stay22"


@pytest.mark.parametrize("updates", [
    {"verified_at": NOW - timedelta(days=30, seconds=1)},
    {"verified_at": NOW + timedelta(seconds=1)}, {"status": "pending"},
    {"discovery_status": "unconfirmed"}, {"health_status": "unsafe"},
])
async def test_config_never_bypasses_review_and_identity(updates):
    hotel = product()
    for key, value in updates.items():
        setattr(hotel.hotel_options[0], key, value)
    assert await public_options(AsyncMock(), hotel, config(), Settings(), NOW, set()) == []


async def test_privacy_signals_cannot_advertise_stay22_when_propagated():
    assert await public_options(
        AsyncMock(), product(), config(), Settings(), NOW, set(), tracking_allowed=False
    ) == []
    result = await public_options(
        AsyncMock(), product(), config(direct_hotel_links_enabled=True), Settings(), NOW,
        set(), tracking_allowed=False,
    )
    assert result[0]["mode"] == "direct" and result[0]["affiliate_channel"] is None


async def test_global_and_platform_disable_take_effect_without_cached_channel():
    for setting in (Stay22Config(), Stay22Config(enabled=True, enabled_providers=["agoda"])):
        assert await public_options(
            AsyncMock(), product(), config(stay22=setting), Settings(), NOW, set()
        ) == []


def click_request(body: bytes, content_type: str = "application/json") -> Request:
    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    return Request({
        "type": "http", "method": "POST", "path": "/",
        "headers": [(b"content-type", content_type.encode())], "query_string": b"",
    }, receive=receive)


@pytest.mark.parametrize("body,content_type", [
    (b"[]", "application/json"), (b"null", "application/json"),
    (b'{"adults":2,"adults":3}', "application/json"),
    (b'{"adults":{"target":"https://evil.example.com"}}', "application/json"),
    (b'{"adults":"2"}', "application/json"),
    (b'{"adults":true}', "application/json"),
    (b'{"adults":2,"aid":null}', "application/json"),
    (b'{"adults":2,"rooms":1}', "application/json"),
    (b'{"adults":2,"children_ages":[]}', "application/json"),
    (b'{"check_in":1798761600,"check_out":1798934400}', "application/json"),
    (b'{"check_in":true,"check_out":false}', "application/json"),
    (b'{"check_in":"2099-01-01T00:00:00Z","check_out":"2099-01-02T00:00:00Z"}',
     "application/json"),
    (b"adults=2&adults=3", "application/x-www-form-urlencoded"),
    (b"adults=2&target=", "application/x-www-form-urlencoded"),
    ("adults=２".encode(), "application/x-www-form-urlencoded"),
    (b"check_in=2099-01-01&check_out=", "application/x-www-form-urlencoded"),
    (b"\xff", "application/x-www-form-urlencoded"),
    (b"adults=2", "text/plain"),
])
async def test_click_context_parser_rejects_ambiguous_and_injected_inputs(body, content_type):
    from app.travel_services.router import _booking_click_context

    with pytest.raises(AppError) as caught:
        await _booking_click_context(click_request(body, content_type), today=date(2026, 9, 9))
    assert caught.value.code == "hotel_booking_context_invalid"


async def test_click_context_parser_legacy_empty_and_explicit_dates_without_guessing():
    from app.travel_services.router import _booking_click_context

    assert await _booking_click_context(click_request(b""), today=date(2026, 9, 9)) is None
    empty = await _booking_click_context(click_request(b"{}"), today=date(2026, 9, 9))
    assert empty.check_in is None and empty.adults is None
    context = await _booking_click_context(
        click_request(
            b"check_in=2099-01-01&check_out=2099-02-15&adults=2&children=0",
            "application/x-www-form-urlencoded; charset=UTF-8",
        ), today=date(2026, 9, 9),
    )
    assert str(context.check_out) == "2099-02-15" and context.adults == 2
    assert context.children == 0
    with pytest.raises(AppError) as caught:
        await _booking_click_context(click_request(b" " * 4097), today=date(2026, 9, 9))
    assert caught.value.code == "request_too_large"
