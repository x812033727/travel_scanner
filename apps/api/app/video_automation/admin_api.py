"""HTTP surface of the video automation settings.

``admin_router`` is the settings tab on /admin/videos: anyone who reviews videos can read it,
only an admin who manages settings can change it, since it chooses paid models and budgets.
``tool_router`` is how the worker (or the owner's own copy of the tool) reads the same values
with a video tool token, through apps/web/app/api/video/automation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import require_capability
from app.db import get_session
from app.models import User
from app.problems import AppError
from app.video_automation import settings as service
from app.video_automation.schemas import SettingsView, SettingsWrite
from app.video_speech.admin_api import VideoTool

admin_router = APIRouter(prefix="/admin/video-automation", tags=["admin video automation"])
tool_router = APIRouter(prefix="/video/automation", tags=["video automation (pipeline)"])
Session = Annotated[AsyncSession, Depends(get_session)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
SettingsManager = Annotated[User, Depends(require_capability("settings.manage"))]


class ToolSettingsView(SettingsWrite):
    updated_at: datetime | None


@admin_router.get("/settings", response_model=SettingsView)
async def get_video_automation_settings(user: ContentReader, session: Session) -> SettingsView:
    _ = user
    return await service.settings_view(session)


@admin_router.put("/settings", response_model=SettingsView)
async def put_video_automation_settings(
    payload: SettingsWrite, user: SettingsManager, session: Session
) -> SettingsView:
    problems = service.settings_problems(payload, await load_runtime_settings(session))
    if problems:
        raise AppError(422, "video_automation_settings_invalid", "；".join(problems))
    return await service.update_settings(session, user, payload)


@tool_router.get("/settings", response_model=ToolSettingsView)
async def get_tool_video_automation_settings(tool: VideoTool, session: Session) -> ToolSettingsView:
    _ = tool
    row = await service.settings_row(session)
    await session.commit()
    return ToolSettingsView(**service.settings_values(row).model_dump(), updated_at=row.updated_at)
