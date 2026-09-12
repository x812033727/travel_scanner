"""The inline enrichment command: inventory without spending, deterministic keys, resume."""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import date
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.catalog_review import enrich_cli
from app.catalog_review.enrich_cli import (
    build_request,
    enrich_food_merchants,
    enrichment_idempotency_key,
)
from app.config import Settings
from app.models import Base, CatalogReviewRun, FoodMerchant, User

ADMIN = "Admin@Example.test"


def merchant(**overrides: Any) -> FoodMerchant:
    values: dict[str, Any] = {
        "slug": f"tokyo-{uuid4().hex[:8]}",
        "destination_id": "tokyo",
        "country_code": "JP",
        "name": "Sushi Dai",
        "local_name": "寿司大",
        "review_status": "pending",
        "map_match_status": "unverified",
        "is_active": False,
    }
    values.update(overrides)
    return FoodMerchant(**values)


@pytest_asyncio.fixture
async def db(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[async_sessionmaker[Any]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        session.add_all(
            [
                User(id=uuid4(), email=ADMIN.lower(), is_admin=True, is_active=True),
                User(id=uuid4(), email="member@example.test", is_admin=False, is_active=True),
                merchant(),
                merchant(slug="seoul-hani", destination_id="seoul", country_code="KR"),
                merchant(slug="tokyo-done", review_status="approved", google_place_id="ChIJdone"),
            ]
        )
        await session.commit()
    redis = SimpleNamespace(aclose=AsyncMock())
    get_redis = Mock(return_value=redis)
    get_redis.cache_clear = Mock()
    monkeypatch.setattr(enrich_cli, "SessionFactory", factory)
    monkeypatch.setattr(enrich_cli, "engine", SimpleNamespace(dispose=AsyncMock()))
    monkeypatch.setattr(enrich_cli, "get_redis", get_redis)
    monkeypatch.setattr(
        enrich_cli,
        "load_runtime_settings",
        AsyncMock(return_value=Settings(_env_file=None, hotspot_guide_gemini_api_key="k")),
    )
    try:
        yield factory
    finally:
        await engine.dispose()


def test_idempotency_key_is_deterministic_per_actor_args_and_day() -> None:
    actor = UUID(int=1)
    request = build_request(destination_ids=["tokyo"], limit=None, max_calls=None, identify=True)
    same = enrichment_idempotency_key(actor, request, date(2026, 9, 12))
    assert same == enrichment_idempotency_key(actor, request, date(2026, 9, 12))
    assert same.startswith("cli-enrich-") and len(same) == len("cli-enrich-") + 32
    assert same != enrichment_idempotency_key(actor, request, date(2026, 9, 13))
    assert same != enrichment_idempotency_key(UUID(int=2), request, date(2026, 9, 12))
    assert same != enrichment_idempotency_key(
        actor,
        build_request(destination_ids=["tokyo"], limit=5, max_calls=None, identify=True),
        date(2026, 9, 12),
    )
    assert same != enrichment_idempotency_key(
        actor,
        build_request(destination_ids=["tokyo"], limit=None, max_calls=None, identify=False),
        date(2026, 9, 12),
    )


def test_build_request_rejects_unknown_destinations_and_bad_limits() -> None:
    with pytest.raises(ValidationError):
        build_request(destination_ids=["atlantis"], limit=None, max_calls=None, identify=True)
    with pytest.raises(ValidationError):
        build_request(destination_ids=[], limit=0, max_calls=None, identify=True)
    request = build_request(destination_ids=[" Tokyo "], limit=3, max_calls=6, identify=False)
    assert request.mode == "enrich_merchants" and request.scope == "foods"
    assert request.destination_ids == ["tokyo"] and request.limit == 3
    assert request.max_calls == 6 and request.identify_places is False


async def test_dry_run_lists_pending_merchants_without_creating_a_run(
    db: async_sessionmaker[Any],
) -> None:
    report = await enrich_food_merchants(
        actor_email=ADMIN,
        destination_ids=[],
        limit=None,
        max_calls=None,
        identify=True,
        dry_run=True,
        idempotency_key=None,
    )
    assert report["dry_run"] is True
    assert report["pending"] == 2
    assert report["by_destination"] == {"seoul": 1, "tokyo": 1}
    assert report["kr"] == 1 and report["no_place_id"] == 1
    assert report["estimated_gemini_calls"] == 2
    assert report["estimated_google_calls"] == 1
    assert report["gaps"]["missing_exact_map_identity"] == 2
    async with db() as session:
        assert (await session.scalars(select(CatalogReviewRun))).all() == []


async def test_non_admin_email_is_refused(db: async_sessionmaker[Any]) -> None:
    for email in ("member@example.test", "nobody@example.test"):
        report = await enrich_food_merchants(
            actor_email=email,
            destination_ids=[],
            limit=None,
            max_calls=None,
            identify=True,
            dry_run=False,
            idempotency_key=None,
        )
        assert report == {"error": "actor_not_admin", "email": email}
    async with db() as session:
        assert (await session.scalars(select(CatalogReviewRun))).all() == []


async def test_run_is_created_executed_inline_and_resumed_on_replay(
    db: async_sessionmaker[Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    executed = AsyncMock()
    monkeypatch.setattr(enrich_cli, "_run", executed)
    first = await enrich_food_merchants(
        actor_email=ADMIN,
        destination_ids=["tokyo"],
        limit=None,
        max_calls=6,
        identify=False,
        dry_run=False,
        idempotency_key="cli-enrich-test",
    )
    assert first["created"] is True and first["resumed"] is False
    assert first["run"]["mode"] == "enrich_merchants" and first["run"]["scope"] == "foods"
    assert first["run"]["max_calls"] == 6 and first["run"]["counts"]["total"] == 1
    assert first["corrections_by_kind"] == {}
    run_id = UUID(first["run"]["id"])
    executed.assert_awaited_once_with(run_id)
    # Redis and the engine are released even though the worker ran inline.
    enrich_cli.get_redis.return_value.aclose.assert_awaited()
    enrich_cli.engine.dispose.assert_awaited()

    async with db() as session:
        run = await session.get(CatalogReviewRun, run_id)
        assert run is not None
        run.status = "partial"
        await session.commit()
    second = await enrich_food_merchants(
        actor_email=ADMIN,
        destination_ids=["tokyo"],
        limit=None,
        max_calls=6,
        identify=False,
        dry_run=False,
        idempotency_key="cli-enrich-test",
    )
    assert second["created"] is False and second["resumed"] is True
    assert second["run"]["id"] == str(run_id)
    assert executed.await_count == 2
    async with db() as session:
        assert len((await session.scalars(select(CatalogReviewRun))).all()) == 1


async def test_a_replayed_run_that_cannot_resume_is_only_reported(
    db: async_sessionmaker[Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    executed = AsyncMock()
    monkeypatch.setattr(enrich_cli, "_run", executed)
    await enrich_food_merchants(
        actor_email=ADMIN,
        destination_ids=[],
        limit=None,
        max_calls=None,
        identify=True,
        dry_run=False,
        idempotency_key="cli-enrich-done",
    )
    async with db() as session:
        (run,) = (await session.scalars(select(CatalogReviewRun))).all()
        run.status = "completed"
        await session.commit()
    replay = await enrich_food_merchants(
        actor_email=ADMIN,
        destination_ids=[],
        limit=None,
        max_calls=None,
        identify=True,
        dry_run=False,
        idempotency_key="cli-enrich-done",
    )
    assert replay == {
        "run": replay["run"],
        "created": False,
        "resumed": False,
        "idempotency_key": "cli-enrich-done",
    }
    assert replay["run"]["status"] == "completed"
    assert executed.await_count == 1
