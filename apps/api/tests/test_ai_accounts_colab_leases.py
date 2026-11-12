"""Colab account leases: several agents, one account each (admin_ai_accounts.colab_leases)."""

import asyncio
import json
import time
from typing import Any

import pytest

import app.admin_ai_accounts.colab_leases as leases_module
from app.main import app
from app.video_speech.admin_api import video_tool
from tests.test_ai_accounts_admin import _client, _token, ai_app, slot

__all__ = ["ai_app"]

ACCOUNTS = "/api/v1/video/colab-accounts"
CREDENTIALS = "/api/v1/video/colab-credentials"
TOKEN_FILE = {"token": "ya29.x", "refresh_token": "1//r", "client_id": "c", "client_secret": "s"}


def colab(letter: str, balance: float | None, *, signed_in: bool = True) -> dict[str, Any]:
    usage = (
        {"source": "live", "windows": [], "compute_units": {"balance": balance}}
        if balance is not None
        else None
    )
    return slot("colab", letter, logged_in=signed_in, auth_method="google", usage=usage)


@pytest.fixture
def leases(ai_app: dict[str, Any]) -> dict[str, Any]:
    # ai_app already points the lease module at a fake Redis (ai_app["redis"]).
    ai_app["agent"].routes[("GET", "/v1/accounts")] = (
        200,
        {
            "slots": [
                slot("claude", "a", logged_in=True),
                colab("a", 120.0),
                colab("b", 410.5),
                colab("c", 35.0),
                colab("d", None, signed_in=False),
            ],
            "defaults": {"claude": "a", "codex": "a", "agy": "a", "colab": "a"},
            "allowlist_configured": True,
        },
    )
    app.dependency_overrides[video_tool] = lambda: _token(colab_access=True)
    return ai_app


@pytest.mark.asyncio
async def test_agents_see_every_colab_account_with_balance_and_holder_but_no_email(
    leases: dict[str, Any],
) -> None:
    async with _client() as client:
        taken = await client.post(f"{ACCOUNTS}/b/lease", json={"holder": "claude-zt-e033"})
        assert taken.status_code == 200
        listed = await client.get(ACCOUNTS)
    assert listed.status_code == 200
    assert listed.headers["cache-control"] == "no-store"
    body = listed.json()
    assert body["default"] == "a"
    assert [item["slot"] for item in body["accounts"]] == ["a", "b", "c", "d"]
    by_slot = {item["slot"]: item for item in body["accounts"]}
    assert by_slot["b"]["compute_units"]["balance"] == 410.5
    assert by_slot["b"]["lease"]["holder"] == "claude-zt-e033"
    assert by_slot["b"]["lease"]["token"] == "mkv_abcdef"
    assert by_slot["a"]["lease"] is None
    assert by_slot["d"]["signed_in"] is False
    assert "email" not in json.dumps(body)


@pytest.mark.asyncio
async def test_a_second_agent_cannot_lease_or_fetch_an_account_another_holds(
    leases: dict[str, Any],
) -> None:
    agent = leases["agent"]
    agent.routes[("GET", "/v1/accounts/colab/b/credentials")] = (
        200,
        {"tool": "colab", "slot": "b", "credentials": TOKEN_FILE},
    )
    async with _client() as client:
        first = await client.post(f"{ACCOUNTS}/b/lease", json={"holder": "agent-one"})
        assert first.status_code == 200
        second = await client.post(f"{ACCOUNTS}/b/lease", json={"holder": "agent-two"})
        assert (second.status_code, second.json()["code"]) == (409, "colab_account_leased")
        assert "agent-one" in second.json()["detail"]
        # The holder gets the credentials; anyone else, named or not, is refused.
        own = await client.get(CREDENTIALS, params={"slot": "b", "holder": "agent-one"})
        assert own.status_code == 200
        assert own.json()["credentials"] == TOKEN_FILE
        other = await client.get(CREDENTIALS, params={"slot": "b", "holder": "agent-two"})
        assert (other.status_code, other.json()["code"]) == (409, "colab_account_leased")
        anonymous = await client.get(CREDENTIALS, params={"slot": "b"})
        assert anonymous.status_code == 409
        assert "1//r" not in anonymous.text
    rows = leases["session"].audits()
    assert [(row.action, row.target) for row in rows] == [
        ("ai_account.colab_leased", "ai-account:colab-b"),
        ("ai_account.colab_credentials_fetched", "ai-account:colab-b"),
    ]
    assert rows[1].metadata_json["holder"] == "agent-one"


@pytest.mark.asyncio
async def test_auto_takes_the_free_account_with_most_units_and_renews_its_own(
    leases: dict[str, Any],
) -> None:
    async with _client() as client:
        one = await client.post(f"{ACCOUNTS}/auto/lease", json={"holder": "agent-one"})
        two = await client.post(f"{ACCOUNTS}/auto/lease", json={"holder": "agent-two"})
        # Asking again renews the lease it has instead of taking a second account.
        again = await client.post(
            f"{ACCOUNTS}/auto/lease", json={"holder": "agent-one", "ttl_minutes": 600}
        )
        # c has 35 units left: under the floor, so a third agent finds nothing.
        three = await client.post(
            f"{ACCOUNTS}/auto/lease", json={"holder": "agent-three", "min_balance": 50}
        )
        four = await client.post(f"{ACCOUNTS}/auto/lease", json={"holder": "agent-four"})
        # The unsigned slot is never leased by name either.
        empty = await client.post(f"{ACCOUNTS}/d/lease", json={"holder": "agent-five"})
    assert one.json()["slot"] == "b"
    assert two.json()["slot"] == "a"
    assert again.json()["slot"] == "b"
    assert again.json()["acquired_at"] == one.json()["acquired_at"]
    assert again.json()["expires_at"] - int(time.time()) > 590 * 60
    assert (three.status_code, three.json()["code"]) == (409, "colab_no_free_account")
    assert "B=agent-one" in three.json()["detail"]
    assert four.json()["slot"] == "c"
    assert (empty.status_code, empty.json()["code"]) == (409, "colab_not_signed_in")
    actions = [row.action for row in leases["session"].audits()]
    assert actions == [
        "ai_account.colab_leased",
        "ai_account.colab_leased",
        "ai_account.colab_lease_renewed",
        "ai_account.colab_leased",
    ]


@pytest.mark.asyncio
async def test_only_the_holder_releases_and_an_expired_lease_frees_the_account(
    leases: dict[str, Any],
) -> None:
    redis = leases["redis"]
    async with _client() as client:
        await client.post(f"{ACCOUNTS}/a/lease", json={"holder": "agent-one"})
        stolen = await client.post(f"{ACCOUNTS}/a/lease/release", json={"holder": "agent-two"})
        assert (stolen.status_code, stolen.json()["code"]) == (409, "colab_account_leased")
        released = await client.post(f"{ACCOUNTS}/a/lease/release", json={"holder": "agent-one"})
        assert released.json() == {"slot": "a", "released": True}
        twice = await client.post(f"{ACCOUNTS}/a/lease/release", json={"holder": "agent-one"})
        assert twice.json() == {"slot": "a", "released": False}
        # A lease whose time is up holds nothing, even before Redis drops the key.
        stale = {"holder": "gone", "token": "mkv_old", "acquired_at": 1, "expires_at": 2}
        await redis.set("colab-lease:c", json.dumps(stale))
        taken = await client.post(f"{ACCOUNTS}/c/lease", json={"holder": "agent-two"})
        assert taken.json()["holder"] == "agent-two"
    assert await redis.ttl("colab-lease:c") > 0


@pytest.mark.asyncio
async def test_two_agents_racing_for_one_account_get_one_lease(leases: dict[str, Any]) -> None:
    redis = leases["redis"]
    results = await asyncio.gather(
        *(leases_module.acquire("e", f"agent-{n}", "mkv_x", 600, redis=redis) for n in range(6)),
        return_exceptions=True,
    )
    won = [item for item in results if not isinstance(item, BaseException)]
    lost = [item for item in results if isinstance(item, BaseException)]
    assert len(won) == 1
    assert all(getattr(item, "code", None) == "colab_account_leased" for item in lost)


@pytest.mark.asyncio
async def test_lease_routes_need_colab_access_and_a_clean_holder(
    leases: dict[str, Any],
) -> None:
    async with _client() as client:
        spaced = await client.post(f"{ACCOUNTS}/a/lease", json={"holder": "two words"})
        assert spaced.status_code == 422
        quoted = await client.get(CREDENTIALS, params={"holder": "x'; rm"})
        assert quoted.status_code == 422
        unknown = await client.post(f"{ACCOUNTS}/z/lease", json={"holder": "agent-one"})
        assert unknown.status_code == 422
        app.dependency_overrides[video_tool] = lambda: _token(colab_access=False)
        for response in (
            await client.get(ACCOUNTS),
            await client.post(f"{ACCOUNTS}/a/lease", json={"holder": "agent-one"}),
            await client.post(f"{ACCOUNTS}/a/lease/release", json={"holder": "agent-one"}),
        ):
            assert (response.status_code, response.json()["code"]) == (
                403,
                "video_tool_token_no_colab",
            )
    assert await leases["redis"].keys("colab-lease:*") == []
