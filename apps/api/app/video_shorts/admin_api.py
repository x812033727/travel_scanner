"""HTTP surface of the Shorts tab on /admin/videos (docs/videos/SHORTS.md §端點).

``admin_router`` is the tab: anyone who reviews videos reads it and changes the calendar and
the ledger; only an admin who manages settings saves the settings, starts the run, or gives
and takes back the consent to publish. Every route names its capability: the path-based
check knows no video path, and a route without one would fall to ``roles.manage``.

``tool_router`` is what the Shorts tool and the worker read with a video tool token, through
apps/web/app/api/video/automation/shorts. The routes that send to YouTube are in
``admin_publish_api``; the worker's jobs are in ``admin_automation_api``.
"""

from __future__ import annotations

from datetime import date
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from pydantic import AwareDatetime, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import require_capability
from app.config import Settings
from app.db import get_session
from app.models import User
from app.problems import AppError
from app.video_automation.settings import configured_providers, model_options
from app.video_shorts import costs, overview, slots
from app.video_shorts import settings as service
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.schemas import (
    AutopublishIn,
    CampaignOut,
    CampaignStartIn,
    CostIn,
    CostOut,
    CostPatch,
    CostsOut,
    MetricsOut,
    OverviewOut,
    SettingsSave,
    SettingsView,
    SettingsWrite,
    SlotOut,
    SlotPatch,
    SlotsOut,
    ToolSettingsView,
)
from app.video_speech.admin_api import VideoTool
from app.video_speech.gemini import GEMINI_TTS_MODELS, PREBUILT_VOICES

admin_router = APIRouter(prefix="/admin/video-shorts", tags=["admin video shorts"])
tool_router = APIRouter(prefix="/video/automation/shorts", tags=["video shorts (pipeline)"])
Session = Annotated[AsyncSession, Depends(get_session)]
ContentReader = Annotated[User, Depends(require_capability("content.read"))]
ContentManager = Annotated[User, Depends(require_capability("content.manage"))]
SettingsManager = Annotated[User, Depends(require_capability("settings.manage"))]


def refused(error: ShortsRefused) -> AppError:
    return AppError(error.status, error.code, error.detail)


def _validated(values: dict[str, Any]) -> SettingsWrite:
    """The merged settings as a whole, or 422 naming what does not hold together."""
    try:
        return SettingsWrite.model_validate(values)
    except ValidationError as error:
        problems = "；".join(
            f"{'.'.join(str(part) for part in problem['loc'])}: {problem['msg']}"
            if problem["loc"]
            else str(problem["msg"])
            for problem in error.errors()
        )
        raise AppError(422, "video_shorts_settings_invalid", problems) from error


async def _settings_problem(session: AsyncSession, payload: SettingsWrite) -> str | None:
    """What the server cannot run as saved, in the owner's words: the voice, then the stage
    models."""
    runtime = await load_runtime_settings(session)
    return _voice_problem(payload, runtime) or _stage_models_problem(payload, runtime)


def _stage_models_problem(payload: SettingsWrite, runtime: Settings) -> str | None:
    """A Shorts stage model no vendor serves, or, with automatic making on, one whose vendor
    the site holds no key for (as the drama's are checked, app/video_automation/settings.py)."""
    if payload.stage_models is None:
        return None
    options = model_options()
    configured = set(configured_providers(runtime))
    problems: list[str] = []
    for stage, choice in payload.stage_models.items():
        if choice.model not in {option.value for option in options[choice.provider]}:
            problems.append(
                f"Shorts 的 {stage}：{choice.provider} 沒有 {choice.model} 這個可用的模型"
            )
        elif payload.enabled and choice.provider not in configured:
            problems.append(
                f"Shorts 的 {stage}：網站還沒有 {choice.provider} 的金鑰，"
                "不能開啟 Shorts 的自動製作"
            )
    return "；".join(problems) or None


def _voice_problem(payload: SettingsWrite, runtime: Settings) -> str | None:
    """A voice the server cannot speak in, in the owner's words."""
    voice = payload.voice
    if voice.provider == "gemini":
        if voice.name not in PREBUILT_VOICES:
            return f"Gemini 沒有 {voice.name} 這個聲音"
        if voice.model is not None and voice.model not in GEMINI_TTS_MODELS:
            return f"Gemini 沒有 {voice.model} 這個語音模型"
        if payload.enabled and "gemini" not in configured_providers(runtime):
            return "網站還沒有 Gemini 的金鑰，不能開啟 Shorts 的自動製作"
        return None
    if voice.name not in runtime.azure_speech_voice_list:
        return f"{voice.name} 不在 Azure 語音的允許清單裡"
    return None


@admin_router.get("/overview", response_model=OverviewOut)
async def shorts_overview(user: ContentReader, session: Session) -> OverviewOut:
    _ = user
    return await overview.overview(session)


@admin_router.get("/slots", response_model=SlotsOut)
async def list_shorts_slots(
    user: ContentReader,
    session: Session,
    first: Annotated[date | None, Query(alias="from")] = None,
    last: Annotated[date | None, Query(alias="to")] = None,
) -> SlotsOut:
    """The calendar between two local days, both included; the whole run without them."""
    _ = user
    return await slots.list_slots(session, first, last)


@admin_router.patch("/slots/{slot_id}", response_model=SlotOut)
async def change_shorts_slot(
    slot_id: UUID, payload: SlotPatch, user: ContentManager, session: Session
) -> SlotOut:
    """Move a slot, give it a Short, take the Short out, or mark the slot as not publishing."""
    try:
        return await slots.patch_slot(session, user, slot_id, payload)
    except ShortsRefused as error:
        raise refused(error) from error


@admin_router.get("/costs", response_model=CostsOut)
async def list_shorts_costs(
    user: ContentReader,
    session: Session,
    limit: Annotated[int, Query(ge=1, le=costs.LIST_LIMIT)] = costs.LIST_LIMIT,
    before: AwareDatetime | None = None,
) -> CostsOut:
    _ = user
    row = await service.settings_row(session)
    await session.commit()
    return await costs.costs_view(session, row, limit=limit, before=before)


@admin_router.post("/costs", response_model=CostOut, status_code=201)
async def add_shorts_cost(payload: CostIn, user: ContentManager, session: Session) -> CostOut:
    """A line the owner enters: a subscription, a tool fee, an amount the site cannot see."""
    try:
        return await costs.add_manual(session, user, payload)
    except ShortsRefused as error:
        raise refused(error) from error


@admin_router.patch("/costs/{cost_id}", response_model=CostOut)
async def change_shorts_cost(
    cost_id: UUID, payload: CostPatch, user: ContentManager, session: Session
) -> CostOut:
    """Correct a line, or give an unknown one its amount so paid work can go on."""
    try:
        return await costs.update_cost(session, user, cost_id, payload)
    except ShortsRefused as error:
        raise refused(error) from error


@admin_router.delete("/costs/{cost_id}", status_code=204)
async def remove_shorts_cost(cost_id: UUID, user: ContentManager, session: Session) -> Response:
    try:
        await costs.delete_cost(session, user, cost_id)
    except ShortsRefused as error:
        raise refused(error) from error
    return Response(status_code=204)


@admin_router.get("/metrics", response_model=MetricsOut)
async def list_shorts_metrics(
    user: ContentReader,
    session: Session,
    limit: Annotated[int, Query(ge=1, le=200)] = overview.METRICS_LIMIT,
    before: AwareDatetime | None = None,
) -> MetricsOut:
    """The public Shorts with the numbers YouTube reported, as they were stored."""
    _ = user
    return await overview.metrics_view(session, limit=limit, before=before)


@admin_router.get("/settings", response_model=SettingsView)
async def get_shorts_settings(user: ContentReader, session: Session) -> SettingsView:
    _ = user
    row = await service.settings_row(session)
    await session.commit()
    return service.settings_view(row, await service.channel_facts(session))


@admin_router.put("/settings", response_model=SettingsView)
async def put_shorts_settings(
    payload: SettingsSave, user: SettingsManager, session: Session
) -> SettingsView:
    """Save the fields the tab sent; the rest keep their stored values."""
    current = service.settings_values(await service.settings_row(session)).model_dump()
    merged = _validated(payload.merged_over(current))
    problem = await _settings_problem(session, merged)
    if problem:
        raise AppError(422, "video_shorts_settings_invalid", problem)
    return await service.update_settings(session, user, merged)


@admin_router.post("/campaign/start", response_model=CampaignOut)
async def start_shorts_campaign(
    payload: CampaignStartIn, user: SettingsManager, session: Session
) -> CampaignOut:
    """Build the run's calendar from the day its first Short goes public."""
    try:
        return await slots.start_campaign(session, user, payload.first_day)
    except ShortsRefused as error:
        raise refused(error) from error


@admin_router.post("/autopublish", response_model=SettingsView)
async def grant_shorts_autopublish(
    payload: AutopublishIn, user: SettingsManager, session: Session
) -> SettingsView:
    """The owner agrees to the wording they were shown: the site may publish on the
    calendar without asking each time, inside the scope the wording names."""
    try:
        return await service.grant_autopublish(session, user, payload.text_sha256)
    except ShortsRefused as error:
        raise refused(error) from error


@admin_router.delete("/autopublish", response_model=SettingsView)
async def revoke_shorts_autopublish(user: SettingsManager, session: Session) -> SettingsView:
    return await service.revoke_autopublish(session, user)


@admin_router.post("/pause", response_model=SettingsView)
async def pause_shorts(user: ContentManager, session: Session) -> SettingsView:
    """Hold publishing at once; making, checking and slotting go on."""
    return await service.set_paused(session, user, True)


@admin_router.post("/resume", response_model=SettingsView)
async def resume_shorts(user: ContentManager, session: Session) -> SettingsView:
    return await service.set_paused(session, user, False)


@tool_router.get("/settings", response_model=ToolSettingsView)
async def get_tool_shorts_settings(tool: VideoTool, session: Session) -> ToolSettingsView:
    """The voice, the length and the languages a Short is made with."""
    _ = tool
    row = await service.settings_row(session)
    await session.commit()
    return service.tool_settings_view(row)
