"""Japan-market direct links must not expand affiliate or hotel identity trust."""

import pytest
from pydantic import ValidationError

from app.models import TravelServiceBrand
from app.travel_services.channels import validate_offer_target
from app.travel_services.rakuten import rakuten_hotel_identity
from app.travel_services.registry import (
    BRANDS,
    affiliate_click_target,
    brand_target,
    direct_hotel_target,
)
from app.travel_services.schemas import Facts, HotelLink, HotelOptionInput, ProductInput
from app.travel_services.stay22 import validate_stay22_target

JAPAN_URL = "https://travel.rakuten.co.jp/HOTEL/187836/187836.html"
GLOBAL_URL = (
    "https://travel.rakuten.com/usa/en-us/hotel_info_item/cnt_taiwan/"
    "sub_taipei/cty_wanhua_district/dst_wanshou_village/34123457167650/"
)
EVIDENCE_URL = "https://solariataipei.mydirectstay.com/tw/index.html"


def test_japan_exact_property_is_a_direct_link_with_its_original_id():
    option = HotelOptionInput(
        provider="rakuten", url=JAPAN_URL, property_id="187836", evidence_url=EVIDENCE_URL
    )
    assert option.url == JAPAN_URL
    assert option.property_id == "187836"
    assert direct_hotel_target("rakuten", JAPAN_URL) == JAPAN_URL
    assert rakuten_hotel_identity(JAPAN_URL) == ("japan", "187836")


@pytest.mark.parametrize("property_id", ["198182", "34123457167650", "japan:187836", "0187836"])
def test_japan_manually_entered_id_must_match_its_property_url(property_id):
    with pytest.raises(ValidationError, match="Rakuten Japan property ID must match the hotel URL"):
        HotelOptionInput(
            provider="rakuten", url=JAPAN_URL, property_id=property_id, evidence_url=EVIDENCE_URL
        )


def test_optional_id_is_not_invented_or_filled_from_another_market():
    option = HotelOptionInput(provider="rakuten", url=JAPAN_URL, evidence_url=EVIDENCE_URL)
    assert option.property_id is None


@pytest.mark.parametrize("destination,country", [("taipei", "TW"), ("seoul", "KR")])
def test_japan_platform_market_does_not_change_an_overseas_hotel_country(destination, country):
    # Market and hotel country are independent. These are structural fixtures;
    # accepting a URL does not perform the separate hotel's identity review.
    hotel = ProductInput(
        source_key=f"overseas-rakuten-{destination}",
        title="Overseas hotel",
        kind="hotel",
        destination_id=destination,
        source_url=EVIDENCE_URL,
        facts=Facts(
            country_codes=[country],
            hotel_links=[HotelLink(provider="rakuten", url=JAPAN_URL, evidence_url=EVIDENCE_URL)],
        ),
    )
    assert hotel.destination_id == destination
    assert hotel.facts.country_codes == [country]
    assert hotel.facts.hotel_links[0].url == JAPAN_URL


@pytest.mark.parametrize(
    "url",
    [
        "https://travel.rakuten.co.jp/",
        "https://travel.rakuten.co.jp/HOTEL/",
        "https://travel.rakuten.co.jp/HOTEL/187836/",
        "https://travel.rakuten.co.jp/HOTEL/187836/rtmap.html",
        "https://travel.rakuten.co.jp/HOTEL/187836/CUSTOM/intro.html",
        "https://travel.rakuten.co.jp/search/",
        "https://travel.rakuten.co.jp/hotel_list/",
        "https://travel.rakuten.co.jp/HOTEL/187836/187837.html",
        "https://travel.rakuten.co.jp/HOTEL/0/0.html",
        "https://travel.rakuten.co.jp/HOTEL/0187836/0187836.html",
        "https://travel.rakuten.co.jp/HOTEL/-1/-1.html",
        "https://travel.rakuten.co.jp/HOTEL/abc/abc.html",
        "https://travel.rakuten.co.jp/HOTEL/１８７８３６/１８７８３６.html",
        "https://travel.rakuten.co.jp/HOTEL/187836/187836.html/extra",
        "https://travel.rakuten.co.jp/HOTEL/187836/../187836/187836.html",
        "https://travel.rakuten.co.jp/%48OTEL/187836/187836.html",
        "https://travel.rakuten.co.jp/HOTEL/187836%2F187836.html",
        "https://travel.rakuten.co.jp/HOTEL/187836/187836.html;next=evil",
        JAPAN_URL + "?redirect=https%3A%2F%2Fevil.example.com",
        JAPAN_URL + "?f_teikei=unverified-affiliate",
        JAPAN_URL + "?f_no=198182",
        JAPAN_URL + "?returnurl=https%3A%2F%2Fevil.example.com",
        "https://travel.rakuten.co.jp.evil.example.com/HOTEL/187836/187836.html",
        "https://evil.travel.rakuten.co.jp/HOTEL/187836/187836.html",
        "https://hotel.travel.rakuten.co.jp/HOTEL/187836/187836.html",
        "https://travel.rakuten.co.jp@evil.example.com/HOTEL/187836/187836.html",
        "http://travel.rakuten.co.jp/HOTEL/187836/187836.html",
    ],
)
def test_japan_rejects_non_property_pages_ambiguous_ids_queries_and_other_hosts(url):
    with pytest.raises(ValidationError):
        HotelLink(provider="rakuten", url=url, evidence_url=EVIDENCE_URL)


@pytest.mark.parametrize("provider", ["official", "booking", "agoda", "trip_com"])
def test_japan_ota_cannot_be_mislabeled_as_official_or_another_provider(provider):
    with pytest.raises(ValidationError):
        HotelLink(provider=provider, url=JAPAN_URL, evidence_url=JAPAN_URL)


def test_japan_platform_subdomains_are_not_the_hotels_official_website():
    subdomain = JAPAN_URL.replace("travel.rakuten.co.jp", "hotel.travel.rakuten.co.jp")
    with pytest.raises(ValidationError, match="not the hotel's official website"):
        HotelLink(provider="official", url=subdomain, evidence_url=subdomain)


def test_japan_direct_support_does_not_enable_affiliate_channels():
    assert BRANDS["rakuten"].hosts == ("travel.rakuten.com",)
    brand = TravelServiceBrand(code="rakuten", channel="travelpayouts")
    for static in (None, "https://tp.st/reviewed-fixture"):
        with pytest.raises(ValueError, match="selected brand"):
            validate_offer_target(brand, JAPAN_URL, static)
    with pytest.raises(ValueError, match="selected brand"):
        brand_target("rakuten", JAPAN_URL)
    with pytest.raises(ValueError, match="selected brand"):
        affiliate_click_target("rakuten", JAPAN_URL)
    with pytest.raises(ValueError, match="not enabled"):
        validate_stay22_target("rakuten", JAPAN_URL)


def test_existing_global_link_and_affiliate_validation_are_unchanged():
    link = HotelLink(provider="rakuten", url=GLOBAL_URL, evidence_url=EVIDENCE_URL)
    assert link.url == GLOBAL_URL
    assert direct_hotel_target("rakuten", GLOBAL_URL) == GLOBAL_URL
    assert brand_target("rakuten", GLOBAL_URL) == GLOBAL_URL
    assert affiliate_click_target("rakuten", GLOBAL_URL) == GLOBAL_URL
    assert rakuten_hotel_identity(GLOBAL_URL) == ("global", "34123457167650")


def test_market_is_part_of_identity_even_if_numeric_ids_happen_to_equal():
    # Deliberate fixture collision, not a discovered Global hotel.
    global_collision = GLOBAL_URL.replace("34123457167650", "187836")
    assert rakuten_hotel_identity(global_collision) == ("global", "187836")
    assert rakuten_hotel_identity(global_collision) != rakuten_hotel_identity(JAPAN_URL)
