import pytest
from pydantic import ValidationError
from starlette.requests import Request

from app.auth.schemas import RegisterRequest, UserPreferencesUpdate
from app.i18n import normalize_locale, provider_locale
from app.problems import AppError, app_error_handler


@pytest.mark.parametrize("locale", ["en", "ja", "ko", "zh-TW", "zh-CN"])
def test_account_schemas_accept_every_supported_locale(locale: str) -> None:
    register = RegisterRequest(
        email="traveler@example.com",
        password="a-secure-password",
        preferred_locale=locale,  # type: ignore[arg-type]
    )
    update = UserPreferencesUpdate(preferred_locale=locale)  # type: ignore[arg-type]
    assert register.preferred_locale == locale
    assert update.preferred_locale == locale


def test_account_schemas_reject_unsupported_locale() -> None:
    with pytest.raises(ValidationError):
        UserPreferencesUpdate(preferred_locale="fr")  # type: ignore[arg-type]


def test_locale_fallback_and_provider_mappings_are_centralized() -> None:
    assert normalize_locale("fr") == "zh-TW"
    assert provider_locale("booking", "zh-CN") == "zh-cn"
    assert provider_locale("booking", "en") == "en-gb"
    assert provider_locale("google", "ko") == "ko"


@pytest.mark.asyncio
async def test_problem_response_uses_controlled_locale_header() -> None:
    request = Request({"type": "http", "headers": [(b"x-travel-locale", b"ja")]})
    response = await app_error_handler(
        request,
        AppError(401, "invalid_credentials", "Email 或密碼不正確"),
    )
    assert response.status_code == 401
    assert "メールアドレスまたはパスワード" in response.body.decode()
