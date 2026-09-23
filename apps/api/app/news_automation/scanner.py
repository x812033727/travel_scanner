from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import UTC, datetime, timedelta
from urllib.parse import urlsplit
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.news_automation.feeds import extract_article, parse_entries
from app.news_automation.fetch import SafeNewsFetcher
from app.news_automation.models import NewsCandidate, NewsEvidence, NewsSource
from app.news_automation.policy import content_fingerprint, normalized_title
from app.news_automation.schemas import Vertical
from app.news_automation.service import settings_row

Enqueue = Callable[[UUID], Awaitable[None]]


def _host(url: str) -> str:
    return (urlsplit(url).hostname or "").casefold().rstrip(".")


def classify_vertical(title: str, text: str) -> Vertical:
    haystack = f"{title} {text}".casefold()
    keywords = {
        "ai": (
            "artificial intelligence",
            "generative ai",
            "openai",
            "anthropic",
            "gemini",
            "llm",
            "人工智慧",
            "生成式 ai",
        ),
        "crypto": (
            "bitcoin",
            "ethereum",
            "blockchain",
            "stablecoin",
            "crypto",
            "token",
            "加密貨幣",
            "虛擬資產",
        ),
        "tech": (
            "security",
            "software",
            "hardware",
            "cloud",
            "standard",
            "technology",
            "cyber",
            "科技",
            "資安",
        ),
    }
    scores = {key: sum(term in haystack for term in terms) for key, terms in keywords.items()}
    best = max(scores, key=scores.get)  # type: ignore[arg-type]
    return best if scores[best] else "tech"  # type: ignore[return-value]


async def claim_due_sources(session: AsyncSession, *, limit: int = 20) -> list[UUID]:
    settings = await settings_row(session)
    if not settings.enabled:
        await session.rollback()
        return []
    now = datetime.now(UTC)
    rows = list(
        await session.scalars(
            select(NewsSource)
            .where(
                NewsSource.enabled.is_(True),
                NewsSource.next_scan_at <= now,
                or_(NewsSource.scan_lock_until.is_(None), NewsSource.scan_lock_until < now),
            )
            .order_by(NewsSource.next_scan_at, NewsSource.id)
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
    )
    for row in rows:
        # Advance from "now", not the stale due time: after downtime each source is scanned
        # once and never floods the queue trying to replay every missed hour.
        row.next_scan_at = now + timedelta(minutes=row.scan_interval_minutes)
        row.scan_lock_until = now + timedelta(minutes=15)
        row.last_status = "queued"
    await session.commit()
    return [row.id for row in rows]


async def _enabled_sources(session: AsyncSession) -> list[NewsSource]:
    return list(await session.scalars(select(NewsSource).where(NewsSource.enabled.is_(True))))


async def scan_source(
    session: AsyncSession,
    source_id: UUID,
    enqueue: Enqueue,
    *,
    fetcher: SafeNewsFetcher | None = None,
) -> int:
    source = await session.get(NewsSource, source_id)
    settings = await settings_row(session)
    if source is None or not source.enabled or not settings.enabled:
        return 0
    own_fetcher = fetcher is None
    fetcher = fetcher or SafeNewsFetcher()
    all_sources = await _enabled_sources(session)
    by_host = {_host(item.url): item for item in all_sources}
    allowed_hosts = set(by_host)
    allowed_redirects = {host for item in all_sources for host in item.allowed_redirect_hosts_json}
    created_ids: list[UUID] = []
    now = datetime.now(UTC)
    try:
        listing = await fetcher.fetch(
            source.url,
            allowed_hosts={_host(source.url)},
            allowed_redirect_hosts=set(source.allowed_redirect_hosts_json),
            etag=source.etag,
            last_modified=source.last_modified,
        )
        source.last_scanned_at = now
        source.scan_lock_until = None
        if listing.not_modified:
            source.last_status = "not_modified"
            source.last_error = None
            source.consecutive_failures = 0
            await session.commit()
            return 0
        entries = parse_entries(
            listing.body,
            source.format,  # type: ignore[arg-type]
            listing.url,
            source.config_json,
        )
        maximum = min(max(int(source.config_json.get("max_entries_per_scan", 20)), 1), 50)
        for entry in entries[:maximum]:
            if _host(entry.url) not in allowed_hosts | allowed_redirects:
                continue
            detail = await fetcher.fetch(
                entry.url,
                allowed_hosts=allowed_hosts,
                allowed_redirect_hosts=allowed_redirects,
            )
            detail_source = by_host.get(_host(detail.url), source)
            page_title, article_text, links = extract_article(
                detail.body, detail.url, detail_source.config_json
            )
            body_text = article_text or entry.summary
            title = page_title or entry.title
            if not body_text.strip():
                continue
            canonical = detail.url
            body_hash = content_fingerprint(body_text)
            idempotency = content_fingerprint(canonical, body_hash)
            if await session.scalar(
                select(NewsCandidate.id).where(NewsCandidate.idempotency_key == idempotency)
            ):
                continue
            normalized = normalized_title(title)[:500]
            exact_duplicate_id = await session.scalar(
                select(NewsCandidate.id)
                .where(
                    or_(
                        NewsCandidate.canonical_url == canonical,
                        NewsCandidate.content_hash == body_hash,
                        NewsCandidate.normalized_title == normalized,
                    )
                )
                .order_by(NewsCandidate.created_at.desc())
                .limit(1)
            )
            vertical: Vertical = (
                classify_vertical(title, body_text)
                if source.vertical == "mixed"
                else source.vertical  # type: ignore[assignment]
            )
            candidate = NewsCandidate(
                source_id=source.id,
                vertical=vertical,
                status="duplicate" if exact_duplicate_id else "discovered",
                canonical_url=canonical,
                source_title=title[:500],
                normalized_title=normalized,
                source_published_at=entry.published_at,
                content_hash=body_hash,
                idempotency_key=idempotency,
                prompt_version=settings.prompt_version,
                policy_version=settings.policy_version,
                error_code="news_exact_duplicate" if exact_duplicate_id else None,
                error_detail=(
                    f"Exact URL, title or content duplicate of {exact_duplicate_id}"
                    if exact_duplicate_id
                    else None
                ),
            )
            session.add(candidate)
            await session.flush()
            session.add(
                NewsEvidence(
                    candidate_id=candidate.id,
                    role=detail_source.role,
                    is_first_party=detail_source.is_first_party,
                    url=canonical,
                    title=title[:500],
                    source_date=entry.published_at.date() if entry.published_at else None,
                    etag=detail.etag,
                    last_modified=detail.last_modified,
                    content_hash=body_hash,
                    excerpt=body_text[:8000],
                )
            )
            if exact_duplicate_id:
                continue
            used = {canonical}
            for link in links:
                linked_source = by_host.get(_host(link))
                if (
                    linked_source is None
                    or linked_source.role != "evidence"
                    or link in used
                    or len(used) >= 5
                ):
                    continue
                linked = await fetcher.fetch(
                    link,
                    allowed_hosts=allowed_hosts,
                    allowed_redirect_hosts=allowed_redirects,
                )
                linked_title, linked_text, _ = extract_article(
                    linked.body, linked.url, linked_source.config_json
                )
                if not linked_text.strip():
                    continue
                used.add(link)
                session.add(
                    NewsEvidence(
                        candidate_id=candidate.id,
                        role="evidence",
                        is_first_party=linked_source.is_first_party,
                        url=linked.url,
                        title=(linked_title or linked_source.name)[:500],
                        etag=linked.etag,
                        last_modified=linked.last_modified,
                        content_hash=content_fingerprint(linked_text),
                        excerpt=linked_text[:8000],
                    )
                )
            created_ids.append(candidate.id)
        source.etag = listing.etag
        source.last_modified = listing.last_modified
        source.last_status = "succeeded"
        source.last_error = None
        source.consecutive_failures = 0
        await session.commit()
    except Exception as error:
        await session.rollback()
        source = await session.get(NewsSource, source_id)
        if source is not None:
            source.last_scanned_at = now
            source.scan_lock_until = None
            source.last_status = "failed"
            source.last_error = f"{type(error).__name__}: {error}"[:4000]
            source.consecutive_failures += 1
            await session.commit()
        raise
    finally:
        if own_fetcher:
            await fetcher.close()
    for candidate_id in created_ids:
        await enqueue(candidate_id)
    return len(created_ids)
