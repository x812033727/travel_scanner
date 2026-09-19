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


def configure_logging() -> None:
    """INFO for the collector's own progress lines, WARNING for the HTTP client.

    httpx logs every request URL at INFO, and until 2026-09-19 those URLs carried the
    YouTube API key, which the Docker log driver then kept. The keys travel in a header
    now, but query strings still carry search terms and place names, so the client's
    request log stays off.
    """
    logging.basicConfig(level=logging.INFO)
    for noisy in ("httpx", "httpcore"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def main() -> None:
    configure_logging()
    asyncio.run(run())


if __name__ == "__main__":
    main()
