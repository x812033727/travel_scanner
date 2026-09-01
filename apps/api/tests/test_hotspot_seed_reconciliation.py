import os
from collections.abc import AsyncIterator
from datetime import UTC, date, datetime

import pytest
import pytest_asyncio
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionFactory, engine
from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.service import seed_catalog
from app.models import HotspotPlaceProfile, HotspotSignal, TravelHotspot

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    # Pooled asyncpg connections stay bound to this module's event loop; leaving them
    # in the pool makes the next integration module fail with "Event loop is closed".
    await engine.dispose(close=False)
    yield
    await engine.dispose()


async def _clear(session: AsyncSession) -> None:
    await session.execute(delete(HotspotSignal))
    await session.execute(delete(TravelHotspot))
    await session.commit()


@pytest.mark.asyncio(loop_scope="module")
async def test_seeding_adopts_a_place_discovery_already_stored() -> None:
    """Discovery finds places before the curated catalog lists them.

    It stores them under a generated slug, so a later catalog release that adds the
    same Wikidata item used to hit uq_travel_hotspots_wikidata_item_id and abort the
    whole collection run.
    """
    # Part of the catalog is itself slugged "wikidata-<id>"; those entries match by slug
    # and never collided. The regression needs a seed whose curated slug differs.
    seed = next(
        item
        for item in HOTSPOT_SEEDS
        if item.slug != f"wikidata-{item.wikidata_item_id.lower()}"
    )
    async with SessionFactory() as session:
        await _clear(session)
        discovered = TravelHotspot(
            slug=f"wikidata-{seed.wikidata_item_id.lower()}",
            name="Discovered name",
            city_code=seed.city_code,
            city_name=seed.city_name,
            country_code=seed.country_code,
            country_name=seed.country_name,
            category=seed.category,
            search_text=seed.search_text,
            wikidata_item_id=seed.wikidata_item_id,
            wikipedia_project=seed.wikipedia_project,
            wikipedia_title=seed.wikipedia_title,
            origin="wikimedia_discovery",
            review_status="pending",
            is_active=True,
            discovered_at=datetime.now(UTC),
            last_seen_at=datetime.now(UTC),
        )
        session.add(discovered)
        await session.commit()
        discovered_id = discovered.id

    async with SessionFactory() as session:
        await seed_catalog(session, date(2026, 9, 1))
        await session.commit()

    async with SessionFactory() as session:
        rows = list(
            (
                await session.scalars(
                    select(TravelHotspot).where(
                        TravelHotspot.wikidata_item_id == seed.wikidata_item_id
                    )
                )
            ).all()
        )
        # One row, not two: the curated seed took over the discovered one.
        assert len(rows) == 1
        assert rows[0].id == discovered_id
        assert rows[0].slug == seed.slug
        assert rows[0].name == seed.name
        assert rows[0].origin == "curated"
        assert rows[0].review_status == "approved"
        await _clear(session)


@pytest.mark.asyncio(loop_scope="module")
async def test_seeding_is_idempotent_on_a_clean_catalog() -> None:
    async with SessionFactory() as session:
        await _clear(session)
        await seed_catalog(session, date(2026, 9, 1))
        await session.commit()

    async with SessionFactory() as session:
        await seed_catalog(session, date(2026, 9, 2))
        await session.commit()

    async with SessionFactory() as session:
        total = len(list((await session.scalars(select(TravelHotspot))).all()))
        assert total == len(HOTSPOT_SEEDS)
        await _clear(session)


@pytest.mark.asyncio(loop_scope="module")
async def test_seeding_preserves_place_id_and_manual_official_website() -> None:
    async with SessionFactory() as session:
        await _clear(session)
        hotspots = await seed_catalog(session, date(2026, 9, 1))
        hotspot = hotspots[0]
        hotspot.google_place_id = "ChIJ-legacy-locked"
        session.add(
            HotspotPlaceProfile(
                hotspot_id=hotspot.id,
                place_id_source="manual",
                match_status="approved",
                manual_official_website_url="https://example.gov/official",
                manual_official_website_source_url="https://example.gov/directory",
                website_review_status="approved",
            )
        )
        await session.commit()
        hotspot_id = hotspot.id

    async with SessionFactory() as session:
        await seed_catalog(session, date(2026, 9, 2))
        await session.commit()

    async with SessionFactory() as session:
        hotspot = await session.get(TravelHotspot, hotspot_id)
        profile = await session.scalar(
            select(HotspotPlaceProfile).where(HotspotPlaceProfile.hotspot_id == hotspot_id)
        )
        assert hotspot is not None
        assert hotspot.google_place_id == "ChIJ-legacy-locked"
        assert profile is not None
        assert profile.place_id_source == "manual"
        assert profile.manual_official_website_url == "https://example.gov/official"
        await _clear(session)
