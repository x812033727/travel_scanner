"""The two Azure Speech REST calls this server makes: synthesize, and list voices.

Real-time synthesis returns audio only, up to ten minutes per request. The pipeline asks for
48 kHz 16-bit mono PCM because its timeline is built on 1,600 samples a frame and it measures
each clip by its byte count. Listing voices costs no characters, which makes it the
connection test.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

OUTPUT_FORMAT = "riff-48khz-16bit-mono-pcm"
USER_AGENT = "Mokaair-video/1.0 (https://mokaair.com; support@mokaair.com)"


class SpeechUpstreamError(Exception):
    """Azure answered with something other than audio."""

    def __init__(self, status: int, message: str, retry_after: str | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.retry_after = retry_after


@dataclass(frozen=True)
class AzureSpeech:
    region: str
    key: str
    timeout_seconds: float

    @property
    def host(self) -> str:
        # ``region`` is pattern-checked in Settings, so this cannot point anywhere else.
        return f"https://{self.region}.tts.speech.microsoft.com"

    def _headers(self) -> dict[str, str]:
        return {"Ocp-Apim-Subscription-Key": self.key, "User-Agent": USER_AGENT}

    async def synthesize(self, ssml: str, client: httpx.AsyncClient | None = None) -> bytes:
        owned = client is None
        http = client or httpx.AsyncClient(timeout=self.timeout_seconds, trust_env=False)
        try:
            response = await http.post(
                f"{self.host}/cognitiveservices/v1",
                content=ssml.encode("utf-8"),
                headers={
                    **self._headers(),
                    "Content-Type": "application/ssml+xml",
                    "X-Microsoft-OutputFormat": OUTPUT_FORMAT,
                },
            )
        except httpx.HTTPError as error:
            raise SpeechUpstreamError(
                502, f"Azure Speech unreachable: {type(error).__name__}"
            ) from error
        finally:
            if owned:
                await http.aclose()
        if response.status_code != 200 or not response.content.startswith(b"RIFF"):
            raise SpeechUpstreamError(
                response.status_code,
                f"Azure Speech answered HTTP {response.status_code}",
                response.headers.get("Retry-After"),
            )
        return response.content

    async def voices(self, client: httpx.AsyncClient | None = None) -> list[dict[str, Any]]:
        owned = client is None
        http = client or httpx.AsyncClient(timeout=min(self.timeout_seconds, 15.0), trust_env=False)
        try:
            response = await http.get(
                f"{self.host}/cognitiveservices/voices/list", headers=self._headers()
            )
        except httpx.HTTPError as error:
            raise SpeechUpstreamError(
                502, f"Azure Speech unreachable: {type(error).__name__}"
            ) from error
        finally:
            if owned:
                await http.aclose()
        if response.status_code != 200:
            raise SpeechUpstreamError(
                response.status_code, f"Azure Speech answered HTTP {response.status_code}"
            )
        payload = response.json()
        return payload if isinstance(payload, list) else []
