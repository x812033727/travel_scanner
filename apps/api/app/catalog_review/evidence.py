"""Small, public-HTTPS-only evidence excerpts with server-assigned source authority.

Neither catalog source rows nor model-authored URLs grant authority. A fetched page is
trusted only when its host is explicitly supplied by the server's seed-derived registry
or belongs to Wikimedia. Google/Naver/Michelin content is not an ingestion source.
"""

from __future__ import annotations

import asyncio
import hashlib
import ipaddress
import json
import re
import socket
from collections.abc import Awaitable, Callable, Collection
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urlencode, urlsplit, urlunsplit

import httpx

from app.catalog_review.schemas import EvidenceSource

MAX_BYTES = 200_000
MAX_TEXT = 12_000
MAX_URLS = 100
TOTAL_SECONDS = 8.0
Resolver = Callable[[str], Awaitable[list[str]]]
_WIKIMEDIA = ("wikimedia.org", "wikipedia.org", "wikidata.org", "wikivoyage.org")
_BLOCKED = (
    "google.com",
    "googleapis.com",
    "googleusercontent.com",
    "gstatic.com",
    "maps.app.goo.gl",
    "goo.gl",
    "naver.com",
    "naver.net",
    "pstatic.net",
    "michelin.com",
    "michelin.co.jp",
)
_ENTITY_LANGUAGES = ("en", "zh", "zh-tw", "zh-hant", "ja", "ko", "th", "vi")
_ENTITY_SITES = ("enwiki", "zhwiki", "jawiki", "kowiki", "thwiki", "viwiki")
_IDENTITY_PROPERTIES = {
    "P31": "instance of",
    "P279": "subclass of",
    "P131": "administrative location",
    "P17": "country",
    "P625": "coordinates (source claim, not map verification)",
    "P856": "official website",
    "P1705": "native name",
    "P1448": "official name",
}


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def normalize_source_url(url: str) -> str | None:
    """Syntactic gate only; every network request also passes public DNS validation."""
    if len(url) > 2048 or any(ord(char) < 32 for char in url) or "\\" in url:
        return None
    try:
        parts = urlsplit(url)
        host = (parts.hostname or "").lower().rstrip(".").encode("idna").decode("ascii")
        if parts.scheme != "https" or not host or parts.username or parts.password:
            return None
        if parts.port not in (None, 443):
            return None
        labels = host.split(".")
        if any(host == item or host.endswith(f".{item}") for item in _BLOCKED):
            return None
        # Google and Michelin also have country-specific domains.
        if "google" in labels or "michelin" in labels or "naver" in labels:
            return None
        address = None
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            pass
        if address is not None and (not address.is_global or address.is_multicast):
            return None
        netloc = f"[{host}]" if ":" in host else host
        return urlunsplit(("https", netloc, parts.path or "/", parts.query, ""))
    except (ValueError, UnicodeError):
        return None


def is_trusted_source(url: str, trusted_hosts: Collection[str]) -> bool:
    normalized = normalize_source_url(url)
    if normalized is None:
        return False
    host = (urlsplit(normalized).hostname or "").removeprefix("www.")
    registry = {item.lower().rstrip(".").removeprefix("www.") for item in trusted_hosts}
    return host in registry or any(host == item or host.endswith(f".{item}") for item in _WIKIMEDIA)


def _wikidata_request(url: str) -> tuple[str, str] | None:
    """Only a canonical entity page enables this fixed official API transformation."""
    parts = urlsplit(url)
    if parts.hostname not in {"www.wikidata.org", "wikidata.org"} or parts.query:
        return None
    match = re.fullmatch(r"/wiki/(Q[1-9][0-9]*)", parts.path)
    if match is None:
        return None
    qid = match.group(1)
    query = urlencode(
        {
            "action": "wbgetentities",
            "format": "json",
            "ids": qid,
            "props": "labels|descriptions|aliases|claims|sitelinks",
            "languages": "|".join(_ENTITY_LANGUAGES),
            "sitefilter": "|".join(_ENTITY_SITES),
            "maxlag": "5",
        }
    )
    return f"https://www.wikidata.org/w/api.php?{query}", qid


def _wikidata_excerpt(document: str, qid: str) -> str:
    body = json.loads(document)
    entities = body.get("entities") if isinstance(body, dict) else None
    entity = entities.get(qid) if isinstance(entities, dict) else None
    if (
        not isinstance(entity, dict)
        or entity.get("id") != qid
        or "missing" in entity
        or "redirects" in body
    ):
        raise ValueError("Wikidata did not return the exact requested entity")
    lines = [f"Wikidata entity {qid}"]
    if isinstance(entity.get("lastrevid"), int):
        lines.append(f"Revision: {entity['lastrevid']}")
    identity_lines = 0
    for field in ("labels", "descriptions", "aliases"):
        localized = entity.get(field)
        if not isinstance(localized, dict):
            continue
        for language in _ENTITY_LANGUAGES:
            value = localized.get(language)
            entries = value if isinstance(value, list) else [value]
            for entry in entries[:10]:
                text = entry.get("value") if isinstance(entry, dict) else None
                if isinstance(text, str) and text.strip():
                    lines.append(f"{field} [{language}]: {normalize_text(text)[:500]}")
                    identity_lines += 1
    if not identity_lines:
        raise ValueError("Wikidata returned no usable entity identity")
    claims = entity.get("claims")
    for property_id, label in _IDENTITY_PROPERTIES.items():
        statements = claims.get(property_id) if isinstance(claims, dict) else None
        for statement in (statements if isinstance(statements, list) else [])[:10]:
            if not isinstance(statement, dict) or statement.get("rank") == "deprecated":
                continue
            snak = statement.get("mainsnak")
            data = snak.get("datavalue") if isinstance(snak, dict) else None
            claim_value: Any = data.get("value") if isinstance(data, dict) else None
            if claim_value is None:
                continue
            if isinstance(claim_value, dict) and claim_value.get("entity-type") == "item":
                claim_value = claim_value.get("id")
                if not isinstance(claim_value, str) or not re.fullmatch(
                    r"Q[1-9][0-9]*", claim_value
                ):
                    continue
            try:
                fact = json.dumps(claim_value, ensure_ascii=False, sort_keys=True, allow_nan=False)
            except (ValueError, TypeError):
                continue
            lines.append(f"{property_id} ({label}): {fact[:600]}")
    sitelinks = entity.get("sitelinks")
    for site in _ENTITY_SITES:
        entry = sitelinks.get(site) if isinstance(sitelinks, dict) else None
        title = entry.get("title") if isinstance(entry, dict) else None
        if isinstance(title, str):
            lines.append(f"Wikipedia [{site}]: {normalize_text(title)[:500]}")
    return normalize_text("\n".join(lines))[:MAX_TEXT]


async def system_resolver(host: str) -> list[str]:
    infos = await asyncio.to_thread(socket.getaddrinfo, host, 443, proto=socket.IPPROTO_TCP)
    return list(dict.fromkeys(str(info[4][0]) for info in infos))


async def public_request_target(
    url: str,
    resolver: Resolver = system_resolver,
) -> tuple[httpx.URL, str] | None:
    """Pin the connection to a checked address, retaining the original TLS SNI/Host.

    Unlike checking DNS then connecting to the hostname, this cannot resolve a second
    answer pointing to a private service. Environment proxies are disabled on owned clients.
    """
    host = urlsplit(url).hostname or ""
    try:
        addresses = await resolver(host)
        if not addresses:
            return None
        for value in addresses:
            address = ipaddress.ip_address(value)
            if not address.is_global or address.is_multicast:
                return None
        return httpx.URL(url).copy_with(host=addresses[0]), host
    except (OSError, ValueError, httpx.InvalidURL):
        return None


class _VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ignored = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "iframe"}:
            self.ignored += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "iframe"}:
            self.ignored = max(0, self.ignored - 1)

    def handle_data(self, data: str) -> None:
        if not self.ignored:
            self.parts.append(data)


async def fetch_sources(
    urls: list[str],
    trusted_hosts: Collection[str],
    *,
    client: httpx.AsyncClient | None = None,
    resolver: Resolver | None = None,
) -> list[EvidenceSource]:
    """Fetch at most 100 URLs, three at a time; failure never aborts other sources."""
    if len(urls) > MAX_URLS:
        raise ValueError("At most 100 evidence sources may be fetched per batch")
    owned = client is None
    transport = client or httpx.AsyncClient(timeout=TOTAL_SECONDS, trust_env=False)
    semaphore = asyncio.Semaphore(3)
    resolve = resolver or system_resolver

    async def fetch(raw: str) -> EvidenceSource:
        url = normalize_source_url(raw)
        if url is None:
            return EvidenceSource(url=raw[:2048], error="blocked_url")
        failure = EvidenceSource(url=url, trusted=is_trusted_source(url, trusted_hosts))
        entity_request = _wikidata_request(url)
        request_url = entity_request[0] if entity_request else url
        async with semaphore:
            try:
                async with asyncio.timeout(TOTAL_SECONDS):
                    target = await public_request_target(request_url, resolve)
                    if target is None:
                        return failure.model_copy(update={"error": "blocked_address"})
                    pinned_url, host = target
                    async with transport.stream(
                        "GET",
                        pinned_url,
                        headers={
                            "Host": host,
                            "Connection": "close",
                            "User-Agent": "MokaairBot/1.0 (+https://mokaair.com; catalog review)",
                            "Accept": "application/json"
                            if entity_request
                            else "text/html,application/xhtml+xml,text/plain",
                        },
                        extensions={"sni_hostname": host},
                        follow_redirects=False,
                        timeout=TOTAL_SECONDS,
                    ) as response:
                        if response.status_code != 200:
                            return failure.model_copy(
                                update={
                                    "error": "redirect_blocked"
                                    if response.is_redirect
                                    else f"http_{response.status_code}",
                                }
                            )
                        content_type = response.headers.get("content-type", "").lower()
                        allowed_types = (
                            ("application/json",)
                            if entity_request
                            else (
                                "html",
                                "text/plain",
                                "xml",
                            )
                        )
                        if not any(item in content_type for item in allowed_types):
                            return failure.model_copy(update={"error": "unsupported_content"})
                        chunks: list[bytes] = []
                        size = 0
                        async for chunk in response.aiter_bytes():
                            size += len(chunk)
                            if size > MAX_BYTES:
                                return failure.model_copy(update={"error": "response_too_large"})
                            chunks.append(chunk)
                        body = b"".join(chunks).decode(
                            response.encoding or "utf-8", errors="replace"
                        )
                        if entity_request:
                            try:
                                excerpt = _wikidata_excerpt(body, entity_request[1])
                            except ValueError:
                                return failure.model_copy(
                                    update={"error": "invalid_wikidata_entity"}
                                )
                        else:
                            parser = _VisibleText()
                            parser.feed(body)
                            excerpt = normalize_text(" ".join(parser.parts))[:MAX_TEXT]
                        if not excerpt:
                            return failure.model_copy(update={"error": "empty_content"})
                        return failure.model_copy(
                            update={
                                "text": excerpt,
                                "fetched": True,
                                "fingerprint": hashlib.sha256(excerpt.encode("utf-8")).hexdigest(),
                            }
                        )
            except (TimeoutError, httpx.TimeoutException):
                return failure.model_copy(update={"error": "timeout"})
            except (httpx.HTTPError, ValueError, UnicodeError, LookupError):
                return failure.model_copy(update={"error": "fetch_failed"})

    try:
        return await asyncio.gather(*(fetch(url) for url in dict.fromkeys(urls)))
    finally:
        if owned:
            await transport.aclose()
