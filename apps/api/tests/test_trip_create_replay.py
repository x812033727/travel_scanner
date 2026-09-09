"""Create requests retain their identity through edits, lost replies and cache loss."""

import asyncio
import json
from datetime import date, timedelta
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from test_trip_preferences import harness as shared_harness

from app.models import TripPlan
from app.trips import router as trips

harness = shared_harness


def payload():
    start = date.today() + timedelta(days=90)
    return {
        "source": "blank", "planning_mode": "manual_blank", "name": "Tokyo calm trip",
        "destination_name": "Tokyo", "start_date": start.isoformat(),
        "end_date": (start + timedelta(days=3)).isoformat(),
        "routing": {"auto_compute": False},
    }


async def create(h, body=None, key="create-attempt-1234", **kwargs):
    return await h["client"].post(
        "/trips", json=body or payload(), headers={"Idempotency-Key": key, **kwargs},
    )


async def test_same_request_replays_once_and_payload_changes_conflict(harness):
    h = harness
    before = await h["session"].scalar(select(func.count()).select_from(TripPlan))
    first = await create(h)
    assert first.status_code == 201, first.text
    repeated = await create(h)
    assert repeated.status_code == 201, repeated.text
    assert repeated.json()["id"] == first.json()["id"]
    changed = await create(h, {**payload(), "name": "Edited while uncertain"})
    assert changed.status_code == 409
    assert changed.json()["code"] == "trip_create_payload_conflict"
    assert await h["session"].scalar(select(func.count()).select_from(TripPlan)) == before + 1
    record = json.loads(await h["redis"].get(trips._trip_create_request_key(
        h["user"].id, "create-attempt-1234",
    )))
    assert record["trip_id"] == first.json()["id"]
    assert len(record["request_hash"]) == 64
    assert "create-attempt-1234" not in json.dumps(first.json())


async def test_hash_uses_normalized_values_and_sorted_object_keys(harness):
    first = await create(harness, {**payload(), "notes": "  Keep original  "})
    reversed_payload = dict(reversed(list({**payload(), "notes": "Keep original"}.items())))
    same = await create(harness, reversed_payload)
    assert same.status_code == 201
    assert same.json()["id"] == first.json()["id"]


async def test_same_key_is_isolated_between_accounts(harness):
    first = await create(harness)
    other = await create(harness, **{"x-test-user": "other"})
    assert first.status_code == other.status_code == 201
    assert first.json()["id"] != other.json()["id"]


async def test_durable_record_recovers_after_cache_eviction(harness):
    first = await create(harness)
    await harness["redis"].flushdb()
    same = await create(harness)
    assert same.status_code == 201
    assert same.json()["id"] == first.json()["id"]
    changed = await create(harness, {**payload(), "destination_name": "Osaka"})
    assert changed.status_code == 409


async def test_retry_recovers_commit_when_redis_write_fails(harness, monkeypatch):
    h = harness
    original = h["redis"].set
    monkeypatch.setattr(h["redis"], "set", AsyncMock(side_effect=ConnectionError("cache offline")))
    with pytest.raises(ConnectionError, match="cache offline"):
        await create(h)
    count = await h["session"].scalar(select(func.count()).select_from(TripPlan))
    monkeypatch.setattr(h["redis"], "set", original)
    repeated = await create(h)
    assert repeated.status_code == 201
    assert await h["session"].scalar(select(func.count()).select_from(TripPlan)) == count


@pytest.mark.parametrize("cached", ["legacy", "bad-json", "missing-trip"])
async def test_legacy_or_invalid_cache_requires_explicit_recovery(harness, cached):
    h = harness
    raw = str(h["trip"].id) if cached == "legacy" else "malformed"
    if cached == "missing-trip":
        from uuid import uuid4
        raw = json.dumps({"trip_id": str(uuid4()), "request_hash": trips._trip_create_payload_hash(
            trips.SaveTripRequest.model_validate(payload()),
        )})
    await h["redis"].set(trips._trip_create_request_key(h["user"].id, "create-attempt-1234"), raw)
    before = await h["session"].scalar(select(func.count()).select_from(TripPlan))
    response = await create(h)
    assert response.status_code == 409
    assert response.json()["code"] == "trip_create_recovery_required"
    assert await h["session"].scalar(select(func.count()).select_from(TripPlan)) == before


async def test_concurrent_same_account_requests_create_one_trip(harness):
    h = harness
    engine = h["session"].bind
    if engine.dialect.name != "postgresql":
        pytest.skip("PostgreSQL transaction-held row lock")
    maker = async_sessionmaker(engine, expire_on_commit=False)
    request = trips.SaveTripRequest.model_validate(payload())

    async def attempt():
        async with maker() as session:
            return await trips.save_trip(request, h["user"], session, "concurrent-create-1234")

    before = await h["session"].scalar(select(func.count()).select_from(TripPlan))
    first, second = await asyncio.gather(attempt(), attempt())
    assert first["id"] == second["id"]
    assert await h["session"].scalar(select(func.count()).select_from(TripPlan)) == before + 1
