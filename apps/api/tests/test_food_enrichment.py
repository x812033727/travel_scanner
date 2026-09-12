"""The shared merchant enrichment writer: what it fills, what it refuses, what it never touches."""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest
import pytest_asyncio
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.foods.enrichment import (
    PLATFORM_HOSTS,
    EnrichmentOrigin,
    MerchantEnrichmentProposal,
    apply_merchant_enrichment,
    is_platform_host,
    proposal_from_corrections,
)
from app.models import (
    AdminAuditLog,
    Base,
    FoodArea,
    FoodCategory,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantSource,
)
from app.problems import AppError

IMPORT = EnrichmentOrigin(kind="json_import", reference="2026-09-12-pilot")
REVIEW = EnrichmentOrigin(kind="catalog_review", reference="run/item")
OFFICIAL = "https://sushi-dai.example/tsukiji"
LISTING = "https://www.gotokyo.org/en/spot/sushi-dai"
NOW = datetime(2026, 9, 12, 8, 0, tzinfo=UTC)


@pytest_asyncio.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


def merchant(**overrides: Any) -> FoodMerchant:
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": "tokyo-sushi-dai",
        "destination_id": "tokyo",
        "country_code": "JP",
        "name": "Sushi Dai",
        "local_name": "寿司大",
        "review_status": "pending",
        "map_match_status": "unverified",
        "is_active": False,
    }
    values.update(overrides)
    return FoodMerchant(**values)


async def seed(
    session: AsyncSession,
    *rows: Any,
) -> None:
    session.add_all(rows)
    await session.flush()


def area(slug: str = "tokyo-tsukiji", destination_id: str = "tokyo", **overrides: Any) -> FoodArea:
    values: dict[str, Any] = {
        "slug": slug,
        "destination_id": destination_id,
        "country_code": "JP",
        "names_json": {"en": "Tsukiji"},
        "match_terms_json": ["築地"],
        "is_active": True,
    }
    values.update(overrides)
    return FoodArea(**values)


def category(slug: str, **overrides: Any) -> FoodCategory:
    values: dict[str, Any] = {"slug": slug, "names_json": {"en": slug}, "is_active": True}
    values.update(overrides)
    return FoodCategory(**values)


def proposal(**overrides: Any) -> MerchantEnrichmentProposal:
    values: dict[str, Any] = {
        "address": "東京都中央区築地5-2-1",
        "official_website": {
            "url": OFFICIAL,
            "title": "寿司大 築地",
            "quote": "寿司大 東京都中央区築地5-2-1 営業時間",
        },
        "listing_source": {
            "url": LISTING,
            "title": "Sushi Dai | GO TOKYO",
            "quote": "Sushi Dai, a Tsukiji institution",
        },
        "area_slug": "tokyo-tsukiji",
        "category_slugs": ["sushi"],
    }
    values.update(overrides)
    return MerchantEnrichmentProposal.model_validate(values)


async def audits(session: AsyncSession) -> list[AdminAuditLog]:
    return list(
        (
            await session.scalars(
                select(AdminAuditLog).where(AdminAuditLog.action == "food_merchant_enriched")
            )
        ).all()
    )


async def sources(session: AsyncSession, row: FoodMerchant) -> list[FoodMerchantSource]:
    return list(
        (
            await session.scalars(
                select(FoodMerchantSource)
                .where(FoodMerchantSource.merchant_id == row.id)
                .order_by(FoodMerchantSource.source_url)
            )
        ).all()
    )


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ({"address": "x", "latitude": 35.0}, ValidationError),
        ({"address": "x", "review_status": "approved"}, ValidationError),
        ({"official_website": {"url": "http://sushi-dai.example/", "title": "t"}}, AppError),
        (
            {
                "official_website": {
                    "url": "https://tabelog.com/tokyo/A1313/A131301/13002260/",
                    "title": "t",
                }
            },
            ValidationError,
        ),
        (
            {"listing_source": {"url": "https://www.google.com/maps/place/x", "title": "t"}},
            AppError,
        ),
        ({"google_place_id": "short"}, ValidationError),
        ({"category_slugs": ["sushi", "sushi"]}, ValidationError),
        ({"area_slug": "Not A Slug"}, ValidationError),
    ],
)
def test_proposal_rejects_extra_fields_http_platform_and_google_urls(
    values: dict[str, Any], expected: type[Exception]
) -> None:
    with pytest.raises(expected):
        MerchantEnrichmentProposal.model_validate(values)


def test_proposal_from_corrections_groups_fields_and_never_includes_place_id() -> None:
    result = proposal_from_corrections(
        [
            {
                "field": "address",
                "value": "東京都中央区築地5-2-1",
                "source_url": OFFICIAL,
                "quote": "q",
            },
            {
                "field": "official_website_url",
                "value": OFFICIAL,
                "source_url": OFFICIAL,
                "quote": "寿司大",
            },
            {
                "field": "listing_source_url",
                "value": LISTING,
                "title": "GO TOKYO",
                "quote": "Sushi Dai",
            },
            {"field": "area_slug", "value": "tokyo-tsukiji"},
            {"field": "category_slug", "value": "sushi"},
            {"field": "category_slug", "value": "sushi"},
            {"field": "category_slug", "value": "seafood"},
            {"field": "google_place_id", "value": "ChIJshouldnotbehere"},
            {"field": "latitude", "value": "35.0"},
        ]
    )
    assert result.address == "東京都中央区築地5-2-1"
    assert result.official_website is not None and result.official_website.quote == "寿司大"
    assert result.official_website.title == "sushi-dai.example"
    assert result.listing_source is not None and result.listing_source.title == "GO TOKYO"
    assert result.area_slug == "tokyo-tsukiji"
    assert result.category_slugs == ["sushi", "seafood"]
    assert result.google_place_id is None


async def test_apply_fills_only_empty_scalars_and_reports_skipped(session: AsyncSession) -> None:
    row = merchant(address="既有地址")
    tsukiji = area()
    await seed(session, row, tsukiji, category("sushi"))
    outcome = await apply_merchant_enrichment(
        session, row, proposal(), actor_id=None, origin=IMPORT, evidence=[], now=NOW
    )
    assert outcome.skipped == {"address": "already_set"}
    assert outcome.applied == {"official_website_url": OFFICIAL, "area_slug": "tokyo-tsukiji"}
    assert row.address == "既有地址"
    assert row.official_website_url == OFFICIAL
    assert row.official_website_verified_at == NOW
    assert row.area_id == tsukiji.id and row.area_source == "admin"
    assert outcome.sources_added == [OFFICIAL, LISTING]
    assert outcome.categories_added == ["sushi"]

    # A second proposal with a *different* official site is refused, the first one kept.
    again = await apply_merchant_enrichment(
        session,
        row,
        proposal(official_website={"url": "https://other.example/", "title": "other"}),
        actor_id=None,
        origin=IMPORT,
        evidence=[],
        now=NOW,
    )
    assert again.skipped["official_website_url"] == "already_set"
    assert again.skipped["area_slug"] == "already_set"
    assert row.official_website_url == OFFICIAL
    assert not again.changed


async def test_apply_upserts_source_by_url_unions_claims_and_refreshes_last_verified_at(
    session: AsyncSession,
) -> None:
    row = merchant()
    earlier = datetime(2026, 9, 1, tzinfo=UTC)
    await seed(
        session,
        row,
        area(),
        category("sushi"),
        FoodMerchantSource(
            merchant_id=row.id,
            source_type="merchant_official",
            source_scope="merchant_website",
            source_title="Human title",
            source_url=OFFICIAL,
            claims_json=["display_name"],
            is_current=False,
            last_verified_at=earlier,
        ),
    )
    outcome = await apply_merchant_enrichment(
        session, row, proposal(), actor_id=None, origin=IMPORT, evidence=[], now=NOW
    )
    assert outcome.sources_refreshed == [OFFICIAL]
    assert outcome.sources_added == [LISTING]
    rows = await sources(session, row)
    assert [item.source_url for item in rows] == sorted([OFFICIAL, LISTING])
    official = next(item for item in rows if item.source_url == OFFICIAL)
    assert official.source_title == "Human title"
    assert official.claims_json == ["display_name", "official_website", "address"]
    assert official.is_current is True
    assert official.last_verified_at.replace(tzinfo=UTC) == NOW

    second = await apply_merchant_enrichment(
        session, row, proposal(), actor_id=None, origin=IMPORT, evidence=[], now=NOW
    )
    assert second.changed is False
    assert second.sources_added == [] and second.categories_added == []
    assert len(await sources(session, row)) == 2


async def test_apply_derives_address_claim_only_when_quote_contains_address(
    session: AsyncSession,
) -> None:
    row = merchant()
    await seed(session, row, area(), category("sushi"))
    await apply_merchant_enrichment(
        session,
        row,
        proposal(
            official_website={"url": OFFICIAL, "title": "t", "quote": "寿司大へようこそ"},
            listing_source={
                "url": LISTING,
                "title": "t",
                "quote": "Sushi Dai 東京都中央区築地5-2-1",
            },
        ),
        actor_id=None,
        origin=IMPORT,
        evidence=[],
        now=NOW,
    )
    by_url = {item.source_url: item for item in await sources(session, row)}
    assert by_url[OFFICIAL].claims_json == ["display_name", "official_website"]
    assert by_url[LISTING].claims_json == ["display_name", "address"]


async def test_apply_adds_categories_without_removing_existing_and_uses_origin_source(
    session: AsyncSession,
) -> None:
    row = merchant()
    sushi, seafood = category("sushi"), category("seafood")
    await seed(session, row, area(), sushi, seafood)
    await seed(
        session,
        FoodMerchantCategory(
            merchant_id=row.id,
            category_id=sushi.id,
            is_primary=True,
            display_order=1,
            source="seed",
        ),
    )
    outcome = await apply_merchant_enrichment(
        session,
        row,
        proposal(category_slugs=["sushi", "seafood"]),
        actor_id=None,
        origin=REVIEW,
        evidence=[],
        now=NOW,
    )
    assert outcome.categories_added == ["seafood"]
    links = list(
        (
            await session.scalars(
                select(FoodMerchantCategory)
                .where(FoodMerchantCategory.merchant_id == row.id)
                .order_by(FoodMerchantCategory.display_order)
            )
        ).all()
    )
    assert [(link.category_id, link.is_primary, link.source) for link in links] == [
        (sushi.id, True, "seed"),
        (seafood.id, False, "gemini"),
    ]


async def test_apply_area_requires_same_destination_active_and_sets_admin_source(
    session: AsyncSession,
) -> None:
    row = merchant()
    await seed(
        session,
        row,
        category("sushi"),
        area("osaka-namba", destination_id="osaka-kyoto"),
        area("tokyo-closed", is_active=False),
    )
    with pytest.raises(AppError) as mismatch:
        await apply_merchant_enrichment(
            session,
            row,
            proposal(area_slug="osaka-namba"),
            actor_id=None,
            origin=IMPORT,
            evidence=[],
        )
    assert mismatch.value.code == "merchant_area_destination_mismatch"
    with pytest.raises(AppError) as inactive:
        await apply_merchant_enrichment(
            session,
            row,
            proposal(area_slug="tokyo-closed"),
            actor_id=None,
            origin=IMPORT,
            evidence=[],
        )
    assert inactive.value.code == "food_area_inactive"
    with pytest.raises(AppError) as missing:
        await apply_merchant_enrichment(
            session,
            row,
            proposal(area_slug=None, category_slugs=["nope"]),
            actor_id=None,
            origin=IMPORT,
            evidence=[],
        )
    assert missing.value.code == "food_category_not_found"
    assert row.area_id is None


async def test_apply_place_id_only_when_empty_and_unowned(session: AsyncSession) -> None:
    owner = merchant(slug="tokyo-owner", google_place_id="ChIJowned0000000000000")
    row = merchant()
    await seed(session, owner, row, area(), category("sushi"))
    taken = await apply_merchant_enrichment(
        session,
        row,
        proposal(google_place_id="ChIJowned0000000000000"),
        actor_id=None,
        origin=IMPORT,
        evidence=[],
        now=NOW,
    )
    assert taken.skipped["google_place_id"] == "owned_by_other:tokyo-owner"
    assert row.google_place_id is None
    assert taken.applied["address"] == "東京都中央区築地5-2-1"  # the rest still landed

    fresh = await apply_merchant_enrichment(
        session,
        row,
        proposal(google_place_id="ChIJfresh00000000000000"),
        actor_id=None,
        origin=IMPORT,
        evidence=[],
        now=NOW,
    )
    assert fresh.applied == {"google_place_id": "ChIJfresh00000000000000"}
    assert row.google_place_id == "ChIJfresh00000000000000"
    repeat = await apply_merchant_enrichment(
        session,
        row,
        proposal(google_place_id="ChIJfresh00000000000000"),
        actor_id=None,
        origin=IMPORT,
        evidence=[],
        now=NOW,
    )
    assert repeat.skipped["google_place_id"] == "already_set"


async def test_apply_listing_requires_trusted_host(session: AsyncSession) -> None:
    row = merchant()
    await seed(session, row, area(), category("sushi"))
    with pytest.raises(AppError) as untrusted:
        await apply_merchant_enrichment(
            session,
            row,
            proposal(listing_source={"url": "https://tourism.example/shop", "title": "t"}),
            actor_id=None,
            origin=IMPORT,
            evidence=[],
        )
    assert untrusted.value.code == "catalog_source_untrusted"
    accepted = await apply_merchant_enrichment(
        session,
        row,
        proposal(listing_source={"url": "https://brand.example/branch", "title": "t"}),
        actor_id=None,
        origin=IMPORT,
        evidence=[],
        trusted_hosts={"brand.example"},
    )
    assert "https://brand.example/branch" in accepted.sources_added


async def test_apply_writes_one_audit_with_before_after_origin_evidence_and_none_when_unchanged(
    session: AsyncSession,
) -> None:
    row = merchant()
    actor = uuid4()
    await seed(session, row, area(), category("sushi"))
    evidence = [{"url": OFFICIAL, "role": "official_site", "observation": "address on page"}]
    await apply_merchant_enrichment(
        session, row, proposal(), actor_id=actor, origin=IMPORT, evidence=evidence, now=NOW
    )
    (audit,) = await audits(session)
    assert audit.actor_user_id == actor
    assert audit.target == f"food_merchant:{row.id}"
    assert audit.metadata_json["origin"] == {"kind": "json_import", "reference": "2026-09-12-pilot"}
    assert audit.metadata_json["before"]["address"] is None
    assert audit.metadata_json["after"]["address"] == "東京都中央区築地5-2-1"
    assert audit.metadata_json["after"]["category_slugs"] == ["sushi"]
    assert sorted(audit.metadata_json["after"]["source_urls"]) == sorted([OFFICIAL, LISTING])
    assert audit.metadata_json["evidence"] == evidence

    await apply_merchant_enrichment(
        session, row, proposal(), actor_id=actor, origin=IMPORT, evidence=evidence, now=NOW
    )
    assert len(await audits(session)) == 1


async def test_apply_never_writes_coordinates_status_or_verification_fields(
    session: AsyncSession,
) -> None:
    row = merchant()
    await seed(session, row, area(), category("sushi"))
    await apply_merchant_enrichment(
        session,
        row,
        proposal(google_place_id="ChIJfresh00000000000000"),
        actor_id=None,
        origin=REVIEW,
        evidence=[],
        now=NOW,
    )
    assert (row.latitude, row.longitude) == (None, None)
    assert row.coordinate_source_type is None and row.coordinate_source_url is None
    assert row.coordinate_verified_at is None
    assert row.naver_map_url is None
    assert row.map_match_status == "unverified"
    assert row.review_status == "pending" and row.is_active is False
    assert row.verified_at is None and row.verified_by_user_id is None


@pytest.mark.parametrize(
    "url",
    [
        "https://tabelog.com/tokyo/A1313/A131301/13002260/",
        "https://tabelog.com/en/tokyo/A1313/",
        "https://r.gnavi.co.jp/g123456/",
        "https://www.hotpepper.jp/strJ001/",
        "https://retty.me/area/PRE13/",
        "https://www.openrice.com/en/hongkong/r-x-r560646",
        "https://app.catchtable.co.kr/ct/shop/x",
        "https://www.tripadvisor.com.tw/Restaurant_Review-x",
        "https://www.yelp.com/biz/x",
        "https://www.facebook.com/x",
        "https://www.instagram.com/x/",
        "https://www.tablecheck.com/en/x/reserve",
        "https://inline.app/booking/x",
    ],
)
def test_platform_hosts_are_never_sources(url: str) -> None:
    assert is_platform_host(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://fb33500.gorp.jp/",
        "https://sushi-dai.example/",
        "https://www.gotokyo.org/en/spot/1",
    ],
)
def test_own_and_tourism_pages_are_not_platforms(url: str) -> None:
    assert not is_platform_host(url)


def test_reservation_platform_hosts_are_pinned_into_the_denylist() -> None:
    assert {
        "tablecheck.com",
        "catchtable.net",
        "eztable.com",
        "chope.co",
        "openrice.com",
    } <= PLATFORM_HOSTS
