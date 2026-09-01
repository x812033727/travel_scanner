from typing import Any

import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient

import app.admin.service as admin_service
from app.admin.schemas import ProviderSettingsUpdate
from app.admin.service import (
    _default_provider_enabled,
    _merge_secret_values,
    _safe_test_message,
    _test_google,
    _validate_provider_values,
    apply_runtime_overrides,
    decrypt_secrets,
    effective_registration_enabled,
    encrypt_secrets,
    settings_snapshot,
    update_provider_settings,
)
from app.auth.service import current_user
from app.config import Settings
from app.main import app
from app.models import AdminAuditLog, ProviderConfig, User
from app.problems import AppError
from app.providers.usage_meter import record_google_maps_request
from app.trips.routing import GoogleRoutesProbeResult, RoutePoint


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


class RegistrationSession:
    def __init__(self, row: ProviderConfig | None) -> None:
        self.row = row

    async def scalar(self, _statement: object) -> ProviderConfig | None:
        return self.row


class UpdateSession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.committed = False

    async def scalar(self, _statement: object) -> None:
        return None

    def add(self, value: object) -> None:
        self.added.append(value)

    async def commit(self) -> None:
        self.committed = True


def test_provider_secrets_are_encrypted_and_round_trip() -> None:
    settings = Settings(
        app_secret_key="test-app-secret-at-least-thirty-two-characters",
        settings_encryption_key="dedicated-settings-key",
    )
    encrypted = encrypt_secrets({"google_maps_api_key": "server-secret-key"}, settings)
    assert encrypted is not None
    assert "server-secret-key" not in encrypted
    assert decrypt_secrets(encrypted, settings) == {"google_maps_api_key": "server-secret-key"}


def test_blank_secret_keeps_existing_value_and_null_clears_it() -> None:
    assert _merge_secret_values({"token": "original"}, {"token": "   "}) == {
        "token": "original"
    }
    assert _merge_secret_values({"token": "original"}, {"token": None}) == {}


def test_new_affiliate_provider_rows_default_to_disabled() -> None:
    assert not _default_provider_enabled("travelpayouts")
    assert not _default_provider_enabled("booking")
    assert not _default_provider_enabled("booking_demand")
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


def test_runtime_accepts_independent_hotel_provider_mode() -> None:
    validated = _validate_provider_values(
        "runtime",
        {},
        admin_service.ProviderSettingsUpdate(
            config={
                "travel_provider_mode": "amadeus",
                "flight_provider_mode": "auto",
                "hotel_provider_mode": "booking",
            }
        ),
    )

    assert validated["hotel_provider_mode"] == "booking"


def test_registration_defaults_to_open() -> None:
    assert Settings.model_construct().registration_enabled is True


def test_registration_setting_rejects_non_boolean_values() -> None:
    with pytest.raises(AppError, match="registration_enabled 必須是布林值"):
        _validate_provider_values(
            "runtime",
            {},
            ProviderSettingsUpdate(config={"registration_enabled": 0}),
        )


@pytest.mark.asyncio
async def test_registration_database_value_overrides_environment_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        admin_service,
        "get_settings",
        lambda: Settings(registration_enabled=False),
    )
    assert not await effective_registration_enabled(RegistrationSession(None))  # type: ignore[arg-type]

    row = ProviderConfig(
        provider="runtime",
        enabled=True,
        config={"registration_enabled": True},
    )
    assert await effective_registration_enabled(RegistrationSession(row))  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_runtime_update_uses_system_audit_without_sensitive_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_snapshot = object()

    async def fake_snapshot(*_args: object) -> object:
        return expected_snapshot

    monkeypatch.setattr(admin_service, "settings_snapshot", fake_snapshot)
    session = UpdateSession()
    actor = User(
        id=admin_service.uuid4(),
        email="admin@example.com",
        password_hash="unused",
        is_admin=True,
    )

    result = await update_provider_settings(
        session,  # type: ignore[arg-type]
        "runtime",
        ProviderSettingsUpdate(
            config={"registration_enabled": False, "provider_timeout_seconds": 8}
        ),
        actor,
        object(),  # type: ignore[arg-type]
    )

    assert result is expected_snapshot
    assert session.committed
    row = next(item for item in session.added if isinstance(item, ProviderConfig))
    audit = next(item for item in session.added if isinstance(item, AdminAuditLog))
    assert row.config["registration_enabled"] is False
    assert audit.action == "system_settings_updated"
    assert audit.actor_user_id == actor.id
    assert audit.target == "runtime"
    assert audit.metadata_json == {
        "config_fields": ["provider_timeout_seconds", "registration_enabled"],
        "registration_enabled": False,
    }


def test_booking_demand_environment_uses_only_official_v31_url() -> None:
    validated = _validate_provider_values(
        "booking_demand",
        {},
        admin_service.ProviderSettingsUpdate(
            config={
                "booking_demand_env": "production",
                "booking_demand_api_base_url": "https://demandapi-sandbox.booking.com/3.1",
                "booking_demand_affiliate_id": "12345",
                "booking_booker_country": "TW",
                "booking_language": "ZH-TW",
            }
        ),
    )
    assert validated["booking_demand_api_base_url"] == "https://demandapi.booking.com/3.1"
    assert validated["booking_booker_country"] == "tw"
    assert validated["booking_language"] == "zh-tw"

    with pytest.raises(AppError, match="Booking Demand API"):
        _validate_provider_values(
            "booking_demand",
            {},
            admin_service.ProviderSettingsUpdate(
                config={"booking_demand_api_base_url": "https://example.com/3.1"}
            ),
        )
    with pytest.raises(AppError, match="Booking Demand API"):
        _validate_provider_values(
            "booking_demand",
            {},
            admin_service.ProviderSettingsUpdate(
                config={"booking_demand_api_base_url": "https://demandapi.booking.com/3.1"}
            ),
        )


@pytest.mark.asyncio
async def test_google_connection_accepts_reachable_empty_route(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed_points: list[RoutePoint] = []

    class PlacesStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def autocomplete(self, *_args: object) -> list[dict[str, Any]]:
            return [{"place_id": "unstable-first-prediction"}]

    class RoutesStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def probe(
            self,
            origin: RoutePoint,
            destination: RoutePoint,
        ) -> GoogleRoutesProbeResult:
            observed_points.extend([origin, destination])
            return GoogleRoutesProbeResult(True, False, status_code=200)

    class WeatherStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def lookup(self, **_kwargs: object) -> object:
            return type("Weather", (), {"current": object(), "days": []})()

    monkeypatch.setattr(admin_service, "GoogleTravelService", PlacesStub)
    monkeypatch.setattr(admin_service, "GoogleRouteProvider", RoutesStub)
    monkeypatch.setattr(admin_service, "GoogleWeatherService", WeatherStub)

    message = await _test_google(Settings(google_maps_api_key="key"), object())  # type: ignore[arg-type]

    assert message == (
        "Google Places、Routes API 可連線；測試路線目前無可用班次；"
        "Weather API 連線成功"
    )
    assert observed_points[0].provider_place_id is None
    assert observed_points[0].latitude == 35.6812


@pytest.mark.asyncio
async def test_google_connection_reports_routes_http_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class PlacesStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def autocomplete(self, *_args: object) -> list[dict[str, Any]]:
            return [{"place_id": "tokyo"}]

    class RoutesStub:
        def __init__(self, *_args: object) -> None:
            pass

        async def probe(
            self,
            _origin: RoutePoint,
            _destination: RoutePoint,
        ) -> GoogleRoutesProbeResult:
            return GoogleRoutesProbeResult(
                False,
                False,
                status_code=403,
                error_code="PERMISSION_DENIED",
            )

    monkeypatch.setattr(admin_service, "GoogleTravelService", PlacesStub)
    monkeypatch.setattr(admin_service, "GoogleRouteProvider", RoutesStub)

    with pytest.raises(
        ConnectionError,
        match=r"Routes API 連線失敗（HTTP 403 / PERMISSION_DENIED）",
    ):
        await _test_google(Settings(google_maps_api_key="key"), object())  # type: ignore[arg-type]


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
async def test_admin_snapshot_lists_google_monthly_free_usage_by_sku() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    await record_google_maps_request(redis, "weather_current")
    await record_google_maps_request(redis, "weather_daily_forecast")
    row = ProviderConfig(
        provider="google_maps",
        enabled=True,
        config={
            "google_maps_essentials_free_limit": 100,
            "google_maps_enterprise_free_limit": 10,
        },
    )

    snapshot = await settings_snapshot(
        SnapshotSession([row]),  # type: ignore[arg-type]
        redis,
    )

    google = next(item for item in snapshot.providers if item.provider == "google_maps")
    assert google.usage is not None
    assert google.usage.used == 2
    weather = next(item for item in google.usage.sku_usage if item.sku == "weather_usage")
    assert weather.used == 2
    assert weather.free_limit == 100
    assert weather.free_remaining == 98
    assert len(google.usage.monthly_history) == 6
    await redis.aclose()


@pytest.mark.asyncio
async def test_production_booking_is_not_marked_available_until_connection_test_passes() -> None:
    base = Settings()
    row = ProviderConfig(
        provider="booking_demand",
        enabled=True,
        config={
            "booking_demand_env": "production",
            "booking_demand_api_base_url": "https://demandapi.booking.com/3.1",
            "booking_demand_affiliate_id": "12345",
        },
        secret_config_encrypted=encrypt_secrets(
            {"booking_demand_api_token": "booking-production-secret"}, base
        ),
    )
    pending = await settings_snapshot(SnapshotSession([row]))  # type: ignore[arg-type]
    booking = next(item for item in pending.providers if item.provider == "booking_demand")
    assert booking.configured is False
    assert booking.status == "test_required"

    row.last_test_status = "success"
    ready = await settings_snapshot(SnapshotSession([row]))  # type: ignore[arg-type]
    booking = next(item for item in ready.providers if item.provider == "booking_demand")
    assert booking.configured is True
    assert booking.status == "ready"
    assert "booking-production-secret" not in ready.model_dump_json()


@pytest.mark.asyncio
async def test_ai_planner_secrets_are_masked_and_reported_as_configured() -> None:
    base = Settings()
    secrets = {
        "openai_api_key": "openai-secret-ending-1234",
        "anthropic_api_key": "anthropic-secret-ending-5678",
    }
    row = ProviderConfig(
        provider="ai_planner",
        enabled=True,
        config={"ai_planner_mode": "auto"},
        secret_config_encrypted=encrypt_secrets(secrets, base),
    )
    snapshot = await settings_snapshot(SnapshotSession([row]))  # type: ignore[arg-type]
    payload = snapshot.model_dump_json()
    assert all(secret not in payload for secret in secrets.values())
    planner = next(item for item in snapshot.providers if item.provider == "ai_planner")
    assert planner.configured is True
    assert planner.secrets["openai_api_key"].masked == "••••••••1234"
    assert planner.secrets["anthropic_api_key"].source == "database"


def test_ai_planner_rejects_non_official_base_url_and_invalid_priority() -> None:
    with pytest.raises(AppError) as host_error:
        _validate_provider_values(
            "ai_planner",
            {},
            ProviderSettingsUpdate(
                config={"openai_api_base_url": "https://attacker.example/v1"}
            ),
        )
    assert getattr(host_error.value, "code", None) == "provider_setting_invalid"

    with pytest.raises(AppError) as priority_error:
        _validate_provider_values(
            "ai_planner",
            {},
            ProviderSettingsUpdate(config={"ai_planner_priority": "openai,openai"}),
        )
    assert getattr(priority_error.value, "code", None) == "provider_setting_invalid"


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
