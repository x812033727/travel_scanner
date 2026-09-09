"""One synthetic catalog stop for the isolated, unmocked frontend-flow CI journey.

From apps/api: PYTHONPATH=. DISCOVERY_E2E=1 python tests/fixtures/frontend_flow_seed.py
DATABASE_URL must explicitly select the loopback PostgreSQL CI database. This
does not enable discovery, call providers, create users, or modify real catalog
rows. The fixture's names, map ID and evidence URLs are deliberately synthetic.
"""

from __future__ import annotations

import asyncio
import ipaddress
import os
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

FIXTURE_ID = UUID("55000000-0000-4000-8000-000000000001")
FIXTURE_SLUG = "frontend-flow-fixture-tokyo-river"
FIXTURE_TITLE = "Frontend flow fixture Tokyo river"
FIXTURE_SOURCE = "https://example.test/frontend-flow-fixture/tokyo-river"


def require_isolated_target(database_url: str | URL) -> URL:
    """Reject before opening a connection; never include credentials in errors."""
    if os.environ.get("DISCOVERY_E2E") != "1":
        raise RuntimeError("Frontend-flow seed requires DISCOVERY_E2E=1")
    try:
        target = make_url(database_url)
        loopback = target.host == "localhost" or ipaddress.ip_address(target.host or "").is_loopback
    except (ArgumentError, ValueError):
        raise RuntimeError(
            "Frontend-flow seed requires an explicit loopback PostgreSQL URL"
        ) from None
    if (
        not loopback
        or target.drivername != "postgresql+asyncpg"
        or not target.database
        or target.query
    ):
        raise RuntimeError("Frontend-flow seed requires an explicit loopback PostgreSQL URL")
    return target


async def seed_catalog(session: AsyncSession) -> None:
    # Verify the actual bound engine as well as the process opt-in, not just a
    # caller-provided URL that could differ from the session's database.
    require_isolated_target(session.get_bind().engine.url)
    from app.models import TravelHotspot

    existing = await session.get(TravelHotspot, FIXTURE_ID)
    slug_owner = await session.scalar(
        select(TravelHotspot.id).where(TravelHotspot.slug == FIXTURE_SLUG)
    )
    if (existing and existing.slug != FIXTURE_SLUG) or slug_owner not in (None, FIXTURE_ID):
        raise RuntimeError("Frontend-flow fixture identity is occupied; no rows changed")
    now = datetime.now(UTC)
    values = {
        "slug": FIXTURE_SLUG,
        "name": FIXTURE_TITLE,
        "search_text": FIXTURE_TITLE,
        "destination_id": "tokyo",
        "city_code": "NRT",
        "city_name": "Tokyo",
        "country_code": "JP",
        "country_name": "Japan",
        "category": "nature",
        "latitude": Decimal("35.710000"),
        "longitude": Decimal("139.810000"),
        "coordinate_source_type": "admin_verified",
        "coordinate_source_url": FIXTURE_SOURCE,
        "coordinate_verified_at": now,
        "google_place_id": "FrontendFlowFixtureTokyoRiver",
        "map_match_status": "verified",
        "map_verified_at": now,
        "review_status": "approved",
        "reviewed_at": now,
        "is_active": True,
        "source_urls": [FIXTURE_SOURCE],
        "metadata_json": {"fixture": "frontend_flow", "recommended_duration_minutes": 60},
    }
    if existing is None:
        session.add(TravelHotspot(id=FIXTURE_ID, **values))
    else:
        for field, value in values.items():
            setattr(existing, field, value)
    await session.flush()


async def main() -> None:
    database_url = require_isolated_target(os.environ.get("DATABASE_URL", ""))
    engine = create_async_engine(database_url)
    try:
        async with async_sessionmaker(engine)() as session, session.begin():
            await seed_catalog(session)
        print(f"Frontend-flow CI fixture ready: hotspot:{FIXTURE_ID}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
