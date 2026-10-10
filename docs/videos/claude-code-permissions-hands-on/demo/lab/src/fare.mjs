// fare-desk：照費率表算票價。
import { readFileSync } from 'node:fs';

const table = new URL('../data/rates.csv', import.meta.url);
const rows = readFileSync(table, 'utf8').trim().split('\n')
  .slice(1).map((line) => line.split(','));

// 回傳某一區的票價；兒童半價，不足一元算一元。
export function fare(zone, child = false) {
  const row = rows.find(([name]) => name === zone);
  if (!row) throw new Error(`unknown zone: ${zone}`);
  const full = Number(row[1]);
  return child ? Math.floor(full / 2) : full;
}
