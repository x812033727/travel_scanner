import os

from redis import Redis
from rq import Queue, SimpleWorker, Worker

from app.config import get_settings


def worker_class(os_name: str = os.name) -> type[Worker] | type[SimpleWorker]:
    return SimpleWorker if os_name == "nt" else Worker


def main() -> None:
    connection = Redis.from_url(get_settings().redis_url)
    worker_class()([Queue("alerts", connection=connection)], connection=connection).work()


if __name__ == "__main__":
    main()
