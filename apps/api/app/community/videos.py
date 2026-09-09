"""Reference-only video rendering. Never fetch third-party media on a public read."""

from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta
from typing import Any
from urllib.parse import parse_qs, urlsplit

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.community.policy import aware
from app.models import HotspotGuide, TravelHotspot

VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}", re.ASCII)


def youtube_source_id(url: str) -> str | None:
    try:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.username or parsed.password or parsed.port:
            return None
        if parsed.hostname == "youtu.be":
            identifier = parsed.path.removeprefix("/")
        elif parsed.hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
            if parsed.path == "/watch":
                values = parse_qs(parsed.query).get("v", [])
                identifier = values[0] if len(values) == 1 else ""
            elif parsed.path.startswith(("/shorts/", "/embed/")):
                identifier = parsed.path.rsplit("/", 1)[-1]
            else:
                return None
        else:
            return None
    except ValueError:
        return None
    return identifier if VIDEO_ID.fullmatch(identifier) else None


def youtube_embed_metadata(guide: HotspotGuide, *, now: datetime | None = None) -> dict[str, Any]:
    """Only explicit provider status is proof; editorial approval alone is not."""
    result: dict[str, Any] = {
        "status": "link_only",
        "embed_url": None,
        "metadata_status": "unverified",
        "verified_at": None,
    }
    identifier = guide.provider_content_id or ""
    if (
        guide.provider != "youtube"
        or guide.content_type != "video"
        or guide.review_status != "approved"
        or not VIDEO_ID.fullmatch(identifier)
        or youtube_source_id(guide.canonical_url) != identifier
    ):
        return result
    current = now or datetime.now(UTC)
    if (
        not guide.last_verified_at
        or not guide.metadata_expires_at
        or aware(guide.last_verified_at) > current
        or aware(guide.last_verified_at) < current - timedelta(days=30)
        or aware(guide.metadata_expires_at) <= current
    ):
        if guide.last_verified_at:
            result["metadata_status"] = "stale"
        return result
    status = (guide.metadata_json or {}).get("youtube_status")
    if not isinstance(status, dict) or not isinstance(status.get("embeddable"), bool):
        return result
    if status.get("privacyStatus") not in {"public", "private", "unlisted"}:
        return result
    result.update(metadata_status="verified", verified_at=guide.last_verified_at)
    if status["embeddable"] and status["privacyStatus"] == "public":
        result.update(
            status="embeddable",
            embed_url=f"https://www.youtube-nocookie.com/embed/{identifier}",
        )
    return result


async def public_video_refs(
    session: AsyncSession, references: list[dict[str, str]]
) -> list[dict[str, Any]]:
    identifiers = list(
        dict.fromkeys(
            ref.get("video_id", "")
            for ref in references
            if ref.get("provider") == "youtube" and VIDEO_ID.fullmatch(ref.get("video_id", ""))
        )
    )[:5]
    if not identifiers:
        return []
    guides = (
        await session.scalars(
            select(HotspotGuide)
            .join(TravelHotspot, TravelHotspot.id == HotspotGuide.hotspot_id)
            .where(
                HotspotGuide.provider == "youtube",
                HotspotGuide.content_type == "video",
                HotspotGuide.provider_content_id.in_(identifiers),
                HotspotGuide.review_status == "approved",
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status.in_(["approved", "auto_approved"]),
            )
            .order_by(HotspotGuide.last_verified_at.desc(), HotspotGuide.id)
            .execution_options(populate_existing=True)
        )
    ).all()
    by_id: dict[str, HotspotGuide] = {}
    for guide in guides:
        by_id.setdefault(guide.provider_content_id or "", guide)
    output: list[dict[str, Any]] = []
    for identifier in identifiers:
        candidate = by_id.get(identifier)
        metadata = (
            youtube_embed_metadata(candidate)
            if candidate
            else {
                "status": "link_only",
                "embed_url": None,
                "metadata_status": "unverified",
                "verified_at": None,
            }
        )
        output.append(
            {
                "provider": "youtube",
                "video_id": identifier,
                "source_url": f"https://www.youtube.com/watch?v={identifier}",
                **metadata,
            }
        )
    return output
