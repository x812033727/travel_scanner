from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from types import SimpleNamespace
from typing import cast
from uuid import uuid4

import pytest

import app.trips.route_tasks as route_tasks
import app.trips.router as trips_router
from app.config import Settings
from app.models import TripPlan, TripPlanItem, TripRouteSegment
from app.trips.routing import RoutePoint, RouteSegment, TravelMode


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

    persist_kwargs: dict[str, object] = {}

    async def fake_persist(
        _session: object,
        _trip_id: object,
        _day_value: object,
        segments: list[RouteSegment],
        **kwargs: object,
    ) -> None:
        persisted.extend(segments)
        persist_kwargs.update(kwargs)

    async def fake_runtime(_session: object) -> object:
        return Settings(route_cache_ttl_seconds=300, route_segment_ttl_seconds=30 * 86_400)

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
    # Applied segments outlive the short provider-result cache: they are only
    # invalidated by itinerary edits or the separate segment TTL.
    assert persisted[0].expires_at is not None
    assert persisted[0].expires_at > datetime.now(UTC) + timedelta(days=29)
    assert persist_kwargs["ttl_seconds"] == 30 * 86_400
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


def make_items(trip_id: object, day_value: date, count: int) -> list[TripPlanItem]:
    rows: list[TripPlanItem] = []
    for index in range(count):
        start = datetime(2026, 11, 10, index, 0, tzinfo=UTC)
        rows.append(
            TripPlanItem(
                id=uuid4(),
                trip_plan_id=trip_id,
                item_type="suggestion",
                day_date=day_value,
                position=index,
                title=f"第 {index + 1} 站",
                location_name=f"第 {index + 1} 站",
                latitude=Decimal("35.68") + Decimal(index) / Decimal(100),
                longitude=Decimal("139.76") + Decimal(index) / Decimal(100),
                start_time=start,
                end_time=start + timedelta(minutes=30),
                data={},
            )
        )
    return rows


def saved_record(
    trip_id: object,
    day_value: date,
    first: TripPlanItem,
    second: TripPlanItem,
    *,
    duration: int,
    travel_mode: str = "transit",
    preference: str = "FEWER_TRANSFERS",
    is_override: bool = False,
    status: str = "resolved",
    expires_in: timedelta = timedelta(days=20),
) -> TripRouteSegment:
    """An in-memory trip_route_segments row; column defaults only apply on INSERT."""
    return TripRouteSegment(
        id=uuid4(),
        trip_plan_id=trip_id,
        day_date=day_value,
        from_item_id=first.id,
        to_item_id=second.id,
        status=status,
        travel_mode=travel_mode,
        is_override=is_override,
        provider="saved",
        attribution="test",
        preference=preference,
        schedule_mode="scheduled",
        duration_minutes=duration,
        buffer_minutes=10,
        steps=[],
        details_available=[],
        warnings=[],
        generated_at=datetime.now(UTC),
        expires_at=datetime.now(UTC) + expires_in,
    )


async def run_day(
    monkeypatch: pytest.MonkeyPatch,
    trip: TripPlan,
    rows: list[TripPlanItem],
    records: list[TripRouteSegment],
    *,
    day_value: date,
    buffer: int = 10,
    mode: str = "transit",
    preference: str = "FEWER_TRANSFERS",
    refresh: bool = False,
) -> tuple[list[RouteSegment], dict[str, object], list[dict[str, object]]]:
    """Run the day recompute with fakes; return persisted segments, persist kwargs, calls."""
    persisted: list[RouteSegment] = []
    persist_kwargs: dict[str, object] = {}
    calls: list[dict[str, object]] = []

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
            origin: RoutePoint,
            destination: RoutePoint,
            *_args: object,
            **kwargs: object,
        ) -> RouteSegment:
            calls.append(
                {
                    "from": origin.item_id,
                    "to": destination.item_id,
                    "travel_mode": kwargs.get("travel_mode"),
                    "refresh": kwargs.get("refresh"),
                }
            )
            return RouteSegment(
                from_item_id=origin.item_id,
                to_item_id=destination.item_id,
                provider="google_routes",
                attribution="Google Maps",
                generated_at=datetime.now(UTC),
                travel_mode=cast(TravelMode, kwargs.get("travel_mode") or "transit"),
                duration_minutes=12,
            )

    async def fake_items(_session: object, _trip_id: object) -> list[TripPlanItem]:
        return rows

    async def fake_setting(*_args: object, **_kwargs: object) -> object:
        return SimpleNamespace(
            default_travel_mode=mode,
            default_buffer_minutes=buffer,
            route_preference=preference,
        )

    async def fake_records(*_args: object, **_kwargs: object) -> list[TripRouteSegment]:
        return records

    async def fake_persist(
        _session: object,
        _trip_id: object,
        _day_value: object,
        segments: list[RouteSegment],
        **kwargs: object,
    ) -> None:
        persisted.extend(segments)
        persist_kwargs.update(kwargs)

    async def fake_runtime(_session: object) -> object:
        return Settings()

    monkeypatch.setattr(route_tasks, "_items", fake_items)
    monkeypatch.setattr(route_tasks, "get_or_create_day_setting", fake_setting)
    monkeypatch.setattr(route_tasks, "load_route_segments", fake_records)
    monkeypatch.setattr(route_tasks, "persist_projected_segments", fake_persist)
    monkeypatch.setattr(route_tasks, "load_runtime_settings", fake_runtime)
    monkeypatch.setattr(route_tasks, "RouteService", Service)
    monkeypatch.setattr(route_tasks, "get_redis", lambda: object())

    await route_tasks.compute_and_apply_routes(
        Session(),  # type: ignore[arg-type]
        trip,
        expected_version=1,
        target_day=day_value,
        refresh=refresh,
    )
    return persisted, persist_kwargs, calls


@pytest.mark.asyncio
async def test_recompute_only_queries_pairs_without_a_saved_segment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trip, _ = trip_with_items()
    day_value = date(2026, 11, 10)
    rows = make_items(trip.id, day_value, 4)
    # An edit to the third stop deleted its two pairs; the middle one is recreated here
    # as "missing" while the outer pairs survived with their provider answers.
    records = [
        saved_record(trip.id, day_value, rows[0], rows[1], duration=20),
        saved_record(trip.id, day_value, rows[2], rows[3], duration=30),
    ]

    persisted, _, calls = await run_day(monkeypatch, trip, rows, records, day_value=day_value)

    assert [(call["from"], call["to"]) for call in calls] == [(rows[1].id, rows[2].id)]
    by_pair = {(segment.from_item_id, segment.to_item_id): segment for segment in persisted}
    assert by_pair[(rows[0].id, rows[1].id)].duration_minutes == 20
    assert by_pair[(rows[0].id, rows[1].id)].provider == "saved"
    assert by_pair[(rows[1].id, rows[2].id)].duration_minutes == 12
    assert by_pair[(rows[1].id, rows[2].id)].provider == "google_routes"
    assert by_pair[(rows[2].id, rows[3].id)].duration_minutes == 30
    # The schedule chains through reused and fresh legs alike (30-minute stays, 10 buffer).
    assert rows[1].start_time == datetime(2026, 11, 10, 1, 0, tzinfo=UTC)
    assert rows[2].start_time == datetime(2026, 11, 10, 1, 52, tzinfo=UTC)
    assert rows[3].start_time == datetime(2026, 11, 10, 3, 2, tzinfo=UTC)


@pytest.mark.asyncio
async def test_recompute_with_only_a_buffer_change_spends_no_provider_requests(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trip, _ = trip_with_items()
    day_value = date(2026, 11, 10)
    rows = make_items(trip.id, day_value, 3)
    records = [
        saved_record(trip.id, day_value, rows[0], rows[1], duration=20),
        saved_record(trip.id, day_value, rows[1], rows[2], duration=15),
    ]

    persisted, _, calls = await run_day(
        monkeypatch, trip, rows, records, day_value=day_value, buffer=30
    )

    assert calls == []
    assert [segment.buffer_minutes for segment in persisted] == [30, 30]
    assert rows[1].start_time == datetime(2026, 11, 10, 1, 20, tzinfo=UTC)
    assert rows[2].start_time == datetime(2026, 11, 10, 2, 35, tzinfo=UTC)


@pytest.mark.asyncio
async def test_recompute_refetches_mode_changes_but_keeps_override_legs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trip, _ = trip_with_items()
    day_value = date(2026, 11, 10)
    rows = make_items(trip.id, day_value, 3)
    records = [
        saved_record(trip.id, day_value, rows[0], rows[1], duration=20, travel_mode="transit"),
        # The traveller picked a car for this leg from the panel, with the trip-level
        # preference rather than the day default; that leg must not be re-queried.
        saved_record(
            trip.id,
            day_value,
            rows[1],
            rows[2],
            duration=9,
            travel_mode="drive",
            is_override=True,
            preference="FASTEST",
        ),
    ]

    persisted, persist_kwargs, calls = await run_day(
        monkeypatch, trip, rows, records, day_value=day_value, mode="walk"
    )

    assert [(call["from"], call["to"], call["travel_mode"]) for call in calls] == [
        (rows[0].id, rows[1].id, "walk")
    ]
    by_pair = {(segment.from_item_id, segment.to_item_id): segment for segment in persisted}
    assert by_pair[(rows[0].id, rows[1].id)].travel_mode == "walk"
    override = by_pair[(rows[1].id, rows[2].id)]
    assert override.travel_mode == "drive"
    assert override.duration_minutes == 9
    assert override.is_override is True
    assert persist_kwargs["override_pairs"] == {(rows[1].id, rows[2].id)}


@pytest.mark.asyncio
async def test_recompute_refresh_stale_or_mismatched_rows_query_the_provider_again(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trip, _ = trip_with_items()
    day_value = date(2026, 11, 10)
    rows = make_items(trip.id, day_value, 3)
    fresh = [
        saved_record(trip.id, day_value, rows[0], rows[1], duration=20),
        saved_record(trip.id, day_value, rows[1], rows[2], duration=15),
    ]

    _, _, calls = await run_day(
        monkeypatch, trip, rows, fresh, day_value=day_value, refresh=True
    )
    assert len(calls) == 2
    assert all(call["refresh"] is True for call in calls)

    expired_or_stale = [
        saved_record(
            trip.id, day_value, rows[0], rows[1], duration=20, expires_in=timedelta(days=-1)
        ),
        saved_record(trip.id, day_value, rows[1], rows[2], duration=15, status="stale"),
    ]
    _, _, calls = await run_day(
        monkeypatch, trip, rows, expired_or_stale, day_value=day_value
    )
    assert len(calls) == 2

    other_preference = [
        saved_record(trip.id, day_value, rows[0], rows[1], duration=20, preference="FASTEST"),
        saved_record(trip.id, day_value, rows[1], rows[2], duration=15),
    ]
    _, _, calls = await run_day(
        monkeypatch, trip, rows, other_preference, day_value=day_value
    )
    assert [(call["from"], call["to"]) for call in calls] == [(rows[0].id, rows[1].id)]
