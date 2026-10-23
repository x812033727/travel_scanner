"""The backup card on the settings tab of /admin/videos, and what the worker tells it.

One private ProviderConfig row, absent from the generic provider editor like the VPS uploader's
(app/video_youtube/vps_settings.py). It stores no credential: the Drive token lives in
/etc/travel-scanner/rclone-videos.conf on the host and only the worker reads it.

``config`` holds the owner's part (path, tiers, folder names, ``saved_at``) and the worker's part
(the lock path, the free space, an open test request). The worker's writes bump the row's
``updated_at``, so the card's optimistic check compares ``saved_at``, which only a save moves:
a worker round never makes the owner's next save a conflict.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, ProviderConfig, User
from app.problems import AppError
from app.video_backup.schemas import (
    LockIn,
    ProbeAnswerIn,
    ProbeView,
    SettingsIn,
    SettingsView,
    SpaceView,
)
from app.video_backup.target import (
    DEFAULT_FOLDER_NAMES,
    DEFAULT_PATH,
    FULL_CATEGORIES,
    PathInvalid,
    Tier,
    as_dict,
    normalise_path,
    remote_prefix,
    segment_problem,
)

PROVIDER = "video_backup"
LOCK_HELP = (
    "要備份到別的地方，請先在主機修改 /etc/travel-scanner/rclone-videos.conf 的 "
    "root_folder_id 與 video-worker 的 VIDEO_BACKUP_LOCK_PATH"
)


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        moment = datetime.fromisoformat(value)
    except ValueError:
        return None
    return moment.replace(tzinfo=UTC) if moment.tzinfo is None else moment.astimezone(UTC)


def stamp(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


async def settings_row(session: AsyncSession, *, lock: bool = False) -> ProviderConfig | None:
    with session.no_autoflush:
        if lock and session.get_bind().dialect.name == "postgresql":
            # Serialize the first save too: two of them must not both insert the row.
            key = int.from_bytes(
                hashlib.sha256(f"provider-settings:{PROVIDER}".encode()).digest()[:8], signed=True
            )
            await session.execute(select(func.pg_advisory_xact_lock(key)))
        statement = select(ProviderConfig).where(ProviderConfig.provider == PROVIDER)
        if lock:
            statement = statement.with_for_update().execution_options(populate_existing=True)
        return cast(ProviderConfig | None, await session.scalar(statement))


def config_of(row: ProviderConfig | None) -> dict[str, Any]:
    config = row.config if row is not None and isinstance(row.config, dict) else {}
    return dict(config)


def enabled_of(row: ProviderConfig | None) -> bool:
    return bool(row is not None and row.enabled)


def path_of(config: dict[str, Any]) -> str:
    path = config.get("path")
    return path if isinstance(path, str) and path else DEFAULT_PATH


def mapping_of(config: dict[str, Any], field: str) -> dict[str, str]:
    value = config.get(field)
    return {str(key): str(item) for key, item in value.items()} if isinstance(value, dict) else {}


def tiers_of(config: dict[str, Any]) -> dict[str, Tier]:
    known: dict[str, Tier] = {"basic": "basic", "full": "full", "off": "off"}
    return {key: known[tier] for key, tier in mapping_of(config, "tiers").items() if tier in known}


def lock_of(config: dict[str, Any]) -> str | None:
    lock = config.get("lock_path")
    return lock if isinstance(lock, str) and lock else None


def problem_of(row: ProviderConfig | None) -> str | None:
    """Why the worker must not copy with these settings, or None when it may."""
    config = config_of(row)
    if not enabled_of(row):
        return "備份尚未開啟"
    reported = config.get("lock_problem")
    if isinstance(reported, str) and reported:
        return reported
    lock = lock_of(config)
    if lock is None:
        return "主機的 video-worker 還沒回報 rclone 鎖定的資料夾（VIDEO_BACKUP_LOCK_PATH）"
    if remote_prefix(path_of(config), lock) is None:
        return f"路徑 {path_of(config)} 不在主機鎖定的 {lock} 之內；{LOCK_HELP}"
    return None


def probe_view(row: ProviderConfig | None) -> ProbeView:
    config = config_of(row)
    pending = as_dict(config.get("test"))
    status = row.last_test_status if row is not None else None
    return ProbeView(
        pending_id=UUID(pending["id"]) if isinstance(pending.get("id"), str) else None,
        requested_at=parse_time(pending.get("requested_at")),
        status="success" if status == "success" else "failed" if status == "failed" else None,
        message=row.last_test_message if row is not None else None,
        tested_at=stamp(row.last_tested_at) if row is not None else None,
    )


def space_view(config: dict[str, Any]) -> SpaceView:
    space = as_dict(config.get("space"))

    def size(field: str) -> int | None:
        value = space.get(field)
        return value if type(value) is int and value >= 0 else None

    return SpaceView(
        free_bytes=size("free_bytes"),
        total_bytes=size("total_bytes"),
        at=parse_time(space.get("at")),
    )


def view_of(row: ProviderConfig | None) -> SettingsView:
    config = config_of(row)
    return SettingsView(
        enabled=enabled_of(row),
        path=path_of(config),
        lock_path=lock_of(config),
        lock_reported_at=parse_time(config.get("lock_reported_at")),
        problem=problem_of(row),
        tiers=tiers_of(config),
        folder_names=mapping_of(config, "folder_names"),
        default_folder_names=dict(DEFAULT_FOLDER_NAMES),
        full_categories=sorted(FULL_CATEGORIES),
        updated_at=parse_time(config.get("saved_at")),
        test=probe_view(row),
        space=space_view(config),
    )


async def view(session: AsyncSession) -> SettingsView:
    return view_of(await settings_row(session))


def _new_row(session: AsyncSession) -> ProviderConfig:
    # Off until the owner turns it on; the worker may report its lock before that.
    row = ProviderConfig(provider=PROVIDER, enabled=False, priority=100, config={})
    session.add(row)
    return row


def _audit(session: AsyncSession, user_id: UUID | None, action: str, **values: Any) -> None:
    session.add(
        AdminAuditLog(actor_user_id=user_id, action=action, target=PROVIDER, metadata_json=values)
    )


def _now() -> datetime:
    return datetime.now(UTC)


async def save(session: AsyncSession, user: User, payload: SettingsIn) -> SettingsView:
    row = await settings_row(session, lock=True)
    config = config_of(row)
    if stamp(payload.expected_updated_at) != parse_time(config.get("saved_at")):
        raise AppError(
            409, "video_backup_settings_conflict", "設定已被其他管理員更新，請重新載入後再儲存"
        )
    if payload.path is not None:
        try:
            config["path"] = normalise_path(payload.path)
        except PathInvalid as error:
            raise AppError(422, "video_backup_path_invalid", str(error)) from None
    lock = lock_of(config)
    path = path_of(config)
    if payload.path is not None and lock is not None and remote_prefix(path, lock) is None:
        raise AppError(
            422,
            "video_backup_path_outside_lock",
            f"主機的 rclone 只能寫入 {lock} 和它底下的資料夾；{LOCK_HELP}",
        )
    if payload.tiers is not None:
        config["tiers"] = dict(sorted(payload.tiers.items()))
    if payload.folder_names is not None:
        names: dict[str, str] = {}
        for key, name in payload.folder_names.items():
            name = name.strip()
            if not name:
                continue
            problem = segment_problem(name)
            if problem:
                raise AppError(422, "video_backup_folder_name_invalid", f"{key}：{problem}")
            names[key] = name
        config["folder_names"] = dict(sorted(names.items()))
    if row is None:
        row = _new_row(session)
    if payload.enabled is not None:
        row.enabled = payload.enabled
    previous = parse_time(config.get("saved_at"))
    moment = _now()
    saved_at = max(moment, previous + timedelta(microseconds=1)) if previous else moment
    config["saved_at"] = saved_at.isoformat()
    config.setdefault("path", path)
    row.config = config
    row.updated_by_user_id = user.id
    _audit(
        session,
        user.id,
        "video_backup_settings_updated",
        fields=sorted(payload.model_fields_set - {"expected_updated_at"}),
        enabled=row.enabled,
        path=path,
    )
    await session.commit()
    return view_of(row)


async def request_test(session: AsyncSession, user: User) -> SettingsView:
    """Ask the worker to write and delete a probe file next round; one open request at a time,
    so clicking again before it answers does not queue another."""
    row = await settings_row(session, lock=True) or _new_row(session)
    config = config_of(row)
    if not isinstance(config.get("test"), dict):
        config["test"] = {
            "id": str(uuid4()),
            "requested_at": _now().isoformat(),
            "requested_by": str(user.id),
        }
        row.config = config
        _audit(session, user.id, "video_backup_test_requested", id=config["test"]["id"])
    await session.commit()
    return view_of(row)


def _space(config: dict[str, Any], free: int | None, total: int | None) -> None:
    if free is None and total is None:
        return
    config["space"] = {"free_bytes": free, "total_bytes": total, "at": _now().isoformat()}


async def record_lock(session: AsyncSession, payload: LockIn) -> SettingsView:
    """The worker's lock path (VIDEO_BACKUP_LOCK_PATH) as it starts, or why it has none."""
    lock: str | None = None
    if payload.lock_path is not None:
        try:
            lock = normalise_path(payload.lock_path)
        except PathInvalid as error:
            raise AppError(422, "video_backup_lock_invalid", str(error)) from None
    row = await settings_row(session, lock=True) or _new_row(session)
    config = config_of(row)
    config["lock_path"] = lock
    config["lock_reported_at"] = _now().isoformat()
    problem = (payload.problem or "").strip()
    if lock is None and not problem:
        problem = "主機沒有設定影片備份用的 rclone（/etc/travel-scanner/rclone-videos.conf）"
    config["lock_problem"] = problem or None
    row.config = config
    await session.commit()
    return view_of(row)


async def answer_test(session: AsyncSession, test_id: UUID, payload: ProbeAnswerIn) -> SettingsView:
    row = await settings_row(session, lock=True)
    config = config_of(row)
    pending = as_dict(config.get("test"))
    if row is None or pending.get("id") != str(test_id):
        raise AppError(404, "video_backup_test_not_found", "沒有這個待回覆的備份測試")
    config["test"] = None
    _space(config, payload.free_bytes, payload.total_bytes)
    row.config = config
    row.last_tested_at = _now()
    row.last_test_status = "success" if payload.ok else "failed"
    row.last_test_message = payload.message
    _audit(session, None, "video_backup_test_answered", id=str(test_id), ok=payload.ok)
    await session.commit()
    return view_of(row)


async def record_space(session: AsyncSession, free: int | None, total: int | None) -> None:
    """The free space a report carried; the caller commits."""
    if free is None and total is None:
        return
    row = await settings_row(session, lock=True) or _new_row(session)
    config = config_of(row)
    _space(config, free, total)
    row.config = config
