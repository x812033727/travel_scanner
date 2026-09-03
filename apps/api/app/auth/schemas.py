from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

Locale = Literal["en", "ja", "ko", "zh-TW", "zh-CN"]
OAuthProvider = Literal["google", "line", "apple"]


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
    has_password: bool = True
    auth_methods: list[str] = Field(default_factory=lambda: ["password"])
    identity_count: int = 0


class UserPreferencesUpdate(BaseModel):
    preferred_locale: Locale


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
