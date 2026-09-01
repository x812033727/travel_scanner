from collections import Counter, defaultdict

from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.cities import HOTSPOT_CITIES, TARGET_PUBLIC_HOTSPOTS


def test_deep_bootstrap_contract() -> None:
    deep = [item for item in HOTSPOT_SEEDS if item.is_deep_travel]
    assert len(HOTSPOT_SEEDS) == 265
    assert len(deep) == 95
    assert TARGET_PUBLIC_HOTSPOTS == 313
    assert len({item.slug for item in HOTSPOT_SEEDS}) == 265
    assert len({item.wikidata_item_id for item in HOTSPOT_SEEDS}) == 265

    by_city = defaultdict(list)
    for item in deep:
        by_city[item.city_code].append(item)
        assert item.local_name
        assert item.depth_reason
        assert item.source_urls
        assert (item.depth_score or 0) >= 70
        assert 1 <= (item.access_minutes or 0) <= (45 if item.depth_kind == "urban_local" else 90)
        assert (item.recommended_duration_minutes or 0) >= 30

    assert set(by_city) == {city.code for city in HOTSPOT_CITIES}
    for rows in by_city.values():
        assert len(rows) == 5
        assert Counter(item.depth_kind for item in rows) == {"urban_local": 3, "day_trip": 2}
        categories = Counter(item.category for item in rows)
        assert len(categories) >= 3
        assert max(categories.values()) <= 2
