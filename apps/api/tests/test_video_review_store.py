"""The preview store's size, set from the admin (owner, 2026-11-19), and its readout."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.admin.schemas import ProviderSettingsUpdate
from app.admin.service import (
    ALWAYS_ENABLED_PROVIDERS,
    PROVIDER_DEFINITIONS,
    _validate_provider_values,
    apply_runtime_overrides,
)
from app.auth.service import current_user
from app.config import Settings
from app.db import get_session
from app.models import ProviderConfig, User
from app.problems import AppError, app_error_handler
from app.video_reviews import admin_api
from app.video_reviews.admin_service import review_store

FIELD = "video_review_max_total_bytes"
GB = 1_000_000_000


def test_the_size_has_a_card_of_its_own_that_is_never_switched_off() -> None:
    owners = [name for name, item in PROVIDER_DEFINITIONS.items() if FIELD in item.config_fields]
    assert owners == ["video_reviews"]
    assert PROVIDER_DEFINITIONS["video_reviews"].secret_fields == ()
    assert "video_reviews" in ALWAYS_ENABLED_PROVIDERS


@pytest.mark.parametrize("value", [10_000_000, 20 * GB, 80 * GB, 500 * GB])
def test_the_size_accepts_whole_bytes_within_the_settings_range(value: int) -> None:
    update = ProviderSettingsUpdate(config={FIELD: value})
    assert _validate_provider_values("video_reviews", {}, update) == {FIELD: value}


@pytest.mark.parametrize("value", [9_999_999, 500 * GB + 1, 80.5 * GB, "80GB", True])
def test_the_size_refuses_values_outside_the_range_or_not_whole_bytes(value: object) -> None:
    with pytest.raises(AppError) as error:
        _validate_provider_values(
            "video_reviews", {}, ProviderSettingsUpdate(config={FIELD: value})
        )
    assert (error.value.status, error.value.code) == (422, "provider_setting_invalid")


def test_a_saved_size_beats_the_environment_and_is_the_one_the_store_enforces(
    tmp_path: Path,
) -> None:
    base = Settings(video_review_dir=str(tmp_path), video_review_max_total_bytes=60 * GB)
    rows = [ProviderConfig(provider="video_reviews", enabled=False, config={FIELD: 80 * GB})]
    effective = apply_runtime_overrides(base, rows)
    assert effective.video_review_max_total_bytes == 80 * GB
    assert review_store(effective).max_total_bytes == 80 * GB
    assert review_store(apply_runtime_overrides(base, [])).max_total_bytes == 60 * GB


def _app(user: User, settings: Settings) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[current_user] = lambda: user
    return app


def _user(*roles: str) -> User:
    user = User(id=uuid4(), email=f"{uuid4().hex}@example.test", password_hash="unused")
    user._admin_roles_cache = frozenset(roles)  # type: ignore[attr-defined]
    return user


@pytest.mark.asyncio
async def test_the_store_reports_what_it_holds_against_its_cap_and_the_disk(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    store_dir = tmp_path / "reviews"
    (store_dir / "a-video").mkdir(parents=True)
    (store_dir / "a-video" / "x").write_bytes(b"1" * 1000)
    (store_dir / "a-video" / "y").write_bytes(b"2" * 500)
    settings = Settings(video_review_dir=str(store_dir), video_review_max_total_bytes=80 * GB)

    async def runtime(_: Any) -> Settings:
        return settings

    monkeypatch.setattr(admin_api, "load_runtime_settings", runtime)
    url = "/api/v1/admin/videos/store"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("viewer"), settings)), base_url="http://test"
    ) as client:
        seen = await client.get(url)
    assert seen.status_code == 200, seen.text
    body = seen.json()
    assert body["used_bytes"] == 1500
    assert body["max_total_bytes"] == 80 * GB
    assert body["max_file_bytes"] == settings.video_review_max_file_bytes
    assert body["disk_total_bytes"] > 0 and body["disk_free_bytes"] >= 0

    # A store not made yet takes nothing and reads the disk it would live on.
    settings = Settings(video_review_dir=str(tmp_path / "later"))
    async with AsyncClient(
        transport=ASGITransport(app=_app(_user("owner"), settings)), base_url="http://test"
    ) as client:
        empty = (await client.get(url)).json()
    assert empty["used_bytes"] == 0 and empty["disk_total_bytes"] > 0

    async with AsyncClient(
        transport=ASGITransport(app=_app(_user(), settings)), base_url="http://test"
    ) as client:
        refused = await client.get(url)
    assert refused.status_code == 403, "no admin role, no readout"
