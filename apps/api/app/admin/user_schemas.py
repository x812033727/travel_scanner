from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator


class AdminUserActivity(BaseModel):
    trips: int = 0
    searches: int = 0
    alerts: int = 0
    community_posts: int = 0
    community_comments: int = 0


class AdminUserSummary(BaseModel):
    id: UUID
    email: str
    is_active: bool
    is_admin: bool
    effective_is_admin: bool
    admin_source: str
    is_self: bool
    can_adjust_usage: bool
    status: Literal["active", "inactive", "suspended", "erasure_pending"] = "active"
    admin_roles: list[str] = Field(default_factory=list)
    auth_methods: list[str] = Field(default_factory=list)
    email_verified: bool = False
    last_login_at: datetime | None = None
    last_activity_at: datetime | None = None
    activity: AdminUserActivity = Field(default_factory=AdminUserActivity)
    suspended_at: datetime | None = None
    suspended_until: datetime | None = None
    suspension_reason: str | None = None
    erasure_status: str | None = None
    remaining_uses: int
    reserved_uses: int
    available_uses: int
    created_at: datetime
    updated_at: datetime


class AdminUserStats(BaseModel):
    total: int
    active: int
    administrators: int
    available_uses: int
    suspended: int = 0
    erasure_pending: int = 0


class AdminUserList(BaseModel):
    items: list[AdminUserSummary]
    page: int
    limit: int
    total: int
    pages: int
    stats: AdminUserStats


class AdminUsageHistoryItem(BaseModel):
    id: UUID
    occurred_at: datetime
    entry_type: str
    status: str
    change: int
    balance_after: int
    summary: str
    reference: str


class AdminUserAuditItem(BaseModel):
    id: UUID
    action: str
    actor_user_id: UUID | None
    metadata: dict[str, object]
    created_at: datetime


class AdminAuthIdentityItem(BaseModel):
    provider: str
    email: str | None
    email_verified: bool
    linked_at: datetime
    last_login_at: datetime | None


class AdminErasureStatus(BaseModel):
    id: UUID
    status: str
    scheduled_for: datetime
    requested_at: datetime
    cancelled_at: datetime | None = None
    completed_at: datetime | None = None
    reason: str


class AdminUserDetail(AdminUserSummary):
    usage_history: list[AdminUsageHistoryItem]
    admin_history: list[AdminUserAuditItem]
    auth_identities: list[AdminAuthIdentityItem] = Field(default_factory=list)
    erasure: AdminErasureStatus | None = None


class AdminUserUpdate(BaseModel):
    is_active: bool | None = None
    is_admin: bool | None = None

    @model_validator(mode="after")
    def require_change(self) -> "AdminUserUpdate":
        if self.is_active is None and self.is_admin is None:
            raise ValueError("至少需要一個帳號設定")
        return self


class AdminUsageAdjustment(BaseModel):
    change: int = Field(ge=-10_000, le=10_000)
    reason: str = Field(min_length=3, max_length=255)

    @field_validator("change")
    @classmethod
    def change_cannot_be_zero(cls, value: int) -> int:
        if value == 0:
            raise ValueError("調整次數不可為 0")
        return value

    @field_validator("reason", mode="before")
    @classmethod
    def clean_reason(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class AdminUsageAdjustmentResult(BaseModel):
    user: AdminUserDetail
    ledger_id: UUID
    change: int
    balance_after: int
    replayed: bool


AdminRole = Literal[
    "viewer",
    "support",
    "content",
    "operations",
    "database_operator",
    "deployer",
    "owner",
]
StepUpScope = Literal[
    "users.roles",
    "users.suspend_permanent",
    "users.erase",
    "database.backup",
    "database.analyze",
]


class AdminStepUpRequest(BaseModel):
    password: str = Field(min_length=1, max_length=128)
    scopes: list[StepUpScope] = Field(min_length=1, max_length=5)

    @field_validator("scopes")
    @classmethod
    def unique_scopes(cls, value: list[StepUpScope]) -> list[StepUpScope]:
        return list(dict.fromkeys(value))


class AdminStepUpResponse(BaseModel):
    scopes: list[StepUpScope]
    expires_at: datetime
    expires_in: int = 300


class AdminRolesUpdate(BaseModel):
    roles: list[AdminRole] = Field(max_length=7)
    reason: str = Field(min_length=3, max_length=255)
    confirmation: str = Field(min_length=1, max_length=400)
    expires_at: datetime | None = None

    @field_validator("roles")
    @classmethod
    def unique_roles(cls, value: list[AdminRole]) -> list[AdminRole]:
        return list(dict.fromkeys(value))

    @field_validator("reason", "confirmation", mode="before")
    @classmethod
    def clean_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class AdminSuspensionRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=255)
    suspended_until: datetime | None = None
    confirmation: str | None = Field(default=None, max_length=400)

    @field_validator("reason", "confirmation", mode="before")
    @classmethod
    def clean_optional_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class AdminReasonRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=255)

    @field_validator("reason", mode="before")
    @classmethod
    def clean_action_reason(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class AdminErasureRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=255)
    confirmation: str = Field(min_length=1, max_length=400)

    @field_validator("reason", "confirmation", mode="before")
    @classmethod
    def clean_erasure_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class AdminActionResult(BaseModel):
    user: AdminUserDetail
    replayed: bool = False
