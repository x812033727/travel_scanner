"""The YouTube Reporting API calls the site makes (docs/videos/YOUTUBE-REPORTS.md).

The bulk-report half of YouTube Analytics: a channel schedules a job per report type, and YouTube
then writes one CSV a day for it (plus 30 days back from when the job was made), each kept for
60 days. Reference pages read on 2026-11-02: base ``https://youtubereporting.googleapis.com/v1``;
``GET /reportTypes``, ``GET /jobs``, ``POST /jobs`` (``reportTypeId`` and ``name``; 409 when the
job exists), ``GET /jobs/{id}/reports`` (``createdAfter``, ``pageToken``) and a GET of each
report's ``downloadUrl`` with the same bearer token. Scope ``yt-analytics.readonly``. The API has
no published quota beyond the project's; the site makes a few dozen calls a day.

Like ``client.py``, every call takes the ``httpx.AsyncClient`` it runs on, so tests hand in a
``MockTransport``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlsplit

import httpx

from app.video_youtube.client import TIMEOUT, _json

API = "https://youtubereporting.googleapis.com/v1"
# The only host a report is downloaded from: the bearer token goes nowhere else.
DOWNLOAD_HOST = "youtubereporting.googleapis.com"
DOWNLOAD_TIMEOUT = httpx.Timeout(120.0, connect=10.0)
# A day of a small channel's busiest report is tens of kilobytes; this stops a runaway file.
MAX_REPORT_BYTES = 32 * 1024 * 1024
MAX_PAGES = 50


class ReportRefused(Exception):
    """A report the site will not download: larger than it keeps, or at an address that is not
    YouTube's (the bearer token is never sent anywhere else)."""


def rfc3339(moment: datetime) -> str:
    """``createdAfter`` as the API reads it: UTC, a Z, microseconds."""
    return moment.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class ReportingClient:
    def __init__(self, http: httpx.AsyncClient, access_token: str) -> None:
        self.http = http
        self.headers = {"Authorization": f"Bearer {access_token}"}

    async def _pages(self, path: str, key: str, params: dict[str, str]) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        token: str | None = None
        for _ in range(MAX_PAGES):
            query = {**params, **({"pageToken": token} if token else {})}
            body = _json(
                await self.http.get(
                    f"{API}/{path}", params=query, headers=self.headers, timeout=TIMEOUT
                )
            )
            items = body.get(key)
            if isinstance(items, list):
                found.extend(item for item in items if isinstance(item, dict))
            next_token = body.get("nextPageToken")
            if not isinstance(next_token, str) or not next_token:
                break
            token = next_token
        return found

    async def report_types(self) -> list[dict[str, Any]]:
        """The report types this channel may schedule (system-managed ones are content-owner
        reports and are left out by default)."""
        return await self._pages("reportTypes", "reportTypes", {})

    async def jobs(self) -> list[dict[str, Any]]:
        return await self._pages("jobs", "jobs", {})

    async def create_job(self, report_type_id: str, name: str) -> dict[str, Any] | None:
        """The new job, or None when YouTube says one for this type already exists (409)."""
        response = await self.http.post(
            f"{API}/jobs",
            json={"reportTypeId": report_type_id, "name": name},
            headers=self.headers,
            timeout=TIMEOUT,
        )
        if response.status_code == 409:
            return None
        return _json(response)

    async def reports(self, job_id: str, created_after: datetime | None) -> list[dict[str, Any]]:
        params = {"createdAfter": rfc3339(created_after)} if created_after else {}
        return await self._pages(f"jobs/{job_id}/reports", "reports", params)

    async def download(self, url: str) -> bytes:
        """The report's CSV, decoded from the gzip transfer encoding YouTube sends it in."""
        parts = urlsplit(url)
        if parts.scheme != "https" or parts.hostname != DOWNLOAD_HOST:
            raise ReportRefused(f"not a report address: {url[:200]}")
        async with self.http.stream(
            "GET",
            url,
            headers={**self.headers, "Accept-Encoding": "gzip"},
            timeout=DOWNLOAD_TIMEOUT,
        ) as response:
            if response.is_error:
                await response.aread()
                _json(response)
            chunks: list[bytes] = []
            size = 0
            async for chunk in response.aiter_bytes():
                size += len(chunk)
                if size > MAX_REPORT_BYTES:
                    raise ReportRefused(f"larger than {MAX_REPORT_BYTES} bytes: {url[:200]}")
                chunks.append(chunk)
        return b"".join(chunks)
