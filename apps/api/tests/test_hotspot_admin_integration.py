import os
from collections.abc import AsyncIterator
from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.listing import (
    COUNTRY_ORDER,
    COUNTRY_RANK,
    DESTINATION_RANK,
    HOTSPOT_CATEGORY_ORDER,
)
from app.db import SessionFactory, engine
from app.hotspots.admin_router import list_hotspot_candidates
from app.hotspots.service import seed_catalog
from app.models import HotspotSignal, TravelHotspot, User

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
    await session.execute(delete(HotspotSignal))
    await session.execute(delete(TravelHotspot))
    await session.commit()


@pytest.mark.asyncio(loop_scope="module")
async def test_candidates_are_grouped_by_country_and_faceted() -> None:
    admin = User(email="hotspot-listing@example.test", password_hash="not-used", is_admin=True)
    async with SessionFactory() as session:
        await _clear(session)
        await seed_catalog(session, date(2026, 9, 1))
        await session.commit()

        listing = await list_hotspot_candidates(admin, session, locale="zh-TW", limit=100)
        assert listing["total"] >= len(listing["items"]) > 0
        keys = [
            (
                COUNTRY_RANK[item["country_code"]],
                DESTINATION_RANK.get(item["destination_id"], 3),
                item["destination_id"],
                item["name"],
            )
            for item in listing["items"]
        ]
        assert keys == sorted(keys)
        assert all(item["country_name"] for item in listing["items"])
        facets = listing["facets"]
        country_codes = [country["code"] for country in facets["countries"]]
        assert country_codes == [code for code in COUNTRY_ORDER if code in country_codes]
        assert sum(country["count"] for country in facets["countries"]) == listing["total"]
        assert {category["code"] for category in facets["categories"]} <= set(
            HOTSPOT_CATEGORY_ORDER
        )

        filtered = await list_hotspot_candidates(
            admin, session, locale="ja", country_code="JP", category="culture", limit=100
        )
        assert filtered["items"]
        assert all(
            item["country_code"] == "JP" and item["category"] == "culture"
            for item in filtered["items"]
        )
        # A facet ignores its own filter but honours the other one.
        assert {c["code"] for c in filtered["facets"]["countries"]} <= set(country_codes)
        japan_total = next(c["count"] for c in facets["countries"] if c["code"] == "JP")
        assert sum(c["count"] for c in filtered["facets"]["categories"]) == japan_total
        japan = next(c for c in filtered["facets"]["countries"] if c["code"] == "JP")
        assert japan["name"] == "日本"
        await _clear(session)
