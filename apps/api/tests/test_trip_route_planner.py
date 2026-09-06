from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

import fakeredis.aioredis
import httpx
import pytest

from app.config import Settings
from app.models import TripPlanItem, TripRouteSegment
from app.trips.route_planner import (
    ESTIMATED_SEGMENT_PROVIDER,
    project_day_schedule,
    project_day_with_estimates,
    segment_from_record,
)
from app.trips.routing import (
    GoogleRouteProvider,
    RoutePoint,
    RouteSegment,
    RouteService,
    estimate_leg_minutes,
)


def row(
    title: str,
    start_hour: int,
    *,
    duration: int = 60,
    locked: bool = False,
    fixed: bool = False,
) -> TripPlanItem:
    start = datetime(2026, 11, 10, start_hour, tzinfo=UTC)
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=uuid4(),
        item_type="suggestion",
        day_date=date(2026, 11, 10),
        position=0,
        title=title,
        start_time=start,
        end_time=start.replace(hour=start_hour + 1),
        duration_minutes=duration,
        locked=locked,
        fixed_time=fixed,
        is_estimated=False,
        data={},
    )


def segment(first: TripPlanItem, second: TripPlanItem, minutes: int) -> RouteSegment:
    return RouteSegment(
        from_item_id=first.id,
        to_item_id=second.id,
        provider="fixture",
        attribution="測試路線",
        generated_at=datetime.now(UTC),
        duration_minutes=minutes,
        buffer_minutes=10,
    )


def test_projected_schedule_shifts_locked_flexible_items_and_preserves_fixed_booking() -> None:
    first = row("淺草寺", 9)
    locked = row("上野公園", 11, locked=True)
    fixed = row("餐廳預約", 11, fixed=True)
    fixed.start_time = datetime(2026, 11, 10, 11, 40, tzinfo=UTC)
    fixed.end_time = datetime(2026, 11, 10, 12, 40, tzinfo=UTC)

    result = project_day_schedule(
        [first, locked, fixed],
        [segment(first, locked, 20), segment(locked, fixed, 20)],
    )

    locked_start, locked_end = result.item_times[locked.id]
    assert locked_start == datetime(2026, 11, 10, 10, 30, tzinfo=UTC)
    assert locked_end == datetime(2026, 11, 10, 11, 30, tzinfo=UTC)
    assert result.item_times[fixed.id][0] == fixed.start_time
    assert result.impact.conflicts[0].late_minutes == 20
    assert result.segments[1].status == "conflict"
    assert result.segments[1].ready_time == datetime(2026, 11, 10, 12, 0, tzinfo=UTC)


@pytest.mark.asyncio
@pytest.mark.parametrize("mode", ["walk", "drive"])
async def test_google_routes_maps_non_transit_modes(mode: str) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        body = request.read().decode()
        assert f'"travelMode":"{mode.upper()}"' in body
        assert "transitPreferences" not in body
        if mode == "drive":
            assert '"routingPreference":"TRAFFIC_AWARE"' in body
        return httpx.Response(
            200,
            json={
                "routes": [
                    {
                        "duration": "720s",
                        "distanceMeters": 1800,
                        "legs": [
                            {
                                "steps": [
                                    {
                                        "travelMode": mode.upper(),
                                        "staticDuration": "720s",
                                        "distanceMeters": 1800,
                                        "navigationInstruction": {"instructions": "沿主要道路前進"},
                                    }
                                ]
                            }
                        ],
                    }
                ]
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    provider = GoogleRouteProvider(Settings(google_maps_api_key="key"), client)
    result = await provider.compute(
        RoutePoint(item_id=uuid4(), name="A", latitude=35.1, longitude=139.1),
        RoutePoint(item_id=uuid4(), name="B", latitude=35.2, longitude=139.2),
        datetime.now(UTC),
        "FEWER_TRANSFERS",
        mode,  # type: ignore[arg-type]
    )
    await client.aclose()
    assert result is not None
    assert result.travel_mode == mode
    assert result.duration_minutes == 12
    if mode == "walk":
        assert any("測試版" in warning for warning in result.warnings)


class ModeCountingProvider:
    name = "mode-counting"

    def __init__(self) -> None:
        self.calls = 0

    async def compute(
        self,
        origin: RoutePoint,
        destination: RoutePoint,
        _departure: datetime | None,
        _preference: str,
        travel_mode: str,
    ) -> RouteSegment:
        self.calls += 1
        return RouteSegment(
            from_item_id=origin.item_id,
            to_item_id=destination.item_id,
            provider=self.name,
            attribution="test",
            generated_at=datetime.now(UTC),
            duration_minutes=10,
            travel_mode=travel_mode,
        )


@pytest.mark.asyncio
async def test_route_cache_separates_travel_modes() -> None:
    provider = ModeCountingProvider()
    service = RouteService(
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        Settings(route_cache_ttl_seconds=300),
        google=provider,
    )
    origin = RoutePoint(item_id=uuid4(), name="A", latitude=35.1, longitude=139.1)
    destination = RoutePoint(item_id=uuid4(), name="B", latitude=35.2, longitude=139.2)
    await service.compute(origin, destination, None, "FASTEST", japan=False, travel_mode="walk")
    await service.compute(origin, destination, None, "FASTEST", japan=False, travel_mode="drive")
    assert provider.calls == 2


def test_persisted_provider_route_becomes_stale_but_manual_route_does_not() -> None:
    values = {
        "trip_plan_id": uuid4(),
        "day_date": date(2026, 11, 10),
        "from_item_id": uuid4(),
        "to_item_id": uuid4(),
        "attribution": "測試",
        "duration_minutes": 20,
        "travel_mode": "transit",
        "is_override": True,
        "schedule_mode": "scheduled",
        "preference": "FEWER_TRANSFERS",
        "buffer_minutes": 10,
        "steps": [],
        "details_available": [],
        "warnings": [],
        "generated_at": datetime.now(UTC) - timedelta(hours=2),
        "expires_at": datetime.now(UTC) - timedelta(hours=1),
    }
    provider = TripRouteSegment(provider="google_routes", **values)
    manual = TripRouteSegment(provider="manual", status="manual", **values)

    assert segment_from_record(provider).status == "stale"
    assert segment_from_record(manual).status == "manual"


def point_for(item: TripPlanItem, latitude: float, longitude: float) -> RoutePoint:
    return RoutePoint(
        item_id=item.id,
        name=item.title or "",
        latitude=latitude,
        longitude=longitude,
    )


def test_a_saved_leg_keeps_its_duration_while_a_missing_one_is_estimated() -> None:
    """After an edit the deleted legs have no segment; the day still has to add up."""
    first = row("淺草寺", 9)
    second = row("晴空塔", 11)
    third = row("上野公園", 13)
    points = {
        first.id: point_for(first, 35.7148, 139.7967),
        second.id: point_for(second, 35.7101, 139.8107),
        third.id: point_for(third, 35.7148, 139.7737),
    }

    result = project_day_with_estimates(
        [first, second, third],
        [segment(first, second, 25)],
        points,
        "transit",
        buffer_minutes=10,
    )

    saved_leg, estimated_leg = result.segments
    assert saved_leg.provider == "fixture" and saved_leg.duration_minutes == 25
    assert estimated_leg.provider == ESTIMATED_SEGMENT_PROVIDER
    assert estimated_leg.status == "estimated"
    assert estimated_leg.duration_minutes == estimate_leg_minutes(
        points[second.id], points[third.id], "transit"
    )
    # 09:00 + 60 min stay + 25 min + 10 min buffer, then the same chain through the estimate.
    assert result.item_times[second.id][0] == datetime(2026, 11, 10, 10, 35, tzinfo=UTC)
    third_start = result.item_times[third.id][0]
    assert third_start is not None
    assert third_start > result.item_times[second.id][0]


def test_a_leg_without_coordinates_is_left_alone_rather_than_guessed() -> None:
    first = row("淺草寺", 9)
    second = row("待確認地點", 11)

    result = project_day_with_estimates(
        [first, second],
        [],
        {first.id: point_for(first, 35.7148, 139.7967)},
        "transit",
    )

    assert result.segments == []
    assert result.item_times[second.id] == (second.start_time, second.end_time)
