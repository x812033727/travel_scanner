import logging
from types import SimpleNamespace
from uuid import UUID, uuid4

import httpx
import pytest

from app.hotspots import ai_tasks


class FakeSession:
    def __init__(self, run: SimpleNamespace) -> None:
        self.run = run
        self.added: list[object] = []
        self.commits = 0
        self.rollbacks = 0

    async def __aenter__(self) -> "FakeSession":
        return self

    async def __aexit__(self, *exc: object) -> None:
        return None

    async def get(self, model: type, run_id: UUID) -> SimpleNamespace:
        return self.run

    def add(self, item: object) -> None:
        self.added.append(item)

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rollbacks += 1


def make_run(status: str) -> SimpleNamespace:
    return SimpleNamespace(
        id=uuid4(),
        actor_user_id=uuid4(),
        status=status,
        progress=0,
        progress_json={},
        result_json={},
        error_code=None,
        error_message=None,
        completed_at=None,
    )


@pytest.mark.asyncio
async def test_runs_already_marked_failed_are_never_re_executed(monkeypatch) -> None:
    run = make_run("failed")
    session = FakeSession(run)
    executed: list[tuple[object, ...]] = []

    async def fake_execute(*args: object) -> None:
        executed.append(args)

    monkeypatch.setattr(ai_tasks, "SessionFactory", lambda: session)
    monkeypatch.setattr(ai_tasks, "execute_ai_search", fake_execute)

    await ai_tasks._run(run.id)

    assert executed == []
    assert run.status == "failed"
    assert session.commits == 0


@pytest.mark.asyncio
async def test_provider_failures_are_recorded_with_their_cause(monkeypatch, caplog) -> None:
    run = make_run("queued")
    session = FakeSession(run)
    request = httpx.Request("POST", "https://api.minimax.io/v1/responses")
    response = httpx.Response(
        401,
        json={"base_resp": {"status_code": 2049, "status_msg": "invalid api key"}},
        request=request,
    )

    async def fake_settings(_session: object) -> object:
        return object()

    async def failing_execute(*args: object) -> None:
        raise httpx.HTTPStatusError("unauthorized", request=request, response=response)

    monkeypatch.setattr(ai_tasks, "SessionFactory", lambda: session)
    monkeypatch.setattr(ai_tasks, "load_runtime_settings", fake_settings)
    monkeypatch.setattr(ai_tasks, "get_redis", lambda: object())
    monkeypatch.setattr(ai_tasks, "execute_ai_search", failing_execute)

    with (
        caplog.at_level(logging.WARNING, logger="app.hotspots.ai_tasks"),
        pytest.raises(httpx.HTTPStatusError),
    ):
        await ai_tasks._run(run.id)

    assert run.status == "failed"
    assert run.error_code == "ai_search_failed"
    assert run.error_message == (
        "AI 景點介紹搜尋未能完整完成：HTTP 401 from api.minimax.io: 2049 invalid api key"
    )
    assert run.progress == 100
    assert session.rollbacks == 1
    assert session.commits == 1
    audit = session.added[-1]
    assert audit.action == "hotspot_guide_ai_search_failed"
    assert audit.metadata_json["error_message"].startswith("HTTP 401 from api.minimax.io")
    logged = [record.getMessage() for record in caplog.records]
    assert any(str(run.id) in message and "HTTP 401" in message for message in logged)
