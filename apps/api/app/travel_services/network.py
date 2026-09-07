"""Bounded, DNS-pinned HTTPS requests; no page bodies retained for link checks."""

import asyncio
from urllib.parse import parse_qs, urljoin, urlsplit

import httpx

from app.catalog_review.evidence import public_request_target
from app.travel_services.registry import affiliate_target, brand_target
from app.travel_services.schemas import safe_url


async def verify_link(
    url: str, code: str, expected: str, *, marker: str | None = None, project: str | None = None
) -> bool:
    current = safe_url(url)
    expected = brand_target(code, expected)
    tracking_verified = marker is None and project is None
    async with asyncio.timeout(25), httpx.AsyncClient(trust_env=False, timeout=8) as client:
        for _ in range(6):
            parsed = urlsplit(current)
            query = parse_qs(parsed.query)
            if parsed.hostname == "tp.media" and marker and project:
                if query.get("marker") == [marker] and query.get("trs") == [project]:
                    tracking_verified = True
            try:
                affiliate_target(current)
            except ValueError:
                brand_target(code, current)
            pinned = await public_request_target(current)
            if pinned is None:
                return False
            target, host = pinned
            async with client.stream(
                "GET",
                target,
                headers={"Host": host, "Connection": "close"},
                extensions={"sni_hostname": host},
                follow_redirects=False,
            ) as response:
                if response.is_redirect:
                    location = response.headers.get("location")
                    if not location:
                        return False
                    current = safe_url(urljoin(current, location))
                    continue
                brand_target(code, current)
                expected_parts = urlsplit(expected)
                expected_query = parse_qs(expected_parts.query, keep_blank_values=True)
                actual_query = parse_qs(urlsplit(current).query, keep_blank_values=True)
                return bool(
                    tracking_verified
                    and response.status_code == 200
                    and urlsplit(current).path.rstrip("/") == expected_parts.path.rstrip("/")
                    and all(actual_query.get(k) == v for k, v in expected_query.items())
                )
    return False
