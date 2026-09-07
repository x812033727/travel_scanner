from __future__ import annotations

import asyncio
import hashlib
import json
from typing import Any
from uuid import uuid4

import httpx
import pytest
from pydantic import ValidationError

from app.catalog_review import evidence
from app.catalog_review import provider as provider_module
from app.catalog_review.errors import CatalogAssessmentError, safe_error_diagnostics
from app.catalog_review.evidence import fetch_sources, is_trusted_source, normalize_source_url
from app.catalog_review.provider import CatalogGeminiProvider
from app.catalog_review.schemas import EvidenceCitation, EvidenceSource, ReviewCandidate
from app.catalog_review.service import allowed_actions, record_assessment
from app.config import Settings
from app.i18n import LOCALES
from app.models import CatalogReviewItem
from app.problems import AppError

OFFICIAL = "https://tourism.example/place"
WIKIDATA = "https://www.wikidata.org/wiki/Q1"


async def public_resolver(host: str) -> list[str]:
    return ["93.184.216.34"]


async def reserve() -> bool:
    return True


def settings() -> Settings:
    return Settings(_env_file=None, hotspot_guide_gemini_api_key="mock-test-key")


def source(url: str = OFFICIAL, text: str = "The official museum is in Tokyo.") -> EvidenceSource:
    return EvidenceSource(
        url=url,
        text=text,
        fingerprint=hashlib.sha256(text.encode()).hexdigest(),
        trusted=True,
        fetched=True,
    )


def candidate(**updates: Any) -> ReviewCandidate:
    return ReviewCandidate.model_validate(
        {
            "candidate_id": "row-1",
            "kind": "hotspot",
            "name": "Museum",
            "local_name": "美術館",
            "destination_id": "tokyo",
            "sources": [source()],
            **updates,
        }
    )


def assessment(**updates: Any) -> dict[str, Any]:
    return {
        "candidate_id": "row-1",
        "decision": "approve",
        "confidence": 0.95,
        "reason": "來源支持此地點。",
        "corrections": {},
        "evidence": [{"url": OFFICIAL, "quote": "official museum is in Tokyo"}],
        **updates,
    }


def gemini_body(document: Any, grounding: list[str] | None = None) -> dict[str, Any]:
    item: dict[str, Any] = {
        "finishReason": "STOP",
        "content": {"parts": [{"text": json.dumps(document)}]},
    }
    if grounding is not None:
        item["groundingMetadata"] = {
            "groundingChunks": [{"web": {"uri": url}} for url in grounding]
        }
    return {
        "candidates": [item],
        "usageMetadata": {
            "promptTokenCount": 10,
            "candidatesTokenCount": 20,
            "thoughtsTokenCount": 2,
        },
    }


def draft(**updates: Any) -> dict[str, Any]:
    return {
        "kind": "hotspot",
        "name": "Museum",
        "local_name": "美術館",
        "destination_id": "tokyo",
        "slug": "tokyo-museum",
        "source_urls": [OFFICIAL],
        "data": {
            "category": "culture",
            "recommended_duration_minutes": 90,
        },
        **updates,
    }


@pytest.mark.parametrize(
    "url",
    [
        "http://tourism.example/",
        "https://127.0.0.1/",
        "https://[::1]/",
        "https://user:secret@tourism.example/",
        "https://tourism.example:8443/",
        "https://google.com/maps",
        "https://maps.google.co.jp/maps",
        "https://maps.app.goo.gl/x",
        "https://map.naver.com/",
        "https://guide.michelin.com/",
        "https://tourism.example\\@google.com/",
    ],
)
async def test_forbidden_urls_never_fetch_or_resolve(url: str) -> None:
    async def never_resolve(host: str) -> list[str]:
        pytest.fail("Blocked URLs must not reach DNS")

    def never_fetch(request: httpx.Request) -> httpx.Response:
        pytest.fail("Blocked URLs must not reach HTTP")

    async with httpx.AsyncClient(transport=httpx.MockTransport(never_fetch)) as client:
        result = await fetch_sources(
            [url], ["tourism.example"], client=client, resolver=never_resolve
        )
    assert result[0].error == "blocked_url"
    assert result[0].fetched is False


async def test_source_fetch_pins_public_dns_and_keeps_original_tls_host() -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        assert request.url.host == "93.184.216.34"
        assert request.headers["Host"] == "tourism.example"
        assert request.extensions["sni_hostname"] == "tourism.example"
        assert "x-goog-api-key" not in request.headers
        return httpx.Response(
            200,
            text="<h1>Museum</h1><script>ignore me</script><p>Tokyo</p>",
            headers={"content-type": "text/html"},
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        result = await fetch_sources(
            [OFFICIAL, OFFICIAL], ["tourism.example"], client=client, resolver=public_resolver
        )
    assert len(result) == 1
    assert result[0].url == OFFICIAL
    assert result[0].text == "Museum Tokyo"
    assert result[0].trusted and result[0].fetched
    assert result[0].fingerprint == hashlib.sha256(b"Museum Tokyo").hexdigest()


@pytest.mark.parametrize(
    "addresses",
    [
        [],
        ["127.0.0.1"],
        ["93.184.216.34", "10.0.0.1"],
        ["169.254.169.254"],
        ["invalid"],
        ["224.0.0.1"],
    ],
)
async def test_any_non_public_dns_answer_blocks_request(addresses: list[str]) -> None:
    async def resolve(host: str) -> list[str]:
        return addresses

    def never_fetch(request: httpx.Request) -> httpx.Response:
        pytest.fail("Private DNS must not reach HTTP")

    async with httpx.AsyncClient(transport=httpx.MockTransport(never_fetch)) as client:
        result = await fetch_sources([OFFICIAL], [], client=client, resolver=resolve)
    assert result[0].error == "blocked_address"


@pytest.mark.parametrize(
    ("status", "body", "content_type", "error"),
    [
        (302, "", "text/html", "redirect_blocked"),
        (503, "", "text/html", "http_503"),
        (200, "picture", "image/png", "unsupported_content"),
        (200, "<script>hidden</script>", "text/html", "empty_content"),
        (200, "x" * 200_001, "text/plain", "response_too_large"),
    ],
    ids=["redirect", "unavailable", "image", "empty", "oversized"],
)
async def test_source_errors_are_typed_and_isolated(
    status: int,
    body: str,
    content_type: str,
    error: str,
) -> None:
    requests = 0

    def respond(request: httpx.Request) -> httpx.Response:
        nonlocal requests
        requests += 1
        if request.url.path == "/ok":
            return httpx.Response(
                200, text="Healthy source", headers={"content-type": "text/plain"}
            )
        return httpx.Response(
            status,
            text=body,
            headers={
                "content-type": content_type,
                "location": "https://127.0.0.1/secret",
            },
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(respond), follow_redirects=True
    ) as client:
        result = await fetch_sources(
            [OFFICIAL, "https://tourism.example/ok"], [], client=client, resolver=public_resolver
        )
    assert requests == 2
    assert result[0].error == error and not result[0].fetched
    assert result[1].fetched and not result[1].trusted


async def test_source_parallelism_is_three_and_whole_request_timeout_is_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    running = maximum = 0

    async def respond(request: httpx.Request) -> httpx.Response:
        nonlocal running, maximum
        running += 1
        maximum = max(maximum, running)
        try:
            await asyncio.sleep(0.01)
            return httpx.Response(200, text="Source", headers={"content-type": "text/plain"})
        finally:
            running -= 1

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        result = await fetch_sources(
            [f"https://tourism.example/{i}" for i in range(7)],
            [],
            client=client,
            resolver=public_resolver,
        )
        assert maximum == 3 and all(item.fetched for item in result)
        monkeypatch.setattr(evidence, "TOTAL_SECONDS", 0.001)
        timeout = await fetch_sources([OFFICIAL], [], client=client, resolver=public_resolver)
    assert timeout[0].error == "timeout"


def test_authority_is_explicit_host_registry_not_llm_claim_or_suffix_guessing() -> None:
    assert is_trusted_source(OFFICIAL, ["tourism.example"])
    assert is_trusted_source("https://www.tourism.example/place", ["tourism.example"])
    assert is_trusted_source(WIKIDATA, [])
    assert not is_trusted_source("https://evil.tourism.example/", ["tourism.example"])
    assert not is_trusted_source("https://tourism.example.evil.com/", ["tourism.example"])
    assert not is_trusted_source("https://official-looking.gov/", [])
    assert normalize_source_url("https://TOURISM.EXAMPLE:443/place#top") == OFFICIAL


async def test_assessment_uses_structured_schema_and_preserves_server_evidence() -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert "tools" not in body
        assert body["generationConfig"]["responseMimeType"] == "application/json"
        assert body["generationConfig"]["responseSchema"]["properties"]["items"]
        return httpx.Response(
            200,
            json=gemini_body(
                {
                    "items": [
                        assessment(
                            corrections={
                                "name": "Exact Museum",
                                "latitude": 1,
                                "longitude": 2,
                                "google_place_id": "madeup",
                                "map_match_status": "verified",
                                "is_active": True,
                                "review_status": "approved",
                                "coordinate_source": "official",
                                "wikidata_id": "Qmadeup",
                            }
                        )
                    ]
                }
            ),
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        result = await provider.assess([candidate()])
        assert provider.call_count == 1
        assert provider.usage == {"input_tokens": 10, "output_tokens": 20, "thought_tokens": 2}
    assert result.items[0].decision == "approve"
    assert result.items[0].corrections == {"name": "Exact Museum"}
    assert result.items[0].evidence[0].url == OFFICIAL


@pytest.mark.parametrize(
    "variation",
    [
        "not_fetched",
        "untrusted",
        "fake_fingerprint",
        "missing_sources",
        "invented_url",
        "invented_quote",
    ],
)
@pytest.mark.parametrize("decision", ["approve", "reject"])
async def test_unsupported_positive_and_negative_decisions_stay_pending(
    variation: str,
    decision: str,
) -> None:
    record = candidate()
    result_item = assessment(decision=decision)
    if variation == "not_fetched":
        record.sources[0].fetched = False
    elif variation == "untrusted":
        record.sources[0].url = "https://unknown.example/place"
        result_item["evidence"][0]["url"] = record.sources[0].url
    elif variation == "fake_fingerprint":
        record.sources[0].fingerprint = "fake"
    elif variation == "missing_sources":
        record.sources = []
    elif variation == "invented_url":
        result_item["evidence"][0]["url"] = "https://tourism.example/not-fetched"
    else:
        result_item["evidence"][0]["quote"] = "This museum is permanently closed"
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json=gemini_body({"items": [result_item]})),
        )
    ) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        result = await provider.assess([record])
    assert result.items[0].decision == "needs_review"


@pytest.mark.parametrize(
    "items", [[assessment(candidate_id="madeup")], [assessment(), assessment()]]
)
async def test_unknown_or_duplicate_model_ids_invalidate_the_batch(
    items: list[dict[str, Any]],
) -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json=gemini_body({"items": items})),
        )
    ) as client:
        provider = CatalogGeminiProvider(settings(), reserve, client=client)
        with pytest.raises(CatalogAssessmentError, match="catalog_response_ids_invalid"):
            await provider.assess([candidate()])
        assert provider.call_count == 1


@pytest.mark.parametrize("document", [{"items": []}, {"items": [assessment()]}, {}])
async def test_missing_model_ids_fail_closed_without_synthetic_assessment_or_paid_repair(
    document: dict[str, Any],
) -> None:
    reservations = 0

    async def counted_reserve() -> bool:
        nonlocal reservations
        reservations += 1
        return True

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json=gemini_body(document)),
        )
    ) as client:
        provider = CatalogGeminiProvider(settings(), counted_reserve, client=client)
        with pytest.raises(CatalogAssessmentError, match="catalog_response_ids_invalid") as caught:
            await provider.assess([candidate(), candidate(candidate_id="row-2")])
        assert caught.value.details == {"candidate_count": 2}
        assert provider.call_count == reservations == 1
        assert provider.usage == {"input_tokens": 10, "output_tokens": 20, "thought_tokens": 2}


async def test_complete_model_ids_preserve_input_order_without_synthetic_assessments() -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                json=gemini_body(
                    {
                        "items": [
                            assessment(candidate_id="row-2"),
                            assessment(reason="真實模型判斷。"),
                        ]
                    }
                ),
            ),
        )
    ) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        result = await provider.assess([candidate(), candidate(candidate_id="row-2")])
        assert [item.candidate_id for item in result.items] == ["row-1", "row-2"]
        assert all(item.decision == "approve" for item in result.items)
        assert result.items[0].reason == "真實模型判斷。"
        assert provider.call_count == 1


async def test_input_batch_is_bounded_without_any_provider_call() -> None:
    def never_request(request: httpx.Request) -> httpx.Response:
        pytest.fail("Invalid or empty input batches must not call Gemini")

    async with httpx.AsyncClient(transport=httpx.MockTransport(never_request)) as client:
        provider = CatalogGeminiProvider(settings(), reserve, client=client)
        with pytest.raises(ValueError, match="At most 20"):
            await provider.assess([candidate(candidate_id=str(i)) for i in range(21)])
        with pytest.raises(ValueError, match="Duplicate input"):
            await provider.assess([candidate(), candidate()])
        assert (await provider.assess([])).items == []
        assert provider.call_count == 0


async def test_every_structured_repair_reserves_before_http() -> None:
    calls: list[str] = []

    async def reserve_counted() -> bool:
        calls.append("reserve")
        return True

    def respond(request: httpx.Request) -> httpx.Response:
        calls.append("http")
        value = {"items": [{"wrong": "schema"}]} if len(calls) == 2 else {"items": [assessment()]}
        return httpx.Response(200, json=gemini_body(value))

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve_counted, client=client, trusted_hosts=["tourism.example"]
        )
        assert (await provider.assess([candidate()])).items[0].decision == "approve"
        assert provider.call_count == 2 and provider.usage["input_tokens"] == 20
    assert calls == ["reserve", "http", "reserve", "http"]


async def test_budget_denial_prevents_request_including_repair() -> None:
    reservations = requests = 0

    async def reserve_counted() -> bool:
        nonlocal reservations
        reservations += 1
        return reservations == 1

    def respond(request: httpx.Request) -> httpx.Response:
        nonlocal requests
        requests += 1
        return httpx.Response(200, json=gemini_body({"items": [{"wrong": "schema"}]}))

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(settings(), reserve_counted, client=client)
        with pytest.raises(AppError) as exc:
            await provider.assess([candidate()])
        assert exc.value.status == 429
        assert requests == 1 and reservations == 2 and provider.call_count == 1


async def test_discovery_is_grounded_without_response_schema_and_removes_authority_fields() -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body["tools"] == [{"google_search": {}}]
        assert "responseSchema" not in body["generationConfig"]
        assert "responseMimeType" not in body["generationConfig"]
        return httpx.Response(
            200,
            json=gemini_body(
                {
                    "items": [
                        draft(
                            data={
                                "category": "culture",
                                "latitude": 1,
                                "longitude": 2,
                                "google_place_id": "fake",
                                "is_active": True,
                                "review_status": "approved",
                                "source_type": "official",
                            }
                        )
                    ]
                },
                [OFFICIAL],
            ),
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        result = await provider.discover("hotspot", 5, [{"id": "tokyo"}], [])
    assert len(result.items) == 1
    assert result.items[0].data == {"category": "culture"}
    assert result.items[0].source_urls == [OFFICIAL]


@pytest.mark.parametrize(
    ("draft_updates", "grounding", "avoid"),
    [
        ({}, [], []),
        ({"source_urls": ["https://tourism.example/invented"]}, [OFFICIAL], []),
        ({"source_urls": ["https://unknown.example/place"]}, ["https://unknown.example/place"], []),
        ({"destination_id": "not-allowed"}, [OFFICIAL], []),
        ({"kind": "merchant"}, [OFFICIAL], []),
        ({}, [OFFICIAL], ["museum"]),
    ],
)
async def test_discovery_never_accepts_invented_sources_destinations_or_existing_records(
    draft_updates: dict[str, Any],
    grounding: list[str],
    avoid: list[str],
) -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                json=gemini_body({"items": [draft(**draft_updates)]}, grounding),
            )
        )
    ) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        result = await provider.discover("hotspot", 1, [{"destination_id": "tokyo"}], avoid)
    assert result.items == []


async def test_discovery_repairs_once_and_reserves_each_attempt() -> None:
    calls = 0

    async def reserve_counted() -> bool:
        nonlocal calls
        calls += 1
        return True

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                json=gemini_body({"items": [{"invalid": "data"}]}),
            )
        )
    ) as client:
        provider = CatalogGeminiProvider(settings(), reserve_counted, client=client)
        with pytest.raises(CatalogAssessmentError, match="catalog_response_invalid"):
            await provider.discover("hotspot", 1, [{"id": "tokyo"}], [])
        assert calls == 2
        with pytest.raises(ValueError, match="one and five"):
            await provider.discover("hotspot", 6, [{"id": "tokyo"}], [])
        with pytest.raises(ValueError, match="destination allowlist"):
            await provider.discover("hotspot", 1, [], [])
        assert calls == 2


@pytest.mark.parametrize("missing_locale", [False, True])
async def test_food_drafts_require_exactly_five_locale_names_and_original_summaries(
    missing_locale: bool,
) -> None:
    localizations = [
        {"locale": locale, "name": "Dish", "summary": "Original summary"}
        for locale in ("en", "ja", "ko", "zh-TW", "zh-CN")
    ]
    if missing_locale:
        localizations.pop()
    item = draft(kind="food", data={"localizations": localizations, "food_kind": "main"})
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                json=gemini_body({"items": [item]}, [OFFICIAL]),
            )
        )
    ) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        result = await provider.discover("food", 1, [{"id": "tokyo"}], [])
    assert len(result.items) == (0 if missing_locale else 1)


def test_short_evidence_quotes_and_missing_key_gate() -> None:
    with pytest.raises(ValidationError):
        EvidenceCitation(url=OFFICIAL, quote="x" * 301)
    with pytest.raises(AppError) as exc:
        CatalogGeminiProvider(Settings(_env_file=None, hotspot_guide_gemini_api_key=None), reserve)
    assert exc.value.code == "catalog_review_unconfigured"


async def test_full_twenty_candidate_batch_is_preserved_in_input_order() -> None:
    records = [candidate(candidate_id=f"row-{i}") for i in range(20)]
    results = [assessment(candidate_id=item.candidate_id) for item in reversed(records)]
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                json=gemini_body({"items": results}),
            )
        )
    ) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        result = await provider.assess(records)
    assert [item.candidate_id for item in result.items] == [item.candidate_id for item in records]
    assert all(item.decision == "approve" for item in result.items)


async def test_failed_http_still_consumes_its_reserved_call() -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(503, text="provider unavailable"),
        )
    ) as client:
        provider = CatalogGeminiProvider(settings(), reserve, client=client)
        with pytest.raises(CatalogAssessmentError, match="catalog_provider_unavailable"):
            await provider.assess([candidate()])
        assert provider.call_count == 1 and provider.usage["input_tokens"] == 0


async def test_initial_budget_denial_never_makes_http_request() -> None:
    async def deny() -> bool:
        return False

    def never_fetch(request: httpx.Request) -> httpx.Response:
        pytest.fail("Budget denial must stop before HTTP")

    async with httpx.AsyncClient(transport=httpx.MockTransport(never_fetch)) as client:
        provider = CatalogGeminiProvider(settings(), deny, client=client)
        with pytest.raises(AppError):
            await provider.discover("merchant", 1, [{"id": "tokyo"}], [])
        assert provider.call_count == 0


@pytest.mark.parametrize(
    "target", [OFFICIAL, "https://127.0.0.1/internal", "https://google.com/maps"]
)
async def test_only_known_grounding_redirect_is_resolved_without_following_publisher(
    target: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redirect = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/verified-token"
    requested: list[str] = []

    async def pin(url: str) -> tuple[httpx.URL, str]:
        assert url == redirect
        return httpx.URL(url).copy_with(host="93.184.216.34"), "vertexaisearch.cloud.google.com"

    def respond(request: httpx.Request) -> httpx.Response:
        requested.append(request.method)
        if request.method == "GET":
            assert request.headers["Host"] == "vertexaisearch.cloud.google.com"
            assert "x-goog-api-key" not in request.headers
            assert request.extensions["sni_hostname"] == "vertexaisearch.cloud.google.com"
            return httpx.Response(302, headers={"location": target})
        return httpx.Response(200, json=gemini_body({"items": [draft()]}, [redirect]))

    monkeypatch.setattr(provider_module, "public_request_target", pin)
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(respond), follow_redirects=True
    ) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        result = await provider.discover("hotspot", 1, [{"id": "tokyo"}], [])
        assert provider.call_count == 1
    assert requested == ["POST", "GET"]
    assert len(result.items) == (1 if target == OFFICIAL else 0)


async def test_discovery_honors_requested_count_and_deduplicates_within_batch() -> None:
    batch = [draft(), draft(), draft(name="Park", local_name="公園", slug="tokyo-park")]
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                json=gemini_body({"items": batch}, [OFFICIAL]),
            )
        )
    ) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        result = await provider.discover("hotspot", 5, [{"id": "tokyo"}], [])
        assert len(result.items) == 2
        limited = await provider.discover("hotspot", 1, [{"id": "tokyo"}], [])
        assert len(limited.items) == 1


async def test_discovery_prompt_bounds_destinations_and_avoid_list() -> None:
    observed: dict[str, Any] = {}

    def respond(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        observed.update(json.loads(body["contents"][0]["parts"][0]["text"]))
        return httpx.Response(200, json=gemini_body({"items": []}))

    avoid = [f"existing-record-{index}-" + "x" * 80 for index in range(1000)]
    destinations = [{"id": f"destination-{index}"} for index in range(6)]
    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(settings(), reserve, client=client)
        await provider.discover("hotspot", 1, destinations, avoid)
    assert observed["destinations"] == destinations
    assert len(observed["avoid_names_and_slugs"]) < len(avoid)
    assert len(json.dumps(observed["avoid_names_and_slugs"], ensure_ascii=False)) <= 8000


async def test_discovery_rejects_unbounded_destination_context() -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: pytest.fail("must not call provider"))
    ) as client:
        provider = CatalogGeminiProvider(settings(), reserve, client=client)
        with pytest.raises(ValueError, match="at most six destinations"):
            await provider.discover(
                "hotspot",
                1,
                [{"id": f"destination-{index}"} for index in range(7)],
                [],
            )


async def test_source_batch_is_bounded_before_any_network_request() -> None:
    with pytest.raises(ValueError, match="At most 100"):
        await fetch_sources([OFFICIAL] * 101, [])


async def test_wikidata_uses_fixed_bounded_entity_api_and_retains_canonical_evidence_url() -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        assert request.headers["Host"] == "www.wikidata.org"
        assert request.extensions["sni_hostname"] == "www.wikidata.org"
        assert request.url.path == "/w/api.php"
        assert request.url.params["action"] == "wbgetentities"
        assert request.url.params["ids"] == "Q1"
        assert request.url.params["props"] == "labels|descriptions|aliases|claims|sitelinks"
        assert request.url.params["sitefilter"] == "enwiki|zhwiki|jawiki|kowiki|thwiki|viwiki"
        return httpx.Response(
            200,
            json={
                "entities": {
                    "Q1": {
                        "id": "Q1",
                        "lastrevid": 123,
                        "labels": {"en": {"value": "Exact Museum"}, "ja": {"value": "美術館"}},
                        "descriptions": {"en": {"value": "A museum in Tokyo"}},
                        "aliases": {"en": [{"value": "Museum alias"}]},
                        "claims": {
                            "P31": [
                                {
                                    "mainsnak": {
                                        "datavalue": {
                                            "value": {
                                                "entity-type": "item",
                                                "id": "Q33506",
                                            }
                                        }
                                    }
                                }
                            ],
                            "P625": [
                                {
                                    "mainsnak": {
                                        "datavalue": {
                                            "value": {
                                                "latitude": 35.7,
                                                "longitude": 139.8,
                                            }
                                        }
                                    }
                                }
                            ],
                            "P18": [
                                {"mainsnak": {"datavalue": {"value": "Do not collect this photo"}}}
                            ],
                        },
                        "sitelinks": {"enwiki": {"title": "Exact Museum"}},
                    }
                }
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        rows = await fetch_sources([WIKIDATA], [], client=client, resolver=public_resolver)
    item = rows[0]
    assert item.url == WIKIDATA and item.fetched and item.trusted and item.error is None
    assert "Exact Museum" in item.text and "Museum alias" in item.text
    assert 'P31 (instance of): "Q33506"' in item.text
    assert "source claim, not map verification" in item.text
    assert "35.7" in item.text and "139.8" in item.text
    assert "Do not collect this photo" not in item.text
    assert item.fingerprint == hashlib.sha256(item.text.encode()).hexdigest()


@pytest.mark.parametrize(
    "body",
    [
        {"entities": {"Q1": {"id": "Q2", "labels": {"en": {"value": "Wrong identity"}}}}},
        {"entities": {"Q1": {"id": "Q1", "missing": ""}}},
        {"entities": {"Q1": {"id": "Q1", "labels": {}}}},
        {"error": {"code": "maxlag"}},
        {"entities": {"Q2": {"id": "Q2"}}},
    ],
)
async def test_wikidata_missing_redirected_or_mismatched_entity_is_not_evidence(
    body: dict[str, Any],
) -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json=body),
        )
    ) as client:
        rows = await fetch_sources([WIKIDATA], [], client=client, resolver=public_resolver)
    assert rows[0].error == "invalid_wikidata_entity"
    assert rows[0].text == "" and rows[0].fetched is False


@pytest.mark.parametrize(
    "url",
    [
        "https://www.wikidata.org/wiki/Q1?other=1",
        "https://www.wikidata.org/wiki/Property:P1",
        "https://www.wikidata.org/wiki/Q0",
        "https://wikidata.org.evil.example/wiki/Q1",
    ],
)
async def test_wikidata_adapter_never_transforms_noncanonical_or_lookalike_urls(url: str) -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        assert request.url.path != "/w/api.php"
        return httpx.Response(200, text="Some public page", headers={"content-type": "text/plain"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        await fetch_sources([url], [], client=client, resolver=public_resolver)


async def test_outbound_context_retains_facts_without_private_actor_metadata() -> None:
    sensitive = "PRIVATE_ACTOR_OR_INTERNAL_NOTE_MUST_NOT_LEAVE_SERVER"
    record = candidate(
        data={
            "reviewed_by_user_id": sensitive,
            "map_verified_by_user_id": sensitive,
            "verified_by_user_id": sensitive,
            "id": sensitive,
            "private_notes": sensitive,
            "latitude": "35.7",
            "longitude": "139.8",
            "country_code": "JP",
            "map_match_status": "verified",
            "google_place_id": "exact-public-place-id",
            "metadata_json": {
                "local_name": "美術館",
                "reviewer_email": sensitive,
                "aliases": ["Museum alias", {"actor": sensitive}],
            },
            "sources": [
                {
                    "id": sensitive,
                    "merchant_id": sensitive,
                    "actor_id": sensitive,
                    "source_url": OFFICIAL,
                    "source_scope": "merchant_website",
                    "claims_json": ["display_name", {"actor": sensitive}],
                }
            ],
            "localizations": [
                {
                    "locale": "en",
                    "name": "Museum",
                    "source": "admin",
                    "author_user_id": sensitive,
                    "id": sensitive,
                }
            ],
            "foods": [{"id": sensitive, "merchant_id": sensitive, "food_id": "public-dish-id"}],
        }
    )

    def respond(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        outgoing = body["contents"][0]["parts"][0]["text"]
        assert sensitive not in outgoing
        facts = json.loads(outgoing)["candidates"][0]["data"]
        assert facts["latitude"] == "35.7" and facts["map_match_status"] == "verified"
        assert facts["metadata"] == {"local_name": "美術館", "aliases": ["Museum alias"]}
        assert facts["foods"] == [{"food_id": "public-dish-id"}]
        assert facts["sources"][0]["source_url"] == OFFICIAL
        return httpx.Response(200, json=gemini_body({"items": [assessment()]}))

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        await provider.assess([record])
    assert record.data["reviewed_by_user_id"] == sensitive  # Local fingerprint input unchanged.


async def test_response_schema_uses_current_candidate_id_enum_and_explicit_constraints() -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        item_schema = payload["generationConfig"]["responseSchema"]["properties"]["items"]["items"]
        assert item_schema["properties"]["candidate_id"]["enum"] == ["row-1", "row-2"]
        assert "0 to 1" in item_schema["properties"]["confidence"]["description"]
        assert (
            "300 characters"
            in item_schema["properties"]["evidence"]["items"]["properties"]["quote"]["description"]
        )
        instruction = payload["system_instruction"]["parts"][0]["text"]
        assert "never 95" in instruction and "never null" in instruction
        return httpx.Response(
            200,
            json=gemini_body(
                {
                    "items": [
                        assessment(),
                        assessment(candidate_id="row-2"),
                    ]
                }
            ),
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        assert (
            len((await provider.assess([candidate(), candidate(candidate_id="row-2")])).items) == 2
        )


async def test_large_evidence_is_excerpted_without_changing_independent_validation_source() -> None:
    records = []
    for index in range(8):
        pages = [
            source(
                url=f"{OFFICIAL}/{index}/{page}",
                text=(
                    "Navigation menu unrelated text. " * 220
                    + "Museum exact identity and branch information. "
                    + "More data. " * 500
                )[:12_000],
            )
            for page in range(5)
        ]
        records.append(
            candidate(
                candidate_id=f"row-{index}",
                sources=pages,
                data={
                    "review_reason": "Long metadata " * 1000,
                    "localizations": [{"summary": "long text " * 1000}] * 50,
                },
            )
        )
    original_text = records[0].sources[0].text
    original_fingerprint = records[0].sources[0].fingerprint
    seen: list[dict[str, Any]] = []

    def respond(request: httpx.Request) -> httpx.Response:
        request_body = json.loads(request.content)
        outgoing = json.loads(request_body["contents"][0]["parts"][0]["text"])
        seen.extend(outgoing["candidates"])
        return httpx.Response(
            200,
            json=gemini_body(
                {
                    "items": [
                        assessment(
                            candidate_id=entry["candidate_id"],
                            evidence=[
                                {
                                    "url": entry["sources"][0]["url"],
                                    "quote": "Museum exact identity",
                                }
                            ],
                        )
                        for entry in outgoing["candidates"]
                    ]
                }
            ),
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        result = await provider.assess(records)
    assert all(item.decision == "needs_review" for item in result.items)
    assert all(item.evidence for item in result.items)  # Quotes still independently validate.
    for row in seen:
        assert row["review_context_complete"] is False
        assert "localizations" in row["review_context_truncated_fields"]
        assert sum(len(entry["text"]) for entry in row["sources"]) <= 4000
        assert all(len(entry["text"]) <= 1600 for entry in row["sources"])
        assert len(json.dumps(row["data"], ensure_ascii=False)) <= 3000
        assert "Museum exact identity" in row["sources"][0]["text"]
        assert row["sources"][0]["excerpt_only"]
    assert records[0].sources[0].text == original_text
    assert records[0].sources[0].fingerprint == original_fingerprint


@pytest.mark.parametrize("decision", ["approve", "reject"])
@pytest.mark.parametrize("long_content", [False, True])
async def test_five_locale_content_requires_complete_context_before_allowed_actions(
    decision: str, long_content: bool
) -> None:
    row_id = uuid4()
    quote = "Example dish is a traditional Japanese noodle dish."
    summary = "Valid content " * 60 if long_content else "An originally summarized noodle dish."
    snapshot = {
        "local_name": "Example dish",
        "country_code": "JP",
        "meal_types": ["lunch"],
        "source_urls": [OFFICIAL],
        "localizations": [
            {"locale": locale, "name": "Example dish", "summary": summary, "source": "admin"}
            for locale in LOCALES
        ],
        "destinations": [{"destination_id": "tokyo"}],
    }
    record = candidate(
        candidate_id=str(row_id), kind="food", data=snapshot, sources=[source(text=quote)]
    )

    def respond(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        outgoing = json.loads(body["contents"][0]["parts"][0]["text"])["candidates"][0]
        locales = outgoing["data"]["localizations"]
        assert {entry["locale"] for entry in locales} == set(LOCALES)
        assert len(locales) == 5
        assert all(entry["name"] == "Example dish" and entry["summary"] for entry in locales)
        assert outgoing["review_context_complete"] is not long_content
        assert outgoing["review_context_truncated_fields"] == (
            ["localizations"] if long_content else []
        )
        assert len(json.dumps(outgoing["data"], ensure_ascii=False)) <= 3000
        if not long_content:
            assert locales == snapshot["localizations"]
        return httpx.Response(
            200,
            json=gemini_body(
                {
                    "items": [
                        assessment(
                            candidate_id=str(row_id),
                            decision=decision,
                            evidence=[{"url": OFFICIAL, "quote": quote}],
                        )
                    ]
                }
            ),
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        result = (await provider.assess([record])).items[0]
    item = CatalogReviewItem(id=row_id, kind="food", snapshot_json=snapshot)
    record_assessment(item, result, record.sources)
    assert item.gaps_json == []  # No unrelated publication gap masks the regression.
    assert item.decision == ("needs_review" if long_content else decision)
    assert allowed_actions(item) == (
        ["keep_pending"] if long_content else [decision, "keep_pending"]
    )
    assert record.data["localizations"][0]["summary"] == summary  # Never truncate the DB snapshot.


@pytest.mark.parametrize(
    "data,changed",
    [
        ({"local_name": "a" * 701}, "local_name"),
        ({"meal_types": ["lunch"] * 101}, "meal_types"),
        ({"metadata_json": {"aliases": ["alias"] * 101}}, "metadata"),
        ({"destinations": [{"destination_id": "tokyo"}] * 101}, "destinations"),
    ],
)
async def test_any_context_truncation_is_explicit_and_cannot_be_rejected(
    data: dict[str, Any], changed: str
) -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        outgoing = json.loads(body["contents"][0]["parts"][0]["text"])["candidates"][0]
        assert outgoing["review_context_complete"] is False
        assert changed in outgoing["review_context_truncated_fields"]
        return httpx.Response(200, json=gemini_body({"items": [assessment(decision="reject")]}))

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        assert (await provider.assess([candidate(data=data)])).items[0].decision == "needs_review"


async def test_truncated_even_valid_partial_json_preserves_thought_usage_and_never_applies() -> (
    None
):
    body = gemini_body({"items": [assessment()]})
    body["candidates"][0]["finishReason"] = "MAX_TOKENS"
    body["usageMetadata"] = {
        "promptTokenCount": 10_000,
        "candidatesTokenCount": 50,
        "thoughtsTokenCount": 7950,
    }
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json=body),
        )
    ) as client:
        provider = CatalogGeminiProvider(
            settings().model_copy(
                update={
                    "hotspot_guide_ai_max_output_tokens": 8000,
                }
            ),
            reserve,
            client=client,
        )
        with pytest.raises(CatalogAssessmentError) as caught:
            await provider.assess([candidate()])
        assert provider.call_count == 1  # Never replay known truncation at the same cap.
        assert provider.usage["thought_tokens"] == 7950
    diagnostics = safe_error_diagnostics(caught.value)
    assert diagnostics["code"] == "catalog_response_truncated"
    assert diagnostics["details"]["finish_reason"] == "MAX_TOKENS"
    assert diagnostics["details"]["thought_tokens"] == 7950
    assert diagnostics["details"]["output_tokens"] == 50
    assert diagnostics["details"]["max_output_tokens"] == 8000


@pytest.mark.parametrize("feedback", [True, False])
async def test_refusal_is_typed_and_not_retried(feedback: bool) -> None:
    body = gemini_body({"items": []})
    if feedback:
        body["promptFeedback"] = {"blockReason": "sensitive-provider-text"}
    else:
        body["candidates"][0]["finishReason"] = "SAFETY"
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json=body),
        )
    ) as client:
        provider = CatalogGeminiProvider(settings(), reserve, client=client)
        with pytest.raises(CatalogAssessmentError) as caught:
            await provider.assess([candidate()])
        assert provider.call_count == 1
    assert caught.value.code == "catalog_response_blocked" and not caught.value.retryable
    assert "sensitive" not in json.dumps(safe_error_diagnostics(caught.value))


@pytest.mark.parametrize("body", [{"candidates": []}, {"candidates": [{"finishReason": "STOP"}]}])
async def test_empty_output_is_typed_after_one_bounded_repair(body: dict[str, Any]) -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json=body),
        )
    ) as client:
        provider = CatalogGeminiProvider(settings(), reserve, client=client)
        with pytest.raises(CatalogAssessmentError) as caught:
            await provider.assess([candidate()])
        assert provider.call_count == 2
    assert caught.value.code == "catalog_response_empty" and caught.value.details["attempt"] == 2


async def test_schema_repair_includes_safe_path_and_constraints_not_previous_response() -> None:
    calls = 0
    raw_secret = "RAW_PRIVATE_PROVIDER_TEXT_SHOULD_NOT_BE_PERSISTED_OR_REPLAYED"

    def respond(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(
                200,
                json=gemini_body(
                    {
                        "items": [
                            assessment(
                                confidence=95,
                                reason=raw_secret,
                            )
                        ]
                    }
                ),
            )
        prompt = json.loads(request.content)["contents"][0]["parts"][0]["text"]
        assert "items.0.confidence" in prompt and "less_than_equal" in prompt
        assert "confidence 0..1" in prompt and raw_secret not in prompt
        return httpx.Response(200, json=gemini_body({"items": [assessment()]}))

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        assert (await provider.assess([candidate()])).items[0].decision == "approve"
        assert provider.call_count == 2


@pytest.mark.parametrize(
    ("status", "code", "retryable"),
    [
        (400, "catalog_provider_unavailable", False),
        (401, "catalog_provider_unavailable", False),
        (429, "catalog_provider_rate_limited", True),
        (503, "catalog_provider_unavailable", True),
    ],
)
async def test_http_status_is_safe_and_never_inlines_provider_body_or_key(
    status: int,
    code: str,
    retryable: bool,
) -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                status,
                json={"error": {"message": "RAW_SECRET_PROVIDER_BODY mock-test-key"}},
            )
        )
    ) as client:
        provider = CatalogGeminiProvider(settings(), reserve, client=client)
        with pytest.raises(CatalogAssessmentError) as caught:
            await provider.assess([candidate()])
        assert provider.call_count == 1
    error = safe_error_diagnostics(caught.value)
    assert error["code"] == code and error["retryable"] == retryable
    assert error["details"]["http_status"] == status
    serialized = json.dumps(error)
    assert "RAW_SECRET" not in serialized and "mock-test-key" not in serialized
    assert "generativelanguage.googleapis.com" not in serialized


@pytest.mark.parametrize("network", [False, True])
async def test_timeout_and_network_error_are_typed_not_raw_exceptions(network: bool) -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        if network:
            raise httpx.ConnectError("raw-host-private", request=request)
        raise httpx.ReadTimeout("raw-key-private", request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
        provider = CatalogGeminiProvider(settings(), reserve, client=client)
        with pytest.raises(CatalogAssessmentError) as caught:
            await provider.assess([candidate()])
    assert caught.value.code == (
        "catalog_provider_unavailable" if network else "catalog_provider_timeout"
    )
    assert "private" not in json.dumps(safe_error_diagnostics(caught.value))


async def test_budget_and_lease_callback_exceptions_never_become_provider_errors() -> None:
    class SimulatedLeaseLost(Exception):
        pass

    async def lost() -> bool:
        raise SimulatedLeaseLost()

    def never_request(request: httpx.Request) -> httpx.Response:
        pytest.fail("Lost lease must not reach provider")

    async with httpx.AsyncClient(transport=httpx.MockTransport(never_request)) as client:
        provider = CatalogGeminiProvider(settings(), lost, client=client)
        with pytest.raises(SimulatedLeaseLost):
            await provider.assess([candidate()])
        assert provider.call_count == 0


def test_diagnostics_allowlist_drops_raw_content_unknown_path_and_legacy_guessing() -> None:
    error = CatalogAssessmentError(
        "catalog_response_invalid",
        details={
            "message": "SECRET",
            "response": "SECRET",
            "url": "https://secret.example",
            "http_status": 400,
            "validation_path": "items.0.SECRET.quote",
            "validation_type": "string_too_long",
            "finish_reason": "SECRET",
        },
    )
    result = safe_error_diagnostics(error)
    assert "SECRET" not in json.dumps(result)
    assert result["details"]["validation_path"] == "items.0.unknown_field.quote"
    assert result["details"]["finish_reason"] == "UNKNOWN"
    legacy = safe_error_diagnostics(ValueError("MAX_TOKENS secret"))
    assert legacy["code"] is None and legacy["details"] == {}


async def test_discovery_truncation_is_typed_without_fabricating_partial_drafts() -> None:
    body = gemini_body({"items": [draft()]}, [OFFICIAL])
    body["candidates"][0]["finishReason"] = "MAX_TOKENS"
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json=body),
        )
    ) as client:
        provider = CatalogGeminiProvider(
            settings(), reserve, client=client, trusted_hosts=["tourism.example"]
        )
        with pytest.raises(CatalogAssessmentError) as caught:
            await provider.discover("hotspot", 1, [{"id": "tokyo"}], [])
        assert provider.call_count == 1
    assert caught.value.code == "catalog_response_truncated"
