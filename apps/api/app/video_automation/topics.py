"""Candidate topics for the next draft: the site's own recent articles first, then the web.

The owner chose on 2026-09-25 to start from what the site has already published and checked
(the hourly news and the lifestyle articles), and to fill the gaps with a Brave search. The
planner model picks among these against the topic scope and the list to avoid; this module
only gathers them.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from urllib.parse import urlparse

import httpx
from redis.asyncio import Redis
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.guides.models import GuideArticle, GuideArticleLocale, GuideSearchEntry
from app.hotspots.guides import consume_search_budget
from app.video_automation.models import VideoAutomationSettings
from app.video_automation.schemas import TopicsOut, TopicView

SITE_DAYS = 14
SITE_LIMIT = 60
# Each topic word is one Brave query; they share the guide search's daily Brave budget.
SEARCH_QUERIES = 5
SEARCH_RESULTS = 10
# Lifestyle articles are read at /guides/<slug>; /life is only the section's list page.
SITE_URL = "https://mokaair.com/zh-TW/guides"


async def site_topics(session: AsyncSession, now: datetime | None = None) -> list[TopicView]:
    """The lifestyle section's zh-TW articles published or dated in the last two weeks."""
    since = (now or datetime.now(UTC)) - timedelta(days=SITE_DAYS)
    rows = await session.execute(
        select(GuideArticle.slug, GuideArticle.news_date, GuideSearchEntry)
        .join(GuideSearchEntry, GuideSearchEntry.article_id == GuideArticle.id)
        .join(
            GuideArticleLocale,
            (GuideArticleLocale.article_id == GuideArticle.id)
            & (GuideArticleLocale.locale == GuideSearchEntry.locale),
        )
        .where(
            GuideArticle.kind == "life",
            GuideArticle.is_active.is_(True),
            GuideSearchEntry.locale == "zh-TW",
            GuideArticleLocale.published_version == GuideSearchEntry.revision_version,
            or_(GuideSearchEntry.published_at >= since, GuideArticle.news_date >= since.date()),
        )
        .order_by(GuideSearchEntry.published_at.desc())
        .limit(SITE_LIMIT)
    )
    return [
        TopicView(
            source="site",
            title=entry.title,
            summary=entry.description,
            url=f"{SITE_URL}/{slug}",
            slug=slug,
            date=(news_date or entry.published_at.date()).isoformat(),
        )
        for slug, news_date, entry in rows
    ]


async def search_topics(
    runtime: Settings,
    redis: Redis,
    words: list[str],
    client: httpx.AsyncClient | None = None,
) -> tuple[list[TopicView], list[str]]:
    """Brave results from the past week for each topic word, within the daily Brave budget."""
    notes: list[str] = []
    if not (runtime.hotspot_guide_brave_enabled and runtime.hotspot_guide_brave_api_key):
        return [], ["Brave 搜尋沒有設定或已關閉"]
    owned = client is None
    http = client or httpx.AsyncClient(timeout=10)
    topics: list[TopicView] = []
    seen: set[str] = set()
    try:
        for word in words[:SEARCH_QUERIES]:
            if not await consume_search_budget(
                redis, "brave", runtime.hotspot_guide_brave_daily_search_budget
            ):
                notes.append("今天的 Brave 搜尋額度已用完")
                break
            try:
                response = await http.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    headers={
                        "X-Subscription-Token": runtime.hotspot_guide_brave_api_key,
                        "Accept": "application/json",
                    },
                    params={
                        "q": word,
                        "count": SEARCH_RESULTS,
                        "freshness": "pw",
                        "search_lang": "zh-hant",
                    },
                )
                response.raise_for_status()
                results = response.json().get("web", {}).get("results", [])
            except (httpx.HTTPError, ValueError) as error:
                notes.append(f"Brave 搜尋「{word}」失敗：{type(error).__name__}")
                continue
            for item in results:
                url = str(item.get("url") or "")
                if urlparse(url).scheme != "https" or url in seen:
                    continue
                seen.add(url)
                topics.append(
                    TopicView(
                        source="search",
                        title=str(item.get("title") or "").strip()[:300],
                        summary=str(item.get("description") or "").strip()[:500],
                        url=url,
                        date=str(item.get("age") or "")[:40] or None,
                    )
                )
    finally:
        if owned:
            await http.aclose()
    return topics, notes


async def gather_topics(
    session: AsyncSession,
    runtime: Settings,
    redis: Redis,
    row: VideoAutomationSettings,
    client: httpx.AsyncClient | None = None,
) -> TopicsOut:
    topics: list[TopicView] = []
    notes: list[str] = []
    if row.topic_from_site:
        topics.extend(await site_topics(session))
    else:
        notes.append("設定關閉了站上文章這個來源")
    if row.topic_from_search:
        found, search_notes = await search_topics(runtime, redis, list(row.topic_scope), client)
        topics.extend(found)
        notes.extend(search_notes)
    else:
        notes.append("設定關閉了 Brave 搜尋這個來源")
    return TopicsOut(topics=topics, notes=notes)
