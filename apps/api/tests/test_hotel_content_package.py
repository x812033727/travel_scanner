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
                if product["source_key"] in {
                    "editorial:seoul:ryse-autograph-collection",
                    "editorial:seoul:mercure-hongdae",
                }:
                    assert option["discovery_status"] == "found"
                    assert review["status"] == "candidate_found_pending_review"
                    assert option["url"] == review["candidate_url"]
                    assert review["matched_fields"] == ["hotel_name"]
                    assert review["review_checkpoint"] == "seoul-links.review-2026-09-08.json"
                else:
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
        expected = (
            6
            if row["source_key"]
            in {"editorial:seoul:ryse-autograph-collection", "editorial:seoul:mercure-hongdae"}
            else 5
        )
        assert sum(option["discovery_status"] == "found" for option in options) == expected


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


def namba_map_checkpoint():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads(
        (directory / "namba-map.review-2026-09-08.json").read_text(encoding="utf-8")
    )
    rows = {}
    for city in ("tokyo", "osaka"):
        package = json.loads((directory / f"{city}.pending.json").read_text(encoding="utf-8"))
        rows.update({r["product"]["source_key"]: r for r in package})
    return evidence, rows


def test_namba_platform_reviews_do_not_approve_unobserved_product_locations():
    evidence, rows = namba_map_checkpoint()
    assert len(evidence["hotels"]) == 5
    config = CatalogConfig(
        public_enabled=True, enabled_destinations=["osaka"], enabled_kinds=["hotel"]
    )
    now = datetime.now(UTC)
    for hotel in evidence["hotels"]:
        source = rows[hotel["source_key"]]
        assert hotel["product_status"] == "pending" and hotel["map_review_status"] == "not_checked"
        assert source["product"]["facts"]["map_verified"] is False
        options = {o["provider"]: o for o in source["booking_options"]}
        approved = [o for o in hotel["platform_reviews"] if o["status"] == "approved"]
        assert {o["provider"] for o in approved} == {"official", "trip_com"}
        product = TravelServiceProduct(**source["product"], id=uuid4(), status="pending")
        for review in approved:
            assert review["url"] == options[review["provider"]]["url"]
            assert review["identity_evidence_url"] == source["product"]["source_url"]
            assert review["matched_name"] and review["matched_address"]
            assert review["health"] == "healthy" and review["version"] == 2
            assert review["browser_verified"] is False
            option = HotelBookingOption(
                **HotelOptionInput.model_validate(options[review["provider"]]).model_dump(),
                id=uuid4(),
                status="approved",
                verified_at=now,
                health_status="healthy",
            )
            assert not ready_option(product, option, config, now)
    sotetsu = next(h for h in evidence["hotels"] if "sotetsu" in h["source_key"])
    trip = next(o for o in sotetsu["platform_reviews"] if o["provider"] == "trip_com")
    assert "4064224" in trip["url"] and "4064224" in trip["supporting_platform_url"]
    assert trip["url"].startswith("https://www.trip.com/")
    assert "four weeks ago" in trip["note"]
    swissotel = next(h for h in evidence["hotels"] if "swissotel" in h["source_key"])
    assert "/pdf/" in swissotel["official_identity_url"]
    assert "/contact-info/" in swissotel["supporting_official_url"]


def test_only_five_observed_maps_approved_without_rewriting_research_inputs():
    evidence, rows = namba_map_checkpoint()
    expected = {
        "editorial:tokyo:tokyo-station-hotel",
        "editorial:tokyo:mitsui-garden-kyobashi",
        "editorial:tokyo:millennium-mitsui-garden-tokyo",
        "editorial:osaka:vischio-osaka",
        "editorial:osaka:hankyu-respire-osaka",
    }
    assert {m["source_key"] for m in evidence["map_reviews"]} == expected
    for review in evidence["map_reviews"]:
        product = rows[review["source_key"]]["product"]
        assert review["status"] == "browser_identity_checked"
        assert review["name_address_website_matched"] is True
        assert review["provider_coordinates_copied"] is False
        assert review["google_place_id"] == product["facts"]["google_place_id"]
        assert review["official_identity_url"] == product["source_url"]
        assert review["product_status"] == "approved" and review["product_version"] == 3
        assert product["facts"]["map_verified"] is False
        assert product["facts"]["source_credits"]
    assert "Debugger unattached" in evidence["browser_status"]
    assert (
        rows["editorial:osaka:intergate-osaka-umeda"]["product"]["facts"]["map_verified"] is False
    )
    live = evidence["production"]
    assert live["products_approved"] + live["products_pending"] == live["products_total"] == 60
    assert live["options_approved"] + live["options_pending"] == live["options_total"] == 360
    assert live["new_hotel_identities"] == live["complete_cities"] == 0
    assert live["config_changed"] is False
    assert set(live["public_hotels_by_locale"]) == {"en", "ja", "ko", "zh-TW", "zh-CN"}
    assert all(v == {"tokyo": 10, "osaka": 2} for v in live["public_hotels_by_locale"].values())


def test_namba_four_candidates_keep_observed_urls_pending_and_no_guessed_ids():
    evidence, rows = namba_map_checkpoint()
    candidates = [
        (h, r) for h in evidence["hotels"] for r in h["platform_reviews"] if r.get("new_candidate")
    ]
    assert len(candidates) == 4
    for hotel, review in candidates:
        option = next(
            o for o in rows[hotel["source_key"]]["booking_options"] if o["provider"] == "agoda"
        )
        assert option["url"] == review["url"] and option["discovery_status"] == "found"
        assert not option.get("property_id") and "status" not in option
        assert "待審" in option["identity_note"]
        assert review["status"] == "pending" and review["health"] == "unchecked"
        assert review["version"] == 2 and review["browser_verified"] is False
    sotetsu = rows["editorial:osaka:sotetsu-grand-fresa-osaka-namba"]
    agoda = next(o for o in sotetsu["booking_options"] if o["provider"] == "agoda")
    assert "/osaka-nanba-washington-plaza-hotel/" in agoda["url"]
    assert "舊名稱 slug" in agoda["identity_note"]
    swissotel = rows["editorial:osaka:swissotel-nankai-osaka"]
    agoda = next(o for o in swissotel["booking_options"] if o["provider"] == "agoda")
    assert agoda["discovery_status"] == "unconfirmed" and not agoda.get("url")
    assert any("kobe-jp" in e["url"] for e in evidence["excluded"])
    assert not any(
        "kobe-jp" in o.get("url", "") for r in rows.values() for o in r["booking_options"]
    )


def kyoto_five_checkpoint():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads(
        (directory / "kyoto-five.review-2026-09-08.json").read_text(encoding="utf-8")
    )
    package = json.loads((directory / "kyoto.pending.json").read_text(encoding="utf-8"))
    return evidence, {r["product"]["source_key"]: r for r in package}


def test_kyoto_five_independent_reviews_preserve_missing_location_gate():
    evidence, rows = kyoto_five_checkpoint()
    assert len(evidence["hotels"]) == 5
    now = datetime.now(UTC)
    config = CatalogConfig(
        public_enabled=True, enabled_destinations=["kyoto"], enabled_kinds=["hotel"]
    )
    approved = []
    for hotel in evidence["hotels"]:
        source = rows[hotel["source_key"]]
        product = TravelServiceProduct(**source["product"], id=uuid4(), status="pending")
        data = ProductInput.model_validate(source["product"])
        assert hotel["product_status"] == "pending" and hotel["map_review_status"] == "not_checked"
        assert not data.facts.map_verified and not data.facts.google_place_id
        assert data.facts.latitude is data.facts.longitude is None
        with pytest.raises(AppError, match="service_identity_required"):
            require_product_review(data)
        options = {o["provider"]: o for o in source["booking_options"]}
        for review in hotel["platform_reviews"]:
            assert review.get("url") == options[review["provider"]].get("url")
            if review["status"] != "approved":
                continue
            approved.append(review)
            assert review["provider"] in {"official", "trip_com"}
            assert review["health"] == "healthy" and review["version"] == 2
            assert review["matched_name"] and review["matched_address"]
            assert review["identity_evidence_url"] == data.source_url
            assert review["browser_verified"] is False
            option = HotelBookingOption(
                **HotelOptionInput.model_validate(options[review["provider"]]).model_dump(),
                id=uuid4(),
                status="approved",
                verified_at=now,
                health_status="healthy",
            )
            assert not ready_option(product, option, config, now)
    assert len(approved) == evidence["production"]["new_platform_approvals"] == 7
    westin = next(h for h in evidence["hotels"] if "westin" in h["source_key"])
    official = next(o for o in westin["platform_reviews"] if o["provider"] == "official")
    assert official["status"] == "pending" and official["version"] == 1
    assert official["error_code"] == "service_link_unavailable"
    assert official["health"] == "unchecked" and official["browser_verified"] is False


def test_kyoto_future_closure_is_dated_sourced_and_does_not_become_an_approval():
    evidence, rows = kyoto_five_checkpoint()
    hotel = next(h for h in evidence["hotels"] if "hyatt-regency" in h["source_key"])
    notice = hotel["operating_notice"]
    assert notice["status"] == "future_closure_announced"
    assert notice["announced_on"] == "2026-04-09" and notice["ends_on"] == "2027-05-09"
    assert notice["review_hold"] is True
    assert notice["source_url"] == "https://orix-realestate.co.jp/news/pdf/press_20260409.pdf"
    assert all(o["status"] == "pending" for o in hotel["platform_reviews"])
    updated = [o for o in hotel["platform_reviews"] if o.get("warning_updated")]
    assert {o["provider"] for o in updated} == {"official", "trip_com"}
    source = rows[hotel["source_key"]]
    for option in source["booking_options"]:
        if option["provider"] not in {"official", "trip_com", "rakuten"}:
            continue
        assert notice["ends_on"] in option["identity_note"]
        assert notice["source_url"] in option["identity_note"]
        assert "status" not in option
    assert source["product"]["facts"]["map_verified"] is False
    assert "already closed" in notice["reason"]


def test_kyoto_rakuten_candidates_use_observed_ids_and_remain_pending():
    evidence, rows = kyoto_five_checkpoint()
    expected = {
        "10123456796386",
        "10123456863505",
        "10123456795882",
        "10123456795210",
        "10123456795704",
    }
    found = set()
    for hotel in evidence["hotels"]:
        review = next(o for o in hotel["platform_reviews"] if o.get("new_candidate"))
        option = next(
            o for o in rows[hotel["source_key"]]["booking_options"] if o["provider"] == "rakuten"
        )
        assert option["url"] == review["url"] and option["property_id"] == review["property_id"]
        assert option["url"].endswith("/" + option["property_id"])
        assert option["property_id"] in expected
        found.add(option["property_id"])
        assert option["discovery_status"] == review["discovery_status"] == "found"
        assert review["status"] == "pending" and review["health"] == "unchecked"
        assert review["version"] == 2 and review["browser_verified"] is False
        assert "待審" in option["identity_note"]
    assert found == expected
    assert evidence["production"]["new_hotel_identities"] == 0
    assert evidence["production"]["new_location_approvals"] == 0
    assert evidence["production"]["complete_cities"] == 0
    assert evidence["production"]["config_changed"] is False
    assert evidence["production"]["five_locale_public_hotels"]["kyoto"] == 0
    assert any("10123456795625" in o["url"] for o in evidence["excluded"])
    assert not any(
        o.get("property_id") == "10123456795625"
        for row in rows.values()
        for o in row["booking_options"]
    )


def kyoto_station_checkpoint():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads(
        (directory / "kyoto-station.review-2026-09-08.json").read_text(encoding="utf-8")
    )
    package = json.loads((directory / "kyoto.pending.json").read_text(encoding="utf-8"))
    return evidence, {r["product"]["source_key"]: r for r in package}


def test_kyoto_station_platform_approvals_do_not_bypass_product_identity():
    evidence, rows = kyoto_station_checkpoint()
    config = CatalogConfig(
        public_enabled=True, enabled_destinations=["kyoto"], enabled_kinds=["hotel"]
    )
    now = datetime.now(UTC)
    approved = []
    assert len(evidence["hotels"]) == 5
    for hotel in evidence["hotels"]:
        source = rows[hotel["source_key"]]
        data = ProductInput.model_validate(source["product"])
        product = TravelServiceProduct(**source["product"], id=uuid4(), status="pending")
        assert hotel["product_status"] == "pending"
        assert hotel["map_review_status"] == "not_checked"
        assert not data.facts.map_verified and not data.facts.google_place_id
        assert data.facts.latitude is data.facts.longitude is None
        with pytest.raises(AppError, match="service_identity_required"):
            require_product_review(data)
        options = {o["provider"]: o for o in source["booking_options"]}
        for review in hotel["platform_reviews"]:
            assert review.get("url") == options[review["provider"]].get("url")
            if review["status"] != "approved":
                continue
            approved.append(review)
            assert review["provider"] in {"official", "trip_com"}
            assert review["health"] == "healthy" and review["version"] == 2
            assert review["matched_name"] and review["matched_address"]
            assert review["identity_evidence_url"] == data.source_url
            assert review["browser_verified"] is False
            option = HotelBookingOption(
                **HotelOptionInput.model_validate(options[review["provider"]]).model_dump(),
                id=uuid4(),
                status="approved",
                verified_at=now,
                health_status="healthy",
            )
            assert not ready_option(product, option, config, now)
    assert len(approved) == evidence["production"]["new_platform_approvals"] == 10
    assert evidence["production"]["new_hotel_identities"] == 0
    assert evidence["production"]["new_location_approvals"] == 0
    assert evidence["production"]["complete_cities"] == 0
    assert evidence["production"]["five_locale_public_hotels"]["kyoto"] == 0


def test_kyoto_station_rakuten_ids_are_observed_unique_and_pending():
    evidence, rows = kyoto_station_checkpoint()
    expected = {
        "10123456796201",
        "10123456864974",
        "10123456860018",
        "10123456795701",
        "10123456795968",
    }
    found = set()
    for hotel in evidence["hotels"]:
        review = next(o for o in hotel["platform_reviews"] if o.get("new_candidate"))
        source = next(
            o for o in rows[hotel["source_key"]]["booking_options"] if o["provider"] == "rakuten"
        )
        assert source["url"] == review["url"]
        assert source["url"].rstrip("/").endswith("/" + source["property_id"])
        assert source["property_id"] == review["property_id"]
        assert source["property_id"] in expected
        found.add(source["property_id"])
        assert review["status"] == "pending" and review["version"] == 2
        assert review["health"] == "unchecked" and review["browser_verified"] is False
        assert review["document_freshness"] and review["query"]
        assert "待審" in source["identity_note"] and "status" not in source
    assert found == expected
    all_rakuten = [
        o["property_id"]
        for r in rows.values()
        for o in r["booking_options"]
        if o["provider"] == "rakuten"
    ]
    assert len(all_rakuten) == len(set(all_rakuten)) == 10
    assert evidence["production"]["new_audit_records"] == 15
    assert evidence["production"]["config_changed"] is False


def test_kyoto_station_wrong_branch_and_unresolved_leads_are_not_substituted():
    evidence, rows = kyoto_station_checkpoint()
    excluded = evidence["excluded"][0]
    assert "9-2" in excluded["reason"] and "14-1" in excluded["reason"]
    assert not any(
        o.get("url") == excluded["url"] for r in rows.values() for o in r["booking_options"]
    )
    for research in evidence["unresolved_research"]:
        hotel = next(h for h in evidence["hotels"] if h["source_key"] == research["source_key"])
        review = next(o for o in hotel["platform_reviews"] if o["provider"] == research["provider"])
        assert review["status"] == "pending" and review["browser_verified"] is False
    miyako = rows["editorial:kyoto:miyako-kyoto-hachijo"]
    trip = next(o for o in miyako["booking_options"] if o["provider"] == "trip_com")
    assert (
        trip["property_id"] == "737157" and "/otokuni-district-hotel-detail-737157/" in trip["url"]
    )
    previous, _ = kyoto_five_checkpoint()
    hyatt = next(h for h in previous["hotels"] if "hyatt-regency" in h["source_key"])
    assert hyatt["operating_notice"]["review_hold"]
    assert all(o["status"] == "pending" for o in hyatt["platform_reviews"])


def seoul_links_checkpoint():
    directory = Path(__file__).resolve().parents[3] / "docs/hotel-platforms"
    evidence = json.loads(
        (directory / "seoul-links.review-2026-09-08.json").read_text(encoding="utf-8")
    )
    package = json.loads((directory / "seoul.pending.json").read_text(encoding="utf-8"))
    return evidence, {r["product"]["source_key"]: r for r in package}


def test_seoul_independent_reviews_preserve_prior_naver_identity_and_pending_inputs():
    evidence, rows = seoul_links_checkpoint()
    config = CatalogConfig(
        public_enabled=True, enabled_destinations=["seoul"], enabled_kinds=["hotel"]
    )
    now = datetime.now(UTC)
    approved = []
    assert len(evidence["hotels"]) == 5
    for hotel in evidence["hotels"]:
        source = rows[hotel["source_key"]]
        data = ProductInput.model_validate(source["product"])
        assert not data.facts.map_verified and not data.facts.google_place_id
        assert data.facts.naver_map_url == hotel["prior_naver_evidence"]["candidate_url"]
        assert hotel["prior_naver_evidence"]["status"] == "browser_identity_checked"
        assert hotel["new_location_review"] is False
        with pytest.raises(AppError, match="service_identity_required"):
            require_product_review(data)
        # Production has a separate prior admin location review; the import does not.
        data.facts.map_verified = True
        require_product_review(data)
        product = TravelServiceProduct(**data.model_dump(), id=uuid4(), status="approved")
        options = {o["provider"]: o for o in source["booking_options"]}
        for review in hotel["platform_reviews"]:
            assert review.get("url") == options[review["provider"]].get("url")
            if not review["review_requested"]:
                continue
            passed = review["status"] == "approved"
            option = HotelBookingOption(
                **HotelOptionInput.model_validate(options[review["provider"]]).model_dump(),
                id=uuid4(),
                status=review["status"],
                verified_at=now if passed else None,
                health_status=review["health"],
            )
            assert ready_option(product, option, config, now) is passed
            assert review["matched_name"] and review["matched_address"]
            assert review["browser_verified"] is False
            if passed:
                approved.append(review)
                assert review["provider"] in {"official", "trip_com"}
                assert review["health"] == "healthy" and review["version"] == 2
            else:
                assert review["version"] == 1
                assert review["error_code"] == "service_link_unavailable"
    assert len(approved) == evidence["production"]["new_platform_approvals"] == 6
    assert evidence["production"]["new_hotel_identities"] == 0
    assert evidence["production"]["new_location_approvals"] == 0
    assert evidence["production"]["complete_cities"] == 0


def test_seoul_rakuten_candidates_keep_observed_locale_urls_and_do_not_become_public():
    evidence, rows = seoul_links_checkpoint()
    assert len(evidence["candidate_additions"]) == 2
    assert {c["property_id"] for c in evidence["candidate_additions"]} == {
        "34123457159873",
        "34123457217428",
    }
    for candidate in evidence["candidate_additions"]:
        hotel = next(h for h in evidence["hotels"] if h["source_key"] == candidate["source_key"])
        source = next(
            o for o in rows[hotel["source_key"]]["booking_options"] if o["provider"] == "rakuten"
        )
        review = next(o for o in hotel["platform_reviews"] if o["provider"] == "rakuten")
        assert source["url"] == candidate["url"] == review["url"]
        assert source["url"].endswith("/" + candidate["property_id"] + "/")
        assert source["property_id"] == candidate["property_id"]
        assert review["status"] == "pending" and review["version"] == 2
        assert review["health"] == "unchecked" and review["new_candidate"]
        assert candidate["query"] and candidate["document_freshness"]
        assert "待審" in source["identity_note"] and "status" not in source
    mercure = next(c for c in evidence["candidate_additions"] if "mercure" in c["source_key"])
    assert "/hkg/zh-hk/" in mercure["url"]
    assert "Internal Error" in mercure["document_freshness"]


def test_seoul_unreadable_or_failed_pages_do_not_silently_gain_approval():
    evidence, _ = seoul_links_checkpoint()
    failed = []
    for hotel in evidence["hotels"]:
        for review in hotel["platform_reviews"]:
            if review.get("error_code"):
                failed.append(review)
                assert review["status"] == "pending" and review["browser_verified"] is False
            if review["provider"] == "booking":
                assert review["status"] == "pending" and not review["review_requested"]
            if review["provider"] == "official" and ":l7-" in hotel["source_key"]:
                assert review["status"] == "pending" and not review["review_requested"]
                assert "Pardon Our Interruption" in review["reason"]
    assert len(failed) == evidence["production"]["failed_reviews"] == 3
    assert evidence["production"]["new_audit_records"] == 8
    assert evidence["production"]["five_locale_seoul_public_options_before"] == 1
    assert evidence["production"]["five_locale_seoul_public_options_after"] == 7
    assert evidence["production"]["config_changed"] is False
