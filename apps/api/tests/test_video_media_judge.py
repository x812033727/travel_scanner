"""The judge: what it sends Gemini, how a verdict is read, and the pass rule."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import httpx
import pytest

from app.config import Settings
from app.video_media.judge import (
    CHECK_INSTRUCTIONS,
    FIX_ARROW,
    INSTRUCTIONS,
    MAX_FIX_CHARS,
    MAX_PROBLEM_CHARS,
    MAX_PROBLEMS,
    PLACEHOLDER_FIX,
    UNDESCRIBED,
    JudgeError,
    judge,
    request_body,
    verdict,
)
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
    scores = body["generationConfig"]["responseSchema"]["properties"]["scores"]
    assert scores["required"] == ["identity_jingwei", "artifacts"]
    assert set(scores["properties"]) == {"identity_jingwei", "artifacts"}
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


def _checks(sha: str) -> JudgeIn:
    return _payload(
        sha,
        rubric=[
            {"key": "text", "question": "Can you read any letter?", "weight": 0.25, "cost": 10},
            {"key": "anatomy", "question": "More than five digits?", "weight": 0.25, "cost": 10},
            {"key": "details", "question": "A secondary thing missing?", "weight": 2, "cost": 3},
            {"key": "awkward", "question": "An awkward hand?", "weight": 3, "cost": 6},
        ],
    )


def test_fault_checks_are_asked_yes_or_no_and_a_scored_rubric_is_asked_as_before(
    tmp_path: Path,
) -> None:
    store, sha = _stored(tmp_path, PNG)
    media = MediaSettings(video_media_dir=str(tmp_path))
    scored = request_body("m", store, media, _payload(sha))
    assert scored["system_instruction"]["parts"][0]["text"] == INSTRUCTIONS
    assert list(scored["generationConfig"]["responseSchema"]["properties"]) == [
        "scores",
        "problems",
        "notes",
    ]
    body = request_body("m", store, media, _checks(sha))
    assert body["system_instruction"]["parts"][0]["text"] == CHECK_INSTRUCTIONS
    assert "\n" not in CHECK_INSTRUCTIONS and "answer true when it is there" in CHECK_INSTRUCTIONS
    lead = body["contents"][0]["parts"][0]["text"]
    assert "- text: Can you read any letter?\n- anatomy: More than five digits?" in lead
    assert "weight" not in lead and "cost" not in lead, "the arithmetic stays on the server"
    schema = body["generationConfig"]["responseSchema"]
    assert list(schema["properties"]) == ["faults", "problems", "notes"]
    assert schema["required"] == ["faults", "problems", "notes"]
    assert schema["properties"]["faults"] == {
        "type": "object",
        "properties": {
            key: {"type": "boolean"} for key in ("text", "anatomy", "details", "awkward")
        },
        "required": ["text", "anatomy", "details", "awkward"],
    }
    with pytest.raises(ValueError, match="all fault checks"):
        _payload(
            sha,
            rubric=[
                {"key": "text", "question": "Any letter?", "cost": 10},
                {"key": "style", "question": "In the style?"},
            ],
        )


def test_a_checks_verdict_scores_ten_less_the_cost_of_each_fault_found() -> None:
    payload = _checks("a" * 64)

    def answered(**faults: Any) -> Any:
        found = {"text": False, "anatomy": False, "details": False, "awkward": False, **faults}
        return verdict(json.dumps({"faults": found, "problems": [], "notes": ""}), payload, 7, "m")

    clean = answered()
    assert clean.scores == {"text": 10.0, "anatomy": 10.0, "details": 10.0, "awkward": 10.0}
    assert clean.overall == 10.0 and clean.passed, "nothing found is the top of the scale"
    flawed = answered(details=True, awkward=True)
    assert flawed.scores["details"] == 7.0 and flawed.scores["awkward"] == 4.0
    assert flawed.overall == 5.64 and not flawed.passed, "two flaws weigh the overall under the bar"
    assert answered(details=True).overall == 8.91 and answered(details=True).passed
    assert answered(awkward=True).overall == 6.73, "this rubric is four of the tool's nine checks"
    redo = answered(text=True)
    assert redo.scores["text"] == 0.0 and redo.overall == 9.55 and not redo.passed, (
        "a fault that costs the whole criterion fails the take whatever the overall"
    )
    silent = verdict(json.dumps({"faults": {"text": False}, "problems": []}), payload, 0, "m")
    assert silent.scores == {"text": 10.0, "anatomy": 0.0, "details": 7.0, "awkward": 4.0}, (
        "a check that was not answered false counts as the fault"
    )
    assert not silent.passed
    odd = verdict(json.dumps({"faults": {"text": "no", "anatomy": 0}}), payload, 0, "m")
    assert odd.scores["text"] == 0.0 and odd.scores["anatomy"] == 0.0, "only a plain false clears"
    with pytest.raises(JudgeError):
        verdict(json.dumps({"scores": {"text": 10}, "problems": []}), payload, 7, "m")


# One line per fault: "<criterion key>: <what is wrong and where> → <one change to the prompt>"
# (docs/videos/ILLUSTRATED.md §judge 的 problems). The judge is asked for it and held to it.
LINE = re.compile(r"[a-z][a-z0-9_]*: .+ → .+")


def test_the_instructions_ask_for_a_keyed_line_with_a_prompt_fix_per_fault() -> None:
    for text in (INSTRUCTIONS, CHECK_INSTRUCTIONS):
        assert '"<criterion key>: <what is wrong and where> → <the one change to the prompt' in text
        assert "as the words to put in the prompt" in text
        assert "name the criterion by its key as the rubric writes it" in text
        assert "look for the same fault everywhere" in text
    # The scale and the fault questions are asked as they were measured; only the problems changed.
    assert "from 0 (fails completely) to 10 (flawless)" in INSTRUCTIONS
    assert "Be strict" in INSTRUCTIONS
    assert "answer true when it is there and false when it is not" in CHECK_INSTRUCTIONS
    assert "never reads the prompt" in CHECK_INSTRUCTIONS


def test_checks_problems_are_one_keyed_line_per_fault_found_with_a_prompt_fix() -> None:
    payload = _checks("a" * 64)
    found = {"text": True, "anatomy": True, "details": False, "awkward": True}
    hand = "awkward: the barista's right hand is a blur → her right hand flat on the counter"
    told = [
        hand,
        "details: the lamp is on the left → the lamp on the right",  # not a fault found: dropped
        "the sign over the door reads CAFE → a plain sign",  # names no criterion: dropped
        "`Text`: a sign over the door reads CAFE",  # no fix: the placeholder
        "anatomy -> every hand with four fingers and a thumb",  # straight to the fix
        hand,  # said twice, kept once
    ]
    out = verdict(json.dumps({"faults": found, "problems": told, "notes": ""}), payload, 7, "m")
    assert out.problems == [
        hand,
        f"text: a sign over the door reads CAFE → {PLACEHOLDER_FIX}",
        f"anatomy: {UNDESCRIBED} → every hand with four fingers and a thumb",
    ], "the judge's order, one line per fault it found, the key as the rubric writes it"
    assert all(LINE.fullmatch(line) for line in out.problems)
    assert not out.passed and out.scores["details"] == 10.0
    # A fault found with no word about it gets a line of its own, with the question asked.
    quiet = {**found, "anatomy": False, "awkward": False}
    silent = verdict(
        json.dumps({"faults": quiet, "problems": ["awkward: a stiff hand → a relaxed hand"]}),
        payload,
        7,
        "m",
    )
    assert silent.problems == [
        f"text: {UNDESCRIBED} (asked: Can you read any letter?) → {PLACEHOLDER_FIX}"
    ]
    # Nothing found: nothing kept, whatever the judge remarked.
    clean = verdict(
        json.dumps({"faults": dict.fromkeys(found, False), "problems": ["details: x → y"]}),
        payload,
        7,
        "m",
    )
    assert clean.problems == [] and clean.passed


def test_scored_problems_name_the_criteria_under_the_bar_or_the_floor() -> None:
    payload = _payload("a" * 64)
    hair = "identity_jingwei: the hair is longer than on the sheet → hair to the shoulder"
    hand = "artifacts: six fingers on the left hand → the left hand with five fingers"
    # The key dressed up as a title or in bold, with a dash: still the rubric's key.
    told = [
        "Identity Jingwei: the hair is longer than on the sheet → hair to the shoulder",
        "**artifacts** - six fingers on the left hand → the left hand with five fingers",
    ]

    def answer(scores: dict[str, float], bar: int = 7) -> Any:
        return verdict(json.dumps({"scores": scores, "problems": told}), payload, bar, "m")

    under = answer({"identity_jingwei": 9, "artifacts": 6.5})
    assert under.problems == [hand], "a remark on a criterion at or over the bar is dropped"
    assert under.passed, "a passed take still names the criterion under the bar"
    both = answer({"identity_jingwei": 6.9, "artifacts": 6.5})
    assert both.problems == [hair, hand] and not both.passed
    # The seven the judge gives "nothing wrong" (ILLUSTRATED.md §judge 的刻度與判定沿用) fails
    # no criterion, so its remarks go.
    seven = answer({"identity_jingwei": 7, "artifacts": 7})
    assert seven.problems == [] and seven.passed
    # Under the floor of 4 a criterion fails the take at any bar, and is named when the judge
    # said nothing about it.
    floor = verdict(
        json.dumps({"scores": {"identity_jingwei": 10, "artifacts": 3}, "problems": []}),
        payload,
        0,
        "m",
    )
    assert floor.problems == [
        f"artifacts: {UNDESCRIBED} (asked: Hands, faces, text?) → {PLACEHOLDER_FIX}"
    ]
    assert not floor.passed


def test_a_problem_line_is_cut_to_size_with_its_fix_kept_and_twenty_lines_at_most() -> None:
    payload = _checks("a" * 64)
    found = {"text": True, "anatomy": False, "details": False, "awkward": False}
    long_line = f"text: {'x' * 600} → {'y' * 300}"
    out = verdict(json.dumps({"faults": found, "problems": [long_line]}), payload, 7, "m")
    assert len(out.problems) == 1 and len(out.problems[0]) == MAX_PROBLEM_CHARS
    assert out.problems[0].startswith("text: xxx")
    assert out.problems[0].endswith(FIX_ARROW + "y" * MAX_FIX_CHARS), "the fix keeps its place"
    many = [f"text: fault {n} → fix {n}" for n in range(25)]
    out = verdict(json.dumps({"faults": found, "problems": many}), payload, 7, "m")
    assert len(out.problems) == MAX_PROBLEMS and out.problems[-1] == "text: fault 19 → fix 19"
    odd = verdict(json.dumps({"faults": found, "problems": "not a list"}), payload, 7, "m")
    assert len(odd.problems) == 1 and odd.problems[0].startswith(f"text: {UNDESCRIBED}")


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
            "scores": {"identity_jingwei": 8, "artifacts": 9 if len(seen) == 1 else 6},
            "problems": ["artifacts: a smear across the sky → a clear sky"],
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
        again = await judge(runtime, media, store, _payload(sha), 7, client)
    assert out.passed and out.overall == 8.33
    assert out.problems == [], "a remark on a criterion over the bar is not a problem"
    assert again.passed and again.overall == 7.33
    assert again.problems == ["artifacts: a smear across the sky → a clear sky"]
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
