import pytest

from app.config import Settings


def secure_production_settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "app_env": "production",
        "app_secret_key": "jwt-secret-that-is-random-and-at-least-32-chars",
        "settings_encryption_key": "settings-secret-that-is-separate-and-at-least-32",
        "database_url": "postgresql+asyncpg://travel:strong-db-password@postgres:5432/travel_scanner",
        "redis_url": "redis://:strong-redis-password@redis:6379/0",
        "api_cors_origins": "https://mocair.io",
        "next_public_site_url": "https://mocair.io",
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
        ({"api_cors_origins": "https://mocair.io/path"}, "API_CORS_ORIGINS"),
        ({"next_public_site_url": "http://mocair.io"}, "NEXT_PUBLIC_SITE_URL"),
        ({"next_public_site_url": "https://user@mocair.io"}, "NEXT_PUBLIC_SITE_URL"),
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
