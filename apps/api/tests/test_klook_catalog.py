from __future__ import annotations

import json
from collections.abc import AsyncIterator
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import httpx
import pytest
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings
from app.db import Base
from app.models import (
    AdminAuditLog,
    HotelBookingOption,
    TravelServiceBrand,
    TravelServiceOffer,
    TravelServiceProduct,
)
from app.travel_services import klook_catalog
from app.travel_services.klook_catalog import (
    CatalogEntry,
    CatalogManifest,
    default_manifest_path,
    import_catalog,
    load_manifest,
)


@pytest.fixture
def manifest() -> CatalogManifest:
    return load_manifest(default_manifest_path())


@pytest.fixture
def settings() -> Settings:
    # Fixture-only enrollment ID. No environment credentials or provider access.
    return Settings(_env_file=None, klook_affiliate_id="123456", klook_enabled=False)


@pytest.fixture
async def session(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[AsyncSession]:
    monkeypatch.setattr(
        httpx.AsyncClient, "request", AsyncMock(side_effect=AssertionError("No provider calls"))
    )
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = [
        model.__table__
        for model in (
            TravelServiceProduct,
            HotelBookingOption,
            TravelServiceBrand,
            TravelServiceOffer,
            AdminAuditLog,
        )
    ]
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    async with async_sessionmaker(engine, expire_on_commit=False)() as value:
        yield value
    await engine.dispose()


async def add_brand(
    session: AsyncSession,
    settings: Settings,
    *,
    channel: str = "klook_direct",
    project_id: str | None = None,
) -> TravelServiceBrand:
    brand = TravelServiceBrand(
        id=uuid4(),
        channel=channel,
        project_id=project_id or settings.klook_affiliate_id,
        code="klook",
        approval="pending",
        enabled=False,
        version=4,
        evidence_url="https://affiliate.klook.com/",
        verified_at=None,
    )
    session.add(brand)
    await session.commit()
    return brand


async def counts(session: AsyncSession) -> tuple[int, ...]:
    return tuple(
        [
            int(await session.scalar(select(func.count()).select_from(model)) or 0)
            for model in (
                TravelServiceProduct,
                TravelServiceOffer,
                HotelBookingOption,
                AdminAuditLog,
            )
        ]
    )


def snapshot(row: Any) -> dict[str, Any]:
    values = {column.name: deepcopy(getattr(row, column.name)) for column in row.__table__.columns}
    # SQLite round-trips timezone-aware UTC columns as naive datetimes.
    return {
        key: value.replace(tzinfo=UTC) if isinstance(value, datetime) else value
        for key, value in values.items()
    }


def test_real_manifest_has_unique_sourced_products_and_truthful_scope(
    manifest: CatalogManifest,
) -> None:
    assert len(manifest.entries) == 10
    assert {row.product_id for row in manifest.entries} == {
        "134125",
        "2274",
        "3217",
        "18203",
        "8962",
        "4158",
        "74132",
        "1244",
        "79844",
        "1478",
    }
    assert all(row.evidence.url == row.source_url for row in manifest.entries)
    shared = [row for row in manifest.entries if row.other_applicable_cities]
    assert {row.product_id for row in shared} == {"3217", "18203"}
    assert all(
        row.destination_id == "osaka" and row.other_applicable_cities == ["kyoto"] for row in shared
    )
    for entry in manifest.entries:
        data = entry.product_input()
        assert data.facts.reference_price is None
        assert data.facts.duration_minutes is None
        assert data.facts.available_start is None
        if entry.kind == "transfer":
            assert data.facts.direction == "arrival"
    seoul = next(entry for entry in manifest.entries if entry.product_id == "4158")
    assert seoul.available_directions == ["arrival", "departure"]
    hotel = manifest.hotel_links[0]
    assert hotel.existing_source_key == "editorial:tokyo:gracery-shinjuku"
    assert hotel.evidence_method == "browser_name_and_address_match"
    assert hotel.official_identity_url == "https://gracery.com/shinjuku/access/"
    assert "/hotels/detail/285841-" in hotel.source_url
    assert {item.product_id for item in manifest.candidates} == {"104418", "695"}


@pytest.mark.parametrize(
    "url",
    [
        "http://www.klook.com/activity/2274-narita/",
        "https://evil.example/activity/2274-narita/",
        "https://www.klook.com.evil.example/activity/2274-narita/",
        "https://www.klook.com/city/2274/",
        "https://www.klook.com/airport-transfers/service/nrt-narita-international-airport/",
        "https://www.klook.com/activity/2274-narita/?aid=123456",
        "https://www.klook.com/activity/2274-narita/?aff_adid=1",
        "https://www.klook.com/activity/2274-narita/#section",
        "https://www.klook.com/activity/%32%32%37%34-narita/",
        "https://www.klook.com/activity/2274-narita/redirect",
        "https://www.klook.com/activity/999-wrong-identity/",
        "https://www.klook.com/hotels/2274",
    ],
)
def test_manifest_rejects_non_exact_or_tracked_product_urls(
    manifest: CatalogManifest,
    url: str,
) -> None:
    row = manifest.entries[1].model_dump(mode="json")
    row["source_url"] = url
    row["evidence"]["url"] = url
    with pytest.raises(ValidationError):
        CatalogEntry.model_validate(row)


def test_manifest_rejects_duplicate_id_wrong_airport_and_unrelated_evidence(
    manifest: CatalogManifest,
) -> None:
    duplicate = manifest.model_dump(mode="json")
    duplicate["entries"].append(duplicate["entries"][0])
    with pytest.raises(ValidationError, match="One manifest record"):
        CatalogManifest.model_validate(duplicate)
    row = manifest.entries[1].model_dump(mode="json")
    row["airport"] = "KIX"
    with pytest.raises(ValidationError, match="Transfer requires"):
        CatalogEntry.model_validate(row)
    row = manifest.entries[0].model_dump(mode="json")
    row["evidence"]["url"] = "https://www.klook.com/"
    with pytest.raises(ValidationError, match="Source evidence"):
        CatalogEntry.model_validate(row)


async def test_preview_is_default_and_never_mutates(
    session: AsyncSession,
    manifest: CatalogManifest,
    settings: Settings,
) -> None:
    brand = await add_brand(session, settings)
    before = snapshot(brand)
    report = await import_catalog(session, manifest, settings)
    assert not report.apply_requested and not report.applied
    assert not report.blockers
    assert len(report.rows) == 10
    assert all(row.product == row.offer == "create" for row in report.rows)
    assert report.candidate_only_count == 2
    assert report.hotels[0].product == "skip"
    assert await counts(session) == (0, 0, 0, 0)
    assert not session.new and not session.dirty
    assert snapshot(brand) == before


async def test_preview_never_autoflushes_and_apply_rejects_dirty_caller_session(
    session: AsyncSession,
    manifest: CatalogManifest,
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    brand = await add_brand(session, settings)
    brand.enabled = True
    flush = AsyncMock(side_effect=AssertionError("Preview cannot flush caller changes"))
    monkeypatch.setattr(session, "flush", flush)
    report = await import_catalog(session, manifest, settings)
    assert not report.applied and not report.blockers
    flush.assert_not_called()
    apply = await import_catalog(session, manifest, settings, apply=True)
    assert not apply.applied and apply.blockers == ["clean_session_required"]
    flush.assert_not_called()
    assert brand in session.dirty
    await session.rollback()


async def test_apply_and_replay_create_pending_once_without_enabling_anything(
    session: AsyncSession,
    manifest: CatalogManifest,
    settings: Settings,
) -> None:
    brand = await add_brand(session, settings)
    before = snapshot(brand)
    report = await import_catalog(session, manifest, settings, apply=True)
    assert report.applied and not report.blockers
    await session.commit()
    assert await counts(session) == (10, 10, 0, 10)
    products = list(await session.scalars(select(TravelServiceProduct)))
    offers = list(await session.scalars(select(TravelServiceOffer)))
    assert all(p.status == "pending" and p.version == 1 and p.verified_at is None for p in products)
    assert all(o.status == "pending" and o.version == 1 and o.verified_at is None for o in offers)
    assert all(o.static_url is None and o.verification_context is None for o in offers)
    assert all("?" not in o.target_url for o in offers)
    logs = list(await session.scalars(select(AdminAuditLog)))
    assert all(log.actor_user_id is None for log in logs)
    assert all(
        log.metadata_json["evidence"]["url"] == log.metadata_json["source_url"] for log in logs
    )
    assert snapshot(brand) == before
    replay = await import_catalog(session, manifest, settings, apply=True)
    await session.commit()
    assert replay.applied and not replay.blockers
    assert all(row.product == row.offer == "preserve" for row in replay.rows)
    assert await counts(session) == (10, 10, 0, 10)
    assert snapshot(brand) == before


async def test_existing_published_core_disabled_offer_and_other_providers_are_preserved(
    session: AsyncSession,
    manifest: CatalogManifest,
    settings: Settings,
) -> None:
    brand = await add_brand(session, settings)
    tp = await add_brand(session, settings, channel="travelpayouts", project_id="tp-project")
    entry = manifest.entries[0]
    product = TravelServiceProduct(
        id=uuid4(),
        **entry.product_input().model_dump(mode="json"),
        status="approved",
        version=9,
        verified_at=datetime(2026, 9, 8, tzinfo=UTC),
    )
    product.title = "User-reviewed localized title"
    product.facts = {"meeting_point": "Manually reviewed meeting point", "duration_minutes": 200}
    hotel = TravelServiceProduct(
        id=uuid4(),
        source_key="editorial:tokyo:gracery-shinjuku",
        kind="hotel",
        destination_id="tokyo",
        title="Reviewed hotel",
        source_url="https://gracery.com/shinjuku/",
        status="approved",
        version=12,
        facts={"manual_fact": "retained"},
        names_json={},
    )
    session.add_all([product, hotel])
    await session.flush()
    direct = TravelServiceOffer(
        product_id=product.id,
        brand_id=brand.id,
        target_url=entry.source_url,
        scope="product",
        status="disabled",
        version=7,
    )
    tp_offer = TravelServiceOffer(
        product_id=product.id,
        brand_id=tp.id,
        target_url=entry.source_url,
        static_url="https://klook.tpx.gr/existing",
        status="approved",
        version=5,
    )
    option = HotelBookingOption(
        product_id=hotel.id,
        provider="booking",
        url="https://www.booking.com/hotel/jp/reviewed.html",
        evidence_url=hotel.source_url,
        status="approved",
        discovery_status="found",
        version=6,
    )
    session.add_all([direct, tp_offer, option])
    await session.commit()
    rows = [brand, tp, product, hotel, direct, tp_offer, option]
    before = [snapshot(row) for row in rows]
    report = await import_catalog(session, manifest, settings, apply=True)
    await session.commit()
    assert report.applied
    assert report.rows[0].product == report.rows[0].offer == "preserve"
    for row in rows:
        await session.refresh(row)
    assert [snapshot(row) for row in rows] == before
    assert await counts(session) == (11, 12, 2, 10)
    new_option = await session.scalar(
        select(HotelBookingOption).where(HotelBookingOption.provider == "klook")
    )
    assert new_option and new_option.status == "pending"
    assert new_option.product_id == hotel.id
    assert new_option.url == manifest.hotel_links[0].source_url
    assert new_option.evidence_url == manifest.hotel_links[0].official_identity_url
    new_offer = await session.scalar(
        select(TravelServiceOffer).where(
            TravelServiceOffer.product_id == hotel.id,
            TravelServiceOffer.brand_id == brand.id,
        )
    )
    assert new_offer and new_offer.target_url == new_option.url and new_offer.status == "pending"
    assert new_option.verified_at is None and new_option.health_status == "unchecked"
    before_replay = await counts(session)
    replay = await import_catalog(session, manifest, settings, apply=True)
    await session.commit()
    assert replay.hotels[0].option == replay.hotels[0].offer == "preserve"
    assert await counts(session) == before_replay


@pytest.mark.parametrize(
    "conflict", ["same_provider", "identity_elsewhere", "wrong_city", "wrong_kind"]
)
async def test_hotel_existing_options_and_conflicting_identity_never_overwritten(
    session: AsyncSession,
    manifest: CatalogManifest,
    settings: Settings,
    conflict: str,
) -> None:
    await add_brand(session, settings)
    evidence = manifest.hotel_links[0]
    hotel = TravelServiceProduct(
        id=uuid4(),
        source_key=evidence.existing_source_key,
        kind="tour" if conflict == "wrong_kind" else "hotel",
        destination_id="osaka" if conflict == "wrong_city" else "tokyo",
        title="Existing curated hotel",
        source_url=evidence.official_identity_url,
        status="approved",
        version=6,
        facts={},
        names_json={},
    )
    session.add(hotel)
    await session.flush()
    if conflict in ("same_provider", "identity_elsewhere"):
        other_id = hotel.id
        if conflict == "identity_elsewhere":
            other = TravelServiceProduct(
                id=uuid4(),
                source_key="other-hotel",
                kind="hotel",
                destination_id="tokyo",
                title="Another hotel",
                source_url="https://hotel.example.com/",
                status="approved",
            )
            session.add(other)
            await session.flush()
            other_id = other.id
        session.add(
            HotelBookingOption(
                product_id=other_id,
                provider="klook",
                url="https://www.klook.com/zh-TW/hotels/99999"
                if conflict == "same_provider"
                else evidence.source_url,
                property_id="99999" if conflict == "same_provider" else evidence.product_id,
                evidence_url=evidence.official_identity_url,
                status="disabled",
                version=7,
            )
        )
    await session.commit()
    before = await counts(session)
    options_before = [snapshot(row) for row in await session.scalars(select(HotelBookingOption))]
    report = await import_catalog(session, manifest, settings, apply=True)
    assert not report.applied and report.hotels[0].product == "conflict"
    assert await counts(session) == before
    assert [
        snapshot(row) for row in await session.scalars(select(HotelBookingOption))
    ] == options_before


async def test_same_existing_disabled_hotel_option_is_not_reset(
    session: AsyncSession,
    manifest: CatalogManifest,
    settings: Settings,
) -> None:
    await add_brand(session, settings)
    evidence = manifest.hotel_links[0]
    hotel = TravelServiceProduct(
        id=uuid4(),
        source_key=evidence.existing_source_key,
        kind="hotel",
        destination_id="tokyo",
        title=evidence.title,
        source_url=evidence.official_identity_url,
        status="disabled",
        version=8,
    )
    session.add(hotel)
    await session.flush()
    option = HotelBookingOption(
        product_id=hotel.id,
        **evidence.option_input().model_dump(),
        status="disabled",
        version=9,
        health_status="unavailable",
    )
    session.add(option)
    await session.commit()
    before = snapshot(option)
    report = await import_catalog(session, manifest, settings, apply=True)
    await session.commit()
    assert report.applied and report.hotels[0].option == "preserve"
    assert report.hotels[0].offer == "create"
    await session.refresh(option)
    assert snapshot(option) == before


async def test_adds_only_missing_direct_offer_to_compatible_product(
    session: AsyncSession,
    manifest: CatalogManifest,
    settings: Settings,
) -> None:
    await add_brand(session, settings)
    entry = manifest.entries[0]
    product = TravelServiceProduct(
        id=uuid4(),
        **entry.product_input().model_dump(mode="json"),
        status="disabled",
        version=8,
    )
    session.add(product)
    await session.commit()
    before = snapshot(product)
    report = await import_catalog(session, manifest, settings, apply=True)
    await session.commit()
    assert report.rows[0].product == "preserve" and report.rows[0].offer == "create"
    await session.refresh(product)
    assert snapshot(product) == before
    assert await counts(session) == (10, 10, 0, 10)


@pytest.mark.parametrize("conflict", ["source_key", "different_key_same_id", "direct_offer"])
async def test_conflicts_block_entire_apply_without_partial_additions(
    session: AsyncSession,
    manifest: CatalogManifest,
    settings: Settings,
    conflict: str,
) -> None:
    brand = await add_brand(session, settings)
    entry = manifest.entries[0]
    data = entry.product_input().model_dump(mode="json")
    if conflict == "source_key":
        data["destination_id"] = "busan"
    elif conflict == "different_key_same_id":
        data["source_key"] = "editorial:existing-fuji-tour"
        data["source_url"] = "https://www.klook.com/zh-TW/activity/134125-another-locale/"
    else:
        data["source_key"] = "another-product"
        data["source_url"] = "https://www.example.com/other-product"
    product = TravelServiceProduct(id=uuid4(), **data, status="approved", version=3)
    session.add(product)
    await session.flush()
    if conflict == "direct_offer":
        session.add(
            TravelServiceOffer(
                product_id=product.id,
                brand_id=brand.id,
                target_url=entry.source_url,
                status="approved",
                scope="product",
                version=4,
            )
        )
    await session.commit()
    before = await counts(session)
    preview = await import_catalog(session, manifest, settings)
    assert preview.rows[0].product == "conflict"
    report = await import_catalog(session, manifest, settings, apply=True)
    assert not report.applied
    assert "catalog_identity_conflict" in report.blockers
    assert await counts(session) == before
    assert not session.new and not session.dirty


@pytest.mark.parametrize(
    "case", ["missing_aid", "invalid_aid", "missing_brand", "other_account", "tp_only"]
)
async def test_missing_or_wrong_enrollment_blocks_apply(
    session: AsyncSession,
    manifest: CatalogManifest,
    settings: Settings,
    case: str,
) -> None:
    if case == "missing_aid":
        settings = settings.model_copy(update={"klook_affiliate_id": None})
    elif case == "invalid_aid":
        settings = settings.model_copy(update={"klook_affiliate_id": "not-numeric"})
    elif case == "other_account":
        await add_brand(session, settings, project_id="999999")
    elif case == "tp_only":
        await add_brand(session, settings, channel="travelpayouts")
    report = await import_catalog(session, manifest, settings, apply=True)
    assert report.blockers and not report.applied
    assert all(row.offer == "blocked" for row in report.rows)
    assert await counts(session) == (0, 0, 0, 0)


async def test_unique_race_rolls_back_whole_batch_savepoint(
    session: AsyncSession,
    manifest: CatalogManifest,
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    await add_brand(session, settings)
    original_flush = session.flush
    calls = 0

    async def raced_flush(*args: Any, **kwargs: Any) -> None:
        nonlocal calls
        calls += 1
        if calls == 4:
            raise IntegrityError("not exposed", {}, Exception("fixture-only conflict"))
        await original_flush(*args, **kwargs)

    monkeypatch.setattr(session, "flush", raced_flush)
    report = await import_catalog(session, manifest, settings, apply=True)
    assert not report.applied
    assert report.blockers == ["concurrent_catalog_change_retry_preview"]
    assert await counts(session) == (0, 0, 0, 0)


@pytest.mark.parametrize("arguments,expected", [([], False), (["--apply"], True)])
def test_cli_requires_explicit_apply(
    monkeypatch: pytest.MonkeyPatch,
    arguments: list[str],
    expected: bool,
) -> None:
    runner = AsyncMock(return_value=0)
    monkeypatch.setattr(klook_catalog, "_run", runner)
    assert klook_catalog.main(arguments) == 0
    assert runner.call_args.args[0].apply is expected


def test_cli_error_does_not_expose_database_or_manifest_exception(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    runner = AsyncMock(side_effect=ValueError("secret credentials must never print"))
    monkeypatch.setattr(klook_catalog, "_run", runner)
    assert klook_catalog.main([]) == 2
    output = capsys.readouterr().out
    assert "secret" not in output and "credentials" not in output
    assert json.loads(output) == {"applied": False, "error": "catalog_validation_or_database_error"}
