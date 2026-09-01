from types import SimpleNamespace
from uuid import uuid4

from app.hotspots import place_tasks


def test_enrichment_queue_chunks_all_450_hotspots_in_batches_of_25(
    monkeypatch,
) -> None:
    queued: list[tuple[tuple[object, ...], dict[str, object]]] = []
    queue_names: list[str] = []

    class FakeQueue:
        def __init__(self, name: str, *, connection: object) -> None:
            queue_names.append(name)

        def enqueue(self, *args: object, **kwargs: object) -> SimpleNamespace:
            queued.append((args, kwargs))
            return SimpleNamespace(id=f"job-{len(queued)}")

    monkeypatch.setattr(place_tasks.SyncRedis, "from_url", lambda _url: object())
    monkeypatch.setattr(place_tasks, "Queue", FakeQueue)

    jobs = place_tasks.enqueue_place_enrichment_run(
        uuid4(), [uuid4() for _ in range(450)]
    )

    assert queue_names == ["hotspot-places"]
    assert len(jobs) == 18
    assert all(len(args[2]) == 25 for args, _kwargs in queued)
    assert all(kwargs["job_timeout"] == 900 for _args, kwargs in queued)
    assert all(kwargs["retry"].max == 2 for _args, kwargs in queued)
