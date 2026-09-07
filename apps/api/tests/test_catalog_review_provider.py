from __future__ import annotations

import asyncio
import hashlib
import json
from typing import Any

import httpx
import pytest
from pydantic import ValidationError

from app.catalog_review import evidence
from app.catalog_review import provider as provider_module
from app.catalog_review.evidence import fetch_sources, is_trusted_source, normalize_source_url
from app.catalog_review.provider import CatalogGeminiProvider
from app.catalog_review.schemas import EvidenceCitation, EvidenceSource, ReviewCandidate
from app.config import Settings
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
        with pytest.raises(ValueError, match="duplicate or unknown"):
            await provider.assess([candidate()])


async def test_omitted_candidate_stays_pending_and_input_batch_is_bounded() -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json=gemini_body({"items": []})),
        )
    ) as client:
        provider = CatalogGeminiProvider(settings(), reserve, client=client)
        result = await provider.assess([candidate()])
        assert result.items[0].decision == "needs_review"
        assert result.items[0].candidate_id == "row-1"
        with pytest.raises(ValueError, match="At most 20"):
            await provider.assess([candidate(candidate_id=str(i)) for i in range(21)])
        with pytest.raises(ValueError, match="Duplicate input"):
            await provider.assess([candidate(), candidate()])
        assert (await provider.assess([])).items == []
        assert provider.call_count == 1


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
        with pytest.raises(ValueError, match="invalid structured data"):
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
        with pytest.raises(httpx.HTTPStatusError):
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
