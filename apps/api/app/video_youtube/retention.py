"""One video's audience retention curve, asked of YouTube for a video tool.

docs/videos/YOUTUBE-REPORTS.md §Audience retention. The daily Reporting API files carry no
per-moment retention, so this is the one place the site asks the YouTube Analytics API v2
(``analytics.py``) on a tool's behalf: with the stored channel grant, which never leaves the site.
Nothing is stored; every call asks YouTube again.

Before the Analytics query the site reads the video with videos.list (1 Data API unit): a video
of another channel is refused here rather than by a vague 403 from Analytics, and the answer
carries the video's length (``contentDetails.duration``, YouTube's metadata) so the tool can turn
elapsed ratios into seconds. The rows go back exactly as YouTube returned them; like the
reports, nothing here finds drops, averages or ranks (the derived-metrics policy in
``reports.py``): the tool does that and labels it as its own.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Any

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.video_youtube import connection
from app.video_youtube.analytics import AUDIENCE_TYPE_SINCE, DIMENSION, METRICS, AnalyticsClient
from app.video_youtube.client import YoutubeClient, YoutubeError
from app.video_youtube.errors import Refused
from app.video_youtube.reports import NEEDS_RELINK, NOT_LINKED, PACIFIC, VIDEO_ID, api_disabled
from app.video_youtube.state import parse_time

ANALYTICS_DISABLED = (
    "Google Cloud 專案還沒有啟用 YouTube Analytics API（跟每天下載報表的 YouTube Reporting API "
    "是兩個不同的 API）：到 Google Cloud 主控台的「API 和服務」→「程式庫」搜尋 "
    "YouTube Analytics API 並按「啟用」，幾分鐘後再試"
)
QUOTA = "YouTube 的 API 配額今天用完了或請求太密：明天（太平洋時間午夜後）再試"
NO_DATA = (
    "YouTube 沒有回這支影片在這段期間的觀眾續看資料：通常是觀看數太少（YouTube 不公布門檻），"
    "或期間太短、太新（資料約晚一到兩天）。拉長期間，或拿掉 --organic 再試"
)
FORBIDDEN = (
    "YouTube 拒絕讀這支影片的分析資料（403）：影片可能不屬於已連結的頻道，"
    "或授權不足；先確認影片 id，再到設定分頁按「重新連結」"
)
POLICY_NOTE = (
    "Rows are YouTube Analytics API data (reports.query, audience retention) exactly as YouTube "
    "returned it; duration_seconds is the video's length from videos.list. The site computes no "
    "derived metrics. Any drop, average or second you compute from these is your own analysis "
    "for the channel owner: label it as such and never present it as YouTube's number or "
    "publish it."
)
_DURATION = re.compile(
    r"^P(?:(?P<days>\d+)D)?(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?$"
)
_SCOPE_WORDS = ("insufficient", "ACCESS_TOKEN_SCOPE_INSUFFICIENT", "insufficientPermissions")
_QUOTA_WORDS = ("quotaExceeded", "rateLimitExceeded", "RESOURCE_EXHAUSTED", "dailyLimitExceeded")


def duration_seconds(value: object) -> int | None:
    """``contentDetails.duration`` (ISO 8601, e.g. ``PT13M5S``) in seconds, or None."""
    match = _DURATION.match(value) if isinstance(value, str) else None
    if not match or value == "P":
        return None
    parts = {name: int(found or 0) for name, found in match.groupdict().items()}
    return parts["days"] * 86400 + parts["hours"] * 3600 + parts["minutes"] * 60 + parts["seconds"]


def refusal_for(error: YoutubeError) -> Refused:
    """A Google refusal as the operator should read it."""
    text = f"{error.reason} {error.message}"
    if api_disabled(error):
        return Refused(503, "video_youtube_analytics_disabled", ANALYTICS_DISABLED)
    if error.status == 429 or any(word in text for word in _QUOTA_WORDS):
        return Refused(429, "video_youtube_analytics_quota", QUOTA)
    if error.status in (401, 403) and any(word in text for word in _SCOPE_WORDS):
        return Refused(409, "video_youtube_analytics_missing", NEEDS_RELINK)
    if error.status == 403:
        return Refused(403, "video_youtube_retention_forbidden", FORBIDDEN)
    return Refused(
        502,
        "video_youtube_analytics_error",
        f"YouTube 回覆 {error.status} {error.reason}：{error.message}"[:1000],
    )


@dataclass
class Retention:
    video_id: str
    title: str | None
    published_at: datetime | None
    duration_seconds: int | None
    start: date
    end: date
    organic: bool
    columns: list[str]
    rows: list[list[Any]]

    def as_json(self) -> dict[str, Any]:
        return {
            "video_id": self.video_id,
            "title": self.title,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "duration_seconds": self.duration_seconds,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "audience": "organic" if self.organic else "all",
            "columns": self.columns,
            "rows": self.rows,
            "day_timezone": "America/Los_Angeles",
            "policy": POLICY_NOTE,
        }


async def retention(
    session: AsyncSession,
    *,
    video_id: str,
    start: date | None = None,
    end: date | None = None,
    organic: bool = False,
    now: datetime | None = None,
) -> Retention:
    """The curve of ``video_id`` for ``start`` to ``end`` (Pacific days, both included; by default
    from the day it was published to today), organic traffic only when ``organic``."""
    if not VIDEO_ID.match(video_id):
        raise Refused(422, "video_youtube_report_videos", "video_id 的格式要像 YouTube 的影片 id")
    if start and end and end < start:
        raise Refused(422, "video_youtube_report_span", "end 早於 start")
    row = await connection.connection_row(session)
    if not connection.linked(row):
        raise Refused(409, "video_youtube_not_linked", NOT_LINKED)
    if not connection.analytics_granted(row):
        raise Refused(409, "video_youtube_analytics_missing", NEEDS_RELINK)
    channel_id = str(row.channel_id)
    today = (now or datetime.now(UTC)).astimezone(PACIFIC).date()
    async with connection.http_client() as http:
        token = await connection.access_token(session, http)
        await session.commit()
        try:
            found = await YoutubeClient(http, token).videos(
                [video_id], parts="snippet,contentDetails"
            )
            video = found[0] if found else None
            if video is None:
                raise Refused(
                    404,
                    "video_youtube_retention_unknown_video",
                    f"YouTube 找不到 {video_id}，或已連結的頻道看不到它",
                )
            raw = video.get("snippet")
            snippet: dict[str, Any] = raw if isinstance(raw, dict) else {}
            if snippet.get("channelId") != channel_id:
                raise Refused(
                    404,
                    "video_youtube_retention_other_channel",
                    f"{video_id} 不是已連結頻道的影片：只讀得到自己頻道影片的觀眾續看",
                )
            published = parse_time(snippet.get("publishedAt"))
            first = start or (published.astimezone(PACIFIC).date() if published else today)
            last = end or today
            if last < first:
                raise Refused(422, "video_youtube_report_span", "end 早於 start（或早於上架日）")
            if organic and first < AUDIENCE_TYPE_SINCE:
                first = AUDIENCE_TYPE_SINCE
            details = video.get("contentDetails")
            table = await AnalyticsClient(http, token).retention(
                video_id, start=first, end=last, organic=organic
            )
        except YoutubeError as error:
            raise refusal_for(error) from error
        except httpx.HTTPError as error:
            raise Refused(
                502, "video_youtube_analytics_error", f"連不到 YouTube：{type(error).__name__}"
            ) from error
    wanted = [DIMENSION, *METRICS]
    position = {name: index for index, name in enumerate(table.columns)}
    if DIMENSION not in position or not table.rows:
        raise Refused(404, "video_youtube_retention_no_data", NO_DATA)
    columns = [name for name in wanted if name in position]
    rows = [
        [line[position[name]] if position[name] < len(line) else None for name in columns]
        for line in table.rows
    ]
    title = snippet.get("title")
    return Retention(
        video_id=video_id,
        title=title if isinstance(title, str) else None,
        published_at=published,
        duration_seconds=duration_seconds(
            details.get("duration") if isinstance(details, dict) else None
        ),
        start=first,
        end=last,
        organic=organic,
        columns=columns,
        rows=rows,
    )
