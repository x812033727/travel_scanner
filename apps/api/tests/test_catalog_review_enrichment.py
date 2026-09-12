"""Merchant enrichment: page classification, correction whitelisting and the service rules."""

from __future__ import annotations

import hashlib
from typing import Any
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.catalog_review.enrichment import (
    EnrichmentTaxonomy,
    VerifiedCandidate,
    location_terms,
    merchant_prompt_context,
    merchant_terms,
    verified_corrections,
    verify_candidates,
)
from app.catalog_review.schemas import (
    EnrichmentAssessment,
    EnrichmentCorrection,
    EvidenceSource,
    ReviewCandidate,
)
from app.catalog_review.service import (
    ApplyRequest,
    StartRequest,
    allowed_actions,
    item_corrections,
    item_view,
    record_enrichment,
    request_document,
)
from app.destinations.catalog import destination_for_id
from app.models import CatalogReviewItem

OFFICIAL = "https://sushi-dai.example/tsukiji"
LISTING = "https://www.gotokyo.org/en/spot/sushi-dai"
TABELOG = "https://tabelog.com/tokyo/A1313/A131301/13002260/"
TRUSTED = {"www.gotokyo.org"}
SNAPSHOT: dict[str, Any] = {
    "name": "Sushi Dai",
    "local_name": "寿司大",
    "names_json": {"ko": "스시다이"},
    "destination_id": "tokyo",
    "country_code": "JP",
    "address": None,
    "source_urls": [],
}


def page(url: str, text: str, *, trusted: bool = False, fetched: bool = True) -> EvidenceSource:
    return EvidenceSource(
        url=url,
        text=text,
        fingerprint=hashlib.sha256(text.encode("utf-8")).hexdigest() if fetched else "",
        trusted=trusted,
        fetched=fetched,
    )


def candidate(sources: list[EvidenceSource], **data: Any) -> ReviewCandidate:
    return ReviewCandidate(
        candidate_id="row-1",
        kind="merchant",
        name="Sushi Dai",
        local_name="寿司大",
        destination_id="tokyo",
        data={**SNAPSHOT, **data},
        sources=sources,
    )


def correction(**values: Any) -> EnrichmentCorrection:
    defaults = {
        "field": "address",
        "value": "東京都中央区築地5-2-1",
        "source_url": OFFICIAL,
        "quote": "寿司大 東京都中央区築地5-2-1",
    }
    return EnrichmentCorrection.model_validate({**defaults, **values})


def assessment(*corrections: EnrichmentCorrection) -> EnrichmentAssessment:
    return EnrichmentAssessment(
        candidate_id="row-1", confidence=0.8, reason="找到官網。", corrections=list(corrections)
    )


def test_merchant_terms_normalize_every_label_and_drop_short_ascii() -> None:
    assert merchant_terms(SNAPSHOT) == ["sushidai", "寿司大", "스시다이"]
    assert merchant_terms({"name": "Dai", "local_name": "大"}) == []


def test_location_terms_split_dual_city_and_skip_airport_codes() -> None:
    terms = location_terms(
        {"address": "東京都中央区築地5-2-1", "destination_id": "osaka-kyoto"},
        destination_for_id("osaka-kyoto"),
    )
    assert "東京都中央区築地5" in terms
    assert "osaka" in terms and "kyoto" in terms
    assert "大阪" in terms and "京都" in terms
    assert not any(len(term) <= 3 and term.isascii() for term in terms)


def test_official_candidate_requires_name_and_location_on_page() -> None:
    profile = destination_for_id("tokyo")
    name_only = page("https://brand.example/about", "Welcome to Sushi Dai, the finest sushi.")
    name_and_city = page(OFFICIAL, "Sushi Dai Tokyo branch, open daily.")
    name_and_address = page(
        "https://brand.example/tsukiji", "寿司大 築地店 東京都中央区築地5-2-1 営業時間"
    )
    result = verify_candidates(
        {**SNAPSHOT, "address": "東京都中央区築地5-2-1"},
        [name_only, name_and_city, name_and_address],
        {OFFICIAL: "Sushi Dai official"},
        profile,
        TRUSTED,
    )
    assert [(item.url, item.kind, item.trusted) for item in result] == [
        (OFFICIAL, "official", False),
        ("https://brand.example/tsukiji", "official", False),
    ]
    assert result[0].title == "Sushi Dai official"


def test_listing_candidate_requires_trusted_host_and_name_and_platforms_never_qualify() -> None:
    profile = destination_for_id("tokyo")
    listing = page(LISTING, "Sushi Dai is a Tsukiji institution.", trusted=True)
    unrelated_trusted = page(
        "https://www.gotokyo.org/en/spot/other", "Another shop in Tokyo.", trusted=True
    )
    wikipedia = page("https://ja.wikipedia.org/wiki/寿司大", "寿司大は東京の寿司店。", trusted=True)
    platform = page(TABELOG, "寿司大 東京都中央区築地5-2-1 3.8")
    unfetched = page(OFFICIAL, "", fetched=False)
    result = verify_candidates(
        SNAPSHOT, [listing, unrelated_trusted, wikipedia, platform, unfetched], {}, profile, TRUSTED
    )
    assert [(item.url, item.kind) for item in result] == [(LISTING, "listing")]


def test_verified_corrections_whitelist_urls_area_category_and_quoted_address() -> None:
    official = page(OFFICIAL, "寿司大 東京都中央区築地5-2-1 営業時間 5:00-13:00")
    listing = page(LISTING, "Sushi Dai, Tsukiji. A sushi counter.", trusted=True)
    verified = [
        VerifiedCandidate(OFFICIAL, "official", "Sushi Dai official", False),
        VerifiedCandidate(LISTING, "listing", "GO TOKYO", True),
    ]
    accepted, rejected = verified_corrections(
        assessment(
            correction(),
            correction(field="official_website_url", value=OFFICIAL, quote="寿司大"),
            correction(
                field="listing_source_url",
                value=LISTING,
                source_url=LISTING,
                quote="Sushi Dai, Tsukiji",
            ),
            correction(field="area_slug", value="tokyo-tsukiji", quote="築地"),
            correction(field="category_slug", value="sushi", quote="寿司大"),
            correction(field="category_slug", value="sushi", quote="寿司大"),
            correction(field="category_slug", value="ramen", quote="寿司大"),
            correction(field="area_slug", value="osaka-namba", quote="築地"),
        ),
        candidate([official, listing]),
        verified,
        area_slugs=["tokyo-tsukiji"],
        category_slugs=["sushi", "seafood"],
    )
    assert [(entry["field"], entry["value"], entry["kind"]) for entry in accepted] == [
        ("address", "東京都中央区築地5-2-1", "address"),
        ("official_website_url", OFFICIAL, "merchant_website"),
        ("listing_source_url", LISTING, "merchant_listing"),
        ("area_slug", "tokyo-tsukiji", "area"),
        ("category_slug", "sushi", "category"),
    ]
    assert accepted[1]["title"] == "Sushi Dai official"
    assert accepted[2]["title"] == "GO TOKYO"
    assert rejected == {"duplicate": 1, "category_not_allowed": 1, "area_not_allowed": 1}


def test_verified_corrections_drop_unquoted_foreign_or_unverified_sources() -> None:
    official = page(OFFICIAL, "寿司大 東京都中央区築地5-2-1")
    tampered = EvidenceSource(
        url="https://brand.example/x",
        text="寿司大 tampered",
        fingerprint="not-the-hash",
        fetched=True,
    )
    accepted, rejected = verified_corrections(
        assessment(
            correction(quote="not on the page"),
            correction(source_url="https://never-fetched.example/"),
            correction(source_url="https://brand.example/x", quote="寿司大 tampered"),
            correction(
                field="official_website_url", value="https://elsewhere.example/", quote="寿司大"
            ),
            correction(field="listing_source_url", value=OFFICIAL, quote="寿司大"),
            correction(field="address", value="大阪府", quote="寿司大"),
        ),
        candidate([official, tampered]),
        [VerifiedCandidate(OFFICIAL, "official", "", False)],
        area_slugs=[],
        category_slugs=[],
    )
    assert accepted == []
    assert rejected == {
        "quote_not_in_source": 1,
        "unknown_source": 2,
        "official_not_verified": 1,
        "listing_not_verified": 1,
        "address_not_on_page": 1,
    }


def test_address_is_not_proposed_when_the_snapshot_already_has_one() -> None:
    official = page(OFFICIAL, "寿司大 東京都中央区築地5-2-1")
    accepted, rejected = verified_corrections(
        assessment(correction()),
        candidate([official], address="既有地址"),
        [VerifiedCandidate(OFFICIAL, "official", "", False)],
        area_slugs=[],
        category_slugs=[],
    )
    assert accepted == [] and rejected == {"address_already_set": 1}


def test_taxonomy_prompt_catalog_is_bounded_to_the_batch_destinations() -> None:
    taxonomy = EnrichmentTaxonomy(
        areas_by_destination={
            "tokyo": [{"slug": "tokyo-tsukiji", "names": {}, "match_terms": ["築地"]}],
            "osaka-kyoto": [{"slug": "osaka-namba", "names": {}, "match_terms": []}],
        },
        categories=[{"slug": "sushi", "names": {"en": "Sushi"}}],
    )
    assert taxonomy.area_slugs("tokyo") == ["tokyo-tsukiji"]
    assert taxonomy.area_slugs(None) == []
    assert taxonomy.category_slugs == ["sushi"]
    assert taxonomy.prompt_catalog({"tokyo"})["areas"] == {
        "tokyo": taxonomy.areas_by_destination["tokyo"]
    }


def enrichment_item(**values: Any) -> CatalogReviewItem:
    defaults: dict[str, Any] = dict(
        id=uuid4(),
        run_id=uuid4(),
        kind="merchant",
        entity_id=uuid4(),
        phase="enrich_merchants",
        name="Sushi Dai",
        destination_id="tokyo",
        snapshot_json={**SNAPSHOT, "google_place_id": None, "sources": [], "categories": []},
        snapshot_hash="a" * 64,
        status="pending",
        assessment_json={},
        evidence_json=[],
        gaps_json=[],
    )
    return CatalogReviewItem(**(defaults | values))


def test_merchant_prompt_context_sends_labels_destination_and_known_urls_only() -> None:
    row = enrichment_item(
        snapshot_json={
            **SNAPSHOT,
            "address": "東京都中央区築地5-2-1",
            "google_place_id": "ChIJsecret",
            "latitude": "35.6",
            "sources": [
                {"source_url": OFFICIAL, "is_current": True, "source_type": "merchant_official"}
            ],
        }
    )
    context = merchant_prompt_context(row, destination_for_id("tokyo"))
    assert context["candidate_id"] == str(row.id)
    assert context["name"] == "Sushi Dai" and context["local_name"] == "寿司大"
    assert context["other_names"] == ["스시다이"]
    assert context["destination"]["id"] == "tokyo" and context["destination"]["country"]
    assert context["known_urls"] == [OFFICIAL]
    assert "google_place_id" not in context and "latitude" not in context


def test_record_enrichment_forces_needs_review_and_exposes_corrections() -> None:
    row = enrichment_item()
    corrections = [
        {
            "field": "address",
            "value": "東京都中央区築地5-2-1",
            "source_url": OFFICIAL,
            "quote": "寿司大 東京都中央区築地5-2-1",
            "title": "Sushi Dai",
            "kind": "address",
        },
        {
            "field": "official_website_url",
            "value": OFFICIAL,
            "source_url": OFFICIAL,
            "quote": "寿司大 東京都中央区築地5-2-1",
            "title": "Sushi Dai",
            "kind": "merchant_website",
        },
    ]
    source = page(OFFICIAL, "寿司大 東京都中央区築地5-2-1")
    record_enrichment(
        row,
        EnrichmentAssessment(candidate_id=str(row.id), confidence=0.8, reason="找到官網。"),
        corrections,
        [source],
        identify={"matched_in_run": True, "place_id": "ChIJx", "skipped": None},
    )
    assert row.status == "assessed" and row.decision == "needs_review"
    assert row.assessment_json["evidence"] == [
        {"url": OFFICIAL, "quote": "寿司大 東京都中央区築地5-2-1"}
    ]
    assert all("text" not in entry for entry in row.evidence_json)
    assert "missing_exact_map_identity" in row.gaps_json
    assert allowed_actions(row) == ["apply_corrections", "keep_pending"]
    view = item_view(row)
    assert view["corrections"] == [
        {key: entry[key] for key in ("field", "value", "source_url", "quote", "kind")}
        for entry in corrections
    ]
    assert view["identify"] == {"matched_in_run": True, "place_id": "ChIJx", "skipped": None}
    assert view["allowed_actions"] == ["apply_corrections", "keep_pending"]

    with pytest.raises(ValueError):
        record_enrichment(
            row,
            EnrichmentAssessment(candidate_id="someone-else", confidence=0.8, reason="x"),
            [],
            [],
        )


def test_enrichment_items_without_corrections_can_only_stay_pending() -> None:
    row = enrichment_item()
    record_enrichment(
        row,
        EnrichmentAssessment(candidate_id=str(row.id), confidence=0.0, reason="沒有找到。"),
        [],
        [],
    )
    assert allowed_actions(row) == ["keep_pending"]
    assert item_corrections(row) == []
    row.status = "applied"
    assert allowed_actions(row) == []
    review_row = enrichment_item(
        phase="review_pending", assessment_json={"corrections": {"name": "x"}}
    )
    assert item_corrections(review_row) == []


@pytest.mark.parametrize(
    "values",
    [
        {"mode": "review_pending", "destination_ids": ["tokyo"]},
        {"mode": "discover_new", "scope": "foods", "limit": 5},
        {"mode": "review_pending", "identify_places": False},
        {"mode": "enrich_merchants", "scope": "foods", "destination_ids": ["atlantis"]},
        {"mode": "enrich_merchants", "scope": "foods", "limit": 0},
        {"mode": "enrich_merchants", "scope": "foods", "limit": "5"},
    ],
)
def test_enrichment_only_fields_are_validated_per_mode(values: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        StartRequest.model_validate(values)


def test_enrich_request_normalizes_destinations_and_keeps_legacy_documents_stable() -> None:
    request = StartRequest(
        mode="enrich_merchants", scope="foods", destination_ids=[" Tokyo ", "tokyo", "osaka-kyoto"]
    )
    assert request.destination_ids == ["tokyo", "osaka-kyoto"]
    document = request_document(request)
    assert document["destination_ids"] == ["tokyo", "osaka-kyoto"]
    assert document["identify_places"] is True and document["limit"] is None
    legacy = request_document(StartRequest(mode="review_pending"))
    assert set(legacy) == {"mode", "scope", "prior_review_run_id", "requested_counts", "max_calls"}
    assert "scope" not in request_document(StartRequest(mode="review_pending"), exclude={"scope"})


def test_apply_request_accepts_apply_corrections_and_nothing_else_new() -> None:
    assert ApplyRequest(item_ids=[uuid4()], action="apply_corrections", expected_version=1)
    with pytest.raises(ValidationError):
        ApplyRequest(
            item_ids=[uuid4()], action="apply_corrections", expected_version=1, fields=["address"]
        )  # type: ignore[call-arg]
    with pytest.raises(ValidationError):
        ApplyRequest(item_ids=[uuid4()], action="publish", expected_version=1)  # type: ignore[arg-type]
