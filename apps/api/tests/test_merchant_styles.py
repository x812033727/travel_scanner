"""Real HTTP/DB style moderation, public isolation, import and migration contracts."""

import asyncio
import json
import os
import runpy
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from fastapi import Depends, Header
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, func, inspect, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.db import Base, get_session
from app.foods.styles import STYLE_NAMES
from app.foods.trend_import import load_trend_merchants, parse_merchant, persist_trend_merchants
from app.main import app
from app.models import (
    AdminAuditLog,
    FoodArea,
    FoodCategory,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantSource,
    FoodMerchantStyle,
    User,
)
from app.problems import AppError


def evidence(style: str = "instagrammable", status: str = "approved") -> dict[str, Any]:
    return {
        "style": style,
        "status": status,
        "evidence_url": "https://shop.example/design",
        "evidence_title": "Branch design",
        "rationale": "Official branch gallery shows a floral greenhouse.",
        "checked_on": datetime.now(UTC).date().isoformat(),
    }


@pytest_asyncio.fixture(
    params=["sqlite"] + (["postgresql"] if os.getenv("RUN_INTEGRATION_TESTS") == "1" else [])
)
async def catalog(request: pytest.FixtureRequest) -> AsyncIterator[Any]:
    schema = "merchant_style_test_" + uuid4().hex
    administrator = None
    if request.param == "postgresql":
        from app.config import get_settings

        administrator = create_async_engine(get_settings().database_url)
        async with administrator.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = create_async_engine(
            get_settings().database_url, connect_args={"server_settings": {"search_path": schema}}
        )
    else:
        engine = create_async_engine("sqlite+aiosqlite://")

        @event.listens_for(engine.sync_engine, "connect")
        def sqlite_functions(connection: Any, _: Any) -> None:
            connection.create_function("btrim", 1, lambda value: value.strip() if value else value)
            connection.execute("PRAGMA foreign_keys=ON")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    admin_id, member_id = uuid4(), uuid4()
    async with factory() as session:
        session.add_all(
            [
                User(id=admin_id, email="styles-admin@example.test", is_admin=True),
                User(id=member_id, email="styles-member@example.test", is_admin=False),
            ]
        )
        area = FoodArea(
            slug="tokyo-kuramae",
            destination_id="tokyo",
            country_code="JP",
            names_json={"en": "Kuramae"},
        )
        category = FoodCategory(slug="cafe-tea", names_json={"en": "Cafe"})
        session.add_all([area, category])
        await session.flush()
        ids = []
        for index in range(3):
            merchant = FoodMerchant(
                slug=f"tokyo-style-{index}",
                name=f"Style shop {index}",
                local_name=f"Shop {index}",
                destination_id="tokyo",
                country_code="JP",
                area_id=area.id,
                names_json={},
                latitude=35.7,
                longitude=139.7,
                coordinate_source_type="merchant_official",
                coordinate_source_url="https://shop.example/location",
                google_place_id=f"TestPlace{index}",
                map_match_status="verified",
                review_status="approved" if index < 2 else "pending",
                is_active=index < 2,
            )
            session.add(merchant)
            await session.flush()
            ids.append(str(merchant.id))
            session.add(
                FoodMerchantSource(
                    merchant_id=merchant.id,
                    source_type="merchant_official",
                    source_scope="merchant_website",
                    source_title="Branch",
                    source_url="https://shop.example/",
                    claims_json=["display_name", "address"],
                    is_current=True,
                )
            )
            session.add(
                FoodMerchantCategory(
                    merchant_id=merchant.id,
                    category_id=category.id,
                    is_primary=True,
                    source="admin",
                )
            )
        await session.commit()

    async def database() -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            yield session

    async def actor(
        session: Annotated[AsyncSession, Depends(get_session)],
        x_test_role: Annotated[str | None, Header()] = None,
    ) -> User:
        if not x_test_role:
            raise AppError(401, "authentication_required", "Sign in")
        user = await session.get(User, admin_id if x_test_role == "admin" else member_id)
        assert user is not None
        return user

    app.dependency_overrides[get_session] = database
    app.dependency_overrides[current_user] = actor
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client, factory, ids, admin_id
    finally:
        app.dependency_overrides.clear()
        await engine.dispose()
        if administrator is not None:
            assert schema.startswith("merchant_style_test_") and len(schema) == 52
            async with administrator.begin() as connection:
                await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
            await administrator.dispose()


async def save(
    client: AsyncClient,
    merchant: str,
    *,
    style: str = "instagrammable",
    status: str = "approved",
    expected: str | None = None,
) -> Any:
    result = await client.put(
        f"/api/v1/admin/foods/merchants/{merchant}/styles",
        headers={"x-test-role": "admin"},
        json={
            "reason": "Checked the branch source",
            "expected_updated_at": expected,
            "review": evidence(style, status),
        },
    )
    assert result.status_code == 200, result.text
    return result.json()


@pytest.mark.asyncio
async def test_styles_require_admin_valid_evidence_and_known_values(catalog: Any) -> None:
    client, _, ids, _ = catalog
    path = f"/api/v1/admin/foods/merchants/{ids[0]}/styles"
    for method in ("GET", "PUT"):
        for role, status in ((None, 401), ("member", 403)):
            response = await client.request(
                method,
                path,
                headers={"x-test-role": role} if role else {},
                **(
                    {"json": {"reason": "Source checked", "review": evidence()}}
                    if method == "PUT"
                    else {}
                ),
            )
            assert response.status_code == status, response.text
    for field, value in (
        ("style", "popular"),
        ("status", "active"),
        ("rationale", " "),
        ("evidence_url", "http://shop.example/"),
        ("evidence_url", "https://localhost/x"),
        ("evidence_url", "https://www.google.com/maps/x"),
        ("checked_on", "2099-01-01"),
    ):
        response = await client.put(
            path,
            headers={"x-test-role": "admin"},
            json={"reason": "Review", "review": {**evidence(), field: value}},
        )
        assert response.status_code == 422, response.text
    assert (await client.get("/api/v1/foods/merchants?style=unknown")).status_code == 422
    assert (await client.get(path, headers={"x-test-role": "admin"})).json() == {"items": []}


@pytest.mark.asyncio
async def test_labels_filters_facets_locales_and_reviews_do_not_publish(catalog: Any) -> None:
    client, factory, ids, admin_id = catalog
    first = await save(client, ids[0])
    await save(client, ids[0], style="artsy")
    await save(client, ids[1], style="artsy")
    await save(client, ids[2])  # a label cannot expose a pending merchant
    for locale in STYLE_NAMES["instagrammable"]:
        result = (
            await client.get(
                "/api/v1/foods/merchants?destination_id=tokyo&area=tokyo-kuramae&category=cafe-tea&style=instagrammable",
                headers={"x-travel-locale": locale},
            )
        ).json()
        assert result["total"] == 1, result
        assert result["items"][0]["id"] == ids[0]
        assert len(result["items"][0]["styles"]) == 2
        assert {item["slug"]: item["name"] for item in result["items"][0]["styles"]} == {
            slug: names[locale] for slug, names in STYLE_NAMES.items()
        }
        assert {item["slug"]: item["merchant_count"] for item in result["facets"]["styles"]} == {
            "instagrammable": 1,
            "artsy": 2,
        }
        assert result["facets"]["categories"][0]["merchant_count"] == 1
        assert result["facets"]["areas"][0]["merchant_count"] == 1
        assert not any(
            "reviewed_by" in key or key == "rationale"
            for item in result["items"][0]["styles"]
            for key in item
        )
    filtered = (await client.get("/api/v1/foods/merchants?style=artsy&q=shop%201")).json()
    assert filtered["total"] == 1
    assert filtered["facets"]["styles"][0]["merchant_count"] == 0
    second = await save(client, ids[0], status="pending", expected=first["updated_at"])
    assert (await client.get("/api/v1/foods/merchants?style=instagrammable")).json()["total"] == 0
    await save(client, ids[0], status="rejected", expected=second["updated_at"])
    async with factory() as session:
        assert (await session.get(FoodMerchant, UUID(ids[2]))).review_status == "pending"
        audits = (
            await session.scalars(
                select(AdminAuditLog).where(AdminAuditLog.action == "food_merchant_style_reviewed")
            )
        ).all()
        assert len(audits) == 6
        assert all(row.actor_user_id == admin_id for row in audits)
        assert all(
            row.metadata_json["reason"]
            and "before" in row.metadata_json
            and "after" in row.metadata_json
            for row in audits
        )


@pytest.mark.asyncio
async def test_stale_review_rejected_and_admin_can_find_pending_labels(catalog: Any) -> None:
    client, _, ids, _ = catalog
    first = await save(client, ids[0], status="pending")
    result = (
        await client.get(
            "/api/v1/admin/foods/merchants?style=instagrammable&style_status=pending",
            headers={"x-test-role": "admin"},
        )
    ).json()
    assert [item["id"] for item in result["items"]] == [ids[0]]
    await save(client, ids[0], expected=first["updated_at"])
    response = await client.put(
        f"/api/v1/admin/foods/merchants/{ids[0]}/styles",
        headers={"x-test-role": "admin"},
        json={
            "reason": "Stale retry",
            "expected_updated_at": first["updated_at"],
            "review": evidence(status="rejected"),
        },
    )
    assert response.status_code == 409
    assert response.json()["code"] == "merchant_style_changed"


@pytest.mark.asyncio
async def test_import_proposes_once_and_never_overwrites_reviews(catalog: Any) -> None:
    client, factory, ids, _ = catalog
    raw_evidence = evidence()
    raw_evidence.pop("status")

    def merchant(slug: str, name: str) -> Any:
        return parse_merchant(
            {
                "destination": "tokyo",
                "district_key": None,
                "slug": slug,
                "name_zh": name,
                "local_name": name,
                "category_slugs": ["cafe-tea"],
                "source_url": "https://shop.example/",
                "source_title": "Official branch",
                "source_kind": "merchant_official",
                "styles": [raw_evidence],
            },
            row=1,
        )

    rows = [merchant("tokyo-style-0", "Shop 0"), merchant("tokyo-new-style-shop", "New shop")]
    async with factory() as session:
        preview = await persist_trend_merchants(session, rows, apply=False)
        assert len(preview["proposed_styles"]) == 2
        assert await session.scalar(select(func.count(FoodMerchantStyle.id))) == 0
        applied = await persist_trend_merchants(session, rows, apply=True)
        assert applied["created"] == 1
        assert len(applied["proposed_styles"]) == 2
        new = await session.scalar(
            select(FoodMerchant).where(FoodMerchant.slug == "tokyo-new-style-shop")
        )
        assert new and not new.is_active and new.review_status == "pending" and new.area_id is None
        assert new.google_place_id is None and new.latitude is None
    before = (
        await client.get(
            f"/api/v1/admin/foods/merchants/{ids[0]}/styles", headers={"x-test-role": "admin"}
        )
    ).json()["items"][0]
    await save(client, ids[0], status="rejected", expected=before["updated_at"])
    async with factory() as session:
        replay = await persist_trend_merchants(session, rows, apply=True)
        assert replay["created"] == 0 and replay["proposed_styles"] == []
        assert (
            await session.scalar(
                select(FoodMerchantStyle).where(FoodMerchantStyle.merchant_id == UUID(ids[0]))
            )
        ).status == "rejected"


@pytest.mark.asyncio
async def test_migration_fresh_existing_and_roundtrip() -> None:
    from alembic import context
    from alembic.migration import MigrationContext
    from alembic.operations import Operations

    migration = runpy.run_path(str(Path("migrations/versions/0061_merchant_styles.py")))
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
                item["name"] for item in inspect(connection).get_columns("food_merchant_styles")
            }
            assert columns == {column.name for column in FoodMerchantStyle.__table__.columns}
            migration["downgrade"]()
            assert "food_merchant_styles" not in inspect(connection).get_table_names()
            migration["upgrade"]()

    async with engine.begin() as connection:
        await connection.run_sync(run)
    await engine.dispose()


@pytest.mark.asyncio
async def test_concurrent_first_reviews_have_one_winner(catalog: Any) -> None:
    client, factory, ids, _ = catalog
    if factory.kw["bind"].dialect.name != "postgresql":
        pytest.skip("PostgreSQL row-lock contract")
    path = f"/api/v1/admin/foods/merchants/{ids[0]}/styles"
    responses = await asyncio.gather(
        *[
            client.put(
                path,
                headers={"x-test-role": "admin"},
                json={
                    "reason": "Concurrent source review",
                    "expected_updated_at": None,
                    "review": evidence(status=status),
                },
            )
            for status in ("approved", "rejected")
        ]
    )
    assert sorted(response.status_code for response in responses) == [200, 409]
    async with factory() as session:
        assert await session.scalar(select(func.count(FoodMerchantStyle.id))) == 1
        assert (
            await session.scalar(
                select(func.count(AdminAuditLog.id)).where(
                    AdminAuditLog.action == "food_merchant_style_reviewed"
                )
            )
            == 1
        )


def test_first_research_batch_is_valid_and_cannot_embed_approvals() -> None:
    rows = load_trend_merchants(Path("app/foods/data/style_merchants_2026_09.json"))
    assert len(rows) == 5
    assert {item.style for row in rows for item in row.styles} == {"instagrammable", "artsy"}
    assert all(row.styles and row.address for row in rows)


@pytest.mark.parametrize(
    ("filename", "count", "style_count"),
    [
        ("style_merchants_2026_09.json", 5, 5),
        ("style_merchants_2026_09_batch_02.json", 8, 9),
        ("style_merchants_2026_09_batch_03.json", 7, 7),
    ],
)
def test_research_batches_contain_evidence_not_publication_state(
    filename: str, count: int, style_count: int
) -> None:
    path = Path("app/foods/data") / filename
    raw = json.loads(path.read_text(encoding="utf-8"))
    rows = load_trend_merchants(path)
    assert len(rows) == count
    assert len({row.slug for row in rows}) == count
    assert len({row.identity for row in rows}) == count
    assert sum(len(row.styles) for row in rows) == style_count
    assert all(row.styles and row.address and row.note for row in rows)
    forbidden = {
        "review_status",
        "is_active",
        "map_match_status",
        "google_place_id",
        "naver_map_url",
        "latitude",
        "longitude",
        "coordinate_source_type",
    }
    for item in raw:
        assert not forbidden.intersection(item)
        assert all("status" not in style for style in item["styles"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("filename", "merchant_count", "style_count"),
    [
        ("style_merchants_2026_09_batch_02.json", 8, 9),
        ("style_merchants_2026_09_batch_03.json", 7, 7),
    ],
)
async def test_research_batch_import_is_private_audited_and_replay_safe(
    catalog: Any,
    filename: str,
    merchant_count: int,
    style_count: int,
) -> None:
    client, factory, _, _ = catalog
    path = Path("app/foods/data") / filename
    rows = load_trend_merchants(path)
    async with factory() as session:
        for slug in sorted({slug for row in rows for slug in row.category_slugs} - {"cafe-tea"}):
            session.add(FoodCategory(slug=slug, names_json={"en": slug}))
        await session.commit()
        preview = await persist_trend_merchants(session, rows, apply=False, source_file=path.name)
        assert preview["created"] == merchant_count
        assert len(preview["proposed_styles"]) == style_count
        assert await session.scalar(select(func.count(FoodMerchant.id))) == 3
        assert await session.scalar(select(func.count(AdminAuditLog.id))) == 0

        applied = await persist_trend_merchants(session, rows, apply=True, source_file=path.name)
        assert applied["created"] == merchant_count
        assert applied["proposed_styles"] == preview["proposed_styles"]
        merchants = (
            await session.scalars(
                select(FoodMerchant).where(FoodMerchant.slug.in_([row.slug for row in rows]))
            )
        ).all()
        assert len(merchants) == merchant_count
        for merchant in merchants:
            assert merchant.review_status == "pending" and not merchant.is_active
            assert merchant.map_match_status == "unverified" and merchant.area_id is None
            assert merchant.google_place_id is None and merchant.naver_map_url is None
            assert merchant.latitude is None and merchant.longitude is None
        styles = (await session.scalars(select(FoodMerchantStyle))).all()
        assert len(styles) == style_count and all(style.status == "pending" for style in styles)
        audits = (await session.scalars(select(AdminAuditLog))).all()
        assert {audit.action for audit in audits} == {
            "food_merchant_created",
            "food_merchant_styles_proposed",
        }
        assert len(audits) == 2
        assert all(a.actor_user_id is None and a.metadata_json["file"] == path.name for a in audits)
        created_audit = next(a for a in audits if a.action == "food_merchant_created")
        assert created_audit.metadata_json["count"] == merchant_count
        styles_audit = next(a for a in audits if a.action == "food_merchant_styles_proposed")
        assert styles_audit.metadata_json["items"] == applied["proposed_styles"]

        replay = await persist_trend_merchants(session, rows, apply=True, source_file=path.name)
        assert replay["created"] == 0 and replay["proposed_styles"] == []
        assert await session.scalar(select(func.count(FoodMerchant.id))) == 3 + merchant_count
        assert await session.scalar(select(func.count(FoodMerchantStyle.id))) == style_count
        assert await session.scalar(select(func.count(AdminAuditLog.id))) == 2
    for style in ("instagrammable", "artsy"):
        assert (await client.get(f"/api/v1/foods/merchants?style={style}")).json()["total"] == 0


def test_research_batches_do_not_repeat_merchant_identities() -> None:
    rows = [
        row
        for path in sorted(Path("app/foods/data").glob("style_merchants_*.json"))
        for row in load_trend_merchants(path)
    ]
    assert len(rows) == len({row.slug for row in rows}) == len({row.identity for row in rows})
