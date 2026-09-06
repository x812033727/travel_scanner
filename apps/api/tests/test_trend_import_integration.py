"""The trend merchant import against a real PostgreSQL: dry run, apply, apply again."""

import os
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionFactory, engine
from app.foods.area_catalog import ALL_AREA_SEEDS
from app.foods.merchant_catalog import MERCHANT_SEEDS
from app.foods.service import seed_food_catalog
from app.foods.trend_import import (
    AUDIT_ACTION,
    DEFAULT_FILE,
    load_trend_merchants,
    persist_trend_merchants,
)
from app.models import (
    AdminAuditLog,
    FoodArea,
    FoodCategory,
    FoodDestination,
    FoodHotspot,
    FoodLocalization,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantFood,
    FoodMerchantSource,
    TravelFood,
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
    await session.execute(delete(FoodMerchantSource))
    await session.execute(delete(FoodMerchantFood))
    await session.execute(delete(FoodMerchantCategory))
    await session.execute(delete(FoodMerchant))
    await session.execute(delete(FoodArea))
    await session.execute(delete(FoodCategory))
    await session.execute(delete(FoodHotspot))
    await session.execute(delete(FoodDestination))
    await session.execute(delete(FoodLocalization))
    await session.execute(delete(TravelFood))
    await session.execute(delete(AdminAuditLog).where(AdminAuditLog.action == AUDIT_ACTION))
    await session.commit()


async def _count(session: AsyncSession, model: type[FoodMerchant] | type[AdminAuditLog]) -> int:
    return int(await session.scalar(select(func.count()).select_from(model)) or 0)


@pytest.mark.asyncio(loop_scope="module")
async def test_the_batch_is_reported_dry_applied_once_and_skipped_after() -> None:
    async with SessionFactory() as session:
        await _clear(session)
        await seed_food_catalog(session)
        assert await _count(session, FoodMerchant) == len(MERCHANT_SEEDS)
        assert int(await session.scalar(select(func.count(FoodArea.id))) or 0) == len(ALL_AREA_SEEDS)

    merchants = load_trend_merchants(DEFAULT_FILE)
    expected_new = len(merchants) - 2  # the two Tainan shops the curated catalog already has

    async with SessionFactory() as session:
        dry = await persist_trend_merchants(session, merchants, apply=False)
    assert dry["applied"] is False
    assert dry["created"] == expected_new
    assert dry["outcomes"] == {
        "skipped_existing_slug": 1,
        "skipped_same_name": 1,
        "would_create": expected_new,
    }
    async with SessionFactory() as session:
        assert await _count(session, FoodMerchant) == len(MERCHANT_SEEDS)
        assert await _count(session, AdminAuditLog) == 0

    async with SessionFactory() as session:
        applied = await persist_trend_merchants(
            session, merchants, apply=True, source_file=DEFAULT_FILE.name
        )
    assert applied["created"] == expected_new
    assert applied["outcomes"]["created"] == expected_new

    async with SessionFactory() as session:
        assert await _count(session, FoodMerchant) == len(MERCHANT_SEEDS) + expected_new
        row = await session.scalar(
            select(FoodMerchant).where(FoodMerchant.slug == "tokyo-dandelion-chocolate")
        )
        assert row is not None
        assert (row.review_status, row.is_active, row.map_match_status) == (
            "pending",
            False,
            "unverified",
        )
        assert row.country_code == "JP"
        assert row.address == "東京都台東区蔵前4-14-6"
        assert row.area_source == "admin"
        area = await session.get(FoodArea, row.area_id)
        assert area is not None and area.slug == "tokyo-kuramae"
        sources = (
            await session.scalars(
                select(FoodMerchantSource).where(FoodMerchantSource.merchant_id == row.id)
            )
        ).all()
        assert [(s.source_type, s.source_scope, s.claims_json, s.is_current) for s in sources] == [
            ("merchant_official", "merchant_website", ["display_name", "address"], True)
        ]
        links = (
            await session.scalars(
                select(FoodMerchantCategory)
                .where(FoodMerchantCategory.merchant_id == row.id)
                .order_by(FoodMerchantCategory.display_order)
            )
        ).all()
        categories = {
            c.id: c.slug for c in (await session.scalars(select(FoodCategory))).all()
        }
        assert [(categories[link.category_id], link.is_primary, link.source) for link in links] == [
            ("desserts-sweets", True, "admin"),
            ("cafe-tea", False, "admin"),
        ]
        audits = (
            await session.scalars(select(AdminAuditLog).where(AdminAuditLog.action == AUDIT_ACTION))
        ).all()
        assert [(a.target, a.metadata_json["count"], a.metadata_json["source"]) for a in audits] == [
            (f"food_merchants:{expected_new}", expected_new, "trend-merchant-sweep")
        ]

    # Running the same file again writes nothing and says so per row.
    async with SessionFactory() as session:
        again = await persist_trend_merchants(session, merchants, apply=True)
    assert again["created"] == 0
    assert again["outcomes"] == {
        "skipped_existing_slug": expected_new + 1,
        "skipped_same_name": 1,
    }
    async with SessionFactory() as session:
        assert await _count(session, FoodMerchant) == len(MERCHANT_SEEDS) + expected_new
        assert await _count(session, AdminAuditLog) == 1
        await _clear(session)
