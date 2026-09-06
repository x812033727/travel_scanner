"""Reading a stored search back is a boundary, and it answers with a status code.

Two routers write ``SearchRequest.request_json`` in two different shapes, and ownership is
the only thing the flight-source endpoints check before reading one. A row written by the
other router can never validate here, so the guards below decide whether that mismatch is a
conflict the caller can read or a pydantic ``ValidationError`` escaping as a 500.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

import pytest

from app.models import FlightOfferRecord, SearchRequest
from app.problems import AppError
from app.providers.live_back_to_back import LiveBackToBackSearch, LiveTripDates
from app.search.router import _stored_offer, _stored_offers, _stored_query
from app.search.schemas import SearchCreate


def _travel_search() -> dict:
    return SearchCreate.model_validate({
        "origin": "TPE",
        "destination": "NRT",
        "departure_date": (date.today() + timedelta(days=30)).isoformat(),
        "return_date": (date.today() + timedelta(days=35)).isoformat(),
        "modules": ["flight"],
    }).model_dump(mode="json")


def _back_to_back() -> dict:
    first = date.today() + timedelta(days=30)
    return LiveBackToBackSearch.model_validate({
        "origin": "TPE",
        "first_destination": "NRT",
        "second_destination": "ICN",
        "first_trip": LiveTripDates(
            departure_date=first, return_date=first + timedelta(days=4)
        ).model_dump(mode="json"),
        "second_trip": LiveTripDates(
            departure_date=first + timedelta(days=10),
            return_date=first + timedelta(days=14),
        ).model_dump(mode="json"),
    }).model_dump(mode="json")


def _offer(**overrides: object) -> dict:
    departure = datetime.now(UTC) + timedelta(days=30)
    payload: dict[str, object] = {
        "id": str(uuid4()),
        "provider": "amadeus",
        "provider_offer_id": "offer-1",
        "currency": "TWD",
        "retrieved_at": datetime.now(UTC).isoformat(),
        "expires_at": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
        "origin": "TPE",
        "destination": "NRT",
        "departure_time": departure.isoformat(),
        "arrival_time": (departure + timedelta(hours=3)).isoformat(),
        "duration_minutes": 180,
        "segments": [{
            "origin": "TPE",
            "destination": "NRT",
            "departure_time": departure.isoformat(),
            "arrival_time": (departure + timedelta(hours=3)).isoformat(),
            "airline": "BR",
            "flight_number": "BR198",
        }],
        "airline": "BR",
        "flight_number": "BR198",
        "base_price": "10000",
        "taxes": "1500",
        "fees": "300",
        "baggage_price": "200",
        "total_price": "12000",
        "carry_on": True,
        "checked_baggage_kg": 23,
        "refundable": False,
        "changeable": True,
    }
    payload.update(overrides)
    return payload


def test_a_back_to_back_row_can_never_be_read_as_a_travel_search() -> None:
    """The premise of the guard: these two shapes are genuinely incompatible."""
    with pytest.raises(ValueError):
        SearchCreate.model_validate(_back_to_back())


def test_expanding_a_row_written_by_another_endpoint_is_a_conflict() -> None:
    search = SearchRequest(
        user_id=uuid4(),
        operation="live_back_to_back_fare_search",
        request_json=_back_to_back(),
    )
    with pytest.raises(AppError) as raised:
        _stored_query(search)
    assert raised.value.status == 409
    assert raised.value.code == "search_not_expandable"


def test_a_travel_search_still_reads_back_as_its_own_query() -> None:
    search = SearchRequest(
        user_id=uuid4(), operation="travel_search", request_json=_travel_search()
    )
    assert _stored_query(search).destination == "NRT"


def test_offers_that_no_longer_parse_are_a_conflict_not_a_crash() -> None:
    search = SearchRequest(
        user_id=uuid4(),
        operation="travel_search",
        request_json=_travel_search(),
        result_json={"modules": {"flight": [_offer(), {"provider": "amadeus"}]}},
    )
    with pytest.raises(AppError) as raised:
        _stored_offers(search)
    assert raised.value.status == 409
    assert raised.value.code == "search_offers_unreadable"


def test_readable_offers_come_back_with_an_itinerary_key() -> None:
    search = SearchRequest(
        user_id=uuid4(),
        operation="travel_search",
        request_json=_travel_search(),
        result_json={"modules": {"flight": [_offer()]}},
    )
    offers = _stored_offers(search)
    assert len(offers) == 1
    assert offers[0].itinerary_key


def test_a_search_with_no_flight_module_reads_as_no_offers() -> None:
    search = SearchRequest(
        user_id=uuid4(),
        operation="live_back_to_back_fare_search",
        request_json=_back_to_back(),
        result_json={"pairs": []},
    )
    assert _stored_offers(search) == []


def test_one_unreadable_offer_record_is_a_conflict() -> None:
    record = FlightOfferRecord(
        search_id=uuid4(),
        provider="amadeus",
        data={"provider": "amadeus"},
        total_price=0,
        currency="TWD",
    )
    with pytest.raises(AppError) as raised:
        _stored_offer(record)
    assert raised.value.status == 409
    assert raised.value.code == "offer_unreadable"
