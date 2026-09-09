import runpy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from alembic import context
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine

from app.foods.merchant_catalog import MERCHANT_SEEDS
from app.foods.platform_link_catalog import PLATFORM_LINK_AUDIT_SEEDS
from app.foods.platform_links import (
    PLATFORMS_BY_COUNTRY,
    expected_platform,
    serialize_reservation_link,
    validate_platform_url,
)
from app.models import FoodMerchantPlatformLink


@pytest.mark.parametrize(
    ("country", "provider"),
    [
        ("JP", "tablecheck"),
        ("KR", "catchtable_global"),
        ("TW", "eztable"),
        ("SG", "chope"),
        ("HK", "openrice"),
        ("TH", "hungry_hub"),
        ("VN", "pasgo"),
    ],
)
def test_country_has_one_fixed_reservation_platform(country: str, provider: str) -> None:
    assert expected_platform(country).provider == provider


@pytest.mark.parametrize(
    ("provider", "url"),
    [
        ("tablecheck", "https://www.tablecheck.com/en/shops/sushi-sakai/reserve"),
        ("catchtable_global", "https://www.catchtable.net/shop/example"),
        ("eztable", "https://www.eztable.com/restaurant/example"),
        ("chope", "https://www.chope.co/singapore-restaurants/restaurant/song-fa"),
        ("openrice", "https://www.openrice.com/en/hongkong/p-yat-lok-p23206360"),
        ("hungry_hub", "https://web.hungryhub.com/en/restaurants/krua-apsorn/web"),
        ("pasgo", "https://pasgo.vn/nha-hang/example"),
    ],
)
def test_exact_merchant_urls_are_accepted(provider: str, url: str) -> None:
    assert validate_platform_url(provider, url) == url


@pytest.mark.parametrize(
    ("provider", "url"),
    [
        ("tablecheck", "https://www.tablecheck.com/en/japan"),
        ("catchtable_global", "https://www.catchtable.net/"),
        ("chope", "https://www.chope.co/singapore-restaurants/list_of_restaurants"),
        ("openrice", "https://www.openrice.com/en/hongkong/restaurants"),
        ("pasgo", "https://pasgo.vn/"),
    ],
)
def test_home_search_and_list_pages_are_rejected(provider: str, url: str) -> None:
    with pytest.raises(ValueError):
        validate_platform_url(provider, url)


def test_every_curated_merchant_has_a_conservative_audit_result() -> None:
    assert len(MERCHANT_SEEDS) == 173
    assert len(PLATFORM_LINK_AUDIT_SEEDS) == len(MERCHANT_SEEDS)
    assert len({item.merchant_slug for item in PLATFORM_LINK_AUDIT_SEEDS}) == 173
    merchants = {item.slug: item for item in MERCHANT_SEEDS}
    for audit in PLATFORM_LINK_AUDIT_SEEDS:
        assert audit.status in {"verified", "not_found", "ambiguous", "disabled"}
        assert audit.provider == PLATFORMS_BY_COUNTRY[
            merchants[audit.merchant_slug].country_code
        ].provider
        if audit.status == "verified":
            assert audit.canonical_url
            validate_platform_url(audit.provider, audit.canonical_url)


def test_public_link_requires_verified_status_and_country_provider_match() -> None:
    row = FoodMerchantPlatformLink(
        provider="catchtable_global",
        canonical_url="https://www.catchtable.net/shop/example",
        localized_urls_json={},
        status="verified",
        checked_at=datetime(2026, 9, 8, tzinfo=UTC),
    )
    public = serialize_reservation_link(row, country_code="KR", locale="zh-TW")
    assert public == {
        "provider": "catchtable_global",
        "label": "Catchtable Global",
        "url": "https://www.catchtable.net/shop/example",
        "verified_at": "2026-09-08T00:00:00+00:00",
        "language_code": "en",
    }
    row.status = "ambiguous"
    assert serialize_reservation_link(row, country_code="KR", locale="zh-TW") is None
    row.status = "verified"
    assert serialize_reservation_link(row, country_code="JP", locale="zh-TW") is None


def test_localized_url_is_selected_only_when_reviewed_on_the_same_row() -> None:
    row = FoodMerchantPlatformLink(
        provider="tablecheck",
        canonical_url="https://www.tablecheck.com/en/shops/sushi-sakai/reserve",
        localized_urls_json={
            "ja": "https://www.tablecheck.com/ja/shops/sushi-sakai/reserve"
        },
        status="verified",
        checked_at=datetime(2026, 9, 8, tzinfo=UTC),
    )
    public = serialize_reservation_link(row, country_code="JP", locale="ja")
    assert public is not None
    assert public["url"] == "https://www.tablecheck.com/ja/shops/sushi-sakai/reserve"
    assert public["language_code"] == "ja"


@pytest.mark.asyncio
async def test_migration_is_idempotent_and_round_trips() -> None:
    migration = runpy.run_path(
        str(Path("migrations/versions/0062_food_merchant_platform_links.py"))
    )
    engine = create_async_engine("sqlite+aiosqlite://")

    def run(connection: Any) -> None:
        with (
            Operations.context(MigrationContext.configure(connection)),
            pytest.MonkeyPatch.context() as patch,
        ):
            patch.setattr(context, "is_offline_mode", lambda: False)
            migration["upgrade"]()
            migration["upgrade"]()
            columns = {
                item["name"]
                for item in inspect(connection).get_columns("food_merchant_platform_links")
            }
            assert columns == {
                column.name for column in FoodMerchantPlatformLink.__table__.columns
            }
            migration["downgrade"]()
            assert "food_merchant_platform_links" not in inspect(connection).get_table_names()

    async with engine.begin() as connection:
        await connection.run_sync(run)
    await engine.dispose()
