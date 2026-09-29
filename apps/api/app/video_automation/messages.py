"""The discussion thread on every series document and every episode's screenplay.

The owner used to have only "send back with a note": one line, the model rewrites the whole
document, and after two rounds the series stops. Now every document (the setting book, the
outline, a chapter's outline, a one-off's story bible) and every episode's screenplay has a
thread (docs/videos/DRAMA-FLOW.md §三): the owner writes a line, the worker's next round has the
planner (documents) or the writer (screenplays) answer it, and when the owner asked for a change
the answer brings a new version of the document, which waits for the owner like any other. A
screenplay's revision is written by the worker into ``video.json`` and ``script.md``; the API
only keeps the reply.

A thread accepts the owner's lines until its document is approved, or its screenplay's gate is
passed; after that it stays as the record. The router turns ``MessageRefused`` into the API's
problem response; nothing here raises ``AppError``.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoProject, VideoReview
from app.video_automation import series as series_module
from app.video_automation.models import (
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaMessage,
    VideoDramaSeries,
)
from app.video_automation.schemas import (
    MessageAnswerIn,
    MessageAnswerOut,
    MessageIn,
    MessageJob,
    MessageJobOut,
    MessageOut,
    SeriesDocOut,
    SeriesDocSubmitIn,
)

SUBJECT = re.compile(r"^(setting|outline|bible|chapter:(\d+)|script:(\d+))$")
SCRIPT_GATE = "script"
SHA_CHARS = 12


class MessageRefused(Exception):
    """Why the line cannot be posted or answered; the router turns it into the API's error."""

    def __init__(self, status: int, code: str, detail: str):
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail


def _now() -> datetime:
    return datetime.now(UTC)


# --- pure helpers ---------------------------------------------------------------------------


def parse_subject(subject: str) -> tuple[str, int]:
    """``("chapter", n)`` or ``("script", n)`` for the numbered subjects, ``(kind, 0)`` for the
    series' documents; raises ValueError for anything else."""
    match = SUBJECT.match(subject)
    if match is None:
        raise ValueError(f"not a thread subject: {subject}")
    if match.group(2) is not None:
        return "chapter", int(match.group(2))
    if match.group(3) is not None:
        return "script", int(match.group(3))
    return match.group(1), 0


def is_script(subject: str) -> bool:
    return subject.startswith("script:")


def subject_problem(series: VideoDramaSeries, subject: str) -> str | None:
    """Why this series has no such thread: a one-off has a bible and one screenplay, a long
    series a setting book, an outline, its chapters' outlines and its episodes' screenplays."""
    try:
        kind, number = parse_subject(subject)
    except ValueError:
        return "沒有這種討論串"
    one_off = series_module.is_one_off(series)
    if kind == "script":
        if number < 1 or number > series.planned_episodes:
            return f"這部作品沒有第 {number} 集"
        return None
    if one_off:
        return None if kind == "bible" else "單集漫劇只有一份故事聖經"
    if kind == "bible":
        return "作品的文件是設定集、總綱與細綱，沒有故事聖經"
    if kind == "chapter":
        total = series_module.chapter_count(series.planned_episodes, series.episodes_per_chapter)
        if number < 1 or number > total:
            return f"這部作品沒有第 {number} 篇"
    return None


def author_for(subject: str) -> str:
    """Who answers a thread: the writer on a screenplay, the planner on a document."""
    return "writer" if is_script(subject) else "planner"


def version_ref(doc: VideoDramaDoc | None) -> str | None:
    return f"v{doc.version}" if doc is not None else None


def sha_ref(sha256: str | None) -> str | None:
    return sha256[:SHA_CHARS] if sha256 else None


def message_view(row: VideoDramaMessage) -> MessageOut:
    return MessageOut(
        id=row.id,
        subject=row.subject,
        author=cast(Any, row.author),
        body_md=row.body_md,
        refers_to=row.refers_to,
        answered_at=row.answered_at,
        created_at=row.created_at,
        created_by_user_id=row.created_by_user_id,
    )


# --- loading ----------------------------------------------------------------------------------


async def _thread(
    session: AsyncSession, series: VideoDramaSeries, subject: str
) -> list[VideoDramaMessage]:
    rows = await session.scalars(
        select(VideoDramaMessage)
        .where(VideoDramaMessage.series_id == series.id, VideoDramaMessage.subject == subject)
        .order_by(VideoDramaMessage.created_at, VideoDramaMessage.id)
    )
    return list(rows.all())


async def _script_review(
    session: AsyncSession, episode: VideoDramaEpisode | None
) -> VideoReview | None:
    """The newest screenplay review of the episode's video, or None before the writer sent one."""
    if episode is None or not episode.slug:
        return None
    review: VideoReview | None = await session.scalar(
        select(VideoReview)
        .join(VideoProject, VideoProject.id == VideoReview.project_id)
        .where(VideoProject.slug == episode.slug, VideoReview.gate == SCRIPT_GATE)
        .order_by(VideoReview.created_at.desc())
        .limit(1)
    )
    return review


async def _target(
    session: AsyncSession, series: VideoDramaSeries, subject: str
) -> tuple[VideoDramaDoc | None, VideoDramaEpisode | None, VideoReview | None]:
    """What the thread is about: the document's latest version, or the episode and its newest
    screenplay review."""
    kind, number = parse_subject(subject)
    if kind == "script":
        episodes = await series_module._episodes(session, series)  # noqa: SLF001
        episode = next((e for e in episodes if e.number == number), None)
        return None, episode, await _script_review(session, episode)
    docs = await series_module._docs(session, series)  # noqa: SLF001
    return series_module.latest_docs(docs).get((kind, number)), None, None


# --- the owner's side ---------------------------------------------------------------------------


async def list_messages(session: AsyncSession, slug: str, subject: str) -> list[MessageOut]:
    series = await series_module._series(session, slug)  # noqa: SLF001
    if subject_problem(series, subject):
        return []
    return [message_view(row) for row in await _thread(session, series, subject)]


async def post_message(
    session: AsyncSession, actor: User, slug: str, payload: MessageIn
) -> MessageOut:
    """The owner's line on a thread; refused once the document is approved or the screenplay
    gate is passed, since nothing would answer it."""
    series = await series_module._series(session, slug, lock=True)  # noqa: SLF001
    problem = subject_problem(series, payload.subject)
    if problem:
        raise MessageRefused(404, "video_drama_thread_not_found", problem)
    doc, episode, review = await _target(session, series, payload.subject)
    if is_script(payload.subject):
        if episode is None or not episode.slug:
            raise MessageRefused(
                409, "video_drama_script_not_started", "這一集還沒開始寫劇本，等劇本卡片出現再討論"
            )
        if review is not None and review.status == "approved":
            raise MessageRefused(
                409, "video_drama_script_approved", "劇本已經核准，這條討論串只留紀錄"
            )
        refers_to = sha_ref(review.content_sha256 if review else None)
    else:
        if doc is not None and doc.status == "approved":
            raise MessageRefused(
                409, "video_drama_doc_approved", "文件已經核准，這條討論串只留紀錄"
            )
        refers_to = version_ref(doc)
    now = _now()
    row = VideoDramaMessage(
        id=uuid4(),
        series_id=series.id,
        subject=payload.subject,
        author="owner",
        body_md=payload.body,
        refers_to=refers_to,
        created_at=now,
        created_by_user_id=actor.id,
    )
    session.add(row)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_drama_message_posted",
            target=f"video-series:{series.slug}",
            metadata_json={"subject": payload.subject, "refers_to": refers_to},
        )
    )
    series.updated_at = now
    await session.commit()
    return message_view(row)


# --- the worker's side ----------------------------------------------------------------------------


def discussion_revision_context(docs: list[VideoDramaDoc], subject: str) -> str:
    """Bind the answer to the target and parents actually read, including pending statuses."""
    kind, chapter = parse_subject(subject)
    keys = {(kind, chapter)}
    if kind in ("outline", "chapter"):
        keys.add(("setting", 0))
    if kind == "chapter":
        keys.add(("outline", 0))
        if chapter > 1:
            keys.add(("chapter", chapter - 1))
    latest = series_module.latest_docs(docs)
    snapshot = [
        [key, None]
        if (doc := latest.get(key)) is None
        else [
            key,
            str(doc.id),
            doc.version,
            doc.status,
            doc.body_md,
            doc.body_json,
        ]
        for key in sorted(keys)
    ]
    return hashlib.sha256(json.dumps(snapshot, sort_keys=True).encode()).hexdigest()


async def next_message(session: AsyncSession) -> MessageJobOut:
    """The oldest of the owner's lines still waiting for the model, with the thread, the
    document's latest version or the episode, and the series' context; none while every thread
    is answered."""
    row = await session.scalar(
        select(VideoDramaMessage)
        .where(VideoDramaMessage.author == "owner", VideoDramaMessage.answered_at.is_(None))
        .order_by(VideoDramaMessage.created_at, VideoDramaMessage.id)
        .limit(1)
    )
    if row is None:
        return MessageJobOut(job=None)
    # Document edits take the same lock, so the target, parent context and fingerprint
    # belong to one snapshot, even when a queued message predates the latest edit.
    series = await session.get(VideoDramaSeries, row.series_id, with_for_update=True)
    if series is None:
        return MessageJobOut(job=None)
    doc, episode, _review = await _target(session, series, row.subject)
    docs = await series_module._docs(session, series)  # noqa: SLF001
    episodes = await series_module._episodes(session, series)  # noqa: SLF001
    kind, number = parse_subject(row.subject)
    # The context an episode's writer or a chapter's planner would read: the chapter's first
    # episode for a chapter thread, the episode itself for a screenplay.
    for_episode = (
        number
        if kind == "script"
        else (series_module.chapter_range(series, number)[0] if kind == "chapter" else None)
    )
    return MessageJobOut(
        job=MessageJob(
            message=message_view(row),
            thread=[message_view(item) for item in await _thread(session, series, row.subject)],
            series=series_module.summary_view(series, docs, episodes),
            subject=row.subject,
            target="script" if kind == "script" else "doc",
            doc=series_module.doc_view(doc) if doc else None,
            episode=series_module.episode_view(episode) if episode else None,
            context=await series_module.context_view(
                session, series, for_episode, discussion=kind != "script"
            ),
            revision_context=(
                discussion_revision_context(docs, row.subject) if kind != "script" else None
            ),
        )
    )


async def _revise_doc(
    session: AsyncSession,
    series: VideoDramaSeries,
    subject: str,
    body_md: str,
    body_json: dict[str, Any],
) -> VideoDramaDoc | None:
    """The revised document as a new version waiting for the owner; the version it replaces
    is closed with the discussion's note, so it never counts as one of the owner's rewrites.
    None when the document was approved meanwhile: the reply is kept, the revision dropped."""
    kind, chapter = parse_subject(subject)
    docs = await series_module._docs(session, series)  # noqa: SLF001
    latest = series_module.latest_docs(docs).get((kind, chapter))
    if latest is not None and latest.status == "approved":
        return None
    payload = SeriesDocSubmitIn(
        kind=cast(Any, kind), chapter_number=chapter, body_md=body_md, body_json=body_json
    )
    problem = series_module.doc_problem(series, payload)
    if problem:
        raise MessageRefused(422, "video_series_doc_invalid", problem)
    now = _now()
    if latest is not None and latest.status in ("review", "generating"):
        latest.status = "rejected"
        latest.note = series_module.DISCUSSION_NOTE
        latest.decided_at = now
    doc = VideoDramaDoc(
        id=uuid4(),
        series_id=series.id,
        kind=kind,
        chapter_number=chapter,
        version=(latest.version + 1) if latest else 1,
        body_md=body_md,
        body_json=body_json,
        status="review",
        created_at=now,
    )
    await series_module.invalidate_document_dependents(session, series, docs, kind, chapter)
    session.add(doc)
    return doc


async def answer_message(
    session: AsyncSession, message_id: UUID, payload: MessageAnswerIn
) -> MessageAnswerOut:
    """The model's reply to one of the owner's lines, and the document's new version when the
    owner asked for a change; a screenplay's change is the worker's own to write."""
    row = await session.scalar(
        select(VideoDramaMessage).where(VideoDramaMessage.id == message_id).with_for_update()
    )
    if row is None:
        raise MessageRefused(404, "video_drama_message_not_found", "找不到這則訊息")
    if row.author != "owner" or row.answered_at is not None:
        raise MessageRefused(409, "video_drama_message_answered", "這則訊息已經回覆過了")
    series = await series_module._series_by_id(session, row.series_id)  # noqa: SLF001
    now = _now()
    revision: VideoDramaDoc | None = None
    revision_refused: str | None = None
    refers_to = row.refers_to
    if is_script(row.subject):
        _doc, episode, review = await _target(session, series, row.subject)
        refers_to = sha_ref(review.content_sha256 if review else None) or refers_to
    elif payload.revised is not None:
        docs = await series_module._docs(session, series)  # noqa: SLF001
        if payload.revision_context is None:
            revision_refused = "未套用新版本：工人沒有提供文件快照。請更新工人後重新提出修改要求。"
        elif payload.revision_context != discussion_revision_context(docs, row.subject):
            revision_refused = (
                "未套用新版本：文件或上游文件已更新，這則回覆依據舊版本。"
                "請核對最新文件後重新提出修改要求。"
            )
        else:
            revision = await _revise_doc(
                session, series, row.subject, payload.revised.body_md, payload.revised.body_json
            )
            if revision is None:
                revision_refused = "未套用新版本：這份文件已核准。"
        if revision is not None:
            refers_to = version_ref(revision)
        elif revision_refused:
            # Do not label an answer written from an old snapshot as a change to the new draft.
            refers_to = None
    else:
        doc, _episode, _review = await _target(session, series, row.subject)
        refers_to = version_ref(doc) or refers_to
    reply = VideoDramaMessage(
        id=uuid4(),
        series_id=series.id,
        subject=row.subject,
        author=author_for(row.subject),
        body_md=(
            f"{payload.reply_md}\n\n（{revision_refused}）"
            if revision_refused
            else payload.reply_md
        ),
        refers_to=refers_to,
        answered_at=now,
        created_at=now,
    )
    session.add(reply)
    row.answered_at = now
    series.updated_at = now
    await session.commit()
    revised_view: SeriesDocOut | None = (
        series_module.doc_view(revision) if revision is not None else None
    )
    return MessageAnswerOut(
        reply=message_view(reply), revision=revised_view, revision_refused=revision_refused
    )
