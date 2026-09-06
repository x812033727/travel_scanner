from collections import Counter, defaultdict

from app.hotspots.catalog import HOTSPOT_SEEDS, LEGACY_SLUGS
from app.hotspots.cities import HOTSPOT_CITIES, TARGET_PUBLIC_HOTSPOTS


def test_deep_bootstrap_contract() -> None:
    deep = [item for item in HOTSPOT_SEEDS if item.is_deep_travel]
    assert len(HOTSPOT_SEEDS) == 563
    assert len(deep) == 165
    assert TARGET_PUBLIC_HOTSPOTS == 649
    assert len({item.slug for item in HOTSPOT_SEEDS}) == 563
    qids = [item.wikidata_item_id for item in HOTSPOT_SEEDS if item.wikidata_item_id]
    assert len(qids) == 560
    assert len(set(qids)) == len(qids)

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
        # Two is the floor now: Chiang Rai's five deep places are three hills and two
        # temples, and there is no third kind of thing to name without inventing one.
        assert len(categories) >= 2
        # No cap on how many share a category. Kanazawa's five deep places really are
        # three temples and a shrine; the old cap of two is why one of them was filed
        # as nature, and a wrong category reaches the planner as a wrong suggestion.


def test_legacy_slugs_all_resolve() -> None:
    # A renamed wikipedia_title used to silently drop its curated slug, re-seeding the
    # attraction as wikidata-<id> and orphaning the old row with no Wikidata id.
    by_slug = {item.slug: item for item in HOTSPOT_SEEDS}
    assert set(LEGACY_SLUGS.values()) <= set(by_slug)
    assert by_slug["n-seoul-tower"].wikidata_item_id == "Q69134"
    assert by_slug["phuket-old-town"].wikidata_item_id == "Q17063772"
    assert by_slug["patong-beach"].wikidata_item_id == "Q630024"


def test_pageview_articles_use_a_wiki_that_has_them() -> None:
    # These five had no en.wikipedia article, so every pageviews lookup returned 404
    # and they never scored. Each now points at the wiki Wikidata actually links.
    by_id = {item.wikidata_item_id: item for item in HOTSPOT_SEEDS}
    expected = {
        "Q56963453": ("ja.wikipedia.org", "白い恋人パーク", "Shiroi Koibito Park"),
        "Q11558610": ("ja.wikipedia.org", "国営海の中道海浜公園", "Uminonakamichi Seaside Park"),
        "Q13026486": ("th.wikipedia.org", "แหลมพรหมเทพ", "Promthep Cape"),
        "Q283373": ("en.wikipedia.org", "Nagoya TV Tower", "Chubu Electric Power MIRAI TOWER"),
        "Q4616917": ("ja.wikipedia.org", "国際通り", "Kokusai-dōri"),
    }
    for item_id, (project, title, legacy_name) in expected.items():
        seed = by_id[item_id]
        assert (seed.wikipedia_project, seed.wikipedia_title) == (project, title)
        # The romanised name stays searchable now that it is no longer the title.
        assert legacy_name in seed.aliases
