"""The one row of video automation settings: reading, validating and saving it."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, cast, get_args

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.ai.catalog import MODEL_CATALOG, Capability
from app.config import Settings
from app.models import AdminAuditLog, User
from app.video_automation.anime_policy import is_long_anime
from app.video_automation.judge import (
    COMPILATION_QA_ITEMS,
    QA_ITEMS,
    final_qa_passed,
    outline_pick_passed,
    publish_package_passed,
    retention_required_for,
    script_check_passed,
)
from app.video_automation.models import (
    DRAMA_FIELDS,
    SLIDES_FIELDS,
    STYLE_PRESETS,
    VideoAutomationSettings,
    VideoDramaSeries,
    VideoStagePrompt,
)
from app.video_automation.schemas import (
    CAPTION_LOCALES,
    ApiProviderName,
    DramaSettings,
    MediaOptionsView,
    MediaOptionView,
    MediaProvider,
    ModelOptionView,
    ProviderName,
    SettingsView,
    SettingsWrite,
    SlidesSettings,
    Stage,
    StagePromptView,
    StageRunIn,
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
AUTO_PICKED_LOOK_NOTE = "judge 給 {key} {score:g}/10、沒有列出問題，依設定自動選"


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
        "codex": _options(MODEL_CATALOG["openai"], None),
    }
    for provider, capability in MODEL_CAPABILITY.items():
        options[provider] = _options(MODEL_CATALOG[provider], capability)
    return options


def configured_providers(runtime: Settings) -> list[ProviderName]:
    keys: dict[ProviderName, str | bool | None] = {
        # Whether the host agent is reachable is only known when a stage runs; configured here
        # means the API has what it needs to ask it.
        "claude_code": runtime.ai_accounts_configured,
        "codex": runtime.ai_accounts_configured,
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
                style_references=model.style_references,
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


def current_caption_locales(stored: Any) -> list[str]:
    """A stored caption-language list as the page knows it: a language the videos are no longer
    made in (zh-CN before 2026-10-09) is dropped rather than refused. Migration 0128 removes it
    from the rows; this keeps a row written between the deploy's steps readable."""
    values = stored if isinstance(stored, list) else []
    return [locale for locale in values if locale in CAPTION_LOCALES]


def drama_values(row: VideoAutomationSettings) -> DramaSettings:
    values = {field: getattr(row, field) for field in DRAMA_FIELDS}
    values["drama_caption_locales"] = current_caption_locales(values["drama_caption_locales"])
    return DramaSettings(**values)


def slides_values(row: VideoAutomationSettings) -> SlidesSettings:
    """The illustrated slides' settings (docs/videos/ILLUSTRATED.md); a row from before
    migration 0114 reads the defaults for what it lacks. A stored NULL image model follows
    the drama's choice rather than the slides' default."""
    return SlidesSettings(
        **{
            field: value
            for field in SLIDES_FIELDS
            if (value := getattr(row, field, None)) is not None
            or (field == "slides_image_model" and hasattr(row, field))
        }
    )


def slides_image_choice(row: VideoAutomationSettings) -> tuple[str, str]:
    """The vendor and model that draw an illustrated slides video's pictures: the slides' own
    image model on the vendor that has it (the settings' image vendor first), or the drama's
    choice when the slides name none."""
    model_id = getattr(row, "slides_image_model", None)
    if not model_id:
        return row.image_provider, row.image_model
    for vendor in sorted(MEDIA_VENDORS, key=lambda vendor: vendor != row.image_provider):
        if find_model(vendor, "image", model_id) is not None:
            return vendor, model_id
    return row.image_provider, model_id


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
        stage_instructions=cast(Any, row.stage_instructions or {}),
        voice=cast(Any, row.voice),
        target_minutes_min=row.target_minutes_min,
        target_minutes_max=row.target_minutes_max,
        caption_locales=cast(Any, current_caption_locales(row.caption_locales)),
        max_drafts_per_month=row.max_drafts_per_month,
        monthly_token_budget_millions=row.monthly_token_budget_millions,
        max_verify_rounds=row.max_verify_rounds,
        max_retake_rounds=row.max_retake_rounds,
        auto_approve_audio=row.auto_approve_audio,
        drama=drama_values(row),
        slides=slides_values(row),
        channel_stance=row.channel_stance or "",
        auto_pick_outline=row.auto_pick_outline,
        auto_approve_final=row.auto_approve_final,
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
    # The drama's own models and narrator voice (docs/videos/DRAMA-FLOW.md §一), when it does
    # not follow the tutorial's.
    if drama.drama_stage_models is not None:
        options = model_options()
        for stage, choice in drama.drama_stage_models.items():
            if choice.model not in {option.value for option in options[choice.provider]}:
                problems.append(
                    f"漫劇的 {stage}：{choice.provider} 沒有 {choice.model} 這個可用的模型"
                )
    narrator = drama.drama_voice
    if narrator is not None:
        problem = _voice_problem(narrator.provider, narrator.name, runtime)
        if problem:
            problems.append(f"漫劇旁白：{problem}")
        if (
            narrator.provider == "gemini"
            and narrator.model is not None
            and narrator.model not in GEMINI_TTS_MODELS
        ):
            problems.append(f"漫劇旁白：Gemini 沒有 {narrator.model} 這個語音模型")
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
    problems.extend(slides_problems(payload.slides, payload.drama, runtime))
    return problems


def slides_problems(slides: SlidesSettings, drama: DramaSettings, runtime: Settings) -> list[str]:
    """What the illustrated slides' settings name that the server cannot serve: a retired image
    model, or, with the pictures on, an image vendor the site has no key for."""
    problems: list[str] = []
    model_id = slides.slides_image_model or drama.image_model
    found = [
        (vendor, model)
        for vendor in sorted(MEDIA_VENDORS, key=lambda vendor: vendor != drama.image_provider)
        if (model := find_model(vendor, "image", model_id)) is not None
    ]
    if not found:
        problems.append(f"投影片插畫：沒有 {model_id} 這個圖片模型")
        return problems
    if all(model.status == "retired" for _vendor, model in found):
        problems.append(f"投影片插畫：{model_id} 已經退役，請換一個模型")
    vendor = found[0][0]
    if slides.slides_media_enabled and vendor not in set(configured_providers(runtime)):
        problems.append(f"投影片插畫：網站還沒有 {vendor} 的金鑰，不能開啟插畫")
    return problems


async def remember_prompt(session: AsyncSession, request: StageRunIn) -> None:
    """Keep the instructions a stage was just sent, so the settings tab can show them as sent.

    The caller commits: the record should survive a run that then fails upstream, since that
    is exactly when the owner wants to read what the model was told.
    """
    await session.merge(
        VideoStagePrompt(
            stage=request.stage,
            format=request.format,
            variant=request.variant or "",
            slug=request.slug,
            instructions=request.instructions,
            sent_at=datetime.now(UTC),
        )
    )


async def stage_prompts(session: AsyncSession) -> list[StagePromptView]:
    """Every stage's last prompt, in the stages' order, a slides video's before a drama's."""
    order = {stage: index for index, stage in enumerate(get_args(Stage))}
    rows = sorted(
        (await session.scalars(select(VideoStagePrompt))).all(),
        key=lambda row: (order.get(row.stage, len(order)), row.format != "slides", row.variant),
    )
    return [
        StagePromptView(
            stage=cast(Any, row.stage),
            format=cast(Any, row.format),
            variant=row.variant or "",
            slug=row.slug,
            instructions=row.instructions,
            sent_at=row.sent_at,
        )
        for row in rows
    ]


def _flat(values: dict[str, Any]) -> dict[str, Any]:
    """The drama and slides objects spread onto columns, for saving and the audit diff."""
    flat = {key: value for key, value in values.items() if key not in {"drama", "slides"}}
    flat.update(values.get("drama") or {})
    flat.update(values.get("slides") or {})
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


async def auto_approves_audio(
    session: AsyncSession, payload: dict[str, Any], format: str = "slides"
) -> bool:
    """Whether a narration review stands on Jev's check; a drama has its own switch."""
    row = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    # With no row yet the defaults apply, and the default is on (the owner's 2026-09-25 choice).
    if row is None:
        enabled = True
    elif format == "drama":
        enabled = row.drama_auto_approve_audio
    else:
        enabled = row.auto_approve_audio
    return enabled and audio_check_passed(payload)


def storyboard_check_passed(payload: dict[str, Any], min_score: int) -> bool:
    """Whether every expected picture is complete and clears the owner's judge threshold.

    New submissions attest the selected files' hashes after checking local bytes and list
    the document's expected shots separately. Older reviews without that coverage evidence
    remain available for owner review, but cannot establish automatic approval.

    A shot sent with ``accepted: true`` is a picture the worker kept with the judge's remarks
    once its prompt fixes were spent (tools/video/media/keyframes.mjs ``--accept-best``): the
    owner decides on it at the final gate, which that video's worker sends for manual review,
    so its score and problems do not hold the storyboard back here. The board's ``overall`` is
    then the lowest score among the other shots, and null when every shot was accepted.
    """
    judge = payload.get("judge")
    shots = payload.get("shots")
    if not isinstance(judge, dict) or not isinstance(shots, list) or not shots:
        return False
    overall = judge.get("overall")
    problems = judge.get("problems")
    if overall is not None and (not isinstance(overall, int | float) or isinstance(overall, bool)):
        return False
    if problems not in (None, []):
        return False
    expected = payload.get("expected_shots")
    if not isinstance(expected, list) or not expected or len(expected) != len(shots):
        return False
    wanted: dict[str, bool] = {}
    for entry in expected:
        if not isinstance(entry, dict):
            return False
        shot_id = entry.get("id")
        end_required = entry.get("end_frame_required")
        if (not isinstance(shot_id, str) or not shot_id or shot_id in wanted
                or not isinstance(end_required, bool)):
            return False
        wanted[shot_id] = end_required

    def has_hash(value: Any) -> bool:
        return isinstance(value, str) and len(value) == 64 and all(
            letter in "0123456789abcdef" for letter in value
        )

    seen: set[str] = set()
    judged = 0
    for shot in shots:
        if not isinstance(shot, dict):
            return False
        shot_id = shot.get("id")
        if not isinstance(shot_id, str) or shot_id not in wanted or shot_id in seen:
            return False
        seen.add(shot_id)
        if (shot.get("complete") is not True or shot.get("incomplete")
                or shot.get("needs_review") or not has_hash(shot.get("file_sha256"))):
            return False
        if wanted[shot_id] and not has_hash(shot.get("end_frame_sha256")):
            return False
        if shot.get("accepted") is True:
            continue
        judged += 1
        verdict = shot.get("judge")
        if not isinstance(verdict, dict):
            return False
        score = verdict.get("overall")
        if (not isinstance(score, int | float) or isinstance(score, bool)
                or not min_score <= score <= 10 or verdict.get("problems") not in (None, [])
                or verdict.get("passed") is False):
            return False
    if overall is None:
        return judged == 0
    return min_score <= overall <= 10


async def hands_off_series(
    session: AsyncSession, series_slug: str | None
) -> VideoDramaSeries | None:
    """The hands-off series a video belongs to (docs/videos/BINGE.md), or None.

    A hands-off series has its sheets, storyboards and screenplays decided by the checks
    whatever the global switches say; the owner set that on the series itself.
    """
    if not series_slug:
        return None
    row = await session.scalar(select(VideoDramaSeries).where(VideoDramaSeries.slug == series_slug))
    return row if (
        row is not None and row.hands_off
        and not getattr(row, "planning_only", False) and not is_long_anime(row)
    ) else None


async def auto_approves_storyboard(
    session: AsyncSession,
    payload: dict[str, Any],
    series_slug: str | None = None,
    video_format: str = "drama",
) -> bool:
    row = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    # A drama's is off by default: the owner looks at the first drama's keyframes before any
    # clip is paid for; a hands-off series decided otherwise when it was created. Illustrated
    # slides (docs/videos/ILLUSTRATED.md) read their own switch, on by default: their pictures
    # are cheap stills and the owner chose to look at the finished cut only.
    if row is None:
        return video_format == "slides" and storyboard_check_passed(payload, 7)
    if video_format == "slides":
        if not slides_values(row).slides_auto_approve_storyboard:
            return False
        return storyboard_check_passed(payload, row.judge_min_score)
    if row.auto_approve_storyboard and series_slug:
        series = await session.scalar(
            select(VideoDramaSeries).where(VideoDramaSeries.slug == series_slug)
        )
        if series is not None and is_long_anime(series):
            return False
    if not row.auto_approve_storyboard and await hands_off_series(session, series_slug) is None:
        return False
    return storyboard_check_passed(payload, row.judge_min_score)


def _suggested_sheet(payload: dict[str, Any]) -> tuple[str, float] | None:
    """The key and score of the sheet the judge suggested, when it listed no problems."""
    suggested = payload.get("suggested")
    options = payload.get("options")
    if not isinstance(suggested, str) or not suggested or not isinstance(options, list):
        return None
    for option in options:
        if not isinstance(option, dict) or option.get("key") != suggested:
            continue
        judge = option.get("judge")
        if not isinstance(judge, dict):
            return None
        overall = judge.get("overall")
        if not isinstance(overall, int | float) or isinstance(overall, bool):
            return None
        if judge.get("problems") not in (None, []):
            return None
        return suggested, float(overall)
    return None


def look_pick_passed(payload: dict[str, Any], min_score: int) -> bool:
    """Whether a look review's suggested sheet clears the threshold with no problems listed.

    The payload is what tools/video/review/sync.mjs sends: {"options": [{"key", "judge":
    {"overall", "problems"}}], "suggested": key}. The judge suggests nothing when no sheet
    passed, and then the owner decides as before.
    """
    found = _suggested_sheet(payload)
    return found is not None and found[1] >= min_score


def look_pick_note(payload: dict[str, Any]) -> str:
    found = _suggested_sheet(payload)
    key, score = found if found is not None else ("?", 0.0)
    return AUTO_PICKED_LOOK_NOTE.format(key=key, score=score)


async def auto_picks_look(
    session: AsyncSession, payload: dict[str, Any], series_slug: str | None = None
) -> bool:
    """Whether a character's sheet is picked for the owner (docs/videos/HANDS-OFF.md)."""
    row = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    # Off by default, like the storyboard: the owner looks at a first drama's sheets, unless
    # the series is hands-off.
    if row is None:
        return False
    if row.auto_pick_look and series_slug:
        series = await session.scalar(
            select(VideoDramaSeries).where(VideoDramaSeries.slug == series_slug)
        )
        if series is not None and is_long_anime(series):
            return False
    if not row.auto_pick_look and await hands_off_series(session, series_slug) is None:
        return False
    return look_pick_passed(payload, row.judge_min_score)


async def auto_approves_script(
    session: AsyncSession, series_slug: str | None, payload: dict[str, Any]
) -> bool:
    """Whether an episode's screenplay stands on the checker's coverage (docs/videos/BINGE.md):
    only on a hands-off series, and only when the rule passes for its genre."""
    series = await hands_off_series(session, series_slug)
    if series is None:
        return False
    return script_check_passed(payload, retention_required=retention_required_for(series.genre))


async def auto_picks_outline(session: AsyncSession, payload: dict[str, Any]) -> bool:
    """Whether an outline review stands on Jev's pick (docs/videos/HANDS-OFF.md).

    The switch must be on and the stance written, so no video gets its viewpoint decided by
    the AI before the owner wrote one down; then the pick must clear the thresholds.
    """
    row = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    if row is None or not row.auto_pick_outline or not (row.channel_stance or "").strip():
        return False
    return outline_pick_passed(payload)


async def auto_approves_final(
    session: AsyncSession,
    gate: str,
    payload: dict[str, Any],
    sha: str,
    format: str = "slides",
    *,
    compilation: bool = False,
) -> bool:
    """Whether a final cut or an upload confirmation stands on the automatic checks.

    A drama has its own switch (docs/videos/DRAMA-FLOW.md §一); the checks are the same. A
    compilation (docs/videos/BINGE.md) is held to its own, shorter list of checks.
    """
    row = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    # With no row yet the defaults apply, and the default is on (docs/videos/HANDS-OFF.md).
    if row is None:
        enabled = True
    elif format == "drama":
        enabled = row.drama_auto_approve_final
    else:
        enabled = row.auto_approve_final
    if not enabled:
        return False
    if gate == "final":
        return final_qa_passed(payload, sha, COMPILATION_QA_ITEMS if compilation else QA_ITEMS)
    if gate == "publish":
        return publish_package_passed(payload, sha)
    return False
