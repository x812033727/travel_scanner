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


class SpeechAnswerLost(SpeechUpstreamError):
    """The request went out and the provider's answer never came back.

    A read or write timeout, a dropped connection, a broken answer or a route's own deadline does
    not say whether the provider ran the request, so it may have synthesized or transcribed it and
    billed for it. The routes answer it with its own code, which tools/video/tts/client.mjs does
    not send again.
    """

    def __init__(self, provider: str, error: BaseException) -> None:
        super().__init__(
            504,
            f"{provider} may have received the request, but its answer was lost: "
            f"{type(error).__name__}",
        )


# A connection that never opened, or a request httpx would not write, cannot have reached the
# provider: nothing ran and nothing was billed.
NEVER_SENT = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.PoolTimeout,
    httpx.UnsupportedProtocol,
    httpx.LocalProtocolError,
)


def paid_request_failed(provider: str, error: httpx.HTTPError) -> SpeechUpstreamError:
    """What a paid POST that raised ``error`` tells the route: never sent, or answer lost."""
    if isinstance(error, NEVER_SENT):
        return SpeechUpstreamError(502, f"{provider} unreachable: {type(error).__name__}")
    return SpeechAnswerLost(provider, error)


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
            raise paid_request_failed("Azure Speech", error) from error
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
