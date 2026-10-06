"""Worker handoff evidence must not masquerade as running work or finished media."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import select

from app.models import VideoProject, VideoReview
from app.video_reviews import admin_service as service
from app.video_reviews.producer_state import MAX_STATE_BYTES, worker_state
from tests.test_video_review_renewal import SLUG, Site
from tests.test_video_review_renewal import site as _site

site = _site


def _state(base: Path, status: str, slug: str = SLUG) -> Path:
    project = base / slug
    project.mkdir(parents=True, exist_ok=True)
    path = project / "auto.json"
    path.write_text(json.dumps({"slug": slug, "status": status}), encoding="utf-8")
    return path


def test_absent_registration_is_distinct_from_an_unavailable_mount(tmp_path: Path) -> None:
    assert worker_state(None, SLUG) == "unavailable"
    assert worker_state(str(tmp_path / "absent"), SLUG) == "unavailable"
    assert worker_state(str(tmp_path), SLUG) == "not_adopted"
    assert list(tmp_path.iterdir()) == [], "a read must not create or enqueue a project"


@pytest.mark.parametrize(
    ("status", "expected"),
    [("active", "registered"), ("done", "done"), ("blocked", "blocked"), ("dropped", "dropped")],
)
def test_persisted_status_is_not_a_heartbeat(tmp_path: Path, status: str, expected: str) -> None:
    path = _state(tmp_path, status)
    before = path.read_bytes()
    assert worker_state(str(tmp_path), SLUG) == expected
    assert path.read_bytes() == before
    assert sorted(p.name for p in path.parent.iterdir()) == ["auto.json"]


@pytest.mark.parametrize("global_stop", [True, False])
def test_stop_is_visible_but_does_not_hide_a_recorded_blocker(
    tmp_path: Path, global_stop: bool
) -> None:
    path = _state(tmp_path, "active")
    (tmp_path if global_stop else path.parent).joinpath("STOP").touch()
    assert worker_state(str(tmp_path), SLUG) == "stopped"
    _state(tmp_path, "blocked")
    assert worker_state(str(tmp_path), SLUG) == "blocked"
    path.unlink()
    assert worker_state(str(tmp_path), SLUG) == "not_adopted"


@pytest.mark.parametrize(
    "raw",
    [
        b"{",
        b"\xff",
        b"[]",
        b"null",
        b"x" * (MAX_STATE_BYTES + 1),
        b'{"slug":"different","status":"active"}',
        json.dumps({"slug": SLUG, "status": "running"}).encode(),
        json.dumps({"slug": SLUG, "status": []}).encode(),
    ],
    ids=[
        "partial-json",
        "invalid-utf8",
        "array",
        "null",
        "oversized",
        "wrong-slug",
        "unknown-status",
        "invalid-status",
    ],
)
def test_bad_or_unbound_states_are_unavailable(tmp_path: Path, raw: bytes) -> None:
    path = _state(tmp_path, "active")
    path.write_bytes(raw)
    assert worker_state(str(tmp_path), SLUG) == "unavailable"


@pytest.mark.parametrize("slug", ["../outside", "UPPER", "", "a" * 81])
def test_invalid_project_names_are_refused(tmp_path: Path, slug: str) -> None:
    assert worker_state(str(tmp_path), slug) == "unavailable"


def test_symlinks_must_not_read_state_outside_the_work_mount(tmp_path: Path) -> None:
    base = tmp_path / "work"
    base.mkdir()
    outside = tmp_path / "outside"
    _state(outside, "active")
    try:
        (base / SLUG).symlink_to(outside / SLUG, target_is_directory=True)
    except OSError:
        pytest.skip("this platform cannot create directory symlinks")
    assert worker_state(str(base), SLUG) == "unavailable"


def test_within_mount_project_symlink_is_not_registered_by_the_worker(tmp_path: Path) -> None:
    base = tmp_path / "work"
    base.mkdir()
    target = _state(base / "original", "active").parent
    assert target.is_relative_to(base)
    try:
        (base / SLUG).symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("this platform cannot create directory symlinks")
    # The target's auto.json has the requested slug, but the worker does not enumerate
    # the symlink as a directory. Containment and JSON identity alone are insufficient.
    assert json.loads((target / "auto.json").read_text(encoding="utf-8"))["slug"] == SLUG
    assert worker_state(str(base), SLUG) == "unavailable"


@pytest.mark.skipif(sys.platform != "win32", reason="NTFS junctions are Windows-only")
def test_within_mount_project_junction_is_not_registered_by_the_worker(tmp_path: Path) -> None:
    base = tmp_path / "work"
    base.mkdir()
    target = _state(base / "original", "active").parent
    entry = base / SLUG
    command = shutil.which("cmd.exe")
    assert command is not None and Path(command).is_absolute()
    subprocess.run(
        [command, "/c", "mklink", "/J", str(entry), str(target)],
        check=True,
        capture_output=True,
    )
    assert entry.is_junction() and target.is_relative_to(base)
    assert json.loads((entry / "auto.json").read_text(encoding="utf-8"))["slug"] == SLUG
    assert worker_state(str(base), SLUG) == "unavailable"


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [None, "active", "blocked", "done"])
async def test_list_and_detail_show_handoff_without_changing_review_results(
    site: Site, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, status: str | None
) -> None:
    monkeypatch.setattr(service, "spend_by_slug", AsyncMock(return_value={}))
    now = datetime.now(UTC)
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        project.format, project.shorts_line = "slides", None
        project.locales = {"en": {"metadata": True, "captions": True}}
        project.locales_decided_at = now
        for gate, payload in (
            ("final", {}),
            ("publish", {}),
            ("languages", {"locales": {"en": {"metadata": "ready"}}}),
        ):
            session.add(
                VideoReview(
                    project_id=project.id,
                    gate=gate,
                    content_sha256="a" * 64,
                    summary=gate,
                    payload=payload,
                    files=[],
                    status="approved",
                    decided_at=now,
                )
            )
        await session.commit()
        before = await service.project_view(session, SLUG)
        if status is not None:
            _state(tmp_path, status)
        detail = await service.project_view(session, SLUG, str(tmp_path))
        listed = await service.list_projects(session, work_dir=str(tmp_path))
        browsed = await service.browse_projects(session, work_dir=str(tmp_path))
        expected = {
            None: "not_adopted",
            "active": "registered",
            "blocked": "blocked",
            "done": "done",
        }[status]
        assert (
            detail.worker_state
            == listed[0].worker_state
            == browsed.items[0].worker_state
            == expected
        )
        assert detail.model_dump(exclude={"worker_state"}) == before.model_dump(
            exclude={"worker_state"}
        )
        assert detail.languages["en"]["metadata"].state == "ready"
        assert detail.languages["en"]["captions"].state == "working"
        assert not detail.ready_to_upload and detail.youtube_video_id is None
        assert all(review.status == "approved" for review in detail.reviews)


@pytest.mark.asyncio
async def test_shorts_keep_their_independent_producer_state(
    site: Site, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "spend_by_slug", AsyncMock(return_value={}))
    _state(tmp_path, "blocked")
    async with site.factory() as session:
        detail = await service.project_view(session, SLUG, str(tmp_path))
        listed = await service.list_projects(session, work_dir=str(tmp_path))
        assert detail.worker_state is None and listed[0].worker_state is None
