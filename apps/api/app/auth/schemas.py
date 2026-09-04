from datetime import datetime
from typing import Literal, cast
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, model_validator

Locale = Literal["en", "ja", "ko", "zh-TW", "zh-CN"]
# The seven currencies apps/web/lib/destinations.ts assigns to the published
# destinations, plus USD as the neutral fallback for anywhere else. Note that
# app/destinations/catalog.py quotes only five of them: it has no price row
# for Singapore or Hong Kong, which are still bookable destinations.
Currency = Literal["TWD", "JPY", "KRW", "THB", "SGD", "HKD", "VND", "USD"]
OAuthProvider = Literal["google", "line", "apple"]
CURRENCIES: tuple[Currency, ...] = ("TWD", "JPY", "KRW", "THB", "SGD", "HKD", "VND", "USD")
DEFAULT_CURRENCY: Currency = "TWD"


def normalize_currency(value: str | None) -> Currency:
    """Fall back rather than 500 on a row written before this list existed."""
    if value in CURRENCIES:
        return cast(Currency, value)
    return DEFAULT_CURRENCY


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)
    preferred_locale: Locale = "zh-TW"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(max_length=128)
    new_password: str = Field(min_length=10, max_length=128)


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_admin: bool = False
    can_deploy: bool = False
    preferred_locale: Locale = "zh-TW"
    preferred_currency: Currency = "TWD"
    has_password: bool = True
    auth_methods: list[str] = Field(default_factory=lambda: ["password"])
    identity_count: int = 0


class UserPreferencesUpdate(BaseModel):
    # Both optional so a switcher can send just the preference it owns; the
    # locale switcher must never overwrite the currency and vice versa.
    preferred_locale: Locale | None = None
    preferred_currency: Currency | None = None

    @model_validator(mode="after")
    def require_one_preference(self) -> "UserPreferencesUpdate":
        if self.preferred_locale is None and self.preferred_currency is None:
            raise ValueError("至少要指定一項偏好設定")
        return self


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class OAuthExchangeResponse(TokenResponse):
    new_account: bool = False


class RegistrationStatus(BaseModel):
    registration_enabled: bool


class OAuthProvidersResponse(BaseModel):
    providers: dict[OAuthProvider, bool]


class OAuthStartRequest(BaseModel):
    intent: Literal["login", "link"] = "login"
    locale: Locale = "zh-TW"
    next_path: str = Field(default="/", max_length=2048)
    browser_binding: str = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")


class OAuthStartResponse(BaseModel):
    authorization_url: str
    flow_id: str
    state: str
    expires_in: int


class OAuthExchangeRequest(BaseModel):
    flow_id: str = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    state: str = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    code: str = Field(min_length=1, max_length=4096)
    browser_binding: str = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")


class AuthIdentityResponse(BaseModel):
    id: UUID
    provider: OAuthProvider
    email: EmailStr | None = None
    linked_at: datetime
    last_login_at: datetime | None = None
