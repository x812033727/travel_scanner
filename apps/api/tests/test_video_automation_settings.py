"""The video automation settings: what they accept, who may change them, and the audio rule."""

from __future__ import annotations

import copy
import hashlib
import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import select

from app.auth.service import current_user
from app.config import Settings
from app.db import SessionFactory, engine, get_session
from app.models import AdminAuditLog, User, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api
from app.video_automation import settings as service
from app.video_automation.models import (
    DEFAULT_CAPTION_LOCALES,
    DEFAULT_DRAMA,
    DEFAULT_STAGE_MODELS,
    DEFAULT_TOPIC_AVOID,
    DEFAULT_TOPIC_SCOPE,
    DEFAULT_VOICE,
    STYLE_PRESETS,
    VideoAutomationSettings,
    VideoStagePrompt,
)
from app.video_automation.schemas import (
    SettingsView,
    SettingsWrite,
    StagePromptView,
    StageRunIn,
    VoiceOptionsView,
)
from app.video_reviews import admin_service as reviews
from app.video_reviews.schemas import ProjectIn, ReviewIn
from app.video_reviews.storage import ReviewStore
from app.video_speech import admin_api as speech_api


def _values(**changes: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "enabled": False,
        "draft_interval_hours": 72,
        "topics_per_run": 1,
        "max_waiting_drafts": 3,
        "topic_scope": list(DEFAULT_TOPIC_SCOPE),
        "topic_avoid": list(DEFAULT_TOPIC_AVOID),
        "topic_from_site": True,
        "topic_from_search": True,
        "stage_models": {stage: dict(choice) for stage, choice in DEFAULT_STAGE_MODELS.items()},
        "voice": dict(DEFAULT_VOICE),
        "target_minutes_min": 8,
        "target_minutes_max": 12,
        "caption_locales": list(DEFAULT_CAPTION_LOCALES),
        "max_drafts_per_month": 8,
        "monthly_token_budget_millions": 20,
        "max_verify_rounds": 3,
        "max_retake_rounds": 2,
        "auto_approve_audio": True,
        "drama": copy.deepcopy(DEFAULT_DRAMA),
        "stage_instructions": {},
        "channel_stance": "",
        "auto_pick_outline": True,
        "auto_approve_final": True,
    }
    values.update(changes)
    return values


def _drama(**changes: Any) -> dict[str, Any]:
    return {**copy.deepcopy(DEFAULT_DRAMA), **changes}


def _view_extras() -> dict[str, Any]:
    return {
        "model_options": service.model_options(),
        "configured_providers": ["anthropic"],
        "voice_options": VoiceOptionsView(gemini=["Sulafat"], gemini_models=[], azure=[]),
        "media_options": service.media_options_view(),
        "style_presets": list(STYLE_PRESETS),
        "updated_at": None,
    }


def test_the_defaults_are_a_valid_setting_the_server_can_run() -> None:
    payload = SettingsWrite(**_values())
    runtime = Settings(azure_speech_voices="zh-TW-HsiaoChenNeural")
    assert service.settings_problems(payload, runtime) == []
    assert payload.stage_models["verifier"].model == "claude-opus-5-5"
    assert payload.voice.name == "Sulafat"
    assert payload.drama.drama_enabled is False and payload.drama.clip_model


def test_drama_settings_the_server_cannot_run_are_named() -> None:
    runtime = Settings(hotspot_guide_gemini_api_key="g", azure_speech_voices="zh-TW-YunJheNeural")
    unknown = service.settings_problems(
        SettingsWrite(**_values(drama=_drama(clip_model="veo-9"))), runtime
    )
    assert unknown == ["片段：gemini 沒有 veo-9 這個模型"]
    seconds = service.settings_problems(
        SettingsWrite(
            **_values(drama=_drama(clip_model="veo-3.1-generate-001", clip_seconds_default=5))
        ),
        runtime,
    )
    assert seconds == ["片段：veo-3.1-generate-001 一次只能做 4、6、8 秒"]
    minimax = service.settings_problems(
        SettingsWrite(
            **_values(
                drama=_drama(
                    drama_enabled=True,
                    clip_provider="minimax",
                    clip_model="MiniMax-H3",
                    clip_resolution="1080p",
                )
            )
        ),
        runtime,
    )
    assert minimax == [
        "片段：MiniMax-H3 沒有 1080p，只有 768p、2k",
        "片段：網站還沒有 minimax 的金鑰，不能開啟漫劇",
    ]
    voices = service.settings_problems(
        SettingsWrite(
            **_values(
                drama=_drama(
                    character_voice_pool=[
                        {"provider": "gemini", "name": "Nobody"},
                        {"provider": "azure", "name": "zh-TW-YunJheNeural", "hint": "長者"},
                    ]
                )
            )
        ),
        runtime,
    )
    assert voices == ["角色聲音：Gemini 沒有 Nobody 這個聲音"]
    for bad in (
        _drama(character_voice_pool=[{"provider": "gemini", "name": "Kore"}] * 2),
        _drama(clip_seconds_default=11),
        _drama(style_preset="noir"),
        _drama(clip_resolution="4320p"),
        _drama(judge_min_score=11),
    ):
        with pytest.raises(ValidationError):
            SettingsWrite(**_values(drama=bad))


def test_the_storyboard_check_needs_the_threshold_and_no_problems() -> None:
    passed = {"shots": [{"id": "a"}, {"id": "b"}], "judge": {"overall": 8, "problems": []}}
    assert service.storyboard_check_passed(passed, 7)
    assert service.storyboard_check_passed({**passed, "judge": {"overall": 7.5}}, 7)
    assert not service.storyboard_check_passed(passed, 9)
    assert not service.storyboard_check_passed(
        {**passed, "judge": {"overall": 9, "problems": ["hands"]}}, 7
    )
    assert not service.storyboard_check_passed(
        {**passed, "shots": [{"id": "a", "needs_review": True}]}, 7
    )
    assert not service.storyboard_check_passed({**passed, "judge": {"overall": True}}, 0)
    assert not service.storyboard_check_passed({**passed, "shots": []}, 0)
    assert not service.storyboard_check_passed({}, 0)


def test_the_look_rule_needs_the_suggested_sheet_to_clear_the_threshold_with_no_problems() -> None:
    payload: dict[str, Any] = {
        "options": [
            {"key": "A", "judge": {"overall": 6, "problems": ["six fingers"]}},
            {"key": "B", "judge": {"overall": 8.5, "problems": []}},
        ],
        "suggested": "B",
    }
    assert service.look_pick_passed(payload, 7)
    assert not service.look_pick_passed(payload, 9)
    assert service.look_pick_note(payload) == "judge 給 B 8.5/10、沒有列出問題，依設定自動選"
    assert not service.look_pick_passed({**payload, "suggested": "A"}, 5), "problems listed"
    assert not service.look_pick_passed({**payload, "suggested": None}, 0), "nothing passed"
    assert not service.look_pick_passed({**payload, "suggested": "C"}, 0), "not an option"
    assert not service.look_pick_passed(
        {**payload, "options": [{"key": "B", "judge": {"overall": True}}]}, 0
    )
    assert not service.look_pick_passed({}, 0)


@pytest.mark.asyncio
async def test_a_sheet_is_picked_only_with_the_switch_on() -> None:
    payload: dict[str, Any] = {
        "options": [{"key": "B", "judge": {"overall": 8, "problems": []}}],
        "suggested": "B",
    }
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=SimpleNamespace(auto_pick_look=True, judge_min_score=7))
    assert await service.auto_picks_look(session, payload)
    session.scalar = AsyncMock(return_value=SimpleNamespace(auto_pick_look=True, judge_min_score=9))
    assert not await service.auto_picks_look(session, payload)
    session.scalar = AsyncMock(
        return_value=SimpleNamespace(auto_pick_look=False, judge_min_score=0)
    )
    assert not await service.auto_picks_look(session, payload)
    session.scalar = AsyncMock(return_value=None)
    assert not await service.auto_picks_look(session, payload), "off until the owner turns it on"


@pytest.mark.parametrize(
    "changes",
    [
        {"target_minutes_min": 13, "target_minutes_max": 12},
        {"topic_from_site": False, "topic_from_search": False},
        {"caption_locales": ["en", "en"]},
        {"caption_locales": ["zh-TW"]},
        {"stage_models": {"writer": {"provider": "anthropic", "model": "claude-sonnet-5"}}},
        {"draft_interval_hours": 1},
        {"topic_scope": []},
        {"topic_scope": ["x" * 41]},
        {"voice": {**DEFAULT_VOICE, "rate": "fast"}},
        {"unknown": 1},
    ],
)
def test_settings_that_cannot_be_stored_are_refused(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        SettingsWrite(**_values(**changes))


def test_models_and_voices_the_server_cannot_run_are_named() -> None:
    runtime = Settings(azure_speech_voices="zh-TW-HsiaoChenNeural")
    models = {stage: dict(choice) for stage, choice in DEFAULT_STAGE_MODELS.items()}
    models["writer"] = {"provider": "anthropic", "model": "gpt-6-astra"}
    models["verifier"] = {"provider": "gemini", "model": "gemini-2.5-pro"}
    problems = service.settings_problems(
        SettingsWrite(**_values(stage_models=models, voice={**DEFAULT_VOICE, "name": "Nobody"})),
        runtime,
    )
    assert len(problems) == 3
    assert any("writer" in problem and "gpt-6-astra" in problem for problem in problems)
    assert any("gemini-2.5-pro" in problem for problem in problems), (
        "a retired model is not offered"
    )
    azure = {"provider": "azure", "name": "zh-TW-YunJheNeural", "rate": "+5%"}
    assert service.settings_problems(SettingsWrite(**_values(voice=azure)), runtime) == [
        "zh-TW-YunJheNeural 不在 Azure 語音的允許清單裡"
    ]


def test_only_vendors_with_a_key_are_offered_as_configured() -> None:
    runtime = Settings(anthropic_api_key="a", hotspot_guide_gemini_api_key="g")
    assert service.configured_providers(runtime) == ["anthropic", "gemini"]
    options = service.model_options()
    assert "claude-opus-5-5" in {option.value for option in options["anthropic"]}
    assert all(option.status != "retired" for choices in options.values() for option in choices)


def test_the_audio_check_passes_only_when_every_line_was_checked_and_none_flagged() -> None:
    passed = {"check": {"lines": 157, "checked": 157, "flagged": 0}, "flagged_lines": []}
    assert service.audio_check_passed(passed)
    assert not service.audio_check_passed({**passed, "check": {**passed["check"], "flagged": 1}})
    assert not service.audio_check_passed({**passed, "check": {**passed["check"], "checked": 150}})
    assert not service.audio_check_passed({**passed, "flagged_lines": [{"id": "k7p2"}]})
    assert not service.audio_check_passed({"check": {"lines": 0, "checked": 0, "flagged": 0}})
    assert not service.audio_check_passed({})


def test_the_drama_s_own_models_and_voice_the_server_cannot_run_are_named() -> None:
    """The drama's stage models and narrator voice are checked like the tutorial's; None means
    it follows the tutorial's and is never a problem (docs/videos/DRAMA-FLOW.md §一)."""
    runtime = Settings(hotspot_guide_gemini_api_key="g", azure_speech_voices="zh-TW-YunJheNeural")
    models = {stage: dict(choice) for stage, choice in DEFAULT_STAGE_MODELS.items()}
    models["writer"] = {"provider": "anthropic", "model": "gpt-6-astra"}
    problems = service.settings_problems(
        SettingsWrite(
            **_values(
                drama=_drama(
                    drama_stage_models=models,
                    drama_voice={**DEFAULT_VOICE, "name": "Nobody", "model": "gemini-9-tts"},
                )
            )
        ),
        runtime,
    )
    assert problems == [
        "漫劇的 writer：anthropic 沒有 gpt-6-astra 這個可用的模型",
        "漫劇旁白：Gemini 沒有 Nobody 這個聲音",
        "漫劇旁白：Gemini 沒有 gemini-9-tts 這個語音模型",
    ]
    follows = SettingsWrite(**_values(drama=_drama(drama_stage_models=None, drama_voice=None)))
    assert service.settings_problems(follows, runtime) == []
    azure = {"provider": "azure", "name": "zh-TW-HsiaoYuNeural", "rate": "+0%"}
    assert service.settings_problems(
        SettingsWrite(**_values(drama=_drama(drama_voice=azure))), runtime
    ) == ["漫劇旁白：zh-TW-HsiaoYuNeural 不在 Azure 語音的允許清單裡"]
    for bad in (
        _drama(drama_stage_models={"writer": models["writer"]}),
        _drama(drama_caption_locales=["en", "en"]),
        _drama(drama_max_verify_rounds=0),
        _drama(drama_stage_instructions={"boss": "x"}),
    ):
        with pytest.raises(ValidationError):
            SettingsWrite(**_values(drama=bad))
    trimmed = SettingsWrite(
        **_values(drama=_drama(drama_stage_instructions={"writer": " 結尾留懸念 ", "planner": " "}))
    )
    assert trimmed.drama.drama_stage_instructions == {"writer": "結尾留懸念"}


@pytest.mark.asyncio
async def test_the_narration_and_final_rules_read_the_drama_s_own_switches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A drama has its own two switches (docs/videos/DRAMA-FLOW.md §一); the checks are shared,
    so the quality check is taken as passed here."""
    monkeypatch.setattr(service, "final_qa_passed", lambda _payload, _sha: True)
    passed = {"check": {"lines": 3, "checked": 3, "flagged": 0}, "flagged_lines": []}
    row = SimpleNamespace(
        auto_approve_audio=True,
        drama_auto_approve_audio=False,
        auto_approve_final=False,
        drama_auto_approve_final=True,
    )
    session = AsyncMock()
    session.scalar = AsyncMock(return_value=row)
    assert await service.auto_approves_audio(session, passed)
    assert await service.auto_approves_audio(session, passed, "slides")
    assert not await service.auto_approves_audio(session, passed, "drama")
    qa = {"qa": {"ok": True, "final_sha256": "f" * 64, "items": []}}
    assert not await service.auto_approves_final(session, "final", qa, "f" * 64)
    assert await service.auto_approves_final(session, "final", qa, "f" * 64, "drama")
    session.scalar = AsyncMock(return_value=None)
    assert await service.auto_approves_audio(session, passed, "drama"), "the default is on"


def _app(user: User | None = None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.tool_router, prefix="/api/v1")
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    if user is not None:
        app.dependency_overrides[current_user] = lambda: user
    return app


@pytest.mark.asyncio
async def test_a_viewer_reads_the_settings_and_only_a_settings_manager_changes_them(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    view = AsyncMock(return_value=SettingsView(**_values(), **_view_extras()))
    update = AsyncMock()
    monkeypatch.setattr(service, "settings_view", view)
    monkeypatch.setattr(service, "update_settings", update)
    url = "/api/v1/admin/video-automation/settings"
    async with AsyncClient(
        transport=ASGITransport(app=_app(viewer)), base_url="http://t"
    ) as client:
        read = await client.get(url)
        refused = await client.put(url, json=_values(enabled=True))
    assert read.status_code == 200 and read.json()["voice"]["name"] == "Sulafat"
    assert refused.status_code == 403
    update.assert_not_awaited()


def _owner() -> User:
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    return owner


def _stored(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    """Stored settings: the writer on Opus 5.5, the drama on; returns the mocked save."""
    stored = _values(
        drama=_drama(
            drama_enabled=True,
            max_usd_per_video=50,
            drama_stage_instructions={"writer": "每集結尾一個懸念"},
            drama_voice={**DEFAULT_VOICE, "name": "Kore"},
        )
    )
    stored["stage_models"]["writer"] = {"provider": "claude_code", "model": "claude-opus-5-5"}
    stored["stage_instructions"] = {"writer": "結尾留懸念"}
    stored["channel_stance"] = "1. 先把帳算清楚再花錢"
    stored["auto_pick_outline"] = False
    monkeypatch.setattr(
        service, "settings_row", AsyncMock(return_value=SimpleNamespace(updated_at=None))
    )
    monkeypatch.setattr(service, "settings_values", lambda _row: SettingsWrite(**stored))
    monkeypatch.setattr(
        admin_api,
        "load_runtime_settings",
        AsyncMock(return_value=Settings(hotspot_guide_gemini_api_key="g")),
    )

    async def save(_session: Any, _user: User, payload: SettingsWrite) -> SettingsView:
        return SettingsView(**payload.model_dump(), **_view_extras())

    update = AsyncMock(side_effect=save)
    monkeypatch.setattr(service, "update_settings", update)
    return update


@pytest.mark.asyncio
async def test_a_settings_save_without_stage_models_keeps_the_stored_ones(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The videos page no longer sends models, so it cannot undo a change made on AI settings."""
    update = _stored(monkeypatch)
    values = _values(enabled=True)
    del values["stage_models"]
    async with AsyncClient(
        transport=ASGITransport(app=_app(_owner())), base_url="http://t"
    ) as client:
        saved = await client.put("/api/v1/admin/video-automation/settings", json=values)
    assert saved.status_code == 200, saved.text
    payload = update.await_args.args[2]
    assert payload.enabled is True
    assert payload.stage_models["writer"].model == "claude-opus-5-5"


@pytest.mark.asyncio
async def test_a_settings_save_without_drama_keeps_the_stored_drama(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A page built before the drama settings existed sends none; it must not reset them."""
    update = _stored(monkeypatch)
    values = _values(enabled=True)
    del values["drama"]
    async with AsyncClient(
        transport=ASGITransport(app=_app(_owner())), base_url="http://t"
    ) as client:
        saved = await client.put("/api/v1/admin/video-automation/settings", json=values)
        lowered = await client.put(
            "/api/v1/admin/video-automation/settings",
            json=_values(drama=_drama(drama_enabled=True, max_usd_per_video=20)),
        )
        refused = await client.put(
            "/api/v1/admin/video-automation/settings",
            json=_values(
                drama=_drama(
                    drama_enabled=True,
                    clip_provider="minimax",
                    clip_model="MiniMax-H3",
                    clip_resolution="2k",
                )
            ),
        )
    assert saved.status_code == 200, saved.text
    kept = update.await_args_list[0].args[2]
    assert kept.drama.drama_enabled is True and kept.drama.max_usd_per_video == 50
    assert lowered.status_code == 200 and lowered.json()["drama"]["max_usd_per_video"] == 20
    assert refused.status_code == 422 and "minimax" in refused.text
    assert update.await_count == 2


@pytest.mark.asyncio
async def test_a_save_changes_only_the_fields_it_sends_at_both_levels(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The tab is three parts saved on their own (docs/videos/DRAMA-FLOW.md §一): a save of one
    field keeps every other stored value, and the drama object merges field by field, so a page
    from before a drama field existed cannot reset it by sending the object without it."""
    update = _stored(monkeypatch)
    url = "/api/v1/admin/video-automation/settings"
    older_drama = {
        key: value
        for key, value in _drama(drama_enabled=True, max_usd_per_video=50).items()
        if not key.startswith("drama_stage_")
        and key not in ("drama_voice", "drama_caption_locales")
    }
    async with AsyncClient(
        transport=ASGITransport(app=_app(_owner())), base_url="http://t"
    ) as client:
        one = await client.put(url, json={"enabled": True})
        drama_only = await client.put(
            url,
            json={
                "drama": _drama(
                    drama_enabled=True,
                    max_usd_per_video=50,
                    drama_stage_instructions={"writer": "", "verifier": "對照設定集"},
                    drama_stage_models=None,
                    drama_voice=None,
                    drama_caption_locales=["ja"],
                    drama_auto_approve_audio=False,
                )
            },
        )
        older = await client.put(url, json={"drama": older_drama})
        nulls = await client.put(url, json={"enabled": None, "channel_stance": None})
    assert one.status_code == 200, one.text
    first = update.await_args_list[0].args[2]
    assert first.enabled is True
    assert first.drama.drama_enabled is True and first.drama.max_usd_per_video == 50
    assert first.drama.drama_stage_instructions == {"writer": "每集結尾一個懸念"}
    assert first.stage_instructions == {"writer": "結尾留懸念"}
    assert first.channel_stance == "1. 先把帳算清楚再花錢" and first.auto_pick_outline is False
    assert drama_only.status_code == 200, drama_only.text
    second = update.await_args_list[1].args[2]
    assert second.enabled is False, "the tutorial part was not sent, so it stays"
    assert second.drama.drama_stage_instructions == {"verifier": "對照設定集"}
    assert second.drama.drama_voice is None and second.drama.drama_caption_locales == ["ja"]
    assert second.drama.drama_auto_approve_audio is False
    assert older.status_code == 200, older.text
    third = update.await_args_list[2].args[2]
    assert third.drama.drama_stage_instructions == {"writer": "每集結尾一個懸念"}
    assert third.drama.drama_voice is not None and third.drama.drama_voice.name == "Kore"
    assert nulls.status_code == 200, nulls.text
    fourth = update.await_args_list[3].args[2]
    assert fourth.enabled is False and fourth.channel_stance == "1. 先把帳算清楚再花錢"


@pytest.mark.asyncio
async def test_a_merged_save_that_does_not_hold_together_is_refused_not_a_server_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The bounds and the consistency rules live on SettingsWrite; a partial save can only be
    checked once it lies over what is stored, and a failure there is the client's 422."""
    update = _stored(monkeypatch)
    url = "/api/v1/admin/video-automation/settings"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_owner())), base_url="http://t"
    ) as client:
        inverted = await client.put(url, json={"target_minutes_min": 13})
        out_of_range = await client.put(url, json={"draft_interval_hours": 1})
        no_source = await client.put(
            url, json={"topic_from_site": False, "topic_from_search": False}
        )
        unknown = await client.put(url, json={"boss": 1})
    assert inverted.status_code == 422 and "target_minutes_min" in inverted.text
    assert out_of_range.status_code == 422 and "draft_interval_hours" in out_of_range.text
    assert no_source.status_code == 422
    assert unknown.status_code == 422
    update.assert_not_awaited()


@pytest.mark.asyncio
async def test_the_models_route_sets_the_drama_s_models_and_null_follows_the_tutorial(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    update = _stored(monkeypatch)
    models = {stage: dict(choice) for stage, choice in DEFAULT_STAGE_MODELS.items()}
    drama_models = {stage: dict(choice) for stage, choice in DEFAULT_STAGE_MODELS.items()}
    drama_models["writer"] = {"provider": "claude_code", "model": "claude-opus-5-5"}
    url = "/api/v1/admin/video-automation/settings/models"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_owner())), base_url="http://t"
    ) as client:
        chosen = await client.put(
            url, json={"stage_models": models, "drama_stage_models": drama_models}
        )
        kept = await client.put(url, json={"stage_models": models})
        follows = await client.put(url, json={"stage_models": models, "drama_stage_models": None})
        incomplete = await client.put(
            url,
            json={"stage_models": models, "drama_stage_models": {"writer": drama_models["writer"]}},
        )
        unknown = await client.put(
            url,
            json={
                "stage_models": models,
                "drama_stage_models": {
                    **drama_models,
                    "writer": {"provider": "anthropic", "model": "gpt-6-sol"},
                },
            },
        )
    assert chosen.status_code == 200, chosen.text
    first = update.await_args_list[0].args[2]
    assert first.drama.drama_stage_models is not None
    assert first.drama.drama_stage_models["writer"].model == "claude-opus-5-5"
    assert first.drama.max_usd_per_video == 50, "the rest of the drama stays"
    assert kept.status_code == 200 and kept.json()["drama"]["drama_stage_models"] is None, (
        "the stored choice (None in the fixture) stays when the page sends nothing"
    )
    assert follows.status_code == 200 and follows.json()["drama"]["drama_stage_models"] is None
    assert incomplete.status_code == 422
    assert unknown.status_code == 422 and "gpt-6-sol" in unknown.text
    assert update.await_count == 3


def test_standing_instructions_are_trimmed_and_an_emptied_one_is_dropped() -> None:
    payload = SettingsWrite(
        **_values(stage_instructions={"writer": "  結尾留下一集的懸念  ", "planner": "   "})
    )
    assert payload.stage_instructions == {"writer": "結尾留下一集的懸念"}
    without = {key: value for key, value in _values().items() if key != "stage_instructions"}
    assert SettingsWrite(**without).stage_instructions == {}
    with pytest.raises(ValidationError):
        SettingsWrite(**_values(stage_instructions={"writer": "長" * 4001}))
    with pytest.raises(ValidationError):
        SettingsWrite(**_values(stage_instructions={"boss": "x"}))


@pytest.mark.asyncio
async def test_a_settings_save_without_standing_instructions_keeps_the_stored_ones(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A page from before the instructions existed sends none; an emptied field drops one."""
    update = _stored(monkeypatch)
    values = _values(enabled=True)
    del values["stage_instructions"]
    url = "/api/v1/admin/video-automation/settings"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_owner())), base_url="http://t"
    ) as client:
        kept = await client.put(url, json=values)
        changed = await client.put(
            url, json=_values(stage_instructions={"writer": "", "verifier": "對照山海經原文"})
        )
    assert kept.status_code == 200, kept.text
    assert update.await_args_list[0].args[2].stage_instructions == {"writer": "結尾留懸念"}
    assert changed.status_code == 200, changed.text
    assert changed.json()["stage_instructions"] == {"verifier": "對照山海經原文"}


def test_the_stance_is_trimmed_and_capped_and_the_switches_default_on_except_the_look() -> None:
    payload = SettingsWrite(**_values(channel_stance="  1. 官方原文優先  "))
    assert payload.channel_stance == "1. 官方原文優先"
    assert payload.auto_pick_outline and payload.auto_approve_final
    assert payload.drama.auto_pick_look is False
    without = {
        key: value
        for key, value in _values().items()
        if key not in ("channel_stance", "auto_pick_outline", "auto_approve_final")
    }
    assert SettingsWrite(**without).channel_stance == ""
    with pytest.raises(ValidationError):
        SettingsWrite(**_values(channel_stance="長" * 4001))


@pytest.mark.asyncio
async def test_a_settings_save_without_the_stance_or_the_switches_keeps_the_stored_ones(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A page from before the hands-off switches existed sends none; it must not reset them."""
    update = _stored(monkeypatch)
    values = _values(enabled=True)
    for key in ("channel_stance", "auto_pick_outline", "auto_approve_final"):
        del values[key]
    url = "/api/v1/admin/video-automation/settings"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_owner())), base_url="http://t"
    ) as client:
        kept = await client.put(url, json=values)
        changed = await client.put(
            url,
            json=_values(
                channel_stance="2. 官方原文優先",
                auto_approve_final=False,
                drama=_drama(auto_pick_look=True),
            ),
        )
    assert kept.status_code == 200, kept.text
    first = update.await_args_list[0].args[2]
    assert first.channel_stance == "1. 先把帳算清楚再花錢"
    assert first.auto_pick_outline is False and first.auto_approve_final is True
    assert changed.status_code == 200, changed.text
    body = changed.json()
    assert body["channel_stance"] == "2. 官方原文優先"
    assert body["auto_pick_outline"] is True and body["auto_approve_final"] is False
    assert body["drama"]["auto_pick_look"] is True


@pytest.mark.asyncio
async def test_the_worker_reads_the_stance_and_the_switches_with_the_settings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _stored(monkeypatch)
    app = _app()
    token = VideoToolToken(id=uuid4(), name="worker", token_hash="h", token_prefix="mkv_w")
    app.dependency_overrides[speech_api.video_tool] = lambda: token
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        response = await client.get("/api/v1/video/automation/settings")
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["channel_stance"] == "1. 先把帳算清楚再花錢"
    assert (body["auto_pick_outline"], body["auto_approve_final"]) == (False, True)
    assert body["drama"]["auto_pick_look"] is False
    # The drama's own copies (docs/videos/DRAMA-FLOW.md §一), which the worker reads by format.
    assert body["drama"]["drama_stage_instructions"] == {"writer": "每集結尾一個懸念"}
    assert body["drama"]["drama_voice"]["name"] == "Kore"
    assert body["drama"]["drama_stage_models"] is None
    assert (body["drama"]["drama_max_verify_rounds"], body["drama"]["drama_max_retake_rounds"]) == (
        3,
        2,
    )


@pytest.mark.asyncio
async def test_the_prompt_a_stage_was_sent_is_kept_per_format_and_read_in_stage_order() -> None:
    session = AsyncMock()
    await service.remember_prompt(
        session,
        StageRunIn(
            stage="writer", slug="jingwei", instructions="Write it.", payload={}, format="drama"
        ),
    )
    kept = session.merge.await_args.args[0]
    assert isinstance(kept, VideoStagePrompt)
    assert (kept.stage, kept.format, kept.slug, kept.instructions) == (
        "writer",
        "drama",
        "jingwei",
        "Write it.",
    )
    assert kept.sent_at.tzinfo is not None

    when = datetime(2026, 9, 26, 15, 0, tzinfo=UTC)
    rows = [
        VideoStagePrompt(stage="writer", format="drama", slug="b", instructions="B", sent_at=when),
        VideoStagePrompt(
            stage="planner", format="slides", slug="a", instructions="A", sent_at=when
        ),
        VideoStagePrompt(stage="writer", format="slides", slug="c", instructions="C", sent_at=when),
    ]
    found = MagicMock()
    found.all.return_value = rows
    session.scalars = AsyncMock(return_value=found)
    prompts = await service.stage_prompts(session)
    assert [(prompt.stage, prompt.format, prompt.slug) for prompt in prompts] == [
        ("planner", "slides", "a"),
        ("writer", "slides", "c"),
        ("writer", "drama", "b"),
    ]


@pytest.mark.asyncio
async def test_a_viewer_reads_the_prompts_as_they_were_sent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    when = datetime(2026, 9, 26, 15, 0, tzinfo=UTC)
    prompt = StagePromptView(
        stage="planner", format="slides", slug="a", instructions="Plan.", sent_at=when
    )
    monkeypatch.setattr(service, "stage_prompts", AsyncMock(return_value=[prompt]))
    async with AsyncClient(
        transport=ASGITransport(app=_app(viewer)), base_url="http://t"
    ) as client:
        read = await client.get("/api/v1/admin/video-automation/prompts")
    assert read.status_code == 200, read.text
    assert read.json()["prompts"] == [
        {
            "stage": "planner",
            "format": "slides",
            "variant": "",
            "slug": "a",
            "instructions": "Plan.",
            "sent_at": "2026-09-26T15:00:00Z",
        }
    ]


@pytest.mark.asyncio
async def test_the_models_route_changes_only_the_stage_models_and_checks_them(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    update = _stored(monkeypatch)
    models = {stage: dict(choice) for stage, choice in DEFAULT_STAGE_MODELS.items()}
    models["verifier"] = {"provider": "anthropic", "model": "claude-sonnet-5"}
    url = "/api/v1/admin/video-automation/settings/models"
    async with AsyncClient(
        transport=ASGITransport(app=_app(_owner())), base_url="http://t"
    ) as client:
        saved = await client.put(url, json={"stage_models": models})
        models["writer"] = {"provider": "anthropic", "model": "gpt-6-sol"}
        refused = await client.put(url, json={"stage_models": models})
        incomplete = await client.put(url, json={"stage_models": {"writer": models["writer"]}})
    assert saved.status_code == 200, saved.text
    payload = update.await_args.args[2]
    assert payload.stage_models["verifier"].model == "claude-sonnet-5"
    assert payload.draft_interval_hours == 72 and payload.enabled is False
    assert refused.status_code == 422 and "gpt-6-sol" in refused.text
    assert incomplete.status_code == 422
    assert update.await_count == 1


@pytest.mark.asyncio
async def test_the_tool_route_needs_a_video_tool_token() -> None:
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://t") as client:
        response = await client.get("/api/v1/video/automation/settings")
        videos = await client.get("/api/v1/video/automation/videos")
    assert response.status_code == 401 and videos.status_code == 401


@pytest.mark.asyncio
async def test_the_worker_lists_every_video_dropped_ones_included(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    listed = AsyncMock(return_value=[])
    monkeypatch.setattr(admin_api, "list_projects", listed)
    app = _app()
    token = VideoToolToken(id=uuid4(), name="worker", token_hash="h", token_prefix="mkv_w")
    app.dependency_overrides[speech_api.video_tool] = lambda: token
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        response = await client.get("/api/v1/video/automation/videos")
    assert response.status_code == 200 and response.json() == []
    listed.assert_awaited_once()


# Against PostgreSQL, as CI runs it.
integration = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


@pytest_asyncio.fixture(loop_scope="module")
async def clean_settings() -> AsyncIterator[None]:
    yield
    async with SessionFactory() as session:
        row = await session.get(VideoAutomationSettings, 1)
        if row is not None:
            await session.delete(row)
            await session.commit()
    await engine.dispose()


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_settings_start_from_defaults_save_with_an_audit_entry_and_read_back(
    clean_settings: None,
) -> None:
    async with SessionFactory() as session:
        owner = User(email=f"video-automation-{uuid4()}@example.com", password_hash="unused")
        session.add(owner)
        await session.commit()
        first = await service.settings_view(session)
        assert first.enabled is False and first.draft_interval_hours == 72
        assert first.channel_stance == "" and first.auto_pick_outline and first.auto_approve_final
        assert first.drama.auto_pick_look is False
        assert first.drama.drama_stage_models is None and first.drama.drama_voice is None
        assert first.drama.drama_stage_instructions == {} and first.drama.drama_auto_approve_audio
        saved = await service.update_settings(
            session, owner, SettingsWrite(**_values(enabled=True, draft_interval_hours=48))
        )
        assert saved.enabled and saved.draft_interval_hours == 48
        audit = await session.scalar(
            select(AdminAuditLog)
            .where(AdminAuditLog.action == "video_automation_settings_updated")
            .order_by(AdminAuditLog.created_at.desc())
        )
        assert audit is not None
        assert audit.metadata_json["changed"] == ["draft_interval_hours", "enabled"]


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_narration_jev_passed_is_approved_as_it_arrives_unless_the_owner_turned_it_off(
    clean_settings: None, tmp_path: Path
) -> None:
    slug = f"it-{uuid4().hex[:12]}"
    store = ReviewStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    passed = {"check": {"lines": 3, "checked": 3, "flagged": 0}, "flagged_lines": []}
    async with SessionFactory() as session:
        owner = User(email=f"video-automation-{uuid4()}@example.com", password_hash="unused")
        token = VideoToolToken(name="it", token_hash=uuid4().hex * 2, token_prefix="mkv_it")
        session.add_all([owner, token])
        await session.commit()
        await reviews.upsert_project(
            session, store, slug, ProjectIn(title="t", stage="audio", checklist=[])
        )

        def review(body: bytes, payload: dict[str, Any]) -> ReviewIn:
            return ReviewIn(
                gate="audio",
                content_sha256=hashlib.sha256(body).hexdigest(),
                summary="narration",
                payload=payload,
                files=[],
            )

        approved = await reviews.submit_review(session, store, slug, review(b"a", passed), token)
        assert approved.status == "approved" and approved.note == service.AUTO_APPROVED_NOTE
        flagged = {**passed, "check": {**passed["check"], "flagged": 1}}
        waiting = await reviews.submit_review(session, store, slug, review(b"b", flagged), token)
        assert waiting.status == "pending"

        await service.update_settings(
            session, owner, SettingsWrite(**_values(auto_approve_audio=False))
        )
        off = await reviews.submit_review(session, store, slug, review(b"c", passed), token)
        assert off.status == "pending", "with the setting off the owner decides"
