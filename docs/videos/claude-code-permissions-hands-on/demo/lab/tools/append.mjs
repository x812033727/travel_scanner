// 示範用：自己開檔，在費率表最後加一列。
import { appendFileSync } from 'node:fs';

const table = new URL('../data/rates.csv', import.meta.url);
appendFileSync(table, 'Z,1\n');
console.log('append.mjs: added one row to data/rates.csv');
