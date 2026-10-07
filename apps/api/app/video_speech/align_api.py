"""``POST /video/speech/align``: when each character of a phrase is spoken (``align.py``).

The video tool calls it with its token through apps/web/app/api/video/speech/align, as it calls
the speech route. Two shapes of request, one answer:

* ``speech`` (the body of ``POST /video/speech``, an Azure voice): the phrase is synthesized
  here instead, through the Speech SDK, and the answer carries the WAV *and* the word
  boundaries the service sent during that one synthesis — the same budget, the same error
  codes and the same billable count as the speech route, so nothing is paid for twice.
  The WAV comes back inside the JSON (base64), which suits a phrase of a Short; a six-minute
  scene belongs to the speech route, whose bytes stream. A Gemini voice has no boundaries:
  ``video_align_voice_unsupported`` says to synthesize it with the speech route and send the
  audio instead.
* ``audio`` + ``text`` (any voice): the server's CPU aligner times the clip. None ships yet
  (``align.load_aligner``), so this answers 503 ``video_align_unavailable`` and the tool keeps
  its estimate; the answer is a provider answer, never a 500.

Like the transcription and the judge this is an operator surface: refusals are ``AlignRefused``
from ``align.py`` turned into the route's error here, and the operator reads the code.
"""

from __future__ import annotations

import base64
import binascii

from fastapi import APIRouter

from app.admin.service import load_runtime_settings
from app.config import Settings
from app.infra import enforce_named_rate_limit, get_redis
from app.problems import AppError
from app.providers.usage_meter import (
    release_azure_speech_characters,
    reserve_azure_speech_characters,
)
from app.video_speech import align
from app.video_speech.admin_api import MAX_REQUEST_CHARACTERS, Session, VideoTool
from app.video_speech.align import ALIGNER_SOURCE, AZURE_SOURCE, AlignRefused
from app.video_speech.azure import SpeechAnswerLost, SpeechUpstreamError
from app.video_speech.gemini import gemini_voice
from app.video_speech.schemas import AlignIn, AlignOut, CharTimingOut, SpeechRequest
from app.video_speech.ssml import Part, Segment, billable_characters, build_ssml

ALIGN_REQUESTS_PER_HOUR = 1200
# The same cap as a transcription: one phrase of a Short, 48 kHz mono, a few seconds.
MAX_CLIP_BYTES = 2_000_000

align_router = APIRouter(prefix="/video", tags=["video narration"])


def _segments(payload: SpeechRequest) -> tuple[Segment, ...]:
    return tuple(
        Segment(
            parts=tuple(Part(text=part.text, alias=part.alias) for part in segment.parts),
            break_after_ms=segment.break_after_ms,
        )
        for segment in payload.segments
    )


def _refusal_for(error: SpeechUpstreamError) -> AlignRefused:
    """The speech route's answers for Azure's failures, so the tool handles both alike."""
    if error.status == 429:
        return AlignRefused(
            429,
            "video_speech_upstream_busy",
            "Azure 語音暫時忙碌，請稍後重試",
            headers={"Retry-After": error.retry_after or "5"},
        )
    if error.status in {401, 403}:
        return AlignRefused(
            502, "video_speech_upstream_rejected_key", "Azure 拒絕了後台設定的金鑰或區域"
        )
    if error.status == 400:
        return AlignRefused(422, "video_speech_rejected", "Azure 無法合成這段內容")
    return AlignRefused(502, "video_speech_upstream_failed", "Azure 語音暫時無法使用")


async def _synthesize_azure(
    speech: SpeechRequest, text: str | None, settings: Settings
) -> AlignOut:
    """The speech route's Azure path with the boundaries kept: budget, allowlist, codes alike."""
    if gemini_voice(speech.voice) is not None:
        raise AlignRefused(
            422,
            "video_align_voice_unsupported",
            "Gemini 聲音沒有字時：用 /video/speech 合成後，把音檔送來對齊",
        )
    characters_of_text = sum(
        len(part.text) for segment in speech.segments for part in segment.parts
    )
    if characters_of_text > MAX_REQUEST_CHARACTERS:
        raise AlignRefused(
            413,
            "video_speech_request_too_long",
            f"一次最多 {MAX_REQUEST_CHARACTERS} 字；這次 {characters_of_text} 字，請分段送出",
        )
    segments = _segments(speech)
    written = "".join(part.text for segment in segments for part in segment.parts)
    if text is not None and align.units_of_text(text) != align.units_of_text(written):
        raise AlignRefused(
            422, "video_align_text_mismatch", "text 跟 speech 的句子不一樣；兩者要說同一句"
        )
    if not (
        settings.azure_speech_configured
        and settings.azure_speech_key
        and settings.azure_speech_region
    ):
        raise AlignRefused(
            503,
            "video_speech_not_configured",
            "後台的 Azure 語音還沒設定或已停用："
            "請在「AI 設定 → API 金鑰 → Azure 語音」填金鑰與區域",
        )
    if speech.voice not in settings.azure_speech_voice_list:
        raise AlignRefused(
            422, "video_speech_voice_not_allowed", f"聲音 {speech.voice} 不在後台允許的清單裡"
        )
    document, billed = build_ssml(speech.voice, segments, speech.rate)
    characters = billable_characters(billed)
    limit = settings.azure_speech_monthly_character_limit
    redis = get_redis()
    if not await reserve_azure_speech_characters(redis, characters, limit):
        raise AlignRefused(
            429,
            "video_speech_budget_exhausted",
            f"本月的語音字數預算（{limit} 計費字元）不夠這次的 {characters} 字元；"
            "可在後台調高上限，或等下個月",
        )
    try:
        audio, boundaries = await align.synthesize_with_boundaries(
            settings.azure_speech_region,
            settings.azure_speech_key,
            document,
            settings.azure_speech_timeout_seconds,
        )
    except SpeechAnswerLost as error:
        # As the speech route: Azure may have synthesized it, so the characters stay counted.
        raise AlignRefused(
            504,
            "video_speech_upstream_lost",
            "Azure 可能已經處理這次請求並計費，但回覆沒有回來；請勿自動重送",
        ) from error
    except SpeechUpstreamError as error:
        # As the speech route: Azure bills only what it processed, so the reservation goes back.
        await release_azure_speech_characters(redis, characters)
        raise _refusal_for(error) from error
    parts = [part for segment in segments for part in segment.parts]
    chars = align.chars_from_boundaries(parts, boundaries, align.wav_milliseconds(audio))
    return AlignOut(
        source=AZURE_SOURCE,
        chars=[CharTimingOut(text=c.text, start_ms=c.start_ms, end_ms=c.end_ms) for c in chars],
        model=speech.voice,
        audio=base64.b64encode(audio).decode("ascii"),
        billable_characters=characters,
    )


async def _align_audio(audio: str, text: str, language: str) -> AlignOut:
    try:
        wav = base64.b64decode(audio, validate=True)
    except (binascii.Error, ValueError) as error:
        raise AlignRefused(422, "video_align_bad_audio", "音檔不是有效的 base64") from error
    if len(wav) > MAX_CLIP_BYTES or not wav.startswith(b"RIFF"):
        raise AlignRefused(422, "video_align_bad_audio", "只收 2 MB 以內的 WAV 音檔")
    aligner = align.load_aligner()
    if aligner is None:
        raise AlignRefused(
            503,
            "video_align_unavailable",
            "伺服器沒有安裝對齊器，這段音檔的字時只能估算；Azure 聲音請改送 speech，"
            "合成時一併取得字時",
        )
    chars = await align.run_aligner(aligner, wav, text, language)
    return AlignOut(
        source=ALIGNER_SOURCE,
        chars=[CharTimingOut(text=c.text, start_ms=c.start_ms, end_ms=c.end_ms) for c in chars],
        model=aligner.name,
    )


@align_router.post("/speech/align", response_model=AlignOut)
async def align_speech(payload: AlignIn, tool: VideoTool, session: Session) -> AlignOut:
    """When each written unit of one phrase is spoken, from the voice's own boundaries or the
    server's aligner; one paid synthesis at most, never a second one."""
    await enforce_named_rate_limit(
        "video_align", str(tool.id), limit=ALIGN_REQUESTS_PER_HOUR, window_seconds=3600
    )
    try:
        if payload.speech is not None:
            settings = await load_runtime_settings(session)
            return await _synthesize_azure(payload.speech, payload.text, settings)
        assert payload.audio is not None and payload.text is not None  # the schema's validator
        return await _align_audio(payload.audio, payload.text, payload.language)
    except AlignRefused as error:
        raise AppError(error.status, error.code, error.detail, headers=error.headers) from error
