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
    # A job's resolution is Gemini's imageSize; without one the model answers at its 1K default.
    large = GeminiImages(GEMINI, "k").request_body(_image_request(resolution="2K"))
    assert large["generationConfig"]["imageConfig"] == {"aspectRatio": "16:9", "imageSize": "2K"}


def test_gemini_images_tell_a_style_plate_from_a_character_sheet() -> None:
    plate = ReferenceImage(role="style", content_type="image/png", data=b"\x89PNGplate")
    styled = GeminiImages(GEMINI, "k").request_body(_image_request(references=(plate,)))
    text = styled["contents"][0]["parts"][0]["text"]
    assert "style plate" in text and "as if by the same hand" in text
    assert "Keep every character" not in text, "a plate carries no character to keep"
    encoded = base64.b64encode(plate.data).decode()
    assert styled["contents"][0]["parts"][1]["inline_data"]["data"] == encoded
    both = GeminiImages(GEMINI, "k").request_body(_image_request(references=(SHEET, plate)))
    text = both["contents"][0]["parts"][0]["text"]
    assert "Keep every character" in text and "The last reference image is a style plate" in text
    none = GeminiImages(GEMINI, "k").request_body(_image_request(references=()))
    assert "reference" not in none["contents"][0]["parts"][0]["text"]


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


def test_lite_keeps_first_last_frames_without_unsupported_audio_or_reference_switches() -> None:
    provider = GeminiVideo(GEMINI, "k")
    body = provider.request_body(
        _clip_request(model="veo-3.1-lite-generate-preview", references=(), last_frame=FRAME)
    )
    assert "image" in body["instances"][0] and "lastFrame" in body["instances"][0]
    assert "referenceImages" not in body["instances"][0]
    assert "generateAudio" not in body["parameters"]
    assert body["parameters"]["durationSeconds"] == 8


@pytest.mark.parametrize("extra", [{"references": (SHEET,)}, {"seconds": 6}])
def test_lite_refuses_incompatible_parameters_before_submit(extra: dict[str, Any]) -> None:
    request = _clip_request(**{"model": "veo-3.1-lite-generate-preview", "references": (), **extra})
    with pytest.raises(MediaUpstreamError) as refused:
        GeminiVideo(GEMINI, "k").request_body(request)
    assert refused.value.kind == "invalid" and refused.value.status == 422


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
    assert image["response_format"] == "base64", "the picture comes back in the answer"
    clip = MiniMaxVideo(MINIMAX, "k").request_body(
        _clip_request(model="MiniMax-H3", resolution="2k")
    )
    assert clip["first_frame_image"].startswith("data:image/jpeg;base64,")
    assert clip["resolution"] == "2K" and clip["duration"] == 8
    assert clip["subject_reference"][0]["image"][0].startswith("data:image/png")
    check_base_resp({"base_resp": {"status_code": 0}})
    for code, kind in (
        (1002, "busy"),
        (1008, "key"),
        (1026, "blocked"),
        (2013, "invalid"),
        (9999, "failed"),
    ):
        with pytest.raises(MediaUpstreamError) as error:
            check_base_resp({"base_resp": {"status_code": code, "status_msg": "x"}})
        assert error.value.kind == kind, code


@pytest.mark.parametrize(
    ("prompt", "negative"),
    [("x" * 1500, ""), ("x" * 1501, ""), ("x" * 1400, "n" * 91)],
)
@pytest.mark.asyncio
async def test_minimax_refuses_overlong_effective_image_prompt_before_network(
    prompt: str, negative: str
) -> None:
    handler, seen = _minimax_answers({})
    async with _client(handler) as client:
        with pytest.raises(MediaUpstreamError) as error:
            await MiniMaxImages(MINIMAX, "secret").submit(
                _image_request(model="image-01", prompt=prompt, negative_prompt=negative), client
            )
    assert (error.value.status, error.value.kind) == (422, "invalid")
    assert "including avoidance text" in error.value.message
    assert seen == [], "a deterministic parameter error must not reach the paid endpoint"


@pytest.mark.parametrize(
    ("prompt", "negative"), [("x" * 1499, ""), ("圖" * 1400, "n" * 90), ("😀" * 1499, "")]
)
def test_minimax_preserves_valid_effective_prompt_and_its_unicode_characters(
    prompt: str, negative: str
) -> None:
    request = _image_request(model="image-01", prompt=prompt, negative_prompt=negative)
    body = MiniMaxImages(MINIMAX, "secret").request_body(request)
    expected = prompt + (f". Avoid: {negative}" if negative else "")
    assert len(expected) == 1499 and body["prompt"] == expected
    assert request.prompt == prompt and request.negative_prompt == negative


def _minimax_answers(*data: Any) -> tuple[Any, list[httpx.Request]]:
    """A handler answering image requests with these ``data`` objects in turn, and what it saw."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            200,
            json={
                "id": "trace-1",
                "data": data[len(seen) - 1],
                "metadata": {"success_count": "1", "failed_count": "0"},
                "base_resp": {"status_code": 0, "status_msg": "success"},
            },
        )

    return handler, seen


@pytest.mark.asyncio
async def test_minimax_images_come_back_as_bytes_in_the_answer() -> None:
    jpeg = b"\xff\xd8\xff\xe0" + b"picture" * 20
    png = b"\x89PNG\r\n\x1a\n" + b"picture" * 20
    wrapped = base64.encodebytes(jpeg).decode()
    assert "\n" in wrapped.strip(), "a line-wrapped answer"
    handler, seen = _minimax_answers(
        {"image_base64": [base64.b64encode(jpeg).decode()]},
        {"image_base64": [base64.b64encode(png).decode()], "image_urls": []},
        {"image_base64": [wrapped]},
    )
    provider = MiniMaxImages(MINIMAX, "secret")
    async with _client(handler) as client:
        first = await provider.submit(_image_request(model="image-01"), client)
        second = await provider.submit(_image_request(model="image-01"), client)
        third = await provider.submit(_image_request(model="image-01"), client)
    assert (first.inline, first.content_type) == (jpeg, "image/jpeg")
    assert first.download is None and first.vendor_ref is None, "nothing to fetch or to poll"
    assert (second.inline, second.content_type) == (png, "image/png"), "the type is in the bytes"
    assert third.inline == jpeg
    assert seen[0].url.path == "/v1/image_generation"
    assert seen[0].headers["authorization"] == "Bearer secret"
    assert json.loads(seen[0].content)["response_format"] == "base64"


@pytest.mark.asyncio
async def test_a_minimax_answer_with_only_a_link_still_goes_through_the_download_check() -> None:
    handler, _seen = _minimax_answers(
        {"image_urls": ["https://cdn.minimax.example/p-1.jpeg"]},
        {"image_base64": [], "image_urls": ["http://cdn.minimax.example/p-2.jpeg"]},
    )
    provider = MiniMaxImages(MINIMAX, "secret")
    async with _client(handler) as client:
        linked = await provider.submit(_image_request(model="image-01"), client)
        refused = await provider.submit(_image_request(model="image-01"), client)
    assert linked.inline is None and linked.download == Download(
        url="https://cdn.minimax.example/p-1.jpeg", content_type_hint="image/jpeg"
    )
    assert provider.fetch(linked.download) == ("https://cdn.minimax.example/p-1.jpeg", {})
    assert refused.inline is None and refused.download is not None
    with pytest.raises(MediaUpstreamError) as error:
        provider.fetch(refused.download)
    assert error.value.kind == "invalid"
    assert error.value.message == "the vendor's download URL is not an https address"


NO_IMAGE = "MiniMax returned no image"
NOT_A_STRING = "MiniMax's image is not a base64 string"
NOT_BASE64 = "MiniMax's image is not valid base64"
EMPTY_IMAGE = "MiniMax returned an empty image"


@pytest.mark.parametrize(
    ("data", "message"),
    [
        pytest.param({"image_base64": []}, NO_IMAGE, id="empty-list"),
        pytest.param({"image_base64": [], "image_urls": []}, NO_IMAGE, id="empty-lists"),
        pytest.param({"image_base64": None, "image_urls": [7]}, NO_IMAGE, id="link-not-a-string"),
        pytest.param({}, NO_IMAGE, id="no-fields"),
        pytest.param(None, NO_IMAGE, id="no-data"),
        pytest.param(["VENDOR-TEXT"], NO_IMAGE, id="data-is-a-list"),
        pytest.param({"image_base64": "VENDOR-TEXT"}, NO_IMAGE, id="not-a-list"),
        pytest.param({"image_base64": [None]}, NOT_A_STRING, id="null-item"),
        pytest.param({"image_base64": [{"b64": "VENDOR-TEXT"}]}, NOT_A_STRING, id="object-item"),
        pytest.param(
            {"image_base64": ["VENDOR-TEXT: https://signed.example/p?token=abc"]},
            NOT_BASE64,
            id="not-base64",
        ),
        pytest.param({"image_base64": ["/9j/4AAQ="]}, NOT_BASE64, id="broken-padding"),
        pytest.param({"image_base64": ["  \n"]}, EMPTY_IMAGE, id="blank-item"),
    ],
)
@pytest.mark.asyncio
async def test_a_minimax_answer_without_a_usable_picture_is_a_vendor_failure(
    data: Any, message: str
) -> None:
    handler, _seen = _minimax_answers(data)
    async with _client(handler) as client:
        with pytest.raises(MediaUpstreamError) as error:
            await MiniMaxImages(MINIMAX, "k").submit(_image_request(model="image-01"), client)
    assert (error.value.status, error.value.kind) == (502, "failed")
    assert error.value.message == message, "a fixed message: nothing the vendor sent is repeated"


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


LAST = ReferenceImage(role="last_frame", content_type="image/png", data=b"\x89PNGlast")
PREVIOUS = ReferenceImage(role="previous_frame", content_type="image/png", data=b"\x89PNGprev")


@pytest.mark.parametrize("model", ["MiniMax-Hailuo-2.3", "MiniMax-Hailuo-02", "I2V-01-Director"])
@pytest.mark.parametrize("full", [True, False], ids=["frames-and-sheets", "first-frame-only"])
@pytest.mark.asyncio
async def test_every_model_but_h3_keeps_the_v1_path_body_and_poll_byte_for_byte(
    model: str, full: bool
) -> None:
    """The v1 request as it stood before H3 moved to v2: same URL, same bytes, same polls."""
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if request.url.path == "/v1/video_generation":
            return httpx.Response(200, json={"task_id": "t 1", "base_resp": {"status_code": 0}})
        if request.url.path == "/v1/query/video_generation":
            return httpx.Response(
                200, json={"status": "Success", "file_id": "f 1", "base_resp": {"status_code": 0}}
            )
        return httpx.Response(
            200,
            json={
                "file": {"download_url": "https://cdn.minimax.example/f-1.mp4"},
                "base_resp": {"status_code": 0},
            },
        )

    extra: dict[str, Any] = (
        {"negative_prompt": "blur", "last_frame": LAST, "references": (SHEET, PREVIOUS, SHEET)}
        if full
        else {"negative_prompt": None, "resolution": None, "references": ()}
    )
    request = _clip_request(model=model, seconds=6, **extra)
    provider = MiniMaxVideo(MINIMAX, "secret")
    async with _client(handler) as client:
        submitted = await provider.submit(request, client)
        done = await provider.poll(submitted.vendor_ref or "", client)
    expected: dict[str, Any] = {
        "model": model,
        "prompt": "slow push in. Avoid: blur" if full else "slow push in",
        "first_frame_image": f"data:image/jpeg;base64,{base64.b64encode(FRAME.data).decode()}",
        "duration": 6,
        "prompt_optimizer": False,
    }
    if full:
        sheet = f"data:image/png;base64,{base64.b64encode(SHEET.data).decode()}"
        expected["resolution"] = "1080P"
        expected["last_frame_image"] = f"data:image/png;base64,{base64.b64encode(LAST.data).decode()}"
        expected["subject_reference"] = [{"type": "character", "image": [sheet, sheet]}]
    sent = calls[0]
    assert (sent.method, str(sent.url)) == ("POST", "https://api.minimaxi.com/v1/video_generation")
    # The same encoder httpx used, so key order and every byte are compared.
    assert sent.content == httpx.Request("POST", sent.url, json=expected).content
    assert sent.headers["authorization"] == "Bearer secret"
    assert submitted.vendor_ref == "t 1", "a v1 task id is kept as the vendor sent it"
    assert [str(call.url) for call in calls[1:]] == [
        "https://api.minimaxi.com/v1/query/video_generation?task_id=t%201",
        "https://api.minimaxi.com/v1/files/retrieve?file_id=f%201",
    ]
    assert done.state == "done" and done.download is not None


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


@pytest.mark.parametrize("native_audio", [False, True])
def test_lite_keeps_avoidance_constraints_in_its_supported_prompt(native_audio: bool) -> None:
    request = _clip_request(
        model="veo-3.1-lite-generate-preview",
        references=(),
        last_frame=FRAME,
        negative_prompt="extra hands, duplicate watches",
        native_audio=native_audio,
        seed=7,
    )
    body = GeminiVideo(GEMINI, "secret").request_body(request)
    instance = body["instances"][0]
    assert instance["prompt"] == "slow push in\n\nAvoid: extra hands, duplicate watches"
    assert "negativePrompt" not in body["parameters"]
    assert body["parameters"] == {
        "aspectRatio": "16:9",
        "durationSeconds": 8,
        "personGeneration": "allow_adult",
        "resolution": "1080p",
        "seed": 7,
    }
    assert (
        instance["image"]
        == instance["lastFrame"]
        == {
            "mimeType": FRAME.content_type,
            "bytesBase64Encoded": base64.b64encode(FRAME.data).decode(),
        }
    )
    assert "referenceImages" not in instance
    assert request.prompt == "slow push in"
    assert request.negative_prompt == "extra hands, duplicate watches"


@pytest.mark.parametrize("model", ["veo-3.1-generate-preview", "gemini-omni-1.1-flash"])
def test_non_lite_video_retains_its_supported_negative_prompt_field(model: str) -> None:
    body = GeminiVideo(GEMINI, "secret").request_body(
        _clip_request(model=model, negative_prompt="extra hands", native_audio=True)
    )
    assert body["instances"][0]["prompt"] == "slow push in"
    assert body["parameters"]["negativePrompt"] == "extra hands"
    assert body["parameters"]["generateAudio"] is True
    assert body["instances"][0]["referenceImages"][0]["referenceType"] == "asset"


@pytest.mark.parametrize("negative_prompt", [None, ""])
def test_lite_without_avoidance_text_preserves_the_prompt(negative_prompt: str | None) -> None:
    body = GeminiVideo(GEMINI, "secret").request_body(
        _clip_request(
            model="veo-3.1-lite-generate-preview", references=(), negative_prompt=negative_prompt
        )
    )
    assert body["instances"][0]["prompt"] == "slow push in"
    assert "negativePrompt" not in body["parameters"]


@pytest.mark.asyncio
async def test_lite_submit_sends_one_compatible_request_without_losing_constraints() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        body = json.loads(request.content)
        assert "negativePrompt" not in body["parameters"]
        assert body["instances"][0]["prompt"] == "slow push in\n\nAvoid: duplicate watches"
        return httpx.Response(200, json={"name": "models/lite/operations/mock-1"})

    async with _client(handler) as client:
        submitted = await GeminiVideo(GEMINI, "fake-secret").submit(
            _clip_request(
                model="veo-3.1-lite-generate-preview",
                references=(),
                negative_prompt="duplicate watches",
            ),
            client,
        )
    assert submitted.vendor_ref == "models/lite/operations/mock-1"
    assert len(seen) == 1
    assert seen[0].url.path == "/v1beta/models/veo-3.1-lite-generate-preview:predictLongRunning"
    assert seen[0].headers["x-goog-api-key"] == "fake-secret"


@pytest.mark.parametrize(
    ("message", "detail"),
    [
        (
            "negativePrompt is not supported by this model. Please remove it.",
            "INVALID_ARGUMENT; unsupported parameter: negativePrompt",
        ),
        (
            'The parameter "generateAudio" is not supported by this model.',
            "INVALID_ARGUMENT; unsupported parameter: generateAudio",
        ),
        (
            "The request was blocked due to safety filters.",
            "INVALID_ARGUMENT; safety rejection",
        ),
        ("The image dimensions are invalid.", "INVALID_ARGUMENT"),
        ("This was not a safety rejection.", "INVALID_ARGUMENT"),
    ],
)
def test_http_rejection_keeps_only_a_canonical_diagnostic(message: str, detail: str) -> None:
    response = httpx.Response(
        400, json={"error": {"code": 400, "status": "INVALID_ARGUMENT", "message": message}}
    )
    with pytest.raises(MediaUpstreamError) as error:
        raise_for_status(response, "Gemini")
    assert error.value.message == f"Gemini refused the request ({detail})"
    assert (error.value.status, error.value.kind, error.value.retry_after) == (422, "blocked", None)


def test_http_rejection_never_retains_request_secrets_or_raw_details(
    caplog: pytest.LogCaptureFixture,
) -> None:
    secrets = [
        "AIza-fake-private-key-xyz",
        "Bearer private-token-xyz",
        "https://files.example/clip?key=private-query&X-Goog-Signature=private-signature",
        "a complete private prompt about a sentinel-actor",
        "data:image/png;base64,cHJpdmF0ZS1mcmFtZS1ieXRlcw==",
    ]
    response = httpx.Response(
        400,
        json={
            "error": {
                "code": 400,
                "status": "INVALID_ARGUMENT",
                "message": "negativePrompt is not supported by this model. " + " ".join(secrets),
                "details": [{"request": secrets, "status": secrets[0]}],
            },
            "request": secrets,
        },
    )
    with pytest.raises(MediaUpstreamError) as error:
        raise_for_status(response, "Gemini")
    assert error.value.message == (
        "Gemini refused the request (INVALID_ARGUMENT; unsupported parameter: negativePrompt)"
    )
    for secret in secrets:
        assert secret not in str(error.value)
        assert secret not in repr(error.value)
        assert secret not in caplog.text
    assert len(error.value.message) < 200


@pytest.mark.parametrize(
    "body",
    [
        b"",
        b"<html>private upstream failure</html>",
        b"{not json",
        b"[]",
        b'{"error":[]}',
        b'{"error":{"code":400,"status":"INVALID_ARGUMENT"}}',
        b'{"error":{"code":400,"status":"INVALID_ARGUMENT","message":[]}}',
        b'{"error":{"code":400,"status":"private-status","message":"private prompt"}}',
        b'{"error":{"code":400,"status":"INVALID_ARGUMENT","message":"' + b"x" * 2049 + b'"}}',
        b'{"error":{"code":400,"status":"INVALID_ARGUMENT","message":"' + b"x" * 8193 + b'"}}',
        b"[" * 2000 + b"]" * 2000,
    ],
)
def test_http_rejection_unusable_bodies_have_a_safe_generic_fallback(body: bytes) -> None:
    with pytest.raises(MediaUpstreamError) as error:
        raise_for_status(httpx.Response(400, content=body), "Gemini")
    assert error.value.message == "Gemini refused the request"
    assert (error.value.status, error.value.kind) == (422, "blocked")


def test_http_rejection_does_not_read_an_unconsumed_stream() -> None:
    response = httpx.Response(400, stream=httpx.ByteStream(b"private unread response"))
    with pytest.raises(MediaUpstreamError) as error:
        raise_for_status(response, "Gemini")
    assert error.value.message == "Gemini refused the request"
    assert not response.is_stream_consumed


@pytest.mark.parametrize(
    ("status", "mapped_status", "kind", "retry"),
    [
        (429, 429, "busy", "7"),
        (401, 502, "key", None),
        (403, 502, "key", None),
        (404, 422, "invalid", None),
        (503, 502, "failed", "7"),
        (418, 502, "failed", None),
    ],
)
def test_http_rejection_diagnostics_do_not_change_other_error_classifications(
    status: int, mapped_status: int, kind: str, retry: str | None
) -> None:
    response = httpx.Response(
        status,
        headers={"Retry-After": "7"},
        json={"error": {"code": 400, "status": "INVALID_ARGUMENT", "message": "private prompt"}},
    )
    with pytest.raises(MediaUpstreamError) as error:
        raise_for_status(response, "Gemini")
    assert (error.value.status, error.value.kind, error.value.retry_after) == (
        mapped_status,
        kind,
        retry,
    )
    assert "private prompt" not in error.value.message
    assert "INVALID_ARGUMENT" not in error.value.message


@pytest.mark.asyncio
async def test_http_rejection_is_propagated_without_resubmitting_a_paid_request() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            400,
            json={
                "error": {
                    "code": 400,
                    "status": "INVALID_ARGUMENT",
                    "message": "negativePrompt is not supported by this model.",
                }
            },
        )

    async with _client(handler) as client:
        with pytest.raises(MediaUpstreamError) as error:
            await GeminiVideo(GEMINI, "fake-secret").submit(_clip_request(), client)
    assert error.value.message == (
        "Gemini refused the request (INVALID_ARGUMENT; unsupported parameter: negativePrompt)"
    )
    assert len(seen) == 1
    assert seen[0].method == "POST"
    assert seen[0].url.host == "generativelanguage.googleapis.com"
