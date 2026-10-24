"""The five selected MiniMax brand stories validate and keep their series look on import."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.video_automation import stories
from app.video_automation.models import (
    VideoAiRun,
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.schemas import SeriesIn
from app.video_automation.series import add_series, next_job_for
from app.video_media.models import VideoMediaJob

CUTE_LOOK = {"preset": "cute-mystery"}
TABLES = (
    User,
    AdminAuditLog,
    VideoToolToken,
    VideoProject,
    VideoReview,
    VideoMediaJob,
    VideoAiRun,
    VideoAutomationSettings,
    VideoDramaSeries,
    VideoDramaDoc,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaEpisode,
)


def _five_file() -> dict[str, Any]:
    folder = Path(__file__).resolve().parents[3] / "docs/videos/brand-stories-five-20261014"
    series = json.loads((folder / "series.json").read_text(encoding="utf-8"))
    episodes = sorted(
        (
            json.loads(file.read_text(encoding="utf-8"))
            for file in (folder / "episodes").glob("*.json")
        ),
        key=lambda episode: episode["number"],
    )
    return {"schema_version": 1, "series": series, "stories": episodes}


def _everyday_file(
    series_slug: str = stories.EVERYDAY_REVERSALS_SLUG, letter: str = "C"
) -> dict[str, Any]:
    document = deepcopy(_five_file())
    document["series"].update(
        slug=series_slug,
        planned_episodes=20,
    )
    source_rows = document["stories"][:3]
    document["stories"] = [deepcopy(source_rows[(number - 1) % 3]) for number in range(1, 21)]
    proofs = []
    for number, story in enumerate(document["stories"], start=1):
        story.update(
            number=number,
            id=f"{letter}{number:02d}",
            slug=(
                stories.C03_VIDEO_SLUG
                if letter == "C" and number == 3
                else f"story-everyday-test-{letter.lower()}{number:02d}"
            ),
            # X stories may be any category; C stories of this batch are all everyday.
            category="tech" if letter == "X" and number % 2 else "everyday",
            title=f"{letter}{number:02d} everyday test",
            publish={"day": number, "slot": "12:00"},
        )
        author_caveats = story.get("caveats", "")
        source = {key: story[key] for key in stories.STORY_KEYS}
        source["caveats"] = author_caveats
        proofs.append({
            "id": story["id"], "number": number, "reviewer": "test independent reviewer",
            "reviewed": "2026-10-23", "source_story_sha256": stories._json_sha256(source),
            "compiled_story_sha256": stories._json_sha256(story, sorted_keys=True),
            "author_caveats": author_caveats, "review_notes": "",
        })
    document["review_certification"] = {
        "series_slug": series_slug,
        "status": "independent-verified", "entries": proofs,
    }
    return document


def _certify_changed_story(document: dict[str, Any], index: int) -> None:
    """Keep a test fixture's independent-review hashes bound to its changed row."""
    story = document["stories"][index]
    proof = document["review_certification"]["entries"][index]
    source = {key: story[key] for key in stories.STORY_KEYS if key in story}
    source["must_verify"] = [
        {key: value for key, value in claim.items() if key != "reviewer_only"}
        for claim in source["must_verify"]
    ]
    source["caveats"] = proof["author_caveats"]
    proof["source_story_sha256"] = stories._json_sha256(source)
    proof["compiled_story_sha256"] = stories._json_sha256(story, sorted_keys=True)


async def _pause_empty_series(session: AsyncSession, document: dict[str, Any]) -> None:
    fields = {
        key: value
        for key, value in document["series"].items()
        if key in SeriesIn.model_fields
    }
    series = await add_series(session, None, SeriesIn.model_validate(fields))
    series.status = "paused"
    await session.commit()


@pytest.fixture
async def db() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: Base.metadata.create_all(
                sync, tables=[model.__table__ for model in TABLES]
            )
        )
    try:
        yield async_sessionmaker(engine, expire_on_commit=False)
    finally:
        await engine.dispose()


def test_selected_five_episode_fixture_passes_api_schema_and_compiled_import_check() -> None:
    document = _five_file()
    series = document["series"]
    payload = SeriesIn.model_validate(
        {key: value for key, value in series.items() if key in SeriesIn.model_fields}
    )
    assert payload.model_dump()["look"] == CUTE_LOOK
    check = stories.check_story_file(document, series["slug"])
    assert check.problems == [] and check.refused == []
    assert [episode["number"] for episode in check.stories] == [1, 2, 3, 4, 5]


def test_compiled_story_accepts_only_the_matching_ten_minute_cute_route() -> None:
    document = _five_file()
    assert stories.series_problems(document["series"]) == []

    for changes, expected in (
        ({"target_minutes": 13}, "series.target_minutes must be 10"),
        ({"image_model": "gemini-3.1-flash-image"}, 'series.image_model must be "image-01"'),
        ({"style_preset": "cinematic-3d"}, 'series.style_preset must be "custom"'),
        ({"look": {"preset": "cute-mystery", "negative": "extra"}}, "series.look needs a style"),
        (
            {"look": {"preset": "cute-mystery", "style": "flat cartoon", "negative": "logos"}},
            "series.look needs a style",
        ),
        (
            {"look": {"style": "a custom look", "negative": "logos"}},
            "series.target_minutes must be 12 to 15",
        ),
    ):
        invalid = _five_file()
        invalid["series"].update(changes)
        assert expected in "\n".join(
            stories.check_story_file(invalid, invalid["series"]["slug"]).problems
        )


def test_everyday_c_prefix_requires_exact_series_slug() -> None:
    document = _everyday_file()
    everyday = document["stories"][2]
    assert stories.check_story_file(document, stories.EVERYDAY_REVERSALS_SLUG).problems == []
    assert stories.story_problems(everyday, series_slug=stories.EVERYDAY_REVERSALS_SLUG) == []
    assert "category \"everyday\" does not fit id C03 (tech)" in "\n".join(
        stories.story_problems(everyday)
    )
    tech = {**everyday, "category": "tech"}
    assert stories.story_problems(tech) == []
    assert "category \"tech\" does not fit id C03 (everyday)" in "\n".join(
        stories.story_problems(tech, series_slug=stories.EVERYDAY_REVERSALS_SLUG)
    )
    document["series"]["slug"] = "brand-stories-100"
    assert "C03: category \"everyday\" does not fit id C03 (tech)" in "\n".join(
        stories.check_story_file(document, "brand-stories-100").problems
    )


def test_everyday_import_requires_exact_hash_bound_twenty_story_review() -> None:
    document = _everyday_file()
    without_review = deepcopy(document)
    del without_review["review_certification"]
    assert "independent review certification" in "\n".join(
        stories.check_story_file(without_review, stories.EVERYDAY_REVERSALS_SLUG).problems
    )
    shortened = deepcopy(document)
    shortened["stories"] = shortened["stories"][:3]
    shortened["review_certification"]["entries"] = shortened["review_certification"]["entries"][:3]
    assert "exactly twenty stories" in "\n".join(
        stories.check_story_file(shortened, stories.EVERYDAY_REVERSALS_SLUG).problems
    )
    changed = deepcopy(document)
    changed["stories"][0]["chapters"][0]["point"] += "新主張。"
    assert "compiled story changed after independent review" in "\n".join(
        stories.check_story_file(changed, stories.EVERYDAY_REVERSALS_SLUG).problems
    )
    malformed = deepcopy(document)
    malformed["stories"][0]["must_verify"][0] = None
    assert "review certification source is malformed" in "\n".join(
        stories.check_story_file(malformed, stories.EVERYDAY_REVERSALS_SLUG).problems
    )


def test_compiled_everyday_batch_matches_python_import_validation() -> None:
    file = (
        Path(__file__).resolve().parents[3]
        / "docs/videos/brand-stories-everyday-reversals-20261020/stories.json"
    )
    document = json.loads(file.read_text(encoding="utf-8"))
    checked = stories.check_story_file(document, stories.EVERYDAY_REVERSALS_SLUG)
    assert len(checked.stories) == 20
    assert checked.problems == []
    assert checked.ignored == []


def test_company_turns_x_batch_is_review_only_and_x_ids_stay_in_their_series() -> None:
    document = _everyday_file(stories.COMPANY_TURNS_SLUG, "X")
    assert stories.check_story_file(document, stories.COMPANY_TURNS_SLUG).problems == []
    assert "X stories belong to the brand-stories-company-turns series" in "\n".join(
        stories.story_problems(document["stories"][0])
    )
    without_review = deepcopy(document)
    del without_review["review_certification"]
    assert "independent review certification" in "\n".join(
        stories.check_story_file(without_review, stories.COMPANY_TURNS_SLUG).problems
    )
    changed = deepcopy(document)
    changed["stories"][4]["chapters"][0]["point"] += "新主張。"
    assert "X05: compiled story changed after independent review" in "\n".join(
        stories.check_story_file(changed, stories.COMPANY_TURNS_SLUG).problems
    )


def test_compiled_company_turns_batch_matches_python_import_validation() -> None:
    file = (
        Path(__file__).resolve().parents[3]
        / "docs/videos/brand-stories-company-turns-20261024/stories.json"
    )
    document = json.loads(file.read_text(encoding="utf-8"))
    checked = stories.check_story_file(document, stories.COMPANY_TURNS_SLUG)
    assert len(checked.stories) == 20
    assert checked.problems == []
    assert checked.ignored == []


async def test_company_turns_import_creates_paused_planned_rows_without_requests(
    db: async_sessionmaker[AsyncSession],
) -> None:
    document = _everyday_file(stories.COMPANY_TURNS_SLUG, "X")
    async with db() as session:
        session.add(VideoAutomationSettings(id=1, drama_enabled=True))
        await session.commit()
        report = await stories.import_story_rows(
            session, document, series_slug=stories.COMPANY_TURNS_SLUG, apply=True
        )
        assert report.problems == [] and report.written and report.series_created
        assert report.create == [f"X{number:02d}" for number in range(1, 21)]
        series = await session.scalar(select(VideoDramaSeries))
        assert series is not None and series.status == "paused"
        episodes = list((await session.scalars(
            select(VideoDramaEpisode).order_by(VideoDramaEpisode.number)
        )).all())
        assert {row.status for row in episodes} == {"planned"} and len(episodes) == 20
        assert (await session.scalars(select(VideoDramaRequest))).all() == []
        again = await stories.import_story_rows(
            session, document, series_slug=stories.COMPANY_TURNS_SLUG, apply=True
        )
        assert again.problems == [] and not again.written and again.create == []


async def test_everyday_import_creates_paused_series_atomically_and_refuses_active_reimport(
    db: async_sessionmaker[AsyncSession],
) -> None:
    document = _everyday_file()
    async with db() as session:
        dry_run = await stories.import_story_rows(
            session, document, series_slug=stories.EVERYDAY_REVERSALS_SLUG,
            limit=3
        )
        assert not dry_run.written and dry_run.series_created
        assert (await session.scalars(select(VideoDramaSeries))).all() == []
        report = await stories.import_story_rows(
            session, document, series_slug=stories.EVERYDAY_REVERSALS_SLUG,
            apply=True, limit=3
        )
        assert report.written and report.series_created and report.create == ["C01", "C02", "C03"]
        series = await session.scalar(select(VideoDramaSeries))
        assert series is not None and series.status == "paused"
        assert len((await session.scalars(select(VideoDramaEpisode))).all()) == 3
        series.status = "active"
        await session.commit()
        report = await stories.import_story_rows(
            session, document, series_slug=stories.EVERYDAY_REVERSALS_SLUG, apply=True
        )
        assert not report.written
        assert "must have status paused" in "\n".join(report.problems)
        assert len((await session.scalars(select(VideoDramaEpisode))).all()) == 3


async def test_paused_everyday_import_links_existing_c03_without_a_new_request_and_is_idempotent(
    db: async_sessionmaker[AsyncSession],
) -> None:
    document = _everyday_file()
    async with db() as session:
        await _pause_empty_series(session, document)
        project = VideoProject(
            slug=stories.C03_VIDEO_SLUG,
            title="Moleskine",
            format="drama",
            stage="outline approved",
            series_slug=stories.EVERYDAY_REVERSALS_SLUG,
            episode_number=3,
        )
        session.add(project)
        session.add(VideoAutomationSettings(id=1, drama_enabled=True))
        await session.commit()
        project_id = project.id

        report = await stories.import_story_rows(
            session, document, series_slug=stories.EVERYDAY_REVERSALS_SLUG,
            apply=True, limit=3
        )
        assert report.problems == [] and report.written
        assert report.create == ["C01", "C02", "C03"]
        series = await session.scalar(select(VideoDramaSeries))
        assert series is not None and series.status == "paused"
        episode_rows = select(VideoDramaEpisode).order_by(VideoDramaEpisode.number)
        episodes = list((await session.scalars(episode_rows)).all())
        assert [(row.number, row.status) for row in episodes] == [
            (1, "planned"), (2, "planned"), (3, "planned")
        ]
        settings = await session.scalar(select(VideoAutomationSettings))
        assert settings is not None
        assert next_job_for(
            series, [], episodes, settings, started_this_month=0
        ) is None
        series.status = "active"
        assert next_job_for(
            series, [], episodes, settings, started_this_month=0
        ) is None
        series.status = "paused"
        assert (await session.scalars(select(VideoDramaRequest))).all() == []
        assert (await session.scalars(select(VideoProject))).one().id == project_id
        audit_count = len((await session.scalars(select(AdminAuditLog))).all())

        again = await stories.import_story_rows(
            session, document, series_slug=stories.EVERYDAY_REVERSALS_SLUG,
            apply=True, limit=3
        )
        assert again.problems == [] and not again.written
        assert again.unchanged == ["C01", "C02", "C03"]
        assert len((await session.scalars(select(AdminAuditLog))).all()) == audit_count
        assert (await session.scalars(select(VideoDramaRequest))).all() == []

        project.episode_number = 4
        await session.commit()
        changed_identity = await stories.import_story_rows(
            session, document, series_slug=stories.EVERYDAY_REVERSALS_SLUG,
            apply=True, limit=3
        )
        assert not changed_identity.written
        assert "C03: slug story-everyday-moleskine-c03 is already a video" in "\n".join(
            changed_identity.problems
        )
        c03 = await session.scalar(
            select(VideoDramaEpisode).where(VideoDramaEpisode.number == 3)
        )
        assert c03 is not None and c03.status == "planned"


@pytest.mark.parametrize(
    ("project_series", "episode_number"),
    [("other-series", 3), (stories.EVERYDAY_REVERSALS_SLUG, 4)],
)
async def test_c03_slug_conflict_remains_when_video_identity_does_not_match(
    db: async_sessionmaker[AsyncSession], project_series: str, episode_number: int
) -> None:
    document = _everyday_file()
    async with db() as session:
        await _pause_empty_series(session, document)
        session.add(
            VideoProject(
                slug=stories.C03_VIDEO_SLUG,
                title="Another video",
                format="drama",
                stage="outline approved",
                series_slug=project_series,
                episode_number=episode_number,
            )
        )
        await session.commit()
        report = await stories.import_story_rows(
            session, document, series_slug=stories.EVERYDAY_REVERSALS_SLUG, apply=True
        )
        assert not report.written
        assert "C03: slug story-everyday-moleskine-c03 is already a video" in "\n".join(
            report.problems
        )
        assert (await session.scalars(select(VideoDramaEpisode))).all() == []


async def test_existing_video_slug_is_not_reused_for_other_everyday_episodes(
    db: async_sessionmaker[AsyncSession],
) -> None:
    document = _everyday_file()
    async with db() as session:
        await _pause_empty_series(session, document)
        session.add(
            VideoProject(
                slug=document["stories"][0]["slug"],
                title="Existing C01 card",
                format="drama",
                stage="outline approved",
                series_slug=stories.EVERYDAY_REVERSALS_SLUG,
                episode_number=1,
            )
        )
        await session.commit()
        report = await stories.import_story_rows(
            session, document, series_slug=stories.EVERYDAY_REVERSALS_SLUG, apply=True
        )
        assert not report.written
        assert "C01: slug story-everyday-test-c01 is already a video" in "\n".join(
            report.problems
        )
        assert (await session.scalars(select(VideoDramaEpisode))).all() == []


async def test_c08_approved_short_slug_reuses_only_the_planned_episode_row(
    db: async_sessionmaker[AsyncSession],
) -> None:
    original = _everyday_file()
    original["stories"][7]["slug"] = stories.C08_ORIGINAL_VIDEO_SLUG
    _certify_changed_story(original, 7)
    revised = deepcopy(original)
    revised["stories"][7]["slug"] = stories.C08_SHORT_VIDEO_SLUG
    _certify_changed_story(revised, 7)

    async with db() as session:
        session.add(VideoAutomationSettings(id=1, drama_enabled=True))
        first = await stories.import_story_rows(
            session, original, series_slug=stories.EVERYDAY_REVERSALS_SLUG, apply=True
        )
        assert first.problems == [] and first.create == [f"C{i:02d}" for i in range(1, 21)]
        rows = list((await session.scalars(
            select(VideoDramaEpisode).order_by(VideoDramaEpisode.number)
        )).all())
        before = [(row.id, row.number, row.slug, deepcopy(row.beats)) for row in rows]
        old_video = VideoProject(
            slug=stories.C08_ORIGINAL_VIDEO_SLUG,
            title="Original approved C08 video",
            format="drama",
            stage="outline approved",
            series_slug=stories.EVERYDAY_REVERSALS_SLUG,
            episode_number=8,
        )
        session.add(old_video)
        await session.commit()
        old_video_id = old_video.id

        dry_run = await stories.import_story_rows(
            session, revised, series_slug=stories.EVERYDAY_REVERSALS_SLUG
        )
        assert dry_run.problems == [] and not dry_run.written
        assert dry_run.update == ["C08"] and dry_run.create == []
        assert dry_run.unchanged == [f"C{i:02d}" for i in range(1, 21) if i != 8]
        assert rows[7].slug == stories.C08_ORIGINAL_VIDEO_SLUG

        applied = await stories.import_story_rows(
            session, revised, series_slug=stories.EVERYDAY_REVERSALS_SLUG, apply=True
        )
        assert applied.problems == [] and applied.written
        assert applied.update == ["C08"] and applied.create == []
        after = list((await session.scalars(
            select(VideoDramaEpisode).order_by(VideoDramaEpisode.number)
        )).all())
        assert len(after) == 20
        assert after[7].id == before[7][0]
        assert after[7].slug == stories.C08_SHORT_VIDEO_SLUG
        assert after[7].status == "planned" and after[7].request_id is None
        assert [(row.id, row.number, row.slug, row.beats) for row in after if row.number != 8] == [
            values for values in before if values[1] != 8
        ]
        assert (await session.scalar(
            select(VideoProject.id).where(VideoProject.slug == stories.C08_ORIGINAL_VIDEO_SLUG)
        )) == old_video_id
        assert (await session.scalars(select(VideoDramaRequest))).all() == []


async def test_c08_short_slug_refuses_foreign_old_slug_or_started_row(
    db: async_sessionmaker[AsyncSession],
) -> None:
    original = _everyday_file()
    original["stories"][7]["slug"] = stories.C08_ORIGINAL_VIDEO_SLUG
    _certify_changed_story(original, 7)
    revised = deepcopy(original)
    revised["stories"][7]["slug"] = stories.C08_SHORT_VIDEO_SLUG
    _certify_changed_story(revised, 7)
    async with db() as session:
        first = await stories.import_story_rows(
            session, original, series_slug=stories.EVERYDAY_REVERSALS_SLUG, apply=True
        )
        assert first.problems == [] and first.written
        c08 = await session.scalar(
            select(VideoDramaEpisode).where(VideoDramaEpisode.number == 8)
        )
        assert c08 is not None
        c08.slug = "story-everyday-kikkoman-c08-other"
        await session.commit()
        foreign = await stories.import_story_rows(
            session, revised, series_slug=stories.EVERYDAY_REVERSALS_SLUG, apply=True
        )
        assert not foreign.written
        assert (
            "existing review-only episode #8 does not match the certified batch"
            in foreign.problems
        )
        assert c08.slug == "story-everyday-kikkoman-c08-other"

        c08.slug = stories.C08_ORIGINAL_VIDEO_SLUG
        c08.status = "ready"
        await session.commit()
        started = await stories.import_story_rows(
            session, revised, series_slug=stories.EVERYDAY_REVERSALS_SLUG, apply=True
        )
        assert not started.written
        assert "existing review-only episode #8 has advanced beyond planned" in started.problems
        assert c08.slug == stories.C08_ORIGINAL_VIDEO_SLUG

        c08.status = "planned"
        session.add(VideoProject(
            slug=stories.C08_SHORT_VIDEO_SLUG,
            title="Conflicting video",
            format="drama",
            stage="outline approved",
            series_slug="another-series",
            episode_number=8,
        ))
        await session.commit()
        conflict = await stories.import_story_rows(
            session, revised, series_slug=stories.EVERYDAY_REVERSALS_SLUG, apply=True
        )
        assert not conflict.written
        assert (
            f"C08: slug {stories.C08_SHORT_VIDEO_SLUG} is already a video on /admin/videos"
            in conflict.problems
        )
        assert c08.slug == stories.C08_ORIGINAL_VIDEO_SLUG


async def test_everyday_reimport_refuses_advanced_or_foreign_rows(
    db: async_sessionmaker[AsyncSession],
) -> None:
    document = _everyday_file()
    async with db() as session:
        await _pause_empty_series(session, document)
        first = await stories.import_story_rows(
            session, document, series_slug=stories.EVERYDAY_REVERSALS_SLUG,
            apply=True, limit=3,
        )
        assert first.problems == [] and first.written
        rows = list((await session.scalars(select(VideoDramaEpisode))).all())
        rows[0].status = "ready"
        await session.commit()
        advanced = await stories.import_story_rows(
            session, document, series_slug=stories.EVERYDAY_REVERSALS_SLUG, apply=True,
        )
        assert not advanced.written
        assert "advanced beyond planned" in "\n".join(advanced.problems)

        rows[0].status = "planned"
        series = await session.scalar(select(VideoDramaSeries))
        assert series is not None
        extra = VideoDramaEpisode(
            series_id=series.id, number=21, chapter_number=1, title="Unexpected",
            logline="Unexpected", slug="story-everyday-unexpected-c21",
            beats={"id": "C21"}, status="planned",
        )
        session.add(extra)
        await session.commit()
        foreign = await stories.import_story_rows(
            session, document, series_slug=stories.EVERYDAY_REVERSALS_SLUG, apply=True,
        )
        assert not foreign.written
        assert "does not match the certified batch" in "\n".join(foreign.problems)


async def test_import_creates_the_cute_story_series_without_rewriting_look(
    db: async_sessionmaker[AsyncSession],
) -> None:
    document = _five_file()
    async with db() as session:
        report = await stories.import_story_rows(
            session, document, series_slug=document["series"]["slug"], apply=True, limit=1
        )
    assert report.problems == [] and report.written and report.series_created
    async with db() as session:
        series = await session.scalar(select(VideoDramaSeries))
        assert series is not None
        assert (series.target_minutes, series.image_model, series.style_preset) == (
            10,
            "image-01",
            "custom",
        )
        assert series.look == CUTE_LOOK
