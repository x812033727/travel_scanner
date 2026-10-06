"""POST /video/media/locate: what it sends Gemini, how boxes are read, and how it is booked."""

from __future__ import annotations

import copy
import hashlib
import io
import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import fakeredis
import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from PIL import Image

from app.config import Settings
from app.db import get_session
from app.models import VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation.models import DEFAULT_DRAMA, DEFAULT_SLIDES, VideoAutomationSettings
from app.video_media import admin_api, meter
from app.video_media.jobs import MediaContext
from app.video_media.locate import (
    INSTRUCTIONS,
    MAX_BOXES,
    SCHEMA,
    LocateError,
    boxes,
    locate,
    picture,
    request_body,
)
from app.video_media.schemas import LocateIn, LocateOut, SubjectBox
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore
from app.video_speech import admin_api as speech_api

MP4 = b"\x00\x00\x00\x18ftypisom" + b"\x00" * 24


def _image(kind: str, width: int = 64, height: int = 36) -> bytes:
    out = io.BytesIO()
    Image.new("RGB", (width, height), (10, 20, 30)).save(out, format=kind)
    return out.getvalue()


def _stored(tmp_path: Path, data: bytes) -> tuple[MediaStore, str]:
    store = MediaStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    sha = hashlib.sha256(data).hexdigest()
    (tmp_path / "v").mkdir(exist_ok=True)
    (tmp_path / "v" / sha).write_bytes(data)
    return store, sha


def _payload(sha: str, **extra: Any) -> LocateIn:
    return LocateIn.model_validate({"slug": "v", "sha256": sha, **extra})


def test_the_request_sends_the_picture_with_its_size_and_asks_for_box_2d_json(
    tmp_path: Path,
) -> None:
    media = MediaSettings(video_media_dir=str(tmp_path))
    for kind, content_type in (
        ("PNG", "image/png"),
        ("JPEG", "image/jpeg"),
        ("WEBP", "image/webp"),
    ):
        store, sha = _stored(tmp_path, _image(kind, 64, 36))
        image = picture(store, media, _payload(sha))
        assert (image.content_type, image.width, image.height) == (content_type, 64, 36), kind
    store, sha = _stored(tmp_path, _image("PNG", 1920, 1080))
    image = picture(store, media, _payload(sha))
    body = request_body(_payload(sha, labels=["Jingwei", "the boat"]), image)
    assert body["system_instruction"]["parts"][0]["text"] == INSTRUCTIONS
    assert "\n" not in INSTRUCTIONS and "[ymin, xmin, ymax, xmax]" in INSTRUCTIONS
    assert "0-1000" in INSTRUCTIONS and "empty list is a correct answer" in INSTRUCTIONS
    parts = body["contents"][0]["parts"]
    assert (
        '["Jingwei", "the boat"]' in parts[0]["text"]
        and "label exactly as given" in parts[0]["text"]
    )
    assert parts[1]["inline_data"]["mime_type"] == "image/png"
    assert len(parts) == 2, "one picture, nothing else"
    assert body["generationConfig"] == {
        "temperature": 0,
        "responseMimeType": "application/json",
        "responseSchema": SCHEMA,
    }
    item = SCHEMA["properties"]["boxes"]["items"]
    assert item["required"] == ["label", "box_2d", "score"]
    assert item["properties"]["box_2d"] == {"type": "array", "items": {"type": "integer"}}
    free = request_body(_payload(sha), image)["contents"][0]["parts"][0]["text"]
    assert "every character in the picture, the main character first" in free


def test_a_clip_a_missing_file_and_an_unreadable_or_oversized_picture_are_refused(
    tmp_path: Path,
) -> None:
    media = MediaSettings(video_media_dir=str(tmp_path))
    store, clip = _stored(tmp_path, MP4)
    with pytest.raises(LocateError) as refused:
        picture(store, media, _payload(clip))
    assert (refused.value.status, refused.value.code) == (422, "video_media_invalid")
    assert "video/mp4" in refused.value.detail and "抽出一格" in refused.value.detail
    with pytest.raises(LocateError) as missing:
        picture(store, media, _payload("0" * 64))
    assert (missing.value.status, missing.value.code) == (404, "video_media_file_not_found")
    store, broken = _stored(tmp_path, b"\x89PNG\r\n\x1a\n" + b"\x00" * 30)
    with pytest.raises(LocateError) as unreadable:
        picture(store, media, _payload(broken))
    assert (unreadable.value.status, unreadable.value.code) == (422, "video_media_invalid")
    small = MediaSettings(video_media_dir=str(tmp_path), video_media_inline_judge_bytes=1_000_000)
    store, big = _stored(tmp_path, _image("PNG") + b"\x00" * 1_000_000)
    with pytest.raises(LocateError) as too_big:
        picture(store, small, _payload(big))
    assert (too_big.value.status, too_big.value.code) == (413, "video_media_judge_too_large")


def test_boxes_are_clamped_ordered_capped_and_an_empty_answer_is_fine() -> None:
    answer = {
        "boxes": [
            {"label": "Jingwei", "box_2d": [100, 200, 900, 600], "score": 0.93},
            {"label": "boat", "box_2d": [1200, -5, 50, 40.6], "score": 3},
            {"label": "", "box_2d": [10, 10, 20, 20], "score": "high"},
            {"label": "three", "box_2d": [1, 2, 3], "score": 0.5},
            {"label": "flat", "box_2d": [0, 0, 0, 500], "score": 0.5},
            {"label": "bool", "box_2d": [True, 0, 500, 500], "score": 0.5},
            "text",
        ]
    }
    assert boxes(json.dumps(answer)) == [
        SubjectBox(label="Jingwei", box=(100, 200, 900, 600), score=0.93),
        SubjectBox(label="boat", box=(50, 0, 1000, 41), score=1.0),
        SubjectBox(label="subject", box=(10, 10, 20, 20), score=0.0),
    ], "coordinates are clamped to 0-1000 and ordered; no area or the wrong shape is dropped"
    assert boxes(json.dumps({"boxes": []})) == []
    many = {
        "boxes": [{"label": str(n), "box_2d": [0, n, 10, n + 1], "score": 1} for n in range(30)]
    }
    assert len(boxes(json.dumps(many))) == MAX_BOXES
    for text in ("not json", json.dumps({"nope": 1}), json.dumps([]), json.dumps({"boxes": "x"})):
        with pytest.raises(LocateError) as bad:
            boxes(text)
        assert (bad.value.status, bad.value.code) == (502, "video_media_locate_failed"), text


@pytest.mark.asyncio
async def test_locate_calls_gemini_with_the_site_key_and_reads_the_boxes(tmp_path: Path) -> None:
    store, sha = _stored(tmp_path, _image("WEBP", 1920, 1080))
    media = MediaSettings(video_media_dir=str(tmp_path))
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        answer = {"boxes": [{"label": "Jingwei", "box_2d": [120, 300, 980, 620], "score": 0.9}]}
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {"content": {"parts": [{"text": json.dumps(answer)}]}, "finishReason": "STOP"}
                ]
            },
        )

    runtime = Settings(hotspot_guide_gemini_api_key="g", hotspot_guide_gemini_model="gemini-x")
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        out = await locate(runtime, media, store, _payload(sha, labels=["Jingwei"]), client)
    assert out == LocateOut(
        boxes=[SubjectBox(label="Jingwei", box=(120, 300, 980, 620), score=0.9)],
        width=1920,
        height=1080,
        model="gemini-x",
    )
    assert seen[0].headers["x-goog-api-key"] == "g"
    assert seen[0].url.path.endswith("/models/gemini-x:generateContent")
    sent = json.loads(seen[0].content)
    assert sent["contents"][0]["parts"][1]["inline_data"]["mime_type"] == "image/webp"
    with pytest.raises(LocateError) as no_key:
        await locate(Settings(), media, store, _payload(sha))
    assert (no_key.value.status, no_key.value.code) == (503, "video_media_locate_unavailable")
    _, clip = _stored(tmp_path, MP4)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(LocateError) as refused:
            await locate(runtime, media, store, _payload(clip), client)
    assert refused.value.code == "video_media_invalid" and len(seen) == 1, (
        "a clip is refused before Gemini is asked"
    )
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda r: httpx.Response(429, headers={"Retry-After": "9"}))
    ) as client:
        with pytest.raises(LocateError) as busy:
            await locate(runtime, media, store, _payload(sha), client)
    assert (busy.value.status, busy.value.code, busy.value.retry_after) == (
        429,
        "video_media_upstream_busy",
        "9",
    )
    blocked = httpx.Response(200, json={"promptFeedback": {"blockReason": "SAFETY"}})
    async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r: blocked)) as client:
        with pytest.raises(LocateError) as silent:
            await locate(runtime, media, store, _payload(sha), client)
    assert (silent.value.status, silent.value.code) == (502, "video_media_locate_failed")


# The route, on the same fakes as test_video_media_api.py: a context the test owns, no rate
# limit, a fake Redis for the meter.


def _app(token: VideoToolToken | None = None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.media_router, prefix="/api/v1")

    async def session() -> Any:
        fake = AsyncMock()
        fake.scalar = AsyncMock(return_value=None)
        yield fake

    app.dependency_overrides[get_session] = session
    if token is not None:
        app.dependency_overrides[speech_api.video_tool] = lambda: token
    return app


def _row(**changes: Any) -> VideoAutomationSettings:
    return VideoAutomationSettings(
        id=1,
        **{
            **copy.deepcopy(DEFAULT_DRAMA),
            **copy.deepcopy(DEFAULT_SLIDES),
            "drama_enabled": True,
            **changes,
        },
    )


@pytest.fixture
def media(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict[str, Any]:
    settings = MediaSettings(video_media_dir=str(tmp_path))
    store = MediaStore(
        tmp_path,
        max_file_bytes=settings.video_media_max_file_bytes,
        max_total_bytes=settings.video_media_max_total_bytes,
    )
    state: dict[str, Any] = {
        "row": _row(),
        "store": store,
        "redis": fakeredis.aioredis.FakeRedis(),
        "settings": settings,
        "limits": AsyncMock(),
    }

    async def context(session: Any, token_id: Any) -> MediaContext:
        return MediaContext(
            session=session,
            redis=state["redis"],
            store=store,
            runtime=Settings(hotspot_guide_gemini_api_key="g"),
            media=settings,
            row=state["row"],
            token_id=token_id,
        )

    monkeypatch.setattr(admin_api, "_context", context)
    monkeypatch.setattr(admin_api, "get_media_settings", lambda: settings)
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", state["limits"])
    monkeypatch.setattr(meter, "month_usd", AsyncMock(return_value=0.0))
    return state


def _token() -> VideoToolToken:
    return VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")


@pytest.mark.asyncio
async def test_the_route_needs_a_token_and_validates_the_body() -> None:
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://t") as client:
        anonymous = await client.post("/api/v1/video/media/locate", json={})
    assert anonymous.status_code == 401
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        for body in (
            {"slug": "v"},
            {"slug": "v", "sha256": "nope"},
            {"slug": "v", "sha256": "a" * 64, "labels": [""]},
            {"slug": "v", "sha256": "a" * 64, "labels": ["x"] * 9},
            {"slug": "v", "sha256": "a" * 64, "kind": "keyframe"},
        ):
            response = await client.post("/api/v1/video/media/locate", json=body)
            assert response.status_code == 422, body


@pytest.mark.asyncio
async def test_a_locate_call_is_booked_like_a_judge_call(
    media: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    found = LocateOut(
        boxes=[SubjectBox(label="Jingwei", box=(100, 200, 900, 600), score=0.93)],
        width=1920,
        height=1080,
        model="m",
    )
    asked: list[LocateIn] = []

    async def fake_locate(
        runtime: Any, settings: Any, store: Any, payload: LocateIn, client: Any = None
    ) -> LocateOut:
        asked.append(payload)
        if payload.sha256 == "b" * 64:
            raise LocateError(422, "video_media_invalid", "that is a clip")
        return found

    monkeypatch.setattr(admin_api, "locate", fake_locate)
    body = {"slug": "v", "sha256": "a" * 64, "labels": ["Jingwei"]}
    async with AsyncClient(
        transport=ASGITransport(app=_app(_token())), base_url="http://t"
    ) as client:
        ok = await client.post("/api/v1/video/media/locate", json=body)
        clip = await client.post("/api/v1/video/media/locate", json={**body, "sha256": "b" * 64})
        media["row"] = _row(monthly_judge_calls_budget=1)
        spent = await client.post("/api/v1/video/media/locate", json=body)
        status = await client.get("/api/v1/video/media/status")
    assert ok.status_code == 200, ok.text
    assert ok.json() == {
        "boxes": [{"label": "Jingwei", "box": [100, 200, 900, 600], "score": 0.93}],
        "width": 1920,
        "height": 1080,
        "model": "m",
    }
    assert asked[0].labels == ["Jingwei"]
    assert clip.status_code == 422 and clip.json()["code"] == "video_media_invalid"
    assert await meter.used(media["redis"], meter.JUDGE_CALLS) == 1, (
        "the refused call gave its unit back"
    )
    assert spent.status_code == 429 and spent.json()["code"] == "video_media_budget_exhausted"
    assert len(asked) == 2, "a spent budget never reaches Gemini"
    names = [call.args[0] for call in media["limits"].await_args_list]
    assert names[:3] == ["video_media_judge"] * 3, "locate shares the judge's per-hour limit"
    assert status.json()["limits"]["locate_labels"] == 8
