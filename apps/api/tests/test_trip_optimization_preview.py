from datetime import UTC, date, datetime
from types import SimpleNamespace
from typing import Any
from uuid import UUID, uuid4

import fakeredis.aioredis
import pytest

from app.config import Settings
from app.main import app
from app.models import TripPlan, TripPlanItem
from app.trips.router import (
    OPTIMIZATION_MOVABLE_LIMIT,
    _chain_minutes,
    _nearest_neighbour,
    _preview_item,
    movable_slots,
    optimization_summary,
    plan_itinerary_optimization,
)
from app.trips.routing import RoutePoint, RouteSegment

DAY = date(2026, 11, 10)


def _row(
    title: str,
    hour: int,
    *,
    locked: bool = False,
    fixed: bool = False,
    latitude: float = 35.0,
) -> TripPlanItem:
    start = datetime(2026, 11, 10, hour, tzinfo=UTC)
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=uuid4(),
        item_type="suggestion",
        day_date=DAY,
        position=0,
        title=title,
        latitude=latitude,
        longitude=139.0,
        start_time=start,
        end_time=start.replace(hour=hour + 1),
        duration_minutes=60,
        locked=locked,
        fixed_time=fixed,
        is_estimated=False,
        data={},
    )


def _trip() -> TripPlan:
    return TripPlan(
        id=uuid4(),
        user_id=uuid4(),
        name="東京五日",
        mode="manual",
        total_price=0,
        currency="TWD",
        data={},
        version=3,
        start_date=DAY,
        end_date=DAY,
        timezone="Asia/Tokyo",
        route_preference="FEWER_TRANSFERS",
    )


def test_optimize_preview_and_apply_routes_are_published() -> None:
    # The web planner has always called these two paths; the backend only ever
    # registered the one-shot route, so both calls 404'd in production.
    paths = app.openapi()["paths"]
    assert "post" in paths["/api/v1/trips/{trip_id}/itinerary/optimize/preview"]
    assert "post" in paths["/api/v1/trips/{trip_id}/itinerary/optimize/apply"]
    assert "post" in paths["/api/v1/trips/{trip_id}/itinerary/optimize"]


def test_nearest_neighbour_follows_the_cheapest_hop() -> None:
    first, second, third = _row("A", 9), _row("B", 11), _row("C", 13)
    costs = {
        (first.id, second.id): 60,
        (first.id, third.id): 10,
        (third.id, second.id): 15,
        (second.id, third.id): 15,
        (second.id, first.id): 60,
        (third.id, first.id): 10,
    }

    ordered = _nearest_neighbour([first, second, third], costs)

    assert [row.title for row in ordered] == ["A", "C", "B"]
    assert _chain_minutes(ordered, costs) == 25
    assert _chain_minutes([first, second, third], costs) == 75


def test_preview_item_matches_the_shape_the_planner_renders() -> None:
    item = _row("淺草寺", 9, locked=True)

    assert _preview_item(item, 2) == {
        "id": str(item.id),
        "title": "淺草寺",
        "position": 2,
        "start_time": item.start_time.isoformat() if item.start_time else None,
        "locked": True,
        "fixed_time": False,
    }


class _StubRouteService:
    """Answer the proposed chain from a fixed matrix instead of calling a provider."""

    matrix: dict[tuple[UUID, UUID], int] = {}
    calls: list[dict[str, Any]] = []

    def __init__(self, *_: object, **__: object) -> None:
        pass

    async def compute_many(
        self,
        pairs: list[tuple[RoutePoint, RoutePoint, Any]],
        _preference: str,
        **kwargs: object,
    ) -> list[RouteSegment | None]:
        type(self).calls.append(
            {
                "pairs": [
                    (origin.item_id, destination.item_id) for origin, destination, _ in pairs
                ],
                "travel_mode": kwargs.get("travel_mode"),
            }
        )
        return [
            RouteSegment(
                from_item_id=origin.item_id,
                to_item_id=destination.item_id,
                provider="fixture",
                attribution="測試路線",
                generated_at=datetime.now(UTC),
                duration_minutes=self.matrix.get((origin.item_id, destination.item_id), 45),
                buffer_minutes=10,
            )
            for origin, destination, _ in pairs
        ]


@pytest.mark.asyncio
async def test_plan_reports_the_saving_without_touching_any_row(monkeypatch: Any) -> None:
    # B sits 4.4 km north of A, C only 0.6 km: by straight-line transit estimate
    # A→B and B→C are 25 minutes each, A→C is 15.
    first = _row("A", 9)
    second = _row("B", 11, latitude=35.04)
    third = _row("C", 13, latitude=35.005)
    for position, row in enumerate([first, second, third]):
        row.position = position
    _StubRouteService.matrix = {}
    _StubRouteService.calls = []
    monkeypatch.setattr("app.trips.router.RouteService", _StubRouteService)
    monkeypatch.setattr("app.trips.router.get_redis", fakeredis.aioredis.FakeRedis)

    plan = await plan_itinerary_optimization(
        _trip(), [first, second, third], [DAY], "FEWER_TRANSFERS", Settings()
    )

    assert plan["changed"] is True
    assert plan["total_duration_before_minutes"] == 50
    assert plan["total_duration_after_minutes"] == 40
    day = plan["days"][0]
    assert day["saved_minutes"] == 10
    assert [item["title"] for item in day["before"]] == ["A", "B", "C"]
    assert [item["title"] for item in day["after"]] == ["A", "C", "B"]
    assert day["order"] == [str(first.id), str(third.id), str(second.id)]
    # Planning must not renumber anything: apply replays the order, preview does not write.
    assert [row.position for row in (first, second, third)] == [0, 1, 2]
    # The matrix is estimated; only the proposed chain (two legs) reaches a provider.
    assert _StubRouteService.calls == [
        {"pairs": [(first.id, third.id), (third.id, second.id)], "travel_mode": "transit"}
    ]


@pytest.mark.asyncio
async def test_plan_routes_the_proposed_chain_in_the_day_travel_mode(monkeypatch: Any) -> None:
    first, second = _row("A", 9), _row("B", 11, latitude=35.01)
    _StubRouteService.calls = []
    monkeypatch.setattr("app.trips.router.RouteService", _StubRouteService)
    monkeypatch.setattr("app.trips.router.get_redis", fakeredis.aioredis.FakeRedis)
    walking_day = SimpleNamespace(
        day_date=DAY, default_travel_mode="walk", default_buffer_minutes=15
    )

    plan = await plan_itinerary_optimization(
        _trip(),
        [first, second],
        [DAY],
        "FEWER_TRANSFERS",
        Settings(),
        day_settings=[walking_day],  # type: ignore[list-item]
    )

    assert _StubRouteService.calls[0]["travel_mode"] == "walk"
    assert all(segment.buffer_minutes == 15 for segment in plan["segments"])
    # 1.1 km on foot at 4.5 km/h, rounded up to five minutes.
    assert plan["total_duration_before_minutes"] == 15


@pytest.mark.asyncio
async def test_plan_leaves_locked_and_fixed_items_where_they_are(monkeypatch: Any) -> None:
    first = _row("A", 9)
    pinned = _row("B", 11, fixed=True, latitude=35.02)
    third = _row("C", 13, latitude=35.005)
    monkeypatch.setattr("app.trips.router.RouteService", _StubRouteService)
    monkeypatch.setattr("app.trips.router.get_redis", fakeredis.aioredis.FakeRedis)

    plan = await plan_itinerary_optimization(
        _trip(), [first, pinned, third], [DAY], "FEWER_TRANSFERS", Settings()
    )

    # The fixed booking keeps slot 1 even though the movable pair is reordered around it.
    assert plan["days"][0]["after"][1]["title"] == "B"
    assert plan["days"][0]["after"][1]["fixed_time"] is True


@pytest.mark.asyncio
async def test_plan_skips_a_day_with_nothing_to_reorder(monkeypatch: Any) -> None:
    only = _row("A", 9)
    monkeypatch.setattr("app.trips.router.RouteService", _StubRouteService)
    monkeypatch.setattr("app.trips.router.get_redis", fakeredis.aioredis.FakeRedis)

    plan = await plan_itinerary_optimization(
        _trip(), [only], [DAY], "FEWER_TRANSFERS", Settings()
    )

    assert plan["days"] == []
    assert plan["changed"] is False


def test_optimization_summary_counts_only_rows_the_optimiser_may_move() -> None:
    free_one, free_two = _row("A", 9), _row("B", 11)
    locked = _row("C", 13, locked=True)
    fixed = _row("D", 15, fixed=True)
    unlocated = _row("E", 17)
    unlocated.latitude = None
    unlocated.longitude = None
    other_day = _row("F", 9)
    other_day.day_date = date(2026, 11, 11)

    summary = optimization_summary([free_one, free_two, locked, fixed, unlocated, other_day])

    assert summary["movable_limit"] == OPTIMIZATION_MOVABLE_LIMIT
    assert summary["days"] == [
        {"date": "2026-11-10", "movable_count": 2},
        {"date": "2026-11-11", "movable_count": 1},
    ]
    assert movable_slots([locked, free_one, fixed, free_two]) == [1, 3]
