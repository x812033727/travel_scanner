from __future__ import annotations

import hashlib
import ipaddress
import re
from collections.abc import Awaitable
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any, cast
from urllib.parse import parse_qs, urlparse, urlunparse
from uuid import UUID

import httpx
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import ColumnElement, Delete, Select, and_, case, delete, func, or_, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.i18n import LOCALES, Locale
from app.models import (
    HotspotGuide,
    HotspotGuideClickDaily,
    HotspotLocalization,
    TravelHotspot,
)
from app.problems import AppError
from app.providers.usage_meter import record_youtube_request

PUBLIC_HOTSPOT_STATUSES = ("approved", "auto_approved")
SEARCH_SUFFIXES: dict[Locale, str] = {
    "en": "travel guide things to do",
    "ja": "観光 旅行 見どころ",
    "ko": "여행 관광 후기",
    "zh-TW": "旅遊 景點 部落格",
    "zh-CN": "旅游 景点 攻略",
}
YOUTUBE_LANGUAGE: dict[Locale, str] = {
    "en": "en",
    "ja": "ja",
    "ko": "ko",
    "zh-TW": "zh-Hant",
    "zh-CN": "zh-Hans",
}
BRAVE_LANGUAGE: dict[Locale, str] = {
    "en": "en",
    "ja": "ja",
    "ko": "ko",
    "zh-TW": "zh-hant",
    "zh-CN": "zh-hans",
}


@dataclass(frozen=True)
class GuideCandidate:
    content_type: str
    provider: str
    locale: Locale
    title: str
    creator_name: str
    canonical_url: str
    provider_content_id: str | None = None
    thumbnail_url: str | None = None
    summary: str | None = None
    published_at: datetime | None = None
    duration_seconds: int | None = None
    view_count: int | None = None
    language_confidence: Decimal = Decimal("0.750")
    discovery_rank: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


def canonical_external_url(value: str) -> str:
    parsed = urlparse(value.strip())
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise AppError(422, "hotspot_guide_url_invalid", "介紹連結必須是公開 HTTPS URL")
    hostname = parsed.hostname.casefold().rstrip(".")
    if hostname in {"localhost", "localhost.localdomain"}:
        raise AppError(422, "hotspot_guide_url_invalid", "介紹連結不可指向內部網路")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        address = None
    if address and not address.is_global:
        raise AppError(422, "hotspot_guide_url_invalid", "介紹連結不可指向內部網路")
    port = f":{parsed.port}" if parsed.port and parsed.port != 443 else ""
    path = parsed.path or "/"
    return urlunparse(("https", f"{hostname}{port}", path, "", parsed.query, ""))


def youtube_video_id(value: str) -> str | None:
    parsed = urlparse(value)
    host = (parsed.hostname or "").casefold()
    if host == "youtu.be":
        candidate = parsed.path.strip("/").split("/")[0]
    elif host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [""])[0]
        elif parsed.path.startswith(("/shorts/", "/embed/")):
            candidate = parsed.path.split("/")[2]
        else:
            return None
    else:
        return None
    return (
        candidate
        if len(candidate) == 11 and candidate.replace("-", "").replace("_", "").isalnum()
        else None
    )


def _parse_youtube_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def classify_content_locale(
    text: str, requested: Locale, declared: str | None = None
) -> tuple[Locale, Decimal]:
    normalized = (declared or "").casefold().replace("_", "-")
    if normalized.startswith("ja"):
        return "ja", Decimal("1.000")
    if normalized.startswith("ko"):
        return "ko", Decimal("1.000")
    if normalized.startswith("zh-hant") or normalized in {"zh-tw", "zh-hk"}:
        return "zh-TW", Decimal("1.000")
    if normalized.startswith("zh-hans") or normalized in {"zh-cn", "zh-sg"}:
        return "zh-CN", Decimal("1.000")
    if normalized.startswith("en"):
        return "en", Decimal("1.000")
    if re.search(r"[\uac00-\ud7af]", text):
        return "ko", Decimal("0.900")
    if re.search(r"[\u3040-\u30fa\u30fd-\u30ff]", text):
        return "ja", Decimal("0.900")
    if re.search(r"[\u4e00-\u9fff]", text):
        return requested, Decimal("0.700")
    letters = [character for character in text if character.isalpha()]
    if letters and sum(character.isascii() for character in letters) / len(letters) >= 0.85:
        return "en", Decimal("0.700")
    return requested, Decimal("0.500")


class YouTubeGuideProvider:
    def __init__(
        self,
        api_key: str,
        client: httpx.AsyncClient | None = None,
        redis: Redis | None = None,
    ) -> None:
        self.api_key = api_key
        self._external_client = client
        self._client = client or httpx.AsyncClient(timeout=10)
        self._redis = redis

    async def close(self) -> None:
        if self._external_client is None:
            await self._client.aclose()

    async def search(self, query: str, locale: Locale, limit: int = 10) -> list[GuideCandidate]:
        if self._redis is not None:
            await record_youtube_request(self._redis, "search_list")
        response = await self._client.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "key": self.api_key,
                "part": "snippet",
                "type": "video",
                "order": "viewCount",
                "maxResults": min(limit, 25),
                "relevanceLanguage": YOUTUBE_LANGUAGE[locale],
                "q": query,
            },
        )
        response.raise_for_status()
        search_items = response.json().get("items", [])
        ids = [item.get("id", {}).get("videoId") for item in search_items]
        ids = [item for item in ids if isinstance(item, str)]
        if not ids:
            return []
        if self._redis is not None:
            await record_youtube_request(self._redis, "videos_list")
        details = await self._client.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "key": self.api_key,
                "part": "snippet,statistics,contentDetails,status",
                "id": ",".join(ids),
                "hl": YOUTUBE_LANGUAGE[locale],
            },
        )
        details.raise_for_status()
        by_id = {item["id"]: item for item in details.json().get("items", [])}
        candidates: list[GuideCandidate] = []
        for rank, video_id in enumerate(ids, start=1):
            item = by_id.get(video_id)
            if not item or item.get("status", {}).get("privacyStatus") != "public":
                continue
            snippet = item.get("snippet", {})
            thumbnails = snippet.get("thumbnails", {})
            thumbnail = thumbnails.get("medium") or thumbnails.get("default") or {}
            detected_locale, confidence = classify_content_locale(
                f"{snippet.get('title', '')} {snippet.get('description', '')}",
                locale,
                snippet.get("defaultAudioLanguage") or snippet.get("defaultLanguage"),
            )
            candidates.append(
                GuideCandidate(
                    content_type="video",
                    provider="youtube",
                    locale=detected_locale,
                    title=str(snippet.get("title") or "").strip(),
                    creator_name=str(snippet.get("channelTitle") or "YouTube").strip(),
                    canonical_url=f"https://www.youtube.com/watch?v={video_id}",
                    provider_content_id=video_id,
                    thumbnail_url=thumbnail.get("url"),
                    summary=None,
                    published_at=_parse_youtube_datetime(snippet.get("publishedAt")),
                    view_count=int(item.get("statistics", {}).get("viewCount", 0)),
                    language_confidence=confidence,
                    discovery_rank=rank,
                )
            )
        return candidates

    async def import_video(self, url: str, locale: Locale) -> GuideCandidate:
        video_id = youtube_video_id(url)
        if not video_id:
            raise AppError(422, "hotspot_guide_youtube_url_invalid", "無法辨識 YouTube 影片 ID")
        if self._redis is not None:
            await record_youtube_request(self._redis, "videos_list")
        response = await self._client.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "key": self.api_key,
                "part": "snippet,statistics,status",
                "id": video_id,
                "hl": YOUTUBE_LANGUAGE[locale],
            },
        )
        response.raise_for_status()
        items = response.json().get("items", [])
        if not items or items[0].get("status", {}).get("privacyStatus") != "public":
            raise AppError(404, "hotspot_guide_not_found", "YouTube 影片不存在或未公開")
        item = items[0]
        snippet = item.get("snippet", {})
        thumbnails = snippet.get("thumbnails", {})
        thumbnail = thumbnails.get("medium") or thumbnails.get("default") or {}
        detected_locale, confidence = classify_content_locale(
            f"{snippet.get('title', '')} {snippet.get('description', '')}",
            locale,
            snippet.get("defaultAudioLanguage") or snippet.get("defaultLanguage"),
        )
        return GuideCandidate(
            content_type="video",
            provider="youtube",
            locale=detected_locale,
            title=str(snippet.get("title") or "").strip(),
            creator_name=str(snippet.get("channelTitle") or "YouTube").strip(),
            canonical_url=f"https://www.youtube.com/watch?v={video_id}",
            provider_content_id=video_id,
            thumbnail_url=thumbnail.get("url"),
            published_at=_parse_youtube_datetime(snippet.get("publishedAt")),
            view_count=int(item.get("statistics", {}).get("viewCount", 0)),
            language_confidence=confidence,
        )


class BraveGuideProvider:
    def __init__(self, api_key: str, client: httpx.AsyncClient | None = None) -> None:
        self.api_key = api_key
        self._external_client = client
        self._client = client or httpx.AsyncClient(timeout=10)

    async def close(self) -> None:
        if self._external_client is None:
            await self._client.aclose()

    async def search(self, query: str, locale: Locale, limit: int = 10) -> list[GuideCandidate]:
        response = await self._client.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers={"X-Subscription-Token": self.api_key, "Accept": "application/json"},
            params={"q": query, "count": min(limit, 20), "search_lang": BRAVE_LANGUAGE[locale]},
        )
        response.raise_for_status()
        candidates: list[GuideCandidate] = []
        for rank, item in enumerate(response.json().get("web", {}).get("results", []), start=1):
            try:
                url = canonical_external_url(str(item.get("url") or ""))
            except AppError:
                continue
            if youtube_video_id(url):
                continue
            detected_locale, confidence = classify_content_locale(
                f"{item.get('title', '')} {item.get('description', '')}", locale
            )
            candidates.append(
                GuideCandidate(
                    content_type="article",
                    provider="brave",
                    locale=detected_locale,
                    title=str(item.get("title") or "").strip(),
                    creator_name=urlparse(url).hostname or "Website",
                    canonical_url=url,
                    summary=str(item.get("description") or "").strip()[:500] or None,
                    language_confidence=confidence,
                    discovery_rank=rank,
                )
            )
        return candidates


async def _search_name(session: AsyncSession, hotspot: TravelHotspot, locale: Locale) -> str:
    localization = await session.scalar(
        select(HotspotLocalization).where(
            HotspotLocalization.hotspot_id == hotspot.id,
            HotspotLocalization.locale == locale,
        )
    )
    return localization.name if localization else hotspot.name


def manual_guide_filter() -> ColumnElement[bool]:
    """Rows an admin added by hand: provider ``manual`` or tagged in metadata (videos)."""
    return or_(
        HotspotGuide.provider == "manual",
        HotspotGuide.metadata_json["discovery_method"].as_string() == "manual",
    )


def not_manual_guide_filter() -> ColumnElement[bool]:
    discovery_method = HotspotGuide.metadata_json["discovery_method"].as_string()
    return and_(
        HotspotGuide.provider != "manual",
        or_(discovery_method.is_(None), discovery_method != "manual"),
    )


def stale_youtube_guides_delete(cutoff: datetime) -> Delete:
    """Delete YouTube rows whose metadata was never re-verified; manual picks are kept."""
    return delete(HotspotGuide).where(
        HotspotGuide.provider == "youtube",
        HotspotGuide.last_verified_at < cutoff,
        not_manual_guide_filter(),
    )


async def upsert_guide(
    session: AsyncSession, hotspot_id: UUID, candidate: GuideCandidate
) -> tuple[HotspotGuide, bool]:
    """Insert ``candidate`` or refresh the row that already stores its URL.

    Returns the row and whether it was newly created. A refreshed row keeps its
    locale and review status so re-discovery never undoes an admin decision.
    """
    now = datetime.now(UTC)
    existing = await session.scalar(
        select(HotspotGuide).where(
            HotspotGuide.hotspot_id == hotspot_id,
            HotspotGuide.canonical_url == candidate.canonical_url,
        )
    )
    if existing:
        existing.title = candidate.title
        existing.creator_name = candidate.creator_name
        existing.thumbnail_url = candidate.thumbnail_url
        existing.summary = candidate.summary
        existing.published_at = candidate.published_at
        existing.view_count = candidate.view_count
        existing.last_verified_at = now
        existing.metadata_expires_at = now + timedelta(days=7)
        existing.metadata_json = {**existing.metadata_json, **candidate.metadata}
        return existing, False
    guide = HotspotGuide(
        hotspot_id=hotspot_id,
        content_type=candidate.content_type,
        provider=candidate.provider,
        locale=candidate.locale,
        title=candidate.title,
        creator_name=candidate.creator_name,
        canonical_url=candidate.canonical_url,
        provider_content_id=candidate.provider_content_id,
        thumbnail_url=candidate.thumbnail_url,
        summary=candidate.summary,
        published_at=candidate.published_at,
        duration_seconds=candidate.duration_seconds,
        view_count=candidate.view_count,
        language_confidence=candidate.language_confidence,
        discovery_rank=candidate.discovery_rank,
        review_status="pending",
        last_verified_at=now,
        metadata_expires_at=now + timedelta(days=7),
        metadata_json=candidate.metadata,
    )
    session.add(guide)
    return guide, True


async def save_candidates(
    session: AsyncSession, hotspot_id: UUID, candidates: list[GuideCandidate]
) -> int:
    created = 0
    for candidate in candidates:
        if not candidate.title:
            continue
        _, is_new = await upsert_guide(session, hotspot_id, candidate)
        created += int(is_new)
    return created


async def discover_guides(
    session: AsyncSession,
    settings: Settings,
    hotspot: TravelHotspot,
    locales: list[Locale],
    *,
    client: httpx.AsyncClient | None = None,
    redis: Redis | None = None,
    automatic: bool = False,
) -> dict[str, Any]:
    report: dict[str, Any] = {"created": 0, "providers": {}, "errors": []}
    youtube = (
        YouTubeGuideProvider(settings.hotspot_guide_youtube_api_key, client, redis)
        if settings.hotspot_guide_youtube_enabled and settings.hotspot_guide_youtube_api_key
        else None
    )
    brave = (
        BraveGuideProvider(settings.hotspot_guide_brave_api_key, client)
        if settings.hotspot_guide_brave_enabled and settings.hotspot_guide_brave_api_key
        else None
    )
    try:
        for locale in locales:
            name = await _search_name(session, hotspot, locale)
            query = f"{name} {SEARCH_SUFFIXES[locale]}"
            for provider_name, provider in (("youtube", youtube), ("brave", brave)):
                if provider is None:
                    report["providers"][provider_name] = "not_configured"
                    continue
                limit = (
                    settings.hotspot_guide_youtube_daily_search_budget
                    if provider_name == "youtube" and automatic
                    else 100
                    if provider_name == "youtube"
                    else settings.hotspot_guide_brave_daily_search_budget
                )
                if redis is not None and not await consume_search_budget(
                    redis, provider_name, limit
                ):
                    report["providers"][provider_name] = "quota_exhausted"
                    continue
                try:
                    candidates = await provider.search(query, locale)
                    report["created"] += await save_candidates(session, hotspot.id, candidates)
                    report["providers"][provider_name] = "ready"
                except (httpx.HTTPError, KeyError, TypeError, ValueError, AppError) as exc:
                    report["errors"].append(
                        {"provider": provider_name, "locale": locale, "error": type(exc).__name__}
                    )
        await session.commit()
    finally:
        if youtube:
            await youtube.close()
        if brave:
            await brave.close()
    return report


async def consume_search_budget(redis: Redis, provider: str, limit: int) -> bool:
    key = f"hotspot-guide-quota:{provider}:{date.today().isoformat()}"
    script = (
        "local current=tonumber(redis.call('GET',KEYS[1]) or '0'); "
        "if current>=tonumber(ARGV[1]) then return -1 end; "
        "local n=redis.call('INCR',KEYS[1]); "
        "if n==1 then redis.call('EXPIRE',KEYS[1],172800) end; return n"
    )
    try:
        count = await cast(Awaitable[Any], redis.eval(script, 1, key, str(limit)))
    except RedisError:
        return False
    return int(count) >= 0


async def guide_quota_status(redis: Redis, settings: Settings) -> dict[str, Any]:
    day = date.today().isoformat()
    keys = [f"hotspot-guide-quota:{provider}:{day}" for provider in ("youtube", "brave")]
    try:
        used = await redis.mget(keys)
    except RedisError:
        used = [None, None]
    return {
        "youtube": {
            "used": int(used[0] or 0),
            "automatic_limit": settings.hotspot_guide_youtube_daily_search_budget,
            "manual_limit": 100,
        },
        "brave": {
            "used": int(used[1] or 0),
            "limit": settings.hotspot_guide_brave_daily_search_budget,
        },
    }


def guideless_hotspots_statement(limit: int) -> Select[tuple[TravelHotspot]]:
    """Hotspots that still have nothing for a visitor to watch or read.

    Verified rows come first because those are the only ones the planner can place on an
    itinerary, so a guide found for them is a guide someone will actually see.
    """
    has_guide = select(HotspotGuide.id).where(HotspotGuide.hotspot_id == TravelHotspot.id)
    return (
        select(TravelHotspot)
        .where(
            TravelHotspot.is_active.is_(True),
            TravelHotspot.review_status == "approved",
            ~has_guide.exists(),
        )
        .order_by(
            case((TravelHotspot.map_match_status == "verified", 0), else_=1),
            TravelHotspot.created_at,
        )
        .limit(limit)
    )


async def guideless_hotspots(session: AsyncSession, limit: int) -> list[TravelHotspot]:
    return list((await session.scalars(guideless_hotspots_statement(limit))).all())


async def backfill_guides_once(
    session: AsyncSession,
    settings: Settings,
    redis: Redis,
    *,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Work through the guide backlog a few hotspots at a time, inside the daily budget.

    Only the default locale is searched. Every extra locale costs another Brave call,
    and Brave's daily budget is the scarce one — spending it on breadth would leave most
    hotspots with nothing at all rather than giving each one a starting set.
    """
    if not settings.hotspot_guide_backfill_enabled or not settings.hotspot_guides_enabled:
        return {"skipped": True, "reason": "disabled"}
    hotspots = await guideless_hotspots(session, settings.hotspot_guide_backfill_batch_size)
    if not hotspots:
        return {"skipped": True, "reason": "nothing_pending"}
    report: dict[str, Any] = {"skipped": False, "attempted": 0, "created": 0, "exhausted": False}
    for hotspot in hotspots:
        outcome = await discover_guides(
            session,
            settings,
            hotspot,
            [cast(Locale, settings.hotspot_guide_backfill_locale)],
            client=client,
            redis=redis,
            automatic=True,
        )
        report["attempted"] += 1
        report["created"] += int(outcome["created"])
        providers = cast(dict[str, Any], outcome["providers"])
        configured = [name for name, state in providers.items() if state != "not_configured"]
        if configured and all(providers[name] == "quota_exhausted" for name in configured):
            report["exhausted"] = True
            break
    return report


def _guide_payload(guide: HotspotGuide, opens: int) -> dict[str, Any]:
    return {
        "id": str(guide.id),
        "type": guide.content_type,
        "provider": guide.provider,
        "locale": guide.locale,
        "title": guide.title,
        "creator_name": guide.creator_name,
        "thumbnail_url": guide.thumbnail_url,
        "summary": guide.summary,
        "published_at": guide.published_at.isoformat() if guide.published_at else None,
        "duration_seconds": guide.duration_seconds,
        "view_count": guide.view_count,
        "opens_30d": opens,
        "updated_at": guide.updated_at.isoformat(),
    }


async def list_guides(
    session: AsyncSession,
    hotspot_id: UUID,
    locale: Locale,
    content_type: str,
    include_other_languages: bool,
    limit_per_type: int,
) -> dict[str, Any]:
    hotspot = await session.scalar(
        select(TravelHotspot).where(
            TravelHotspot.id == hotspot_id,
            TravelHotspot.is_active.is_(True),
            TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
        )
    )
    if hotspot is None:
        raise AppError(404, "hotspot_not_found", "找不到這個景點")
    since = date.today() - timedelta(days=29)
    youtube_freshness = or_(
        HotspotGuide.provider != "youtube",
        manual_guide_filter(),
        HotspotGuide.last_verified_at >= datetime.now(UTC) - timedelta(days=30),
    )
    clicks = (
        select(
            HotspotGuideClickDaily.guide_id.label("guide_id"),
            func.sum(HotspotGuideClickDaily.unique_opens).label("opens"),
        )
        .where(HotspotGuideClickDaily.observed_on >= since)
        .group_by(HotspotGuideClickDaily.guide_id)
        .subquery()
    )
    locale_filter = [] if include_other_languages else [HotspotGuide.locale == locale]
    other_languages_available = bool(
        await session.scalar(
            select(func.count(HotspotGuide.id)).where(
                HotspotGuide.hotspot_id == hotspot_id,
                HotspotGuide.review_status == "approved",
                HotspotGuide.locale != locale,
                youtube_freshness,
            )
        )
    )

    async def section(kind: str) -> list[dict[str, Any]]:
        rows = (
            await session.execute(
                select(HotspotGuide, func.coalesce(clicks.c.opens, 0))
                .outerjoin(clicks, clicks.c.guide_id == HotspotGuide.id)
                .where(
                    HotspotGuide.hotspot_id == hotspot_id,
                    HotspotGuide.review_status == "approved",
                    HotspotGuide.content_type == kind,
                    youtube_freshness,
                    *locale_filter,
                )
                .order_by(
                    case((HotspotGuide.locale == locale, 0), else_=1),
                    HotspotGuide.view_count.desc().nullslast()
                    if kind == "video"
                    else func.coalesce(clicks.c.opens, 0).desc(),
                    HotspotGuide.discovery_rank.asc().nullslast(),
                )
                .limit(limit_per_type)
            )
        ).all()
        return [_guide_payload(guide, int(opens)) for guide, opens in rows]

    videos = await section("video") if content_type in {"all", "video"} else []
    articles = await section("article") if content_type in {"all", "article"} else []
    return {
        "hotspot_id": str(hotspot.id),
        "hotspot_name": hotspot.name,
        "locale": locale,
        "videos": videos,
        "articles": articles,
        "video_sort": "youtube_view_count",
        "article_sort": "travel_scanner_opens_30d_then_discovery",
        "other_languages_available": other_languages_available,
        "updated_at": max((item["updated_at"] for item in [*videos, *articles]), default=None),
    }


async def resolve_guide_open(
    session: AsyncSession, redis: Redis, guide_id: UUID, visitor: str
) -> str:
    guide = await session.scalar(
        select(HotspotGuide).where(
            HotspotGuide.id == guide_id, HotspotGuide.review_status == "approved"
        )
    )
    if guide is None:
        raise AppError(404, "hotspot_guide_not_found", "找不到這筆景點介紹")
    url = canonical_external_url(guide.canonical_url)
    day = date.today()
    digest = hashlib.sha256(visitor.encode()).hexdigest()
    try:
        fresh = await redis.set(
            f"hotspot-guide-open:{guide_id}:{day.isoformat()}:{digest}", "1", ex=86_400, nx=True
        )
    except RedisError:
        fresh = False
    if fresh:
        statement = pg_insert(HotspotGuideClickDaily).values(
            guide_id=guide_id, observed_on=day, unique_opens=1
        )
        statement = statement.on_conflict_do_update(
            constraint="uq_hotspot_guide_click_day",
            set_={
                "unique_opens": HotspotGuideClickDaily.unique_opens + 1,
                "updated_at": datetime.now(UTC),
            },
        )
        await session.execute(statement)
        await session.commit()
    return url


async def guide_coverage(session: AsyncSession) -> dict[str, Any]:
    rows = (
        await session.execute(
            select(
                TravelHotspot.id,
                TravelHotspot.name,
                HotspotGuide.locale,
                HotspotGuide.content_type,
                func.count(HotspotGuide.id),
            )
            .outerjoin(
                HotspotGuide,
                (HotspotGuide.hotspot_id == TravelHotspot.id)
                & (HotspotGuide.review_status == "approved"),
            )
            .where(
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status.in_(PUBLIC_HOTSPOT_STATUSES),
            )
            .group_by(
                TravelHotspot.id,
                TravelHotspot.name,
                HotspotGuide.locale,
                HotspotGuide.content_type,
            )
        )
    ).all()
    grouped: dict[UUID, dict[str, Any]] = {}
    for hotspot_id, name, locale, kind, count in rows:
        item = grouped.setdefault(
            hotspot_id,
            {
                "id": str(hotspot_id),
                "name": name,
                "coverage": {value: {"article": 0, "video": 0} for value in LOCALES},
            },
        )
        if locale in LOCALES and kind in {"article", "video"}:
            item["coverage"][locale][kind] = int(count)
    for item in grouped.values():
        item["complete"] = all(
            values["article"] > 0 and values["video"] > 0 for values in item["coverage"].values()
        )
    return {
        "items": list(grouped.values()),
        "total": len(grouped),
        "complete": sum(bool(item["complete"]) for item in grouped.values()),
    }
