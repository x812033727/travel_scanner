"""Planned attractions and food keep five site locales plus the original script."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import uuid4

import httpx
import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from app.ai.itinerary import (
    AIDraftDay,
    AIDraftItem,
    AIItineraryDraft,
    AIPlannerCandidate,
    _request_payload,
    draft_to_itinerary,
)
from app.foods.service import food_names, merchant_names
from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.service import hotspot_names
from app.i18n import LOCALES, active_locale, bind_request_locale, reset_request_locale
from app.localized_names import item_names
from app.middleware import RequestContextMiddleware
from app.models import FoodMerchant, TravelFood, TravelHotspot, TripPlanItem
from app.trips.itinerary import ItineraryFood, ItineraryHotspot, ItineraryItem, build_itinerary
from app.trips.replan import sync_ai_meal_slots
from app.trips.router import (
    ItineraryItemRequest,
    apply_item_request,
    item_record,
    serialize_item,
)
from app.trips.schedule import MEAL_PLACEHOLDER_LABELS
from tests.test_ai_itinerary import request_for
from tests.test_mock_providers import sample_query

SENSOJI = {
    "zh-TW": "淺草寺",
    "zh-CN": "淺草寺",
    "en": "Sensō-ji",
    "ja": "浅草寺",
    "ko": "센소지",
    "original": "浅草寺",
    "original_locale": "ja",
}


def _seed(**match: object):  # type: ignore[no-untyped-def]
    return next(
        seed
        for seed in HOTSPOT_SEEDS
        if all(getattr(seed, key) == value for key, value in match.items())
    )


def test_every_hotspot_seed_has_a_label_in_every_site_locale() -> None:
    for seed in HOTSPOT_SEEDS:
        names = seed.localized_names
        assert set(LOCALES) <= set(names), seed.slug
        assert names["zh-TW"] == seed.name


def test_hotspot_seed_names_follow_the_country_script() -> None:
    sensoji = _seed(slug="sensoji").localized_names
    assert sensoji["en"] == "Sensō-ji"
    assert sensoji["zh-TW"] == "淺草寺"
    assert sensoji["ja"] == sensoji["original"] == "浅草寺"
    assert sensoji["ko"] == "센소지"  # the Korean label now comes from Wikidata

    # Nothing is invented where no label exists: this Bangkok seed has no Korean, so
    # Korean readers get the English name rather than a transliteration made up here.
    sea_life = _seed(name="曼谷暹羅海洋世界").localized_names
    assert sea_life["ko"] == sea_life["en"] == "Sea Life Bangkok Ocean World"

    gyeongbokgung = _seed(slug="gyeongbokgung").localized_names
    assert gyeongbokgung["ko"] == gyeongbokgung["original"] == "경복궁"
    assert gyeongbokgung["ja"] == "Gyeongbokgung"

    lumphini = _seed(name="倫披尼公園").localized_names
    assert lumphini["en"] == "Lumphini Park"
    # Thai is not a site locale, so it never becomes one of the five labels, but the
    # seed does carry the original-script name and it is exposed under "original".
    assert lumphini["original"] == "สวนลุมพินี"
    assert lumphini["original_locale"] == "th"
    assert set(LOCALES) & {"th"} == set()

    nakamise = _seed(name="仲見世商店街").localized_names
    assert nakamise["en"] == "Nakamise-dori"
    assert nakamise["ja"] == nakamise["original"] == "仲見世通り"
    assert nakamise["original_locale"] == "ja"

    hongdae = _seed(name="弘大").localized_names
    assert hongdae["en"] == "Hongdae"  # the Wikipedia disambiguator is not a name

    taichung = _seed(name="國立自然科學博物館").localized_names
    assert taichung["original"] == taichung["zh-TW"] == "國立自然科學博物館"
    assert taichung["original_locale"] == "zh-TW"


def test_fetched_wikidata_labels_fill_what_the_seed_cannot_derive() -> None:
    base = _seed(slug="sensoji")
    fetched = replace(
        base,
        names={"ko": "센소지", "zh-CN": "浅草寺", "en": "Senso-ji Temple", "zh-TW": "淺草観音"},
    )
    names = fetched.localized_names
    assert names["ko"] == "센소지"
    assert names["zh-CN"] == "浅草寺"
    assert names["en"] == "Sensō-ji"  # the reviewed alias still wins over the fetched label
    assert names["zh-TW"] == "淺草寺"  # the curated name is never replaced
    assert names["original"] == "浅草寺"

    thai = replace(
        _seed(name="倫披尼公園"),
        local_name=None,
        names={"ko": "룸피니 공원", "ja": "ルンピニー公園"},
    )
    assert thai.localized_names["ja"] == "ルンピニー公園"
    assert (
        "original" not in thai.localized_names
    )  # without a local_name there is no original-script text to expose
    korean = replace(_seed(slug="gyeongbokgung"), local_name=None, names={"ko": "경복궁"})
    assert korean.original_name == "경복궁"  # a fetched label can stand in for the original


def test_hotspot_names_merge_stored_localizations_with_the_original() -> None:
    hotspot = TravelHotspot(
        name="淺草寺", country_code="JP", metadata_json={"local_name": "浅草寺"}
    )
    assert hotspot_names(hotspot, {"en": "Sensō-ji", "ko": "센소지"}) == SENSOJI
    taipei = TravelHotspot(name="龍山寺", country_code="TW", metadata_json={})
    assert hotspot_names(taipei, {})["original"] == "龍山寺"


def test_merchant_and_dish_names_come_from_their_columns_and_overrides() -> None:
    merchant = FoodMerchant(
        name="Ichiran Shibuya",
        local_name="一蘭 渋谷店",
        country_code="JP",
        names_json={"zh-TW": "一蘭 澀谷店", "fr": "ignored", "ja": ""},
    )
    assert merchant_names(merchant) == {
        "zh-TW": "一蘭 澀谷店",
        "zh-CN": "一蘭 澀谷店",
        "en": "Ichiran Shibuya",
        "ja": "一蘭 渋谷店",
        "ko": "Ichiran Shibuya",
        "original": "一蘭 渋谷店",
        "original_locale": "ja",
    }
    taipei = FoodMerchant(name="Lan Jia Gua Bao", local_name="藍家割包", country_code="TW")
    assert merchant_names(taipei)["zh-TW"] == "藍家割包"
    assert merchant_names(taipei)["en"] == "Lan Jia Gua Bao"

    # Japanese shop names read as kanji for Chinese travellers; Korean ones do not.
    kanda = FoodMerchant(name="Kanda Matsuya", local_name="神田まつや", country_code="JP")
    assert merchant_names(kanda)["zh-TW"] == merchant_names(kanda)["zh-CN"] == "神田まつや"
    assert merchant_names(kanda)["ko"] == "Kanda Matsuya"
    seoul = FoodMerchant(name="Korea House", local_name="한국의집", country_code="KR")
    assert merchant_names(seoul)["zh-TW"] == "Korea House"
    assert merchant_names(seoul)["ko"] == "한국의집"

    ramen = TravelFood(local_name="ラーメン", romanized_name="Ramen", country_code="JP")
    names = food_names(ramen, {"zh-TW": "拉麵", "en": "Ramen"})
    assert names["ja"] == names["original"] == "ラーメン"
    assert names["ko"] == "Ramen"


def _catalog_stop(**overrides: object) -> TripPlanItem:
    values: dict[str, object] = {
        "id": uuid4(),
        "trip_plan_id": uuid4(),
        "item_type": "activity",
        "day_date": date(2026, 11, 11),
        "position": 1,
        "title": "淺草寺",
        "location_name": "淺草寺",
        "names_json": item_names(title=SENSOJI, location_name=SENSOJI),
        "data": {"hotspot_id": "hotspot-1"},
        # Column defaults only apply at flush time; the request model needs booleans.
        "locked": False,
        "is_estimated": False,
        "fixed_time": False,
        "is_skipped": False,
    }
    values.update(overrides)
    return TripPlanItem(**values)


def test_serialize_item_labels_stops_in_the_request_locale() -> None:
    stop = _catalog_stop()
    assert serialize_item(stop, locale="ja")["title"] == "浅草寺"
    assert serialize_item(stop, locale="en")["location_name"] == "Sensō-ji"
    assert serialize_item(stop, localized=False)["title"] == "淺草寺"
    token = bind_request_locale("ko")
    try:
        assert active_locale() == "ko"
        payload = serialize_item(stop)
    finally:
        reset_request_locale(token)
    assert payload["title"] == "센소지"
    assert payload["names"]["title"]["original"] == "浅草寺"
    assert active_locale() == "zh-TW"

    free_text = _catalog_stop(title="自己加的咖啡店", names_json={})
    assert serialize_item(free_text, locale="en")["title"] == "自己加的咖啡店"
    assert serialize_item(free_text, locale="en")["names"] == {}


def _request(record: TripPlanItem, **overrides: object) -> ItineraryItemRequest:
    payload = {**serialize_item(record, localized=False), **overrides}
    return ItineraryItemRequest.model_validate(payload)


def test_echoing_a_shown_label_keeps_the_catalog_names_and_canonical_title() -> None:
    stop = _catalog_stop()
    apply_item_request(stop, _request(stop, title="浅草寺", location_name="浅草寺"), locale="ja")
    assert stop.names_json == item_names(title=SENSOJI, location_name=SENSOJI)
    assert stop.title == stop.location_name == "淺草寺"
    apply_item_request(stop, _request(stop), locale="en")
    assert stop.names_json["title"] == SENSOJI


def test_renaming_a_stop_drops_the_labels_for_that_field_only() -> None:
    stop = _catalog_stop()
    apply_item_request(stop, _request(stop, title="淺草寺（早上去）"), locale="ja")
    assert stop.title == "淺草寺（早上去）"
    assert "title" not in stop.names_json
    assert stop.names_json["location_name"] == SENSOJI
    assert serialize_item(stop, locale="en")["title"] == "淺草寺（早上去）"
    assert serialize_item(stop, locale="en")["location_name"] == "Sensō-ji"


def test_item_record_only_copies_planner_names() -> None:
    planned = ItineraryItem(
        id=uuid4(),
        item_type="hotspot",
        day_date=date(2026, 11, 11),
        position=0,
        title="淺草寺",
        names=item_names(title=SENSOJI),
    )
    assert item_record(uuid4(), planned).names_json == {"title": SENSOJI}
    client_row = ItineraryItemRequest(
        item_type="custom", day_date=date(2026, 11, 11), position=0, title="咖啡店"
    )
    assert item_record(uuid4(), client_row).names_json == {}


def _localized_candidates() -> list[AIPlannerCandidate]:
    ramen = {"zh-TW": "拉麵", "en": "Ramen", "ja": "ラーメン", "original": "ラーメン"}
    ichiran = {
        "zh-TW": "一蘭 澀谷店",
        "en": "Ichiran Shibuya",
        "ja": "一蘭 渋谷店",
        "original": "一蘭 渋谷店",
        "original_locale": "ja",
    }
    return [
        AIPlannerCandidate(
            key="hotspot:1",
            kind="hotspot",
            name="淺草寺",
            names=SENSOJI,
            category="culture",
            latitude=35.71,
            longitude=139.79,
            duration_minutes=90,
            map_links=[{"provider": "google", "url": "https://maps.example/1"}],
            hotspot_id=uuid4(),
            rank=1,
        ),
        AIPlannerCandidate(
            key="merchant:1",
            kind="merchant",
            name="Ichiran Shibuya",
            local_name="ラーメン",
            names=ichiran,
            dish_names=ramen,
            category="food",
            latitude=35.66,
            longitude=139.70,
            duration_minutes=75,
            map_links=[{"provider": "google", "url": "https://maps.example/2"}],
            merchant_id=uuid4(),
            meal_types=["lunch", "dinner"],
            rank=1,
        ),
    ]


def test_ai_draft_items_carry_catalog_names_and_the_prompt_omits_them() -> None:
    request = request_for().model_copy(update={"candidates": _localized_candidates()})
    prompt_candidates = _request_payload(request)["candidates"]
    assert all("names" not in item and "dish_names" not in item for item in prompt_candidates)
    assert prompt_candidates[0]["name"] == "淺草寺"

    draft = AIItineraryDraft(
        summary="測試",
        days=[
            AIDraftDay(
                date=date(2026, 11, 11),
                items=[
                    AIDraftItem(candidate_key="hotspot:1", start_time="10:00", reason="經典"),
                    AIDraftItem(
                        candidate_key="merchant:1",
                        start_time="12:00",
                        reason="午餐",
                        slot_type="lunch",
                    ),
                ],
            )
        ],
    )
    hotspot, meal = draft_to_itinerary(request, draft, "openai", "gpt")[0].items
    assert hotspot.title == "淺草寺"
    assert hotspot.names["title"]["ko"] == "센소지"
    assert hotspot.names["location_name"]["original"] == "浅草寺"
    assert meal.title == "ラーメン · Ichiran Shibuya"
    assert meal.names["title"]["ja"] == "ラーメン · 一蘭 渋谷店"
    assert meal.names["title"]["zh-TW"] == "拉麵 · 一蘭 澀谷店"
    assert meal.names["location_name"]["en"] == "Ichiran Shibuya"
    assert serialize_item(item_record(uuid4(), meal), locale="en")["title"] == (
        "Ramen · Ichiran Shibuya"
    )


def test_ai_meal_sync_copies_labels_and_localizes_the_empty_state() -> None:
    day = date(2026, 11, 11)
    lunch = TripPlanItem(
        trip_plan_id=uuid4(),
        item_type="meal",
        day_date=day,
        position=1,
        title="舊店",
        system_role="lunch",
        data={"meal_selection_source": "ai"},
        names_json={"title": {"zh-TW": "舊店", "en": "Old place"}},
    )
    dinner = TripPlanItem(
        trip_plan_id=lunch.trip_plan_id,
        item_type="meal",
        day_date=day,
        position=3,
        title="舊晚餐",
        system_role="dinner",
        data={"meal_selection_source": "ai"},
        names_json={"title": {"zh-TW": "舊晚餐"}},
    )
    generated = ItineraryItem(
        id=uuid4(),
        item_type="meal",
        day_date=day,
        position=1,
        title="ラーメン · Ichiran Shibuya",
        location_name="Ichiran Shibuya",
        system_role="lunch",
        names={"title": {"zh-TW": "拉麵 · 一蘭 澀谷店", "en": "Ramen · Ichiran Shibuya"}},
        data={"generated_by": "ai_planner", "meal_selection_source": "ai"},
    )
    sync_ai_meal_slots([lunch, dinner], [generated])
    assert lunch.names_json == generated.names
    assert serialize_item(lunch, locale="zh-TW")["title"] == "拉麵 · 一蘭 澀谷店"
    assert dinner.title == MEAL_PLACEHOLDER_LABELS["dinner"]["zh-TW"]
    assert serialize_item(dinner, locale="en")["title"] == "Dinner not planned yet"
    assert serialize_item(dinner, locale="ko")["title"] == "저녁 식사 미정"


def test_deterministic_builder_labels_catalog_stops() -> None:
    query = sample_query()
    query = query.model_copy(
        update={
            "preferences": query.preferences.model_copy(
                update={"interests": ["deep_travel", "food"]}
            )
        }
    )
    hotspot = ItineraryHotspot(
        hotspot_id=uuid4(),
        name="淺草寺",
        names=SENSOJI,
        category="culture",
        latitude=35.71,
        longitude=139.79,
        depth_kind="urban_local",
        depth_score=85,
        access_minutes=20,
        recommended_duration_minutes=90,
    )
    food = ItineraryFood(
        food_id=uuid4(),
        name="拉麵",
        local_name="ラーメン",
        names={"zh-TW": "拉麵", "en": "Ramen", "original": "ラーメン"},
        merchant_names={"zh-TW": "一蘭 澀谷店", "en": "Ichiran Shibuya"},
        food_kind="noodle_soup",
        meal_types=["lunch", "dinner"],
        merchant_id=uuid4(),
        merchant_name="Ichiran Shibuya",
        latitude=35.66,
        longitude=139.70,
        map_links=[{"provider": "google", "url": "https://maps.example/2"}],
        merchant_status="verified",
    )
    itinerary = build_itinerary(query, None, None, None, None, [hotspot], [food])
    items = [item for day in itinerary for item in day.items]
    placed = next(item for item in items if item.item_type == "hotspot")
    assert placed.names["title"]["en"] == "Sensō-ji"
    meal = next(item for item in items if item.item_type == "food")
    assert meal.names["title"]["en"] == "Ramen"
    assert meal.names["location_name"]["en"] == "Ichiran Shibuya"


@pytest.mark.asyncio
async def test_middleware_binds_the_request_locale_for_the_whole_request() -> None:
    async def echo(_request: Request) -> PlainTextResponse:
        return PlainTextResponse(active_locale())

    app = Starlette(routes=[Route("/locale", echo)])
    app.add_middleware(RequestContextMiddleware)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        assert (await client.get("/locale", headers={"X-Travel-Locale": "ja"})).text == "ja"
        assert (await client.get("/locale", headers={"X-Travel-Locale": "fr"})).text == "zh-TW"
        assert (await client.get("/locale")).text == "zh-TW"
    assert active_locale() == "zh-TW"


def test_trip_plan_item_names_default_to_an_empty_map() -> None:
    row = TripPlanItem(
        trip_plan_id=uuid4(),
        item_type="custom",
        day_date=date(2026, 11, 11),
        position=0,
        title="自訂",
        latitude=Decimal("35.0"),
        longitude=Decimal("139.0"),
        start_time=datetime(2026, 11, 11, 9, tzinfo=UTC),
    )
    assert serialize_item(row)["names"] == {}
