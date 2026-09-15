"""The two operator commands behind the article search: a full reindex and the alias seed.

Kept out of ``app/cli.py`` so they can be exercised against the guides test database
without importing the whole command surface, and out of ``search`` so that module stays
free of the session factory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db import SessionFactory
from app.guides import aliases, search


async def reindex_guide_search(
    *, dry_run: bool = False, factory: async_sessionmaker[AsyncSession] | None = None
) -> dict[str, Any]:
    async with (factory or SessionFactory)() as session:
        report = await search.reindex_all(session)
        if dry_run:
            await session.rollback()
        else:
            await session.commit()
        return {"dry_run": dry_run, **report}


async def seed_guide_aliases(
    *,
    terms_file: Path | None = None,
    dry_run: bool = False,
    factory: async_sessionmaker[AsyncSession] | None = None,
) -> dict[str, Any]:
    try:
        rows = aliases.seed_rows(terms_file)
    except FileNotFoundError as error:
        raise SystemExit(f"Alias file not found: {error}") from error
    async with (factory or SessionFactory)() as session:
        report = await aliases.apply_seed(session, rows, dry_run=dry_run)
        if dry_run:
            await session.rollback()
        else:
            await session.commit()
        return {"rows": len(rows), **report}
