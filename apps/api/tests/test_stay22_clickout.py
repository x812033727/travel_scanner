"""Allez building is deterministic and never makes a real affiliate click."""

from datetime import date, timedelta
from urllib.parse import parse_qs, quote, urlsplit

import pytest
from pydantic import ValidationError

from app.models import HotelBookingOption
from app.travel_services.schemas import (
    CatalogConfig,
    HotelBookingContext,
    HotelConfigPatch,
    Stay22Config,
)
from app.travel_services.stay22 import (
    booking_channel,
    build_stay22_url,
    stay22_eligible,
    validate_booking_context,
    validate_stay22_target,
)

TARGETS = {
    "booking": "https://www.booking.com/hotel/jp/example.zh-tw.html",
    "agoda": "https://www.agoda.com/zh-tw/example/hotel/tokyo-jp.html",
    "expedia": "https://www.expedia.com/Tokyo-Hotels-Example.h123456.Hotel-Information",
}


def active_config():
    return Stay22Config(enabled=True, enabled_providers=["booking", "agoda", "expedia"])


@pytest.mark.parametrize("provider", TARGETS)
def test_fixed_provider_exact_property_once_encoded_no_network(provider):
    start = date.today() + timedelta(days=40)
    context = HotelBookingContext(
        check_in=start,
        check_out=start + timedelta(days=21),
        adults=3,
        children=2,
        rooms=2,
        children_ages=[5, 11],
    )
    result = build_stay22_url(
        provider, TARGETS[provider], active_config(), context=context,
        destination_id="tokyo", locale="zh-TW", placement="trip",
    )
    parsed = urlsplit(result)
    assert parsed.scheme == "https" and parsed.netloc == "www.stay22.com"
    assert parsed.path == f"/allez/{provider}"
    assert parse_qs(parsed.query) == {
        "aid": ["mokaair"],
        "link": [TARGETS[provider]],
        "campaign": [f"mokaair_tokyo_{provider}_zh_TW_trip"],
        "lang": ["zh-TW"],
        "currency": ["TWD"],
        "checkin": [str(start)],
        "checkout": [str(start + timedelta(days=21))],
        "adults": ["3"],
        "children": ["2"],
    }
    assert f"link={quote(TARGETS[provider], safe='')}" in result
    assert "rooms" not in result and "ages" not in result


def test_percent_encoded_property_kept_opaque_without_double_decoding():
    target = "https://www.booking.com/hotel/jp/%E6%9D%B1%E4%BA%AC.html"
    result = build_stay22_url("booking", target, active_config(), destination_id="tokyo")
    assert parse_qs(urlsplit(result).query)["link"] == [target]
    assert "%25E6%259D%25B1" in result  # Encoding the URL once preserves its own path encoding.


@pytest.mark.parametrize("provider,target", [
    ("official", "https://hotel.example.com/stay"),
    ("trip_com", "https://trip.com/hotels/tokyo-hotel-detail-1"),
    ("booking", "https://booking.com/hotel/jp/test.html?checkin=2027-01-01"),
    ("booking", "https://booking.com/hotel/jp/test.html?adults=2"),
    ("booking", "https://booking.com/hotel/jp/test.html?label=someone"),
    ("booking", "https://booking.com/hotel/jp/test.html?aid=123"),
    ("booking", "https://booking.com/hotel/jp/test.html?%2561id=123"),
    ("booking", "https://booking.com/hotel/jp/test.html?unknown=something"),
    ("booking", "https://booking.com/hotel/jp/test.html?link=https%3A%2F%2Fevil.example.com"),
    ("booking", "https://booking.com/hotel/jp/test.html?utm_campaign=something"),
    ("booking", "https://booking.com/hotel/jp/test.html#aid=123"),
    ("booking", "http://booking.com/hotel/jp/test.html"),
    ("booking", "https://user:secret@booking.com/hotel/jp/test.html"),
    ("booking", "https://booking.com:8443/hotel/jp/test.html"),
    ("booking", "https://booking.com.evil.example.com/hotel/jp/test.html"),
    ("booking", "https://127.0.0.1/hotel/jp/test.html"),
    ("booking", "https://booking.com/searchresults.html"),
    ("booking", "https://booking.com/city/jp/tokyo.html"),
    ("booking", "https://booking.com/hotel/jp/%252e%252e"),
    ("booking", "https://booking.com/hotel/jp/test%253Fredirect%253Devil"),
    ("booking", "https://booking.com/hotel/jp/test%25253Fredirect%25253Devil"),
    ("booking", "https://booking.com/hotel/jp/test%xx.html"),
    ("booking", "https://booking.com/hotel/jp/test%0a.html"),
    ("booking", "https://booking.com/hotel/jp/test%5c.html"),
    ("agoda", "https://www.agoda.com/search?city=1"),
    ("agoda", "https://www.agoda.com/redirect.html"),
    ("expedia", "https://www.expedia.com/Hotel-Search"),
    ("expedia", "https://www.expedia.com/Seattle-Hotels"),
    ("expedia", TARGETS["booking"]),
])
def test_no_ambiguous_context_redirect_search_or_foreign_target(provider, target):
    with pytest.raises(ValueError):
        validate_stay22_target(provider, target)


@pytest.mark.parametrize("provider,target", [
    ("booking", "https://booking.com/hotel/jp/test/"),
    ("agoda", "https://www.agoda.com/test/hotel/seoul-kr.html"),
    ("agoda", "https://www.agoda.com/ja/test/hotel/tokyo-jp.html"),
    ("expedia", "https://www.expedia.co.uk/Tokyo-Hotels-Example.h123.Hotel-Information"),
])
def test_recognized_canonical_variants(provider, target):
    assert validate_stay22_target(provider, target) == target


def test_default_off_config_independent_factories_and_patch_presence():
    default = CatalogConfig()
    assert default.stay22.model_dump() == {
        "enabled": False, "aid": "mokaair", "enabled_providers": [],
        "integration_mode": "allez", "lma_id": None,
    }
    default.stay22.enabled_providers.append("booking")
    assert CatalogConfig().stay22.enabled_providers == []
    assert HotelConfigPatch(version=1, hotel_enabled=True).model_fields_set == {
        "version", "hotel_enabled",
    }
    assert HotelConfigPatch(version=1, stay22=active_config()).stay22.enabled


@pytest.mark.parametrize("payload", [
    {"enabled": "true"}, {"enabled": 1}, {"aid": ""},
    {"aid": "mokaair&link=https://evil.example.com"}, {"aid": " a "},
    {"enabled_providers": ["official"]}, {"enabled_providers": ["booking", "booking"]},
    {"api_key": "not-supported"}, {"aid": "a" * 129},
])
def test_invalid_or_unsupported_config_rejected(payload):
    with pytest.raises(ValidationError):
        Stay22Config.model_validate(payload)


@pytest.mark.parametrize("payload", [
    {"check_in": "2027-01-01"}, {"check_out": "2027-01-02"},
    {"check_in": "2027-01-02", "check_out": "2027-01-02"},
    {"check_in": "2027-01-02", "check_out": "2027-01-01"},
    {"check_in": 1798761600, "check_out": 1798934400},
    {"check_in": "2027-01-01T00:00:00Z", "check_out": "2027-01-02T00:00:00Z"},
    {"adults": True}, {"adults": 0}, {"adults": 10}, {"children": -1}, {"children": 10},
    {"rooms": 0}, {"rooms": 5}, {"children_ages": [-1]}, {"children_ages": [18]},
    {"children_ages": [True]}, {"children": 0, "children_ages": [5]},
    {"children": 2, "children_ages": [5]}, {"aid": "injected"},
    {"target": "https://evil.example.com"}, {"campaign": "user-private-id"},
])
def test_context_bounds_no_extra_identifiers_or_silent_repair(payload):
    with pytest.raises(ValidationError):
        HotelBookingContext.model_validate(payload)


def test_past_context_retained_for_editor_but_clickout_rejects_and_never_shortens():
    old = HotelBookingContext(check_in=date(2020, 1, 1), check_out=date(2020, 1, 9))
    with pytest.raises(ValueError, match="past"):
        build_stay22_url(
            "booking", TARGETS["booking"], active_config(), context=old, destination_id="tokyo"
        )
    assert old.check_out == date(2020, 1, 9)
    current = HotelBookingContext(check_in=date(2027, 1, 1), check_out=date(2027, 2, 15))
    assert validate_booking_context(current, today=date(2027, 1, 1)) == current


def test_empty_context_never_injects_guessed_dates_or_guests():
    result = build_stay22_url(
        "booking", TARGETS["booking"], active_config(), context=HotelBookingContext(),
        destination_id="seoul", locale="ko", placement="hotspot",
    )
    query = parse_qs(urlsplit(result).query)
    assert not {"checkin", "checkout", "adults", "children"} & query.keys()
    assert query["campaign"] == ["mokaair_seoul_booking_ko_hotspot"]


@pytest.mark.parametrize("labels", [
    {"destination_id": "private-user-id"}, {"locale": "user@example.com"},
    {"placement": "some-trip-id"},
])
def test_attribution_only_accepts_public_registry_labels(labels):
    with pytest.raises(ValueError):
        build_stay22_url(
            "booking", TARGETS["booking"], active_config(), **{"destination_id": "tokyo", **labels}
        )


@pytest.mark.parametrize("has_offer,stay22_on,tracking,direct,expected", [
    (True, True, True, True, "existing"), (True, False, True, False, "existing"),
    (False, True, True, False, "stay22"), (False, False, True, True, "direct"),
    (False, True, False, True, "direct"), (False, True, False, False, None),
    (False, False, True, False, None),
])
def test_existing_priority_privacy_and_explicit_direct_fallback(
    has_offer, stay22_on, tracking, direct, expected
):
    config = CatalogConfig(
        stay22=Stay22Config(enabled=stay22_on, enabled_providers=["booking"]),
        direct_hotel_links_enabled=direct,
    )
    option = HotelBookingOption(provider="booking", url=TARGETS["booking"])
    assert booking_channel(
        option, config, has_offer=has_offer, tracking_allowed=tracking,
    ) == expected


def test_platform_and_official_independence_and_bad_query_downgrade():
    config = CatalogConfig(stay22=active_config(), direct_hotel_links_enabled=True)
    for provider, target in (("official", "https://hotel.example.com/stay"),
                             ("booking", TARGETS["booking"] + "?checkin=2027-01-01")):
        option = HotelBookingOption(provider=provider, url=target)
        assert not stay22_eligible(option, config)
        assert booking_channel(option, config, has_offer=False) == "direct"
    with pytest.raises(ValueError):
        build_stay22_url(
            "booking", TARGETS["booking"], Stay22Config(), destination_id="tokyo"
        )
