from __future__ import annotations

from typing import Any

from app.admin.service import load_runtime_settings
from app.db import SessionFactory
from app.hotspots.service import collect_hotspots


async def collect_once() -> dict[str, Any]:
    async with SessionFactory() as session:
        return await collect_hotspots(session, await load_runtime_settings(session))
