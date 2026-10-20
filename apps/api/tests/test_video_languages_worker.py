"""The worker makes titles and captions in es, pt, id, vi and th for every video.

On 2026-10-20 the owner opened the five languages first added for an imported series
(tests/test_video_languages_imported.py) to every video, of every category, drama included:
the worker now makes their titles, descriptions and captions
(tasks/open/2026-10-19-worker-video-languages-five.md, phase one). Their dubs are phase two, so a
dub in one of them stays refused unless the video was imported, and the settings tab pre-ticks
titles and captions in all eight.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models import VideoProject
from app.problems import AppError
from app.video_automation import series as series_service
from app.video_automation import settings as settings_service
from app.video_automation.models import DEFAULT_CAPTION_LOCALES, DEFAULT_DRAMA
from app.video_automation.schemas import CAPTION_LOCALES, SettingsWrite
from app.video_reviews import admin_service as service
from app.video_reviews.schemas import (
    DUB_LOCALES,
    IMPORTED_DUB_LOCALES,
    WORKER_CAPTION_LOCALES,
    WORKER_DUB_LOCALES,
    DubLocalesIn,
    LocalesIn,
)
from tests.test_video_automation_settings import _drama, _values
from tests.test_video_review_renewal import SLUG, Site
from tests.test_video_review_renewal import site as _site
from tests.test_video_story_policy import _report, _series, _store, _token
from tests.test_video_story_policy import db as _db

site = _site  # The renewal tests' real SQLite database, without collecting their tests here.
db = _db  # The story tests' in-memory database with the series tables.

EIGHT = ["en", "ja", "ko", "es", "pt", "id", "vi", "th"]
FIVE = ["es", "pt", "id", "vi", "th"]
TITLES_AND_CAPTIONS = {"metadata": True, "captions": True, "dub": False}
EVERYTHING = {"metadata": True, "captions": True, "dub": True}
IMPORTED = {"key": "imported", "label": "匯入的成片", "done": True}
# (format, category): a slides tutorial, a brand story, an explainer and a drama.
KINDS = [
    ("slides", "tutorial"),
    ("drama", "story"),
    ("drama", "explainer"),
    ("drama", "drama"),
    ("slides", "ai-news"),
    ("drama", "long-drama"),
]


@pytest.fixture(autouse=True)
def _no_spend(monkeypatch: pytest.MonkeyPatch) -> None:
    # The SQLite fixture has no media-spend table.
    monkeypatch.setattr(service, "spend_by_slug", AsyncMock(return_value={}))


async def _seed(
    site: Site, *, format: str = "slides", category: str | None = None, imported: bool = False
) -> None:
    """The fixture's project as a finished long video of this kind, made by the pipeline."""
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        project.format, project.shorts_line, project.category = format, None, category
        project.title, project.stage = "一支影片", "final"
        project.checklist = [IMPORTED] if imported else []
        project.locales, project.locales_decided_at = {}, None
        await session.commit()


async def _save(site: Site, choice: dict[str, Any]) -> Any:
    async with site.factory() as session:
        return await service.set_locales(
            session, SLUG, site.owner, LocalesIn.model_validate({"locales": choice})
        )


async def _view(site: Site) -> Any:
    async with site.factory() as session:
        return await service.project_view(session, SLUG)


def test_the_worker_makes_titles_and_captions_in_eight_and_dubs_in_three() -> None:
    assert WORKER_DUB_LOCALES == ("en", "ja", "ko")
    assert IMPORTED_DUB_LOCALES == tuple(FIVE)
    assert list(DUB_LOCALES) == list(WORKER_CAPTION_LOCALES) == EIGHT
    assert list(CAPTION_LOCALES) == EIGHT, "the settings tab offers the panel's eight"


@pytest.mark.asyncio
@pytest.mark.parametrize(("format", "category"), KINDS)
async def test_every_pipeline_video_offers_eight_and_takes_titles_and_captions_in_the_five(
    site: Site, format: str, category: str
) -> None:
    await _seed(site, format=format, category=category)
    assert (await _view(site)).locale_options == EIGHT

    # Ticked in any order, stored in the page's order; titles alone or captions alone work too.
    chosen: dict[str, Any] = {locale: TITLES_AND_CAPTIONS for locale in reversed(EIGHT)}
    chosen["vi"] = {"metadata": True}
    chosen["th"] = {"captions": True}
    saved = await _save(site, chosen)
    assert list(saved.locales) == EIGHT
    assert saved.locales["vi"].model_dump() == {"metadata": True, "captions": False, "dub": False}
    assert saved.locales["th"].model_dump() == {"metadata": False, "captions": True, "dub": False}
    assert saved.locales_decided_at is not None
    for locale in FIVE:
        states = {part: state.state for part, state in saved.languages[locale].items()}
        assert "dub" not in states and set(states.values()) == {"working"}, locale


@pytest.mark.asyncio
@pytest.mark.parametrize(("format", "category"), [("slides", "tutorial"), ("drama", "explainer")])
async def test_a_dub_in_the_five_is_refused_on_a_pipeline_video(
    site: Site, format: str, category: str
) -> None:
    await _seed(site, format=format, category=category)
    for locale in FIVE:
        with pytest.raises(AppError) as refused:
            await _save(site, {"en": EVERYTHING, locale: EVERYTHING})
        assert refused.value.status == 422, locale
        assert refused.value.code == "video_locales_dub_imported_only", locale
        assert refused.value.detail.startswith(f"{locale} 的配音自動產線還不會做")
        assert "只有匯入的影片" in refused.value.detail
    with pytest.raises(AppError) as both:
        await _save(site, {"th": EVERYTHING, "es": {"dub": True}, "pt": TITLES_AND_CAPTIONS})
    assert both.value.detail.startswith("es、th 的配音"), "only the dubbed ones, in page order"
    assert (await _view(site)).locales_decided_at is None, "nothing was stored"

    # The dub checkboxes of the old page take the same rule.
    with pytest.raises(AppError) as old_page:
        async with site.factory() as session:
            await service.set_dub_locales(
                session, SLUG, site.owner, DubLocalesIn.model_validate({"locales": ["en", "vi"]})
            )
    assert old_page.value.code == "video_locales_dub_imported_only"

    # en, ja and ko dubs are what they were.
    saved = await _save(site, {"ja": EVERYTHING, "es": TITLES_AND_CAPTIONS})
    assert saved.locales["ja"].dub and list(saved.locales) == ["ja", "es"]


@pytest.mark.asyncio
async def test_a_drama_keeps_its_own_dub_rule_and_takes_titles_and_captions(site: Site) -> None:
    await _seed(site, format="drama", category="drama")
    with pytest.raises(AppError) as refused:
        await _save(site, {"en": EVERYTHING})
    assert refused.value.code == "video_locales_dub_not_for_drama"
    saved = await _save(site, {locale: TITLES_AND_CAPTIONS for locale in EIGHT})
    assert list(saved.locales) == EIGHT


@pytest.mark.asyncio
async def test_an_imported_video_still_dubs_the_five(site: Site) -> None:
    await _seed(site, imported=True)
    assert (await _view(site)).locale_options == EIGHT
    saved = await _save(site, {locale: EVERYTHING for locale in EIGHT})
    assert list(saved.locales) == EIGHT
    assert all(saved.locales[locale].dub for locale in FIVE)


def test_the_settings_pre_tick_the_eight_for_tutorials_and_dramas() -> None:
    assert DEFAULT_CAPTION_LOCALES == EIGHT
    assert DEFAULT_DRAMA["drama_caption_locales"] == EIGHT
    saved = SettingsWrite(**_values(caption_locales=EIGHT, drama=_drama()))
    assert saved.caption_locales == EIGHT and saved.drama.drama_caption_locales == EIGHT
    assert SettingsWrite(**_values(caption_locales=["th", "en"])).caption_locales == ["th", "en"]
    for bad in (
        _values(caption_locales=[*EIGHT, "fr"]),
        _values(caption_locales=["vi", "vi"]),
        _values(caption_locales=[*EIGHT, "en"]),
        _values(drama=_drama(drama_caption_locales=["th", "th"])),
        _values(drama=_drama(drama_caption_locales=[*EIGHT, "zh-CN"])),
        _values(drama=_drama(drama_caption_locales=["fr"])),
    ):
        with pytest.raises(ValidationError):
            SettingsWrite(**bad)


def test_a_stored_list_reads_the_five_and_drops_what_the_videos_are_not_made_in() -> None:
    assert settings_service.current_caption_locales(["zh-CN", "th", "en", "fr"]) == ["th", "en"]


async def test_a_brand_story_s_server_decision_includes_the_five(
    db: async_sessionmaker[AsyncSession], tmp_path: Path
) -> None:
    await _series(db, "stories", "story", [(1, "story-rolling-case", "ready")])
    async with db() as session:
        settings = await settings_service.settings_row(session)
        assert settings.drama_caption_locales == EIGHT, "a fresh row pre-ticks the eight"
        await series_service.start_episode(session, _token(), "stories", 1, "story-rolling-case")
    async with db() as session:
        view = await service.upsert_project(
            session, _store(tmp_path), "story-rolling-case", _report("stories", 1)
        )
    assert {locale: choice.model_dump() for locale, choice in view.locales.items()} == {
        locale: TITLES_AND_CAPTIONS for locale in EIGHT
    }, "titles, descriptions and captions in all eight, no dub"
