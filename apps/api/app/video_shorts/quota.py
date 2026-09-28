"""What the Shorts' calls take of the day's YouTube quota, counted in Redis.

A Cloud project has 10,000 units a day, reset at midnight Pacific time
(developers.google.com/youtube/v3/determine_quota_cost, read 2026-09-28). Sending a Short is
what the units are for, so reading stops first: past four fifths of the day's units the numbers
are no longer read, and once YouTube refuses a call for the quota nothing is asked again until
the day turns.
"""

from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from redis.asyncio import Redis
from redis.exceptions import RedisError

DAILY_UNITS = 10_000
READING_STOPS_AT = 8_000
PACIFIC = ZoneInfo("America/Los_Angeles")
COSTS = {
    "channels.list": 1,
    "videos.list": 1,
    "playlistItems.list": 1,
    "videos.update": 50,
    # One run of app.video_youtube.sync on an uploaded Short: videos.list, videos.update,
    # captions.list and one captions.insert.
    "sync": 501,
}
# A little over two days, so the counter of a day outlives the day wherever the host's clock is.
KEEP_SECONDS = 60 * 60 * 50
QUOTA_REASONS = frozenset({"quotaExceeded", "dailyLimitExceeded", "rateLimitExceeded"})


def pacific_day(now: datetime | None = None) -> str:
    return (now or datetime.now(UTC)).astimezone(PACIFIC).date().isoformat()


class Quota:
    """The day's counter. Redis being away never stops a Short from going out: the counter
    then reads as nothing spent, and YouTube's own refusal is what stops the calls."""

    def __init__(self, redis: Redis, now: datetime | None = None) -> None:
        self.redis = redis
        day = pacific_day(now)
        self.units_key = f"video:shorts:quota:{day}"
        self.refused_key = f"video:shorts:quota-refused:{day}"

    async def spent(self) -> int:
        try:
            return int(await self.redis.get(self.units_key) or 0)
        except (RedisError, ValueError):
            return 0

    async def add(self, call: str, times: int = 1) -> None:
        if times <= 0:
            return
        try:
            await self.redis.incrby(self.units_key, COSTS[call] * times)
            await self.redis.expire(self.units_key, KEEP_SECONDS)
        except RedisError:
            return

    async def refused(self) -> bool:
        """Whether YouTube already refused a call for the quota today."""
        try:
            return bool(await self.redis.exists(self.refused_key))
        except RedisError:
            return False

    async def mark_refused(self) -> None:
        try:
            await self.redis.set(self.refused_key, "1", ex=KEEP_SECONDS)
        except RedisError:
            return

    async def allows_sending(self) -> bool:
        return not await self.refused()

    async def allows_reading(self) -> bool:
        return not await self.refused() and await self.spent() < READING_STOPS_AT
