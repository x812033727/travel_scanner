from __future__ import annotations

import asyncio
from uuid import UUID

from redis import Redis as SyncRedis
from redis.exceptions import RedisError
from rq import Queue, Retry

from app.auth.oauth import attempt_provider_revocation
from app.config import get_settings
from app.db import SessionFactory, engine
from app.models import UserAuthIdentity


def enqueue_provider_revocation(identity_id: UUID) -> bool:
    try:
        connection = SyncRedis.from_url(get_settings().redis_url)
        Queue("auth-revocations", connection=connection).enqueue(
            "app.auth.jobs.run_provider_revocation",
            str(identity_id),
            job_id=f"auth-revocation-{identity_id}",
            job_timeout=60,
            retry=Retry(max=5, interval=[60, 300, 1_800, 7_200, 21_600]),
        )
    except RedisError:
        return False
    return True


async def _run(identity_id: UUID) -> None:
    async with SessionFactory() as session:
        identity = await session.get(UserAuthIdentity, identity_id)
        if identity is None or not identity.revocation_pending:
            return
        if not await attempt_provider_revocation(session, identity):
            raise RuntimeError("provider revocation remains pending")


def run_provider_revocation(identity_id: str) -> None:
    async def run_and_close_resources() -> None:
        try:
            await _run(UUID(identity_id))
        finally:
            await engine.dispose()

    asyncio.run(run_and_close_resources())
