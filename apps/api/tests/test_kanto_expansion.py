import json
from collections import Counter
from pathlib import Path

import app.hotspots as hotspots_package
from app.hotspots.areas import resolve_area
from app.hotspots.catalog import CATEGORY_CORRECTIONS, FOOD_AREA_NAMES, HOTSPOT_SEEDS

ROWS = json.loads(
    (Path(hotspots_package.__file__).parent / "kanto_expansion_bootstrap.json").read_text(
        encoding="utf-8"
    )
)
# The Gemini list repeated fourteen places the catalog already carried; the generator
# skips them by Wikidata item so the same attraction never appears twice.
ALREADY_CURATED_QIDS = {
    "Q615183",  # 淺草寺
    "Q57965",  # 東京晴空塔
    "Q746216",  # 上野公園
    "Q21083961",  # 澀谷十字路口
    "Q287165",  # 明治神宮
    "Q776863",  # 新宿御苑
    "Q500681",  # 東京皇居
    "Q183536",  # 東京鐵塔
    "Q859471",  # 築地場外市場
    "Q418096",  # 秋葉原
    "Q4388146",  # 清澄庭園
    "Q3275957",  # 神樂坂
    "Q1329959",  # 高尾山
    "Q843997",  # 東京迪士尼樂園
}
FOOD_ROWS = {
    "nrt-ameyoko",
    "nrt-omoide-yokocho",
    "nrt-toyosu-market",
    "nrt-toyosu-senkyaku-banrai",
    "nrt-harmonica-yokocho",
    "nrt-togoshi-ginza",
    "yok-yokohama-chinatown",
    "kmk-komachi-dori",
}


def test_expansion_file_shape() -> None:
    assert len(ROWS) == 113
    assert Counter(row["city_code"] for row in ROWS) == {"NRT": 83, "YOK": 15, "KMK": 15}
    assert Counter(row["provenance"] for row in ROWS) == {"gemini": 86, "editorial": 27}
    for row in ROWS:
        assert row["slug"].startswith(f"{row['city_code'].casefold()}-")
        assert not row["slug"].startswith("wikidata-")
        assert row["local_name"] and row["aliases"] and row["source_urls"]
        assert row["recommended_duration_minutes"] >= 20
        assert row["coordinate_source"] in {"wikidata_p625", "curated_coordinate"}
        if row["coordinate_source"] == "curated_coordinate":
            # Reviewed coordinates always cite the public page they were read from.
            assert row["source_urls"][-1].startswith("https://")
        if row["city_code"] == "NRT":
            assert row["is_deep_travel"] is False
    assert {row["slug"] for row in ROWS if row["category"] == "food"} == FOOD_ROWS


def test_expansion_skips_places_the_catalog_already_has() -> None:
    qids = [row["wikidata_item_id"] for row in ROWS if row["wikidata_item_id"]]
    assert len(qids) == len(set(qids)) == 111
    assert not set(qids) & ALREADY_CURATED_QIDS
    names = {row["name"] for row in ROWS} | {row["local_name"] for row in ROWS}
    assert not names & FOOD_AREA_NAMES
    assert not names & set(CATEGORY_CORRECTIONS)


def test_expansion_rows_are_seeded_with_provenance_and_an_area() -> None:
    by_slug = {seed.slug: seed for seed in HOTSPOT_SEEDS}
    for row in ROWS:
        seed = by_slug[row["slug"]]
        assert seed.provenance == row["provenance"]
        assert row["aliases"][0] in seed.aliases
        assert resolve_area(seed.city_code, seed.latitude, seed.longitude) is not None, row["slug"]


def test_yokohama_and_kamakura_are_tokyo_extensions() -> None:
    for city_code, destination_id in (("YOK", "yokohama"), ("KMK", "kamakura")):
        rows = [seed for seed in HOTSPOT_SEEDS if seed.city_code == city_code]
        assert len(rows) == 15
        assert {seed.destination_id for seed in rows} == {destination_id}
        deep = [seed for seed in rows if seed.is_deep_travel]
        assert Counter(seed.depth_kind for seed in deep) == {"urban_local": 3, "day_trip": 2}
        assert any(seed.category == "food" for seed in rows)
    tokyo_gemini = [seed for seed in HOTSPOT_SEEDS if seed.provenance == "gemini"]
    assert Counter(seed.city_code for seed in tokyo_gemini) == {"NRT": 83, "YOK": 2, "KMK": 1}
