"""Public navigation groups and lazy, reauthorized planning detail contracts."""

from datetime import UTC, date, datetime, timedelta
from unittest.mock import AsyncMock
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

import httpx
import pytest
from sqlalchemy import update
from test_travel_discovery import harness as harness
from test_travel_discovery import hotspot

from app.models import (
    FoodDestination,
    FoodLocalization,
    FoodMerchant,
    FoodMerchantFood,
    FoodMerchantPlatformLink,
    FoodMerchantSource,
    HotelBookingOption,
    HotspotGuide,
    HotspotIntro,
    HotspotPlaceProfile,
    ProviderConfig,
    TravelFood,
    TravelServiceConfig,
    TravelServiceProduct,
    TripPlan,
)


def food(name="Fixture ramen"):
    return TravelFood(
        slug=uuid4().hex,
        local_name=name,
        romanized_name=name,
        country_code="JP",
        food_kind="noodle_soup",
        search_text=name,
    )


@pytest.mark.asyncio
async def test_trip_options_resolve_catalog_identity_without_exposing_private_data(
    harness, monkeypatch
):
    from app.trips.router import router as trips_router

    client, factory, users, _, _ = harness
    client._transport.app.include_router(trips_router, prefix="/api/v1")
    limit = AsyncMock(return_value=20)
    monkeypatch.setattr("app.trips.router.limit_for", limit)

    def trip(name, destination_name=None, data=None, **overrides):
        return TripPlan(
            **({
                "user_id": users[0],
                "name": name,
                "mode": "manual",
                "total_price": 0,
                "destination_name": destination_name,
                "data": data or {},
                "start_date": date(2026, 11, 11),
                "end_date": date(2026, 11, 13),
                "version": 4,
            } | overrides)
        )

    async with factory() as session:
        session.add_all([
            trip("Chinese trip", "東京", {"notes": "Private notes"}),
            trip("Airport alias", "NRT"),
            trip("Canonical snapshot", "東京", {"destination_id": "seoul"}),
            trip("Legacy snapshot", data={"destination_city": "Tokyo"}),
            trip("Unknown", "A private place", {"destination_id": {"invalid": True}}),
            trip("Undated", "東京", start_date=None, end_date=None),
            trip("Other member", "東京", user_id=users[1]),
        ])
        await session.commit()

    assert (await client.get("/api/v1/trips/options")).status_code == 401
    response = await client.get(
        "/api/v1/trips/options", headers={"X-Test-User": str(users[0])}
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert {item["name"]: item["destination_id"] for item in payload["items"]} == {
        "Chinese trip": "tokyo",
        "Airport alias": "tokyo",
        "Canonical snapshot": "seoul",
        "Legacy snapshot": "tokyo",
        "Unknown": None,
    }
    assert payload["count"] == 6
    assert payload["undated_count"] == 1
    assert payload["can_create"] is True
    assert payload["limit"] == 20
    assert "Private notes" not in response.text
    assert all("data" not in item and item["version"] == 4 for item in payload["items"])
    limit.assert_awaited_once()


def merchant(name="Fixture restaurant", **overrides):
    values = {
        "slug": uuid4().hex,
        "name": name,
        "local_name": name,
        "destination_id": "tokyo",
        "country_code": "JP",
        "review_status": "approved",
        "is_active": True,
        "map_match_status": "verified",
        "google_place_id": f"exact-fixture-{uuid4().hex}",
        "latitude": 35.68,
        "longitude": 139.76,
        "coordinate_source_type": "merchant_official",
        "coordinate_source_url": "https://example.com/location",
    }
    return FoodMerchant(**(values | overrides))


def guide(place, title="Fixture article", **overrides):
    values = {
        "hotspot_id": place.id,
        "content_type": "article",
        "provider": "manual",
        "locale": "en",
        "title": title,
        "summary": "Reviewed source text",
        "creator_name": "Fixture publisher",
        "canonical_url": f"https://example.com/{uuid4()}",
        "review_status": "approved",
    }
    return HotspotGuide(**(values | overrides))


async def seed_types(factory):
    async with factory() as session:
        place, dish, restaurant = hotspot(), food(), merchant()
        hotel = TravelServiceProduct(
            source_key=uuid4().hex,
            kind="hotel",
            destination_id="tokyo",
            title="Fixture hotel",
            source_url="https://example.com/hotel",
            status="approved",
            verified_at=datetime.now(UTC),
            facts={},
        )
        session.add_all([place, dish, restaurant, hotel])
        await session.flush()
        article = guide(place)
        video = guide(place, "Fixture video", content_type="video")
        session.add_all(
            [
                article,
                video,
                FoodDestination(food_id=dish.id, destination_id="tokyo"),
                FoodLocalization(
                    food_id=dish.id, locale="en", name=dish.local_name, summary="Ramen"
                ),
                FoodMerchantSource(
                    merchant_id=restaurant.id,
                    source_url="https://example.com/restaurant",
                    source_type="merchant_official",
                    source_title="Official",
                    is_current=True,
                ),
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
        return place, dish, restaurant, hotel, article, video


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint", ["search", "feed"])
async def test_categories_intersect_legacy_types_before_pagination(harness, endpoint):
    client, factory, _, _, _ = harness
    await seed_types(factory)
    path = f"/api/v1/discovery/{endpoint}"
    expected = {
        "all": {"hotspot", "food", "merchant", "hotel", "article", "video"},
        "hotspots": {"hotspot"},
        "foods": {"food", "merchant"},
        "hotels": {"hotel"},
        "guides": {"article", "video"},
    }
    for category, kinds in expected.items():
        response = await client.get(path, params={"category": category, "limit": 1})
        assert response.status_code == 200, response.text
        result, found = response.json(), []
        while True:
            assert result["filters"]["category"] == category
            found.extend(item["kind"] for item in result["items"])
            if not result["next_cursor"]:
                break
            result = (
                await client.get(
                    path,
                    params={
                        "category": category,
                        "limit": 1,
                        "cursor": result["next_cursor"],
                    },
                )
            ).json()
        assert set(found) == kinds
        assert all(item["detail"] is None for item in response.json()["items"])
    narrowed = await client.get(path, params={"category": "foods", "type": "merchant"})
    assert [item["kind"] for item in narrowed.json()["items"]] == ["merchant"]
    mismatch = await client.get(path, params={"category": "foods", "type": "hotel"})
    assert mismatch.json()["items"] == [] and mismatch.json()["next_cursor"] is None
    assert (await client.get(path, params={"category": "unknown"})).status_code == 422
    assert {item["kind"] for item in (await client.get(path)).json()["items"]} == expected["all"]


@pytest.mark.asyncio
async def test_group_before_candidate_limit_cursor_binding_and_live_withdrawal(harness):
    client, factory, _, _, _ = harness
    async with factory() as session:
        place = hotspot()
        session.add(place)
        await session.flush()
        videos = [
            guide(
                place,
                "Older film",
                content_type="video",
                updated_at=datetime.now(UTC) - timedelta(days=i + 2),
            )
            for i in range(2)
        ]
        session.add_all([*videos, *[guide(place, f"New story {i}") for i in range(101)]])
        await session.commit()
    params = {"category": "guides", "type": "video", "limit": 1}
    first = (await client.get("/api/v1/discovery/search", params=params)).json()
    assert first["items"][0]["id"] == f"guide:{videos[0].id}"
    cursor = first["next_cursor"]
    assert cursor
    assert (
        await client.get(
            "/api/v1/discovery/search",
            params={
                **params,
                "category": "all",
                "cursor": cursor,
            },
        )
    ).status_code == 422
    async with factory() as session:
        await session.execute(
            update(HotspotGuide)
            .where(HotspotGuide.id == videos[1].id)
            .values(review_status="rejected")
        )
        await session.commit()
    second = (
        await client.get(
            "/api/v1/discovery/search",
            params={
                **params,
                "cursor": cursor,
            },
        )
    ).json()
    assert second["items"] == [] and second["next_cursor"] is None


@pytest.mark.asyncio
async def test_suggestions_group_and_following_auth_not_weakened(harness):
    client, factory, _, _, _ = harness
    await seed_types(factory)
    result = (
        await client.get(
            "/api/v1/discovery/suggestions",
            params={
                "category": "foods",
                "q": "Fixture",
            },
        )
    ).json()
    assert {item["label"] for item in result["items"]} == {"Fixture ramen", "Fixture restaurant"}
    assert result["destinations"] and result["topics"]
    assert (
        await client.get(
            "/api/v1/discovery/feed",
            params={
                "category": "foods",
                "type": "hotel",
                "mode": "following",
            },
        )
    ).status_code == 401


@pytest.mark.asyncio
async def test_public_detail_approved_intro_fresh_cache_sources_and_expiry(harness, monkeypatch):
    client, factory, _, _, _ = harness
    now = datetime.now(UTC)
    async with factory() as session:
        place = hotspot(
            map_match_status="verified",
            google_place_id="fixture-exact-id",
            latitude=34.395483,
            longitude=132.453592,
            coordinate_source_type="wikidata",
            coordinate_source_url="https://www.wikidata.org/Q1",
        )
        other = hotspot("Unrelated place")
        session.add_all([place, other])
        await session.flush()
        profile = HotspotPlaceProfile(
            hotspot_id=place.id,
            match_status="approved",
            provider_locale="ja",
            provider_fetched_at=now,
            provider_expires_at=now + timedelta(days=30),
            formatted_address="Provider original address",
            opening_hours_json={"open_24_hours": True},
            google_latitude=1,
            google_longitude=2,
            manual_official_website_url="https://example.com/manual-official",
            provider_website_uri="https://example.com/provider-candidate",
            provider_attributions_json=[
                {"displayName": "Fixture attribution", "uri": "https://example.com"}
            ],
            candidate_name="Unreviewed candidate secret",
            review_reason="Admin-only evidence",
        )
        approved = guide(place)
        session.add_all(
            [
                profile,
                approved,
                guide(place, "Pending secret", review_status="pending"),
                guide(other, "Other place article"),
                guide(place, "Japanese article", locale="ja"),
                guide(
                    place,
                    "Expired video",
                    provider="youtube",
                    content_type="video",
                    last_verified_at=now - timedelta(days=31),
                    metadata_expires_at=now - timedelta(days=1),
                ),
                HotspotIntro(
                    hotspot_id=place.id,
                    locale="en",
                    body="Approved local introduction",
                    source="manual",
                    review_status="approved",
                ),
                HotspotIntro(
                    hotspot_id=place.id,
                    locale="ja",
                    body="Pending introduction",
                    source="manual",
                    review_status="pending",
                ),
            ]
        )
        await session.commit()

    def no_provider_client(*args, **kwargs):
        raise AssertionError("Public detail must not construct network clients")

    monkeypatch.setattr(httpx.AsyncClient, "__init__", no_provider_client)
    response = await client.get(f"/api/v1/discovery/content/hotspot/{place.id}")
    assert response.status_code == 200, response.text
    item, detail = response.json(), response.json()["detail"]
    assert item["content"]["text"] == "Approved local introduction"
    assert detail["place"]["status"] == "ready"
    assert detail["place"]["data_locale"] == "ja"
    assert detail["place"]["coordinates"]["latitude"] == pytest.approx(34.395483)
    assert detail["place"]["attribution"]["provider"] == "Google Maps"
    assert detail["planning"]["selection_path"] == f"/hotspots/{place.id}/trip-selections"
    assert [row["id"] for row in detail["guides"]] == [f"guide:{approved.id}"]
    for private in (
        "Pending secret",
        "Unreviewed candidate secret",
        "Admin-only evidence",
        "Expired video",
    ):
        assert private not in response.text
    article = (await client.get(f"/api/v1/discovery/content/article/{approved.id}")).json()
    assert article["detail"]["planning"]["id"] == str(place.id)
    assert article["content"]["text"] == "Reviewed source text"
    assert article["source"]["url"] == approved.canonical_url
    async with factory() as session:
        await session.execute(
            update(HotspotPlaceProfile)
            .where(HotspotPlaceProfile.id == profile.id)
            .values(provider_expires_at=now - timedelta(seconds=1))
        )
        await session.commit()
    stale = (await client.get(f"/api/v1/discovery/content/hotspot/{place.id}")).json()["detail"][
        "place"
    ]
    assert stale["status"] == "stale" and stale["address"] is None
    assert stale["opening_hours"] == {} and stale["attribution"]["provider"] is None
    assert (
        stale["google_maps_url"]
        and stale["official_website_url"] == "https://example.com/manual-official"
    )
    assert stale["coordinates"]["latitude"] == pytest.approx(34.395483)


@pytest.mark.asyncio
async def test_pending_location_missing_intro_and_hidden_hotspot_fail_closed(harness):
    client, factory, _, _, _ = harness
    async with factory() as session:
        place = hotspot(
            map_match_status="verified",
            google_place_id="exact-id",
            latitude=35,
            longitude=139,
            coordinate_source_type="google_places_cache",
            coordinate_source_url="https://maps.google.com/",
        )
        session.add(place)
        await session.flush()
        session.add(
            HotspotPlaceProfile(
                hotspot_id=place.id,
                match_status="pending",
                formatted_address="Unapproved location",
                provider_expires_at=datetime.now(UTC) + timedelta(days=20),
            )
        )
        await session.commit()
    result = (await client.get(f"/api/v1/discovery/content/hotspot/{place.id}")).json()
    assert result["detail"]["planning"] is None and result["detail"]["intro"] is None
    assert "selection_path" not in result["place_ref"]
    assert result["detail"]["place"]["status"] == "pending_review"
    assert result["detail"]["place"]["address"] is None
    assert result["detail"]["place"]["coordinates"]["latitude"] is None
    async with factory() as session:
        session.add(ProviderConfig(provider="layout", config={"hotspots_enabled": False}))
        await session.commit()
    assert (await client.get(f"/api/v1/discovery/content/hotspot/{place.id}")).status_code == 404


@pytest.mark.asyncio
async def test_dish_options_only_real_publishable_merchants_and_reauthorize(harness):
    client, factory, _, _, _ = harness
    async with factory() as session:
        dish = food()
        valid, pending, no_source = (
            merchant(),
            merchant("Pending", review_status="pending"),
            merchant("No source"),
        )
        session.add_all([dish, valid, pending, no_source])
        await session.flush()
        session.add(FoodDestination(food_id=dish.id, destination_id="tokyo"))
        for row in (valid, pending, no_source):
            session.add(FoodMerchantFood(food_id=dish.id, merchant_id=row.id))
        for row in (valid, pending):
            session.add(
                FoodMerchantSource(
                    merchant_id=row.id,
                    source_type="merchant_official",
                    source_title="Official",
                    source_url="https://example.com/source",
                    is_current=True,
                )
            )
        await session.commit()
    detail = (await client.get(f"/api/v1/discovery/content/food/{dish.id}")).json()["detail"]
    assert [card["id"] for card in detail["merchants"]] == [str(valid.id)]
    assert detail["planning"]["selection_path"] == f"/foods/{dish.id}/trip-selections"
    assert (
        detail["planning"]["merchants"][0]["selection_path"]
        == f"/foods/merchants/{valid.id}/trip-selections"
    )
    assert detail["merchants"][0]["map_links"] and detail["merchants"][0]["sources"]
    assert (await client.get(f"/api/v1/discovery/content/merchant/{pending.id}")).status_code == 404
    async with factory() as session:
        await session.execute(
            update(FoodMerchantSource)
            .where(FoodMerchantSource.merchant_id == valid.id)
            .values(is_current=False)
        )
        await session.commit()
    cleared = (await client.get(f"/api/v1/discovery/content/food/{dish.id}")).json()["detail"]
    assert cleared["merchants"] == [] and cleared["planning"] is None


RESERVATION_FIXTURES = [
    ("JP", "tokyo", "tablecheck", "TableCheck", "en",
     "https://www.tablecheck.com/en/shops/mokaair-fixture/reserve"),
    ("KR", "seoul", "catchtable_global", "Catchtable Global", "en",
     "https://www.catchtable.net/shop/mokaair-fixture"),
    ("TW", "taipei", "eztable", "EZTABLE", "zh-TW",
     "https://www.eztable.com/restaurant/99999999"),
    ("SG", "singapore", "chope", "Chope", "en",
     "https://www.chope.co/singapore-restaurants/restaurant/mokaair-fixture"),
    ("HK", "hong-kong", "openrice", "OpenRice", "en",
     "https://www.openrice.com/en/hongkong/r-mokaair-fixture-r99999999"),
    ("TH", "bangkok", "hungry_hub", "Hungry Hub", "en",
     "https://web.hungryhub.com/en/restaurants/mokaair-fixture"),
    ("VN", "ho-chi-minh-city", "pasgo", "PasGo", "vi",
     "https://pasgo.vn/nha-hang/mokaair-fixture-99999999"),
]


async def seed_reservation_merchant(factory, *, country="JP", city="tokyo", **link_values):
    """Synthetic identities only: these URLs must never be fetched by the tests."""
    async with factory() as session:
        dish = food("Synthetic sushi")
        row = merchant(
            "Synthetic branch",
            country_code=country,
            destination_id=city,
            address="1 Synthetic Branch Street",
            official_website_url="https://restaurant.example.com/branch",
            official_website_verified_at=datetime.now(UTC),
            naver_map_url="https://map.naver.com/p/entry/place/99999999"
            if country == "KR" else None,
        )
        row.map_identity_metadata = {"map_identities": {"google_places": {
            "provider": "google_places", "place_id": row.google_place_id,
            "status": "verified",
        }}}
        session.add_all([dish, row])
        await session.flush()
        session.add_all([
            FoodDestination(food_id=dish.id, destination_id=city),
            FoodMerchantFood(food_id=dish.id, merchant_id=row.id),
            FoodMerchantSource(
                merchant_id=row.id, source_type="merchant_official",
                source_scope="merchant_website", source_title="Synthetic official branch",
                source_url="https://restaurant.example.com/branch", is_current=True,
            ),
            FoodMerchantPlatformLink(**({
                "merchant_id": row.id, "provider": "tablecheck", "status": "verified",
                "canonical_url": RESERVATION_FIXTURES[0][-1],
                "checked_at": datetime.now(UTC), "review_note": "Private branch audit note",
            } | link_values)),
        ])
        await session.commit()
        return dish, row


def block_detail_provider_clients(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Reading food/merchant links must not construct provider clients")

    monkeypatch.setattr(httpx.AsyncClient, "__init__", forbidden)


@pytest.mark.asyncio
@pytest.mark.parametrize("locale", ["en", "ja", "ko", "zh-TW", "zh-CN"])
@pytest.mark.parametrize("country,city,provider,label,language,url", RESERVATION_FIXTURES)
async def test_food_and_merchant_details_share_exact_reviewed_links_without_provider_calls(
    harness, monkeypatch, locale, country, city, provider, label, language, url
):
    client, factory, _, _, _ = harness
    dish, row = await seed_reservation_merchant(
        factory, country=country, city=city, provider=provider, canonical_url=url
    )
    block_detail_provider_clients(monkeypatch)
    headers = {"X-Travel-Locale": locale}
    food_response = await client.get(
        f"/api/v1/discovery/content/food/{dish.id}", headers=headers
    )
    own_response = await client.get(
        f"/api/v1/discovery/content/merchant/{row.id}", headers=headers
    )
    assert food_response.status_code == own_response.status_code == 200
    cards = food_response.json()["detail"]["merchants"]
    assert cards == own_response.json()["detail"]["merchants"]
    assert len(cards) == 1 and cards[0]["id"] == str(row.id)
    assert cards[0]["address"] == row.address
    assert cards[0]["official_website_url"] == row.official_website_url
    maps, links = cards[0]["map_links"], cards[0]["reservation_links"]
    assert [entry["provider"] for entry in maps] == (
        ["naver", "google"] if country == "KR" else ["google"]
    )
    assert maps[0]["primary"] is True
    if country == "KR":
        assert maps[0]["url"] == row.naver_map_url and maps[1]["primary"] is False
    assert parse_qs(urlsplit(maps[-1]["url"]).query)["query_place_id"] == [row.google_place_id]
    assert len(links) == 1 and links[0] == {
        "provider": provider, "label": label, "url": url,
        "verified_at": links[0]["verified_at"], "language_code": language,
    }
    assert links[0]["verified_at"]
    # A fallback stays the reviewed original, not a guessed translated path.
    assert all("Private branch audit note" not in response.text
               for response in (food_response, own_response))


@pytest.mark.asyncio
@pytest.mark.parametrize("overrides", [
    {"status": "not_found", "canonical_url": None},
    {"status": "ambiguous"},
    {"status": "disabled"},
    {"canonical_url": "https://www.tablecheck.com/"},
    {"canonical_url": "https://www.tablecheck.com/en/search"},
    {"canonical_url": "https://unreviewed.example.com/en/shops/fixture/reserve"},
    {"canonical_url": "http://www.tablecheck.com/en/shops/fixture/reserve"},
    {"canonical_url": "javascript:alert(1)"},
    {"canonical_url": "https://127.0.0.1/en/shops/fixture/reserve"},
    {"provider": "chope", "canonical_url": RESERVATION_FIXTURES[3][-1]},
])
async def test_discovery_omits_unreviewed_unsafe_or_wrong_country_reservation_links(
    harness, monkeypatch, overrides
):
    client, factory, _, _, _ = harness
    dish, row = await seed_reservation_merchant(factory, **overrides)
    block_detail_provider_clients(monkeypatch)
    for kind, identifier in (("food", dish.id), ("merchant", row.id)):
        response = await client.get(f"/api/v1/discovery/content/{kind}/{identifier}")
        assert response.status_code == 200
        cards = response.json()["detail"]["merchants"]
        assert len(cards) == 1 and cards[0]["reservation_links"] == []
        assert cards[0]["map_links"] and cards[0]["address"] == row.address


@pytest.mark.asyncio
async def test_discovery_reservation_locale_and_live_withdrawal_preserve_other_links(
    harness, monkeypatch
):
    client, factory, _, _, _ = harness
    localized_url = "https://www.tablecheck.com/ja/shops/mokaair-fixture/reserve"
    dish, row = await seed_reservation_merchant(
        factory, localized_urls_json={"ja": localized_url}
    )
    block_detail_provider_clients(monkeypatch)
    path = f"/api/v1/discovery/content/food/{dish.id}"
    payload = (await client.get(path, headers={"X-Travel-Locale": "ja"})).json()
    link = payload["detail"]["merchants"][0]["reservation_links"][0]
    assert link["url"] == localized_url and link["language_code"] == "ja"
    async with factory() as session:
        await session.execute(update(FoodMerchantPlatformLink).where(
            FoodMerchantPlatformLink.merchant_id == row.id
        ).values(status="disabled"))
        await session.commit()
    withdrawn = (await client.get(path)).json()["detail"]["merchants"][0]
    assert withdrawn["reservation_links"] == [] and withdrawn["map_links"]
    assert withdrawn["official_website_url"] == row.official_website_url
    async with factory() as session:
        await session.execute(update(FoodMerchant).where(
            FoodMerchant.id == row.id
        ).values(review_status="rejected", is_active=False))
        await session.commit()
    assert (await client.get(path)).json()["detail"]["merchants"] == []
    assert (await client.get(f"/api/v1/discovery/content/merchant/{row.id}")).status_code == 404


@pytest.mark.asyncio
async def test_hotel_reviewed_action_no_price_or_booking_identity_leak(harness, monkeypatch):
    client, factory, _, _, _ = harness
    _, _, _, hotel, _, _ = await seed_types(factory)
    async with factory() as session:
        await session.execute(
            update(TravelServiceProduct)
            .where(TravelServiceProduct.id == hotel.id)
            .values(
                facts={
                    "latitude": 35.6812,
                    "longitude": 139.7671,
                    "coordinate_source_url": "https://example.com/location",
                    "google_place_id": "exact-hotel",
                    "map_verified": True,
                    "area_code": "marunouchi",
                    "reference_price": 99999,
                    "currency": "USD",
                    "price_checked_at": datetime.now(UTC).isoformat(),
                }
            )
        )
        await session.commit()

    def no_network(*args, **kwargs):
        raise AssertionError("No hotel provider client is allowed in discovery detail")

    monkeypatch.setattr(httpx.AsyncClient, "__init__", no_network)
    response = await client.get(f"/api/v1/discovery/content/hotel/{hotel.id}")
    assert response.status_code == 200, response.text
    detail = response.json()["detail"]
    assert detail["hotel"]["facts"]["reference_price"] is None
    assert detail["hotel"]["facts"]["currency"] is None
    assert "hotel_links" not in detail["hotel"]["facts"]
    assert detail["hotel"]["booking_options"] == [] and detail["hotel"]["offers"] == []
    assert detail["planning"]["product_id"] == str(hotel.id)
    assert detail["planning"]["destination_id"] == "tokyo"
    async with factory() as session:
        await session.execute(
            update(TravelServiceProduct)
            .where(TravelServiceProduct.id == hotel.id)
            .values(facts={"reference_price": 99999})
        )
        await session.commit()
    assert (await client.get(f"/api/v1/discovery/content/hotel/{hotel.id}")).json()["detail"][
        "planning"
    ] is None
    async with factory() as session:
        await session.execute(
            update(TravelServiceProduct)
            .where(TravelServiceProduct.id == hotel.id)
            .values(verified_at=datetime.now(UTC) - timedelta(days=31))
        )
        await session.commit()
    assert (await client.get(f"/api/v1/discovery/content/hotel/{hotel.id}")).status_code == 404


@pytest.mark.asyncio
async def test_hotel_options_keep_review_freshness_switch_and_server_side_targets(harness):
    client, factory, _, _, _ = harness
    _, _, _, hotel, _, _ = await seed_types(factory)
    now = datetime.now(UTC)
    async with factory() as session:
        option = HotelBookingOption(
            product_id=hotel.id,
            provider="official",
            status="approved",
            discovery_status="found",
            url="https://hotel.example.com/exact-property",
            evidence_url="https://hotel.example.com/about",
            verified_at=now,
            health_status="healthy",
            identity_note="Private review proof",
        )
        pending = HotelBookingOption(
            product_id=hotel.id,
            provider="booking",
            status="pending",
            discovery_status="found",
            url="https://www.booking.com/hotel/jp/fixture.html",
            evidence_url="https://example.com/proof",
            verified_at=now,
            health_status="healthy",
        )
        session.add_all([option, pending])
        await session.commit()
    path = f"/api/v1/discovery/content/hotel/{hotel.id}"
    assert (await client.get(path)).json()["detail"]["hotel"]["booking_options"] == []
    async with factory() as session:
        config = await session.get(TravelServiceConfig, 1)
        config.data = {**config.data, "direct_hotel_links_enabled": True}
        await session.commit()
    response = await client.get(path)
    hotel_detail = response.json()["detail"]["hotel"]
    assert hotel_detail["booking_options"] == [
        {
            "id": str(option.id),
            "provider": "official",
            "name": None,
            "mode": "direct",
            "quote_status": "not_configured",
        }
    ]
    assert hotel_detail["direct_links"] == [{"provider": "official", "name": None}]
    for private in ("exact-property", "Private review proof", "booking.com/hotel", "/proof"):
        assert private not in response.text
    async with factory() as session:
        await session.execute(
            update(HotelBookingOption)
            .where(HotelBookingOption.id == option.id)
            .values(verified_at=now - timedelta(days=31))
        )
        await session.commit()
    expired = (await client.get(path)).json()["detail"]["hotel"]
    assert expired["booking_options"] == [] and expired["direct_links"] == []
