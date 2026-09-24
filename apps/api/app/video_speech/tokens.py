"""Video tool tokens: made in the admin panel, shown once, stored as a SHA-256.

A token authorizes exactly one thing, synthesizing narration, so a leaked one can at worst
spend the month's speech budget, and revoking it is immediate.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import VideoToolToken

# A public marker that says what kind of credential a string is, not part of the secret.
TOKEN_PREFIX = "mkv_"  # noqa: S105
PREFIX_SHOWN = 10
# Recording every use would write a row per scene; once a minute is enough to tell whether a
# token is still in use.
LAST_USED_RESOLUTION = timedelta(minutes=1)


def new_token() -> str:
    return f"{TOKEN_PREFIX}{secrets.token_urlsafe(32)}"


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def looks_like_token(token: str) -> bool:
    return token.startswith(TOKEN_PREFIX) and 40 <= len(token) <= 80


async def find_active_token(session: AsyncSession, token: str) -> VideoToolToken | None:
    if not looks_like_token(token):
        return None
    row: VideoToolToken | None = await session.scalar(
        select(VideoToolToken).where(
            VideoToolToken.token_hash == token_hash(token),
            VideoToolToken.revoked_at.is_(None),
        )
    )
    return row


def touch(row: VideoToolToken, now: datetime | None = None) -> bool:
    """Mark the token used; return whether the row changed and needs a commit."""
    moment = now or datetime.now(UTC)
    if row.last_used_at is not None and moment - row.last_used_at < LAST_USED_RESOLUTION:
        return False
    row.last_used_at = moment
    return True
