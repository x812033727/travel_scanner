import asyncio
from uuid import UUID

from sqlalchemy import select

from app.db import SessionFactory
from app.infra import get_redis
from app.models import SearchJob, SearchRequest, UsageReservation
from app.search.events import publish_event
from app.search.orchestrator import orchestrate_search
from app.usage.service import release_reservation, usage_status


async def _run(search_id: UUID) -> None:
    async with SessionFactory() as session:
        try:
            await orchestrate_search(session, search_id)
        except Exception:
            await session.rollback()
            search = await session.get(SearchRequest, search_id)
            reservation = await session.scalar(
                select(UsageReservation).where(UsageReservation.resource_id == search_id)
            )
            job = await session.scalar(select(SearchJob).where(SearchJob.search_id == search_id))
            if reservation is not None:
                await release_reservation(session, reservation, "system_error")
            if search is not None:
                search.status = "failed"
                search.progress = 100
                search.warnings_json = ["搜尋處理發生系統錯誤，已自動退回保留次數。"]
            if job is not None:
                job.status = "failed"
                job.error = "Search processing failed"
            await session.commit()
            await publish_event(
                get_redis(),
                search_id,
                "search.failed",
                100,
                {
                    "status": "failed",
                    "warnings": ["搜尋處理發生系統錯誤，已自動退回保留次數。"],
                    "usage": usage_status(reservation).model_dump() if reservation else None,
                },
            )
            raise


def run_search_job(search_id: str) -> None:
    asyncio.run(_run(UUID(search_id)))
