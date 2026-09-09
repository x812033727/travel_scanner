import hashlib
import hmac
import json
import time
from typing import Any, TypeVar
from uuid import uuid4

import httpx
from pydantic import BaseModel

from app.config import Settings, get_settings
from app.database_admin.schemas import (
    AgentDatabaseCreateRequest,
    AgentDatabaseCreateResponse,
    AgentDatabaseJob,
    AgentDatabaseOverview,
    DatabaseOperationType,
)
from app.problems import AppError

T = TypeVar("T", bound=BaseModel)


class DatabaseAgentClient:
    """Narrow client for the database endpoints on the privileged host agent."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def _headers(self, method: str, path: str, body: bytes) -> dict[str, str]:
        key = self.settings.deploy_agent_hmac_key
        if not key:
            raise AppError(503, "database_agent_unavailable", "資料庫維運代理尚未完成設定")
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
                "database_agent_unavailable",
                "資料庫維運代理目前無法連線，請檢查主機服務",
            ) from exc
        if response.status_code >= 400:
            try:
                problem: dict[str, Any] = response.json()
            except ValueError:
                problem = {}
            raise AppError(
                response.status_code,
                str(problem.get("code") or "database_agent_error")[:64],
                str(problem.get("detail") or "資料庫維運代理拒絕這次操作")[:500],
            )
        try:
            return model.model_validate(response.json())
        except ValueError as exc:
            raise AppError(
                502, "database_agent_invalid_response", "資料庫維運代理回應格式不正確"
            ) from exc

    async def overview(self) -> AgentDatabaseOverview:
        return await self._request("GET", "/v1/database/overview", AgentDatabaseOverview)

    async def create(
        self, run_id: str, action: DatabaseOperationType
    ) -> AgentDatabaseCreateResponse:
        return await self._request(
            "POST",
            "/v1/database/operations",
            AgentDatabaseCreateResponse,
            AgentDatabaseCreateRequest(run_id=run_id, action=action),
        )

    async def job(self, job_id: str) -> AgentDatabaseJob:
        return await self._request(
            "GET", f"/v1/database/operations/{job_id}", AgentDatabaseJob
        )
