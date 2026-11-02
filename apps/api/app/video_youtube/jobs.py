"""The daily fetch of the channel reports, run by the RQ worker (docs/videos/YOUTUBE-REPORTS.md).

``app.analytics.scheduler`` enqueues ``sync_reports`` on the "analytics" queue twice a day; the
sync itself does nothing within twelve hours of the last complete run, and nothing at all while
no channel is linked with YouTube Analytics. A run that stops at its download limit goes on in
the same job until nothing is left, so the 30 days YouTube backfills for a new job arrive in one
go and no report ages past YouTube's 60 days unread.
"""

from __future__ import annotations

import asyncio
from typing import Any

from app.db import SessionFactory
from app.video_youtube import reports

MAX_ROUNDS = 10


async def _run() -> dict[str, Any]:
    downloaded = replaced = 0
    status = "not_due"
    problem: str | None = None
    for round_number in range(MAX_ROUNDS):
        async with SessionFactory() as session:
            result = await reports.sync(session, force=round_number > 0, limit=reports.MAX_LIMIT)
        downloaded += result.downloaded
        replaced += result.replaced
        status, problem = result.status, result.problem
        if not (result.status == "partial" and result.remaining):
            break
    return {"status": status, "downloaded": downloaded, "replaced": replaced, "problem": problem}


def sync_reports() -> dict[str, Any]:
    return asyncio.run(_run())
