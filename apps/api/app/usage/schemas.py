from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

SUPPORTED_LOCALES = ("zh-TW", "zh-CN", "en", "ja", "ko")


class UsageStatus(BaseModel):
    status: Literal["reserved", "charged", "released"]
    uses: int = 1
    reference: str


class UsagePackageInput(BaseModel):
    localized_names: dict[str, str]
    uses: int = Field(ge=1, le=100_000)
    price_twd: int = Field(ge=0, le=10_000_000)
    display_order: int = Field(ge=0, le=10_000)
    is_active: bool = True
    is_featured: bool = False

    @field_validator("localized_names")
    @classmethod
    def validate_localized_names(cls, value: dict[str, str]) -> dict[str, str]:
        if set(value) != set(SUPPORTED_LOCALES):
            raise ValueError("方案名稱必須完整提供五種支援語系")
        cleaned = {locale: name.strip() for locale, name in value.items()}
        if any(not name or len(name) > 100 for name in cleaned.values()):
            raise ValueError("各語系方案名稱必須包含 1 到 100 個字元")
        return cleaned


class TrialSettingsUpdate(BaseModel):
    uses: int = Field(ge=1, le=10_000)


class OperationCostsUpdate(BaseModel):
    costs: dict[str, int]

    @field_validator("costs")
    @classmethod
    def validate_cost_values(cls, value: dict[str, int]) -> dict[str, int]:
        if not value:
            raise ValueError("請至少提供一項功能扣次設定")
        if any(type(uses) is not int or uses < 0 or uses > 100 for uses in value.values()):
            raise ValueError("功能扣次必須是 0 到 100 的整數")
        return value


class AdminUsagePackageView(BaseModel):
    id: UUID
    code: str
    localized_names: dict[str, str]
    uses: int
    price_twd: int
    display_order: int
    is_active: bool
    is_featured: bool


class UsageOperationCostView(BaseModel):
    operation: str
    uses: int
    source: Literal["default", "database"]


class UsageSettingsAuditView(BaseModel):
    id: UUID
    actor_user_id: UUID | None
    action: str
    target: str
    metadata: dict[str, object]
    created_at: datetime


class UsageSettingsSnapshot(BaseModel):
    trial_uses: int
    packages: list[AdminUsagePackageView]
    operation_costs: list[UsageOperationCostView]
    audit: list[UsageSettingsAuditView]


class PublicUsagePackageView(BaseModel):
    code: str
    name: str
    uses: int
    price_twd: int
    display_order: int
    is_featured: bool
    expires: bool = False
    purchasable: bool = False


class UsageCatalog(BaseModel):
    trial_uses: int
    packages: list[PublicUsagePackageView]
    operation_costs: dict[str, int]
