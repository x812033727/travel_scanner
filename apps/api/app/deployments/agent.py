import hashlib
import hmac
import json
import time
from typing import Any, TypeVar
from uuid import uuid4

import httpx
from pydantic import BaseModel

from app.config import Settings, get_settings
from app.deployments.schemas import (
    AgentCreateRequest,
    AgentCreateResponse,
    AgentDeploymentJob,
    AgentOverview,
    DeploymentPreflightResult,
)
from app.problems import AppError

T = TypeVar("T", bound=BaseModel)


class DeploymentAgentClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def _headers(self, method: str, path: str, body: bytes) -> dict[str, str]:
        key = self.settings.deploy_agent_hmac_key
        if not key:
            raise AppError(503, "deployment_agent_unavailable", "部署代理尚未完成設定")
        timestamp = str(int(time.time()))
        nonce = uuid4().hex
        digest = hashlib.sha256(body).hexdigest()
        message = f"{timestamp}\n{nonce}\n{method.upper()}\n{path}\n{digest}".encode()
        signature = hmac.new(key.encode(), message, hashlib.sha256).hexdigest()
        return {
            "Content-Type": "application/json",
            "X-Deploy-Timestamp": timestamp,
            "X-Deploy-Nonce": nonce,
            "X-Deploy-Signature": signature,
        }

    async def _request(
        self,
        method: str,
        path: str,
        model: type[T],
        payload: BaseModel | None = None,
    ) -> T:
        body = (
            json.dumps(payload.model_dump(mode="json"), separators=(",", ":")).encode()
            if payload is not None
            else b""
        )
        transport = httpx.AsyncHTTPTransport(uds=self.settings.deploy_agent_socket)
        try:
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://deployer",
                timeout=self.settings.deploy_agent_timeout_seconds,
            ) as client:
                response = await client.request(
                    method,
                    path,
                    content=body or None,
                    headers=self._headers(method, path, body),
                )
        except (httpx.HTTPError, OSError) as exc:
            raise AppError(
                503,
                "deployment_agent_unavailable",
                "部署代理目前無法連線，請檢查主機服務",
            ) from exc
        if response.status_code >= 400:
            try:
                problem: dict[str, Any] = response.json()
            except ValueError:
                problem = {}
            code = str(problem.get("code") or "deployment_agent_error")[:64]
            detail = str(problem.get("detail") or "部署代理拒絕這次操作")[:500]
            raise AppError(response.status_code, code, detail)
        try:
            return model.model_validate(response.json())
        except ValueError as exc:
            raise AppError(
                502, "deployment_agent_invalid_response", "部署代理回應格式不正確"
            ) from exc

    async def overview(self) -> AgentOverview:
        return await self._request("GET", "/v1/overview", AgentOverview)

    async def preflight(self) -> DeploymentPreflightResult:
        return await self._request("POST", "/v1/preflight", DeploymentPreflightResult)

    async def create(self, run_id: str, target_sha: str) -> AgentCreateResponse:
        return await self._request(
            "POST",
            "/v1/deployments",
            AgentCreateResponse,
            AgentCreateRequest(run_id=run_id, target_sha=target_sha),
        )

    async def job(self, job_id: str) -> AgentDeploymentJob:
        return await self._request("GET", f"/v1/deployments/{job_id}", AgentDeploymentJob)
