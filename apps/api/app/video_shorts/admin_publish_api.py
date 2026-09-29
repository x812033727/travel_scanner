"""The routes that send Shorts to YouTube (docs/videos/SHORTS.md §上架): the worker's knock,
and on the tab the files that wait for the owner's upload, the claim that finds them on the
channel, and the recall of what is scheduled. Registered in ``app.main`` with the rest.

The file name carries ``admin`` on purpose: its errors are the operator's, in Traditional
Chinese, and ``tests/test_error_localization.py`` asks for four more languages of any
``AppError`` raised outside an admin file.
"""

from __future__ import annotations

import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTask

from app.admin.service import load_runtime_settings
from app.auth.service import require_capability
from app.db import get_session
from app.infra import enforce_named_rate_limit, get_redis
from app.models import User
from app.problems import AppError
from app.video_reviews.admin_service import review_store
from app.video_shorts import claim as claims
from app.video_shorts import publish
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.quota import Quota
from app.video_shorts.schemas import ClaimOut, RecallOut, TickOut, UploadsOut
from app.video_shorts.settings import settings_row
from app.video_shorts.tick import tick
from app.video_speech.admin_api import VideoTool
from app.video_youtube import connection

# The worker knocks every five minutes; this only stops a runaway loop.
TICKS_PER_HOUR = 60

admin_router = APIRouter(prefix="/admin/video-shorts", tags=["admin video shorts"])
tool_router = APIRouter(prefix="/video/automation/shorts", tags=["video shorts (pipeline)"])
Session = Annotated[AsyncSession, Depends(get_session)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
ContentManager = Annotated[User, Depends(require_capability("content.manage"))]


def refused(error: ShortsRefused) -> AppError:
    return AppError(error.status, error.code, error.detail)


@tool_router.post("/tick", response_model=TickOut)
async def shorts_tick(tool: VideoTool, session: Session) -> TickOut:
    """Do what is due on the Shorts calendar; the answer is how much of each was done."""
    await enforce_named_rate_limit(
        "video_shorts_tick", str(tool.id), limit=TICKS_PER_HOUR, window_seconds=3600
    )
    return await tick(session, get_redis())


@admin_router.get("/uploads", response_model=UploadsOut)
async def list_shorts_uploads(user: ContentReader, session: Session) -> UploadsOut:
    """The Shorts of the coming days whose files the owner uploads to YouTube Studio."""
    _ = user
    return await claims.uploads_view(session)


@admin_router.get("/uploads/batch.zip")
async def download_shorts_uploads(user: ContentManager, session: Session) -> FileResponse:
    """Those files in one archive, each under the name the claim looks for."""
    _ = user
    row = await settings_row(session)
    await session.commit()
    store = review_store(await load_runtime_settings(session))
    waiting = await claims.waiting_uploads(session, row)
    try:
        # Tens of megabytes are copied: off the event loop.
        path = await asyncio.to_thread(claims.batch_zip, store, waiting)
    except ShortsRefused as error:
        raise refused(error) from error
    return FileResponse(
        path,
        media_type="application/zip",
        filename="mokaair-shorts.zip",
        headers={"Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff"},
        background=BackgroundTask(path.unlink, missing_ok=True),
    )


@admin_router.post("/uploads/claim", response_model=ClaimOut)
async def claim_shorts_uploads(user: ContentManager, session: Session) -> ClaimOut:
    """ "I uploaded them": find the files on the channel and give the Shorts their videos."""
    try:
        async with connection.http_client() as http:
            return await claims.claim(session, http, user, Quota(get_redis()))
    except ShortsRefused as error:
        raise refused(error) from error


@admin_router.post("/recall", response_model=RecallOut)
async def recall_shorts(user: ContentManager, session: Session) -> RecallOut:
    """Take what is scheduled and not public yet off YouTube's schedule, and pause."""
    try:
        async with connection.http_client() as http:
            return await publish.recall(session, http, user, Quota(get_redis()))
    except ShortsRefused as error:
        raise refused(error) from error
