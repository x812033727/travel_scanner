from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

GpuRoute = Literal["colab", "runpod"]
Canvas = Literal["736p", "1088p"]


class PodStartIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # What the batch is, for the admin list and the audit log.
    label: str = Field(min_length=1, max_length=80)
    slug: str | None = Field(default=None, max_length=120, pattern=r"^[a-z0-9][a-z0-9-]*$")


class PodStarted(BaseModel):
    session_id: UUID
    pod_id: str
    # The pod's gate behind RunPod's HTTP proxy; it answers once ComfyUI is up.
    base_url: str
    # Shown once: the gate accepts it as a bearer token. Only its SHA-256 is kept.
    gate_token: str
    cost_per_hr: Decimal | None
    idle_stop_minutes: int
    max_pod_hours: int
    # The card's sampling profile, for a runner not told one.
    default_profile: str


class PodView(BaseModel):
    session_id: UUID
    pod_id: str | None
    label: str
    slug: str | None
    gpu: str
    cloud_type: str
    data_center_id: str | None
    cost_per_hr: Decimal | None
    started_at: datetime
    last_heartbeat_at: datetime | None
    stopped_at: datetime | None
    stop_reason: str | None
    # Settled once stopped; while running, what it has cost so far.
    usd: Decimal
    token_prefix: str | None = None


class SessionsOverview(BaseModel):
    running: list[PodView]
    recent: list[PodView]
    month_usd: Decimal
    monthly_usd_cap: int
    configured: bool


class ReapResult(BaseModel):
    stopped: list[PodView]


class RouteState(BaseModel):
    route: GpuRoute
    allowed: bool
    ready: bool
    note: str


class GpuRoutes(BaseModel):
    routes: list[RouteState]
    # Null when no route this token may use is ready.
    recommended: GpuRoute | None
    reason: str
    default: Literal["auto", "colab", "runpod"]


class VolumeView(BaseModel):
    id: str
    name: str | None
    size_gb: int
    data_center_id: str | None
    # The card's GPU in this volume's data centre; None means no stock, "unknown" a failed read.
    stock: str | None
    usable: bool


class VolumesOverview(BaseModel):
    gpu: str
    volumes: list[VolumeView]
    # What opening a volume would give and cost per month.
    new_volume_gb: int
    new_volume_usd_per_month: Decimal


class AdminPodStartIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str = Field(default="後台手動開啟", min_length=1, max_length=80)


class VolumeCreateIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # Left out: the first data centre with stock of the card's GPU.
    data_center_id: str | None = Field(default=None, pattern=r"^[A-Z]{2}-[A-Z]{2,5}-[0-9]{1,3}$")
