"""Real PostgreSQL locks, including the missing-row first-write race; no paid calls."""

from __future__ import annotations

import asyncio
import os
from datetime import UTC, datetime
from typing import cast
from uuid import uuid4

import pytest
from redis.asyncio import Redis
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.admin import service
from app.admin.schemas import ProviderSettingsSnapshot, ProviderSettingsUpdate
from app.config import get_settings
from app.models import AdminAuditLog, ProviderConfig, User
from app.problems import AppError


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.asyncio
@pytest.mark.parametrize("existing", [False, True])
@pytest.mark.parametrize("guarded", [False, True])
async def test_concurrent_provider_saves_serialize_first_create_and_existing_rows(
    monkeypatch: pytest.MonkeyPatch,
    existing: bool,
    guarded: bool,
) -> None:
    engine = create_async_engine(get_settings().database_url)
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    provider = f"test_settings_{uuid4().hex}"
    actor = User(id=uuid4(), email=f"{provider}@example.com", password_hash="unused", is_admin=True)
    timestamp = datetime(2026, 9, 1, tzinfo=UTC)
    monkeypatch.setitem(
        service.PROVIDER_DEFINITIONS,
        provider,
        service.ProviderDefinition(
            label="Concurrency fixture",
            description="No provider access",
            config_fields=("route_cache_ttl_seconds", "weather_cache_ttl_seconds"),
            secret_fields=("google_maps_api_key",),
        ),
    )

    async def snapshot(*_args: object) -> ProviderSettingsSnapshot:
        return ProviderSettingsSnapshot(providers=[], audit=[], encryption_source="test")

    monkeypatch.setattr(service, "settings_snapshot", snapshot)
    async with sessions() as setup:
        setup.add(actor)
        await setup.flush()
        if existing:
            setup.add(
                ProviderConfig(provider=provider, enabled=True, config={}, updated_at=timestamp)
            )
        await setup.commit()
    barrier = asyncio.Event()
    arrivals = 0
    original_lock = service._locked_provider_config

    async def synchronized_lock(session: AsyncSession, name: str) -> ProviderConfig | None:
        nonlocal arrivals
        arrivals += 1
        if arrivals == 2:
            barrier.set()
        await asyncio.wait_for(barrier.wait(), timeout=5)
        return await original_lock(session, name)

    monkeypatch.setattr(service, "_locked_provider_config", synchronized_lock)

    async def save(field: str, value: int, secret: bool) -> int:
        payload = ProviderSettingsUpdate(
            config={field: value},
            secrets={"google_maps_api_key": "preserved-secret"} if secret else {},
        )
        if guarded:
            payload.expected_updated_at = timestamp if existing else None
        async with sessions() as session:
            try:
                await service.update_provider_settings(
                    session,
                    provider,
                    payload,
                    actor,
                    cast(Redis, object()),
                )
            except AppError as error:
                assert error.code == "provider_setting_conflict"
                return error.status
        return 200

    try:
        results = await asyncio.wait_for(
            asyncio.gather(
                save("route_cache_ttl_seconds", 1200, True),
                save("weather_cache_ttl_seconds", 3600, False),
            ),
            timeout=15,
        )
        assert sorted(results) == ([200, 409] if guarded else [200, 200])
        async with sessions() as verify:
            rows = (
                await verify.scalars(
                    select(ProviderConfig).where(
                        ProviderConfig.provider == provider,
                    )
                )
            ).all()
            assert len(rows) == 1
            if guarded:
                assert len(rows[0].config) == 1
            else:
                assert rows[0].config == {
                    "route_cache_ttl_seconds": 1200,
                    "weather_cache_ttl_seconds": 3600,
                }
                assert service.decrypt_secrets(rows[0].secret_config_encrypted) == {
                    "google_maps_api_key": "preserved-secret",
                }
    finally:
        async with sessions() as cleanup:
            await cleanup.execute(delete(AdminAuditLog).where(AdminAuditLog.target == provider))
            await cleanup.execute(delete(ProviderConfig).where(ProviderConfig.provider == provider))
            await cleanup.execute(delete(User).where(User.id == actor.id))
            await cleanup.commit()
        await engine.dispose()
