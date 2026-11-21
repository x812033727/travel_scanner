"""IndexNow instant URL submission for Bing, Yahoo TW, Naver, and ChatGPT Search.

Submissions are strictly best-effort and never block or roll back an article publication.
When ``INDEXNOW_KEY`` is unset or ``NEXT_PUBLIC_SITE_URL`` is not an HTTPS origin (dev/test),
every call returns a structured skipped result without making any network request.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import cast
from urllib.parse import urlparse

import httpx
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings, official_provider_url_ok
from app.guides.models import GuideArticle, GuideArticleLocale, GuideArticleRevision
from app.guides.publication import published_filters
from app.guides.schemas import Kind

logger = logging.getLogger(__name__)

KEY_PATTERN = re.compile(r"^[A-Za-z0-9-]{8,128}$")
INDEXNOW_KEY_FILENAME = "indexnow-key.txt"
MAX_URLS_PER_BATCH = 10_000
DEFAULT_TIMEOUT_SECONDS = 5.0


@dataclass(frozen=True)
class IndexNowResult:
    submitted: int
    accepted: bool
    status_code: int | None = None
    skipped_reason: str | None = None
    error: str | None = None


def valid_key(value: str | None) -> str | None:
    if not value:
        return None
    trimmed = value.strip()
    return trimmed if KEY_PATTERN.fullmatch(trimmed) else None


def guide_public_url(site_url: str, locale: str, kind: Kind, slug: str) -> str:
    origin = site_url.rstrip("/")
    path = f"/life/{slug}" if kind == "life" else f"/guides/{kind}/{slug}"
    return f"{origin}/{locale}{path}"


def _https_origin(site_url: str) -> tuple[str, str] | None:
    parsed = urlparse(site_url.rstrip("/"))
    if parsed.scheme != "https" or not parsed.hostname:
        return None
    return f"https://{parsed.netloc}", parsed.hostname.lower()


async def notify_urls(
    urls: Sequence[str],
    *,
    key: str | None = None,
    site_url: str | None = None,
    endpoint: str | None = None,
    client: httpx.AsyncClient | None = None,
) -> IndexNowResult:
    """Submit canonical public URLs to IndexNow in batches of up to 10,000."""
    settings = get_settings()
    resolved_key = valid_key(key if key is not None else settings.indexnow_key)
    if not resolved_key:
        return IndexNowResult(submitted=0, accepted=False, skipped_reason="key_unconfigured")

    resolved_site = (site_url if site_url is not None else settings.next_public_site_url).strip()
    origin_info = _https_origin(resolved_site)
    if origin_info is None:
        return IndexNowResult(submitted=0, accepted=False, skipped_reason="non_https_origin")
    origin, host = origin_info

    resolved_endpoint = (endpoint if endpoint is not None else settings.indexnow_endpoint).strip()
    if not official_provider_url_ok("indexnow_endpoint", resolved_endpoint):
        return IndexNowResult(submitted=0, accepted=False, skipped_reason="invalid_endpoint")

    deduped: list[str] = []
    seen: set[str] = set()
    for raw in urls:
        candidate = raw.strip()
        if not candidate or candidate in seen:
            continue
        parsed = urlparse(candidate)
        if parsed.scheme != "https" or (parsed.hostname or "").lower() != host:
            continue
        seen.add(candidate)
        deduped.append(candidate)

    if not deduped:
        return IndexNowResult(submitted=0, accepted=False, skipped_reason="no_valid_urls")

    key_location = f"{origin}/{INDEXNOW_KEY_FILENAME}"
    total_submitted = 0
    last_status: int | None = None
    owns_client = client is None
    http = client or httpx.AsyncClient(timeout=DEFAULT_TIMEOUT_SECONDS)
    try:
        for start in range(0, len(deduped), MAX_URLS_PER_BATCH):
            batch = deduped[start : start + MAX_URLS_PER_BATCH]
            payload = {
                "host": host,
                "key": resolved_key,
                "keyLocation": key_location,
                "urlList": batch,
            }
            response = await http.post(resolved_endpoint, json=payload)
            last_status = response.status_code
            if response.status_code not in (200, 202):
                logger.warning(
                    "IndexNow submission rejected with HTTP %s for %d URL(s)",
                    response.status_code,
                    len(batch),
                )
                return IndexNowResult(
                    submitted=total_submitted,
                    accepted=False,
                    status_code=response.status_code,
                    error=f"HTTP {response.status_code}",
                )
            total_submitted += len(batch)
        return IndexNowResult(submitted=total_submitted, accepted=True, status_code=last_status)
    except Exception as exc:
        logger.warning("IndexNow submission failed: %s", exc)
        return IndexNowResult(
            submitted=total_submitted,
            accepted=False,
            status_code=last_status,
            error=str(exc),
        )
    finally:
        if owns_client:
            await http.aclose()


async def notify_guide_change(
    kind: Kind,
    slug: str,
    locales: Sequence[str],
    *,
    client: httpx.AsyncClient | None = None,
) -> IndexNowResult:
    """Notify IndexNow after one or more translations of a guide are published or withdrawn."""
    settings = get_settings()
    if not valid_key(settings.indexnow_key):
        return IndexNowResult(submitted=0, accepted=False, skipped_reason="key_unconfigured")
    urls = [guide_public_url(settings.next_public_site_url, loc, kind, slug) for loc in locales]
    return await notify_urls(urls, client=client)


async def recent_published_urls(
    session: AsyncSession,
    *,
    since_hours: int,
    site_url: str,
    limit: int = MAX_URLS_PER_BATCH,
) -> list[str]:
    """Collect canonical URLs of live translations modified within ``since_hours``."""
    cutoff = datetime.now(UTC) - timedelta(hours=max(1, since_hours))
    rows = await session.execute(
        select(GuideArticle.kind, GuideArticle.slug, GuideArticleLocale.locale)
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .join(
            GuideArticleRevision,
            and_(
                GuideArticleRevision.article_locale_id == GuideArticleLocale.id,
                GuideArticleRevision.version == GuideArticleLocale.published_version,
                GuideArticleRevision.action == "published",
            ),
        )
        .where(
            GuideArticleLocale.published_at.is_not(None),
            GuideArticleRevision.created_at >= cutoff,
            *published_filters(),
        )
        .order_by(
            GuideArticleRevision.created_at.desc(),
            GuideArticle.slug,
            GuideArticleLocale.locale,
        )
        .limit(min(max(limit, 1), MAX_URLS_PER_BATCH))
    )
    return [
        guide_public_url(site_url, locale, cast(Kind, kind), slug)
        for kind, slug, locale in rows
    ]
