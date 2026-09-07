"""Research inputs are validated, not silently approved or counted as published hotels."""

import csv
import io
import json
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


@pytest.mark.parametrize("city,reviewed", [("tokyo", 6), ("osaka", 0), ("taipei", 0), ("seoul", 0)])
def test_pending_content_preserves_prior_identities_and_marks_gaps(city, reviewed):
    path = Path(__file__).resolve().parents[3] / f"docs/hotel-platforms/{city}.pending.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    assert len(rows) == 10
    assert len({r["product"]["source_key"] for r in rows}) == 10
    if city == "seoul":
        assert all(not r["product"]["facts"].get("google_place_id") for r in rows)
        assert sum(bool(r["product"]["facts"].get("naver_map_url")) for r in rows) == 1
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
        assert p.facts.coordinate_source_url == p.facts.source_credits[0].url
        if city == "seoul":
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
            assert record["naver"]["discovery_url"] == product["source_url"]
            assert record["naver"]["candidate_url"] == facts["naver_map_url"]
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


def test_pending_seoul_options_cannot_be_public_even_if_product_were_approved():
    path = Path(__file__).resolve().parents[3] / "docs/hotel-platforms/seoul.pending.json"
    now = datetime.now(UTC)
    config = CatalogConfig(enabled_destinations=["seoul"], enabled_kinds=["hotel"])
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
