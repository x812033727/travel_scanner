"""Offline assertions for the exact 443-record follow-up evidence manifest.

These tests do not fetch source content or mutate production. Live preservation
and public-language visibility are verified by a separate locked operator.
"""

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from uuid import UUID

import pytest

PATH = Path(__file__).resolve().parents[3] / "docs/catalog-content-reviews/2026-09-09-followup.json"
SEMANTIC_HASH = "f1ff565837229d70ba1398f137b81c4b48d3b262e79f12bb64b060e0d5cfd574"
LOCALES = {"en", "ja", "ko", "zh-TW", "zh-CN"}
CORRECTIONS = {
    "144cbf39-40db-474f-ab35-697b929eb11e": "zh-TW",
    "1d49536d-6747-4910-8fbb-c61f1b44fe37": "en",
    "1f82ff3a-b626-4a24-a3c7-e82a177e2084": "en",
    "448d5309-5215-4595-9c67-e1d5bcd3c754": "zh-TW",
}


@pytest.fixture(scope="module")
def manifest():
    return json.loads(PATH.read_text(encoding="utf-8"))


def test_exact_sealed_scope_and_semantic_content(manifest):
    actual = hashlib.sha256(json.dumps(manifest, sort_keys=True, default=str).encode()).hexdigest()
    assert actual == SEMANTIC_HASH
    assert manifest["batch_id"] == "2026-09-09-content-followup"
    assert manifest["runtime_sha"] == "b675f5d34a353eddfb789a953968c3c6d45eac4a"
    assert manifest["database_schema"] == "0063_destination_offers"
    expected = {
        "guides": (280, "1f8e8d8b399bb1bb300ccbcdf01e282ada4808319e342ab2b610b801b09b10cc"),
        "merchants": (163, "e834ec9fc11deaea01adbb1c991b73de73648c59b311fcb2add11d0261c783af"),
    }
    for kind, (count, id_hash) in expected.items():
        rows = manifest[kind]
        assert len(rows) == len({r["id"] for r in rows}) == count
        assert (
            hashlib.sha256("\n".join(sorted(r["id"] for r in rows)).encode()).hexdigest() == id_hash
        )
    assert manifest["initial_scope"]["new_ids_since_prior_review"] == 0
    assert manifest["initial_scope"]["changed_records_since_prior_review"] == 0


def test_truthful_outcomes_do_not_claim_all_pending_resolved(manifest):
    actual = {
        kind: dict(Counter(r["decision"] for r in manifest["guides"] if r["content_type"] == kind))
        for kind in ("article", "video")
    }
    actual["merchant"] = dict(Counter(r["decision"] for r in manifest["merchants"]))
    assert (
        actual
        == manifest["decisions_by_type"]
        == {
            "article": {"approve": 10, "reject": 103, "keep_pending": 59},
            "video": {"approve": 30, "reject": 45, "keep_pending": 33},
            "merchant": {"keep_pending": 163},
        }
    )
    assert manifest["review_coverage_complete"] is True
    assert manifest["all_items_approved_or_rejected"] is False
    assert manifest["remaining_evidence_gaps"]["total"] == 255


def test_normal_handler_reasons_saved_ids_and_source_evidence(manifest):
    for row in manifest["guides"] + manifest["merchants"]:
        assert str(UUID(row["id"])) == row["id"]
        assert row["decision"] in {"approve", "reject", "keep_pending"}
        assert 0 < len(row["reason"]) <= 500
        assert row["method"] and row["sources"]
        assert re.fullmatch(r"[a-f0-9]{64}", row["expected_record_fingerprint"])
        for source in row["sources"]:
            parsed = urlsplit(source)
            assert parsed.scheme == "https" and parsed.hostname
            assert parsed.username is None and parsed.password is None


def test_merchants_still_require_exact_identity_and_durable_evidence(manifest):
    for row in manifest["merchants"]:
        assert row["decision"] == "keep_pending"
        assert row["independent_review_gaps"]
        assert row["preservation"]["proposed_mutation_fields"] == []
        assert row["preservation"]["old_apply_receipt_replayed"] is False
        assert row["followup"]["all_record_and_relation_hashes_match"] is True
        assert row["followup"]["proof_ready_for_publication"] is False
        assert set(row["expected_relation_fingerprints"]) == {
            "sources",
            "categories",
            "foods",
            "platforms",
            "styles",
        }
    by_id = {r["id"]: r for r in manifest["merchants"]}
    sunny = by_id["90e25d52-61a7-4a3e-89fa-a8d875da913b"]
    assert "government_dataset_match_is_different_branch" in sunny["independent_review_gaps"]
    mak = by_id["29732d41-650b-4931-9c85-beeb5445cc80"]
    assert "wikidata_coordinate_precision_insufficient" in mak["independent_review_gaps"]


def test_only_four_explicit_body_verified_article_locale_corrections(manifest):
    assert {r["id"]: r["review_locale"] for r in manifest["guides"] if "review_locale" in r} == (
        CORRECTIONS
    )
    for row in manifest["guides"]:
        assert row["locale"] in LOCALES
        if row["id"] in CORRECTIONS:
            assert row["decision"] == "approve" and row["content_type"] == "article"
            assert row["evidence"]["duplicate_check"]["known_collisions"] == 0
            assert row["review_locale"] != row["locale"]


def test_live_iab_redirect_language_conflict_overrides_proposed_approval(manifest):
    by_id = {r["id"]: r for r in manifest["guides"]}
    wiki = by_id["5357a6be-5828-4226-b920-808e114047c6"]
    assert wiki["decision"] == "keep_pending"
    assert wiki["locale"] == "zh-CN" and "review_locale" not in wiki
    assert "IAB" in wiki["reason"] and "繁體" in wiki["reason"]
    geek = by_id["7c8c27eb-3f1f-47fa-b6a2-de67e15084a0"]
    assert geek["decision"] == "approve" and geek["locale"] == "en"
    assert geek["evidence"]["observed_landing_url"].endswith("taipei-technology-district#syntrend")


def test_articles_distinguish_ineligibility_from_access_failure(manifest):
    rows = [r for r in manifest["guides"] if r["content_type"] == "article"]
    for row in rows:
        assert row["preservation"]["creator_metadata_unchanged"] is True
        assert row["preservation"]["no_full_body_copied"] is True
        if row["decision"] == "keep_pending":
            assert row["preservation"]["allowed_mutation_fields"] == []
    by_id = {r["id"]: r for r in rows}
    assert by_id["017003ea-ba67-48c4-9b91-45acb1e3c78b"]["decision"] == "reject"
    assert "通用首頁" in by_id["017003ea-ba67-48c4-9b91-45acb1e3c78b"]["reason"]
    assert by_id["040456ae-7743-479c-b76f-605e41916b8d"]["decision"] == "keep_pending"
    conflict = by_id["ef2399a3-4a6e-4739-93a0-00dea446cede"]
    assert conflict["decision"] == "reject" and "NParks" in conflict["reason"]


def test_video_approval_needs_exact_timestamped_explanation_not_model_score(manifest):
    for row in manifest["guides"]:
        if row["content_type"] != "video":
            continue
        assert row["no_metadata_or_locale_rewrite"] is True
        assert row["original_title_preserved"] is True
        assert row["language_review"]["locale_change_proposed"] is False
        assert (
            row["language_review"]["creator_nationality_or_location_used_to_infer_language"]
            is False
        )
        if row["decision"] == "approve":
            assert row["prior_result"]["status"] == "assessed"
            assert row["evidence"] and row["reason"]
            assert all(
                re.fullmatch(r"\d{2,}:\d{2}(?::\d{2})?", e["timestamp"]) for e in row["evidence"]
            )
    podcast = next(
        r for r in manifest["guides"] if r["id"] == "4f65b694-a956-44d1-881e-5ea3ad876202"
    )
    assert podcast["decision"] == "approve"
    assert podcast["language_review"]["new_clip_spoken_language"] == "Mandarin"
    assert podcast["language_review"]["new_clip_caption_script"] == "none"


def test_invalid_clip_and_unproven_english_subtitles_remain_pending(manifest):
    by_id = {r["id"]: r for r in manifest["guides"]}
    for identity in (
        "1388cc3e-ca68-4dce-aac5-88d103246838",  # Out-of-range timestamps.
        "13244dc1-9c0f-4351-9227-b25f5055923f",  # Cantonese, English captions not localized.
        "84e9ab65-2513-413f-b7a0-25baa0dc39fe",  # A silent minute does not describe the full video.
        "198c5a69-e0d7-4cda-a76a-9e6e4c69630c",
    ):
        assert by_id[identity]["decision"] == "keep_pending"
    assert by_id["1388cc3e-ca68-4dce-aac5-88d103246838"]["new_timestamp_evidence"] == []


def test_twelve_calls_exact_usage_no_retries_or_additional_search_calls(manifest):
    usage = manifest["provider_usage"]
    assert usage["audited_requests"] == usage["result_files"] == usage["provider_calls"] == 12
    assert usage["result_hashes_verified"] == usage["rebuilt_request_payload_hashes_verified"] == 12
    assert usage["retries"] == usage["unknown_usage_calls"] == 0
    assert usage["member_usage_charged"] is False
    assert usage["statuses"] == {"assessed": 11, "response_invalid": 1}
    assert usage["usage_reported_by_provider"] == {
        "promptTokenCount": 56493,
        "candidatesTokenCount": 3323,
        "totalTokenCount": 59816,
    }
    assert usage["quota_status"]["gemini"] == {"used": 489, "limit": 1000}
    assert usage["quota_status"]["brave"]["used"] == 30
    assert usage["quota_status"]["youtube"]["used"] == 80
    assert len({r["audit_id"] for r in usage["attempts"]}) == 12
    totals = Counter()
    for row in usage["attempts"]:
        assert row["calls"] == 1
        totals.update(row["usage"])
    assert dict(totals) == usage["usage_reported_by_provider"]


def test_report_has_no_credentials_full_bodies_or_coordinate_values(manifest):
    prohibited = {
        "api_key",
        "access_token",
        "refresh_token",
        "password",
        "email",
        "raw_response",
        "full_text",
        "transcript",
        "chain_of_thought",
        "latitude",
        "longitude",
        "invalid_final_text",
    }

    def inspect(value):
        if isinstance(value, dict):
            assert not (set(value) & prohibited)
            for item in value.values():
                inspect(item)
        elif isinstance(value, list):
            for item in value:
                inspect(item)

    inspect(manifest)
