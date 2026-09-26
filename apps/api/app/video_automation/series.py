"""A long drama series: the series, its documents, its episodes, and what the worker does next.

The owner starts a series on /admin/videos (docs/videos/SERIES.md). The worker plans the setting
book, then the whole-series outline, then one chapter's detailed outline at a time; the owner
approves each, or sends it back with a note, and the worker rewrites it. Once a chapter is
approved its episodes are ready, and the worker starts them in order: the next one when the
previous is done (cleared for upload) or skipped, while fewer than ``series_max_in_flight`` are
in the making. Every rule about "what next" is a pure function over the loaded rows
(``next_job_for``), so it can be tested without a database.

The router turns ``SeriesRefused`` into the API's problem response; nothing here raises
``AppError``.
"""

from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, cast
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoProject, VideoToolToken
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.requests import request_view
from app.video_automation.schemas import (
    SeriesContextOut,
    SeriesDocEditIn,
    SeriesDocOut,
    SeriesDocSubmitIn,
    SeriesEpisodeEditIn,
    SeriesEpisodeOut,
    SeriesEpisodeRecapIn,
    SeriesEpisodeStartOut,
    SeriesIn,
    SeriesJob,
    SeriesJobOut,
    SeriesOut,
    SeriesPatch,
    SeriesSummary,
)
from app.video_media.meter import spend_by_slug
from app.video_reviews.admin_service import list_projects

# The episode fields a chapter outline must give every episode, in the order the owner reads
# them: the hook, the conflict, the turn, the cliffhanger (docs/videos/SERIES.md).
BEAT_FIELDS = ("hook", "conflict", "turn", "cliffhanger")
RECENT_RECAPS = 3
ACTIVE_STATUSES = ("setting", "outline", "active")
EPISODE_OPEN = ("planned", "ready", "queued", "started")


class SeriesRefused(Exception):
    """Why the change cannot be made; the router turns it into the API's error."""

    def __init__(self, status: int, code: str, detail: str):
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail


def _now() -> datetime:
    return datetime.now(UTC)


# --- pure helpers ---------------------------------------------------------------------------


def chapter_count(planned_episodes: int, episodes_per_chapter: int) -> int:
    return max(1, -(-planned_episodes // episodes_per_chapter))


def chapter_range(series: VideoDramaSeries, chapter: int) -> tuple[int, int]:
    """The first and last episode number of a chapter; the last chapter may be short."""
    size = series.episodes_per_chapter
    first = (chapter - 1) * size + 1
    return first, min(chapter * size, series.planned_episodes)


def chapter_of(series: VideoDramaSeries, number: int) -> int:
    return (number - 1) // series.episodes_per_chapter + 1


def latest_docs(docs: list[VideoDramaDoc]) -> dict[tuple[str, int], VideoDramaDoc]:
    """The newest version of every document, keyed by kind and chapter (0 for the series')."""
    latest: dict[tuple[str, int], VideoDramaDoc] = {}
    for doc in docs:
        key = (doc.kind, doc.chapter_number)
        if key not in latest or doc.version > latest[key].version:
            latest[key] = doc
    return latest


def approved_doc(docs: list[VideoDramaDoc], kind: str, chapter: int = 0) -> VideoDramaDoc | None:
    """The newest approved version of a document, whatever came after it."""
    found = [
        doc
        for doc in docs
        if doc.kind == kind and doc.chapter_number == chapter and doc.status == "approved"
    ]
    return max(found, key=lambda doc: doc.version) if found else None


def doc_problem(series: VideoDramaSeries, payload: SeriesDocSubmitIn) -> str | None:
    """Why a document the worker sends cannot be filed, in the worker's words; None when it can.

    The shapes are the contract with tools/video/automation/series.mjs: a setting book names
    its characters; an outline lists every chapter with its episodes; a chapter outline gives
    every episode of its range the beats the owner reads.
    """
    body = payload.body_json
    if payload.kind == "setting":
        characters = body.get("characters")
        if not isinstance(characters, list) or not characters:
            return "a setting book needs a characters list"
        for character in characters:
            if not isinstance(character, dict) or not all(
                isinstance(character.get(key), str) and character.get(key)
                for key in ("id", "name", "appearance")
            ):
                return "every character needs an id, a name and an appearance"
        return None
    if payload.kind == "outline":
        chapters = body.get("chapters")
        total = chapter_count(series.planned_episodes, series.episodes_per_chapter)
        if not isinstance(chapters, list) or len(chapters) != total:
            return f"an outline lists {total} chapters"
        numbers: list[int] = []
        for chapter in chapters:
            if not isinstance(chapter, dict) or not isinstance(chapter.get("episodes"), list):
                return "every chapter needs a title and an episodes list"
            for episode in chapter["episodes"]:
                if not isinstance(episode, dict) or not isinstance(episode.get("number"), int):
                    return "every episode needs a number, a title and a logline"
                numbers.append(int(episode["number"]))
        if sorted(numbers) != list(range(1, series.planned_episodes + 1)):
            return f"the outline's episodes must be numbered 1 to {series.planned_episodes}"
        return None
    first, last = chapter_range(series, payload.chapter_number)
    if payload.chapter_number < 1 or first > series.planned_episodes:
        return f"chapter {payload.chapter_number} is outside the series"
    episodes = body.get("episodes")
    if not isinstance(episodes, list):
        return "a chapter outline needs an episodes list"
    numbers = []
    for episode in episodes:
        if not isinstance(episode, dict) or not isinstance(episode.get("number"), int):
            return "every episode needs a number"
        missing = [key for key in BEAT_FIELDS if not episode.get(key)]
        if missing:
            return f"episode {episode['number']} lacks {', '.join(missing)}"
        numbers.append(int(episode["number"]))
    if sorted(numbers) != list(range(first, last + 1)):
        return f"chapter {payload.chapter_number} covers episodes {first} to {last}"
    return None


@dataclass(frozen=True)
class NextJob:
    kind: str
    chapter_number: int | None = None
    episode_number: int | None = None
    previous: VideoDramaDoc | None = None
    rewrites_left: int = 0


def _rewrite_job(
    kind: str, chapter: int, docs: list[VideoDramaDoc], rewrites: int
) -> NextJob | None:
    """Plan (or rewrite) a document when none is waiting or approved for this kind and chapter."""
    latest = latest_docs(docs).get((kind, chapter))
    if latest is None:
        return NextJob(kind=kind, chapter_number=chapter, rewrites_left=rewrites)
    if latest.status != "rejected":
        return None
    # The first version was not a rewrite: version 2 is the first rewrite.
    left = rewrites - (latest.version - 1)
    if left <= 0:
        return None
    return NextJob(kind=kind, chapter_number=chapter, previous=latest, rewrites_left=left)


def next_job_for(
    series: VideoDramaSeries,
    docs: list[VideoDramaDoc],
    episodes: list[VideoDramaEpisode],
    settings: VideoAutomationSettings,
    *,
    started_this_month: int,
) -> NextJob | None:
    """What the worker should do next for this series, or None when it waits for the owner.

    Documents come first (the setting book, then the outline, then a chapter's outline when it
    is due), then the next ready episode, in order, one at a time unless the settings allow two.
    """
    rewrites = settings.series_doc_rewrites
    if series.status == "setting":
        return _rewrite_job("setting", 0, docs, rewrites)
    if series.status == "outline":
        return _rewrite_job("outline", 0, docs, rewrites)
    if series.status != "active":
        return None
    by_number = {episode.number: episode for episode in episodes}
    latest = latest_docs(docs)
    started_numbers = [e.number for e in episodes if e.status in ("started", "done", "skipped")]
    reached = max(started_numbers, default=0)
    total = chapter_count(series.planned_episodes, series.episodes_per_chapter)
    for chapter in range(1, total + 1):
        current = latest.get(("chapter", chapter))
        if current is not None and current.status in ("review", "generating"):
            break
        if current is not None and current.status == "approved":
            continue
        previous_ok = chapter == 1 or (
            (previous := latest.get(("chapter", chapter - 1))) is not None
            and previous.status == "approved"
        )
        if not previous_ok:
            break
        _first, last_of_previous = chapter_range(series, chapter - 1) if chapter > 1 else (0, 0)
        due = (
            chapter == 1
            or series.requested_chapter == chapter
            or reached >= last_of_previous - settings.series_chapter_ahead
        )
        if not due:
            break
        job = _rewrite_job("chapter", chapter, docs, rewrites)
        if job is not None:
            return job
        break
    in_flight = sum(1 for episode in episodes if episode.status == "started")
    if in_flight >= settings.series_max_in_flight:
        return None
    if started_this_month >= settings.series_episodes_per_month:
        return None
    ready = sorted(e.number for e in episodes if e.status == "ready")
    if not ready:
        return None
    number = ready[0]
    previous_episode = by_number.get(number - 1)
    previous_done = number == 1 or (
        previous_episode is not None and previous_episode.status in ("done", "skipped")
    )
    if series.force_next:
        return NextJob(kind="episode", episode_number=number)
    if not previous_done or (number > 1 and not settings.series_auto_continue):
        return None
    return NextJob(kind="episode", episode_number=number)


def episode_rows_from_outline(
    series: VideoDramaSeries, body: dict[str, Any]
) -> dict[int, dict[str, str]]:
    """Every episode's title and logline from an approved outline, by number."""
    rows: dict[int, dict[str, str]] = {}
    for chapter in body.get("chapters") or []:
        if not isinstance(chapter, dict):
            continue
        for episode in chapter.get("episodes") or []:
            if not isinstance(episode, dict) or not isinstance(episode.get("number"), int):
                continue
            number = int(episode["number"])
            if 1 <= number <= series.planned_episodes:
                rows[number] = {
                    "title": str(episode.get("title") or f"第 {number} 集")[:200],
                    "logline": str(episode.get("logline") or ""),
                }
    for number in range(1, series.planned_episodes + 1):
        rows.setdefault(number, {"title": f"第 {number} 集", "logline": ""})
    return rows


def beats_from_chapter(body: dict[str, Any]) -> dict[int, dict[str, Any]]:
    """Every episode's beats from an approved chapter outline, by number."""
    beats: dict[int, dict[str, Any]] = {}
    for episode in body.get("episodes") or []:
        if isinstance(episode, dict) and isinstance(episode.get("number"), int):
            beats[int(episode["number"])] = dict(episode)
    return beats


# --- views ----------------------------------------------------------------------------------


def doc_view(doc: VideoDramaDoc) -> SeriesDocOut:
    return SeriesDocOut(
        id=doc.id,
        kind=cast(Any, doc.kind),
        chapter_number=doc.chapter_number,
        version=doc.version,
        body_md=doc.body_md,
        body_json=doc.body_json or {},
        status=cast(Any, doc.status),
        note=doc.note,
        decided_at=doc.decided_at,
        created_at=doc.created_at,
    )


def episode_view(
    episode: VideoDramaEpisode, video: dict[str, object] | None = None
) -> SeriesEpisodeOut:
    return SeriesEpisodeOut(
        number=episode.number,
        chapter_number=episode.chapter_number,
        title=episode.title,
        logline=episode.logline,
        beats=episode.beats or {},
        status=cast(Any, episode.status),
        slug=episode.slug,
        recap=episode.recap,
        started_at=episode.started_at,
        finished_at=episode.finished_at,
        video=video,
    )


def summary_view(
    series: VideoDramaSeries,
    docs: list[VideoDramaDoc],
    episodes: list[VideoDramaEpisode],
    *,
    media_usd: float = 0.0,
    clip_seconds: int = 0,
) -> SeriesSummary:
    latest = latest_docs(docs)
    return SeriesSummary(
        id=series.id,
        slug=series.slug,
        title=series.title,
        premise=series.premise,
        aspects=cast(Any, list(series.aspects or [])),
        tone=cast(Any, series.tone),
        style_preset=cast(Any, series.style_preset),
        target_minutes=series.target_minutes,
        planned_episodes=series.planned_episodes,
        episodes_per_chapter=series.episodes_per_chapter,
        chapters=chapter_count(series.planned_episodes, series.episodes_per_chapter),
        open_ended=series.open_ended,
        status=cast(Any, series.status),
        note=series.note,
        requested_chapter=series.requested_chapter,
        force_next=series.force_next,
        episodes_done=sum(1 for e in episodes if e.status == "done"),
        episodes_started=sum(1 for e in episodes if e.status == "started"),
        episodes_ready=sum(1 for e in episodes if e.status == "ready"),
        docs_pending=sum(1 for doc in latest.values() if doc.status == "review"),
        media_usd=media_usd,
        clip_seconds=clip_seconds,
        created_at=series.created_at,
        updated_at=series.updated_at,
    )


# --- loading ----------------------------------------------------------------------------------


async def _series(session: AsyncSession, slug: str, *, lock: bool = False) -> VideoDramaSeries:
    statement = select(VideoDramaSeries).where(VideoDramaSeries.slug == slug)
    if lock:
        statement = statement.with_for_update()
    row = await session.scalar(statement)
    if row is None:
        raise SeriesRefused(404, "video_series_not_found", "找不到這部作品")
    return row


async def _docs(session: AsyncSession, series: VideoDramaSeries) -> list[VideoDramaDoc]:
    rows = await session.scalars(
        select(VideoDramaDoc)
        .where(VideoDramaDoc.series_id == series.id)
        .order_by(VideoDramaDoc.kind, VideoDramaDoc.chapter_number, VideoDramaDoc.version)
    )
    return list(rows.all())


async def _episodes(session: AsyncSession, series: VideoDramaSeries) -> list[VideoDramaEpisode]:
    rows = await session.scalars(
        select(VideoDramaEpisode)
        .where(VideoDramaEpisode.series_id == series.id)
        .order_by(VideoDramaEpisode.number)
    )
    return list(rows.all())


async def _started_this_month(session: AsyncSession, series: VideoDramaSeries) -> int:
    now = _now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    found = await session.scalar(
        select(func.count())
        .select_from(VideoDramaEpisode)
        .where(VideoDramaEpisode.series_id == series.id, VideoDramaEpisode.started_at >= start)
    )
    return int(found or 0)


async def _spend(session: AsyncSession, episodes: list[VideoDramaEpisode]) -> tuple[float, int]:
    slugs = [episode.slug for episode in episodes if episode.slug]
    if not slugs:
        return 0.0, 0
    spend = await spend_by_slug(session, slugs)
    return (
        round(sum(item.usd for item in spend.values()), 2),
        sum(item.clip_seconds for item in spend.values()),
    )


# --- the owner's side ---------------------------------------------------------------------------


async def create_series(session: AsyncSession, actor: User, payload: SeriesIn) -> SeriesOut:
    taken = await session.scalar(
        select(VideoDramaSeries.id).where(VideoDramaSeries.slug == payload.slug)
    )
    if taken is not None:
        raise SeriesRefused(409, "video_series_slug_taken", f"{payload.slug} 已經是另一部作品")
    now = _now()
    row = VideoDramaSeries(
        id=uuid4(),
        **payload.model_dump(),
        status="setting",
        created_by_user_id=actor.id,
        created_at=now,
        updated_at=now,
    )
    session.add(row)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_created",
            target=f"video-series:{row.slug}",
            metadata_json={
                "planned_episodes": payload.planned_episodes,
                "episodes_per_chapter": payload.episodes_per_chapter,
                "tone": payload.tone,
            },
        )
    )
    await session.commit()
    return await series_view(session, row.slug)


async def list_series(session: AsyncSession) -> list[SeriesSummary]:
    rows = list(
        (
            await session.scalars(
                select(VideoDramaSeries).order_by(VideoDramaSeries.created_at.desc()).limit(50)
            )
        ).all()
    )
    out: list[SeriesSummary] = []
    for series in rows:
        docs = await _docs(session, series)
        episodes = await _episodes(session, series)
        usd, seconds = await _spend(session, episodes)
        out.append(summary_view(series, docs, episodes, media_usd=usd, clip_seconds=seconds))
    return out


async def series_view(session: AsyncSession, slug: str) -> SeriesOut:
    series = await _series(session, slug)
    docs = await _docs(session, series)
    episodes = await _episodes(session, series)
    usd, seconds = await _spend(session, episodes)
    videos = {
        project.slug: project.model_dump(mode="json")
        for project in await list_projects(session, series_slug=series.slug, limit=1000)
    }
    return SeriesOut(
        **summary_view(series, docs, episodes, media_usd=usd, clip_seconds=seconds).model_dump(),
        docs=[doc_view(doc) for doc in latest_docs(docs).values()],
        episodes=[episode_view(episode, videos.get(episode.slug or "")) for episode in episodes],
    )


async def patch_series(
    session: AsyncSession, actor: User, slug: str, payload: SeriesPatch
) -> SeriesOut:
    series = await _series(session, slug, lock=True)
    changes = payload.model_dump(exclude_unset=True)
    if "status" in changes and series.status in ("setting", "outline"):
        raise SeriesRefused(
            409, "video_series_not_planned", "設定集與總綱核准之後，作品才能暫停、繼續或完結"
        )
    episodes = await _episodes(session, series)
    reached = max((e.number for e in episodes if e.status != "planned"), default=0)
    if "planned_episodes" in changes and changes["planned_episodes"] < reached:
        raise SeriesRefused(
            409, "video_series_too_short", f"已經做到第 {reached} 集，集數不能比它少"
        )
    if "episodes_per_chapter" in changes and episodes:
        raise SeriesRefused(409, "video_series_chapters_fixed", "總綱核准之後，每篇集數就固定了")
    for key, value in changes.items():
        setattr(series, key, value)
    series.updated_at = _now()
    if "planned_episodes" in changes and episodes:
        # A longer series: the new episodes exist as planned rows, titled by number.
        known = {episode.number for episode in episodes}
        for number in range(1, series.planned_episodes + 1):
            if number not in known:
                session.add(_new_episode(series, number, f"第 {number} 集", ""))
        for episode in episodes:
            if episode.number > series.planned_episodes and episode.status == "planned":
                await session.delete(episode)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_updated",
            target=f"video-series:{series.slug}",
            metadata_json={"changed": sorted(changes)},
        )
    )
    await session.commit()
    return await series_view(session, slug)


def _new_episode(
    series: VideoDramaSeries, number: int, title: str, logline: str
) -> VideoDramaEpisode:
    now = _now()
    return VideoDramaEpisode(
        id=uuid4(),
        series_id=series.id,
        number=number,
        chapter_number=chapter_of(series, number),
        title=title,
        logline=logline,
        beats={},
        status="planned",
        state_json={},
        created_at=now,
        updated_at=now,
    )


async def _doc(
    session: AsyncSession, series: VideoDramaSeries, kind: str, chapter: int
) -> VideoDramaDoc:
    doc = await session.scalar(
        select(VideoDramaDoc)
        .where(
            VideoDramaDoc.series_id == series.id,
            VideoDramaDoc.kind == kind,
            VideoDramaDoc.chapter_number == chapter,
        )
        .order_by(VideoDramaDoc.version.desc())
        .limit(1)
        .with_for_update()
    )
    if doc is None:
        raise SeriesRefused(404, "video_series_doc_not_found", "這份文件還沒有產生")
    return doc


async def _apply_approval(
    session: AsyncSession, series: VideoDramaSeries, doc: VideoDramaDoc
) -> None:
    """What an approved document changes: the series moves on, the episode table fills in."""
    body = doc.body_json or {}
    if doc.kind == "setting":
        if series.status == "setting":
            series.status = "outline"
    elif doc.kind == "outline":
        rows = episode_rows_from_outline(series, body)
        episodes = {episode.number: episode for episode in await _episodes(session, series)}
        for number, values in rows.items():
            episode = episodes.get(number)
            if episode is None:
                session.add(_new_episode(series, number, values["title"], values["logline"]))
            elif episode.status == "planned":
                episode.title = values["title"]
                episode.logline = values["logline"]
                episode.updated_at = _now()
        if series.status == "outline":
            series.status = "active"
    else:
        beats = beats_from_chapter(body)
        episodes = {episode.number: episode for episode in await _episodes(session, series)}
        first, last = chapter_range(series, doc.chapter_number)
        for number in range(first, last + 1):
            planned = beats.get(number)
            episode = episodes.get(number)
            if episode is None:
                episode = _new_episode(series, number, f"第 {number} 集", "")
                session.add(episode)
            if episode.status not in ("planned", "ready") or planned is None:
                continue
            episode.title = str(planned.get("title") or episode.title)[:200]
            episode.logline = str(planned.get("logline") or episode.logline)
            episode.beats = {key: value for key, value in planned.items() if key != "number"}
            episode.status = "ready"
            episode.updated_at = _now()
        if series.requested_chapter == doc.chapter_number:
            series.requested_chapter = None
    series.updated_at = _now()


async def decide_doc(
    session: AsyncSession,
    actor: User,
    slug: str,
    kind: str,
    chapter: int,
    decision: str,
    note: str | None,
) -> SeriesOut:
    series = await _series(session, slug, lock=True)
    doc = await _doc(session, series, kind, chapter)
    if doc.status != "review":
        raise SeriesRefused(409, "video_series_doc_not_pending", "這份文件不在等你決定")
    text = (note or "").strip()
    if decision == "reject" and not text:
        raise SeriesRefused(422, "video_series_note_required", "退回要寫原因，模型才知道改什麼")
    doc.status = "approved" if decision == "approve" else "rejected"
    doc.note = text or None
    doc.decided_at = _now()
    doc.decided_by_user_id = actor.id
    if decision == "approve":
        await _apply_approval(session, series, doc)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action=f"video_series_doc_{doc.status}",
            target=f"video-series:{series.slug}",
            metadata_json={"kind": kind, "chapter": chapter, "version": doc.version},
        )
    )
    await session.commit()
    return await series_view(session, slug)


async def edit_doc(
    session: AsyncSession,
    actor: User,
    slug: str,
    kind: str,
    chapter: int,
    payload: SeriesDocEditIn,
) -> SeriesOut:
    """The owner's own version of a document: a new version, approved at once when asked."""
    series = await _series(session, slug, lock=True)
    docs = await _docs(session, series)
    latest = latest_docs(docs).get((kind, chapter))
    if latest is None:
        raise SeriesRefused(404, "video_series_doc_not_found", "這份文件還沒有產生")
    body_json = payload.body_json if payload.body_json is not None else latest.body_json
    if payload.approve:
        problem = doc_problem(
            series,
            SeriesDocSubmitIn(
                kind=cast(Any, kind),
                chapter_number=chapter,
                body_md=payload.body_md,
                body_json=body_json or {},
            ),
        )
        if problem:
            raise SeriesRefused(422, "video_series_doc_invalid", problem)
    if latest.status == "review":
        latest.status = "rejected"
        latest.note = latest.note or "站主自己改了一版"
        latest.decided_at = _now()
        latest.decided_by_user_id = actor.id
    doc = VideoDramaDoc(
        id=uuid4(),
        series_id=series.id,
        kind=kind,
        chapter_number=chapter,
        version=latest.version + 1,
        body_md=payload.body_md,
        body_json=body_json or {},
        status="approved" if payload.approve else "review",
        decided_at=_now() if payload.approve else None,
        decided_by_user_id=actor.id if payload.approve else None,
        created_at=_now(),
    )
    session.add(doc)
    if payload.approve:
        await _apply_approval(session, series, doc)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_doc_edited",
            target=f"video-series:{series.slug}",
            metadata_json={"kind": kind, "chapter": chapter, "version": doc.version},
        )
    )
    await session.commit()
    return await series_view(session, slug)


async def edit_episode(
    session: AsyncSession, actor: User, slug: str, number: int, payload: SeriesEpisodeEditIn
) -> SeriesOut:
    series = await _series(session, slug, lock=True)
    episode = await _episode(session, series, number)
    if episode.status not in ("planned", "ready"):
        raise SeriesRefused(409, "video_series_episode_started", "這一集已經開始做，不能再改細綱")
    changes = payload.model_dump(exclude_unset=True)
    for key, value in changes.items():
        if value is not None:
            setattr(episode, key, value)
    episode.updated_at = _now()
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_episode_edited",
            target=f"video-series:{series.slug}",
            metadata_json={"number": number, "changed": sorted(changes)},
        )
    )
    await session.commit()
    return await series_view(session, slug)


async def _episode(
    session: AsyncSession, series: VideoDramaSeries, number: int
) -> VideoDramaEpisode:
    episode = await session.scalar(
        select(VideoDramaEpisode)
        .where(VideoDramaEpisode.series_id == series.id, VideoDramaEpisode.number == number)
        .with_for_update()
    )
    if episode is None:
        raise SeriesRefused(404, "video_series_episode_not_found", f"這部作品沒有第 {number} 集")
    return episode


async def act(session: AsyncSession, actor: User, slug: str, action: str) -> tuple[SeriesOut, str]:
    """The owner pushes the series along: plan the next chapter now, or start the next episode
    without waiting for the previous one."""
    series = await _series(session, slug, lock=True)
    if series.status != "active":
        raise SeriesRefused(409, "video_series_not_active", "作品要在進行中才能推進")
    docs = await _docs(session, series)
    latest = latest_docs(docs)
    total = chapter_count(series.planned_episodes, series.episodes_per_chapter)
    if action == "plan-next-chapter":
        pending = [
            chapter
            for chapter in range(1, total + 1)
            if (doc := latest.get(("chapter", chapter))) is None or doc.status != "approved"
        ]
        if not pending:
            raise SeriesRefused(409, "video_series_all_planned", "每一篇都已經規劃過了")
        series.requested_chapter = pending[0]
        detail = f"第 {pending[0]} 篇的細綱會在工人的下一輪產生"
    else:
        series.force_next = True
        detail = "工人的下一輪會開始下一集，不等上一集上架"
    series.updated_at = _now()
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_action",
            target=f"video-series:{series.slug}",
            metadata_json={"action": action},
        )
    )
    await session.commit()
    return await series_view(session, slug), detail


async def skip_episode(session: AsyncSession, actor: User, slug: str, number: int) -> SeriesOut:
    series = await _series(session, slug, lock=True)
    episode = await _episode(session, series, number)
    if episode.status not in ("planned", "ready"):
        raise SeriesRefused(409, "video_series_episode_started", "這一集已經開始做，不能跳過")
    episode.status = "skipped"
    episode.updated_at = _now()
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_series_episode_skipped",
            target=f"video-series:{series.slug}",
            metadata_json={"number": number},
        )
    )
    await session.commit()
    return await series_view(session, slug)


# --- the worker's side ----------------------------------------------------------------------------


async def context_view(
    session: AsyncSession, series: VideoDramaSeries, episode_number: int | None
) -> SeriesContextOut:
    docs = await _docs(session, series)
    episodes = await _episodes(session, series)
    chapter = chapter_of(series, episode_number) if episode_number else None
    episode = next((e for e in episodes if e.number == episode_number), None)
    setting = approved_doc(docs, "setting")
    done = [e for e in episodes if e.status == "done" and e.recap]
    recaps = [
        {"number": e.number, "title": e.title, "recap": e.recap, "state": e.state_json or {}}
        for e in done[-RECENT_RECAPS:]
    ]
    mysteries = (setting.body_json or {}).get("mysteries") if setting else None
    return SeriesContextOut(
        series=summary_view(series, docs, episodes),
        setting=doc_view(setting) if setting else None,
        outline=(doc_view(found) if (found := approved_doc(docs, "outline")) else None),
        chapter=(
            doc_view(found)
            if chapter and (found := approved_doc(docs, "chapter", chapter))
            else None
        ),
        chapter_number=chapter,
        chapter_range=chapter_range(series, chapter) if chapter else None,
        episode=episode_view(episode) if episode else None,
        episodes=[episode_view(e) for e in episodes],
        recaps=cast(list[dict[str, object]], recaps),
        mysteries=cast(list[dict[str, object]], mysteries if isinstance(mysteries, list) else []),
    )


async def next_job(session: AsyncSession, settings: VideoAutomationSettings) -> SeriesJobOut:
    """The next document to plan or episode to start across every series, oldest series first."""
    rows = list(
        (
            await session.scalars(
                select(VideoDramaSeries)
                .where(VideoDramaSeries.status.in_(ACTIVE_STATUSES))
                .order_by(VideoDramaSeries.created_at)
            )
        ).all()
    )
    for series in rows:
        docs = await _docs(session, series)
        episodes = await _episodes(session, series)
        job = next_job_for(
            series,
            docs,
            episodes,
            settings,
            started_this_month=await _started_this_month(session, series),
        )
        if job is None:
            continue
        episode = (
            next((e for e in episodes if e.number == job.episode_number), None)
            if job.episode_number
            else None
        )
        chapter_for_context = job.chapter_number if job.kind == "chapter" else None
        context = await context_view(
            session,
            series,
            job.episode_number
            or (chapter_range(series, chapter_for_context)[0] if chapter_for_context else None),
        )
        return SeriesJobOut(
            job=SeriesJob(
                kind=cast(Any, job.kind),
                series=summary_view(series, docs, episodes),
                chapter_number=job.chapter_number if job.kind == "chapter" else None,
                episode=episode_view(episode) if episode else None,
                previous=doc_view(job.previous) if job.previous else None,
                rewrites_left=job.rewrites_left,
                context=context,
            )
        )
    return SeriesJobOut(job=None)


async def submit_doc(session: AsyncSession, slug: str, payload: SeriesDocSubmitIn) -> SeriesDocOut:
    """The worker files a planned document as a new version that waits for the owner."""
    series = await _series(session, slug, lock=True)
    problem = doc_problem(series, payload)
    if problem:
        raise SeriesRefused(422, "video_series_doc_invalid", problem)
    docs = await _docs(session, series)
    latest = latest_docs(docs).get((payload.kind, payload.chapter_number))
    if latest is not None and latest.status in ("review", "approved"):
        raise SeriesRefused(
            409, "video_series_doc_not_wanted", "這份文件已經在等站主或已核准，不能再送一版"
        )
    doc = VideoDramaDoc(
        id=uuid4(),
        series_id=series.id,
        kind=payload.kind,
        chapter_number=payload.chapter_number,
        version=(latest.version + 1) if latest else 1,
        body_md=payload.body_md,
        body_json=payload.body_json,
        status="review",
        created_at=_now(),
    )
    session.add(doc)
    series.updated_at = _now()
    await session.commit()
    return doc_view(doc)


async def start_episode(
    session: AsyncSession, token: VideoToolToken, slug: str, number: int, video_slug: str
) -> SeriesEpisodeStartOut:
    """The worker starts an episode: a request row is filed as started under the video's slug,
    so the episode travels through the same path as a one-off request."""
    series = await _series(session, slug, lock=True)
    episode = await _episode(session, series, number)
    if episode.status != "ready":
        raise SeriesRefused(409, "video_series_episode_not_ready", "這一集的篇章細綱還沒核准")
    taken = await session.scalar(
        select(VideoDramaRequest.id).where(VideoDramaRequest.slug == video_slug)
    )
    if taken is not None:
        raise SeriesRefused(409, "video_drama_request_slug_taken", f"{video_slug} 已經是另一支影片")
    now = _now()
    beats = episode.beats or {}
    premise = "\n".join(
        part
        for part in (
            f"{series.title} 第 {number} 集：{episode.title}",
            episode.logline,
            *(f"{key}: {beats[key]}" for key in BEAT_FIELDS if isinstance(beats.get(key), str)),
        )
        if part
    )[:4000]
    request = VideoDramaRequest(
        id=uuid4(),
        premise=premise or episode.title,
        title=f"{series.title} 第 {number} 集 {episode.title}"[:200],
        style_preset=series.style_preset,
        target_minutes=series.target_minutes,
        note=series.note,
        status="started",
        slug=video_slug,
        series_id=series.id,
        episode_number=number,
        started_by_token_id=token.id,
        created_at=now,
        updated_at=now,
        started_at=now,
    )
    session.add(request)
    # The episode points at the request, and nothing tells the unit of work which of the two
    # to write first: flush the request before the episode carries its id.
    await session.flush()
    episode.status = "started"
    episode.slug = video_slug
    episode.request_id = request.id
    episode.started_at = now
    episode.updated_at = now
    series.force_next = False
    series.updated_at = now
    project = await session.scalar(select(VideoProject).where(VideoProject.slug == video_slug))
    if project is not None:
        project.series_slug = series.slug
        project.episode_number = number
    await session.commit()
    return SeriesEpisodeStartOut(
        request=request_view(request),
        episode=episode_view(episode),
        context=await context_view(session, series, number),
    )


async def recap_episode(
    session: AsyncSession, slug: str, number: int, payload: SeriesEpisodeRecapIn
) -> SeriesEpisodeOut:
    series = await _series(session, slug, lock=True)
    episode = await _episode(session, series, number)
    if episode.status not in ("started", "done"):
        raise SeriesRefused(409, "video_series_episode_not_started", "這一集還沒開始做")
    episode.recap = payload.recap
    episode.state_json = payload.state
    episode.updated_at = _now()
    await session.commit()
    return episode_view(episode)


async def finish_episode(session: AsyncSession, slug: str, number: int) -> SeriesEpisodeOut:
    """The worker reports the episode is cleared for upload: the next one may start."""
    series = await _series(session, slug, lock=True)
    episode = await _episode(session, series, number)
    if episode.status != "started":
        raise SeriesRefused(409, "video_series_episode_not_started", "這一集還沒開始做")
    now = _now()
    episode.status = "done"
    episode.finished_at = now
    episode.updated_at = now
    if episode.request_id is not None:
        request = await session.get(VideoDramaRequest, episode.request_id)
        if request is not None and request.status == "started":
            request.status = "done"
            request.finished_at = now
            request.updated_at = now
    episodes = await _episodes(session, series)
    if all(e.status in ("done", "skipped") for e in episodes) and len(episodes) >= (
        series.planned_episodes
    ):
        series.status = "finished"
    series.updated_at = now
    await session.commit()
    return episode_view(episode)


def month_days(now: datetime | None = None) -> int:
    """How many days this month has; the tab shows the month's episode pace against the cap."""
    when = now or _now()
    return calendar.monthrange(when.year, when.month)[1]
