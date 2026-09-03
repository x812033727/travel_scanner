from datetime import date, datetime
from typing import Literal
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


class ProviderSkuUsageView(BaseModel):
    sku: str
    label: str
    category: str
    operations: tuple[str, ...]
    used: int
    free_limit: int
    free_usage: int
    free_remaining: int
    billable_overage: int
    percentage: float


class ProviderMonthlyUsageView(BaseModel):
    period: str
    period_start: date
    period_end: date
    used: int
    free_limit: int
    free_usage: int
    free_remaining: int
    billable_overage: int
    breakdown: dict[str, int]
    sku_usage: tuple[ProviderSkuUsageView, ...]
    tracking_started_at: datetime | None = None


class ProviderUsageView(BaseModel):
    period: str
    period_start: date
    period_end: date
    used: int | None
    monthly_limit: int
    remaining: int | None
    percentage: float | None
    free_limit: int
    free_usage: int | None
    free_remaining: int | None
    billable_overage: int | None
    breakdown: dict[str, int]
    sku_usage: tuple[ProviderSkuUsageView, ...]
    monthly_history: tuple[ProviderMonthlyUsageView, ...]
    tracking_started_at: datetime | None = None
    observed_at: datetime
    available: bool
    period_kind: Literal["month", "day"] = "month"
    scope: str = "server_requests"
    billing_timezone: str = "America/Los_Angeles"
    pricing_region: str = "global"


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
    requests_24h: int = 0
    errors_24h: int = 0
    last_error_at: datetime | None = None


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
    google_routes_enabled: bool = False
    google_places_enabled: bool = False
    google_maps_embed_enabled: bool = False
    google_maps_javascript_enabled: bool = False
    navitime_enabled: bool = False
    naver_maps_browser_client_id: str | None = None
    naver_maps_enabled: bool = False
    naver_places_enabled: bool = False
    naver_directions_enabled: bool = False
    naver_dynamic_map_enabled: bool = False


class SiteVisibility(BaseModel):
    hotspots_enabled: bool = True
    trips_enabled: bool = True
    alerts_enabled: bool = True
    flight_status_enabled: bool = True
    airline_fares_enabled: bool = True
    pricing_enabled: bool = True
