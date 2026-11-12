"""Who is using which Colab account right now, so parallel agents never share one.

Each Colab account (slots A–E on /admin/ai-accounts) can carry one lease: a holder name the
agent chose (``claude-zt-e033``, ``codex-story-7``), the video tool token that took it, and an
expiry. A lease is how two agents working at the same time each get an account of their own:
`POST /api/video/colab-accounts/{slot|auto}/lease` takes one, the credentials route refuses an
account another holder leased, and the lease runs out by itself if the agent forgets to give
it back. It lives in Redis only: nothing about it outlasts its expiry.

Every change is a WATCH/MULTI transaction on the slot's key, so two agents asking for the same
account at the same moment get one lease and one refusal, never two leases.
"""

import json
import time
from collections.abc import Mapping
from typing import Any

from redis.asyncio import Redis
from redis.exceptions import RedisError, WatchError

from app.admin_ai_accounts.schemas import (
    SLOTS,
    AiAccountSlot,
    ColabAccounts,
    ColabAccountView,
    ColabLease,
    Slot,
    Tool,
)
from app.infra import get_redis
from app.problems import AppError

KEY_PREFIX = "colab-lease:"
ATTEMPTS = 5


def _key(slot: Slot) -> str:
    return f"{KEY_PREFIX}{slot}"


def _unavailable() -> AppError:
    return AppError(503, "colab_lease_unavailable", "Colab 帳號租用服務暫時無法使用")


def _parse(slot: Slot, raw: bytes | str | None, now: int) -> ColabLease | None:
    if not raw:
        return None
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", "replace")
    try:
        data: dict[str, Any] = json.loads(raw)
        lease = ColabLease.model_validate({**data, "slot": slot})
    except ValueError:
        # Something else wrote the key: it holds no account.
        return None
    return lease if lease.expires_at > now else None


def leased_by_other(slot: Slot, lease: ColabLease, holder: str | None) -> AppError:
    left = max(1, (lease.expires_at - int(time.time()) + 59) // 60)
    asker = "" if holder is None else f"（你是「{holder}」）"
    return AppError(
        409,
        "colab_account_leased",
        f"Colab 帳號 {slot.upper()} 正由「{lease.holder}」使用（權杖 {lease.token}）{asker}，"
        f"約 {left} 分鐘後到期；換一個帳號，或等它 release",
    )


async def current(slot: Slot, *, redis: Redis | None = None) -> ColabLease | None:
    client = redis or get_redis()
    try:
        raw = await client.get(_key(slot))
    except RedisError as exc:
        raise _unavailable() from exc
    return _parse(slot, raw, int(time.time()))


async def all_leases(*, redis: Redis | None = None) -> dict[Slot, ColabLease]:
    client = redis or get_redis()
    try:
        values = await client.mget([_key(slot) for slot in SLOTS])
    except RedisError as exc:
        raise _unavailable() from exc
    now = int(time.time())
    found: dict[Slot, ColabLease] = {}
    for slot, raw in zip(SLOTS, values, strict=True):
        lease = _parse(slot, raw, now)
        if lease is not None:
            found[slot] = lease
    return found


async def acquire(
    slot: Slot,
    holder: str,
    token_prefix: str,
    ttl_seconds: int,
    *,
    redis: Redis | None = None,
) -> tuple[ColabLease, bool]:
    """Lease ``slot`` to ``holder``, or renew the lease it already holds.

    Returns the lease and whether it is new (False: a renewal). Another holder's live lease
    is a 409 ``colab_account_leased``.
    """
    client = redis or get_redis()
    key = _key(slot)
    try:
        for _ in range(ATTEMPTS):
            async with client.pipeline(transaction=True) as pipe:
                try:
                    await pipe.watch(key)
                    now = int(time.time())
                    existing = _parse(slot, await pipe.get(key), now)
                    if existing is not None and existing.holder != holder:
                        raise leased_by_other(slot, existing, holder)
                    lease = ColabLease(
                        slot=slot,
                        holder=holder,
                        token=token_prefix,
                        acquired_at=existing.acquired_at if existing else now,
                        expires_at=now + ttl_seconds,
                    )
                    pipe.multi()  # type: ignore[no-untyped-call]
                    pipe.set(key, lease.model_dump_json(exclude={"slot"}), ex=ttl_seconds)
                    await pipe.execute()
                    return lease, existing is None
                except WatchError:
                    continue
    except RedisError as exc:
        raise _unavailable() from exc
    raise AppError(409, "colab_lease_contended", "同時有其他 agent 在搶這個帳號，請稍後再試")


async def release(slot: Slot, holder: str, *, redis: Redis | None = None) -> bool:
    """Give the lease back. Only its holder can; anything else is a no-op that says False."""
    client = redis or get_redis()
    key = _key(slot)
    try:
        for _ in range(ATTEMPTS):
            async with client.pipeline(transaction=True) as pipe:
                try:
                    await pipe.watch(key)
                    existing = _parse(slot, await pipe.get(key), int(time.time()))
                    if existing is None:
                        return False
                    if existing.holder != holder:
                        raise leased_by_other(slot, existing, holder)
                    pipe.multi()  # type: ignore[no-untyped-call]
                    pipe.delete(key)
                    await pipe.execute()
                    return True
                except WatchError:
                    continue
    except RedisError as exc:
        raise _unavailable() from exc
    raise AppError(409, "colab_lease_contended", "同時有其他 agent 在搶這個帳號，請稍後再試")


def accounts_view(
    slots: list[AiAccountSlot],
    defaults: Mapping[Tool, Slot],
    leases: dict[Slot, ColabLease],
) -> ColabAccounts:
    """What an agent sees when it picks an account: never an email, never a credential."""
    views = [
        ColabAccountView(
            slot=item.slot,
            is_default=item.is_default,
            signed_in=bool(item.logged_in),
            compute_units=item.usage.compute_units if item.usage else None,
            usage_error=item.usage_error,
            checked_at=item.checked_at,
            lease=leases.get(item.slot),
        )
        for item in slots
        if item.tool == "colab"
    ]
    views.sort(key=lambda view: view.slot)
    return ColabAccounts(accounts=views, default=defaults.get("colab"))


def pick_order(accounts: ColabAccounts, holder: str, min_balance: float | None) -> list[Slot]:
    """The accounts `auto` tries, best first.

    The one this holder already leases comes first (asking again renews it, an agent never
    holds two). Then the signed-in, unleased accounts with the most compute units left; an
    account whose balance is unknown goes last, and one under ``min_balance`` not at all.
    """
    own = [view.slot for view in accounts.accounts if view.lease and view.lease.holder == holder]
    if own:
        return own[:1]
    free: list[tuple[float, Slot]] = []
    for view in accounts.accounts:
        if not view.signed_in or view.lease is not None:
            continue
        balance = view.compute_units.balance if view.compute_units else None
        if balance is not None and min_balance is not None and balance < min_balance:
            continue
        free.append((balance if balance is not None else -1.0, view.slot))
    free.sort(key=lambda pair: (-pair[0], pair[1]))
    return [slot for _, slot in free]
