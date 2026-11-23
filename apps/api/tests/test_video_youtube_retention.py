"""One video's audience retention curve from the YouTube Analytics API, for a video tool
(docs/videos/YOUTUBE-REPORTS.md §Audience retention).

``FakeAnalytics`` answers youtubeanalytics.googleapis.com the way the reference pages read on
2026-11-11 describe ``reports.query``; OAuth and videos.list come from test_video_youtube.py's
FakeGoogle. No network.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from urllib.parse import parse_qs
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.db import Base, get_session
from app.models import VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_speech.admin_api import video_tool
from app.video_youtube import admin_reports_api, connection, retention
from app.video_youtube.admin_reports_api import tool_router
from app.video_youtube.client import YOUTUBE_SCOPE, YoutubeError
from app.video_youtube.errors import Refused
from tests.test_video_youtube import CHANNEL, Site, open_site

HOST = "youtubeanalytics.googleapis.com"
NOW = datetime(2026, 11, 11, 12, 0, tzinfo=UTC)
VIDEO = "gkl0vABh1_c"
OTHER = "otherVIDEO1"


def curve() -> list[list[float]]:
    """100 points: a slow slide, a sharp fall at 9-10%, then flat."""
    points: list[list[float]] = []
    for step in range(1, 101):
        watch = 1.0 - step * 0.004 - (0.2 if step >= 10 else 0.0)
        points.append([round(step / 100, 2), round(watch, 4), 0.42])
    return points


@dataclass
class FakeAnalytics:
    queries: list[dict[str, list[str]]] = field(default_factory=list)
    rows: list[list[float]] = field(default_factory=curve)
    error: tuple[int, dict[str, Any]] | None = None

    def handle(self, request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v2/reports"
        assert request.headers["authorization"].startswith("Bearer access-")
        query = parse_qs(request.url.query.decode())
        self.queries.append(query)
        if self.error:
            return httpx.Response(self.error[0], json=self.error[1])
        headers = [
            {"name": "elapsedVideoTimeRatio", "columnType": "DIMENSION", "dataType": "FLOAT"},
            {"name": "audienceWatchRatio", "columnType": "METRIC", "dataType": "FLOAT"},
            {"name": "relativeRetentionPerformance", "columnType": "METRIC", "dataType": "FLOAT"},
        ]
        body: dict[str, Any] = {"kind": "youtubeAnalytics#resultTable", "columnHeaders": headers}
        if self.rows:
            body["rows"] = self.rows
        return httpx.Response(200, json=body)


@dataclass
class World:
    site: Site
    analytics: FakeAnalytics


@pytest.fixture
async def world(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> AsyncIterator[World]:
    async with open_site(monkeypatch, tmp_path) as site:
        engine = site.factory.kw["bind"]
        async with engine.begin() as db:
            await db.run_sync(
                lambda sync_db: Base.metadata.create_all(sync_db, tables=[VideoToolToken.__table__])
            )
        fake = FakeAnalytics()
        site.google.videos[VIDEO] = {
            "id": VIDEO,
            "snippet": {
                "channelId": CHANNEL,
                "title": "奇聞檔案局 H01",
                "publishedAt": "2026-10-20T03:00:00Z",
            },
            "contentDetails": {"duration": "PT13M5S"},
        }
        site.google.videos[OTHER] = {
            "id": OTHER,
            "snippet": {"channelId": "UCsomeoneelse000000000", "title": "x"},
            "contentDetails": {"duration": "PT1M"},
        }

        def handle(request: httpx.Request) -> httpx.Response:
            if request.url.host == HOST:
                return fake.handle(request)
            return site.google.handle(request)

        monkeypatch.setattr(
            connection,
            "http_client",
            lambda: httpx.AsyncClient(transport=httpx.MockTransport(handle)),
        )
        yield World(site, fake)


async def _ask(world: World, **options: Any) -> retention.Retention:
    async with world.site.factory() as session:
        return await retention.retention(session, video_id=VIDEO, now=NOW, **options)


async def _refused(world: World, **options: Any) -> Refused:
    with pytest.raises(Refused) as caught:
        await _ask(world, **options)
    return caught.value


def google_error(
    status: int, message: str, reason: str | None = None, state: str = ""
) -> dict[str, Any]:
    error: dict[str, Any] = {"code": status, "message": message}
    if reason:
        error["errors"] = [{"reason": reason, "message": message}]
    if state:
        error["status"] = state
    return {"error": error}


async def test_the_curve_comes_back_as_youtube_returned_it_with_the_video_s_length(
    world: World,
) -> None:
    await world.site.link()
    found = await _ask(world)
    assert found.columns == [
        "elapsedVideoTimeRatio",
        "audienceWatchRatio",
        "relativeRetentionPerformance",
    ]
    assert len(found.rows) == 100 and found.rows == curve(), "untouched, no derived drop"
    assert found.duration_seconds == 13 * 60 + 5
    assert found.title == "奇聞檔案局 H01"
    # By default from the Pacific day it was published to today (Pacific).
    assert (found.start, found.end) == (date(2026, 10, 19), date(2026, 11, 11))
    [query] = world.analytics.queries
    assert query["ids"] == ["channel==MINE"]
    assert query["dimensions"] == ["elapsedVideoTimeRatio"]
    assert query["metrics"] == ["audienceWatchRatio,relativeRetentionPerformance"]
    assert query["filters"] == [f"video=={VIDEO}"]
    assert (query["startDate"], query["endDate"]) == (["2026-10-19"], ["2026-11-11"])
    view = found.as_json()
    assert view["audience"] == "all" and "derived" in view["policy"]
    for derived in ("drop", "average", "seconds_at"):
        assert derived not in view, f"the site must not compute a {derived}"


async def test_organic_only_adds_the_audience_type_filter_and_keeps_the_span_asked(
    world: World,
) -> None:
    await world.site.link()
    found = await _ask(world, organic=True, start=date(2026, 10, 25), end=date(2026, 11, 8))
    assert found.organic and found.as_json()["audience"] == "organic"
    [query] = world.analytics.queries
    assert query["filters"] == [f"video=={VIDEO};audienceType==ORGANIC"]
    assert (query["startDate"], query["endDate"]) == (["2026-10-25"], ["2026-11-08"])


async def test_a_grant_without_analytics_is_told_to_link_again_before_asking_google(
    world: World,
) -> None:
    world.site.google.granted_scope = YOUTUBE_SCOPE
    await world.site.link()
    refused = await _refused(world)
    assert (refused.status, refused.code) == (409, "video_youtube_analytics_missing")
    assert "重新連結" in refused.detail and "yt-analytics.readonly" in refused.detail
    assert world.analytics.queries == []


async def test_nothing_is_asked_before_a_channel_is_linked(world: World) -> None:
    refused = await _refused(world)
    assert refused.code == "video_youtube_not_linked"


async def test_an_insufficient_scope_answer_from_google_also_means_link_again(
    world: World,
) -> None:
    await world.site.link()
    world.analytics.error = (
        403,
        google_error(
            403,
            "Request had insufficient authentication scopes.",
            "insufficientPermissions",
            "PERMISSION_DENIED",
        ),
    )
    refused = await _refused(world)
    assert (refused.status, refused.code) == (409, "video_youtube_analytics_missing")


async def test_an_analytics_api_the_project_has_not_enabled_says_which_api(world: World) -> None:
    await world.site.link()
    world.analytics.error = (
        403,
        google_error(
            403,
            "YouTube Analytics API has not been used in project 1234 before or it is "
            "disabled. Enable it by visiting https://console.developers.google.com/...",
            "accessNotConfigured",
            "PERMISSION_DENIED",
        ),
    )
    refused = await _refused(world)
    assert (refused.status, refused.code) == (503, "video_youtube_analytics_disabled")
    assert "YouTube Analytics API" in refused.detail and "啟用" in refused.detail


async def test_quota_and_other_refusals_are_named(world: World) -> None:
    await world.site.link()
    world.analytics.error = (429, google_error(429, "Quota exceeded", "quotaExceeded"))
    assert (await _refused(world)).code == "video_youtube_analytics_quota"
    world.analytics.error = (403, google_error(403, "Forbidden", "forbidden"))
    assert (await _refused(world)).code == "video_youtube_retention_forbidden"
    world.analytics.error = (400, google_error(400, "Unknown identifier", "badRequest"))
    other = await _refused(world)
    assert (other.status, other.code) == (502, "video_youtube_analytics_error")
    assert "400 badRequest" in other.detail


async def test_no_rows_means_too_few_views_and_says_so(world: World) -> None:
    await world.site.link()
    world.analytics.rows = []
    refused = await _refused(world)
    assert (refused.status, refused.code) == (404, "video_youtube_retention_no_data")
    assert "觀看數太少" in refused.detail


async def test_another_channel_s_video_a_missing_one_and_a_bad_id_are_refused_before_analytics(
    world: World,
) -> None:
    await world.site.link()
    async with world.site.factory() as session:
        for video_id, code in (
            (OTHER, "video_youtube_retention_other_channel"),
            ("missingVid1", "video_youtube_retention_unknown_video"),
            ("../x", "video_youtube_report_videos"),
        ):
            with pytest.raises(Refused) as caught:
                await retention.retention(session, video_id=video_id, now=NOW)
            assert caught.value.code == code
        with pytest.raises(Refused) as span:
            await retention.retention(
                session, video_id=VIDEO, start=date(2026, 11, 2), end=date(2026, 11, 1), now=NOW
            )
        assert span.value.code == "video_youtube_report_span"
    assert world.analytics.queries == []


def test_durations_and_refusals_parse_the_way_youtube_writes_them() -> None:
    assert retention.duration_seconds("PT13M5S") == 785
    assert retention.duration_seconds("PT1H2M") == 3720
    assert retention.duration_seconds("P1DT1S") == 86401
    assert retention.duration_seconds("P0D") == 0
    assert retention.duration_seconds("P") is None
    assert retention.duration_seconds(None) is None
    assert retention.refusal_for(YoutubeError(500, "backendError", "x")).status == 502


def _tool_app(world: World, token: VideoToolToken | None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(tool_router, prefix="/api/v1")

    async def session() -> AsyncIterator[Any]:
        async with world.site.factory() as db:
            yield db

    def tool() -> VideoToolToken:
        if token is None:
            raise AppError(401, "video_tool_token_invalid", "影片工具權杖無效或已撤銷")
        return token

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[video_tool] = tool
    return app


async def test_a_video_tool_reads_the_curve_through_its_token(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    await world.site.link()
    limit = AsyncMock()
    monkeypatch.setattr(admin_reports_api, "enforce_named_rate_limit", limit)
    token = VideoToolToken(
        id=uuid4(), name="Claude 雲端 session", token_hash="h" * 64, token_prefix="mkv_x"
    )
    base = "/api/v1/video/youtube-reports/retention"
    async with AsyncClient(
        transport=ASGITransport(app=_tool_app(world, token)), base_url="http://test"
    ) as client:
        ok = await client.get(
            base,
            params={"video_id": VIDEO, "start": "2026-10-20", "end": "2026-11-09", "organic": "1"},
        )
        bad = await client.get(base, params={"video_id": "a b"})
        other = await client.get(base, params={"video_id": OTHER})
    assert ok.status_code == 200 and ok.headers["cache-control"] == "no-store"
    body = ok.json()
    assert (body["video_id"], body["duration_seconds"], body["audience"]) == (VIDEO, 785, "organic")
    assert len(body["rows"]) == 100 and body["rows"][9] == curve()[9]
    assert world.analytics.queries[0]["filters"] == [f"video=={VIDEO};audienceType==ORGANIC"]
    assert bad.status_code == 422
    assert (other.status_code, other.json()["code"]) == (
        404,
        "video_youtube_retention_other_channel",
    )
    assert limit.await_args is not None and limit.await_args.args[0] == "video_youtube_retention"
    async with AsyncClient(
        transport=ASGITransport(app=_tool_app(world, None)), base_url="http://test"
    ) as client:
        assert (await client.get(base, params={"video_id": VIDEO})).status_code == 401
