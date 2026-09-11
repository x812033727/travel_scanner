"""Both branches of /destinations/discover answer with the same keys.

The wizard reads `recommendations` unconditionally. When the caller sets no dates,
no trip length and no countries, the endpoint took a branch that omitted that key
entirely, and the five-step form crashed to the error boundary with every answer
lost. These tests pin the shape rather than the contents, so either branch may
change what it recommends without breaking the caller again.
"""

from collections.abc import AsyncIterator
from typing import Any

import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db import Base, get_session
from app.problems import AppError, app_error_handler
from app.places.router import router as destinations_router

REQUIRED = {"origin", "source", "recommendations", "assumptions"}


@pytest_asyncio.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async def database() -> AsyncIterator[Any]:
        async with factory() as session:
            yield session

    app = FastAPI()
    app.include_router(destinations_router, prefix="/api/v1")
    app.add_exception_handler(AppError, app_error_handler)
    app.dependency_overrides[get_session] = database
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
        headers={"X-Travel-Locale": "en"},
    ) as http:
        yield http
    await engine.dispose()


def _body(**over: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "origin": "TPE",
        "destination_countries": ["JP"],
        "travel_window": {"start_date": "2026-11-01", "end_date": "2026-11-30"},
        "trip_length_range": {"min_days": 3, "max_days": 6},
        "travelers": {"adults": 2, "children": 0, "children_ages": [], "rooms": 1},
        "top_n": 3,
    }
    base.update(over)
    return base


@pytest.mark.asyncio
async def test_narrowed_request_carries_the_shared_keys(client: httpx.AsyncClient) -> None:
    response = await client.post("/api/v1/destinations/discover", json=_body())
    assert response.status_code == 200, response.text
    assert REQUIRED <= set(response.json())


@pytest.mark.asyncio
async def test_wide_open_request_still_carries_recommendations(
    client: httpx.AsyncClient,
) -> None:
    """No dates, no trip length, no countries — the branch that used to omit the key."""
    response = await client.post(
        "/api/v1/destinations/discover",
        json=_body(destination_countries=[], travel_window=None, trip_length_range=None),
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert REQUIRED <= set(payload), f"missing {REQUIRED - set(payload)}"
    assert isinstance(payload["recommendations"], list)
    # This branch answers with city candidates instead; the wizard renders those.
    assert isinstance(payload.get("candidates"), list)
