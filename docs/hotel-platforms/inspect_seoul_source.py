"""Read the public KOGL-1 lodging CSV; print selected facts, never import/approve.

The download form is public on OA-16044's Sheet tab. The page explicitly documents
EPSG:5174. Do not substitute older mirrors' EPSG:2097 or persist the complete CSV.
Run with: uv run --with pyproj python ../../docs/hotel-platforms/inspect_seoul_source.py
"""

import argparse
import csv
import io
import json
import math
import sys
from pathlib import Path

import httpx

DIRECTORY = Path(__file__).resolve().parent


def projected_pair(x, y):
    pair = float(x), float(y)
    if not all(math.isfinite(value) for value in pair):
        raise ValueError("Finite source coordinates required")
    return pair


def transform_pair(x, y):
    # Research-only dependency: never add a projection package to the serving API.
    from pyproj import Transformer

    transform = Transformer.from_crs("EPSG:5174", "EPSG:4326", always_xy=True)
    longitude, latitude = transform.transform(*projected_pair(x, y), errcheck=True)
    if not (37 < latitude < 38 and 126 < longitude < 128):
        raise ValueError("Selected permit is outside Seoul; check axis order and CRS")
    return round(latitude, 7), round(longitude, 7)


def selected_facts(rows, permit_ids):
    selected = []
    seen = set()
    for row in rows:
        permit_id = row.get("관리번호")
        if permit_id not in permit_ids:
            continue
        if permit_id in seen:
            raise ValueError(f"Duplicate permit identity: {permit_id}")
        if row.get("영업상태코드") != "01":
            raise ValueError(f"Permit needs status review: {permit_id}")
        seen.add(permit_id)
        x, y = row.get("좌표정보(X)"), row.get("좌표정보(Y)")
        latitude, longitude = transform_pair(x, y)
        selected.append(
            {
                "permit_id": permit_id,
                "name": row["사업장명"],
                "address": row["도로명주소"],
                "x": x,
                "y": y,
                "latitude": latitude,
                "longitude": longitude,
            }
        )
    if missing := permit_ids - seen:
        raise ValueError(f"Missing selected permit identities: {sorted(missing)}")
    return selected


def verify_saved():
    """Verify only saved licensed facts. No provider, network or database calls."""
    evidence = json.loads((DIRECTORY / "seoul.evidence.json").read_text(encoding="utf-8"))
    assert evidence["source_crs"] == "EPSG:5174"
    assert evidence["target_crs"] == "EPSG:4326" and evidence["always_xy"] is True
    package = json.loads((DIRECTORY / "seoul.pending.json").read_text(encoding="utf-8"))
    products = {row["product"]["source_key"]: row["product"] for row in package}
    assert len(products) == len(package) == len(evidence["hotels"]) == 10
    assert set(products) == {hotel["source_key"] for hotel in evidence["hotels"]}
    for hotel in evidence["hotels"]:
        pair = transform_pair(hotel["x"], hotel["y"])
        assert pair == (hotel["latitude"], hotel["longitude"]), hotel["permit_id"]
        facts = products[hotel["source_key"]]["facts"]
        assert pair == (facts["latitude"], facts["longitude"]), hotel["source_key"]
    return len(products)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify-saved", action="store_true", help="Offline coordinate verification"
    )
    args = parser.parse_args()
    if args.verify_saved:
        print(f"Verified {verify_saved()} saved coordinate transforms; no network/import/approval.")
        return
    evidence = json.loads((DIRECTORY / "seoul.evidence.json").read_text(encoding="utf-8"))
    permit_ids = {hotel["permit_id"] for hotel in evidence["hotels"]}
    response = httpx.post(
        "https://datafile.seoul.go.kr/bigfile/iot/sheet/csv/download.do",
        data={
            "infId": "OA-16044",
            "srvType": "S",
            "serviceKind": "1",
            "pageNo": "1",
            "ssUserId": "SAMPLE_VIEW",
            "strWhere": "",
            "strOrderby": "",
        },
        timeout=30,
        headers={"User-Agent": "Mokaair-Hotel-Catalog-Review/1.0 (+https://mokaair.com)"},
    )
    response.raise_for_status()
    rows = csv.DictReader(io.StringIO(response.content.decode("cp949")))
    print(json.dumps(selected_facts(rows, permit_ids), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
