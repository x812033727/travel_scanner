"""Create a synthetic 50-row sales exercise and independently specified audit answers."""
import csv
import importlib.util
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "examples/67"
OUT.mkdir(parents=True, exist_ok=True)


def table(name, fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    (OUT / name).write_text(stream.getvalue(), encoding="utf-8", newline="\n")


data = []
for i in range(1, 41):
    data.append({"source_id": f"S{i:03}", "order_id": f"T{i:03}", "date": f"2026-09-{(i-1)%14+1:02}", "product": "cup" if i % 2 else "notebook", "currency": "TWD", "quantity": str((i-1)%3+1), "unit_price": "300" if i % 2 else "80", "kind": "sale", "note": "合成交易"})


def add(number, **changes):
    row = {"source_id": f"S{number:03}", "order_id": f"T{number:03}", "date": "2026-09-12", "product": "cup", "currency": "TWD", "quantity": "2", "unit_price": "300", "kind": "sale", "note": "合成練習"}
    row.update(changes)
    data.append(row)


add(41, **{k: v for k, v in data[4].items() if k != "source_id"})
add(42, unit_price="", note="金額缺失，不能補零")
add(43, date="2026-02-30", note="無效日期")
add(44, date="2026/09/12", note="明確年/月/日，可標準化")
add(45, date="09/10/2026", note="日期次序不明，待確認")
add(46, currency="USD", unit_price="25", note="不同幣別分組，不自行換匯")
add(47, currency="", note="幣別缺失")
add(48, quantity="-1", kind="refund", note="已確認一件退款，保留負值")
add(49, quantity="100", note="已確認團體訂單，不能因大額刪除")
add(50, order_id="T010", product="notebook", unit_price="90", note="與S010同單號但內容不同，兩列隔離")
fields = list(data[0])
table("sales-dirty.csv", fields, data)
reasons = {10: "同單號內容衝突，與S050一起待確認", 41: "完整重複S005，只排除重複副本", 42: "單價缺失", 43: "無效日期", 45: "日期次序不明", 47: "幣別缺失", 50: "同單號內容衝突，與S010一起待確認"}
excluded = [{"source_id": f"S{i:03}", "source_csv_row": i + 1, "reason": reason} for i, reason in reasons.items()]
table("expected-exclusions.csv", list(excluded[0]), excluded)
# The oracle follows the declared transaction specification, not the cleaner's result.
# First 40: cup units 40, notebook units 39. Exclude T010: one notebook.
# Add S044: two cups; S048: minus one cup; S049: one hundred cups.
totals = [
    {"currency": "TWD", "product": "cup", "rows": 23, "quantity": 141, "amount": "42300.00"},
    {"currency": "TWD", "product": "notebook", "rows": 19, "quantity": 38, "amount": "3040.00"},
    {"currency": "USD", "product": "cup", "rows": 1, "quantity": 2, "amount": "50.00"},
]
table("expected-totals.csv", list(totals[0]), totals)
oracle = {"rawRows": 50, "acceptedRows": 43, "excludedRows": 7, "totals": totals, "basis": "40筆基礎資料：前36筆兩種各36件；最後4筆cup 1+3件、notebook 2+1件；隔離T010一件notebook；新增TWD cup 2-1+100件；USD cup 2件，分幣別。"}
(OUT / "expected.json").write_text(json.dumps(oracle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
spec = importlib.util.spec_from_file_location("creative_checks", HERE / "examples/creative_checks.py")
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
result = checks.sales(OUT)
(OUT / "cleaning-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"rows": len(data), "expected": oracle}, ensure_ascii=False))
