import asyncio
from collections.abc import AsyncIterator
from typing import Any

import anyio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class Base(DeclarativeBase):
    pass


class CancellationSafeSession(AsyncSession):
    """An ``AsyncSession`` that throws its connection away when a cancellation ends it.

    A task can be cancelled while its session is part-way through a statement: when a
    reader closes the community event stream, Starlette's ``StreamingResponse`` cancels
    the stream whatever query its catch-up is running. The asyncpg connection is then
    still mid-operation, and closing rolls it back and returns it to the pool, from
    where the next request can get "another operation is in progress" or "cannot use
    Connection.transaction() in a manually started transaction" (full-stack-smoke on
    2026-10-04 answered 93 requests with 500). Invalidating closes the connection
    instead, and the pool opens a fresh one.

    The shield matters as much as the invalidation. Starlette cancels through anyio,
    whose cancellation is level-triggered: every await in the cancelled task raises
    again, so cleanup awaited there stops at its first await, and the pool never gets
    the slot back. Any other exit, an error included, closes as usual.
    """

    async def __aexit__(self, type_: Any, value: Any, traceback: Any) -> None:
        if isinstance(value, asyncio.CancelledError):
            with anyio.CancelScope(shield=True):
                await self.invalidate()
            return
        await super().__aexit__(type_, value, traceback)


settings = get_settings()
engine = create_async_engine(settings.database_url, pool_pre_ping=True)
# Typed as the base class: callers take and pass ``async_sessionmaker[AsyncSession]``.
SessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, class_=CancellationSafeSession, expire_on_commit=False
)


def escape_like(value: str) -> str:
    """Escape LIKE/ILIKE metacharacters so user input matches literally.

    Use together with ``column.ilike(pattern, escape="\\\\")``.
    """
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionFactory() as session:
        yield session
