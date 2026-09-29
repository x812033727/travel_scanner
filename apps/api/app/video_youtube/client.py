"""Google's OAuth endpoints and the YouTube Data API calls the site makes, and nothing else.

Every call takes the ``httpx.AsyncClient`` it runs on, so tests hand in a ``MockTransport`` and
production one client per job. The quota each call costs is from the reference pages read on
2026-09-27 (docs/videos/YOUTUBE-API-AUDIT.md lists them): channels.list, videos.list and
playlistItems.list 1, videos.update 50, captions.list 50, captions.insert 400, thumbnails.set
50, and videos.insert one call from its own bucket of 100 a day.
"""

from __future__ import annotations

import json
import secrets
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Literal, cast

import httpx

AUTHORIZE = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN = "https://oauth2.googleapis.com/token"  # noqa: S105 -- endpoint URL, not a secret
REVOKE = "https://oauth2.googleapis.com/revoke"
API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"
# The one scope the site asks for: videos.update, captions and thumbnails all accept it, and
# captions accept nothing narrower (docs/videos/HANDS-OFF.md §YouTube API).
SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
TIMEOUT = httpx.Timeout(30.0, connect=10.0)
# One chunk of the mp4 can take a while on the host's uplink.
UPLOAD_TIMEOUT = httpx.Timeout(300.0, connect=10.0)


class YoutubeError(Exception):
    """Google refused a call. ``reason`` is the API's own reason code (quotaExceeded,
    invalidPublishAt, captionExists, forbidden...) or the OAuth error (invalid_grant)."""

    def __init__(self, status: int, reason: str, message: str) -> None:
        super().__init__(f"{status} {reason}: {message}")
        self.status = status
        self.reason = reason
        self.message = message


class AuthorizationLost(YoutubeError):
    """The refresh token no longer works: the owner revoked it, or Google expired it."""


class UploadInterrupted(Exception):
    """A chunk did not arrive (a network error or a 5xx); the session can be asked where it is."""


def error_from(response: httpx.Response) -> YoutubeError:
    """The refusal in a Google error body, which comes in two shapes.

    The Data API answers ``{"error": {"code", "message", "errors": [{"reason", "message"}]}}``;
    the OAuth endpoints answer ``{"error": "invalid_grant", "error_description": "..."}``.
    """
    try:
        body = response.json()
    except ValueError:
        body = {}
    error = body.get("error") if isinstance(body, dict) else None
    if isinstance(error, dict):
        details = error.get("errors")
        first = details[0] if isinstance(details, list) and details else {}
        reason = str(first.get("reason") or error.get("status") or "error")
        message = str(error.get("message") or first.get("message") or response.reason_phrase)
        return YoutubeError(response.status_code, reason, message)
    if isinstance(error, str):
        message = str(body.get("error_description") or error)
        kind = (
            AuthorizationLost if error in ("invalid_grant", "unauthorized_client") else YoutubeError
        )
        return kind(response.status_code, error, message)
    return YoutubeError(response.status_code, "error", response.text[:300] or "no body")


def _json(response: httpx.Response) -> dict[str, Any]:
    if response.is_error:
        raise error_from(response)
    try:
        body = response.json()
    except ValueError as exc:
        raise YoutubeError(response.status_code, "invalid_json", response.text[:300]) from exc
    return cast(dict[str, Any], body) if isinstance(body, dict) else {}


# --- OAuth ---------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Grant:
    access_token: str
    refresh_token: str | None
    scope: str


async def exchange_code(
    http: httpx.AsyncClient,
    *,
    client_id: str,
    client_secret: str,
    code: str,
    verifier: str,
    redirect_uri: str,
) -> Grant:
    body = _json(
        await http.post(
            TOKEN,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "client_secret": client_secret,
                "code_verifier": verifier,
            },
            timeout=TIMEOUT,
        )
    )
    token = body.get("access_token")
    if not isinstance(token, str) or not token:
        raise YoutubeError(502, "no_access_token", "Google answered without an access token")
    refresh = body.get("refresh_token")
    return Grant(
        access_token=token,
        refresh_token=refresh if isinstance(refresh, str) and refresh else None,
        scope=str(body.get("scope") or ""),
    )


async def refresh_access_token(
    http: httpx.AsyncClient, *, client_id: str, client_secret: str, refresh_token: str
) -> str:
    body = _json(
        await http.post(
            TOKEN,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret,
            },
            timeout=TIMEOUT,
        )
    )
    token = body.get("access_token")
    if not isinstance(token, str) or not token:
        raise YoutubeError(502, "no_access_token", "Google answered without an access token")
    return token


async def revoke_token(http: httpx.AsyncClient, token: str) -> bool:
    """Ask Google to forget the grant; False when it could not be reached or said no."""
    try:
        response = await http.post(REVOKE, data={"token": token}, timeout=TIMEOUT)
    except httpx.HTTPError:
        return False
    # 400 invalid_token: already revoked, which is the state asked for.
    return response.status_code == 200 or (
        response.status_code == 400 and "invalid_token" in response.text
    )


# --- the Data API --------------------------------------------------------------------------------


@dataclass(frozen=True)
class UploadState:
    """Where a resumable upload stands: finished with the video, at a byte offset, or gone."""

    kind: Literal["done", "partial", "gone"]
    offset: int = 0
    video: dict[str, Any] | None = None


class YoutubeClient:
    def __init__(self, http: httpx.AsyncClient, access_token: str) -> None:
        self.http = http
        self.headers = {"Authorization": f"Bearer {access_token}"}

    async def my_channel(self) -> dict[str, Any] | None:
        """channels.list mine=true (1 unit): the channel the grant speaks for, or None."""
        body = _json(
            await self.http.get(
                f"{API}/channels",
                params={"part": "snippet", "mine": "true"},
                headers=self.headers,
                timeout=TIMEOUT,
            )
        )
        items = body.get("items")
        return cast(dict[str, Any], items[0]) if isinstance(items, list) and items else None

    async def video(self, video_id: str) -> dict[str, Any] | None:
        """videos.list (1 unit) with the parts videos.update rewrites, or None when not found."""
        body = _json(
            await self.http.get(
                f"{API}/videos",
                params={"part": "snippet,status,localizations", "id": video_id},
                headers=self.headers,
                timeout=TIMEOUT,
            )
        )
        items = body.get("items")
        return cast(dict[str, Any], items[0]) if isinstance(items, list) and items else None

    async def uploads_playlist(self) -> str | None:
        """channels.list mine=true (1 unit): the playlist that holds everything the channel
        uploaded, or None when the grant speaks for no channel."""
        body = _json(
            await self.http.get(
                f"{API}/channels",
                params={"part": "contentDetails", "mine": "true"},
                headers=self.headers,
                timeout=TIMEOUT,
            )
        )
        items = body.get("items")
        if not isinstance(items, list) or not items or not isinstance(items[0], dict):
            return None
        details = items[0].get("contentDetails")
        related = details.get("relatedPlaylists") if isinstance(details, dict) else None
        uploads = related.get("uploads") if isinstance(related, dict) else None
        return uploads if isinstance(uploads, str) and uploads else None

    async def playlist_videos(self, playlist_id: str, *, limit: int = 50) -> list[str]:
        """playlistItems.list (1 unit): the ids of a playlist's newest videos, newest first."""
        body = _json(
            await self.http.get(
                f"{API}/playlistItems",
                params={
                    "part": "contentDetails",
                    "playlistId": playlist_id,
                    "maxResults": str(max(1, min(limit, 50))),
                },
                headers=self.headers,
                timeout=TIMEOUT,
            )
        )
        items = body.get("items")
        found: list[str] = []
        for item in items if isinstance(items, list) else []:
            details = item.get("contentDetails") if isinstance(item, dict) else None
            video_id = details.get("videoId") if isinstance(details, dict) else None
            if isinstance(video_id, str) and video_id:
                found.append(video_id)
        return found

    async def videos(self, video_ids: Sequence[str], *, parts: str) -> list[dict[str, Any]]:
        """videos.list (1 unit) for up to fifty ids at once; a video that is gone, or that the
        grant may not see, is simply not in the answer."""
        if not video_ids:
            return []
        if len(video_ids) > 50:
            raise ValueError("videos.list takes at most fifty ids")
        body = _json(
            await self.http.get(
                f"{API}/videos",
                params={"part": parts, "id": ",".join(video_ids), "maxResults": "50"},
                headers=self.headers,
                timeout=TIMEOUT,
            )
        )
        items = body.get("items")
        return [item for item in items if isinstance(item, dict)] if isinstance(items, list) else []

    async def update_video(self, body: dict[str, Any]) -> dict[str, Any]:
        """videos.update (50 units); ``body`` carries every property the parts should keep."""
        return _json(
            await self.http.put(
                f"{API}/videos",
                params={"part": "snippet,status,localizations"},
                json=body,
                headers=self.headers,
                timeout=TIMEOUT,
            )
        )

    async def captions(self, video_id: str) -> list[dict[str, Any]]:
        """captions.list (50 units): the tracks the video has, uploaded or automatic."""
        body = _json(
            await self.http.get(
                f"{API}/captions",
                params={"part": "snippet", "videoId": video_id},
                headers=self.headers,
                timeout=TIMEOUT,
            )
        )
        items = body.get("items")
        return [item for item in items if isinstance(item, dict)] if isinstance(items, list) else []

    async def insert_caption(
        self, video_id: str, *, language: str, name: str, data: bytes
    ) -> dict[str, Any]:
        """captions.insert (400 units), as a multipart upload of the snippet and the file."""
        boundary = f"mokaair-{secrets.token_hex(12)}"
        snippet = json.dumps(
            {
                "snippet": {
                    "videoId": video_id,
                    "language": language,
                    "name": name,
                    "isDraft": False,
                }
            },
            ensure_ascii=False,
        ).encode()
        content = b"".join(
            [
                f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n".encode(),
                snippet,
                f"\r\n--{boundary}\r\nContent-Type: application/octet-stream\r\n\r\n".encode(),
                data,
                f"\r\n--{boundary}--\r\n".encode(),
            ]
        )
        return _json(
            await self.http.post(
                f"{UPLOAD}/captions",
                params={"part": "snippet", "uploadType": "multipart"},
                content=content,
                headers={
                    **self.headers,
                    "Content-Type": f"multipart/related; boundary={boundary}",
                },
                timeout=TIMEOUT,
            )
        )

    async def set_thumbnail(self, video_id: str, data: bytes, content_type: str) -> dict[str, Any]:
        """thumbnails.set (50 units)."""
        return _json(
            await self.http.post(
                f"{UPLOAD}/thumbnails/set",
                params={"videoId": video_id, "uploadType": "media"},
                content=data,
                headers={**self.headers, "Content-Type": content_type},
                timeout=TIMEOUT,
            )
        )

    async def start_upload(self, body: dict[str, Any], *, size: int, content_type: str) -> str:
        """Open a resumable videos.insert session; returns the session URI to PUT the file to."""
        response = await self.http.post(
            f"{UPLOAD}/videos",
            params={"uploadType": "resumable", "part": "snippet,status"},
            json=body,
            headers={
                **self.headers,
                "X-Upload-Content-Length": str(size),
                "X-Upload-Content-Type": content_type,
            },
            timeout=TIMEOUT,
        )
        if response.is_error:
            raise error_from(response)
        location = str(response.headers.get("location") or "")
        if not location or not location.startswith(f"{UPLOAD}/videos"):
            raise YoutubeError(
                response.status_code, "no_upload_session", "no session URI in the answer"
            )
        return location

    def _state(self, response: httpx.Response) -> UploadState:
        if response.status_code in (200, 201):
            return UploadState("done", video=_json(response))
        if response.status_code == 308:
            # "Range: bytes=0-N" names the last byte YouTube kept; no header means none yet.
            received = response.headers.get("range", "")
            last = received.rpartition("-")[2]
            return UploadState("partial", offset=int(last) + 1 if last.isdigit() else 0)
        if response.status_code in (404, 410):
            return UploadState("gone")
        if response.status_code >= 500:
            raise UploadInterrupted(f"{response.status_code} from the upload session")
        raise error_from(response)

    async def upload_status(self, session_uri: str, *, size: int) -> UploadState:
        """Ask the session how much of the file it has (a PUT with an empty body)."""
        try:
            response = await self.http.put(
                session_uri,
                content=b"",
                headers={**self.headers, "Content-Range": f"bytes */{size}"},
                timeout=TIMEOUT,
            )
        except httpx.HTTPError as exc:
            raise UploadInterrupted(str(exc)) from exc
        return self._state(response)

    async def upload_chunk(
        self, session_uri: str, *, offset: int, data: bytes, size: int, content_type: str
    ) -> UploadState:
        end = offset + len(data) - 1
        try:
            response = await self.http.put(
                session_uri,
                content=data,
                headers={
                    **self.headers,
                    "Content-Type": content_type,
                    "Content-Range": f"bytes {offset}-{end}/{size}",
                },
                timeout=UPLOAD_TIMEOUT,
            )
        except httpx.HTTPError as exc:
            raise UploadInterrupted(str(exc)) from exc
        return self._state(response)
