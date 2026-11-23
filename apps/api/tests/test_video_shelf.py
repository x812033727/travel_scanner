"""The review catalog's shows, series and topics (app/video_reviews/shelf.py, migration 0147)."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest
import pytest_asyncio

from app.db import SessionFactory, engine
from app.models import User, VideoProject
from app.video_backup import target
from app.video_reviews import admin_service as service
from app.video_reviews import shelf
from app.video_reviews.schemas import CategoryIn, ProjectIn
from app.video_reviews.storage import ReviewStore

POSTGRES = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


def _project(slug: str, **fields: Any) -> VideoProject:
    return VideoProject(slug=slug, title=slug, stage="outline", **fields)


@pytest.mark.parametrize(
    ("slug", "fields", "expected"),
    [
        ("curio-h01", {"category": "explainer"}, ("curio", "H-歷史懸案")),
        ("curio-h01-v2", {"category": "explainer"}, ("curio", "H-歷史懸案")),
        ("curio-b01-coca-cola", {"category": "explainer"}, ("curio", "W-商業與品牌奇聞")),
        ("curio-t09", {"category": "explainer"}, ("curio", "H-歷史懸案")),
        ("curio-t999", {"category": "explainer"}, ("curio", None)),
        ("sothatswhy-p17-gecko-feet", {"category": "explainer"}, ("sothatswhy", "生物動物與植物")),
        ("sothatswhy-bio-01", {"category": "explainer"}, ("sothatswhy", "生物動物與植物")),
        ("tai-nainai-e057", {"category": "drama", "format": "drama"}, ("tai-nainai", None)),
        ("zhong-tian-qu-qi-e001-005", {"category": "drama"}, ("zhong-tian-qu-qi", None)),
        ("zhong-tian-qu-qi-e055-r2", {"category": "drama"}, ("zhong-tian-qu-qi-r2", None)),
        ("story-ikea", {"category": "story"}, ("story", None)),
        ("ai-term-token", {"category": "ai-terms"}, ("ai-terms", None)),
        ("wuxia-s01e03", {"category": "long-drama", "series_slug": "wuxia"}, ("wuxia", None)),
        ("siri-how-to", {"category": "tutorial"}, (None, None)),
        ("tai-nainai-e057", {"category": None}, (None, None)),
        ("curio-h01-short", {"shorts_line": "cut", "category": "explainer"}, (None, None)),
    ],
)
def test_a_video_is_filed_by_the_rules_drive_backup_files_it_by(
    slug: str, fields: dict[str, Any], expected: tuple[str | None, str | None]
) -> None:
    assert shelf.shelf_fields(_project(slug, **fields)) == expected


def test_the_two_shows_are_the_explainer_prefixes_drive_backup_knows() -> None:
    prefixes = dict((key, prefix) for prefix, key in target.SLUG_PREFIXES)
    assert set(shelf.SHOWS) <= set(prefixes)
    assert set(shelf.SHOWS) <= target.AI_DRAMA_SERIES


def test_refresh_says_whether_anything_changed() -> None:
    project = _project("curio-h01", category="explainer")
    assert shelf.refresh(project) is True
    assert (project.series_key, project.topic) == ("curio", "H-歷史懸案")
    assert shelf.refresh(project) is False
    project.shorts_line = "cut"
    assert shelf.refresh(project) is True
    assert (project.series_key, project.topic) == (None, None)


def test_a_series_is_named_by_the_owner_then_drive_then_its_title_then_the_scripts() -> None:
    labels = shelf.series_labels(
        {"curio": "奇聞", "blank": "  "}, {"wuxia": "武俠長篇", "tai-nainai": "不會用到"}
    )
    assert labels["curio"] == "奇聞", "the owner's folder name wins"
    assert labels["sothatswhy"] == "原來如此事務所"
    assert labels["tai-nainai"] == "恁祖媽今年18", "Drive's default beats a series row"
    assert labels["wuxia"] == "武俠長篇"
    assert labels["xiuxian-jiangli"], "a packaged drama is named from its scripts"
    assert "blank" not in labels


@pytest_asyncio.fixture(loop_scope="module")
async def _dispose() -> AsyncIterator[None]:
    yield
    await engine.dispose()


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_the_catalog_has_a_shelf_a_series_and_a_topic(
    tmp_path: Path, _dispose: None
) -> None:
    tag = uuid4().hex[:10]
    store = ReviewStore(tmp_path, max_file_bytes=10_000, max_total_bytes=50_000)
    async with SessionFactory() as session:
        owner = User(email=f"video-shelf-{uuid4()}@example.com", password_hash="unused")
        session.add(owner)
        await session.commit()

        async def report(slug: str, **fields: Any) -> None:
            await service.upsert_project(
                session, store, slug, ProjectIn(stage="outline", title=f"{slug} {tag}", **fields)
            )

        await report(f"curio-h02-{tag}", category="explainer")
        await report(f"curio-h01-{tag}", category="explainer")
        await report(f"curio-p03-{tag}", category="explainer")
        await report(f"sothatswhy-p17-{tag}", category="explainer")
        await report(f"concept-{tag}", category="explainer")
        await report(f"dra{tag}-e002", category="drama", format="drama")
        await report(f"dra{tag}-e001", category="drama", format="drama")
        await report(f"drb{tag}-e001", category="drama", format="drama")
        await report(f"story-{tag}", category="story", format="drama")
        await report(f"curio-h01-{tag}-cut", category="explainer", shorts_line="cut")

        page = await service.browse_projects(session, q=tag, limit=100)
        assert page.total == 9, "the Short is still left out"
        shelves = {facet.code: facet.count for facet in page.facets.shelf}
        assert list(shelves)[:2] == ["curio", "sothatswhy"]
        assert (shelves["curio"], shelves["sothatswhy"], shelves["explainer"]) == (3, 1, 1)
        assert (shelves["drama"], shelves["story"], shelves["none"]) == (3, 1, 0)
        categories = {facet.code: facet.count for facet in page.facets.category}
        assert categories["explainer"] == 5, "the old facet still counts the shows in theirs"
        assert page.facets.series == [] and page.facets.topic == [], "no shelf, no second row"

        def slugs(result: Any) -> list[str]:
            return [item.slug for item in result.items]

        other = await service.browse_projects(session, q=tag, shelf_code="explainer")
        assert slugs(other) == [f"concept-{tag}"], "觀念解說 leaves the two shows out"
        assert await service.browse_projects(session, q=tag, category="explainer") == other, (
            "an old ?category= link is the shelf of the same name"
        )

        curio = await service.browse_projects(session, q=tag, shelf_code="curio")
        assert {f.code: f.count for f in curio.facets.topic} == {"H-歷史懸案": 2, "P-預言與末日": 1}
        assert [(f.code, f.label) for f in curio.facets.series] == [("curio", "奇聞檔案局")]
        h = await service.browse_projects(session, q=tag, shelf_code="curio", topic="H-歷史懸案")
        assert slugs(h) == [f"curio-h01-{tag}", f"curio-h02-{tag}"], "a topic lists in order"
        assert {f.code: f.count for f in h.facets.topic}["P-預言與末日"] == 1, (
            "the topic counts do not narrow themselves"
        )
        assert h.items[0].series_key == "curio" and h.items[0].topic == "H-歷史懸案"

        dramas = await service.browse_projects(session, q=tag, shelf_code="drama")
        assert {f.code: f.count for f in dramas.facets.series} == {f"dra{tag}": 2, f"drb{tag}": 1}
        assert dramas.facets.topic == [], "a drama has no topics"
        one = await service.browse_projects(
            session, q=tag, shelf_code="drama", series=f"dra{tag}"
        )
        assert slugs(one) == [f"dra{tag}-e001", f"dra{tag}-e002"], "episodes in order"
        assert {f.code: f.count for f in one.facets.series}[f"drb{tag}"] == 1

        # The owner moves a curio episode to 觀念解說's other shelf by its category: it stays
        # in the show, which is what its slug says.
        await service.set_category(session, f"curio-p03-{tag}", owner, CategoryIn(category=None))
        assert slugs(await service.browse_projects(session, q=tag, shelf_code="none")) == []
        # A drama whose category is cleared leaves its drama: an imported drama is known by its
        # category, as on Drive.
        await service.set_category(session, f"drb{tag}-e001", owner, CategoryIn(category=None))
        unfiled = await service.browse_projects(session, q=tag, shelf_code="none")
        assert slugs(unfiled) == [f"drb{tag}-e001"]
        assert unfiled.items[0].series_key is None

        # The backfill fills rows written before the columns and changes nothing twice.
        row = await service._project(session, f"dra{tag}-e001")
        row.series_key = row.topic = None
        await session.commit()
        dry = await shelf.backfill(session, apply=False)
        assert dry["changed"] >= 1 and dry["apply"] is False
        assert (await service._project(session, f"dra{tag}-e001")).series_key is None
        done = await shelf.backfill(session, apply=True)
        assert done["by_series"].get(f"dra{tag}") == 1
        assert (await service._project(session, f"dra{tag}-e001")).series_key == f"dra{tag}"
        assert (await shelf.backfill(session, apply=True))["changed"] == 0


@POSTGRES
@pytest.mark.asyncio(loop_scope="module")
async def test_opening_the_catalog_files_videos_written_before_the_columns(
    _dispose: None,
) -> None:
    """The owner, 2026-11-18: no backfill on the host; the catalog files old rows itself."""
    tag = uuid4().hex[:8]
    old = {
        f"curio-h01-{tag}": {"category": "explainer"},
        f"dr{tag}-e001": {"category": "drama", "format": "drama"},
        f"tutorial-{tag}": {"category": "tutorial"},
        f"curio-h01-{tag}-cut": {"category": "explainer", "shorts_line": "cut"},
    }
    async with SessionFactory() as session:
        for slug, fields in old.items():
            session.add(_project(slug, **fields))
        await session.commit()
        # Rows from before migration 0147 have no series_key or topic.
        healed = await shelf.heal(session)
        assert healed >= 2
        rows = {
            slug: await service._project(session, slug) for slug in old
        }
        assert (rows[f"curio-h01-{tag}"].series_key, rows[f"curio-h01-{tag}"].topic) == (
            "curio",
            "H-歷史懸案",
        )
        assert rows[f"dr{tag}-e001"].series_key == f"dr{tag}"
        assert rows[f"tutorial-{tag}"].series_key is None
        assert rows[f"curio-h01-{tag}-cut"].series_key is None, "a Short has no shelf"
        assert await shelf.heal(session) == 0, "nothing left to file"
        curio = await service.browse_projects(session, q=tag, shelf_code="curio")
        assert [item.slug for item in curio.items] == [f"curio-h01-{tag}"]


def test_the_healing_candidates_cover_every_series_prefix() -> None:
    sql = str(shelf._candidates().compile(compile_kwargs={"literal_binds": True}))
    for prefix, _key in target.SLUG_PREFIXES:
        assert f"'{prefix}" in sql, prefix
    assert "series_slug IS NOT NULL" in sql and "shorts_line IS NULL" in sql
