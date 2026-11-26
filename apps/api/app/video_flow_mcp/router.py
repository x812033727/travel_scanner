"""Paired cloud MCP proxy for `mokaair-flow` and `mokaair-flow-music`.

A paired cloud environment (Claude Cloud, Codex Cloud, Antigravity Cloud, Colab) presents
its video tool token (`Bearer mkv_...`) with `flow_access = true` to:
  - `POST /api/v1/video/mcp/flow`
  - `POST /api/v1/video/mcp/flow-music`
  - `GET  /api/v1/video/mcp/health`

Requests are validated, rate-limited, audited in `admin_audit_logs` (for `tools/call`
without recording prompts/secrets), signed with HMAC-SHA256 (`FLOW_MCP_GATEWAY_SECRET`),
and forwarded over the host loopback to `tools/video/flow-mcp/gateway.mjs`.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Annotated, Any, Literal
from uuid import uuid4

import httpx
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.db import get_session
from app.infra import enforce_named_rate_limit
from app.models import AdminAuditLog, VideoToolToken
from app.problems import AppError
from app.video_speech.admin_api import video_tool

router = APIRouter(prefix="/video/mcp", tags=["video tool"])
Session = Annotated[AsyncSession, Depends(get_session)]

McpService = Literal["flow", "flow-music"]
ALLOWED_RPC_METHODS = frozenset(
    {
        "initialize",
        "notifications/initialized",
        "ping",
        "tools/list",
        "tools/call",
        "resources/list",
        "prompts/list",
    }
)
MCP_CALLS_PER_HOUR = 300
MAX_RPC_BODY_BYTES = 1024 * 1024


def _require_flow(token: VideoToolToken) -> None:
    if not token.flow_access:
        raise AppError(
            403,
            "video_tool_token_no_flow",
            "這組影片工具權杖沒有 Flow / Flow Music MCP 權限；"
            "重新配對時加上 --flow，或在後台建立時勾選",
        )


def _gateway_target(settings: Settings) -> tuple[str, str | None]:
    socket_path = (settings.flow_mcp_gateway_socket or "").strip()
    if socket_path.startswith("/"):
        return "http://flow-gateway.local", socket_path
    return settings.flow_mcp_gateway_url.rstrip("/"), None


def _require_gateway(settings: Settings) -> tuple[str, str | None, str]:
    if not settings.flow_mcp_gateway_configured or not settings.flow_mcp_gateway_secret:
        raise AppError(
            503,
            "flow_mcp_gateway_disabled",
            "Flow MCP 雲端閘道尚未啟用或未完成設定",
        )
    base_url, socket_path = _gateway_target(settings)
    return base_url, socket_path, settings.flow_mcp_gateway_secret


def _build_gateway_client(timeout: float, socket_path: str | None) -> httpx.AsyncClient:
    if socket_path:
        return httpx.AsyncClient(
            timeout=timeout,
            transport=httpx.AsyncHTTPTransport(uds=socket_path),
        )
    return httpx.AsyncClient(timeout=timeout)


def sign_gateway_headers(
    secret: str,
    method: str,
    path: str,
    body: bytes,
    *,
    timestamp: int | None = None,
    nonce: str | None = None,
) -> dict[str, str]:
    ts = str(int(time.time()) if timestamp is None else timestamp)
    used_nonce = nonce or uuid4().hex
    digest = hashlib.sha256(body).hexdigest()
    message = f"{ts}\n{used_nonce}\n{method.upper()}\n{path}\n{digest}".encode()
    signature = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()
    return {
        "Content-Type": "application/json",
        "X-Mokaair-Timestamp": ts,
        "X-Mokaair-Nonce": used_nonce,
        "X-Mokaair-Signature": signature,
    }


@router.get("/health")
async def flow_mcp_health(
    response: Response,
    token: Annotated[VideoToolToken, Depends(video_tool)],
) -> dict[str, Any]:
    response.headers["Cache-Control"] = "no-store"
    _require_flow(token)
    settings = get_settings()
    if not settings.flow_mcp_gateway_configured or not settings.flow_mcp_gateway_secret:
        return {"ok": False, "enabled": False, "reachable": False, "services": []}

    base_url, socket_path = _gateway_target(settings)
    headers = sign_gateway_headers(settings.flow_mcp_gateway_secret, "GET", "/health", b"")
    try:
        async with _build_gateway_client(10.0, socket_path) as client:
            res = await client.get(f"{base_url}/health", headers=headers)
        if res.status_code == 200:
            data = res.json()
            return {
                "ok": bool(data.get("ok")),
                "enabled": True,
                "reachable": True,
                "services": data.get("services", []),
                "uptimeSec": data.get("uptimeSec"),
            }
        return {"ok": False, "enabled": True, "reachable": False, "status": res.status_code}
    except (httpx.HTTPError, OSError):
        return {"ok": False, "enabled": True, "reachable": False, "services": []}


@router.post("/{service}")
async def proxy_flow_mcp(
    service: McpService,
    request: Request,
    response: Response,
    session: Session,
    token: Annotated[VideoToolToken, Depends(video_tool)],
) -> Response:
    response.headers["Cache-Control"] = "no-store"
    _require_flow(token)
    settings = get_settings()
    base_url, socket_path, secret = _require_gateway(settings)

    await enforce_named_rate_limit(
        "video_flow_mcp",
        str(token.id),
        limit=MCP_CALLS_PER_HOUR,
        window_seconds=3_600,
    )

    body = await request.body()
    if len(body) > MAX_RPC_BODY_BYTES:
        raise AppError(413, "flow_mcp_body_too_large", "MCP 請求內容超過 1 MiB 上限")

    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AppError(
            400,
            "flow_mcp_invalid_json",
            "MCP 請求必須為有效的 JSON-RPC 2.0 物件",
        ) from exc

    if not isinstance(payload, dict) or payload.get("jsonrpc") != "2.0":
        raise AppError(400, "flow_mcp_invalid_jsonrpc", "MCP 請求必須符合 JSON-RPC 2.0 格式")

    method = str(payload.get("method") or "")
    if method not in ALLOWED_RPC_METHODS:
        raise AppError(400, "flow_mcp_method_not_allowed", f"不支援的 MCP 方法：{method}")

    # Audit every tool invocation without storing raw prompts or credentials.
    if method == "tools/call":
        raw_params = payload.get("params")
        params: dict[str, Any] = raw_params if isinstance(raw_params, dict) else {}
        tool_name = str(params.get("name") or "")[:80]
        session.add(
            AdminAuditLog(
                actor_user_id=token.created_by_user_id,
                action="video_flow_mcp.tool_call",
                target=f"flow-mcp:{service}",
                metadata_json={
                    "token": token.token_prefix,
                    "service": service,
                    "tool": tool_name,
                },
            )
        )
        await session.commit()

    gateway_path = f"/mcp/{service}"
    headers = sign_gateway_headers(secret, "POST", gateway_path, body)
    try:
        async with _build_gateway_client(
            settings.flow_mcp_gateway_timeout_seconds, socket_path
        ) as client:
            upstream = await client.post(
                f"{base_url}{gateway_path}",
                content=body,
                headers=headers,
            )
    except (httpx.HTTPError, OSError) as exc:
        raise AppError(
            502,
            "flow_mcp_gateway_unavailable",
            "Flow MCP 主機閘道目前無法回應，請確認主機服務 mokaair-flow-gateway 是否運行中",
        ) from exc

    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        media_type=upstream.headers.get("content-type", "application/json"),
        headers={"Cache-Control": "no-store"},
    )
