"""Attractions and food added to a plan re-label themselves per request locale."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

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
)

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
async def test_planned_stops_follow_the_request_locale_until_renamed() -> None:
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
        registered = await client.post(
            "/api/v1/auth/register",
            json={"email": f"localized-{suffix}@example.com", "password": "integration-pass-123"},
        )
        assert registered.status_code == 201
        headers = {"Authorization": f"Bearer {registered.json()['access_token']}"}
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
