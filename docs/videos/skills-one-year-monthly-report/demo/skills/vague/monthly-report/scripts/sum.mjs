// 月結報表的算數：讀一個月的 CSV，印出總營收、各品項小計、
// 退貨列與單筆超過 10,000 元的交易。
import { readFileSync } from "node:fs";
const file = process.argv[2];
if (!file) {
  console.error("usage: node sum.mjs data/YYYY-MM.csv");
  process.exit(2);
}
const text = readFileSync(file, "utf8").trim();
const rows = text.split("\n").slice(1).map((line) => {
  const [date, item, qty, unit_price] = line.split(",");
  const amount = Number(qty) * Number(unit_price);
  return { date, item, qty: Number(qty), amount };
});
const total = rows.reduce((sum, row) => sum + row.amount, 0);
const byItem = {};
for (const row of rows) {
  byItem[row.item] = (byItem[row.item] ?? 0) + row.amount;
}
const items = Object.entries(byItem)
  .sort((a, b) => b[1] - a[1])
  .map(([item, amount]) => ({ item, amount }));
const returns = rows.filter((row) => row.qty < 0);
const large = rows.filter((row) => row.amount > 10000);
const out = { total, items, returns, large };
console.log(JSON.stringify(out, null, 2));
