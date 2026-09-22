"""The Jev client: answer parsing, the token guard, retries, and the key staying put.

Jev is the one provider whose 422 means "this module built an illegal question", so
the tests care as much about what is never retried as about what is.
"""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from app.ai.jev import (
    ChoiceQuestion,
    JevAuthError,
    JevClient,
    JevQuestion,
    JevRequestInvalid,
    JevRequestTooLarge,
    NoulAnswer,
    NoulQuestion,
    ScoreQuestion,
    estimate_tokens,
    route,
    route_answer,
)
from app.config import Settings

SECRET = "jev-test-key-that-must-never-appear-in-a-url"

ANSWERS = {
    "model": "jev-1.13.0",
    "answers": {
        "department": {
            "type": "choice",
            "choice": "technical",
            "confidence": 0.78,
            "probabilities": {"technical": 0.85, "billing": 0.15, "sales": 0.0},
        },
        "frustration": {
            "type": "score",
            "score": 1.0,
            "confidence": 1.0,
            "legend": {"0": "calm", "1": "annoyed", "2": "angry"},
            "probabilities": {"0": 0.0, "1": 1.0, "2": 0.0},
        },
        "is_urgent": {"type": "noul", "noul": 1.0},
    },
    "usage": {"input_tokens": 392, "output_tokens": 65},
}

QUESTIONS: dict[str, JevQuestion] = {
    "department": ChoiceQuestion(
        instructions="Which team should handle this",
        criteria={"billing": "payments", "technical": "bugs", "sales": "pricing"},
    ),
    "frustration": ScoreQuestion(
        instructions="How frustrated the customer appears",
        criteria=["calm", "annoyed", "angry"],
    ),
    "is_urgent": NoulQuestion(instructions="The message conveys urgency"),
}


def _client(
    responses: list[httpx.Response],
) -> tuple[JevClient, list[httpx.Request]]:
    seen: list[httpx.Request] = []
    queue = list(responses)

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return queue.pop(0)

    transport = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return (
        JevClient(
            SECRET,
            "https://api.typesafe.ai/v1",
            "jev-1.13.0",
            10.0,
            client=transport,
        ),
        seen,
    )


@pytest.mark.asyncio
async def test_one_call_carries_every_question_and_parses_all_three_types() -> None:
    client, seen = _client([httpx.Response(200, json=ANSWERS)])
    answers, usage = await client.ask("a support ticket", QUESTIONS)

    assert len(seen) == 1, "batching the questions is what keeps us under the rate limit"
    body = seen[0].read().decode()
    assert '"model":"jev-1.13.0"' in body
    assert answers["department"].choice == "technical"  # type: ignore[union-attr]
    assert answers["frustration"].legend["1"] == "annoyed"  # type: ignore[union-attr]
    assert answers["is_urgent"] == NoulAnswer(type="noul", noul=1.0)
    assert not hasattr(answers["is_urgent"], "confidence"), "a noul answer has no confidence"
    assert usage == {"input_tokens": 392, "output_tokens": 65}


@pytest.mark.asyncio
async def test_the_key_rides_in_the_header_and_never_in_the_url() -> None:
    client, seen = _client([httpx.Response(200, json=ANSWERS)])
    await client.ask("a support ticket", QUESTIONS)

    request = seen[0]
    assert request.headers["Authorization"] == f"Bearer {SECRET}"
    assert SECRET not in str(request.url)
    assert request.url.query == b""
    assert str(request.url) == "https://api.typesafe.ai/v1/systemone"


def test_the_module_never_builds_a_query_string() -> None:
    """The 2026-09-19 leak was a key in a logged URL; this path cannot grow one."""
    source = Path(__file__).resolve().parents[1] / "app" / "ai" / "jev.py"
    assert "params=" not in source.read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_a_rejected_key_is_not_retried() -> None:
    client, seen = _client([httpx.Response(401, json={"message": "bad key"})])
    with pytest.raises(JevAuthError):
        await client.ask("state", {"ok": NoulQuestion(instructions="true")})
    assert len(seen) == 1, "a wrong key is still wrong on the second try"


@pytest.mark.asyncio
async def test_a_denied_key_is_not_retried_either() -> None:
    """403 is a real key without access to this model; asking twice does not help."""
    client, seen = _client([httpx.Response(403, json={"message": "no access"})])
    with pytest.raises(JevAuthError):
        await client.ask("state", {"ok": NoulQuestion(instructions="true")})
    assert len(seen) == 1


@pytest.mark.asyncio
async def test_a_400_is_read_the_same_way_as_a_422() -> None:
    client, seen = _client([httpx.Response(400, json={"message": "malformed question"})])
    with pytest.raises(JevRequestInvalid, match="malformed question"):
        await client.ask("state", {"ok": NoulQuestion(instructions="true")})
    assert len(seen) == 1


@pytest.mark.asyncio
async def test_a_422_is_our_bug_and_is_not_retried() -> None:
    client, seen = _client([httpx.Response(422, json={"message": "criteria is required"})])
    with pytest.raises(JevRequestInvalid, match="criteria is required"):
        await client.ask("state", {"ok": NoulQuestion(instructions="true")})
    assert len(seen) == 1


@pytest.mark.asyncio
async def test_a_429_backs_off_and_then_succeeds() -> None:
    client, seen = _client(
        [
            httpx.Response(429, headers={"Retry-After": "0"}),
            httpx.Response(200, json=ANSWERS),
        ]
    )
    answers, _ = await client.ask("a support ticket", QUESTIONS)
    assert len(seen) == 2
    assert answers["department"].choice == "technical"  # type: ignore[union-attr]


@pytest.mark.asyncio
async def test_an_overloaded_service_is_retried_then_raises() -> None:
    client, seen = _client([httpx.Response(529, headers={"Retry-After": "0"})] * 4)
    with pytest.raises(httpx.HTTPStatusError):
        await client.ask("state", {"ok": NoulQuestion(instructions="true")})
    assert len(seen) == 4, "three retries, then the failure is real"


@pytest.mark.asyncio
async def test_an_illegal_question_never_reaches_the_vendor() -> None:
    client, seen = _client([])
    with pytest.raises(JevRequestInvalid, match="2-10 ordered levels"):
        await client.ask("state", {"bad": ScoreQuestion(instructions="x", criteria=["only one"])})
    with pytest.raises(JevRequestInvalid, match="1-255 options"):
        await client.ask(
            "state",
            {"bad": ChoiceQuestion(instructions="x", criteria={str(n): "o" for n in range(256)})},
        )
    assert seen == [], "the vendor should never be billed for a request we know is illegal"


@pytest.mark.asyncio
async def test_an_oversized_batch_is_refused_before_it_is_sent() -> None:
    client, seen = _client([])
    client.max_state_tokens = 100
    with pytest.raises(JevRequestTooLarge, match="split the batch"):
        await client.ask("汁" * 500, {"ok": NoulQuestion(instructions="true")})
    assert seen == []


@pytest.mark.asyncio
async def test_a_noul_without_criteria_does_not_send_a_null() -> None:
    """criteria is optional on a noul; absent is not the same as null to a validator."""
    client, seen = _client([httpx.Response(200, json=ANSWERS)])
    await client.ask("a support ticket", QUESTIONS)
    body = seen[0].read().decode()
    assert '"is_urgent":{"type":"noul","instructions":"The message conveys urgency"}' in body
    assert "null" not in body


@pytest.mark.asyncio
async def test_a_noul_may_still_clarify_what_yes_and_no_cover() -> None:
    client, seen = _client([httpx.Response(200, json=ANSWERS)])
    await client.ask(
        "a support ticket",
        {
            **QUESTIONS,
            "is_urgent": NoulQuestion(
                instructions="The message conveys urgency",
                criteria={"true": "needs an answer today", "false": "can wait a week"},
            ),
        },
    )
    assert '"needs an answer today"' in seen[0].read().decode()


def test_cjk_is_estimated_at_least_as_heavily_as_latin() -> None:
    """The estimate is pessimistic on purpose: this product's state is usually CJK."""
    assert estimate_tokens("東京車站") >= 4
    assert estimate_tokens("東京車站") > estimate_tokens("tokyo station")


def test_routing_downgrades_a_confident_non_english_answer_until_it_is_validated() -> None:
    confident = NoulAnswer(type="noul", noul=0.97)
    assert route(confident, act_at=0.9, flag_at=0.5, locale="en") == "act"
    assert route(confident, act_at=0.9, flag_at=0.5, locale="zh-TW") == "confirm"
    assert (
        route(confident, act_at=0.9, flag_at=0.5, locale="zh-TW", cjk_autopilot=True) == "act"
    )


def test_routing_reads_the_probability_a_noul_answer_actually_carries() -> None:
    assert route(NoulAnswer(type="noul", noul=0.2), act_at=0.9, flag_at=0.5) == "hold"
    assert route(NoulAnswer(type="noul", noul=0.6), act_at=0.9, flag_at=0.5) == "confirm"


def test_the_settings_bound_router_keeps_the_non_english_guard_shut() -> None:
    """A call site cannot opt out of the downgrade by passing its own numbers."""
    settings = Settings()
    assert settings.jev_cjk_autopilot_enabled is False
    confident = NoulAnswer(type="noul", noul=0.99)
    assert route_answer(confident, settings, locale="en") == "act"
    assert route_answer(confident, settings, locale="zh-TW") == "confirm"
    assert route_answer(confident, settings, locale="ja") == "confirm"
