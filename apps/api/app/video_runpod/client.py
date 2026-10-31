"""The RunPod calls the broker makes: pods and network volumes on REST, GPU stock on GraphQL.

Base ``runpod_api_base_url`` (pinned to rest.runpod.io), bearer auth. Request and response
fields follow the REST reference read 2026-10-30 (docs.runpod.io/api-reference/pods): ``env``
is a map, ``ports`` a list of ``"<port>/<protocol>"``, ``desiredStatus`` one of RUNNING,
EXITED or TERMINATED. Delete (terminate) rather than stop: a stopped pod keeps billing for
its pod volume, and the models live on the network volume, which a delete leaves alone.
"""

from __future__ import annotations

from typing import Any

import httpx

from app.config import Settings

API_TIMEOUT_SECONDS = 30.0
COMFY_PORT = 8188
CONTAINER_DISK_GB = 40
# H3's text encoder and VAE are moved between GPU and system memory; below this they swap.
MIN_RAM_PER_GPU_GB = 64
STOCK_QUERY = """
query Stock($gpu: String!, $dataCenterId: String, $secureCloud: Boolean) {
  gpuTypes(input: { id: $gpu }) {
    lowestPrice(input: { gpuCount: 1, dataCenterId: $dataCenterId, secureCloud: $secureCloud }) {
      stockStatus
    }
  }
}
"""


class RunPodError(Exception):
    def __init__(self, status: int, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.detail = detail


def proxy_url(pod_id: str, port: int = COMFY_PORT) -> str:
    """RunPod's HTTP proxy for a pod port (the pod's gate answers there)."""
    return f"https://{pod_id}-{port}.proxy.runpod.net"


class RunPodClient:
    def __init__(self, settings: Settings, http: httpx.AsyncClient | None = None) -> None:
        if not settings.runpod_api_key:
            raise RunPodError(503, "RunPod API 金鑰還沒設定")
        self._settings = settings
        self._base = settings.runpod_api_base_url.rstrip("/")
        self._owned = http is None
        self._http = http or httpx.AsyncClient(timeout=API_TIMEOUT_SECONDS, trust_env=False)

    async def __aenter__(self) -> RunPodClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        if self._owned:
            await self._http.aclose()

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._settings.runpod_api_key}",
            "Accept": "application/json",
        }

    async def _call(
        self, method: str, path: str, body: dict[str, Any] | None = None
    ) -> httpx.Response:
        try:
            return await self._http.request(
                method, f"{self._base}{path}", headers=self._headers(), json=body
            )
        except httpx.HTTPError as error:
            raise RunPodError(502, f"RunPod 連不上（{type(error).__name__}）") from error

    @staticmethod
    def _json(response: httpx.Response) -> dict[str, Any]:
        try:
            body = response.json()
        except ValueError as error:
            raise RunPodError(502, "RunPod 回的不是 JSON") from error
        if not isinstance(body, dict):
            raise RunPodError(502, "RunPod 回的格式不對")
        return body

    @staticmethod
    def _refused(response: httpx.Response, action: str) -> RunPodError:
        if response.status_code in {401, 403}:
            return RunPodError(502, f"RunPod 金鑰被拒（HTTP {response.status_code}）")
        return RunPodError(502, f"RunPod {action}失敗（HTTP {response.status_code}）")

    async def create_pod(
        self, *, name: str, env: dict[str, str], data_center_id: str, network_volume_id: str
    ) -> dict[str, Any]:
        settings = self._settings
        body: dict[str, Any] = {
            "name": name[:191],
            "imageName": settings.runpod_image,
            "gpuTypeIds": [settings.runpod_gpu_type_id],
            "gpuCount": 1,
            "cloudType": settings.runpod_cloud_type,
            "dataCenterIds": [data_center_id],
            "networkVolumeId": network_volume_id,
            "volumeMountPath": "/workspace",
            "containerDiskInGb": CONTAINER_DISK_GB,
            "minRAMPerGPU": MIN_RAM_PER_GPU_GB,
            "ports": [f"{COMFY_PORT}/http"],
            "env": env,
            "interruptible": False,
        }
        response = await self._call("POST", "/pods", body)
        if response.status_code not in {200, 201}:
            raise self._refused(response, "開 pod ")
        pod = self._json(response)
        if not isinstance(pod.get("id"), str) or not pod["id"]:
            raise RunPodError(502, "RunPod 開了 pod 卻沒回 id")
        return pod

    async def get_pod(self, pod_id: str) -> dict[str, Any] | None:
        response = await self._call("GET", f"/pods/{pod_id}")
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise self._refused(response, "讀 pod ")
        return self._json(response)

    async def delete_pod(self, pod_id: str) -> bool:
        """Terminate the pod; False when RunPod no longer knows it."""
        response = await self._call("DELETE", f"/pods/{pod_id}")
        if response.status_code in {404, 400}:
            return False
        if response.status_code not in {200, 204}:
            raise self._refused(response, "停 pod ")
        return True

    async def list_volumes(self) -> list[dict[str, Any]]:
        response = await self._call("GET", "/networkvolumes")
        if response.status_code != 200:
            raise self._refused(response, "列 volume ")
        try:
            body = response.json()
        except ValueError as error:
            raise RunPodError(502, "RunPod 回的不是 JSON") from error
        if not isinstance(body, list):
            raise RunPodError(502, "RunPod 回的格式不對")
        return [item for item in body if isinstance(item, dict) and item.get("id")]

    async def create_volume(
        self, *, name: str, size_gb: int, data_center_id: str
    ) -> dict[str, Any]:
        response = await self._call(
            "POST",
            "/networkvolumes",
            {"name": name, "size": size_gb, "dataCenterId": data_center_id},
        )
        if response.status_code not in {200, 201}:
            raise self._refused(response, "開 volume ")
        volume = self._json(response)
        if not isinstance(volume.get("id"), str) or not volume["id"]:
            raise RunPodError(502, "RunPod 開了 volume 卻沒回 id")
        return volume

    async def delete_volume(self, volume_id: str) -> bool:
        response = await self._call("DELETE", f"/networkvolumes/{volume_id}")
        if response.status_code == 404:
            return False
        if response.status_code not in {200, 204}:
            raise self._refused(response, "刪 volume ")
        return True

    async def gpu_stock(self, data_center_id: str) -> str | None:
        """The stock level of the card's GPU in one data centre; None when it has none."""
        settings = self._settings
        try:
            response = await self._http.post(
                settings.runpod_graphql_url,
                headers=self._headers(),
                json={
                    "query": STOCK_QUERY,
                    "variables": {
                        "gpu": settings.runpod_gpu_type_id,
                        "dataCenterId": data_center_id,
                        "secureCloud": settings.runpod_cloud_type == "SECURE",
                    },
                },
            )
        except httpx.HTTPError as error:
            raise RunPodError(502, f"RunPod 連不上（{type(error).__name__}）") from error
        if response.status_code != 200:
            raise self._refused(response, "查供應")
        body = self._json(response)
        if body.get("errors"):
            raise RunPodError(502, "RunPod 查供應回了錯誤")
        gpus = (body.get("data") or {}).get("gpuTypes") or []
        lowest = gpus[0].get("lowestPrice") if gpus and isinstance(gpus[0], dict) else None
        return (lowest.get("stockStatus") or None) if isinstance(lowest, dict) else None
