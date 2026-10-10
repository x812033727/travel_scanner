// The brief's rule for outcome 3, from the table tally.mjs prints (read on stdin):
// a difference may go on a card only if it is larger than the largest spread of the first
// request inside one arm (n and f each, the larger of the two).
import { readFileSync } from 'node:fs';

const rows = readFileSync(0, 'utf8').split('\n').filter((line) => / \| /.test(line) && !line.startsWith('name |'))
  .map((line) => line.split(' | ')).filter((cells) => cells.length === 19)
  .map((c) => ({ name: c[0], requests: Number(c[11]), first: Number(c[12]), last: Number(c[13]), all: Number(c[14]), cost: Number(c[16]) }));
const by = (prefix) => rows.filter((row) => new RegExp(`^${prefix}\\d$`).test(row.name));
const mean = (list) => list.reduce((a, b) => a + b, 0) / list.length;
const spread = (list) => Math.max(...list) - Math.min(...list);
const n = by('n'); const f = by('f');
const fFirst = f.map((r) => r.first); const nFirst = n.map((r) => r.first);
const fMean = mean(fFirst); const nMean = mean(nFirst);
const limit = Math.max(spread(fFirst), spread(nFirst));
console.log(`f arm first request: ${fFirst.join(', ')} | mean ${fMean.toFixed(1)} | spread ${spread(fFirst)}`);
console.log(`n arm first request: ${nFirst.join(', ')} | mean ${nMean.toFixed(1)} | spread ${spread(nFirst)}`);
console.log(`largest spread inside one arm (the bar a difference must clear): ${limit}`);
const one = (name) => rows.find((row) => row.name === name);
const lines = [
  ['n arm (2 tools, deferred), mean of 3', nMean, mean(n.map((r) => r.requests)), mean(n.map((r) => r.all))],
  ...['w1', 'u1', 'p1', 'e1', 'x1', 'r1'].filter(one).map((name) => [`${name}, 1 run`, one(name).first, one(name).requests, one(name).all]),
];
console.log(`f arm, mean of 3: requests ${mean(f.map((r) => r.requests))} | all requests added up ${mean(f.map((r) => r.all)).toFixed(1)}`);
for (const [label, first, requests, all] of lines) {
  const diff = first - fMean;
  console.log(`${label}: first request ${Number(first).toFixed(1)} | minus the f mean ${diff >= 0 ? '+' : ''}${diff.toFixed(1)} | ${Math.abs(diff) > limit ? 'larger than the bar' : 'NOT larger than the bar'} | requests ${requests} | all requests added up ${Number(all).toFixed(1)} (minus the f mean ${(all - mean(f.map((r) => r.all))).toFixed(1)})`);
}
const w = one('w1'); const u = one('u1');
if (w && u) {
  console.log(`w1 minus the n mean: ${(w.first - nMean).toFixed(1)} | u1 minus w1: ${u.first - w.first} | u1 minus the n mean: ${(u.first - nMean).toFixed(1)}`);
  console.log(`all requests added up: n mean ${mean(n.map((r) => r.all)).toFixed(1)} | w1 ${w.all} | u1 ${u.all} (u1 minus w1 ${u.all - w.all})`);
}
console.log(`total_cost_usd over ${rows.length} rows: ${rows.reduce((a, r) => a + r.cost, 0).toFixed(4)}`);
