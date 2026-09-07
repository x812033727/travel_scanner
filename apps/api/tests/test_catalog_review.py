from copy import deepcopy
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.catalog_review.repository import (
    fingerprint,
    normalized_name,
    publication_gaps,
    source_urls,
)
from app.catalog_review.schemas import EvidenceCitation, EvidenceSource, ReviewAssessment
from app.catalog_review.service import (
    LEGACY_OMISSION_REASON,
    ApplyRequest,
    StartRequest,
    allowed_actions,
    is_legacy_missing_assessment,
    item_view,
    prepare_resume,
    record_assessment,
    run_view,
    snapshot_review_complete,
)
from app.models import CatalogReviewItem, CatalogReviewRun

URL = "https://www.wikidata.org/wiki/Q123"


def food_data():
    return {
        "source_urls": [URL],
        "meal_types": ["lunch"],
        "destinations": [{"destination_id": "tokyo"}],
        "localizations": [
            {"locale": locale, "name": "Dish", "summary": "Original summary"}
            for locale in ["en", "ja", "ko", "zh-TW", "zh-CN"]
        ],
    }


def place_data(country="JP"):
    return {
        "source_urls": [URL],
        "destination_id": "tokyo",
        "country_code": country,
        "wikidata_item_id": "Q123",
        "latitude": "35.71",
        "longitude": "139.79",
        "coordinate_source_type": "wikidata",
        "coordinate_source_url": URL,
        "coordinate_verified_at": "2026-09-07T01:00:00+00:00",
        "google_place_id": "ChIJexisting-independent-identity",
        "naver_map_url": None,
        "map_match_status": "verified",
        "map_verified_at": "2026-09-07T01:00:00+00:00",
        "verified_at": "2026-09-07T01:00:00+00:00",
    }


def item(kind="hotspot", data=None):
    return CatalogReviewItem(
        id=uuid4(),
        run_id=uuid4(),
        kind=kind,
        entity_id=uuid4(),
        phase="review_pending",
        name="Temple",
        destination_id="tokyo",
        snapshot_json=data or place_data(),
        snapshot_hash="a" * 64,
        status="pending",
        assessment_json={},
        evidence_json=[],
        gaps_json=[],
    )


def assessment(row, decision="approve", confidence=0.98):
    return ReviewAssessment(
        candidate_id=str(row.id),
        decision=decision,
        confidence=confidence,
        reason="Official source confirms this specific place",
        evidence=[EvidenceCitation(url=URL, quote="Exact temple name")],
    )


def legacy_omission_item():
    row = item()
    record_assessment(
        row,
        ReviewAssessment(
            candidate_id=str(row.id),
            decision="needs_review",
            confidence=0,
            reason=LEGACY_OMISSION_REASON,
        ),
        [source()],
    )
    return row


@pytest.mark.parametrize(
    "field,value",
    [
        ("candidate_id", str(uuid4())),
        ("candidate_id", None),
        ("decision", "approve"),
        ("confidence", False),
        ("confidence", "0"),
        ("confidence", None),
        ("confidence", 0.01),
        ("reason", LEGACY_OMISSION_REASON + " "),
        ("reason", "The model could not confirm this candidate."),
        ("evidence", [{"url": URL, "quote": "Exact temple name"}]),
        ("evidence", None),
        ("corrections", {"name": "Temple"}),
        ("corrections", None),
    ],
)
def test_legacy_omission_requires_the_exact_synthetic_assessment(field, value):
    row = legacy_omission_item()
    assert is_legacy_missing_assessment(row)
    row.assessment_json = {**row.assessment_json, field: value}
    assert not is_legacy_missing_assessment(row)
    assert snapshot_review_complete([row])


@pytest.mark.parametrize(
    "field,value",
    [
        ("status", "pending"),
        ("status", "error"),
        ("status", "applied"),
        ("status", "stale"),
        ("applied_action", "keep_pending"),
        ("applied_action", ""),
        ("decision", "reject"),
        ("reason", "Reviewed by an administrator"),
    ],
)
def test_legacy_omission_never_reclassifies_changed_or_applied_rows(field, value):
    row = legacy_omission_item()
    setattr(row, field, value)
    assert not is_legacy_missing_assessment(row)


def test_legacy_omission_projects_a_typed_error_without_mutating_stored_result():
    row = legacy_omission_item()
    original = deepcopy(row.assessment_json)
    assert is_legacy_missing_assessment(row)
    assert not snapshot_review_complete([row])
    assert allowed_actions(row) == []
    view = item_view(row)
    assert view["status"] == "error"
    assert view["error_code"] == "catalog_response_ids_invalid"
    assert view["decision"] is None and view["confidence"] is None
    assert view["allowed_actions"] == []
    assert row.status == "assessed" and row.assessment_json == original


@pytest.mark.parametrize(
    ("stored", "expected"),
    [
        ({"code": "catalog_response_truncated"}, "catalog_response_truncated"),
        ({"code": "catalog_provider_timeout"}, "catalog_provider_timeout"),
        ({"error": "ValueError"}, None),
        ({"code": "private-provider-response", "details": {"secret": "not-for-browser"}}, None),
        ({"code": ["catalog_response_invalid"]}, None),
    ],
)
def test_item_view_only_exposes_allowlisted_error_codes(stored, expected):
    row = item()
    row.status = "error"
    row.assessment_json = stored
    view = item_view(row)
    assert view["error_code"] == expected
    assert "details" not in view
    assert "secret" not in view
    row.status = "assessed"
    assert item_view(row)["error_code"] is None


def source(**overrides):
    return EvidenceSource(
        url=URL,
        text="A document. Exact temple name. Further details.",
        fingerprint="b" * 64,
        fetched=True,
        trusted=True,
    ).model_copy(update=overrides)


def test_all_three_requested_counts_are_bounded_and_no_new_unrecognized_types():
    payload = StartRequest(mode="discover_new")
    assert payload.requested_counts == {"hotspot": 40, "food": 20, "merchant": 40}
    for counts in [
        {"hotspot": 101, "food": 0, "merchant": 0},
        {"hotspot": 0, "food": 0, "merchant": 0},
        {"hotspot": -1, "food": 20, "merchant": 40},
        {"hotspot": 20, "food": 20, "merchant": 60, "injected": 1},
        {"hotspot": True, "food": 0, "merchant": 0},
    ]:
        with pytest.raises(ValidationError):
            StartRequest(mode="discover_new", requested_counts=counts)
    with pytest.raises(ValidationError):
        StartRequest(mode="review_pending", max_calls=100_000)


def test_apply_has_no_client_supplied_verification_or_assessment():
    with pytest.raises(ValidationError):
        ApplyRequest(
            item_ids=[uuid4()], action="approve", expected_version=1, map_match_status="verified"
        )
    with pytest.raises(ValidationError):
        ApplyRequest(item_ids=[], action="approve", expected_version=1)


def test_fingerprint_includes_relations_and_is_order_stable_for_object_keys():
    assert fingerprint({"a": 1, "b": [2]}) == fingerprint({"b": [2], "a": 1})
    assert fingerprint({"sources": [{"is_current": True}]}) != fingerprint(
        {"sources": [{"is_current": False}]}
    )


def test_name_normalization_matches_width_punctuation_and_case():
    assert normalized_name(" ＭＡＫＩＮＯ・Kyoto ") == normalized_name("Makino Kyoto")


@pytest.mark.parametrize(
    "field,value,gap",
    [
        ("google_place_id", None, "missing_exact_map_identity"),
        ("map_match_status", "unverified", "map_not_independently_verified"),
        ("map_verified_at", None, "map_not_independently_verified"),
        ("latitude", None, "missing_durable_coordinates"),
        ("latitude", 91, "missing_durable_coordinates"),
        ("longitude", "nan", "missing_durable_coordinates"),
        ("coordinate_source_type", "google_places", "missing_durable_coordinates"),
        ("coordinate_source_url", "http://example.org", "missing_durable_coordinates"),
        ("coordinate_verified_at", None, "coordinates_not_verified"),
        ("wikidata_item_id", None, "missing_wikidata_identity"),
        ("destination_id", "invented", "missing_destination"),
    ],
)
def test_publication_gates_cannot_be_waived_by_model_confidence(field, value, gap):
    data = {**place_data(), field: value}
    row = item(data=data)
    record_assessment(row, assessment(row), [source()])
    assert row.decision == "needs_review"
    assert gap in row.gaps_json
    assert "approve" not in allowed_actions(row)


def test_korean_places_require_exact_naver_not_google_identity():
    data = place_data("KR")
    assert "missing_exact_map_identity" in publication_gaps("hotspot", data)
    data["naver_map_url"] = "https://map.naver.com/p/entry/place/1234567"
    assert "missing_exact_map_identity" not in publication_gaps("hotspot", data)


def test_trusted_evidence_plus_existing_verified_identity_only_produces_a_preview():
    row = item()
    record_assessment(row, assessment(row), [source()])
    assert row.decision == "approve"
    assert row.status == "assessed"
    assert row.applied_action is None
    assert allowed_actions(row) == ["approve", "keep_pending"]
    assert "text" not in row.evidence_json[0]
    assert row.evidence_json[0]["fingerprint"] == "b" * 64
    assert item_view(row)["evidence"][0]["quote"] == "Exact temple name"


@pytest.mark.parametrize(
    "changes",
    [
        {"trusted": False},
        {"fetched": False},
        {"text": "does not contain the quote"},
    ],
)
def test_source_url_presence_is_not_verified_content(changes):
    row = item()
    record_assessment(row, assessment(row), [source(**changes)])
    assert row.decision == "needs_review"
    assert "missing_verified_source_evidence" in row.gaps_json
    assert row.assessment_json["evidence"] == []


def test_reject_is_a_suggestion_and_still_requires_exact_trusted_quote():
    row = item(data={**place_data(), "map_match_status": "unverified"})
    record_assessment(row, assessment(row, "reject"), [source()])
    assert row.decision == "reject"
    assert allowed_actions(row) == ["reject", "keep_pending"]
    second = item()
    record_assessment(second, assessment(second, "reject"), [])
    assert second.decision == "needs_review"
    assert allowed_actions(second) == ["keep_pending"]


def test_low_confidence_and_unknown_candidate_never_apply():
    row = item()
    record_assessment(row, assessment(row, confidence=0.5), [source()])
    assert row.decision == "needs_review"
    wrong = assessment(row).model_copy(update={"candidate_id": str(uuid4())})
    with pytest.raises(ValueError, match="does not match"):
        record_assessment(row, wrong, [source()])


def test_food_requires_complete_locales_and_destination_but_not_a_fake_poi():
    data = food_data()
    assert publication_gaps("food", data) == []
    data["localizations"].pop()
    assert "missing_five_locale_content" in publication_gaps("food", data)
    data["destinations"] = []
    assert "missing_destination" in publication_gaps("food", data)


def test_merchant_background_is_not_direct_evidence():
    data = {
        **place_data(),
        "sources": [{"is_current": True, "source_scope": "destination_context", "claims_json": []}],
        "categories": [{}],
    }
    assert "missing_direct_merchant_source" in publication_gaps("merchant", data)
    data["sources"][0].update(source_scope="merchant_listing", claims_json=["display_name"])
    assert "missing_direct_merchant_source" not in publication_gaps("merchant", data)


def test_completed_evaluation_does_not_require_pending_to_reach_zero():
    row = item()
    assert not snapshot_review_complete([row])
    record_assessment(row, assessment(row, "needs_review"), [source()])
    assert snapshot_review_complete([row])
    row.status = "error"
    assert not snapshot_review_complete([row])
    row.status = "applied"
    assert allowed_actions(row) == []


def test_source_list_is_deduplicated_bounded_and_keeps_identity_source_first():
    urls = source_urls({**place_data(), "source_urls": [URL] * 8 + ["https://example.org/x"]})
    assert urls[0] == URL
    assert len(urls) == 2


async def test_run_reports_suggestions_separately_from_actual_applies(monkeypatch):
    import app.catalog_review.service as service

    row = item()
    record_assessment(row, assessment(row), [source()])
    monkeypatch.setattr(service, "run_items", AsyncMock(return_value=[row]))
    run = CatalogReviewRun(
        id=row.run_id,
        actor_user_id=uuid4(),
        idempotency_key="test-key",
        request_hash="f" * 64,
        request_json={"max_calls": 80},
        mode="review_pending",
        phase="review_pending",
        status="completed",
        model="test-gemini",
        version=1,
        usage_json={"calls": 1, "thought_tokens": 4200},
        result_json={},
        created_at=datetime.now(UTC),
    )
    view = await run_view(AsyncMock(), run)
    assert view["counts"]["approved"] == 1
    assert view["counts"]["applied"] == 0
    assert view["usage"]["thought_tokens"] == 4200
    assert view["review_complete"]
    assert not view["can_resume"]


@pytest.mark.parametrize(
    "age_minutes,lease_minutes,expected",
    [(0, None, False), (6, None, True), (6, 2, False), (0, -1, True)],
)
async def test_orphaned_queue_can_resume_but_not_a_fresh_queue_or_live_lease(
    monkeypatch, age_minutes, lease_minutes, expected
):
    import app.catalog_review.service as service

    monkeypatch.setattr(service, "run_items", AsyncMock(return_value=[]))
    now = datetime.now(UTC)
    run = CatalogReviewRun(
        id=uuid4(),
        mode="review_pending",
        phase="review_pending",
        status="queued",
        model="test-gemini",
        version=1,
        request_json={"max_calls": 80},
        usage_json={"calls": 0},
        result_json={},
        created_at=now - timedelta(minutes=age_minutes),
        updated_at=now - timedelta(minutes=age_minutes),
        lease_until=now + timedelta(minutes=lease_minutes) if lease_minutes is not None else None,
    )
    assert (await run_view(AsyncMock(), run))["can_resume"] is expected
    run.usage_json = {"calls": 80}
    assert not (await run_view(AsyncMock(), run))["can_resume"]


@pytest.mark.parametrize("status", ["completed", "queued", "running", "cancelled"])
async def test_legacy_omission_counts_are_honest_and_resume_keeps_original_bounds(
    monkeypatch, status
):
    import app.catalog_review.service as service

    missing = [legacy_omission_item() for _ in range(21)]
    reviewed = [item() for _ in range(286)]
    for row in reviewed:
        record_assessment(row, assessment(row, "needs_review"), [source()])
    monkeypatch.setattr(service, "run_items", AsyncMock(return_value=missing + reviewed))
    now = datetime.now(UTC)
    run = CatalogReviewRun(
        id=uuid4(),
        mode="review_pending",
        phase="review_pending",
        status=status,
        version=1,
        request_json={"max_calls": 80},
        usage_json={"calls": 32},
        result_json={},
        created_at=now,
        updated_at=now,
        lease_until=now + timedelta(minutes=5) if status == "running" else None,
    )
    view = await run_view(AsyncMock(), run)
    assert view["status"] == ("partial" if status == "completed" else status)
    assert view["counts"]["total"] == 307
    assert view["counts"]["assessed"] == 286
    assert view["counts"]["needs_review"] == 286
    assert view["counts"]["failed"] == 21
    assert not view["review_complete"]
    assert view["can_resume"] is (status == "completed")
    assert run.status == status and run.usage_json == {"calls": 32}
    run.request_json = {"max_calls": 32}
    assert not (await run_view(AsyncMock(), run))["can_resume"]


@pytest.mark.parametrize("entity_state", ["pending", "changed", "approved", "deleted"])
async def test_resume_only_clears_current_errors_and_exact_legacy_omissions_and_audits_counts(
    monkeypatch, entity_state
):
    import app.catalog_review.service as service

    missing, applied, stale = [legacy_omission_item() for _ in range(3)]
    missing.snapshot_hash = fingerprint(missing.snapshot_json)
    applied.status, applied.applied_action = "applied", "keep_pending"
    stale.status = "stale"
    normal = item()
    record_assessment(normal, assessment(normal, "needs_review", confidence=0), [source()])
    error = item()
    error.status = "error"
    error.assessment_json = {"code": "catalog_response_truncated"}
    error.evidence_json = [source().model_dump(mode="json", exclude={"text"})]
    pending = item()
    rows = [missing, normal, applied, stale, error, pending]
    protected = [normal, applied, stale, pending]
    original = {
        row.id: deepcopy((row.status, row.decision, row.assessment_json, row.assessed_at))
        for row in protected
    }
    source_metadata = {row.id: deepcopy(row.evidence_json) for row in [missing, error]}
    now = datetime.now(UTC)
    usage = {"calls": 32, "input_tokens": 123, "output_tokens": 45, "member_charged": False}
    run = CatalogReviewRun(
        id=uuid4(),
        mode="review_pending",
        phase="review_pending",
        status="completed",
        version=4,
        request_json={"max_calls": 80},
        usage_json=deepcopy(usage),
        result_json={"apply_receipts": {"existing": {}}},
        created_at=now,
        updated_at=now,
        completed_at=now,
    )
    monkeypatch.setattr(service, "run_items", AsyncMock(return_value=rows))
    monkeypatch.setattr(service, "get_run", AsyncMock(return_value=run))
    monkeypatch.setattr(service, "_serialize_starts", AsyncMock())
    entity = None if entity_state == "deleted" else SimpleNamespace(review_status=entity_state)
    if entity_state == "changed":
        entity.review_status = "pending"
    load = AsyncMock(return_value=entity)
    snapshot = AsyncMock(
        return_value={**missing.snapshot_json, "name": "Changed"}
        if entity_state == "changed"
        else missing.snapshot_json
    )
    monkeypatch.setattr(service, "load_entity", load)
    monkeypatch.setattr(service, "entity_snapshot", snapshot)
    session = SimpleNamespace(scalar=AsyncMock(return_value=None), add=Mock(), commit=AsyncMock())
    assert await prepare_resume(session, run.id, uuid4()) is run
    assert run.status == "queued" and run.version == 5 and run.completed_at is None
    assert run.lease_token is None and run.lease_until is None
    assert run.usage_json == usage
    assert run.result_json == {"apply_receipts": {"existing": {}}}
    retried = [missing, error] if entity_state == "pending" else [error]
    for row in retried:
        assert row.status == "pending" and row.decision is None and row.assessed_at is None
        assert row.reason == "" and row.assessment_json == {} and row.gaps_json == []
        assert row.evidence_json == source_metadata[row.id]
    if entity_state != "pending":
        assert missing.status == "stale" and missing.assessed_at is not None
        assert missing.assessment_json["reason"] == LEGACY_OMISSION_REASON
        assert missing.evidence_json == source_metadata[missing.id]
    for row in protected:
        assert (row.status, row.decision, row.assessment_json, row.assessed_at) == original[row.id]
    audit = session.add.call_args.args[0]
    assert audit.action == "catalog_review_resumed"
    expected_legacy = int(entity_state == "pending")
    assert audit.metadata_json == {
        "retried_items": 1 + expected_legacy,
        "legacy_missing_items": expected_legacy,
        "stale_items": 1 - expected_legacy,
    }
    load.assert_awaited_once_with(session, missing.kind, missing.entity_id, lock=True)
    assert snapshot.await_count == int(entity_state in {"pending", "changed"})
    session.commit.assert_awaited_once()
