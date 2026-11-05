"""The broker's routes: video tools start and stop pods, the admin watches and stops them.

Tool routes take a video tool token (mkv_) through the web forwarders under
apps/web/app/api/video/runpod and gpu-routes; no browser session reaches them. Admin routes sit
under /admin/provider-settings/runpod so they share the settings card's permission
(settings.read to look, settings.manage to stop).
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import AdminUser
from app.db import get_session
from app.infra import enforce_named_rate_limit
from app.models import AdminAuditLog, VideoToolToken
from app.problems import AppError
from app.video_runpod import service
from app.video_runpod.client import RunPodClient, RunPodError
from app.video_runpod.models import VideoRunpodSession
from app.video_runpod.schemas import (
    AdminPodStartIn,
    Canvas,
    GpuRoutes,
    PodStarted,
    PodStartIn,
    PodView,
    ReapResult,
    SessionsOverview,
    VolumeCreateIn,
    VolumesOverview,
    VolumeView,
)
from app.video_speech.admin_api import video_tool

Session = Annotated[AsyncSession, Depends(get_session)]
Token = Annotated[VideoToolToken, Depends(video_tool)]

tool_router = APIRouter(prefix="/video/runpod", tags=["video tool"])
routes_router = APIRouter(prefix="/video/gpu-routes", tags=["video tool"])
admin_router = APIRouter(prefix="/admin/provider-settings/runpod", tags=["admin runpod"])

STARTS_PER_HOUR = 30
# The runner beats once a minute; twice that leaves room for retries.
HEARTBEATS_PER_HOUR = 120
RECENT = 20
# RunPod's standard network storage, what the volume form showed on 2026-10-31.
VOLUME_USD_PER_GB_MONTH = Decimal("0.07")


def _require_runpod(token: VideoToolToken) -> None:
    if not token.runpod_access:
        raise AppError(
            403,
            "video_tool_token_no_runpod",
            "這組影片工具權杖沒有 RunPod 權限；重新配對時要求 RunPod，或在後台建立時勾選",
        )


async def _own_row(
    session: AsyncSession, session_id: UUID, token: VideoToolToken
) -> VideoRunpodSession:
    row = await session.get(VideoRunpodSession, session_id)
    if row is None or row.token_id != token.id:
        raise AppError(404, "runpod_session_not_found", "找不到這個 RunPod pod")
    return row


@routes_router.get("", response_model=GpuRoutes)
async def get_gpu_routes(
    session: Session,
    response: Response,
    token: Token,
    canvas: Canvas = "736p",
    upscale: bool = False,
) -> GpuRoutes:
    """Which GPU route this token may use for a batch, and the one the site recommends."""
    response.headers["Cache-Control"] = "no-store"
    settings = await load_runtime_settings(session)
    now = datetime.now(UTC)
    return service.gpu_routes(
        settings,
        token,
        canvas=canvas,
        upscale=upscale,
        month_usd=await service.month_spend(session, now),
        pod_running=bool(await service.running(session)),
    )


@tool_router.post("/pods", response_model=PodStarted, status_code=201)
async def start_pod(
    payload: PodStartIn, session: Session, response: Response, token: Token
) -> PodStarted:
    response.headers["Cache-Control"] = "no-store"
    _require_runpod(token)
    await enforce_named_rate_limit(
        "video_runpod_start", str(token.id), limit=STARTS_PER_HOUR, window_seconds=3_600
    )
    settings = await load_runtime_settings(session)
    row, gate_token = await service.start_pod(
        session, settings, token, label=payload.label, slug=payload.slug
    )
    assert row.pod_id is not None
    return PodStarted(
        session_id=row.id,
        pod_id=row.pod_id,
        base_url=service.base_url(row),
        gate_token=gate_token,
        cost_per_hr=row.cost_per_hr,
        idle_stop_minutes=settings.runpod_idle_stop_minutes,
        max_pod_hours=settings.runpod_max_pod_hours,
        default_profile=settings.runpod_default_profile,
    )


@tool_router.get("/pods", response_model=list[PodView])
async def list_own_pods(session: Session, token: Token) -> list[PodView]:
    """This token's pods still running: what a runner checks when a start's answer was lost."""
    _require_runpod(token)
    now = datetime.now(UTC)
    return [
        service.view(row, now, token.token_prefix)
        for row in await service.running(session)
        if row.token_id == token.id
    ]


@tool_router.get("/pods/{session_id}", response_model=PodView)
async def get_pod(session_id: UUID, session: Session, token: Token) -> PodView:
    _require_runpod(token)
    row = await _own_row(session, session_id, token)
    return service.view(row, datetime.now(UTC), token.token_prefix)


@tool_router.post("/pods/{session_id}/heartbeat", response_model=PodView)
async def heartbeat(session_id: UUID, session: Session, token: Token) -> PodView:
    _require_runpod(token)
    await enforce_named_rate_limit(
        "video_runpod_heartbeat", str(token.id), limit=HEARTBEATS_PER_HOUR, window_seconds=3_600
    )
    row = await service.heartbeat(session, await _own_row(session, session_id, token))
    if row.stopped_at is not None:
        # The runner learns here that the reaper or the owner stopped its pod.
        raise AppError(409, "runpod_pod_stopped", f"這個 pod 已經停了（{row.stop_reason}）")
    return service.view(row, datetime.now(UTC), token.token_prefix)


@tool_router.post("/pods/{session_id}/stop", response_model=PodView)
async def stop_pod(session_id: UUID, session: Session, token: Token) -> PodView:
    _require_runpod(token)
    row = await _own_row(session, session_id, token)
    settings = await load_runtime_settings(session)
    row = await service.stop_pod(
        session, settings, row, reason="manual", actor_id=token.created_by_user_id
    )
    return service.view(row, datetime.now(UTC), token.token_prefix)


@tool_router.post("/reap", response_model=ReapResult)
async def reap(session: Session, token: Token) -> ReapResult:
    """The worker's five-minute `auto` calls this with its own token; it only ever stops pods."""
    await enforce_named_rate_limit(
        "video_runpod_reap", str(token.id), limit=60, window_seconds=3_600
    )
    settings = await load_runtime_settings(session)
    stopped = await service.reap(session, settings)
    now = datetime.now(UTC)
    return ReapResult(stopped=[service.view(row, now) for row in stopped])


async def _prefixes(session: AsyncSession, rows: list[VideoRunpodSession]) -> dict[UUID, str]:
    ids = {row.token_id for row in rows if row.token_id is not None}
    if not ids:
        return {}
    tokens = await session.scalars(select(VideoToolToken).where(VideoToolToken.id.in_(ids)))
    return {item.id: item.token_prefix for item in tokens}


@admin_router.get("/sessions", response_model=SessionsOverview)
async def list_sessions(user: AdminUser, session: Session) -> SessionsOverview:
    _ = user
    now = datetime.now(UTC)
    settings = await load_runtime_settings(session)
    running = await service.running(session)
    recent = list(
        await session.scalars(
            select(VideoRunpodSession)
            .where(VideoRunpodSession.stopped_at.is_not(None))
            .order_by(VideoRunpodSession.started_at.desc())
            .limit(RECENT)
        )
    )
    prefixes = await _prefixes(session, running + recent)

    def show(row: VideoRunpodSession) -> PodView:
        return service.view(row, now, prefixes.get(row.token_id) if row.token_id else None)

    return SessionsOverview(
        running=[show(row) for row in running],
        recent=[show(row) for row in recent],
        month_usd=await service.month_spend(session, now),
        monthly_usd_cap=settings.runpod_monthly_usd_cap,
        configured=not service.missing_settings(settings),
    )


@admin_router.post("/sessions/{session_id}/stop", response_model=PodView)
async def admin_stop(session_id: UUID, user: AdminUser, session: Session) -> PodView:
    row = await session.get(VideoRunpodSession, session_id)
    if row is None:
        raise AppError(404, "runpod_session_not_found", "找不到這個 RunPod pod")
    settings = await load_runtime_settings(session)
    row = await service.stop_pod(session, settings, row, reason="manual", actor_id=user.id)
    return service.view(row, datetime.now(UTC))


def _volume_problem(error: RunPodError) -> AppError:
    if error.status == 409:
        return AppError(409, "runpod_no_stock", error.detail)
    if error.status == 503:
        return AppError(503, "runpod_not_configured", error.detail)
    return AppError(502, "runpod_volume_failed", error.detail)


@admin_router.get("/volumes", response_model=VolumesOverview)
async def list_volumes(user: AdminUser, session: Session) -> VolumesOverview:
    _ = user
    settings = await load_runtime_settings(session)
    views: list[VolumeView] = []
    try:
        async with RunPodClient(settings) as client:
            for item in await client.list_volumes():
                place = item.get("dataCenterId")
                views.append(
                    VolumeView(
                        id=str(item["id"]),
                        name=item.get("name"),
                        size_gb=service.volume_gb(item),
                        data_center_id=place,
                        stock=await service.stock_or_unknown(client, place) if place else None,
                        usable=service.volume_gb(item) >= service.MIN_VOLUME_GB,
                    )
                )
    except RunPodError as error:
        raise _volume_problem(error) from error
    return VolumesOverview(
        gpu=settings.runpod_gpu_type_id,
        volumes=views,
        new_volume_gb=service.VOLUME_SIZE_GB,
        new_volume_usd_per_month=VOLUME_USD_PER_GB_MONTH * service.VOLUME_SIZE_GB,
    )


@admin_router.post("/volumes", response_model=VolumeView, status_code=201)
async def create_volume(payload: VolumeCreateIn, user: AdminUser, session: Session) -> VolumeView:
    settings = await load_runtime_settings(session)
    try:
        async with RunPodClient(settings) as client:
            created = await service.create_model_volume(client, settings, payload.data_center_id)
            stock = await service.stock_or_unknown(client, created["dataCenterId"])
    except RunPodError as error:
        raise _volume_problem(error) from error
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="runpod.volume_created",
            target=f"runpod-volume:{created['id']}",
            metadata_json={"data_center": created["dataCenterId"], "size_gb": created["size"]},
        )
    )
    await session.commit()
    return VolumeView(
        id=created["id"],
        name=created.get("name"),
        size_gb=created["size"],
        data_center_id=created["dataCenterId"],
        stock=stock,
        usable=True,
    )


@admin_router.delete("/volumes/{volume_id}", status_code=204)
async def delete_volume(volume_id: str, user: AdminUser, session: Session) -> Response:
    if await service.running(session):
        raise AppError(409, "runpod_pod_running", "還有 pod 在跑；先停掉再刪空間")
    settings = await load_runtime_settings(session)
    try:
        async with RunPodClient(settings) as client:
            await client.delete_volume(volume_id)
    except RunPodError as error:
        raise _volume_problem(error) from error
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="runpod.volume_deleted",
            target=f"runpod-volume:{volume_id}",
            metadata_json={},
        )
    )
    await session.commit()
    return Response(status_code=204)


@admin_router.post("/sessions", response_model=PodStarted, status_code=201)
async def admin_start(
    payload: AdminPodStartIn, user: AdminUser, session: Session, response: Response
) -> PodStarted:
    response.headers["Cache-Control"] = "no-store"
    settings = await load_runtime_settings(session)
    row, gate_token = await service.start_pod(
        session, settings, None, label=payload.label, slug=None, actor_id=user.id
    )
    assert row.pod_id is not None
    return PodStarted(
        session_id=row.id,
        pod_id=row.pod_id,
        base_url=service.base_url(row),
        gate_token=gate_token,
        cost_per_hr=row.cost_per_hr,
        idle_stop_minutes=settings.runpod_idle_stop_minutes,
        max_pod_hours=settings.runpod_max_pod_hours,
        default_profile=settings.runpod_default_profile,
    )


@admin_router.post("/sessions/{session_id}/heartbeat", response_model=PodView)
async def admin_heartbeat(session_id: UUID, user: AdminUser, session: Session) -> PodView:
    """The open panel keeps a pod it started alive; a tool's pod is kept alive by its runner."""
    _ = user
    row = await session.get(VideoRunpodSession, session_id)
    if row is None or row.token_id is not None:
        raise AppError(404, "runpod_session_not_found", "找不到這個 RunPod pod")
    row = await service.heartbeat(session, row)
    return service.view(row, datetime.now(UTC))
