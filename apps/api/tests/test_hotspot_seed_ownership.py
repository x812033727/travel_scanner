"""Exercise real seed reconciliation without requiring a running database."""

from copy import deepcopy
from dataclasses import replace
from datetime import UTC, date, datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.hotspots import service
from app.hotspots.catalog import HOTSPOT_SEEDS
from app.models import HotspotLocalization, TravelHotspot

SEED = next(seed for seed in HOTSPOT_SEEDS if seed.slug == "sensoji")
NOW = datetime(2026, 9, 7, tzinfo=UTC)


class SeedSession:
    def __init__(self, rows: list[object] | None = None) -> None:
        self.rows = list(rows or [])

    async def scalars(self, statement: object) -> SimpleNamespace:
        model = statement.column_descriptions[0]["entity"]
        return SimpleNamespace(all=lambda: [row for row in self.rows if isinstance(row, model)])

    def add(self, row: object) -> None:
        if row not in self.rows:
            self.rows.append(row)

    async def flush(self) -> None:
        for row in self.rows:
            if row.id is None:
                row.id = uuid4()
            if isinstance(row, TravelHotspot) and row.map_match_status is None:
                row.map_match_status = "unverified"


def snapshot(row: object) -> dict[str, object]:
    return {column.key: deepcopy(getattr(row, column.key)) for column in row.__table__.columns}


def existing_hotspot(**changes: object) -> TravelHotspot:
    fields = dict(
        id=uuid4(),
        slug=SEED.slug,
        name="Reviewed name",
        destination_id=SEED.destination_id,
        city_code=SEED.city_code,
        city_name=SEED.city_name,
        country_code=SEED.country_code,
        country_name=SEED.country_name,
        category="culture",
        search_text="reviewed search terms",
        latitude=Decimal("35.123456"),
        longitude=Decimal("139.123456"),
        coordinate_source_type="wikidata",
        coordinate_source_url="https://example.gov/reviewed-coordinate",
        coordinate_verified_at=NOW,
        wikipedia_project="en.wikipedia.org",
        wikipedia_title="Reviewed title",
        wikidata_item_id=SEED.wikidata_item_id,
        origin="curated",
        review_status="approved",
        review_reason=None,
        is_active=True,
        reviewed_at=NOW,
        map_match_status="unverified",
        source_urls=["https://example.gov/reviewed-place"],
        metadata_json={"local_name": "Reviewed original", "review_note": "retain this"},
    )
    return TravelHotspot(**(fields | changes))


@pytest.fixture(autouse=True)
def isolated_seed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "HOTSPOT_SEEDS", (SEED,))
    monkeypatch.setattr(service, "_upsert_signal", AsyncMock())


@pytest.mark.parametrize(
    "changes",
    [
        {"review_status": "pending"},
        {"review_status": "rejected", "review_reason": "Wrong Wikidata entity"},
        {"review_status": "disabled"},
        {"is_active": False},
        {"reviewed_by_user_id": uuid4()},
        {"review_reason": "Administrator reviewed the source identity"},
        {"map_match_status": "ambiguous"},
        {"map_match_status": "disabled"},
        {"map_match_status": "verified", "google_place_id": "ChIJ-reviewed"},
        {"naver_map_url": "https://map.naver.com/p/entry/place/12345"},
        {"map_verified_at": NOW},
        {"map_verified_by_user_id": uuid4()},
        {"coordinate_source_type": "official_tourism"},
    ],
)
async def test_reseed_preserves_review_decisions_and_the_entire_identity(
    changes: dict[str, object],
) -> None:
    hotspot = existing_hotspot(**changes)
    localization = HotspotLocalization(
        id=uuid4(), hotspot_id=hotspot.id, locale="en", name="Administrator label",
        aliases=["Administrator alias"], search_terms=["Administrator search"],
    )
    session = SeedSession([hotspot, localization])
    before = snapshot(hotspot), snapshot(localization)

    for _ in range(2):
        assert await service.seed_catalog(session, date(2026, 9, 7)) == [hotspot]

    assert (snapshot(hotspot), snapshot(localization)) == before
    assert session.rows == [hotspot, localization]


async def test_reseed_preserves_a_discovered_slug_and_pending_review() -> None:
    hotspot = existing_hotspot(
        slug=f"wikidata-{SEED.wikidata_item_id.lower()}",
        origin="wikimedia_discovery", review_status="pending", reviewed_at=None,
    )
    before = snapshot(hotspot)
    session = SeedSession([hotspot])

    await service.seed_catalog(session, date(2026, 9, 7))

    assert snapshot(hotspot) == before
    assert session.rows == [hotspot]


async def test_reseed_cannot_take_another_rows_wikidata_identity() -> None:
    target = existing_hotspot(wikidata_item_id="Q123456789")
    owner = existing_hotspot(slug="reviewed-other-place", reviewed_by_user_id=uuid4())
    session = SeedSession([target, owner])
    before = snapshot(target), snapshot(owner)

    await service.seed_catalog(session, date(2026, 9, 7))

    assert (snapshot(target), snapshot(owner)) == before
    assert session.rows == [target, owner]


async def test_fresh_seed_and_unreviewed_seed_updates_remain_idempotent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = SeedSession()
    first = await service.seed_catalog(session, date(2026, 9, 7))
    hotspot = first[0]
    assert hotspot.name == SEED.name
    assert hotspot.slug == SEED.slug
    assert hotspot.review_status == "approved"
    assert hotspot.map_match_status == "unverified"
    assert hotspot.google_place_id is None
    assert hotspot.naver_map_url is None
    assert hotspot.reviewed_at is not None  # Written by seed, not a human ownership marker.
    row_count = len(session.rows)
    corrected = replace(SEED, name="Corrected catalog name", latitude=35.123456)
    monkeypatch.setattr(service, "HOTSPOT_SEEDS", (corrected,))

    for _ in range(2):
        assert await service.seed_catalog(session, date(2026, 9, 7)) == first

    assert len(session.rows) == row_count
    assert hotspot.name == corrected.name
    assert hotspot.latitude == Decimal("35.123456")
    assert hotspot.slug == SEED.slug
    assert hotspot.map_match_status == "unverified"
