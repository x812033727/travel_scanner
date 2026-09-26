"""The vendor adapters: what they send, how they read answers, and where a key may travel."""

from __future__ import annotations

import base64
import json
from typing import Any

import httpx
import pytest

from app.video_media.providers import (
    Download,
    MediaRequest,
    MediaUpstreamError,
    ReferenceImage,
    check_download,
    public_https_host,
    raise_for_status,
)
from app.video_media.providers.gemini_images import GeminiImages
from app.video_media.providers.gemini_music import GeminiMusic
from app.video_media.providers.gemini_video import GeminiVideo
from app.video_media.providers.minimax import MiniMaxImages, MiniMaxVideo, check_base_resp

GEMINI = "https://generativelanguage.googleapis.com"
MINIMAX = "https://api.minimaxi.com/v1"
SHEET = ReferenceImage(role="character", content_type="image/png", data=b"\x89PNGsheet")
FRAME = ReferenceImage(role="first_frame", content_type="image/jpeg", data=b"\xff\xd8\xffframe")


def _client(handler: Any) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


def _image_request(**extra: Any) -> MediaRequest:
    fields: dict[str, Any] = {
        "kind": "image",
        "model": "gemini-3-pro-image",
        "prompt": "a girl on a ridge",
        "negative_prompt": "text",
        "aspect": "16:9",
        "references": (SHEET,),
    }
    return MediaRequest(**{**fields, **extra})


def _clip_request(**extra: Any) -> MediaRequest:
    fields: dict[str, Any] = {
        "kind": "clip",
        "model": "gemini-omni-1.1-flash",
        "prompt": "slow push in",
        "seconds": 8,
        "resolution": "1080p",
        "first_frame": FRAME,
        "references": (SHEET,),
    }
    return MediaRequest(**{**fields, **extra})


def test_gemini_images_send_the_prompt_the_references_and_the_aspect() -> None:
    body = GeminiImages(GEMINI, "k").request_body(_image_request())
    parts = body["contents"][0]["parts"]
    assert "Avoid: text" in parts[0]["text"] and "reference images" in parts[0]["text"]
    assert parts[1]["inline_data"] == {
        "mime_type": "image/png",
        "data": base64.b64encode(SHEET.data).decode(),
    }
    assert body["generationConfig"]["imageConfig"] == {"aspectRatio": "16:9"}
    assert body["generationConfig"]["responseModalities"] == ["IMAGE"]


@pytest.mark.asyncio
async def test_gemini_images_come_back_inline_and_a_refusal_is_blocked() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if json.loads(request.content)["contents"][0]["parts"][0]["text"].startswith("blocked"):
            return httpx.Response(200, json={"promptFeedback": {"blockReason": "SAFETY"}})
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {
                                    "inlineData": {
                                        "mimeType": "image/png",
                                        "data": base64.b64encode(b"\x89PNGout").decode(),
                                    }
                                }
                            ]
                        }
                    }
                ]
            },
        )

    provider = GeminiImages(GEMINI, "secret")
    async with _client(handler) as client:
        out = await provider.submit(_image_request(), client)
        with pytest.raises(MediaUpstreamError) as blocked:
            await provider.submit(_image_request(prompt="blocked prompt"), client)
    assert (out.inline, out.content_type) == (b"\x89PNGout", "image/png")
    assert blocked.value.kind == "blocked" and "SAFETY" in blocked.value.message
    assert seen[0].url.path == "/v1beta/models/gemini-3-pro-image:generateContent"
    assert seen[0].headers["x-goog-api-key"] == "secret"
    assert "Mokaair-video" in seen[0].headers["user-agent"]


def test_gemini_video_body_carries_frames_references_and_parameters() -> None:
    body = GeminiVideo(GEMINI, "k").request_body(
        _clip_request(last_frame=FRAME, native_audio=True, seed=7)
    )
    instance = body["instances"][0]
    assert instance["image"]["mimeType"] == "image/jpeg" and "lastFrame" in instance
    assert instance["referenceImages"][0]["referenceType"] == "asset"
    assert body["parameters"] == {
        "aspectRatio": "16:9",
        "durationSeconds": 8,
        "personGeneration": "allow_adult",
        "generateAudio": True,
        "resolution": "1080p",
        "seed": 7,
    }
    with pytest.raises(MediaUpstreamError):
        GeminiVideo(GEMINI, "k").request_body(_clip_request(first_frame=None))


@pytest.mark.asyncio
async def test_gemini_video_is_submitted_polled_and_fetched_only_from_its_own_host() -> None:
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(f"{request.method} {request.url.path}")
        if request.url.path.endswith(":predictLongRunning"):
            return httpx.Response(200, json={"name": "models/x/operations/op-1"})
        if len(calls) == 2:
            return httpx.Response(200, json={"name": "models/x/operations/op-1", "done": False})
        return httpx.Response(
            200,
            json={
                "done": True,
                "response": {
                    "generateVideoResponse": {
                        "generatedSamples": [
                            {"video": {"uri": f"{GEMINI}/v1beta/files/abc:download?alt=media"}}
                        ]
                    }
                },
            },
        )

    provider = GeminiVideo(GEMINI, "secret")
    async with _client(handler) as client:
        submitted = await provider.submit(_clip_request(), client)
        running = await provider.poll(submitted.vendor_ref or "", client)
        done = await provider.poll(submitted.vendor_ref or "", client)
    assert submitted.vendor_ref == "models/x/operations/op-1"
    assert running.state == "running" and done.state == "done"
    assert done.download is not None and done.download.needs_key
    url, headers = provider.fetch(done.download)
    assert url.startswith(GEMINI) and headers == {"x-goog-api-key": "secret"}
    with pytest.raises(MediaUpstreamError) as elsewhere:
        provider.fetch(Download(url="https://evil.example/clip.mp4", needs_key=True))
    assert elsewhere.value.kind == "invalid"
    assert calls == [
        "POST /v1beta/models/gemini-omni-1.1-flash:predictLongRunning",
        "GET /v1beta/models/x/operations/op-1",
        "GET /v1beta/models/x/operations/op-1",
    ]


@pytest.mark.asyncio
async def test_a_filtered_or_errored_gemini_operation_fails_with_a_reason() -> None:
    answers = iter(
        [
            {
                "done": True,
                "response": {
                    "generateVideoResponse": {
                        "raiMediaFilteredCount": 1,
                        "raiMediaFilteredReasons": ["violence"],
                    }
                },
            },
            {"done": True, "error": {"message": "internal"}},
        ]
    )
    provider = GeminiVideo(GEMINI, "k")
    async with _client(lambda request: httpx.Response(200, json=next(answers))) as client:
        filtered = await provider.poll("models/x/operations/op", client)
        errored = await provider.poll("models/x/operations/op", client)
    assert filtered.state == "failed" and "violence" in (filtered.reason or "")
    assert errored.state == "failed" and errored.reason == "internal"


def test_lyria_asks_for_an_instrumental_of_the_wanted_length() -> None:
    body = GeminiMusic(GEMINI, "k").request_body(
        MediaRequest(kind="music", model="lyria-3.5", prompt="solo guqin", seconds=150)
    )
    text = body["contents"][0]["parts"][0]["text"]
    assert "solo guqin" in text and "150 seconds" in text and "no vocals" in text
    assert body["generationConfig"]["responseModalities"] == ["AUDIO"]


def test_minimax_bodies_and_status_codes() -> None:
    image = MiniMaxImages(MINIMAX, "k").request_body(_image_request(model="image-01"))
    assert image["subject_reference"][0]["image_file"].startswith("data:image/png;base64,")
    assert image["aspect_ratio"] == "16:9" and image["n"] == 1
    clip = MiniMaxVideo(MINIMAX, "k").request_body(
        _clip_request(model="MiniMax-H3", resolution="2k")
    )
    assert clip["first_frame_image"].startswith("data:image/jpeg;base64,")
    assert clip["resolution"] == "2K" and clip["duration"] == 8
    assert clip["subject_reference"][0]["image"][0].startswith("data:image/png")
    check_base_resp({"base_resp": {"status_code": 0}})
    for code, kind in ((1002, "busy"), (1008, "key"), (1026, "blocked"), (9999, "failed")):
        with pytest.raises(MediaUpstreamError) as error:
            check_base_resp({"base_resp": {"status_code": code, "status_msg": "x"}})
        assert error.value.kind == kind, code


@pytest.mark.asyncio
async def test_minimax_video_polls_to_a_download_url_without_sending_the_key() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        path = request.url.path
        if path == "/v1/video_generation":
            return httpx.Response(200, json={"task_id": "t-1", "base_resp": {"status_code": 0}})
        if path.endswith("/query/video_generation"):
            status = "Processing" if len(calls) == 2 else "Success"
            return httpx.Response(
                200, json={"status": status, "file_id": "f-1", "base_resp": {"status_code": 0}}
            )
        return httpx.Response(
            200,
            json={
                "file": {"download_url": "https://cdn.minimax.example/f-1.mp4"},
                "base_resp": {"status_code": 0},
            },
        )

    provider = MiniMaxVideo(MINIMAX, "secret")
    async with _client(handler) as client:
        submitted = await provider.submit(
            _clip_request(model="MiniMax-H3", resolution="768p"), client
        )
        running = await provider.poll("t-1", client)
        done = await provider.poll("t-1", client)
    assert submitted.vendor_ref == "t-1" and running.state == "running" and done.state == "done"
    assert calls[0].headers["authorization"] == "Bearer secret"
    assert done.download is not None
    assert provider.fetch(done.download) == ("https://cdn.minimax.example/f-1.mp4", {})


def test_downloads_must_be_https_on_a_real_host() -> None:
    assert public_https_host("https://cdn.example.com/a.mp4") == "cdn.example.com"
    for url in (
        "http://cdn.example.com/a",
        "https://127.0.0.1/a",
        "https://localhost/a",
        "https://[::1]/a",
        "ftp://x/a",
    ):
        assert public_https_host(url) is None, url
        with pytest.raises(MediaUpstreamError):
            check_download(Download(url=url))
    with pytest.raises(MediaUpstreamError):
        check_download(Download(url="https://cdn.example.com/a"), frozenset({"other.example"}))


def test_http_statuses_say_who_can_fix_them() -> None:
    raise_for_status(httpx.Response(200), "v")
    for status, kind in (
        (429, "busy"),
        (401, "key"),
        (403, "key"),
        (404, "invalid"),
        (400, "blocked"),
        (503, "failed"),
    ):
        with pytest.raises(MediaUpstreamError) as error:
            raise_for_status(httpx.Response(status, headers={"Retry-After": "7"}), "v")
        assert error.value.kind == kind, status
        if status in (429, 503):
            assert error.value.retry_after == "7"
