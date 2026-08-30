from rq import SimpleWorker, Worker

from app.worker import worker_class


def test_worker_uses_simple_worker_when_fork_is_unavailable() -> None:
    assert worker_class("nt") is SimpleWorker
    assert worker_class("posix") is Worker
