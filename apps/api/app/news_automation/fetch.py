from __future__ import annotations

import asyncio
import ipaddress
import socket
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

import httpx
from redis.asyncio import Redis

from app.news_automation.schemas import FetchResult

USER_AGENT = "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
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
        self._client = client or httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=False)
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
        self, url: str, allowed_hosts: set[str], headers: dict[str, str]
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
                        if declared_size > MAX_RESPONSE_BYTES:
                            raise UnsafeNewsUrl("news source response is too large")
                    body = bytearray()
                    async for chunk in streamed.aiter_bytes():
                        body.extend(chunk)
                        if len(body) > MAX_RESPONSE_BYTES:
                            raise UnsafeNewsUrl("news source response is too large")
                    response = httpx.Response(
                        streamed.status_code,
                        headers=streamed.headers,
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
        robots_url = urlunsplit(("https", parsed.netloc, "/robots.txt", "", ""))
        if robots_url not in self._robots:
            response = await self._request(robots_url, allowed_hosts, {"Accept": "text/plain"})
            parser: RobotFileParser | None = None
            if 200 <= response.status_code < 300:
                body = response.content[:256_000].decode("utf-8", errors="replace")
                parser = RobotFileParser()
                parser.set_url(robots_url)
                parser.parse(body.splitlines())
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
            response = await self._request(current, permitted, headers)
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
