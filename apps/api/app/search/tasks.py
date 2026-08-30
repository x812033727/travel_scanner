import asyncio
from uuid import UUID

from app.db import SessionFactory
from app.search.orchestrator import orchestrate_search


async def _run(search_id: UUID) -> None:
    async with SessionFactory() as session:
        await orchestrate_search(session, search_id)


def run_search_job(search_id: str) -> None:
    asyncio.run(_run(UUID(search_id)))
