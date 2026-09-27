from __future__ import annotations

from datetime import UTC, datetime
from urllib.parse import urlsplit

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.news_automation.feeds import extract_article, parse_entries
from app.news_automation.fetch import RateLimiter, SafeNewsFetcher
from app.news_automation.models import NewsEvidence, NewsSource
from app.news_automation.policy import content_fingerprint
from app.problems import AppError


def source_host(url: str) -> str:
    return (urlsplit(url).hostname or "").casefold().rstrip(".")


async def _source_index(
    session: AsyncSession,
) -> tuple[dict[str, NewsSource], set[str], set[str]]:
    """Enabled sources by host (redirect hosts included), and the hosts a fetch may reach."""
    sources = list(await session.scalars(select(NewsSource).where(NewsSource.enabled.is_(True))))
    by_host: dict[str, NewsSource] = {}
    for source in sources:
        by_host[source_host(source.url)] = source
        for redirect_host in source.allowed_redirect_hosts_json or []:
            by_host.setdefault(redirect_host.casefold().rstrip("."), source)
    allowed_hosts = {source_host(source.url) for source in sources}
    allowed_redirects = {
        host.casefold().rstrip(".")
        for source in sources
        for host in source.allowed_redirect_hosts_json or []
    }
    return by_host, allowed_hosts, allowed_redirects


async def refresh_evidence(
    session: AsyncSession,
    evidence: list[NewsEvidence],
    *,
    fetcher: SafeNewsFetcher | None = None,
    rate_limiter: RateLimiter | None = None,
) -> tuple[list[str], list[str]]:
    """Take each evidence page's current text; return the changed URLs and any problems.

    The same host and source-policy rules as ``revalidate_evidence`` apply, and the pages
    are fetched without conditional headers so a stale ETag cannot hide the change. Rows
    are updated only when every page could be read, so a candidate never ends up with half
    its evidence refreshed.
    """

    by_host, allowed_hosts, allowed_redirects = await _source_index(session)
    own_fetcher = fetcher is None
    fetcher = fetcher or SafeNewsFetcher(rate_limiter=rate_limiter)
    problems: list[str] = []
    fetched_rows: list[tuple[NewsEvidence, str, str | None, str | None]] = []
    try:
        for row in evidence:
            matched_source = by_host.get(source_host(row.url))
            if matched_source is None:
                problems.append(f"source_disabled_or_unlisted:{row.url}")
                continue
            if (
                row.role != matched_source.role
                or row.is_first_party != matched_source.is_first_party
            ):
                problems.append(f"source_policy_changed:{row.url}")
                continue
            try:
                fetched = await fetcher.fetch(
                    row.url,
                    allowed_hosts=allowed_hosts,
                    allowed_redirect_hosts=allowed_redirects,
                )
            except Exception as error:
                problems.append(f"source_refetch_failed:{row.url}:{type(error).__name__}")
                continue
            _, article_text, _ = extract_article(
                fetched.body, fetched.url, matched_source.config_json
            )
            if not article_text.strip():
                problems.append(f"source_became_unreadable:{row.url}")
                continue
            fetched_rows.append((row, article_text, fetched.etag, fetched.last_modified))
    finally:
        if own_fetcher:
            await fetcher.close()
    if problems:
        return [], problems
    changed: list[str] = []
    now = datetime.now(UTC)
    for row, article_text, etag, last_modified in fetched_rows:
        digest = content_fingerprint(article_text)
        if digest != row.content_hash:
            changed.append(row.url)
        row.content_hash = digest
        row.excerpt = article_text[:8000]
        row.retrieved_at = now
        row.etag = etag
        row.last_modified = last_modified
    return changed, []


async def validate_source_configuration(
    source: NewsSource, *, fetcher: SafeNewsFetcher | None = None
) -> None:
    """Fail closed before a source can be enabled.

    A successful HTTPS fetch is not enough: robots must allow the request and the
    configured parser must produce at least one readable entry.
    """

    own_fetcher = fetcher is None
    fetcher = fetcher or SafeNewsFetcher()
    try:
        listing = await fetcher.fetch(
            source.url,
            allowed_hosts={source_host(source.url)},
            allowed_redirect_hosts=set(source.allowed_redirect_hosts_json or []),
        )
        entries = parse_entries(
            listing.body,
            source.format,  # type: ignore[arg-type]
            listing.url,
            source.config_json or {},
        )
        if not entries:
            raise AppError(
                422,
                "news_source_unreadable",
                "來源可以連線，但目前設定無法讀出任何新聞項目",
            )
        detail = await fetcher.fetch(
            entries[0].url,
            allowed_hosts={source_host(source.url)},
            allowed_redirect_hosts=set(source.allowed_redirect_hosts_json or []),
        )
        _, article_text, _ = extract_article(detail.body, detail.url, source.config_json or {})
        if not article_text.strip() and not entries[0].summary.strip():
            raise AppError(
                422,
                "news_source_detail_unreadable",
                "來源清單可讀，但目前設定無法擷取新聞內頁內容",
            )
    except AppError:
        raise
    except Exception as error:
        raise AppError(
            422,
            "news_source_validation_failed",
            f"來源安全檢查或內容解析失敗：{type(error).__name__}",
        ) from error
    finally:
        if own_fetcher:
            await fetcher.close()


async def revalidate_evidence(
    session: AsyncSession,
    evidence: list[NewsEvidence],
    *,
    fetcher: SafeNewsFetcher | None = None,
    rate_limiter: RateLimiter | None = None,
) -> tuple[bool, list[str]]:
    """Refetch evidence through the SSRF-safe client and compare extracted text hashes."""

    by_host, allowed_hosts, allowed_redirects = await _source_index(session)
    own_fetcher = fetcher is None
    fetcher = fetcher or SafeNewsFetcher(rate_limiter=rate_limiter)
    reasons: list[str] = []
    try:
        for row in evidence:
            matched_source = by_host.get(source_host(row.url))
            if matched_source is None:
                reasons.append(f"source_disabled_or_unlisted:{row.url}")
                continue
            if (
                row.role != matched_source.role
                or row.is_first_party != matched_source.is_first_party
            ):
                reasons.append(f"source_policy_changed:{row.url}")
                continue
            try:
                fetched = await fetcher.fetch(
                    row.url,
                    allowed_hosts=allowed_hosts,
                    allowed_redirect_hosts=allowed_redirects,
                    etag=row.etag,
                    last_modified=row.last_modified,
                )
            except Exception as error:
                reasons.append(f"source_refetch_failed:{row.url}:{type(error).__name__}")
                continue
            if fetched.not_modified:
                row.retrieved_at = datetime.now(UTC)
                continue
            _, article_text, _ = extract_article(
                fetched.body, fetched.url, matched_source.config_json
            )
            if not article_text.strip():
                reasons.append(f"source_became_unreadable:{row.url}")
                continue
            if content_fingerprint(article_text) != row.content_hash:
                reasons.append(f"source_content_changed:{row.url}")
                continue
            row.retrieved_at = datetime.now(UTC)
            row.etag = fetched.etag
            row.last_modified = fetched.last_modified
        return not reasons, reasons
    finally:
        if own_fetcher:
            await fetcher.close()
