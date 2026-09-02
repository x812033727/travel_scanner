import os
from collections.abc import AsyncIterator
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from app.db import SessionFactory, engine
from app.main import app
from app.models import FoodFavorite, HotspotFavorite, TravelFood, TravelHotspot, User

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    yield
    await engine.dispose(close=False)


@pytest.mark.asyncio(loop_scope="module")
async def test_saved_items_are_account_scoped_idempotent_and_public_only() -> None:
    suffix = uuid4().hex
    async with SessionFactory() as session:
        hotspot = TravelHotspot(
            slug=f"saved-hotspot-{suffix}", name="Saved Hotspot", city_code="TPE",
            destination_id="taipei", city_name="Taipei", country_code="TW",
            country_name="Taiwan", category="culture", search_text="saved",
            google_place_id=f"saved-place-{suffix}", map_match_status="verified",
            review_status="approved", is_active=True,
        )
        food = TravelFood(
            slug=f"saved-food-{suffix}", country_code="TW", local_name="收藏料理",
            romanized_name="Saved Food", food_kind="main", search_text="saved",
            source_urls=["https://example.test/source"], review_status="approved", is_active=True,
        )
        session.add_all([hotspot, food])
        await session.commit()
        hotspot_id, food_id = hotspot.id, food.id

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        registration = await client.post(
            "/api/v1/auth/register",
            json={
                "email": f"saved-{suffix}@example.com",
                "password": "integration-password-123",
            },
        )
        assert registration.status_code == 201
        user_id = UUID(registration.json()["user"]["id"])
        headers = {"Authorization": f"Bearer {registration.json()['access_token']}"}
        assert (await client.get("/api/v1/saved-items")).status_code == 401
        for item_type, item_id in (("hotspot", hotspot_id), ("food", food_id)):
            first = await client.put(f"/api/v1/saved-items/{item_type}/{item_id}", headers=headers)
            replay = await client.put(f"/api/v1/saved-items/{item_type}/{item_id}", headers=headers)
            assert first.status_code == replay.status_code == 201
        listed = await client.get("/api/v1/saved-items", headers=headers)
        assert listed.status_code == 200
        assert {(item["type"], item["id"]) for item in listed.json()["items"]} == {
            ("hotspot", str(hotspot_id)), ("food", str(food_id))
        }
        removed = await client.delete(f"/api/v1/saved-items/hotspot/{hotspot_id}", headers=headers)
        assert removed.status_code == 204

    async with SessionFactory() as session:
        await session.execute(
            delete(HotspotFavorite).where(HotspotFavorite.hotspot_id == hotspot_id)
        )
        await session.execute(delete(FoodFavorite).where(FoodFavorite.food_id == food_id))
        await session.execute(delete(TravelHotspot).where(TravelHotspot.id == hotspot_id))
        await session.execute(delete(TravelFood).where(TravelFood.id == food_id))
        await session.execute(delete(User).where(User.id == user_id))
        await session.commit()
