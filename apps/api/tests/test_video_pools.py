from __future__ import annotations

import hashlib
import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.auth.service import current_user
from app.db import get_session
from app.i18n import ERROR_DETAILS
from app.models import User
from app.problems import AppError, app_error_handler
from app.video_pools import catalog
from app.video_pools.router import router
from app.video_pools.schemas import (
    CorePage,
    EpisodePage,
    ExpansionPage,
    PoolOverview,
    ThemeDetail,
    ThemePage,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
URL = "/api/v1/admin/video-pools"
POOL_DIRS = {
    "curio": "docs/videos/history-curiosity/pool",
    "so-thats-why": "docs/videos/so-thats-why/pool",
}


def _app(role: str | None = "viewer", *, authenticated: bool = True) -> FastAPI:
    application = FastAPI()
    application.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    application.include_router(router, prefix="/api/v1")

    async def session() -> AsyncIterator[AsyncMock]:
        mock = AsyncMock()
        mock.execute.side_effect = AssertionError("pool viewing must not query the database")
        mock.scalars.side_effect = AssertionError("pool viewing must not query the database")
        yield mock

    application.dependency_overrides[get_session] = session
    if authenticated:
        user = User(id=uuid4(), email="pools-reader@example.com", password_hash="unused")
        user.__dict__["_admin_roles_cache"] = frozenset({role} if role else ())
        application.dependency_overrides[current_user] = lambda: user
    return application


def _client(application: FastAPI) -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=application), base_url="http://test")


def test_packaged_bundle_matches_the_committed_pools() -> None:
    bundle = catalog.load_bundle()
    for series in bundle.series:
        themes = REPO_ROOT / POOL_DIRS[series.key] / "themes.json"
        assert series.sources.themes_sha256 == hashlib.sha256(themes.read_bytes()).hexdigest()
        source = {episode["id"]: episode for episode in json.loads(themes.read_text())["episodes"]}
        assert {theme.id for theme in series.themes} == set(source)
        for theme in series.themes:
            assert theme.title == source[theme.id]["title"]
            if theme.producible:
                assert theme.audience is not None
                assert theme.audience.score >= series.audience_min


@pytest.mark.parametrize(
    ("role", "authenticated", "expected"),
    [
        (None, False, 401),
        (None, True, 403),
        ("support", True, 403),
        ("viewer", True, 200),
        ("content", True, 200),
        ("owner", True, 200),
    ],
)
async def test_read_capability_is_required(
    role: str | None, authenticated: bool, expected: int
) -> None:
    async with _client(_app(role, authenticated=authenticated)) as client:
        response = await client.get(URL)
    assert response.status_code == expected


async def test_overview_lists_both_series_with_counts() -> None:
    async with _client(_app()) as client:
        response = await client.get(URL)
    page = PoolOverview.model_validate_json(response.content)
    assert [series.key for series in page.series] == ["curio", "so-thats-why"]
    for series in page.series:
        assert series.counts.producible > 0
        assert series.counts.long_themes == series.counts.producible + series.counts.long_reserve


async def test_producible_themes_are_ranked_by_audience_and_filterable() -> None:
    async with _client(_app()) as client:
        response = await client.get(f"{URL}/curio/themes", params={"page_size": 100})
        reserve = await client.get(f"{URL}/curio/themes", params={"status": "reserve"})
        strong = await client.get(f"{URL}/curio/themes", params={"min_score": 7.5})
    page = ThemePage.model_validate_json(response.content)
    assert page.items and all(item.producible for item in page.items)
    ranks = [item.audience.rank for item in page.items if item.audience]
    assert ranks == sorted(ranks)
    assert all(not item.producible for item in ThemePage.model_validate_json(reserve.content).items)
    high = ThemePage.model_validate_json(strong.content)
    assert all(item.audience and item.audience.score >= 7.5 for item in high.items)
    assert "chapters" not in response.json()["items"][0]


async def test_search_category_and_detail() -> None:
    async with _client(_app()) as client:
        listing = await client.get(f"{URL}/so-thats-why/themes", params={"status": "all"})
        first = ThemePage.model_validate_json(listing.content).items[0]
        detail = await client.get(f"{URL}/so-thats-why/themes/{first.id}")
        found = await client.get(
            f"{URL}/so-thats-why/themes", params={"status": "all", "q": first.id.lower()}
        )
        missing = await client.get(f"{URL}/so-thats-why/themes/NOPE999")
        wrong_series = await client.get(f"{URL}/brand/themes")
    theme = ThemeDetail.model_validate_json(detail.content)
    assert theme.id == first.id and theme.chapters
    assert first.id in {item.id for item in ThemePage.model_validate_json(found.content).items}
    assert missing.status_code == 404
    assert wrong_series.status_code == 422
    if first.category:
        async with _client(_app()) as client:
            by_category = await client.get(
                f"{URL}/so-thats-why/themes", params={"status": "all", "category": first.category}
            )
        assert all(
            item.category == first.category
            for item in ThemePage.model_validate_json(by_category.content).items
        )


async def test_expansions_are_newest_first() -> None:
    async with _client(_app()) as client:
        response = await client.get(f"{URL}/so-thats-why/expansions")
    page = ExpansionPage.model_validate_json(response.content)
    days = [batch.created_on or "" for batch in page.expansions]
    assert days == sorted(days, reverse=True)
    assert page.checkpoints


@pytest.mark.parametrize("content", [None, "{}", "not json"])
async def test_missing_or_invalid_bundle_fails_closed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, content: str | None
) -> None:
    path = tmp_path / "pools.json"
    if content is not None:
        path.write_text(content, encoding="utf-8")
    monkeypatch.setattr(catalog, "BUNDLE_PATH", path)
    async with _client(_app()) as client:
        response = await client.get(URL)
    assert response.status_code == 503
    assert response.json()["code"] == "video_pools_unavailable"


BRAND = "W-商業與品牌奇聞"


def test_packaged_cores_match_the_committed_pool() -> None:
    bundle = catalog.load_bundle()
    for series in bundle.series:
        pool = json.loads((REPO_ROOT / POOL_DIRS[series.key] / "pool.json").read_text())
        source = {
            row["id"]: row
            for row in pool["candidates"]
            if row.get("selected") and (row.get("editorial") or {}).get("role") == "episode_core"
        }
        assert {core.id for core in series.cores} == set(source)
        for core in series.cores:
            assert core.question == source[core.id]["question"]
            if core.audience is not None:
                assert core.audience.score == source[core.id]["audience"]["score"]
    curio = next(series for series in bundle.series if series.key == "curio")
    assert curio.counts.cores_passing > 0
    assert any(core.category == BRAND for core in curio.cores)


async def test_cores_default_to_the_ones_over_the_gate_in_rank_order() -> None:
    async with _client(_app()) as client:
        response = await client.get(f"{URL}/curio/cores", params={"page_size": 100})
        second = await client.get(f"{URL}/curio/cores", params={"page_size": 100, "page": 2})
    page = CorePage.model_validate_json(response.content)
    minimum = next(s for s in catalog.load_bundle().series if s.key == "curio").audience_min
    assert page.items and all(i.audience and i.audience.score >= minimum for i in page.items)
    ranks = [item.audience.rank for item in page.items if item.audience]
    assert ranks == sorted(ranks)
    later = CorePage.model_validate_json(second.content)
    assert page.total == later.total > 100
    assert not {item.id for item in page.items} & {item.id for item in later.items}
    # 商業與品牌奇聞沒有長題案，只在這裡出現；分類選單要列得出它。
    assert BRAND in {facet.category for facet in page.categories}


async def test_cores_need_the_read_capability() -> None:
    async with _client(_app("support")) as client:
        refused = await client.get(f"{URL}/curio/cores")
    async with _client(_app(None, authenticated=False)) as client:
        anonymous = await client.get(f"{URL}/curio/cores")
    assert (refused.status_code, anonymous.status_code) == (403, 401)


async def test_cores_filter_by_category_status_score_and_text() -> None:
    async with _client(_app()) as client:
        brand = await client.get(f"{URL}/curio/cores", params={"category": BRAND})
        unscored = await client.get(f"{URL}/curio/cores", params={"status": "unscored"})
        everything = await client.get(f"{URL}/curio/cores", params={"status": "all"})
        scored = await client.get(f"{URL}/curio/cores", params={"status": "scored"})
        strong = await client.get(f"{URL}/curio/cores", params={"min_score": 7.5})
        found = await client.get(
            f"{URL}/curio/cores", params={"status": "all", "q": "n5803", "sort": "id"}
        )
        empty = await client.get(f"{URL}/so-thats-why/cores", params={"status": "all"})
        wrong_series = await client.get(f"{URL}/brand/cores")
        wrong_status = await client.get(f"{URL}/curio/cores", params={"status": "producible"})
    branded = CorePage.model_validate_json(brand.content)
    assert branded.items and all(item.category == BRAND for item in branded.items)
    waiting = CorePage.model_validate_json(unscored.content)
    assert waiting.items and all(item.audience is None for item in waiting.items)
    total = CorePage.model_validate_json(everything.content).total
    assert total == waiting.total + CorePage.model_validate_json(scored.content).total
    high = CorePage.model_validate_json(strong.content)
    assert high.items and all(i.audience and i.audience.score >= 7.5 for i in high.items)
    assert [item.id for item in CorePage.model_validate_json(found.content).items] == ["N5803"]
    assert CorePage.model_validate_json(empty.content).total == 0
    assert wrong_series.status_code == 422
    assert wrong_status.status_code == 422


def test_bundle_counts_must_match_its_cores(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    raw: dict[str, Any] = json.loads(catalog.BUNDLE_PATH.read_text(encoding="utf-8"))
    raw["series"][0]["counts"]["cores_passing"] += 1
    path = tmp_path / "pools.json"
    path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(catalog, "BUNDLE_PATH", path)
    with pytest.raises(AppError):
        catalog.load_bundle()


def test_bundle_counts_must_match_its_themes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    raw: dict[str, Any] = json.loads(catalog.BUNDLE_PATH.read_text(encoding="utf-8"))
    raw["series"][0]["counts"]["producible"] += 1
    path = tmp_path / "pools.json"
    path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(catalog, "BUNDLE_PATH", path)
    with pytest.raises(AppError):
        catalog.load_bundle()


def test_error_codes_are_localized() -> None:
    for locale in ("en", "ja", "ko", "zh-CN"):
        assert "video_pools_unavailable" in ERROR_DETAILS[locale]
        assert "video_pool_theme_not_found" in ERROR_DETAILS[locale]


def _episode_app(rows: list[SimpleNamespace]) -> tuple[FastAPI, list[Any]]:
    application = _app()
    statements: list[Any] = []

    async def session() -> AsyncIterator[AsyncMock]:
        mock = AsyncMock()

        async def execute(statement: Any) -> MagicMock:
            statements.append(statement)
            result = MagicMock()
            result.all.return_value = rows
            return result

        mock.execute.side_effect = execute
        yield mock

    application.dependency_overrides[get_session] = session
    return application, statements


def _project(slug: str, youtube: str | None, *, dropped: bool = False) -> SimpleNamespace:
    return SimpleNamespace(
        slug=slug,
        youtube_video_id=youtube,
        youtube_publish_at=datetime(2026, 11, 1, tzinfo=UTC) if youtube else None,
        stage="published" if youtube else "review",
        dropped_at=datetime(2026, 11, 2, tzinfo=UTC) if dropped else None,
    )


async def test_episodes_prefer_the_site_upload_and_fall_back_to_the_catalog() -> None:
    bundle = catalog.load_bundle()
    stw = next(series for series in bundle.series if series.key == "so-thats-why")
    cataloged = next(episode for episode in stw.episodes if episode.catalog.youtube_id)
    bare = next(
        episode for episode in stw.episodes if not episode.catalog.youtube_id and episode.slugs
    )
    rows = [_project(cataloged.slugs[0], "AAAAAAAAAAA"), _project(bare.slugs[0], None)]
    application, statements = _episode_app(rows)
    async with _client(application) as client:
        published = await client.get(f"{URL}/so-thats-why/episodes")
        everything = await client.get(f"{URL}/so-thats-why/episodes", params={"status": "all"})
        waiting = await client.get(f"{URL}/so-thats-why/episodes", params={"status": "unpublished"})
        found = await client.get(
            f"{URL}/so-thats-why/episodes", params={"status": "all", "q": bare.slugs[0]}
        )
    assert len(statements) == 4
    page = EpisodePage.model_validate_json(published.content)
    by_key = {row.key: row for row in page.items}
    site = by_key[cataloged.key]
    assert (site.youtube_id, site.youtube_source, site.stage) == (
        "AAAAAAAAAAA",
        "site",
        "published",
    )
    assert site.youtube_url == "https://www.youtube.com/watch?v=AAAAAAAAAAA"
    assert all(row.published for row in page.items)
    other = next(row for row in page.items if row.key != cataloged.key)
    assert other.youtube_source == "catalog" and other.youtube_id
    full = EpisodePage.model_validate_json(everything.content)
    assert full.total == full.published + full.unpublished == len(stw.episodes)
    pending = EpisodePage.model_validate_json(waiting.content)
    assert bare.key in {row.key for row in pending.items}
    assert all(not row.published for row in pending.items)
    assert [row.key for row in EpisodePage.model_validate_json(found.content).items] == [bare.key]


async def test_a_dropped_upload_does_not_count_as_published() -> None:
    bundle = catalog.load_bundle()
    curio = next(series for series in bundle.series if series.key == "curio")
    episode = next(item for item in curio.episodes if not item.catalog.youtube_id and item.slugs)
    application, _ = _episode_app([_project(episode.slugs[0], "BBBBBBBBBBB", dropped=True)])
    async with _client(application) as client:
        response = await client.get(
            f"{URL}/curio/episodes", params={"status": "all", "q": episode.slugs[0]}
        )
    row = next(
        item
        for item in EpisodePage.model_validate_json(response.content).items
        if item.key == episode.key
    )
    assert not row.published and row.dropped and row.youtube_id is None
