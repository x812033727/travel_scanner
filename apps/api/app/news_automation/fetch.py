from __future__ import annotations

import asyncio
import http.client
import ipaddress
import socket
import ssl
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


def tls_context() -> ssl.SSLContext:
    """The verifying TLS context every news fetch uses, without Python 3.13's strict X.509 mode.

    Python 3.13 turned ``VERIFY_X509_STRICT`` on by default, and the TWCA chain that Taiwan's
    government sites are served with (the central bank, FSC, MODA, NSTC) fails it with
    "Missing Subject Key Identifier": every Taiwan source failed before its listing was read.
    The chain, the expiry and the host name are still verified; only the RFC 5280 profile
    checks that browsers do not enforce are left out.
    """
    context = httpx.create_ssl_context()
    context.verify_flags &= ~ssl.VERIFY_X509_STRICT
    return context
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


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """Connect to a checked IP while authenticating the source's original hostname."""

    def __init__(self, ip: str, hostname: str, *, timeout: float) -> None:
        context = tls_context()
        address = f"[{ip}]" if ":" in ip else ip
        super().__init__(address, timeout=timeout, context=context)
        self._tls_context = context
        self._source_hostname = hostname

    def connect(self) -> None:
        plain = socket.create_connection((self.host, self.port), self.timeout)
        try:
            self.sock = self._tls_context.wrap_socket(
                plain, server_hostname=self._source_hostname
            )
        except BaseException:
            plain.close()
            raise


def _pinned_stdlib_request(
    url: str, ip: str, hostname: str, headers: dict[str, str], timeout: float
) -> httpx.Response:
    """Retry a challenged request without httpcore's TLS handshake shape.

    The connection still uses the address checked by resolve_public_ips. The TLS
    certificate is checked against hostname, redirects stay visible to fetch(), and
    the response is capped and must use the requested identity encoding.
    """
    request = httpx.Request(
        "GET",
        _pinned_url(url, ip),
        headers={
            **headers,
            "Host": hostname,
            "User-Agent": USER_AGENT,
            "Accept-Encoding": "identity",
        },
    )
    connection = _PinnedHTTPSConnection(ip, hostname, timeout=timeout)
    received: http.client.HTTPResponse | None = None
    try:
        connection.request(
            "GET", request.url.raw_path.decode("ascii"), headers=dict(request.headers)
        )
        received = connection.getresponse()
        response_headers = received.getheaders()
        if received.status >= 300:
            # The caller only needs the status and Location for errors/redirects.
            # A second challenge can be arbitrarily large or compressed.
            return httpx.Response(
                received.status,
                headers=[
                    (name, value)
                    for name, value in response_headers
                    if name.lower() not in {"content-encoding", "content-length"}
                ],
                content=b"",
                request=request,
            )
        encoding = (received.getheader("content-encoding") or "").casefold()
        if encoding not in {"", "identity"}:
            raise UnsafeNewsUrl("news source ignored identity content encoding")
        declared = received.getheader("content-length")
        declared_size: int | None = None
        if declared:
            try:
                declared_size = int(declared)
            except ValueError as error:
                raise UnsafeNewsUrl("news source returned an invalid content length") from error
            if declared_size < 0:
                raise UnsafeNewsUrl("news source returned an invalid content length")
            if declared_size > MAX_RESPONSE_BYTES:
                raise UnsafeNewsUrl("news source response is too large")
        wire_body = received.read(MAX_RESPONSE_BYTES + 1)
        if len(wire_body) > MAX_RESPONSE_BYTES:
            raise UnsafeNewsUrl("news source response is too large")
        if declared_size is not None and len(wire_body) != declared_size:
            raise httpx.TransportError("news source response ended early", request=request)
    except (OSError, http.client.HTTPException) as error:
        raise httpx.TransportError(str(error), request=request) from error
    finally:
        if received is not None:
            received.close()
        connection.close()

    return httpx.Response(
        received.status,
        headers=[
            (name, value)
            for name, value in response_headers
            if name.lower() not in {"content-encoding", "content-length"}
        ],
        content=wire_body,
        request=request,
    )


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
        self._timeout_seconds = timeout_seconds
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
                    if streamed.status_code in {401, 403} and self._external_client is None:
                        # Try the same checked IP before reading a possibly oversized
                        # challenge body. The alternate transport has its own size cap.
                        await self._rate_limit(host)
                        try:
                            alternate = await asyncio.to_thread(
                                _pinned_stdlib_request,
                                url,
                                ips[0],
                                host,
                                headers,
                                self._timeout_seconds,
                            )
                        except httpx.TransportError:
                            return httpx.Response(
                                streamed.status_code,
                                content=b"",
                                request=streamed.request,
                            )
                        else:
                            if (
                                alternate.status_code == 429 or alternate.status_code >= 500
                            ) and attempt < 2:
                                await asyncio.sleep(2**attempt)
                                continue
                            return alternate
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
                    # aiter_bytes() already undoes gzip/br, and the limit applies to the
                    # decoded size, so a small compressed bomb stops at 2 MB too.
                    async for chunk in streamed.aiter_bytes():
                        body.extend(chunk)
                        if len(body) > MAX_RESPONSE_BYTES:
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
        robots_url = urlunsplit(("https", parsed.netloc, "/robots.txt", "", ""))
        if robots_url not in self._robots:
            response = await self._request(robots_url, allowed_hosts, {"Accept": "text/plain"})
            if response.status_code == 429 or response.status_code >= 500:
                # The host is briefly unavailable; that is not a refusal to remember.
                response.raise_for_status()
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
