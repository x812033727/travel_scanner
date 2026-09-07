"""Real SQL import constraints in SQLite; no network and no external database required."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any
from uuid import UUID, uuid4

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from app.catalog_review.jobs import _discovery_context
from app.catalog_review.repository import (
    duplicate_draft,
    entity_snapshot,
    fingerprint,
    import_draft,
    make_review_item,
    publication_gaps,
    source_urls,
)
from app.catalog_review.schemas import DiscoveryDraft
from app.db import Base
from app.models import (
    AdminAuditLog,
    CatalogReviewItem,
    CatalogReviewRun,
    FoodArea,
    FoodCategory,
    FoodDestination,
    FoodHotspot,
    FoodLocalization,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantFood,
    FoodMerchantSource,
    HotspotLocalization,
    TravelFood,
    TravelHotspot,
    User,
)
from app.problems import AppError

WIKIDATA = "https://www.wikidata.org/wiki/Q123"
TABLES = (
    User,
    TravelHotspot,
    HotspotLocalization,
    TravelFood,
    FoodLocalization,
    FoodDestination,
    FoodHotspot,
    FoodMerchant,
    FoodMerchantSource,
    FoodCategory,
    FoodArea,
    FoodMerchantCategory,
    FoodMerchantFood,
    AdminAuditLog,
    CatalogReviewRun,
    CatalogReviewItem,
)


class LocalSession:
    """Async-shaped adapter around real SQLAlchemy queries and FK enforcement."""

    def __init__(self, database: Session) -> None:
        self.database = database

    async def scalar(self, statement: Any) -> Any:
        return self.database.scalar(statement)

    async def scalars(self, statement: Any) -> Any:
        return self.database.scalars(statement)

    async def flush(self) -> None:
        self.database.flush()

    def add(self, row: Any) -> None:
        self.database.add(row)


@pytest.fixture
def database() -> Iterator[tuple[LocalSession, User, CatalogReviewRun]]:
    engine = create_engine("sqlite://")
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys = ON"))
        Base.metadata.create_all(connection, tables=[model.__table__ for model in TABLES])
        with Session(connection, expire_on_commit=False) as session:
            actor = User(id=uuid4(), email="catalog-import@example.test", is_admin=True)
            session.add(actor)
            session.flush()
            run = CatalogReviewRun(
                id=uuid4(),
                actor_user_id=actor.id,
                idempotency_key="import-test",
                request_hash="hash",
                mode="discover_new",
                model="mock-gemini",
            )
            session.add(run)
            session.flush()
            yield LocalSession(session), actor, run
    engine.dispose()


def merchant_draft(**changes: Any) -> DiscoveryDraft:
    return DiscoveryDraft.model_validate(
        {
            "kind": "merchant",
            "name": "Example exact branch",
            "local_name": "範例本店",
            "destination_id": "tokyo",
            "slug": "example-exact-branch",
            "source_urls": [WIKIDATA],
            **changes,
        }
    )


@pytest.mark.parametrize(
    "url",
    [
        WIKIDATA,
        "https://www.japan.travel/en/spot/reference/",
        "https://restaurant.example/unverified-branch",
    ],
)
async def test_discovery_urls_are_unverified_audit_refs_not_authoritative_sources(
    database: Any,
    url: str,
) -> None:
    session, actor, run = database
    row = await import_draft(
        session,
        merchant_draft(
            source_urls=[url],
            data={
                "google_place_id": "model-invented-id",
                "latitude": 35.0,
                "longitude": 139.0,
                "official_website_url": url,
                "source_type": "merchant_official",
                "source_scope": "merchant_website",
                "claims_json": ["display_name"],
                "verified_at": "2026-09-07",
                "map_match_status": "verified",
            },
        ),
        actor.id,
        run.id,
    )
    assert isinstance(row, FoodMerchant)
    assert list((await session.scalars(select(FoodMerchantSource))).all()) == []
    assert row.review_status == "pending" and row.is_active is False
    assert row.map_match_status == "unverified"
    assert row.google_place_id is None and row.naver_map_url is None
    assert row.latitude is None and row.longitude is None
    assert row.verified_at is None and row.coordinate_verified_at is None
    assert row.official_website_url is None and row.official_website_verified_at is None
    snapshot = await entity_snapshot(session, row)
    assert snapshot["discovery_reference_urls"] == [url]
    assert source_urls(snapshot) == [url]
    gaps = publication_gaps("merchant", snapshot)
    assert "missing_direct_merchant_source" in gaps and "missing_food_category" in gaps
    item = await make_review_item(session, run.id, "merchant", row, "review_new")
    await session.flush()
    assert item.snapshot_hash == fingerprint(snapshot)
    assert item.snapshot_json["discovery_reference_urls"] == [url]


async def test_reference_audit_lookup_is_exact_normalized_and_fingerprint_stable(database: Any):
    session, actor, run = database
    row = await import_draft(
        session,
        merchant_draft(
            source_urls=[
                "https://WWW.WIKIDATA.ORG:443/wiki/Q123#label",
                WIKIDATA,
            ]
        ),
        actor.id,
        run.id,
    )
    assert isinstance(row, FoodMerchant)
    # SQLite reloads timezone-aware columns as naive values; compare persisted
    # snapshots on both sides rather than a transient Python datetime representation.
    session.database.expire_all()
    before = await entity_snapshot(session, row)
    assert before["discovery_reference_urls"] == [WIKIDATA]
    # Neither another entity's import nor another action on this entity is its source.
    for action, target in (
        ("catalog_candidate_imported", f"merchant:{uuid4()}"),
        ("catalog_candidate_updated", f"merchant:{row.id}"),
        ("catalog_candidate_imported", f"hotspot:{row.id}"),
    ):
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action=action,
                target=target,
                metadata_json={"source_urls": ["https://wrong.example/"]},
            )
        )
    await session.flush()
    session.database.expire_all()
    after = await entity_snapshot(session, row)
    assert after == before
    assert fingerprint(after) == fingerprint(before)


def existing_food(session: LocalSession, **changes: Any) -> TravelFood:
    row = TravelFood(
        **(
            {
                "id": uuid4(),
                "slug": "jp-existing-dish",
                "country_code": "JP",
                "local_name": "既有料理",
                "romanized_name": "Existing dish",
                "food_kind": "main",
                "meal_types": ["lunch"],
                "search_text": "existing dish",
                "review_status": "approved",
                "is_active": True,
            }
            | changes
        )
    )
    session.add(row)
    session.database.flush()
    return row


async def test_import_uses_existing_relation_ids_dedupes_and_preserves_pending_state(database: Any):
    session, actor, run = database
    category = FoodCategory(id=uuid4(), slug="existing-category", is_active=True)
    session.add(category)
    dish = existing_food(session)
    session.add(FoodDestination(food_id=dish.id, destination_id="tokyo"))
    await session.flush()
    row = await import_draft(
        session,
        merchant_draft(
            data={
                "category_slugs": [category.slug, category.slug],
                "food_slugs": [dish.slug, dish.slug],
            }
        ),
        actor.id,
        run.id,
    )
    categories = list((await session.scalars(select(FoodMerchantCategory))).all())
    foods = list((await session.scalars(select(FoodMerchantFood))).all())
    assert len(categories) == len(foods) == 1
    assert categories[0].category_id == category.id
    assert categories[0].source == "gemini"
    assert foods[0].food_id == dish.id
    assert categories[0].merchant_id == foods[0].merchant_id == row.id
    assert categories[0].is_primary and foods[0].is_primary
    assert row.review_status == "pending" and row.map_match_status == "unverified"
    snapshot = await entity_snapshot(session, row)
    assert "missing_food_category" not in publication_gaps("merchant", snapshot)
    assert "missing_direct_merchant_source" in publication_gaps("merchant", snapshot)


@pytest.mark.parametrize(
    "condition",
    [
        "unknown_food",
        "pending_food",
        "rejected_food",
        "disabled_food",
        "inactive_food",
        "other_destination",
        "no_destination",
        "other_country",
        "unknown_category",
        "inactive_category",
    ],
)
async def test_invalid_or_unavailable_relations_fail_before_creating_merchant(
    database: Any,
    condition: str,
) -> None:
    session, actor, run = database
    changes: dict[str, Any] = {}
    if condition in {"pending_food", "rejected_food", "disabled_food"}:
        changes["review_status"] = condition.removesuffix("_food")
    if condition == "inactive_food":
        changes["is_active"] = False
    if condition == "other_country":
        changes["country_code"] = "TW"
    dish = existing_food(session, **changes)
    if condition != "no_destination":
        session.add(
            FoodDestination(
                food_id=dish.id,
                destination_id=("seoul" if condition == "other_destination" else "tokyo"),
            )
        )
    category = FoodCategory(id=uuid4(), slug="category", is_active=condition != "inactive_category")
    session.add(category)
    await session.flush()
    data = {
        "food_slugs": ["invented-food" if condition == "unknown_food" else dish.slug],
        "category_slugs": [
            "invented-category" if condition == "unknown_category" else category.slug
        ],
    }
    with pytest.raises(AppError) as caught:
        await import_draft(session, merchant_draft(data=data), actor.id, run.id)
    assert caught.value.code == "catalog_relation_invalid"
    assert list((await session.scalars(select(FoodMerchant))).all()) == []
    assert list((await session.scalars(select(AdminAuditLog))).all()) == []


@pytest.mark.parametrize(
    "data",
    [
        {"category_slugs": "sushi"},
        {"category_slugs": [None]},
        {"category_slugs": ["../sushi"]},
        {"food_slugs": [str(UUID(int=1)).upper()]},
        {"food_slugs": {"id": "invented"}},
        {"food_slugs": [12]},
        {"food_slugs": ["x" * 129]},
        {"category_slugs": ["x"] * 7},
    ],
)
async def test_malformed_relation_lists_are_rejected(database: Any, data: dict[str, Any]):
    session, actor, run = database
    with pytest.raises(AppError) as caught:
        await import_draft(session, merchant_draft(data=data), actor.id, run.id)
    assert caught.value.code == "catalog_relation_invalid"
    assert list((await session.scalars(select(FoodMerchant))).all()) == []


@pytest.mark.parametrize(
    "url",
    [
        "https://guide.michelin.com/restaurant",
        "https://www.google.co.jp/maps/place/test",
        "https://map.naver.com/p/entry/place/123",
    ],
)
async def test_provider_owned_references_are_not_imported(database: Any, url: str):
    session, actor, run = database
    with pytest.raises(AppError):
        await import_draft(session, merchant_draft(source_urls=[url]), actor.id, run.id)
    assert list((await session.scalars(select(FoodMerchant))).all()) == []


@pytest.mark.parametrize(
    "variant", ["Historic Alias", "historic-alias", "Ｈｉｓｔｏｒｉｃ Ａｌｉａｓ"]
)
async def test_localized_alias_of_rejected_hotspot_is_a_dedupe_tombstone(
    database: Any, variant: str
):
    session, _, _ = database
    row = TravelHotspot(
        id=uuid4(),
        slug="existing-rejected",
        name="Rejected place",
        destination_id="tokyo",
        city_code="NRT",
        city_name="東京",
        country_code="JP",
        country_name="日本",
        category="culture",
        search_text="rejected",
        review_status="rejected",
        is_active=False,
    )
    session.add(row)
    await session.flush()
    session.add(
        HotspotLocalization(
            hotspot_id=row.id,
            locale="en",
            name="Another English name",
            aliases=["Historic Alias"],
            search_terms=[],
        )
    )
    await session.flush()
    candidate = DiscoveryDraft(
        kind="hotspot",
        slug="new-generated-slug",
        name=variant,
        local_name="Different local name",
        destination_id="tokyo",
        source_urls=[WIKIDATA],
        data={"category": "culture"},
    )
    assert await duplicate_draft(session, candidate) is True


async def test_discovery_context_offers_only_publishable_dishes_but_avoids_all_names(database: Any):
    session, _, _ = database
    slugs = []
    for index, (status, active) in enumerate(
        (
            ("approved", True),
            ("pending", True),
            ("rejected", False),
            ("approved", False),
        )
    ):
        dish = existing_food(session, slug=f"dish-{index}", review_status=status, is_active=active)
        session.add(FoodDestination(food_id=dish.id, destination_id="tokyo"))
        slugs.append(dish.slug)
    await session.flush()
    destinations, avoid = await _discovery_context(session)
    tokyo = next(entry for entry in destinations if entry["id"] == "tokyo")
    assert tokyo["food_slugs"] == [slugs[0]]
    assert set(slugs) <= set(avoid)


@pytest.mark.parametrize(
    ("field", "value"),
    [("name", "Different museum"), ("aliases", ["Different historic alias"])],
)
async def test_hotspot_localization_edits_change_snapshot_without_mutating_prior_item(
    database: Any, field: str, value: Any
):
    session, actor, run = database
    row = await import_draft(
        session,
        DiscoveryDraft(
            kind="hotspot",
            slug="localized-museum",
            name="Museum",
            local_name="博物館",
            destination_id="tokyo",
            source_urls=[WIKIDATA],
            data={"category": "culture"},
        ),
        actor.id,
        run.id,
    )
    assert isinstance(row, TravelHotspot)
    for locale in ("zh-TW", "en"):
        session.add(
            HotspotLocalization(
                hotspot_id=row.id,
                locale=locale,
                name=f"Original museum {locale}",
                aliases=["Historic museum"],
                search_terms=["museum"],
            )
        )
    await session.flush()
    session.database.expire_all()
    item = await make_review_item(session, run.id, "hotspot", row, "review_new")
    await session.flush()
    before = await entity_snapshot(session, row)
    assert [entry["locale"] for entry in before["localizations"]] == ["en", "zh-TW"]
    assert before["localizations"][0]["search_terms"] == ["museum"]
    assert item.snapshot_hash == fingerprint(before)

    localization = await session.scalar(
        select(HotspotLocalization).where(
            HotspotLocalization.hotspot_id == row.id,
            HotspotLocalization.locale == "en",
        )
    )
    setattr(localization, field, value)
    await session.flush()
    session.database.expire_all()
    after = await entity_snapshot(session, row)
    assert before["updated_at"] == after["updated_at"]
    assert before["localizations"][0][field] != after["localizations"][0][field]
    assert fingerprint(after) != item.snapshot_hash
    assert fingerprint(item.snapshot_json) == item.snapshot_hash
