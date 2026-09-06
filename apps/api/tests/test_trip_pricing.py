from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from app.crawlers.fx import FxRateError
from app.crawlers.schemas import FxRateSnapshot
from app.models import TripPlan, TripPlanItem
from app.trips.pricing import (
    lodging_from_offer,
    offer_price_snapshot,
    trip_pricing,
    trip_pricing_with_rates,
)

DAY = date(2026, 11, 10)


def _trip(**data: object) -> TripPlan:
    return TripPlan(
        id=uuid4(),
        user_id=uuid4(),
        name="東京五日",
        mode="balanced",
        total_price=Decimal("32000"),
        currency="TWD",
        data=dict(data),
        version=1,
        start_date=DAY,
        end_date=DAY,
        timezone="Asia/Tokyo",
    )


def _anchor(trip: TripPlan, role: str, offer_id: object, snapshot: dict[str, object] | None):
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=trip.id,
        item_type="flight",
        day_date=DAY,
        position=0,
        title="長榮航空 BR 198",
        offer_id=offer_id,
        locked=True,
        fixed_time=True,
        is_estimated=False,
        system_role=role,
        data={"price_snapshot": snapshot} if snapshot else {},
    )


def test_offer_snapshot_keeps_only_what_outlives_the_offer() -> None:
    snapshot = offer_price_snapshot(
        {
            "id": "offer-1",
            "provider": "amadeus",
            "source_mode": "live",
            "total_price": Decimal("18500.00"),
            "currency": "TWD",
            "nightly_price": "4625",
            "nights": 4,
            "retrieved_at": "2026-09-01T00:00:00Z",
            "expires_at": "2026-09-01T06:00:00Z",
            "booking_url": "https://example.test/secret",
        }
    )
    assert snapshot == {
        "total_price": "18500.00",
        "currency": "TWD",
        "provider": "amadeus",
        "source_mode": "live",
        "retrieved_at": "2026-09-01T00:00:00Z",
        "expires_at": "2026-09-01T06:00:00Z",
        "nightly_price": "4625",
        "nights": 4,
    }
    assert offer_price_snapshot({"currency": "TWD"}) is None
    assert offer_price_snapshot(None) is None


def test_lodging_from_offer_matches_the_stay_area_shape() -> None:
    lodging = lodging_from_offer(
        {
            "id": "hotel-offer-1",
            "provider": "booking",
            "hotel_id": "h-1",
            "hotel_name": "丸之內測試飯店",
            "address": "東京都千代田區丸之內",
            "latitude": 35.68,
            "longitude": 139.76,
            "total_price": "18500",
            "currency": "TWD",
            "nights": 4,
        },
        selection_source="search",
    )
    assert lodging is not None
    assert lodging["name"] == "丸之內測試飯店"
    assert lodging["offer_id"] == "hotel-offer-1"
    assert lodging["selection_source"] == "search"
    assert lodging["location_source"] == "provider"
    assert lodging["price_snapshot"]["total_price"] == "18500"
    assert lodging_from_offer({"total_price": "1"}, selection_source="search") is None


def test_round_trip_offer_is_counted_once_and_estimates_stay_separate() -> None:
    offer_id = uuid4()
    trip = _trip(
        total_cost={"confirmed_cost": "30000", "estimated_cost": "2400", "total_cost": "32400"},
        primary_lodging={
            "name": "丸之內測試飯店",
            "location_name": "東京都千代田區丸之內",
            "offer_id": "hotel-offer-1",
            "price_snapshot": {"total_price": "18500", "currency": "TWD"},
        },
    )
    flight = {"total_price": "11500", "currency": "TWD", "provider": "amadeus"}
    rows = [
        _anchor(trip, "outbound_flight", offer_id, flight),
        _anchor(trip, "return_flight", offer_id, flight),
    ]

    pricing = trip_pricing(trip, rows)

    assert pricing["currency"] == "TWD"
    assert pricing["quoted_total"] == "30000"
    assert pricing["estimated_total"] == "2400"
    assert [(item["kind"], item["counted"]) for item in pricing["items"]] == [
        ("flight", True),
        ("flight", False),
        ("hotel", True),
    ]
    assert pricing["unsummed_currencies"] == []


def test_foreign_currency_quotes_are_listed_but_never_converted() -> None:
    trip = _trip()
    rows = [
        _anchor(
            trip,
            "outbound_flight",
            uuid4(),
            {"total_price": "52000", "currency": "JPY", "provider": "skyscanner"},
        )
    ]

    pricing = trip_pricing(trip, rows)

    assert pricing["quoted_total"] == "0"
    assert pricing["estimated_total"] is None
    assert pricing["unsummed_currencies"] == ["JPY"]
    assert pricing["items"][0]["counted"] is False


def test_manual_anchor_without_snapshot_contributes_nothing() -> None:
    trip = _trip()
    rows = [_anchor(trip, "outbound_flight", None, None)]

    pricing = trip_pricing(trip, rows)

    assert pricing["items"] == []
    assert pricing["quoted_total"] == "0"


def test_foreign_currency_quotes_convert_when_a_rate_is_available() -> None:
    trip = _trip()
    offer_id = uuid4()
    rows = [
        _anchor(
            trip,
            "outbound_flight",
            offer_id,
            {"total_price": "52000", "currency": "JPY", "provider": "skyscanner"},
        ),
        _anchor(
            trip,
            "return_flight",
            offer_id,
            {"total_price": "52000", "currency": "JPY", "provider": "skyscanner"},
        ),
    ]
    rate = FxRateSnapshot(
        base_currency="JPY",
        rate=Decimal("0.2"),
        as_of=date(2026, 9, 5),
        source_url="https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/jpy.min.json",
    )

    pricing = trip_pricing(trip, rows, rates={"JPY": rate})

    # The round trip is converted once (same offer on both anchors); the converted sum is
    # a separate number so `quoted_total` keeps meaning "quoted in the trip's currency".
    assert pricing["quoted_total"] == "0"
    assert pricing["converted_total"] == "10400.00"
    assert pricing["unsummed_currencies"] == []
    assert pricing["items"][0]["converted_amount"] == "10400.00"
    assert pricing["items"][0]["counted"] is False
    assert pricing["items"][1]["converted_amount"] is None
    assert pricing["conversions"] == [
        {
            "currency": "JPY",
            "rate": "0.2",
            "as_of": "2026-09-05",
            "is_stale": False,
            "source_url": rate.source_url,
        }
    ]


@pytest.mark.asyncio
async def test_trip_pricing_with_rates_only_asks_for_the_currencies_it_needs() -> None:
    trip = _trip()
    rows = [
        _anchor(
            trip,
            "outbound_flight",
            uuid4(),
            {"total_price": "52000", "currency": "JPY", "provider": "skyscanner"},
        )
    ]
    asked: list[tuple[str, str]] = []

    class Provider:
        async def rate(self, base: str, quote: str) -> FxRateSnapshot:
            asked.append((base, quote))
            if base == "KRW":
                raise FxRateError("nope")
            return FxRateSnapshot(
                base_currency=base,
                quote_currency=quote,
                rate=Decimal("0.2"),
                as_of=date(2026, 9, 5),
                source_url="test",
            )

    pricing = await trip_pricing_with_rates(trip, rows, Provider())  # type: ignore[arg-type]
    assert asked == [("JPY", "TWD")]
    assert pricing["converted_total"] == "10400.00"

    # A currency the provider cannot serve stays listed instead of breaking the trip page.
    rows[0].data = {"price_snapshot": {"total_price": "500000", "currency": "KRW"}}
    pricing = await trip_pricing_with_rates(trip, rows, Provider())  # type: ignore[arg-type]
    assert pricing["converted_total"] is None
    assert pricing["unsummed_currencies"] == ["KRW"]
