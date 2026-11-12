"""The one YouTube Analytics API v2 call the site makes: a video's audience retention curve.

docs/videos/YOUTUBE-REPORTS.md §Audience retention. Reference pages read on 2026-11-11:
``GET https://youtubeanalytics.googleapis.com/v2/reports`` (``reports.query``), scope
``yt-analytics.readonly`` (``client.ANALYTICS_SCOPE``, already part of the channel link), and the
channel "Audience retention" report:

- dimension ``elapsedVideoTimeRatio`` (required, the only one): YouTube returns 100 points per
  video, ratios 0.01 to 1.0;
- metrics ``audienceWatchRatio`` (views of that moment over the video's views; can exceed 1 when
  viewers rewind) and ``relativeRetentionPerformance`` (0 to 1, against all YouTube videos of a
  similar length; 0.5 is the median);
- filter ``video==<id>`` is required and takes exactly ONE id (no comma-separated list);
  ``audienceType`` is optional, one of ``ORGANIC``, ``AD_INSTREAM``, ``AD_INDISPLAY``, with data
  only from 2013-09-25 on; ``subscribedStatus`` and ``youtubeProduct`` are optional too and not
  used here.
- The pages state no minimum view count, but YouTube answers a video with too few views for the
  span with no rows at all; the service turns that into its own refusal.

The API has its own daily quota in the Google Cloud project, separate from the Data API's units;
one retention curve is one query. Like ``client.py``, the call takes the ``httpx.AsyncClient``
it runs on, so tests hand in a ``MockTransport``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

import httpx

from app.video_youtube.client import TIMEOUT, _json

API = "https://youtubeanalytics.googleapis.com/v2"
DIMENSION = "elapsedVideoTimeRatio"
METRICS = ("audienceWatchRatio", "relativeRetentionPerformance")
ORGANIC = "ORGANIC"
# The first day YouTube keeps audienceType data for.
AUDIENCE_TYPE_SINCE = date(2013, 9, 25)


@dataclass(frozen=True)
class Table:
    """``reports.query``'s answer: the column names YouTube gave and its rows, untouched."""

    columns: list[str]
    rows: list[list[Any]]


class AnalyticsClient:
    def __init__(self, http: httpx.AsyncClient, access_token: str) -> None:
        self.http = http
        self.headers = {"Authorization": f"Bearer {access_token}"}

    async def retention(
        self, video_id: str, *, start: date, end: date, organic: bool, channel_id: str = "MINE"
    ) -> Table:
        filters = f"video=={video_id}" + (f";audienceType=={ORGANIC}" if organic else "")
        body = _json(
            await self.http.get(
                f"{API}/reports",
                params={
                    "ids": f"channel=={channel_id}",
                    "startDate": start.isoformat(),
                    "endDate": end.isoformat(),
                    "dimensions": DIMENSION,
                    "metrics": ",".join(METRICS),
                    "filters": filters,
                    "sort": DIMENSION,
                },
                headers=self.headers,
                timeout=TIMEOUT,
            )
        )
        headers = body.get("columnHeaders")
        columns = [
            str(item.get("name") or "")
            for item in (headers if isinstance(headers, list) else [])
            if isinstance(item, dict)
        ]
        rows = body.get("rows")
        return Table(
            columns=columns,
            rows=[list(row) for row in rows if isinstance(row, list)]
            if isinstance(rows, list)
            else [],
        )
