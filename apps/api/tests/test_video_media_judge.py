"""The judge: what it sends Gemini, how a verdict is read, and the pass rule."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx
import pytest

from app.config import Settings
from app.video_media.judge import JudgeError, judge, request_body, verdict
from app.video_media.schemas import JudgeIn
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 20


def _stored(tmp_path: Path, data: bytes) -> tuple[MediaStore, str]:
    import hashlib

    store = MediaStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    sha = hashlib.sha256(data).hexdigest()
    (tmp_path / "v").mkdir(exist_ok=True)
    (tmp_path / "v" / sha).write_bytes(data)
    return store, sha


def _payload(sha: str, **extra: Any) -> JudgeIn:
    return JudgeIn.model_validate(
        {
            "slug": "v",
            "kind": "keyframe",
            "files": [{"sha256": sha, "label": "keyframe"}],
            "rubric": [
                {
                    "key": "identity_jingwei",
                    "question": "Is it the girl of the sheet?",
                    "weight": 2,
                },
                {"key": "artifacts", "question": "Hands, faces, text?", "weight": 1},
            ],
            "context": {"shot": "opening"},
            **extra,
        }
    )


def test_the_request_labels_each_file_and_asks_for_json(tmp_path: Path) -> None:
    store, sha = _stored(tmp_path, PNG)
    media = MediaSettings(video_media_dir=str(tmp_path))
    body = request_body("gemini-3.8-flash", store, media, _payload(sha))
    parts = body["contents"][0]["parts"]
    assert (
        "identity_jingwei (weight 2)" in parts[0]["text"]
        and '"shot": "opening"' in parts[0]["text"]
    )
    assert parts[1] == {"text": "[keyframe]"}
    assert parts[2]["inline_data"]["mime_type"] == "image/png"
    assert body["generationConfig"]["responseMimeType"] == "application/json"
    with pytest.raises(JudgeError) as missing:
        request_body("m", store, media, _payload("0" * 64))
    assert missing.value.code == "video_media_file_not_found"
    small = MediaSettings(video_media_dir=str(tmp_path), video_media_inline_judge_bytes=1_000_000)
    store2, big = _stored(tmp_path, PNG + b"\x00" * 1_000_000)
    with pytest.raises(JudgeError) as too_big:
        request_body("m", store2, small, _payload(big))
    assert too_big.value.code == "video_media_judge_too_large"


def test_a_verdict_is_clamped_weighted_and_passes_only_above_the_bar() -> None:
    payload = _payload("a" * 64)
    good = verdict(
        json.dumps(
            {"scores": {"identity_jingwei": 9, "artifacts": 6}, "problems": [], "notes": "ok"}
        ),
        payload,
        7,
        "m",
    )
    assert good.scores == {"identity_jingwei": 9.0, "artifacts": 6.0}
    assert good.overall == 8.0 and good.passed and good.model == "m"
    weak = verdict(
        json.dumps(
            {"scores": {"identity_jingwei": 10, "artifacts": 3}, "problems": ["six fingers"]}
        ),
        payload,
        7,
        "m",
    )
    assert weak.overall == 7.67 and not weak.passed, (
        "a criterion under 4 fails whatever the overall"
    )
    odd = verdict(
        json.dumps(
            {"scores": {"identity_jingwei": 14, "artifacts": "x"}, "problems": "not a list"}
        ),
        payload,
        5,
        "m",
    )
    assert odd.scores == {"identity_jingwei": 10.0, "artifacts": 0.0} and not odd.passed
    with pytest.raises(JudgeError):
        verdict("not json", payload, 7, "m")
    with pytest.raises(JudgeError):
        verdict(json.dumps({"problems": []}), payload, 7, "m")


@pytest.mark.asyncio
async def test_judge_calls_gemini_with_the_site_key_and_reads_the_json_answer(
    tmp_path: Path,
) -> None:
    store, sha = _stored(tmp_path, PNG)
    media = MediaSettings(video_media_dir=str(tmp_path))
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        answer = {
            "scores": {"identity_jingwei": 8, "artifacts": 9},
            "problems": [],
            "notes": "fine",
        }
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {"content": {"parts": [{"text": json.dumps(answer)}]}, "finishReason": "STOP"}
                ]
            },
        )

    runtime = Settings(hotspot_guide_gemini_api_key="g")
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        out = await judge(runtime, media, store, _payload(sha), 7, client)
    assert out.passed and out.overall == 8.33
    assert seen[0].headers["x-goog-api-key"] == "g" and ":generateContent" in seen[0].url.path
    with pytest.raises(JudgeError) as no_key:
        await judge(Settings(), media, store, _payload(sha), 7)
    assert no_key.value.code == "video_media_judge_unavailable"
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda r: httpx.Response(429, headers={"Retry-After": "9"}))
    ) as client:
        with pytest.raises(JudgeError) as busy:
            await judge(runtime, media, store, _payload(sha), 7, client)
    assert busy.value.status == 429 and busy.value.retry_after == "9"
