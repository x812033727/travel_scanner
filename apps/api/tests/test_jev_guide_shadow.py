"""The Jev shadow pass must measure the guide assessor without ever disturbing it.

Everything here is about the same promise from different angles: whatever Jev does --
answer, refuse, time out, run out of budget, come back half empty -- the run that owns
the decision keeps its own answer and keeps going.
"""

from __future__ import annotations

from typing import Any, cast

import httpx
import pytest
from redis.asyncio import Redis

from app.ai.jev import JevRequestTooLarge
from app.ai.jev import jev_client as real_jev_client
from app.config import Settings
from app.hotspots import ai_search
from app.hotspots.guides import GuideCandidate


def _candidate(index: int) -> GuideCandidate:
    return GuideCandidate(
        content_type="article",
        provider="brave",
        locale="zh-TW",
        title=f"候選 {index}",
        creator_name="someone",
        canonical_url=f"https://example.com/{index}",
        summary="一篇關於這個景點的介紹",
    )


def _score(candidate_id: str, relevance: int, detected: str = "zh-TW") -> Any:
    return ai_search.CandidateAssessment(
        candidate_id=candidate_id,
        relevance_score=relevance,
        quality_score=70,
        detected_locale=detected,
        language_confidence=0.9,
        recommendation_reason="ok",
    )


def _inputs(count: int = 2) -> tuple[dict[str, GuideCandidate], dict[str, Any]]:
    by_id = {f"c{index}": _candidate(index) for index in range(count)}
    scores = {
        candidate_id: _score(candidate_id, 80 if index == 0 else 20)
        for index, candidate_id in enumerate(by_id)
    }
    return by_id, scores


class FakeRedis:
    def __init__(self, allow: int = 99) -> None:
        self.allow = allow
        self.calls = 0

    async def eval(self, _script: str, _keys: int, _key: str, _limit: str) -> int:
        self.calls += 1
        return 1 if self.calls <= self.allow else -1


def _shadow_settings(**overrides: object) -> Settings:
    return Settings(
        jev_shadow_guide_assessment="shadow",
        jev_api_key="jev-test-key",
        **overrides,  # type: ignore[arg-type]
    )


def _answers(values: dict[str, float]) -> dict[str, Any]:
    return {
        "model": "jev-1.13.0",
        "answers": {key: {"type": "noul", "noul": value} for key, value in values.items()},
        "usage": {"input_tokens": 120, "output_tokens": 0},
    }


def _transport(handler: Any) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


async def _run(settings: Settings, redis: Any, monkeypatch: Any, client: Any = None) -> Any:
    by_id, scores = _inputs()
    if client is not None:
        monkeypatch.setattr(ai_search, "jev_client", lambda s, _c=None: real_jev_client(s, client))
    return await ai_search._jev_shadow_assessment(
        settings,
        redis,
        locale="zh-TW",
        context={"attraction": {"name": "台北101"}, "requested_locale": "zh-TW"},
        by_id=by_id,
        scores=scores,
    )


@pytest.mark.asyncio
async def test_shadow_is_off_by_default_and_touches_nothing(monkeypatch) -> None:
    """The measuring pass must cost nothing at all until somebody turns it on."""

    def explode(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("a Jev client must not be built while shadow is off")

    monkeypatch.setattr(ai_search, "jev_client", explode)
    redis = FakeRedis()
    by_id, scores = _inputs()

    assert Settings().jev_shadow_guide_assessment == "off"
    outcome = await ai_search._jev_shadow_assessment(
        Settings(),
        cast("Redis", redis),
        locale="zh-TW",
        context={},
        by_id=by_id,
        scores=scores,
    )

    assert outcome is None
    assert redis.calls == 0, "shadow must not spend the Jev budget while it is off"


@pytest.mark.asyncio
async def test_a_missing_key_is_reported_rather_than_raised() -> None:
    outcome = await ai_search._jev_shadow_assessment(
        Settings(jev_shadow_guide_assessment="shadow", jev_api_key=None),
        cast("Redis", FakeRedis()),
        locale="zh-TW",
        context={},
        by_id=_inputs()[0],
        scores=_inputs()[1],
    )
    assert outcome == {"error": "jev_not_configured", "rows": []}


@pytest.mark.asyncio
async def test_rows_compare_jev_against_the_line_the_run_actually_used(monkeypatch) -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json=_answers({"c0": 0.97, "c1": 0.02}))

    async with _transport(handler) as client:
        outcome = await _run(_shadow_settings(), FakeRedis(), monkeypatch, client)

    assert outcome is not None
    assert len(captured) == 1, "every candidate rides in one call"
    rows = {row["candidate_id"]: row for row in outcome["rows"]}
    # c0 scored 80 and Jev is sure; c1 scored 20 and Jev is sure it is not. Both agree.
    assert rows["c0"]["shipped_accepted"] is True
    assert rows["c0"]["jev_accepted"] is True
    assert rows["c0"]["agreed"] is True
    assert rows["c1"]["shipped_accepted"] is False
    assert rows["c1"]["agreed"] is True
    assert outcome["usage"] == {"calls": 1, "input_tokens": 120}
    assert "errors" not in outcome


@pytest.mark.asyncio
async def test_a_confident_answer_about_chinese_is_still_only_confirm(monkeypatch) -> None:
    """The measured tier has to carry the same non-English guard the real path would."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=_answers({"c0": 0.99, "c1": 0.99}))

    async with _transport(handler) as client:
        outcome = await _run(_shadow_settings(), FakeRedis(), monkeypatch, client)

    assert outcome is not None
    assert {row["jev_tier"] for row in outcome["rows"]} == {"confirm"}

    async with _transport(handler) as client:
        opted_in = await _run(
            _shadow_settings(jev_cjk_autopilot_enabled=True), FakeRedis(), monkeypatch, client
        )
    assert opted_in is not None
    assert {row["jev_tier"] for row in opted_in["rows"]} == {"act"}


@pytest.mark.asyncio
async def test_a_rejected_key_is_recorded_and_never_raised(monkeypatch) -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"message": "bad key"})

    async with _transport(handler) as client:
        outcome = await _run(_shadow_settings(), FakeRedis(), monkeypatch, client)

    assert outcome is not None
    assert outcome["rows"] == []
    assert outcome["errors"], "a failure has to leave a trace, just not an exception"
    assert "jev-test-key" not in str(outcome)


@pytest.mark.asyncio
async def test_an_exhausted_budget_stops_the_measurement_not_the_run(monkeypatch) -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        raise AssertionError("no call may be made once the budget is spent")

    async with _transport(handler) as client:
        outcome = await _run(_shadow_settings(), FakeRedis(allow=0), monkeypatch, client)

    assert outcome is not None
    assert outcome["errors"] == ["jev_quota_exhausted"]
    assert outcome["rows"] == []


@pytest.mark.asyncio
async def test_an_oversized_batch_splits_instead_of_giving_up(monkeypatch) -> None:
    """The split follows the client's own size refusal, not a guessed chunk size."""
    seen: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = request.read().decode()
        asked = [key for key in ("c0", "c1") if f'"{key}"' in body]
        seen.append(len(asked))
        return httpx.Response(200, json=_answers({key: 0.9 for key in asked}))

    settings = _shadow_settings()
    async with _transport(handler) as client:
        jev = real_jev_client(settings, client)
        jev.max_state_tokens = 10_000

        original = jev.ask
        calls = {"n": 0}

        async def ask(state: Any, questions: Any) -> Any:
            calls["n"] += 1
            if calls["n"] == 1:
                raise JevRequestTooLarge("too big; split the batch")
            return await original(state, questions)

        jev.ask = ask  # type: ignore[method-assign]
        monkeypatch.setattr(ai_search, "jev_client", lambda *_a, **_k: jev)
        by_id, scores = _inputs()
        outcome = await ai_search._jev_shadow_assessment(
            settings,
            cast("Redis", FakeRedis()),
            locale="zh-TW",
            context={},
            by_id=by_id,
            scores=scores,
        )

    assert outcome is not None
    assert seen == [1, 1], "the batch of two was halved and both halves were asked"
    assert {row["candidate_id"] for row in outcome["rows"]} == {"c0", "c1"}


@pytest.mark.asyncio
async def test_a_half_empty_answer_drops_only_the_rows_it_is_missing(monkeypatch) -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=_answers({"c0": 0.9, "c1": 0.9}))

    async with _transport(handler) as client:
        monkeypatch.setattr(ai_search, "jev_client", lambda s, _c=None: real_jev_client(s, client))
        by_id, scores = _inputs()
        scores.pop("c1")  # the assessor said nothing about this one
        outcome = await ai_search._jev_shadow_assessment(
            _shadow_settings(),
            cast("Redis", FakeRedis()),
            locale="zh-TW",
            context={},
            by_id=by_id,
            scores=scores,
        )

    assert outcome is not None
    assert [row["candidate_id"] for row in outcome["rows"]] == ["c0"]


@pytest.mark.asyncio
async def test_the_inputs_the_run_still_needs_are_left_untouched(monkeypatch) -> None:
    """The run reads these after the shadow pass; the shadow pass may not edit them."""

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=_answers({"c0": 0.9, "c1": 0.1}))

    by_id, scores = _inputs()
    before = ({key: id(value) for key, value in by_id.items()}, dict(scores))

    async with _transport(handler) as client:
        monkeypatch.setattr(ai_search, "jev_client", lambda s, _c=None: real_jev_client(s, client))
        await ai_search._jev_shadow_assessment(
            _shadow_settings(),
            cast("Redis", FakeRedis()),
            locale="zh-TW",
            context={},
            by_id=by_id,
            scores=scores,
        )

    assert {key: id(value) for key, value in by_id.items()} == before[0]
    assert scores == before[1]


def test_jev_never_reaches_a_generating_provider_list() -> None:
    """The shadow pass must not have quietly made Jev selectable as a writer."""
    assert "jev" not in ai_search.AIProviderName.__args__  # type: ignore[attr-defined]
    assert "jev" not in Settings().ai_planner_priority
