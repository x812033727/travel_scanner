from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, cast
from urllib.parse import quote

import httpx

RETRY_STATUS_CODES = frozenset({429, 503})
MAX_RETRY_DELAY_SECONDS = 30.0


@dataclass(frozen=True)
class PageviewWindow:
    current: int
    previous: int
    observed_on: date
    source_url: str


class WikimediaPageviewClient:
    base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"

    def __init__(
        self,
        user_agent: str,
        timeout_seconds: float = 10.0,
        client: httpx.AsyncClient | None = None,
        max_retries: int = 3,
        retry_backoff_seconds: float = 1.0,
    ) -> None:
        self.user_agent = user_agent
        self.timeout_seconds = timeout_seconds
        self.client = client
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds

    def _retry_delay(self, response: httpx.Response, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return min(max(float(retry_after), 0.0), MAX_RETRY_DELAY_SECONDS)
            except ValueError:
                pass
        backoff = self.retry_backoff_seconds * (2.0**attempt)
        # Jitter keeps the concurrent collectors from retrying in lockstep.
        return min(backoff * (1 + random.random() * 0.25), MAX_RETRY_DELAY_SECONDS)

    async def _get(self, client: httpx.AsyncClient, source_url: str) -> httpx.Response:
        headers = {"User-Agent": self.user_agent, "Accept": "application/json"}
        for attempt in range(self.max_retries + 1):
            response = await client.get(source_url, headers=headers)
            if response.status_code not in RETRY_STATUS_CODES or attempt == self.max_retries:
                break
            await asyncio.sleep(self._retry_delay(response, attempt))
        response.raise_for_status()
        return response

    async def pageviews(
        self,
        project: str,
        title: str,
        *,
        observed_on: date | None = None,
    ) -> PageviewWindow:
        end = observed_on or (date.today() - timedelta(days=1))
        start = end - timedelta(days=59)
        encoded_title = quote(title.replace(" ", "_"), safe="")
        source_url = (
            f"{self.base_url}/{project}/all-access/user/{encoded_title}/daily/"
            f"{start:%Y%m%d}00/{end:%Y%m%d}00"
        )
        owns_client = self.client is None
        client = self.client or httpx.AsyncClient(timeout=self.timeout_seconds)
        try:
            response = await self._get(client, source_url)
            payload = cast(dict[str, Any], response.json())
        finally:
            if owns_client:
                await client.aclose()
        daily = {
            str(item["timestamp"])[:8]: int(item["views"]) for item in payload.get("items", [])
        }
        values = [daily.get(f"{start + timedelta(days=offset):%Y%m%d}", 0) for offset in range(60)]
        return PageviewWindow(
            current=sum(values[30:]),
            previous=sum(values[:30]),
            observed_on=end,
            source_url=source_url,
        )
