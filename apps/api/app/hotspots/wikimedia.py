from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, cast
from urllib.parse import quote

import httpx


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
    ) -> None:
        self.user_agent = user_agent
        self.timeout_seconds = timeout_seconds
        self.client = client

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
            response = await client.get(
                source_url,
                headers={"User-Agent": self.user_agent, "Accept": "application/json"},
            )
            response.raise_for_status()
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
