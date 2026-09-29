"""Preloaded review documents stay consistent through approval, editing and discussion."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.db import SessionFactory
from app.models import User, VideoToolToken
from app.video_automation import messages
from app.video_automation import series as service
from app.video_automation.models import VideoDramaDoc, VideoDramaEpisode, VideoDramaMessage
from app.video_automation.schemas import (
    MessageAnswerIn,
    RevisedDocIn,
    SeriesDocEditIn,
    SeriesDocSubmitIn,
)
from tests.test_video_series import _doc, _series, _settings, clean_series, integration
from tests.test_video_story import db

__all__ = ["clean_series", "db"]


def _body(kind: str, chapter: int = 0) -> dict[str, Any]:
    if kind in ("setting", "bible"):
        return {
            "characters": [{"id": "lead", "name": "原名", "appearance": "red coat"}],
            "mysteries": [{"id": "letter", "secret": "only the lead knows"}],
            "acts": [{"number": 1}],
            "outline": {"title": "一個故事", "logline": "完整結局"},
        }
    if kind == "outline":
        return {
            "chapters": [{"episodes": [{"number": n, "title": f"第{n}集"}]} for n in range(1, 5)]
        }
    return {
        "episodes": [
            {
                "number": chapter,
                "title": f"第{chapter}集",
                **dict.fromkeys(service.BEAT_FIELDS, "beat"),
            }
        ]
    }


class Documents:
    """Actual ORM rows and service mutations; only SQL transport is replaced."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch, *, one_off: bool = False):
        self.series = _series(
            status="setting",
            planned_episodes=1 if one_off else 4,
            episodes_per_chapter=1,
            kind="one-off" if one_off else "series",
            hands_off=False,
        )
        keys = (
            [("bible", 0)]
            if one_off
            else [("setting", 0), ("outline", 0)] + [("chapter", n) for n in range(1, 5)]
        )
        self.docs = [_doc(kind, chapter, status="review") for kind, chapter in keys]
        for doc in self.docs:
            doc.series_id = self.series.id
            doc.body_json = _body(doc.kind, doc.chapter_number)
        self.episodes: list[VideoDramaEpisode] = []
        self.owner = User(id=uuid4())
        self.session = MagicMock(commit=AsyncMock(), scalar=AsyncMock(return_value=None))
        self.session.add.side_effect = self.add
        monkeypatch.setattr(service, "_series", AsyncMock(return_value=self.series))
        monkeypatch.setattr(service, "_docs", AsyncMock(side_effect=lambda *_: self.docs.copy()))
        monkeypatch.setattr(
            service, "_episodes", AsyncMock(side_effect=lambda *_: self.episodes.copy())
        )
        monkeypatch.setattr(
            service, "_doc", AsyncMock(side_effect=lambda _s, _r, k, c: self.latest(k, c))
        )
        monkeypatch.setattr(
            service, "_episode", AsyncMock(side_effect=lambda _s, _r, n: self.episode(n))
        )
        monkeypatch.setattr(service, "series_view", AsyncMock(return_value=None))

    def add(self, row: Any) -> None:
        if isinstance(row, VideoDramaDoc):
            self.docs.append(row)
        elif isinstance(row, VideoDramaEpisode):
            self.episodes.append(row)

    def latest(self, kind: str, chapter: int = 0) -> VideoDramaDoc:
        return service.latest_docs(self.docs)[kind, chapter]

    def episode(self, number: int) -> VideoDramaEpisode:
        return next(e for e in self.episodes if e.number == number)

    async def decide(self, kind: str, chapter: int = 0, decision: str = "approve") -> None:
        await service.decide_doc(
            self.session,
            self.owner,
            self.series.slug,
            kind,
            chapter,
            decision,
            "修改" if decision == "reject" else None,
            expected_version=self.latest(kind, chapter).version,
        )

    async def approve_all(self) -> None:
        for kind, chapter in list(service.latest_docs(self.docs)):
            await self.decide(kind, chapter)

    def next(self) -> service.NextJob | None:
        return service.next_job_for(
            self.series, self.docs, self.episodes, _settings(), started_this_month=0
        )

    async def edit(
        self, kind: str, chapter: int = 0, *, paired: bool = True, approve: bool = False
    ) -> None:
        await service.edit_doc(
            self.session,
            self.owner,
            self.series.slug,
            kind,
            chapter,
            SeriesDocEditIn(
                body_md="# 新版本",
                body_json=_body(kind, chapter) if paired else None,
                approve=approve,
            ),
        )


@pytest.mark.asyncio
async def test_six_preloaded_documents_require_current_parents_and_approve_in_order(monkeypatch):
    store = Documents(monkeypatch)
    for kind, chapter in [("outline", 0), ("chapter", 1), ("chapter", 4)]:
        with pytest.raises(service.SeriesRefused, match="最新版本") as refused:
            await store.decide(kind, chapter)
        assert refused.value.code == "video_series_doc_prerequisite"
        assert store.latest(kind, chapter).status == "review"
    assert store.series.status == "setting" and store.episodes == [] and store.next() is None
    await store.decide("setting")
    await store.decide("outline")
    with pytest.raises(service.SeriesRefused):
        await store.decide("chapter", 2)
    await store.decide("chapter", 1)
    assert store.series.status == "active"
    assert store.episode(1).status == "ready"
    assert store.next().episode_number == 1  # Later preloaded chapters do not stop chapter 1.
    for number in range(2, 5):
        await store.decide("chapter", number)
    assert all(e.status == "ready" for e in store.episodes)
    with pytest.raises(service.SeriesRefused) as repeat:
        await store.decide("chapter", 1)
    assert repeat.value.code == "video_series_doc_not_pending"


@pytest.mark.asyncio
async def test_markdown_save_requires_explicit_reconciliation_before_approval(monkeypatch):
    store = Documents(monkeypatch)
    with pytest.raises(service.SeriesRefused) as refused:
        await store.edit("setting", paired=False, approve=True)
    assert refused.value.code == "video_series_structured_data_required"
    assert store.latest("setting").version == 1
    await store.edit("setting", paired=False)
    draft = store.latest("setting")
    assert draft.body_json == {} and draft.status == "review"
    assert service.doc_view(draft).needs_reconciliation
    with pytest.raises(service.SeriesRefused) as refused:
        await store.decide("setting")
    assert refused.value.code == "video_series_structured_data_required"
    # The existing, explicitly requested discussion produces both representations.
    revised = await messages._revise_doc(
        store.session, store.series, "setting", "# 新版本", _body("setting")
    )
    assert revised is not None and not service.doc_view(revised).needs_reconciliation
    assert revised.status == "review" and store.series.status == "setting"
    await store.decide("setting")
    assert store.series.status == "outline"


@pytest.mark.parametrize("decision", ["approve", "reject"])
async def test_owner_cannot_decide_a_newer_document_than_the_version_they_read(
    monkeypatch, decision
):
    store = Documents(monkeypatch)
    await store.edit("setting")
    current = store.latest("setting")
    assert current.version == 2 and current.status == "review"
    commits = store.session.commit.await_count
    with pytest.raises(service.SeriesRefused) as stale:
        await service.decide_doc(
            store.session,
            store.owner,
            store.series.slug,
            "setting",
            0,
            decision,
            "需修改" if decision == "reject" else None,
            expected_version=1,
        )
    assert stale.value.code == "video_series_doc_stale" and stale.value.status == 409
    assert current.status == "review" and current.decided_at is None
    assert store.session.commit.await_count == commits
    await store.decide("setting", decision=decision)
    assert current.status == ("approved" if decision == "approve" else "rejected")


@pytest.mark.asyncio
@pytest.mark.parametrize("kind,chapter", [("setting", 0), ("outline", 0), ("chapter", 2)])
async def test_revisions_require_review_of_dependents_without_touching_running_or_done(
    monkeypatch, kind, chapter
):
    store = Documents(monkeypatch)
    await store.approve_all()
    store.episode(1).status = "done"
    store.episode(2).status = "started"
    old_beats = store.episode(2).beats.copy()
    await store.edit(kind, chapter)
    assert store.episode(1).status == "done" and store.episode(2).status == "started"
    assert store.episode(2).beats == old_beats
    assert store.episode(3).status == "planned" and store.episode(3).beats == {}
    assert store.latest("chapter", 3).status == "review"
    assert store.latest("chapter", 3).version == 2
    assert any(
        d.kind == "chapter" and d.chapter_number == 3 and d.version == 1 and d.status == "approved"
        for d in store.docs
    )
    assert store.next() is None
    await store.decide(kind, chapter)
    assert store.episode(3).status == "planned", (
        "parent approval alone cannot revive old child beats"
    )


@pytest.mark.asyncio
async def test_later_revision_does_not_hold_earlier_chapter_and_rejection_cannot_revive_old_ready(
    monkeypatch,
):
    store = Documents(monkeypatch)
    await store.approve_all()
    await store.edit("chapter", 2)
    assert store.episode(1).status == "ready" and store.next().episode_number == 1
    await store.edit("chapter", 1)
    await store.decide("chapter", 1, "reject")
    assert store.episode(1).status == "planned"
    # Simulate an old ready row, and an exhausted rewrite budget: both dispatch and direct
    # start must independently recheck the latest document rather than the old approval.
    store.episode(1).status = "ready"
    store.latest("chapter", 1).version = 20
    assert store.next() is None
    with pytest.raises(service.SeriesRefused) as refused:
        await service.start_episode(
            store.session, VideoToolToken(id=uuid4()), store.series.slug, 1, "probe-e001"
        )
    assert refused.value.code == "video_series_episode_documents"
    store.session.scalar.assert_not_awaited()


@pytest.mark.asyncio
async def test_discussion_reads_latest_draft_parents_while_production_keeps_approved_context(
    monkeypatch,
):
    store = Documents(monkeypatch)
    draft = await service.context_view(store.session, store.series, 1, discussion=True)
    assert draft.setting.status == "review" and draft.outline.status == "review"
    assert draft.setting.version == 1 and draft.mysteries[0]["id"] == "letter"
    assert (await service.context_view(store.session, store.series, 1)).setting is None
    await store.decide("setting")
    await store.edit("setting", paired=False)
    draft = await service.context_view(store.session, store.series, 1, discussion=True)
    assert draft.setting.version == 2 and draft.setting.needs_reconciliation
    production = await service.context_view(store.session, store.series, 1)
    assert production.setting.version == 1 and production.setting.status == "approved"
    store.docs = [d for d in store.docs if d.kind != "outline"]
    assert (
        await service.context_view(store.session, store.series, 1, discussion=True)
    ).outline is None


@pytest.mark.asyncio
async def test_worker_auto_approval_cannot_skip_preloaded_parents(monkeypatch):
    store = Documents(monkeypatch)
    store.latest("chapter", 1).status = "rejected"
    store.series.hands_off = True
    monkeypatch.setattr(service, "auto_doc_status", lambda *_: ("approved", None))
    with pytest.raises(service.SeriesRefused) as refused:
        await service.submit_doc(
            store.session,
            store.series.slug,
            SeriesDocSubmitIn(
                kind="chapter", chapter_number=1, body_md="# new", body_json=_body("chapter", 1)
            ),
        )
    assert refused.value.code == "video_series_doc_prerequisite"
    assert store.latest("chapter", 1).version == 1


@pytest.mark.asyncio
async def test_reopened_dependency_does_not_spend_a_model_rewrite(monkeypatch):
    store = Documents(monkeypatch)
    await store.approve_all()
    await store.edit("setting", approve=True)
    await store.decide("outline", decision="reject")
    job = store.next()
    assert job is not None and job.kind == "outline" and job.rewrites_left == 2


@pytest.mark.asyncio
async def test_one_off_reconciles_bible_and_story_still_has_no_document_requirement(monkeypatch):
    store = Documents(monkeypatch, one_off=True)
    await store.approve_all()
    assert store.next().episode_number == 1
    await store.edit("bible", paired=False)
    assert store.episode(1).status == "planned" and store.next() is None
    assert service.episode_document_problem(_series(kind="story"), [], 1) is None


def test_old_out_of_order_approved_parents_do_not_strand_a_series_in_outline():
    row = _series(status="outline")
    docs = [_doc("setting"), _doc("outline"), _doc("chapter", 1, status="review")]
    assert service.next_job_for(row, docs, [], _settings(), started_this_month=0) is None
    docs[-1].status = "rejected"
    job = service.next_job_for(row, docs, [], _settings(), started_this_month=0)
    assert job is not None and job.kind == "chapter"


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_preloaded_approvals_and_revision_invalidation_commit_together(clean_series: str):
    await _committed_lifecycle(SessionFactory, clean_series)


async def test_preloaded_lifecycle_on_sqlite(db):
    await _committed_lifecycle(db, "preloaded-lifecycle")


@pytest.mark.parametrize(
    "change", ["none", "target", "parent-version", "parent-status", "approved", "missing-binding"]
)
async def test_discussion_answer_only_revises_the_exact_delivered_document_snapshot(
    monkeypatch, change
):
    store = Documents(monkeypatch)
    question = VideoDramaMessage(
        id=uuid4(),
        series_id=store.series.id,
        subject="chapter:1",
        author="owner",
        body_md="請同步我的修改",
        refers_to="v1",
        created_at=store.series.created_at,
    )
    # The queued request predates v2: the worker must bind what it actually reads now.
    await store.edit("chapter", 1, paired=False)
    store.session.scalar.return_value = question
    store.session.get = AsyncMock(return_value=store.series)
    monkeypatch.setattr(messages, "_thread", AsyncMock(return_value=[question]))
    monkeypatch.setattr(service, "_series_by_id", AsyncMock(return_value=store.series))
    job = (await messages.next_message(store.session)).job
    assert job is not None and job.doc is not None and job.doc.version == 2
    assert job.revision_context and job.message.refers_to == "v1"
    assert store.session.get.await_args.kwargs["with_for_update"] is True
    if change == "target":
        await service.edit_doc(
            store.session,
            store.owner,
            store.series.slug,
            "chapter",
            1,
            SeriesDocEditIn(body_md="# 最新文字"),
        )
    elif change == "parent-version":
        await store.edit("setting")
    elif change == "parent-status":
        store.latest("setting").status = "rejected"
    elif change == "approved":
        store.latest("chapter", 1).status = "approved"
    current = store.latest("chapter", 1)
    before = (len(store.docs), current.id, current.status, current.body_md, current.body_json)
    answer = await messages.answer_message(
        store.session,
        question.id,
        MessageAnswerIn(
            reply_md="修改完成",
            revised=RevisedDocIn(body_md="# AI version", body_json=_body("chapter", 1)),
            revision_context=None if change == "missing-binding" else job.revision_context,
        ),
    )
    assert question.answered_at is not None
    if change == "none":
        assert answer.revision is not None and answer.revision.version == 3
        assert answer.revision.status == "review" and answer.revision_refused is None
        assert answer.reply.refers_to == "v3"
    else:
        current = store.latest("chapter", 1)
        assert (
            len(store.docs),
            current.id,
            current.status,
            current.body_md,
            current.body_json,
        ) == before
        assert answer.revision is None and answer.revision_refused
        assert "未套用新版本" in answer.reply.body_md and answer.reply.refers_to is None


async def _committed_lifecycle(factory, slug):
    async with factory() as session:
        owner = User(email=f"doc-lifecycle-{uuid4()}@example.com", password_hash="unused")
        row = _series(slug=slug, status="setting", planned_episodes=4, episodes_per_chapter=1)
        session.add_all([owner, row])
        await session.flush()
        for kind, chapter in [("setting", 0), ("outline", 0)] + [
            ("chapter", n) for n in range(1, 5)
        ]:
            doc = _doc(kind, chapter, status="review")
            doc.series_id = row.id
            doc.body_json = _body(kind, chapter)
            session.add(doc)
        await session.commit()
        with pytest.raises(service.SeriesRefused) as refused:
            await service.decide_doc(
                session, owner, row.slug, "outline", 0, "approve", None, expected_version=1
            )
        assert refused.value.code == "video_series_doc_prerequisite"
        for kind, chapter in [("setting", 0), ("outline", 0)] + [
            ("chapter", n) for n in range(1, 5)
        ]:
            await service.decide_doc(
                session, owner, row.slug, kind, chapter, "approve", None, expected_version=1
            )
        revised = await service.edit_doc(
            session,
            owner,
            row.slug,
            "setting",
            0,
            SeriesDocEditIn(body_md="# Revised setting", body_json=_body("setting"), approve=True),
        )
        assert revised.status == "outline"
        assert all(e.status == "planned" and e.beats == {} for e in revised.episodes)
        latest = service.latest_docs(await service._docs(session, row))
        assert latest["outline", 0].status == "review" and latest["outline", 0].version == 2
        assert latest["chapter", 1].status == "review" and latest["chapter", 1].version == 2
        assert (
            service.next_job_for(
                row,
                list(latest.values()),
                await service._episodes(session, row),
                _settings(),
                started_this_month=0,
            )
            is None
        )
