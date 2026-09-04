import json
from pathlib import Path

import httpx
import pytest

from app.ai.gemini import GeminiStructuredProvider
from app.hotspots.candidate_cli import load_candidates
from app.hotspots.candidate_generation import (
    CANDIDATE_RESPONSE_SCHEMA,
    GeneratedCandidate,
    build_candidate_file,
    clean_rows,
    generate_candidates,
)
from app.hotspots.cities import CITY_BY_CODE


def reply(rows: list[dict[str, str]], **extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": json.dumps({"candidates": rows}, ensure_ascii=False)}]
                },
                "finishReason": "STOP",
            }
        ],
        "usageMetadata": {"promptTokenCount": 12, "candidatesTokenCount": 34},
    }
    body.update(extra)
    return body


def transport(bodies: list[object], calls: list[httpx.Request]) -> httpx.MockTransport:
    queue = list(bodies)

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json=queue.pop(0))

    return httpx.MockTransport(handler)


def provider(bodies: list[object], calls: list[httpx.Request]) -> GeminiStructuredProvider:
    return GeminiStructuredProvider(
        "gemini-key",
        "https://generativelanguage.googleapis.com",
        "gemini-3.5-flash",
        30.0,
        16_000,
        httpx.AsyncClient(transport=transport(bodies, calls)),
    )


@pytest.mark.asyncio
async def test_the_request_carries_the_key_in_a_header_and_asks_for_schema_bound_json() -> None:
    calls: list[httpx.Request] = []
    client = provider([reply([{"name": "清水寺", "district": "京都市東山區"}])], calls)

    document, usage, _ = await build_candidate_file(
        client, CITY_BY_CODE["KIX"], count=10, avoid=[]
    )
    await client.close()

    assert document == {
        "city_code": "KIX",
        "candidates": [{"name": "清水寺", "district": "京都市東山區"}],
    }
    assert usage["input_tokens"] == 12 and usage["output_tokens"] == 34
    request = calls[0]
    assert request.headers["x-goog-api-key"] == "gemini-key"
    assert request.url.path.endswith("/v1beta/models/gemini-3.5-flash:generateContent")
    sent = json.loads(request.read())
    # Ungrounded call, so a schema is allowed and no search tool may be attached.
    assert "tools" not in sent
    assert sent["generationConfig"]["responseMimeType"] == "application/json"
    assert sent["generationConfig"]["responseSchema"] == CANDIDATE_RESPONSE_SCHEMA
    payload = json.loads(sent["contents"][0]["parts"][0]["text"])
    assert payload["city_code"] == "KIX" and payload["count"] == 10
    assert payload["coverage"] and "radius_km" in payload["coverage"][0]


@pytest.mark.asyncio
async def test_a_fenced_reply_still_parses() -> None:
    calls: list[httpx.Request] = []
    fenced = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "```json\n"
                            + json.dumps(
                                {"candidates": [{"name": "金閣寺", "district": "京都市北區"}]}
                            )
                            + "\n```"
                        }
                    ]
                },
                "finishReason": "STOP",
            }
        ]
    }
    client = provider([fenced], calls)

    document, _, _ = await build_candidate_file(client, CITY_BY_CODE["KIX"], count=5, avoid=[])
    await client.close()

    assert [row["name"] for row in document["candidates"]] == ["金閣寺"]


@pytest.mark.asyncio
async def test_an_invalid_reply_is_repaired_on_the_second_attempt() -> None:
    calls: list[httpx.Request] = []
    broken = {
        "candidates": [
            {
                "content": {"parts": [{"text": '{"candidates": "not-a-list"}'}]},
                "finishReason": "STOP",
            }
        ]
    }
    client = provider([broken, reply([{"name": "二條城", "district": "京都市中京區"}])], calls)

    document, _, _ = await build_candidate_file(client, CITY_BY_CODE["KIX"], count=5, avoid=[])
    await client.close()

    assert len(calls) == 2
    second = json.loads(calls[1].read())["contents"][0]["parts"][0]["text"]
    assert "Repair the previous invalid JSON" in second
    assert [row["name"] for row in document["candidates"]] == ["二條城"]


@pytest.mark.asyncio
async def test_a_truncated_reply_is_refused() -> None:
    calls: list[httpx.Request] = []
    truncated = {
        "candidates": [
            {"content": {"parts": [{"text": '{"candidates": ['}]}, "finishReason": "MAX_TOKENS"}
        ]
    }
    client = provider([truncated], calls)

    with pytest.raises(ValueError, match="未完成"):
        await build_candidate_file(client, CITY_BY_CODE["KIX"], count=5, avoid=[])
    await client.close()


@pytest.mark.asyncio
async def test_a_blocked_reply_is_refused() -> None:
    calls: list[httpx.Request] = []
    client = provider([{"promptFeedback": {"blockReason": "SAFETY"}}], calls)

    with pytest.raises(ValueError, match="拒絕回應"):
        await build_candidate_file(client, CITY_BY_CODE["KIX"], count=5, avoid=[])
    await client.close()


def test_duplicate_and_unusable_names_never_reach_the_file() -> None:
    rows = [
        GeneratedCandidate(name="清水寺", district="京都市東山區"),
        GeneratedCandidate(name="清 水 寺", district="京都市東山區"),
        GeneratedCandidate(name="", district="京都市北區"),
        GeneratedCandidate(name="https://example.com/kyoto", district="京都市北區"),
        GeneratedCandidate(name="金閣寺", district="京都市北區"),
    ]

    kept, dropped = clean_rows(rows, CITY_BY_CODE["KIX"], avoid=["金閣寺"], count=10)

    assert [row["name"] for row in kept] == ["清水寺"]
    assert dropped["duplicate"] == 1
    assert dropped["empty_name"] == 1
    assert dropped["url_in_name"] == 1
    assert dropped["avoided"] == 1


def test_an_uncertain_district_is_blanked_rather_than_guessed() -> None:
    rows = [
        GeneratedCandidate(name="通天閣", district="不確定"),
        GeneratedCandidate(name="海遊館", district="N/A"),
        GeneratedCandidate(name="道頓堀", district="道頓堀"),
        GeneratedCandidate(name="黑門市場", district="大阪／京都"),
        GeneratedCandidate(name="住吉大社", district="大阪市住吉區"),
    ]

    kept, _ = clean_rows(rows, CITY_BY_CODE["KIX"], avoid=[], count=10)

    assert [row["district"] for row in kept] == ["", "", "", "", "大阪市住吉區"]
    assert len(kept) == 5


def test_the_response_schema_omits_keywords_gemini_rejects() -> None:
    # maxItems makes the API answer a bare 400 INVALID_ARGUMENT, so the cap lives in the
    # validator instead. Verified against the live API on 2026-09-04.
    array = CANDIDATE_RESPONSE_SCHEMA["properties"]["candidates"]
    assert "maxItems" not in array
    assert set(array["items"]) == {"type", "properties", "required", "propertyOrdering"}


def test_over_count_rows_are_trimmed_and_counted() -> None:
    rows = [GeneratedCandidate(name=f"景點{index}") for index in range(5)]

    kept, dropped = clean_rows(rows, CITY_BY_CODE["KIX"], avoid=[], count=3)

    assert len(kept) == 3
    assert dropped["over_count"] == 2


@pytest.mark.asyncio
async def test_the_written_file_is_what_load_candidates_reads(tmp_path: Path) -> None:
    calls: list[httpx.Request] = []
    body = reply([{"name": "清水寺", "district": "京都市東山區"}])
    target = tmp_path / "KIX.json"

    client = provider([body], calls)
    document, _, _ = await build_candidate_file(client, CITY_BY_CODE["KIX"], count=5, avoid=[])
    await client.close()
    target.write_text(json.dumps(document, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    city_code, candidates = load_candidates(target)

    assert city_code == "KIX"
    assert candidates[0].name == "清水寺"
    assert candidates[0].city_qualifier == "京都市東山區 大阪／京都"


@pytest.mark.asyncio
async def test_an_unknown_city_code_is_refused_before_any_call() -> None:
    with pytest.raises(SystemExit, match="unknown city_code"):
        await generate_candidates(
            city_code="zzz",
            count=None,
            out=None,
            model=None,
            dry_run=True,
            force=False,
            avoid_files=[],
        )


@pytest.mark.asyncio
async def test_an_existing_file_is_not_overwritten_without_force(tmp_path: Path) -> None:
    target = tmp_path / "KIX.json"
    target.write_text("keep me", encoding="utf-8")

    with pytest.raises(SystemExit, match="--force"):
        await generate_candidates(
            city_code="KIX",
            count=None,
            out=target,
            model=None,
            dry_run=False,
            force=False,
            avoid_files=[],
        )

    assert target.read_text(encoding="utf-8") == "keep me"
