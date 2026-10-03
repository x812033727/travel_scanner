from collections import Counter

import pytest

from app.hotspots.areas import (
    HOTSPOT_AREAS,
    area_by_code,
    area_name,
    area_payload,
    resolve_area,
    resolve_area_code,
)
from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.cities import CITY_BY_CODE
from app.i18n import Locale

# Seeds whose stored coordinates do not match the place they name, so no honest area
# contains them. They are tracked here instead of widening a circle to swallow them;
# fixing the coordinates is a separate data change that should shrink this set.
AREA_MISPLACED_SEEDS = {
    "deep-icn-q13902883",  # ICN 世宗村: coordinates sit in Mapo, 4 km from Seochon
    "deep-pus-q135683915",  # PUS 흰여울문化마을: coordinates near Seomyeon, not Yeongdo
    "gye-q491088",  # GYE 雞林: coordinates sit 4 km north of the Gyerim forest
}

# Seeds outside every circle because they genuinely are: temples, parks and villages
# reached as a day trip. Their coordinates are right, so this set is not a defect list
# and widening a city circle to swallow them would misplace them instead.
AREA_OUT_OF_TOWN_SEEDS = {
    "cei-wat-huai-pla-kang",  # CEI: 5 km north of the Chiang Rai city circles
    "cei-wat-phra-that-doi-tung",  # CEI: mountain ridge 60 km from Chiang Rai
    "deep-kbv-q13024195",  # KBV: national park 45 km north of Krabi town
    "hui-cau-ngoi-thanh-toan",  # HUI: rural covered bridge 8 km east of Huế
    "kix-rinku-premium-outlets",  # KIX: Izumisano, 25 km past the outermost Osaka circle
    "nrt-mitsui-outlet-tama-minami-osawa",  # NRT: Hachioji, 8 km west of the 多摩 circle
}

AREA_UNASSIGNED_SEEDS = AREA_MISPLACED_SEEDS | AREA_OUT_OF_TOWN_SEEDS


def test_every_city_has_a_reviewed_area_catalog() -> None:
    assert set(HOTSPOT_AREAS) == set(CITY_BY_CODE)
    for city_code, areas in HOTSPOT_AREAS.items():
        assert len(areas) >= 7, city_code
        codes = [area.code for area in areas]
        assert len(set(codes)) == len(codes), city_code
        for area in areas:
            assert area.radius_km > 0
            assert area.names["zh-TW"] and area.names["en"]
            assert area_by_code(city_code, area.code) is area


def test_resolver_prefers_the_tightest_containing_circle() -> None:
    # 秋葉原 sits inside both its own 1.3 km circle and the larger 上野 circle; the
    # smaller relative distance wins, so it never shows up as "上野／谷中".
    assert resolve_area_code("NRT", 35.6983, 139.7731) == "akihabara"
    assert resolve_area_code("nrt", 35.7122, 139.7711) == "ueno"
    # Outside every circle: no area, rather than the nearest one stretched to fit.
    assert resolve_area("NRT", 35.3, 139.0) is None
    assert resolve_area("NRT", None, 139.7) is None
    assert resolve_area(None, 35.6983, 139.7731) is None
    assert resolve_area("XXX", 35.6983, 139.7731) is None


def test_curated_seeds_all_resolve_to_an_area() -> None:
    unassigned = {
        seed.slug
        for seed in HOTSPOT_SEEDS
        if resolve_area(seed.city_code, seed.latitude, seed.longitude) is None
    }
    assert unassigned == AREA_UNASSIGNED_SEEDS
    per_city = Counter(
        seed.city_code
        for seed in HOTSPOT_SEEDS
        if resolve_area(seed.city_code, seed.latitude, seed.longitude) is not None
    )
    assert set(per_city) == set(CITY_BY_CODE)


def test_seed_spot_checks() -> None:
    by_slug = {seed.slug: seed for seed in HOTSPOT_SEEDS}
    expected = {
        "sensoji": "asakusa",
        "wikidata-q418096": "akihabara",  # 秋葉原
        "wikidata-q287165": "shibuya",  # 明治神宮
        "wikidata-q776863": "shinjuku",  # 新宿御苑
        "deep-nrt-q1329959": "takao",  # 高尾山
        "deep-nrt-q3080561": "kawagoe",  # 喜多院
        "wikidata-q843997": "maihama",  # 東京迪士尼樂園
        "dotonbori": "namba",
        "fushimi-inari": "fushimi",
        "wikidata-q11650434": "kawaramachi",  # 錦市場
        "gyeongbokgung": "jongno",
        "wikidata-q484407": "myeongdong",  # 明洞
        "icn-yongsan-electronics-market": "yongsan-electronics",
        "wat-arun": "thonburi",
        "grand-palace-bangkok": "rattanakosin",
        "wikidata-q83101": "xinyi",  # 台北 101
        "tpe-syntrend-creative-park": "guanghua",
        "wikidata-q17541": "peak",  # 太平山
        "wikidata-q7698673": "mong-kok",  # 廟街夜市
        "khh-q701113": "qianjin",  # 六合夜市
        "hij-q231140": "peace-park",  # 原爆ドーム
        "nrt-otome-road": "ikebukuro",
        "nrt-teamlab-borderless": "roppongi",  # Azabudai Hills, not the old Odaiba venue
        "nrt-toyosu-market": "toyosu",
        "nrt-ghibli-museum": "kichijoji",
        "nrt-sanrio-puroland": "tama",
        "yok-minato-mirai-21": "minato-mirai",
        "yok-yokohama-red-brick-warehouse": "shinko",
        "yok-yokohama-chinatown": "chinatown",
        "kmk-kotoku-in": "hase",
        "kmk-enoshima": "enoshima",
    }
    for slug, code in expected.items():
        seed = by_slug[slug]
        assert resolve_area_code(seed.city_code, seed.latitude, seed.longitude) == code, slug


def test_okinawa_american_village_is_in_chatan_not_osaka() -> None:
    """The OKA 美國村 seed used to carry Q4745722, Osaka's アメリカ村, and its coordinate.

    It now names Mihama American Village in Chatan. The slug keeps the old id on purpose:
    it is the public identity of the row already in production, and keeping it lets the
    seeder correct that row in place instead of adding a second 美國村 beside it.
    """

    by_slug = {seed.slug: seed for seed in HOTSPOT_SEEDS}
    okinawa = by_slug["wikidata-q4745722"]
    assert okinawa.city_code == "OKA"
    assert okinawa.wikidata_item_id is not None
    assert okinawa.wikidata_item_id != "Q4745722"
    # Okinawa Island, roughly; Osaka's アメリカ村 is at 34.67 N, 135.50 E.
    assert 26.0 <= okinawa.latitude <= 26.9, okinawa.latitude
    assert 127.6 <= okinawa.longitude <= 128.4, okinawa.longitude
    assert resolve_area_code("OKA", okinawa.latitude, okinawa.longitude) == "chatan"
    # The freed id belongs to the Osaka shop row, which still lands in an Osaka area.
    osaka = by_slug["kix-amerikamura"]
    assert osaka.wikidata_item_id == "Q4745722"
    assert resolve_area("KIX", osaka.latitude, osaka.longitude) is not None


def test_electronics_circles_preserve_neighbouring_areas() -> None:
    by_slug = {seed.slug: seed for seed in HOTSPOT_SEEDS}
    expected = {
        "wikidata-q494407": "yongsan",  # National Museum of Korea
        "wikidata-q540794": "taipei-station",  # Chiang Kai-shek Memorial Hall
        "tpe-taipei-city-mall": "taipei-station",
    }
    for slug, code in expected.items():
        seed = by_slug[slug]
        assert resolve_area_code(seed.city_code, seed.latitude, seed.longitude) == code, slug
    # No current seed represents Yongnidan-gil itself. Its established center must
    # retain its own label rather than becoming part of the electronics quarter.
    assert resolve_area_code("ICN", 37.532, 126.972) == "yongnidan"


def test_guanghua_covers_the_huashan_quarter_named_in_its_label() -> None:
    # Huashan 1914, Wikidata Q14594864 (OSM relation 5177809).
    # This point has no catalog seed; checking only Syntrend
    # would allow a circle too small to cover the other half of the area name.
    assert resolve_area_code("TPE", 25.044609, 121.529183) == "guanghua"


@pytest.mark.parametrize(
    ("city_code", "code", "names"),
    [
        (
            "ICN",
            "yongsan-electronics",
            {
                "zh-TW": "龍山電子商街",
                "en": "Yongsan Electronics Market",
                "ja": "龍山電子商街",
                "ko": "용산전자상가",
                "zh-CN": "龙山电子商街",
            },
        ),
        (
            "TPE",
            "guanghua",
            {
                "zh-TW": "光華商圈／華山",
                "en": "Guanghua & Huashan",
                "ja": "Guanghua & Huashan",
                "ko": "Guanghua & Huashan",
                "zh-CN": "光华商圈／华山",
            },
        ),
    ],
)
def test_electronics_area_payloads_in_all_locales(
    city_code: str, code: str, names: dict[Locale, str]
) -> None:
    area = area_by_code(city_code, code)
    assert area is not None
    for locale, expected in names.items():
        assert area_name(area, locale) == expected
        assert area_payload(area, locale) == {"code": code, "name": expected}


def test_area_names_fall_back_per_locale() -> None:
    area = area_by_code("NRT", "shibuya")
    assert area is not None
    assert area_name(area, "zh-TW") == "澀谷／原宿"
    # zh-CN used to fall straight back to Traditional; the table now answers first.
    assert area_name(area, "zh-CN") == "涩谷／原宿"
    assert area_name(area, "ja") == "渋谷・原宿"
    assert area_name(area, "en") == "Shibuya & Harajuku"
    assert area_name(area, "ko") == "Shibuya & Harajuku"
    assert area_payload(area, "en") == {"code": "shibuya", "name": "Shibuya & Harajuku"}
    assert area_payload(None, "en") is None
    seoul = area_by_code("ICN", "hongdae")
    assert seoul is not None
    assert area_name(seoul, "ko") == "홍대·합정"


def test_simplified_readers_get_simplified_area_names_where_the_scripts_differ() -> None:
    """Every area served Traditional characters to zh-CN before the table existed."""
    from app.hotspots.areas import SIMPLIFIED_AREA_NAMES, HotspotArea, area_name

    area = HotspotArea("shibuya", {"zh-TW": "澀谷／原宿", "en": "Shibuya"}, 0.0, 0.0, 1.0)
    if "澀谷／原宿" in SIMPLIFIED_AREA_NAMES:
        assert area_name(area, "zh-CN") == SIMPLIFIED_AREA_NAMES["澀谷／原宿"]
    # A name written the same way in both scripts has no entry and falls back.
    same = HotspotArea("takao", {"zh-TW": "高尾山", "en": "Mount Takao"}, 0.0, 0.0, 1.0)
    assert area_name(same, "zh-CN") == "高尾山"


def test_the_simplified_table_only_holds_names_the_catalog_actually_uses() -> None:
    """A stale key is a silent no-op, so the table must not drift from the catalog."""
    from app.hotspots.areas import HOTSPOT_AREAS, SIMPLIFIED_AREA_NAMES

    catalog = {area.names["zh-TW"] for areas in HOTSPOT_AREAS.values() for area in areas}
    assert set(SIMPLIFIED_AREA_NAMES) <= catalog
    # An entry equal to its key would be a conversion that changed nothing.
    assert all(key != value for key, value in SIMPLIFIED_AREA_NAMES.items())
