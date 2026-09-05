"""CLI entry point for filling food merchant coordinates from their cited pages.

The URLs come from ``food_merchant_sources``, which administrators and seed data write, and
this process runs inside the compose stack next to postgres and redis. So the fetcher treats
every stored URL as untrusted input: https only, no redirect it has not re-checked, and no
host that resolves to a private, loopback, link-local or otherwise non-global address. That
closes the obvious blind-SSRF path — one edited source row aiming the fetcher at
``http://postgres:5432`` or a cloud metadata endpoint.

The check resolves the hostname and then lets httpx resolve it again to connect, so a name
that answers differently between the two lookups is not covered. Pinning the address would
mean hand-rolling the connection; against an attacker who can already write source rows the
extra cost buys little, and the response never reaches a user — only a coordinate inside the
country box is ever stored.
"""

from __future__ import annotations

import asyncio
import ipaddress
import socket
import sys
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import urljoin, urlsplit

import httpx

from app.db import SessionFactory
from app.foods.coordinate_fill import (
    FetchResult,
    fill_merchant_coordinates,
    merchant_page_sources,
    merchants_without_coordinates,
    summarize,
)

USER_AGENT = "MokaairBot/1.0 (+https://mokaair.com; food merchant coordinate check)"
# Big enough for a restaurant page with its JSON-LD, small enough that one endless response
# cannot stall the batch. Enforced while streaming, so a compressed bomb stops here too.
MAX_BYTES = 3_000_000
MAX_REDIRECTS = 3
# The whole-request deadline, redirects and slow trickling included.
TOTAL_SECONDS = 45.0

Resolver = Callable[[str], list[str]]


def system_resolver(host: str) -> list[str]:
    infos = socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
    return [str(info[4][0]) for info in infos]


def is_public_https_url(url: str, resolve: Resolver = system_resolver) -> bool:
    """Whether this URL is https and every address its host resolves to is on the internet."""

    parts = urlsplit(url)
    if parts.scheme != "https" or not parts.hostname:
        return False
    try:
        addresses = resolve(parts.hostname)
    except OSError:
        return False
    if not addresses:
        return False
    for address in addresses:
        try:
            ip = ipaddress.ip_address(address)
        except ValueError:
            return False
        if not ip.is_global or ip.is_multicast:
            return False
    return True


def same_site(first: str, second: str) -> bool:
    """Whether two URLs sit on the same site, allowing only a www/apex style hop."""

    a = (urlsplit(first).hostname or "").lower()
    b = (urlsplit(second).hostname or "").lower()
    if not a or not b:
        return False
    return a == b or a.endswith(f".{b}") or b.endswith(f".{a}")


async def read_capped(response: httpx.Response) -> str:
    chunks: list[bytes] = []
    total = 0
    async for chunk in response.aiter_bytes():
        chunks.append(chunk)
        total += len(chunk)
        if total >= MAX_BYTES:
            break
    body = b"".join(chunks)[:MAX_BYTES]
    return body.decode(response.encoding or "utf-8", errors="replace")


def build_fetcher(
    client: httpx.AsyncClient, resolve: Resolver = system_resolver
) -> Callable[[str], Awaitable[FetchResult]]:
    """A fetcher that re-checks every hop, so a redirect cannot walk into the private network.

    httpx has no whole-request deadline — its read timeout restarts on every socket read, so a
    server trickling one byte at a time never trips it. ``asyncio.timeout`` supplies the
    deadline that actually bounds a run.
    """

    async def walk(url: str) -> FetchResult:
        start = url
        for _ in range(MAX_REDIRECTS + 1):
            if not is_public_https_url(url, resolve):
                return FetchResult(None, "blocked_url")
            async with client.stream("GET", url) as response:
                if response.is_redirect:
                    location = response.headers.get("location")
                    if not location:
                        return FetchResult(None, "redirect_without_target")
                    url = urljoin(url, location)
                    # The cited URL is what gets stored as provenance, so a hop off the
                    # cited site would make that citation describe a page it did not come
                    # from. Refuse rather than quietly re-attribute the coordinate.
                    if not same_site(start, url):
                        return FetchResult(None, "redirect_offsite")
                    continue
                if response.status_code != 200:
                    return FetchResult(None, f"http_{response.status_code}")
                content_type = response.headers.get("content-type", "")
                if "html" not in content_type and "xml" not in content_type:
                    return FetchResult(None, "not_html")
                return FetchResult(await read_capped(response), "ok")
        return FetchResult(None, "too_many_redirects")

    async def fetch(url: str) -> FetchResult:
        try:
            async with asyncio.timeout(TOTAL_SECONDS):
                return await walk(url)
        except TimeoutError:
            return FetchResult(None, "timeout")

    return fetch


async def fill_food_merchant_coordinates(
    destination_ids: list[str],
    limit: int | None,
    apply: bool,
) -> dict[str, Any]:
    async with SessionFactory() as session:
        merchants = await merchants_without_coordinates(
            session,
            destination_ids=tuple(destination_ids),
            limit=limit,
        )
        sources = await merchant_page_sources(session, merchants)
        # Reading opened a transaction; end it before the slow part so a dry run, which never
        # commits, does not hold one open across every fetch. Writes autobegin a new one.
        await session.rollback()
        timeout = httpx.Timeout(20.0, connect=10.0)
        async with httpx.AsyncClient(
            headers={"User-Agent": USER_AGENT, "Accept-Language": "en;q=0.8"},
            follow_redirects=False,
            timeout=timeout,
        ) as client:
            reports = await fill_merchant_coordinates(
                session,
                merchants,
                sources,
                build_fetcher(client),
                apply=apply,
                progress=lambda line: print(line, file=sys.stderr, flush=True),
                pause=asyncio.sleep,
            )
    report = summarize(reports)
    report["applied"] = apply
    return report
