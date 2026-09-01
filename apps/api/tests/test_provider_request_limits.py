from datetime import date
from types import SimpleNamespace
from uuid import uuid4

import pytest

import app.places.router as places_router
import app.trips.router as trips_router
from app.config import Settings
from app.problems import AppError
from app.trips.router import RouteComputeRequest


@pytest.mark.asyncio
async def test_google_place_requests_share_a_per_user_rate_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user_id = uuid4()
    observed: list[tuple[str, str, int, int]] = []

    async def load_settings(_session: object) -> Settings:
        return Settings(google_maps_api_key="server-key")

    async def enforce_limit(
        namespace: str,
        identifier: str,
        *,
        limit: int,
        window_seconds: int,
    ) -> None:
        observed.append((namespace, identifier, limit, window_seconds))

    class PlacesStub:
        configured = True

        def __init__(self, *_args: object) -> None:
            pass

        async def autocomplete(self, *_args: object) -> list[dict[str, object]]:
            return []

        async def place_details(self, *_args: object) -> dict[str, object]:
            return {"id": "places/example"}

    monkeypatch.setattr(places_router, "load_runtime_settings", load_settings)
    monkeypatch.setattr(places_router, "enforce_named_rate_limit", enforce_limit)
    monkeypatch.setattr(places_router, "GoogleTravelService", PlacesStub)
    monkeypatch.setattr(places_router, "get_redis", lambda: object())
    user = SimpleNamespace(id=user_id)

    await places_router.autocomplete_places(
        user,  # type: ignore[arg-type]
        object(),  # type: ignore[arg-type]
        q="東京",
    )
    await places_router.get_place_details(
        "google_places",
        "places/example",
        user,  # type: ignore[arg-type]
        object(),  # type: ignore[arg-type]
    )

    assert observed == [
        (
            "google-places-user",
            str(user_id),
            places_router.GOOGLE_PLACES_USER_LIMIT,
            places_router.GOOGLE_PLACES_USER_WINDOW_SECONDS,
        ),
        (
            "google-places-user",
            str(user_id),
            places_router.GOOGLE_PLACES_USER_LIMIT,
            places_router.GOOGLE_PLACES_USER_WINDOW_SECONDS,
        ),
    ]


@pytest.mark.asyncio
async def test_route_compute_rejects_unbounded_provider_fanout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trip_id = uuid4()
    user_id = uuid4()
    trip = SimpleNamespace(id=trip_id, version=1)
    rows = [SimpleNamespace(day_date=date(2026, 9, 1)) for _ in range(13)]

    async def owned_trip(_session: object, _user_id: object, _trip_id: object) -> object:
        return trip

    async def load_items(_session: object, _trip_id: object) -> list[object]:
        return rows

    async def hydrate(_session: object, _trip: object, values: list[object]) -> list[object]:
        return values

    monkeypatch.setattr(trips_router, "owned_trip", owned_trip)
    monkeypatch.setattr(trips_router, "load_items", load_items)
    monkeypatch.setattr(trips_router, "hydrate_legacy_items", hydrate)

    with pytest.raises(AppError) as captured:
        await trips_router.compute_trip_routes(
            trip_id,
            RouteComputeRequest(version=1),
            SimpleNamespace(id=user_id),  # type: ignore[arg-type]
            object(),  # type: ignore[arg-type]
        )

    assert captured.value.status == 422
    assert captured.value.code == "route_items_limit"
