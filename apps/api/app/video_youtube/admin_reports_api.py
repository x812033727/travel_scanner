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
from app.video_youtube import reports, retention
from app.video_youtube.errors import Refused
from app.video_youtube.schemas import ReportsSyncIn, ReportsSyncOut

# A tool's `sync` loops while files remain; the worker knocks a few times a day.
SYNCS_PER_HOUR = 30
# Each retention curve is one videos.list unit and one YouTube Analytics API query.
RETENTION_PER_HOUR = 60

Session = Annotated[AsyncSession, Depends(get_session)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
ContentManager = Annotated[User, Depends(require_capability("content.manage"))]

tool_router = APIRouter(prefix="/video/youtube-reports", tags=["video tool"])
admin_router = APIRouter(prefix="/admin/video-youtube/reports", tags=["admin video youtube"])


# Which linked channel (VideoYoutubeConnection.key, migration 0147); the default one if left out.
ChannelKey = Annotated[str, Query(alias="channel", pattern=r"^[a-z][a-z0-9-]{1,31}$")]


def _refused(error: Refused) -> AppError:
    return AppError(error.status, error.code, error.detail)


def _sync_out(result: reports.SyncResult) -> ReportsSyncOut:
    return ReportsSyncOut(**asdict(result))


@tool_router.get("")
async def tool_overview(
    tool: VideoTool, session: Session, channel: ChannelKey = "default"
) -> dict[str, Any]:
    """Which reports the site keeps for a channel and for which days, the site's videos on
    it, and every linked channel under ``channels``."""
    _ = tool
    try:
        return await reports.overview(session, key=channel)
    except Refused as error:
        raise _refused(error) from error


@tool_router.post("/sync", response_model=ReportsSyncOut)
async def tool_sync(
    payload: ReportsSyncIn, tool: VideoTool, session: Session, channel: ChannelKey = "default"
) -> ReportsSyncOut:
    await enforce_named_rate_limit(
        "video_youtube_reports_sync", str(tool.id), limit=SYNCS_PER_HOUR, window_seconds=3600
    )
    try:
        result = await reports.sync(
            session, force=payload.force, limit=payload.limit, key=channel
        )
    except Refused as error:
        raise _refused(error) from error
    return _sync_out(result)


@tool_router.get("/rows")
async def tool_rows(
    tool: VideoTool,
    session: Session,
    report: Annotated[str, Query(min_length=3, max_length=100, pattern=r"^[a-z0-9_]+$")],
    start: date,
    end: date,
    video_id: Annotated[list[str] | None, Query(max_length=50)] = None,
    output: Annotated[Literal["json", "csv"], Query(alias="format")] = "json",
    channel: ChannelKey = "default",
) -> Response:
    """One report family's rows for the days ``start`` to ``end`` (Pacific, inclusive), as
    YouTube wrote them; ``video_id`` (repeatable) keeps the rows of those videos only."""
    _ = tool
    try:
        found = await reports.rows(
            session,
            report=report,
            start=start,
            end=end,
            video_ids=video_id or (),
            output=output,
            key=channel,
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


@tool_router.get("/retention")
async def tool_retention(
    tool: VideoTool,
    session: Session,
    video_id: Annotated[str, Query(min_length=6, max_length=20, pattern=r"^[A-Za-z0-9_-]+$")],
    start: date | None = None,
    end: date | None = None,
    organic: bool = False,
) -> JSONResponse:
    """One video's audience retention curve from the YouTube Analytics API (100 points of
    ``elapsedVideoTimeRatio`` with ``audienceWatchRatio`` and ``relativeRetentionPerformance``),
    asked of YouTube now with the stored grant; ``organic`` keeps organic traffic only."""
    await enforce_named_rate_limit(
        "video_youtube_retention", str(tool.id), limit=RETENTION_PER_HOUR, window_seconds=3600
    )
    try:
        found = await retention.retention(
            session, video_id=video_id, start=start, end=end, organic=organic
        )
    except Refused as error:
        raise _refused(error) from error
    return JSONResponse(found.as_json(), headers={"Cache-Control": "no-store"})


@admin_router.get("")
async def admin_overview(
    user: ContentReader, session: Session, channel: ChannelKey = "default"
) -> dict[str, Any]:
    """The card's line: the overview without the list of videos."""
    _ = user
    try:
        view = await reports.overview(session, key=channel)
    except Refused as error:
        raise _refused(error) from error
    view.pop("videos", None)
    return view


@admin_router.post("/sync", response_model=ReportsSyncOut)
async def admin_sync(
    user: ContentManager, session: Session, channel: ChannelKey = "default"
) -> ReportsSyncOut:
    _ = user
    try:
        return _sync_out(await reports.sync(session, force=True, key=channel))
    except Refused as error:
        raise _refused(error) from error
