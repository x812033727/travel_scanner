"""HTTP surface of the channel reports (docs/videos/YOUTUBE-REPORTS.md).

``tool_router`` is what a paired video tool calls with its video tool token (mkv_), through the
web forwarders under apps/web/app/api/video/youtube-reports: every active token may read the
reports, since they only describe the owner's own channel and say nothing a token could spend or
change. ``admin_router`` is the line on the YouTube card of /admin/videos: anyone who reviews
videos may look, and fetching now needs ``content.manage``.

The file name carries ``admin`` on purpose: its errors are the operator's, in Traditional
Chinese, like the other video tool routes.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import date
from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import require_capability
from app.db import get_session
from app.infra import enforce_named_rate_limit
from app.models import User
from app.problems import AppError
from app.video_speech.admin_api import VideoTool
from app.video_youtube import reports
from app.video_youtube.errors import Refused
from app.video_youtube.schemas import ReportsSyncIn, ReportsSyncOut

# A tool's `sync` loops while files remain; the worker knocks a few times a day.
SYNCS_PER_HOUR = 30

Session = Annotated[AsyncSession, Depends(get_session)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
ContentManager = Annotated[User, Depends(require_capability("content.manage"))]

tool_router = APIRouter(prefix="/video/youtube-reports", tags=["video tool"])
admin_router = APIRouter(prefix="/admin/video-youtube/reports", tags=["admin video youtube"])


def _refused(error: Refused) -> AppError:
    return AppError(error.status, error.code, error.detail)


def _sync_out(result: reports.SyncResult) -> ReportsSyncOut:
    return ReportsSyncOut(**asdict(result))


@tool_router.get("")
async def tool_overview(tool: VideoTool, session: Session) -> dict[str, Any]:
    """Which reports the site keeps and for which days, and the site's videos on YouTube."""
    _ = tool
    return await reports.overview(session)


@tool_router.post("/sync", response_model=ReportsSyncOut)
async def tool_sync(payload: ReportsSyncIn, tool: VideoTool, session: Session) -> ReportsSyncOut:
    await enforce_named_rate_limit(
        "video_youtube_reports_sync", str(tool.id), limit=SYNCS_PER_HOUR, window_seconds=3600
    )
    return _sync_out(await reports.sync(session, force=payload.force, limit=payload.limit))


@tool_router.get("/rows")
async def tool_rows(
    tool: VideoTool,
    session: Session,
    report: Annotated[str, Query(min_length=3, max_length=100, pattern=r"^[a-z0-9_]+$")],
    start: date,
    end: date,
    video_id: Annotated[list[str] | None, Query(max_length=50)] = None,
    output: Annotated[Literal["json", "csv"], Query(alias="format")] = "json",
) -> Response:
    """One report family's rows for the days ``start`` to ``end`` (Pacific, inclusive), as
    YouTube wrote them; ``video_id`` (repeatable) keeps the rows of those videos only."""
    _ = tool
    try:
        found = await reports.rows(
            session, report=report, start=start, end=end, video_ids=video_id or (), output=output
        )
    except Refused as error:
        raise _refused(error) from error
    headers = {
        "Cache-Control": "no-store",
        "X-Report-Type": found.report_type_id,
        "X-Report-Days": str(len(found.days)),
        "X-Rows-Truncated": "true" if found.truncated else "false",
    }
    if output == "csv":
        return Response(
            reports.as_csv(found), media_type="text/csv; charset=utf-8", headers=headers
        )
    return JSONResponse(
        {
            "report_type_id": found.report_type_id,
            "columns": found.columns,
            "rows": found.rows,
            "days": found.days,
            "truncated": found.truncated,
            "policy": reports.POLICY_NOTE,
        },
        headers=headers,
    )


@admin_router.get("")
async def admin_overview(user: ContentReader, session: Session) -> dict[str, Any]:
    """The card's line: the overview without the list of videos."""
    _ = user
    view = await reports.overview(session)
    view.pop("videos", None)
    return view


@admin_router.post("/sync", response_model=ReportsSyncOut)
async def admin_sync(user: ContentManager, session: Session) -> ReportsSyncOut:
    _ = user
    return _sync_out(await reports.sync(session, force=True))
