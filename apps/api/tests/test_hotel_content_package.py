"""Research inputs are validated, not silently approved or counted as published hotels."""

import json
from pathlib import Path

import pytest

from app.travel_services.schemas import HotelOptionInput, ProductInput
from app.travel_services.service import require_product_review


@pytest.mark.parametrize("city,reviewed", [("tokyo", 6), ("osaka", 0), ("taipei", 0)])
def test_pending_content_preserves_prior_identities_and_marks_gaps(city, reviewed):
    path = Path(__file__).resolve().parents[3] / f"docs/hotel-platforms/{city}.pending.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    assert len(rows) == 10
    assert len({r["product"]["source_key"] for r in rows}) == 10
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
        # Synthetic review only validates coordinates/area/identity syntax, not actual approval.
        p.facts.map_verified = True
        require_product_review(p)


def test_osaka_source_reversed_columns_are_documented_not_swapped_in_product():
    path = Path(__file__).resolve().parents[3] / "docs/hotel-platforms/osaka.pending.json"
    for row in json.loads(path.read_text(encoding="utf-8")):
        facts = row["product"]["facts"]
        assert 34 < facts["latitude"] < 35
        assert 135 < facts["longitude"] < 136
        assert "欄位" in facts["source_credits"][0]["changes"]
