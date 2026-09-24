"""Pairing the local video tool by an admin's click: codes, the Redis flow and the endpoints."""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient

import app.video_speech.admin_api as admin_api
from app.auth.service import current_user
from app.db import get_session
from app.main import app
from app.models import AdminAuditLog, User, VideoToolToken
from app.video_speech.pairing import (
    PAIRING_TTL_SECONDS,
    USER_CODE_ALPHABET,
    collect,
    decide,
    display_code,
    find_pairing,
    new_user_code,
    normalize_user_code,
    start_pairing,
)
from app.video_speech.tokens import token_hash

NOW = datetime(2026, 9, 24, 5, 0, tzinfo=UTC)


def test_user_codes_have_no_vowels_or_digits_and_forgive_typing() -> None:
    code = new_user_code()
    assert len(code) == 8 and all(ch in USER_CODE_ALPHABET for ch in code)
    assert not set("AEIOU0123456789") & set(USER_CODE_ALPHABET)
    assert display_code("KQMXBCDF") == "KQMX-BCDF"
    assert normalize_user_code(" kqmx-bcdf ") == "KQMXBCDF"
    assert normalize_user_code("KQMX BCDF") == "KQMXBCDF"
    for bad in ("KQMX-BCD", "KQMX-BCDA", "KQMX-BCD1", ""):
        assert normalize_user_code(bad) is None


@pytest.mark.asyncio
async def test_an_approval_is_collected_exactly_once() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    device_code, pairing = await start_pairing(
        redis, client_name="筆電", client_ip="203.0.113.9", now=NOW
    )
    assert pairing.status == "pending" and pairing.client_ip == "203.0.113.9"
    assert (await redis.ttl(f"video:pairing:code:{pairing.user_code}")) <= PAIRING_TTL_SECONDS
    assert await collect(redis, device_code) == ("pending", None)

    actor = uuid4()
    decided = await decide(redis, pairing, approve=True, actor_id=actor)
    assert decided.status == "approved"
    status, grant = await collect(redis, device_code)
    assert status == "approved" and grant is not None
    assert grant.approved_by == actor and grant.client_name == "筆電"
    # Handed out once: the next poll finds nothing, and the code no longer resolves.
    assert await collect(redis, device_code) == ("expired", None)
    assert await find_pairing(redis, pairing.user_code) is None


@pytest.mark.asyncio
async def test_a_denial_is_reported_once_and_nothing_is_granted() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    device_code, pairing = await start_pairing(redis, client_name="x", client_ip="203.0.113.9")
    await decide(redis, pairing, approve=False, actor_id=uuid4())
    assert await collect(redis, device_code) == ("denied", None)
    assert await collect(redis, device_code) == ("expired", None)


@pytest.mark.asyncio
async def test_an_unknown_or_expired_device_code_gets_nothing() -> None:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    assert await collect(redis, "x" * 43) == ("expired", None)
    device_code, pairing = await start_pairing(redis, client_name="x", client_ip="203.0.113.9")
    await redis.delete(f"video:pairing:code:{pairing.user_code}")
    assert await collect(redis, device_code) == ("expired", None)
    with pytest.raises(LookupError):
        await decide(redis, pairing, approve=True, actor_id=uuid4())


class TokenSession:
    """Just enough of AsyncSession for the pairing endpoints."""

    def __init__(self, active: int = 0) -> None:
        self.active = active
        self.added: list[Any] = []
        self.commits = 0

    async def scalar(self, statement: Any) -> Any:
        return self.active

    def add(self, row: Any) -> None:
        self.added.append(row)

    async def commit(self) -> None:
        self.commits += 1


@pytest.fixture
def pairing_app(monkeypatch: pytest.MonkeyPatch) -> Any:
    redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    state: dict[str, Any] = {"redis": redis, "limits": [], "session": TokenSession()}

    async def count_limit(namespace: str, identifier: str, **_: Any) -> None:
        state["limits"].append((namespace, identifier))

    monkeypatch.setattr(admin_api, "get_redis", lambda: redis)
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", count_limit)
    previous = app.dependency_overrides.copy()
    state["actor"] = User(id=uuid4(), email="owner@example.com", is_admin=True)
    app.dependency_overrides[current_user] = lambda: state["actor"]
    app.dependency_overrides[get_session] = lambda: state["session"]
    yield state
    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous)


PAIRINGS = "/api/v1/video/pairings"
ADMIN = "/api/v1/admin/provider-settings/azure_speech/video-tool-tokens/pairings"


def _client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_the_whole_pairing_ends_with_one_token_minted_for_the_approver(
    pairing_app: Any,
) -> None:
    async with _client() as client:
        started = await client.post(PAIRINGS, json={"client_name": "工作室筆電"})
        assert started.status_code == 201
        body = started.json()
        code = body["user_code"]
        assert len(code) == 9 and code[4] == "-"
        assert body["verification_path"].endswith(f"video_pairing={code.replace('-', '')}")
        assert body["verification_path"].startswith("/zh-TW/admin/settings?provider=azure_speech")
        assert body["interval"] == 5 and body["expires_in"] == PAIRING_TTL_SECONDS
        device_code = body["device_code"]

        pending = await client.post(f"{PAIRINGS}/poll", json={"device_code": device_code})
        assert pending.json() == {
            "status": "pending",
            "interval": 5,
            "token": None,
            "token_name": None,
        }
        assert pending.headers["cache-control"] == "no-store"

        seen = await client.get(f"{ADMIN}/{code.lower()}")
        assert seen.status_code == 200
        assert seen.json()["client_name"] == "工作室筆電" and seen.json()["status"] == "pending"
        assert device_code not in seen.text

        allowed = await client.post(f"{ADMIN}/{code}/approve")
        assert allowed.status_code == 200 and allowed.json()["status"] == "approved"
        again = await client.post(f"{ADMIN}/{code}/deny")
        assert again.status_code == 409 and again.json()["code"] == "video_pairing_already_decided"

        collected = await client.post(f"{PAIRINGS}/poll", json={"device_code": device_code})
        result = collected.json()
        assert result["status"] == "approved" and result["token"].startswith("mkv_")
        assert result["token_name"] == "配對：工作室筆電"
        after = await client.post(f"{PAIRINGS}/poll", json={"device_code": device_code})
        assert after.json()["status"] == "expired" and after.json()["token"] is None

    session = pairing_app["session"]
    row = next(item for item in session.added if isinstance(item, VideoToolToken))
    assert row.token_hash == token_hash(result["token"])
    assert row.created_by_user_id == pairing_app["actor"].id
    actions = [item.action for item in session.added if isinstance(item, AdminAuditLog)]
    assert actions == ["video_tool_pairing_approved", "video_tool_token_created"]
    assert all(
        result["token"] not in str(item.metadata_json)
        for item in session.added
        if isinstance(item, AdminAuditLog)
    )
    namespaces = [namespace for namespace, _ in pairing_app["limits"]]
    assert namespaces[0] == "video_pairing_start" and "video_pairing_poll" in namespaces


@pytest.mark.asyncio
async def test_a_denied_pairing_never_mints_a_token(pairing_app: Any) -> None:
    async with _client() as client:
        body = (await client.post(PAIRINGS, json={})).json()
        denied = await client.post(f"{ADMIN}/{body['user_code']}/deny")
        assert denied.json()["status"] == "denied"
        polled = await client.post(f"{PAIRINGS}/poll", json={"device_code": body["device_code"]})
    assert polled.json()["status"] == "denied"
    session = pairing_app["session"]
    assert not any(isinstance(item, VideoToolToken) for item in session.added)
    assert [item.action for item in session.added] == ["video_tool_pairing_denied"]


@pytest.mark.asyncio
async def test_unknown_codes_are_404_and_a_full_token_list_refuses_approval(
    pairing_app: Any,
) -> None:
    async with _client() as client:
        missing = await client.get(f"{ADMIN}/BCDF-GHJK")
        assert missing.status_code == 404 and missing.json()["code"] == "video_pairing_not_found"
        malformed = await client.post(f"{ADMIN}/not-a-code/approve")
        assert malformed.status_code == 404

        body = (await client.post(PAIRINGS, json={"client_name": "x"})).json()
        pairing_app["session"].active = 10
        refused = await client.post(f"{ADMIN}/{body['user_code']}/approve")
        assert refused.status_code == 409 and refused.json()["code"] == "video_tool_token_limit"
        # The pairing is still waiting, so the owner can revoke an old token and try again.
        still = await client.get(f"{ADMIN}/{body['user_code']}")
        assert still.json()["status"] == "pending"


@pytest.mark.asyncio
async def test_a_poll_with_a_malformed_device_code_is_refused_by_the_schema(
    pairing_app: Any,
) -> None:
    async with _client() as client:
        response = await client.post(f"{PAIRINGS}/poll", json={"device_code": "short"})
    assert response.status_code == 422
