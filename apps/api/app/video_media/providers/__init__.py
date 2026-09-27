"""The vendors the media stages talk to, behind one small protocol.

A provider ``submit``s a request and answers with the bytes (a synchronous image model), a
download to fetch, or a vendor reference to ``poll``; a poll says running, done (with the
download) or failed; ``fetch`` turns a download into the URL and headers the store streams
from. Every adapter reads its key from the site's settings and only ever sends it to the
host its base URL is pinned to (``OFFICIAL_PROVIDER_HOSTS`` in app.config).
"""

from __future__ import annotations

import base64
import ipaddress
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol
from urllib.parse import urlsplit

import httpx

USER_AGENT = "Mokaair-video/1.0 (https://mokaair.com; support@mokaair.com)"
ErrorKind = Literal["blocked", "busy", "key", "expired", "failed", "invalid"]


@dataclass(frozen=True)
class ReferenceImage:
    role: str
    content_type: str
    data: bytes


@dataclass(frozen=True)
class MediaRequest:
    kind: Literal["image", "clip", "music"]
    model: str
    prompt: str
    negative_prompt: str | None = None
    aspect: str = "16:9"
    seconds: int = 0
    resolution: str | None = None
    native_audio: bool = False
    seed: int | None = None
    first_frame: ReferenceImage | None = None
    last_frame: ReferenceImage | None = None
    references: tuple[ReferenceImage, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Download:
    url: str
    needs_key: bool = False
    content_type_hint: str | None = None


@dataclass(frozen=True)
class Submitted:
    vendor_ref: str | None = None
    download: Download | None = None
    inline: bytes | None = None
    content_type: str | None = None


@dataclass(frozen=True)
class Polled:
    state: Literal["running", "done", "failed"]
    download: Download | None = None
    retry_after: int = 10
    reason: str | None = None


class MediaUpstreamError(Exception):
    """The vendor refused or failed; ``kind`` says who can fix it."""

    def __init__(
        self, status: int, message: str, kind: ErrorKind = "failed", retry_after: str | None = None
    ) -> None:
        super().__init__(message)
        self.status = status
        self.message = message
        self.kind = kind
        self.retry_after = retry_after


class MediaProvider(Protocol):
    @property
    def name(self) -> str: ...

    async def submit(self, request: MediaRequest, client: httpx.AsyncClient) -> Submitted: ...

    async def poll(self, vendor_ref: str, client: httpx.AsyncClient) -> Polled: ...

    def fetch(self, download: Download) -> tuple[str, dict[str, str]]: ...


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def data_url(image: ReferenceImage) -> str:
    return f"data:{image.content_type};base64,{b64(image.data)}"


def public_https_host(url: str) -> str | None:
    """The host of an https URL that is a real name (no IP literal, no localhost), else None."""
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    if parts.scheme != "https" or not host or host == "localhost" or host.endswith(".localhost"):
        return None
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return host
    return None


def check_download(download: Download, allowed_hosts: frozenset[str] | None = None) -> str:
    """The download's URL once it is https on a public host (and on an allowed one when given)."""
    host = public_https_host(download.url)
    if host is None:
        raise MediaUpstreamError(
            502, "the vendor's download URL is not an https address", "invalid"
        )
    if allowed_hosts is not None and host not in allowed_hosts:
        raise MediaUpstreamError(
            502, f"the download is on {host}, not on the vendor's host", "invalid"
        )
    return download.url


def raise_for_status(response: httpx.Response, vendor: str) -> None:
    """Map a vendor's HTTP status to who can fix it; 2xx passes."""
    status = response.status_code
    if 200 <= status < 300:
        return
    retry = response.headers.get("Retry-After")
    if status == 429:
        raise MediaUpstreamError(429, f"{vendor} is busy or over quota", "busy", retry)
    if status in (401, 403):
        raise MediaUpstreamError(502, f"{vendor} rejected the site's key", "key")
    if status == 404:
        raise MediaUpstreamError(422, f"{vendor} does not know this model or operation", "invalid")
    if status == 400:
        raise MediaUpstreamError(422, f"{vendor} refused the request", "blocked")
    if status >= 500:
        raise MediaUpstreamError(502, f"{vendor} answered HTTP {status}", "failed", retry)
    raise MediaUpstreamError(502, f"{vendor} answered HTTP {status}", "failed")


async def post_json(
    client: httpx.AsyncClient, url: str, body: dict[str, Any], headers: dict[str, str], vendor: str
) -> dict[str, Any]:
    try:
        response = await client.post(url, json=body, headers={**headers, "User-Agent": USER_AGENT})
    except httpx.HTTPError as error:
        raise MediaUpstreamError(
            502, f"{vendor} unreachable: {type(error).__name__}", "failed"
        ) from error
    raise_for_status(response, vendor)
    payload = response.json()
    return payload if isinstance(payload, dict) else {}


async def get_json(
    client: httpx.AsyncClient, url: str, headers: dict[str, str], vendor: str
) -> dict[str, Any]:
    try:
        response = await client.get(url, headers={**headers, "User-Agent": USER_AGENT})
    except httpx.HTTPError as error:
        raise MediaUpstreamError(
            502, f"{vendor} unreachable: {type(error).__name__}", "failed"
        ) from error
    raise_for_status(response, vendor)
    payload = response.json()
    return payload if isinstance(payload, dict) else {}


def inline_part(payload: dict[str, Any]) -> tuple[bytes, str] | None:
    """The first inline media part of a generateContent answer: (bytes, mime type)."""
    for candidate in payload.get("candidates") or []:
        for part in (candidate.get("content") or {}).get("parts") or []:
            inline = part.get("inlineData") or part.get("inline_data") or {}
            data = inline.get("data")
            if data:
                mime = str(inline.get("mimeType") or inline.get("mime_type") or "")
                return base64.b64decode(data), mime.split(";")[0].strip().lower()
    return None


def gemini_refusal(payload: dict[str, Any]) -> str | None:
    feedback = payload.get("promptFeedback")
    if isinstance(feedback, dict) and feedback.get("blockReason"):
        return str(feedback["blockReason"])
    for candidate in payload.get("candidates") or []:
        reason = candidate.get("finishReason")
        if reason not in (None, "STOP"):
            return str(reason)
    return None
