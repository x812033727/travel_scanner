"""The worker's knock: what is due on the Shorts calendar is done now
(docs/videos/SHORTS.md §誰在什麼時候動手).

The API has no scheduler for videos, and the review store and the channel's grant are only in
the API container. So the clock is the worker's, which knocks at the start of every round, and
the work is done here, in the request: mark what the site finished scheduling, lock the slots
whose time has come, send what may go out, read the numbers that are due, and once a day check
that the grant still works. One knock runs at a time. The answer is counts and nothing else.
"""

from __future__ import annotations

import logging
import secrets
from datetime import UTC, datetime

import httpx
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.video_reviews.admin_service import review_store
from app.video_shorts import publish, stats
from app.video_shorts.quota import QUOTA_REASONS, Quota, pacific_day
from app.video_shorts.schemas import TickOut
from app.video_shorts.settings import channel_facts, settings_row
from app.video_shorts.slots import lock_due_slots
from app.video_youtube import connection
from app.video_youtube.client import YoutubeClient, YoutubeError
from app.video_youtube.errors import Refused

logger = logging.getLogger(__name__)

LOCK_KEY = "video:shorts:tick"
# Longer than a knock takes, shorter than the worker's round: a knock that died lets the next
# one in.
LOCK_SECONDS = 240
VERIFIED_KEY = "video:shorts:verified:{day}"
VERIFIED_SECONDS = 60 * 60 * 50
BUSY = "上一次敲門還在跑"
NO_REDIS = "Redis 沒有回應，這一輪不做"


async def _read(session: AsyncSession, quota: Quota, now: datetime) -> stats.Read:
    """The numbers that are due, or nothing when YouTube cannot be asked."""
    try:
        async with connection.http_client() as http:
            client = YoutubeClient(http, await connection.access_token(session, http))
            read = await stats.read_due(session, client, quota, now)
            await session.commit()
            return read
    except Refused:
        # The grant is lost: the connection says so on its card, and the top row with it.
        await session.rollback()
    except YoutubeError as error:
        await session.rollback()
        if error.reason in QUOTA_REASONS:
            await quota.mark_refused()
        else:
            logger.warning("the Shorts' numbers could not be read: %s", error)
    except httpx.HTTPError as error:
        await session.rollback()
        logger.warning("the Shorts' numbers could not be read: YouTube is unreachable: %s", error)
    return stats.Read()


async def _verify_daily(session: AsyncSession, redis: Redis, quota: Quota, now: datetime) -> bool:
    """Once a Pacific day, ask YouTube whether the grant still speaks for the channel."""
    key = VERIFIED_KEY.format(day=pacific_day(now))
    try:
        if await redis.exists(key):
            return False
    except RedisError:
        return False
    try:
        view = await connection.verify(session)
    except Refused:
        # YouTube could not be asked: the next knock asks again.
        await session.rollback()
        return False
    try:
        await redis.set(key, "1", ex=VERIFIED_SECONDS)
    except RedisError:
        pass
    if view.problem is not None:
        # The grant is lost, or speaks for another channel: the card says so.
        return False
    await quota.add("channels.list")
    return True


async def tick(session: AsyncSession, redis: Redis, now: datetime | None = None) -> TickOut:
    moment = now or datetime.now(UTC)
    token = secrets.token_hex(8)
    try:
        if not await redis.set(LOCK_KEY, token, nx=True, ex=LOCK_SECONDS):
            return TickOut(ran=False, skipped=BUSY)
    except RedisError:
        return TickOut(ran=False, skipped=NO_REDIS)
    try:
        row = await settings_row(session)
        # What was scheduled since the last knock is marked first: a slot whose Short is on
        # YouTube's schedule is not one that ran out of time.
        scheduled = await publish.settle(session, moment)
        changes = await lock_due_slots(session, moment)
        await session.commit()
        channel = await channel_facts(session)
        quota = Quota(redis, moment)
        store = review_store(await load_runtime_settings(session))
        sent = await publish.send_due(session, store, row, channel, quota, moment)
        usable = channel.linked and not channel.problem
        read = (
            await _read(session, quota, moment)
            if usable and await quota.allows_reading()
            else stats.Read()
        )
        verified = (
            await _verify_daily(session, redis, quota, moment)
            if usable and await quota.allows_sending()
            else False
        )
        answer = TickOut(
            ran=True,
            locked=sum(1 for change in changes if change.status == "locked"),
            missed=sum(1 for change in changes if change.status == "missed"),
            sent=sent.sent,
            held=sent.held,
            scheduled=scheduled,
            published=read.published,
            snapshots=read.snapshots,
            removed=read.removed,
            verified=verified,
            quota_units=await quota.spent(),
        )
        row = await settings_row(session, lock=True)
        row.last_tick_at = moment
        row.last_tick = answer.model_dump(mode="json")
        await session.commit()
        return answer
    finally:
        try:
            if await redis.get(LOCK_KEY) == token:
                await redis.delete(LOCK_KEY)
        except RedisError:
            pass
