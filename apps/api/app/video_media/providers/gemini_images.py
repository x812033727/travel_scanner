"""Gemini image models (Nano Banana family) through generateContent: prompt in, one image out.

Reference images (character sheets, style frames) ride along as inline parts, which is how
these models keep a character consistent across shots. Synchronous: the image comes back in
the same answer, so ``submit`` returns the bytes and there is nothing to poll.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from app.video_media.providers import (
    Download,
    MediaRequest,
    MediaUpstreamError,
    Polled,
    Submitted,
    b64,
    gemini_refusal,
    inline_part,
    post_json,
)


@dataclass(frozen=True)
class GeminiImages:
    base_url: str
    key: str
    name: str = "gemini"

    def request_body(self, request: MediaRequest) -> dict[str, Any]:
        text = request.prompt
        if request.negative_prompt:
            text += f"\n\nAvoid: {request.negative_prompt}"
        if request.references:
            text += "\n\nKeep every character exactly as in the reference images."
        parts: list[dict[str, Any]] = [{"text": text}]
        for image in request.references:
            parts.append(
                {"inline_data": {"mime_type": image.content_type, "data": b64(image.data)}}
            )
        return {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {"aspectRatio": request.aspect},
            },
        }

    async def submit(self, request: MediaRequest, client: httpx.AsyncClient) -> Submitted:
        # ``base_url`` is pinned to the official host in Settings.
        url = f"{self.base_url.rstrip('/')}/v1beta/models/{request.model}:generateContent"
        payload = await post_json(
            client, url, self.request_body(request), {"x-goog-api-key": self.key}, "Gemini"
        )
        found = inline_part(payload)
        if found is None:
            reason = gemini_refusal(payload) or "no image in the answer"
            raise MediaUpstreamError(422, f"Gemini returned no image ({reason})", "blocked")
        data, mime = found
        return Submitted(inline=data, content_type=mime or None)

    async def poll(self, vendor_ref: str, client: httpx.AsyncClient) -> Polled:
        raise MediaUpstreamError(502, "Gemini images are synchronous; nothing to poll", "invalid")

    def fetch(self, download: Download) -> tuple[str, dict[str, str]]:
        raise MediaUpstreamError(502, "Gemini images arrive inline; nothing to fetch", "invalid")
