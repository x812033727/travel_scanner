"""The discussion thread on every series document and every screenplay: the subjects, who may
write and when, what the worker gets to answer, and what an answer files."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import delete, select

from app.auth.service import current_user
from app.db import SessionFactory, engine, get_session
from app.models import AdminAuditLog, User, VideoReview, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api
from app.video_automation import messages as service
from app.video_automation import series as series_service
from app.video_automation import settings as settings_service
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.schemas import (
    DramaRequestIn,
    MessageAnswerIn,
    MessageIn,
    RevisedDocIn,
    SeriesDocSubmitIn,
)
from app.video_speech import admin_api as speech_api

WHEN = datetime(2026, 9, 27, 1, 0, tzinfo=UTC)
BIBLE: dict[str, Any] = {
    "characters": [{"id": "jingwei", "name": "精衛", "appearance": "x"}],
    "acts": [{"number": 1, "title": "溺水"}],
    "outline": {"title": "精衛填海", "logline": "一隻鳥要填平東海"},
}


def _series(**changes: Any) -> VideoDramaSeries:
    values: dict[str, Any] = {
        "id": uuid4(),
        "slug": "xianxia",
        "kind": "series",
        "title": "問劍",
        "premise": "兩個少年",
        "aspects": [],
        "tone": "dual-male-leads-subtext",
        "style_preset": "cinematic-3d",
        "target_minutes": 3,
        "planned_episodes": 25,
        "episodes_per_chapter": 10,
        "open_ended": True,
        "status": "active",
        "requested_chapter": None,
        "force_next": False,
        "created_at": WHEN,
        "updated_at": WHEN,
    }
    values.update(changes)
    return VideoDramaSeries(**values)


def _one_off() -> VideoDramaSeries:
    return _series(
        slug="one-off-1a2b3c4d",
        kind="one-off",
        planned_episodes=1,
        episodes_per_chapter=1,
        status="setting",
    )


def _doc(
    kind: str, version: int = 1, status: str = "review", note: str | None = None
) -> VideoDramaDoc:
    return VideoDramaDoc(
        id=uuid4(),
        kind=kind,
        chapter_number=0,
        version=version,
        body_md="# doc",
        body_json={},
        status=status,
        note=note,
        created_at=WHEN + timedelta(minutes=version),
    )


def _message(subject: str, author: str = "owner", answered: bool = False) -> VideoDramaMessage:
    return VideoDramaMessage(
        id=uuid4(),
        series_id=uuid4(),
        subject=subject,
        author=author,
        body_md="第二幕為什麼要死一個人",
        refers_to="v1",
        answered_at=WHEN if answered else None,
        created_at=WHEN,
        created_by_user_id=uuid4(),
    )


def test_a_subject_names_a_document_or_an_episode_s_screenplay() -> None:
    assert service.parse_subject("setting") == ("setting", 0)
    assert service.parse_subject("bible") == ("bible", 0)
    assert service.parse_subject("chapter:3") == ("chapter", 3)
    assert service.parse_subject("script:12") == ("script", 12)
    for bad in ("chapter", "script:", "boss", "setting:1", "chapter:x"):
        with pytest.raises(ValueError):
            service.parse_subject(bad)
        with pytest.raises(ValidationError):
            MessageIn(subject=bad, body="x")
    assert MessageIn(subject="script:1", body="  改  ").body == "改"
    with pytest.raises(ValidationError):
        MessageIn(subject="setting", body="   ")
    with pytest.raises(ValidationError):
        MessageIn(subject="setting", body="x" * 8001)
    assert (
        service.author_for("script:2") == "writer" and service.author_for("chapter:2") == "planner"
    )
    assert service.sha_ref("a" * 64) == "a" * 12 and service.sha_ref(None) is None
    assert service.version_ref(_doc("setting", version=3)) == "v3"
    assert service.version_ref(None) is None


def test_a_series_has_the_threads_of_its_documents_and_episodes_a_one_off_its_bible() -> None:
    series = _series()
    for subject in ("setting", "outline", "chapter:1", "chapter:3", "script:1", "script:25"):
        assert service.subject_problem(series, subject) is None, subject
    assert "第 4 篇" in str(service.subject_problem(series, "chapter:4"))
    assert "第 26 集" in str(service.subject_problem(series, "script:26"))
    assert "故事聖經" in str(service.subject_problem(series, "bible"))
    one_off = _one_off()
    assert service.subject_problem(one_off, "bible") is None
    assert service.subject_problem(one_off, "script:1") is None
    assert "故事聖經" in str(service.subject_problem(one_off, "setting"))
    assert "第 2 集" in str(service.subject_problem(one_off, "script:2"))
    assert service.subject_problem(series, "boss") == "沒有這種討論串"


def test_a_discussion_s_new_version_is_not_one_of_the_owner_s_rewrites() -> None:
    """v1 was replaced by the discussion, v2 sent back by the owner: one rewrite is used."""
    series = _series(status="setting")
    settings = VideoAutomationSettings(series_doc_rewrites=2)
    discussed = _doc("setting", 1, "rejected", series_service.DISCUSSION_NOTE)
    sent_back = _doc("setting", 2, "rejected", "再暗一點")
    job = series_service.next_job_for(
        series, [discussed, sent_back], [], settings, started_this_month=0
    )
    assert job is not None and job.kind == "setting" and job.rewrites_left == 2
    twice = _doc("setting", 3, "rejected", "還是不夠")
    job = series_service.next_job_for(
        series, [discussed, sent_back, twice], [], settings, started_this_month=0
    )
    assert job is not None and job.rewrites_left == 1
    thrice = _doc("setting", 4, "rejected", "算了")
    assert (
        series_service.next_job_for(
            series, [discussed, sent_back, twice, thrice], [], settings, started_this_month=0
        )
        is None
    )


def _session(**answers: Any) -> AsyncMock:
    session = AsyncMock()
    session.add = MagicMock()
    for name, value in answers.items():
        setattr(session, name, value)
    return session


def _wire(
    monkeypatch: pytest.MonkeyPatch,
    series: VideoDramaSeries,
    *,
    docs: list[VideoDramaDoc] | None = None,
    episodes: list[VideoDramaEpisode] | None = None,
    thread: list[VideoDramaMessage] | None = None,
    review: VideoReview | None = None,
) -> None:
    monkeypatch.setattr(series_service, "_series", AsyncMock(return_value=series))
    monkeypatch.setattr(series_service, "_series_by_id", AsyncMock(return_value=series))
    monkeypatch.setattr(series_service, "_docs", AsyncMock(return_value=list(docs or [])))
    monkeypatch.setattr(series_service, "_episodes", AsyncMock(return_value=list(episodes or [])))
    monkeypatch.setattr(service, "_thread", AsyncMock(return_value=list(thread or [])))
    monkeypatch.setattr(service, "_script_review", AsyncMock(return_value=review))


def _episode(number: int, slug: str | None) -> VideoDramaEpisode:
    return VideoDramaEpisode(
        id=uuid4(),
        number=number,
        chapter_number=1,
        title=f"第 {number} 集",
        logline="",
        beats={},
        status="started" if slug else "ready",
        slug=slug,
        state_json={},
        created_at=WHEN,
        updated_at=WHEN,
    )


def _owner() -> User:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    return owner


@pytest.mark.asyncio
async def test_the_owner_writes_on_a_thread_until_its_document_is_approved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = _owner()
    series = _series(status="setting")
    _wire(monkeypatch, series, docs=[_doc("setting", 2, "review")])
    session = _session()
    posted = await service.post_message(
        session, owner, "xianxia", MessageIn(subject="setting", body="第二幕？")
    )
    assert (posted.author, posted.subject, posted.refers_to, posted.answered_at) == (
        "owner",
        "setting",
        "v2",
        None,
    )
    row, audit = (call.args[0] for call in session.add.call_args_list)
    assert isinstance(row, VideoDramaMessage) and row.series_id == series.id
    assert row.created_by_user_id == owner.id and row.body_md == "第二幕？"
    assert isinstance(audit, AdminAuditLog) and audit.action == "video_drama_message_posted"
    assert audit.metadata_json == {"subject": "setting", "refers_to": "v2"}
    assert session.commit.await_count == 1

    # Before the first version exists the line is kept without a version to point at.
    _wire(monkeypatch, series, docs=[])
    early = await service.post_message(
        _session(), owner, "xianxia", MessageIn(subject="setting", body="先問")
    )
    assert early.refers_to is None

    _wire(monkeypatch, series, docs=[_doc("setting", 2, "approved")])
    with pytest.raises(service.MessageRefused) as approved:
        await service.post_message(
            _session(), owner, "xianxia", MessageIn(subject="setting", body="x")
        )
    assert (approved.value.status, approved.value.code) == (409, "video_drama_doc_approved")
    with pytest.raises(service.MessageRefused) as unknown:
        await service.post_message(
            _session(), owner, "xianxia", MessageIn(subject="chapter:9", body="x")
        )
    assert (unknown.value.status, unknown.value.code) == (404, "video_drama_thread_not_found")
    with pytest.raises(service.MessageRefused):
        await service.post_message(
            _session(), owner, "xianxia", MessageIn(subject="bible", body="x")
        )


@pytest.mark.asyncio
async def test_a_screenplay_thread_opens_once_the_episode_started_and_closes_when_its_gate_passed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = _owner()
    series = _series()
    _wire(monkeypatch, series, episodes=[_episode(1, None)])
    with pytest.raises(service.MessageRefused) as not_started:
        await service.post_message(
            _session(), owner, "xianxia", MessageIn(subject="script:1", body="x")
        )
    assert not_started.value.code == "video_drama_script_not_started"

    pending = VideoReview(gate="script", status="pending", content_sha256="b" * 64)
    _wire(monkeypatch, series, episodes=[_episode(1, "xianxia-e001")], review=pending)
    posted = await service.post_message(
        _session(), owner, "xianxia", MessageIn(subject="script:1", body="師兄少講話")
    )
    assert posted.refers_to == "b" * 12

    _wire(monkeypatch, series, episodes=[_episode(1, "xianxia-e001")], review=None)
    early = await service.post_message(
        _session(), owner, "xianxia", MessageIn(subject="script:1", body="x")
    )
    assert early.refers_to is None, "the writer has not sent the screenplay yet"

    approved = VideoReview(gate="script", status="approved", content_sha256="c" * 64)
    _wire(monkeypatch, series, episodes=[_episode(1, "xianxia-e001")], review=approved)
    with pytest.raises(service.MessageRefused) as closed:
        await service.post_message(
            _session(), owner, "xianxia", MessageIn(subject="script:1", body="x")
        )
    assert closed.value.code == "video_drama_script_approved"


@pytest.mark.asyncio
async def test_the_worker_gets_the_oldest_unanswered_line_with_the_thread_and_the_document(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    series = _series(status="setting")
    doc = _doc("setting", 2, "review")
    question = _message("setting")
    question.series_id = series.id
    earlier = _message("setting", "planner", answered=True)
    _wire(monkeypatch, series, docs=[doc], thread=[earlier, question])
    monkeypatch.setattr(
        series_service, "context_view", AsyncMock(return_value=MagicMock(name="context"))
    )
    session = _session(scalar=AsyncMock(return_value=question), get=AsyncMock(return_value=series))
    with monkeypatch.context() as patched:
        # The job's context is pydantic-validated; hand it a real one built from the mocks.
        patched.setattr(series_service, "context_view", AsyncMock(side_effect=_context))
        job = (await service.next_message(session)).job
    assert job is not None and job.message.id == question.id and job.target == "doc"
    assert job.subject == "setting" and job.doc is not None and job.doc.version == 2
    assert [m.author for m in job.thread] == ["planner", "owner"] and job.episode is None
    assert job.series.slug == "xianxia"
    statement = str(session.scalar.await_args.args[0]).lower()
    assert "answered_at is null" in statement and "author" in statement

    nothing = _session(scalar=AsyncMock(return_value=None))
    assert (await service.next_message(nothing)).job is None

    # A screenplay thread names the episode, whose slug is the video the worker rewrites.
    line = _message("script:1")
    line.series_id = series.id
    _wire(monkeypatch, series, episodes=[_episode(1, "xianxia-e001")], thread=[line])
    with monkeypatch.context() as patched:
        patched.setattr(series_service, "context_view", AsyncMock(side_effect=_context))
        job = (
            await service.next_message(
                _session(scalar=AsyncMock(return_value=line), get=AsyncMock(return_value=series))
            )
        ).job
    assert job is not None and job.target == "script" and job.doc is None
    assert job.episode is not None and job.episode.slug == "xianxia-e001"


async def _context(
    session: Any, series: VideoDramaSeries, episode_number: int | None, *, discussion: bool = False
) -> Any:
    docs = await series_service._docs(session, series)  # noqa: SLF001
    episodes = await series_service._episodes(session, series)  # noqa: SLF001
    from app.video_automation.schemas import SeriesContextOut

    return SeriesContextOut(
        series=series_service.summary_view(series, docs, episodes),
        setting=None,
        outline=None,
        chapter=None,
        chapter_number=None,
        chapter_range=None,
        episode=None,
        episodes=[],
        recaps=[],
        mysteries=[],
    )


@pytest.mark.asyncio
async def test_an_answer_files_a_new_version_of_a_document_and_only_a_reply_for_a_screenplay(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    series = _one_off()
    current = _doc("bible", 1, "review")
    question = _message("bible")
    question.series_id = series.id
    _wire(monkeypatch, series, docs=[current])
    session = _session(scalar=AsyncMock(return_value=question))
    answered = await service.answer_message(
        session,
        question.id,
        MessageAnswerIn(
            reply_md="把第二幕改成…",
            revised=RevisedDocIn(body_md="# v2", body_json=BIBLE),
            revision_context=service.discussion_revision_context([current], "bible"),
        ),
    )
    assert answered.revision is not None and answered.revision.version == 2
    assert answered.revision.status == "review" and answered.revision.body_md == "# v2"
    assert (answered.reply.author, answered.reply.refers_to) == ("planner", "v2")
    assert answered.reply.answered_at is not None and question.answered_at is not None
    assert current.status == "rejected" and current.note == series_service.DISCUSSION_NOTE
    added = [call.args[0] for call in session.add.call_args_list]
    assert [type(item).__name__ for item in added] == ["VideoDramaDoc", "VideoDramaMessage"]
    assert session.commit.await_count == 1

    # A bad revision is refused before anything is written.
    fresh = _message("bible")
    invalid_doc = _doc("bible", 1, "review")
    _wire(monkeypatch, series, docs=[invalid_doc])
    with pytest.raises(service.MessageRefused) as invalid:
        await service.answer_message(
            _session(scalar=AsyncMock(return_value=fresh)),
            fresh.id,
            MessageAnswerIn(
                reply_md="x",
                revised=RevisedDocIn(body_md="# x", body_json={}),
                revision_context=service.discussion_revision_context([invalid_doc], "bible"),
            ),
        )
    assert invalid.value.code == "video_series_doc_invalid" and fresh.answered_at is None

    # A question gets a reply and no version; a document approved meanwhile keeps the reply
    # and drops the revision.
    asked = _message("bible")
    _wire(monkeypatch, series, docs=[_doc("bible", 1, "review")])
    plain = await service.answer_message(
        _session(scalar=AsyncMock(return_value=asked)), asked.id, MessageAnswerIn(reply_md="因為…")
    )
    assert plain.revision is None and plain.reply.refers_to == "v1"
    late = _message("bible")
    _wire(monkeypatch, series, docs=[_doc("bible", 1, "approved")])
    kept = await service.answer_message(
        _session(scalar=AsyncMock(return_value=late)),
        late.id,
        MessageAnswerIn(reply_md="太晚了", revised=RevisedDocIn(body_md="# x", body_json=BIBLE)),
    )
    assert kept.revision is None and late.answered_at is not None

    # A screenplay: the writer answers, the revision is the worker's own to write.
    long_series = _series()
    line = _message("script:1")
    review = VideoReview(gate="script", status="pending", content_sha256="d" * 64)
    _wire(monkeypatch, long_series, episodes=[_episode(1, "xianxia-e001")], review=review)
    session = _session(scalar=AsyncMock(return_value=line))
    scripted = await service.answer_message(
        session,
        line.id,
        MessageAnswerIn(reply_md="改好了", revised=RevisedDocIn(body_md="# no", body_json={})),
    )
    assert scripted.revision is None
    assert (scripted.reply.author, scripted.reply.refers_to) == ("writer", "d" * 12)
    assert [type(call.args[0]).__name__ for call in session.add.call_args_list] == [
        "VideoDramaMessage"
    ]

    # Answered once, or not the owner's: refused.
    with pytest.raises(service.MessageRefused) as twice:
        await service.answer_message(
            _session(scalar=AsyncMock(return_value=line)), line.id, MessageAnswerIn(reply_md="x")
        )
    assert twice.value.code == "video_drama_message_answered"
    with pytest.raises(service.MessageRefused) as missing:
        await service.answer_message(
            _session(scalar=AsyncMock(return_value=None)), uuid4(), MessageAnswerIn(reply_md="x")
        )
    assert missing.value.status == 404


def _app(user: User | None = None, token: VideoToolToken | None = None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.tool_router, prefix="/api/v1")
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    if user is not None:
        app.dependency_overrides[current_user] = lambda: user
    if token is not None:
        app.dependency_overrides[speech_api.video_tool] = lambda: token
    return app


def _user(role: str) -> User:
    user = User(id=uuid4(), email=f"{role}@example.com", password_hash="unused")
    user._admin_roles_cache = frozenset({role})  # type: ignore[attr-defined]
    return user


@pytest.mark.asyncio
async def test_a_viewer_reads_a_thread_and_only_a_content_manager_writes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    line = _message("chapter:2")
    monkeypatch.setattr(
        service, "list_messages", AsyncMock(return_value=[service.message_view(line)])
    )
    post = AsyncMock(return_value=service.message_view(line))
    monkeypatch.setattr(service, "post_message", post)
    base = "/api/v1/admin/video-automation/series/xianxia/messages"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("viewer"))), base_url="http://t"
    ) as client:
        read = await client.get(base, params={"subject": "chapter:2"})
        bad_subject = await client.get(base, params={"subject": "boss"})
        no_subject = await client.get(base)
        refused = await client.post(base, json={"subject": "chapter:2", "body": "x"})
    assert read.status_code == 200 and read.json()["messages"][0]["subject"] == "chapter:2"
    assert service.list_messages.await_args.args[1:] == ("xianxia", "chapter:2")  # type: ignore[attr-defined]
    assert bad_subject.status_code == 422 and no_subject.status_code == 422
    assert refused.status_code == 403
    post.assert_not_awaited()
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("owner"))), base_url="http://t"
    ) as client:
        posted = await client.post(base, json={"subject": "chapter:2", "body": " 第二幕？ "})
        invalid = await client.post(base, json={"subject": "chapter:2", "body": ""})
        post.side_effect = service.MessageRefused(409, "video_drama_doc_approved", "已核准")
        closed = await client.post(base, json={"subject": "chapter:2", "body": "x"})
    assert posted.status_code == 201 and posted.json()["author"] == "owner"
    assert post.await_args_list[0].args[3].body == "第二幕？"
    assert invalid.status_code == 422
    assert closed.status_code == 409 and closed.json()["code"] == "video_drama_doc_approved"


@pytest.mark.asyncio
async def test_the_worker_asks_for_the_next_line_and_answers_it_by_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", AsyncMock())
    from app.video_automation.schemas import MessageAnswerOut, MessageJobOut

    monkeypatch.setattr(service, "next_message", AsyncMock(return_value=MessageJobOut(job=None)))
    line = _message("setting")
    answer = AsyncMock(
        return_value=MessageAnswerOut(
            reply=service.message_view(_message("setting", "planner", answered=True)), revision=None
        )
    )
    monkeypatch.setattr(service, "answer_message", answer)
    base = "/api/v1/video/automation/series/messages"
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://t") as client:
        anonymous = await client.get(f"{base}/next")
    assert anonymous.status_code == 401
    async with AsyncClient(
        transport=ASGITransport(app=_app(token=token)), base_url="http://t"
    ) as client:
        nothing = await client.get(f"{base}/next")
        answered = await client.post(
            f"{base}/{line.id}/answer",
            json={"reply_md": "因為…", "revised": {"body_md": "# v2", "body_json": {"a": 1}}},
        )
        bad = await client.post(f"{base}/{line.id}/answer", json={"reply_md": ""})
        answer.side_effect = service.MessageRefused(409, "video_drama_message_answered", "回過了")
        twice = await client.post(f"{base}/{line.id}/answer", json={"reply_md": "x"})
    assert nothing.status_code == 200 and nothing.json() == {"job": None}
    assert answered.status_code == 200 and answered.json()["reply"]["author"] == "planner"
    payload = answer.await_args_list[0].args[2]
    assert payload.revised is not None and payload.revised.body_json == {"a": 1}
    assert answer.await_args_list[0].args[1] == line.id
    assert bad.status_code == 422
    assert twice.status_code == 409 and twice.json()["code"] == "video_drama_message_answered"


integration = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


@pytest_asyncio.fixture(loop_scope="module")
async def clean_one_off() -> AsyncIterator[list[str]]:
    slugs: list[str] = []
    yield slugs
    async with SessionFactory() as session:
        for slug in slugs:
            found = await session.scalar(
                select(VideoDramaSeries).where(VideoDramaSeries.slug == slug)
            )
            if found is not None:
                await session.execute(
                    delete(VideoDramaRequest).where(VideoDramaRequest.series_id == found.id)
                )
                await session.delete(found)
        await session.commit()
    await engine.dispose()


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_a_thread_runs_from_the_owner_s_line_to_a_new_version_and_closes_on_approval(
    clean_one_off: list[str],
) -> None:
    async with SessionFactory() as session:
        owner = User(email=f"thread-{uuid4()}@example.com", password_hash="unused")
        session.add(owner)
        await session.commit()
        filed = await series_service.create_one_off(
            session, owner, DramaRequestIn(premise="精衛填海", title="精衛")
        )
        slug = filed.series_slug or ""
        clean_one_off.append(slug)
        await series_service.submit_doc(
            session, slug, SeriesDocSubmitIn(kind="bible", body_md="# v1", body_json=BIBLE)
        )
        asked = await service.post_message(
            session, owner, slug, MessageIn(subject="bible", body="第二幕為什麼要死一個人")
        )
        assert asked.refers_to == "v1"
        view = await series_service.series_view(session, slug)
        assert view.messages_pending == 1 and view.docs[0].unanswered == 1
        listed = await series_service.list_series(session, kind="one-off")
        assert next(s for s in listed if s.slug == slug).messages_pending == 1

        job = (await service.next_message(session)).job
        assert job is not None and job.message.id == asked.id and job.target == "doc"
        assert job.doc is not None and job.doc.version == 1 and job.series.slug == slug
        assert [m.author for m in job.thread] == ["owner"]
        answered = await service.answer_message(
            session,
            asked.id,
            MessageAnswerIn(
                reply_md="改成受傷",
                revised=RevisedDocIn(body_md="# v2", body_json=BIBLE),
                revision_context=job.revision_context,
            ),
        )
        assert answered.revision is not None and answered.revision.version == 2
        view = await series_service.series_view(session, slug)
        assert view.messages_pending == 0 and view.docs[0].version == 2
        assert view.docs[0].status == "review" and view.docs[0].unanswered == 0
        thread = await service.list_messages(session, slug, "bible")
        assert [(m.author, m.refers_to) for m in thread] == [("owner", "v1"), ("planner", "v2")]
        assert (await service.next_message(session)).job is None or (
            (await service.next_message(session)).job.message.id != asked.id  # type: ignore[union-attr]
        )
        # The replaced version is not one of the owner's rewrites: the budget is untouched.
        settings = await settings_service.settings_row(session)
        sent_back = await series_service.decide_doc(
            session, owner, slug, "bible", 0, "reject", "再緊一點", expected_version=2
        )
        assert sent_back.docs[0].status == "rejected"
        plan = (await series_service.next_job(session, settings)).job
        assert plan is not None and plan.kind == "bible"
        assert plan.rewrites_left == settings.series_doc_rewrites
        await series_service.submit_doc(
            session, slug, SeriesDocSubmitIn(kind="bible", body_md="# v3", body_json=BIBLE)
        )
        await series_service.decide_doc(
            session, owner, slug, "bible", 0, "approve", None, expected_version=3
        )
        with pytest.raises(service.MessageRefused, match="已經核准"):
            await service.post_message(session, owner, slug, MessageIn(subject="bible", body="x"))
        with pytest.raises(service.MessageRefused, match="還沒開始寫劇本"):
            await service.post_message(
                session, owner, slug, MessageIn(subject="script:1", body="x")
            )
        assert len(await service.list_messages(session, slug, "bible")) == 2, "the record stays"
        assert await service.list_messages(session, slug, "outline") == []
        await session.delete(owner)
        await session.commit()
