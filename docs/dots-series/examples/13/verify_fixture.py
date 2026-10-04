"""Independent integer arithmetic for synthetic input fixtures; never calls dots."""
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def read(name):
    with (BASE / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def totals(rows):
    result = {"orders": len(rows), "units": 0, "gross": 0,
              "discount": 0, "refund": 0, "net": 0,
              "channel_net": {}, "product_net": {}}
    for row in rows:
        units, price, discount, refund = [int(row[key]) for key in
                                         ("units", "unit_price", "discount", "refund")]
        gross = units * price
        net = gross - discount - refund
        for key, value in (("units", units), ("gross", gross),
                           ("discount", discount), ("refund", refund), ("net", net)):
            result[key] += value
        for field in ("channel", "product"):
            bucket = result[field + "_net"]
            bucket[row[field]] = bucket.get(row[field], 0) + net
    assert sum(result["channel_net"].values()) == result["net"]
    assert sum(result["product_net"].values()) == result["net"]
    return result


v1 = read("sales-v1.csv")
changes = read("sales-update-v2.csv")
assert len({row["order_id"] for row in v1}) == len(v1)
assert len({row["order_id"] for row in changes}) == len(changes)
merged = {row["order_id"]: row for row in v1}
merged.update({row["order_id"]: row for row in changes})
expected = json.loads((BASE / "expected-baseline.json").read_text(encoding="utf-8"))
actual = {"v1": totals(v1), "v2": totals(list(merged.values()))}
for version in actual:
    assert actual[version] == expected[version], (version, actual[version])
assert actual["v2"]["net"] - actual["v1"]["net"] == expected["update"]["total_net_difference"]
assert int(merged["O008"]["units"]) == 3
print(json.dumps({"status": "fixture_arithmetic_verified_not_dots_test", **actual}, ensure_ascii=False))
