import pytest

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
