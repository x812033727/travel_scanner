from collections import Counter
from urllib.parse import parse_qs, unquote, urlparse

from app.foods.catalog import FOOD_SEEDS
from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.maps import build_map_links
from app.i18n import LOCALES


def test_food_catalog_has_exactly_ten_complete_items_per_country() -> None:
    assert len(FOOD_SEEDS) == 70
    assert Counter(item.country_code for item in FOOD_SEEDS) == {
        "HK": 10,
        "JP": 10,
        "KR": 10,
        "SG": 10,
        "TH": 10,
        "TW": 10,
        "VN": 10,
    }
    assert len({item.slug for item in FOOD_SEEDS}) == 70
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
    assert len(by_destination) == 31
    assert len(food_areas) == 37
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


def test_google_map_link_prefers_place_id_then_coordinates() -> None:
    links = build_map_links(
        name="築地場外市場",
        local_name="築地場外市場",
        city_name="東京",
        country_code="JP",
        latitude=35.6654,
        longitude=139.7707,
        google_place_id="ChIJ example/id",
    )
    assert [item["provider"] for item in links] == ["google"]
    query = parse_qs(urlparse(str(links[0]["url"])).query)
    assert query["query"] == ["35.665400,139.770700"]
    assert query["query_place_id"] == ["ChIJ example/id"]
    assert links[0]["primary"] is True


def test_korean_map_links_put_encoded_naver_search_first() -> None:
    links = build_map_links(
        name="廣藏市場",
        local_name="광장시장",
        city_name="首爾",
        country_code="KR",
        latitude=37.5701,
        longitude=126.9996,
    )
    assert [item["provider"] for item in links] == ["naver", "google"]
    assert links[0]["primary"] is True
    assert links[1]["primary"] is False
    assert unquote(urlparse(str(links[0]["url"])).path).endswith("/광장시장")


def test_google_map_link_falls_back_to_name_and_city() -> None:
    link = build_map_links(
        name="清萊夜市",
        local_name="เชียงรายไนท์บาซาร์",
        city_name="清萊",
        country_code="TH",
        latitude=None,
        longitude=None,
    )[0]
    query = parse_qs(urlparse(str(link["url"])).query)
    assert query["query"] == ["清萊夜市 清萊"]
