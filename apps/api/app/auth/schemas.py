from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

Locale = Literal["en", "ja", "ko", "zh-TW", "zh-CN"]


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


class UserPreferencesUpdate(BaseModel):
    preferred_locale: Locale


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class RegistrationStatus(BaseModel):
    registration_enabled: bool
