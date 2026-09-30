"""/admin/videos: the review file store, the decision rules, and who may call what."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import String, Table

from app.auth.service import current_user
from app.config import Settings
from app.db import get_session
from app.models import VIDEO_CATEGORIES, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation.judge import QA_AUTO_APPROVED_NOTE
from app.video_automation.models import VideoDramaEpisode, VideoDramaRequest, VideoDramaSeries
from app.video_automation.settings import AUTO_APPROVED_STORYBOARD_NOTE
from app.video_reviews import admin_api, admin_service
from app.video_reviews.schemas import (
    VIDEO_CATEGORY_CODES,
    CategoryIn,
    DecisionIn,
    DropIn,
    DubLocalesIn,
    LocalesIn,
    ProjectIn,
    ProjectSummary,
    ReviewIn,
)
from app.video_reviews.storage import PART_BYTES, ReviewStore, StorageRefused
from app.video_speech import admin_api as speech_api


def _store(root: Path, **limits: int) -> ReviewStore:
    return ReviewStore(
        root,
        max_file_bytes=limits.get("max_file_bytes", 50_000_000),
        max_total_bytes=limits.get("max_total_bytes", 100_000_000),
    )


def _parts(data: bytes) -> list[bytes]:
    return [data[start : start + PART_BYTES] for start in range(0, len(data), PART_BYTES)]


def test_parts_arrive_in_any_order_and_the_last_one_assembles_and_verifies(tmp_path: Path) -> None:
    store = _store(tmp_path)
    data = bytes(range(256)) * (PART_BYTES // 256 * 2 + 3)
    sha = hashlib.sha256(data).hexdigest()
    chunks = _parts(data)
    assert len(chunks) == 3
    first = store.put_part("ai-model-choice", sha, index=2, count=3, size=len(data), data=chunks[2])
    assert (first.received, first.complete) == ([2], False)
    assert store.path("ai-model-choice", sha) is None
    store.put_part("ai-model-choice", sha, index=0, count=3, size=len(data), data=chunks[0])
    done = store.put_part("ai-model-choice", sha, index=1, count=3, size=len(data), data=chunks[1])
    assert done.complete
    path = store.path("ai-model-choice", sha)
    assert path is not None and path.read_bytes() == data
    assert not (tmp_path / "ai-model-choice" / ".parts").joinpath(sha).exists()
    again = store.put_part("ai-model-choice", sha, index=0, count=3, size=len(data), data=b"")
    assert again.complete, "a finished file is not uploaded twice"


def test_parts_that_do_not_add_up_to_the_hash_are_thrown_away(tmp_path: Path) -> None:
    store = _store(tmp_path)
    data = b"preview"
    with pytest.raises(StorageRefused) as mismatch:
        store.put_part("v", "0" * 64, index=0, count=1, size=len(data), data=data)
    assert mismatch.value.code == "video_review_hash_mismatch"
    assert store.path("v", "0" * 64) is None
    sha = hashlib.sha256(data).hexdigest()
    with pytest.raises(StorageRefused) as short:
        store.put_part("v", sha, index=0, count=1, size=len(data), data=data[:3])
    assert short.value.code == "video_review_bad_part"
    with pytest.raises(StorageRefused) as count:
        store.put_part("v", sha, index=0, count=2, size=len(data), data=data)
    assert count.value.code == "video_review_bad_part"


def test_names_limits_and_the_total_cap_are_enforced(tmp_path: Path) -> None:
    store = _store(tmp_path, max_file_bytes=1_000_000, max_total_bytes=1_000_010)
    for slug in ("../etc", "UPPER", "a" * 81, ""):
        with pytest.raises(StorageRefused):
            store.put_part(slug, "a" * 64, index=0, count=1, size=1, data=b"x")
    with pytest.raises(StorageRefused) as not_hex:
        store.path("ok", "../../secret")
    assert not_hex.value.code == "video_review_bad_hash"
    with pytest.raises(StorageRefused) as too_big:
        store.put_part("ok", "a" * 64, index=0, count=1, size=1_000_001, data=b"x")
    assert too_big.value.status == 413
    first = b"a" * 1_000_000
    store.put_part(
        "ok", hashlib.sha256(first).hexdigest(), index=0, count=1, size=len(first), data=first
    )
    second = b"b" * 20
    with pytest.raises(StorageRefused) as full:
        store.put_part(
            "ok", hashlib.sha256(second).hexdigest(), index=0, count=1, size=20, data=second
        )
    assert full.value.status == 507


def test_only_files_a_live_review_shows_are_kept(tmp_path: Path) -> None:
    store = _store(tmp_path)
    names = []
    for body in (b"old cut", b"new cut", b"sheet"):
        sha = hashlib.sha256(body).hexdigest()
        store.put_part("v", sha, index=0, count=1, size=len(body), data=body)
        names.append(sha)
    reviews = [
        VideoReview(status="superseded", files=[{"sha256": names[0]}]),
        VideoReview(status="pending", files=[{"sha256": names[1]}, {"sha256": names[2]}]),
    ]
    assert admin_service.kept_files(reviews) == {names[1], names[2]}
    assert store.keep_only("v", admin_service.kept_files(reviews)) == [names[0]]
    assert store.path("v", names[1]) is not None and store.path("v", names[0]) is None


def _review(
    gate: str, status: str = "pending", payload: dict[str, Any] | None = None
) -> VideoReview:
    return VideoReview(gate=gate, status=status, payload=payload or {}, files=[])


def test_decisions_need_a_pending_review_a_reason_to_reject_and_an_outline_choice() -> None:
    outline = _review("outline", payload={"options": [{"key": "A"}, {"key": "B"}, {"key": "C"}]})
    assert admin_service.outline_choices(outline.payload) == ["A", "B", "C"]
    approve = DecisionIn(decision="approve")
    assert "選一個大綱" in (admin_service.decision_problem(outline, approve) or "")
    assert (
        admin_service.decision_problem(outline, DecisionIn(decision="approve", choice="B")) is None
    )
    assert admin_service.decision_problem(outline, DecisionIn(decision="approve", choice="D"))
    assert "原因" in (
        admin_service.decision_problem(_review("final"), DecisionIn(decision="reject")) or ""
    )
    assert (
        admin_service.decision_problem(
            _review("final"), DecisionIn(decision="reject", note="片頭太長")
        )
        is None
    )
    assert admin_service.decision_problem(_review("audio", "superseded"), approve)
    assert admin_service.decision_problem(_review("publish"), approve) is None


def test_a_look_review_needs_one_of_its_sheets_chosen_and_a_storyboard_does_not() -> None:
    look = _review("look", payload={"options": [{"key": "A"}, {"key": "B"}]})
    approve = DecisionIn(decision="approve")
    assert "角色設定圖" in (admin_service.decision_problem(look, approve) or "")
    assert admin_service.decision_problem(look, DecisionIn(decision="approve", choice="B")) is None
    assert admin_service.decision_problem(look, DecisionIn(decision="approve", choice="Z"))
    assert admin_service.decision_problem(_review("storyboard"), approve) is None


def test_a_dubs_review_is_approved_as_uploaded_or_sent_back_with_a_reason() -> None:
    """No choice to make: approving says the tracks are on YouTube, rejecting needs a reason."""
    approve = DecisionIn(decision="approve")
    assert admin_service.decision_problem(_review("dubs"), approve) is None
    assert (
        admin_service.decision_problem(_review("dubs"), DecisionIn(decision="approve", choice="en"))
        is None
    ), "a stray choice is ignored, not refused"
    assert "原因" in (
        admin_service.decision_problem(_review("dubs"), DecisionIn(decision="reject")) or ""
    )
    assert (
        admin_service.decision_problem(
            _review("dubs"), DecisionIn(decision="reject", note="英文太快")
        )
        is None
    )


def test_a_dubs_review_carries_its_tracks_as_m4a_mp3_or_wav() -> None:
    base = {"gate": "dubs", "content_sha256": "a" * 64, "summary": "配音"}
    track = {"role": "dub_zh_cn", "sha256": "b" * 64, "size": 1}
    for content_type in ("audio/mp4", "audio/mpeg", "audio/wav"):
        review = ReviewIn.model_validate(
            {**base, "files": [{**track, "content_type": content_type}]}
        )
        assert review.gate == "dubs" and review.files[0].content_type == content_type
    with pytest.raises(ValueError):
        ReviewIn.model_validate({**base, "files": [{**track, "content_type": "audio/ogg"}]})


def test_the_dub_languages_are_the_caption_languages_each_at_most_once_in_page_order() -> None:
    assert DubLocalesIn.model_validate({"locales": []}).locales == []
    assert DubLocalesIn.model_validate({"locales": ["ko", "en"]}).locales == ["en", "ko"]
    assert DubLocalesIn.model_validate({"locales": ["zh-CN", "ja", "ko", "en"]}).locales == [
        "en",
        "ja",
        "ko",
        "zh-CN",
    ]
    for bad in (["en", "en"], ["zh-TW"], ["fr"], ["en", "ja", "ko", "zh-CN", "en"]):
        with pytest.raises(ValueError):
            DubLocalesIn.model_validate({"locales": bad})


def test_a_language_choice_keeps_page_order_drops_empty_languages_and_a_dub_brings_captions() -> (
    None
):
    """The language panel's body (docs/videos/LANGUAGES.md): each language with its parts."""
    chosen = LocalesIn.model_validate(
        {"locales": {"ko": {"dub": True}, "en": {"metadata": True}, "ja": {}}}
    )
    assert list(chosen.locales) == ["en", "ko"], "page order, the empty language dropped"
    assert chosen.locales["ko"].model_dump() == {"metadata": False, "captions": True, "dub": True}
    assert chosen.locales["en"].chosen() == ["metadata"]
    assert LocalesIn.model_validate({}).locales == {}, (
        "nothing chosen is 'only Traditional Chinese'"
    )
    assert LocalesIn.model_validate({"locales": {"en": {"voice": True}}}).locales == {}, (
        "a stray field is ignored, as on the other routes, and leaves the language empty"
    )
    for bad in ({"zh-TW": {"captions": True}}, {"fr": {}}):
        with pytest.raises(ValueError):
            LocalesIn.model_validate({"locales": bad})
    # A stored shape no page wrote reads as no choice, not as an error.
    assert (
        admin_service.locale_choices(
            VideoProject(slug="v", title="t", stage="s", locales={"en": 1})
        )
        == {}
    )


def _batch(status: str, payload: dict[str, Any], day: int) -> VideoReview:
    return VideoReview(
        id=uuid4(),
        gate="languages",
        status=status,
        content_sha256=str(day) * 64,
        summary="languages",
        payload=payload,
        files=[],
        created_at=datetime(2026, 9, day, tzinfo=UTC),
    )


def test_where_each_chosen_part_stands_follows_the_languages_batches_newest_last() -> None:
    choices = admin_service.locale_choices(
        VideoProject(
            slug="v",
            title="t",
            stage="s",
            locales={
                "en": {"metadata": True, "dub": True},
                "ja": {"captions": True},
                "ko": {"metadata": True},
            },
        )
    )
    nothing = admin_service.language_states(choices, [])
    assert {
        locale: {part: out.state for part, out in parts.items()}
        for locale, parts in nothing.items()
    } == {
        "en": {"metadata": "working", "captions": "working", "dub": "working"},
        "ja": {"captions": "working"},
        "ko": {"metadata": "working"},
    }
    first = _batch(
        "approved",
        {
            "locales": {
                "en": {"metadata": "ready", "captions": "ready", "dub": "ready"},
                "ja": {"captions": "ready"},
            }
        },
        20,
    )
    second = _batch(
        "pending",
        {
            "locales": {
                "ko": {"metadata": "ready"},
                "en": {"dub": {"status": "skipped", "reason": "1.15 倍還塞不下"}},
            }
        },
        22,
    )
    sent_back = _batch("rejected", {"locales": {"ja": {"captions": "skipped", "reason": "x"}}}, 23)
    unrelated = VideoReview(
        gate="dubs",
        status="approved",
        content_sha256="f" * 64,
        payload={"locales": {"en": {"status": "ready"}}},
        files=[],
    )
    # Newest first, as the service lists them; the states read them oldest first.
    states = admin_service.language_states(choices, [sent_back, unrelated, second, first])
    assert states["en"]["metadata"].state == "ready", "descriptions the site sends stay ready"
    assert states["en"]["captions"].state == "ready"
    assert (states["en"]["dub"].state, states["en"]["dub"].reason) == (
        "skipped",
        "1.15 倍還塞不下",
    ), "the later batch speaks last"
    assert states["ja"]["captions"].state == "ready", "a sent-back batch counts for nothing"
    assert states["ko"]["metadata"].state == "ready"
    uploaded = admin_service.language_states(choices, [first])
    assert uploaded["en"]["dub"].state == "uploaded", (
        "a dub ready in an approved batch was uploaded"
    )
    assert uploaded["ko"]["metadata"].state == "working"
    # A batch the owner must act on is one with a dub track to upload.
    assert admin_service.languages_need_owner(first.payload)
    assert not admin_service.languages_need_owner(second.payload)
    assert not admin_service.languages_need_owner({"locales": {"en": {"metadata": "ready"}}})
    assert not admin_service.languages_need_owner({})


def test_a_video_is_ready_to_upload_once_confirmed_decided_and_every_chosen_part_is_done() -> None:
    noon = datetime(2026, 9, 27, 12, tzinfo=UTC)
    choices = admin_service.locale_choices(
        VideoProject(
            slug="v", title="t", stage="s", locales={"en": {"metadata": True, "dub": True}}
        )
    )
    done = admin_service.language_states(
        choices,
        [
            _batch(
                "pending",
                {
                    "locales": {
                        "en": {
                            "metadata": "ready",
                            "captions": "ready",
                            "dub": "skipped",
                            "reason": "r",
                        }
                    }
                },
                20,
            )
        ],
    )
    working = admin_service.language_states(choices, [])
    decided = VideoProject(
        slug="v",
        title="t",
        stage="done",
        checklist=[],
        last_synced_at=noon,
        locales={"en": {"metadata": True, "captions": True, "dub": True}},
        locales_decided_at=noon,
    )
    assert admin_service.ready_to_upload(decided, noon, done)
    assert not admin_service.ready_to_upload(decided, noon, working), "a part still working"
    assert not admin_service.ready_to_upload(decided, None, done), (
        "the upload confirmation is not approved"
    )
    undecided = VideoProject(
        slug="v", title="t", stage="done", checklist=[], last_synced_at=noon, locales={}
    )
    assert not admin_service.ready_to_upload(undecided, noon, {}), (
        "the owner has not decided the languages"
    )
    only_chinese = VideoProject(
        slug="v", title="t", stage="done", locales={}, locales_decided_at=noon
    )
    assert admin_service.ready_to_upload(only_chinese, noon, {}), (
        "'only Traditional Chinese' is a decision"
    )
    assert not admin_service.ready_to_upload(
        VideoProject(
            slug="v",
            title="t",
            stage="done",
            locales={},
            locales_decided_at=noon,
            youtube_video_id="dQw4w9WgXcQ",
        ),
        noon,
        {},
    )
    assert not admin_service.ready_to_upload(
        VideoProject(
            slug="v", title="t", stage="done", locales={}, locales_decided_at=noon, dropped_at=noon
        ),
        noon,
        {},
    )
    # The summary carries the choice, the states and the verdict; the dub languages are derived
    # for the older page.
    summary = ProjectSummary(**admin_service._summary(decided, 0, None, noon, done))
    assert summary.ready_to_upload and summary.locales_decided_at == noon
    assert summary.locales["en"].model_dump() == {"metadata": True, "captions": True, "dub": True}
    assert summary.languages["en"]["dub"].state == "skipped" and summary.dub_locales == ["en"]
    assert not ProjectSummary(**admin_service._summary(undecided, 0)).ready_to_upload


@pytest.mark.asyncio
async def test_the_owner_decides_a_video_s_languages_once_and_a_drama_or_a_dropped_one_refuses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = VideoProject(id=uuid4(), slug="v", title="AI 模型怎麼挑", stage="final", locales={})
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "project_view", AsyncMock(return_value="view"))
    session = AsyncMock()
    session.add = MagicMock()
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    assert (
        admin_service._summary(project, 0)["locales"] == {} and project.locales_decided_at is None
    )

    chosen = LocalesIn.model_validate({"locales": {"ko": {"dub": True}, "en": {"metadata": True}}})
    assert await admin_service.set_locales(session, "v", owner, chosen) == "view"
    assert project.locales == {
        "en": {"metadata": True, "captions": False, "dub": False},
        "ko": {"metadata": False, "captions": True, "dub": True},
    }
    decided = project.locales_decided_at
    assert decided is not None
    audit = session.add.call_args.args[0]
    assert audit.action == "video_locales_set" and audit.actor_user_id == owner.id
    assert audit.target == f"video_project:{project.id}"
    assert audit.metadata_json == {"slug": "v", "locales": project.locales}
    assert session.commit.await_count == 1
    assert admin_service._summary(project, 0)["dub_locales"] == ["ko"]

    same = LocalesIn.model_validate(
        {"locales": {"en": {"metadata": True}, "ko": {"captions": True, "dub": True}}}
    )
    assert await admin_service.set_locales(session, "v", owner, same) == "view"
    assert session.add.call_count == 1 and session.commit.await_count == 1, (
        "the same choice again is not a change"
    )

    # "Only Traditional Chinese" is a decision too, recorded once with its time kept.
    only = LocalesIn.model_validate({"locales": {}})
    assert await admin_service.set_locales(session, "v", owner, only) == "view"
    assert project.locales == {} and project.locales_decided_at == decided
    assert session.commit.await_count == 2

    # The dub checkboxes of the older page: a ticked language gets every part, an unticked one
    # loses its dub and keeps the rest.
    project.locales = {"en": {"metadata": True, "captions": True, "dub": True}}
    await admin_service.set_dub_locales(
        session, "v", owner, DubLocalesIn.model_validate({"locales": ["ja"]})
    )
    assert project.locales == {
        "en": {"metadata": True, "captions": True, "dub": False},
        "ja": {"metadata": True, "captions": True, "dub": True},
    }
    assert session.add.call_args.args[0].action == "video_locales_set"

    project.format = "drama"
    with pytest.raises(AppError) as drama:
        await admin_service.set_locales(
            session, "v", owner, LocalesIn.model_validate({"locales": {"en": {"dub": True}}})
        )
    assert drama.value.code == "video_locales_dub_not_for_drama"
    await admin_service.set_locales(
        session, "v", owner, LocalesIn.model_validate({"locales": {"en": {"captions": True}}})
    )
    assert project.locales == {"en": {"metadata": False, "captions": True, "dub": False}}, (
        "a drama takes descriptions and captions"
    )

    project.dropped_at = datetime.now(UTC)
    with pytest.raises(AppError) as refused:
        await admin_service.set_locales(session, "v", owner, only)
    assert refused.value.code == "video_project_dropped"
    assert project.locales == {"en": {"metadata": False, "captions": True, "dub": False}}


def test_a_review_carries_up_to_48_files_and_a_subject_that_is_an_id() -> None:
    base = {"gate": "storyboard", "content_sha256": "a" * 64, "summary": "分鏡"}
    file = {"role": "shot_01", "sha256": "b" * 64, "size": 1, "content_type": "image/png"}
    ReviewIn.model_validate({**base, "files": [file] * 48})
    with pytest.raises(ValueError):
        ReviewIn.model_validate({**base, "files": [file] * 49})
    assert ReviewIn.model_validate({**base, "gate": "look", "subject": "jingwei"}).subject
    with pytest.raises(ValueError):
        ReviewIn.model_validate({**base, "gate": "look", "subject": "Jing Wei"})


@pytest.mark.asyncio
async def test_a_look_review_replaces_only_the_pending_one_of_its_character(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    store = _store(tmp_path)
    project = VideoProject(id=uuid4(), slug="v", title="精衛填海", stage="look")
    jingwei = VideoReview(
        gate="look",
        subject="jingwei",
        status="pending",
        content_sha256="a" * 64,
        payload={},
        files=[],
    )
    yandi = VideoReview(
        gate="look",
        subject="yandi",
        status="pending",
        content_sha256="b" * 64,
        payload={},
        files=[],
    )
    outline = VideoReview(
        gate="outline",
        subject=None,
        status="pending",
        content_sha256="c" * 64,
        payload={},
        files=[],
    )
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(
        admin_service, "_reviews", AsyncMock(return_value=[jingwei, yandi, outline])
    )
    monkeypatch.setattr(admin_service, "auto_approves_audio", AsyncMock(return_value=False))
    monkeypatch.setattr(admin_service, "auto_approves_storyboard", AsyncMock(return_value=True))
    session = AsyncMock()
    session.add = MagicMock()
    token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")

    newer = ReviewIn(
        gate="look",
        subject="jingwei",
        content_sha256="d" * 64,
        summary="精衛的新設定圖",
        payload={"options": [{"key": "A"}]},
    )
    out = await admin_service.submit_review(session, store, "v", newer, token)
    assert out.subject == "jingwei" and out.status == "pending"
    assert (jingwei.status, yandi.status, outline.status) == ("superseded", "pending", "pending")

    board = ReviewIn(
        gate="storyboard",
        content_sha256="e" * 64,
        summary="分鏡",
        payload={"shots": [{"id": "a"}], "judge": {"overall": 9, "problems": []}},
    )
    auto = await admin_service.submit_review(session, store, "v", board, token)
    assert auto.status == "approved" and auto.note == AUTO_APPROVED_STORYBOARD_NOTE
    assert session.add.call_args.args[0].action == "video_review_auto_approved"


@pytest.mark.asyncio
async def test_dropping_a_video_closes_its_reviews_deletes_its_previews_and_is_final(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    store = _store(tmp_path)
    body = b"outline preview"
    sha = hashlib.sha256(body).hexdigest()
    store.put_part("v", sha, index=0, count=1, size=len(body), data=body)
    project = VideoProject(id=uuid4(), slug="v", title="Google AI 學生方案", stage="outline")
    pending = _review("outline")
    decided = _review("audio", "approved")
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=[pending, decided]))
    monkeypatch.setattr(admin_service, "project_view", AsyncMock(return_value="view"))
    session = AsyncMock()
    session.add = MagicMock()
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")

    note = DropIn(note="  第二批已經做了這題  ")
    assert await admin_service.drop_project(session, store, "v", owner, note) == "view"
    assert (pending.status, decided.status) == ("superseded", "approved")
    assert project.dropped_at is not None and project.dropped_by_user_id == owner.id
    assert project.dropped_note == "第二批已經做了這題"
    assert store.path("v", sha) is None, "a dropped video keeps no previews"
    assert session.add.call_args.args[0].action == "video_project_dropped"

    await admin_service.drop_project(session, store, "v", owner, DropIn(note="again"))
    assert session.add.call_count == 1 and project.dropped_note == "第二批已經做了這題"

    token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")
    outline = ReviewIn(gate="outline", content_sha256="a" * 64, summary="大綱")
    with pytest.raises(AppError) as submitted:
        await admin_service.submit_review(session, store, "v", outline, token)
    with pytest.raises(AppError) as decided_after:
        await admin_service.decide(session, "v", uuid4(), owner, DecisionIn(decision="approve"))
    assert submitted.value.code == decided_after.value.code == "video_project_dropped"


def _series_episode(
    episode_status: str, request_status: str
) -> tuple[VideoDramaSeries, VideoDramaEpisode, VideoDramaRequest]:
    """A three-episode drama whose second episode is being made as the video "saga-two"."""
    series = VideoDramaSeries(
        id=uuid4(), slug="saga", title="長篇", status="active", planned_episodes=3
    )
    request = VideoDramaRequest(
        id=uuid4(),
        premise="長篇 第 2 集",
        status=request_status,
        slug="saga-two",
        series_id=series.id,
        episode_number=2,
    )
    episode = VideoDramaEpisode(
        id=uuid4(),
        series_id=series.id,
        number=2,
        slug="saga-two",
        status=episode_status,
        request_id=request.id,
    )
    return series, episode, request


def _dropping(
    monkeypatch: pytest.MonkeyPatch,
    project: VideoProject,
    found: tuple[VideoDramaEpisode, VideoDramaSeries] | None,
    request: VideoDramaRequest,
) -> AsyncMock:
    """A session on which dropping ``project`` finds ``found`` as its episode and ``request``
    as the row that episode travelled as."""
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=[]))
    monkeypatch.setattr(admin_service, "project_view", AsyncMock(return_value="view"))
    if found is not None:
        monkeypatch.setattr(admin_service, "_episode_of", AsyncMock(return_value=found))
    session = AsyncMock()
    session.add = MagicMock()
    session.scalar = AsyncMock(return_value=request)
    session.scalars = AsyncMock(return_value=[] if found is None else [found[0]])
    return session


@pytest.mark.asyncio
async def test_dropping_an_episode_s_video_cancels_the_request_it_was_started_as(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    series, episode, request = _series_episode("started", "started")
    project = VideoProject(
        id=uuid4(), slug="saga-two", title="長篇 第 2 集", stage="outline", series_slug="saga"
    )
    session = _dropping(monkeypatch, project, (episode, series), request)
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")

    await admin_service.drop_project(session, _store(tmp_path), "saga-two", owner, DropIn(note="x"))

    assert episode.status == "skipped"
    assert request.status == "cancelled" and request.cancelled_at == project.dropped_at
    assert request.updated_at == project.dropped_at and request.finished_at is None
    assert session.scalar.await_count == 1 and session.commit.await_count == 1
    assert series.status == "active", "episodes 1 and 3 are still to come"


@pytest.mark.asyncio
async def test_dropping_an_episode_s_video_after_it_was_done_leaves_its_request_done(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    project = VideoProject(
        id=uuid4(), slug="saga-two", title="長篇 第 2 集", stage="final", series_slug="saga"
    )
    series, episode, request = _series_episode("done", "done")
    session = _dropping(monkeypatch, project, (episode, series), request)
    await admin_service.drop_project(session, _store(tmp_path), "saga-two", owner, DropIn(note="x"))
    assert (episode.status, request.status, request.cancelled_at) == ("done", "done", None)

    # An episode still open whose request the worker already reported done keeps it done too.
    project.dropped_at = None
    series, episode, request = _series_episode("started", "done")
    session = _dropping(monkeypatch, project, (episode, series), request)
    await admin_service.drop_project(session, _store(tmp_path), "saga-two", owner, DropIn(note="x"))
    assert (episode.status, request.status, request.cancelled_at) == ("skipped", "done", None)


@pytest.mark.asyncio
async def test_dropping_a_video_of_no_series_touches_no_drama_request(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _, _, request = _series_episode("started", "started")
    project = VideoProject(id=uuid4(), slug="ai-agent-permissions", title="教學", stage="outline")
    session = _dropping(monkeypatch, project, None, request)
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")

    await admin_service.drop_project(
        session, _store(tmp_path), "ai-agent-permissions", owner, DropIn(note="x")
    )

    assert project.dropped_at is not None
    assert (request.status, request.cancelled_at) == ("started", None)
    assert session.scalar.await_count == 0 and session.scalars.await_count == 0
    assert [call.args[0].action for call in session.add.call_args_list] == [
        "video_project_dropped"
    ]


def test_a_report_keeps_the_source_article_an_older_tool_does_not_send() -> None:
    assert ProjectIn(title="t", stage="s").source_guide is None
    assert ProjectIn(title="t", stage="s", source_guide="ai-news-x-20260820").source_guide
    with pytest.raises(ValueError):
        ProjectIn(title="t", stage="s", source_guide="../etc")
    assert ProjectIn(title="t", stage="s").category is None, "an older tool sends no category"
    assert ProjectIn(title="t", stage="s", category="tutorial").category == "tutorial"
    with pytest.raises(ValueError):
        ProjectIn(title="t", stage="s", category="news")


def test_the_categories_are_one_list_in_the_model_the_schema_and_the_migration() -> None:
    assert set(VIDEO_CATEGORY_CODES) == set(VIDEO_CATEGORIES)
    assert len(VIDEO_CATEGORY_CODES) == 8
    table = cast(Table, VideoProject.__table__)
    column = table.c.category
    assert isinstance(column.type, String) and column.type.length == 16 and column.nullable
    assert any(constraint.name == "ck_video_project_category" for constraint in table.constraints)
    # The owner may clear a category; the key itself is not optional.
    assert CategoryIn.model_validate({"category": None}).category is None
    with pytest.raises(ValueError):
        CategoryIn.model_validate({})
    with pytest.raises(ValueError):
        CategoryIn.model_validate({"category": "none"})


@pytest.mark.asyncio
async def test_the_owner_files_a_video_under_a_category_and_the_same_choice_is_no_change(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = VideoProject(id=uuid4(), slug="v", title="AI 模型怎麼挑", stage="final")
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "project_view", AsyncMock(return_value="view"))
    session = AsyncMock()
    session.add = MagicMock()
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    assert admin_service._summary(project, 0)["category"] is None

    filed = CategoryIn(category="tutorial")
    assert await admin_service.set_category(session, "v", owner, filed) == "view"
    assert project.category == "tutorial"
    audit = session.add.call_args.args[0]
    assert audit.action == "video_category_set" and audit.actor_user_id == owner.id
    assert audit.target == f"video_project:{project.id}"
    assert audit.metadata_json == {"slug": "v", "category": "tutorial", "previous": None}
    assert session.commit.await_count == 1
    assert admin_service._summary(project, 0)["category"] == "tutorial"

    assert await admin_service.set_category(session, "v", owner, filed) == "view"
    assert session.add.call_count == 1 and session.commit.await_count == 1, (
        "the same category again is not a change"
    )

    cleared = CategoryIn(category=None)
    assert await admin_service.set_category(session, "v", owner, cleared) == "view"
    assert project.category is None and session.commit.await_count == 2
    assert session.add.call_args.args[0].metadata_json["previous"] == "tutorial"

    # A dropped video is filed too: the catalog lists it under its category.
    project.dropped_at = datetime.now(UTC)
    await admin_service.set_category(session, "v", owner, filed)
    assert project.category == "tutorial"


def test_a_review_payload_is_capped() -> None:
    body = {"gate": "final", "content_sha256": "a" * 64, "summary": "成片"}
    ReviewIn.model_validate({**body, "payload": {"text": "字" * 1000}})
    with pytest.raises(ValueError):
        ReviewIn.model_validate({**body, "payload": {"text": "字" * 100_000}})


def _app(user: User | None = None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.tool_router, prefix="/api/v1")
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    if user is not None:
        app.dependency_overrides[current_user] = lambda: user
    return app


@pytest.mark.asyncio
async def test_admin_routes_need_content_capabilities(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    monkeypatch.setattr(admin_service, "list_projects", AsyncMock(return_value=[]))

    # The list route opens the review store first (it prunes published videos' mp4 files).
    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    decide = AsyncMock()
    drop = AsyncMock()
    retry = AsyncMock()
    dubs = AsyncMock()
    languages = AsyncMock()
    monkeypatch.setattr(admin_service, "decide", decide)
    monkeypatch.setattr(admin_service, "drop_project", drop)
    monkeypatch.setattr(admin_service, "retry_project", retry)
    monkeypatch.setattr(admin_service, "set_dub_locales", dubs)
    monkeypatch.setattr(admin_service, "set_locales", languages)
    category = AsyncMock()
    monkeypatch.setattr(admin_service, "set_category", category)
    empty_page = {
        "items": [], "total": 0, "page": 1, "pages": 0, "facets": {"category": [], "state": []},
    }
    monkeypatch.setattr(admin_service, "browse_projects", AsyncMock(return_value=empty_page))
    app = _app(viewer)
    review = f"/api/v1/admin/videos/v/reviews/{uuid4()}/decision"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        nobody = await client.get("/api/v1/admin/videos")
        viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
        listed = await client.get("/api/v1/admin/videos")
        refused = await client.post(review, json={"decision": "approve"})
        not_dropped = await client.post("/api/v1/admin/videos/v/drop", json={"note": "重複"})
        not_retried = await client.post("/api/v1/admin/videos/v/retry")
        not_dubbed = await client.put("/api/v1/admin/videos/v/dubs", json={"locales": ["en"]})
        not_chosen = await client.put(
            "/api/v1/admin/videos/v/languages", json={"locales": {"en": {"captions": True}}}
        )
        browsed = await client.get("/api/v1/admin/videos/browse")
        not_filed = await client.put(
            "/api/v1/admin/videos/v/category", json={"category": "tutorial"}
        )
    assert nobody.status_code == 403 and listed.status_code == 200
    assert browsed.status_code == 200, "a viewer reads the catalog"
    assert not_filed.status_code == 403, "but does not file a video"
    category.assert_not_awaited()
    assert refused.status_code == 403, "a viewer can read but not decide"
    assert not_dropped.status_code == 403, "nor drop a video"
    assert not_retried.status_code == 403, "nor retry a blocked video"
    assert not_dubbed.status_code == 403, "nor pick its dub languages"
    assert not_chosen.status_code == 403, "nor decide its languages"
    decide.assert_not_awaited()
    drop.assert_not_awaited()
    retry.assert_not_awaited()
    dubs.assert_not_awaited()
    languages.assert_not_awaited()


@pytest.mark.asyncio
async def test_content_manager_can_request_a_blocked_video_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    view = {
        "slug": "v", "title": "Blocked video", "stage": "blocked", "checklist": [],
        "youtube_video_id": None, "last_synced_at": "2026-09-27T00:00:00Z", "pending": 0,
        "retry_request_id": str(uuid4()), "retry_acknowledged_id": None, "reviews": [],
    }
    request = AsyncMock(return_value=view)
    monkeypatch.setattr(admin_service, "retry_project", request)
    app = _app(owner)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/admin/videos/v/retry")
    assert response.status_code == 200
    assert response.json()["retry_request_id"] == view["retry_request_id"]
    request.assert_awaited_once()


@pytest.mark.asyncio
async def test_a_content_manager_sets_the_dub_languages_and_bad_ones_never_reach_the_service(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    view = {
        "slug": "v",
        "title": "AI 模型怎麼挑",
        "stage": "final",
        "checklist": [],
        "youtube_video_id": None,
        "last_synced_at": "2026-09-27T00:00:00Z",
        "pending": 0,
        "dub_locales": ["en"],
        "reviews": [],
    }
    set_dubs = AsyncMock(return_value=view)
    set_languages = AsyncMock(return_value=view)
    monkeypatch.setattr(admin_service, "set_dub_locales", set_dubs)
    monkeypatch.setattr(admin_service, "set_locales", set_languages)
    url = "/api/v1/admin/videos/v/dubs"
    languages = "/api/v1/admin/videos/v/languages"
    transport = ASGITransport(app=_app(owner))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        saved = await client.put(url, json={"locales": ["en"]})
        twice = await client.put(url, json={"locales": ["en", "en"]})
        original = await client.put(url, json={"locales": ["zh-TW"]})
        unknown = await client.put(url, json={"locales": ["en"], "note": "x"})
        chosen = await client.put(languages, json={"locales": {"ja": {"dub": True}}})
        only = await client.put(languages, json={})
        stray = await client.put(languages, json={"locales": {"en": {"voice": True}}})
        chinese = await client.put(languages, json={"locales": {"zh-TW": {"captions": True}}})
    assert saved.status_code == 200, saved.text
    assert saved.json()["dub_locales"] == ["en"]
    assert set_dubs.await_args.args[3].locales == ["en"]
    assert twice.status_code == 422 and original.status_code == 422
    assert unknown.status_code == 200, "an extra field is ignored, as on the other routes"
    assert set_dubs.await_count == 2
    assert chosen.status_code == 200, chosen.text
    assert set_languages.await_args_list[0].args[3].locales["ja"].model_dump() == {
        "metadata": False,
        "captions": True,
        "dub": True,
    }
    assert only.status_code == 200 and set_languages.await_args_list[1].args[3].locales == {}
    assert stray.status_code == 200 and set_languages.await_args_list[2].args[3].locales == {}, (
        "a stray part is ignored, as on the other routes, and leaves nothing chosen"
    )
    assert chinese.status_code == 422
    assert set_languages.await_count == 3


@pytest.mark.asyncio
async def test_pipeline_routes_need_a_video_tool_token() -> None:
    app = _app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/video/reviews/v")
        admin = await client.get("/api/v1/admin/videos")
    assert response.status_code == 401
    assert admin.status_code == 401


@pytest.mark.asyncio
async def test_uploaded_parts_land_in_the_configured_store(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    app = _app()
    token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")
    app.dependency_overrides[speech_api.video_tool] = lambda: token
    body = b"narration preview"
    sha = hashlib.sha256(body).hexdigest()
    url = f"/api/v1/video/reviews/ai-model-choice/files/{sha}"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        done = await client.put(
            url, params={"part": 0, "parts": 1, "size": len(body)}, content=body
        )
        wrong = await client.put(
            f"/api/v1/video/reviews/ai-model-choice/files/{'b' * 64}",
            params={"part": 0, "parts": 1, "size": len(body)},
            content=body,
        )
    assert done.status_code == 200 and done.json() == {"received": [0], "complete": True}
    assert (tmp_path / "ai-model-choice" / sha).read_bytes() == body
    assert wrong.status_code == 422 and wrong.json()["code"] == "video_review_hash_mismatch"


@pytest.mark.asyncio
async def test_a_preview_is_served_with_byte_ranges_and_never_cached(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    preview = tmp_path / "preview.mp4"
    preview.write_bytes(bytes(range(200)))
    monkeypatch.setattr(
        admin_service, "file_for_admin", AsyncMock(return_value=(preview, "video/mp4"))
    )

    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    app = _app(owner)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            f"/api/v1/admin/videos/v/files/{'a' * 64}", headers={"Range": "bytes=10-19"}
        )
    assert response.status_code == 206
    assert response.content == bytes(range(10, 20))
    assert response.headers["content-type"] == "video/mp4"
    assert response.headers["cache-control"] == "private, no-store"


@pytest.mark.asyncio
async def test_jev_picks_the_outline_the_checks_pass_the_final_cut_and_a_resent_file_is_rejudged(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The hands-off approvals (docs/videos/HANDS-OFF.md): the server applies the rules to the
    worker's payload as it arrives, and a file sent again while it waits is judged again."""
    store = ReviewStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    now = datetime.now(UTC)
    project = VideoProject(id=uuid4(), slug="v", title="t", stage="final", checklist=[])
    waiting = VideoReview(
        id=uuid4(),
        project_id=project.id,
        gate="final",
        subject=None,
        status="pending",
        content_sha256="f" * 64,
        summary="成片",
        payload={},
        files=[],
        created_at=now,
    )
    decided = VideoReview(
        id=uuid4(),
        project_id=project.id,
        gate="audio",
        subject=None,
        status="approved",
        content_sha256="a" * 64,
        summary="旁白",
        payload={},
        files=[],
        created_at=now,
        decided_at=now,
    )
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=[waiting, decided]))
    monkeypatch.setattr(admin_service, "auto_approves_audio", AsyncMock(return_value=False))
    monkeypatch.setattr(admin_service, "auto_approves_storyboard", AsyncMock(return_value=False))
    monkeypatch.setattr(admin_service, "auto_picks_outline", AsyncMock(return_value=True))
    monkeypatch.setattr(admin_service, "compilation_slugs", AsyncMock(return_value=set()))
    final_rule = AsyncMock(return_value=True)
    monkeypatch.setattr(admin_service, "auto_approves_final", final_rule)
    session = AsyncMock()
    session.add = MagicMock()
    token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")

    pick = {
        "choice": "B",
        "probabilities": {"A": 0.26, "B": 0.74},
        "options": {"A": {"stance": 0.9, "demo": 0.4}, "B": {"stance": 0.81, "demo": 0.92}},
        "advice": 0.05,
    }
    outline = ReviewIn(
        gate="outline",
        content_sha256="c" * 64,
        summary="大綱",
        payload={"options": [{"key": "A"}, {"key": "B"}], "pick": pick},
    )
    picked = await admin_service.submit_review(session, store, "v", outline, token)
    assert picked.status == "approved" and picked.choice == "B"
    assert (
        picked.note == "Jev 挑了 B（0.74）：符合立場 0.81、有示範 0.92、建議 0.05，依設定自動核准"
    )
    assert session.add.call_args.args[0].action == "video_review_auto_approved"

    # The same final cut sent again while it waits: the quality check arrived after the fact.
    qa = {"ok": True, "final_sha256": "f" * 64, "items": []}
    resent = ReviewIn(
        gate="final", content_sha256="f" * 64, summary="成片＋品管", payload={"qa": qa}
    )
    again = await admin_service.submit_review(session, store, "v", resent, token)
    assert again.id == waiting.id and again.status == "approved"
    assert again.note == QA_AUTO_APPROVED_NOTE
    assert waiting.summary == "成片＋品管" and waiting.payload == {"qa": qa}
    # A project row from before formats existed reads as a tutorial (DRAMA-FLOW.md §一).
    assert final_rule.await_args.args[1:] == ("final", {"qa": qa}, "f" * 64, "slides")

    # A decided review of the same file comes back as it is.
    settled = ReviewIn(gate="audio", content_sha256="a" * 64, summary="旁白", payload={"x": 1})
    same = await admin_service.submit_review(session, store, "v", settled, token)
    assert same.id == decided.id and same.status == "approved" and decided.payload == {}

    # A batch of languages: descriptions and captions the site sends, so nothing waits on the
    # owner; a dub track does, since only they can upload it in Studio.
    captions_only = ReviewIn(
        gate="languages",
        content_sha256="1" * 64,
        summary="語言：en 標題說明與 CC",
        payload={"locales": {"en": {"metadata": "ready", "captions": "ready"}}},
    )
    arrived = await admin_service.submit_review(session, store, "v", captions_only, token)
    assert (arrived.status, arrived.note) == (
        "approved",
        admin_service.LANGUAGES_AUTO_APPROVED_NOTE,
    )
    with_dub = ReviewIn(
        gate="languages",
        content_sha256="2" * 64,
        summary="語言：ja 配音",
        payload={"locales": {"ja": {"metadata": "ready", "captions": "ready", "dub": "ready"}}},
    )
    waits = await admin_service.submit_review(session, store, "v", with_dub, token)
    assert waits.status == "pending"

    # A character's sheet: the judge's suggestion stands when the owner turned that on.
    monkeypatch.setattr(admin_service, "auto_picks_look", AsyncMock(return_value=True))
    sheets = ReviewIn(
        gate="look",
        subject="jingwei",
        content_sha256="d" * 64,
        summary="精衛的設定圖",
        payload={
            "options": [{"key": "B", "judge": {"overall": 8, "problems": []}}],
            "suggested": "B",
        },
    )
    picked_sheet = await admin_service.submit_review(session, store, "v", sheets, token)
    assert picked_sheet.status == "approved" and picked_sheet.choice == "B"
    assert picked_sheet.note == "judge 給 B 8/10、沒有列出問題，依設定自動選"


# --- a binge series' screenplay and compilation (docs/videos/BINGE.md) ---------------------------


@pytest.mark.asyncio
async def test_a_screenplay_on_a_hands_off_series_is_approved_as_it_arrives(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from app.video_automation.judge import SCRIPT_AUTO_APPROVED_NOTE

    store = ReviewStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    project = VideoProject(
        id=uuid4(),
        slug="rebirth-20260927-ab12-e001",
        title="第 1 集",
        stage="script",
        checklist=[],
        series_slug="rebirth-20260927-ab12",
        episode_number=1,
    )
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=[]))
    script_rule = AsyncMock(return_value=True)
    monkeypatch.setattr(admin_service, "auto_approves_script", script_rule)
    monkeypatch.setattr(admin_service, "compilation_slugs", AsyncMock(return_value=set()))
    session = AsyncMock()
    session.add = MagicMock()
    token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")
    payload = {"coverage": {"hook": "有"}, "continuity_problems": []}
    review = ReviewIn(gate="script", content_sha256="5" * 64, summary="劇本", payload=payload)
    out = await admin_service.submit_review(session, store, project.slug, review, token)
    assert out.status == "approved" and out.note == SCRIPT_AUTO_APPROVED_NOTE
    assert script_rule.await_args.args[1:] == ("rebirth-20260927-ab12", payload)
    assert session.add.call_args.args[0].action == "video_review_auto_approved"

    # A compilation's final cut is judged by the shorter list: the rule is told which it is.
    final_rule = AsyncMock(return_value=False)
    monkeypatch.setattr(admin_service, "auto_approves_final", final_rule)
    monkeypatch.setattr(admin_service, "compilation_slugs", AsyncMock(return_value={project.slug}))
    cut = ReviewIn(gate="final", content_sha256="f" * 64, summary="合集", payload={"qa": {}})
    waiting = await admin_service.submit_review(session, store, project.slug, cut, token)
    assert waiting.status == "pending"
    assert final_rule.await_args.kwargs == {"compilation": True}


def test_a_compilation_s_cut_is_found_only_under_its_own_slug_in_the_work_volume(
    tmp_path: Path,
) -> None:
    (tmp_path / "s-full" / "upload").mkdir(parents=True)
    (tmp_path / "s-full" / "upload" / "final.mp4").write_bytes(b"mp4")
    assert admin_service.download_file(str(tmp_path), "s-full") == (
        tmp_path / "s-full" / "upload" / "final.mp4"
    )
    assert admin_service.download_file(str(tmp_path), "other") is None
    assert admin_service.download_file(None, "s-full") is None, "the volume is not mounted"
    assert admin_service.download_file(str(tmp_path), "../s-full") is None


@pytest.mark.asyncio
async def test_a_compilation_s_cut_is_downloaded_with_byte_ranges_and_only_by_a_manager(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    work = tmp_path / "work"
    (work / "s-full" / "upload").mkdir(parents=True)
    (work / "s-full" / "upload" / "final.mp4").write_bytes(bytes(range(200)))
    project = VideoProject(id=uuid4(), slug="s-full", title="合集", stage="publish", checklist=[])
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "compilation_slugs", AsyncMock(return_value={"s-full"}))

    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path), video_work_dir=str(work))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    async with AsyncClient(
        transport=ASGITransport(app=_app(owner)), base_url="http://test"
    ) as client:
        part = await client.get(
            "/api/v1/admin/videos/s-full/download", headers={"Range": "bytes=0-9"}
        )
        missing = await client.get("/api/v1/admin/videos/other/download")
    assert part.status_code == 206 and part.content == bytes(range(10))
    assert part.headers["content-type"] == "video/mp4"
    assert "s-full.mp4" in part.headers["content-disposition"]
    assert part.headers["cache-control"] == "private, no-store"
    assert missing.status_code == 404 and missing.json()["code"] == "video_download_not_found"
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    async with AsyncClient(
        transport=ASGITransport(app=_app(viewer)), base_url="http://test"
    ) as client:
        refused = await client.get("/api/v1/admin/videos/s-full/download")
    assert refused.status_code == 403, "a viewer watches previews but does not take the cut"


@pytest.mark.asyncio
async def test_the_catalog_takes_a_category_a_state_a_search_and_a_page(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    empty_page = {
        "items": [], "total": 0, "page": 1, "pages": 0, "facets": {"category": [], "state": []},
    }
    browsed = AsyncMock(return_value=empty_page)
    monkeypatch.setattr(admin_service, "browse_projects", browsed)
    filed = AsyncMock(
        return_value={
            "slug": "v", "title": "t", "stage": "s", "checklist": [], "youtube_video_id": None,
            "last_synced_at": "2026-09-30T00:00:00Z", "pending": 0, "category": "tutorial",
            "reviews": [],
        }
    )
    monkeypatch.setattr(admin_service, "set_category", filed)

    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path), video_work_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    url = "/api/v1/admin/videos/browse"
    async with AsyncClient(
        transport=ASGITransport(app=_app(owner)), base_url="http://test"
    ) as client:
        plain = await client.get(url)
        narrowed = await client.get(
            url,
            params={"category": "none", "state": "published", "q": "模型", "page": 3, "limit": 10},
        )
        refused = [
            await client.get(url, params=params)
            for params in (
                {"category": "bogus"},
                {"state": "library"},
                {"page": 0},
                {"limit": 101},
                {"q": "x" * 81},
            )
        ]
        set_ok = await client.put("/api/v1/admin/videos/v/category", json={"category": "tutorial"})
        set_bad = await client.put("/api/v1/admin/videos/v/category", json={"category": "news"})
        set_none = await client.put("/api/v1/admin/videos/v/category", json={})
    assert plain.status_code == narrowed.status_code == 200
    assert plain.json()["facets"] == {"category": [], "state": []}
    calls = [call.kwargs for call in browsed.await_args_list]
    keys = ("category", "state", "q", "page", "limit")
    assert {k: calls[0][k] for k in keys} == {
        "category": None, "state": None, "q": None, "page": 1,
        "limit": admin_service.BROWSE_PAGE_SIZE,
    }
    assert {k: calls[1][k] for k in keys} == {
        "category": "none", "state": "published", "q": "模型", "page": 3, "limit": 10,
    }
    assert calls[1]["work_dir"] == str(tmp_path)
    assert [response.status_code for response in refused] == [422] * 5
    assert len(calls) == 2, "a refused request never reaches the service"
    assert set_ok.status_code == 200 and set_ok.json()["category"] == "tutorial"
    assert filed.await_args.args[1] == "v"
    assert filed.await_args.args[3].category == "tutorial"
    assert set_bad.status_code == 422 and set_none.status_code == 422
    assert filed.await_count == 1, "a bad category never reaches the service"


@pytest.mark.asyncio
async def test_the_list_takes_the_shorts_filter_and_a_state_only_with_it(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    listed = AsyncMock(return_value=[])
    monkeypatch.setattr(admin_service, "list_projects", listed)
    monkeypatch.setattr(admin_service, "prune_published_previews", AsyncMock(return_value={}))

    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    url = "/api/v1/admin/videos"
    before = "2026-10-01T00:00:00+08:00"
    async with AsyncClient(
        transport=ASGITransport(app=_app(owner)), base_url="http://test"
    ) as client:
        plain = await client.get(url)
        others = await client.get(url, params={"shorts": "exclude", "format": "drama"})
        tab = await client.get(
            url,
            params={
                "shorts": "only",
                "state": "published",
                "limit": 20,
                "before": before,
                "format": "shorts",
            },
        )
        stateless = await client.get(url, params={"state": "library"})
        unknown = await client.get(url, params={"shorts": "some"})
        too_many = await client.get(url, params={"shorts": "only", "limit": 201})
        naive = await client.get(url, params={"before": "2026-10-01T00:00:00"})
    assert [plain.status_code, others.status_code, tab.status_code] == [200, 200, 200]
    calls = [call.kwargs for call in listed.await_args_list]
    assert len(calls) == 3
    assert {
        key: calls[0][key] for key in ("video_format", "shorts", "state", "limit", "before")
    } == {"video_format": None, "shorts": None, "state": None, "limit": None, "before": None}, (
        "asked as before, the list is asked as before"
    )
    assert (calls[1]["shorts"], calls[1]["video_format"]) == ("exclude", "drama")
    assert (calls[2]["shorts"], calls[2]["state"], calls[2]["limit"]) == ("only", "published", 20)
    assert calls[2]["video_format"] == "shorts"
    assert calls[2]["before"] == datetime.fromisoformat(before)
    assert stateless.status_code == 422
    assert stateless.json()["code"] == "video_shorts_state_needs_only"
    assert [unknown.status_code, too_many.status_code, naive.status_code] == [422, 422, 422]
