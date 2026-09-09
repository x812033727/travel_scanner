from datetime import UTC, date, datetime, timedelta, tzinfo
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import fakeredis.aioredis
import pytest
from pydantic import ValidationError

from app.models import HotelBookingOption, TravelServiceProduct
from app.travel_services import hotel_quotes
from app.travel_services.hotel_options import ready_option
from app.travel_services.hotel_quotes import (
    ADAPTERS,
    HotelQuote,
    HotelQuoteRequest,
    RoomOccupancy,
    rank_quotes,
    search_quotes,
)
from app.travel_services.schemas import CatalogConfig, HotelOptionInput, HotelQuotePolicy

NOW = datetime(2026, 11, 1, 12, tzinfo=UTC)
QUERY = HotelQuoteRequest(
    check_in=date(2026, 11, 11),
    check_out=date(2026, 11, 13),
    rooms=[RoomOccupancy(adults=2)],
    currency="TWD",
    booker_country="TW",
)


@pytest.fixture(autouse=True)
def frozen_quote_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    # Collection can precede this module's tests by more than the two-minute TTL.
    # Keep quote generation and the service's validity/quota clocks consistent.
    class FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz: tzinfo | None = None) -> datetime:
            return NOW.astimezone(tz) if tz is not None else NOW.replace(tzinfo=None)

    monkeypatch.setattr(hotel_quotes, "datetime", FrozenDateTime)


def rate(provider="booking", **overrides):
    data = dict(
        provider=provider,
        property_id=provider + "-1",
        rate_id="rate1",
        stay=QUERY,
        currency="TWD",
        total=Decimal("2000"),
        taxes=Decimal("100"),
        pay_at_property=Decimal("0"),
        mandatory_charges_complete=True,
        room_name="Original room",
        room_match_key="reviewed-double",
        bed_key="double",
        meal_key="no-meal",
        cancellation_key="nonrefundable",
        payment_key="prepaid",
        retrieved_at=NOW - timedelta(seconds=10),
        expires_at=NOW + timedelta(minutes=2),
    )
    return HotelQuote.model_validate({**data, **overrides})


def hotel():
    row = TravelServiceProduct(
        id=uuid4(),
        kind="hotel",
        destination_id="tokyo",
        status="approved",
        facts={},
        hotel_options=[],
    )
    for provider in ("booking", "trip_com"):
        path = (
            "booking.com/hotel/jp/fixture"
            if provider == "booking"
            else "trip.com/hotels/fixture-hotel-detail-123"
        )
        row.hotel_options.append(
            HotelBookingOption(
                id=uuid4(),
                provider=provider,
                url=f"https://{path}/",
                property_id=provider + "-1",
                evidence_url="https://official.example.com/location",
                identity_note="Reviewed identity",
                discovery_status="found",
                status="approved",
                version=1,
                verified_at=NOW,
                health_status="healthy",
            )
        )
    return row


def config(**extra):
    return CatalogConfig(
        direct_hotel_links_enabled=True,
        enabled_kinds=["hotel"],
        enabled_destinations=["tokyo"],
        **extra,
    )


def test_two_platforms_require_matching_terms_before_lowest_label():
    rates = rank_quotes([rate(), rate("trip_com", total=Decimal("1900"))], QUERY, NOW)
    assert [q["lowest_in_group"] for q in rates] == [True, False]
    assert all(q["comparable"] for q in rates)
    assert not rank_quotes([rate()], QUERY, NOW)[0]["lowest_in_group"]


@pytest.mark.parametrize(
    "changes",
    [
        {"taxes": None},
        {"pay_at_property": None},
        {"mandatory_charges_complete": False},
        {"public_rate": False},
        {"currency": "JPY"},
        {"room_match_key": None},
        {"bed_key": "twin"},
        {"meal_key": "breakfast"},
        {"cancellation_key": "refundable"},
        {"payment_key": "pay-at-property"},
    ],
)
def test_unknown_or_different_terms_are_never_cheapest(changes):
    rates = rank_quotes([rate(), rate("trip_com", **changes)], QUERY, NOW)
    assert not any(q["lowest_in_group"] or q["comparable"] for q in rates)


def test_expired_and_wrong_conditions_not_shown():
    expired = rate(retrieved_at=NOW - timedelta(minutes=10), expires_at=NOW - timedelta(seconds=1))
    wrong = rate(stay=QUERY.model_copy(update={"rooms": [RoomOccupancy(adults=1)]}))
    assert rank_quotes([expired, wrong], QUERY, NOW) == []


def test_no_price_is_not_zero_and_no_unapproved_cache():
    with pytest.raises(ValidationError):
        rate(total=0)
    with pytest.raises(ValidationError):
        HotelQuotePolicy(enabled=True, daily_limit=100)
    with pytest.raises(ValidationError):
        HotelQuotePolicy(cache_seconds=10)
    with pytest.raises(ValidationError):
        HotelOptionInput(
            provider="booking",
            discovery_status="not_found",
            url="https://booking.com/hotel/jp/fixture",
        )


@pytest.mark.parametrize(
    "health,expected",
    [("healthy", True), ("unconfirmed", True), ("unsafe", False), ("unavailable", False)],
)
def test_link_health_does_not_confuse_bot_blocks_with_removal(health, expected):
    product = hotel()
    option = product.hotel_options[0]
    option.health_status = health
    assert ready_option(product, option, config(), NOW) is expected
    option.status = "pending"
    assert not ready_option(product, option, config(), NOW)


async def test_without_adapter_or_permission_never_calls_provider(monkeypatch):
    redis = fakeredis.aioredis.FakeRedis()
    adapter = AsyncMock()
    monkeypatch.setitem(ADAPTERS, "booking", adapter)
    result = await search_quotes(hotel(), QUERY, "zh-TW", config(), redis)
    assert result["status"] == "not_configured" and result["quotes"] == []
    adapter.search.assert_not_called()
    assert await redis.dbsize() == 0
    await redis.aclose()


@pytest.mark.parametrize("expires_after,expected", [(-1, "no_availability"), (120, "available")])
async def test_search_quote_validity_uses_fixed_clock(monkeypatch, expires_after, expected):
    redis = fakeredis.aioredis.FakeRedis()
    adapter = AsyncMock()
    adapter.search.return_value = [rate(expires_at=NOW + timedelta(seconds=expires_after))]
    monkeypatch.setitem(ADAPTERS, "booking", adapter)
    policy = HotelQuotePolicy(
        enabled=True,
        comparison_allowed=True,
        terms_url="https://official.example.com/terms",
        daily_limit=1,
    )
    try:
        assert hotel_quotes.datetime.now(UTC) == NOW
        result = await search_quotes(
            hotel(), QUERY, "ja", config(hotel_quote_policies={"booking": policy}), redis
        )
        assert result["status"] == expected
        assert len(result["quotes"]) == int(expires_after > 0)
        adapter.search.assert_awaited_once()
    finally:
        await redis.aclose()


async def test_partial_failure_quota_and_identity_isolation(monkeypatch):
    redis = fakeredis.aioredis.FakeRedis()
    policies = {
        p: HotelQuotePolicy(
            enabled=True,
            comparison_allowed=True,
            terms_url="https://official.example.com/terms",
            daily_limit=1,
        )
        for p in ("booking", "trip_com")
    }
    first = AsyncMock()
    first.search.return_value = [rate()]
    second = AsyncMock()
    second.search.side_effect = TimeoutError()
    monkeypatch.setitem(ADAPTERS, "booking", first)
    monkeypatch.setitem(ADAPTERS, "trip_com", second)
    result = await search_quotes(hotel(), QUERY, "ja", config(hotel_quote_policies=policies), redis)
    assert result["status"] == "partial" and len(result["quotes"]) == 1
    again = await search_quotes(hotel(), QUERY, "ja", config(hotel_quote_policies=policies), redis)
    assert all(p["status"] == "quota_exceeded" for p in again["providers"])
    assert first.search.await_count == 1
    await redis.flushall()
    first.search.return_value = [rate(property_id="different-property")]
    result = await search_quotes(hotel(), QUERY, "ja", config(hotel_quote_policies=policies), redis)
    assert result["status"] == "unavailable" and result["quotes"] == []
    await redis.aclose()
