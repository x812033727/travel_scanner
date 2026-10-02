"""Imported planning rows retain the authored scope but cannot become production jobs."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
import sqlalchemy as sa
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import User, VideoToolToken
from app.video_automation import series as service
from app.video_automation.models import VideoAutomationSettings, VideoDramaDoc, VideoDramaSeries
from app.video_automation.schemas import (
    SeriesDocEditIn,
    SeriesDocSubmitIn,
    SeriesEpisodeEditIn,
    SeriesEpisodeRecapIn,
    SeriesIn,
    SeriesPatch,
)

WHEN = datetime(2026, 10, 2, tzinfo=UTC)


def planning_series(**changes: Any) -> VideoDramaSeries:
    values: dict[str, Any] = dict(
        id=uuid4(),
        slug="borrowed-dawn",
        title="借來的黎明",
        premise="原創異世界長篇",
        kind="series",
        category="anime",
        planning_only=True,
        planning_spec={"runtime": {"story_minutes": 22}, "lead": "ensemble"},
        target_minutes=22,
        planned_episodes=120,
        episodes_per_chapter=12,
        tone="no-romance",
        style_preset="anime-2d",
        genre="custom",
        lead="ensemble",
        aspects=["world", "structure"],
        status="paused",
        hands_off=False,
        compilation=False,
        force_next=False,
        requested_chapter=None,
        open_ended=False,
        created_at=WHEN,
        updated_at=WHEN,
    )
    values.update(changes)
    return VideoDramaSeries(**values)


@pytest.mark.parametrize("status", ["paused", "active", "setting", "finished"])
def test_planning_never_advertises_a_job_even_if_in_memory_status_is_wrong(status: str) -> None:
    series = planning_series(status=status, compilation=True)
    assert (
        service.next_job_for(series, [], [], VideoAutomationSettings(), started_this_month=0)
        is None
    )
    assert not service.finish_if_complete(series, [], WHEN)


def test_summary_preserves_real_runtime_classification_and_original_spec() -> None:
    summary = service.summary_view(planning_series(), [], [])
    assert summary.target_minutes == 22
    assert summary.lead == "ensemble"
    assert summary.category == "anime"
    assert summary.planning_only
    assert summary.planning_spec == {"runtime": {"story_minutes": 22}, "lead": "ensemble"}
    assert summary.status == "paused" and summary.chapters == 10


@pytest.mark.parametrize(
    "field,value",
    [
        ("planning_only", True),
        ("category", "anime"),
        ("planning_spec", {}),
        ("lead", "ensemble"),
    ],
)
def test_ordinary_create_and_patch_cannot_set_importer_only_fields(field: str, value: Any) -> None:
    with pytest.raises(ValidationError):
        SeriesIn.model_validate({"premise": "x", field: value})
    with pytest.raises(ValidationError):
        SeriesPatch.model_validate({field: value})


@pytest.mark.parametrize("minutes", [9, 20, 22])
def test_ordinary_drama_runtime_limits_stay_in_place(minutes: int) -> None:
    with pytest.raises(ValidationError):
        SeriesIn.model_validate({"premise": "x", "target_minutes": minutes})
    assert SeriesIn(premise="x", target_minutes=8).target_minutes == 8


@pytest.mark.parametrize(
    "changes",
    [
        {"status": "active"},
        {"hands_off": True},
        {"compilation": True},
        {"target_minutes": 8},
        {"planned_episodes": 121},
        {"title": "改稿"},
    ],
)
def test_planning_patches_are_refused(changes: dict[str, Any]) -> None:
    refusal = service.patch_problem(planning_series(), changes)
    assert refusal and (refusal.status, refusal.code) == (409, "video_series_planning_only")


@pytest.mark.parametrize(
    "operation",
    [
        "patch",
        "decide",
        "edit-doc",
        "edit-episode",
        "act",
        "skip",
        "restore",
        "redo",
        "submit",
        "start",
        "recap",
        "finish",
        "compile",
        "finish-compile",
        "apply-approval",
    ],
)
@pytest.mark.asyncio
async def test_direct_mutation_routes_refuse_before_writes(
    operation: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    row = planning_series()
    session = MagicMock()
    session.commit = AsyncMock()
    monkeypatch.setattr(service, "_series", AsyncMock(return_value=row))
    actor = User(id=uuid4())
    token = VideoToolToken(id=uuid4())
    calls: dict[str, Any] = {
        "patch": lambda: service.patch_series(
            session, actor, row.slug, SeriesPatch(status="active")
        ),
        "decide": lambda: service.decide_doc(
            session, actor, row.slug, "setting", 0, "approve", None, expected_version=1
        ),
        "edit-doc": lambda: service.edit_doc(
            session, actor, row.slug, "setting", 0, SeriesDocEditIn(body_md="# edit", approve=True)
        ),
        "edit-episode": lambda: service.edit_episode(
            session, actor, row.slug, 1, SeriesEpisodeEditIn(title="edit")
        ),
        "act": lambda: service.act(session, actor, row.slug, "start-next"),
        "skip": lambda: service.skip_episode(session, actor, row.slug, 1),
        "restore": lambda: service.restore_episode(session, actor, row.slug, 1),
        "redo": lambda: service.redo_episode(session, actor, row.slug, 1),
        "submit": lambda: service.submit_doc(
            session, row.slug, SeriesDocSubmitIn(kind="setting", body_md="# edit")
        ),
        "start": lambda: service.start_episode(session, token, row.slug, 1, "dawn-e001"),
        "recap": lambda: service.recap_episode(
            session, row.slug, 1, SeriesEpisodeRecapIn(recap="fake completion")
        ),
        "finish": lambda: service.finish_episode(session, row.slug, 1),
        "compile": lambda: service.start_compilation(session, token, row.slug, "dawn-full"),
        "finish-compile": lambda: service.finish_compilation(session, row.slug),
        "apply-approval": lambda: service._apply_approval(  # noqa: SLF001
            session, row, VideoDramaDoc(kind="outline", body_json={})
        ),
    }
    with pytest.raises(service.SeriesRefused) as caught:
        await calls[operation]()
    assert (caught.value.status, caught.value.code) == (409, "video_series_planning_only")
    session.add.assert_not_called()
    session.commit.assert_not_awaited()


@pytest.mark.parametrize(
    "changes",
    [
        {"planning_only": False},
        {"status": "active"},
        {"category": None},
        {"category": "drama"},
        {"kind": "story"},
        {"hands_off": True},
        {"compilation": True},
        {"force_next": True},
        {"requested_chapter": 1},
        {"target_minutes": 31},
        {"lead": "invalid"},
    ],
)
def test_model_checks_block_raw_sql_bypasses(changes: dict[str, Any]) -> None:
    engine = sa.create_engine("sqlite://")
    try:
        cast(sa.Table, VideoDramaSeries.__table__).create(engine)
        with Session(engine) as session:
            row = planning_series()
            session.add(row)
            session.commit()
            assignments = ", ".join(f"{key} = :{key}" for key in changes)
            with pytest.raises(IntegrityError):
                session.execute(sa.text(f"UPDATE video_drama_series SET {assignments}"), changes)
            session.rollback()
            stored = session.get(VideoDramaSeries, row.id)
            assert stored and stored.target_minutes == 22 and stored.planning_only
    finally:
        engine.dispose()


def test_existing_production_defaults_and_database_runtime_are_unchanged() -> None:
    engine = sa.create_engine("sqlite://")
    try:
        cast(sa.Table, VideoDramaSeries.__table__).create(engine)
        with Session(engine) as session:
            row = planning_series(
                planning_only=False,
                category=None,
                planning_spec=None,
                target_minutes=20,
                lead="male",
                status="active",
            )
            session.add(row)
            session.commit()
            with pytest.raises(IntegrityError):
                session.execute(sa.text("UPDATE video_drama_series SET target_minutes = 21"))
            session.rollback()
            assert not row.planning_only and row.target_minutes == 20
    finally:
        engine.dispose()
