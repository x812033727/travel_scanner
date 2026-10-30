"""Paid-provider waits leave a real one-slot pool available to independent readers.

SQLite exercises SQLAlchemy's actual async queue pool, settings SELECT and token ORM
state locally. It is not a PostgreSQL load test or proof of an incident's cause.
"""

from __future__ import annotations

import asyncio
import base64
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import Request
from sqlalchemy import inspect, select, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool

from app import db
from app.admin import service as admin_service
from app.config import Settings
from app.models import ProviderConfig, User, VideoToolToken
from app.problems import AppError
from app.video_budget.models import VideoPilotBudget, VideoPilotBudgetOperation
from app.video_speech import admin_api, align_api
from app.video_speech import align as speech_align
from app.video_speech.azure import AzureSpeech, SpeechAnswerLost, SpeechUpstreamError
from app.video_speech.gemini import GeminiSpeech, wav_from_pcm
from app.video_speech.schemas import AlignIn, JudgeIn, SpeechRequest, TranscribeIn
from app.video_speech.tokens import new_token, token_hash

PILOT = "story-rolling-suitcase"
WAV = wav_from_pcm(b"\x01\x00" * 800, 24_000)


@pytest_asyncio.fixture
async def pooled(monkeypatch, tmp_path):
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{(tmp_path / 'speech.db').as_posix()}",
        poolclass=AsyncAdaptedQueuePool,
        pool_size=1,
        max_overflow=0,
        pool_timeout=0.25,
    )
    factory = async_sessionmaker(
        engine, class_=db.SessionFactory.class_, expire_on_commit=False
    )
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: db.Base.metadata.create_all(
                sync,
                tables=[
                    User.__table__,
                    VideoToolToken.__table__,
                    ProviderConfig.__table__,
                    VideoPilotBudget.__table__,
                    VideoPilotBudgetOperation.__table__,
                ],
            )
        )
    token = new_token()
    async with factory() as session:
        session.add(
            VideoToolToken(name="local test", token_hash=token_hash(token), token_prefix=token[:10])
        )
        session.add(VideoPilotBudget(slug=PILOT, limit_usd=Decimal("25")))
        await session.commit()
    settings = Settings(
        _env_file=None,
        azure_speech_key="local-test-key",
        azure_speech_region="eastasia",
        hotspot_guide_gemini_api_key="local-test-key",
        jev_api_key="local-test-key",
    )
    # Keep the actual settings-table SELECT; only the credential-free base values differ.
    monkeypatch.setattr(admin_service, "get_settings", lambda: settings)
    for module in (admin_api, align_api):
        monkeypatch.setattr(module, "enforce_named_rate_limit", AsyncMock())
        monkeypatch.setattr(module, "get_redis", lambda: object())
        monkeypatch.setattr(module, "reserve_azure_speech_characters", AsyncMock(return_value=True))
        monkeypatch.setattr(module, "release_azure_speech_characters", AsyncMock())
    try:
        yield engine, factory, token
    finally:
        await engine.dispose()


def speech_request(*, gemini=False, **extra):
    return SpeechRequest.model_validate(
        {
            "voice": "gemini:Sulafat" if gemini else "zh-TW-HsiaoChenNeural",
            "segments": [{"parts": [{"text": "行李箱"}]}],
            **extra,
        }
    )


async def dispatch(route, session, tool):
    if route in {"azure", "gemini"}:
        return await admin_api.synthesize_speech(
            speech_request(gemini=route == "gemini"), tool, session
        )
    if route == "transcribe":
        return await admin_api.transcribe_narration(
            TranscribeIn(audio=base64.b64encode(WAV).decode()), tool, session
        )
    if route == "align":
        return await align_api.align_speech(AlignIn(speech=speech_request()), tool, session)
    return await admin_api.judge_narration(
        JudgeIn(lines=[{"id": "abcd", "intended": "好", "spoken_form": "好", "heard": "好"}]),
        Request({"type": "http", "headers": []}),
        tool,
        session,
    )


@pytest.mark.parametrize("route", ["azure", "gemini", "transcribe", "judge", "align"])
@pytest.mark.parametrize("recent_token", [False, True])
async def test_independent_reader_progresses_while_provider_is_blocked(
    pooled, monkeypatch, route, recent_token
):
    engine, factory, token = pooled
    entered, release = asyncio.Event(), asyncio.Event()

    async def provider(*args, **kwargs):
        entered.set()
        await release.wait()
        return {
            "azure": WAV,
            "gemini": WAV,
            "transcribe": "行李箱",
            "judge": {"abcd": 0.9},
            "align": (WAV, []),
        }[route]

    monkeypatch.setattr(AzureSpeech, "synthesize", provider)
    monkeypatch.setattr(GeminiSpeech, "synthesize", provider)
    monkeypatch.setattr(admin_api, "transcribe", provider)
    monkeypatch.setattr(admin_api, "judge", provider)
    monkeypatch.setattr(speech_align, "synthesize_with_boundaries", provider)
    async with factory() as session:
        # SQLite drops timezone offsets on reload. Keep this real ORM identity alive
        # with an aware timestamp to exercise touch's recent-token/no-commit branch.
        row = await session.scalar(select(VideoToolToken))
        if recent_token:
            row.last_used_at = datetime.now(UTC)
            await session.commit()
        tool = await admin_api.video_tool(session, f"Bearer {token}")
        original_id, original_used = tool.id, tool.last_used_at
        task = asyncio.create_task(dispatch(route, session, tool))
        try:
            await asyncio.wait_for(entered.wait(), 5)
            assert not task.done() and not release.is_set()
            # This is a separate live DB borrower while the provider is still blocked.
            async with factory() as reader:
                assert await reader.scalar(text("SELECT 1")) == 1
                persisted = await reader.scalar(select(VideoToolToken))
                assert persisted.id == original_id and persisted.last_used_at is not None
                assert persisted.name == "local test"
            assert not session.in_transaction()
            assert not inspect(tool).expired_attributes
            assert (tool.id, tool.last_used_at) == (original_id, original_used)
            assert engine.sync_engine.pool.checkedout() == 0
        finally:
            release.set()
            await task


@pytest.mark.parametrize("outcome", ["settled", "released", "uncertain", "cancelled"])
async def test_pilot_hold_is_durable_before_dispatch_and_outcome_stays_honest(
    pooled, monkeypatch, outcome
):
    _, factory, token = pooled
    entered, release = asyncio.Event(), asyncio.Event()
    operation_id = uuid4()
    payload = speech_request(gemini=True, video_slug=PILOT, operation_id=operation_id)

    async def provider(*args, **kwargs):
        entered.set()
        await release.wait()
        if outcome == "released":
            raise SpeechUpstreamError(401, "test refusal")
        if outcome == "uncertain":
            raise SpeechAnswerLost()
        return WAV, {"promptTokenCount": 30, "candidatesTokenCount": 100}

    monkeypatch.setattr(GeminiSpeech, "synthesize_with_usage", provider)
    async with factory() as session:
        tool = await admin_api.video_tool(session, f"Bearer {token}")
        task = asyncio.create_task(admin_api.synthesize_speech(payload, tool, session))
        try:
            await asyncio.wait_for(entered.wait(), 5)
            async with factory() as reader:
                held = await reader.scalar(select(VideoPilotBudgetOperation))
                assert held.status == "reserved"
                assert held.operation_id == str(operation_id) and held.attempts == 1
                assert held.max_usd == admin_api.PILOT_GEMINI_TTS_MAX_USD
            assert not session.in_transaction()
        finally:
            if outcome == "cancelled":
                task.cancel()
            release.set()
            if outcome == "cancelled":
                with pytest.raises(asyncio.CancelledError):
                    await task
            elif outcome in {"released", "uncertain"}:
                with pytest.raises(AppError):
                    await task
            else:
                assert (await task).body == WAV
    async with factory() as reader:
        result = await reader.scalar(select(VideoPilotBudgetOperation))
        assert result.status == ("reserved" if outcome == "cancelled" else outcome)
        if outcome == "settled":
            assert result.actual_usd == Decimal("0.000915")
        else:
            assert result.actual_usd is None


async def test_database_commit_failure_cannot_dispatch_an_unreserved_request(pooled, monkeypatch):
    _, factory, token = pooled
    vendor = AsyncMock()
    monkeypatch.setattr(GeminiSpeech, "synthesize", vendor)
    async with factory() as session:
        tool = await admin_api.video_tool(session, f"Bearer {token}")
        monkeypatch.setattr(session, "commit", AsyncMock(side_effect=RuntimeError("commit failed")))
        with pytest.raises(RuntimeError, match="commit failed"):
            await admin_api.synthesize_speech(speech_request(gemini=True), tool, session)
        vendor.assert_not_awaited()


async def test_pilot_reused_operation_refuses_a_second_vendor_dispatch(pooled, monkeypatch):
    _, factory, token = pooled
    vendor = AsyncMock(side_effect=SpeechAnswerLost())
    monkeypatch.setattr(GeminiSpeech, "synthesize_with_usage", vendor)
    payload = speech_request(gemini=True, video_slug=PILOT, operation_id=uuid4())
    async with factory() as session:
        tool = await admin_api.video_tool(session, f"Bearer {token}")
        with pytest.raises(AppError, match=".*"):
            await admin_api.synthesize_speech(payload, tool, session)
        with pytest.raises(AppError) as refused:
            await admin_api.synthesize_speech(payload, tool, session)
        assert refused.value.code == "video_budget_operation_reused"
        assert vendor.await_count == 1
    async with factory() as reader:
        operation = await reader.scalar(select(VideoPilotBudgetOperation))
        assert operation.status == "uncertain" and operation.attempts == 1
