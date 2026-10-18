// npm test 跑的就是這一支：三個案例，錯一個結束碼就是 1。
import { fare } from '../src/fare.mjs';

const cases = [
  ['A', false, 30],
  ['B', false, 45],
  ['B', true, 23],
];
let failed = 0;
for (const [zone, child, want] of cases) {
  const got = fare(zone, child);
  const mark = got === want ? 'ok  ' : 'FAIL';
  if (got !== want) failed += 1;
  const call = `fare(${zone}, ${child})`;
  console.log(`${mark} ${call} = ${got}, want ${want}`);
}
console.log(failed ? `${failed} failed` : 'all 3 passed');
process.exit(failed ? 1 : 0);
