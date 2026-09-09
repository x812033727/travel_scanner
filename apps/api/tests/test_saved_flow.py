"""Saved-library contracts run on SQLite and on PostgreSQL in full-stack CI."""

from datetime import UTC, date, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from sqlalchemy import delete, func, select, update
from test_community_foundation import Harness
from test_community_foundation import harness as community_harness
from test_discovery_community import guide_fixture

from app.community.models import Collection, CollectionItem, Profile
from app.config import get_settings
from app.models import (
    HotspotFavorite,
    HotspotGuide,
    ProviderConfig,
    RestaurantFavorite,
    RestaurantPlace,
    TravelHotspot,
    TravelServiceConfig,
    TravelServiceFavorite,
    TravelServiceProduct,
    TripPlan,
    TripPlanItem,
)
from app.saved import service

harness = community_harness


@pytest.mark.parametrize(
    "url",
    [
        "",
        "not a database URL",
        "postgresql+asyncpg://test:test@db.example.com/fixture",
        "postgresql+asyncpg://test:test@192.168.1.2/fixture",
        "postgresql+asyncpg://test:test@127.0.0.1/fixture?host=production.example.com",
        "postgresql+asyncpg://test:test@127.0.0.1/fixture?service=prod",
        "sqlite+aiosqlite://",
    ],
)
def test_frontend_seed_rejects_non_loopback_or_connection_overrides(
    monkeypatch: pytest.MonkeyPatch, url: str
) -> None:
    from fixtures.frontend_flow_seed import require_isolated_target

    monkeypatch.setenv("DISCOVERY_E2E", "1")
    with pytest.raises(RuntimeError, match="loopback"):
        require_isolated_target(url)


def test_frontend_seed_requires_explicit_opt_in(monkeypatch: pytest.MonkeyPatch) -> None:
    from fixtures.frontend_flow_seed import require_isolated_target

    monkeypatch.delenv("DISCOVERY_E2E", raising=False)
    with pytest.raises(RuntimeError, match="DISCOVERY_E2E=1"):
        require_isolated_target("postgresql+asyncpg://test:test@127.0.0.1/fixture")
    monkeypatch.setenv("DISCOVERY_E2E", "1")
    for host in ("127.0.0.1", "localhost", "[::1]"):
        assert require_isolated_target(f"postgresql+asyncpg://test:test@{host}/fixture").database


@pytest.mark.asyncio
async def test_frontend_seed_replay_is_searchable_saved_and_plannable(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    from fixtures import frontend_flow_seed as fixture

    from app.discovery.sources import catalog_items

    h = harness
    # Guards have separate rejection tests; use this same replay/read contract on
    # the isolated SQLite harness as well as CI's PostgreSQL scratch schema.
    monkeypatch.setattr(fixture, "require_isolated_target", lambda value: value)
    monkeypatch.setattr("app.trips.router.get_redis", lambda: AsyncMock())
    async with h.factory() as session:
        await fixture.seed_catalog(session)
        await fixture.seed_catalog(session)
        assert await session.scalar(select(func.count()).select_from(TravelHotspot)) == 1
        results = await catalog_items(session, "en", q="Frontend flow fixture")
        assert len(results) == 1 and results[0].title == fixture.FIXTURE_TITLE
        assert results[0].place_ref["selection_path"] == (
            f"/hotspots/{fixture.FIXTURE_ID}/trip-selections"
        )
        trip = TripPlan(
            user_id=h.ids[0],
            name="Fixture trip",
            mode="manual",
            destination_name="Tokyo",
            timezone="Asia/Tokyo",
            start_date=date(2027, 1, 10),
            end_date=date(2027, 1, 11),
            total_price=0,
            currency="TWD",
            data={"fixture": "frontend_flow"},
        )
        session.add(trip)
        await session.commit()
        trip_id, version = str(trip.id), trip.version
    await h.call("PUT", f"/saved-items/hotspot/{fixture.FIXTURE_ID}", expected=201)
    result = await h.call(
        "POST",
        f"/hotspots/{fixture.FIXTURE_ID}/trip-selections",
        json={"trip_id": trip_id, "version": version, "day_date": "2027-01-10"},
    )
    assert result.json()["version"] > version
    async with h.factory() as session:
        assert await session.scalar(
            select(TripPlanItem.id).where(
                TripPlanItem.trip_plan_id == UUID(trip_id),
                TripPlanItem.title == fixture.FIXTURE_TITLE,
            )
        )


async def seed(h: Harness, count: int = 1) -> list[UUID]:
    async with h.factory() as session:
        rows = [
            TravelHotspot(
                slug=f"saved-test-{index}",
                name=f"Place {index}",
                search_text=f"Place {index}",
                destination_id="tokyo" if index % 2 == 0 else "osaka",
                city_name="Tokyo",
                city_code="NRT",
                country_code="JP",
                country_name="Japan",
                category="culture",
                review_status="approved",
                is_active=True,
                source_urls=["https://example.org/source"],
            )
            for index in range(count)
        ]
        session.add_all(rows)
        await session.commit()
        return [row.id for row in rows]


async def guide(h: Harness, *, enabled: bool = True) -> UUID:
    hotspot = (await seed(h))[0]
    async with h.factory() as session:
        row = guide_fixture(hotspot_id=hotspot, review_status="approved" if enabled else "pending")
        session.add(row)
        await session.commit()
        return row.id


async def create_list(h: Harness, name: str = "Weekend", actor: int = 0) -> str:
    return (
        await h.call("POST", "/saved-items/collections", actor=actor, json={"name": name})
    ).json()["id"]


@pytest.mark.asyncio
async def test_one_click_collection_and_anonymous_contract_without_community(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    monkeypatch.setattr(get_settings(), "discovery_enabled", True)
    identifier = (await seed(h))[0]
    key = f"hotspot:{identifier}"
    async with h.factory() as session:
        await session.execute(
            update(ProviderConfig)
            .where(ProviderConfig.provider == "community")
            .values(config={"enabled": False})
        )
        await session.execute(delete(Profile).where(Profile.user_id == h.ids[0]))
        await session.commit()
    for method, path, kwargs in (
        ("GET", "/saved-items/all", {}),
        ("POST", "/saved-items/states", {"json": {"keys": [key]}}),
        ("PUT", f"/saved-items/hotspot/{identifier}", {}),
    ):
        await h.call(method, path, actor=None, expected=401, **kwargs)
    assert (await h.call("POST", "/saved-items/states", json={"keys": [key]})).json() == {
        "items": [{"key": key, "saved": False, "collection_ids": []}]
    }
    first = await h.call("PUT", f"/saved-items/hotspot/{identifier}", expected=201)
    assert first.json()["created"] is True
    assert first.headers["cache-control"] == "private, no-store"
    assert (
        await h.call("PUT", f"/saved-items/hotspot/{identifier.hex.upper()}", expected=201)
    ).json()["created"] is False
    listing = await h.call("GET", "/saved-items/all")
    assert listing.headers["cache-control"] == "private, no-store"
    assert listing.json()["total"] == 1 and listing.json()["items"][0]["key"] == key
    collection = await create_list(h)
    await h.call(
        "POST",
        f"/saved-items/collections/{collection}/items",
        json={"kind": "hotspot", "id": str(identifier)},
    )
    content = (await h.call("GET", f"/saved-items/collections/{collection}")).json()["items"][0]
    removed = await h.call("DELETE", f"/saved-items/collections/{collection}/items/{content['id']}")
    assert removed.json() == {"deleted": True, "key": key, "saved": True, "collection_ids": []}
    assert (await h.call("GET", "/saved-items/all")).json()["total"] == 1


@pytest.mark.asyncio
async def test_favorite_conflict_is_idempotent_and_stale_state_does_not_double_count(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    h = harness
    identifier = (await seed(h))[0]
    key = f"hotspot:{identifier}"
    async with h.factory() as session:
        values = {"user_id": h.ids[0], "hotspot_id": identifier}
        columns = ["user_id", "hotspot_id"]
        assert await service.insert_unique_reference(session, HotspotFavorite, values, columns)
        assert not await service.insert_unique_reference(session, HotspotFavorite, values, columns)
        await session.commit()
    monkeypatch.setattr(
        service,
        "states",
        AsyncMock(return_value={"items": [{"key": key, "saved": False, "collection_ids": []}]}),
    )
    event = AsyncMock()
    monkeypatch.setattr("app.analytics.service.record_event", event)
    response = await h.call("PUT", f"/saved-items/hotspot/{identifier}", expected=201)
    assert response.json()["created"] is False
    event.assert_not_awaited()
    async with h.factory() as session:
        assert await session.scalar(select(func.count()).select_from(HotspotFavorite)) == 1


@pytest.mark.asyncio
async def test_real_cursor_more_than_500_deduplicates_and_filters_before_limit(
    harness: Harness,
) -> None:
    h = harness
    ids = await seed(h, 551)
    moment = datetime(2026, 1, 1, tzinfo=UTC)
    collection = await create_list(h)
    async with h.factory() as session:
        session.add_all(
            [
                HotspotFavorite(user_id=h.ids[0], hotspot_id=identifier, created_at=moment)
                for identifier in ids
            ]
        )
        session.add(
            CollectionItem(
                collection_id=UUID(collection),
                kind="hotspot",
                target=ids[0].hex.upper(),
                created_at=moment,
            )
        )
        session.add(
            CollectionItem(
                collection_id=UUID(collection),
                kind="hotspot",
                target=str(ids[0]),
                created_at=moment,
            )
        )
        await session.commit()
    seen = []
    cursor = None
    while True:
        params = {"limit": 100, **({"cursor": cursor} if cursor else {})}
        page = (await h.call("GET", "/saved-items/all", params=params)).json()
        assert page["total"] == 551
        seen.extend(item["key"] for item in page["items"])
        cursor = page["next_cursor"]
        if cursor is None:
            assert not page["has_more"]
            break
    assert len(seen) == len(set(seen)) == 551
    tokyo = (await h.call("GET", "/saved-items/all?type=hotspot&destination=tokyo&limit=1")).json()
    assert tokyo["total"] == 276
    scoped = (await h.call("GET", f"/saved-items/all?collection={collection}")).json()
    assert scoped["total"] == 1
    await h.call(
        "GET",
        "/saved-items/all",
        actor=1,
        expected=422,
        params={"cursor": tokyo["next_cursor"], "destination": "tokyo", "type": "hotspot"},
    )
    await h.call(
        "GET",
        "/saved-items/all",
        expected=422,
        params={"cursor": tokyo["next_cursor"], "destination": "osaka", "type": "hotspot"},
    )
    await h.call(
        "POST", "/saved-items/states", expected=422, json={"keys": [f"hotspot:{ids[0]}"] * 101}
    )
    assert (
        await h.call("POST", "/saved-items/states", json={"keys": [f"hotspot:{ids[-1]}"]})
    ).json()["items"][0]["saved"]


@pytest.mark.asyncio
async def test_inbox_unique_hidden_and_immutable_for_both_collection_apis(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    monkeypatch.setattr(get_settings(), "discovery_enabled", True)
    identifier = await guide(h)
    for kind in ("guide", "video", "article"):
        result = (await h.call("PUT", f"/saved-items/{kind}/{identifier}", expected=201)).json()
        assert result["key"] == f"guide:{identifier}"
    async with h.factory() as session:
        inbox = await session.scalar(select(Collection).where(Collection.user_id == h.ids[0]))
        assert inbox is not None and inbox.system_role == "inbox"
        inbox_id = inbox.id
        assert await session.scalar(select(func.count()).select_from(CollectionItem)) == 1
    assert (await h.call("GET", "/saved-items/collections")).json()["items"] == []
    assert (await h.call("GET", "/discovery/collections")).json()["items"] == []
    assert (await h.call("GET", "/community/collections")).json()["items"] == []
    for prefix in ("saved-items", "discovery", "community"):
        await h.call("DELETE", f"/{prefix}/collections/{inbox_id}", expected=404)
    await h.call("PUT", f"/community/collections/{inbox_id}", expected=404, json={"name": "Oops"})
    assert (await h.call("GET", "/saved-items/all?type=video")).json()["total"] == 1
    assert (await h.call("GET", "/saved-items/all?type=article")).json()["total"] == 0
    await h.call("DELETE", f"/saved-items/guide/{identifier}", expected=204)
    assert (await h.call("GET", "/saved-items/all")).json()["total"] == 0


@pytest.mark.asyncio
async def test_downpublished_content_is_private_removable_placeholder(harness: Harness) -> None:
    h = harness
    identifier = (await seed(h))[0]
    await h.call("PUT", f"/saved-items/hotspot/{identifier}", expected=201)
    first, second = await create_list(h, "First"), await create_list(h, "Second")
    for collection in (first, second):
        await h.call(
            "POST",
            f"/saved-items/collections/{collection}/items",
            json={"kind": "hotspot", "id": str(identifier)},
        )
    async with h.factory() as session:
        await session.execute(
            update(TravelHotspot)
            .where(TravelHotspot.id == identifier)
            .values(name="Private withdrawn name", review_status="rejected")
        )
        await session.commit()
    listing = (await h.call("GET", "/saved-items/all")).json()
    assert listing["total"] == 1
    row = listing["items"][0]
    assert row["unavailable"] and "title" not in row and "discovery" not in row
    assert "Private withdrawn name" not in str(listing)
    await h.call("PUT", f"/saved-items/hotspot/{identifier}", expected=404)
    await h.call("DELETE", f"/saved-items/hotspot/{identifier}", expected=204)
    assert (await h.call("GET", "/saved-items/all")).json()["total"] == 0
    for collection in (first, second):
        assert (await h.call("GET", f"/saved-items/collections/{collection}")).json()["items"] == []


@pytest.mark.asyncio
async def test_legacy_collection_only_reference_survives_remove_and_delete(
    harness: Harness,
) -> None:
    h = harness
    ids = await seed(h, 2)
    collection = await create_list(h)
    async with h.factory() as session:
        rows = [
            CollectionItem(collection_id=UUID(collection), kind="hotspot", target=str(identifier))
            for identifier in ids
        ]
        rows.append(
            CollectionItem(collection_id=UUID(collection), kind="pet_place", target="bad-id")
        )
        session.add_all(rows)
        await session.commit()
        first = rows[0].id
    await h.call("DELETE", f"/saved-items/collections/{collection}/items/{first}")
    await h.call("DELETE", f"/saved-items/collections/{collection}")
    listing = (await h.call("GET", "/saved-items/all")).json()
    assert listing["total"] == 3
    assert any(row["type"] == "pet_place" and row["unavailable"] for row in listing["items"])
    await h.call("DELETE", "/saved-items/pet_place/bad-id", expected=204)
    assert (await h.call("GET", "/saved-items/all")).json()["total"] == 2


@pytest.mark.asyncio
async def test_account_guard_ownership_and_no_publication_leak(harness: Harness) -> None:
    h = harness
    identifier = (await seed(h))[0]
    collection = await create_list(h)
    await h.call(
        "PUT", f"/saved-items/hotspot/{identifier}?expected_user_id={h.ids[1]}", expected=409
    )
    await h.call(
        "POST",
        f"/saved-items/collections?expected_user_id={h.ids[1]}",
        expected=409,
        json={"name": "Wrong account"},
    )
    await h.call(
        "POST",
        f"/saved-items/collections/{collection}/items?expected_user_id={h.ids[1]}",
        expected=409,
        json={"kind": "hotspot", "id": str(identifier)},
    )
    await h.call("GET", f"/saved-items/all?collection={collection}", actor=1, expected=404)
    await h.call("DELETE", f"/saved-items/collections/{collection}", actor=1, expected=404)
    await h.call("PUT", f"/saved-items/hotspot/{identifier}", expected=201)
    assert not (
        await h.call(
            "POST", "/saved-items/states", actor=1, json={"keys": [f"hotspot:{identifier}"]}
        )
    ).json()["items"][0]["saved"]
    await h.call("DELETE", f"/saved-items/hotspot/{identifier}", actor=1, expected=204)
    assert (await h.call("GET", "/saved-items/all")).json()["total"] == 1


@pytest.mark.asyncio
async def test_hotel_alias_does_not_misclassify_other_services(harness: Harness) -> None:
    h = harness
    async with h.factory() as session:
        session.add(
            TravelServiceConfig(
                id=1,
                data={
                    "public_enabled": True,
                    "enabled_kinds": ["hotel", "tour"],
                    "enabled_destinations": ["tokyo"],
                },
            )
        )
        products = [
            TravelServiceProduct(
                source_key=f"saved:{kind}",
                kind=kind,
                destination_id="tokyo",
                title=f"Reviewed {kind}",
                source_url="https://example.org",
                status="approved",
                verified_at=datetime.now(UTC),
            )
            for kind in ("hotel", "tour")
        ]
        session.add_all(products)
        await session.commit()
        hotel, tour = [product.id for product in products]
    result = (await h.call("PUT", f"/saved-items/hotel/{hotel}", expected=201)).json()
    assert result["key"] == f"service:{hotel}"
    await h.call("PUT", f"/saved-items/service/{hotel}", expected=201)
    await h.call("PUT", f"/saved-items/hotel/{tour}", expected=404)
    await h.call("PUT", f"/saved-items/service/{tour}", expected=201)
    assert (await h.call("GET", "/saved-items/all?type=hotel")).json()["total"] == 1
    plain = (await h.call("GET", "/saved-items/all?type=service")).json()
    assert plain["total"] == 2
    assert "discovery" not in next(row for row in plain["items"] if row["id"] == str(tour))
    async with h.factory() as session:
        assert await session.scalar(select(func.count()).select_from(TravelServiceFavorite)) == 2
        await session.execute(
            update(TravelServiceProduct)
            .where(TravelServiceProduct.id == hotel)
            .values(verified_at=datetime.now(UTC) - timedelta(days=31))
        )
        await session.commit()
    expired = (await h.call("GET", "/saved-items/all?type=hotel")).json()["items"][0]
    assert expired["unavailable"] and "title" not in expired
    await h.call("PUT", f"/saved-items/service/{hotel}", expected=404)
    await h.call("DELETE", f"/saved-items/hotel/{hotel}", expected=204)
    async with h.factory() as session:
        config = await session.get(TravelServiceConfig, 1)
        config.data = {**config.data, "public_enabled": False}
        await session.commit()
    hidden = (await h.call("GET", "/saved-items/all?type=service")).json()["items"]
    assert len(hidden) == 1 and hidden[0]["id"] == str(tour)
    assert hidden[0]["unavailable"] and "title" not in hidden[0] and "href" not in hidden[0]
    await h.call("PUT", f"/saved-items/service/{tour}", expected=404)
    await h.call("DELETE", f"/saved-items/service/{tour}", expected=204)
    assert (await h.call("GET", "/saved-items/all")).json()["total"] == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("place_id", ["ChIJ_Case-Sensitive-ID", "C" * 255])
async def test_restaurant_place_id_is_opaque_not_uuid(harness: Harness, place_id: str) -> None:
    h = harness
    async with h.factory() as session:
        place = RestaurantPlace(
            google_place_id=place_id,
            generated_maps_url="https://www.google.com/maps/search/?api=1&query=place",
        )
        session.add(place)
        await session.commit()
    await h.call("PUT", f"/saved-items/restaurant/{place_id}", expected=201)
    collection = await create_list(h)
    await h.call(
        "POST",
        f"/saved-items/collections/{collection}/items",
        json={"kind": "restaurant", "id": place_id},
    )
    page = (await h.call("GET", "/saved-items/all")).json()
    assert page["total"] == 1 and page["items"][0]["key"] == f"restaurant:{place_id}"
    await h.call("DELETE", f"/saved-items/restaurant/{place_id}", expected=204)
    async with h.factory() as session:
        assert await session.scalar(select(func.count()).select_from(RestaurantFavorite)) == 0


@pytest.mark.asyncio
async def test_inbox_capacity_rollback_keeps_legacy_collection(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    h = harness
    collection = await create_list(h)
    async with h.factory() as session:
        session.add(
            CollectionItem(collection_id=UUID(collection), kind="guide", target=str(uuid4()))
        )
        await session.commit()
    monkeypatch.setattr(service, "MAX_INBOX_ITEMS", 0)
    await h.call("DELETE", f"/saved-items/collections/{collection}", expected=403)
    assert len((await h.call("GET", f"/saved-items/collections/{collection}")).json()["items"]) == 1
    async with h.factory() as session:
        assert (
            await session.scalar(
                select(func.count())
                .select_from(Collection)
                .where(Collection.system_role == "inbox")
            )
            == 0
        )


@pytest.mark.asyncio
async def test_expired_guide_and_rollout_off_keep_reference_not_provider_content(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    monkeypatch.setattr(get_settings(), "discovery_enabled", True)
    identifier = await guide(h)
    await h.call("PUT", f"/saved-items/guide/{identifier}", expected=201)
    async with h.factory() as session:
        await session.execute(
            update(HotspotGuide)
            .where(HotspotGuide.id == identifier)
            .values(metadata_expires_at=datetime.now(UTC) - timedelta(days=1))
        )
        await session.commit()
    assert (await h.call("GET", "/saved-items/all")).json()["items"][0]["unavailable"]
    await h.call("PUT", f"/saved-items/guide/{identifier}", expected=404)
    monkeypatch.setattr(get_settings(), "discovery_enabled", False)
    assert (await h.call("GET", "/saved-items/all")).json()["items"][0]["unavailable"]
    await h.call("DELETE", f"/saved-items/guide/{identifier}", expected=204)


@pytest.mark.asyncio
async def test_organize_failure_rolls_back_new_base_and_analytics(
    harness: Harness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    h = harness
    monkeypatch.setattr(get_settings(), "discovery_enabled", True)
    identifier = await guide(h)
    collection = await create_list(h)
    async with h.factory() as session:
        session.add_all(
            CollectionItem(collection_id=UUID(collection), kind="guide", target=str(uuid4()))
            for _ in range(500)
        )
        await session.commit()
    await h.call(
        "POST",
        f"/saved-items/collections/{collection}/items",
        expected=403,
        json={"kind": "guide", "id": str(identifier)},
    )
    async with h.factory() as session:
        assert (
            await session.scalar(
                select(func.count())
                .select_from(Collection)
                .where(Collection.system_role == "inbox")
            )
            == 0
        )
        assert await session.scalar(select(func.count()).select_from(CollectionItem)) == 500


@pytest.mark.asyncio
async def test_saved_aliases_are_deduplicated_before_any_state_and_collection_filter(
    harness: Harness,
) -> None:
    h = harness
    collection = await create_list(h)
    identifier = uuid4()
    async with h.factory() as session:
        session.add_all(
            [
                CollectionItem(
                    collection_id=UUID(collection), kind="hotel", target=identifier.hex.upper()
                ),
                CollectionItem(
                    collection_id=UUID(collection), kind="service", target=str(identifier)
                ),
            ]
        )
        await session.commit()
    state = (
        await h.call(
            "POST",
            "/saved-items/states",
            json={"keys": [f"hotel:{identifier}", f"service:{identifier.hex.upper()}"]},
        )
    ).json()["items"]
    assert state == [
        {"key": f"service:{identifier}", "saved": True, "collection_ids": [collection]}
    ]
    listing = (await h.call("GET", f"/saved-items/all?collection={collection}")).json()
    assert listing["total"] == 1 and listing["items"][0]["unavailable"]
    await h.call("DELETE", f"/saved-items/hotel/{identifier}", expected=204)
    assert (await h.call("GET", "/saved-items/all")).json()["total"] == 0


@pytest.mark.parametrize(
    "key", ["saved_account_changed", "saved_item_limit", "saved_cursor_invalid"]
)
def test_new_saved_errors_have_five_locale_copy(key: str) -> None:
    from app.i18n import ERROR_DETAILS, LOCALES

    assert service.failure(key).detail == ERROR_DETAILS["zh-TW"][key]
    assert all(ERROR_DETAILS[locale][key] != key for locale in LOCALES)
