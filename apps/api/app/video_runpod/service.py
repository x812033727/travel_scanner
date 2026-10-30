"""Starting, watching and stopping RunPod pods for video tools, with the caps enforced here.

One pod at a time. A start takes a transaction-scoped advisory lock, checks that nothing is
running and that the month's spend (settled pods plus what running pods have cost so far) is
under ``runpod_monthly_usd_cap``, writes the row, commits, and only then asks RunPod, so a
pod whose create answer is lost still has a row for the reaper. The reaper stops pods idle
past ``runpod_idle_stop_minutes``, older than ``runpod_max_pod_hours``, past the cap, or gone
from RunPod, and marks rows whose create never answered.
"""

from __future__ import annotations

import hashlib
import secrets
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, cast
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models import AdminAuditLog, VideoToolToken
from app.problems import AppError
from app.video_runpod.client import RunPodClient, RunPodError, proxy_url
from app.video_runpod.models import VideoRunpodSession
from app.video_runpod.schemas import (
    Canvas,
    GpuRoute,
    GpuRoutes,
    PodView,
    RouteState,
)

# A create that has not answered in this long is treated as failed (and its pod, if RunPod
# made one, is the one thing the owner may have to delete in the RunPod console).
CREATE_GRACE = timedelta(minutes=10)
LOCK_KEY = int.from_bytes(hashlib.sha256(b"video-runpod:start").digest()[:8], signed=True)
CENT = Decimal("0.0001")
# Room for models.lock (109.7 GiB) and scratch; a smaller volume cannot hold the models.
VOLUME_SIZE_GB = 150
MIN_VOLUME_GB = 120
# Data centres the RunPod console offers network volumes in (read 2026-10-31).
VOLUME_DATA_CENTERS = (
    "EU-RO-1",
    "EU-CZ-1",
    "EUR-IS-1",
    "EU-NL-1",
    "EUR-IS-3",
    "EUR-IS-4",
    "EUR-NO-1",
    "EUR-NO-2",
    "EU-FR-1",
    "US-CA-2",
    "US-CO-1",
    "US-IL-1",
    "US-KS-2",
    "US-NC-1",
    "US-NE-1",
    "US-TX-3",
    "US-WA-1",
    "CA-MTL-1",
    "CA-MTL-3",
    "CA-MTL-4",
    "AP-JP-1",
    "AP-IN-1",
    "AP-IN-2",
)

ClientFactory = Callable[[Settings], RunPodClient]


def missing_settings(settings: Settings) -> list[str]:
    return [
        label
        for value, label in (
            (settings.runpod_api_key, "API 金鑰"),
            (settings.runpod_image, "映像"),
        )
        if not value
    ]


def month_start(now: datetime) -> datetime:
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def cost_so_far(row: VideoRunpodSession, now: datetime) -> Decimal:
    if row.usd is not None:
        return row.usd
    if row.cost_per_hr is None or row.pod_id is None:
        return Decimal(0)
    end = row.stopped_at or now
    hours = Decimal(max((end - row.started_at).total_seconds(), 0)) / Decimal(3600)
    return (row.cost_per_hr * hours).quantize(CENT, rounding=ROUND_HALF_UP)


async def month_spend(session: AsyncSession, now: datetime) -> Decimal:
    rows = await session.scalars(
        select(VideoRunpodSession).where(VideoRunpodSession.started_at >= month_start(now))
    )
    return sum((cost_so_far(row, now) for row in rows), Decimal(0))


async def running(session: AsyncSession) -> list[VideoRunpodSession]:
    return list(
        await session.scalars(
            select(VideoRunpodSession)
            .where(VideoRunpodSession.stopped_at.is_(None))
            .order_by(VideoRunpodSession.started_at)
        )
    )


def view(row: VideoRunpodSession, now: datetime, token_prefix: str | None = None) -> PodView:
    return PodView(
        session_id=row.id,
        pod_id=row.pod_id,
        label=row.label,
        slug=row.slug,
        gpu=row.gpu,
        cloud_type=row.cloud_type,
        data_center_id=row.data_center_id,
        cost_per_hr=row.cost_per_hr,
        started_at=row.started_at,
        last_heartbeat_at=row.last_heartbeat_at,
        stopped_at=row.stopped_at,
        stop_reason=row.stop_reason,
        usd=cost_so_far(row, now),
        token_prefix=token_prefix,
    )


def _audit(
    session: AsyncSession,
    action: str,
    row: VideoRunpodSession,
    actor_id: UUID | None,
    **extra: Any,
) -> None:
    session.add(
        AdminAuditLog(
            actor_user_id=actor_id,
            action=action,
            target=f"runpod-session:{row.id}",
            metadata_json={"pod_id": row.pod_id, "label": row.label, "slug": row.slug, **extra},
        )
    )


def _price(pod: dict[str, Any]) -> Decimal | None:
    for key in ("adjustedCostPerHr", "costPerHr"):
        value = pod.get(key)
        if isinstance(value, int | float) and value > 0:
            return Decimal(str(value)).quantize(CENT)
    return None


def volume_gb(volume: dict[str, Any]) -> int:
    size = volume.get("size")
    return size if isinstance(size, int) else 0


async def stock_or_unknown(client: RunPodClient, data_center: str) -> str | None:
    """Stock in a data centre; a failed read is "unknown", so the create itself gets to answer."""
    try:
        return await client.gpu_stock(data_center)
    except RunPodError:
        return "unknown"


async def first_data_center_with_stock(client: RunPodClient, settings: Settings) -> str | None:
    preferred = settings.runpod_data_center_id
    others = [item for item in VOLUME_DATA_CENTERS if item != preferred]
    for data_center in ([preferred] if preferred else []) + others:
        if await client.gpu_stock(data_center):
            return data_center
    return None


async def existing_volume(client: RunPodClient, settings: Settings) -> dict[str, Any] | None:
    """The volume to use: the card's, else any in the account big enough for the models."""
    usable = [item for item in await client.list_volumes() if volume_gb(item) >= MIN_VOLUME_GB]
    chosen = next((i for i in usable if i["id"] == settings.runpod_network_volume_id), None)
    return chosen or (usable[0] if usable else None)


async def create_model_volume(
    client: RunPodClient, settings: Settings, data_center: str | None = None
) -> dict[str, Any]:
    """Open a volume where the GPU has stock now; RunPod bills it monthly until it is deleted."""
    place = data_center or await first_data_center_with_stock(client, settings)
    if place is None:
        raise RunPodError(
            409, f"{settings.runpod_gpu_type_id} 目前全區都沒貨；沒有開空間，也沒有花錢"
        )
    volume = await client.create_volume(
        name=f"mokaair-h3-{place.lower()}", size_gb=VOLUME_SIZE_GB, data_center_id=place
    )
    return {"size": VOLUME_SIZE_GB, "dataCenterId": place, **volume}


async def place_pod(
    client: RunPodClient, settings: Settings
) -> tuple[str, str, dict[str, Any] | None]:
    """Where the pod goes: (volume id, data centre, the volume if this call created it)."""
    volume = await existing_volume(client, settings)
    if volume is None:
        created = await create_model_volume(client, settings)
        return created["id"], created["dataCenterId"], created
    place = str(volume.get("dataCenterId"))
    # An existing volume is never left behind for a second one: its models are already there.
    if not await stock_or_unknown(client, place):
        raise RunPodError(
            409, f"{settings.runpod_gpu_type_id} 在現有空間的資料中心 {place} 目前沒貨；等有貨再開"
        )
    return volume["id"], place, None


async def start_pod(
    session: AsyncSession,
    settings: Settings,
    token: VideoToolToken | None,
    *,
    label: str,
    slug: str | None,
    client_factory: ClientFactory = RunPodClient,
    now: datetime | None = None,
    actor_id: UUID | None = None,
) -> tuple[VideoRunpodSession, str]:
    """Start one pod for a token or, with none, the admin; return its row and the gate token."""
    actor = token.created_by_user_id if token else actor_id
    missing = missing_settings(settings)
    if missing:
        raise AppError(503, "runpod_not_configured", f"後台 RunPod 卡還沒填：{'、'.join(missing)}")
    moment = now or datetime.now(UTC)
    await session.execute(select(func.pg_advisory_xact_lock(LOCK_KEY)))
    if await running(session):
        raise AppError(
            409, "runpod_pod_running", "已經有一個 RunPod pod 在跑；先停掉它或等回收器處理"
        )
    spent = await month_spend(session, moment)
    if spent >= settings.runpod_monthly_usd_cap:
        raise AppError(
            409,
            "runpod_cap_reached",
            f"本月 RunPod 已花 US${spent:.2f}，達到上限 US${settings.runpod_monthly_usd_cap}",
        )
    gate_token = secrets.token_urlsafe(32)
    row = VideoRunpodSession(
        id=uuid4(),
        token_id=token.id if token else None,
        label=label.strip(),
        slug=slug,
        gpu=settings.runpod_gpu_type_id,
        cloud_type=settings.runpod_cloud_type,
        data_center_id=settings.runpod_data_center_id,
        gate_token_hash=hashlib.sha256(gate_token.encode()).hexdigest(),
        started_at=moment,
        last_heartbeat_at=moment,
    )
    session.add(row)
    await session.commit()
    try:
        async with client_factory(settings) as client:
            volume_id, data_center, created = await place_pod(client, settings)
            row.data_center_id = data_center
            if created:
                _audit(
                    session,
                    "runpod.volume_created",
                    row,
                    actor,
                    volume_id=volume_id,
                    data_center=data_center,
                    size_gb=created["size"],
                )
                await session.commit()
            pod = await client.create_pod(
                # The row id is in the name, so a pod whose answer was lost can be found in the
                # RunPod console.
                name=f"mokaair-{row.id.hex[:8]}-{row.label}",
                env={"GATE_TOKEN": gate_token, "H3_PROFILE": settings.runpod_default_profile},
                data_center_id=data_center,
                network_volume_id=volume_id,
            )
    except RunPodError as error:
        row.stopped_at = datetime.now(UTC)
        row.stop_reason = "failed"
        row.usd = Decimal(0)
        _audit(session, "runpod.pod_failed", row, actor, detail=error.detail)
        await session.commit()
        if error.status == 409:
            raise AppError(409, "runpod_no_stock", error.detail) from error
        raise AppError(502, "runpod_create_failed", error.detail) from error
    row.pod_id = str(pod["id"])
    row.cost_per_hr = _price(pod)
    _audit(
        session,
        "runpod.pod_started",
        row,
        actor,
        token=token.token_prefix if token else None,
        gpu=row.gpu,
        cost_per_hr=str(row.cost_per_hr) if row.cost_per_hr is not None else None,
    )
    await session.commit()
    return row, gate_token


def base_url(row: VideoRunpodSession) -> str:
    return proxy_url(row.pod_id) if row.pod_id else ""


async def stop_pod(
    session: AsyncSession,
    settings: Settings,
    row: VideoRunpodSession,
    *,
    reason: str,
    actor_id: UUID | None,
    client_factory: ClientFactory = RunPodClient,
    now: datetime | None = None,
    already_gone: bool = False,
) -> VideoRunpodSession:
    """Terminate the pod (if RunPod still has it) and settle the row. Idempotent."""
    if row.stopped_at is not None:
        return row
    if row.pod_id and not already_gone:
        try:
            async with client_factory(settings) as client:
                await client.delete_pod(row.pod_id)
        except RunPodError as error:
            raise AppError(502, "runpod_stop_failed", error.detail) from error
    moment = now or datetime.now(UTC)
    row.stopped_at = moment
    row.stop_reason = reason
    row.usd = cost_so_far(row, moment)
    _audit(
        session,
        "runpod.pod_reaped" if reason not in {"manual"} else "runpod.pod_stopped",
        row,
        actor_id,
        reason=reason,
        usd=str(row.usd),
    )
    await session.commit()
    return row


async def heartbeat(
    session: AsyncSession, row: VideoRunpodSession, now: datetime | None = None
) -> VideoRunpodSession:
    if row.stopped_at is None:
        row.last_heartbeat_at = now or datetime.now(UTC)
        await session.commit()
    return row


def reap_reason(
    row: VideoRunpodSession, settings: Settings, now: datetime, over_cap: bool
) -> str | None:
    if row.pod_id is None:
        return "failed" if now - row.started_at > CREATE_GRACE else None
    if over_cap:
        return "cap"
    if now - row.started_at > timedelta(hours=settings.runpod_max_pod_hours):
        return "max_hours"
    last = row.last_heartbeat_at or row.started_at
    if now - last > timedelta(minutes=settings.runpod_idle_stop_minutes):
        return "idle"
    return None


async def reap(
    session: AsyncSession,
    settings: Settings,
    *,
    client_factory: ClientFactory = RunPodClient,
    now: datetime | None = None,
) -> list[VideoRunpodSession]:
    moment = now or datetime.now(UTC)
    rows = await running(session)
    if not rows:
        return []
    over_cap = await month_spend(session, moment) > settings.runpod_monthly_usd_cap
    stopped: list[VideoRunpodSession] = []
    for row in rows:
        reason = reap_reason(row, settings, moment, over_cap)
        gone = False
        if reason is None and row.pod_id and settings.runpod_api_key:
            # Someone may have deleted it in the RunPod console; then nothing is billing.
            try:
                async with client_factory(settings) as client:
                    pod = await client.get_pod(row.pod_id)
            except RunPodError:
                pod = {}
            if pod is None or (pod or {}).get("desiredStatus") in {"EXITED", "TERMINATED"}:
                reason, gone = "gone", True
        if reason is None:
            continue
        stopped.append(
            await stop_pod(
                session,
                settings,
                row,
                reason=reason,
                actor_id=None,
                client_factory=client_factory,
                now=moment,
                already_gone=gone or row.pod_id is None,
            )
        )
    return stopped


def gpu_routes(
    settings: Settings,
    token: VideoToolToken,
    *,
    canvas: Canvas,
    upscale: bool,
    month_usd: Decimal,
    pod_running: bool,
) -> GpuRoutes:
    """Which GPU route this token may use for a batch, and which one to use.

    `auto`: RunPod when the batch needs what Colab cannot give (a 1088p canvas, or the GPU
    upscale to 1080p), Colab otherwise, since its compute units are already paid for. A route
    the token may not use is never recommended.
    """
    missing = missing_settings(settings)
    remaining = Decimal(settings.runpod_monthly_usd_cap) - month_usd
    runpod_ready = bool(token.runpod_access) and not missing and remaining > 0 and not pod_running
    if not token.runpod_access:
        runpod_note = "這組權杖沒有 RunPod 權限"
    elif missing:
        runpod_note = f"後台 RunPod 卡還沒填：{'、'.join(missing)}"
    elif remaining <= 0:
        runpod_note = f"本月已達上限 US${settings.runpod_monthly_usd_cap}"
    elif pod_running:
        runpod_note = "已經有一個 pod 在跑"
    else:
        runpod_note = (
            f"{settings.runpod_gpu_type_id}（{settings.runpod_cloud_type}），"
            f"本月還剩 US${remaining:.2f}"
        )
    colab_ready = bool(token.colab_access)
    colab_note = (
        "最大 1344×768，運算單元餘額要用 h3.sh usage 自己查"
        if colab_ready
        else "這組權杖沒有 Colab 權限"
    )
    routes = [
        RouteState(
            route="colab", allowed=bool(token.colab_access), ready=colab_ready, note=colab_note
        ),
        RouteState(
            route="runpod", allowed=bool(token.runpod_access), ready=runpod_ready, note=runpod_note
        ),
    ]
    needs_runpod = canvas == "1088p" or upscale
    preferred = settings.gpu_route_default
    recommended: str | None
    if preferred == "runpod":
        recommended, reason = ("runpod", "後台預設 RunPod") if runpod_ready else (None, runpod_note)
    elif preferred == "colab":
        if needs_runpod:
            recommended, reason = None, "後台預設 Colab，但這批要 1088p 或 GPU 放大，Colab 做不到"
        else:
            recommended, reason = ("colab", "後台預設 Colab") if colab_ready else (None, colab_note)
    elif needs_runpod:
        recommended, reason = (
            ("runpod", "這批要 1088p 或 GPU 放大，只有 RunPod 做得到")
            if runpod_ready
            else (None, f"這批要 RunPod，但{runpod_note}")
        )
    elif colab_ready:
        recommended, reason = "colab", "736p 不放大：先用已付月費的 Colab 運算單元"
    elif runpod_ready:
        recommended, reason = "runpod", "這組權杖不能用 Colab，改用 RunPod"
    else:
        recommended, reason = None, "這組權杖准用的路線都還不能用"
    return GpuRoutes(
        routes=routes,
        recommended=cast(GpuRoute | None, recommended),
        reason=reason,
        default=preferred,
    )
