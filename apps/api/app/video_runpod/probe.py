"""The RunPod card's connection test: reads the account, the volume and the GPU, creates nothing.

Three things decide whether a pod can start where the settings say: the key works (the
balance comes back), the network volume exists in the chosen data centre (a pod can only
mount a volume in its own data centre), and the chosen GPU type has stock there. REST
(``runpod_api_base_url``) reports volumes; balance and stock are only on GraphQL
(``runpod_graphql_url``). Both hosts are pinned in ``OFFICIAL_PROVIDER_HOSTS``.
"""

from __future__ import annotations

from typing import Any

import httpx

from app.config import Settings

API_TIMEOUT_SECONDS = 15.0

PROBE_QUERY = """
query Probe($gpu: String!, $gpuCount: Int!, $dataCenterId: String, $secureCloud: Boolean) {
  myself { clientBalance }
  gpuTypes(input: { id: $gpu }) {
    id
    displayName
    memoryInGb
    lowestPrice(
      input: { gpuCount: $gpuCount, dataCenterId: $dataCenterId, secureCloud: $secureCloud }
    ) {
      stockStatus
      uninterruptablePrice
    }
  }
}
"""


class RunPodProbeError(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


def _headers(settings: Settings) -> dict[str, str]:
    return {"Authorization": f"Bearer {settings.runpod_api_key}", "Accept": "application/json"}


async def _graphql(http: httpx.AsyncClient, settings: Settings) -> dict[str, Any]:
    try:
        response = await http.post(
            settings.runpod_graphql_url,
            headers=_headers(settings),
            json={
                "query": PROBE_QUERY,
                "variables": {
                    "gpu": settings.runpod_gpu_type_id,
                    "gpuCount": 1,
                    "dataCenterId": settings.runpod_data_center_id,
                    "secureCloud": settings.runpod_cloud_type == "SECURE",
                },
            },
        )
    except httpx.HTTPError as error:
        raise RunPodProbeError(f"RunPod GraphQL 連不上（{type(error).__name__}）") from error
    if response.status_code in {401, 403}:
        raise RunPodProbeError(f"RunPod 金鑰被拒（HTTP {response.status_code}）")
    if response.status_code != 200:
        raise RunPodProbeError(f"RunPod GraphQL 回 HTTP {response.status_code}")
    try:
        body = response.json()
    except ValueError as error:
        raise RunPodProbeError("RunPod GraphQL 回的不是 JSON") from error
    if not isinstance(body, dict):
        raise RunPodProbeError("RunPod GraphQL 回的格式不對")
    errors = body.get("errors")
    if errors:
        first = errors[0].get("message") if isinstance(errors[0], dict) else None
        raise RunPodProbeError(f"RunPod GraphQL 錯誤：{str(first or errors[0])[:200]}")
    data = body.get("data")
    if not isinstance(data, dict):
        raise RunPodProbeError("RunPod GraphQL 沒有回 data")
    return data


async def _volume(http: httpx.AsyncClient, settings: Settings) -> dict[str, Any]:
    base = settings.runpod_api_base_url.rstrip("/")
    url = f"{base}/networkvolumes/{settings.runpod_network_volume_id}"
    try:
        response = await http.get(url, headers=_headers(settings))
    except httpx.HTTPError as error:
        raise RunPodProbeError(f"RunPod REST 連不上（{type(error).__name__}）") from error
    if response.status_code == 404:
        raise RunPodProbeError(f"找不到 network volume {settings.runpod_network_volume_id}")
    if response.status_code in {401, 403}:
        raise RunPodProbeError(f"RunPod 金鑰被拒（HTTP {response.status_code}）")
    if response.status_code != 200:
        raise RunPodProbeError(f"RunPod REST 回 HTTP {response.status_code}")
    try:
        body = response.json()
    except ValueError as error:
        raise RunPodProbeError("RunPod REST 回的不是 JSON") from error
    if not isinstance(body, dict):
        raise RunPodProbeError("RunPod REST 回的格式不對")
    return body


async def probe(settings: Settings, client: httpx.AsyncClient | None = None) -> str:
    """Return a one-line summary, or raise ``RunPodProbeError`` naming what is wrong."""
    if not settings.runpod_api_key:
        raise RunPodProbeError("請先填 RunPod API 金鑰")
    owned = client is None
    http = client or httpx.AsyncClient(timeout=API_TIMEOUT_SECONDS, trust_env=False)
    parts: list[str] = []
    problems: list[str] = []
    try:
        data = await _graphql(http, settings)
        myself = data.get("myself") or {}
        balance = myself.get("clientBalance") if isinstance(myself, dict) else None
        if isinstance(balance, int | float):
            parts.append(f"餘額 US${balance:,.2f}")

        gpus = data.get("gpuTypes") or []
        gpu = gpus[0] if isinstance(gpus, list) and gpus and isinstance(gpus[0], dict) else None
        if gpu is None:
            problems.append(f"RunPod 沒有 {settings.runpod_gpu_type_id} 這個 GPU 型號")
        else:
            lowest = gpu.get("lowestPrice") if isinstance(gpu.get("lowestPrice"), dict) else {}
            stock = lowest.get("stockStatus") if lowest else None
            price = lowest.get("uninterruptablePrice") if lowest else None
            name = gpu.get("displayName") or gpu.get("id")
            where = settings.runpod_data_center_id or "任一資料中心"
            cloud = settings.runpod_cloud_type.title()
            if not stock:
                problems.append(f"{name} 在 {where}（{cloud}）目前沒貨")
            else:
                priced = f"、US${price:.2f}/h" if isinstance(price, int | float) else ""
                parts.append(f"{name} 在 {where}（{cloud}）：{stock}{priced}")

        if not settings.runpod_network_volume_id:
            problems.append("還沒填 network volume")
        else:
            volume = await _volume(http, settings)
            volume_dc = volume.get("dataCenterId")
            size = volume.get("size")
            sized = f" {size} GB" if isinstance(size, int) else ""
            if settings.runpod_data_center_id and volume_dc != settings.runpod_data_center_id:
                problems.append(
                    f"volume {settings.runpod_network_volume_id} 在 {volume_dc}，"
                    f"不是設定的 {settings.runpod_data_center_id}（pod 掛不上）"
                )
            else:
                parts.append(f"volume{sized} 在 {volume_dc}")
        if not settings.runpod_data_center_id:
            problems.append("還沒填資料中心")
        if not settings.runpod_image:
            problems.append("還沒填映像（要帶 digest）")
    except RunPodProbeError as error:
        problems.insert(0, error.detail)
    finally:
        if owned:
            await http.aclose()
    if problems:
        raise RunPodProbeError("；".join(problems + parts))
    return "RunPod 連線成功：" + "；".join(parts)
