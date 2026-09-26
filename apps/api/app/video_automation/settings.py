"""The one row of video automation settings: reading, validating and saving it."""

from __future__ import annotations

from typing import Any, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.ai.catalog import MODEL_CATALOG, Capability
from app.config import Settings
from app.models import AdminAuditLog, User
from app.video_automation.models import DRAMA_FIELDS, STYLE_PRESETS, VideoAutomationSettings
from app.video_automation.schemas import (
    ApiProviderName,
    DramaSettings,
    MediaOptionsView,
    MediaOptionView,
    MediaProvider,
    ModelOptionView,
    ProviderName,
    SettingsView,
    SettingsWrite,
    VoiceOptionsView,
)
from app.video_automation.usage import usage_view
from app.video_media.catalog import MEDIA_VENDORS, MediaKind, find_model, media_options
from app.video_speech.gemini import GEMINI_TTS_MODELS, PREBUILT_VOICES

# The stages run through the same vendor adapters as the news writer and verifier
# (app.hotspots.ai_search), so a vendor offers the catalog models that can drive them.
MODEL_CAPABILITY: dict[ApiProviderName, Capability] = {
    "openai": "responses_json_schema_strict",
    "anthropic": "anthropic_structured_output",
    "minimax": "responses_json_schema_strict",
    "gemini": "gemini_structured",
}
AUTO_APPROVED_NOTE = "Jev 判斷每一句都唸對了，依設定自動核准"
AUTO_APPROVED_STORYBOARD_NOTE = "judge 給每一鏡的分數都達到門檻、沒有列出問題，依設定自動核准"


def _options(entries: Any, capability: Capability | None) -> list[ModelOptionView]:
    return [
        ModelOptionView(
            value=entry.id, label=entry.label, description=entry.note, status=entry.status
        )
        for entry in entries
        if (capability is None or capability in entry.capabilities) and entry.status != "retired"
    ]


def model_options() -> dict[ProviderName, list[ModelOptionView]]:
    options: dict[ProviderName, list[ModelOptionView]] = {
        # Claude Code takes the same model names as the API; it runs them on the subscription.
        "claude_code": _options(MODEL_CATALOG["anthropic"], None),
    }
    for provider, capability in MODEL_CAPABILITY.items():
        options[provider] = _options(MODEL_CATALOG[provider], capability)
    return options


def configured_providers(runtime: Settings) -> list[ProviderName]:
    keys: dict[ProviderName, str | bool | None] = {
        # Whether the host agent is reachable is only known when a stage runs; configured here
        # means the API has what it needs to ask it.
        "claude_code": runtime.ai_accounts_configured,
        "openai": runtime.openai_api_key,
        "anthropic": runtime.anthropic_api_key,
        "minimax": runtime.minimax_api_key,
        "gemini": runtime.hotspot_guide_gemini_api_key,
    }
    return [provider for provider, key in keys.items() if key]


def voice_options(runtime: Settings) -> VoiceOptionsView:
    return VoiceOptionsView(
        gemini=list(PREBUILT_VOICES),
        gemini_models=list(GEMINI_TTS_MODELS),
        azure=list(runtime.azure_speech_voice_list),
    )


def _media_options(kind: MediaKind) -> dict[MediaProvider, list[MediaOptionView]]:
    return {
        vendor: [
            MediaOptionView(
                value=model.id,
                label=model.label,
                description=model.note,
                status=model.status,
                resolutions=list(model.resolutions),
                durations=list(model.durations),
                reference_images=model.reference_images,
                native_audio=model.native_audio,
                usd_per_second=model.usd_per_second,
                usd_per_image=model.usd_per_image,
                usd_per_track=model.usd_per_track,
            )
            for model in media_options(vendor, kind)
        ]
        for vendor in MEDIA_VENDORS
    }


def media_options_view() -> MediaOptionsView:
    """The image, clip and music models the drama section of the settings tab can offer."""
    return MediaOptionsView(
        images=_media_options("image"), clips=_media_options("clip"), music=_media_options("music")
    )


def drama_values(row: VideoAutomationSettings) -> DramaSettings:
    return DramaSettings(**{field: getattr(row, field) for field in DRAMA_FIELDS})


async def settings_row(session: AsyncSession, *, lock: bool = False) -> VideoAutomationSettings:
    statement = select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    if lock:
        statement = statement.with_for_update()
    row = await session.scalar(statement)
    if row is None:
        row = VideoAutomationSettings(id=1)
        session.add(row)
        await session.flush()
    return row


def settings_values(row: VideoAutomationSettings) -> SettingsWrite:
    return SettingsWrite(
        enabled=row.enabled,
        draft_interval_hours=row.draft_interval_hours,
        topics_per_run=row.topics_per_run,
        max_waiting_drafts=row.max_waiting_drafts,
        topic_scope=list(row.topic_scope),
        topic_avoid=list(row.topic_avoid),
        topic_from_site=row.topic_from_site,
        topic_from_search=row.topic_from_search,
        stage_models=cast(Any, row.stage_models),
        voice=cast(Any, row.voice),
        target_minutes_min=row.target_minutes_min,
        target_minutes_max=row.target_minutes_max,
        caption_locales=cast(Any, row.caption_locales),
        max_drafts_per_month=row.max_drafts_per_month,
        monthly_token_budget_millions=row.monthly_token_budget_millions,
        max_verify_rounds=row.max_verify_rounds,
        max_retake_rounds=row.max_retake_rounds,
        auto_approve_audio=row.auto_approve_audio,
        drama=drama_values(row),
    )


async def settings_view(session: AsyncSession) -> SettingsView:
    row = await settings_row(session)
    runtime = await load_runtime_settings(session)
    return SettingsView(
        **settings_values(row).model_dump(),
        model_options=model_options(),
        configured_providers=configured_providers(runtime),
        voice_options=voice_options(runtime),
        media_options=media_options_view(),
        style_presets=list(STYLE_PRESETS),
        usage=await usage_view(session, row),
        updated_at=row.updated_at,
    )


def _voice_problem(provider: str, name: str, runtime: Settings) -> str | None:
    if provider == "gemini":
        return None if name in PREBUILT_VOICES else f"Gemini 沒有 {name} 這個聲音"
    return (
        None if name in runtime.azure_speech_voice_list else f"{name} 不在 Azure 語音的允許清單裡"
    )


def drama_problems(drama: DramaSettings, runtime: Settings) -> list[str]:
    """What the drama settings name that the server cannot serve (docs/videos/DRAMA.md)."""
    problems: list[str] = []
    configured = set(configured_providers(runtime))
    choices: tuple[tuple[MediaKind, str, MediaProvider, str], ...] = (
        ("image", "圖片", drama.image_provider, drama.image_model),
        ("clip", "片段", drama.clip_provider, drama.clip_model),
        ("music", "音樂", drama.music_provider, drama.music_model),
    )
    for kind, label, provider, model_id in choices:
        model = find_model(provider, kind, model_id)
        if model is None:
            problems.append(f"{label}：{provider} 沒有 {model_id} 這個模型")
            continue
        if model.status == "retired":
            problems.append(f"{label}：{model_id} 已經退役，請換一個模型")
        if kind == "clip":
            if drama.clip_resolution not in model.resolutions:
                problems.append(
                    f"片段：{model_id} 沒有 {drama.clip_resolution}，"
                    f"只有 {'、'.join(model.resolutions)}"
                )
            if drama.clip_seconds_default not in model.durations:
                problems.append(
                    f"片段：{model_id} 一次只能做 {'、'.join(map(str, model.durations))} 秒"
                )
        if drama.drama_enabled and provider not in configured:
            problems.append(f"{label}：網站還沒有 {provider} 的金鑰，不能開啟漫劇")
    for voice in drama.character_voice_pool:
        problem = _voice_problem(voice.provider, voice.name, runtime)
        if problem:
            problems.append(f"角色聲音：{problem}")
    return problems


def settings_problems(payload: SettingsWrite, runtime: Settings) -> list[str]:
    """What the server cannot run as written: a model a vendor cannot serve, or a voice it lacks."""
    problems: list[str] = []
    options = model_options()
    for stage, choice in payload.stage_models.items():
        if choice.model not in {option.value for option in options[choice.provider]}:
            problems.append(f"{stage}：{choice.provider} 沒有 {choice.model} 這個可用的模型")
    voice = payload.voice
    if voice.provider == "gemini":
        if voice.name not in PREBUILT_VOICES:
            problems.append(f"Gemini 沒有 {voice.name} 這個聲音")
        if voice.model is not None and voice.model not in GEMINI_TTS_MODELS:
            problems.append(f"Gemini 沒有 {voice.model} 這個語音模型")
    elif voice.name not in runtime.azure_speech_voice_list:
        problems.append(f"{voice.name} 不在 Azure 語音的允許清單裡")
    problems.extend(drama_problems(payload.drama, runtime))
    return problems


def _flat(values: dict[str, Any]) -> dict[str, Any]:
    """The drama object spread onto the row's columns, for saving and for the audit diff."""
    flat = {key: value for key, value in values.items() if key != "drama"}
    flat.update(values.get("drama") or {})
    return flat


async def update_settings(
    session: AsyncSession, actor: User, payload: SettingsWrite
) -> SettingsView:
    """Save settings ``settings_problems`` has already passed; the admin router checks first."""
    row = await settings_row(session, lock=True)
    before = _flat(settings_values(row).model_dump(mode="json"))
    after = _flat(payload.model_dump(mode="json"))
    for key, value in after.items():
        setattr(row, key, value)
    row.updated_by_user_id = actor.id
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_automation_settings_updated",
            target="video-automation-settings:1",
            metadata_json={
                "changed": sorted(key for key in after if after[key] != before.get(key)),
                "enabled": payload.enabled,
            },
        )
    )
    await session.commit()
    return await settings_view(session)


def audio_check_passed(payload: dict[str, Any]) -> bool:
    """Whether a narration review's check says Jev passed every line, none left unchecked."""
    check = payload.get("check")
    if not isinstance(check, dict):
        return False
    lines, checked, flagged = check.get("lines"), check.get("checked"), check.get("flagged")
    return (
        isinstance(lines, int)
        and lines > 0
        and checked == lines
        and flagged == 0
        and not payload.get("flagged_lines")
    )


async def auto_approves_audio(session: AsyncSession, payload: dict[str, Any]) -> bool:
    row = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    # With no row yet the defaults apply, and the default is on (the owner's 2026-09-25 choice).
    enabled = True if row is None else row.auto_approve_audio
    return enabled and audio_check_passed(payload)


def storyboard_check_passed(payload: dict[str, Any], min_score: int) -> bool:
    """Whether a storyboard review's judge summary clears the owner's threshold with no problems.

    The payload carries {"shots": [...], "judge": {"overall": 0-10, "problems": [...]}} from
    the keyframes stage; a shot left for a prompt fix (needs_review) never auto-approves.
    """
    judge = payload.get("judge")
    shots = payload.get("shots")
    if not isinstance(judge, dict) or not isinstance(shots, list) or not shots:
        return False
    overall = judge.get("overall")
    problems = judge.get("problems")
    if not isinstance(overall, int | float) or isinstance(overall, bool):
        return False
    if problems not in (None, []):
        return False
    if any(isinstance(shot, dict) and shot.get("needs_review") for shot in shots):
        return False
    return overall >= min_score


async def auto_approves_storyboard(session: AsyncSession, payload: dict[str, Any]) -> bool:
    row = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    # Off by default: the owner looks at the first drama's keyframes before any clip is paid for.
    if row is None or not row.auto_approve_storyboard:
        return False
    return storyboard_check_passed(payload, row.judge_min_score)
