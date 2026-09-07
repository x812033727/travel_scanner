"""Validate a pending research package and print admin CSV; never writes to a database."""

import csv
import json
import sys
from pathlib import Path

from app.travel_services.schemas import HotelOptionInput, ProductInput


def main():
    # Windows redirected stdout otherwise defaults to cp1252 and loses Asian names.
    sys.stdout.reconfigure(encoding="utf-8")
    rows = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert len({r["product"]["source_key"] for r in rows}) == len(rows)
    writer = csv.DictWriter(sys.stdout, fieldnames=["source_key", "kind", "destination_id", "title",
        "source_url", "names_json", "facts", "booking_options"])
    writer.writeheader()
    for row in rows:
        product = ProductInput.model_validate(row["product"])
        options = [HotelOptionInput.model_validate(o) for o in row["booking_options"]]
        assert len({o.provider for o in options}) == len(options)
        assert product.kind == "hotel" and product.facts.reference_price is None
        data = product.model_dump(mode="json")
        data["facts"].pop("hotel_links", None)
        for key in ("facts", "names_json"):
            data[key] = json.dumps(data[key], ensure_ascii=False)
        writer.writerow({**data, "booking_options": json.dumps([o.model_dump(mode="json") for o in options], ensure_ascii=False)})


if __name__ == "__main__":
    main()
