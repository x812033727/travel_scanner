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
AREA_UNASSIGNED_SEEDS = {
    "wikidata-q4745722",  # OKA 美國村: Q4745722 is Osaka's Amerikamura, not Chatan
    "deep-icn-q13902883",  # ICN 世宗村: coordinates sit in Mapo, 4 km from Seochon
    "deep-pus-q135683915",  # PUS 흰여울문化마을: coordinates near Seomyeon, not Yeongdo
    "deep-kbv-q38684",  # KBV 孟加拉灣: Q38684 is the Bay of Bengal, 1,300 km away
    "cei-kok-river",  # CEI 郭河: coordinates point at the river's source in Myanmar
    "gye-q491088",  # GYE 雞林: coordinates sit 4 km north of the Gyerim forest
}


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
    }
    for slug, code in expected.items():
        seed = by_slug[slug]
        assert resolve_area_code(seed.city_code, seed.latitude, seed.longitude) == code, slug


def test_area_names_fall_back_per_locale() -> None:
    area = area_by_code("NRT", "shibuya")
    assert area is not None
    assert area_name(area, "zh-TW") == "澀谷／原宿"
    assert area_name(area, "zh-CN") == "澀谷／原宿"
    assert area_name(area, "ja") == "渋谷・原宿"
    assert area_name(area, "en") == "Shibuya & Harajuku"
    assert area_name(area, "ko") == "Shibuya & Harajuku"
    assert area_payload(area, "en") == {"code": "shibuya", "name": "Shibuya & Harajuku"}
    assert area_payload(None, "en") is None
    seoul = area_by_code("ICN", "hongdae")
    assert seoul is not None
    assert area_name(seoul, "ko") == "홍대·합정"
