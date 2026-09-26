"""HTTP surface of the video automation settings.

``admin_router`` is the settings tab on /admin/videos: anyone who reviews videos can read it,
only an admin who manages settings can change it, since it chooses paid models and budgets.
``tool_router`` is how the worker (or the owner's own copy of the tool) reads the same values
with a video tool token, through apps/web/app/api/video/automation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import require_capability
from app.db import get_session
from app.infra import enforce_named_rate_limit, get_redis
from app.models import User
from app.problems import AppError
from app.video_automation import requests as drama_requests
from app.video_automation import settings as service
from app.video_automation.ai import StageFailed, run_stage
from app.video_automation.requests import RequestRefused
from app.video_automation.schemas import (
    DramaRequestIn,
    DramaRequestOut,
    DramaRequestsOut,
    DramaRequestStart,
    NextDramaRequestOut,
    SettingsSave,
    SettingsView,
    SettingsWrite,
    StageModelsWrite,
    StageRunIn,
    StageRunOut,
    TopicsOut,
)
from app.video_automation.topics import gather_topics
from app.video_reviews.admin_service import list_projects
from app.video_reviews.schemas import ProjectSummary
from app.video_speech.admin_api import VideoTool

# A whole video is a few dozen stage calls; this only stops a runaway loop.
RUNS_PER_HOUR = 120
TOPIC_LOOKUPS_PER_HOUR = 12
# The worker asks every few minutes; this only stops a runaway loop.
REQUEST_CALLS_PER_HOUR = 240

admin_router = APIRouter(prefix="/admin/video-automation", tags=["admin video automation"])
tool_router = APIRouter(prefix="/video/automation", tags=["video automation (pipeline)"])
Session = Annotated[AsyncSession, Depends(get_session)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
ContentManager = Annotated[User, Depends(require_capability("content.manage"))]
SettingsManager = Annotated[User, Depends(require_capability("settings.manage"))]


class ToolSettingsView(SettingsWrite):
    updated_at: datetime | None


@admin_router.get("/settings", response_model=SettingsView)
async def get_video_automation_settings(user: ContentReader, session: Session) -> SettingsView:
    _ = user
    return await service.settings_view(session)


async def _save(session: AsyncSession, user: User, payload: SettingsWrite) -> SettingsView:
    problems = service.settings_problems(payload, await load_runtime_settings(session))
    if problems:
        raise AppError(422, "video_automation_settings_invalid", "；".join(problems))
    return await service.update_settings(session, user, payload)


@admin_router.put("/settings", response_model=SettingsView)
async def put_video_automation_settings(
    payload: SettingsSave, user: SettingsManager, session: Session
) -> SettingsView:
    values = payload.model_dump()
    if payload.stage_models is None or payload.drama is None:
        # The stage models are chosen on the AI settings page, and a page from before the drama
        # settings existed sends none: keep the stored ones in both cases.
        current = service.settings_values(await service.settings_row(session)).model_dump()
        if payload.stage_models is None:
            values["stage_models"] = current["stage_models"]
        if payload.drama is None:
            values["drama"] = current["drama"]
    return await _save(session, user, SettingsWrite.model_validate(values))


@admin_router.put("/settings/models", response_model=SettingsView)
async def put_video_automation_models(
    payload: StageModelsWrite, user: SettingsManager, session: Session
) -> SettingsView:
    """Change only the stage models, from the AI settings page."""
    current = service.settings_values(await service.settings_row(session)).model_dump()
    merged = SettingsWrite.model_validate({**current, **payload.model_dump()})
    return await _save(session, user, merged)


@tool_router.get("/settings", response_model=ToolSettingsView)
async def get_tool_video_automation_settings(tool: VideoTool, session: Session) -> ToolSettingsView:
    _ = tool
    row = await service.settings_row(session)
    await session.commit()
    return ToolSettingsView(**service.settings_values(row).model_dump(), updated_at=row.updated_at)


@tool_router.post("/run", response_model=StageRunOut)
async def run_video_stage(request: StageRunIn, tool: VideoTool, session: Session) -> StageRunOut:
    """One writing stage with the model the owner chose for it; the model is not the caller's."""
    await enforce_named_rate_limit(
        "video_ai_run", str(tool.id), limit=RUNS_PER_HOUR, window_seconds=3600
    )
    row = await service.settings_row(session)
    runtime = await load_runtime_settings(session)
    try:
        return await run_stage(session, runtime, row, request, tool.id)
    except StageFailed as error:
        raise AppError(
            error.status,
            error.code,
            error.detail,
            headers={"Retry-After": error.retry_after} if error.retry_after else None,
        ) from error


@tool_router.get("/videos", response_model=list[ProjectSummary])
async def list_tool_videos(tool: VideoTool, session: Session) -> list[ProjectSummary]:
    """Every video on /admin/videos, dropped ones too, so a new draft does not repeat a topic."""
    _ = tool
    return await list_projects(session)


@tool_router.get("/topics", response_model=TopicsOut)
async def get_video_topics(tool: VideoTool, session: Session) -> TopicsOut:
    """Candidate topics for the next draft: the site's recent articles, then a web search."""
    await enforce_named_rate_limit(
        "video_topics", str(tool.id), limit=TOPIC_LOOKUPS_PER_HOUR, window_seconds=3600
    )
    row = await service.settings_row(session)
    runtime = await load_runtime_settings(session)
    return await gather_topics(session, runtime, get_redis(), row)


# The owner's drama requests (docs/videos/DRAMA.md): filed on /admin/videos, claimed by the worker.


def _refused(error: RequestRefused) -> AppError:
    return AppError(error.status, error.code, error.detail)


@admin_router.get("/drama-requests", response_model=DramaRequestsOut)
async def list_drama_requests(user: ContentReader, session: Session) -> DramaRequestsOut:
    """Every request the owner filed, newest first, with the video each one became."""
    _ = user
    return DramaRequestsOut(requests=await drama_requests.list_requests(session))


@admin_router.post("/drama-requests", response_model=DramaRequestOut, status_code=201)
async def create_drama_request(
    payload: DramaRequestIn, user: ContentManager, session: Session
) -> DramaRequestOut:
    """The owner asks for an episode; the worker starts it on its next round, before any
    scheduled draft. Refused while the drama route is switched off, so nothing queues for a
    worker that will never take it."""
    row = await service.settings_row(session)
    if not row.drama_enabled:
        raise AppError(
            409, "video_drama_disabled", "漫劇還沒開啟：先在影片審核的設定分頁打開 AI 漫劇"
        )
    return await drama_requests.create_request(session, user, payload)


@admin_router.delete("/drama-requests/{request_id}", response_model=DramaRequestOut)
async def cancel_drama_request(
    request_id: UUID, user: ContentManager, session: Session
) -> DramaRequestOut:
    """Withdraw a request the worker has not started; a started one is dropped as a video."""
    try:
        return await drama_requests.cancel_request(session, user, request_id)
    except RequestRefused as error:
        raise _refused(error) from error


@tool_router.get("/drama-requests", response_model=DramaRequestsOut)
async def list_active_drama_requests(tool: VideoTool, session: Session) -> DramaRequestsOut:
    """The requests still queued or in the making, oldest first, so a restarted worker can
    tell which of its videos answers which request."""
    await enforce_named_rate_limit(
        "video_drama_requests", str(tool.id), limit=REQUEST_CALLS_PER_HOUR, window_seconds=3600
    )
    return DramaRequestsOut(requests=await drama_requests.list_requests(session, active_only=True))


@tool_router.get("/drama-requests/next", response_model=NextDramaRequestOut)
async def next_drama_request(tool: VideoTool, session: Session) -> NextDramaRequestOut:
    """The oldest queued request, or none: what the worker should start before a scheduled draft."""
    await enforce_named_rate_limit(
        "video_drama_requests", str(tool.id), limit=REQUEST_CALLS_PER_HOUR, window_seconds=3600
    )
    return NextDramaRequestOut(request=await drama_requests.next_request(session))


@tool_router.post("/drama-requests/{request_id}/start", response_model=DramaRequestOut)
async def start_drama_request(
    request_id: UUID, payload: DramaRequestStart, tool: VideoTool, session: Session
) -> DramaRequestOut:
    """The worker claims a queued request for the video it is about to make."""
    await enforce_named_rate_limit(
        "video_drama_requests", str(tool.id), limit=REQUEST_CALLS_PER_HOUR, window_seconds=3600
    )
    try:
        return await drama_requests.start_request(session, tool, request_id, payload.slug)
    except RequestRefused as error:
        raise _refused(error) from error


@tool_router.post("/drama-requests/{request_id}/done", response_model=DramaRequestOut)
async def finish_drama_request(
    request_id: UUID, tool: VideoTool, session: Session
) -> DramaRequestOut:
    """The worker reports the request's video is finished and published."""
    await enforce_named_rate_limit(
        "video_drama_requests", str(tool.id), limit=REQUEST_CALLS_PER_HOUR, window_seconds=3600
    )
    try:
        return await drama_requests.finish_request(session, request_id)
    except RequestRefused as error:
        raise _refused(error) from error
