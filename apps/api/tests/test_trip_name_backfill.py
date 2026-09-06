"""Existing stops get catalog labels only while their text still matches the catalog."""

from __future__ import annotations

from datetime import date
from uuid import uuid4

from app.models import FoodMerchant, TravelFood, TravelHotspot, TripPlanItem
from app.restaurants.user_router import SAVED_RESTAURANT_LABELS
from app.trips.itinerary import CROSS_CITY_TITLE_SUFFIX, MERCHANT_PENDING_LABELS
from app.trips.name_backfill import rebuild_item_names
from app.trips.schedule import MEAL_PLACEHOLDER_LABELS

SENSOJI = {"zh-TW": "淺草寺", "en": "Sensō-ji", "ja": "浅草寺", "original": "浅草寺"}
ICHIRAN = {
    "zh-TW": "一蘭 渋谷店",
    "en": "Ichiran Shibuya",
    "ja": "一蘭 渋谷店",
    "original": "一蘭 渋谷店",
}
RAMEN = {"zh-TW": "拉麵", "en": "Ramen", "ja": "ラーメン", "original": "ラーメン"}


def _item(title: str, location: str | None = None, **overrides: object) -> TripPlanItem:
    values: dict[str, object] = {
        "trip_plan_id": uuid4(),
        "item_type": "activity",
        "day_date": date(2026, 11, 11),
        "position": 0,
        "title": title,
        "location_name": location,
        "names_json": {},
        "data": {},
    }
    values.update(overrides)
    return TripPlanItem(**values)


def _hotspot() -> tuple[TravelHotspot, dict[str, str]]:
    return TravelHotspot(name="淺草寺", country_code="JP"), SENSOJI


def _merchant() -> tuple[FoodMerchant, dict[str, str]]:
    return FoodMerchant(
        name="Ichiran Shibuya", local_name="一蘭 渋谷店", country_code="JP"
    ), ICHIRAN


def _dish() -> tuple[TravelFood, dict[str, str]]:
    return TravelFood(local_name="ラーメン", romanized_name="Ramen", country_code="JP"), RAMEN


def test_hotspot_stops_keep_the_catalog_labels_while_their_text_matches() -> None:
    assert rebuild_item_names(_item("淺草寺", "淺草寺"), hotspot=_hotspot()) == {
        "title": SENSOJI,
        "location_name": SENSOJI,
    }
    # A renamed stop keeps its own words; only the untouched location follows the locale.
    assert rebuild_item_names(_item("淺草寺（早上去）", "淺草寺"), hotspot=_hotspot()) == {
        "location_name": SENSOJI
    }
    # Google resolution already replaced the location, so only the title is rebuilt.
    assert rebuild_item_names(_item("淺草寺", "2-3-1 Asakusa"), hotspot=_hotspot()) == {
        "title": SENSOJI
    }
    cross_city = rebuild_item_names(
        _item(f"淺草寺{CROSS_CITY_TITLE_SUFFIX['zh-TW']}", "淺草寺"), hotspot=_hotspot()
    )
    assert cross_city["title"]["en"] == "Sensō-ji cross-city deep-travel day"


def test_meals_match_the_dish_and_merchant_forms_the_planners_wrote() -> None:
    joined = rebuild_item_names(
        _item("ラーメン · Ichiran Shibuya", "Ichiran Shibuya"), merchant=_merchant(), dish=_dish()
    )
    assert joined["title"]["ja"] == "ラーメン · 一蘭 渋谷店"
    assert joined["title"]["en"] == "Ramen · Ichiran Shibuya"
    assert joined["location_name"] == ICHIRAN

    merchant_only = rebuild_item_names(
        _item("Ichiran Shibuya", "1-22-7 Jinnan, Shibuya"), merchant=_merchant()
    )
    assert merchant_only == {"title": ICHIRAN}  # an address is single-language text

    catalog_dish = rebuild_item_names(
        _item("拉麵", MERCHANT_PENDING_LABELS["zh-TW"], item_type="food"), dish=_dish()
    )
    assert catalog_dish == {"title": RAMEN, "location_name": MERCHANT_PENDING_LABELS}

    assert rebuild_item_names(_item("我最愛的拉麵店", "Ichiran Shibuya"), merchant=_merchant()) == {
        "location_name": ICHIRAN
    }


def test_system_meal_cards_get_their_placeholder_labels() -> None:
    lunch = _item(MEAL_PLACEHOLDER_LABELS["lunch"]["zh-TW"], item_type="meal", system_role="lunch")
    assert rebuild_item_names(lunch) == {"title": MEAL_PLACEHOLDER_LABELS["lunch"]}
    saved = _item(
        SAVED_RESTAURANT_LABELS["ja"],
        SAVED_RESTAURANT_LABELS["ja"],
        item_type="meal",
        system_role="dinner",
    )
    assert rebuild_item_names(saved) == {
        "title": SAVED_RESTAURANT_LABELS,
        "location_name": SAVED_RESTAURANT_LABELS,
    }
    chosen = _item("銀座晚餐", "銀座", item_type="meal", system_role="dinner")
    assert rebuild_item_names(chosen) == {}


def test_free_text_rows_stay_untouched() -> None:
    assert rebuild_item_names(_item("自己加的咖啡店", "澀谷")) == {}
    assert rebuild_item_names(_item("淺草寺"), hotspot=None, merchant=None, dish=None) == {}
