"""Lyria (Gemini API) through generateContent: a description in, one instrumental track out.

Synchronous like the image models: the audio comes back inline. The request shape follows the
Gemini API music docs as read on 2026-09-26 (re-check on first use); the track's length is
asked for in the prompt, and the mix stage loops or trims it to the video.
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
    gemini_refusal,
    inline_part,
    post_json,
)

AUDIO_TYPES = {
    "audio/mpeg": "audio/mpeg",
    "audio/mp3": "audio/mpeg",
    "audio/wav": "audio/wav",
    "audio/x-wav": "audio/wav",
}


@dataclass(frozen=True)
class GeminiMusic:
    base_url: str
    key: str
    name: str = "gemini"

    def request_body(self, request: MediaRequest) -> dict[str, Any]:
        text = (
            f"{request.prompt}\n\nInstrumental only, no vocals, no lyrics. "
            f"About {request.seconds} seconds long, with a clear beginning and a soft ending."
        )
        return {
            "contents": [{"role": "user", "parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"]},
        }

    async def submit(self, request: MediaRequest, client: httpx.AsyncClient) -> Submitted:
        url = f"{self.base_url.rstrip('/')}/v1beta/models/{request.model}:generateContent"
        payload = await post_json(
            client, url, self.request_body(request), {"x-goog-api-key": self.key}, "Gemini"
        )
        found = inline_part(payload)
        if found is None:
            reason = gemini_refusal(payload) or "no audio in the answer"
            raise MediaUpstreamError(422, f"Lyria returned no audio ({reason})", "blocked")
        data, mime = found
        return Submitted(inline=data, content_type=AUDIO_TYPES.get(mime, mime or None))

    async def poll(self, vendor_ref: str, client: httpx.AsyncClient) -> Polled:
        raise MediaUpstreamError(502, "Lyria is synchronous; nothing to poll", "invalid")

    def fetch(self, download: Download) -> tuple[str, dict[str, str]]:
        raise MediaUpstreamError(502, "Lyria audio arrives inline; nothing to fetch", "invalid")
