from datetime import date
from decimal import Decimal
from uuid import uuid4

from app.models import TripPlan, TripPlanItem
from app.trips.pricing import lodging_from_offer, offer_price_snapshot, trip_pricing

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
