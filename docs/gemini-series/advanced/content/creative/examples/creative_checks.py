"""Read-only validators for the authored creative exercises. No model calls or file edits."""
import argparse
import csv
import json
import re
from collections import defaultdict
from datetime import date as calendar_date
from decimal import Decimal, InvalidOperation
from pathlib import Path


def rows(path):
    with Path(path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def clean_sales(path):
    raw = rows(path)
    fields = {"source_id", "order_id", "date", "product", "currency", "quantity", "unit_price", "kind", "note"}
    if not raw or any(set(r) != fields or any(v is None for v in r.values()) for r in raw):
        raise ValueError("invalid_csv_shape")
    if len({r["source_id"] for r in raw}) != len(raw) or any(not r["source_id"] or not r["order_id"] for r in raw):
        raise ValueError("missing_or_duplicate_source_id")
    by_order = defaultdict(set)
    keys = sorted(fields - {"source_id", "note"})
    for r in raw:
        by_order[r["order_id"]].add(tuple(r[k] for k in keys))
    accepted, excluded, seen = [], [], set()
    for n, r in enumerate(raw, 2):
        reason = None
        if len(by_order[r["order_id"]]) > 1:
            reason = "conflicting_order"
        elif r["order_id"] in seen:
            reason = "duplicate_copy"
        elif not re.fullmatch(r"\d{4}([-\/])\d{2}\1\d{2}", r["date"]):
            reason = "ambiguous_date"
        else:
            try:
                date = calendar_date.fromisoformat(r["date"].replace("/", "-")).isoformat()
            except ValueError:
                reason = "invalid_date"
            if r["currency"] not in {"TWD", "USD"}:
                reason = "missing_or_unknown_currency"
            elif r["product"] not in {"cup", "notebook"}:
                reason = "unknown_product"
            elif r["kind"] not in {"sale", "refund"}:
                reason = "unknown_transaction_kind"
            else:
                try:
                    quantity = int(r["quantity"])
                    price = Decimal(r["unit_price"])
                    if not price.is_finite() or price < 0 or price != price.quantize(Decimal("0.01")):
                        raise ValueError("invalid price")
                    if quantity == 0 or (r["kind"] == "sale" and quantity < 0) or (r["kind"] == "refund" and quantity > 0):
                        raise ValueError("quantity sign")
                except (ValueError, InvalidOperation):
                    reason = "missing_or_invalid_amount"
        if reason:
            excluded.append({"source_id": r["source_id"], "source_csv_row": n, "reason": reason})
            continue
        seen.add(r["order_id"])
        accepted.append({**r, "date": date, "quantity": quantity, "unit_price": str(price), "amount": str((quantity * price).quantize(Decimal("0.01"))), "source_csv_row": n})
    totals = {}
    for r in accepted:
        key = r["currency"], r["product"]
        total = totals.setdefault(key, {"currency": key[0], "product": key[1], "rows": 0, "quantity": 0, "amount": Decimal(0)})
        total["rows"] += 1
        total["quantity"] += r["quantity"]
        total["amount"] += Decimal(r["amount"])
    return {"rawRows": len(raw), "acceptedRows": len(accepted), "excludedRows": len(excluded), "accepted": accepted, "excluded": excluded, "totals": [{**r, "amount": str(r["amount"].quantize(Decimal("0.01")))} for _, r in sorted(totals.items())], "currencyConversion": False}


def sales(folder):
    folder = Path(folder)
    result = clean_sales(folder / "sales-dirty.csv")
    expected = json.loads((folder / "expected.json").read_text(encoding="utf-8"))
    for key in ["rawRows", "acceptedRows", "excludedRows", "totals"]:
        if result[key] != expected[key]:
            raise ValueError("oracle_mismatch_" + key)
    if {r["source_id"] for r in result["excluded"]} != {r["source_id"] for r in rows(folder / "expected-exclusions.csv")}:
        raise ValueError("exclusion_mismatch")
    return result


def flow_request(folder, model, mode, seconds):
    data = json.loads((Path(folder) / "model-capabilities.json").read_text(encoding="utf-8"))
    if model not in data["models"]:
        raise ValueError("unknown_model_check_current_docs")
    entry = data["models"][model]
    if mode not in {"ingredients", "frames_first_last", "video_edit", "extend"} or not entry[mode]:
        raise ValueError("unsupported_mode")
    durations = entry["ingredients_seconds"] if mode == "ingredients" else ([4, 6, 8, 10] if model.startswith("Gemini Omni") else [4, 6, 8])
    if seconds not in durations or mode == "extend" and seconds != 8:
        raise ValueError("unsupported_duration")
    return {"documentCompatible": True, "checked_on": data["checked_on"], "actualUiVerified": False}


def affected_assets(folder):
    folder = Path(folder)
    before = json.loads((folder / "brief-v1.json").read_text(encoding="utf-8"))["facts"]
    after = json.loads((folder / "brief-v2.json").read_text(encoding="utf-8"))["facts"]
    changed = {key for key in before.keys() | after.keys() if before.get(key) != after.get(key)}
    assets = rows(folder / "asset-register.csv")
    ids = [a["asset_id"] for a in assets]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate_asset_id")
    affected = []
    for asset in assets:
        dependencies = set(asset["fact_ids"].split("|"))
        if not dependencies.issubset(before.keys() | after.keys()):
            raise ValueError("unknown_fact_dependency")
        if dependencies & changed:
            affected.append(asset["asset_id"])
    return {"changedFacts": sorted(changed), "affected": affected, "note": "dependency records require visual review for undeclared facts"}


def pending(folder, name, required):
    folder = Path(folder).resolve()
    records = rows(folder / name)
    if len(records) != required:
        raise ValueError("missing_observation_rows")
    for r in records:
        if r["status"] == "not_run":
            continue
        if r["status"] != "reviewed":
            raise ValueError("unknown_observation_status")
        file = r.get("file") or r.get("output_file") or r.get("output")
        if not file or not r.get("reason", r.get("failure_reason", r.get("decision", ""))).strip():
            raise ValueError("actual_output_and_review_required")
        candidate = (folder / file).resolve()
        if not candidate.is_relative_to(folder) or not candidate.is_file():
            raise ValueError("missing_or_outside_output")
    return {"rows": required, "pending": sum(r["status"] == "not_run" for r in records), "modelGenerationProved": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=["sales", "affected"])
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(sales(args.directory) if args.kind == "sales" else affected_assets(args.directory), ensure_ascii=False, indent=2))
