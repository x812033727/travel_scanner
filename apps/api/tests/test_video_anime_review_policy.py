"""Long-anime review capacity and runtime proofs stay bound to the server's episode."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.models import User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError
from app.video_automation.models import VideoDramaEpisode, VideoDramaSeries
from app.video_reviews import admin_service
from app.video_reviews.schemas import DecisionIn, ReviewIn
from app.video_reviews.storage import ReviewStore

RUNTIME = {
    "body_target_seconds": 1320,
    "op_ed_budget_seconds": 180,
    "broadcast_slot_seconds": 1800,
    "slot_reserve_seconds": 300,
}
SHA = "a" * 64


def native() -> tuple[VideoDramaSeries, VideoDramaEpisode, dict[str, Any]]:
    series = VideoDramaSeries(
        id=uuid4(),
        slug="borrowed-dawn-production",
        kind="series",
        genre="custom",
        lead="ensemble",
        planned_episodes=120,
        open_ended=False,
        category="anime",
        style_preset="anime-2d",
        production_policy="long-anime-v1",
        runtime_spec=RUNTIME,
        planning_only=False,
    )
    episode = VideoDramaEpisode(
        id=uuid4(),
        series_id=series.id,
        number=120,
        chapter_number=10,
        slug="borrowed-dawn-production-120",
        beats={"closed_ending": True},
    )
    context = {
        "slug": series.slug,
        "episode": 120,
        "chapter": 10,
        "planned_episodes": 120,
        "open_ended": False,
        "closed_ending": True,
        "kind": "series",
        "genre": "custom",
        "lead": "ensemble",
    }
    canonical = [
        "long-anime-v1",
        [[key, RUNTIME[key]] for key in admin_service.ANIME_RUNTIME_KEYS],
        "anime",
        "anime-2d",
        [[key, context[key]] for key in admin_service.ANIME_CONTEXT_KEYS],
    ]
    policy_hash = hashlib.sha256(
        json.dumps(canonical, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()
    proof = {
        "basis": "measured",
        "production_policy": "long-anime-v1",
        "runtime_spec": deepcopy(RUNTIME),
        "runtime_context": context,
        "policy_hash": policy_hash,
        "fps": 30,
        "body_frames": 39600,
        "op_ed_frames": 900,
        "presentation_frames": 40500,
        "body_seconds": 1320,
        "op_ed_seconds": 30,
        "presentation_seconds": 1350,
        "speech_hash": "b" * 16,
        "final_sha256": SHA,
    }
    payload = {
        "production_policy": "long-anime-v1",
        "runtime_spec": deepcopy(RUNTIME),
        "runtime_context": context,
        "runtime_policy_hash": policy_hash,
        "runtime_proof": proof,
        "qa": {
            "final_sha256": SHA,
            "policy_hash": policy_hash,
            "runtime_spec": deepcopy(RUNTIME),
            "runtime_context": context,
        },
        "final_media_sha256": SHA,
    }
    return series, episode, payload


def test_long_script_has_bounded_capacity_only_with_an_explicit_valid_profile() -> None:
    _, _, payload = native()
    payload["scenes"] = [{"data": {"prompt": "景" * 100000}}]
    base = {"gate": "script", "summary": "22 分鐘劇本", "content_sha256": SHA}
    assert ReviewIn.model_validate({**base, "payload": payload})
    for update in (
        {"production_policy": None},
        {"runtime_spec": {**RUNTIME, "body_target_seconds": True}},
        {"runtime_context": {"kind": "series", "genre": "custom", "lead": "double"}},
    ):
        with pytest.raises(ValueError, match="payload is larger"):
            ReviewIn.model_validate({**base, "payload": {**payload, **update}})
    with pytest.raises(ValueError, match="payload is larger"):
        ReviewIn.model_validate({**base, "gate": "final", "payload": payload})
    payload["scenes"][0]["data"]["prompt"] = "景" * 400000
    with pytest.raises(ValueError, match="payload is larger"):
        ReviewIn.model_validate({**base, "payload": payload})


def test_measured_final_and_publish_proofs_match_declared_closed_episode() -> None:
    series, episode, payload = native()
    for gate in ("script", "audio", "final", "publish"):
        assert admin_service.anime_review_problem(gate, payload, SHA, series, episode) is None
    payload["manual_review_qa"] = payload.pop("qa")
    assert admin_service.anime_review_problem("final", payload, SHA, series, episode) is None
    assert admin_service.anime_review_problem("final", {}, SHA, series, episode)
    assert admin_service.anime_review_problem("script", payload, SHA, None, None)
    # Filing an ordinary video as anime does not grant a native envelope or runtime exemption.
    series.production_policy = None
    assert admin_service.anime_review_problem("final", payload, SHA, series, episode)
    assert admin_service.anime_review_problem("final", {}, SHA, series, episode) is None


@pytest.mark.parametrize(
    "mutation",
    [
        {"basis": "estimated"},
        {"final_sha256": "c" * 64},
        {"policy_hash": "c" * 64},
        {"speech_hash": "old"},
        {"fps": True},
        {"fps": 24},
        {"body_frames": True},
        {"body_frames": 10**400, "body_seconds": 0},
        {"body_seconds": 1321},
        {"presentation_frames": 40501},
        {"runtime_context": {"episode": 1}},
        {"runtime_spec": {**RUNTIME, "slot_reserve_seconds": 0}},
    ],
)
def test_missing_stale_or_self_inconsistent_measurement_cannot_be_approved(mutation) -> None:
    series, episode, payload = native()
    payload["runtime_proof"].update(mutation)
    assert admin_service.anime_review_problem("final", payload, SHA, series, episode)


@pytest.mark.parametrize(
    "body,oped,accepted",
    [
        (1260, 30, True),
        (1380, 30, True),
        (1259, 30, False),
        (1381, 30, False),
        (1320, 180, True),
        (1320, 181, False),
        (1380, 180, False),
    ],
)
def test_body_and_bookends_have_separate_frame_boundaries(body, oped, accepted) -> None:
    series, episode, payload = native()
    proof = payload["runtime_proof"]
    proof.update(
        body_frames=body * 30,
        body_seconds=body,
        op_ed_frames=oped * 30,
        op_ed_seconds=oped,
        presentation_frames=(body + oped) * 30,
        presentation_seconds=body + oped,
    )
    problem = admin_service.anime_review_problem("final", payload, SHA, series, episode)
    assert (problem is None) is accepted


def test_server_identity_and_quiet_finale_cannot_be_forged_in_review_payload() -> None:
    series, episode, payload = native()
    payload["runtime_context"] = {**payload["runtime_context"], "episode": 119}
    assert admin_service.anime_review_problem("script", payload, SHA, series, episode)
    _, _, payload = native()
    episode.beats = {"closed_ending": False}
    assert admin_service.anime_review_problem("final", payload, SHA, series, episode)
    _, _, payload = native()
    assert admin_service.anime_review_problem("final", payload, SHA, series, None)
    episode.beats = []
    assert admin_service.anime_review_problem("final", payload, SHA, series, episode)


@pytest.mark.asyncio
async def test_manual_approval_checks_actual_server_profile_even_when_payload_omits_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    series, episode, _ = native()
    project = VideoProject(
        id=uuid4(),
        slug=episode.slug,
        series_slug=series.slug,
        episode_number=120,
    )
    review = VideoReview(
        id=uuid4(),
        project_id=project.id,
        gate="final",
        status="pending",
        content_sha256=SHA,
        payload={},
    )
    session = MagicMock(scalar=AsyncMock(side_effect=[review, series, episode]), commit=AsyncMock())
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    with pytest.raises(AppError) as refused:
        await admin_service.decide(
            session, project.slug, review.id, User(id=uuid4()), DecisionIn(decision="approve")
        )
    assert refused.value.code == "video_anime_runtime_invalid"
    assert review.status == "pending"
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_submission_checks_runtime_before_idempotency_or_auto_approval(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    series, episode, _ = native()
    project = VideoProject(
        id=uuid4(),
        slug=episode.slug,
        series_slug=series.slug,
        episode_number=120,
    )
    session = MagicMock(scalar=AsyncMock(side_effect=[series, episode]), commit=AsyncMock())
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    store = ReviewStore(tmp_path, max_file_bytes=1000, max_total_bytes=10000)
    with pytest.raises(AppError) as refused:
        await admin_service.submit_review(
            session,
            store,
            project.slug,
            ReviewIn(gate="final", summary="old receipt", content_sha256=SHA),
            VideoToolToken(id=uuid4()),
        )
    assert refused.value.code == "video_anime_runtime_invalid"
    session.add.assert_not_called()
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_publish_requires_current_approved_final_with_the_exact_measured_receipt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    series, episode, payload = native()
    project = VideoProject(
        id=uuid4(),
        slug=episode.slug,
        series_slug=series.slug,
        episode_number=120,
    )
    final = VideoReview(gate="final", status="approved", content_sha256=SHA, payload=payload)
    session = MagicMock(scalar=AsyncMock(side_effect=[series, episode]))
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=[final]))
    await admin_service._check_anime_review(session, project, "publish", payload, "d" * 64)
    final.status = "pending"
    session.scalar = AsyncMock(side_effect=[series, episode])
    with pytest.raises(AppError) as refused:
        await admin_service._check_anime_review(session, project, "publish", payload, "d" * 64)
    assert refused.value.code == "video_anime_final_review_stale"


def test_real_node_runtime_hash_agrees_with_the_api_episode_binding() -> None:
    series, episode, payload = native()
    video = {
        "format": "drama",
        "category": "anime",
        "look": {"preset": "anime-2d"},
        "target_minutes": [22, 22],
        "production_policy": payload["production_policy"],
        "runtime_spec": RUNTIME,
        "series": payload["runtime_context"],
    }
    node = shutil.which("node")
    assert node is not None
    output = subprocess.check_output(
        [
            node,
            "--input-type=module",
            "-e",
            "import{readFileSync}from'node:fs';"
            "import{runtimePolicyHash}from'./tools/video/core/anime-policy.mjs';"
            "process.stdout.write(runtimePolicyHash(JSON.parse(readFileSync(0,'utf8'))));",
        ],
        cwd=Path(__file__).resolve().parents[3],
        input=json.dumps(video),
        text=True,
    )
    assert output == payload["runtime_policy_hash"]
    assert admin_service.anime_review_problem("final", payload, SHA, series, episode) is None


@pytest.mark.asyncio
async def test_worker_relabelling_cannot_hide_the_server_created_native_episode() -> None:
    series, episode, _ = native()
    for relabel in (None, "ordinary-series", "does-not-exist"):
        project = VideoProject(
            id=uuid4(),
            slug=episode.slug,
            series_slug=relabel,
            episode_number=120,
        )
        session = MagicMock(scalar=AsyncMock(return_value=series))
        with pytest.raises(AppError) as refused:
            await admin_service._check_anime_review(session, project, "final", {}, SHA)
        assert refused.value.code == "video_anime_runtime_invalid"


@pytest.mark.asyncio
@pytest.mark.parametrize("gate", ["script", "audio", "look", "storyboard", "final", "languages"])
async def test_native_submissions_wait_for_the_owner_even_when_global_shortcuts_are_on(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    gate: str,
) -> None:
    series, episode, payload = native()
    project = VideoProject(
        id=uuid4(),
        slug=episode.slug,
        series_slug=series.slug,
        episode_number=120,
        format="drama",
    )
    session = MagicMock(scalar=AsyncMock(side_effect=[series, episode]), commit=AsyncMock())
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=[]))
    shortcuts = []
    for name in (
        "auto_approves_audio",
        "auto_approves_storyboard",
        "auto_picks_look",
        "auto_approves_script",
        "auto_picks_outline",
        "auto_approves_final",
    ):
        shortcut = AsyncMock(return_value=True)
        monkeypatch.setattr(admin_service, name, shortcut)
        shortcuts.append(shortcut)
    review = await admin_service.submit_review(
        session,
        ReviewStore(tmp_path, max_file_bytes=1000, max_total_bytes=10000),
        project.slug,
        ReviewIn(gate=gate, summary="待站主審核", content_sha256=SHA, payload=payload),
        VideoToolToken(id=uuid4()),
    )
    assert review.status == "pending" and review.decided_at is None
    for shortcut in shortcuts:
        shortcut.assert_not_awaited()


def test_json_booleans_cannot_impersonate_runtime_or_episode_integers() -> None:
    series, episode, payload = native()
    episode.number = 1
    episode.beats = {"closed_ending": False}
    payload["runtime_context"] = {**payload["runtime_context"], "episode": True}
    assert admin_service.anime_review_problem("script", payload, SHA, series, episode)
    series.runtime_spec = {**RUNTIME, "op_ed_budget_seconds": 0, "slot_reserve_seconds": 480}
    payload["runtime_spec"] = {**series.runtime_spec, "op_ed_budget_seconds": False}
    assert not admin_service._same_anime_runtime(payload["runtime_spec"], series.runtime_spec)
