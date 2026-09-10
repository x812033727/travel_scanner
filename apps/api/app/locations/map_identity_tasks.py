"""Bounded review-only Google candidate batches on the existing place worker queue."""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from redis import Redis as SyncRedis
from redis.exceptions import RedisError
from rq import Queue
from rq.exceptions import NoSuchJobError
from rq.job import Job

from app.admin.service import load_runtime_settings
from app.config import get_settings
from app.db import SessionFactory, engine
from app.infra import get_redis
from app.locations.map_identity_review import (
    BATCH_TTL_SECONDS,
    CatalogReference,
    collect_candidates,
)
from app.models import AdminAuditLog
from app.problems import AppError


def batch_key(batch_id: str | UUID) -> str:
    return f"map-identities:batch:{batch_id}"


def enqueue_identity_batch(batch_id: UUID, actor_id: UUID, targets: list[CatalogReference]) -> None:
    connection = SyncRedis.from_url(get_settings().redis_url)
    try:
        Queue("hotspot-places", connection=connection).enqueue(
            "app.locations.map_identity_tasks.run_identity_batch",
            str(batch_id),
            str(actor_id),
            [target.model_dump(mode="json") for target in targets],
            job_timeout=900,
            job_id=f"map-identities-{batch_id}",
        )
    finally:
        connection.close()


def identity_batch_job_status(batch_id: UUID) -> str | None:
    """Observe worker failure even when a killed worker could not update our status."""
    connection = SyncRedis.from_url(get_settings().redis_url)
    try:
        status = Job.fetch(f"map-identities-{batch_id}", connection=connection).get_status()
        return status.value if status else None
    except (NoSuchJobError, RedisError):
        return None
    finally:
        connection.close()


async def _run_batch(batch_id: UUID, actor_id: UUID, raw_targets: list[dict[str, Any]]) -> None:
    if not 1 <= len(raw_targets) <= 50:
        raise ValueError("An identity batch must contain 1 to 50 explicit catalog targets")
    targets = [CatalogReference.model_validate(raw) for raw in raw_targets]
    redis = get_redis()
    raw_state = await redis.get(batch_key(batch_id))
    if not raw_state:
        return
    state = json.loads(raw_state)
    if state.get("status") in {"completed", "partial", "failed"}:
        return
    state["status"] = "running"
    await redis.set(batch_key(batch_id), json.dumps(state), ex=BATCH_TTL_SECONDS)
    async with SessionFactory() as session:
        settings = await load_runtime_settings(session)
        for reference in targets:
            if any(
                result["kind"] == reference.kind and result["id"] == str(reference.id)
                for result in state["results"]
            ):
                continue
            outcome = "failed"
            try:
                result = await collect_candidates(session, redis, settings, reference, actor_id)
                outcome = "pending" if result["candidates"] else "unmatched"
            except AppError as exc:
                await session.rollback()
                outcome = exc.code
            except Exception:
                await session.rollback()
            state["results"].append(
                {
                    "kind": reference.kind,
                    "id": str(reference.id),
                    "outcome": outcome,
                }
            )
            state["processed"] = len(state["results"])
            await redis.set(batch_key(batch_id), json.dumps(state), ex=BATCH_TTL_SECONDS)
            if outcome in {"google_maps_usage_guard", "google_maps_not_configured"}:
                break
        state["status"] = (
            "completed"
            if state["processed"] == state["total"]
            and all(result["outcome"] in {"pending", "unmatched"} for result in state["results"])
            else "partial"
        )
        state["completed_at"] = datetime.now(UTC).isoformat()
        session.add(
            AdminAuditLog(
                actor_user_id=actor_id,
                action="map_identity.batch_completed",
                target=f"map-identity-batch:{batch_id}",
                metadata_json={
                    "status": state["status"],
                    "total": state["total"],
                    "processed": state["processed"],
                    "results": state["results"],
                },
            )
        )
        await session.commit()
        await redis.set(batch_key(batch_id), json.dumps(state), ex=BATCH_TTL_SECONDS)


def run_identity_batch(batch_id: str, actor_id: str, targets: list[dict[str, Any]]) -> None:
    async def run_and_close() -> None:
        try:
            await _run_batch(UUID(batch_id), UUID(actor_id), targets)
        except Exception:
            redis = get_redis()
            raw = await redis.get(batch_key(batch_id))
            if raw:
                state = json.loads(raw)
                state.update(
                    {
                        "status": "failed",
                        "error_code": "worker_failed",
                        "completed_at": datetime.now(UTC).isoformat(),
                    }
                )
                await redis.set(batch_key(batch_id), json.dumps(state), ex=BATCH_TTL_SECONDS)
            raise
        finally:
            try:
                await get_redis().aclose()
            finally:
                get_redis.cache_clear()
                await engine.dispose()

    asyncio.run(run_and_close())
