import os
from collections.abc import AsyncIterator
from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionFactory, engine
from app.foods.admin_router import FoodBatchPayload, batch_foods
from app.foods.service import food_facets, list_foods, seed_food_catalog
from app.hotspots.service import seed_catalog
from app.models import (
    AdminAuditLog,
    FoodDestination,
    FoodHotspot,
    FoodLocalization,
    TravelFood,
    TravelHotspot,
    User,
)

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


async def _clear(session: AsyncSession) -> None:
    await session.execute(delete(FoodHotspot))
    await session.execute(delete(FoodDestination))
    await session.execute(delete(FoodLocalization))
    await session.execute(delete(TravelFood))
    await session.execute(delete(TravelHotspot))
    await session.commit()


@pytest.mark.asyncio(loop_scope="module")
async def test_food_seed_public_filters_maps_and_admin_state_are_idempotent() -> None:
    async with SessionFactory() as session:
        await _clear(session)
        await seed_catalog(session, date(2026, 9, 1))
        assert await seed_food_catalog(session) == 70
        await session.commit()

    async with SessionFactory() as session:
        assert int(await session.scalar(select(func.count(TravelFood.id))) or 0) == 70
        assert int(await session.scalar(select(func.count(FoodLocalization.id))) or 0) == 350
        assert int(await session.scalar(select(func.count(FoodDestination.id))) or 0) >= 70
        assert int(await session.scalar(select(func.count(FoodHotspot.id))) or 0) >= 70

        korean = await list_foods(session, locale="ko", country_code="KR", limit=20)
        assert korean["total"] == 10
        assert all(item["name"] for item in korean["items"])
        assert all(item["food_hotspots"] for item in korean["items"])
        assert all(
            item["food_hotspots"][0]["map_links"][0]["provider"] == "naver"
            for item in korean["items"]
        )
        facets = await food_facets(session)
        assert facets["total"] == 70
        assert len(facets["countries"]) == 7

        disabled = await session.scalar(select(TravelFood).order_by(TravelFood.slug).limit(1))
        assert disabled is not None
        disabled.review_status = "disabled"
        disabled.is_active = False
        await session.commit()

    async with SessionFactory() as session:
        assert await seed_food_catalog(session) == 70
        await session.commit()
        disabled = await session.scalar(select(TravelFood).order_by(TravelFood.slug).limit(1))
        assert disabled is not None
        assert disabled.review_status == "disabled"
        assert disabled.is_active is False
        assert int(await session.scalar(select(func.count(TravelFood.id))) or 0) == 70

        admin = User(
            email="food-admin-integration@example.test",
            password_hash="not-used",
            is_admin=True,
        )
        session.add(admin)
        await session.flush()
        candidate = await session.scalar(
            select(TravelFood).where(TravelFood.review_status == "approved").limit(1)
        )
        assert candidate is not None
        result = await batch_foods(
            FoodBatchPayload(ids=[candidate.id], action="disable"), admin, session
        )
        assert result == {"updated": 1, "status": "disabled"}
        await session.refresh(candidate)
        assert candidate.review_status == "disabled"
        assert candidate.is_active is False
        audit = await session.scalar(
            select(AdminAuditLog).where(
                AdminAuditLog.actor_user_id == admin.id,
                AdminAuditLog.action == "foods_batch_updated",
            )
        )
        assert audit is not None
        await session.delete(audit)
        await session.delete(admin)
        await session.commit()
        await _clear(session)
