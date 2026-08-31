from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator


class AdminUserSummary(BaseModel):
    id: UUID
    email: str
    is_active: bool
    is_admin: bool
    effective_is_admin: bool
    admin_source: str
    is_self: bool
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


class AdminUserDetail(AdminUserSummary):
    usage_history: list[AdminUsageHistoryItem]
    admin_history: list[AdminUserAuditItem]


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
