from datetime import UTC, date, datetime
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

import pytest

import app.trips.route_tasks as route_tasks
import app.trips.router as trips_router
from app.config import Settings
from app.models import TripPlan, TripPlanItem
from app.trips.routing import RouteSegment


def trip_with_items() -> tuple[TripPlan, list[TripPlanItem]]:
    trip_id = uuid4()
    trip = TripPlan(
        id=trip_id,
        user_id=uuid4(),
        name="東京測試",
        mode="manual",
        total_price=Decimal("0"),
        currency="TWD",
        data={"routing_defaults": {"default_travel_mode": "transit"}},
        version=1,
        destination_name="東京",
        timezone="Asia/Tokyo",
    )
    day_value = date(2026, 11, 10)
    first = TripPlanItem(
        id=uuid4(),
        trip_plan_id=trip_id,
        item_type="suggestion",
        day_date=day_value,
        position=0,
        title="東京車站",
        location_name="東京車站",
        latitude=Decimal("35.6812"),
        longitude=Decimal("139.7671"),
        start_time=datetime(2026, 11, 10, 0, 0, tzinfo=UTC),
        end_time=datetime(2026, 11, 10, 1, 0, tzinfo=UTC),
        data={},
    )
    second = TripPlanItem(
        id=uuid4(),
        trip_plan_id=trip_id,
        item_type="suggestion",
        day_date=day_value,
        position=1,
        title="淺草寺",
        location_name="淺草寺",
        latitude=Decimal("35.7148"),
        longitude=Decimal("139.7967"),
        start_time=datetime(2026, 11, 10, 1, 0, tzinfo=UTC),
        end_time=datetime(2026, 11, 10, 2, 0, tzinfo=UTC),
        data={},
    )
    return trip, [first, second]


@pytest.mark.asyncio
async def test_background_route_success_persists_and_propagates_time(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trip, rows = trip_with_items()
    persisted: list[RouteSegment] = []

    class Session:
        async def scalar(self, _statement: object) -> int:
            return 2

        async def commit(self) -> None:
            return None

        async def rollback(self) -> None:
            return None

    class Service:
        def __init__(self, *_args: object) -> None:
            pass

        async def compute(
            self,
            origin: object,
            destination: object,
            *_args: object,
            **_kwargs: object,
        ) -> RouteSegment:
            return RouteSegment(
                from_item_id=origin.item_id,  # type: ignore[attr-defined]
                to_item_id=destination.item_id,  # type: ignore[attr-defined]
                provider="google_routes",
                attribution="Google Maps",
                generated_at=datetime.now(UTC),
                duration_minutes=12,
            )

    async def fake_items(_session: object, _trip_id: object) -> list[TripPlanItem]:
        return rows

    async def fake_setting(*_args: object, **_kwargs: object) -> object:
        return SimpleNamespace(
            default_travel_mode="transit",
            default_buffer_minutes=10,
            route_preference="FEWER_TRANSFERS",
        )

    async def fake_records(*_args: object, **_kwargs: object) -> list[object]:
        return []

    async def fake_persist(
        _session: object,
        _trip_id: object,
        _day_value: object,
        segments: list[RouteSegment],
        **_kwargs: object,
    ) -> None:
        persisted.extend(segments)

    async def fake_runtime(_session: object) -> object:
        return Settings(route_cache_ttl_seconds=300)

    monkeypatch.setattr(route_tasks, "_items", fake_items)
    monkeypatch.setattr(route_tasks, "get_or_create_day_setting", fake_setting)
    monkeypatch.setattr(route_tasks, "load_route_segments", fake_records)
    monkeypatch.setattr(route_tasks, "persist_projected_segments", fake_persist)
    monkeypatch.setattr(route_tasks, "load_runtime_settings", fake_runtime)
    monkeypatch.setattr(route_tasks, "RouteService", Service)
    monkeypatch.setattr(route_tasks, "get_redis", lambda: object())

    status = await route_tasks.compute_and_apply_routes(
        Session(),  # type: ignore[arg-type]
        trip,
        expected_version=1,
        target_day=date(2026, 11, 10),
    )

    assert status["status"] == "complete"
    assert len(persisted) == 1
    assert persisted[0].provider == "google_routes"
    assert persisted[0].expires_at is not None
    assert rows[1].start_time == datetime(2026, 11, 10, 1, 22, tzinfo=UTC)


@pytest.mark.asyncio
async def test_auto_location_match_is_destination_limited_and_marked(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trip, rows = trip_with_items()
    target = rows[1]
    target.location_name = "淺草寺"
    target.latitude = None
    target.longitude = None
    observed: dict[str, object] = {}

    class Session:
        async def execute(self, _statement: object) -> None:
            return None

    class Places:
        configured = True

        def __init__(self, *_args: object) -> None:
            pass

        async def search_place(
            self,
            query: str,
            latitude: float | None,
            longitude: float | None,
            **kwargs: object,
        ) -> dict[str, object]:
            observed.update(query=query, latitude=latitude, longitude=longitude, **kwargs)
            return {
                "id": "asakusa",
                "formattedAddress": "日本東京都台東區淺草",
                "displayName": {"text": "淺草寺"},
                "location": {"latitude": 35.7148, "longitude": 139.7967},
                "googleMapsUri": "https://maps.google.com/?cid=asakusa",
            }

    async def fake_runtime(_session: object) -> Settings:
        return Settings(google_maps_api_key="key")

    monkeypatch.setattr(trips_router, "GoogleTravelService", Places)
    monkeypatch.setattr(trips_router, "load_runtime_settings", fake_runtime)
    monkeypatch.setattr(trips_router, "get_redis", lambda: object())
    matched, unresolved = await trips_router._resolve_trip_locations(
        Session(),  # type: ignore[arg-type]
        trip,
        rows,
        item_ids={target.id},
    )

    assert len(matched) == 1
    assert not unresolved
    assert observed["region_code"] == "jp"
    assert "東京" in str(observed["query"])
    assert target.location_source == "google_places_auto"
    assert target.data["needs_place_confirmation"] is True
    assert target.latitude == Decimal("35.7148")


@pytest.mark.asyncio
async def test_auto_location_does_not_guess_blank_or_wrong_country(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trip, rows = trip_with_items()
    blank, wrong = rows
    blank.title = "新的行程安排"
    blank.location_name = ""
    blank.latitude = blank.longitude = None
    wrong.title = "中央公園"
    wrong.location_name = "中央公園"
    wrong.latitude = wrong.longitude = None

    class Session:
        async def execute(self, _statement: object) -> None:
            raise AssertionError("no route should be invalidated")

    class Places:
        configured = True

        def __init__(self, *_args: object) -> None:
            pass

        async def search_place(self, *_args: object, **_kwargs: object) -> dict[str, object]:
            return {
                "id": "seoul",
                "formattedAddress": "韓國首爾",
                "location": {"latitude": 37.55, "longitude": 126.97},
            }

    async def fake_runtime(_session: object) -> Settings:
        return Settings(google_maps_api_key="key")

    monkeypatch.setattr(trips_router, "GoogleTravelService", Places)
    monkeypatch.setattr(trips_router, "load_runtime_settings", fake_runtime)
    monkeypatch.setattr(trips_router, "get_redis", lambda: object())
    matched, unresolved = await trips_router._resolve_trip_locations(
        Session(),  # type: ignore[arg-type]
        trip,
        rows,
    )

    assert not matched
    assert {item["item_id"] for item in unresolved} == {str(blank.id), str(wrong.id)}
    assert wrong.latitude is None
