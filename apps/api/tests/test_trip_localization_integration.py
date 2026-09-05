"""Attractions and food added to a plan re-label themselves per request locale."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, select

from app.db import SessionFactory, engine
from app.infra import get_redis
from app.main import app
from app.models import (
    FoodLocalization,
    FoodMerchant,
    FoodMerchantFood,
    FoodMerchantSource,
    HotspotLocalization,
    TravelFood,
    TravelHotspot,
    TripPlan,
    TripPlanItem,
    User,
)
from app.trips.name_backfill import backfill_trip_item_names

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def isolate_async_clients_for_module() -> AsyncIterator[None]:
    # The preceding integration module can leave pooled clients bound to its
    # module-scoped event loop. Drop those pools without trying to close their
    # already-stopped loop, then clean up this module's clients normally.
    await engine.dispose(close=False)
    get_redis.cache_clear()
    yield
    await engine.dispose()
    await get_redis().aclose()
    get_redis.cache_clear()


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def member() -> dict[str, str]:
    """One registered member for the whole module: registration is rate limited per IP."""

    email = f"localized-{uuid4().hex}@example.com"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "integration-pass-123"},
        )
    assert registered.status_code == 201, registered.text
    return {"email": email, "authorization": f"Bearer {registered.json()['access_token']}"}


def _stop(trip: dict[str, Any], **match: object) -> dict[str, Any]:
    return next(
        item
        for item in trip["items"]
        if all(
            (item["data"].get(key) if key != "system_role" else item.get(key)) == value
            for key, value in match.items()
        )
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_planned_stops_follow_the_request_locale_until_renamed(
    member: dict[str, str],
) -> None:
    suffix = uuid4().hex
    now = datetime.now(UTC)
    async with SessionFactory() as session:
        hotspot = TravelHotspot(
            slug=f"localized-hotspot-{suffix}",
            name="淺草寺",
            city_code="NRT",
            destination_id="tokyo",
            city_name="東京",
            country_code="JP",
            country_name="日本",
            category="culture",
            search_text="sensoji",
            latitude=Decimal("35.714765"),
            longitude=Decimal("139.796655"),
            coordinate_source_type="wikidata",
            coordinate_source_url="https://www.wikidata.org/wiki/Q617422",
            coordinate_verified_at=now,
            google_place_id=f"localized-place-{suffix}",
            map_match_status="verified",
            review_status="approved",
            is_active=True,
            metadata_json={"local_name": "浅草寺", "recommended_duration_minutes": 90},
        )
        merchant = FoodMerchant(
            slug=f"localized-merchant-{suffix}",
            destination_id="tokyo",
            country_code="JP",
            name="Ichiran Shibuya",
            local_name="一蘭 渋谷店",
            names_json={"zh-TW": "一蘭 澀谷店"},
            latitude=Decimal("35.661777"),
            longitude=Decimal("139.700294"),
            coordinate_source_type="merchant_official",
            coordinate_source_url="https://example.test/ichiran/shibuya",
            coordinate_verified_at=now,
            google_place_id=f"localized-merchant-place-{suffix}",
            map_match_status="verified",
            review_status="approved",
            is_active=True,
            verified_at=now,
        )
        food = TravelFood(
            slug=f"localized-food-{suffix}",
            country_code="JP",
            local_name="ラーメン",
            romanized_name="Ramen",
            food_kind="noodle_soup",
            meal_types=["lunch", "dinner"],
            search_text="ramen",
            source_urls=["https://example.test/ramen"],
            review_status="approved",
            is_active=True,
        )
        session.add_all([hotspot, merchant, food])
        await session.flush()
        session.add_all(
            [
                HotspotLocalization(
                    hotspot_id=hotspot.id, locale="en", name="Sensō-ji", aliases=[], search_terms=[]
                ),
                HotspotLocalization(
                    hotspot_id=hotspot.id, locale="ko", name="센소지", aliases=[], search_terms=[]
                ),
                FoodLocalization(food_id=food.id, locale="zh-TW", name="拉麵", summary="湯麵"),
                FoodLocalization(food_id=food.id, locale="en", name="Ramen", summary="Noodles"),
                FoodMerchantFood(merchant_id=merchant.id, food_id=food.id, is_primary=True),
                FoodMerchantSource(
                    merchant_id=merchant.id,
                    source_type="merchant_official",
                    source_scope="merchant_listing",
                    source_title="Official shop page",
                    source_url="https://example.test/ichiran/shibuya",
                    claims_json=["name"],
                    is_current=True,
                ),
            ]
        )
        await session.commit()
        hotspot_id, merchant_id = hotspot.id, merchant.id

    def localized(headers: dict[str, str], locale: str) -> dict[str, str]:
        return {**headers, "X-Travel-Locale": locale}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        headers = {"Authorization": member["authorization"]}
        created = await client.post(
            "/api/v1/trips",
            headers=headers,
            json={
                "source": "blank",
                "planning_mode": "manual_blank",
                "name": "東京多語言行程",
                "destination_name": "日本東京",
                "start_date": "2026-11-10",
                "end_date": "2026-11-12",
            },
        )
        assert created.status_code == 201
        trip = created.json()

        added = await client.post(
            f"/api/v1/hotspots/{hotspot_id}/trip-selections",
            headers=localized(headers, "ja"),
            json={"trip_id": trip["id"], "version": trip["version"], "day_date": "2026-11-11"},
        )
        assert added.status_code == 200, added.text
        stop = _stop(added.json(), hotspot_id=str(hotspot_id))
        assert stop["title"] == stop["location_name"] == "浅草寺"
        assert stop["names"]["title"]["original"] == "浅草寺"
        assert stop["names"]["title"]["original_locale"] == "ja"

        expected = {"en": "Sensō-ji", "ko": "센소지", "zh-TW": "淺草寺", "zh-CN": "淺草寺"}
        for locale, title in expected.items():
            fetched = await client.get(
                f"/api/v1/trips/{trip['id']}", headers=localized(headers, locale)
            )
            assert fetched.status_code == 200
            assert _stop(fetched.json(), hotspot_id=str(hotspot_id))["title"] == title
        trip = fetched.json()

        lunch = await client.post(
            f"/api/v1/foods/merchants/{merchant_id}/trip-selections",
            headers=localized(headers, "ja"),
            json={
                "trip_id": trip["id"],
                "version": trip["version"],
                "day_date": "2026-11-11",
                "meal_role": "lunch",
            },
        )
        assert lunch.status_code == 200, lunch.text
        meal = _stop(lunch.json(), merchant_id=str(merchant_id))
        assert meal["title"] == "ラーメン · 一蘭 渋谷店"
        assert meal["location_name"] == "一蘭 渋谷店"
        meal_titles = {
            "en": "Ramen · Ichiran Shibuya",
            "zh-TW": "拉麵 · 一蘭 澀谷店",
            "zh-CN": "拉麵 · 一蘭 澀谷店",
        }
        for locale, title in meal_titles.items():
            fetched = await client.get(
                f"/api/v1/trips/{trip['id']}", headers=localized(headers, locale)
            )
            assert _stop(fetched.json(), merchant_id=str(merchant_id))["title"] == title
        trip = fetched.json()

        # Saving the plan from the Japanese UI echoes the Japanese label: the
        # catalog labels survive and the canonical text is untouched.
        japanese = (
            await client.get(f"/api/v1/trips/{trip['id']}", headers=localized(headers, "ja"))
        ).json()
        japanese_stop = _stop(japanese, hotspot_id=str(hotspot_id))
        saved = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=localized(headers, "ja"),
            json={"version": japanese["version"], "items": [japanese_stop]},
        )
        assert saved.status_code == 200, saved.text
        assert _stop(saved.json(), hotspot_id=str(hotspot_id))["title"] == "浅草寺"
        english = await client.get(f"/api/v1/trips/{trip['id']}", headers=localized(headers, "en"))
        assert _stop(english.json(), hotspot_id=str(hotspot_id))["title"] == "Sensō-ji"

        # A real rename wins in every language.
        renamed = await client.put(
            f"/api/v1/trips/{trip['id']}/itinerary",
            headers=localized(headers, "ja"),
            json={
                "version": saved.json()["version"],
                "items": [{**japanese_stop, "title": "浅草寺（朝いち）"}],
            },
        )
        assert renamed.status_code == 200, renamed.text
        for locale in ("en", "zh-TW"):
            fetched = await client.get(
                f"/api/v1/trips/{trip['id']}", headers=localized(headers, locale)
            )
            renamed_stop = _stop(fetched.json(), hotspot_id=str(hotspot_id))
            assert renamed_stop["title"] == "浅草寺（朝いち）"
            assert "title" not in renamed_stop["names"]
            assert renamed_stop["location_name"] == expected.get(locale, "浅草寺")

    async with SessionFactory() as session:
        await session.execute(delete(TripPlan).where(TripPlan.id == trip["id"]))
        await session.execute(delete(FoodMerchant).where(FoodMerchant.id == merchant_id))
        await session.execute(
            delete(TravelFood).where(TravelFood.slug == f"localized-food-{suffix}")
        )
        await session.execute(delete(TravelHotspot).where(TravelHotspot.id == hotspot_id))
        await session.commit()


@pytest.mark.asyncio(loop_scope="module")
async def test_backfill_labels_stops_saved_before_the_column_existed(
    member: dict[str, str],
) -> None:
    suffix = uuid4().hex
    day = date(2026, 11, 11)
    async with SessionFactory() as session:
        hotspot = TravelHotspot(
            slug=f"backfill-hotspot-{suffix}",
            name="淺草寺",
            city_code="NRT",
            destination_id="tokyo",
            city_name="東京",
            country_code="JP",
            country_name="日本",
            category="culture",
            search_text="sensoji",
            metadata_json={"local_name": "浅草寺"},
        )
        merchant = FoodMerchant(
            slug=f"backfill-merchant-{suffix}",
            destination_id="tokyo",
            country_code="JP",
            name="Ichiran Shibuya",
            local_name="一蘭 渋谷店",
        )
        food = TravelFood(
            slug=f"backfill-food-{suffix}",
            country_code="JP",
            local_name="ラーメン",
            romanized_name="Ramen",
            food_kind="noodle_soup",
            meal_types=["lunch", "dinner"],
            search_text="ramen",
        )
        session.add_all([hotspot, merchant, food])
        await session.flush()
        session.add_all(
            [
                HotspotLocalization(
                    hotspot_id=hotspot.id, locale="en", name="Sensō-ji", aliases=[], search_terms=[]
                ),
                FoodLocalization(food_id=food.id, locale="zh-TW", name="拉麵", summary="湯麵"),
            ]
        )
        await session.commit()
        hotspot_id, merchant_id, food_id = hotspot.id, merchant.id, food.id

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        headers = {"Authorization": member["authorization"]}

        async with SessionFactory() as session:
            user_id = await session.scalar(select(User.id).where(User.email == member["email"]))
            trip = TripPlan(
                user_id=user_id,
                name="升級前的行程",
                mode="manual",
                total_price=Decimal(0),
                currency="TWD",
                data={"source": "blank"},
                version=1,
                destination_name="日本東京",
                start_date=date(2026, 11, 10),
                end_date=date(2026, 11, 12),
                timezone="Asia/Tokyo",
            )
            session.add(trip)
            await session.flush()

            def legacy(**values: Any) -> TripPlanItem:
                base: dict[str, Any] = {
                    "trip_plan_id": trip.id,
                    "day_date": day,
                    "names_json": {},
                    "locked": False,
                    "is_estimated": False,
                    "fixed_time": False,
                    "is_skipped": False,
                }
                return TripPlanItem(**{**base, **values})

            session.add_all(
                [
                    legacy(
                        item_type="activity",
                        position=1,
                        title="淺草寺",
                        location_name="淺草寺",
                        data={"hotspot_id": str(hotspot_id), "selection_source": "hotspot_card"},
                    ),
                    legacy(
                        item_type="activity",
                        position=2,
                        title="淺草寺（早上去）",
                        location_name="淺草寺",
                        data={"hotspot_id": str(hotspot_id)},
                    ),
                    legacy(
                        item_type="meal",
                        position=3,
                        system_role="lunch",
                        locked=True,
                        fixed_time=True,
                        title="ラーメン · Ichiran Shibuya",
                        location_name="Ichiran Shibuya",
                        data={
                            "generated_by": "ai_planner",
                            "meal_selection_source": "ai",
                            "merchant_id": str(merchant_id),
                            "food_id": str(food_id),
                        },
                    ),
                    legacy(
                        item_type="meal",
                        position=4,
                        system_role="dinner",
                        locked=True,
                        fixed_time=True,
                        is_estimated=True,
                        title="晚餐尚未安排",
                        location_name=None,
                        data={"meal_selection_source": "unset"},
                    ),
                ]
            )
            await session.commit()
            trip_id = trip.id

        async with SessionFactory() as session:
            preview = await backfill_trip_item_names(session, dry_run=True)
        assert preview["filled"] >= 4
        async with SessionFactory() as session:
            untouched = await session.scalar(
                select(TripPlanItem.names_json).where(
                    TripPlanItem.trip_plan_id == trip_id, TripPlanItem.position == 1
                )
            )
            assert untouched == {}  # a dry run writes nothing
            counts = await backfill_trip_item_names(session)
        assert counts["filled"] >= 4

        fetched = await client.get(
            f"/api/v1/trips/{trip_id}", headers={**headers, "X-Travel-Locale": "ja"}
        )
        assert fetched.status_code == 200, fetched.text
        by_title = {item["title"]: item for item in fetched.json()["items"]}
        assert "浅草寺" in by_title  # the untouched stop follows the locale
        assert by_title["浅草寺"]["names"]["title"]["en"] == "Sensō-ji"
        renamed = by_title["淺草寺（早上去）"]  # the rename survives, its location follows
        assert renamed["location_name"] == "浅草寺"
        assert "title" not in renamed["names"]
        assert "ラーメン · 一蘭 渋谷店" in by_title
        assert by_title["ラーメン · 一蘭 渋谷店"]["location_name"] == "一蘭 渋谷店"
        assert "夕食は未定" in by_title

    async with SessionFactory() as session:
        await session.execute(delete(TripPlan).where(TripPlan.id == trip_id))
        await session.execute(delete(FoodMerchant).where(FoodMerchant.id == merchant_id))
        await session.execute(delete(TravelFood).where(TravelFood.id == food_id))
        await session.execute(delete(TravelHotspot).where(TravelHotspot.id == hotspot_id))
        await session.commit()
