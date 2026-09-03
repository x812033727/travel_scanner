from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from uuid import UUID

import httpx
from pydantic import ValidationError

from app.admin.service import load_runtime_settings
from app.db import SessionFactory, engine
from app.hotspots.ai_search import execute_ai_search, summarize_provider_error
from app.infra import get_redis
from app.models import AdminAuditLog, HotspotGuideAISearchRun
from app.problems import AppError

logger = logging.getLogger(__name__)

# Only runs in these states may execute. Everything else is terminal, so a stale
# queued job (for example a retry that was scheduled before the worker ran a
# scheduler) never re-runs a search the admin has already seen fail.
RUNNABLE_STATUSES = frozenset({"queued", "running"})
EXPECTED_FAILURES = (httpx.HTTPError, ValidationError, ValueError, AppError)


async def _mark_failed(run_id: UUID, exc: Exception, summary: str) -> None:
    async with SessionFactory() as session:
        run = await session.get(HotspotGuideAISearchRun, run_id)
        if run is None:
            return
        result = run.result_json or {}
        run.status = "partial" if int(result.get("created") or 0) > 0 else "failed"
        run.progress = 100
        run.progress_json = {"stage": "failed"}
        run.error_code = exc.code if isinstance(exc, AppError) else "ai_search_failed"
        run.error_message = f"AI 景點介紹搜尋未能完整完成：{summary}"
        run.completed_at = datetime.now(UTC)
        session.add(
            AdminAuditLog(
                actor_user_id=run.actor_user_id,
                action="hotspot_guide_ai_search_failed",
                target=f"hotspot-guide-ai-search:{run.id}",
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
        run = await session.get(HotspotGuideAISearchRun, run_id)
        if run is None or run.status not in RUNNABLE_STATUSES:
            logger.info(
                "hotspot guide AI search %s skipped: %s",
                run_id,
                "missing" if run is None else run.status,
            )
            return
        try:
            settings = await load_runtime_settings(session)
            await execute_ai_search(session, get_redis(), run, settings)
        except Exception as exc:
            await session.rollback()
            summary = summarize_provider_error(exc)
            if isinstance(exc, EXPECTED_FAILURES):
                logger.warning(
                    "hotspot guide AI search %s failed (%s): %s",
                    run_id,
                    type(exc).__name__,
                    summary,
                )
            else:
                logger.exception("hotspot guide AI search %s crashed: %s", run_id, summary)
            await _mark_failed(run_id, exc, summary)
            raise


def run_hotspot_guide_ai_search(run_id: str) -> None:
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
