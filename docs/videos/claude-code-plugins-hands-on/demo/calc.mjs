// What a small number of runs can and cannot show. Plain arithmetic, no session, no model.
// Usage: node <seed>/calc.mjs

// 1. If the file made no difference, how often would k successes out of 2n runs all land in
//    the n runs that had the file? One way out of C(2n, n) (Fisher's exact test, one-sided).
const choose = (n, k) => {
  let value = 1;
  for (let i = 1; i <= k; i += 1) value = (value * (n - k + i)) / i;
  return Math.round(value);
};
console.log('all-or-nothing split: with the file n of n, without it 0 of n');
for (const n of [2, 3, 4, 5]) {
  const ways = choose(2 * n, n);
  console.log(`  n = ${n}: 1 way in ${ways} (${(100 / ways).toFixed(1)}%) if the file made no difference`);
}

// 2. n followed out of n: the lowest follow rate that would still give n of n at least 5% of
//    the time is 0.05 ** (1 / n) (the one-sided 95% lower bound, Clopper-Pearson).
console.log('n of n followed: the follow rate is at least this (95% confidence)');
for (const n of [1, 3, 5, 10, 20, 29, 59, 299]) {
  console.log(`  ${String(n).padStart(3)} of ${String(n).padEnd(3)}: at least ${(100 * 0.05 ** (1 / n)).toFixed(1)}%`);
}

// 3. The other way round: how many runs in a row, all followed, before a rate can be claimed.
console.log('runs in a row, all followed, needed to claim a follow rate (95% confidence)');
for (const rate of [0.5, 0.8, 0.9, 0.95, 0.99]) {
  console.log(`  ${(rate * 100).toFixed(0)}%: ${Math.ceil(Math.log(0.05) / Math.log(rate))} runs`);
}
