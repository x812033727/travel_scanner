"""Gemini video models (Omni, Veo) through predictLongRunning: a start frame in, a clip out.

The call returns an operation name; polling it says when the clip is ready and where. The
result URI is on Google's own host and needs the API key to download, so ``fetch`` attaches
the key only after checking the URI really is that host: the key must never travel elsewhere.
Field names follow the Gemini API video docs as read on 2026-09-26 (re-check on first use).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

import httpx

from app.video_media.providers import (
    Download,
    MediaRequest,
    MediaUpstreamError,
    Polled,
    ReferenceImage,
    Submitted,
    b64,
    check_download,
    get_json,
    post_json,
)


def _image(image: ReferenceImage) -> dict[str, str]:
    return {"bytesBase64Encoded": b64(image.data), "mimeType": image.content_type}


@dataclass(frozen=True)
class GeminiVideo:
    base_url: str
    key: str
    name: str = "gemini"

    @property
    def host(self) -> str:
        return (urlsplit(self.base_url).hostname or "").lower()

    def request_body(self, request: MediaRequest) -> dict[str, Any]:
        if request.first_frame is None:
            raise MediaUpstreamError(422, "a clip needs its first frame", "invalid")
        instance: dict[str, Any] = {"prompt": request.prompt, "image": _image(request.first_frame)}
        if request.last_frame is not None:
            instance["lastFrame"] = _image(request.last_frame)
        if request.references:
            instance["referenceImages"] = [
                {"image": _image(image), "referenceType": "asset"} for image in request.references
            ]
        parameters: dict[str, Any] = {
            "aspectRatio": request.aspect,
            "durationSeconds": request.seconds,
            "personGeneration": "allow_adult",
            "generateAudio": request.native_audio,
        }
        if request.resolution:
            parameters["resolution"] = request.resolution
        if request.negative_prompt:
            parameters["negativePrompt"] = request.negative_prompt
        if request.seed is not None:
            parameters["seed"] = request.seed
        return {"instances": [instance], "parameters": parameters}

    async def submit(self, request: MediaRequest, client: httpx.AsyncClient) -> Submitted:
        url = f"{self.base_url.rstrip('/')}/v1beta/models/{request.model}:predictLongRunning"
        payload = await post_json(
            client, url, self.request_body(request), {"x-goog-api-key": self.key}, "Gemini"
        )
        name = payload.get("name")
        if not isinstance(name, str) or not name:
            raise MediaUpstreamError(502, "Gemini returned no operation name", "failed")
        return Submitted(vendor_ref=name)

    async def poll(self, vendor_ref: str, client: httpx.AsyncClient) -> Polled:
        url = f"{self.base_url.rstrip('/')}/v1beta/{vendor_ref}"
        payload = await get_json(client, url, {"x-goog-api-key": self.key}, "Gemini")
        if not payload.get("done"):
            return Polled("running", retry_after=10)
        error = payload.get("error")
        if isinstance(error, dict):
            return Polled(
                "failed", reason=str(error.get("message") or error.get("status") or "error")
            )
        response = payload.get("response") or {}
        generated = response.get("generateVideoResponse") or response
        samples = generated.get("generatedSamples") or generated.get("videos") or []
        if not samples:
            filtered = generated.get("raiMediaFilteredCount") or 0
            reasons = generated.get("raiMediaFilteredReasons") or []
            why = "; ".join(str(reason) for reason in reasons) if reasons else "no sample"
            return Polled("failed", reason=f"filtered ({filtered}): {why}" if filtered else why)
        first: dict[str, Any] = samples[0] if isinstance(samples[0], dict) else {}
        nested = first.get("video")
        video: dict[str, Any] = nested if isinstance(nested, dict) else first
        uri = video.get("uri") or video.get("url")
        if not isinstance(uri, str) or not uri:
            return Polled("failed", reason="the sample has no video URI")
        return Polled(
            "done", download=Download(url=uri, needs_key=True, content_type_hint="video/mp4")
        )

    def fetch(self, download: Download) -> tuple[str, dict[str, str]]:
        url = check_download(download, frozenset({self.host}))
        return url, {"x-goog-api-key": self.key}
