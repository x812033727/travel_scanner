"""The daily AI and tech news brief, one request a day
(.agents/skills/youtube-video/references/daily-brief.md).

Once the Asia/Taipei hour in ``daily_brief_hour`` comes, the first time the worker asks for the
next brief the server files the previous day's (by ``news_date``, the day the news happened):
the published zh-TW lifestyle articles of that day carrying the ai-news or tech-news topic or
one of their sub-topics, newest first. A day with fewer than ``daily_brief_min_stories`` of
them is filed as skipped, with the reason and an audit row, so the page shows why no video came;
a skipped day is never filed again. The worker starts the oldest queued day under the slug the
row names, ``daily-ai-YYYYMMDD``, and reports it done once its upload is confirmed. A queued day
the worker never started within two days is cancelled as stale instead of made: yesterday's
news a week late is no brief.

Nothing here asks for the owner: the switch on the settings tab is the owner's one decision.
The router turns ``RequestRefused`` into the API's problem response.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from hashlib import sha256
from typing import cast
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.guides.models import GuideArticle, GuideArticleTopic, GuideSearchEntry
from app.guides.taxonomy import topic_ids_including_children
from app.models import AdminAuditLog, VideoProject, VideoToolToken
from app.video_automation import topics
from app.video_automation.judge import DAILY_BRIEF_SLUG_PREFIX
from app.video_automation.models import VideoAutomationSettings, VideoDailyBriefRequest
from app.video_automation.requests import RequestRefused
from app.video_automation.schemas import DailyBriefRequestOut, DailyBriefStatus, DailyBriefStory
from app.video_automation.settings import daily_brief_values

ZONE = ZoneInfo("Asia/Taipei")
# The site's news topics a brief retells, each with its sub-topics.
NEWS_TOPICS = ("ai-news", "tech-news")
# The most stories one brief is handed; the writer keeps five to eight of them.
MAX_STORIES = 12
# A queued day older than this many days before today (Taipei) is cancelled, not made.
STALE_DAYS = 2
STALE_REASON = "stale"
LIST_LIMIT = 30


def slug_for(news_date: date) -> str:
    return f"{DAILY_BRIEF_SLUG_PREFIX}{news_date:%Y%m%d}"


def _now() -> datetime:
    return datetime.now(UTC)


async def _stories(session: AsyncSession, slugs: list[str]) -> list[DailyBriefStory]:
    """The articles among ``slugs`` the site still serves, in ``slugs``' order."""
    if not slugs:
        return []
    rows = await session.execute(
        topics.published_life(GuideArticle.slug, GuideArticle.news_date, GuideSearchEntry).where(
            GuideArticle.slug.in_(slugs)
        )
    )
    found = {
        slug: DailyBriefStory(
            slug=slug,
            title=entry.title,
            description=entry.description,
            url=f"{topics.SITE_URL}/{slug}",
            news_date=news_date,
        )
        for slug, news_date, entry in rows
        if news_date is not None
    }
    return [found[slug] for slug in slugs if slug in found]


async def request_view(
    session: AsyncSession,
    row: VideoDailyBriefRequest,
    youtube_video_id: str | None = None,
    dropped_at: datetime | None = None,
) -> DailyBriefRequestOut:
    """The request as the page and the worker see it, with its stories as the site serves them
    now: started and on YouTube reads as done, started and dropped by the owner as dropped."""
    status = row.status
    if row.status == "started" and youtube_video_id:
        status = "done"
    elif row.status == "started" and dropped_at is not None:
        status = "dropped"
    guides = list(row.source_guides or [])
    return DailyBriefRequestOut(
        id=row.id,
        news_date=row.news_date,
        slug=row.slug,
        status=cast(DailyBriefStatus, status),
        skip_reason=row.skip_reason,
        source_guides=guides,
        stories=await _stories(session, guides),
        created_at=row.created_at,
        started_at=row.started_at,
        finished_at=row.finished_at,
        cancelled_at=row.cancelled_at,
    )


async def day_articles(session: AsyncSession, news_date: date) -> list[str]:
    """The slugs of the day's published zh-TW news articles, newest first, at most
    ``MAX_STORIES``: the lifestyle articles the site serves whose ``news_date`` is the day and
    which carry ai-news, tech-news or a sub-topic of either."""
    topic_ids: list[UUID] = []
    for slug in NEWS_TOPICS:
        topic_ids.extend(await topic_ids_including_children(session, slug))
    if not topic_ids:
        return []
    rows = await session.execute(
        topics.published_life(GuideArticle.slug)
        .where(
            GuideArticle.news_date == news_date,
            GuideArticle.id.in_(
                select(GuideArticleTopic.article_id).where(
                    GuideArticleTopic.topic_id.in_(topic_ids)
                )
            ),
        )
        .order_by(GuideSearchEntry.published_at.desc(), GuideArticle.slug)
        .limit(MAX_STORIES)
    )
    return list(dict.fromkeys(slug for (slug,) in rows))


async def _lock_day(session: AsyncSession, news_date: date) -> None:
    """Two lanes asking at once both see no row for the day before either inserts; the
    transaction-scoped lock makes the second wait and then find the first. SQLite (the unit
    tests) has no advisory locks and one writer anyway."""
    if session.get_bind().dialect.name != "postgresql":
        return
    key = int.from_bytes(
        sha256(f"video-daily-brief:{news_date.isoformat()}".encode()).digest()[:8], signed=True
    )
    await session.execute(select(func.pg_advisory_xact_lock(key)))


async def _file_day(
    session: AsyncSession, settings: VideoAutomationSettings, news_date: date, now: datetime
) -> None:
    """File the day as queued, or as skipped with too few stories. The caller holds the day's
    lock and commits."""
    guides = await day_articles(session, news_date)
    minimum = daily_brief_values(settings).daily_brief_min_stories
    row = VideoDailyBriefRequest(
        id=uuid4(),
        news_date=news_date,
        slug=slug_for(news_date),
        source_guides=guides,
        status="queued",
        created_at=now,
        updated_at=now,
    )
    if len(guides) < minimum:
        row.status = "skipped"
        row.skip_reason = (
            f"{news_date.isoformat()} 只有 {len(guides)} 則已發布的 AI／科技新聞，"
            f"少於設定的 {minimum} 則，這天不做快報"
        )
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action="video_daily_brief_skipped",
                target=f"video-daily-brief:{row.id}",
                metadata_json={
                    "news_date": news_date.isoformat(),
                    "stories": len(guides),
                    "min_stories": minimum,
                },
            )
        )
    session.add(row)


async def next_request(
    session: AsyncSession, now: datetime | None = None
) -> DailyBriefRequestOut | None:
    """The oldest queued brief the worker should make, filing yesterday's first once the hour
    has come; None while the automation or the brief is switched off.

    Yesterday is the day before today in Asia/Taipei, whatever the server's clock zone. Before
    the hour nothing is filed, but a day filed earlier and not yet started is still handed out.
    """
    moment = now or _now()
    settings = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    if settings is None or not settings.enabled:
        return None
    brief = daily_brief_values(settings)
    if not brief.daily_brief_enabled:
        return None
    local = moment.astimezone(ZONE)
    today = local.date()
    changed = False
    if local.hour >= brief.daily_brief_hour:
        target = today - timedelta(days=1)
        await _lock_day(session, target)
        filed = await session.scalar(
            select(VideoDailyBriefRequest.id).where(VideoDailyBriefRequest.news_date == target)
        )
        if filed is None:
            await _file_day(session, settings, target, moment)
            changed = True
    cutoff = today - timedelta(days=STALE_DAYS)
    stale = (
        await session.scalars(
            select(VideoDailyBriefRequest)
            .where(
                VideoDailyBriefRequest.status == "queued",
                VideoDailyBriefRequest.news_date < cutoff,
            )
            .with_for_update()
        )
    ).all()
    for old in stale:
        old.status = "cancelled"
        old.skip_reason = STALE_REASON
        old.cancelled_at = moment
        old.updated_at = moment
        changed = True
    if changed:
        await session.commit()
    row = await session.scalar(
        select(VideoDailyBriefRequest)
        .where(
            VideoDailyBriefRequest.status == "queued",
            VideoDailyBriefRequest.news_date >= cutoff,
        )
        .order_by(VideoDailyBriefRequest.news_date.asc())
        .limit(1)
    )
    return await request_view(session, row) if row is not None else None


async def list_requests(session: AsyncSession) -> list[DailyBriefRequestOut]:
    """The latest days, newest first, with what became of the video each one started."""
    rows = await session.execute(
        select(VideoDailyBriefRequest, VideoProject.youtube_video_id, VideoProject.dropped_at)
        .outerjoin(VideoProject, VideoProject.slug == VideoDailyBriefRequest.slug)
        .order_by(VideoDailyBriefRequest.news_date.desc())
        .limit(LIST_LIMIT)
    )
    return [
        await request_view(session, row, youtube, dropped) for row, youtube, dropped in rows.all()
    ]


async def _request(session: AsyncSession, request_id: UUID) -> VideoDailyBriefRequest:
    # Locked: two lanes may act on one request at once.
    row = await session.scalar(
        select(VideoDailyBriefRequest)
        .where(VideoDailyBriefRequest.id == request_id)
        .with_for_update()
    )
    if row is None:
        raise RequestRefused(404, "video_daily_brief_not_found", "找不到這一天的新聞快報請求")
    return row


async def start_request(
    session: AsyncSession, token: VideoToolToken, request_id: UUID, slug: str
) -> DailyBriefRequestOut:
    """The worker claims a queued day under the day's own slug. The same claim sent again is
    answered as the first was (client.mjs sends it again after a lost connection or a 5xx)."""
    row = await _request(session, request_id)
    if slug != row.slug:
        raise RequestRefused(
            409,
            "video_daily_brief_slug_mismatch",
            f"這一天的快報只能用 {row.slug} 開始，不能用 {slug}",
        )
    if row.status == "started" and row.started_by_token_id == token.id:
        return await request_view(session, row)
    if row.status != "queued":
        raise RequestRefused(
            409, "video_daily_brief_not_queued", "這一天的快報不在排隊中，不能開始"
        )
    now = _now()
    row.status = "started"
    row.started_at = now
    row.updated_at = now
    row.started_by_token_id = token.id
    await session.commit()
    return await request_view(session, row)


async def finish_request(session: AsyncSession, request_id: UUID) -> DailyBriefRequestOut:
    """The worker reports the day's video confirmed for upload. Said twice, the second answer
    is the first: the report may be sent again after a lost answer."""
    row = await _request(session, request_id)
    if row.status == "done":
        return await request_view(session, row)
    if row.status != "started":
        raise RequestRefused(
            409, "video_daily_brief_not_started", "這一天的快報還沒開始做，不能標成完成"
        )
    now = _now()
    row.status = "done"
    row.finished_at = now
    row.updated_at = now
    await session.commit()
    return await request_view(session, row)
