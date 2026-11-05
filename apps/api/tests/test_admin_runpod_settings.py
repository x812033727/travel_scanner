"""The RunPod GPU card (ticket 2026-10-30-runpod-admin-settings).

RunPod is never called: the connection test runs on ``httpx.MockTransport``.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from app.admin import service as admin_service
from app.admin.schemas import ProviderSettingsUpdate
from app.admin.service import (
    CONNECTION_TESTED_PROVIDERS,
    PROVIDER_DEFINITIONS,
    _validate_provider_values,
    apply_runtime_overrides,
    card_state,
)
from app.config import Settings
from app.models import ProviderConfig
from app.problems import AppError
from app.video_runpod.probe import RunPodProbeError, probe

DIGEST = "ghcr.io/mokaair/runpod-h3@sha256:" + "a" * 64
READY = Settings(
    runpod_api_key="rp-key",
    runpod_data_center_id="EU-RO-1",
    runpod_network_volume_id="abc123xyz",
    runpod_image=DIGEST,
)


def _update(**config: Any) -> ProviderSettingsUpdate:
    return ProviderSettingsUpdate(config=config)


def test_the_card_is_registered_under_its_own_fields() -> None:
    definition = PROVIDER_DEFINITIONS["runpod"]
    assert definition.secret_fields == ("runpod_api_key",)
    assert "gpu_route_default" in definition.config_fields
    assert "runpod" in CONNECTION_TESTED_PROVIDERS
    defaults = Settings()
    assert defaults.runpod_gpu_type_id == "NVIDIA RTX 6000 Ada Generation"
    assert (defaults.runpod_cloud_type, defaults.runpod_default_canvas) == (
        "SECURE",
        "736p_upscale",
    )
    assert (
        defaults.runpod_idle_stop_minutes,
        defaults.runpod_max_pod_hours,
        defaults.runpod_monthly_usd_cap,
    ) == (15, 4, 50)
    assert defaults.gpu_route_default == "auto"


def test_valid_values_are_kept_and_blank_ids_are_dropped() -> None:
    merged = _validate_provider_values(
        "runpod",
        {"runpod_network_volume_id": "oldvolume1"},
        _update(
            runpod_image=f"  {DIGEST} ",
            runpod_data_center_id="US-TX-3",
            runpod_network_volume_id="",
            runpod_cloud_type="COMMUNITY",
            runpod_monthly_usd_cap=200,
            gpu_route_default="runpod",
        ),
    )
    assert merged["runpod_image"] == DIGEST
    assert merged["runpod_data_center_id"] == "US-TX-3"
    assert "runpod_network_volume_id" not in merged
    assert merged["runpod_monthly_usd_cap"] == 200


@pytest.mark.parametrize(
    ("config", "message"),
    [
        ({"runpod_image": "ghcr.io/mokaair/runpod-h3:latest"}, "digest"),
        ({"runpod_data_center_id": "eu-ro-1"}, "EU-RO-1"),
        ({"runpod_network_volume_id": "has spaces"}, "volume"),
        ({"runpod_api_base_url": "https://evil.example.com/v1"}, "官方"),
        ({"runpod_graphql_url": "https://evil.example.com/graphql"}, "官方"),
        ({"runpod_idle_stop_minutes": 0}, "範圍"),
        ({"runpod_max_pod_hours": 25}, "範圍"),
        ({"runpod_monthly_usd_cap": 5000}, "範圍"),
        ({"runpod_gpu_type_id": "NVIDIA H100"}, "範圍"),
        ({"gpu_route_default": "kling"}, "範圍"),
    ],
)
def test_invalid_values_are_refused(config: dict[str, Any], message: str) -> None:
    with pytest.raises(AppError) as refused:
        _validate_provider_values("runpod", {}, _update(**config))
    assert refused.value.status == 422
    assert message in refused.value.detail


def test_a_stored_off_host_url_is_ignored_so_the_key_never_leaves() -> None:
    base = Settings(app_secret_key="test-app-secret-at-least-thirty-two-characters")
    row = ProviderConfig(
        provider="runpod",
        enabled=True,
        config={"runpod_graphql_url": "https://evil.example.com/graphql"},
        secret_config_encrypted=admin_service.encrypt_secrets({"runpod_api_key": "db-key"}, base),
    )
    effective = apply_runtime_overrides(base, [row])
    assert effective.runpod_api_key == "db-key"
    assert effective.runpod_graphql_url == "https://api.runpod.io/graphql"


def test_the_card_names_what_is_missing() -> None:
    configured, status, message = card_state(
        "runpod",
        Settings(runpod_api_key="rp-key"),
        enabled=True,
        last_test_status=None,
        last_test_message=None,
    )
    assert (configured, status) == (False, "not_configured")
    assert "映像" in message and "network volume" not in message
    configured, status, message = card_state(
        "runpod", READY, enabled=True, last_test_status=None, last_test_message=None
    )
    assert (configured, status) == (True, "unverified")
    assert "RTX 6000 Ada" in message


def _runpod(
    *,
    stock: str | None = "High",
    volume_dc: str = "EU-RO-1",
    graphql_status: int = 200,
    seen: list[httpx.Request] | None = None,
) -> httpx.AsyncClient:
    def handler(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)
        assert request.headers["Authorization"] == "Bearer rp-key"
        if request.url.host == "api.runpod.io":
            assert request.method == "POST"
            variables = json.loads(request.content)["variables"]
            assert variables == {
                "gpu": "NVIDIA RTX 6000 Ada Generation",
                "gpuCount": 1,
                "dataCenterId": "EU-RO-1",
                "secureCloud": True,
            }
            if graphql_status != 200:
                return httpx.Response(graphql_status)
            return httpx.Response(
                200,
                json={
                    "data": {
                        "myself": {"clientBalance": 24.5},
                        "gpuTypes": [
                            {
                                "id": "NVIDIA RTX 6000 Ada Generation",
                                "displayName": "RTX 6000 Ada",
                                "memoryInGb": 48,
                                "lowestPrice": {
                                    "stockStatus": stock,
                                    "uninterruptablePrice": 1.03,
                                },
                            }
                        ],
                    }
                },
            )
        assert request.method == "GET"
        assert str(request.url) == "https://rest.runpod.io/v1/networkvolumes/abc123xyz"
        return httpx.Response(
            200, json={"id": "abc123xyz", "size": 100, "dataCenterId": volume_dc}
        )

    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


async def test_the_probe_reads_balance_stock_and_volume_and_creates_nothing() -> None:
    seen: list[httpx.Request] = []
    async with _runpod(seen=seen) as client:
        message = await probe(READY, client)
    assert message.startswith("RunPod 連線成功")
    assert "US$24.50" in message and "High" in message and "US$1.03/h" in message
    assert "100 GB" in message
    assert [request.method for request in seen] == ["POST", "GET"]


async def test_the_probe_names_each_problem() -> None:
    async with _runpod(volume_dc="US-TX-3") as client:
        with pytest.raises(RunPodProbeError, match="掛不上"):
            await probe(READY, client)
    async with _runpod(stock=None) as client:
        with pytest.raises(RunPodProbeError, match="沒貨"):
            await probe(READY, client)
    async with _runpod(graphql_status=401) as client:
        with pytest.raises(RunPodProbeError, match="金鑰被拒"):
            await probe(READY, client)
    with pytest.raises(RunPodProbeError, match="API 金鑰"):
        await probe(Settings())


async def test_the_service_test_wires_the_probe(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.video_runpod import probe as probe_module

    async def fake_probe(runtime: Settings, client: Any = None) -> str:
        raise RunPodProbeError("還沒填映像")

    monkeypatch.setattr(probe_module, "probe", fake_probe)
    with pytest.raises(ConnectionError, match="還沒填映像"):
        await admin_service._test_provider("runpod", READY, object())  # type: ignore[arg-type]


def test_the_blackwell_workstation_card_is_offered_by_runpods_exact_id() -> None:
    merged = _validate_provider_values(
        "runpod",
        {},
        _update(runpod_gpu_type_id="NVIDIA RTX PRO 6000 Blackwell Workstation Edition"),
    )
    assert merged["runpod_gpu_type_id"] == "NVIDIA RTX PRO 6000 Blackwell Workstation Edition"
    with pytest.raises(AppError):
        _validate_provider_values("runpod", {}, _update(runpod_gpu_type_id="RTX PRO 6000 WK"))
