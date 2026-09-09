import asyncio
import os
from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy import event, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings
from app.db import Base
from app.models import (
    AdminAuditLog,
    AffiliateClick,
    DestinationAffiliateOffer,
    HotelBookingClick,
    HotelBookingOption,
    TravelServiceBrand,
    TravelServiceConfig,
    TravelServiceImport,
    TravelServiceOffer,
    TravelServiceProduct,
    TripServiceSelection,
    User,
)
from app.problems import AppError
from app.travel_services import admin, hotel_admin
from app.travel_services.imports import commit_import, parse_csv, upsert_product
from app.travel_services.schemas import ConfigInput, CsvInput, HotelConfigPatch, ProductInput


@pytest.fixture
async def session(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite://")

    @event.listens_for(engine.sync_engine, "connect")
    def sqlite_advisory_stub(connection: Any, _record: Any) -> None:
        # SQLite fixture tests exercise merge/validation only. The PostgreSQL
        # regression below checks actual cross-connection lock serialization.
        connection.create_function("pg_advisory_xact_lock", 1, lambda _key: 0)

    tables = [
        model.__table__
        for model in (
            TravelServiceProduct,
            HotelBookingOption,
            TravelServiceBrand,
            TravelServiceOffer,
            DestinationAffiliateOffer,
            TravelServiceConfig,
            TravelServiceImport,
            AdminAuditLog,
            AffiliateClick,
            HotelBookingClick,
            TripServiceSelection,
        )
    ]
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    settings = Settings(travelpayouts_project_id="hotel-test")
    monkeypatch.setattr(admin, "load_runtime_settings", AsyncMock(return_value=settings))
    monkeypatch.setattr(hotel_admin, "load_runtime_settings", AsyncMock(return_value=settings))
    async with async_sessionmaker(engine, expire_on_commit=False)() as value:
        yield value
    await engine.dispose()


def actor() -> User:
    return User(id=uuid4(), email="admin@example.com")


def product(key: str, kind: str = "hotel", status: str = "pending") -> TravelServiceProduct:
    return TravelServiceProduct(
        source_key=key,
        kind=kind,
        destination_id="tokyo",
        title=key,
        source_url="https://www.example.com/place",
        facts={},
        names_json={},
        status=status,
    )


def csv_row(key: str = "hotel-one", kind: str = "hotel") -> str:
    return "source_key,kind,destination_id,title,source_url\n" + (
        f"{key},{kind},tokyo,Example,https://www.example.com/place\n"
    )


async def test_hotel_patch_preserves_other_domains_and_omitted_policies(
    session: AsyncSession,
) -> None:
    original = {
        "public_enabled": False,
        "enabled_kinds": ["tour", "esim"],
        "enabled_destinations": ["tokyo"],
        "airalo_feed_enabled": True,
        "direct_hotel_links_enabled": False,
        "hotel_quote_policies": {"agoda": {"enabled": False, "daily_limit": 42}},
        "future_shared_setting": {"keep": True},
    }
    row = TravelServiceConfig(id=1, version=7, data=original)
    session.add(row)
    await session.commit()
    result = await hotel_admin.patch_config(
        HotelConfigPatch(
            version=7,
            hotel_enabled=True,
            direct_hotel_links_enabled=True,
            hotel_quote_policies={"booking": {"daily_limit": 12}},
        ),
        actor(),
        session,
    )
    assert result == {"version": 8}
    assert row.data["enabled_kinds"] == ["tour", "esim", "hotel"]
    assert row.data["hotel_quote_policies"]["agoda"] == original["hotel_quote_policies"]["agoda"]
    assert row.data["hotel_quote_policies"]["booking"]["daily_limit"] == 12
    for field in (
        "public_enabled",
        "enabled_destinations",
        "airalo_feed_enabled",
        "future_shared_setting",
    ):
        assert row.data[field] == original[field]
    with pytest.raises(AppError):
        await hotel_admin.patch_config(
            HotelConfigPatch(version=7, hotel_enabled=False), actor(), session
        )
    row = await session.get(TravelServiceConfig, 1)
    assert row is not None
    assert row.version == 8
    assert "hotel" in row.data["enabled_kinds"]


async def test_catalog_lock_runs_before_select_and_refreshes_cached_state() -> None:
    session = AsyncMock()
    session.scalar.return_value = None
    assert await admin.locked_catalog_config(session) is None
    assert [call[0] for call in session.method_calls] == ["execute", "scalar"]
    assert "pg_advisory_xact_lock" in str(session.execute.call_args.args[0])
    statement = session.scalar.call_args.args[0]
    assert "FOR UPDATE" in str(statement)
    assert statement.get_execution_options()["populate_existing"] is True


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.parametrize("second_writer", ["hotel", "legacy"])
async def test_first_catalog_writes_are_serialized_across_connections(
    monkeypatch: pytest.MonkeyPatch, second_writer: str
) -> None:
    # Never delete or overwrite the stack's shared singleton. Each test owns a
    # fresh schema, exercising the truly absent-row case on real PostgreSQL.
    schema = f"test_hotel_config_lock_{uuid4().hex}"
    bootstrap = create_async_engine(Settings().database_url)
    scoped = create_async_engine(
        Settings().database_url, connect_args={"server_settings": {"search_path": schema}}
    )
    monkeypatch.setattr(admin, "audit", lambda *_args: None)
    monkeypatch.setattr(hotel_admin, "audit", lambda *_args: None)
    async with bootstrap.begin() as connection:
        await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    try:
        async with scoped.begin() as connection:
            await connection.run_sync(
                lambda sync: Base.metadata.create_all(sync, tables=[TravelServiceConfig.__table__])
            )
        factory = async_sessionmaker(scoped, expire_on_commit=False)
        start = asyncio.Event()

        async def write(kind: str) -> int:
            async with factory() as database:
                await start.wait()
                try:
                    if kind == "hotel":
                        await hotel_admin.patch_config(
                            HotelConfigPatch(version=0, hotel_enabled=True), actor(), database
                        )
                    else:
                        await admin.put_config(
                            ConfigInput(version=0, enabled_kinds=["tour"]), actor(), database
                        )
                    return 200
                except AppError as error:
                    assert error.code == "service_version_conflict"
                    return error.status

        requests = [asyncio.create_task(write(kind)) for kind in ("hotel", second_writer)]
        start.set()
        assert sorted(await asyncio.wait_for(asyncio.gather(*requests), timeout=15)) == [200, 409]
        async with factory() as database:
            row = await database.get(TravelServiceConfig, 1)
            assert row is not None and row.version == 1
    finally:
        await scoped.dispose()
        async with bootstrap.begin() as connection:
            await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        await bootstrap.dispose()


@pytest.mark.parametrize(
    "field,value",
    [
        ("public_enabled", True),
        ("airalo_feed_enabled", True),
        ("enabled_destinations", ["seoul"]),
        ("enabled_kinds", ["tour"]),
        ("hotel_enabled", None),
    ],
)
def test_hotel_config_rejects_global_or_null_fields(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        HotelConfigPatch.model_validate({"version": 0, field: value})


async def test_hotel_overview_scopes_every_product_offer_and_metric(session: AsyncSession) -> None:
    hotel = product("hotel", status="approved")
    tour = product("tour", "tour", "approved")
    session.add_all([hotel, tour, product("pending-hotel")])
    brand = TravelServiceBrand(code="klook", project_id="hotel-test")
    session.add(brand)
    await session.flush()
    for item in (hotel, tour):
        session.add(
            TravelServiceOffer(
                product_id=item.id,
                brand_id=brand.id,
                target_url=f"https://www.klook.com/{item.kind}",
            )
        )
        session.add(
            TripServiceSelection(
                trip_id=uuid4(),
                product_id=item.id,
                idempotency_key=item.kind,
                request_hash="a" * 64,
                status="booked",
            )
        )
        session.add(
            AffiliateClick(
                partner="klook",
                module=item.kind,
                service_type=item.kind,
                sub_id=item.kind,
                destination_summary="Tokyo",
                target_host="www.klook.com",
            )
        )
    for module in ("hotel", "activities"):
        session.add(
            DestinationAffiliateOffer(
                brand_id=brand.id,
                destination_id="tokyo",
                module=module,
                target_url=f"https://www.klook.com/{module}",
            )
        )
    session.add_all(
        [
            TravelServiceImport(source="csv", rows_json=[{"product": {"kind": "tour"}}]),
            TravelServiceImport(source="hotel_csv", rows_json=[{"product": {"kind": "hotel"}}]),
        ]
    )
    await session.commit()
    result = await hotel_admin.overview(actor(), session, offset=0, limit=60)
    assert {p["kind"] for p in result["products"]} == {"hotel"}
    assert result["summary"] == {"total": 2, "pending": 1, "approved": 1, "disabled": 0}
    assert {o["product_id"] for o in result["offers"]} == {hotel.id}
    assert {o["module"] for o in result["destination_offers"]} == {"hotel"}
    assert {run["source"] for run in result["imports"]} == {"hotel_csv"}
    assert result["review_due"] == 1
    assert result["operations"]["outbound_clicks"] == 1
    assert result["operations"]["self_reported_booked"] == 1
    assert all(c["counts"]["tour"] == 0 for c in result["coverage"])
    assert all("hotel" in brand["kinds"] for brand in result["brand_definitions"].values())
    assert not any(p["adapter_available"] for p in result["quote_providers"].values())
    other = await admin.overview_data(session, domain="services")
    assert {p["kind"] for p in other["products"]} == {"tour"}
    assert {o["module"] for o in other["destination_offers"]} == {"activities"}


async def test_hotel_preview_rejects_nonhotel_and_cross_kind_source_keys(
    session: AsyncSession,
) -> None:
    session.add(product("shared-key", "tour"))
    await session.commit()
    for value, code in (
        (csv_row(kind="tour"), "service_import_scope_mismatch"),
        (csv_row("shared-key"), "service_source_kind_mismatch"),
    ):
        preview = await hotel_admin.preview_import(CsvInput(csv=value), actor(), session)
        assert preview["source"] == "hotel_csv"
        assert preview["rows_json"][0]["error"] == code
        with pytest.raises(AppError):
            await hotel_admin.apply_import(preview["id"], actor(), session)
    existing = await session.scalar(
        select(TravelServiceProduct).where(TravelServiceProduct.source_key == "shared-key")
    )
    assert existing and existing.kind == "tour"


async def test_missing_options_matches_dashboard_absence_not_link_readiness(
    session: AsyncSession,
) -> None:
    missing = product("without-options")
    with_pending = product("has-pending-option", status="approved")
    session.add_all([missing, with_pending, product("tour-no-options", "tour")])
    await session.flush()
    session.add(
        HotelBookingOption(product_id=with_pending.id, provider="official", status="pending")
    )
    await session.commit()
    result = await hotel_admin.overview(actor(), session, missing_options=True, offset=0, limit=60)
    assert [row["id"] for row in result["products"]] == [missing.id]
    assert result["summary"]["total"] == 2
    normal = await hotel_admin.overview(actor(), session, offset=0, limit=60)
    assert len(normal["products"]) == 2
    review = await hotel_admin.overview(actor(), session, status="pending", offset=0, limit=60)
    assert [row["id"] for row in review["products"]] == [missing.id]


async def test_commit_checks_scope_before_completed_replay(session: AsyncSession) -> None:
    for source, kind in (("csv", "hotel"), ("hotel_csv", "tour")):
        run = TravelServiceImport(
            source=source,
            status="completed",
            rows_json=parse_csv(csv_row(kind=kind)),
            result_json={"processed": 1},
        )
        session.add(run)
        await session.commit()
        with pytest.raises(AppError):
            await commit_import(session, run.id, None, required_kind="hotel")


async def test_hotel_import_is_idempotent_and_keeps_all_review_gates_pending(
    session: AsyncSession,
) -> None:
    preview = await hotel_admin.preview_import(CsvInput(csv=csv_row()), actor(), session)
    first = await hotel_admin.apply_import(preview["id"], actor(), session)
    second = await hotel_admin.apply_import(preview["id"], actor(), session)
    assert first == second == {"processed": 1, "changed": 1, "pending_review": 1}
    rows = list(await session.scalars(select(TravelServiceProduct)))
    assert len(rows) == 1 and rows[0].status == "pending" and rows[0].verified_at is None
    assert not list(await session.scalars(select(TravelServiceBrand)))


async def test_commit_rechecks_collisions_created_after_preview(session: AsyncSession) -> None:
    preview = await hotel_admin.preview_import(CsvInput(csv=csv_row()), actor(), session)
    collision = product("hotel-one", "tour")
    session.add(collision)
    await session.commit()
    with pytest.raises(AppError):
        await hotel_admin.apply_import(preview["id"], actor(), session)
    assert collision.kind == "tour"
    with pytest.raises(AppError):
        await upsert_product(
            session, ProductInput.model_validate(parse_csv(csv_row())[0]["product"])
        )
    assert collision.kind == "tour"
