import pytest
from pydantic import ValidationError

from app.config import Settings


def secure_production_settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "app_env": "production",
        "app_secret_key": "jwt-secret-that-is-random-and-at-least-32-chars",
        "settings_encryption_key": "settings-secret-that-is-separate-and-at-least-32",
        "database_url": "postgresql+asyncpg://travel:strong-db-password@postgres:5432/travel_scanner",
        "redis_url": "redis://:strong-redis-password@redis:6379/0",
        "api_cors_origins": "https://mokaair.com",
        "next_public_site_url": "https://mokaair.com",
        "cookie_secure": True,
    }
    values.update(overrides)
    return Settings(**values)


def test_secure_production_configuration_is_accepted() -> None:
    secure_production_settings().validate_deployment_security()


@pytest.mark.parametrize(
    ("override", "message"),
    [
        ({"app_secret_key": "short"}, "APP_SECRET_KEY"),
        ({"settings_encryption_key": None}, "SETTINGS_ENCRYPTION_KEY"),
        ({"cookie_secure": False}, "COOKIE_SECURE"),
        ({"api_cors_origins": "*"}, "API_CORS_ORIGINS"),
        ({"api_cors_origins": "https://mokaair.com/path"}, "API_CORS_ORIGINS"),
        ({"next_public_site_url": "http://mokaair.com"}, "NEXT_PUBLIC_SITE_URL"),
        ({"next_public_site_url": "https://user@mokaair.com"}, "NEXT_PUBLIC_SITE_URL"),
        (
            {
                "openai_api_key": "production-openai-key",
                "openai_api_base_url": "https://attacker.example/v1",
            },
            "OPENAI_API_BASE_URL",
        ),
        (
            {
                "anthropic_api_key": "production-anthropic-key",
                "anthropic_api_base_url": "http://api.anthropic.com/v1",
            },
            "ANTHROPIC_API_BASE_URL",
        ),
        (
            {
                "line_messaging_enabled": True,
                "line_channel_secret": "line-channel-secret",
                "line_channel_access_token": "line-access-token",
                "line_official_account_id": "@travel",
                "line_api_base_url": "https://attacker.example",
            },
            "LINE_API_BASE_URL",
        ),
        ({"line_add_friend_url": "https://attacker.example/add"}, "LINE_ADD_FRIEND_URL"),
        (
            {"flightaware_api_key": "key", "flightaware_base_url": "https://attacker.example/x"},
            "FLIGHTAWARE_BASE_URL",
        ),
        (
            {"skyscanner_api_key": "key", "skyscanner_base_url": "https://evil.example"},
            "SKYSCANNER_BASE_URL",
        ),
        (
            {"duffel_access_token": "token", "duffel_base_url": "http://api.duffel.com"},
            "DUFFEL_BASE_URL",
        ),
        (
            {
                "google_travel_impact_api_key": "key",
                "google_travel_impact_base_url": "https://attacker.example/v1",
            },
            "GOOGLE_TRAVEL_IMPACT_BASE_URL",
        ),
        (
            {
                "travelpayouts_enabled": True,
                "travelpayouts_api_token": "token",
                "travelpayouts_api_base_url": "https://attacker.example",
            },
            "TRAVELPAYOUTS_API_BASE_URL",
        ),
        (
            {"database_url": "postgresql+asyncpg://travel:travel@postgres:5432/travel_scanner"},
            "DATABASE_URL",
        ),
        ({"redis_url": "redis://redis:6379/0"}, "REDIS_URL"),
    ],
)
def test_unsafe_production_configuration_is_rejected(
    override: dict[str, object], message: str
) -> None:
    with pytest.raises(RuntimeError, match=message):
        secure_production_settings(**override).validate_deployment_security()


def test_official_ai_and_line_endpoints_are_accepted_in_production() -> None:
    secure_production_settings(
        openai_api_key="production-openai-key",
        openai_api_base_url="https://api.openai.com/v1",
        anthropic_api_key="production-anthropic-key",
        anthropic_api_base_url="https://api.anthropic.com/v1",
        minimax_api_key="production-minimax-key",
        minimax_api_base_url="https://api.minimax.io/v1",
        line_messaging_enabled=True,
        line_channel_secret="line-channel-secret",
        line_channel_access_token="line-access-token",
        line_official_account_id="@travel",
        line_api_base_url="https://api.line.me",
        line_add_friend_url="https://lin.ee/example",
    ).validate_deployment_security()


def test_official_provider_endpoints_are_accepted_in_production() -> None:
    secure_production_settings(
        flightaware_api_key="key",
        flightaware_base_url="https://aeroapi.flightaware.com/aeroapi",
        skyscanner_api_key="key",
        skyscanner_base_url="https://partners.api.skyscanner.net",
        duffel_access_token="token",
        duffel_base_url="https://api.duffel.com",
        google_travel_impact_api_key="key",
        google_travel_impact_base_url="https://travelimpactmodel.googleapis.com/v1",
    ).validate_deployment_security()


def test_api_process_rejects_wildcard_cors_in_every_environment() -> None:
    with pytest.raises(RuntimeError, match="API_CORS_ORIGINS"):
        Settings(api_cors_origins="*").validate_api_serving_security()
    Settings(api_cors_origins="http://localhost:3000").validate_api_serving_security()


def test_production_api_process_requires_trusted_proxy_client_ip() -> None:
    with pytest.raises(RuntimeError, match="TRUST_PROXY_CLIENT_IP"):
        secure_production_settings(trust_proxy_client_ip=False).validate_api_serving_security()
    secure_production_settings(trust_proxy_client_ip=True).validate_api_serving_security()


def test_access_token_lifetime_is_bounded() -> None:
    with pytest.raises(ValidationError):
        Settings(access_token_expire_minutes=100_000)
    with pytest.raises(ValidationError):
        Settings(access_token_expire_minutes=1)
    assert Settings(access_token_expire_minutes=1440).access_token_expire_minutes == 1440
