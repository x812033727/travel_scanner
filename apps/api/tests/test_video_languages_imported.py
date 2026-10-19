"""An imported video's other languages: es, pt, id, vi and th besides en, ja and ko.

The owner added Latin-American Spanish, Brazilian Portuguese, Indonesian, Vietnamese and Thai for
種田娶妻打天下 on 2026-10-18, an imported series whose files are made outside the pipeline
(docs/videos/LANGUAGES.md). Only a video ``tools/video/cli.mjs import`` put on the site may choose
them; the worker's three and every other video stay as they were.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.models import User, VideoProject
from app.problems import AppError
from app.video_reviews import admin_service as service
from app.video_reviews.schemas import (
    DUB_LOCALES,
    IMPORTED_LOCALES,
    WORKER_LOCALES,
    LocalesIn,
    ReviewIn,
)
from app.video_youtube import language_package, requests, retitle
from tests.test_video_review_renewal import SLUG, Site, _file, _submit
from tests.test_video_review_renewal import site as _site
from tests.test_video_reviews import _app

site = _site  # The renewal tests' real SQLite database, without collecting their tests here.

CAPTIONS = "1\n00:00:01,000 --> 00:00:03,000\nHola, mundo\n"
EVERYTHING = {"metadata": True, "captions": True, "dub": True}
IMPORTED = {"key": "imported", "label": "匯入的成片", "done": True}


@pytest.fixture(autouse=True)
def _no_spend(monkeypatch: pytest.MonkeyPatch) -> None:
    # The SQLite fixture has no media-spend table.
    monkeypatch.setattr(service, "spend_by_slug", AsyncMock(return_value={}))


async def _seed(site: Site, *, imported: bool) -> None:
    """The fixture's project as a finished long video, imported or made by the pipeline."""
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        project.format, project.shorts_line = "slides", None
        project.title, project.stage = "種田娶妻打天下 第1集", "final"
        project.checklist = [IMPORTED] if imported else []
        await session.commit()


async def _save(site: Site, choice: dict[str, Any]) -> Any:
    async with site.factory() as session:
        return await service.set_locales(
            session, SLUG, site.owner, LocalesIn.model_validate({"locales": choice})
        )


async def _view(site: Site) -> Any:
    async with site.factory() as session:
        return await service.project_view(session, SLUG)


def test_the_eight_languages_list_the_worker_s_three_first() -> None:
    assert WORKER_LOCALES == ("en", "ja", "ko")
    assert IMPORTED_LOCALES == ("es", "pt", "id", "vi", "th")
    assert DUB_LOCALES == (*WORKER_LOCALES, *IMPORTED_LOCALES)


@pytest.mark.asyncio
async def test_an_imported_video_chooses_eight_languages_and_its_batch_reads_ready(
    site: Site,
) -> None:
    await _seed(site, imported=True)
    assert (await _view(site)).locale_options == list(DUB_LOCALES)

    # Ticked in any order, stored in the page's order.
    chosen = {locale: EVERYTHING for locale in ("th", "es", "en", "vi", "pt", "id")}
    saved = await _save(site, chosen)
    assert list(saved.locales) == ["en", "es", "pt", "id", "vi", "th"]
    assert all(saved.languages[locale]["dub"].state == "working" for locale in saved.locales)

    # The batch tools/video/import sends: every chosen part ready, the owner decides.
    locales: dict[str, Any] = {}
    files = []
    for locale in saved.locales:
        files += [
            _file(site, f"Title {locale}\n\nAbout {locale}\n".encode(), f"description_{locale}",
                  "text/plain"),
            _file(site, CAPTIONS.replace("Hola", locale).encode(), f"captions_{locale}",
                  "application/x-subrip"),
            _file(site, f"{locale} track".encode(), f"dub_{locale}", "audio/mp4"),
        ]
        locales[locale] = {
            "metadata": "ready", "captions": "ready", "dub": "ready",
            "file": f"dub.{locale}.m4a", "format": "m4a", "file_role": f"dub_{locale}",
        }
    batch = await _submit(
        site,
        ReviewIn(
            gate="languages",
            content_sha256="8" * 64,
            summary="語言：匯入",
            payload={"locales": locales, "imported": True, "hand_pushed": True},
            files=files,
        ),
    )
    assert batch.status == "pending", "a hand-pushed batch waits for the owner"
    view = await _view(site)
    for locale in ("es", "pt", "id", "vi", "th"):
        assert {part: state.state for part, state in view.languages[locale].items()} == {
            "metadata": "ready", "captions": "ready", "dub": "ready",
        }, locale
    assert language_package.choices(view.model_dump()["locales"]) == {
        locale: EVERYTHING for locale in saved.locales
    }, "YouTube sync reads the eight languages too"


@pytest.mark.asyncio
async def test_a_pipeline_video_keeps_three_languages_and_refuses_the_five(site: Site) -> None:
    await _seed(site, imported=False)
    assert (await _view(site)).locale_options == ["en", "ja", "ko"]
    with pytest.raises(AppError) as refused:
        await _save(site, {"en": EVERYTHING, "es": {"metadata": True}, "th": {"captions": True}})
    assert refused.value.status == 422
    assert refused.value.code == "video_locales_imported_only"
    assert "es、th" in refused.value.detail
    assert (await _view(site)).locales_decided_at is None, "nothing was stored"

    saved = await _save(site, {"ko": EVERYTHING, "en": {"metadata": True}})
    assert list(saved.locales) == ["en", "ko"], "en, ja and ko behave as before"


@pytest.mark.asyncio
async def test_a_dub_retry_takes_only_the_worker_s_languages() -> None:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    async with AsyncClient(
        transport=ASGITransport(app=_app(owner)), base_url="http://test"
    ) as client:
        refused = await client.post("/api/v1/admin/videos/v/languages/es/dub/retry")
    assert refused.status_code == 422, "only the worker remakes a dub"


def test_youtube_gets_the_owner_s_varieties_and_each_language_s_caption_word() -> None:
    assert [requests.youtube_language(locale) for locale in DUB_LOCALES] == [
        "en", "ja", "ko", "es-419", "pt-BR", "id", "vi", "th",
    ]
    metadata = {
        "title": "種田娶妻打天下 第1集",
        "localizations": {
            "es": {"title": "Siembra, cásate y conquista Cap. 1 | CC", "description": "d"},
            "pt": {"title": "Plantar, Casar e Conquistar Ep. 1 | Legendado", "description": "d"},
            "id": {"title": "Bertani, Beristri, Berkuasa Episode 1 | Sub Indo", "description": "d"},
            "vi": {"title": "Làm Ruộng Cưới Vợ Đoạt Thiên Hạ Tập 1 | Vietsub", "description": "d"},
            "th": {"title": "ทะลุมิติไปทำนา ได้เมีย ครองแผ่นดิน ตอนที่ 1", "description": "d"},
            "en": {"title": "Farm, Marry, Conquer Ep. 1 | CC", "description": "d"},
        },
    }
    titles = {key: entry["title"] for key, entry in requests.localizations(metadata).items()}
    assert titles == {
        "es-419": "Siembra, cásate y conquista Cap. 1｜CC",
        "pt-BR": "Plantar, Casar e Conquistar Ep. 1｜Legendado",
        "id": "Bertani, Beristri, Berkuasa Episode 1｜Sub Indo",
        "vi": "Làm Ruộng Cưới Vợ Đoạt Thiên Hạ Tập 1｜Vietsub",
        "th": "ทะลุมิติไปทำนา ได้เมีย ครองแผ่นดิน ตอนที่ 1｜ซับไทย",
        "en": "Farm, Marry, Conquer Ep. 1｜CC Subtitles",
    }
    # A compilation's title says dub and subtitles; in the five languages it keeps its words.
    for language, title in (
        ("id", "Bertani, Beristri, Berkuasa Episode 1–5 | Dub + Sub Indo"),
        ("pt", "Plantar, Casar e Conquistar Ep. 1–5 | Dublado + Legendado"),
        ("es", "Siembra, cásate y conquista Cap. 1–5 | Doblaje latino + CC"),
        ("th", "ทะลุมิติไปทำนา ได้เมีย ครองแผ่นดิน ตอนที่ 1–5 | พากย์ไทย + ซับไทย"),
    ):
        assert requests.captioned(title, language) == title, language
    # en, ja and ko are tagged as before.
    assert (
        requests.captioned("Farm, Marry, Conquer Ep. 1–5 | Dub + CC", "en")
        == "Farm, Marry, Conquer Ep. 1–5 | Dub + CC｜CC Subtitles"
    )
    assert requests.captioned("AI 模型怎麼挑", "ja") == "AI 模型怎麼挑｜字幕付き"
    assert requests.NARRATION_LANGUAGES == ("zh-TW", "en", "ja", "ko")
    with pytest.raises(ValueError):
        requests.narration_language({"default_language": "es"})


def test_the_retitle_tool_reads_youtube_s_tags_as_the_site_s_languages() -> None:
    assert [
        retitle.tag_language(code)
        for code in ("es-419", "pt-BR", "id", "vi", "th", "ko", "zh-Hant", "fr", "")
    ] == ["es", "pt", "id", "vi", "th", "ko", "zh-TW", "en", "zh-TW"]
    planned = retitle.plan(
        {
            "id": "abcdefghijk",
            "snippet": {"title": "種田娶妻打天下 第1集｜CC字幕", "defaultLanguage": "zh-TW"},
            "localizations": {
                "pt-BR": {"title": "Plantar, Casar e Conquistar Ep. 1 | Legendado"},
                "vi": {"title": "Làm Ruộng Cưới Vợ Đoạt Thiên Hạ Tập 1｜Vietsub"},
            },
        }
    )
    assert planned["titles"] == {
        "pt-BR": [
            "Plantar, Casar e Conquistar Ep. 1 | Legendado",
            "Plantar, Casar e Conquistar Ep. 1｜Legendado",
        ]
    }, "a title keeps its own language's word, not an English one"
