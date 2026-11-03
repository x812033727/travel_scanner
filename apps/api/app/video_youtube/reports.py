"""The channel's daily reports: fetching them from YouTube and handing them to a video tool.

docs/videos/YOUTUBE-REPORTS.md. ``sync`` makes sure the channel has a reporting job for every
family in FAMILIES (at the newest version YouTube offers), then downloads the reports created
since the last one kept for each job. A run downloads at most ``limit`` files and says whether
more are waiting; the first run after a job is made has about thirty days of backfill.

``overview`` and ``rows`` are what a paired AI session reads through its video tool token: which
reports there are and for which days, the site's own videos with their YouTube ids, and the rows
of one report family for a span of days, filtered to some videos if asked. The rows are the CSV
lines exactly as YouTube wrote them. Nothing here adds them up, averages, ranks or rates them:
YouTube's developer policies do not let an API client present metrics it derived from API data
without the audit covering that, and the analysis the owner's AI does is its own work, read from
these raw rows.
"""

from __future__ import annotations

import csv
import gzip
import io
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from typing import Any, Literal
from zoneinfo import ZoneInfo

import httpx
from redis.exceptions import RedisError
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra import get_redis
from app.models import VideoProject
from app.video_youtube import connection
from app.video_youtube.client import YoutubeError
from app.video_youtube.errors import Refused
from app.video_youtube.models import (
    VideoYoutubeReport,
    VideoYoutubeReportJob,
    VideoYoutubeReportState,
)
from app.video_youtube.reporting import ReportingClient, ReportRefused
from app.video_youtube.state import parse_time

PACIFIC = ZoneInfo("America/Los_Angeles")
# The report families the site keeps, and what each answers. channel_combined (every dimension
# at once) is left out: it is the largest file and the others cover its questions.
FAMILIES: dict[str, str] = {
    "channel_basic": "每支影片每天的觀看、engaged views、觀看時間、平均觀看時長與百分比、"
    "喜歡、留言、分享、訂閱增減，依國家、是否訂閱者、直播或隨選分列",
    "channel_reach_basic": "每支影片每天的縮圖曝光次數與曝光點閱率",
    "channel_reach_combined": "縮圖曝光與點閱率，依流量來源、裝置與作業系統分列",
    "channel_traffic_source": "觀看從哪裡來：搜尋（含搜尋字詞）、推薦、Shorts 動態、外部網站等",
    "channel_playback_location": "在哪裡播放：觀看頁、嵌入、頻道頁、Shorts 動態等",
    "channel_device_os": "用什麼裝置與作業系統看",
    "channel_demographics": "觀眾的年齡層與性別（佔比）",
    "channel_sharing_service": "影片被分享到哪些服務",
    "channel_subtitles": "觀看時開了哪一種字幕語言",
    "channel_end_screens": "片尾畫面元素的曝光與點擊",
}
JOB_PREFIX = "mokaair-"
SYNC_EVERY = timedelta(hours=12)
DEFAULT_LIMIT = 150
MAX_LIMIT = 400
LOCK_KEY = "video-youtube-reports-sync"
LOCK_SECONDS = 900
MAX_SPAN_DAYS = 120
MAX_VIDEO_IDS = 50
MAX_ROWS = {"csv": 500_000, "json": 50_000}
VERSION = re.compile(r"^(?P<family>[a-z_]+)_a(?P<version>[0-9]+)$")
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{6,20}$")
NEEDS_RELINK = (
    "頻道授權沒有包含 YouTube Analytics（yt-analytics.readonly）：到設定分頁按「重新連結」，"
    "在 Google 的同意畫面勾選它，報表才讀得到"
)
API_DISABLED = (
    "Google Cloud 專案還沒有啟用 YouTube Reporting API：到 Google Cloud 主控台的「API 和服務」→"
    "「程式庫」搜尋 YouTube Reporting API 並按「啟用」，幾分鐘後再下載一次"
)
NOT_LINKED = "還沒有連結 YouTube 頻道：到 /admin/videos 的設定分頁連結"
POLICY_NOTE = (
    "Rows are YouTube Reporting API data exactly as YouTube generated it (one CSV per Pacific "
    "day). The site computes no derived metrics. Any totals, ratios or rankings you compute are "
    "your own analysis for the channel owner: label them as such and never present them as "
    "YouTube's numbers or publish them."
)

SyncStatus = Literal["synced", "partial", "not_due", "running", "not_linked", "needs_relink"]


@dataclass
class SyncResult:
    status: SyncStatus
    jobs_created: list[str] = field(default_factory=list)
    downloaded: int = 0
    replaced: int = 0
    skipped: int = 0
    remaining: bool = False
    problem: str | None = None
    synced_at: datetime | None = None
    chosen_types: dict[str, str] = field(default_factory=dict)


def api_disabled(error: YoutubeError) -> bool:
    """Google's answer when the project has not enabled the API: a 403 whose message says so
    (``SERVICE_DISABLED`` / ``accessNotConfigured``), unlike a grant without the scope."""
    text = f"{error.reason} {error.message}"
    return error.status == 403 and (
        "SERVICE_DISABLED" in text
        or "accessNotConfigured" in text
        or "has not been used in project" in text
        or "it is disabled" in text
    )


def pacific_day(moment: datetime) -> date:
    return moment.astimezone(PACIFIC).date()


def choose_types(report_types: Iterable[dict[str, Any]], now: datetime) -> dict[str, str]:
    """For each family the newest version YouTube offers that is not deprecated (a deprecated
    one only when nothing else is), e.g. ``channel_basic`` -> ``channel_basic_a3``."""
    best: dict[str, tuple[bool, int, str]] = {}
    for item in report_types:
        type_id = str(item.get("id") or "")
        match = VERSION.match(type_id)
        if not match or match["family"] not in FAMILIES or item.get("systemManaged"):
            continue
        deprecated_at = parse_time(item.get("deprecateTime"))
        current = deprecated_at is None or deprecated_at > now
        rank = (current, int(match["version"]), type_id)
        if match["family"] not in best or rank > best[match["family"]]:
            best[match["family"]] = rank
    return {family: rank[2] for family, rank in sorted(best.items())}


def version_of(report_type_id: str) -> int:
    match = VERSION.match(report_type_id)
    return int(match["version"]) if match else 0


def family_of(report_type_id: str) -> str | None:
    match = VERSION.match(report_type_id)
    return match["family"] if match and match["family"] in FAMILIES else None


def parse_csv(content: bytes) -> tuple[list[str], int]:
    """The header and the number of data rows of a report file."""
    text = content.decode("utf-8-sig", errors="replace")
    reader = csv.reader(io.StringIO(text))
    header = next(reader, [])
    return [name.strip() for name in header], sum(1 for row in reader if row)


async def state_row(session: AsyncSession) -> VideoYoutubeReportState:
    row = await session.get(VideoYoutubeReportState, 1)
    if row is None:
        row = VideoYoutubeReportState(id=1, chosen_types={})
        session.add(row)
        await session.flush()
    return row


async def _record_problem(session: AsyncSession, problem: str, now: datetime) -> None:
    state = await state_row(session)
    state.problem = problem
    state.attempted_at = now
    await session.commit()


async def _latest_created(session: AsyncSession, job_id: str) -> datetime | None:
    value = await session.scalar(
        select(func.max(VideoYoutubeReport.create_time)).where(VideoYoutubeReport.job_id == job_id)
    )
    return value if isinstance(value, datetime) else None


async def _keep_report(
    session: AsyncSession,
    *,
    channel_id: str,
    job: VideoYoutubeReportJob,
    report: dict[str, Any],
    content: bytes,
    now: datetime,
) -> Literal["new", "replaced", "older"]:
    start = parse_time(report.get("startTime"))
    end = parse_time(report.get("endTime"))
    created = parse_time(report.get("createTime"))
    assert start is not None and end is not None and created is not None
    day = pacific_day(start)
    existing = await session.scalar(
        select(VideoYoutubeReport).where(
            VideoYoutubeReport.channel_id == channel_id,
            VideoYoutubeReport.report_type_id == job.report_type_id,
            VideoYoutubeReport.day == day,
        )
    )
    if existing is not None and existing.create_time >= created:
        return "older"
    columns, row_count = parse_csv(content)
    values = {
        "report_id": str(report.get("id"))[:64],
        "job_id": job.job_id,
        "start_time": start,
        "end_time": end,
        "create_time": created,
        "downloaded_at": now,
        "columns": columns,
        "row_count": row_count,
        "size_bytes": len(content),
        "content_gzip": gzip.compress(content),
    }
    if existing is None:
        session.add(
            VideoYoutubeReport(
                channel_id=channel_id, report_type_id=job.report_type_id, day=day, **values
            )
        )
        return "new"
    for name, value in values.items():
        setattr(existing, name, value)
    return "replaced"


async def _acquire_lock() -> bool:
    try:
        return bool(await get_redis().set(LOCK_KEY, "1", nx=True, ex=LOCK_SECONDS))
    except RedisError:
        # Without Redis two runs could overlap; the unique day key keeps them from doubling.
        return True


async def _release_lock() -> None:
    try:
        await get_redis().delete(LOCK_KEY)
    except RedisError:
        pass


async def forget_other_channels(session: AsyncSession) -> str | None:
    """Delete what was read for a channel the site no longer holds a grant for: every report
    after an unlink, another channel's after a link in its place (Developer Policies III.E.4).
    Every read and every run starts with it, and the card reads the reports again right after
    an unlink. Returns the linked channel's id, or None."""
    row = await connection.connection_row(session)
    channel_id = str(row.channel_id) if connection.linked(row) else None
    if channel_id is None:
        await session.execute(delete(VideoYoutubeReport))
        await session.execute(delete(VideoYoutubeReportJob))
        state = await session.get(VideoYoutubeReportState, 1)
        if state is not None and (state.synced_at or state.chosen_types):
            state.synced_at = None
            state.chosen_types = {}
    else:
        await session.execute(
            delete(VideoYoutubeReport).where(VideoYoutubeReport.channel_id != channel_id)
        )
        await session.execute(
            delete(VideoYoutubeReportJob).where(VideoYoutubeReportJob.channel_id != channel_id)
        )
    return channel_id


async def sync(
    session: AsyncSession,
    *,
    force: bool = False,
    limit: int = DEFAULT_LIMIT,
    now: datetime | None = None,
) -> SyncResult:
    """Schedule the missing jobs and download what YouTube made since the last run. A run
    within SYNC_EVERY of the last complete one does nothing unless ``force``."""
    moment = now or datetime.now(UTC)
    limit = max(1, min(limit, MAX_LIMIT))
    await forget_other_channels(session)
    row = await connection.connection_row(session)
    state = await state_row(session)
    if not connection.linked(row):
        await session.commit()
        return SyncResult(status="not_linked", problem=NOT_LINKED)
    if not connection.analytics_granted(row):
        await _record_problem(session, NEEDS_RELINK, moment)
        return SyncResult(status="needs_relink", problem=NEEDS_RELINK)
    if not force and state.synced_at is not None and moment - state.synced_at < SYNC_EVERY:
        result = SyncResult(status="not_due", synced_at=state.synced_at)
        await session.commit()
        return result
    channel_id = str(row.channel_id)
    if not await _acquire_lock():
        await session.commit()
        return SyncResult(status="running")
    try:
        return await _sync_locked(session, channel_id, limit, moment)
    finally:
        await _release_lock()


async def _sync_locked(
    session: AsyncSession, channel_id: str, limit: int, moment: datetime
) -> SyncResult:
    result = SyncResult(status="synced")
    async with connection.http_client() as http:
        try:
            token = await connection.access_token(session, http)
        except Refused as refused:
            await _record_problem(session, refused.detail, moment)
            return SyncResult(status="not_linked", problem=refused.detail)
        await session.commit()
        api = ReportingClient(http, token)
        try:
            chosen = choose_types(await api.report_types(), moment)
            remote = await api.jobs()
            jobs = await _ensure_jobs(session, api, channel_id, chosen, remote, moment, result)
            await session.commit()
            for job in jobs:
                if result.downloaded + result.replaced >= limit:
                    result.remaining = True
                    break
                await _download_job(session, api, channel_id, job, limit, moment, result)
                await session.commit()
        except YoutubeError as error:
            await session.rollback()
            disabled = api_disabled(error)
            relink = error.status == 403 and not disabled
            if disabled:
                problem = API_DISABLED
            elif relink:
                problem = NEEDS_RELINK
            else:
                problem = (
                    f"YouTube Reporting API 回覆 {error.status} {error.reason}：{error.message}"
                )
            await _record_problem(session, problem[:1000], moment)
            # What was downloaded before the refusal is committed; the next run continues.
            result.status = "needs_relink" if relink else "partial"
            result.problem = problem
            return result
        except httpx.HTTPError as error:
            await session.rollback()
            problem = f"連不到 YouTube Reporting API：{type(error).__name__}"
            await _record_problem(session, problem, moment)
            result.status = "partial"
            result.problem = problem
            return result
    state = await state_row(session)
    state.attempted_at = moment
    state.chosen_types = chosen
    state.problem = None
    result.chosen_types = chosen
    if result.remaining:
        result.status = "partial"
    else:
        state.synced_at = moment
    result.synced_at = state.synced_at
    await session.commit()
    return result


async def _ensure_jobs(
    session: AsyncSession,
    api: ReportingClient,
    channel_id: str,
    chosen: dict[str, str],
    remote: list[dict[str, Any]],
    moment: datetime,
    result: SyncResult,
) -> list[VideoYoutubeReportJob]:
    """A job for every chosen type, and every job YouTube still has for one of the families
    (an older version keeps producing for three months after it is deprecated)."""
    by_type: dict[str, dict[str, Any]] = {}
    for job in remote:
        type_id = str(job.get("reportTypeId") or "")
        if family_of(type_id) and job.get("id") and not job.get("systemManaged"):
            by_type.setdefault(type_id, job)
    for type_id in chosen.values():
        if type_id in by_type:
            continue
        made = await api.create_job(type_id, f"{JOB_PREFIX}{type_id}"[:100])
        if made is None:
            # Made meanwhile, by another run or by hand: read the list again for it.
            for job in await api.jobs():
                if job.get("reportTypeId") == type_id and job.get("id"):
                    by_type[type_id] = job
                    break
            continue
        by_type[type_id] = made
        result.jobs_created.append(type_id)
    rows: list[VideoYoutubeReportJob] = []
    for type_id, job in sorted(by_type.items()):
        job_id = str(job["id"])[:64]
        row = await session.get(VideoYoutubeReportJob, job_id)
        if row is None:
            row = VideoYoutubeReportJob(
                job_id=job_id,
                channel_id=channel_id,
                report_type_id=type_id[:100],
                name=str(job.get("name") or type_id)[:100],
                recorded_at=moment,
            )
            session.add(row)
        row.created_at = parse_time(job.get("createTime"))
        row.expire_at = parse_time(job.get("expireTime"))
        rows.append(row)
    await session.flush()
    return rows


async def _download_job(
    session: AsyncSession,
    api: ReportingClient,
    channel_id: str,
    job: VideoYoutubeReportJob,
    limit: int,
    moment: datetime,
    result: SyncResult,
) -> None:
    listed = await api.reports(job.job_id, await _latest_created(session, job.job_id))
    usable = [
        report
        for report in listed
        if report.get("id")
        and report.get("downloadUrl")
        and parse_time(report.get("startTime"))
        and parse_time(report.get("endTime"))
        and parse_time(report.get("createTime"))
    ]
    # Oldest first, so a run that stops at the limit leaves ``createdAfter`` where it stopped.
    usable.sort(key=lambda report: (parse_time(report.get("createTime")), str(report.get("id"))))
    kept = set(
        await session.scalars(
            select(VideoYoutubeReport.report_id).where(
                VideoYoutubeReport.report_id.in_([str(report["id"]) for report in usable])
            )
        )
    )
    for report in usable:
        if str(report["id"]) in kept:
            continue
        if result.downloaded + result.replaced >= limit:
            result.remaining = True
            return
        try:
            content = await api.download(str(report["downloadUrl"]))
        except ReportRefused:
            result.skipped += 1
            continue
        outcome = await _keep_report(
            session, channel_id=channel_id, job=job, report=report, content=content, now=moment
        )
        if outcome == "new":
            result.downloaded += 1
        elif outcome == "replaced":
            result.replaced += 1
        else:
            result.skipped += 1
        await session.flush()


# --- what a video tool reads ----------------------------------------------------------------


async def overview(session: AsyncSession, now: datetime | None = None) -> dict[str, Any]:
    moment = now or datetime.now(UTC)
    await forget_other_channels(session)
    row = await connection.connection_row(session)
    state = await state_row(session)
    is_linked = connection.linked(row)
    coverage = (
        await session.execute(
            select(
                VideoYoutubeReport.report_type_id,
                func.count(VideoYoutubeReport.id),
                func.min(VideoYoutubeReport.day),
                func.max(VideoYoutubeReport.day),
                func.sum(VideoYoutubeReport.row_count),
            ).group_by(VideoYoutubeReport.report_type_id)
        )
    ).all()
    newest_columns: dict[str, list[str]] = {}
    for type_id, *_ in coverage:
        columns = await session.scalar(
            select(VideoYoutubeReport.columns)
            .where(VideoYoutubeReport.report_type_id == type_id)
            .order_by(VideoYoutubeReport.day.desc())
            .limit(1)
        )
        newest_columns[str(type_id)] = list(columns or [])
    jobs = {job.report_type_id: job for job in await session.scalars(select(VideoYoutubeReportJob))}
    reports = [
        {
            "family": family_of(str(type_id)),
            "report_type_id": str(type_id),
            "about": FAMILIES.get(family_of(str(type_id)) or "", ""),
            "job_id": jobs[str(type_id)].job_id if str(type_id) in jobs else None,
            "days": int(days),
            "first_day": first.isoformat() if first else None,
            "last_day": last.isoformat() if last else None,
            "rows": int(total or 0),
            "columns": newest_columns.get(str(type_id), []),
        }
        for type_id, days, first, last, total in sorted(coverage, key=lambda item: str(item[0]))
    ]
    waiting = [
        {
            "family": family_of(job.report_type_id),
            "report_type_id": job.report_type_id,
            "job_id": job.job_id,
            "job_created_at": job.created_at,
        }
        for job in jobs.values()
        if job.report_type_id not in {item["report_type_id"] for item in reports}
    ]
    due = state.synced_at is None or moment - state.synced_at >= SYNC_EVERY
    videos = [
        {
            "video_id": project.youtube_video_id,
            "slug": project.slug,
            "title": project.title,
            "category": project.category,
            "format": project.format,
            "shorts": project.shorts_line is not None,
            "series": project.series_slug,
            "episode": project.episode_number,
            "published_at": project.youtube_publish_at,
            "removed_at": project.youtube_removed_at,
        }
        for project in await session.scalars(
            select(VideoProject)
            .where(VideoProject.youtube_video_id.is_not(None))
            .order_by(VideoProject.youtube_publish_at.desc().nulls_last())
            .limit(2000)
        )
    ]
    result = {
        "linked": is_linked,
        "channel_id": row.channel_id if is_linked else None,
        "channel_title": row.channel_title if is_linked else None,
        "analytics_granted": connection.analytics_granted(row),
        "synced_at": state.synced_at,
        "attempted_at": state.attempted_at,
        "sync_due": due,
        "problem": state.problem
        or (None if not is_linked or connection.analytics_granted(row) else NEEDS_RELINK)
        or (None if is_linked else NOT_LINKED),
        "families": FAMILIES,
        "reports": reports,
        "waiting_for_first_report": waiting,
        "videos": videos,
        "day_timezone": "America/Los_Angeles",
        "policy": POLICY_NOTE,
    }
    await session.commit()
    return result


@dataclass
class Rows:
    report_type_id: str
    columns: list[str]
    rows: list[list[str]]
    days: list[str]
    truncated: bool


async def _types_for(session: AsyncSession, report: str) -> list[str]:
    """The report type ids a request names: one id, or every stored version of a family,
    newest version first."""
    stored = list(await session.scalars(select(VideoYoutubeReport.report_type_id).distinct()))
    if report in stored:
        return [report]
    if report not in FAMILIES:
        raise Refused(
            422,
            "video_youtube_report_unknown",
            f"沒有這種報表：{report}；可用的有 {', '.join(FAMILIES)}",
        )
    versions = [type_id for type_id in stored if family_of(type_id) == report]
    return sorted(versions, key=version_of, reverse=True)


async def rows(
    session: AsyncSession,
    *,
    report: str,
    start: date,
    end: date,
    video_ids: Sequence[str] = (),
    output: Literal["csv", "json"] = "json",
) -> Rows:
    """The rows of ``report`` for the days ``start`` to ``end`` (Pacific, both included).
    When two versions of a family cover one day, the newer version's file is the one used;
    a column a day's file lacks is empty in its rows."""
    if end < start:
        raise Refused(422, "video_youtube_report_span", "end 早於 start")
    if (end - start).days + 1 > MAX_SPAN_DAYS:
        raise Refused(422, "video_youtube_report_span", f"一次最多 {MAX_SPAN_DAYS} 天，請分段讀")
    wanted = {video_id for video_id in video_ids if video_id}
    if len(wanted) > MAX_VIDEO_IDS or any(not VIDEO_ID.match(item) for item in wanted):
        raise Refused(
            422,
            "video_youtube_report_videos",
            f"video_id 最多 {MAX_VIDEO_IDS} 個，格式要像 YouTube 的影片 id",
        )
    await forget_other_channels(session)
    types = await _types_for(session, report)
    files = list(
        await session.scalars(
            select(VideoYoutubeReport)
            .where(
                VideoYoutubeReport.report_type_id.in_(types),
                VideoYoutubeReport.day >= start,
                VideoYoutubeReport.day <= end,
            )
            .order_by(VideoYoutubeReport.day)
        )
    )
    rank = {type_id: index for index, type_id in enumerate(types)}
    by_day: dict[date, VideoYoutubeReport] = {}
    for item in files:
        current = by_day.get(item.day)
        if current is None or rank[item.report_type_id] < rank[current.report_type_id]:
            by_day[item.day] = item
    chosen = [by_day[day] for day in sorted(by_day)]
    columns: list[str] = []
    for item in sorted(
        chosen, key=lambda value: (rank[value.report_type_id], -value.day.toordinal())
    ):
        for name in item.columns:
            if name not in columns:
                columns.append(name)
    cap = MAX_ROWS[output]
    found: list[list[str]] = []
    truncated = False
    for item in chosen:
        reader = csv.reader(
            io.StringIO(gzip.decompress(item.content_gzip).decode("utf-8-sig", errors="replace"))
        )
        header = [name.strip() for name in next(reader, [])]
        position = {name: index for index, name in enumerate(header)}
        video_at = position.get("video_id")
        for line in reader:
            if not line:
                continue
            if wanted and (
                video_at is None or video_at >= len(line) or line[video_at] not in wanted
            ):
                continue
            if len(found) >= cap:
                truncated = True
                break
            found.append(
                [
                    line[position[name]] if name in position and position[name] < len(line) else ""
                    for name in columns
                ]
            )
        if truncated:
            break
    await session.commit()
    return Rows(
        report_type_id=types[0] if types else report,
        columns=columns,
        rows=found,
        days=[item.day.isoformat() for item in chosen],
        truncated=truncated,
    )


def as_csv(result: Rows) -> str:
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(result.columns)
    writer.writerows(result.rows)
    return out.getvalue()
