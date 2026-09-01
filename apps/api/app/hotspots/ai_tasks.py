from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from uuid import UUID

from app.admin.service import load_runtime_settings
from app.db import SessionFactory, engine
from app.hotspots.ai_search import execute_ai_search
from app.infra import get_redis
from app.models import AdminAuditLog, HotspotGuideAISearchRun
from app.problems import AppError


async def _mark_failed(run_id: UUID, exc: Exception) -> None:
    async with SessionFactory() as session:
        run = await session.get(HotspotGuideAISearchRun, run_id)
        if run is None:
            return
        result = run.result_json or {}
        run.status = "partial" if int(result.get("created") or 0) > 0 else "failed"
        run.progress = 100
        run.progress_json = {"stage": "failed"}
        run.error_code = exc.code if isinstance(exc, AppError) else "ai_search_failed"
        run.error_message = "AI 景點介紹搜尋未能完整完成"
        run.completed_at = datetime.now(UTC)
        session.add(
            AdminAuditLog(
                actor_user_id=run.actor_user_id,
                action="hotspot_guide_ai_search_failed",
                target=f"hotspot-guide-ai-search:{run.id}",
                metadata_json={"status": run.status, "error_code": run.error_code},
            )
        )
        await session.commit()


async def _run(run_id: UUID) -> None:
    async with SessionFactory() as session:
        run = await session.get(HotspotGuideAISearchRun, run_id)
        if run is None or run.status not in {"queued", "running", "failed"}:
            return
        try:
            settings = await load_runtime_settings(session)
            await execute_ai_search(session, get_redis(), run, settings)
        except Exception as exc:
            await session.rollback()
            await _mark_failed(run_id, exc)
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
