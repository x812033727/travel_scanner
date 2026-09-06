from collections import Counter

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

# Seeds whose stored coordinates do not match the place they name, so no honest area
# contains them. They are tracked here instead of widening a circle to swallow them;
# fixing the coordinates is a separate data change that should shrink this set.
AREA_MISPLACED_SEEDS = {
    "wikidata-q4745722",  # OKA 美國村: Q4745722 is Osaka's Amerikamura, not Chatan
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
        "wat-arun": "thonburi",
        "grand-palace-bangkok": "rattanakosin",
        "wikidata-q83101": "xinyi",  # 台北 101
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
