from copy import deepcopy
from dataclasses import replace
from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace
from typing import Any, cast
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import service
from app.foods.catalog import FOOD_SEEDS
from app.foods.merchant_catalog import MerchantDirectSourceSeed, MerchantSeed
from app.models import (
    FoodLocalization,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantFood,
    FoodMerchantSource,
    TravelFood,
)

FOOD_SEED = next(seed for seed in FOOD_SEEDS if seed.slug == "jp-sushi")
MERCHANT_SEED = MerchantSeed(
    slug="tokyo-seed-ownership", destination_id="tokyo", country_code="JP",
    name="Seed restaurant", local_name="種子料理店", food_slugs=(), display_order=1,
)
DIRECT_SOURCE = MerchantDirectSourceSeed(
    merchant_slug=MERCHANT_SEED.slug, source_type="merchant_official",
    source_scope="merchant_website", source_title="Restaurant official page",
    source_url="https://example.test/restaurant", claims=("display_name", "official_website"),
    official_website_url="https://example.test/restaurant",
)
NOW = datetime(2026, 9, 7, tzinfo=UTC)


class FoodSeedSession:
    def __init__(self) -> None:
        self.rows: list[Any] = []

    async def scalars(self, statement: Any) -> SimpleNamespace:
        column = statement.column_descriptions[0]
        model = column["entity"]
        rows = [row for row in self.rows if isinstance(row, model)]
        if column["expr"] is not model:
            rows = [getattr(row, column["expr"].key) for row in rows]
        return SimpleNamespace(all=lambda: rows)

    def add(self, row: object) -> None:
        if row not in self.rows:
            self.rows.append(row)

    async def flush(self) -> None:
        for row in self.rows:
            if row.id is None:
                row.id = uuid4()


def snapshot(row: Any) -> dict[str, object]:
    return {column.key: deepcopy(getattr(row, column.key)) for column in row.__table__.columns}


@pytest.fixture(autouse=True)
def isolated_catalog(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(service, "FOOD_SEEDS", (FOOD_SEED,))
    monkeypatch.setattr(service, "MERCHANT_SEEDS", ())
    monkeypatch.setattr(service, "MERCHANT_DIRECT_SOURCE_SEEDS", ())
    monkeypatch.setattr(service, "CATEGORY_SEEDS", ())
    monkeypatch.setattr(service, "ALL_AREA_SEEDS", ())


@pytest.mark.parametrize("status", ["pending", "rejected", "disabled", "approved"])
async def test_dish_reseed_preserves_admin_names_sources_and_review(status: str) -> None:
    session = FoodSeedSession()
    await service.seed_food_catalog(cast(AsyncSession, session))
    food = next(row for row in session.rows if isinstance(row, TravelFood))
    localization = next(row for row in session.rows if isinstance(row, FoodLocalization))
    food.source = "admin"
    food.romanized_name = "Administrator dish name"
    food.source_urls = ["https://example.gov/reviewed-dish"]
    food.review_status = status
    food.is_active = status == "approved"
    localization.source = "admin"
    localization.name = "Administrator localized name"
    localization.summary = "Administrator summary"
    before = snapshot(food), snapshot(localization)
    row_count = len(session.rows)

    for _ in range(2):
        assert await service.seed_food_catalog(cast(AsyncSession, session)) == 1

    assert (snapshot(food), snapshot(localization)) == before
    assert len(session.rows) == row_count


@pytest.mark.parametrize("status", ["pending", "rejected", "disabled"])
async def test_dish_seed_text_updates_do_not_publish_a_held_dish(
    status: str, monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = FoodSeedSession()
    await service.seed_food_catalog(cast(AsyncSession, session))
    food = next(row for row in session.rows if isinstance(row, TravelFood))
    food.review_status = status
    food.is_active = False
    monkeypatch.setattr(service, "FOOD_SEEDS", (replace(FOOD_SEED, romanized_name="New seed"),))

    await service.seed_food_catalog(cast(AsyncSession, session))

    assert food.romanized_name == "New seed"
    assert food.review_status == status
    assert food.is_active is False


async def seed_merchant(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[FoodSeedSession, FoodMerchant]:
    monkeypatch.setattr(service, "MERCHANT_SEEDS", (MERCHANT_SEED,))
    monkeypatch.setattr(service, "MERCHANT_DIRECT_SOURCE_SEEDS", (DIRECT_SOURCE,))
    session = FoodSeedSession()
    await service.seed_food_catalog(cast(AsyncSession, session))
    merchant = next(row for row in session.rows if isinstance(row, FoodMerchant))
    return session, merchant


async def test_fresh_merchant_sources_and_reseeding_are_idempotent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, merchant = await seed_merchant(monkeypatch)
    sources = [row for row in session.rows if isinstance(row, FoodMerchantSource)]
    assert len(sources) == 2
    assert merchant.review_status == "pending"
    assert merchant.map_match_status == "unverified"
    assert merchant.is_active is False
    assert merchant.official_website_url == DIRECT_SOURCE.official_website_url
    before = snapshot(merchant), [snapshot(row) for row in sources]
    row_count = len(session.rows)

    for _ in range(2):
        await service.seed_food_catalog(cast(AsyncSession, session))

    assert len(session.rows) == row_count
    assert (snapshot(merchant), [snapshot(row) for row in sources]) == before


@pytest.mark.parametrize("status", ["pending", "rejected", "disabled", "approved"])
async def test_merchant_review_identity_and_source_edits_survive_seed(
    status: str, monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, merchant = await seed_merchant(monkeypatch)
    merchant.name = "Reviewed merchant"
    merchant.local_name = "人工確認店名"
    merchant.names_json = {"en": "Reviewed English name"}
    merchant.latitude = Decimal("35.123456")
    merchant.longitude = Decimal("139.123456")
    merchant.coordinate_source_type = "merchant_official"
    merchant.coordinate_source_url = "https://example.test/reviewed-coordinates"
    merchant.coordinate_verified_at = NOW
    merchant.google_place_id = "ChIJ-reviewed-restaurant"
    merchant.map_match_status = "verified" if status == "approved" else "unverified"
    merchant.review_status = status
    merchant.is_active = status == "approved"
    merchant.verified_at = NOW if status == "approved" else None
    # A cleared website and deactivated source are deliberate, even while pending.
    merchant.official_website_url = None
    merchant.official_website_verified_at = None
    sources = [row for row in session.rows if isinstance(row, FoodMerchantSource)]
    for source in sources:
        source.source_url += "/reviewed"
        source.source_title = "Administrator reviewed source"
        source.claims_json = ["address"]
        source.is_current = False
        source.last_verified_at = NOW
    before = snapshot(merchant), [snapshot(row) for row in sources]
    row_count = len(session.rows)

    for _ in range(2):
        await service.seed_food_catalog(cast(AsyncSession, session))

    assert len(session.rows) == row_count
    assert (snapshot(merchant), [snapshot(row) for row in sources]) == before


async def test_a_seed_adopts_a_merchant_an_administrator_published_and_only_links_the_dish(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Production holds merchants an administrator created and published by hand
    (``busan-songjeong-samdae-gukbap``), in no seed file. A seed that names one of them as
    the anchor of a new dish must add the dish link and nothing else: not a second merchant,
    not a source, not a category, and never a change of review state or identity on a row
    the public already sees."""
    session = FoodSeedSession()
    merchant = FoodMerchant(
        slug=MERCHANT_SEED.slug, destination_id="tokyo", country_code="JP",
        name="Published by hand", local_name="手動公開店", display_order=7,
        review_status="approved", is_active=True, map_match_status="verified",
        google_place_id="ChIJ-published-by-hand", area_source="admin", verified_at=NOW,
    )
    merchant.id = uuid4()
    source = FoodMerchantSource(
        merchant_id=merchant.id, source_type="official_tourism",
        source_scope="merchant_listing", source_title="Tourism board page",
        source_url="https://example.test/listing", claims_json=["display_name"],
        is_current=True, last_verified_at=NOW,
    )
    source.id = uuid4()
    curated = FoodMerchantCategory(
        merchant_id=merchant.id, category_id=uuid4(), is_primary=True, display_order=1,
        source="admin",
    )
    curated.id = uuid4()
    session.rows += [merchant, source, curated]
    monkeypatch.setattr(
        service, "MERCHANT_SEEDS", (replace(MERCHANT_SEED, food_slugs=(FOOD_SEED.slug,)),)
    )
    monkeypatch.setattr(service, "MERCHANT_DIRECT_SOURCE_SEEDS", (DIRECT_SOURCE,))
    before = snapshot(merchant), snapshot(source), snapshot(curated)

    for _ in range(2):
        await service.seed_food_catalog(cast(AsyncSession, session))

    assert (snapshot(merchant), snapshot(source), snapshot(curated)) == before
    assert [row for row in session.rows if isinstance(row, FoodMerchant)] == [merchant]
    assert [row for row in session.rows if isinstance(row, FoodMerchantSource)] == [source]
    assert [row for row in session.rows if isinstance(row, FoodMerchantCategory)] == [curated]
    food = next(row for row in session.rows if isinstance(row, TravelFood))
    links = [row for row in session.rows if isinstance(row, FoodMerchantFood)]
    assert [(link.merchant_id, link.food_id) for link in links] == [(merchant.id, food.id)]


async def test_unverified_merchant_with_deleted_sources_is_not_treated_as_new(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session, merchant = await seed_merchant(monkeypatch)
    session.rows = [row for row in session.rows if not isinstance(row, FoodMerchantSource)]
    merchant.official_website_url = None
    merchant.official_website_verified_at = None

    await service.seed_food_catalog(cast(AsyncSession, session))

    assert not any(isinstance(row, FoodMerchantSource) for row in session.rows)
    assert merchant.official_website_url is None
    assert merchant.review_status == "pending"
    assert merchant.map_match_status == "unverified"
