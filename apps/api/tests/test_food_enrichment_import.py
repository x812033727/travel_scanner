"""The researched-batch importer: whole-file validation, fill-only-empty, honest dry runs."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.foods import enrichment_import
from app.foods.enrichment_import import (
    DATA_DIR,
    EnrichmentFileError,
    apply_enrichment_batch,
    apply_food_merchant_enrichment,
    export_food_merchant_worklist,
    load_enrichment_file,
    parse_enrichment_batch,
    researched_index,
    summarize,
)
from app.models import (
    AdminAuditLog,
    Base,
    FoodArea,
    FoodCategory,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantPlatformLink,
    FoodMerchantSource,
)

OFFICIAL = "https://sushi-dai.example/tsukiji"
LISTING = "https://www.gotokyo.org/en/spot/sushi-dai"
PLACE_ID = "ChIJN1t_tDeuEmsRUsoyG83frY4"
MAPS_URL = (
    "https://www.google.com/maps/place/Sushi+Dai/@35.66,139.77,17z/"
    f"data=!3m1!4b1!4m6!3m5!1s{PLACE_ID}!8m2!3d35.66!4d139.77!16s%2Fg%2F1?entry=ttu"
)
CHECKED_AT = "2026-09-12T09:41:00+00:00"


@pytest_asyncio.fixture
async def factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    try:
        yield maker
    finally:
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


async def seed(maker: async_sessionmaker[AsyncSession], *rows: Any) -> None:
    async with maker() as session:
        session.add_all(rows)
        await session.commit()


def taxonomy() -> list[Any]:
    return [
        FoodArea(
            slug="tokyo-tsukiji",
            destination_id="tokyo",
            country_code="JP",
            names_json={"en": "Tsukiji"},
            match_terms_json=["築地"],
            is_active=True,
        ),
        FoodCategory(slug="sushi", names_json={"en": "Sushi"}, is_active=True),
    ]


def record(row: FoodMerchant, **overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "merchant_id": str(row.id),
        "slug": row.slug,
        "name": row.name,
        "local_name": row.local_name,
        "country_code": row.country_code,
        "destination_id": row.destination_id,
        "outcome": "found",
        "checked_at": CHECKED_AT,
        "address_local": {
            "value": "東京都中央区築地5-2-1",
            "source_url": OFFICIAL,
            "quote": "住所 東京都中央区築地5-2-1",
        },
        "official_website": {
            "url": OFFICIAL,
            "title": "寿司大 築地",
            "quote": "寿司大 住所 東京都中央区築地5-2-1",
        },
        "listing_source": {
            "url": LISTING,
            "title": "Sushi Dai | GO TOKYO",
            "quote": "Sushi Dai, Tsukiji",
            "source_type": "official_tourism",
        },
        "google_maps_url": None,
        "google_place_id": PLACE_ID,
        "map_identity_observation": "Maps page title and Tsukiji address match the official site.",
        "area_slug": "tokyo-tsukiji",
        "category_slugs": ["sushi"],
        "naver": None,
        "reservation_batch_id": None,
        "evidence": [
            {"url": OFFICIAL, "role": "official_site", "observation": "Address and hours on page."}
        ],
        "notes": None,
    }
    values.update(overrides)
    return values


def batch(*records: dict[str, Any], **envelope: Any) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "batch_id": "2026-09-12-test",
        "researched_at": CHECKED_AT,
        "researched_by": "test",
        "method": "fixture",
        "rules": {"sources": "official or tourism only"},
        "records": list(records),
        **envelope,
    }


def write_batch(tmp_path: Path, document: dict[str, Any], name: str = "batch.json") -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    return path


def not_found(row: FoodMerchant, **overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "outcome": "not_found",
        "address_local": None,
        "official_website": None,
        "listing_source": None,
        "google_place_id": None,
        "map_identity_observation": None,
        "area_slug": None,
        "category_slugs": [],
        "evidence": [
            {
                "url": "https://html.duckduckgo.com/html/?q=x",
                "role": "search_result",
                "observation": "Only blogs.",
            }
        ],
    }
    values.update(overrides)
    return record(row, **values)


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        (
            {
                "official_website": {
                    "url": "https://tabelog.com/tokyo/A1313/x/",
                    "title": "t",
                    "quote": "q",
                },
                "address_local": None,
            },
            "聚合站",
        ),
        (
            {"official_website": {"url": "http://sushi-dai.example/", "title": "t", "quote": "q"}},
            "",
        ),
        (
            {"google_maps_url": "https://maps.app.goo.gl/abc123", "google_place_id": None},
            "short link",
        ),
        (
            {
                "listing_source": {
                    "url": "https://www.google.com/maps/place/x",
                    "title": "t",
                    "quote": "q",
                }
            },
            "",
        ),
        ({"official_website": {"url": OFFICIAL, "title": "t", "quote": "x" * 301}}, "300"),
        (
            {"address_local": {"value": "x", "source_url": "https://other.example/", "quote": "x"}},
            "address_local.source_url",
        ),
        ({"country_code": "KR", "destination_id": "seoul", "area_slug": None}, "naver"),
        ({"naver": {"outcome": "not_possible_in_pane"}}, "Korean"),
        ({"official_website": None, "listing_source": None, "address_local": None}, "found needs"),
        ({"google_place_id": None, "map_identity_observation": None}, "Google identity"),
        ({"google_place_id": "ChIJother0000000000000", "google_maps_url": MAPS_URL}, "disagrees"),
        ({"checked_at": "2026-09-12T09:41:00"}, "timezone"),
        ({"outcome": "surprising"}, ""),
        ({"latitude": 35.6}, ""),
        ({"area_slug": "osaka-namba"}, "destination"),
        ({"category_slugs": ["sushi", "sushi"]}, "repeats"),
        (
            {
                "outcome": "blocked_retry_later",
                "official_website": None,
                "listing_source": None,
                "address_local": None,
                "google_place_id": None,
                "map_identity_observation": None,
                "area_slug": None,
                "category_slugs": [],
            },
            "blocked",
        ),
    ],
)
def test_one_invalid_record_rejects_the_whole_file(overrides: dict[str, Any], message: str) -> None:
    good = merchant()
    bad = merchant(slug="tokyo-bad", id=uuid4())
    document = batch(record(good), record(bad, **overrides))
    with pytest.raises(EnrichmentFileError) as failure:
        parse_enrichment_batch(document)
    assert "records[1] (tokyo-bad)" in str(failure.value)
    assert message in str(failure.value)


def test_not_found_records_may_not_propose_and_ids_may_not_repeat() -> None:
    row = merchant()
    with pytest.raises(EnrichmentFileError, match="must not propose"):
        parse_enrichment_batch(batch(not_found(row, area_slug="tokyo-tsukiji")))
    with pytest.raises(EnrichmentFileError, match="repeated"):
        parse_enrichment_batch(batch(record(row), not_found(row)))
    parsed = parse_enrichment_batch(batch(not_found(row)))
    assert parsed.records[0].has_proposal is False


def test_place_id_is_derived_from_the_expanded_maps_url() -> None:
    row = merchant()
    parsed = parse_enrichment_batch(
        batch(record(row, google_maps_url=MAPS_URL, google_place_id=None))
    )
    assert parsed.records[0].google_place_id == PLACE_ID
    parsed = parse_enrichment_batch(
        batch(
            record(
                row,
                google_maps_url=f"https://www.google.com/maps/place/?q=place_id:{PLACE_ID}",
                google_place_id=None,
            )
        )
    )
    assert parsed.records[0].google_place_id == PLACE_ID


async def test_check_mode_validates_without_a_database(tmp_path: Path) -> None:
    row = merchant()
    path = write_batch(tmp_path, batch(record(row), not_found(merchant(slug="tokyo-two"))))
    report = await apply_food_merchant_enrichment(path, apply=False, check_only=True)
    assert report == {
        "batch_id": "2026-09-12-test",
        "valid": True,
        "records": 2,
        "research_outcomes": {"found": 1, "not_found": 1},
    }


async def test_dry_run_reports_would_enrich_and_writes_nothing_then_apply_writes(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    row = merchant()
    await seed(factory, row, *taxonomy())
    parsed = parse_enrichment_batch(batch(record(row)))
    async with factory() as session:
        (dry,) = await apply_enrichment_batch(session, parsed, apply=False)
    assert dry.action == "would_enrich"
    assert dry.filled == (
        "address",
        "official_website_url",
        "area_slug",
        "google_place_id",
        "sources",
        "categories",
    )
    assert dry.skipped == {}
    async with factory() as session:
        fresh = await session.get(FoodMerchant, row.id)
        assert fresh is not None and fresh.address is None and fresh.google_place_id is None
        assert (await session.scalars(select(AdminAuditLog))).all() == []
        (applied,) = await apply_enrichment_batch(session, parsed, apply=True)
    assert applied.action == "enriched" and applied.filled == dry.filled
    async with factory() as session:
        fresh = await session.get(FoodMerchant, row.id)
        assert fresh is not None
        assert fresh.address == "東京都中央区築地5-2-1"
        assert fresh.official_website_url == OFFICIAL
        assert fresh.google_place_id == PLACE_ID
        assert fresh.area_id is not None and fresh.area_source == "admin"
        sources = (
            await session.scalars(
                select(FoodMerchantSource)
                .where(FoodMerchantSource.merchant_id == row.id)
                .order_by(FoodMerchantSource.source_url)
            )
        ).all()
        assert [(s.source_scope, s.source_url, s.claims_json) for s in sources] == [
            ("merchant_website", OFFICIAL, ["display_name", "official_website", "address"]),
            ("merchant_listing", LISTING, ["display_name"]),
        ]
        links = (
            await session.scalars(
                select(FoodMerchantCategory).where(FoodMerchantCategory.merchant_id == row.id)
            )
        ).all()
        assert [(link.is_primary, link.source) for link in links] == [(True, "admin")]
        (audit,) = (await session.scalars(select(AdminAuditLog))).all()
        assert audit.action == "food_merchant_enriched"
        assert audit.metadata_json["origin"] == {
            "kind": "json_import",
            "reference": "2026-09-12-test",
        }
        assert audit.metadata_json["evidence"][0]["role"] == "official_site"
        assert audit.metadata_json["evidence"][0]["batch_id"] == "2026-09-12-test"
        assert audit.metadata_json["evidence"][-1]["role"] == "map_identity"
        # A second run finds nothing to write and adds no audit row.
        (again,) = await apply_enrichment_batch(session, parsed, apply=True)
        assert again.action == "unchanged"
        assert len((await session.scalars(select(AdminAuditLog))).all()) == 1


async def test_fill_only_empty_scalars_and_place_id_ownership_are_reported(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    owner = merchant(slug="tokyo-owner", google_place_id=PLACE_ID)
    row = merchant(address="既有地址")
    await seed(factory, owner, row, *taxonomy())
    parsed = parse_enrichment_batch(batch(record(row)))
    async with factory() as session:
        (outcome,) = await apply_enrichment_batch(session, parsed, apply=True)
        assert outcome.action == "enriched"
        assert outcome.skipped == {
            "address": "already_set",
            "google_place_id": "owned_by_other:tokyo-owner",
        }
        assert "address" not in outcome.filled and "google_place_id" not in outcome.filled
        fresh = await session.get(FoodMerchant, row.id)
        assert fresh is not None and fresh.address == "既有地址" and fresh.google_place_id is None
        assert fresh.official_website_url == OFFICIAL


async def test_kr_records_carry_naver_into_the_audit_but_never_into_the_row(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    row = merchant(
        slug="seoul-hani", destination_id="seoul", country_code="KR", local_name="하니칼국수"
    )
    await seed(factory, row)
    parsed = parse_enrichment_batch(
        batch(
            record(
                row,
                google_place_id=None,
                map_identity_observation=None,
                listing_source=None,
                address_local=None,
                area_slug=None,
                category_slugs=[],
                official_website={
                    "url": "https://hani.example/",
                    "title": "하니칼국수",
                    "quote": "하니칼국수",
                },
                naver={
                    "outcome": "not_possible_in_pane",
                    "url": None,
                    "note": "pane refuses map.naver.com",
                },
            )
        )
    )
    async with factory() as session:
        (outcome,) = await apply_enrichment_batch(session, parsed, apply=True)
        assert outcome.action == "enriched"
        fresh = await session.get(FoodMerchant, row.id)
        assert fresh is not None and fresh.naver_map_url is None
        assert fresh.official_website_url == "https://hani.example/"
        (audit,) = (await session.scalars(select(AdminAuditLog))).all()
        assert audit.metadata_json["evidence"][-1] == {
            "role": "naver",
            "outcome": "not_possible_in_pane",
            "url": None,
            "note": "pane refuses map.naver.com",
            "batch_id": "2026-09-12-test",
        }


async def test_never_writes_coordinates_map_status_or_review_state(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    row = merchant()
    await seed(factory, row, *taxonomy())
    async with factory() as session:
        await apply_enrichment_batch(
            session, parse_enrichment_batch(batch(record(row))), apply=True
        )
        fresh = await session.get(FoodMerchant, row.id)
        assert fresh is not None
        assert (fresh.latitude, fresh.longitude, fresh.coordinate_source_type) == (None, None, None)
        assert fresh.map_match_status == "unverified"
        assert fresh.review_status == "pending" and fresh.is_active is False
        assert fresh.verified_at is None


async def test_not_found_records_are_noted_once_and_blocked_ones_stay_open(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    row = merchant()
    blocked_row = merchant(slug="tokyo-blocked")
    await seed(factory, row, blocked_row)
    parsed = parse_enrichment_batch(
        batch(
            not_found(row),
            not_found(
                blocked_row,
                outcome="blocked_retry_later",
                evidence=[{"url": OFFICIAL, "role": "blocked", "observation": "Cloudflare wall."}],
            ),
        )
    )
    async with factory() as session:
        dry = await apply_enrichment_batch(session, parsed, apply=False)
        assert [item.action for item in dry] == ["would_note", "would_note"]
        assert (await session.scalars(select(AdminAuditLog))).all() == []
        applied = await apply_enrichment_batch(session, parsed, apply=True)
        assert [item.action for item in applied] == ["noted", "noted"]
        again = await apply_enrichment_batch(session, parsed, apply=True)
        assert [item.action for item in again] == ["already_noted", "already_noted"]
        audits = (await session.scalars(select(AdminAuditLog))).all()
        assert len(audits) == 2
        assert {a.action for a in audits} == {"food_merchant.cli_enrichment_researched"}
        assert audits[0].metadata_json["batch_id"] == "2026-09-12-test"
        fresh = await session.get(FoodMerchant, row.id)
        assert fresh is not None and fresh.address is None


async def test_slug_mismatch_missing_merchant_rejected_rows_and_bad_taxonomy_are_skipped(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    renamed = merchant(slug="tokyo-renamed")
    rejected = merchant(slug="tokyo-rejected", review_status="rejected")
    no_area = merchant(slug="tokyo-no-area")
    await seed(factory, renamed, rejected, no_area, FoodCategory(slug="sushi", names_json={}))
    parsed = parse_enrichment_batch(
        batch(
            record(renamed, slug="tokyo-old-slug"),
            record(merchant(slug="tokyo-ghost")),
            record(rejected),
            record(no_area),
        )
    )
    async with factory() as session:
        outcomes = await apply_enrichment_batch(session, parsed, apply=True)
    assert [(o.action, o.detail) for o in outcomes] == [
        ("skipped_slug_mismatch", "tokyo-renamed"),
        ("skipped_missing_merchant", None),
        ("skipped_not_enrichable", "rejected"),
        ("skipped_taxonomy", "food_area_not_found"),
    ]
    async with factory() as session:
        fresh = await session.get(FoodMerchant, no_area.id)
        assert fresh is not None and fresh.address is None
    summary = summarize(parsed, outcomes, apply=True)
    assert summary["actions"] == {
        "skipped_missing_merchant": 1,
        "skipped_not_enrichable": 1,
        "skipped_slug_mismatch": 1,
        "skipped_taxonomy": 1,
    }
    assert [entry["slug"] for entry in summary["skipped"]] == [
        "tokyo-old-slug",
        "tokyo-ghost",
        "tokyo-rejected",
        "tokyo-no-area",
    ]


async def test_limit_and_slug_filters_and_summary_counts(
    factory: async_sessionmaker[AsyncSession],
) -> None:
    first = merchant(slug="tokyo-first")
    second = merchant(slug="tokyo-second")
    await seed(factory, first, second, *taxonomy())
    parsed = parse_enrichment_batch(
        batch(record(first), record(second, google_place_id="ChIJsecond00000000000"))
    )
    async with factory() as session:
        limited = await apply_enrichment_batch(session, parsed, apply=False, limit=1)
        assert [o.slug for o in limited] == ["tokyo-first"]
        chosen = await apply_enrichment_batch(session, parsed, apply=False, slugs=["tokyo-second"])
        assert [o.slug for o in chosen] == ["tokyo-second"]
        outcomes = await apply_enrichment_batch(session, parsed, apply=False)
    summary = summarize(parsed, outcomes, apply=False)
    assert summary["applied"] is False and summary["processed"] == 2 and summary["records"] == 2
    assert summary["actions"] == {"would_enrich": 2}
    assert summary["research_outcomes"] == {"found": 2}
    assert summary["fields"] == {
        "address": 2,
        "area_slug": 2,
        "categories": 2,
        "google_place_id": 2,
        "official_website_url": 2,
        "sources": 2,
    }
    assert summary["field_skips"] == {} and summary["skipped"] == []


async def test_worklist_export_shape_and_researched_marker(
    factory: async_sessionmaker[AsyncSession], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    settled = merchant(slug="tokyo-settled")
    blocked = merchant(slug="tokyo-blocked")
    untouched = merchant(slug="tokyo-untouched", google_place_id="ChIJuntouched000000000")
    approved = merchant(slug="tokyo-approved", review_status="approved")
    area, category = taxonomy()
    await seed(factory, settled, blocked, untouched, approved, area, category)
    async with factory() as session:
        untouched_row = await session.get(FoodMerchant, untouched.id)
        assert untouched_row is not None
        untouched_row.area_id = area.id
        session.add_all(
            [
                FoodMerchantCategory(
                    merchant_id=untouched.id, category_id=category.id, is_primary=True
                ),
                FoodMerchantSource(
                    merchant_id=untouched.id,
                    source_type="official_tourism",
                    source_scope="destination_context",
                    source_title="Tokyo food guide",
                    source_url="https://www.gotokyo.org/en/food",
                    claims_json=[],
                ),
                FoodMerchantPlatformLink(
                    merchant_id=untouched.id,
                    provider="tablecheck",
                    status="ambiguous",
                    checked_at=datetime.now(UTC),
                ),
            ]
        )
        await session.commit()
    write_batch(
        tmp_path,
        batch(
            not_found(settled),
            not_found(
                blocked,
                outcome="blocked_retry_later",
                evidence=[{"url": OFFICIAL, "role": "blocked", "observation": "wall"}],
            ),
        ),
        name="2026-09-12-a.json",
    )
    monkeypatch.setattr(enrichment_import, "SessionFactory", factory)
    assert set(researched_index(tmp_path)) == {settled.id, blocked.id}

    worklist = await export_food_merchant_worklist(data_dir=tmp_path)
    assert worklist["status"] == "pending" and worklist["count"] == 2
    assert [row["slug"] for row in worklist["merchants"]] == ["tokyo-blocked", "tokyo-untouched"]
    blocked_row, untouched_export = worklist["merchants"]
    assert blocked_row["researched"]["outcome"] == "blocked_retry_later"
    assert untouched_export["researched"] is None
    assert untouched_export["area_slug"] == "tokyo-tsukiji"
    assert untouched_export["category_slugs"] == ["sushi"]
    assert untouched_export["google_place_id"] == "ChIJuntouched000000000"
    assert untouched_export["sources"][0]["scope"] == "destination_context"
    assert untouched_export["platform_links"] == [
        {"provider": "tablecheck", "status": "ambiguous", "canonical_url": None}
    ]
    assert untouched_export["has_coordinates"] is False
    assert worklist["categories"] == [{"slug": "sushi", "names": {"en": "Sushi"}}]
    assert worklist["areas_by_destination"] == {
        "tokyo": [{"slug": "tokyo-tsukiji", "names": {"en": "Tsukiji"}, "match_terms": ["築地"]}]
    }

    everything = await export_food_merchant_worklist(
        status="all", include_researched=True, data_dir=tmp_path
    )
    assert [row["slug"] for row in everything["merchants"]] == [
        "tokyo-approved",
        "tokyo-blocked",
        "tokyo-settled",
        "tokyo-untouched",
    ]
    only_seoul = await export_food_merchant_worklist(destination_ids=["Seoul"], data_dir=tmp_path)
    assert only_seoul["count"] == 0 and only_seoul["areas_by_destination"] == {}


def test_committed_enrichment_files_are_valid() -> None:
    files = sorted(DATA_DIR.glob("*.json"))
    assert files, "the data directory must carry at least the skeleton batch"
    for path in files:
        parsed = load_enrichment_file(path)
        assert parsed.schema_version == 1
        assert parsed.rules["sources"]
    assert UUID(int=0)  # keep the import honest for the type checker
