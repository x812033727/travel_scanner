"""The compute-day endpoint's explicit refresh reaches the worker that computes the routes.

``POST /trips/{id}/routes/compute-day`` accepted ``refresh`` and rate-limited on it, but the
job it queued never carried the flag, so a full-day refresh reused every saved leg like an
ordinary run (2026-09-10). Older API processes may still have three-argument jobs in the
queue, so the flag is a trailing optional argument.
"""

from __future__ import annotations

import inspect
from datetime import date
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.trips import route_tasks


class FakeQueue:
    calls: list[tuple[str, tuple[object, ...], dict[str, object]]] = []

    def __init__(self, name: str, connection: object) -> None:
        self.name = name
        self.connection = connection

    def enqueue(self, *args: object, **kwargs: object) -> SimpleNamespace:
        FakeQueue.calls.append((self.name, args, kwargs))
        return SimpleNamespace(id="job-1")


def test_enqueue_passes_refresh_as_the_fourth_job_argument(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    FakeQueue.calls.clear()
    monkeypatch.setattr(route_tasks, "Queue", FakeQueue)
    monkeypatch.setattr(route_tasks, "SyncRedis", SimpleNamespace(from_url=lambda url: "redis"))
    trip_id = uuid4()

    assert route_tasks.enqueue_trip_routing(trip_id, 7, date(2026, 11, 10), refresh=True) == "job-1"
    assert route_tasks.enqueue_trip_routing(trip_id, 7) == "job-1"

    (name, args, kwargs), (_, default_args, _) = FakeQueue.calls
    assert name == "trip-routes"
    assert args == (
        "app.trips.route_tasks.run_trip_routing_job",
        str(trip_id),
        7,
        "2026-11-10",
        True,
    )
    assert kwargs == {"job_timeout": 180}
    # Without the flag a job is queued exactly as before, plus an explicit False.
    assert default_args[1:] == (str(trip_id), 7, None, False)


def test_an_older_three_argument_job_still_runs_without_a_refresh() -> None:
    parameters = inspect.signature(route_tasks.run_trip_routing_job).parameters
    assert list(parameters) == ["trip_id", "expected_version", "target_day", "refresh"]
    assert parameters["refresh"].default is False


@pytest.mark.asyncio
async def test_the_job_forwards_refresh_to_the_route_computation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: list[tuple[object, int, date | None, bool]] = []

    async def fake_compute(
        session: object,
        trip: object,
        *,
        expected_version: int,
        target_day: date | None = None,
        refresh: bool = False,
    ) -> dict[str, object]:
        seen.append((trip, expected_version, target_day, refresh))
        return {}

    trip = object()

    class FakeSession:
        async def get(self, model: object, key: object) -> object:
            return trip

        async def __aenter__(self) -> FakeSession:
            return self

        async def __aexit__(self, *exc: object) -> None:
            return None

    monkeypatch.setattr(route_tasks, "SessionFactory", lambda: FakeSession())
    monkeypatch.setattr(route_tasks, "compute_and_apply_routes", fake_compute)
    trip_id = uuid4()

    await route_tasks._run(trip_id, 3, date(2026, 11, 10), True)
    # A job queued before the flag existed carries none: ordinary reuse, as before.
    await route_tasks._run(trip_id, 3, None)

    assert seen == [(trip, 3, date(2026, 11, 10), True), (trip, 3, None, False)]
