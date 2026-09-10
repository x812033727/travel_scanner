"""Dual identities never change the trip's canonical place or paid routing policy."""

from datetime import UTC, date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import fakeredis.aioredis
import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import Settings
from app.i18n import LOCALES
from app.models import Base, TripPlan, TripPlanItem, TripRouteSegment, User
from app.problems import AppError
from app.trips import router
from app.trips.map_identities import item_route_point, location_map_links, trip_map_identities
from app.trips.routing import (
    GoogleRouteProvider,
    RoutePoint,
    external_navigations,
    korean_external_route_reason,
    route_map_capabilities,
    route_provider_configured,
)


def stop(trip_id, position=0):
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=trip_id,
        item_type="activity",
        title="景福宮",
        location_name="경복궁",
        latitude=Decimal("37.5796"),
        longitude=Decimal("126.9770"),
        day_date=date(2026, 11, 11),
        position=position,
        provider_place_id="temporary-naver-hash",
        location_source="naver_local",
        start_time=datetime(2026, 11, 11, 9 + position, tzinfo=UTC),
        duration_minutes=60,
        data={
            "place_provider": "naver_local",
            "map_identities": {
                "naver_maps": {
                    "provider": "naver_maps",
                    "place_id": "12345",
                    "map_url": "https://map.naver.com/p/entry/place/12345",
                    "status": "verified",
                }
            },
        },
    )


@pytest.mark.parametrize(
    "mode,expected_maps,expected_outbound",
    [
        ("transit", ["google_maps"], ["google_maps", "naver_maps"]),
        ("walk", ["naver_maps", "google_maps"], ["naver_maps", "google_maps"]),
        ("drive", ["naver_maps"], ["naver_maps"]),
    ],
)
def test_korean_mode_matrix(mode, expected_maps, expected_outbound):
    first, second = item_route_point(stop(uuid4())), item_route_point(stop(uuid4(), 1))
    assert first and second
    assert route_map_capabilities("KR", mode)["providers"] == expected_maps
    links = external_navigations(first, second, mode, "KR")
    assert [link.provider for link in links] == expected_outbound
    assert all(link.web_url.startswith("https://") for link in links)
    assert all("temporary-naver-hash" not in link.web_url for link in links)


@pytest.mark.parametrize("region", ["KR", "kr"])
@pytest.mark.parametrize(
    "mode,credential,expected",
    [
        ("walk", "google", False),
        ("walk", "naver", False),
        ("walk", "odsay", False),
        ("drive", "google", False),
        ("drive", "naver", True),
        ("drive", "odsay", False),
        ("transit", "google", True),
        ("transit", "naver", False),
        ("transit", "odsay", True),
    ],
)
def test_korean_timing_capability_matches_the_real_provider_matrix(
    mode, credential, expected, region
):
    settings = Settings(
        google_maps_api_key="fixture-google" if credential == "google" else None,
        naver_maps_client_id="fixture-naver" if credential == "naver" else None,
        naver_maps_client_secret="fixture-secret" if credential == "naver" else None,
        odsay_api_key="fixture-odsay" if credential == "odsay" else None,
    )
    assert route_provider_configured(settings, region, mode) is expected


def test_only_independent_verified_google_identity_is_used_as_google_waypoint():
    item = stop(uuid4())
    point = item_route_point(item)
    assert point and "placeId" not in GoogleRouteProvider.waypoint(point)
    item.data["map_identities"]["google_places"] = {
        "provider": "google_places",
        "place_id": "ChIJ-google-exact",
        "status": "pending",
    }
    assert "placeId" not in GoogleRouteProvider.waypoint(item_route_point(item))
    item.data["map_identities"]["google_places"]["status"] = "verified"
    assert GoogleRouteProvider.waypoint(item_route_point(item)) == {"placeId": "ChIJ-google-exact"}
    assert trip_map_identities(item)["naver_maps"]["place_id"] == "12345"


def test_navermap_hash_does_not_become_exact_identity():
    item = stop(uuid4())
    item.data["map_identities"]["naver_maps"]["map_url"] = "https://map.naver.com/p/search/test"
    assert "naver_maps" not in trip_map_identities(item)
    assert item_route_point(item).naver_map_url is None


def test_fork_preserves_dual_identities_without_private_review_data():
    from app.trips.share_router import copied_item
    item = stop(uuid4())
    item.data["map_identities"]["google_places"] = {
        "provider": "google_places", "place_id": "ChIJ-copy", "status": "verified",
        "verified_by_user_id": str(uuid4()), "evidence_url": "https://private.example/review",
    }
    clone = copied_item(uuid4(), item)
    assert set(trip_map_identities(clone)) == {"google_places", "naver_maps"}
    assert "private.example" not in str(clone.data)
    assert clone.latitude == item.latitude


def test_external_names_are_encoded_not_open_redirect_targets():
    first = RoutePoint(
        item_id=uuid4(), name="A/&x=https://evil.test/#", latitude=37.5, longitude=127
    )
    links = external_navigations(first, first, "transit", "KR")
    assert links[0].web_url.startswith("https://www.google.com/maps/dir/?")
    assert links[1].web_url.startswith("https://map.naver.com/p/directions/")
    assert "&x=https://evil.test" not in links[0].web_url
    assert "A/%26" not in links[1].web_url


@pytest_asyncio.fixture
async def trip_db(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(router, "get_redis", lambda: redis)
    monkeypatch.setattr(router, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(
        router,
        "load_runtime_settings",
        AsyncMock(
            return_value=Settings(
                google_maps_api_key="fixture-only",
                google_maps_enabled=True,
            )
        ),
    )
    async with async_sessionmaker(engine, expire_on_commit=False)() as session:
        user = User(id=uuid4(), email=f"dual-{uuid4().hex}@example.test")
        trip = TripPlan(
            id=uuid4(),
            user_id=user.id,
            name="首爾",
            mode="balanced",
            total_price=Decimal("0"),
            destination_name="首爾",
            timezone="Asia/Seoul",
            version=1,
            data={},
        )
        first, second = stop(trip.id), stop(trip.id, 1)
        route = TripRouteSegment(
            id=uuid4(),
            trip_plan_id=trip.id,
            from_item_id=first.id,
            to_item_id=second.id,
            day_date=first.day_date,
            travel_mode="walk",
            provider="manual",
            attribution="manual",
            duration_minutes=17,
            generated_at=datetime.now(UTC),
            status="resolved",
        )
        session.add_all([user, trip, first, second, route])
        await session.commit()

        # Keep this endpoint test isolated from pricing/calendar read projections.
        async def serialize(db, current):
            return {"id": str(current.id), "version": current.version}

        monkeypatch.setattr(router, "serialize_trip", serialize)
        yield session, user, trip, first, second, route
    await redis.aclose()
    await engine.dispose()


@pytest.mark.asyncio
@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize(
    "mode,odsay_configured",
    [("transit", True), ("transit", False), ("walk", False), ("drive", False)],
)
async def test_unavailable_preview_keeps_reasons_on_every_external_navigation(
    trip_db, monkeypatch, mode, odsay_configured, locale
):
    session, user, trip, first, second, _ = trip_db
    compute = AsyncMock(return_value=[])
    monkeypatch.setattr(router.RouteService, "compute_options", compute)
    monkeypatch.setattr(router, "active_locale", lambda: locale)
    monkeypatch.setattr(
        router, "load_runtime_settings",
        AsyncMock(
            return_value=Settings(odsay_api_key="fixture-only" if odsay_configured else None)
        ),
    )
    response = await router.preview_trip_route(
        trip.id,
        router.RoutePreviewRequest(
            version=trip.version,
            from_item_id=first.id,
            to_item_id=second.id,
            travel_mode=mode,
        ),
        user,
        session,
    )
    assert response["kind"] == "external_only"
    assert response["segment"] is None and response["preview_id"] is None
    links = response["external_navigations"]
    assert links
    assert all(link["reason"] == response["external_navigation"]["reason"] for link in links)
    assert all(link["reason"] and link["travel_mode"] == mode for link in links)
    expected = korean_external_route_reason(mode, odsay_configured=odsay_configured, locale=locale)
    assert response["external_navigation"]["reason"] == expected
    if locale != "zh-TW":
        assert expected != korean_external_route_reason(
            mode, odsay_configured=odsay_configured, locale="zh-TW"
        )
    assert compute.await_args.kwargs["region_code"] == "KR"


@pytest.mark.parametrize(
    "mode,odsay_configured,expected",
    [
        (
            "transit", True,
            "ODsay 目前沒有回傳可套用的大眾運輸路線；可在 Google Maps 或 NAVER Maps 查看。",
        ),
        (
            "transit", False,
            "尚未設定站內大眾運輸服務；可在 Google Maps 或 NAVER Maps 查看。",
        ),
        (
            "walk", False,
            "步行地圖僅供位置參考；可外開 NAVER／Google Maps 或輸入手動時間。",
        ),
        ("drive", False, "目前沒有可套用的汽車路線；請到 NAVER Maps 查看即時導航。"),
    ],
)
def test_korean_external_reasons_keep_existing_traditional_chinese(
    mode, odsay_configured, expected
):
    assert korean_external_route_reason(
        mode, odsay_configured=odsay_configured, locale="zh-TW"
    ) == expected


@pytest.mark.asyncio
async def test_link_only_survives_reload_preserves_manual_route_and_replays(trip_db, monkeypatch):
    session, user, trip, first, _, route = trip_db
    lookup = AsyncMock(
        return_value={"place_id": "ChIJ-confirmed", "latitude": 37.5796, "longitude": 126.977}
    )
    monkeypatch.setattr(router.GoogleTravelService, "place_details", lookup)
    before = (
        first.title,
        first.latitude,
        first.longitude,
        first.start_time,
        first.position,
        first.provider_place_id,
    )
    payload = router.TripMapIdentityRequest(
        version=1, place_id="ChIJ-confirmed", confirmed_same_place=True
    )
    result = await router.supplement_trip_map_identity(
        trip.id, first.id, payload, user, session, "same-key-123"
    )
    assert result["version"] == 2
    await session.refresh(first)
    assert (
        first.title,
        first.latitude,
        first.longitude,
        first.start_time.replace(tzinfo=UTC),
        first.position,
        first.provider_place_id,
    ) == before
    assert set(trip_map_identities(first)) == {"google_places", "naver_maps"}
    assert (await session.get(TripRouteSegment, route.id)).duration_minutes == 17
    replay = await router.supplement_trip_map_identity(
        trip.id, first.id, payload, user, session, "same-key-123"
    )
    assert replay["version"] == 2
    assert lookup.await_count == 1
    different = payload.model_copy(update={"place_id": "ChIJ-different"})
    with pytest.raises(AppError) as error:
        await router.supplement_trip_map_identity(
            trip.id, first.id, different, user, session, "same-key-123"
        )
    assert error.value.code == "idempotency_key_conflict"


@pytest.mark.asyncio
async def test_identity_requires_owner_current_version_and_same_place(trip_db, monkeypatch):
    session, user, trip, first, _, _ = trip_db
    payload = router.TripMapIdentityRequest(
        version=9, place_id="ChIJ-confirmed", confirmed_same_place=True
    )
    lookup = AsyncMock(
        return_value={"place_id": "ChIJ-confirmed", "latitude": 35, "longitude": 139}
    )
    monkeypatch.setattr(router.GoogleTravelService, "place_details", lookup)
    with pytest.raises(AppError) as conflict:
        await router.supplement_trip_map_identity(
            trip.id, first.id, payload, user, session, "version-key"
        )
    assert conflict.value.code == "trip_version_conflict"
    assert lookup.await_count == 0
    payload.version = 1
    with pytest.raises(AppError) as mismatch:
        await router.supplement_trip_map_identity(
            trip.id, first.id, payload, user, session, "mismatch-key"
        )
    assert mismatch.value.code == "map_identity_location_mismatch"
    assert not await session.scalar(select(TripPlan.version).where(TripPlan.version > 1))


@pytest.mark.asyncio
async def test_navigation_is_read_only_and_does_not_call_provider(trip_db, monkeypatch):
    session, user, trip, first, second, _ = trip_db
    compute = AsyncMock(side_effect=AssertionError("navigation must not compute routes"))
    monkeypatch.setattr(router.RouteService, "compute_options", compute)
    response = await router.trip_route_navigation(
        trip.id, first.id, second.id, user, session, "transit"
    )
    assert [link["provider"] for link in response["external_navigations"]] == [
        "google_maps",
        "naver_maps",
    ]
    assert trip.version == 1
    assert compute.await_count == 0
    assert response["route_availability"] == {
        "status": "available", "provider": "google_routes", "can_query": True,
    }
    assert "fixture-only" not in str(response)


@pytest.mark.parametrize(
    "mode,provider,status,can_query",
    [
        ("transit", "google_routes", "available", True),
        ("walk", None, "external_only", False),
        ("drive", "naver_maps", "unconfigured", False),
    ],
)
@pytest.mark.asyncio
async def test_navigation_describes_korean_query_limits_before_search(
    trip_db, monkeypatch, mode, provider, status, can_query
):
    session, user, trip, first, second, route = trip_db
    compute = AsyncMock(side_effect=AssertionError("capabilities cannot query a provider"))
    monkeypatch.setattr(router.RouteService, "compute_options", compute)
    before_time = second.start_time
    before_duration = route.duration_minutes
    response = await router.trip_route_navigation(
        trip.id, first.id, second.id, user, session, mode
    )
    assert response["route_availability"] == {
        "status": status, "provider": provider, "can_query": can_query,
    }
    assert trip.version == 1
    assert second.start_time == before_time
    assert route.duration_minutes == before_duration
    assert compute.await_count == 0


def test_route_query_availability_distinguishes_google_transit_from_naver_drive():
    assert router.route_query_availability(Settings(), "KR", "transit") == {
        "status": "unconfigured", "provider": "google_routes", "can_query": False,
    }
    maps_only = Settings(google_maps_api_key="google-secret", google_maps_enabled=True)
    assert router.route_query_availability(maps_only, "KR", "transit") == {
        "status": "available", "provider": "google_routes", "can_query": True,
    }
    assert router.route_query_availability(maps_only, "KR", "drive")["can_query"] is False
    assert router.route_query_availability(maps_only, "TW", "transit") == {
        "status": "available", "provider": "google_routes", "can_query": True,
    }
    assert router.route_query_availability(
        Settings(odsay_api_key="odsay-secret", odsay_enabled=True), "KR", "transit"
    ) == {"status": "available", "provider": "odsay", "can_query": True}
    assert router.route_query_availability(
        Settings(
            naver_maps_enabled=True,
            naver_maps_client_id="browser-id",
            naver_maps_client_secret="naver-secret",
        ),
        "KR", "drive",
    ) == {"status": "available", "provider": "naver_maps", "can_query": True}


@pytest.mark.asyncio
async def test_other_user_cannot_read_navigation_capabilities(trip_db, monkeypatch):
    session, _, trip, first, second, _ = trip_db
    other_user = User(id=uuid4(), email=f"navigation-other-{uuid4().hex}@example.test")
    runtime_lookup = AsyncMock(side_effect=AssertionError("ownership check must precede settings"))
    monkeypatch.setattr(router, "load_runtime_settings", runtime_lookup)
    with pytest.raises(AppError) as error:
        await router.trip_route_navigation(trip.id, first.id, second.id, other_user, session)
    assert error.value.code == "trip_not_found"
    assert runtime_lookup.await_count == 0


@pytest.mark.asyncio
async def test_translated_ordinary_save_preserves_reviewed_identities(trip_db, monkeypatch):
    session, user, trip, first, second, _ = trip_db
    first.names_json = {
        "location_name": {"ko": "경복궁", "en": "Gyeongbokgung Palace"},
    }
    first.data = {
        **first.data,
        "map_identities": {
            **first.data["map_identities"],
            "google_places": {
                "provider": "google_places",
                "place_id": "ChIJ-reviewed",
                "status": "verified",
            },
        },
    }
    await session.commit()
    monkeypatch.setattr(router, "active_locale", lambda: "en")
    monkeypatch.setattr(router, "reproject_saved_times", AsyncMock(return_value=[]))
    first_payload = router.serialize_item(first, locale="en")
    assert first_payload["location_name"] == "Gyeongbokgung Palace"
    first_payload["notes"] = "Only changing a note"
    payload = router.ItineraryUpdateRequest.model_validate(
        {
            "version": trip.version,
            "items": [first_payload, router.serialize_item(second, locale="en")],
        }
    )
    await router.update_itinerary(trip.id, payload, user, session)
    await session.refresh(first)
    assert first.location_name == "경복궁"
    assert set(trip_map_identities(first)) == {"google_places", "naver_maps"}
    assert first.notes == "Only changing a note"


@pytest.mark.asyncio
async def test_real_place_replacement_clears_previous_verified_identities(trip_db, monkeypatch):
    session, user, trip, first, second, _ = trip_db
    monkeypatch.setattr(router, "reproject_saved_times", AsyncMock(return_value=[]))
    changed = router.serialize_item(first, localized=False)
    changed.update(
        location_name="Different branch",
        provider_place_id="ChIJ-client-supplied",
        location_source="confirmed",
        latitude=37.58,
        data={
            **first.data,
            "place_provider": "google_places",
            "map_identities": {
                "google_places": {
                    "provider": "google_places",
                    "place_id": "ChIJ-client-supplied",
                    "status": "verified",
                }
            },
        },
    )
    payload = router.ItineraryUpdateRequest.model_validate(
        {"version": trip.version, "items": [changed, router.serialize_item(second)]}
    )
    await router.update_itinerary(trip.id, payload, user, session)
    await session.refresh(first)
    assert first.location_name == "Different branch"
    assert first.data["map_identities"] == {}
    assert trip_map_identities(first) == {}
    assert item_route_point(first).google_place_id is None


@pytest.mark.asyncio
async def test_ordinary_save_materializes_true_legacy_google_identity(trip_db, monkeypatch):
    session, user, trip, first, second, _ = trip_db
    first.location_source = "confirmed"
    first.provider_place_id = "ChIJ-legacy"
    first.data = {"place_provider": "google_places"}
    await session.commit()
    monkeypatch.setattr(router, "reproject_saved_times", AsyncMock(return_value=[]))
    payload = router.ItineraryUpdateRequest.model_validate(
        {
            "version": trip.version,
            "items": [router.serialize_item(first), router.serialize_item(second)],
        }
    )
    await router.update_itinerary(trip.id, payload, user, session)
    await session.refresh(first)
    assert first.data["map_identities"]["google_places"]["place_id"] == "ChIJ-legacy"
    assert trip_map_identities(first)["google_places"]["status"] == "verified"


def test_explicit_empty_metadata_cannot_use_legacy_google_confirmation():
    item = stop(uuid4())
    item.location_source = "confirmed"
    item.provider_place_id = "ChIJ-client-supplied"
    item.data = {"place_provider": "google_places", "map_identities": {}}
    assert trip_map_identities(item) == {}
    assert item_route_point(item).google_place_id is None


def test_unsaved_draft_can_show_coordinate_link_without_a_route_point_uuid():
    item = stop(uuid4())
    item.id = None
    links = location_map_links(item)
    google = next(link for link in links if link["provider"] == "google")
    assert google["position_only"] is True
    assert "37.5796000%2C126.9770000" in google["url"]


@pytest.mark.asyncio
async def test_other_user_cannot_supplement_trip_identity(trip_db, monkeypatch):
    session, _, trip, first, _, _ = trip_db
    other_user = User(id=uuid4(), email=f"other-{uuid4().hex}@example.test")
    lookup = AsyncMock(side_effect=AssertionError("ownership must precede Google lookup"))
    monkeypatch.setattr(router.GoogleTravelService, "place_details", lookup)
    with pytest.raises(AppError) as error:
        await router.supplement_trip_map_identity(
            trip.id,
            first.id,
            router.TripMapIdentityRequest(
                version=1, place_id="ChIJ-confirmed", confirmed_same_place=True
            ),
            other_user,
            session,
            "other-user-key",
        )
    assert error.value.status == 404
    assert error.value.code == "trip_not_found"
    assert lookup.await_count == 0
    assert trip.version == 1


@pytest.mark.parametrize("replace_hotel", [False, True])
@pytest.mark.asyncio
async def test_primary_lodging_preserves_only_same_hotel_server_identities(trip_db, replace_hotel):
    session, user, trip, first, second, _ = trip_db
    identities = {
        **first.data["map_identities"],
        "google_places": {
            "provider": "google_places",
            "place_id": "ChIJ-reviewed-hotel",
            "status": "verified",
        },
    }
    for anchor, role in ((first, "hotel_start"), (second, "hotel_end")):
        anchor.item_type = "hotel"
        anchor.system_role = role
        anchor.locked = True
        anchor.data = {**anchor.data, "source_mode": "system", "map_identities": identities}
    trip.data = {
        "routing_defaults": {"auto_compute": False},
        "primary_lodging": {
            "name": "서울호텔",
            "location_name": "서울호텔 본관",
            "provider_place_id": first.provider_place_id,
            "latitude": float(first.latitude),
            "longitude": float(first.longitude),
            "location_source": "confirmed",
            "place_provider": "naver_local",
            "map_identities": identities,
        },
    }
    await session.commit()
    payload = router.PrimaryLodgingUpdateRequest.model_validate(
        {
            "version": trip.version,
            "name": "Updated hotel label",
            "location_name": "Updated hotel address label",
            "provider_place_id": "ChIJ-new-hotel" if replace_hotel else first.provider_place_id,
            "latitude": 37.58 if replace_hotel else float(first.latitude),
            "longitude": float(first.longitude),
            "location_source": "confirmed",
            # Unknown client metadata is not a source of provider verification.
            "place_provider": "google_places",
            "map_identities": {
                "google_places": {
                    "provider": "google_places", "place_id": "ChIJ-forged", "status": "verified",
                },
            },
        }
    )
    await router.update_primary_lodging(trip.id, payload, user, session)
    await session.refresh(trip)
    expected = set() if replace_hotel else {"naver_maps", "google_places"}
    lodging = trip.data["primary_lodging"]
    assert set(lodging["map_identities"]) == expected
    assert lodging["place_provider"] == (None if replace_hotel else "naver_local")
    for anchor in (first, second):
        await session.refresh(anchor)
        assert set(trip_map_identities(anchor)) == expected
        assert anchor.data["map_identities"] == lodging["map_identities"]
        assert anchor.data["place_provider"] == lodging["place_provider"]
        assert "ChIJ-forged" not in str(anchor.data)


@pytest.mark.parametrize(
    "latitude,longitude",
    [
        (float("nan"), 126.977),
        (37.5796, float("nan")),
        (float("inf"), 126.977),
        (37.5796, float("-inf")),
        (91, 126.977),
        (37.5796, 181),
        (True, 126.977),
    ],
)
@pytest.mark.asyncio
async def test_supplement_rejects_invalid_google_coordinates(
    trip_db, monkeypatch, latitude, longitude
):
    session, user, trip, first, _, _ = trip_db
    monkeypatch.setattr(
        router.GoogleTravelService,
        "place_details",
        AsyncMock(return_value={
            "place_id": "ChIJ-invalid-coordinates", "latitude": latitude, "longitude": longitude,
        }),
    )
    with pytest.raises(AppError) as error:
        await router.supplement_trip_map_identity(
            trip.id,
            first.id,
            router.TripMapIdentityRequest(
                version=1, place_id="ChIJ-invalid-coordinates", confirmed_same_place=True
            ),
            user,
            session,
            "invalid-coordinates-key",
        )
    assert error.value.code == "map_identity_location_mismatch"
    await session.refresh(trip)
    await session.refresh(first)
    assert trip.version == 1
    assert set(trip_map_identities(first)) == {"naver_maps"}
