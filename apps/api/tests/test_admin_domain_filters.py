"""Canonical location links and dashboard filters select exact database rows."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.db import get_session
from app.hotspots.admin_router import router
from app.models import Base, TravelHotspot, User


@pytest_asyncio.fixture(
    params=[
        "sqlite",
        pytest.param(
            "postgresql",
            marks=pytest.mark.skipif(
                os.getenv("RUN_INTEGRATION_TESTS") != "1",
                reason="PostgreSQL integration not enabled",
            ),
        ),
    ]
)
async def client(request: pytest.FixtureRequest) -> AsyncIterator[AsyncClient]:
    schema = "admin_filters_" + uuid4().hex
    administrator = None
    if request.param == "postgresql":
        from app.config import get_settings

        administrator = create_async_engine(get_settings().database_url)
        async with administrator.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = create_async_engine(
            get_settings().database_url, connect_args={"server_settings": {"search_path": schema}}
        )
    else:
        engine = create_async_engine("sqlite+aiosqlite://")
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        async with async_sessionmaker(engine, expire_on_commit=False)() as session:
            user = User(
                id=uuid4(), email="domain-filters@example.test", is_admin=True, is_active=True
            )
            session.add(user)
            for index, (status, lat, lon) in enumerate(
                [
                    ("pending", None, None),
                    ("approved", None, None),
                    ("rejected", None, None),
                    ("approved", 35.0, 139.0),
                    ("disabled", 0.0, 0.0),
                ]
            ):
                session.add(
                    TravelHotspot(
                        id=uuid4(),
                        slug=f"location-{index}",
                        name=f"Location {index}",
                        city_code="TYO",
                        city_name="Tokyo",
                        destination_id="tokyo",
                        country_code="JP",
                        country_name="Japan",
                        category="culture",
                        search_text=f"Location {index}",
                        review_status=status,
                        latitude=lat,
                        longitude=lon,
                        is_active=False,
                    )
                )
            await session.commit()

            async def database():
                yield session

            app = FastAPI()
            app.include_router(router)
            app.dependency_overrides[current_user] = lambda: user
            app.dependency_overrides[get_session] = database
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as http:
                yield http
    finally:
        await engine.dispose()
        if administrator is not None:
            async with administrator.begin() as connection:
                await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
            await administrator.dispose()


@pytest.mark.asyncio
async def test_status_and_missing_location_counts_match_rows_and_facets(
    client: AsyncClient,
) -> None:
    response = await client.get("/admin/hotspots/candidates?missing_location=true&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3 and data["pages"] == 2 and len(data["items"]) == 2
    assert data["facets"]["countries"][0]["count"] == 3
    assert data["facets"]["categories"][0]["count"] == 3
    second = await client.get("/admin/hotspots/candidates?missing_location=true&limit=2&page=2")
    assert len(second.json()["items"]) == 1
    assert all(item["latitude"] is None or item["longitude"] is None for item in data["items"])
    combined = await client.get("/admin/hotspots/candidates?missing_location=true&status=approved")
    assert combined.json()["total"] == 1
    assert combined.json()["items"][0]["name"] == "Location 1"
    all_rows = await client.get("/admin/hotspots/candidates?missing_location=false")
    assert all_rows.json()["total"] == 5  # Zero coordinates are valid, not missing.
    pending = await client.get("/admin/hotspots/candidates?status=pending")
    assert pending.json()["total"] == 1


@pytest.mark.asyncio
async def test_exact_hotspot_filter_cannot_return_a_different_place(client: AsyncClient) -> None:
    listing = (await client.get("/admin/hotspots/candidates")).json()
    expected = next(item for item in listing["items"] if item["name"] == "Location 3")
    result = await client.get(f"/admin/hotspots/candidates?hotspot_id={expected['id']}")
    assert result.status_code == 200
    assert result.json()["total"] == 1
    assert result.json()["items"] == [expected]
    assert result.json()["facets"]["countries"][0]["count"] == 1
    mismatch = await client.get(
        f"/admin/hotspots/candidates?hotspot_id={expected['id']}&status=pending"
    )
    assert mismatch.json()["total"] == 0 and mismatch.json()["items"] == []
    unknown = await client.get(f"/admin/hotspots/candidates?hotspot_id={uuid4()}")
    assert unknown.json()["total"] == 0
    assert (await client.get("/admin/hotspots/candidates?hotspot_id=invalid")).status_code == 422
