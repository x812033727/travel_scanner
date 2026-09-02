from __future__ import annotations

import base64
import hashlib
import hmac
from typing import Any
from uuid import UUID

import httpx

from app.config import Settings


class LineApiError(ConnectionError):
    def __init__(self, detail: str, *, status_code: int | None = None) -> None:
        super().__init__(detail)
        self.status_code = status_code

    @property
    def retryable(self) -> bool:
        return self.status_code is None or self.status_code == 429 or self.status_code >= 500


def verify_webhook_signature(body: bytes, signature: str, channel_secret: str) -> bool:
    digest = hmac.new(channel_secret.encode("utf-8"), body, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode("ascii")
    return hmac.compare_digest(expected, signature)


class LineMessagingClient:
    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None) -> None:
        self.settings = settings
        self._client = client

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        retry_key: UUID | None = None,
    ) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.settings.line_channel_access_token or ''}",
            "Content-Type": "application/json",
        }
        if retry_key is not None:
            headers["X-Line-Retry-Key"] = str(retry_key)
        owns_client = self._client is None
        client = self._client or httpx.AsyncClient(timeout=10)
        try:
            response = await client.request(
                method,
                f"{self.settings.line_api_base_url.rstrip('/')}{path}",
                headers=headers,
                json=json,
            )
        except httpx.HTTPError as exc:
            raise LineApiError("LINE API 暫時無法連線") from exc
        finally:
            if owns_client:
                await client.aclose()
        if response.status_code >= 400:
            raise LineApiError(
                f"LINE API 回應 {response.status_code}", status_code=response.status_code
            )
        if not response.content:
            return {}
        payload = response.json()
        return payload if isinstance(payload, dict) else {}

    async def issue_link_token(self, line_user_id: str) -> str:
        payload = await self._request("POST", f"/v2/bot/user/{line_user_id}/linkToken")
        token = payload.get("linkToken")
        if not isinstance(token, str) or not token:
            raise LineApiError("LINE 未回傳帳號連結權杖")
        return token

    async def profile(self, line_user_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/v2/bot/profile/{line_user_id}")

    async def reply_text(self, reply_token: str, text: str) -> None:
        await self._request(
            "POST",
            "/v2/bot/message/reply",
            json={"replyToken": reply_token, "messages": [{"type": "text", "text": text}]},
        )

    async def reply_link(self, reply_token: str, link_url: str) -> None:
        await self._request(
            "POST",
            "/v2/bot/message/reply",
            json={
                "replyToken": reply_token,
                "messages": [
                    {
                        "type": "template",
                        "altText": "連結 Mokaair 帳號",
                        "template": {
                            "type": "buttons",
                            "text": "登入 Mokaair，將價格通知安全連結到這個 LINE 帳號。",
                            "actions": [
                                {"type": "uri", "label": "連結帳號", "uri": link_url}
                            ],
                        },
                    }
                ],
            },
        )

    async def push_messages(
        self, line_user_id: str, messages: list[dict[str, Any]], *, retry_key: UUID
    ) -> None:
        await self._request(
            "POST",
            "/v2/bot/message/push",
            json={"to": line_user_id, "messages": messages},
            retry_key=retry_key,
        )

    async def push_text(self, line_user_id: str, text: str, *, retry_key: UUID) -> None:
        await self.push_messages(
            line_user_id,
            [{"type": "text", "text": text}],
            retry_key=retry_key,
        )
