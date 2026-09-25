"""HTTP surface of video narration. Operator-only: readers never reach it.

Two routers. ``admin_router`` sits under the provider settings path, so the admin capability
map already gives it settings.read / settings.manage; the owner makes and revokes video tool
tokens there, and allows or denies pairings. ``speech_router`` is what the local pipeline calls
with such a token, through the dedicated web routes apps/web/app/api/video/speech and
apps/web/app/api/video/pairings (nginx exposes only the web app). Its two pairing endpoints
take no token: they are how the tool gets one, and an admin's click is what authorizes it.
"""

from __future__ import annotations

import base64
import binascii
from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID, uuid4

import httpx
from fastapi import APIRouter, Depends, Header, Request, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.ai.jev import JevError
from app.auth.service import AdminUser
from app.config import Settings
from app.db import get_session
from app.infra import client_ip, enforce_named_rate_limit, get_redis
from app.models import AdminAuditLog, VideoToolToken
from app.problems import AppError
from app.providers.usage_meter import (
    GEMINI_SPEECH_PROVIDER,
    azure_speech_usage_snapshot,
    release_azure_speech_characters,
    reserve_azure_speech_characters,
)
from app.video_speech.azure import OUTPUT_FORMAT, AzureSpeech, SpeechUpstreamError
from app.video_speech.checking import CheckUnavailable, judge, transcribe
from app.video_speech.gemini import (
    DEFAULT_GEMINI_TTS_MODEL,
    GEMINI_TTS_MODELS,
    PREBUILT_VOICES,
    VOICE_PREFIX,
    GeminiSpeech,
    gemini_voice,
    speech_text,
)
from app.video_speech.pairing import (
    PAIRING_TTL_SECONDS,
    POLL_INTERVAL_SECONDS,
    Pairing,
    collect,
    decide,
    device_hash,
    display_code,
    find_pairing,
    normalize_user_code,
    start_pairing,
)
from app.video_speech.schemas import (
    JudgeIn,
    JudgeOut,
    JudgeResult,
    PairingPollIn,
    PairingPollOut,
    PairingStarted,
    PairingStartIn,
    PairingView,
    SpeechRequest,
    SpeechStatus,
    TranscribeIn,
    TranscribeOut,
    VideoToolTokenCreate,
    VideoToolTokenCreated,
    VideoToolTokenView,
)
from app.video_speech.ssml import Part, Segment, billable_characters, build_ssml
from app.video_speech.tokens import PREFIX_SHOWN, find_active_token, new_token, token_hash, touch

# Text per request, before markup. At about 4.5 characters a second this is under six minutes
# of audio, about 32 MB of 48 kHz PCM; a longer scene is split by the pipeline.
MAX_REQUEST_CHARACTERS = 1500
MAX_ACTIVE_TOKENS = 10
SPEECH_REQUESTS_PER_MINUTE = 120
PAIRING_STARTS_PER_HOUR = 10

admin_router = APIRouter(
    prefix="/admin/provider-settings/azure_speech/video-tool-tokens",
    tags=["admin video tool tokens"],
)
speech_router = APIRouter(prefix="/video", tags=["video narration"])
Session = Annotated[AsyncSession, Depends(get_session)]


def _view(row: VideoToolToken) -> VideoToolTokenView:
    return VideoToolTokenView(
        id=row.id,
        name=row.name,
        token_prefix=row.token_prefix,
        created_at=row.created_at,
        last_used_at=row.last_used_at,
        revoked_at=row.revoked_at,
    )


@admin_router.get("", response_model=list[VideoToolTokenView])
async def list_video_tool_tokens(user: AdminUser, session: Session) -> list[VideoToolTokenView]:
    _ = user
    rows = await session.scalars(
        select(VideoToolToken).order_by(VideoToolToken.created_at.desc()).limit(50)
    )
    return [_view(row) for row in rows]


async def _refuse_over_token_limit(session: AsyncSession) -> None:
    active = await session.scalar(
        select(func.count()).select_from(VideoToolToken).where(VideoToolToken.revoked_at.is_(None))
    )
    if (active or 0) >= MAX_ACTIVE_TOKENS:
        raise AppError(
            409,
            "video_tool_token_limit",
            f"最多 {MAX_ACTIVE_TOKENS} 組有效的影片工具權杖；請先撤銷不用的",
        )


def _mint_token(
    session: AsyncSession, *, name: str, actor_id: UUID, via: str
) -> tuple[VideoToolToken, str]:
    """A new token row and its plaintext, added to the session with its audit entry."""
    token = new_token()
    now = datetime.now(UTC)
    row = VideoToolToken(
        id=uuid4(),
        name=name,
        token_hash=token_hash(token),
        token_prefix=token[:PREFIX_SHOWN],
        created_by_user_id=actor_id,
        created_at=now,
        updated_at=now,
    )
    session.add(row)
    session.add(
        AdminAuditLog(
            actor_user_id=actor_id,
            action="video_tool_token_created",
            target=f"video_tool_token:{row.id}",
            metadata_json={"name": row.name, "prefix": row.token_prefix, "via": via},
        )
    )
    return row, token


@admin_router.post("", response_model=VideoToolTokenCreated, status_code=201)
async def create_video_tool_token(
    payload: VideoToolTokenCreate, user: AdminUser, session: Session
) -> VideoToolTokenCreated:
    await enforce_named_rate_limit(
        "video_tool_token_create", str(user.id), limit=10, window_seconds=3600
    )
    await _refuse_over_token_limit(session)
    row, token = _mint_token(
        session, name=payload.name.strip() or "影片工具", actor_id=user.id, via="admin"
    )
    await session.commit()
    return VideoToolTokenCreated(**_view(row).model_dump(), token=token)


@admin_router.delete("/{token_id}", response_model=VideoToolTokenView)
async def revoke_video_tool_token(
    token_id: UUID, user: AdminUser, session: Session
) -> VideoToolTokenView:
    row = await session.get(VideoToolToken, token_id)
    if row is None:
        raise AppError(404, "video_tool_token_not_found", "找不到這組影片工具權杖")
    if row.revoked_at is None:
        row.revoked_at = datetime.now(UTC)
        session.add(
            AdminAuditLog(
                actor_user_id=user.id,
                action="video_tool_token_revoked",
                target=f"video_tool_token:{row.id}",
                metadata_json={"name": row.name, "prefix": row.token_prefix},
            )
        )
        await session.commit()
    return _view(row)


def _pairing_view(pairing: Pairing) -> PairingView:
    return PairingView(
        user_code=display_code(pairing.user_code),
        client_name=pairing.client_name,
        client_ip=pairing.client_ip,
        created_at=pairing.created_at,
        expires_at=pairing.expires_at,
        status=pairing.status,
    )


async def _pending_pairing(user_code: str) -> Pairing:
    code = normalize_user_code(user_code)
    pairing = await find_pairing(get_redis(), code) if code else None
    if pairing is None:
        raise AppError(
            404,
            "video_pairing_not_found",
            "找不到這組驗證碼，或已經超過 10 分鐘；請在本機重新執行 login",
        )
    return pairing


@admin_router.get("/pairings/{user_code}", response_model=PairingView)
async def get_video_tool_pairing(user_code: str, user: AdminUser) -> PairingView:
    _ = user
    return _pairing_view(await _pending_pairing(user_code))


async def _decide_pairing(
    user_code: str, user: AdminUser, session: AsyncSession, *, approve: bool
) -> PairingView:
    pairing = await _pending_pairing(user_code)
    if pairing.status != "pending":
        raise AppError(409, "video_pairing_already_decided", "這組驗證碼已經處理過了")
    if approve:
        await _refuse_over_token_limit(session)
    try:
        decided = await decide(get_redis(), pairing, approve=approve, actor_id=user.id)
    except LookupError as error:
        raise AppError(
            404, "video_pairing_not_found", "這組驗證碼剛剛過期；請在本機重新執行 login"
        ) from error
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_tool_pairing_approved" if approve else "video_tool_pairing_denied",
            target=f"video_tool_pairing:{pairing.user_code}",
            metadata_json={"client_name": pairing.client_name, "client_ip": pairing.client_ip},
        )
    )
    await session.commit()
    return _pairing_view(decided)


@admin_router.post("/pairings/{user_code}/approve", response_model=PairingView)
async def approve_video_tool_pairing(
    user_code: str, user: AdminUser, session: Session
) -> PairingView:
    return await _decide_pairing(user_code, user, session, approve=True)


@admin_router.post("/pairings/{user_code}/deny", response_model=PairingView)
async def deny_video_tool_pairing(user_code: str, user: AdminUser, session: Session) -> PairingView:
    return await _decide_pairing(user_code, user, session, approve=False)


async def video_tool(
    session: Session,
    authorization: Annotated[str | None, Header()] = None,
) -> VideoToolToken:
    presented = ""
    if authorization and authorization[:7].lower() == "bearer ":
        presented = authorization[7:].strip()
    row = await find_active_token(session, presented)
    if row is None:
        raise AppError(
            401,
            "video_tool_token_invalid",
            "影片工具權杖無效或已撤銷；請到後台的 Azure 語音卡建立新的權杖",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if touch(row):
        await session.commit()
    await enforce_named_rate_limit(
        "video_speech", str(row.id), limit=SPEECH_REQUESTS_PER_MINUTE, window_seconds=60
    )
    return row


VideoTool = Annotated[VideoToolToken, Depends(video_tool)]


@speech_router.get("/speech/status", response_model=SpeechStatus)
async def speech_status(tool: VideoTool, session: Session) -> SpeechStatus:
    _ = tool
    settings = await load_runtime_settings(session)
    limit = settings.azure_speech_monthly_character_limit
    redis = get_redis()
    usage = await azure_speech_usage_snapshot(redis, limit)
    gemini_limit = settings.video_speech_gemini_monthly_character_limit
    gemini_usage = await azure_speech_usage_snapshot(
        redis, gemini_limit, provider=GEMINI_SPEECH_PROVIDER
    )
    gemini_ready = bool(settings.hotspot_guide_gemini_api_key)
    return SpeechStatus(
        configured=settings.azure_speech_configured,
        region=settings.azure_speech_region,
        voices=list(settings.azure_speech_voice_list),
        output_format=OUTPUT_FORMAT,
        max_request_characters=MAX_REQUEST_CHARACTERS,
        monthly_limit=limit,
        used=usage.used,
        remaining=usage.remaining,
        gemini_configured=gemini_ready,
        gemini_models=list(GEMINI_TTS_MODELS) if gemini_ready else [],
        gemini_voices=[f"{VOICE_PREFIX}{name}" for name in PREBUILT_VOICES] if gemini_ready else [],
        gemini_monthly_limit=gemini_limit,
        gemini_used=gemini_usage.used,
    )


async def _synthesize_with_gemini(
    payload: SpeechRequest, voice: str, segments: tuple[Segment, ...], settings: Settings
) -> Response:
    """The same contract as Azure's path: WAV back, characters counted against a month."""
    key = settings.hotspot_guide_gemini_api_key
    if not key:
        raise AppError(
            503,
            "video_speech_not_configured",
            "網站的 Gemini 金鑰還沒設定：請在「API 與供應商設定 → AI 服務」填 Gemini 金鑰",
        )
    if not voice:
        raise AppError(422, "video_speech_voice_not_allowed", "Gemini 聲音名稱的格式不對")
    model = payload.model or DEFAULT_GEMINI_TTS_MODEL
    if model not in GEMINI_TTS_MODELS:
        raise AppError(
            422,
            "video_speech_model_not_allowed",
            f"Gemini 語音模型只能是 {'、'.join(GEMINI_TTS_MODELS)}",
        )
    text = speech_text(segments)
    characters = len(text)
    limit = settings.video_speech_gemini_monthly_character_limit
    redis = get_redis()
    if not await reserve_azure_speech_characters(
        redis, characters, limit, provider=GEMINI_SPEECH_PROVIDER
    ):
        raise AppError(
            429,
            "video_speech_budget_exhausted",
            f"本月的 Gemini 語音字數預算（{limit} 字）不夠這次的 {characters} 字；"
            "可調高 VIDEO_SPEECH_GEMINI_MONTHLY_CHARACTER_LIMIT，或等下個月",
        )
    speech = GeminiSpeech(
        base_url=settings.hotspot_guide_gemini_base_url,
        key=key,
        timeout_seconds=settings.video_speech_gemini_timeout_seconds,
    )
    try:
        audio = await speech.synthesize(text, voice, payload.style, model)
    except SpeechUpstreamError as error:
        await release_azure_speech_characters(redis, characters, provider=GEMINI_SPEECH_PROVIDER)
        if error.status == 429:
            raise AppError(
                429,
                "video_speech_upstream_busy",
                "Gemini 語音暫時忙碌或達到用量上限，請稍後重試",
                headers={"Retry-After": error.retry_after or "10"},
            ) from error
        if error.status in {401, 403}:
            raise AppError(
                502,
                "video_speech_upstream_rejected_key",
                "Gemini 拒絕了網站的金鑰（金鑰的 API 或 IP 限制可能不包含語音）",
            ) from error
        if error.status in {400, 404}:
            raise AppError(
                422,
                "video_speech_rejected",
                "Gemini 無法用這個聲音或模型合成這段內容",
            ) from error
        raise AppError(502, "video_speech_upstream_failed", "Gemini 語音暫時無法使用") from error
    return Response(
        content=audio,
        media_type="audio/wav",
        headers={"X-Billable-Characters": str(characters), "Cache-Control": "no-store"},
    )


@speech_router.post("/speech")
async def synthesize_speech(payload: SpeechRequest, tool: VideoTool, session: Session) -> Response:
    _ = tool
    settings = await load_runtime_settings(session)
    characters_of_text = sum(
        len(part.text) for segment in payload.segments for part in segment.parts
    )
    if characters_of_text > MAX_REQUEST_CHARACTERS:
        raise AppError(
            413,
            "video_speech_request_too_long",
            f"一次最多 {MAX_REQUEST_CHARACTERS} 字；這次 {characters_of_text} 字，請分段送出",
        )
    segments = tuple(
        Segment(
            parts=tuple(Part(text=part.text, alias=part.alias) for part in segment.parts),
            break_after_ms=segment.break_after_ms,
        )
        for segment in payload.segments
    )
    voice = gemini_voice(payload.voice)
    if voice is not None:
        return await _synthesize_with_gemini(payload, voice, segments, settings)
    if not (
        settings.azure_speech_configured
        and settings.azure_speech_key
        and settings.azure_speech_region
    ):
        raise AppError(
            503,
            "video_speech_not_configured",
            "後台的 Azure 語音還沒設定或已停用："
            "請在「API 與供應商設定 → AI 服務 → Azure 語音」填金鑰與區域",
        )
    if payload.voice not in settings.azure_speech_voice_list:
        raise AppError(
            422,
            "video_speech_voice_not_allowed",
            f"聲音 {payload.voice} 不在後台允許的清單裡",
        )
    document, billed = build_ssml(payload.voice, segments, payload.rate)
    characters = billable_characters(billed)
    limit = settings.azure_speech_monthly_character_limit
    redis = get_redis()
    if not await reserve_azure_speech_characters(redis, characters, limit):
        raise AppError(
            429,
            "video_speech_budget_exhausted",
            f"本月的語音字數預算（{limit} 計費字元）不夠這次的 {characters} 字元；"
            "可在後台調高上限，或等下個月",
        )
    speech = AzureSpeech(
        region=settings.azure_speech_region,
        key=settings.azure_speech_key,
        timeout_seconds=settings.azure_speech_timeout_seconds,
    )
    try:
        audio = await speech.synthesize(document)
    except SpeechUpstreamError as error:
        # Azure bills only requests it processed, so a refused one goes back to the budget.
        await release_azure_speech_characters(redis, characters)
        if error.status == 429:
            raise AppError(
                429,
                "video_speech_upstream_busy",
                "Azure 語音暫時忙碌，請稍後重試",
                headers={"Retry-After": error.retry_after or "5"},
            ) from error
        if error.status in {401, 403}:
            raise AppError(
                502,
                "video_speech_upstream_rejected_key",
                "Azure 拒絕了後台設定的金鑰或區域",
            ) from error
        if error.status == 400:
            raise AppError(422, "video_speech_rejected", "Azure 無法合成這段內容") from error
        raise AppError(502, "video_speech_upstream_failed", "Azure 語音暫時無法使用") from error
    return Response(
        content=audio,
        media_type="audio/wav",
        headers={"X-Billable-Characters": str(characters), "Cache-Control": "no-store"},
    )


TRANSCRIBE_REQUESTS_PER_HOUR = 1200
MAX_CLIP_BYTES = 2_000_000


@speech_router.post("/speech/transcribe", response_model=TranscribeOut)
async def transcribe_narration(
    payload: TranscribeIn, tool: VideoTool, session: Session
) -> TranscribeOut:
    """One narrated line back as text, so the tool can check it against the script."""
    await enforce_named_rate_limit(
        "video_transcribe", str(tool.id), limit=TRANSCRIBE_REQUESTS_PER_HOUR, window_seconds=3600
    )
    try:
        wav = base64.b64decode(payload.audio, validate=True)
    except (binascii.Error, ValueError) as error:
        raise AppError(422, "video_transcribe_bad_audio", "音檔不是有效的 base64") from error
    if len(wav) > MAX_CLIP_BYTES or not wav.startswith(b"RIFF"):
        raise AppError(422, "video_transcribe_bad_audio", "只收 2 MB 以內的 WAV 音檔")
    settings = await load_runtime_settings(session)
    try:
        text = await transcribe(settings, wav, terms=payload.terms)
    except CheckUnavailable as error:
        raise AppError(error.status, error.code, error.detail) from error
    except SpeechUpstreamError as error:
        if error.status == 429:
            raise AppError(
                429,
                "video_speech_upstream_busy",
                "Gemini 暫時忙碌，請稍後重試",
                headers={"Retry-After": error.retry_after or "10"},
            ) from error
        if error.status in {401, 403}:
            raise AppError(
                502, "video_speech_upstream_rejected_key", "Gemini 拒絕了網站的金鑰"
            ) from error
        if error.status in {500, 503, 504}:
            # Overloaded or failing on Google's side: worth another try after a real pause,
            # not the tool's one-to-sixteen-second backoff.
            raise AppError(
                503,
                "video_speech_upstream_busy",
                f"Gemini 暫時無法轉寫（{error}），請稍後重試",
                headers={"Retry-After": error.retry_after or "20"},
            ) from error
        raise AppError(
            502, "video_speech_upstream_failed", f"Gemini 暫時無法轉寫（{error}）"
        ) from error
    return TranscribeOut(text=text)


@speech_router.post("/speech/judge", response_model=JudgeOut)
async def judge_narration(payload: JudgeIn, tool: VideoTool, session: Session) -> JudgeOut:
    """Jev's judgement of whether each transcript says the script's words; one Jev call."""
    _ = tool
    settings = await load_runtime_settings(session)
    lines = [line.model_dump() for line in payload.lines]
    try:
        verdicts = await judge(settings, get_redis(), lines)
    except CheckUnavailable as error:
        raise AppError(error.status, error.code, error.detail) from error
    except (JevError, httpx.HTTPError) as error:
        raise AppError(502, "video_judge_upstream_failed", "Jev 暫時無法判斷") from error
    results = [JudgeResult(id=line["id"], noul=verdicts[line["id"]]) for line in lines]
    return JudgeOut(results=results)


# The owner lands on the Azure Speech card with the code filled in, and still compares it with
# the one on their own terminal before allowing it.
VERIFICATION_PATH = "/zh-TW/admin/settings?provider=azure_speech&video_pairing={code}"


@speech_router.post("/pairings", response_model=PairingStarted, status_code=201)
async def start_video_tool_pairing(payload: PairingStartIn, request: Request) -> PairingStarted:
    # Anyone can ask; only an admin's click turns a request into a token. The limit keeps a
    # stranger from filling the owner's card with codes.
    address = client_ip(request)
    await enforce_named_rate_limit(
        "video_pairing_start", address, limit=PAIRING_STARTS_PER_HOUR, window_seconds=3600
    )
    device_code, pairing = await start_pairing(
        get_redis(), client_name=payload.client_name.strip() or "影片工具", client_ip=address
    )
    return PairingStarted(
        device_code=device_code,
        user_code=display_code(pairing.user_code),
        verification_path=VERIFICATION_PATH.format(code=pairing.user_code),
        expires_in=PAIRING_TTL_SECONDS,
        interval=POLL_INTERVAL_SECONDS,
    )


@speech_router.post("/pairings/poll", response_model=PairingPollOut)
async def poll_video_tool_pairing(
    payload: PairingPollIn, session: Session, response: Response
) -> PairingPollOut:
    response.headers["Cache-Control"] = "no-store"
    await enforce_named_rate_limit(
        "video_pairing_poll", device_hash(payload.device_code), limit=30, window_seconds=60
    )
    status, grant = await collect(get_redis(), payload.device_code)
    if grant is None:
        return PairingPollOut(status=status, interval=POLL_INTERVAL_SECONDS)
    # The grant is gone from Redis now, so a failure below means pairing again, never a
    # second token for the same approval.
    await _refuse_over_token_limit(session)
    row, token = _mint_token(
        session, name=f"配對：{grant.client_name}", actor_id=grant.approved_by, via="pairing"
    )
    await session.commit()
    return PairingPollOut(
        status="approved", interval=POLL_INTERVAL_SECONDS, token=token, token_name=row.name
    )
