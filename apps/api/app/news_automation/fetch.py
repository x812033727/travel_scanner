from __future__ import annotations

import asyncio
import ipaddress
import socket
import ssl
import time
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

import certifi
import httpx
from redis.asyncio import Redis

from app.news_automation.schemas import FetchResult

USER_AGENT = "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
# A source's listing may be allowed more (config ``max_response_bytes``), never past this:
# GitHub's blog feed carries every post's full text and is 2.3 MB.
MAX_LISTING_BYTES = 8 * 1024 * 1024
ALLOWED_TYPES = (
    "application/atom+xml",
    "application/feed+json",
    "application/json",
    "application/rss+xml",
    "application/xml",
    "text/html",
    "text/xml",
)
MAX_REDIRECTS = 4
Resolver = Callable[[str], Awaitable[tuple[str, ...]]]


class _NoAlpnContext(ssl.SSLContext):
    """A TLS context on which httpcore's ALPN offer is a no-op.

    httpcore offers ``http/1.1`` through ALPN on every connection it opens, and Cloudflare
    challenges a Python handshake that offers ALPN (403 with ``cf-mitigated: challenge``) where
    it lets the same request through without the offer: the CFTC feed and its press releases
    answered 403 to every scan from 2026-10-06 and 200 once the offer was left out, measured
    from the host on 2026-10-16. urllib, which offers none, was never refused. Without the
    offer the server speaks HTTP/1.1, which is all this client speaks anyway; the request,
    its User-Agent and robots.txt are unchanged.
    """

    def set_alpn_protocols(self, alpn_protocols: Iterable[str]) -> None:
        del alpn_protocols


def tls_context() -> ssl.SSLContext:
    """The verifying TLS context every news fetch uses, without Python 3.13's strict X.509 mode.

    Python 3.13 turned ``VERIFY_X509_STRICT`` on by default, and the TWCA chain that Taiwan's
    government sites are served with (the central bank, FSC, MODA, NSTC) fails it with
    "Missing Subject Key Identifier": every Taiwan source failed before its listing was read.
    The chain, the expiry and the host name are still verified; only the RFC 5280 profile
    checks that browsers do not enforce are left out. Built the way ``ssl.create_default_context``
    builds httpx's (certifi's roots, partial chains allowed), as a ``_NoAlpnContext``.
    """
    context = _NoAlpnContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile=certifi.where())
    context.verify_flags |= ssl.VERIFY_X509_PARTIAL_CHAIN
    context.verify_flags &= ~ssl.VERIFY_X509_STRICT
    return context


def listing_byte_limit(config: dict[str, object] | None) -> int:
    """How much of a source's listing may be read: config ``max_response_bytes``, within bounds."""
    raw = (config or {}).get("max_response_bytes")
    if isinstance(raw, bool) or not isinstance(raw, int) or raw <= MAX_RESPONSE_BYTES:
        return MAX_RESPONSE_BYTES
    return min(raw, MAX_LISTING_BYTES)


def _sniff_xml(body: bytes) -> bool:
    """Whether a body served as text/plain is an XML feed (Mistral serves its RSS that way)."""
    head = body[:512].lstrip(b"\xef\xbb\xbf \t\r\n").lower()
    return head.startswith((b"<?xml", b"<rss", b"<feed", b"<rdf:rdf"))
RateLimiter = Callable[[str], Awaitable[None]]


class UnsafeNewsUrl(ValueError):
    pass


class RedisHostRateLimiter:
    """One request per host per second across every news worker process."""

    def __init__(self, redis: Redis, *, interval_ms: int = 1000) -> None:
        self._redis = redis
        self._interval_ms = interval_ms

    async def __call__(self, host: str) -> None:
        deadline = time.monotonic() + 20
        key = f"news:fetch-rate:{host}"
        while True:
            if await self._redis.set(key, "1", nx=True, px=self._interval_ms):
                return
            if time.monotonic() >= deadline:
                raise TimeoutError("news source host rate limiter timed out")
            await asyncio.sleep(0.1)


async def resolve_public_ips(host: str) -> tuple[str, ...]:
    rows = await asyncio.get_running_loop().getaddrinfo(
        host, None, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM
    )
    values: list[str] = []
    for row in rows:
        value = str(row[4][0])
        address = ipaddress.ip_address(value)
        if not address.is_global:
            raise UnsafeNewsUrl("news source resolved to a non-public address")
        if value not in values:
            values.append(value)
    if not values:
        raise UnsafeNewsUrl("news source did not resolve")
    return tuple(values)


def validate_https_url(url: str, allowed_hosts: set[str]) -> tuple[str, int | None]:
    parsed = urlsplit(url)
    host = (parsed.hostname or "").casefold().rstrip(".")
    if (
        parsed.scheme != "https"
        or not host
        or parsed.username is not None
        or parsed.password is not None
        or host not in allowed_hosts
    ):
        raise UnsafeNewsUrl("URL is outside the HTTPS source allow-list")
    try:
        port = parsed.port
    except ValueError as error:
        raise UnsafeNewsUrl("URL has an invalid port") from error
    if port not in {None, 443}:
        raise UnsafeNewsUrl("news sources may only use HTTPS port 443")
    return host, port


def _robots_without_rules(url: str) -> RobotFileParser:
    parser = RobotFileParser()
    parser.set_url(url)
    parser.parse([])
    return parser


def _pinned_url(original: str, ip: str) -> str:
    parsed = urlsplit(original)
    host = f"[{ip}]" if ":" in ip else ip
    return urlunsplit((parsed.scheme, host, parsed.path or "/", parsed.query, ""))


@dataclass
class _HostRate:
    lock: asyncio.Lock
    last_request: float = 0.0


class SafeNewsFetcher:
    def __init__(
        self,
        *,
        client: httpx.AsyncClient | None = None,
        resolver: Resolver = resolve_public_ips,
        timeout_seconds: float = 20.0,
        rate_limiter: RateLimiter | None = None,
    ) -> None:
        self._external_client = client
        self._client = client or httpx.AsyncClient(
            timeout=timeout_seconds, follow_redirects=False, verify=tls_context()
        )
        self._resolver = resolver
        self._distributed_rate_limiter = rate_limiter
        self._rates: dict[str, _HostRate] = {}
        # One scan reads many pages from few hosts, so robots.txt is read once per host
        # for the life of this fetcher (one scan job). None records "not readable".
        self._robots: dict[str, RobotFileParser | None] = {}

    async def close(self) -> None:
        if self._external_client is None:
            await self._client.aclose()

    async def _rate_limit(self, host: str) -> None:
        row = self._rates.setdefault(host, _HostRate(asyncio.Lock()))
        async with row.lock:
            delay = 1.0 - (time.monotonic() - row.last_request)
            if delay > 0:
                await asyncio.sleep(delay)
            if self._distributed_rate_limiter is not None:
                await self._distributed_rate_limiter(host)
            row.last_request = time.monotonic()

    async def _request(
        self,
        url: str,
        allowed_hosts: set[str],
        headers: dict[str, str],
        max_bytes: int = MAX_RESPONSE_BYTES,
    ) -> httpx.Response:
        host, _ = validate_https_url(url, allowed_hosts)
        ips = await self._resolver(host)
        for attempt in range(3):
            await self._rate_limit(host)
            try:
                # The URL contains the validated address, while Host and SNI retain the
                # allow-listed name. This closes the DNS-rebinding gap between validation
                # and connect.
                async with self._client.stream(
                    "GET",
                    _pinned_url(url, ips[0]),
                    headers={**headers, "Host": host, "User-Agent": USER_AGENT},
                    extensions={"sni_hostname": host},
                ) as streamed:
                    if streamed.status_code == 429 or streamed.status_code >= 500:
                        if attempt < 2:
                            await asyncio.sleep(2**attempt)
                            continue
                    declared = streamed.headers.get("content-length")
                    if declared:
                        try:
                            declared_size = int(declared)
                        except ValueError as error:
                            raise UnsafeNewsUrl(
                                "news source returned an invalid content length"
                            ) from error
                        if declared_size > max_bytes:
                            raise UnsafeNewsUrl("news source response is too large")
                    body = bytearray()
                    # aiter_bytes() already undoes gzip/br, and the limit applies to the
                    # decoded size, so a small compressed bomb stops at 2 MB too.
                    async for chunk in streamed.aiter_bytes():
                        body.extend(chunk)
                        if len(body) > max_bytes:
                            raise UnsafeNewsUrl("news source response is too large")
                    # The rebuilt response holds decoded bytes. Keeping Content-Encoding
                    # would make httpx decode them a second time (DecodingError on every
                    # compressed page, which is nearly every real site).
                    response = httpx.Response(
                        streamed.status_code,
                        headers=[
                            (name, value)
                            for name, value in streamed.headers.multi_items()
                            if name.lower() not in {"content-encoding", "content-length"}
                        ],
                        content=bytes(body),
                        request=streamed.request,
                    )
            except (httpx.TimeoutException, httpx.TransportError):
                if attempt == 2:
                    raise
                await asyncio.sleep(2**attempt)
                continue
            return response
        raise RuntimeError("unreachable network retry state")

    async def _robots_allowed(self, url: str, allowed_hosts: set[str]) -> bool:
        parsed = urlsplit(url)
        host, _ = validate_https_url(url, allowed_hosts)
        robots_url = urlunsplit(("https", parsed.netloc, "/robots.txt", "", ""))
        if robots_url not in self._robots:
            parser: RobotFileParser | None = None
            current = robots_url
            redirected = False
            for _ in range(MAX_REDIRECTS + 1):
                # A robots redirect is acceptable only within the original host. Every
                # hop still resolves, pins and verifies its public HTTPS destination.
                response = await self._request(current, {host}, {"Accept": "text/plain"})
                if response.status_code in {301, 302, 303, 307, 308}:
                    location = response.headers.get("location")
                    if not location:
                        break
                    target = urljoin(current, location)
                    try:
                        validate_https_url(target, {host})
                    except UnsafeNewsUrl:
                        break
                    current = target
                    redirected = True
                    continue
                if response.status_code == 429 or response.status_code >= 500:
                    # A transient failure is not a refusal to remember.
                    response.raise_for_status()
                if 400 <= response.status_code < 500:
                    # RFC 9309 §2.3.1.3: an unavailable robots.txt (any other 4xx) places no
                    # restriction. MODA and NSTC answer 404, Ars Technica 405.
                    parser = _robots_without_rules(current)
                elif 200 <= response.status_code < 300:
                    body = response.content[:256_000].decode("utf-8", errors="replace")
                    content_type = response.headers.get("content-type", "").split(";", 1)[0]
                    if redirected and (
                        content_type.casefold() != "text/plain"
                        or not any(
                            line.strip().casefold().startswith("user-agent:")
                            for line in body.splitlines()
                        )
                    ):
                        # The redirect landed on a page that is not a robots file (the central
                        # bank sends /robots.txt to its home page): the site has none, which
                        # restricts nothing, as a 404 would. Its text is not read as rules.
                        parser = _robots_without_rules(current)
                    else:
                        parser = RobotFileParser()
                        parser.set_url(current)
                        parser.parse(body.splitlines())
                break
            self._robots[robots_url] = parser
        cached = self._robots[robots_url]
        return cached is not None and cached.can_fetch(USER_AGENT, url)

    async def fetch(
        self,
        url: str,
        *,
        allowed_hosts: set[str],
        allowed_redirect_hosts: set[str] | None = None,
        etag: str | None = None,
        last_modified: str | None = None,
        check_robots: bool = True,
        max_bytes: int = MAX_RESPONSE_BYTES,
    ) -> FetchResult:
        redirects = allowed_redirect_hosts or set()
        permitted = {host.casefold().rstrip(".") for host in allowed_hosts | redirects}
        current = url
        if check_robots and not await self._robots_allowed(current, permitted):
            raise UnsafeNewsUrl("robots.txt did not permit this fetch")
        headers = {"Accept": ", ".join(ALLOWED_TYPES)}
        if etag:
            headers["If-None-Match"] = etag
        if last_modified:
            headers["If-Modified-Since"] = last_modified
        for _ in range(MAX_REDIRECTS + 1):
            response = await self._request(current, permitted, headers, max_bytes)
            if response.status_code in {301, 302, 303, 307, 308}:
                location = response.headers.get("location")
                if not location:
                    raise UnsafeNewsUrl("redirect omitted Location")
                current = urljoin(current, location)
                validate_https_url(current, permitted)
                if check_robots and not await self._robots_allowed(current, permitted):
                    raise UnsafeNewsUrl("robots.txt did not permit redirected fetch")
                continue
            if response.status_code == 304:
                return FetchResult(
                    url=current,
                    status_code=304,
                    content_type="",
                    body=b"",
                    etag=response.headers.get("etag"),
                    last_modified=response.headers.get("last-modified"),
                    not_modified=True,
                )
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").split(";", 1)[0].casefold()
            if content_type == "text/plain" and _sniff_xml(response.content):
                content_type = "application/xml"
            if content_type not in ALLOWED_TYPES:
                raise UnsafeNewsUrl(f"unsupported content type: {content_type or 'missing'}")
            body = response.content
            return FetchResult(
                url=current,
                status_code=response.status_code,
                content_type=content_type,
                body=body,
                etag=response.headers.get("etag"),
                last_modified=response.headers.get("last-modified"),
            )
        raise UnsafeNewsUrl("too many redirects")
