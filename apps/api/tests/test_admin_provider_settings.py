from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient

from app.admin.service import (
    _default_provider_enabled,
    _safe_test_message,
    apply_runtime_overrides,
    decrypt_secrets,
    encrypt_secrets,
    settings_snapshot,
)
from app.auth.service import current_user
from app.config import Settings
from app.main import app
from app.models import ProviderConfig, User


class ScalarRows:
    def __init__(self, rows: list[Any]) -> None:
        self.rows = rows

    def all(self) -> list[Any]:
        return self.rows


class SnapshotSession:
    def __init__(self, providers: list[ProviderConfig]) -> None:
        self.providers = providers
        self.calls = 0

    async def scalars(self, _statement: object) -> ScalarRows:
        self.calls += 1
        return ScalarRows(self.providers if self.calls == 1 else [])


def test_provider_secrets_are_encrypted_and_round_trip() -> None:
    settings = Settings(
        app_secret_key="test-app-secret-at-least-thirty-two-characters",
        settings_encryption_key="dedicated-settings-key",
    )
    encrypted = encrypt_secrets({"google_maps_api_key": "server-secret-key"}, settings)
    assert encrypted is not None
    assert "server-secret-key" not in encrypted
    assert decrypt_secrets(encrypted, settings) == {"google_maps_api_key": "server-secret-key"}


def test_new_affiliate_provider_rows_default_to_disabled() -> None:
    assert not _default_provider_enabled("travelpayouts")
    assert not _default_provider_enabled("booking")
    assert _default_provider_enabled("google_maps")


def test_database_provider_settings_override_environment_and_can_disable_provider() -> None:
    base = Settings(
        app_secret_key="test-app-secret-at-least-thirty-two-characters",
        google_maps_api_key="environment-key",
        route_cache_ttl_seconds=900,
    )
    row = ProviderConfig(
        provider="google_maps",
        enabled=True,
        config={"route_cache_ttl_seconds": 1800},
        secret_config_encrypted=encrypt_secrets({"google_maps_api_key": "database-key"}, base),
    )
    effective = apply_runtime_overrides(base, [row])
    assert effective.google_maps_api_key == "database-key"
    assert effective.route_cache_ttl_seconds == 1800

    row.enabled = False
    disabled = apply_runtime_overrides(base, [row])
    assert disabled.google_maps_api_key is None


def test_connection_failure_message_redacts_provider_secrets() -> None:
    settings = Settings(google_maps_api_key="secret-google-key")
    message = _safe_test_message(
        "google_maps",
        "request with secret-google-key was rejected",
        settings,
    )
    assert message == "request with *** was rejected"


@pytest.mark.asyncio
async def test_admin_snapshot_never_returns_plaintext_secret() -> None:
    base = Settings()
    secret = "google-key-that-must-not-leak"
    row = ProviderConfig(
        provider="google_maps",
        enabled=True,
        config={},
        secret_config_encrypted=encrypt_secrets({"google_maps_api_key": secret}, base),
    )
    snapshot = await settings_snapshot(SnapshotSession([row]))  # type: ignore[arg-type]
    payload = snapshot.model_dump_json()
    assert secret not in payload
    google = next(item for item in snapshot.providers if item.provider == "google_maps")
    assert google.secrets["google_maps_api_key"].masked == "••••••••leak"
    assert google.secrets["google_maps_api_key"].source == "database"


@pytest.mark.asyncio
async def test_admin_api_rejects_regular_user() -> None:
    user = User(
        email="member@example.com",
        password_hash="unused",
        is_active=True,
        is_admin=False,
    )
    app.dependency_overrides[current_user] = lambda: user
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/admin/provider-settings")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 403
    assert response.json()["code"] == "admin_required"
