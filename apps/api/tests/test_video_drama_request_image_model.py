"""A one-off explainer request names its image model: what the request accepts, what the cute
presets are given, what is stored, and the filing that is refused when the site has no key for
the model's vendor (docs/videos/explainer-route/DESIGN.md section 4)."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError

from app.config import Settings
from app.db import SessionFactory
from app.models import AdminAuditLog, User, VideoToolToken
from app.video_automation import admin_api, schemas
from app.video_automation import requests as service
from app.video_automation import series as drama_series
from app.video_automation import settings as settings_service
from app.video_automation.models import VideoAutomationSettings, VideoDramaSeries
from app.video_automation.schemas import (
    PRESET_IMAGE_MODELS,
    DramaRequestIn,
    SeriesDocSubmitIn,
)
from app.video_media import jobs
from tests.test_video_drama_requests import ADMIN, FakeSession, _app, _owner, _row
from tests.test_video_series import clean_one_off, integration  # noqa: F401

QUESTION = "為什麼雷聲總比閃電晚到？"


def test_the_cute_presets_and_only_they_have_a_default_image_model() -> None:
    assert PRESET_IMAGE_MODELS == {"cute-cartoon": "image-01", "cute-mystery": "image-01"}


def test_an_explainer_may_name_its_image_model_and_a_cute_preset_takes_image_01() -> None:
    plain = DramaRequestIn(premise=QUESTION, style_preset="flat-explainer")
    assert plain.image_model is None, "flat-explainer with no model follows the settings"
    named = DramaRequestIn(premise=QUESTION, style_preset="flat-explainer", image_model="image-01")
    assert named.image_model == "image-01"
    for preset in ("cute-cartoon", "cute-mystery"):
        assert DramaRequestIn(premise=QUESTION, style_preset=preset).image_model == "image-01"
        explicit_null = DramaRequestIn.model_validate(
            {"premise": QUESTION, "style_preset": preset, "image_model": None}
        )
        assert explicit_null.image_model == "image-01"
    other = DramaRequestIn(
        premise=QUESTION, style_preset="cute-mystery", image_model="gemini-3-pro-image"
    )
    assert other.image_model == "gemini-3-pro-image", "a named model wins over the default"
    assert DramaRequestIn(premise="精衛填海").image_model is None, "a cast drama names none"


def test_a_cast_preset_an_unknown_model_and_an_empty_one_are_refused() -> None:
    for preset in ("cinematic-3d", "custom"):
        with pytest.raises(ValidationError, match="explainer preset only"):
            DramaRequestIn(premise="精衛填海", style_preset=preset, image_model="image-01")
    with pytest.raises(ValidationError, match="is not an image model of the media catalog"):
        DramaRequestIn(premise=QUESTION, style_preset="flat-explainer", image_model="image-99")
    with pytest.raises(ValidationError):
        DramaRequestIn(premise=QUESTION, style_preset="flat-explainer", image_model="")


def test_a_retired_default_is_refused_by_name_and_never_stored(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(schemas.PRESET_IMAGE_MODELS, "cute-mystery", "image-99")
    with pytest.raises(ValidationError, match="image-99 is not an image model"):
        DramaRequestIn(premise=QUESTION, style_preset="cute-mystery")


@pytest.mark.asyncio
async def test_the_one_off_series_row_and_the_audit_entry_carry_the_model() -> None:
    owner = _owner()
    session = FakeSession(None)
    await drama_series.create_one_off(
        session,  # type: ignore[arg-type]
        owner,
        DramaRequestIn(premise=QUESTION, style_preset="cute-mystery"),
    )
    series, _episode, _request, audit = session.added
    assert isinstance(series, VideoDramaSeries) and series.image_model == "image-01"
    assert isinstance(audit, AdminAuditLog)
    assert audit.metadata_json["image_model"] == "image-01"

    plain = FakeSession(None)
    await drama_series.create_one_off(
        plain,  # type: ignore[arg-type]
        owner,
        DramaRequestIn(premise=QUESTION, style_preset="flat-explainer"),
    )
    assert plain.added[0].image_model is None, "nothing that exists moves"
    assert plain.added[3].metadata_json["image_model"] is None


def _filing(monkeypatch: pytest.MonkeyPatch, runtime: Settings) -> tuple[AsyncMock, AsyncMock]:
    """The route with the drama switched on, the storing step stubbed and the site's keys set."""
    monkeypatch.setattr(
        settings_service,
        "settings_row",
        AsyncMock(return_value=VideoAutomationSettings(id=1, drama_enabled=True)),
    )
    create = AsyncMock(
        return_value=service.request_view(_row(episode_number=1), series_slug="one-off-1a2b3c4d")
    )
    monkeypatch.setattr(drama_series, "create_one_off", create)
    load = AsyncMock(return_value=runtime)
    monkeypatch.setattr(admin_api, "load_runtime_settings", load)
    return create, load


async def _post(body: dict[str, Any]) -> Any:
    async with AsyncClient(
        transport=ASGITransport(app=_app(_owner())), base_url="http://t"
    ) as client:
        return await client.post(ADMIN, json=body)


@pytest.mark.asyncio
async def test_a_cute_request_is_refused_at_filing_when_the_site_has_no_minimax_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create, load = _filing(
        monkeypatch, Settings(hotspot_guide_gemini_api_key="g", minimax_api_key="")
    )
    refused = await _post({"premise": QUESTION, "style_preset": "cute-cartoon"})
    assert refused.status_code == 409, refused.text
    assert refused.json()["code"] == "video_drama_image_model_not_configured"
    assert "minimax" in refused.json()["detail"] and "image-01" in refused.json()["detail"]
    named = await _post(
        {"premise": QUESTION, "style_preset": "flat-explainer", "image_model": "image-01"}
    )
    assert named.status_code == 409
    assert named.json()["code"] == "video_drama_image_model_not_configured"
    create.assert_not_awaited()
    assert load.await_count == 2


@pytest.mark.asyncio
async def test_a_cute_request_is_filed_with_image_01_when_the_site_has_the_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    create, _load = _filing(
        monkeypatch, Settings(hotspot_guide_gemini_api_key="g", minimax_api_key="m")
    )
    filed = await _post({"premise": QUESTION, "style_preset": "cute-cartoon"})
    assert filed.status_code == 201, filed.text
    payload = create.await_args.args[2]
    assert (payload.style_preset, payload.image_model) == ("cute-cartoon", "image-01")
    assert payload.target_minutes == 10


@pytest.mark.asyncio
async def test_a_request_that_names_no_model_reads_no_keys_and_a_cast_preset_takes_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_keys = Settings(hotspot_guide_gemini_api_key="", minimax_api_key="")
    create, load = _filing(monkeypatch, no_keys)
    plain = await _post({"premise": QUESTION, "style_preset": "flat-explainer"})
    assert plain.status_code == 201, plain.text
    assert create.await_args.args[2].image_model is None
    load.assert_not_awaited()
    cast = await _post(
        {"premise": "精衛填海", "style_preset": "cinematic-3d", "image_model": "image-01"}
    )
    assert cast.status_code == 422
    assert create.await_count == 1
    load.assert_not_awaited()


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_a_cute_one_off_is_drawn_with_the_model_its_request_stored(
    clean_one_off: list[str],  # noqa: F811
) -> None:
    async with SessionFactory() as session:
        owner = User(email=f"cute-{uuid4()}@example.com", password_hash="unused")
        session.add(owner)
        token = VideoToolToken(name="cute-test", token_hash=uuid4().hex, token_prefix="mkv_c")
        session.add(token)
        await session.commit()
        filed = await drama_series.create_one_off(
            session, owner, DramaRequestIn(premise=QUESTION, style_preset="cute-mystery")
        )
        assert filed.series_slug is not None
        slug = filed.series_slug
        clean_one_off.append(slug)
        bible = {
            "characters": [],
            "acts": [{"number": 1}],
            "outline": {
                "question": QUESTION,
                "answer": "光比聲音快太多。",
                "reasons": ["光速約每秒三十萬公里", "聲速約每秒三百四十公尺"],
                "hook": "閃電亮了，你數到幾？",
                "sources": ["https://en.wikipedia.org/wiki/Speed_of_sound"],
            },
        }
        await drama_series.submit_doc(
            session, slug, SeriesDocSubmitIn(kind="bible", body_md="# 企劃", body_json=bible)
        )
        await drama_series.decide_doc(
            session, owner, slug, "bible", 0, "approve", None, expected_version=1
        )
        started = await drama_series.start_episode(session, token, slug, 1, f"{slug}-e001")
        assert started.context.series.image_model == "image-01"
        assert await jobs.series_image_model(session, f"{slug}-e001") == "image-01"
        await session.delete(owner)
        await session.delete(token)
        await session.commit()
