"""Administrator overrides of the web UI copy, layered over the JSON catalogs.

The catalogs in ``apps/web/messages`` are the versioned defaults; ``ui_text_overrides``
holds only the sentences an administrator changed. The web server merges the two on
every render, so the public read below is the highest-QPS internal call in the API and
is served from Redis. Every write deletes the cached payloads after its commit — the
first administrator write in this codebase that invalidates a cache, which is why the
TTL is a safety net rather than the mechanism.

The API never sees the catalogs, so placeholder parity is checked against the default
text the editor sends along, and that text is kept as ``default_snapshot``. The web
loader repeats the check against the live default at merge time, so this validation is
for the person typing, not for safety.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from collections.abc import Mapping
from typing import Any

from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas import AdminAuditView
from app.config import get_settings
from app.i18n import LOCALES, Locale
from app.models import AdminAuditLog, UiTextOverride, User
from app.problems import AppError
from app.ui_text.schemas import (
    UI_TEXT_LOCKED_NAMESPACES,
    UI_TEXT_NAMESPACES,
    PublicUiText,
    UiTextBatchWrite,
    UiTextEntryView,
    UiTextSnapshot,
    UiTextWrite,
)

logger = logging.getLogger(__name__)

# The same extraction as tools/check-i18n.mjs (/\{([A-Za-z_][\w]*)/g). Python's \w is
# Unicode-aware, so the class is spelled out to keep both sides identical.
ICU_PARAMETER_PATTERN = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)")
# Every C0/C1 control character except LF, plus the Unicode line and paragraph separators.
CONTROL_CHARACTERS = re.compile(r"[\x00-\x09\x0b-\x1f\x7f-\x9f\u2028\u2029]")
CACHE_KEY = "ui-text:overrides:{locale}"
AUDIT_ACTIONS: tuple[str, ...] = ("ui_text_updated", "ui_text_reset")
AUDIT_LIMIT = 20
AUDIT_VALUE_LIMIT = 500


def icu_parameters(message: str) -> set[str]:
    return set(ICU_PARAMETER_PATTERN.findall(message))


def braces_balanced(message: str) -> bool:
    depth = 0
    for character in message:
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def content_version(entries: Mapping[str, str]) -> str:
    serialized = json.dumps(dict(entries), sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]


def require_namespace(namespace: str) -> None:
    if namespace in UI_TEXT_LOCKED_NAMESPACES:
        raise AppError(422, "ui_text_namespace_locked", "這個文案群組不能在後台修改")
    if namespace not in UI_TEXT_NAMESPACES:
        raise AppError(422, "ui_text_namespace_unknown", "這個文案群組不存在")


def normalize_value(value: str, default_value: str | None, *, key: str) -> str:
    """Return the text to store, or raise the reason it cannot be.

    Line endings become LF and nothing else is touched: 47 catalog defaults are
    separators such as ", " whose leading or trailing space is the whole point, so the
    value is never stripped, only rejected when it is blank. Seven English defaults use
    ICU plural syntax; the placeholder regex still finds their argument name, but only
    the brace check catches a plural that lost its closing brace, which next-intl would
    otherwise turn into the raw key path on the page.
    """

    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.strip():
        raise AppError(422, "ui_text_value_empty", f"{key}：文案不能留空；要移除覆寫請用還原預設")
    if CONTROL_CHARACTERS.search(normalized):
        raise AppError(422, "ui_text_value_control_chars", f"{key}：文案含有不支援的控制字元")
    if not braces_balanced(normalized):
        raise AppError(422, "ui_text_braces_unbalanced", f"{key}：大括號沒有成對")
    if default_value is None:
        raise AppError(422, "ui_text_default_required", f"{key}：驗證覆寫需要提供預設文案")
    expected = icu_parameters(default_value)
    actual = icu_parameters(normalized)
    if actual != expected:
        missing = "、".join(sorted(expected - actual)) or "無"
        extra = "、".join(sorted(actual - expected)) or "無"
        raise AppError(
            422,
            "ui_text_parameters_mismatch",
            f"{key}：參數必須與預設相同（缺少：{missing}；多出：{extra}）",
        )
    return normalized


def _truncate(value: str | None) -> str | None:
    if value is None or len(value) <= AUDIT_VALUE_LIMIT:
        return value
    return value[:AUDIT_VALUE_LIMIT]


def _target(locale: str, namespace: str) -> str:
    # The key stays in the metadata: a 200-character key would not fit the target column.
    return f"ui-text:{locale}:{namespace}"


# Database access lives in these four functions so the unit tests can stand in for the
# table while exercising validation, caching and audit logic unchanged.


async def _public_rows(session: AsyncSession, locale: str) -> list[tuple[str, str, str]]:
    result = await session.execute(
        select(UiTextOverride.namespace, UiTextOverride.key, UiTextOverride.value)
        .where(UiTextOverride.locale == locale)
        .order_by(UiTextOverride.namespace, UiTextOverride.key)
    )
    return [(str(namespace), str(key), str(value)) for namespace, key, value in result.all()]


async def _list_overrides(
    session: AsyncSession, locale: str
) -> list[tuple[UiTextOverride, str | None]]:
    result = await session.execute(
        select(UiTextOverride, User.email)
        .outerjoin(User, User.id == UiTextOverride.updated_by_user_id)
        .where(UiTextOverride.locale == locale)
        .order_by(UiTextOverride.namespace, UiTextOverride.key)
    )
    return [(row, email) for row, email in result.all()]


async def _find_override(
    session: AsyncSession, locale: str, namespace: str, key: str
) -> UiTextOverride | None:
    row: UiTextOverride | None = await session.scalar(
        select(UiTextOverride).where(
            UiTextOverride.locale == locale,
            UiTextOverride.namespace == namespace,
            UiTextOverride.key == key,
        )
    )
    return row


async def _recent_audit(session: AsyncSession) -> list[AdminAuditLog]:
    rows = await session.scalars(
        select(AdminAuditLog)
        .where(AdminAuditLog.action.in_(list(AUDIT_ACTIONS)))
        .order_by(AdminAuditLog.created_at.desc())
        .limit(AUDIT_LIMIT)
    )
    return list(rows.all())


async def public_ui_text(session: AsyncSession, redis: Redis, locale: Locale) -> PublicUiText:
    cache_key = CACHE_KEY.format(locale=locale)
    try:
        cached = await redis.get(cache_key)
    except RedisError:
        logger.warning("ui_text_cache_read_failed", extra={"locale": locale})
        cached = None
    if cached:
        try:
            return PublicUiText.model_validate_json(cached)
        except ValueError:
            logger.warning("ui_text_cache_payload_invalid", extra={"locale": locale})
    rows = await _public_rows(session, locale)
    entries = {f"{namespace}.{key}": value for namespace, key, value in rows}
    payload = PublicUiText(locale=locale, version=content_version(entries), entries=entries)
    try:
        await redis.set(
            cache_key, payload.model_dump_json(), ex=get_settings().ui_text_cache_ttl_seconds
        )
    except RedisError:
        logger.warning("ui_text_cache_write_failed", extra={"locale": locale})
    return payload


async def invalidate_ui_text_cache(redis: Redis) -> None:
    # One command for every locale: a write to one locale cannot leave another stale
    # through a wrong-locale bug, and the TTL covers a Redis outage here.
    try:
        await redis.delete(*[CACHE_KEY.format(locale=locale) for locale in LOCALES])
    except RedisError:
        logger.warning("ui_text_cache_invalidate_failed")


def _entry_view(row: UiTextOverride, email: str | None) -> UiTextEntryView:
    return UiTextEntryView(
        namespace=row.namespace,
        key=row.key,
        locale=row.locale,
        value=row.value,
        default_snapshot=row.default_snapshot,
        updated_at=row.updated_at,
        updated_by_email=email,
    )


async def ui_text_snapshot(
    session: AsyncSession, locale: Locale, namespace: str | None
) -> UiTextSnapshot:
    if namespace is not None:
        require_namespace(namespace)
    rows = await _list_overrides(session, locale)
    counts: dict[str, int] = {}
    for row, _ in rows:
        counts[row.namespace] = counts.get(row.namespace, 0) + 1
    entries = {f"{row.namespace}.{row.key}": row.value for row, _ in rows}
    selected = [
        _entry_view(row, email)
        for row, email in rows
        if namespace is None or row.namespace == namespace
    ]
    audit = [
        AdminAuditView(
            id=row.id,
            actor_user_id=row.actor_user_id,
            action=row.action,
            target=row.target,
            metadata=row.metadata_json,
            created_at=row.created_at,
        )
        for row in await _recent_audit(session)
    ]
    return UiTextSnapshot(
        locale=locale,
        namespace=namespace,
        version=content_version(entries),
        namespaces=list(UI_TEXT_NAMESPACES),
        locked_namespaces=list(UI_TEXT_LOCKED_NAMESPACES),
        namespace_counts=counts,
        entries=selected,
        audit=audit,
    )


async def upsert_ui_text(
    session: AsyncSession,
    redis: Redis,
    actor: User,
    locale: Locale,
    namespace: str,
    key: str,
    payload: UiTextWrite,
) -> UiTextSnapshot:
    require_namespace(namespace)
    value = normalize_value(payload.value, payload.default_value, key=key)
    row = await _find_override(session, locale, namespace, key)
    before = row.value if row is not None else None
    if row is None:
        row = UiTextOverride(namespace=namespace, key=key, locale=locale, value=value)
        session.add(row)
    row.value = value
    row.default_snapshot = payload.default_value
    row.updated_by_user_id = actor.id
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="ui_text_updated",
            target=_target(locale, namespace),
            metadata_json={
                "changes": [{"key": key, "before": _truncate(before), "after": _truncate(value)}],
                "count": 1,
            },
        )
    )
    await session.commit()
    await invalidate_ui_text_cache(redis)
    return await ui_text_snapshot(session, locale, namespace)


async def reset_ui_text(
    session: AsyncSession,
    redis: Redis,
    actor: User,
    locale: Locale,
    namespace: str,
    key: str,
) -> UiTextSnapshot:
    require_namespace(namespace)
    row = await _find_override(session, locale, namespace, key)
    if row is None:
        raise AppError(404, "ui_text_override_not_found", f"{key}：這條文案沒有覆寫")
    before = row.value
    await session.delete(row)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="ui_text_reset",
            target=_target(locale, namespace),
            metadata_json={"key": key, "before": _truncate(before)},
        )
    )
    await session.commit()
    await invalidate_ui_text_cache(redis)
    return await ui_text_snapshot(session, locale, namespace)


async def batch_ui_text(
    session: AsyncSession,
    redis: Redis,
    actor: User,
    payload: UiTextBatchWrite,
) -> UiTextSnapshot:
    require_namespace(payload.namespace)
    seen: set[str] = set()
    for entry in payload.entries:
        if entry.key in seen:
            raise AppError(
                422, "ui_text_batch_duplicate_key", f"{entry.key}：同一條文案在這次儲存中出現多次"
            )
        seen.add(entry.key)
    # Validate every entry before touching a row, so one bad sentence leaves the whole
    # batch unapplied instead of half of it.
    normalized: dict[str, str | None] = {
        entry.key: (
            None
            if entry.value is None
            else normalize_value(entry.value, entry.default_value, key=entry.key)
        )
        for entry in payload.entries
    }
    changes: list[dict[str, Any]] = []
    for entry in payload.entries:
        value = normalized[entry.key]
        row = await _find_override(session, payload.locale, payload.namespace, entry.key)
        if value is None:
            if row is None:
                continue
            changes.append({"key": entry.key, "before": _truncate(row.value), "after": None})
            await session.delete(row)
            continue
        before = row.value if row is not None else None
        if row is None:
            row = UiTextOverride(
                namespace=payload.namespace, key=entry.key, locale=payload.locale, value=value
            )
            session.add(row)
        row.value = value
        row.default_snapshot = entry.default_value
        row.updated_by_user_id = actor.id
        if before != value:
            changes.append(
                {"key": entry.key, "before": _truncate(before), "after": _truncate(value)}
            )
    if changes:
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action="ui_text_updated",
                target=_target(payload.locale, payload.namespace),
                metadata_json={"changes": changes, "count": len(changes)},
            )
        )
    await session.commit()
    await invalidate_ui_text_cache(redis)
    return await ui_text_snapshot(session, payload.locale, payload.namespace)
