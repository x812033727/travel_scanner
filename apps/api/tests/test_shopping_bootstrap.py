"""The dedicated-store batch: what makes a row in it admissible.

Every other seed file in this directory was written from a list and given coordinates
afterwards. This one was written the other way round: a candidate only became a row once
a public source that names the shop also carried its position. The first pass took the
nearest coordinate to a remembered guess and produced 南大沢駅 for an outlet mall,
三越劇場 for a department store, a tram stop for 狸小路 and a temple for 光華商場 — which
is why the rules below are about provenance rather than about shape.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import app.hotspots as hotspots_package
from app.hotspots.areas import resolve_area
from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.theme_catalog import SHOP_THEME_SLUGS
from app.hotspots.themes import THEME_BOOTSTRAP

ROWS = json.loads(
    (Path(hotspots_package.__file__).parent / "shopping_bootstrap.json").read_text(
        encoding="utf-8"
    )
)
BY_SLUG = {seed.slug: seed for seed in HOTSPOT_SEEDS}
ASSIGNMENTS = {assignment.hotspot_slug: assignment for assignment in THEME_BOOTSTRAP}

# 大阪アメリカ村's Q4745722 is already carried by the Okinawa 美國村 seed, whose
# coordinates point at Osaka. A Wikidata id may appear once, so this row keeps the
# coordinate and cites the item without claiming the id; fixing the Okinawa row frees it.
QID_HELD_ELSEWHERE = {"kix-amerikamura"}


def test_file_shape() -> None:
    assert len(ROWS) == 30
    assert Counter(row["city_code"] for row in ROWS) == {
        "NRT": 7,
        "KIX": 6,
        "ICN": 4,
        "TPE": 2,
        "HKG": 4,
        "BKK": 3,
        "FUK": 1,
        "CTS": 1,
        "NGO": 1,
        "PUS": 1,
    }
    for row in ROWS:
        assert row["category"] == "shopping"
        assert row["provenance"] == "editorial"
        assert row["is_deep_travel"] is False
        assert row["slug"].startswith(f"{row['city_code'].casefold()}-")
        assert row["name"] and row["local_name"] and row["aliases"]
        assert 60 <= row["recommended_duration_minutes"] <= 120


def test_every_coordinate_names_its_own_source() -> None:
    """A row is only as good as the page its position came from.

    Both accepted sources name the shop themselves: a Wikidata item's P625, or an
    OpenStreetMap object whose name and address are the shop's. Nothing here was placed
    from memory, so there is no `curated_coordinate` in this file on purpose.
    """

    for row in ROWS:
        assert row["coordinate_source"] in {"wikidata_p625", "openstreetmap"}, row["slug"]
        assert row["source_urls"], row["slug"]
        assert all(url.startswith("https://") for url in row["source_urls"]), row["slug"]
        if row["coordinate_source"] == "wikidata_p625":
            qid = row["wikidata_item_id"]
            assert (qid is None) == (row["slug"] in QID_HELD_ELSEWHERE), row["slug"]
            assert any("wikidata.org/wiki/Q" in url for url in row["source_urls"]), row["slug"]
        else:
            assert row["wikidata_item_id"] is None, row["slug"]
            assert any("openstreetmap.org/" in url for url in row["source_urls"]), row["slug"]


# The locale a shop's own signage is written in, per destination.
LOCAL_LOCALE = {
    "NRT": "ja", "KIX": "ja", "FUK": "ja", "CTS": "ja", "NGO": "ja",
    "ICN": "ko", "PUS": "ko",
}


def test_names_are_written_for_five_audiences() -> None:
    for row in ROWS:
        localized = BY_SLUG[row["slug"]].localized_names
        assert set(localized) >= {"zh-TW", "zh-CN", "en", "ja", "ko"}, row["slug"]
        assert all(localized.values()), row["slug"]


def test_local_name_is_the_name_on_the_shop_front() -> None:
    """`local_name` is what a traveller standing outside will actually see.

    Somebody looking for 唐吉訶德 in Shibuya is looking for a sign that reads
    ドン・キホーテ, so the Japanese and Korean rows carry their own script here rather
    than a translation of the Traditional Chinese label.
    """

    for row in ROWS:
        locale = LOCAL_LOCALE.get(row["city_code"])
        if locale is None:  # TPE, HKG write Chinese; BKK carries Thai with no zh source.
            continue
        assert row["local_name"] == row["names"][locale], row["slug"]


def test_every_store_carries_at_least_one_shop_type() -> None:
    """A shop with no shop type is invisible to the very filter it was seeded for."""

    for row in ROWS:
        assignment = ASSIGNMENTS.get(row["slug"])
        assert assignment is not None, f"{row['slug']} has no theme_bootstrap entry"
        shop_types = set(assignment.themes) & SHOP_THEME_SLUGS
        assert shop_types, row["slug"]
        assert not assignment.months, f"{row['slug']} is a shop, not a season"


def test_the_batch_gives_every_shop_type_somewhere_to_go() -> None:
    counts = Counter(
        theme
        for row in ROWS
        for theme in ASSIGNMENTS[row["slug"]].themes
        if theme in SHOP_THEME_SLUGS
    )
    assert set(counts) == SHOP_THEME_SLUGS
    # Outlet malls had no seed at all before this batch, which left the chip dead.
    assert counts["outlet"] >= 3


def test_rows_reach_the_catalog_and_an_area() -> None:
    from tests.test_hotspot_areas import AREA_UNASSIGNED_SEEDS

    for row in ROWS:
        seed = BY_SLUG[row["slug"]]
        assert seed.category == "shopping"
        assert seed.provenance == "editorial"
        assert row["aliases"][0] in seed.aliases
        area = resolve_area(seed.city_code, seed.latitude, seed.longitude)
        assert (area is not None) or row["slug"] in AREA_UNASSIGNED_SEEDS, row["slug"]


def test_no_row_re_seeds_a_place_the_catalog_already_had() -> None:
    new_slugs = {row["slug"] for row in ROWS}
    others = [seed for seed in HOTSPOT_SEEDS if seed.slug not in new_slugs]
    taken_qids = {seed.wikidata_item_id for seed in others if seed.wikidata_item_id}
    for row in ROWS:
        if row["wikidata_item_id"]:
            assert row["wikidata_item_id"] not in taken_qids, row["slug"]
    # 明洞, 心齋橋 and 秋葉原 are already districts in the catalog; the batch adds shops
    # inside them, never the districts a second time.
    existing_names = {seed.name for seed in others}
    assert not {row["name"] for row in ROWS} & existing_names
