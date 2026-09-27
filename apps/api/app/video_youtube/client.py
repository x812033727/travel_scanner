"""The few YouTube Data API calls the site makes, on an access token it was given.

Every method raises YouTubeError with YouTube's own message when the call is refused, so the
sync records exactly what YouTube said next to the step that failed.
"""

from __future__ import annotations

from typing import Any

import httpx

from app.video_youtube.sync import caption_metadata, multipart_related

API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"
TIMEOUT_SECONDS = 60.0


class YouTubeError(Exception):
    def __init__(self, status: int, detail: str) -> None:
        super().__init__(f"{status}: {detail}")
        self.status = status
        self.detail = detail


def _detail(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return response.text[:300] or f"HTTP {response.status_code}"
    error = body.get("error") if isinstance(body, dict) else None
    if isinstance(error, dict):
        reasons = error.get("errors")
        reason = reasons[0].get("reason") if isinstance(reasons, list) and reasons else None
        message = str(error.get("message") or f"HTTP {response.status_code}")
        return f"{message}（{reason}）" if reason else message
    if isinstance(error, str):
        return error
    return f"HTTP {response.status_code}"


class YouTubeClient:
    def __init__(self, http: httpx.AsyncClient, access_token: str) -> None:
        self.http = http
        self.headers = {"Authorization": f"Bearer {access_token}"}

    async def _json(self, response: httpx.Response) -> dict[str, Any]:
        if response.status_code >= 400:
            raise YouTubeError(response.status_code, _detail(response))
        body = response.json()
        return body if isinstance(body, dict) else {}

    async def video(self, video_id: str) -> dict[str, Any] | None:
        """The video's snippet, status and localizations as YouTube holds them, or None when
        the channel has no such video (a wrong id, or another channel's)."""
        response = await self.http.get(
            f"{API}/videos",
            params={"part": "snippet,status,localizations", "id": video_id},
            headers=self.headers,
        )
        body = await self._json(response)
        items = body.get("items")
        return items[0] if isinstance(items, list) and items else None

    async def update_video(self, body: dict[str, Any]) -> dict[str, Any]:
        response = await self.http.put(
            f"{API}/videos",
            params={"part": "snippet,status,localizations"},
            headers=self.headers,
            json=body,
        )
        return await self._json(response)

    async def captions(self, video_id: str) -> list[dict[str, Any]]:
        response = await self.http.get(
            f"{API}/captions", params={"part": "snippet", "videoId": video_id}, headers=self.headers
        )
        body = await self._json(response)
        items = body.get("items")
        return items if isinstance(items, list) else []

    async def insert_caption(self, video_id: str, locale: str, srt: bytes) -> dict[str, Any]:
        body, boundary = multipart_related(caption_metadata(video_id, locale), srt, "text/plain")
        response = await self.http.post(
            f"{UPLOAD}/captions",
            params={"part": "snippet", "uploadType": "multipart"},
            headers={
                **self.headers,
                "Content-Type": f"multipart/related; boundary={boundary}",
            },
            content=body,
        )
        return await self._json(response)

    async def set_thumbnail(self, video_id: str, jpeg: bytes) -> dict[str, Any]:
        response = await self.http.post(
            f"{UPLOAD}/thumbnails/set",
            params={"videoId": video_id, "uploadType": "media"},
            headers={**self.headers, "Content-Type": "image/jpeg"},
            content=jpeg,
        )
        return await self._json(response)
