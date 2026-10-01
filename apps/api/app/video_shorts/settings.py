"""The one row of Shorts settings: reading and saving it, the owner's standing consent to
publish, the pause switch, and the rule that approves a Short's final cut as it arrives."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoYoutubeConnection
from app.video_automation.judge import shorts_package_passed, shorts_qa_passed
from app.video_shorts import rules
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import VideoShortsSettings
from app.video_shorts.schemas import (
    ConsentOffer,
    ConsentView,
    SettingsView,
    SettingsWrite,
    ToolSettingsView,
)
from app.video_youtube.connection import linked

# What changing takes the consent with it; the rest of the settings leave it alone.
SCOPE_FIELDS = ("lines", "max_per_day", "slot_times", "timezone")


@dataclass(frozen=True)
class ChannelFacts:
    linked: bool
    channel_id: str | None = None
    title: str | None = None
    audited: bool = False
    problem: str | None = None


async def settings_row(session: AsyncSession, *, lock: bool = False) -> VideoShortsSettings:
    statement = select(VideoShortsSettings).where(VideoShortsSettings.id == 1)
    if lock:
        statement = statement.with_for_update()
    row = await session.scalar(statement)
    if row is None:
        row = VideoShortsSettings(id=1)
        session.add(row)
        await session.flush()
    return row


async def channel_facts(session: AsyncSession) -> ChannelFacts:
    """The channel the site publishes to, read without creating its row."""
    row = await session.scalar(select(VideoYoutubeConnection).where(VideoYoutubeConnection.id == 1))
    if row is None or not linked(row):
        return ChannelFacts(linked=False, problem=row.problem if row is not None else None)
    return ChannelFacts(
        linked=True,
        channel_id=row.channel_id,
        title=row.channel_title,
        audited=bool(row.audited),
        problem=row.problem,
    )


def settings_values(row: VideoShortsSettings) -> SettingsWrite:
    return SettingsWrite(
        enabled=row.enabled,
        lines=cast(Any, list(row.lines)),
        weekly_quota=cast(Any, dict(row.weekly_quota)),
        daily_pattern=cast(Any, list(row.daily_pattern)),
        slot_times=list(row.slot_times),
        timezone=row.timezone,
        stock_days=row.stock_days,
        lock_hours=row.lock_hours,
        upload_ahead_days=row.upload_ahead_days,
        max_per_day=row.max_per_day,
        seconds_min=row.seconds_min,
        seconds_max=row.seconds_max,
        voice=cast(Any, row.voice),
        locales=cast(Any, list(row.locales)),
        made_for_kids=row.made_for_kids,
        auto_approve=row.auto_approve,
        budget_ntd_30d=row.budget_ntd_30d,
        budget_soft_ntd=row.budget_soft_ntd,
        budget_total_ntd=row.budget_total_ntd,
        subject_models=cast(Any, dict(row.subject_models or {})),
        max_per_month=row.max_per_month,
    )


def current_scope(row: VideoShortsSettings, channel: ChannelFacts) -> dict[str, Any] | None:
    """What a consent given now would cover; None while no channel is linked."""
    if not channel.linked or channel.channel_id is None:
        return None
    return rules.consent_scope(
        channel_id=channel.channel_id,
        channel_title=channel.title,
        lines=row.lines,
        max_per_day=row.max_per_day,
        slot_times=row.slot_times,
        timezone=row.timezone,
    )


def consent_view(
    row: VideoShortsSettings, channel: ChannelFacts, now: datetime | None = None
) -> ConsentView:
    moment = now or datetime.now(UTC)
    scope = current_scope(row, channel)
    state, problem = rules.consent_state(
        autopublish=row.autopublish,
        granted=row.consent_scope,
        expires_at=row.consent_expires_at,
        current=scope,
        now=moment,
    )
    offer = None
    if scope is not None:
        text = rules.consent_text(scope)
        offer = ConsentOffer(text=text, text_sha256=rules.consent_sha256(text), scope=scope)
    return ConsentView(
        state=cast(Any, state),
        problem=problem,
        granted_at=row.consent_at,
        granted_by_user_id=row.consent_by_user_id,
        expires_at=row.consent_expires_at,
        text_sha256=row.consent_text_sha256,
        scope=row.consent_scope,
        offer=offer,
    )


def may_publish(
    row: VideoShortsSettings, channel: ChannelFacts, now: datetime | None = None
) -> tuple[bool, str | None]:
    """Whether the site may send a Short to YouTube on the owner's behalf now, and if not,
    why: the consent must hold for the settings as they are, and publishing must not be
    paused. The automatic sender (ticket video-shorts-youtube-auto) asks before every send."""
    view = consent_view(row, channel, now)
    if view.state == "none":
        return False, "還沒有自動上架授權"
    if view.state in ("expired", "invalid"):
        return False, view.problem
    if row.paused_at is not None:
        return False, "自動上架暫停中"
    return True, None


def settings_view(
    row: VideoShortsSettings, channel: ChannelFacts, now: datetime | None = None
) -> SettingsView:
    return SettingsView(
        **settings_values(row).model_dump(),
        campaign_start=row.campaign_start,
        autopublish=row.autopublish,
        paused_at=row.paused_at,
        consent=consent_view(row, channel, now),
        updated_at=row.updated_at,
    )


def tool_settings_view(row: VideoShortsSettings) -> ToolSettingsView:
    return ToolSettingsView(
        **settings_values(row).model_dump(),
        campaign_start=row.campaign_start,
        paused=row.paused_at is not None,
        updated_at=row.updated_at,
    )


async def update_settings(
    session: AsyncSession, actor: User, payload: SettingsWrite
) -> SettingsView:
    """Save the settings. A consent whose scope the new settings step outside of stops
    holding at once: publishing goes off until the owner agrees to the new wording."""
    row = await settings_row(session, lock=True)
    channel = await channel_facts(session)
    before = settings_values(row).model_dump(mode="json")
    after = payload.model_dump(mode="json")
    for key, value in after.items():
        setattr(row, key, value)
    row.updated_by_user_id = actor.id
    changed = sorted(key for key in after if after[key] != before.get(key))
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_shorts_settings_updated",
            target="video-shorts-settings:1",
            metadata_json={"changed": changed, "enabled": payload.enabled},
        )
    )
    scope = current_scope(row, channel)
    if row.autopublish and row.consent_scope is not None and scope is not None:
        problems = rules.scope_problems(row.consent_scope, scope)
        if problems:
            row.autopublish = False
            session.add(
                AdminAuditLog(
                    actor_user_id=actor.id,
                    action="video_shorts_autopublish_invalidated",
                    target="video-shorts-settings:1",
                    metadata_json={
                        "consent_id": str(row.consent_id) if row.consent_id else None,
                        "reasons": problems,
                    },
                )
            )
    await session.commit()
    return settings_view(row, channel)


async def grant_autopublish(
    session: AsyncSession, actor: User, text_sha256: str, now: datetime | None = None
) -> SettingsView:
    """Record the owner's agreement to the wording they were shown.

    The hash they send must be the hash of the wording for the settings as they are now: a
    page opened before a setting changed cannot agree to what it never displayed.
    """
    moment = now or datetime.now(UTC)
    row = await settings_row(session, lock=True)
    channel = await channel_facts(session)
    scope = current_scope(row, channel)
    if scope is None:
        raise ShortsRefused(
            409, "video_shorts_no_channel", "還沒有連結 YouTube 頻道：先到設定分頁連結"
        )
    text = rules.consent_text(scope)
    if rules.consent_sha256(text) != text_sha256:
        raise ShortsRefused(
            409,
            "video_shorts_consent_stale",
            "授權的條文已經跟著設定變了，請重新整理後讀過再同意",
        )
    row.consent_id = uuid4()
    row.consent_at = moment
    row.consent_by_user_id = actor.id
    row.consent_text_sha256 = text_sha256
    row.consent_expires_at = moment + timedelta(days=rules.CONSENT_DAYS)
    row.consent_scope = scope
    row.autopublish = True
    row.updated_by_user_id = actor.id
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_shorts_autopublish_granted",
            target="video-shorts-settings:1",
            metadata_json={
                "consent_id": str(row.consent_id),
                "text_sha256": text_sha256,
                "scope": scope,
                "expires_at": row.consent_expires_at.isoformat(),
            },
        )
    )
    await session.commit()
    return settings_view(row, channel, moment)


async def revoke_autopublish(session: AsyncSession, actor: User) -> SettingsView:
    """The owner takes the consent back; what is already scheduled on YouTube stays until
    they recall it."""
    row = await settings_row(session, lock=True)
    channel = await channel_facts(session)
    if row.consent_id is not None or row.autopublish:
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action="video_shorts_autopublish_revoked",
                target="video-shorts-settings:1",
                metadata_json={"consent_id": str(row.consent_id) if row.consent_id else None},
            )
        )
    row.autopublish = False
    row.consent_id = None
    row.consent_at = None
    row.consent_by_user_id = None
    row.consent_text_sha256 = None
    row.consent_expires_at = None
    row.consent_scope = None
    row.updated_by_user_id = actor.id
    await session.commit()
    return settings_view(row, channel)


async def set_paused(
    session: AsyncSession, actor: User, paused: bool, now: datetime | None = None
) -> SettingsView:
    """Hold or release publishing. Pausing stops new uploads and schedules at once; making,
    checking and slotting go on."""
    row = await settings_row(session, lock=True)
    channel = await channel_facts(session)
    if paused != (row.paused_at is not None):
        row.paused_at = (now or datetime.now(UTC)) if paused else None
        row.updated_by_user_id = actor.id
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action="video_shorts_paused" if paused else "video_shorts_resumed",
                target="video-shorts-settings:1",
                metadata_json={},
            )
        )
    await session.commit()
    return settings_view(row, channel)


async def auto_approves_shorts(
    session: AsyncSession, gate: str, payload: dict[str, Any], sha: str
) -> bool:
    """Whether a Short's final cut or upload confirmation stands on the automatic checks."""
    row = await session.scalar(select(VideoShortsSettings).where(VideoShortsSettings.id == 1))
    # With no row yet the defaults apply, and the default is on: the owner chose fully
    # automatic on 2026-09-28.
    if row is not None and not row.auto_approve:
        return False
    if gate == "final":
        return shorts_qa_passed(payload, sha)
    if gate == "publish":
        return shorts_package_passed(payload, sha)
    return False
