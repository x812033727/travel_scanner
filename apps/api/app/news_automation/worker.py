"""The news queue's own worker (compose service ``news-worker``, profile ``news``).

One candidate is twenty-odd model calls and may run for up to an hour. In the general
worker it would hold the only process that also serves search and trip routing, so the
``news`` queue is deliberately absent from ``app.worker.QUEUE_NAMES``.
"""

from __future__ import annotations

from redis import Redis
from rq import Queue

from app.config import get_settings
from app.worker import worker_class

QUEUE_NAME = "news"


def main() -> None:
    connection = Redis.from_url(get_settings().redis_url)
    # with_scheduler moves Retry(interval=...) and enqueue_in jobs back onto this queue.
    worker_class()([Queue(QUEUE_NAME, connection=connection)], connection=connection).work(
        with_scheduler=True
    )


if __name__ == "__main__":
    main()
