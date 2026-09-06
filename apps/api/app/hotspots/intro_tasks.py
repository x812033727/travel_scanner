"""The queued job that drafts one attraction's introductions.

Mirrors ``app.hotspots.ai_tasks``: a run row records what was asked for, the job
executes it once, and a terminal run is never executed again — a stale queued job
must not re-spend the budget on work an administrator has already seen finish.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from uuid import UUID

import httpx
from pydantic import ValidationError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.config import Settings
from app.db import SessionFactory, engine
from app.hotspots.ai_search import summarize_provider_error
from app.hotspots.guides import consume_search_budget
from app.hotspots.intro_generation import build_intro_provider, generate_intro_drafts
from app.infra import get_redis
from app.models import AdminAuditLog, HotspotIntroRun, TravelHotspot
from app.problems import AppError

logger = logging.getLogger(__name__)

RUNNABLE_STATUSES = frozenset({"queued", "running"})
EXPECTED_FAILURES = (httpx.HTTPError, ValidationError, ValueError, AppError)


async def execute_intro_run(
    session: AsyncSession,
    redis: Redis,
    run: HotspotIntroRun,
    settings: Settings,
) -> None:
    """Draft every requested locale for one attraction and record what happened."""

    hotspot = await session.get(TravelHotspot, run.hotspot_id)
    if hotspot is None:
        raise AppError(404, "hotspot_not_found", "找不到這個景點")
    # Charged before the call, not after: a crash mid-request still cost the vendor.
    if not await consume_search_budget(
        redis, "intro-call", settings.hotspot_intro_ai_daily_call_budget
    ):
        raise AppError(429, "hotspot_intro_ai_quota_exhausted", "今日介紹產生額度已用完")
    run.status = "running"
    run.started_at = datetime.now(UTC)
    run.progress = 10
    run.progress_json = {"stage": "drafting"}
    await session.flush()

    provider = build_intro_provider(settings, run.provider)  # type: ignore[arg-type]
    try:
        report = await generate_intro_drafts(
            session,
            hotspot,
            locales=list(run.requested_locales),  # type: ignore[arg-type]
            provider=provider,
            run_id=run.id,
            force=run.force,
        )
    finally:
        await provider.close()

    run.status = "partial" if report["rejected"] else "completed"
    run.progress = 100
    run.progress_json = {"stage": "done"}
    run.usage_json = report.get("usage") or {}
    run.result_json = {
        "created": report["created"],
        "kept_approved": report["kept_approved"],
        "rejected": report["rejected"],
    }
    run.completed_at = datetime.now(UTC)
    session.add(
        AdminAuditLog(
            actor_user_id=run.actor_user_id,
            action="hotspot_intro_generation_completed",
            target=f"hotspot-intro-run:{run.id}",
            metadata_json={
                "hotspot_id": str(run.hotspot_id),
                "created": report["created"],
                "kept_approved": report["kept_approved"],
                "rejected": report["rejected"],
                "status": run.status,
            },
        )
    )
    await session.commit()


async def _mark_failed(run_id: UUID, exc: Exception, summary: str) -> None:
    async with SessionFactory() as session:
        run = await session.get(HotspotIntroRun, run_id)
        if run is None:
            return
        created = (run.result_json or {}).get("created") or []
        run.status = "partial" if created else "failed"
        run.progress = 100
        run.progress_json = {"stage": "failed"}
        run.error_code = (
            exc.code if isinstance(exc, AppError) else "hotspot_intro_generation_failed"
        )
        run.error_message = f"景點介紹產生未能完成：{summary}"
        run.completed_at = datetime.now(UTC)
        session.add(
            AdminAuditLog(
                actor_user_id=run.actor_user_id,
                action="hotspot_intro_generation_failed",
                target=f"hotspot-intro-run:{run.id}",
                metadata_json={
                    "status": run.status,
                    "error_code": run.error_code,
                    "error_message": summary,
                },
            )
        )
        await session.commit()


async def _run(run_id: UUID) -> None:
    async with SessionFactory() as session:
        run = await session.get(HotspotIntroRun, run_id)
        if run is None or run.status not in RUNNABLE_STATUSES:
            logger.info(
                "hotspot intro run %s skipped: %s",
                run_id,
                "missing" if run is None else run.status,
            )
            return
        try:
            settings = await load_runtime_settings(session)
            await execute_intro_run(session, get_redis(), run, settings)
        except Exception as exc:
            await session.rollback()
            summary = summarize_provider_error(exc)
            if isinstance(exc, EXPECTED_FAILURES):
                logger.warning(
                    "hotspot intro run %s failed (%s): %s", run_id, type(exc).__name__, summary
                )
            else:
                logger.exception("hotspot intro run %s crashed: %s", run_id, summary)
            await _mark_failed(run_id, exc, summary)
            raise


def run_hotspot_intro_generation(run_id: str) -> None:
    async def run_and_close_resources() -> None:
        try:
            await _run(UUID(run_id))
        finally:
            try:
                await get_redis().aclose()
            finally:
                get_redis.cache_clear()
                await engine.dispose()

    asyncio.run(run_and_close_resources())
