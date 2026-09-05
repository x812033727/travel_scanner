from collections import Counter
from urllib.parse import parse_qs, urlparse

from app.foods.catalog import FOOD_SEEDS, OFFICIAL_FOOD_SOURCES
from app.foods.merchant_catalog import (
    MERCHANT_DIRECT_SOURCE_SEEDS,
    MERCHANT_SEEDS,
    OFFICIAL_DESTINATION_FOOD_SOURCES,
)
from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.maps import build_map_links
from app.i18n import LOCALES


def test_food_catalog_has_at_least_ten_complete_items_per_country() -> None:
    # Floors, matching validate_catalog. Asserting equality here would put back the ceiling
    # that made a city with no dish of its own impossible to serve.
    assert len(FOOD_SEEDS) >= 70
    counts = Counter(item.country_code for item in FOOD_SEEDS)
    assert set(counts) == {"HK", "JP", "KR", "SG", "TH", "TW", "VN"}
    assert all(count >= 10 for count in counts.values())
    assert len({item.slug for item in FOOD_SEEDS}) == len(FOOD_SEEDS)
    for item in FOOD_SEEDS:
        assert set(item.localized_names) == set(LOCALES)
        assert set(item.localized_summaries) == set(LOCALES)
        assert all(item.localized_names.values())
        assert all(item.localized_summaries.values())
        assert len(item.source_urls) == 2
        assert "wikipedia.org" in item.source_urls[1]
        assert item.destination_ids
        assert set(item.meal_types) <= {
            "breakfast",
            "lunch",
            "dinner",
            "snack",
            "dessert",
            "drink",
        }


def test_every_destination_has_an_approved_coordinate_complete_food_area() -> None:
    food_areas = [item for item in HOTSPOT_SEEDS if item.category == "food"]
    by_destination = {item.destination_id for item in food_areas}
    assert len(by_destination) == 33
    assert len(food_areas) == 45
    for item in food_areas:
        assert item.latitude is not None
        assert item.longitude is not None
        assert item.source_urls or item.wikipedia_url

    wrong_categories = {
        "台中大都會歌劇院",
        "衛武營國家藝術文化中心",
        "瑞鳳殿",
        "Sendai Literature Museum",
        "廣島和平紀念資料館",
        "臺南孔子廟",
    }
    assert not wrong_categories & {item.name for item in food_areas}


def test_google_map_link_uses_verified_place_id_and_never_coordinates() -> None:
    links = build_map_links(
        name="築地場外市場",
        local_name="築地場外市場",
        city_name="東京",
        country_code="JP",
        latitude=35.6654,
        longitude=139.7707,
        google_place_id="ChIJ example/id",
        map_match_status="verified",
    )
    assert [item["provider"] for item in links] == ["google"]
    query = parse_qs(urlparse(str(links[0]["url"])).query)
    assert query["query"] == ["築地場外市場 東京"]
    assert query["query_place_id"] == ["ChIJ example/id"]
    assert "35.665400" not in str(links[0]["url"])
    assert links[0]["primary"] is True


def test_korean_map_links_return_only_a_verified_exact_naver_place() -> None:
    links = build_map_links(
        name="廣藏市場",
        local_name="광장시장",
        city_name="首爾",
        country_code="KR",
        latitude=37.5701,
        longitude=126.9996,
        naver_map_url="https://map.naver.com/p/entry/place/13543735",
        map_match_status="verified",
    )
    assert [item["provider"] for item in links] == ["naver"]
    assert links[0]["primary"] is True
    assert links[0]["url"] == "https://map.naver.com/p/entry/place/13543735"


def test_unverified_or_search_only_map_identity_is_not_published() -> None:
    assert (
        build_map_links(
            name="清萊夜市",
            local_name="เชียงรายไนท์บาซาร์",
            city_name="清萊",
            country_code="TH",
            latitude=None,
            longitude=None,
        )
        == []
    )
    assert (
        build_map_links(
            name="廣藏市場",
            local_name="광장시장",
            city_name="首爾",
            country_code="KR",
            latitude=37.5701,
            longitude=126.9996,
            naver_map_url="https://map.naver.com/p/search/test",
            map_match_status="verified",
        )
        == []
    )


def test_merchant_candidates_cover_all_relations_but_are_not_fake_map_matches() -> None:
    assert len(MERCHANT_SEEDS) >= 155
    actual_pairs = {
        (merchant.destination_id, food_slug)
        for merchant in MERCHANT_SEEDS
        for food_slug in merchant.food_slugs
    }
    assert len(actual_pairs) >= 173
    assert all(merchant.source_url.startswith("https://") for merchant in MERCHANT_SEEDS)
    assert all(
        merchant.source_title == "Official destination food guide (regional context only)"
        for merchant in MERCHANT_SEEDS
    )
    assert len(OFFICIAL_DESTINATION_FOOD_SOURCES) >= 30
    # Every merchant's destination must have an official guide; the reverse is allowed so a
    # city's guide can be added in the same change that gives the city its first restaurant.
    assert {merchant.destination_id for merchant in MERCHANT_SEEDS} <= set(
        OFFICIAL_DESTINATION_FOOD_SOURCES
    )
    assert not any(
        stale in url
        for url in OFFICIAL_DESTINATION_FOOD_SOURCES.values()
        for stale in (
            "gofukuoka.jp/gourmet.html",
            "dive-hiroshima.com/en/explore/food/",
            "visitkanazawa.jp/en/gourmet",
            "vietnam-food-20-must-try-dishes",
        )
    )


def test_the_two_repaired_official_sources_stay_repaired() -> None:
    """Pins the addresses fixed in 0039; both predecessors had rotted in different ways.

    The JP page answered 404 outright, and it is the first source of all ten Japanese
    dishes. The TW address still answered 200 but had become a New Taipei City page, which
    is the worse failure of the two because nothing about it looks broken.
    """

    assert OFFICIAL_FOOD_SOURCES["JP"] == "https://www.japan.travel/en/things-to-do/eat-and-drink/"
    assert OFFICIAL_FOOD_SOURCES["TW"] == "https://eng.taiwan.net.tw/m1.aspx?sNo=0002026"
    taiwan = {"taipei", "taichung", "kaohsiung", "tainan"}
    for destination in taiwan:
        assert OFFICIAL_DESTINATION_FOOD_SOURCES[destination] == OFFICIAL_FOOD_SOURCES["TW"]


def test_non_japan_direct_sources_are_verified_and_country_balanced() -> None:
    merchant_country = {merchant.slug: merchant.country_code for merchant in MERCHANT_SEEDS}
    assert len(MERCHANT_DIRECT_SOURCE_SEEDS) == 47
    assert len({seed.merchant_slug for seed in MERCHANT_DIRECT_SOURCE_SEEDS}) == 47
    assert Counter(
        merchant_country[seed.merchant_slug] for seed in MERCHANT_DIRECT_SOURCE_SEEDS
    ) == {
        "HK": 7,
        "KR": 6,
        "SG": 7,
        "TH": 6,
        "TW": 14,
        "VN": 7,
    }
    assert sum(seed.official_website_url is not None for seed in MERCHANT_DIRECT_SOURCE_SEEDS) == 21
    for seed in MERCHANT_DIRECT_SOURCE_SEEDS:
        assert merchant_country[seed.merchant_slug] != "JP"
        assert seed.source_url.startswith("https://")
        assert seed.claims
        assert not any(
            excluded in seed.source_url
            for excluded in ("google.com/maps", "maps.app.goo.gl", "tripadvisor.", "wikipedia.")
        )
        if seed.official_website_url:
            assert seed.source_type == "merchant_official"
            assert seed.source_scope == "merchant_website"
            assert "official_website" in seed.claims
            assert seed.official_website_url == seed.source_url
