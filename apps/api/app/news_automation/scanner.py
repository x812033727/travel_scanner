from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import UTC, datetime, timedelta
from urllib.parse import urlsplit
from uuid import UUID

import httpx
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.news_automation.evidence import evidence_excerpt
from app.news_automation.feeds import parse_entries, read_article
from app.news_automation.fetch import SafeNewsFetcher
from app.news_automation.models import NewsCandidate, NewsEvidence, NewsSource
from app.news_automation.policy import (
    body_fingerprint,
    content_fingerprint,
    evidence_site,
    normalized_title,
)
from app.news_automation.schemas import Entry, Vertical
from app.news_automation.service import settings_row

Enqueue = Callable[[UUID], Awaitable[None]]
# What one unreachable, refused or unreadable page raises: HTTP status and transport
# errors, DNS and socket failures (OSError, TimeoutError included) and the fetcher's
# UnsafeNewsUrl (a ValueError). Anything else is a bug and still fails the scan.
PAGE_ERRORS: tuple[type[Exception], ...] = (
    httpx.HTTPError,
    httpx.InvalidURL,
    OSError,
    ValueError,
)
MAX_REPORTED_SKIPS = 5
# A publisher that refuses the scanner outright (openai.com/index/* answers every request
# with a Cloudflare challenge, HTTP 403) never becomes a candidate if a refused page is only
# skipped: the entry is tried and skipped every hour and nobody sees the story. A recent
# entry is kept instead as a lead holding the feed's own summary, which cannot be drafted
# from (lead_only evidence stops at needs_evidence) but shows up in the review queue.
REFUSED_STATUSES = frozenset({401, 403})
SUMMARY_LEAD_MAX_AGE = timedelta(hours=72)
PAGE_REFUSED = "news_page_refused"
# A readable article (a press report, say) that links to a story still waiting for evidence
# -- a refused page kept as a lead, or a candidate with lead-only pages -- is attached to that
# story as its evidence, and the story is drafted instead of the report filing a second one.
ATTACHED = "news_attached_as_evidence"
# A source's first scan reads a listing that is mostly its back catalogue. Every entry older
# than this (or undated: an HTML listing has no dates) is recorded as seen without being
# fetched or drafted, so adding a source files only its news of the last days.
BASELINE = "news_baseline"
WAITING_LOOKUP_LIMIT = 200
# Links that are plainly not articles. Apple Newsroom's first scan fetched 76 image links
# as evidence, each one a robots check and a rate-limited request that then failed.
NON_ARTICLE_SUFFIXES = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".avif",
    ".svg",
    ".ico",
    ".bmp",
    ".tif",
    ".tiff",
    ".mp4",
    ".m4v",
    ".mov",
    ".webm",
    ".mp3",
    ".m4a",
    ".wav",
    ".pdf",
    ".zip",
    ".gz",
)


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


async def _already_seen(session: AsyncSession, url: str) -> bool:
    # A feed lists the same entries for days. Refetching each of them every hour costs
    # two requests per entry and, when the page text drifts, files a new "duplicate".
    return (
        await session.scalar(
            select(NewsCandidate.id).where(NewsCandidate.canonical_url == url).limit(1)
        )
    ) is not None


def _corroborating_link(link: str, primary: str) -> bool:
    """A link worth fetching as a second source: an article on another website."""
    if urlsplit(link).path.casefold().endswith(NON_ARTICLE_SUFFIXES):
        return False
    # Pages of the primary page's own site are not a second source (owner decision,
    # 2026-09-24), so they are not fetched at all.
    return evidence_site(link) != evidence_site(primary)


def _transient(error: Exception) -> bool:
    """A failure worth retrying next hour: timeouts, resets, DNS, 429 and 5xx."""
    if isinstance(error, httpx.HTTPStatusError):
        return error.response.status_code == 429 or error.response.status_code >= 500
    return isinstance(error, (httpx.TransportError, OSError))


def _refused(error: Exception) -> bool:
    """The page exists and the publisher will not serve it to us: retrying will not help."""
    return (
        isinstance(error, httpx.HTTPStatusError)
        and error.response.status_code in REFUSED_STATUSES
    )


def _summary_lead_ok(entry: Entry, now: datetime) -> bool:
    """A refused entry worth keeping from its feed summary: recent, dated and not empty.
    An undated or older entry would put a feed's whole back catalogue in the queue the first
    time a publisher starts refusing the scanner."""
    return (
        bool(entry.summary.strip())
        and entry.published_at is not None
        and now - entry.published_at <= SUMMARY_LEAD_MAX_AGE
    )


def _link_key(url: str) -> str:
    """A URL as two pages link to it: no query, no fragment, no trailing slash, host in
    lower case. A press report links to the announcement with tracking parameters and
    sometimes a trailing slash the feed did not have."""
    parts = urlsplit(url)
    return f"{(parts.hostname or '').casefold()}{parts.path.rstrip('/')}"


async def _waiting_for(
    session: AsyncSession, links: list[str], canonical: str
) -> NewsCandidate | None:
    """The newest candidate still waiting for evidence that this page links to."""
    keys = {_link_key(link) for link in links} - {_link_key(canonical)}
    if not keys:
        return None
    waiting = await session.scalars(
        select(NewsCandidate)
        .where(NewsCandidate.status == "needs_evidence")
        .order_by(NewsCandidate.created_at.desc())
        .limit(WAITING_LOOKUP_LIMIT)
    )
    return next((row for row in waiting if _link_key(row.canonical_url) in keys), None)


def _baseline_candidate(
    source: NewsSource, entry: Entry, prompt: str, policy: str
) -> NewsCandidate:
    """An entry a new source already listed, closed as seen. Its hashes are the URL's, so it
    never matches a later story's content, only its own URL."""
    return NewsCandidate(
        source_id=source.id,
        vertical=source.vertical if source.vertical != "mixed" else "tech",
        status="rejected",
        canonical_url=entry.url,
        source_title=entry.title[:500],
        normalized_title="",
        source_published_at=entry.published_at,
        content_hash=content_fingerprint("baseline", entry.url),
        idempotency_key=content_fingerprint("baseline", entry.url, "key"),
        prompt_version=prompt,
        policy_version=policy,
        error_code=BASELINE,
        error_detail="Listed when the source was first scanned; recorded as seen, not drafted.",
    )


def _skip_note(skipped: list[str], summarized: list[str] | None = None) -> str:
    notes: list[str] = []
    if skipped:
        shown = "; ".join(skipped[:MAX_REPORTED_SKIPS])
        more = len(skipped) - MAX_REPORTED_SKIPS
        notes.append(
            f"Skipped {len(skipped)} page(s): {shown}" + (f"; and {more} more" if more > 0 else "")
        )
    if summarized:
        shown = "; ".join(summarized[:MAX_REPORTED_SKIPS])
        more = len(summarized) - MAX_REPORTED_SKIPS
        notes.append(
            f"Kept {len(summarized)} refused page(s) as feed summaries: {shown}"
            + (f"; and {more} more" if more > 0 else "")
        )
    return ". ".join(notes)


async def _keep_summary_lead(
    session: AsyncSession,
    source: NewsSource,
    entry: Entry,
    error: Exception,
    prompt_version: str,
    policy_version: str,
) -> bool:
    """Store a refused entry as a candidate waiting for evidence. False when the same URL
    or title is already a candidate, so a story seen through two feeds is kept once."""
    title = entry.title
    normalized = normalized_title(title)[:500]
    if await session.scalar(
        select(NewsCandidate.id)
        .where(
            or_(
                NewsCandidate.canonical_url == entry.url,
                NewsCandidate.normalized_title == normalized,
            )
        )
        .limit(1)
    ):
        return False
    summary = entry.summary.strip()
    body_hash = content_fingerprint(summary)
    status = error.response.status_code if isinstance(error, httpx.HTTPStatusError) else None
    candidate = NewsCandidate(
        source_id=source.id,
        vertical=(
            classify_vertical(title, summary) if source.vertical == "mixed" else source.vertical
        ),
        status="needs_evidence",
        canonical_url=entry.url,
        source_title=title[:500],
        normalized_title=normalized,
        source_published_at=entry.published_at,
        content_hash=body_hash,
        idempotency_key=content_fingerprint(entry.url, body_hash),
        prompt_version=prompt_version,
        policy_version=policy_version,
        error_code=PAGE_REFUSED,
        error_detail=(
            f"The article page refused the scanner (HTTP {status}); only the feed's summary "
            "is kept. Write the story from the publisher's other pages, or reject it."
        ),
    )
    session.add(candidate)
    await session.flush()
    session.add(
        NewsEvidence(
            candidate_id=candidate.id,
            role="lead_only",
            is_first_party=source.is_first_party,
            url=entry.url,
            title=title[:500],
            source_date=entry.published_at.date() if entry.published_at else None,
            content_hash=body_hash,
            excerpt=evidence_excerpt(summary),
        )
    )
    return True


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
    # One unreachable article or linked page is skipped and reported, never allowed to
    # roll back the whole scan: the same entry would then break every later scan too.
    skipped: list[str] = []
    # Refused entries kept as summary leads (never queued: nothing can be drafted from them).
    summarized: list[str] = []
    # Stories that were waiting for evidence and got it from a page read in this scan.
    attached_ids: list[UUID] = []
    now = datetime.now(UTC)
    first_scan = source.last_scanned_at is None
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
            if await _already_seen(session, entry.url):
                continue
            if first_scan and not (
                entry.published_at is not None
                and now - entry.published_at <= SUMMARY_LEAD_MAX_AGE
            ):
                session.add(
                    _baseline_candidate(
                        source, entry, settings.prompt_version, settings.policy_version
                    )
                )
                continue
            try:
                detail = await fetcher.fetch(
                    entry.url,
                    allowed_hosts=allowed_hosts,
                    allowed_redirect_hosts=allowed_redirects,
                )
            except PAGE_ERRORS as error:
                if _refused(error) and _summary_lead_ok(entry, now):
                    if await _keep_summary_lead(
                        session,
                        source,
                        entry,
                        error,
                        settings.prompt_version,
                        settings.policy_version,
                    ):
                        summarized.append(entry.url)
                    continue
                skipped.append(f"{entry.url} ({type(error).__name__})")
                continue
            # Feed links that redirect (tracking, feed proxies) only match after the
            # fetch; without this the same page files a new "duplicate" every hour.
            if detail.url != entry.url and await _already_seen(session, detail.url):
                continue
            detail_source = by_host.get(_host(detail.url), source)
            page = read_article(detail.body, detail.url, detail_source.config_json)
            page_title, article_text, links = page.title, page.text, page.links
            body_text = article_text or entry.summary
            title = page_title or entry.title
            if not body_text.strip():
                continue
            canonical = detail.url
            body_hash = content_fingerprint(body_text)
            # The story alone, None when the page had too little of it (a feed summary
            # never gets one): the same story behind a second URL or re-rendered chrome.
            story_hash = body_fingerprint(page) if article_text else None
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
                        *(
                            [NewsCandidate.body_hash == story_hash]
                            if story_hash is not None
                            else []
                        ),
                    )
                )
                .order_by(NewsCandidate.created_at.desc())
                .limit(1)
            )
            linked_rows: list[NewsEvidence] = []
            deferred = False
            if not exact_duplicate_id:
                seen_urls = {canonical}
                for link in links:
                    linked_source = by_host.get(_host(link))
                    if (
                        linked_source is None
                        or linked_source.role != "evidence"
                        or link in seen_urls
                        or len(linked_rows) >= 4
                        or not _corroborating_link(link, canonical)
                    ):
                        continue
                    try:
                        linked = await fetcher.fetch(
                            link,
                            allowed_hosts=allowed_hosts,
                            allowed_redirect_hosts=allowed_redirects,
                        )
                    except PAGE_ERRORS as error:
                        skipped.append(f"{link} ({type(error).__name__})")
                        if _transient(error):
                            # A primary source that is briefly down would leave the candidate
                            # short of evidence for good; nothing is stored, so the whole
                            # entry is tried again on the next scan.
                            deferred = True
                            break
                        continue
                    linked_page = read_article(
                        linked.body, linked.url, linked_source.config_json
                    )
                    linked_title, linked_text = linked_page.title, linked_page.text
                    # Two links that redirect to one page would repeat an evidence URL,
                    # and a redirect can land back on the primary page's own site.
                    if (
                        not linked_text.strip()
                        or linked.url in seen_urls
                        or not _corroborating_link(linked.url, canonical)
                    ):
                        continue
                    seen_urls.update({link, linked.url})
                    linked_rows.append(
                        NewsEvidence(
                            role="evidence",
                            is_first_party=linked_source.is_first_party,
                            url=linked.url,
                            title=(linked_title or linked_source.name)[:500],
                            etag=linked.etag,
                            last_modified=linked.last_modified,
                            content_hash=content_fingerprint(linked_text),
                            body_hash=body_fingerprint(linked_page),
                            excerpt=evidence_excerpt(linked_text),
                        )
                    )
            if deferred:
                continue
            waiting = (
                await _waiting_for(session, links, canonical)
                if not exact_duplicate_id and detail_source.role == "evidence"
                else None
            )
            if waiting is not None:
                waiting.status = "discovered"
                waiting.error_code = None
                waiting.error_detail = None
                session.add(
                    NewsEvidence(
                        candidate_id=waiting.id,
                        role="evidence",
                        is_first_party=detail_source.is_first_party,
                        url=canonical,
                        title=title[:500],
                        source_date=entry.published_at.date() if entry.published_at else None,
                        etag=detail.etag,
                        last_modified=detail.last_modified,
                        content_hash=body_hash,
                        body_hash=story_hash,
                        excerpt=evidence_excerpt(body_text),
                    )
                )
                for row in linked_rows:
                    row.candidate_id = waiting.id
                    session.add(row)
                linked_rows = []
                attached_ids.append(waiting.id)
            vertical: Vertical = (
                classify_vertical(title, body_text)
                if source.vertical == "mixed"
                else source.vertical  # type: ignore[assignment]
            )
            candidate = NewsCandidate(
                source_id=source.id,
                vertical=vertical,
                status="duplicate" if exact_duplicate_id or waiting else "discovered",
                canonical_url=canonical,
                source_title=title[:500],
                normalized_title=normalized,
                source_published_at=entry.published_at,
                content_hash=body_hash,
                body_hash=story_hash,
                idempotency_key=idempotency,
                prompt_version=settings.prompt_version,
                policy_version=settings.policy_version,
                error_code=(
                    "news_exact_duplicate" if exact_duplicate_id else ATTACHED if waiting else None
                ),
                error_detail=(
                    f"Exact URL, title or content duplicate of {exact_duplicate_id}"
                    if exact_duplicate_id
                    else f"Attached as evidence to {waiting.id}"
                    if waiting
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
                    body_hash=story_hash,
                    excerpt=evidence_excerpt(body_text),
                )
            )
            for row in linked_rows:
                row.candidate_id = candidate.id
                session.add(row)
            if exact_duplicate_id or waiting:
                continue
            created_ids.append(candidate.id)
        if not skipped:
            # Keeping the old validators after a skip makes the next scan read the listing
            # again (a 304 would hide the skipped entries); seen entries cost one query.
            source.etag = listing.etag
            source.last_modified = listing.last_modified
        source.last_status = "partial" if skipped or summarized else "succeeded"
        source.last_error = (
            _skip_note(skipped, summarized)[:4000] if skipped or summarized else None
        )
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
    for candidate_id in [*created_ids, *attached_ids]:
        await enqueue(candidate_id)
    return len(created_ids) + len(attached_ids)
