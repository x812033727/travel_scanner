import asyncio
import logging

from app.config import get_settings
from app.hotspots.jobs import collect_once

logger = logging.getLogger(__name__)


async def run() -> None:
    settings = get_settings()
    if not settings.hotspot_collection_enabled:
        logger.info("Hotspot collection is disabled")
        await asyncio.Event().wait()
    while True:
        try:
            report = await collect_once()
            logger.info("Hotspot collection completed: %s", report)
        except Exception:
            logger.exception("Hotspot collection failed")
        await asyncio.sleep(settings.hotspot_collection_interval_seconds)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())


if __name__ == "__main__":
    main()
