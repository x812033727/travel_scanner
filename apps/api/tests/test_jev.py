"""Budgeted Jev calls do not assume a provider rate limit is free."""

from __future__ import annotations

import httpx
import pytest

from app.ai.jev import JevClient, JevOutcomeUncertain, NoulQuestion


@pytest.mark.asyncio
@pytest.mark.parametrize("status", (429, 529))
async def test_budgeted_jev_refusal_stays_uncertain_after_one_wire(status: int) -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(status, json={"message": "busy"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        jev = JevClient(
            "test-key",
            "https://api.typesafe.ai/v1",
            "jev-1.13.0",
            10.0,
            retry_refusals=False,
            client=http,
        )
        with pytest.raises(JevOutcomeUncertain) as raised:
            await jev.ask("the pilot's state", {"answer": NoulQuestion(instructions="true")})

    assert len(seen) == 1
    assert jev.wires_sent == 1
    assert raised.value.status == status
    assert raised.value.phase == "response"
    assert raised.value.wires_sent == 1
    assert len(raised.value.request_sha256) == 64
