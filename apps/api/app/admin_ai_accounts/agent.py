import hashlib
import hmac
import json
import time
from typing import Any, TypeVar
from uuid import uuid4

import httpx
from pydantic import BaseModel

from app.admin_ai_accounts.schemas import (
    AgentOverview,
    AiDefaults,
    AiLoginSession,
    AiLogoutResult,
    Slot,
    Tool,
)
from app.config import Settings, get_settings
from app.problems import AppError

T = TypeVar("T", bound=BaseModel)

# A prompt run writes a whole script on the host; the agent itself stops it at 900 s.
RUN_TIMEOUT_SECONDS = 960.0
# How long the agent may hold a run while every account with room runs another prompt.
RUN_QUEUE_SECONDS = 60.0


class AgentRunResult(BaseModel):
    """One prompt the agent ran on a signed-in Claude Code account (ai_accounts_agent.runs)."""

    text: str
    slot: str
    model: str
    input_tokens: int
    output_tokens: int
    duration_ms: int


class AiAccountsAgentClient:
    """Signed requests to the host agent, in the same scheme as the deployment agent."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def _headers(self, method: str, path: str, body: bytes) -> dict[str, str]:
        key = self.settings.ai_accounts_agent_hmac_key
        if not key:
            raise AppError(503, "ai_accounts_agent_unavailable", "AI 帳號代理尚未完成設定")
        timestamp = str(int(time.time()))
        nonce = uuid4().hex
        digest = hashlib.sha256(body).hexdigest()
        message = f"{timestamp}\n{nonce}\n{method.upper()}\n{path}\n{digest}".encode()
        return {
            "Content-Type": "application/json",
            "X-Agent-Timestamp": timestamp,
            "X-Agent-Nonce": nonce,
            "X-Agent-Signature": hmac.new(key.encode(), message, hashlib.sha256).hexdigest(),
        }

    def _transport(self) -> httpx.AsyncBaseTransport:
        return httpx.AsyncHTTPTransport(uds=self.settings.ai_accounts_agent_socket)

    async def _request(
        self,
        method: str,
        path: str,
        model: type[T],
        payload: dict[str, Any] | None = None,
        read_timeout: float | None = None,
    ) -> T:
        body = json.dumps(payload, separators=(",", ":")).encode() if payload is not None else b""
        transport = self._transport()
        try:
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://ai-accounts",
                timeout=read_timeout or self.settings.ai_accounts_agent_timeout_seconds,
            ) as client:
                response = await client.request(
                    method, path, content=body or None, headers=self._headers(method, path, body)
                )
        except (httpx.HTTPError, OSError) as exc:
            raise AppError(
                503,
                "ai_accounts_agent_unavailable",
                "AI 帳號代理目前無法連線，請檢查主機服務 mokaair-ai-accounts",
            ) from exc
        if response.status_code >= 400:
            try:
                problem: dict[str, Any] = response.json()
            except ValueError:
                problem = {}
            code = str(problem.get("code") or "ai_accounts_agent_error")[:64]
            detail = str(problem.get("detail") or "AI 帳號代理拒絕這次操作")[:500]
            raise AppError(response.status_code, code, detail)
        try:
            return model.model_validate(response.json())
        except ValueError as exc:
            raise AppError(
                502, "ai_accounts_agent_invalid_response", "AI 帳號代理回應格式不正確"
            ) from exc

    async def overview(self, *, fresh: bool = False) -> AgentOverview:
        path = "/v1/accounts?fresh=1" if fresh else "/v1/accounts"
        return await self._request("GET", path, AgentOverview)

    async def start_login(self, tool: Tool, slot: Slot) -> AiLoginSession:
        return await self._request("POST", f"/v1/accounts/{tool}/{slot}/login", AiLoginSession)

    async def login(self, login_id: str) -> AiLoginSession:
        return await self._request("GET", f"/v1/logins/{login_id}", AiLoginSession)

    async def submit_code(self, login_id: str, code: str) -> AiLoginSession:
        return await self._request(
            "POST", f"/v1/logins/{login_id}/code", AiLoginSession, {"code": code}
        )

    async def cancel_login(self, login_id: str) -> AiLoginSession:
        return await self._request("POST", f"/v1/logins/{login_id}/cancel", AiLoginSession)

    async def logout(self, tool: Tool, slot: Slot) -> AiLogoutResult:
        return await self._request("POST", f"/v1/accounts/{tool}/{slot}/logout", AiLogoutResult)

    async def set_default(self, tool: Tool, slot: Slot) -> AiDefaults:
        return await self._request("PUT", f"/v1/defaults/{tool}", AiDefaults, {"slot": slot})

    async def run_prompt(
        self,
        *,
        model: str,
        system: str,
        prompt: str,
        max_usage_percent: int,
        timeout_seconds: float = RUN_TIMEOUT_SECONDS - 60,
        queue_seconds: float = RUN_QUEUE_SECONDS,
    ) -> AgentRunResult:
        """One prompt on the Claude account with the most room; the agent turns every tool off.

        Refusals come back as AppError with the agent's code: ``subscription_quota_paused``
        (429, with the reset time in the detail), ``subscription_busy`` (503, every account with
        room stayed busy for ``queue_seconds``), ``subscription_not_signed_in`` (409),
        ``subscription_run_failed`` (502).
        """
        payload = {
            "tool": "claude",
            "model": model,
            "system": system,
            "prompt": prompt,
            "max_usage_percent": max_usage_percent,
            "timeout_seconds": timeout_seconds,
            "queue_seconds": queue_seconds,
        }
        return await self._request(
            "POST",
            "/v1/runs",
            AgentRunResult,
            payload,
            read_timeout=timeout_seconds + queue_seconds + 60,
        )
