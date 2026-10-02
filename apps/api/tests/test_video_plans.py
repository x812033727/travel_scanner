from __future__ import annotations

import hashlib
import json
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError

from app.auth.service import current_user
from app.db import get_session
from app.i18n import ERROR_DETAILS, GENERIC_DETAILS, LOCALES, Locale
from app.models import User
from app.problems import AppError, app_error_handler
from app.video_plans import catalog
from app.video_plans.router import router
from app.video_plans.schemas import CATALOG_COUNTS, CatalogBundle, PlanPage

REPO_ROOT = Path(__file__).resolve().parents[3]
URL = "/api/v1/admin/video-plans"


def _app(role: str | None = "viewer", *, authenticated: bool = True) -> FastAPI:
    application = FastAPI()
    application.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    application.include_router(router, prefix="/api/v1")

    async def session() -> AsyncIterator[AsyncMock]:
        # Authentication may request a session; catalog viewing must not execute SQL.
        mock = AsyncMock()
        mock.execute.side_effect = AssertionError("catalog viewing must not query the database")
        mock.scalars.side_effect = AssertionError("catalog viewing must not query the database")
        yield mock

    application.dependency_overrides[get_session] = session
    if authenticated:
        user = User(id=uuid4(), email="plans-reader@example.com", password_hash="unused")
        user.__dict__["_admin_roles_cache"] = frozenset({role} if role else ())
        application.dependency_overrides[current_user] = lambda: user
    return application


@pytest.fixture
def raw_bundle() -> dict[str, Any]:
    return json.loads(catalog.CATALOG_PATH.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def _install_bundle(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, bundle: dict[str, Any]
) -> None:
    path = tmp_path / "catalog.json"
    path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(catalog, "CATALOG_PATH", path)


def test_packaged_catalog_preserves_all_source_plans_and_provenance() -> None:
    bundle = catalog.load_catalog()
    plans_path = REPO_ROOT / "docs/videos/long-form/plans.json"
    source = json.loads(plans_path.read_text(encoding="utf-8"))
    assert bundle.plans_sha256 == hashlib.sha256(plans_path.read_bytes()).hexdigest()
    assert len(bundle.entries) == 473
    assert bundle.catalog_counts == CATALOG_COUNTS
    originals = {(entry["catalog"], entry["id"]): entry for entry in source["entries"]}
    hashes: dict[str, str] = {}
    for entry in bundle.entries:
        original = originals[(entry.catalog, entry.id)]
        assert entry.stage == original["stage"]
        assert entry.source_status == original["source_status"]
        assert entry.video_slug == original["video_slug"]
        assert entry.target_duration_seconds == original["target_seconds"]
        assert entry.min_duration_seconds == 480
        assert entry.source_path == original["source"]
        assert entry.source_record_sha256 == original["source_record_sha256"]
        assert entry.source_package_path == original.get("source_package")
        assert entry.source_package_sha256 == original.get("source_package_sha256")
        for path, digest in (
            (entry.source_path, entry.source_sha256),
            (entry.source_package_path, entry.source_package_sha256),
        ):
            if path is not None:
                if path not in hashes:
                    hashes[path] = hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest()
                assert digest == hashes[path]


@pytest.mark.parametrize(
    ("role", "authenticated", "expected"),
    [
        (None, False, 401),
        (None, True, 403),
        ("support", True, 403),
        ("operations", True, 403),
        ("viewer", True, 200),
        ("content", True, 200),
        ("owner", True, 200),
    ],
)
async def test_read_capability_is_required(
    role: str | None, authenticated: bool, expected: int
) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=_app(role, authenticated=authenticated)), base_url="http://test"
    ) as client:
        response = await client.get(URL)
    assert response.status_code == expected


async def test_listing_has_typed_details_paging_and_global_counts() -> None:
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://test") as client:
        response = await client.get(URL)
        second = await client.get(URL, params={"page": 2})
        final = await client.get(URL, params={"page": 5, "page_size": 100})
        beyond = await client.get(URL, params={"page": 6, "page_size": 100})
    assert response.status_code == 200
    page = PlanPage.model_validate_json(response.content)
    assert (page.total, page.catalog_total, page.page, page.page_size) == (473, 473, 1, 25)
    assert len(page.items) == 25
    assert all(item.title and item.details for item in page.items)
    assert {count.catalog: count.count for count in page.catalogs} == CATALOG_COUNTS
    assert {count.stage: count.count for count in page.stages} == {
        "REVIEWED_OUTLINE_NOT_MEDIA": 192,
        "CHECKED_CANDIDATE_REQUIRES_OUTLINE": 100,
        "REVIEWED_STORY_PLAN_NOT_MEDIA": 100,
        "TERM_PLAN_NOT_MEDIA": 80,
        "COVERED_DO_NOT_REMAKE": 1,
    }
    first_ids = {item.video_slug for item in page.items}
    assert first_ids.isdisjoint(item["video_slug"] for item in second.json()["items"])
    assert len(final.json()["items"]) == 73
    assert beyond.json()["items"] == []
    assert beyond.json()["total"] == 473


async def test_catalog_stage_and_search_filters_keep_global_facets() -> None:
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://test") as client:
        brands = await client.get(URL, params={"catalog": "brand-stories", "page_size": 100})
        covered = await client.get(URL, params={"stage": "COVERED_DO_NOT_REMAKE"})
        combined = await client.get(
            URL, params={"catalog": "season2", "stage": "REVIEWED_OUTLINE_NOT_MEDIA"}
        )
        incompatible = await client.get(
            URL, params={"catalog": "season3", "stage": "TERM_PLAN_NOT_MEDIA"}
        )
        searched = await client.get(URL, params={"q": "  SOTHATSWHY-B01  "})
        blank = await client.get(URL, params={"q": "   "})
        absent = await client.get(URL, params={"q": "no-such-plan-fixture-12345"})
    assert brands.json()["total"] == 100
    assert all(item["target_duration_seconds"] == 780 for item in brands.json()["items"])
    assert covered.json()["total"] == 1
    assert covered.json()["items"][0]["catalog"] == "ai-terms"
    assert combined.json()["total"] == 92
    assert incompatible.json()["total"] == 0
    assert incompatible.json()["catalog_total"] == 473
    assert incompatible.json()["catalogs"] == brands.json()["catalogs"]
    assert searched.json()["total"] == 1
    assert searched.json()["items"][0]["id"] == "B01"
    assert blank.json()["total"] == 473
    assert absent.json()["items"] == []


async def test_search_does_not_match_cross_references_in_source_details(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, raw_bundle: dict[str, Any]
) -> None:
    raw_bundle["entries"][0]["details"][0]["text"] += " Details-Only-Needle %_"
    _install_bundle(monkeypatch, tmp_path, raw_bundle)
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://test") as client:
        response = await client.get(URL, params={"q": "details-only-needle %_"})
    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["items"] == []
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://test") as client:
        by_id = await client.get(URL, params={"q": raw_bundle["entries"][0]["video_slug"]})
    assert by_id.json()["total"] == 1
    assert by_id.json()["items"][0]["details"] == raw_bundle["entries"][0]["details"]


@pytest.mark.parametrize(
    "params",
    [
        {"page": 0},
        {"page_size": 0},
        {"page_size": 101},
        {"page_size": "invalid"},
        {"catalog": "shorts"},
        {"stage": "PUBLISHED"},
        {"q": "x" * 201},
    ],
)
async def test_invalid_query_is_rejected(params: dict[str, Any]) -> None:
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://test") as client:
        response = await client.get(URL, params=params)
    assert response.status_code == 422


@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE"])
async def test_catalog_has_no_mutation_routes(method: str) -> None:
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://test") as client:
        response = await client.request(method, URL, json={"enabled": True})
    assert response.status_code == 405


@pytest.mark.parametrize("failure", ["missing", "malformed", "oversized"])
async def test_unavailable_bundle_is_503_without_fallback(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, failure: str
) -> None:
    path = tmp_path / "catalog.json"
    if failure == "malformed":
        path.write_bytes(b"{broken-json")
    elif failure == "oversized":
        path.write_bytes(b"x" * 1025)
        monkeypatch.setattr(catalog, "MAX_CATALOG_BYTES", 1024)
    monkeypatch.setattr(catalog, "CATALOG_PATH", path)
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://test") as client:
        response = await client.get(URL)
    assert response.status_code == 503
    assert response.json()["code"] == "video_plans_unavailable"
    assert "items" not in response.json()


@pytest.mark.parametrize("locale", LOCALES)
async def test_catalog_unavailable_has_a_specific_sentence_in_the_requested_locale(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, locale: Locale
) -> None:
    monkeypatch.setattr(catalog, "CATALOG_PATH", tmp_path / "missing-catalog.json")
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://test") as client:
        response = await client.get(URL, headers={"X-Travel-Locale": locale})
    assert response.status_code == 503
    assert response.json()["code"] == "video_plans_unavailable"
    assert response.json()["detail"] != GENERIC_DETAILS[locale]
    if locale == "zh-TW":
        assert response.json()["detail"] == "影片企劃資料包缺漏或驗證失敗，請檢查部署版本"
    else:
        assert response.json()["detail"] == ERROR_DETAILS[locale]["video_plans_unavailable"]


@pytest.mark.parametrize(
    "failure",
    [
        "count",
        "duplicate",
        "legacy_duration",
        "wrong_catalog_duration",
        "stage",
        "hash",
        "path",
        "package_provenance",
        "details",
        "extra",
        "version",
        "boolean_version",
        "float_target",
        "float_minimum",
        "covered_removed",
        "covered_source_status",
        "outline_original_removed",
        "outline_effective_removed",
        "revised_chapters_removed",
    ],
)
async def test_invalid_bundle_is_rejected_instead_of_partial_success(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, raw_bundle: dict[str, Any], failure: str
) -> None:
    entry = raw_bundle["entries"][0]
    if failure == "count":
        raw_bundle["entries"].pop()
    elif failure == "duplicate":
        raw_bundle["entries"][1] = entry
    elif failure == "legacy_duration":
        entry["target_duration_seconds"] = 180
    elif failure == "wrong_catalog_duration":
        entry["target_duration_seconds"] = 780
    elif failure == "stage":
        entry["stage"] = "COVERED_DO_NOT_REMAKE"
    elif failure == "hash":
        entry["source_sha256"] = "invalid"
    elif failure == "path":
        entry["source_path"] = "docs/videos/../../secret"
    elif failure == "package_provenance":
        entry["source_package_sha256"] = None
    elif failure == "details":
        entry["details"] = []
    elif failure == "extra":
        entry["published"] = True
    elif failure == "version":
        raw_bundle["format_version"] = 2
    elif failure == "boolean_version":
        raw_bundle["format_version"] = True
    elif failure == "float_target":
        entry["target_duration_seconds"] = 600.0
    elif failure == "float_minimum":
        entry["min_duration_seconds"] = 480.0
    elif failure == "covered_removed":
        covered = next(
            item for item in raw_bundle["entries"] if item["stage"] == "COVERED_DO_NOT_REMAKE"
        )
        covered["stage"] = "TERM_PLAN_NOT_MEDIA"
        covered["source_status"] = "planned"
    elif failure == "covered_source_status":
        covered = next(
            item for item in raw_bundle["entries"] if item["stage"] == "COVERED_DO_NOT_REMAKE"
        )
        covered["source_status"] = "planned"
    elif failure == "outline_original_removed":
        entry["source_package_path"] = None
        entry["source_package_sha256"] = None
        entry["details"] = [
            detail for detail in entry["details"] if detail["label"] != "source_package"
        ]
    elif failure == "outline_effective_removed":
        entry["details"] = [
            detail for detail in entry["details"] if detail["label"] != "effective_inputs"
        ]
    elif failure == "revised_chapters_removed":
        revised = next(item for item in raw_bundle["entries"] if item["catalog"] == "season2")
        revised["details"] = [
            detail for detail in revised["details"] if detail["label"] != "effective_chapters"
        ]
    with pytest.raises(ValidationError):
        CatalogBundle.model_validate(raw_bundle)
    _install_bundle(monkeypatch, tmp_path, raw_bundle)
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://test") as client:
        response = await client.get(URL)
    assert response.status_code == 503
    assert response.json()["code"] == "video_plans_unavailable"


async def test_valid_read_does_not_hide_a_subsequent_broken_bundle(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, raw_bundle: dict[str, Any]
) -> None:
    _install_bundle(monkeypatch, tmp_path, raw_bundle)
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://test") as client:
        assert (await client.get(URL)).status_code == 200
        catalog.CATALOG_PATH.write_bytes(b"{interrupted-deployment")
        response = await client.get(URL)
    assert response.status_code == 503
    assert response.json()["code"] == "video_plans_unavailable"
