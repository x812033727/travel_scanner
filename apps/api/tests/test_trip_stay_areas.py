from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from types import SimpleNamespace
from typing import Any
from uuid import NAMESPACE_URL, uuid4, uuid5

import pytest

from app.config import Settings
from app.crawlers.fx import FxRateError
from app.hotspots.areas import HotspotArea, city_areas, resolve_area
from app.hotspots.discovery import haversine_km
from app.models import TripPlan, TripPlanItem
from app.optimization.engine import TripOptimizer
from app.optimization.hotel_filters import filter_hotels_with_relaxation
from app.providers.mock import MockProvider
from app.providers.schemas import HotelOffer
from app.search.schemas import SearchCreate, SearchModule
from app.trips.stay_areas import (
    STAY_AREA_MIN,
    AreaOffer,
    evidence_items,
    normalize_offers,
    rank_area_offers,
    score_stay_areas,
    split_area_offers,
    stay_dates,
    stay_partner_options,
    stay_search_query,
    trip_city,
)

NRT_AREAS = city_areas("NRT")
URBAN = [area for area in NRT_AREAS if area.radius_km <= 3.0]
DAY_TRIP = next(
    area
    for area in NRT_AREAS
    if area.radius_km > 5.0 and resolve_area("NRT", area.latitude, area.longitude) is area
)
FAR_AWAY = (38.0, 141.0)  # 250 km north of Tokyo: outside every NRT circle


def trip(**overrides: Any) -> TripPlan:
    values: dict[str, Any] = {
        "id": uuid4(),
        "user_id": uuid4(),
        "name": "東京五日",
        "mode": "manual",
        "total_price": Decimal("0"),
        "currency": "TWD",
        "data": {},
        "version": 1,
        "destination_name": "東京",
        "start_date": date(2026, 11, 10),
        "end_date": date(2026, 11, 15),
        "timezone": "Asia/Tokyo",
        "route_preference": "FEWER_TRANSFERS",
    }
    values.update(overrides)
    return TripPlan(**values)


def row(
    target: TripPlan,
    area: HotspotArea | None,
    *,
    day: date = date(2026, 11, 10),
    position: int = 0,
    coordinates: tuple[float, float] | None = None,
    **overrides: Any,
) -> TripPlanItem:
    if coordinates is None and area is not None:
        coordinates = (area.latitude, area.longitude)
    values: dict[str, Any] = {
        "id": uuid4(),
        "trip_plan_id": target.id,
        "item_type": "custom",
        "day_date": day,
        "position": position,
        "title": f"景點 {position}",
        "latitude": Decimal(str(coordinates[0])) if coordinates else None,
        "longitude": Decimal(str(coordinates[1])) if coordinates else None,
        "duration_minutes": 90,
        "locked": False,
        "is_estimated": False,
        "fixed_time": False,
        "is_skipped": False,
        "data": {},
    }
    values.update(overrides)
    return TripPlanItem(**values)


def hotel(
    hotel_id: str,
    latitude: float,
    longitude: float,
    nightly: int,
    *,
    provider: str = "mock",
    currency: str = "TWD",
    booking_url: str | None = None,
    breakfast: bool = True,
    review_score: float | None = 8.0,
    review_count: int | None = 100,
) -> HotelOffer:
    now = datetime.now(UTC)
    total = Decimal(nightly) * 2
    return HotelOffer(
        id=uuid5(NAMESPACE_URL, f"test:{provider}:{hotel_id}:{nightly}"),
        provider=provider,
        provider_offer_id=f"{hotel_id}:{nightly}",
        currency=currency,
        booking_url=booking_url,
        retrieved_at=now,
        expires_at=now + timedelta(minutes=10),
        hotel_id=hotel_id,
        hotel_name=f"Hotel {hotel_id}",
        latitude=latitude,
        longitude=longitude,
        rating=4,
        room_type="標準雙人房",
        check_in=now,
        check_out=now + timedelta(days=2),
        nights=2,
        base_price=total,
        taxes=Decimal(0),
        fees=Decimal(0),
        total_price=total,
        breakfast_included=breakfast,
        refundable=True,
        station_walk_minutes=0,
        nightly_price=Decimal(nightly),
        review_score=review_score,
        review_count=review_count,
    )


def test_evidence_items_skip_lodging_logistics_unlocated_rows_and_weight_meals() -> None:
    target = trip()
    rows = [
        row(target, URBAN[0], position=0),
        row(target, URBAN[0], position=1, system_role="lunch"),
        row(target, URBAN[1], position=2, system_role="hotel_start"),
        row(target, URBAN[1], position=3, item_type="flight"),
        row(target, URBAN[1], position=4, is_skipped=True),
        row(target, None, position=5),
        row(target, None, position=6, coordinates=(0.0, 0.0)),
        row(target, URBAN[1], position=7, is_estimated=True),
    ]

    items, excluded = evidence_items(rows, "NRT")

    assert excluded == {}
    assert [item.weight for item in items] == [1.0, 0.5, 0.6]
    assert [item.area.code for item in items if item.area] == [
        URBAN[0].code,
        URBAN[0].code,
        URBAN[1].code,
    ]


def test_score_stay_areas_ranks_by_itinerary_weight_and_penalises_day_trip_zones() -> None:
    target = trip()
    rows = [
        row(target, URBAN[0], position=0),
        row(target, URBAN[0], position=1, day=date(2026, 11, 11)),
        row(target, URBAN[0], position=2, day=date(2026, 11, 12)),
        row(target, URBAN[1], position=3),
        row(target, DAY_TRIP, position=4, day=date(2026, 11, 13), duration_minutes=480),
        row(target, None, position=5, coordinates=FAR_AWAY),
    ]
    items, _ = evidence_items(rows, "NRT")

    recommendation = score_stay_areas("NRT", items)

    assert recommendation.status == "recommended"
    assert recommendation.located_item_count == 6
    assert recommendation.unassigned_item_count == 1
    codes = [score.area.code for score in recommendation.areas]
    assert codes[0] == URBAN[0].code
    assert "most_items" in recommendation.areas[0].reasons
    assert "most_days" in recommendation.areas[0].reasons
    assert URBAN[1].code in codes
    day_trip = next(score for score in recommendation.areas if score.area.code == DAY_TRIP.code)
    assert day_trip.is_day_trip
    assert "day_trip_zone" in day_trip.reasons
    assert day_trip.score < recommendation.areas[0].score
    assert 2 <= len(recommendation.areas) <= 4


def test_score_stay_areas_falls_back_to_urban_catalog_areas_without_evidence() -> None:
    recommendation = score_stay_areas("NRT", [], current_lodging_area=URBAN[0])

    assert recommendation.status == "no_evidence"
    assert len(recommendation.areas) == 3
    assert all(score.area.radius_km <= 3.0 for score in recommendation.areas)
    assert all("destination_default" in score.reasons for score in recommendation.areas)
    assert "current_lodging" in recommendation.areas[0].reasons


def test_single_item_is_low_evidence_but_still_offers_a_second_area() -> None:
    target = trip()
    items, _ = evidence_items([row(target, URBAN[0])], "NRT")

    recommendation = score_stay_areas("NRT", items)

    assert recommendation.status == "low_evidence"
    assert len(recommendation.areas) >= STAY_AREA_MIN
    assert recommendation.areas[0].area.code == URBAN[0].code
    assert "central" in recommendation.areas[1].reasons


def test_extension_city_items_are_excluded_and_flagged() -> None:
    target = trip()
    rows = [
        row(target, URBAN[0], position=0),
        row(target, URBAN[0], position=1, data={"destination_id": "kamakura"}),
        row(target, URBAN[0], position=2, data={"destination_id": "kamakura"}),
    ]

    items, excluded = evidence_items(rows, "NRT", ("kamakura",))
    recommendation = score_stay_areas("NRT", items, excluded_extension=excluded)

    assert len(items) == 1
    assert excluded == {"kamakura": 2}
    assert recommendation.excluded_extension == {"kamakura": 2}
    assert "consider_second_stay" in recommendation.warnings


def test_trip_city_resolves_blank_and_search_trips_and_rejects_unknown_places() -> None:
    profile, city_code = trip_city(trip(), None)
    assert profile is not None and city_code == "NRT"

    profile, city_code = trip_city(trip(destination_name="Somewhere"), {"destination": "HND"})
    assert profile is not None and city_code == "NRT"

    assert trip_city(trip(destination_name="火星基地", data={}), None) == (None, None)


def test_stay_dates_cover_missing_past_ongoing_short_and_long_trips() -> None:
    today = date(2026, 9, 4)
    ready = stay_dates(trip(), today)
    assert (ready.status, ready.nights, ready.check_in, ready.check_out) == (
        "ready",
        5,
        date(2026, 11, 10),
        date(2026, 11, 15),
    )
    assert stay_dates(trip(start_date=None, end_date=None), today).status == "dates_missing"
    assert (
        stay_dates(trip(start_date=date(2026, 8, 1), end_date=date(2026, 8, 5)), today).status
        == "dates_past"
    )

    ongoing = stay_dates(trip(start_date=date(2026, 9, 1), end_date=date(2026, 9, 8)), today)
    assert ongoing.check_in == today
    assert "checkin_moved_to_today" in ongoing.notes

    single = stay_dates(trip(start_date=date(2026, 10, 1), end_date=date(2026, 10, 1)), today)
    assert single.nights == 1 and "assumed_one_night" in single.notes

    long_stay = stay_dates(trip(start_date=date(2026, 10, 1), end_date=date(2026, 11, 30)), today)
    assert long_stay.nights == 14 and "stay_truncated" in long_stay.notes


def test_stay_search_query_from_blank_trip_keeps_lodging_preferences_only() -> None:
    target = trip(
        end_date=date(2026, 11, 12),
        data={
            "travelers": {"adults": 2, "rooms": 1},
            "preferences": {
                "hotel_min_rating": 4,
                "breakfast_required": True,
                "preferred_areas": ["新宿"],
                "extension_destination_ids": ["kamakura"],
            },
        },
    )

    query = stay_search_query(target, "NRT", None, stay_dates(target, date(2026, 9, 4)), "ja")

    assert query.destination == "NRT"
    assert query.modules == [SearchModule.HOTEL]
    assert query.travelers.adults == 2
    assert query.preferences.hotel_min_rating == 4
    assert query.preferences.breakfast_required
    assert query.preferences.preferred_areas == []
    assert query.preferences.extension_destination_ids == []
    assert query.locale == "ja"
    assert query.currency == "TWD"


def test_split_area_offers_uses_radius_margin_and_nearest_fallback() -> None:
    area = URBAN[0]
    offers = [
        hotel("in-1", area.latitude + 0.001, area.longitude, 3000),
        hotel("in-2", area.latitude, area.longitude + 0.002, 2500),
        hotel("out-1", area.latitude + 0.1, area.longitude, 2000),
        hotel("out-2", area.latitude + 0.2, area.longitude, 2200),
        hotel("out-3", area.latitude + 0.3, area.longitude, 2400),
    ]

    in_area, nearby = split_area_offers(area, offers)

    assert {item.offer.hotel_id for item in in_area} == {"in-1", "in-2"}
    assert all(item.in_area for item in in_area)
    assert [item.offer.hotel_id for item in nearby] == ["out-1", "out-2", "out-3"]
    assert all(not item.in_area for item in nearby)
    assert nearby[0].distance_km < nearby[1].distance_km


@pytest.mark.asyncio
async def test_normalize_offers_converts_to_twd_flags_failures_and_dedupes_rooms() -> None:
    class FakeFx:
        async def rate_to_twd(self, currency: str) -> Any:
            if currency == "JPY":
                return SimpleNamespace(rate=Decimal("0.21"))
            raise FxRateError("no rate")

    area = URBAN[0]
    offers = [
        hotel("jpy", area.latitude, area.longitude, 10000, currency="JPY"),
        hotel("krw", area.latitude, area.longitude, 90000, currency="KRW"),
        hotel("unplaced", 0.0, 0.0, 1000),
        hotel("dup", area.latitude, area.longitude, 3000),
        hotel("dup", area.latitude, area.longitude, 2500),
    ]

    normalized = await normalize_offers(offers, FakeFx())  # type: ignore[arg-type]

    by_id = {offer.hotel_id: offer for offer in normalized}
    assert set(by_id) == {"jpy", "krw", "dup"}
    assert by_id["jpy"].currency == "TWD"
    assert by_id["jpy"].nightly_price == Decimal(2100)
    assert by_id["jpy"].total_price == Decimal(4200)
    assert by_id["jpy"].original_currency == "JPY"
    assert by_id["jpy"].original_total_price == Decimal(20000)
    assert by_id["jpy"].exchange_rate == Decimal("0.21")
    assert by_id["krw"].price_estimate_unavailable and by_id["krw"].currency == "KRW"
    assert by_id["dup"].nightly_price == Decimal(2500) and by_id["dup"].offer_count == 2


def test_rank_area_offers_keeps_gapped_hotels_after_full_matches() -> None:
    area = URBAN[0]
    query = SearchCreate(
        origin="TPE",
        destination="NRT",
        departure_date=date(2026, 11, 10),
        return_date=date(2026, 11, 12),
        modules=[SearchModule.HOTEL],
        preferences={"breakfast_required": True, "hotel_max_nightly_twd": 3000},
    )
    candidates = [
        AreaOffer(hotel("pricey", area.latitude, area.longitude, 5000), 0.1, True),
        AreaOffer(
            hotel("no-breakfast", area.latitude, area.longitude, 1500, breakfast=False), 0.2, True
        ),
        AreaOffer(hotel("full", area.latitude, area.longitude, 2000), 0.3, True),
    ]

    ranked = rank_area_offers(candidates, query.preferences, query.travelers)

    assert [item.offer.hotel_id for item in ranked.hotels] == ["full", "no-breakfast", "pricey"]
    assert ranked.filters.relaxed == []
    gaps = {offer_id: codes for offer_id, codes in ranked.filters.gaps.items()}
    assert gaps[candidates[1].offer.id] == ["breakfast"]
    assert gaps[candidates[0].offer.id] == ["nightly_max"]

    strict = rank_area_offers(candidates[:2], query.preferences, query.travelers)
    assert [constraint.code for constraint in strict.filters.relaxed] == ["breakfast"]


@pytest.mark.asyncio
async def test_filter_extraction_matches_optimizer_labels_and_can_ignore_station_walk() -> None:
    query = SearchCreate(
        origin="TPE",
        destination="NRT",
        departure_date=date(2026, 11, 10),
        return_date=date(2026, 11, 15),
        modules=[SearchModule.HOTEL],
        preferences={"hotel_min_review_count": 1000, "max_station_walk_minutes": 1},
    )
    hotels = await MockProvider().search_hotels(query)
    optimizer = TripOptimizer()

    matches = optimizer._filter_hotels(query, hotels)
    result = filter_hotels_with_relaxation(query.preferences, 1, hotels)

    assert matches
    assert optimizer.relaxed_hotel_preferences == [item.label for item in result.relaxed]
    assert "最低評論筆數" in optimizer.relaxed_hotel_preferences
    lenient = filter_hotels_with_relaxation(query.preferences, 1, hotels, ignore_station_walk=True)
    assert "station_walk" not in {item.code for item in lenient.relaxed}
    assert all("station_walk" not in codes for codes in lenient.gaps.values())


def test_stay_partner_options_follow_owner_order_and_link_kinds() -> None:
    settings = Settings(
        agoda_enabled=True,
        agoda_cid="cid",
        agoda_affiliate_url_template="https://www.agoda.com/search?textToSearch={query}",
    )
    booked = hotel(
        "b-1",
        35.7,
        139.7,
        4000,
        provider="booking",
        booking_url="https://www.booking.com/hotel/jp/test.html",
    )

    with_hotel = stay_partner_options(settings, "淺草", booked)
    assert [(item["partner"], item["kind"]) for item in with_hotel] == [
        ("agoda", "hotel_search"),
        ("booking", "deep_link"),
    ]
    assert [item["kind"] for item in stay_partner_options(settings, "淺草", None)] == [
        "area_search"
    ]
    assert "淺草" in stay_partner_options(settings, "淺草", None)[0]["cta"]
    mock_hotel = hotel("m-1", 35.7, 139.7, 4000)
    assert [item["partner"] for item in stay_partner_options(settings, "淺草", mock_hotel)] == [
        "agoda"
    ]


def test_stay_partner_options_hide_a_partner_without_a_hotel_target() -> None:
    # Travelpayouts counts as configured once any one module target is set, so a hotel
    # button must not render off a flight-only setup: clicking it would have no link.
    base = {
        "travelpayouts_enabled": True,
        "travelpayouts_api_token": "token",
        "travelpayouts_marker": "123",
        "travelpayouts_project_id": "456",
        "travelpayouts_flight_target_url": "https://tp.st/flights",
    }
    flight_only = Settings.model_validate(base)
    with_hotel = Settings.model_validate(
        {**base, "travelpayouts_hotel_target_url": "https://tp.st/hotels"}
    )
    static_template = Settings.model_validate(
        {**base, "travelpayouts_static_url_template": "https://tp.st/go?sub_id={sub_id}"}
    )

    assert stay_partner_options(flight_only, "淺草", None) == []
    assert [item["partner"] for item in stay_partner_options(with_hotel, "淺草", None)] == [
        "travelpayouts"
    ]
    assert [item["partner"] for item in stay_partner_options(static_template, "淺草", None)] == [
        "travelpayouts"
    ]


@pytest.mark.asyncio
async def test_mock_provider_searches_near_a_point_deterministically() -> None:
    query = SearchCreate(
        origin="TPE",
        destination="NRT",
        departure_date=date(2026, 11, 10),
        return_date=date(2026, 11, 12),
        modules=[SearchModule.HOTEL],
    )
    provider = MockProvider()

    near = await provider.search_hotels_near(query, latitude=35.71, longitude=139.80, radius_km=1)
    again = await provider.search_hotels_near(query, latitude=35.71, longitude=139.80, radius_km=1)
    citywide = await provider.search_hotels(query)

    assert len(near) == 4
    assert [offer.id for offer in near] == [offer.id for offer in again]
    assert not {offer.id for offer in near} & {offer.id for offer in citywide}
    assert all(
        haversine_km(35.71, 139.80, offer.latitude, offer.longitude) <= 1.5 for offer in near
    )
