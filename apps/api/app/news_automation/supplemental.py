"""Opt-in links to an official article's own documentation, never a second publisher.

This only selects links. The scanner still owns fetching, redirects, extraction and
evidence hashes, and never follows links found inside a supplemental page.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Protocol
from urllib.parse import SplitResult, urlsplit

MAX_SUPPLEMENTAL_PAGES = 2
MAX_SUPPLEMENTAL_PATHS = 8
_AMBIGUOUS_PATH = re.compile(r"%(?:2e|2f|5c|25)", re.IGNORECASE)


class SupplementalSource(Protocol):
    @property
    def url(self) -> str: ...

    @property
    def enabled(self) -> bool: ...

    @property
    def role(self) -> str: ...

    @property
    def is_first_party(self) -> bool: ...

    @property
    def config_json(self) -> Mapping[str, object]: ...


def _plain_path(path: str) -> bool:
    return (
        path.startswith("/")
        and not path.startswith("//")
        and "\\" not in path
        and not _AMBIGUOUS_PATH.search(path)
        and not any(part in {".", ".."} for part in path.split("/"))
        and not any(ord(character) <= 32 for character in path)
    )


def _paths(source: SupplementalSource | None) -> tuple[str, ...]:
    if (
        source is None
        or source.enabled is not True
        or source.is_first_party is not True
        or source.role != "evidence"
    ):
        return ()
    config = source.config_json
    if not isinstance(config, Mapping):
        return ()
    raw = config.get("supplemental_paths")
    if not isinstance(raw, list) or not 1 <= len(raw) <= MAX_SUPPLEMENTAL_PATHS:
        return ()
    if any(
        not isinstance(path, str)
        or not 1 < len(path) <= 256
        or not _plain_path(path)
        or "?" in path
        or "#" in path
        for path in raw
    ):
        return ()  # A malformed configuration fails closed as a whole.
    return tuple(raw)


def _url(value: str) -> SplitResult | None:
    if any(ord(character) <= 32 for character in value) or "\\" in value:
        return None
    try:
        parsed = urlsplit(value)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.port not in {None, 443}
            or not _plain_path(parsed.path or "/")
        ):
            return None
    except ValueError:
        return None
    return parsed


def is_supplemental_url(
    source: SupplementalSource | None, primary: str, url: str
) -> bool:
    """Require an enabled first-party source, exact host and an approved path boundary."""
    paths = _paths(source)
    if not paths or source is None:
        return False
    configured, origin, target = _url(source.url), _url(primary), _url(url)
    if configured is None or origin is None or target is None:
        return False
    if not configured.hostname == origin.hostname == target.hostname:
        return False
    # Tracking queries and fragments do not turn the lead page into a second document.
    if target.path.rstrip("/") == origin.path.rstrip("/"):
        return False
    return any(
        target.path == prefix.rstrip("/") or target.path.startswith(prefix.rstrip("/") + "/")
        for prefix in paths
    )


def supplemental_urls(
    source: SupplementalSource | None,
    primary: str,
    links: Iterable[str],
    *,
    excluded_suffixes: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Choose at most two distinct in-story document paths, in their original order.

    The caller counts attempts, including refused or unreadable pages. No additional
    links are selected to replace a failed request, and no URL is synthesized.
    """
    if not _paths(source):
        return ()
    chosen: list[str] = []
    paths: set[str] = set()
    for url in links:
        if not is_supplemental_url(source, primary, url):
            continue
        path = urlsplit(url).path
        if path.casefold().endswith(excluded_suffixes) or path.rstrip("/") in paths:
            continue
        paths.add(path.rstrip("/"))
        chosen.append(url)
        if len(chosen) == MAX_SUPPLEMENTAL_PAGES:
            break
    return tuple(chosen)
