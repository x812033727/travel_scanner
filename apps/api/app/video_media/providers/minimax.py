"""MiniMax image-01 and the Hailuo video models.

Images are synchronous (the answer holds a download URL); video is a task to poll, whose
result is a file id exchanged for a download URL. Downloads are on MiniMax's CDN and need no
key, so ``fetch`` sends none. ``base_resp.status_code`` carries the vendor's own verdicts
(quota, balance, sensitive content) inside an HTTP 200, so every answer is checked for it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import httpx

from app.video_media.providers import (
    Download,
    MediaRequest,
    MediaUpstreamError,
    Polled,
    Submitted,
    check_download,
    data_url,
    get_json,
    post_json,
)

# MiniMax's own status codes, as documented on 2026-09-26.
BUSY = {1002, 1039}
KEY = {1004, 1008, 2049}
BLOCKED = {1026, 1027, 2013}


def check_base_resp(payload: dict[str, Any]) -> None:
    base = payload.get("base_resp")
    if not isinstance(base, dict):
        return
    code = base.get("status_code")
    if code in (None, 0):
        return
    message = str(base.get("status_msg") or code)
    if code in BUSY:
        raise MediaUpstreamError(429, f"MiniMax is busy ({message})", "busy")
    if code in KEY:
        raise MediaUpstreamError(502, f"MiniMax rejected the key or balance ({message})", "key")
    if code in BLOCKED:
        raise MediaUpstreamError(422, f"MiniMax refused the content ({message})", "blocked")
    raise MediaUpstreamError(502, f"MiniMax answered {code}: {message}", "failed")


@dataclass(frozen=True)
class MiniMaxImages:
    base_url: str
    key: str
    name: str = "minimax"

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.key}"}

    def request_body(self, request: MediaRequest) -> dict[str, Any]:
        body: dict[str, Any] = {
            "model": request.model,
            "prompt": request.prompt
            if not request.negative_prompt
            else f"{request.prompt}. Avoid: {request.negative_prompt}",
            "aspect_ratio": request.aspect,
            "response_format": "url",
            "n": 1,
            "prompt_optimizer": False,
        }
        subject = next((image for image in request.references if image.role == "character"), None)
        if subject is not None:
            body["subject_reference"] = [{"type": "character", "image_file": data_url(subject)}]
        return body

    async def submit(self, request: MediaRequest, client: httpx.AsyncClient) -> Submitted:
        url = f"{self.base_url.rstrip('/')}/image_generation"
        payload = await post_json(
            client, url, self.request_body(request), self._headers(), "MiniMax"
        )
        check_base_resp(payload)
        urls = (payload.get("data") or {}).get("image_urls") or []
        if not urls or not isinstance(urls[0], str):
            raise MediaUpstreamError(502, "MiniMax returned no image URL", "failed")
        return Submitted(download=Download(url=urls[0], content_type_hint="image/jpeg"))

    async def poll(self, vendor_ref: str, client: httpx.AsyncClient) -> Polled:
        raise MediaUpstreamError(502, "MiniMax images are synchronous; nothing to poll", "invalid")

    def fetch(self, download: Download) -> tuple[str, dict[str, str]]:
        return check_download(download), {}


@dataclass(frozen=True)
class MiniMaxVideo:
    base_url: str
    key: str
    name: str = "minimax"

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.key}"}

    def request_body(self, request: MediaRequest) -> dict[str, Any]:
        if request.first_frame is None:
            raise MediaUpstreamError(422, "a clip needs its first frame", "invalid")
        body: dict[str, Any] = {
            "model": request.model,
            "prompt": request.prompt
            if not request.negative_prompt
            else f"{request.prompt}. Avoid: {request.negative_prompt}",
            "first_frame_image": data_url(request.first_frame),
            "duration": request.seconds,
            "prompt_optimizer": False,
        }
        if request.resolution:
            body["resolution"] = request.resolution.upper()
        if request.last_frame is not None:
            body["last_frame_image"] = data_url(request.last_frame)
        characters = [image for image in request.references if image.role == "character"]
        if characters:
            body["subject_reference"] = [
                {"type": "character", "image": [data_url(image) for image in characters]}
            ]
        return body

    async def submit(self, request: MediaRequest, client: httpx.AsyncClient) -> Submitted:
        url = f"{self.base_url.rstrip('/')}/video_generation"
        payload = await post_json(
            client, url, self.request_body(request), self._headers(), "MiniMax"
        )
        check_base_resp(payload)
        task = payload.get("task_id")
        if not isinstance(task, str) or not task:
            raise MediaUpstreamError(502, "MiniMax returned no task id", "failed")
        return Submitted(vendor_ref=task)

    async def poll(self, vendor_ref: str, client: httpx.AsyncClient) -> Polled:
        base = self.base_url.rstrip("/")
        payload = await get_json(
            client,
            f"{base}/query/video_generation?task_id={quote(vendor_ref)}",
            self._headers(),
            "MiniMax",
        )
        check_base_resp(payload)
        status = str(payload.get("status") or "")
        if status in ("Preparing", "Queueing", "Processing", ""):
            return Polled("running", retry_after=15)
        if status != "Success":
            return Polled("failed", reason=f"MiniMax task {status}")
        file_id = payload.get("file_id")
        if not file_id:
            return Polled("failed", reason="MiniMax task succeeded without a file id")
        found = await get_json(
            client,
            f"{base}/files/retrieve?file_id={quote(str(file_id))}",
            self._headers(),
            "MiniMax",
        )
        check_base_resp(found)
        url = (found.get("file") or {}).get("download_url")
        if not isinstance(url, str) or not url:
            return Polled("failed", reason="MiniMax gave no download URL for the file")
        return Polled("done", download=Download(url=url, content_type_hint="video/mp4"))

    def fetch(self, download: Download) -> tuple[str, dict[str, str]]:
        return check_download(download), {}
