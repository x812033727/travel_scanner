from __future__ import annotations

import json
import shutil
from collections.abc import AsyncIterator
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.auth.service import current_user
from app.db import get_session
from app.i18n import ERROR_DETAILS
from app.models import User
from app.problems import AppError, app_error_handler
from app.video_dramas import catalog
from app.video_dramas.router import router
from app.video_dramas.schemas import DocumentDetail, DramaIndex, EpisodeDetail

REPO_ROOT = Path(__file__).resolve().parents[3]
URL = "/api/v1/admin/video-dramas"


def _app(role: str | None = "viewer", *, authenticated: bool = True) -> FastAPI:
    application = FastAPI()
    application.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    application.include_router(router, prefix="/api/v1")

    async def session() -> AsyncIterator[AsyncMock]:
        mock = AsyncMock()
        mock.execute.side_effect = AssertionError("script viewing must not query the database")
        mock.scalars.side_effect = AssertionError("script viewing must not query the database")
        yield mock

    application.dependency_overrides[get_session] = session
    if authenticated:
        user = User(id=uuid4(), email="scripts-reader@example.com", password_hash="unused")
        user.__dict__["_admin_roles_cache"] = frozenset({role} if role else ())
        application.dependency_overrides[current_user] = lambda: user
    return application


def _client(application: FastAPI) -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=application), base_url="http://test")


def test_packaged_scripts_match_the_repository() -> None:
    index = catalog.load_index()
    assert [series.key for series in index.series] == [
        "tai-nainai",
        "zhong-tian-qu-qi",
        "ou-de-jianghu",
        "zero-root-yaozu",
        "xiuxian-jiangli",
    ]
    tai = index.series[0]
    assert tai.counts.episodes == len(tai.episodes) > 0
    first = tai.episodes[0]
    script = (REPO_ROOT / "docs/videos" / first.slug / "script.md").read_text(encoding="utf-8")
    detail = catalog.episode("tai-nainai", first.slug)
    assert {doc.kind: doc.markdown for doc in detail.docs}["script"] == script


@pytest.mark.parametrize(
    ("role", "authenticated", "expected"),
    [(None, False, 401), (None, True, 403), ("support", True, 403), ("viewer", True, 200)],
)
async def test_read_capability_is_required(
    role: str | None, authenticated: bool, expected: int
) -> None:
    async with _client(_app(role, authenticated=authenticated)) as client:
        response = await client.get(URL)
    assert response.status_code == expected


async def test_index_episode_and_document() -> None:
    async with _client(_app()) as client:
        listing = await client.get(URL)
        index = DramaIndex.model_validate_json(listing.content)
        series = next(item for item in index.series if item.key == "zhong-tian-qu-qi")
        revised = next(item for item in series.episodes if item.variant == "r2")
        episode = await client.get(f"{URL}/zhong-tian-qu-qi/episodes/{revised.slug}")
        document = await client.get(f"{URL}/zhong-tian-qu-qi/documents/{series.documents[0].id}")
        missing = await client.get(f"{URL}/zhong-tian-qu-qi/episodes/zhong-tian-qu-qi-e999")
        other = await client.get(f"{URL}/tai-nainai/episodes/{revised.slug}")
        unknown = await client.get(f"{URL}/brand/episodes/brand-e001")
    detail = EpisodeDetail.model_validate_json(episode.content)
    assert detail.slug == revised.slug and detail.docs[0].markdown
    assert [doc.kind for doc in detail.docs] == [doc.kind for doc in revised.docs]
    assert DocumentDetail.model_validate_json(document.content).markdown
    assert missing.status_code == 404
    assert other.status_code == 404
    assert unknown.status_code == 422


async def test_missing_index_fails_closed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(catalog, "DATA_DIR", tmp_path)
    async with _client(_app()) as client:
        response = await client.get(URL)
    assert response.status_code == 503
    assert response.json()["code"] == "video_dramas_unavailable"


async def test_tampered_content_fails_closed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    for source in catalog.DATA_DIR.glob("*.json"):
        shutil.copy(source, tmp_path / source.name)
    content = json.loads((tmp_path / "xiuxian-jiangli.json").read_text(encoding="utf-8"))
    content["documents"] = {}
    (tmp_path / "xiuxian-jiangli.json").write_text(json.dumps(content), encoding="utf-8")
    monkeypatch.setattr(catalog, "DATA_DIR", tmp_path)
    async with _client(_app()) as client:
        response = await client.get(f"{URL}/xiuxian-jiangli/episodes/xiuxian-jiangli-e001")
    assert response.status_code == 503


def test_error_codes_are_localized() -> None:
    for locale in ("en", "ja", "ko", "zh-CN"):
        assert "video_dramas_unavailable" in ERROR_DETAILS[locale]
        assert "video_drama_not_found" in ERROR_DETAILS[locale]
