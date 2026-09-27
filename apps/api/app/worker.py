import os

from redis import Redis
from rq import Queue, SimpleWorker, Worker

from app.config import get_settings

QUEUE_NAMES = (
    "search",
    "trip-routes",
    "hotspot-guides",
    "hotspot-intros",
    "hotspot-places",
    "catalog-review",
    "restaurant-scans",
    "analytics",
    "travel-services",
    "auth-revocations",
    "community",
    # "news" has its own worker (app.news_automation.worker): one candidate can hold a
    # worker for an hour, which must not happen to the process serving search.
)


def worker_class(os_name: str = os.name) -> type[Worker] | type[SimpleWorker]:
    return SimpleWorker if os_name == "nt" else Worker


def main() -> None:
    connection = Redis.from_url(get_settings().redis_url)
    queues = [Queue(name, connection=connection) for name in QUEUE_NAMES]
    # Jobs enqueued with Retry(interval=...) are parked in the ScheduledJobRegistry
    # after a failure. Only the worker-side scheduler moves them back onto the
    # queue, so without it every retry in this codebase silently never runs.
    worker_class()(queues, connection=connection).work(with_scheduler=True)


if __name__ == "__main__":
    main()
