"""The channel's daily Reporting API reports: fetching them, keeping them, and handing them to a
video tool (docs/videos/YOUTUBE-REPORTS.md).

``FakeReporting`` answers youtubereporting.googleapis.com the way the reference pages read on
2026-11-02 describe it, on top of test_video_youtube.py's FakeGoogle for OAuth and channels.
"""

from __future__ import annotations

import gzip
import json
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from urllib.parse import parse_qs
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, func, select

from app.db import Base, get_session
from app.models import VideoProject, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_speech.admin_api import video_tool
from app.video_youtube import admin_reports_api, connection, reports
from app.video_youtube.admin_reports_api import tool_router
from app.video_youtube.client import ANALYTICS_SCOPE, YOUTUBE_SCOPE
from app.video_youtube.errors import Refused
from app.video_youtube.models import (
    VideoYoutubeReport,
    VideoYoutubeReportJob,
    VideoYoutubeReportState,
)
from tests.test_video_youtube import CHANNEL, Site, open_site

HOST = "youtubereporting.googleapis.com"
NOW = datetime(2026, 11, 2, 12, 0, tzinfo=UTC)
TYPES: list[dict[str, Any]] = [
    {
        "id": "channel_basic_a2",
        "name": "User activity (old)",
        "deprecateTime": "2025-10-31T00:00:00Z",
    },
    {"id": "channel_basic_a3", "name": "User activity"},
    {"id": "channel_reach_basic_a1", "name": "Reach"},
    {"id": "channel_combined_a3", "name": "Combined"},
    {"id": "content_owner_basic_a4", "name": "Owner", "systemManaged": True},
]
BASIC_HEADER = (
    "date,channel_id,video_id,live_or_on_demand,subscribed_status,country_code,"
    "views,engaged_views,watch_time_minutes"
)


def basic_csv(day: str, rows: list[tuple[str, str, int]]) -> bytes:
    lines = [BASIC_HEADER]
    for video, country, views in rows:
        lines.append(
            f"{day},{CHANNEL},{video},on_demand,subscribed,{country},"
            f"{views},{views - 1},{views * 2}.5"
        )
    return ("\n".join(lines) + "\n").encode()


def pacific_start(day: date) -> str:
    """Pacific midnight of ``day`` in UTC (PDT until November 1, 2026)."""
    offset = 7 if day < date(2026, 11, 1) else 8
    return (datetime(day.year, day.month, day.day, tzinfo=UTC) + timedelta(hours=offset)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


@dataclass
class FakeReporting:
    jobs: list[dict[str, Any]] = field(default_factory=list)
    # job id -> its reports, each with "content" kept beside the resource.
    reports: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    calls: list[tuple[str, str, dict[str, list[str]]]] = field(default_factory=list)
    forbid: bool = False
    disabled: bool = False
    page_size: int = 2

    def add_report(
        self,
        job_id: str,
        day: date,
        content: bytes,
        created: datetime,
        report_id: str | None = None,
    ) -> dict[str, Any]:
        rid = report_id or f"r{uuid4().hex[:10]}"
        start = pacific_start(day)
        end = pacific_start(day + timedelta(days=1))
        report = {
            "id": rid,
            "jobId": job_id,
            "startTime": start,
            "endTime": end,
            "createTime": created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "downloadUrl": f"https://{HOST}/v1/media/CHANNEL/{CHANNEL}/jobs/{job_id}/reports/{rid}?alt=media",
            "_content": content,
        }
        self.reports.setdefault(job_id, []).append(report)
        return report

    def handle(self, request: httpx.Request) -> httpx.Response:
        query = parse_qs(request.url.query.decode())
        self.calls.append((request.method, request.url.path, query))
        assert request.headers["authorization"].startswith("Bearer access-")
        if self.disabled:
            return httpx.Response(
                403,
                json={
                    "error": {
                        "code": 403,
                        "message": "YouTube Reporting API has not been used in project 1234 "
                        "before or it is disabled. Enable it by visiting https://console...",
                        "status": "PERMISSION_DENIED",
                    }
                },
            )
        if self.forbid:
            return httpx.Response(
                403,
                json={
                    "error": {
                        "code": 403,
                        "message": "Insufficient Permission",
                        "status": "PERMISSION_DENIED",
                    }
                },
            )
        path = request.url.path
        if path == "/v1/reportTypes":
            return httpx.Response(200, json={"reportTypes": TYPES})
        if path == "/v1/jobs" and request.method == "GET":
            return httpx.Response(200, json={"jobs": self.jobs})
        if path == "/v1/jobs" and request.method == "POST":
            body = json.loads(request.content)
            if any(job["reportTypeId"] == body["reportTypeId"] for job in self.jobs):
                return httpx.Response(409, json={"error": {"code": 409, "message": "exists"}})
            job = {
                "id": f"job-{body['reportTypeId']}",
                "reportTypeId": body["reportTypeId"],
                "name": body["name"],
                "createTime": "2026-11-02T12:00:00Z",
            }
            self.jobs.append(job)
            return httpx.Response(200, json=job)
        if path.startswith("/v1/jobs/") and path.endswith("/reports"):
            job_id = path.split("/")[3]
            after = query.get("createdAfter", [None])[0]
            listed = [
                {key: value for key, value in report.items() if key != "_content"}
                for report in self.reports.get(job_id, [])
                if after is None or report["createTime"] > after
            ]
            start = int(query.get("pageToken", ["0"])[0])
            page = listed[start : start + self.page_size]
            answer: dict[str, Any] = {"reports": page}
            if start + self.page_size < len(listed):
                answer["nextPageToken"] = str(start + self.page_size)
            return httpx.Response(200, json=answer)
        if path.startswith("/v1/media/"):
            rid = path.rsplit("/", 1)[1]
            for listed in self.reports.values():
                for report in listed:
                    if report["id"] == rid:
                        return httpx.Response(
                            200,
                            content=gzip.compress(report["_content"]),
                            headers={
                                "Content-Encoding": "gzip",
                                "Content-Type": "application/octet-stream",
                            },
                        )
            return httpx.Response(404)
        raise AssertionError(f"unexpected {request.method} {request.url}")


@dataclass
class World:
    site: Site
    reporting: FakeReporting


@pytest.fixture
async def world(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> AsyncIterator[World]:
    async with open_site(monkeypatch, tmp_path) as site:
        engine = site.factory.kw["bind"]
        async with engine.begin() as db:
            await db.run_sync(
                lambda sync_db: Base.metadata.create_all(
                    sync_db,
                    tables=[
                        VideoYoutubeReportJob.__table__,
                        VideoYoutubeReport.__table__,
                        VideoYoutubeReportState.__table__,
                        VideoToolToken.__table__,
                    ],
                )
            )
        fake = FakeReporting()

        def handle(request: httpx.Request) -> httpx.Response:
            if request.url.host == HOST:
                return fake.handle(request)
            return site.google.handle(request)

        monkeypatch.setattr(
            connection,
            "http_client",
            lambda: httpx.AsyncClient(transport=httpx.MockTransport(handle)),
        )
        monkeypatch.setattr(reports, "get_redis", lambda: site.redis)

        # SQLite drops timezone offsets; PostgreSQL hands back aware datetimes.
        def restore_utc(target: Any, _context: Any, *_more: Any) -> None:
            for column in target.__table__.columns:
                value = getattr(target, column.name)
                if isinstance(value, datetime) and value.tzinfo is None:
                    setattr(target, column.name, value.replace(tzinfo=UTC))

        mine = (VideoYoutubeReportJob, VideoYoutubeReport, VideoYoutubeReportState)
        for model in mine:
            event.listen(model, "load", restore_utc)
            event.listen(model, "refresh", restore_utc)
        yield World(site, fake)
        for model in mine:
            event.remove(model, "load", restore_utc)
            event.remove(model, "refresh", restore_utc)


async def _sync(world: World, **options: Any) -> reports.SyncResult:
    async with world.site.factory() as session:
        return await reports.sync(session, now=options.pop("now", NOW), **options)


async def _count(world: World) -> int:
    async with world.site.factory() as session:
        return int(await session.scalar(select(func.count(VideoYoutubeReport.id))) or 0)


def test_the_newest_current_version_of_each_family_is_chosen() -> None:
    chosen = reports.choose_types(TYPES, NOW)
    assert chosen == {
        "channel_basic": "channel_basic_a3",
        "channel_reach_basic": "channel_reach_basic_a1",
    }
    # Only a deprecated version left: it is still read, YouTube makes it for three months.
    assert reports.choose_types(TYPES[:1], NOW) == {"channel_basic": "channel_basic_a2"}


async def test_the_link_asks_for_analytics_and_the_card_says_whether_it_was_granted(
    world: World,
) -> None:
    await world.site.link()
    async with world.site.factory() as session:
        view = await connection.connection_view(session)
    assert view.analytics_granted
    assert set(view.scope.split()) == {YOUTUBE_SCOPE, ANALYTICS_SCOPE}


async def test_a_channel_linked_without_analytics_is_told_to_link_again(world: World) -> None:
    world.site.google.granted_scope = YOUTUBE_SCOPE
    await world.site.link()
    result = await _sync(world)
    assert result.status == "needs_relink"
    assert "yt-analytics.readonly" in (result.problem or "")
    assert world.reporting.calls == [], "nothing is asked of YouTube without the scope"
    async with world.site.factory() as session:
        assert (await connection.connection_view(session)).analytics_granted is False
        view = await reports.overview(session, NOW)
    assert view["problem"] and "重新連結" in view["problem"]


async def test_nothing_is_fetched_before_a_channel_is_linked(world: World) -> None:
    assert (await _sync(world)).status == "not_linked"


async def test_a_first_run_schedules_the_jobs_and_keeps_every_report_as_youtube_wrote_it(
    world: World,
) -> None:
    await world.site.link()
    first = await _sync(world)
    assert first.status == "synced"
    assert sorted(first.jobs_created) == ["channel_basic_a3", "channel_reach_basic_a1"]
    posted = [path for method, path, _ in world.reporting.calls if method == "POST"]
    assert posted == ["/v1/jobs", "/v1/jobs"]
    # YouTube posts the backfill later; the next run picks it up.
    content = basic_csv("2026-10-30", [("vidAAAAAAA1", "TW", 10), ("vidBBBBBBB2", "JP", 3)])
    for offset in range(3):
        world.reporting.add_report(
            "job-channel_basic_a3",
            date(2026, 10, 28) + timedelta(days=offset),
            content,
            NOW + timedelta(hours=offset),
        )
    assert (await _sync(world, now=NOW + timedelta(hours=1))).status == "not_due"
    later = NOW + timedelta(hours=13)
    second = await _sync(world, now=later)
    assert (second.status, second.downloaded, second.jobs_created) == ("synced", 3, [])
    async with world.site.factory() as session:
        kept = list(
            await session.scalars(select(VideoYoutubeReport).order_by(VideoYoutubeReport.day))
        )
    assert [row.day for row in kept] == [date(2026, 10, 28), date(2026, 10, 29), date(2026, 10, 30)]
    assert gzip.decompress(kept[0].content_gzip) == content
    assert kept[0].row_count == 2 and kept[0].columns[:3] == ["date", "channel_id", "video_id"]
    # The third run asks only for what was made after the newest file it keeps.
    await _sync(world, now=later + timedelta(hours=13))
    listed = [
        query
        for _, path, query in world.reporting.calls
        if path == "/v1/jobs/job-channel_basic_a3/reports"
    ]
    assert "createdAfter" not in listed[0]
    assert listed[-1]["createdAfter"] == ["2026-11-02T14:00:00.000000Z"]


async def test_a_regenerated_day_replaces_the_older_file_and_an_older_one_never_does(
    world: World,
) -> None:
    await world.site.link()
    await _sync(world)
    day = date(2026, 10, 30)
    world.reporting.add_report(
        "job-channel_basic_a3", day, basic_csv("2026-10-30", [("vidAAAAAAA1", "TW", 10)]), NOW
    )
    await _sync(world, force=True)
    newer = basic_csv("2026-10-30", [("vidAAAAAAA1", "TW", 12)])
    world.reporting.add_report("job-channel_basic_a3", day, newer, NOW + timedelta(hours=5))
    result = await _sync(world, force=True)
    assert result.replaced == 1 and await _count(world) == 1
    async with world.site.factory() as session:
        row = await session.scalar(select(VideoYoutubeReport))
    assert row is not None and gzip.decompress(row.content_gzip) == newer


async def test_a_run_stops_at_its_limit_and_the_next_one_continues(world: World) -> None:
    await world.site.link()
    await _sync(world)
    for offset in range(5):
        world.reporting.add_report(
            "job-channel_basic_a3",
            date(2026, 10, 20) + timedelta(days=offset),
            basic_csv("2026-10-20", [("vidAAAAAAA1", "TW", offset + 1)]),
            NOW + timedelta(minutes=offset),
        )
    first = await _sync(world, force=True, limit=2)
    assert (first.status, first.downloaded, first.remaining) == ("partial", 2, True)
    async with world.site.factory() as session:
        assert (await reports.state_row(session)).synced_at == NOW, (
            "a partial run is not a full one"
        )
    rest = await _sync(world, force=True, limit=10)
    assert (rest.status, rest.downloaded, rest.remaining) == ("synced", 3, False)
    assert await _count(world) == 5


async def test_a_report_off_youtube_s_host_is_never_fetched_with_the_token(world: World) -> None:
    await world.site.link()
    await _sync(world)
    report = world.reporting.add_report(
        "job-channel_basic_a3", date(2026, 10, 30), basic_csv("2026-10-30", []), NOW
    )
    report["downloadUrl"] = "https://attacker.example/steal"
    result = await _sync(world, force=True)
    assert (result.status, result.downloaded, result.skipped) == ("synced", 0, 1)


async def test_a_refusal_from_youtube_is_recorded_and_403_means_link_again(world: World) -> None:
    await world.site.link()
    world.reporting.forbid = True
    result = await _sync(world)
    assert result.status == "needs_relink"
    async with world.site.factory() as session:
        assert (await reports.state_row(session)).problem == reports.NEEDS_RELINK


async def _seed(world: World) -> None:
    await world.site.link()
    await _sync(world)
    for offset, views in enumerate((10, 20, 30)):
        day = date(2026, 10, 28) + timedelta(days=offset)
        world.reporting.add_report(
            "job-channel_basic_a3",
            day,
            basic_csv(day.isoformat(), [("vidAAAAAAA1", "TW", views), ("vidBBBBBBB2", "JP", 1)]),
            NOW + timedelta(minutes=offset),
        )
    await _sync(world, force=True)
    async with world.site.factory() as session:
        session.add(
            VideoProject(
                slug="ai-agent-vs-chatbot",
                title="AI 代理和聊天機器人差在哪",
                stage="published",
                youtube_video_id="vidAAAAAAA1",
                youtube_publish_at=datetime(2026, 10, 20, tzinfo=UTC),
                category="ai-terms",
            )
        )
        await session.commit()


async def test_rows_are_youtube_s_lines_for_the_days_and_videos_asked(world: World) -> None:
    await _seed(world)
    async with world.site.factory() as session:
        found = await reports.rows(
            session,
            report="channel_basic",
            start=date(2026, 10, 29),
            end=date(2026, 10, 30),
            video_ids=["vidAAAAAAA1"],
        )
    assert found.report_type_id == "channel_basic_a3"
    assert found.days == ["2026-10-29", "2026-10-30"]
    assert found.columns == BASIC_HEADER.split(",")
    assert [row[2] for row in found.rows] == ["vidAAAAAAA1", "vidAAAAAAA1"]
    assert [row[6] for row in found.rows] == ["20", "30"], "the numbers as YouTube wrote them"
    assert reports.as_csv(found).splitlines()[0] == BASIC_HEADER


async def test_rows_refuse_a_long_span_a_bad_video_id_and_an_unknown_report(world: World) -> None:
    await _seed(world)
    async with world.site.factory() as session:
        for options, code in (
            (
                {"report": "channel_basic", "start": date(2026, 1, 1), "end": date(2026, 10, 1)},
                "video_youtube_report_span",
            ),
            (
                {"report": "channel_basic", "start": date(2026, 10, 2), "end": date(2026, 10, 1)},
                "video_youtube_report_span",
            ),
            (
                {
                    "report": "channel_basic",
                    "start": date(2026, 10, 1),
                    "end": date(2026, 10, 2),
                    "video_ids": ["../x"],
                },
                "video_youtube_report_videos",
            ),
            (
                {"report": "channel_money", "start": date(2026, 10, 1), "end": date(2026, 10, 2)},
                "video_youtube_report_unknown",
            ),
        ):
            with pytest.raises(Refused) as refused:
                await reports.rows(session, **options)  # type: ignore[arg-type]
            assert refused.value.code == code


async def test_the_overview_names_the_reports_and_the_site_s_videos_and_derives_nothing(
    world: World,
) -> None:
    await _seed(world)
    async with world.site.factory() as session:
        view = await reports.overview(session, NOW)
    assert view["linked"] and view["analytics_granted"] and view["channel_id"] == CHANNEL
    basic = next(item for item in view["reports"] if item["report_type_id"] == "channel_basic_a3")
    assert (basic["days"], basic["first_day"], basic["last_day"], basic["rows"]) == (
        3,
        "2026-10-28",
        "2026-10-30",
        6,
    )
    assert [item["report_type_id"] for item in view["waiting_for_first_report"]] == [
        "channel_reach_basic_a1"
    ]
    assert view["videos"][0]["slug"] == "ai-agent-vs-chatbot"
    assert view["videos"][0]["video_id"] == "vidAAAAAAA1"
    text = json.dumps(view, default=str).lower()
    for derived in ("average", "median", "rank", "score", "total_views", "ratio"):
        assert f'"{derived}' not in text, f"the overview must not carry a derived {derived}"


async def test_unlinking_takes_the_reports_with_the_grant(world: World) -> None:
    await _seed(world)
    assert await _count(world) == 3
    async with world.site.factory() as session:
        await connection.unlink(session, world.site.owner)
    async with world.site.factory() as session:
        view = await reports.overview(session, NOW)
    assert view["reports"] == [] and not view["linked"]
    assert await _count(world) == 0
    async with world.site.factory() as session:
        assert await session.scalar(select(func.count()).select_from(VideoYoutubeReportJob)) == 0


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


async def test_a_video_tool_reads_the_reports_through_its_token(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    await _seed(world)
    monkeypatch.setattr(admin_reports_api, "enforce_named_rate_limit", AsyncMock())
    token = VideoToolToken(
        id=uuid4(), name="Claude 雲端 session", token_hash="h" * 64, token_prefix="mkv_x"
    )
    async with AsyncClient(
        transport=ASGITransport(app=_tool_app(world, token)), base_url="http://test"
    ) as client:
        overview = await client.get("/api/v1/video/youtube-reports")
        csv_rows = await client.get(
            "/api/v1/video/youtube-reports/rows",
            params={
                "report": "channel_basic",
                "start": "2026-10-28",
                "end": "2026-10-30",
                "video_id": "vidBBBBBBB2",
                "format": "csv",
            },
        )
        json_rows = await client.get(
            "/api/v1/video/youtube-reports/rows",
            params={"report": "channel_basic", "start": "2026-10-28", "end": "2026-10-28"},
        )
        refused = await client.get(
            "/api/v1/video/youtube-reports/rows",
            params={"report": "channel_basic", "start": "2026-01-01", "end": "2026-10-28"},
        )
        synced = await client.post(
            "/api/v1/video/youtube-reports/sync", json={"force": True, "limit": 5}
        )
    assert (
        overview.status_code == 200
        and overview.json()["videos"][0]["slug"] == "ai-agent-vs-chatbot"
    )
    assert csv_rows.status_code == 200 and csv_rows.headers["content-type"].startswith("text/csv")
    assert csv_rows.headers["x-report-days"] == "3"
    assert [line.split(",")[2] for line in csv_rows.text.splitlines()[1:]] == ["vidBBBBBBB2"] * 3
    assert json_rows.json()["rows"][0][:3] == ["2026-10-28", CHANNEL, "vidAAAAAAA1"]
    assert "derived" in json_rows.json()["policy"]
    assert (refused.status_code, refused.json()["code"]) == (422, "video_youtube_report_span")
    assert synced.status_code == 200 and synced.json()["status"] == "synced"
    async with AsyncClient(
        transport=ASGITransport(app=_tool_app(world, None)), base_url="http://test"
    ) as client:
        assert (await client.get("/api/v1/video/youtube-reports")).status_code == 401


async def test_an_api_the_project_has_not_enabled_says_so_instead_of_asking_for_a_relink(
    world: World,
) -> None:
    await world.site.link()
    world.reporting.disabled = True
    result = await _sync(world)
    assert (result.status, result.problem) == ("partial", reports.API_DISABLED)
    async with world.site.factory() as session:
        assert (await reports.state_row(session)).problem == reports.API_DISABLED
