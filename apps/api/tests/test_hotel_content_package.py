"""Research inputs are validated, not silently approved or counted as published hotels."""

import csv
import io
import json
import runpy
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from app.hotspots.areas import city_areas
from app.hotspots.discovery import haversine_km
from app.models import HotelBookingOption, TravelServiceProduct
from app.problems import AppError
from app.travel_services.hotel_options import ready_option
from app.travel_services.schemas import CatalogConfig, HotelOptionInput, ProductInput
from app.travel_services.service import require_product_review


@pytest.mark.parametrize(
    "city,reviewed",
    [("tokyo", 6), ("osaka", 0), ("taipei", 0), ("seoul", 0), ("kyoto", 0), ("busan", 0)],
)
def test_pending_content_preserves_prior_identities_and_marks_gaps(city, reviewed):
    path = Path(__file__).resolve().parents[3] / f"docs/hotel-platforms/{city}.pending.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    assert len(rows) == 10
    assert len({r["product"]["source_key"] for r in rows}) == 10
    if city == "seoul":
        assert all(not r["product"]["facts"].get("google_place_id") for r in rows)
        assert sum(bool(r["product"]["facts"].get("naver_map_url")) for r in rows) == 5
    elif city in ("kyoto", "busan"):
        assert all(not r["product"]["facts"].get("google_place_id") for r in rows)
    else:
        assert len({r["product"]["facts"]["google_place_id"] for r in rows}) == 10
    assert len({r["product"]["facts"]["area_code"] for r in rows}) >= 3
    assert sum(r["product"]["facts"]["map_verified"] for r in rows) == reviewed
    for row in rows:
        p = ProductInput.model_validate(row["product"])
        assert p.destination_id == city
        assert p.facts.source_credits and p.facts.reference_price is None
        assert not p.facts.hotel_links
        options = [HotelOptionInput.model_validate(o) for o in row["booking_options"]]
        assert {o.provider for o in options} == {
            "official",
            "booking",
            "trip_com",
            "agoda",
            "expedia",
            "rakuten",
        }
        assert sum(o.discovery_status == "found" for o in options) >= 3
        assert all("status" not in o for o in row["booking_options"])
        if city in ("kyoto", "busan"):
            # Licensed permit addresses do not magically become a coordinate dataset.
            assert p.facts.latitude is p.facts.longitude is p.facts.coordinate_source_url is None
            with pytest.raises(AppError, match="service_identity_required"):
                require_product_review(p)
            p.facts.map_verified = True
            with pytest.raises(AppError, match="service_identity_required"):
                require_product_review(p)
        elif city == "seoul":
            assert p.facts.coordinate_source_url == p.facts.source_credits[0].url
            # No newly researched map is automatically approved, even one checked in Chrome.
            with pytest.raises(AppError, match="service_identity_required"):
                require_product_review(p)
            area = next(a for a in city_areas("ICN") if a.code == p.facts.area_code)
            assert (
                haversine_km(area.latitude, area.longitude, p.facts.latitude, p.facts.longitude)
                <= area.radius_km
            )
            if not p.facts.naver_map_url:
                p.facts.map_verified = True
                with pytest.raises(AppError, match="service_identity_required"):
                    require_product_review(p)
        else:
            assert p.facts.coordinate_source_url == p.facts.source_credits[0].url
            # Synthetic syntax check, not a factual review or an approval persisted to the package.
            p.facts.map_verified = True
            require_product_review(p)


def test_osaka_source_reversed_columns_are_documented_not_swapped_in_product():
    path = Path(__file__).resolve().parents[3] / "docs/hotel-platforms/osaka.pending.json"
    for row in json.loads(path.read_text(encoding="utf-8")):
        facts = row["product"]["facts"]
        assert 34 < facts["latitude"] < 35
        assert 135 < facts["longitude"] < 136
        assert "欄位" in facts["source_credits"][0]["changes"]


def test_seoul_provenance_and_unconfirmed_candidates_stay_separate():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads((directory / "seoul.evidence.json").read_text(encoding="utf-8"))
    package = json.loads((directory / "seoul.pending.json").read_text(encoding="utf-8"))
    records = {r["source_key"]: r for r in evidence["hotels"]}
    assert len(records) == len({r["permit_id"] for r in records.values()}) == 10
    assert evidence["source_crs"] == "EPSG:5174"
    assert evidence["target_crs"] == "EPSG:4326" and evidence["always_xy"] is True
    assert evidence["catalog_status"] == "pending_research_not_approved"
    for row in package:
        product = row["product"]
        facts = product["facts"]
        record = records[product["source_key"]]
        assert record["permit_status"] == "01"
        assert 190000 < float(record["x"]) < 210000
        assert 440000 < float(record["y"]) < 460000
        assert 37.50 < facts["latitude"] < 37.58 and 126.90 < facts["longitude"] < 127.08
        assert (facts["latitude"], facts["longitude"]) == (record["latitude"], record["longitude"])
        credit = facts["source_credits"][0]
        assert credit["url"] == evidence["dataset_url"]
        assert credit["license_url"] == evidence["license_url"]
        assert "KOGL Type 1" in credit["license_name"]
        assert record["permit_id"] in credit["changes"] and "EPSG:5174" in credit["changes"]
        assert record["official_identity_url"] == product["source_url"]
        if record["naver"]["status"] == "browser_identity_checked":
            assert record["naver"]["candidate_url"] == facts["naver_map_url"]
            assert record["naver"]["checked_on"]
            if record["naver"]["checked_on"] == "2026-09-08":
                assert record["naver"]["matched_name"]
                assert record["naver"]["matched_address"].startswith("서울 ")
                assert record["naver"]["matched_official_url"].startswith("https://")
            else:
                assert record["naver"]["discovery_url"] == product["source_url"]
        else:
            assert not facts.get("naver_map_url")
        reviews = {r["provider"]: r for r in record["platform_research"]}
        assert set(reviews) == {"booking", "trip_com", "agoda", "expedia", "rakuten"}
        for option in row["booking_options"]:
            if option["provider"] == "official":
                continue
            review = reviews[option["provider"]]
            assert review["searched_on"] and review["query"] and review["searched_domains"]
            if option["provider"] == "rakuten":
                assert option["discovery_status"] == review["status"] == "unconfirmed"
                assert not option.get("url") and not option.get("property_id")
            else:
                assert option["url"] == review["candidate_url"]
                assert review["status"] == "name_address_matched_pending_review"
                assert option.get("property_id", "") != record["permit_id"]


@pytest.mark.parametrize("city", ["seoul", "busan"])
def test_pending_options_cannot_be_public_even_if_product_were_approved(city):
    path = Path(__file__).resolve().parents[3] / f"docs/hotel-platforms/{city}.pending.json"
    now = datetime.now(UTC)
    config = CatalogConfig(enabled_destinations=[city], enabled_kinds=["hotel"])
    for row in json.loads(path.read_text(encoding="utf-8")):
        product = TravelServiceProduct(**row["product"], id=uuid4(), status="approved")
        for source in row["booking_options"]:
            option = HotelBookingOption(
                **HotelOptionInput.model_validate(source).model_dump(),
                id=uuid4(),
                status="pending",
                verified_at=None,
                health_status="unchecked",
            )
            assert not ready_option(product, option, config, now)


def test_seoul_admin_csv_transfer_preserves_utf8_and_does_not_add_approval():
    root = Path(__file__).resolve().parents[3]
    directory = root / "docs/hotel-platforms"
    result = subprocess.run(
        [
            sys.executable,
            str(directory / "prepare_import.py"),
            str(directory / "seoul.pending.json"),
        ],
        cwd=root / "apps/api",
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    rows = list(csv.DictReader(io.StringIO(result.stdout)))
    assert len(rows) == len({row["source_key"] for row in rows}) == 10
    assert any(row["title"] == "머큐어 앰배서더 서울 홍대" for row in rows)
    for row in rows:
        assert json.loads(row["facts"])["map_verified"] is False
        options = json.loads(row["booking_options"])
        assert len(options) == 6 and all("status" not in option for option in options)
        assert sum(option["discovery_status"] == "found" for option in options) == 5


def test_kyoto_permit_evidence_does_not_invent_locations_or_save_personal_fields():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads((directory / "kyoto.evidence.json").read_text(encoding="utf-8"))
    package = json.loads((directory / "kyoto.pending.json").read_text(encoding="utf-8"))
    records = {r["source_key"]: r for r in evidence["hotels"]}
    assert len(records) == 10
    assert evidence["coordinate_status"] == "missing_source_dataset_has_no_coordinates"
    assert evidence["catalog_status"] == "pending_research_not_approved"
    assert evidence["license_name"] == "CC BY 4.0"
    for row in package:
        product = ProductInput.model_validate(row["product"])
        record = records[product.source_key]
        assert record["official_identity_url"] == product.source_url
        assert record["permit_category"] == "旅館・ホテル"
        assert record["permit_address"].startswith("京都市")
        assert record["permitted_on"]
        assert record["map_status"] == "not_checked"
        assert record["coordinate_status"] == "not_available"
        assert not {"operator", "business_person", "latitude", "longitude", "google_place_id"} & (
            record.keys()
        )
        assert product.facts.source_credits[0].url == evidence["dataset_url"]
        reviews = {review["provider"]: review for review in record["platform_research"]}
        for option in row["booking_options"]:
            if option["provider"] == "official":
                continue
            review = reviews[option["provider"]]
            assert review["searched_on"] and review["searched_domains"] and review["query"]
            if option.get("url"):
                assert review["candidate_url"] == option["url"]
                assert review["status"] == "identity_candidate_pending_browser_review"
            else:
                assert option["discovery_status"] == review["status"] == "unconfirmed"
                assert not option.get("property_id")


def test_recent_seoul_checks_exclude_parnas_interrupted_browser_and_restaurants():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads((directory / "seoul.evidence.json").read_text(encoding="utf-8"))
    checked = [r for r in evidence["hotels"] if r["naver"]["status"] == "browser_identity_checked"]
    assert len(checked) == 5
    assert not any("parnas" in record["source_key"] for record in checked)
    rejected_restaurant_ids = {"1477750254", "1002390145", "20753494", "11714851", "18689714"}
    assert not rejected_restaurant_ids & {
        record["naver"]["candidate_url"].rstrip("/").split("/")[-1] for record in checked
    }


def test_busan_identity_research_excludes_closure_and_does_not_assert_licensing():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads((directory / "busan.evidence.json").read_text(encoding="utf-8"))
    package = json.loads((directory / "busan.pending.json").read_text(encoding="utf-8"))
    records = {r["source_key"]: r for r in evidence["hotels"]}
    assert len(records) == 10
    assert evidence["catalog_status"] == "pending_research_not_approved"
    closure = next(r for r in evidence["excluded_candidates"] if r["reason"] == "scheduled_closure")
    assert closure["effective_date"] == "2026-12-29"
    assert closure["browser_checked_on"] == "2026-09-08"
    assert not any("solaria" in row["product"]["source_key"] for row in package)
    assert not any("ibis" in row["product"]["source_key"] for row in package)
    for row in package:
        product = ProductInput.model_validate(row["product"])
        record = records[product.source_key]
        assert record["official_name"] == product.title
        assert record["official_identity_url"] == product.source_url
        assert record["official_address"]
        assert record["map_status"] == "not_checked"
        assert product.facts.naver_map_url is None
        assert product.facts.google_place_id is None
        assert "no content reuse license asserted" in product.facts.source_credits[0].license_name
        reviews = {r["provider"]: r for r in record["platform_research"]}
        for option in row["booking_options"]:
            if option["provider"] == "official":
                continue
            review = reviews[option["provider"]]
            assert review["query"] and review["searched_on"] and review["searched_domains"]
            if option.get("url"):
                assert option["url"] == review["candidate_url"]
                assert review["status"] == "identity_candidate_pending_browser_review"
            else:
                assert option["discovery_status"] == review["status"] == "unconfirmed"
                assert not option.get("property_id")


def credit_fixture():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    prepare = runpy.run_path(str(directory / "prepare_credit_update.py"))["prepare_credit_update"]
    source = json.loads((directory / "tokyo.pending.json").read_text(encoding="utf-8"))[0][
        "product"
    ]
    researched = ProductInput.model_validate(source)
    source["facts"].pop("source_credits")
    source["names_json"]["zh-TW"] = "Keep the administrator's saved label"
    return prepare, ProductInput.model_validate(source), researched


def test_tokyo_review_checkpoint_keeps_platform_and_browser_decisions_independent():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads((directory / "tokyo.review-2026-09-08.json").read_text(encoding="utf-8"))
    package = json.loads((directory / "tokyo.pending.json").read_text(encoding="utf-8"))
    original = {
        r["product"]["source_key"]: r for r in package if r["product"]["facts"]["map_verified"]
    }
    assert {r["source_key"] for r in evidence["hotels"]} == set(original)
    assert len(original) == 6
    for hotel in evidence["hotels"]:
        row = original[hotel["source_key"]]
        assert hotel["location_status"] == "existing_review_preserved_not_reverified"
        assert hotel["official_identity_url"] == row["product"]["source_url"]
        assert hotel["source_credit_url"] == row["product"]["facts"]["source_credits"][0]["url"]
        options = {o["provider"]: o for o in row["booking_options"]}
        assert len(hotel["platform_reviews"]) == 5
        for review in hotel["platform_reviews"]:
            assert review.get("url") == options[review["provider"]].get("url")
            if review["provider"] == "trip_com":
                assert review["status"] == "approved" and review["version"] == 2
                assert review["health"] == "healthy" and review["browser_verified"] is False
                assert review["matched_name"] and review["matched_address"]
                assert review["reviewed_on"] == evidence["checked_on"]
            else:
                assert review["status"] == "pending"
                assert review["reason"]
            if not review.get("url"):
                assert review["health"] == "not_checked"
                assert review["reason"] == "Discovery unresolved; no asserted URL or network check."


def test_credit_only_update_preserves_saved_identity_labels_and_omits_legacy_links():
    prepare, current, researched = credit_fixture()
    result = prepare(current, researched)
    assert result.names_json == current.names_json
    assert result.facts.source_credits == researched.facts.source_credits
    assert "hotel_links" not in result.facts.model_fields_set
    before = current.model_dump(mode="json")
    after = result.model_dump(mode="json")
    before["facts"].pop("source_credits")
    after["facts"].pop("source_credits")
    assert before == after
    assert prepare(result, researched) == result


@pytest.mark.parametrize(
    "field,value", [("latitude", 35.1), ("google_place_id", "changed"), ("map_verified", False)]
)
def test_credit_update_rejects_changed_or_unreviewed_location(field, value):
    prepare, current, researched = credit_fixture()
    setattr(current.facts, field, value)
    with pytest.raises(ValueError, match="identity changed"):
        prepare(current, researched)


def test_credit_update_rejects_legacy_projection_and_conflicting_credit():
    prepare, current, researched = credit_fixture()
    projected = current.model_dump(mode="json")
    with pytest.raises(ValueError, match="legacy hotel_links"):
        prepare(ProductInput.model_validate(projected), researched)
    current.facts.source_credits = [
        researched.facts.source_credits[0].model_copy(update={"publisher": "Someone else"})
    ]
    with pytest.raises(ValueError, match="Existing attribution differs"):
        prepare(current, researched)


def test_tokyo_four_review_does_not_promote_unobserved_maps_with_approved_options():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads(
        (directory / "tokyo-four.review-2026-09-08.json").read_text(encoding="utf-8")
    )
    package = json.loads((directory / "tokyo.pending.json").read_text(encoding="utf-8"))
    rows = {r["product"]["source_key"]: r for r in package}
    checked = [
        h for h in evidence["hotels"] if h["map_review"]["status"] == "browser_identity_checked"
    ]
    assert len(checked) == 1
    assert checked[0]["source_key"] == "editorial:tokyo:ryumeikan-tokyo"
    assert checked[0]["map_review"]["name_address_website_matched"] is True
    now = datetime.now(UTC)
    config = CatalogConfig(enabled_destinations=["tokyo"], enabled_kinds=["hotel"])
    for hotel in evidence["hotels"]:
        row = rows[hotel["source_key"]]
        # A reviewed production location is not replayed as approved import input.
        assert row["product"]["facts"]["map_verified"] is False
        assert hotel["official_identity_url"] == row["product"]["source_url"]
        options = {o["provider"]: o for o in row["booking_options"]}
        approved = [r for r in hotel["platform_reviews"] if r["status"] == "approved"]
        assert {r["provider"] for r in approved} == {"official", "trip_com"}
        for review in approved:
            assert review["url"] == options[review["provider"]]["url"]
            assert review["health"] == "healthy" and review["browser_verified"] is False
            assert review["matched_address"] and review["identity_evidence_url"]
            if hotel["product_status"] == "pending":
                product = TravelServiceProduct(**row["product"], id=uuid4(), status="pending")
                option = HotelBookingOption(
                    **HotelOptionInput.model_validate(options[review["provider"]]).model_dump(),
                    id=uuid4(),
                    status="approved",
                    verified_at=now,
                    health_status="healthy",
                )
                assert not ready_option(product, option, config, now)


def test_new_tokyo_agoda_candidates_are_not_approved_from_http_health():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads(
        (directory / "tokyo-four.review-2026-09-08.json").read_text(encoding="utf-8")
    )
    package = json.loads((directory / "tokyo.pending.json").read_text(encoding="utf-8"))
    rows = {r["product"]["source_key"]: r for r in package}
    candidates = [
        (h, r) for h in evidence["hotels"] for r in h["platform_reviews"] if r.get("new_candidate")
    ]
    assert len(candidates) == 3
    for hotel, review in candidates:
        source = next(
            o for o in rows[hotel["source_key"]]["booking_options"] if o["provider"] == "agoda"
        )
        assert review["status"] == "pending" and review["health"] == "healthy"
        assert source["url"] == review["url"] and source["discovery_status"] == "found"
        assert "待審" in source["identity_note"] and "status" not in source
        assert not source.get("property_id")


def test_osaka_platform_review_keeps_unverified_hotels_hidden_even_when_city_enabled():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads(
        (directory / "osaka-five.review-2026-09-08.json").read_text(encoding="utf-8")
    )
    package = json.loads((directory / "osaka.pending.json").read_text(encoding="utf-8"))
    rows = {r["product"]["source_key"]: r for r in package}
    assert len(evidence["hotels"]) == 5
    now = datetime.now(UTC)
    config = CatalogConfig(
        public_enabled=True, enabled_destinations=["osaka"], enabled_kinds=["hotel"]
    )
    reviewed_ids = set()
    for hotel in evidence["hotels"]:
        row = rows[hotel["source_key"]]
        data = ProductInput.model_validate(row["product"])
        assert hotel["product_status"] == "pending" and not data.facts.map_verified
        assert hotel["map_review_status"] == "not_checked"
        assert hotel["official_identity_url"] == data.source_url
        options = {o["provider"]: o for o in row["booking_options"]}
        approved = [r for r in hotel["platform_reviews"] if r["status"] == "approved"]
        assert {r["provider"] for r in approved} == {"official", "trip_com"}
        product = TravelServiceProduct(**row["product"], id=uuid4(), status="pending")
        for review in approved:
            assert review["url"] == options[review["provider"]]["url"]
            assert review["identity_evidence_url"] == data.source_url
            assert review["matched_name"] and review["matched_address"]
            assert review["version"] == 2 and review["health"] == "healthy"
            assert review["browser_verified"] is False
            assert review["reviewed_on"] == evidence["checked_on"]
            reviewed_ids.add(review["option_id"])
            option = HotelBookingOption(
                **HotelOptionInput.model_validate(options[review["provider"]]).model_dump(),
                id=uuid4(),
                status="approved",
                verified_at=now,
                health_status="healthy",
            )
            assert not ready_option(product, option, config, now)
    assert len(reviewed_ids) == 10


def test_osaka_candidate_additions_do_not_guess_ids_or_promote_ambiguous_sources():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads(
        (directory / "osaka-five.review-2026-09-08.json").read_text(encoding="utf-8")
    )
    package = json.loads((directory / "osaka.pending.json").read_text(encoding="utf-8"))
    rows = {r["product"]["source_key"]: r for r in package}
    candidates = [
        (h, r) for h in evidence["hotels"] for r in h["platform_reviews"] if r.get("new_candidate")
    ]
    assert len(candidates) == 4
    for hotel, review in candidates:
        option = next(
            o for o in rows[hotel["source_key"]]["booking_options"] if o["provider"] == "agoda"
        )
        assert option["url"] == review["url"]
        assert option["discovery_status"] == "found" and not option.get("property_id")
        assert "待審" in option["identity_note"] and "status" not in option
        assert review["status"] == "pending" and review["health"] == "unchecked"
        assert review["browser_verified"] is False and review["version"] == 2
    granvia = rows["editorial:osaka:granvia-osaka"]
    agoda = next(o for o in granvia["booking_options"] if o["provider"] == "agoda")
    assert agoda["discovery_status"] == "unconfirmed" and not agoda.get("url")
    assert not any("kobe-jp" in o.get("url", "") for r in package for o in r["booking_options"])
    intergate = next(h for h in evidence["hotels"] if "intergate" in h["source_key"])
    assert intergate["official_address"].endswith("梅田2-5-2")
    assert any(e.get("address", "").endswith("梅田2丁目4-9") for e in evidence["excluded"])
