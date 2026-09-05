from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import fakeredis.aioredis
import pytest

import app.restaurants.router as restaurants_router
from app.config import Settings
from app.restaurants.router import RestaurantSearchRequest, restaurant_search


@pytest.mark.asyncio
async def test_restaurant_search_replays_the_first_result_for_the_same_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A retried request must not spend Google quota a second time."""

    calls: list[dict[str, Any]] = []

    async def fake_search(*_args: Any, **kwargs: Any) -> dict[str, Any]:
        calls.append(kwargs)
        return {"hotspot_id": "h1", "items": [{"place_id": "p1"}], "next_cursor": None}

    async def no_rate_limit(*_args: Any, **_kwargs: Any) -> None:
        return None

    async def settings(_session: Any) -> Settings:
        return Settings()

    monkeypatch.setattr(restaurants_router, "search_restaurants", fake_search)
    monkeypatch.setattr(restaurants_router, "enforce_named_rate_limit", no_rate_limit)
    monkeypatch.setattr(restaurants_router, "load_runtime_settings", settings)

    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    user = SimpleNamespace(id=uuid4())
    hotspot_id = uuid4()
    payload = RestaurantSearchRequest()

    first = await restaurant_search(
        hotspot_id, payload, user, None, redis, "zh-TW", "retry-key-0001"  # type: ignore[arg-type]
    )
    replay = await restaurant_search(
        hotspot_id, payload, user, None, redis, "zh-TW", "retry-key-0001"  # type: ignore[arg-type]
    )
    fresh = await restaurant_search(
        hotspot_id, payload, user, None, redis, "zh-TW", "retry-key-0002"  # type: ignore[arg-type]
    )

    assert len(calls) == 2
    assert first["items"] == replay["items"] == fresh["items"]
    assert replay["replayed"] is True
    assert "replayed" not in first and "replayed" not in fresh
