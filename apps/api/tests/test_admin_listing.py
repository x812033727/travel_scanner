from dataclasses import dataclass

from app.admin.listing import (
    COUNTRY_ORDER,
    COUNTRY_RANK,
    DESTINATION_RANK,
    FOOD_KIND_ORDER,
    HOTSPOT_CATEGORY_ORDER,
    country_name_for,
    country_rank,
    destination_rank,
    ranked,
)
from app.foods.catalog import COUNTRY_NAMES
from app.models import TravelFood, TravelHotspot


def test_country_order_matches_the_food_catalog() -> None:
    assert COUNTRY_ORDER == ("JP", "KR", "TH", "TW", "SG", "HK", "VN")
    assert set(COUNTRY_ORDER) == set(COUNTRY_NAMES)
    assert COUNTRY_RANK["JP"] == 0
    assert COUNTRY_RANK["VN"] == 6
    assert HOTSPOT_CATEGORY_ORDER[0] == "culture"
    assert FOOD_KIND_ORDER[0] == "main"


def test_country_name_localizes_and_falls_back() -> None:
    assert country_name_for("JP", "ko") == "일본"
    assert country_name_for("HK", "en") == "Hong Kong"
    assert country_name_for("XX", "zh-TW") == "XX"
    assert country_name_for("XX", "zh-TW", "未知") == "未知"


def test_country_rank_orders_known_countries_first() -> None:
    sql = str(country_rank(TravelFood.country_code).compile(compile_kwargs={"literal_binds": True}))
    assert "WHEN 'JP' THEN 0" in sql
    assert "WHEN 'VN' THEN 6" in sql
    assert "ELSE 7" in sql


def test_ranked_keeps_fixed_order_and_appends_unknown_codes() -> None:
    @dataclass
    class Row:
        code: str

    rows = [Row("zz"), Row("dessert"), Row("main"), Row("aa")]
    assert [row.code for row in ranked(rows, "code", FOOD_KIND_ORDER)] == [
        "main",
        "dessert",
        "aa",
        "zz",
    ]


def test_destination_rank_puts_primary_cities_first() -> None:
    assert DESTINATION_RANK["tokyo"] == 0
    assert DESTINATION_RANK["taichung"] == 1
    assert DESTINATION_RANK["tainan"] == 2
    sql = str(
        destination_rank(TravelHotspot.destination_id).compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert "WHEN 'tokyo' THEN 0" in sql
    assert "ELSE 3" in sql
