"""HTTP surface of the video backup (docs/videos/BACKUP.md).

``admin_router`` is the "備份位置" card and the backup status on /admin/videos: anyone who
reviews videos may read them; saving the settings and asking for a test need
``settings.manage``, since they decide what leaves the host. ``tool_router`` is how the worker
reads the settings and reports each video's backup with its video tool token, through
apps/web/app/api/video/automation/backup.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import require_capability
from app.db import get_session
from app.models import User
from app.video_backup import admin_settings as settings
from app.video_backup import admin_status as status
from app.video_backup.schemas import (
    BackupView,
    LockIn,
    ProbeAnswerIn,
    ProbeView,
    ReportIn,
    SettingsIn,
    SettingsView,
    StatusView,
    WorkerConfig,
)
from app.video_speech.admin_api import VideoTool

Session = Annotated[AsyncSession, Depends(get_session)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
SettingsManager = Annotated[User, Depends(require_capability("settings.manage"))]
# A video's slug, as the video projects store it.
Slug = Annotated[str, Path(pattern=r"^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$")]

admin_router = APIRouter(prefix="/admin/video-backup", tags=["admin video backup"])
tool_router = APIRouter(prefix="/video/automation/backup", tags=["video backup (worker)"])


@admin_router.get("/settings", response_model=SettingsView)
async def read_settings(user: ContentReader, session: Session) -> SettingsView:
    _ = user
    return await settings.view(session)


@admin_router.put("/settings", response_model=SettingsView)
async def save_settings(
    payload: SettingsIn, user: SettingsManager, session: Session
) -> SettingsView:
    return await settings.save(session, user, payload)


@admin_router.post("/test", response_model=SettingsView)
async def request_test(user: SettingsManager, session: Session) -> SettingsView:
    return await settings.request_test(session, user)


@admin_router.get("/test", response_model=ProbeView)
async def read_test(user: ContentReader, session: Session) -> ProbeView:
    _ = user
    return (await settings.view(session)).test


@admin_router.get("/status", response_model=StatusView)
async def read_status(
    user: ContentReader, session: Session, all: Annotated[bool, Query()] = False
) -> StatusView:
    """Whether every uploaded video is in Drive; only those that are not, unless ``all``."""
    _ = user
    return await status.status(session, everything=all)


@admin_router.get("/status/{slug}", response_model=BackupView)
async def read_video_status(slug: Slug, user: ContentReader, session: Session) -> BackupView:
    _ = user
    return await status.video_status(session, slug)


@tool_router.get("/config", response_model=WorkerConfig)
async def worker_config(tool: VideoTool, session: Session) -> WorkerConfig:
    _ = tool
    return await status.worker_config(session)


@tool_router.post("/lock", response_model=SettingsView)
async def report_lock(payload: LockIn, tool: VideoTool, session: Session) -> SettingsView:
    _ = tool
    return await settings.record_lock(session, payload)


@tool_router.post("/test/{test_id}", response_model=SettingsView)
async def answer_test(
    test_id: UUID, payload: ProbeAnswerIn, tool: VideoTool, session: Session
) -> SettingsView:
    _ = tool
    return await settings.answer_test(session, test_id, payload)


@tool_router.post("/{slug}/report", response_model=BackupView)
async def report(slug: Slug, payload: ReportIn, tool: VideoTool, session: Session) -> BackupView:
    return await status.report(session, tool, slug, payload)
