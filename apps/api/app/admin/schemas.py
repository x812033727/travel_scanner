from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

type JsonScalar = str | int | float | bool


class ProviderSettingsUpdate(BaseModel):
    enabled: bool | None = None
    config: dict[str, JsonScalar | None] = Field(default_factory=dict)
    secrets: dict[str, str | None] = Field(default_factory=dict)


class SecretState(BaseModel):
    configured: bool
    masked: str | None = None
    source: str = "none"


class ProviderUsageView(BaseModel):
    period: str
    period_start: date
    period_end: date
    used: int | None
    monthly_limit: int
    remaining: int | None
    percentage: float | None
    breakdown: dict[str, int]
    tracking_started_at: datetime | None = None
    observed_at: datetime
    available: bool
    scope: str = "server_requests"


class ProviderSettingsView(BaseModel):
    provider: str
    label: str
    description: str
    enabled: bool
    configured: bool
    status: str
    status_message: str
    config: dict[str, JsonScalar | None]
    config_sources: dict[str, str]
    secrets: dict[str, SecretState]
    last_tested_at: datetime | None = None
    last_test_status: str | None = None
    last_test_message: str | None = None
    updated_at: datetime | None = None
    usage: ProviderUsageView | None = None


class AdminAuditView(BaseModel):
    id: UUID
    actor_user_id: UUID | None
    action: str
    target: str
    metadata: dict[str, object]
    created_at: datetime


class ProviderSettingsSnapshot(BaseModel):
    providers: list[ProviderSettingsView]
    audit: list[AdminAuditView]
    encryption_source: str


class ProviderTestResult(BaseModel):
    provider: str
    status: str
    message: str
    tested_at: datetime
    latency_ms: int


class PublicRuntimeConfig(BaseModel):
    google_maps_browser_key: str | None = None
    google_maps_enabled: bool = False
