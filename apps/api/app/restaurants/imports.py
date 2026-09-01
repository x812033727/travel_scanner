from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import httpx

from app.problems import AppError

PLACE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{10,255}$")
EMBEDDED_PLACE_ID_RE = re.compile(r"(?<![A-Za-z0-9_-])((?:ChI|Ei|Gh)[A-Za-z0-9_-]{12,252})")
ALLOWED_GOOGLE_MAP_HOSTS = frozenset(
    {
        "maps.app.goo.gl",
        "goo.gl",
        "www.google.com",
        "maps.google.com",
        "www.google.com.tw",
        "maps.google.com.tw",
        "www.google.co.jp",
        "maps.google.co.jp",
        "www.google.co.kr",
        "maps.google.co.kr",
        "www.google.com.hk",
        "maps.google.com.hk",
        "www.google.com.sg",
        "maps.google.com.sg",
    }
)
SHORT_MAP_HOSTS = frozenset({"maps.app.goo.gl", "goo.gl"})


@dataclass(frozen=True)
class MapsImportResolution:
    place_id: str | None
    expanded_url: str | None
    suggested_query: str | None
    source: str


def _normalized_host(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise AppError(422, "restaurant_maps_url_invalid", "只接受 Google Maps HTTPS 網址")
    if parsed.port not in {None, 443}:
        raise AppError(422, "restaurant_maps_url_invalid", "Google Maps 網址不可使用自訂連接埠")
    host = parsed.hostname.casefold().rstrip(".")
    if host not in ALLOWED_GOOGLE_MAP_HOSTS:
        raise AppError(422, "restaurant_maps_url_host_invalid", "只接受 Google 官方地圖網址")
    return host


def extract_place_id(value: str) -> str | None:
    candidate = value.strip()
    if PLACE_ID_RE.fullmatch(candidate):
        return candidate
    if not candidate.startswith("https://"):
        return None
    _normalized_host(candidate)
    parsed = urlparse(candidate)
    query = parse_qs(parsed.query)
    for key in ("query_place_id", "place_id"):
        for raw in query.get(key, []):
            direct = raw.strip()
            if PLACE_ID_RE.fullmatch(direct):
                return direct
            if match := EMBEDDED_PLACE_ID_RE.search(direct):
                return match.group(1)
    for raw in query.get("q", []):
        direct = raw.removeprefix("place_id:").strip()
        if raw.startswith("place_id:") and PLACE_ID_RE.fullmatch(direct):
            return direct
        if match := EMBEDDED_PLACE_ID_RE.search(direct):
            return match.group(1)
    decoded = unquote(candidate)
    if match := re.search(r"!1s((?:ChI|Ei|Gh)[A-Za-z0-9_-]{12,252})", decoded):
        return match.group(1)
    if match := EMBEDDED_PLACE_ID_RE.search(decoded):
        return match.group(1)
    return None


def suggested_query_from_maps_url(url: str) -> str | None:
    parsed = urlparse(url)
    path_parts = [unquote(item).strip() for item in parsed.path.split("/") if item]
    if "place" in path_parts:
        index = path_parts.index("place")
        if index + 1 < len(path_parts):
            candidate = path_parts[index + 1].replace("+", " ").strip()
            if 2 <= len(candidate) <= 255 and not EMBEDDED_PLACE_ID_RE.fullmatch(candidate):
                return candidate
    query = parse_qs(parsed.query)
    for raw in query.get("query", []) + query.get("q", []):
        candidate = raw.removeprefix("place_id:").strip()
        if 2 <= len(candidate) <= 255 and not EMBEDDED_PLACE_ID_RE.fullmatch(candidate):
            return candidate
    return None


async def resolve_maps_input(
    value: str,
    *,
    client: httpx.AsyncClient | None = None,
    max_redirects: int = 5,
) -> MapsImportResolution:
    raw = value.strip()
    if place_id := extract_place_id(raw):
        return MapsImportResolution(
            place_id,
            raw if raw.startswith("https://") else None,
            None,
            "direct",
        )
    if not raw.startswith("https://"):
        raise AppError(
            422,
            "restaurant_place_id_or_maps_url_required",
            "請貼上 Google Place ID 或 Google Maps 網址",
        )
    host = _normalized_host(raw)
    current = raw
    owns_client = client is None
    active_client = client or httpx.AsyncClient(timeout=10, follow_redirects=False)
    try:
        if host in SHORT_MAP_HOSTS:
            for _ in range(max_redirects):
                try:
                    response = await active_client.get(current, follow_redirects=False)
                except httpx.HTTPError as exc:
                    raise AppError(
                        503,
                        "restaurant_maps_url_unavailable",
                        "目前無法展開 Google Maps 短網址",
                    ) from exc
                if response.status_code not in {301, 302, 303, 307, 308}:
                    current = str(response.url)
                    break
                location = response.headers.get("location")
                if not location:
                    break
                current = urljoin(current, location)
                _normalized_host(current)
            else:
                raise AppError(
                    422,
                    "restaurant_maps_redirect_limit",
                    "Google Maps 網址重新導向過多",
                )
        _normalized_host(current)
        return MapsImportResolution(
            extract_place_id(current),
            current,
            suggested_query_from_maps_url(current),
            "expanded" if current != raw else "url",
        )
    finally:
        if owns_client:
            await active_client.aclose()
