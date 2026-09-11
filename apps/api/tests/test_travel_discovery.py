from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import httpx
import pytest
import pytest_asyncio
from fastapi import Depends, FastAPI, Header
from sqlalchemy import event, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user, optional_current_user
from app.community.models import (
    Collection,
    CollectionItem,
    Media,
    Post,
    PostRevision,
    Profile,
    Relationship,
)
from app.config import Settings
from app.db import Base, get_session
from app.discovery.models import DiscoveryDismissal, DiscoveryPreference
from app.discovery.preferences import erase_preferences, update_preferences
from app.discovery.router import router
from app.discovery.schemas import PreferenceInput
from app.discovery.service import resolve_discovery_items
from app.models import (
    FoodDestination,
    FoodLocalization,
    FoodMerchant,
    FoodMerchantSource,
    HotspotFavorite,
    HotspotGuide,
    HotspotLocalization,
    ProviderConfig,
    TravelFood,
    TravelHotspot,
    TravelServiceConfig,
    TravelServiceProduct,
    User,
)
from app.problems import AppError, app_error_handler


class MemoryRedis:
    def __init__(self):
        self.values = {}

    async def get(self, key):
        return self.values.get(key)

    async def set(self, key, value, *, ex):
        assert ex == 300
        self.values[key] = value


@pytest_asyncio.fixture
async def harness(monkeypatch) -> AsyncIterator[Any]:
    engine = create_async_engine("sqlite+aiosqlite://")

    @event.listens_for(engine.sync_engine, "connect")
    def sqlite_functions(connection, _):
        connection.create_function("btrim", 1, lambda value: value.strip() if value else value)
        connection.execute("PRAGMA foreign_keys=ON")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    ids = [uuid4(), uuid4()]
    async with factory() as session:
        session.add_all([User(id=value, email=f"{value}@example.com") for value in ids])
        await session.commit()
    settings = Settings(discovery_enabled=True, community_enabled=False)
    redis = MemoryRedis()
    for module in ("router", "service"):
        monkeypatch.setattr(f"app.discovery.{module}.get_settings", lambda: settings)
    monkeypatch.setattr("app.discovery.service.get_redis", lambda: redis)
    monkeypatch.setattr("app.community.collections.rate", AsyncMock())
    monkeypatch.setattr("app.analytics.service.record_event", AsyncMock())

    async def database():
        async with factory() as session:
            yield session

    async def optional(
        session: Annotated[AsyncSession, Depends(get_session)],
        x_test_user: Annotated[str | None, Header()] = None,
    ):
        return await session.get(User, UUID(x_test_user)) if x_test_user else None

    async def required(user: Annotated[User | None, Depends(optional)]):
        if not user:
            raise AppError(401, "authentication_required", "Sign in")
        return user

    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    app.add_exception_handler(AppError, app_error_handler)
    app.dependency_overrides[get_session] = database
    app.dependency_overrides[current_user] = required
    app.dependency_overrides[optional_current_user] = optional
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
        headers={"X-Travel-Locale": "en"},
    ) as client:
        yield client, factory, ids, settings, redis
    await engine.dispose()


def hotspot(name="Temple", city="tokyo", **kwargs):
    return TravelHotspot(
        slug=uuid4().hex,
        name=name,
        destination_id=city,
        city_code="NRT",
        city_name=city,
        country_code="JP",
        country_name="Japan",
        category="culture",
        search_text=name,
        **kwargs,
    )


async def seed_hotspots(factory, count=3):
    async with factory() as session:
        rows = [
            hotspot(f"Temple {i}", updated_at=datetime.now(UTC) - timedelta(hours=i))
            for i in range(count)
        ]
        session.add_all(rows)
        await session.commit()
        return [row.id for row in rows]


@pytest.mark.asyncio
async def test_default_off_status_and_every_endpoint_fail_closed(harness):
    client, _, ids, settings, _ = harness
    settings.discovery_enabled = False
    status = await client.get("/api/v1/discovery/status")
    assert status.json() == {"enabled": False}
    assert status.headers["cache-control"] == "no-store"
    for path in (
        "search",
        "feed",
        "suggestions",
        "preferences",
        "collections",
        f"content/hotspot/{uuid4()}",
    ):
        response = await client.get(
            f"/api/v1/discovery/{path}", headers={"X-Test-User": str(ids[0])}
        )
        assert response.status_code == 503, response.text
        assert response.json()["code"] == "discovery_unavailable"
    assert Settings().discovery_enabled is False


@pytest.mark.asyncio
async def test_alias_literal_search_visibility_and_selection(harness):
    client, factory, _, _, _ = harness
    async with factory() as session:
        public = hotspot("淺草寺", map_match_status="verified")
        pending = hotspot("Secret Temple", review_status="pending")
        inactive = hotspot("Inactive Temple", is_active=False)
        session.add_all([public, pending, inactive])
        await session.flush()
        session.add(
            HotspotLocalization(
                hotspot_id=public.id,
                locale="en",
                name="Sensoji",
                aliases=["Asakusa Temple"],
                search_terms=[],
            )
        )
        await session.commit()
    result = await client.get(
        "/api/v1/discovery/search", params={"q": "Asakusa", "locale": "en", "type": "hotspot"}
    )
    assert result.status_code == 200, result.text
    item = result.json()["items"][0]
    assert item["title"] == "Sensoji"
    assert item["place_ref"]["selection_path"] == f"/hotspots/{public.id}/trip-selections"
    assert item["collection_ref"] == {"kind": "hotspot", "id": str(public.id)}
    assert (await client.get("/api/v1/discovery/search", params={"q": "%"})).json()["items"] == []
    assert (
        len((await client.get("/api/v1/discovery/search", params={"q": "Tokyo"})).json()["items"])
        == 1
    )
    async with factory() as session:
        session.add(ProviderConfig(provider="layout", config={"hotspots_enabled": False}))
        await session.commit()
    assert (await client.get(f"/api/v1/discovery/content/hotspot/{public.id}")).status_code == 404


@pytest.mark.asyncio
async def test_pagination_reauthorizes_hidden_deleted_and_reader_filters(harness):
    client, factory, ids, _, redis = harness
    places = await seed_hotspots(factory, 4)
    first = (await client.get("/api/v1/discovery/search", params={"limit": 1})).json()
    cursor = first["next_cursor"]
    assert first["items"][0]["id"] == f"hotspot:{places[0]}"
    async with factory() as session:
        row = await session.get(TravelHotspot, places[1])
        row.review_status = "disabled"
        await session.commit()
    second = await client.get("/api/v1/discovery/search", params={"limit": 2, "cursor": cursor})
    assert [item["id"] for item in second.json()["items"]] == [
        f"hotspot:{value}" for value in places[2:]
    ]
    for params, headers in (({"q": "other"}, {}), ({}, {"X-Test-User": str(ids[0])})):
        response = await client.get(
            "/api/v1/discovery/search", params={"cursor": cursor, **params}, headers=headers
        )
        assert response.status_code == 422
    assert all("Temple" not in value and "@example" not in value for value in redis.values.values())
    redis.values.clear()
    assert (
        await client.get("/api/v1/discovery/search", params={"cursor": cursor})
    ).status_code == 409


@pytest.mark.asyncio
async def test_preferences_version_reset_dismiss_and_private_isolation(harness):
    client, factory, ids, _, _ = harness
    places = await seed_hotspots(factory)
    headers = {"X-Test-User": str(ids[0])}
    path = "/api/v1/discovery/preferences"
    assert (await client.get(path)).status_code == 401
    assert (await client.get(path, headers=headers)).json()["version"] == 0
    payload = {
        "version": 0,
        "destinations": ["tokyo"],
        "topics": ["culture"],
        "include_saved": True,
    }
    result = await client.put(path, json=payload, headers=headers)
    assert result.status_code == 200, result.text
    assert result.json()["version"] == 1
    assert (await client.put(path, json=payload, headers=headers)).status_code == 409
    assert (await client.get(path, headers={"X-Test-User": str(ids[1])})).json()[
        "destinations"
    ] == []
    dismissed = await client.post(
        "/api/v1/discovery/dismiss", json={"id": f"hotspot:{places[0]}"}, headers=headers
    )
    assert dismissed.status_code == 200, dismissed.text
    items = (await client.get("/api/v1/discovery/feed", headers=headers)).json()["items"]
    assert len(items) == 2 and items[0]["recommendation_reason"] == "destination_interest"
    reset = await client.delete(path, params={"version": 1}, headers=headers)
    assert reset.json()["version"] == 2 and reset.json()["destinations"] == []
    assert len((await client.get("/api/v1/discovery/feed", headers=headers)).json()["items"]) == 3
    assert (await client.put(path, json=payload, headers=headers)).status_code == 409
    async with factory() as session:
        await erase_preferences(session, ids[0])
        await session.commit()
        assert await session.get(DiscoveryPreference, ids[0]) is None
        assert list(await session.scalars(select(DiscoveryDismissal))) == []


@pytest.mark.asyncio
async def test_public_guides_freshness_unsafe_sources_no_fake_embed(harness):
    client, factory, _, _, _ = harness
    async with factory() as session:
        place = hotspot()
        session.add(place)
        await session.flush()
        now = datetime.now(UTC)
        fresh = HotspotGuide(
            hotspot_id=place.id,
            content_type="video",
            provider="youtube",
            locale="en",
            title="Verified video",
            creator_name="Fixture publisher",
            canonical_url="https://www.youtube.com/watch?v=abcdefghijk",
            provider_content_id="abcdefghijk",
            review_status="approved",
            last_verified_at=now,
            metadata_expires_at=now + timedelta(days=7),
            metadata_json={},
        )
        stale = HotspotGuide(
            hotspot_id=place.id,
            content_type="video",
            provider="youtube",
            locale="en",
            title="Stale video",
            creator_name="Fixture publisher",
            canonical_url="https://www.youtube.com/watch?v=bcdefghijkl",
            provider_content_id="bcdefghijkl",
            review_status="approved",
            last_verified_at=now - timedelta(days=31),
            metadata_expires_at=now - timedelta(days=1),
        )
        unsafe = HotspotGuide(
            hotspot_id=place.id,
            content_type="article",
            provider="manual",
            locale="en",
            title="Unsafe",
            creator_name="Fixture publisher",
            canonical_url="https://127.0.0.1/private",
            review_status="approved",
        )
        session.add_all([fresh, stale, unsafe])
        await session.commit()
    items = (
        await client.get("/api/v1/discovery/search", params={"type": "video", "locale": "en"})
    ).json()["items"]
    assert len(items) == 1
    assert items[0]["video"]["status"] == "link_only" and items[0]["thumbnail_url"] is None
    assert (await client.get(f"/api/v1/discovery/content/article/{fresh.id}")).status_code == 404
    assert (await client.get(f"/api/v1/discovery/content/video/{fresh.id}")).status_code == 200
    assert (await client.get(f"/api/v1/discovery/content/article/{unsafe.id}")).status_code == 404
    async with factory() as session:
        row = await session.get(HotspotGuide, fresh.id)
        row.metadata_json = {"youtube_status": {"embeddable": True, "privacyStatus": "public"}}
        await session.commit()
    detail = (await client.get(f"/api/v1/discovery/content/video/{fresh.id}")).json()
    assert detail["video"]["embed_url"] == "https://www.youtube-nocookie.com/embed/abcdefghijk"


@pytest.mark.asyncio
async def test_food_merchant_hotel_existing_publication_contracts(harness):
    client, factory, _, _, _ = harness
    async with factory() as session:
        food = TravelFood(
            slug="ramen",
            local_name="拉麵",
            romanized_name="Ramen",
            country_code="JP",
            food_kind="noodle_soup",
            search_text="ramen",
        )
        merchant = FoodMerchant(
            slug="ramen-shop",
            is_active=True,
            name="Ramen Shop",
            local_name="店",
            destination_id="tokyo",
            country_code="JP",
            review_status="approved",
            map_match_status="verified",
            google_place_id="exact-place",
            latitude=35,
            longitude=139,
            coordinate_source_type="merchant_official",
            coordinate_source_url="https://example.com/map",
        )
        hotel = TravelServiceProduct(
            # A public identifier may legitimately contain the private-price digits.
            id=UUID("99900000-0000-4000-8000-000000000001"),
            source_key="test:hotel",
            kind="hotel",
            destination_id="tokyo",
            title="Reviewed hotel",
            source_url="https://example.com/hotel",
            status="approved",
            verified_at=datetime.now(UTC),
            facts={"reference_price": 999},
        )
        session.add_all([food, merchant, hotel])
        await session.flush()
        session.add_all(
            [
                FoodLocalization(
                    food_id=food.id, locale="en", name="Ramen", summary="Soup noodles"
                ),
                FoodDestination(food_id=food.id, destination_id="tokyo"),
                TravelServiceConfig(
                    id=1,
                    data={
                        "public_enabled": True,
                        "enabled_kinds": ["hotel"],
                        "enabled_destinations": ["tokyo"],
                    },
                ),
            ]
        )
        await session.commit()
    result = await client.get(
        "/api/v1/discovery/search", params={"locale": "en", "destination": "Tokyo"}
    )
    assert result.status_code == 200, result.text
    payload = result.json()
    assert {item["kind"] for item in payload["items"]} == {"food", "hotel"}
    public_hotel = next(item for item in payload["items"] if item["kind"] == "hotel")
    assert public_hotel["id"] == f"hotel:{hotel.id}"

    def assert_no_private_price(value: Any) -> None:
        # Inspect fields and whole scalar values, not substrings of timestamps/UUIDs.
        if isinstance(value, dict):
            assert "reference_price" not in value
            for child in value.values():
                assert_no_private_price(child)
        elif isinstance(value, list):
            for child in value:
                assert_no_private_price(child)
        else:
            assert value not in (999, "999")

    assert_no_private_price(payload)
    async with factory() as session:
        session.add(
            FoodMerchantSource(
                merchant_id=merchant.id,
                source_url="https://example.com/review",
                source_type="merchant_official",
                source_title="Official merchant",
                is_current=True,
            )
        )
        await session.commit()
    merchant_result = await client.get("/api/v1/discovery/search", params={"type": "merchant"})
    assert len(merchant_result.json()["items"]) == 1, merchant_result.text
    async with factory() as session:
        row = await session.get(TravelServiceProduct, hotel.id)
        row.verified_at = datetime.now(UTC) - timedelta(days=31)
        await session.commit()
    assert (await client.get(f"/api/v1/discovery/content/hotel/{hotel.id}")).status_code == 404


@pytest.mark.asyncio
async def test_public_post_current_revision_blocks_and_following(harness):
    client, factory, ids, _, _ = harness
    async with factory() as session:
        session.add(ProviderConfig(provider="community", config={"enabled": True}))
        session.add(Profile(user_id=ids[1], handle="author", display_name="Author"))
        post = Post(author_id=ids[1], state="published", published_at=datetime.now(UTC))
        session.add(post)
        await session.flush()
        photo = Media(
            owner_id=ids[1],
            object_key="private/original",
            thumbnail_key="private/thumbnail",
            width=800,
            height=600,
            size=20,
            alt="Published travel photo",
        )
        draft_photo = Media(
            owner_id=ids[1],
            object_key="private/draft",
            thumbnail_key="private/draft-thumbnail",
            width=800,
            height=600,
            size=20,
            alt="Unpublished draft",
        )
        session.add_all([photo, draft_photo])
        await session.flush()
        revision = PostRevision(
            post_id=post.id,
            title="Public Kyoto",
            body="Public snapshot only",
            locale="en",
            destination="京都",
            kind="itinerary",
            topics=["culture"],
            itinerary={"title": "Public route", "days": []},
            media_ids=[str(photo.id)],
        )
        session.add(revision)
        await session.flush()
        post.published_revision_id = revision.id
        session.add(Relationship(actor_id=ids[0], target_id=ids[1], kind="follow"))
        await session.commit()
    headers = {"X-Test-User": str(ids[0])}
    assert (
        await client.get("/api/v1/discovery/feed", params={"mode": "following"})
    ).status_code == 401
    result = await client.get(
        "/api/v1/discovery/feed", params={"mode": "following", "locale": "en"}, headers=headers
    )
    assert result.status_code == 200, result.text
    assert result.json()["items"][0]["kind"] == "itinerary"
    assert result.json()["items"][0]["content"]["media"] == [
        {"id": str(photo.id), "alt": "Published travel photo", "width": 800, "height": 600}
    ]
    assert "private/original" not in result.text and str(draft_photo.id) not in result.text
    async with factory() as session:
        image = await session.get(Media, photo.id)
        image.deleted_at = datetime.now(UTC)
        await session.commit()
    after_delete = await client.get(
        f"/api/v1/discovery/content/itinerary/{post.id}", headers=headers
    )
    assert after_delete.json()["content"]["media"] == []
    async with factory() as session:
        session.add(Relationship(actor_id=ids[1], target_id=ids[0], kind="block"))
        await session.commit()
    assert (
        await client.get(f"/api/v1/discovery/content/itinerary/{post.id}", headers=headers)
    ).status_code == 404


@pytest.mark.asyncio
async def test_collections_without_social_profile_reauthorize_and_private(harness):
    client, factory, ids, _, _ = harness
    places = await seed_hotspots(factory, 1)
    headers = {"X-Test-User": str(ids[0])}
    created = await client.post(
        "/api/v1/discovery/collections", json={"name": "Private ideas"}, headers=headers
    )
    assert created.status_code == 200, created.text
    path = "/api/v1/discovery/collections/" + created.json()["id"]
    saved = await client.post(
        path + "/items", json={"kind": "hotspot", "id": str(places[0])}, headers=headers
    )
    assert saved.status_code == 200, saved.text
    assert (await client.get(path, headers={"X-Test-User": str(ids[1])})).status_code == 404
    assert (await client.get(path, headers=headers)).json()["items"][0]["discovery"][
        "id"
    ] == f"hotspot:{places[0]}"
    async with factory() as session:
        row = await session.get(TravelHotspot, places[0])
        row.is_active = False
        await session.commit()
    assert (await client.get(path, headers=headers)).json()["items"][0]["unavailable"] is True


@pytest.mark.asyncio
async def test_saved_interest_only_explicit_and_resolver_bounded(harness):
    client, factory, ids, _, _ = harness
    places = await seed_hotspots(factory)
    async with factory() as session:
        session.add(HotspotFavorite(user_id=ids[0], hotspot_id=places[-1]))
        await session.commit()
        user = await session.get(User, ids[0])
        with pytest.raises(AppError):
            await resolve_discovery_items(session, [f"hotspot:{places[0]}"] * 101, user, "en")
    headers = {"X-Test-User": str(ids[0])}
    first = (await client.get("/api/v1/discovery/feed", headers=headers)).json()["items"]
    assert {item["recommendation_reason"] for item in first} == {"latest"}
    await client.put(
        "/api/v1/discovery/preferences", headers=headers, json={"version": 0, "include_saved": True}
    )
    second = (await client.get("/api/v1/discovery/feed", headers=headers)).json()["items"]
    assert {item["recommendation_reason"] for item in second} == {"saved_interest"}


@pytest.mark.asyncio
async def test_account_erasure_wins_over_cached_authenticated_user(harness):
    _, factory, ids, _, _ = harness
    async with factory() as session:
        user = await session.get(User, ids[0])
        assert user.is_active
        await session.execute(
            update(User)
            .where(User.id == ids[0])
            .values(is_active=False, deleted_at=datetime.now(UTC))
            .execution_options(synchronize_session=False)
        )
        assert user.is_active  # Simulate authentication's stale identity map.
        with pytest.raises(AppError) as error:
            await update_preferences(session, ids[0], PreferenceInput(version=0, topics=["food"]))
        assert error.value.status == 401
        assert await session.get(DiscoveryPreference, ids[0]) is None


@pytest.mark.asyncio
async def test_explicit_interests_and_topics_are_applied_before_candidate_limit(harness):
    client, factory, ids, _, _ = harness
    async with factory() as session:
        recent = [hotspot(f"Recent {i}") for i in range(105)]
        older = hotspot("Older Kyoto", "kyoto", updated_at=datetime.now(UTC) - timedelta(days=30))
        older.category = "nature"
        session.add_all([*recent, older])
        await session.commit()
    headers = {"X-Test-User": str(ids[0])}
    response = await client.get("/api/v1/discovery/search", params={"topic": "nature"})
    assert [row["id"] for row in response.json()["items"]] == [f"hotspot:{older.id}"]
    await client.put(
        "/api/v1/discovery/preferences",
        headers=headers,
        json={"version": 0, "destinations": ["kyoto"]},
    )
    response = await client.get("/api/v1/discovery/feed", headers=headers)
    assert response.json()["items"][0]["id"] == f"hotspot:{older.id}"


@pytest.mark.asyncio
async def test_expired_video_window_cannot_starve_fresh_metadata(harness):
    client, factory, _, _, _ = harness
    async with factory() as session:
        place = hotspot()
        session.add(place)
        await session.flush()
        now = datetime.now(UTC)
        for index in range(105):
            session.add(
                HotspotGuide(
                    hotspot_id=place.id,
                    content_type="video",
                    provider="youtube",
                    locale="en",
                    title=f"Expired {index}",
                    creator_name="Fixture",
                    canonical_url=f"https://www.youtube.com/watch?v={index:011d}",
                    review_status="approved",
                    last_verified_at=now - timedelta(days=31),
                    metadata_expires_at=now - timedelta(days=1),
                )
            )
        fresh = HotspotGuide(
            hotspot_id=place.id,
            content_type="video",
            provider="youtube",
            locale="ja",
            title="Fresh Japanese source",
            creator_name="Fixture",
            canonical_url="https://www.youtube.com/watch?v=abcdefghijk",
            review_status="approved",
            last_verified_at=now,
            metadata_expires_at=now + timedelta(days=7),
            updated_at=now - timedelta(days=2),
        )
        session.add(fresh)
        await session.commit()
    response = await client.get("/api/v1/discovery/search", params={"type": "video"})
    assert [row["id"] for row in response.json()["items"]] == [f"guide:{fresh.id}"]
    assert response.json()["items"][0]["locale"] == "ja"
    assert (
        await client.get("/api/v1/discovery/search", params={"type": "video", "locale": "en"})
    ).json()["items"] == []


@pytest.mark.asyncio
async def test_suggestions_real_labels_header_locale_and_no_blank_collection(harness):
    client, factory, ids, _, _ = harness
    async with factory() as session:
        place = hotspot()
        session.add(place)
        await session.flush()
        session.add(
            HotspotLocalization(
                hotspot_id=place.id, locale="ja", name="本物の寺", aliases=[], search_terms=[]
            )
        )
        await session.commit()
    response = await client.get(
        "/api/v1/discovery/search", params={"type": "hotspot"}, headers={"X-Travel-Locale": "ja"}
    )
    assert response.json()["items"][0]["title"] == "本物の寺"
    assert response.json()["items"][0]["href"].startswith("/ja/")
    suggestions = await client.get(
        "/api/v1/discovery/suggestions", headers={"X-Travel-Locale": "en"}
    )
    assert suggestions.json()["items"] == []
    assert {"id": "culture", "label": "Culture"} in suggestions.json()["topics"]
    assert (
        await client.post(
            "/api/v1/discovery/collections",
            headers={"X-Test-User": str(ids[0])},
            json={"name": "   "},
        )
    ).status_code == 422


@pytest.mark.asyncio
async def test_search_metrics_keep_only_coarse_result_facts(harness, monkeypatch):
    client, _, _, _, _ = harness
    record = AsyncMock(return_value=False)
    monkeypatch.setattr("app.analytics.service.record_event", record)
    response = await client.get(
        "/api/v1/discovery/search", params={"q": "private search phrase", "type": "hotspot"}
    )
    assert response.status_code == 200
    assert [call.args[1] for call in record.call_args_list] == [
        "discovery_search",
        "discovery_empty",
    ]
    assert record.call_args_list[0].kwargs["properties"] == {"kind": "hotspot", "result_count": 0}
    assert "private search phrase" not in str(record.call_args_list)


@pytest.mark.asyncio
async def test_saved_count_is_public_and_orders_its_own_mode(harness):
    client, factory, ids, _, _ = harness
    newest, middle, oldest = await seed_hotspots(factory, 3)
    async with factory() as session:
        third = User(id=uuid4(), email=f"{uuid4()}@example.com")
        session.add(third)
        session.add_all(
            [
                HotspotFavorite(user_id=ids[0], hotspot_id=oldest),
                HotspotFavorite(user_id=ids[1], hotspot_id=oldest),
                HotspotFavorite(user_id=ids[0], hotspot_id=middle),
            ]
        )
        await session.flush()
        # The same account organizing its own save must not count twice.
        named = Collection(user_id=ids[0], name="Kyoto shortlist")
        session.add(named)
        await session.flush()
        session.add(CollectionItem(collection_id=named.id, kind="hotspot", target=str(middle)))
        await session.commit()

    latest = await client.get("/api/v1/discovery/feed", params={"mode": "latest"})
    assert latest.status_code == 200, latest.text
    assert [item["id"] for item in latest.json()["items"]] == [
        f"hotspot:{value}" for value in (newest, middle, oldest)
    ]
    # Anonymous readers see the count in every mode, not only on the ranking tab.
    assert [item["saved_count"] for item in latest.json()["items"]] == [0, 1, 2]

    ranked = await client.get("/api/v1/discovery/feed", params={"mode": "most_saved"})
    assert ranked.status_code == 200, ranked.text
    assert [item["id"] for item in ranked.json()["items"]] == [
        f"hotspot:{value}" for value in (oldest, middle, newest)
    ]
    assert [item["saved_count"] for item in ranked.json()["items"]] == [2, 1, 0]
    assert [item["recommendation_reason"] for item in ranked.json()["items"]] == [None] * 3

    detail = await client.get(f"/api/v1/discovery/content/hotspot/{oldest}")
    assert detail.status_code == 200, detail.text
    assert detail.json()["saved_count"] == 2
    assert (
        await client.get("/api/v1/discovery/search", params={"mode": "most_saved", "q": "Temple"})
    ).status_code == 200


@pytest.mark.asyncio
async def test_saved_count_reads_guides_that_only_exist_in_a_collection(harness):
    client, factory, ids, _, _ = harness
    async with factory() as session:
        place = hotspot("Guided temple", map_match_status="verified")
        session.add(place)
        await session.flush()
        guide = HotspotGuide(
            hotspot_id=place.id,
            content_type="article",
            provider="editorial",
            locale="en",
            title="Walking the temple district",
            creator_name="Fixture publisher",
            canonical_url="https://example.org/walk",
            review_status="approved",
            last_verified_at=datetime.now(UTC),
            metadata_json={},
        )
        session.add(guide)
        inbox = Collection(user_id=ids[0], name="Saved references", system_role="inbox")
        other = Collection(user_id=ids[1], name="Reading list")
        session.add_all([inbox, other])
        await session.flush()
        # Guides have no typed favorite table, so the collection rows are the only source.
        # The dashed and bare spellings both normalize to one reference.
        session.add_all(
            [
                CollectionItem(collection_id=inbox.id, kind="guide", target=str(guide.id)),
                CollectionItem(collection_id=other.id, kind="article", target=guide.id.hex),
            ]
        )
        await session.commit()

    result = await client.get(
        "/api/v1/discovery/feed", params={"mode": "most_saved", "type": "article"}
    )
    assert result.status_code == 200, result.text
    items = result.json()["items"]
    assert [item["id"] for item in items] == [f"guide:{guide.id}"]
    assert items[0]["saved_count"] == 2
