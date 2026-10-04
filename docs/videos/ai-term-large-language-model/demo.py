"""Deterministic fictional evidence demo. No network, model, or account access."""
import argparse
import json

RECORDS = [
    {"id": "L001", "item": "umbrella", "location": "north_counter", "status": "unclaimed"},
    {"id": "L002", "item": "bottle", "location": "east_shelf", "status": "returned"},
    {"id": "L003", "item": "umbrella", "location": "west_basket", "status": "unclaimed"},
    {"id": "L004", "item": "scarf", "location": "south_hook", "status": "unclaimed"},
    {"id": "L005", "item": "cap", "location": "east_shelf", "status": "returned"},
    {"id": "L006", "item": "glove", "location": "west_basket", "status": "unclaimed"},
]


def evidence():
    result = next(record.copy() for record in RECORDS if record["id"] == "L001")
    assert result == {"id": "L001", "item": "umbrella", "location": "north_counter", "status": "unclaimed"}
    return ["fictional_data=true; model_called=false", "L001 | umbrella | north_counter | unclaimed"]


def missing():
    record = next(record for record in RECORDS if record["id"] == "L001")
    assert "owner_phone" not in record
    return ["record=L001; field=owner_phone", "result=UNKNOWN; reason=field_not_in_dataset"]


def count():
    unclaimed = [record for record in RECORDS if record["status"] == "unclaimed"]
    umbrellas = [record for record in unclaimed if record["item"] == "umbrella"]
    assert len(RECORDS) == 6
    assert [record["id"] for record in unclaimed] == ["L001", "L003", "L004", "L006"]
    assert [record["id"] for record in umbrellas] == ["L001", "L003"]
    return ["records=6; returned=2; unclaimed=4", "unclaimed_ids=L001,L003,L004,L006", "unclaimed_umbrellas=2; ids=L001,L003"]


def all_results():
    return ["CASE evidence", *evidence(), "CASE missing", *missing(), "CASE count", *count()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=["evidence", "missing", "count", "all", "data"], nargs="?", default="all")
    args = parser.parse_args()
    if args.case == "data":
        print(json.dumps(RECORDS, ensure_ascii=False, indent=2))
        return
    handlers = {"evidence": evidence, "missing": missing, "count": count, "all": all_results}
    print("\n".join(handlers[args.case]()))


if __name__ == "__main__":
    main()
