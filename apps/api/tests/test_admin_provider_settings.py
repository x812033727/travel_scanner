from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient

import app.admin.service as admin_service
from app.admin.service import (
    _default_provider_enabled,
    _merge_secret_values,
    _safe_test_message,
    _test_google,
    _validate_provider_values,
    apply_runtime_overrides,
    decrypt_secrets,
    encrypt_secrets,
    settings_snapshot,
)
from app.auth.service import current_user
from app.config import Settings
from app.main import app
from app.models import ProviderConfig, User
from app.problems import AppError
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

    monkeypatch.setattr(admin_service, "GoogleTravelService", PlacesStub)
    monkeypatch.setattr(admin_service, "GoogleRouteProvider", RoutesStub)

    message = await _test_google(Settings(google_maps_api_key="key"), object())  # type: ignore[arg-type]

    assert message == "Google Places 與 Routes API 連線成功；測試路線目前無可用班次"
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
