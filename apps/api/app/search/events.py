import json
from typing import Any
from uuid import UUID

from redis.asyncio import Redis


def stream_key(search_id: UUID) -> str:
    return f"search:events:{search_id}"


async def publish_event(
    redis: Redis,
    search_id: UUID,
    event: str,
    progress: int,
    data: dict[str, Any] | None = None,
) -> str:
    payload = {"search_id": str(search_id), "progress": progress, **(data or {})}
    event_id = await redis.xadd(
        stream_key(search_id),
        {"event": event, "data": json.dumps(payload, ensure_ascii=False, default=str)},
        maxlen=500,
        approximate=True,
    )
    await redis.expire(stream_key(search_id), 3600)
    return str(event_id)
