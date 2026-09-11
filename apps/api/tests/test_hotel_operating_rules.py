"""Calendar contracts and boundary cases for unavailable accommodation nights."""

from copy import deepcopy
from datetime import UTC, date, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.models import TravelServiceProduct
from app.problems import AppError
from app.travel_services.hotel_operating import (
    hotel_publicly_available,
    hotel_stay_available,
    hotel_today,
    require_hotel_booking_target,
    require_hotel_stay,
)
from app.travel_services.schemas import Facts, HotelOperatingRules, ProductInput

NOW = datetime(2026, 9, 11, tzinfo=UTC)
BLACKOUT = {
    "start_date": "2027-01-14", "end_date": "2027-01-16",
    "reason": "Conservative nights affected by the published maintenance closure",
    "source_url": "https://hotel.example.org/notices/maintenance",
}
CUTOFF = {
    "last_checkout_date": "2027-05-09",
    "last_checkout_reason": "Published final checkout date",
    "last_checkout_source_url": "https://hotel.example.org/notices/closure",
}


def hotel(rules=None, *, destination="kyoto", kind="hotel"):
    return TravelServiceProduct(
        id=uuid4(), kind=kind, destination_id=destination,
        facts={"hotel_operating_rules": rules} if rules is not None else {},
    )


def test_optional_policy_and_conservative_night_contract_roundtrip():
    assert Facts().hotel_operating_rules is None
    value = HotelOperatingRules.model_validate({"unavailable_stays": [BLACKOUT], **CUTOFF})
    assert value.unavailable_stays[0].start_date == date(2027, 1, 14)
    assert value.model_dump(mode="json")["last_checkout_date"] == "2027-05-09"
    require_hotel_stay(hotel(), now=NOW)
    require_hotel_stay(hotel({"malformed": True}, kind="tour"), now=NOW)


@pytest.mark.parametrize("start,end,allowed", [
    ("2027-01-12", "2027-01-14", True),
    ("2027-01-14", "2027-01-15", False),
    ("2027-01-13", "2027-01-16", False),
    ("2027-01-15", "2027-01-16", False),
    ("2027-01-16", "2027-01-17", True),
    ("2027-05-08", "2027-05-09", True),
    ("2027-05-08", "2027-05-10", False),
    ("2027-05-09", "2027-05-10", False),
    ("2027-01-17", "2027-01-17", False),
])
def test_half_open_nights_and_last_checkout(start, end, allowed):
    assert hotel_stay_available(
        hotel({"unavailable_stays": [BLACKOUT], **CUTOFF}),
        date.fromisoformat(start), date.fromisoformat(end), now=NOW,
    ) is allowed


@pytest.mark.parametrize("start,end", [(None, None), (date(2027, 1, 1), None)])
def test_restricted_hotel_cannot_omit_dates(start, end):
    with pytest.raises(AppError) as caught:
        require_hotel_stay(hotel({"unavailable_stays": [BLACKOUT]}), start, end, now=NOW)
    assert caught.value.code == "hotel_operating_dates_required"


@pytest.mark.parametrize("destination,utc_boundary", [
    ("kyoto", datetime(2027, 5, 8, 15, tzinfo=UTC)),
    ("seoul", datetime(2027, 5, 8, 15, tzinfo=UTC)),
    ("taipei", datetime(2027, 5, 8, 16, tzinfo=UTC)),
])
def test_final_checkout_uses_destination_midnight(destination, utc_boundary):
    from datetime import timedelta

    product = hotel(CUTOFF, destination=destination)
    assert hotel_today(product, utc_boundary) == date(2027, 5, 9)
    assert hotel_publicly_available(product, utc_boundary - timedelta(microseconds=1))
    assert not hotel_publicly_available(product, utc_boundary)
    with pytest.raises(AppError, match="最後可退房"):
        require_hotel_stay(product, date(2027, 5, 9), date(2027, 5, 10), now=utc_boundary)


@pytest.mark.parametrize("updates", [
    {"start_date": "2027-01-16"}, {"end_date": "2027-01-13"},
    {"start_date": "2027-02-30"}, {"start_date": "2027-1-14"},
    {"start_date": "2027-01-14T00:00:00Z"}, {"start_date": 1799884800},
    {"start_date": datetime(2027, 1, 14)}, {"reason": "  "},
    {"source_url": "http://hotel.example.org/notice"},
    {"source_url": "https://maps.google.com/notice"},
    {"source_url": "https://map.naver.com/p/entry/place/123"},
    {"source_url": "https://127.0.0.1/notice"},
    {"source_url": "https://user:password@hotel.example.org/notice"},
    {"extra": "ignored by older clients"},
])
def test_invalid_blackout_rejected(updates):
    with pytest.raises(ValidationError):
        HotelOperatingRules.model_validate({"unavailable_stays": [{**BLACKOUT, **updates}]})


@pytest.mark.parametrize("rules", [
    {}, {"unavailable_stays": [BLACKOUT] * 2}, {"unavailable_stays": [BLACKOUT] * 51},
    {"unavailable_stays": [BLACKOUT, {**BLACKOUT, "start_date": "2027-01-15"}]},
    {"last_checkout_date": "2027-05-09"},
    {**CUTOFF, "last_checkout_reason": "  "},
    {**CUTOFF, "last_checkout_source_url": "https://google.com/notice"},
    {**CUTOFF, "last_checkout_date": "2027-02-29"},
    {**CUTOFF, "last_checkout_date": True},
    {**CUTOFF, "unrecognized": True},
])
def test_invalid_rules_rejected(rules):
    with pytest.raises(ValidationError):
        HotelOperatingRules.model_validate(rules)


def test_adjacent_ranges_are_valid_and_canonicalized_without_mutating_input():
    second = {**BLACKOUT, "start_date": "2027-01-16", "end_date": "2027-01-17"}
    raw = {"unavailable_stays": [second, deepcopy(BLACKOUT)]}
    value = HotelOperatingRules.model_validate(raw)
    assert value.unavailable_stays[0].start_date == date(2027, 1, 14)
    assert raw["unavailable_stays"][0] == second


@pytest.mark.parametrize("malformed", [{}, [], False, "invalid", {"unavailable_stays": [{}]}])
def test_malformed_stored_rules_fail_closed(malformed):
    product = hotel(malformed)
    assert not hotel_publicly_available(product, NOW)
    with pytest.raises(AppError) as caught:
        require_hotel_stay(product, date(2027, 1, 1), date(2027, 1, 2), now=NOW)
    assert caught.value.code == "hotel_operating_rules_invalid"


def test_nonhotel_input_cannot_gain_hotel_rules():
    with pytest.raises(ValidationError, match="only supported for hotels"):
        ProductInput(
            source_key="tour-example", kind="tour", destination_id="kyoto", title="Tour",
            source_url="https://hotel.example.org/", facts={"hotel_operating_rules": CUTOFF},
        )


@pytest.mark.parametrize("query", [
    "checkin=2027-01-14&checkout=2027-01-15", "hotel_id=123", "arrival=2027-01-14",
    "opaque=some-necessary-property-or-stay-value",
])
def test_saved_queries_are_never_rewritten_for_restricted_hotels(query):
    target = f"https://hotel.example.org/book?{query}"
    policy = {"unavailable_stays": [BLACKOUT]}
    with pytest.raises(AppError) as caught:
        require_hotel_booking_target(hotel(policy), target)
    assert caught.value.code == "hotel_operating_rules_invalid"
    require_hotel_booking_target(hotel(), target)
    require_hotel_booking_target(hotel(policy, kind="tour"), target)
    require_hotel_booking_target(hotel(policy), "https://hotel.example.org/book")
