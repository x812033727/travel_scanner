"""The site sends Shorts to YouTube on the calendar, under the owner's standing consent
(docs/videos/SHORTS.md §上架).

A slot is locked a day before its time. When its Short has a video on YouTube (until the API
audit passes, the file the owner uploaded and the site found), the consent holds for the
settings as they are and publishing is not paused, the site writes the details and the captions
and schedules the video for the slot's time, through the same run the owner's own button starts
(``app.video_youtube.sync``). The audit entry names who gave the consent and says the request
was automatic. The site never makes a video public: YouTube does, at the time.

When the consent does not hold, the reason is written on the slot and nothing is sent. A time
someone else gave the video, on the card or in Studio, is left as it is. The owner's final say
stays: until the time, what is scheduled can be recalled.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID
from zoneinfo import ZoneInfo

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoProject
from app.video_reviews.storage import ReviewStore
from app.video_shorts import rules
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import VideoShortsSettings, VideoShortsSlot
from app.video_shorts.quota import QUOTA_REASONS, Quota, pacific_day
from app.video_shorts.schemas import RecallItem, RecallOut
from app.video_shorts.settings import ChannelFacts, channel_facts, may_publish, settings_row
from app.video_shorts.slots import day_bounds
from app.video_youtube import connection, sync
from app.video_youtube.client import YoutubeClient, YoutubeError
from app.video_youtube.errors import Refused
from app.video_youtube.requests import as_dict, unschedule_body
from app.video_youtube.schemas import PublishIn
from app.video_youtube.state import now_text, parse_time, running

# A run that failed is started again on the next knock, this many times in all; then the slot
# says why and waits for the owner, or for its time to pass.
MAX_ATTEMPTS = 3
WAITS_FOR_UPLOAD = "等站主把這支的檔案上傳到 YouTube Studio"
QUOTA_SPENT = "今天的 YouTube API 配額用完了，明天再送"
RECALLED = "站主撤回了排程"
# What a run that YouTube refused for the quota leaves as its error.
QUOTA_ERROR = sync.describe(YoutubeError(403, "quotaExceeded", ""))


@dataclass(frozen=True)
class Sent:
    sent: int = 0
    held: int = 0


def scheduled_for(state: dict[str, Any] | None, starts_at: datetime) -> bool:
    """Whether the video's last request was to go public at this slot's time."""
    request = as_dict(state.get("request")) if state else {}
    return request.get("visibility") == "scheduled" and parse_time(
        request.get("publish_at")
    ) == starts_at.astimezone(UTC)


def _state(project: VideoProject) -> dict[str, Any] | None:
    return project.youtube_sync if isinstance(project.youtube_sync, dict) else None


def _note(slot: VideoShortsSlot, note: str | None, now: datetime) -> None:
    if slot.note != note:
        slot.note = note
        slot.updated_at = now


async def _held(
    session: AsyncSession,
    statuses: tuple[str, ...],
    after: datetime | None = None,
    *,
    lock: bool = False,
) -> list[tuple[VideoShortsSlot, VideoProject]]:
    """The slots of these statuses that hold a Short, earliest first, each with its Short;
    only the ones after ``after`` when it is given."""
    statement = select(VideoShortsSlot).where(
        VideoShortsSlot.status.in_(statuses), VideoShortsSlot.project_slug.is_not(None)
    )
    if after is not None:
        statement = statement.where(VideoShortsSlot.starts_at > after)
    if lock:
        statement = statement.with_for_update()
    slots = list(await session.scalars(statement.order_by(VideoShortsSlot.starts_at)))
    if not slots:
        return []
    projects = {
        project.slug: project
        for project in await session.scalars(
            select(VideoProject).where(
                VideoProject.slug.in_([str(slot.project_slug) for slot in slots])
            )
        )
    }
    return [
        (slot, projects[str(slot.project_slug)])
        for slot in slots
        if str(slot.project_slug) in projects
    ]


async def settle(session: AsyncSession, now: datetime | None = None) -> int:
    """The locked slots whose Short the site finished scheduling become scheduled. Returns
    how many did. The caller commits.

    Every locked slot is looked at, however close its time is or even past it: a run that
    finished while nobody knocked did schedule the video, and the calendar says so before
    ``lock_due_slots`` gives up the slots that did not make it.
    """
    moment = now or datetime.now(UTC)
    done = 0
    for slot, project in await _held(session, ("locked",)):
        state = _state(project)
        if (
            state is not None
            and state.get("status") == "done"
            and scheduled_for(state, slot.starts_at)
            and project.youtube_publish_at == slot.starts_at
        ):
            slot.status = "scheduled"
            slot.note = None
            slot.updated_at = moment
            done += 1
    return done


def _failed_today(state: dict[str, Any], now: datetime) -> bool:
    finished = parse_time(state.get("finished_at"))
    return finished is not None and pacific_day(finished) == pacific_day(now)


def outside_consent(
    scope: Mapping[str, Any] | None, line: str | None, starts_at: datetime, place: int
) -> str | None:
    """Why this Short, in this slot, is not what the owner agreed to, or None when it is.

    The consent names the content lines, the times of day and how many a day. The settings
    are held to it when they are saved; this holds each Short to it as it is sent, because a
    slot can be moved to any time on the calendar, and a Short can be older than the consent.
    ``place`` counts the slots of the day that go out, this one included, earliest first.
    What is outside the consent is the owner's to send, from the card.
    """
    if scope is None:
        return "還沒有自動上架授權"
    if line not in scope.get("lines", []):
        name = rules.LINE_NAMES.get(str(line), str(line))
        return f"授權的內容線沒有「{name}」，這一支要站主自己送"
    times = [str(value) for value in scope.get("slot_times", [])]
    local = starts_at.astimezone(ZoneInfo(str(scope.get("timezone") or "UTC")))
    if f"{local:%H:%M}" not in times:
        return (
            f"這一格的時間 {local:%H:%M} 不在授權的公開時間裡（{'、'.join(times)}），"
            "這一支要站主自己送"
        )
    limit = int(scope.get("max_per_day") or 0)
    if place > limit:
        return f"這一天排了超過 {limit} 支，授權是一天最多 {limit} 支，這一支要站主自己送"
    return None


async def _places(
    session: AsyncSession, slots: Sequence[VideoShortsSlot], timezone: str
) -> dict[UUID, int]:
    """For the slots of the days these slots fall on: each one's place among the slots of
    its day that go out or went out, earliest first, from 1."""
    if not slots:
        return {}
    zone = ZoneInfo(timezone)
    days = {slot.starts_at.astimezone(zone).date() for slot in slots}
    first = day_bounds(min(days), timezone)[0]
    last = day_bounds(max(days), timezone)[1]
    places: dict[UUID, int] = {}
    counted: dict[date, int] = {}
    for row in await session.scalars(
        select(VideoShortsSlot)
        .where(
            VideoShortsSlot.status.in_(("locked", "scheduled", "published")),
            VideoShortsSlot.starts_at >= first,
            VideoShortsSlot.starts_at < last,
        )
        .order_by(VideoShortsSlot.starts_at)
    ):
        day = row.starts_at.astimezone(zone).date()
        counted[day] = counted.get(day, 0) + 1
        places[row.id] = counted[day]
    return places


async def send_due(
    session: AsyncSession,
    store: ReviewStore,
    row: VideoShortsSettings,
    channel: ChannelFacts,
    quota: Quota,
    now: datetime | None = None,
) -> Sent:
    """Start the run of every locked slot that may go out now; hold the rest and say why."""
    moment = now or datetime.now(UTC)
    allowed, reason = may_publish(row, channel, moment)
    giver = (
        await session.get(User, row.consent_by_user_id)
        if allowed and row.consent_by_user_id is not None
        else None
    )
    if allowed and giver is None:
        allowed, reason = False, "同意自動上架的那個帳號已經不在了，要重新同意"
    behalf = {"auto": True, "consent_id": str(row.consent_id) if row.consent_id else None}
    zone = ZoneInfo(row.timezone)
    due = await _held(session, ("locked",), moment + rules.MIN_LEAD)
    scope = row.consent_scope if isinstance(row.consent_scope, dict) else None
    places = await _places(
        session, [slot for slot, _project in due], str((scope or {}).get("timezone") or "UTC")
    )
    sent = held = 0
    for slot, project in due:
        slug = project.slug
        state = _state(project)
        status = state.get("status") if state else None
        mine = scheduled_for(state, slot.starts_at)
        going = running(state)
        # Where the video stands on YouTube's schedule, as far as the site knows. A recall
        # empties it, so what was recalled is sent again once publishing is resumed.
        placed = project.youtube_publish_at if status == "done" else None
        if mine and (going or placed == slot.starts_at):
            continue
        failed = state is not None and mine and status == "failed"
        error = str(state.get("error") or "原因不明") if state is not None and failed else ""
        out_of_quota = failed and error == QUOTA_ERROR
        if state is not None and out_of_quota and _failed_today(state, moment):
            await quota.mark_refused()
        attempts = int(state.get("attempts") or 0) if state is not None else 0
        outside = (
            outside_consent(scope, project.shorts_line, slot.starts_at, places.get(slot.id, 1))
            if allowed
            else None
        )
        waits: str | None = None
        if project.dropped_at is not None:
            waits = "這支已經被放棄了"
        elif not allowed:
            waits = reason
        elif outside is not None:
            waits = outside
        elif project.youtube_video_id is None:
            # Until the API audit passes the site uploads nothing itself.
            waits = WAITS_FOR_UPLOAD
        elif going:
            waits = "這支正在送 YouTube，等它跑完"
        elif placed is not None and placed != slot.starts_at:
            waits = (
                f"這支已經排在 {placed.astimezone(zone):%m/%d %H:%M} 公開，不是這一格的時間；"
                "網站不改已經排好的時間"
            )
        elif not await quota.allows_sending():
            waits = QUOTA_SPENT
        elif failed and not out_of_quota and attempts >= MAX_ATTEMPTS:
            waits = f"送了 {attempts} 次都沒有成功：{error}"
        if waits is not None:
            _note(slot, waits, moment)
            held += 1
            continue
        assert giver is not None
        # A run the recall stopped starts over: the time it may have written is gone again.
        again = failed and error != RECALLED
        try:
            if again:
                await sync.retry_sync(session, slug, giver, on_behalf=behalf)
            else:
                await sync.request_sync(
                    session,
                    store,
                    slug,
                    giver,
                    PublishIn(
                        mode="studio",
                        url=project.youtube_video_id,
                        visibility="scheduled",
                        publish_at=slot.starts_at,
                    ),
                    on_behalf=behalf,
                )
        except Refused as refused:
            _note(slot, refused.detail, moment)
            held += 1
            continue
        await quota.add("sync")
        _note(slot, f"上一次沒有成功（{error}），已經重新送出" if again else None, moment)
        sent += 1
    await session.commit()
    return Sent(sent=sent, held=held)


def _stop_run(project: VideoProject, now: datetime) -> None:
    """End a run that is on its way: it finds its state replaced and stops at its next step."""
    state = _state(project)
    if state is None or state.get("status") not in ("queued", "running"):
        return
    project.youtube_sync = {
        **state,
        "status": "failed",
        "error": RECALLED,
        "run": None,
        "lease_until": None,
        "finished_at": now_text(now),
        # Not a failure of YouTube's: resuming sends it again, whatever was tried before.
        "attempts": 0,
    }


async def recall(
    session: AsyncSession,
    http: httpx.AsyncClient,
    user: User,
    quota: Quota,
    now: datetime | None = None,
) -> RecallOut:
    """Take every Short that is scheduled and not public yet off YouTube's schedule: it stays
    on the channel, private, and its slot holds it again.

    YouTube is asked about every Short whose slot is locked or scheduled, so one whose run
    finished a moment ago is recalled with the rest. Publishing is paused with it: otherwise
    the next knock would schedule the same Shorts again, which is not what someone who
    recalls them means; "resume" sends them once more.
    """
    moment = now or datetime.now(UTC)
    row = await settings_row(session, lock=True)
    channel = await channel_facts(session)
    held = [
        (slot, project)
        for slot, project in await _held(session, ("locked", "scheduled"), moment, lock=True)
        if project.youtube_video_id
    ]
    paused = row.paused_at is None
    if paused:
        row.paused_at = moment
        row.updated_by_user_id = user.id
    items: list[RecallItem] = []
    if held:
        if not channel.linked:
            raise ShortsRefused(
                409, "video_shorts_no_channel", "YouTube 頻道沒有連結，撤回不了已經排程的影片"
            )
        try:
            client = YoutubeClient(http, await connection.access_token(session, http))
        except Refused as refused:
            raise ShortsRefused(refused.status, refused.code, refused.detail) from refused
        refused_for_quota = False
        for slot, project in held:
            video_id = str(project.youtube_video_id)
            _stop_run(project, moment)
            if refused_for_quota:
                items.append(_not_recalled(project, QUOTA_SPENT.replace("再送", "再撤回")))
                continue
            try:
                video = await client.video(video_id)
                await quota.add("videos.list")
                status = as_dict(video.get("status")) if video is not None else {}
                if video is None:
                    items.append(_not_recalled(project, "YouTube 上找不到這支影片"))
                    continue
                if status.get("privacyStatus") == "public":
                    items.append(_not_recalled(project, "已經公開了；要下架請在 Studio 處理"))
                    continue
                if not status.get("publishAt"):
                    # Nothing to take back on YouTube. A locked slot only waited for its
                    # run; a scheduled one was taken off the schedule in Studio.
                    if slot.status == "scheduled":
                        _release(slot, project, moment)
                        items.append(_not_recalled(project, "YouTube 上已經沒有排程了"))
                    continue
                await client.update_video(unschedule_body(video))
                await quota.add("videos.update")
            except YoutubeError as error:
                if error.reason in QUOTA_REASONS:
                    await quota.mark_refused()
                    refused_for_quota = True
                items.append(_not_recalled(project, sync.describe(error)))
                continue
            except httpx.HTTPError:
                items.append(_not_recalled(project, "連不到 YouTube，請再試一次"))
                continue
            _release(slot, project, moment)
            items.append(
                RecallItem(
                    slug=project.slug,
                    youtube_video_id=video_id,
                    recalled=True,
                    detail="已經取消排程，影片保持私人",
                )
            )
    recalled = sum(1 for item in items if item.recalled)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_shorts_recalled",
            target="video-shorts-settings:1",
            metadata_json={
                "recalled": [item.slug for item in items if item.recalled],
                "not_recalled": [item.slug for item in items if not item.recalled],
                "paused": paused,
            },
        )
    )
    await session.commit()
    return RecallOut(recalled=recalled, items=items)


def _release(slot: VideoShortsSlot, project: VideoProject, now: datetime) -> None:
    """The video is off YouTube's schedule: the slot holds its Short again, unsent."""
    project.youtube_publish_at = None
    project.updated_at = now
    if slot.status == "scheduled":
        slot.status = "assigned"
        slot.locked_at = None
    slot.note = RECALLED
    slot.updated_at = now


def _not_recalled(project: VideoProject, detail: str) -> RecallItem:
    return RecallItem(
        slug=project.slug,
        youtube_video_id=str(project.youtube_video_id),
        recalled=False,
        detail=detail,
    )
