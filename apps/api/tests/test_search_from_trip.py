"""Searching from a saved trip: criteria derivation and offer-backed anchors."""

from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from app.models import TripPlan, TripPlanItem
from app.problems import AppError
from app.providers.schemas import FlightOffer, FlightSegment
from app.search.schemas import SearchCreate, SearchModule
from app.trips.flight_anchor import apply_flight_offer, offer_has_leg, offer_leg_date
from app.trips.search_criteria import (
    ORIGIN_OPTIONS,
    TRIP_SEARCH_OVERRIDES,
    derive_trip_search,
    trip_search_criteria,
)

TODAY = date(2026, 9, 1)
START, END = date(2026, 11, 10), date(2026, 11, 14)


def _trip(**overrides: object) -> TripPlan:
    values: dict[str, object] = {
        "id": uuid4(),
        "user_id": uuid4(),
        "name": "東京五日",
        "mode": "manual",
        "total_price": Decimal(0),
        "currency": "TWD",
        "data": {
            "source": "blank",
            "origin_airport": "TPE",
            "travelers": {"adults": 2, "children": 1, "children_ages": [8], "rooms": 1},
            "preferences": {"pace": "relaxed", "interests": ["food"], "budget_twd": 60000},
        },
        "version": 1,
        "destination_name": "日本東京",
        "start_date": START,
        "end_date": END,
        "timezone": "Asia/Tokyo",
    }
    values.update(overrides)
    return TripPlan(**values)


SEARCH_JSON = {
    "trip_type": "round_trip",
    "origin": "KHH",
    "destination": "HND",
    "departure_date": "2026-11-10",
    "return_date": "2026-11-14",
    "travelers": {"adults": 3, "children": 0, "children_ages": [], "rooms": 2},
    "modules": ["flight", "hotel"],
    "preferences": {"pace": "packed", "extension_destination_ids": []},
    "cabin_class": "premium_economy",
}


def test_blank_trip_yields_a_round_trip_from_its_own_keys() -> None:
    trip = _trip()
    query = trip_search_criteria(
        trip, None, modules=[SearchModule.FLIGHT], locale="ja", today=TODAY
    )
    assert query.trip_id == trip.id
    assert (query.origin, query.destination) == ("TPE", "NRT")
    assert (query.departure_date, query.return_date) == (START, END)
    assert query.travelers.adults == 2 and query.travelers.children_ages == [8]
    assert query.preferences.pace == "relaxed" and query.preferences.budget_twd == 60000
    assert query.modules == [SearchModule.FLIGHT]
    assert query.cabin_class == "economy"
    assert query.locale == "ja" and query.currency == "TWD"
    assert not query.flexible_dates


def test_search_sourced_trip_keeps_the_airport_and_party_it_was_searched_with() -> None:
    trip = _trip(data={"source": "search", "origin_airport": "KHH"})
    query = trip_search_criteria(
        trip, SEARCH_JSON, modules=[SearchModule.FLIGHT], locale="zh-TW", today=TODAY
    )
    # HND is a catalog alias for Tokyo: the search that built the trip used it,
    # so the follow-up search does too instead of quietly moving to NRT.
    assert (query.origin, query.destination) == ("KHH", "HND")
    assert query.travelers.adults == 3 and query.travelers.rooms == 2
    assert query.preferences.pace == "packed"
    assert query.cabin_class == "premium_economy"


def test_extension_cities_never_leak_into_the_flight_search() -> None:
    # Extension ids carry a "trip must be four days" rule that has nothing to
    # do with the flight, and a two-day trip must still be searchable.
    trip = _trip(
        end_date=date(2026, 11, 11),
        data={
            "origin_airport": "TPE",
            "preferences": {"extension_destination_ids": ["jp-kyoto"], "pace": "balanced"},
        },
    )
    query = trip_search_criteria(
        trip, None, modules=[SearchModule.FLIGHT], locale="zh-TW", today=TODAY
    )
    assert query.preferences.extension_destination_ids == []


@pytest.mark.parametrize(
    ("overrides", "code"),
    [
        ({"data": {}}, "trip_origin_required"),
        (
            {"data": {"origin_airport": "TPE"}, "destination_name": "月球"},
            "trip_destination_unsupported",
        ),
        ({"start_date": None, "end_date": None}, "trip_dates_required"),
        ({"start_date": date(2026, 8, 30), "end_date": date(2026, 9, 2)}, "trip_dates_past"),
        ({"end_date": START}, "trip_dates_too_short"),
    ],
)
def test_each_gap_is_reported_with_its_own_code(overrides: dict[str, object], code: str) -> None:
    trip = _trip(**overrides)
    derivation = derive_trip_search(
        trip, None, modules=[SearchModule.FLIGHT], locale="zh-TW", today=TODAY
    )
    assert [issue.code for issue in derivation.issues] == [code]
    with pytest.raises(AppError) as raised:
        trip_search_criteria(trip, None, modules=[SearchModule.FLIGHT], locale="zh-TW", today=TODAY)
    assert raised.value.status == 422 and raised.value.code == code


def test_derivation_still_returns_what_it_could_read_next_to_the_issues() -> None:
    derivation = derive_trip_search(
        _trip(data={}), None, modules=[SearchModule.FLIGHT], locale="zh-TW", today=TODAY
    )
    assert derivation.fields["origin"] is None
    assert derivation.fields["destination"] == "NRT"
    assert derivation.fields["departure_date"] == "2026-11-10"
    assert derivation.fields["trip_id"] == str(derivation.fields["trip_id"])
    assert ORIGIN_OPTIONS == ("TPE", "TSA", "KHH")


def test_an_explicit_field_settles_the_issue_the_trip_could_not() -> None:
    trip = _trip(data={"travelers": {"adults": 1}})
    query = trip_search_criteria(
        trip,
        None,
        modules=[SearchModule.FLIGHT],
        locale="zh-TW",
        overrides={"origin": "TSA", "preferences": {"avoid_red_eye": True}},
        today=TODAY,
    )
    assert query.origin == "TSA"
    assert query.preferences.avoid_red_eye is True
    assert query.destination == "NRT"


def test_explicit_dates_are_still_validated_as_a_round_trip() -> None:
    with pytest.raises(Exception) as raised:
        trip_search_criteria(
            _trip(),
            None,
            modules=[SearchModule.FLIGHT],
            locale="zh-TW",
            overrides={"departure_date": "2026-11-14", "return_date": "2026-11-10"},
            today=TODAY,
        )
    # The same 422 the request body would have produced on its own.
    assert raised.type.__name__ == "RequestValidationError"


def test_overridable_fields_exclude_what_the_trip_owns() -> None:
    assert "trip_id" not in TRIP_SEARCH_OVERRIDES
    assert "modules" not in TRIP_SEARCH_OVERRIDES
    assert "legs" not in TRIP_SEARCH_OVERRIDES
    assert {"origin", "destination", "departure_date", "return_date"} <= TRIP_SEARCH_OVERRIDES


def test_search_create_accepts_a_bare_trip_id_and_rejects_multi_city_with_one() -> None:
    bare = SearchCreate.model_validate({"trip_id": str(uuid4()), "modules": ["flight"]})
    assert bare.origin is None and bare.trip_id is not None
    with pytest.raises(ValidationError):
        SearchCreate.model_validate({"modules": ["flight"]})
    with pytest.raises(ValidationError):
        SearchCreate.model_validate(
            {"trip_id": str(uuid4()), "modules": ["flight"], "trip_type": "multi_city"}
        )


def _offer(*, return_leg: bool = True) -> FlightOffer:
    now = datetime(2026, 9, 1, tzinfo=UTC)
    segments = [
        FlightSegment(
            origin="TPE",
            destination="NRT",
            departure_time=datetime.fromisoformat("2026-11-10T08:50:00+08:00"),
            arrival_time=datetime.fromisoformat("2026-11-10T13:10:00+09:00"),
            airline="長榮航空",
            flight_number="BR198",
            leg_index=0,
            departure_timezone="Asia/Taipei",
            arrival_timezone="Asia/Tokyo",
        )
    ]
    if return_leg:
        segments.append(
            FlightSegment(
                origin="NRT",
                destination="TPE",
                departure_time=datetime.fromisoformat("2026-11-14T14:20:00+09:00"),
                arrival_time=datetime.fromisoformat("2026-11-14T17:10:00+08:00"),
                airline="長榮航空",
                flight_number="BR197",
                leg_index=1,
                departure_timezone="Asia/Tokyo",
                arrival_timezone="Asia/Taipei",
            )
        )
    return FlightOffer(
        id=UUID("00000000-0000-4000-8000-00000000f1a1"),
        provider="amadeus",
        provider_offer_id="AMA-1",
        retrieved_at=now,
        expires_at=now,
        source_mode="live",
        is_mock=False,
        is_bookable=True,
        origin="TPE",
        destination="NRT",
        departure_time=segments[0].departure_time,
        arrival_time=segments[0].arrival_time,
        duration_minutes=200,
        segments=segments,
        airline="長榮航空",
        flight_number="BR198",
        base_price=Decimal("9000"),
        taxes=Decimal("2000"),
        fees=Decimal("500"),
        baggage_price=Decimal(0),
        total_price=Decimal("11500"),
        carry_on=True,
        checked_baggage_kg=23,
        refundable=False,
        changeable=True,
        return_departure_time=segments[1].departure_time if return_leg else None,
        return_arrival_time=segments[1].arrival_time if return_leg else None,
    )


def _anchor(role: str, day: date) -> TripPlanItem:
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=uuid4(),
        item_type="flight",
        day_date=day,
        position=0,
        title="去程航班尚未設定",
        locked=True,
        fixed_time=True,
        is_estimated=True,
        system_role=role,
        data={
            "source_mode": "system",
            "flight_selection_source": "unset",
            "flight_info": None,
            "price_snapshot": {"total_price": "1", "currency": "TWD"},
            "destination_city": "東京",
        },
    )


def test_an_offer_backed_anchor_keeps_the_offer_id_the_quote_and_local_times() -> None:
    item = _anchor("outbound_flight", START)
    offer = _offer()
    apply_flight_offer(item, "outbound_flight", offer)
    assert item.offer_id == offer.id
    assert item.title == "長榮航空 BR198"
    assert item.location_name == "TPE → NRT"
    assert item.start_time == offer.departure_time and item.end_time == offer.arrival_time
    assert item.locked and item.fixed_time and not item.is_estimated
    assert item.data["flight_selection_source"] == "offer"
    assert item.data["flight_leg"] == "outbound"
    assert item.data["source_mode"] == "live" and item.data["is_bookable"] is True
    assert item.data["flight_info"]["departure_local"] == "2026-11-10T08:50"
    assert item.data["flight_info"]["arrival_timezone"] == "Asia/Tokyo"
    assert item.data["price_snapshot"]["total_price"] == "11500"
    assert item.data["price_snapshot"]["provider"] == "amadeus"
    # Keys that describe the trip rather than the flight survive the swap.
    assert item.data["destination_city"] == "東京"


def test_the_return_anchor_takes_the_second_leg() -> None:
    item = _anchor("return_flight", END)
    apply_flight_offer(item, "return_flight", _offer())
    assert item.title == "長榮航空 BR197"
    assert item.location_name == "NRT → TPE"
    assert item.data["flight_leg"] == "return"
    assert item.data["flight_info"]["departure_local"] == "2026-11-14T14:20"
    assert offer_leg_date(_offer(), "return_flight") == END
    assert offer_leg_date(_offer(), "outbound_flight") == START


def test_a_one_way_offer_has_no_return_leg_to_attach() -> None:
    assert offer_has_leg(_offer(return_leg=False), "outbound_flight")
    assert not offer_has_leg(_offer(return_leg=False), "return_flight")
    assert offer_has_leg(_offer(), "return_flight")
