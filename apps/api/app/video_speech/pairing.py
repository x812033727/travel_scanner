"""Pairing the local video tool with this server by an admin's click, not a pasted token.

The device authorization flow of RFC 8628, cut down to what one site owner needs. The local
tool asks for a pairing and shows a short code; the owner opens the admin card, compares the
code and allows it; the tool, polling with a device code only it holds, then collects a new
video tool token exactly once. Nobody copies the token, and it never appears on a screen or
in a chat with an assistant.

Records live in Redis for ten minutes and nowhere else. The token itself is minted when the
tool collects it, so no plaintext token is ever stored, and ``GETDEL`` on the grant makes a
second collection impossible even when two polls race.
"""

from __future__ import annotations

import hashlib
import json
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Literal
from uuid import UUID

from redis.asyncio import Redis

# No vowels, so a code never spells a word, and no digits, so nothing reads as 0/O or 1/I.
USER_CODE_ALPHABET = "BCDFGHJKLMNPQRSTVWXZ"
USER_CODE_LENGTH = 8
PAIRING_TTL_SECONDS = 600
POLL_INTERVAL_SECONDS = 5

PairingStatus = Literal["pending", "approved", "denied"]
PollStatus = Literal["pending", "approved", "denied", "expired"]


@dataclass(frozen=True)
class Pairing:
    user_code: str
    client_name: str
    client_ip: str
    created_at: datetime
    expires_at: datetime
    status: PairingStatus
    device_hash: str

    def as_record(self) -> dict[str, Any]:
        return {
            "client_name": self.client_name,
            "client_ip": self.client_ip,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "status": self.status,
            "device_hash": self.device_hash,
        }


@dataclass(frozen=True)
class Grant:
    """What an approval hands to the collecting poll: who allowed it, for which machine."""

    approved_by: UUID
    client_name: str


def new_device_code() -> str:
    return secrets.token_urlsafe(32)


def device_hash(device_code: str) -> str:
    return hashlib.sha256(device_code.encode("utf-8")).hexdigest()


def new_user_code() -> str:
    return "".join(secrets.choice(USER_CODE_ALPHABET) for _ in range(USER_CODE_LENGTH))


def normalize_user_code(raw: str) -> str | None:
    """The code as stored, from whatever the owner typed: case, spaces and dashes ignored."""
    code = "".join(raw.split()).replace("-", "").upper()
    if len(code) != USER_CODE_LENGTH or any(ch not in USER_CODE_ALPHABET for ch in code):
        return None
    return code


def display_code(code: str) -> str:
    return f"{code[:4]}-{code[4:]}"


def _text(value: bytes | str | None) -> str | None:
    # The app's client decodes replies; the stubs cannot know that.
    return value.decode("utf-8") if isinstance(value, bytes) else value


def _code_key(code: str) -> str:
    return f"video:pairing:code:{code}"


def _device_key(digest: str) -> str:
    return f"video:pairing:device:{digest}"


def _grant_key(digest: str) -> str:
    return f"video:pairing:grant:{digest}"


def _pairing(code: str, raw: str) -> Pairing:
    record = json.loads(raw)
    return Pairing(
        user_code=code,
        client_name=str(record["client_name"]),
        client_ip=str(record["client_ip"]),
        created_at=datetime.fromisoformat(record["created_at"]),
        expires_at=datetime.fromisoformat(record["expires_at"]),
        status=record["status"],
        device_hash=str(record["device_hash"]),
    )


async def start_pairing(
    redis: Redis, *, client_name: str, client_ip: str, now: datetime | None = None
) -> tuple[str, Pairing]:
    """Open a pairing; return the device code (for the tool only) and the pairing record."""
    moment = now or datetime.now(UTC)
    device_code = new_device_code()
    digest = device_hash(device_code)
    for _ in range(5):
        code = new_user_code()
        pairing = Pairing(
            user_code=code,
            client_name=client_name,
            client_ip=client_ip,
            created_at=moment,
            expires_at=moment + timedelta(seconds=PAIRING_TTL_SECONDS),
            status="pending",
            device_hash=digest,
        )
        stored = await redis.set(
            _code_key(code), json.dumps(pairing.as_record()), nx=True, ex=PAIRING_TTL_SECONDS
        )
        if stored:
            await redis.set(_device_key(digest), code, ex=PAIRING_TTL_SECONDS)
            return device_code, pairing
    # 20^8 codes and a handful alive at once: five collisions in a row means something is wrong.
    raise RuntimeError("could not allocate a pairing code")


async def find_pairing(redis: Redis, code: str) -> Pairing | None:
    raw = _text(await redis.get(_code_key(code)))
    return _pairing(code, raw) if raw else None


async def decide(redis: Redis, pairing: Pairing, *, approve: bool, actor_id: UUID) -> Pairing:
    """Record the owner's answer for the rest of the pairing's life.

    The grant is written before the status, so a poll between the two writes still sees
    "pending" and simply tries again, never an approval without a grant.
    """
    ttl = await redis.ttl(_code_key(pairing.user_code))
    if ttl <= 0:
        raise LookupError(pairing.user_code)
    decided = Pairing(
        user_code=pairing.user_code,
        client_name=pairing.client_name,
        client_ip=pairing.client_ip,
        created_at=pairing.created_at,
        expires_at=pairing.expires_at,
        status="approved" if approve else "denied",
        device_hash=pairing.device_hash,
    )
    if approve:
        grant = {"approved_by": str(actor_id), "client_name": pairing.client_name}
        await redis.set(_grant_key(pairing.device_hash), json.dumps(grant), ex=ttl)
    await redis.set(_code_key(pairing.user_code), json.dumps(decided.as_record()), ex=ttl)
    return decided


async def collect(redis: Redis, device_code: str) -> tuple[PollStatus, Grant | None]:
    """What the polling tool gets: an answer, and on approval the grant, handed out once."""
    digest = device_hash(device_code)
    code = _text(await redis.get(_device_key(digest)))
    if code is None:
        return "expired", None
    raw_grant = _text(await redis.getdel(_grant_key(digest)))
    if raw_grant:
        await redis.delete(_code_key(code), _device_key(digest))
        grant = json.loads(raw_grant)
        return "approved", Grant(
            approved_by=UUID(grant["approved_by"]), client_name=str(grant["client_name"])
        )
    pairing = await find_pairing(redis, code)
    if pairing is None:
        return "expired", None
    if pairing.status == "denied":
        await redis.delete(_code_key(code), _device_key(digest))
        return "denied", None
    # "approved" without a grant means a racing poll collected it a moment ago and is about to
    # delete the record; this poll gets nothing, and its next one sees "expired".
    return "pending", None
