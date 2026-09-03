from rq import SimpleWorker, Worker

from app import worker
from app.worker import worker_class


def test_worker_uses_simple_worker_when_fork_is_unavailable() -> None:
    assert worker_class("nt") is SimpleWorker
    assert worker_class("posix") is Worker


def test_main_listens_on_every_queue_and_runs_the_scheduler(monkeypatch) -> None:
    names: list[str] = []
    calls: dict[str, object] = {}

    class FakeQueue:
        def __init__(self, name: str, *, connection: object) -> None:
            names.append(name)

    class FakeWorker:
        def __init__(self, queues: list[object], *, connection: object) -> None:
            calls["queues"] = queues

        def work(self, **kwargs: object) -> None:
            calls["work"] = kwargs

    monkeypatch.setattr(worker.Redis, "from_url", lambda _url: object())
    monkeypatch.setattr(worker, "Queue", FakeQueue)
    monkeypatch.setattr(worker, "worker_class", lambda: FakeWorker)

    worker.main()

    assert names == list(worker.QUEUE_NAMES)
    assert "hotspot-guides" in names
    assert len(calls["queues"]) == len(worker.QUEUE_NAMES)  # type: ignore[arg-type]
    # Retry(interval=...) jobs only leave the ScheduledJobRegistry when a scheduler runs.
    assert calls["work"] == {"with_scheduler": True}
