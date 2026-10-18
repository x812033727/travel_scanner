// Writes gear-lab/server/stock.tsv (tab-separated, LF, no BOM) and truth.json from the table
// below, or with --check compares what is on disk with what it would write. The data is made up
// for the video: no real shop, no real stock. No session, no model.
// Usage: node <seed>/gen-stock.mjs [--check]
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const ROWS = [
  ['G-108', '行李秤', 'A-03', 2], ['G-121', '登山杖', 'B-11', 3], ['G-134', '防水袋', 'A-09', 14],
  ['G-150', '頸枕', 'C-02', 21], ['G-176', '轉接頭', 'A-01', 46], ['G-205', '冰爪', 'E-04', 5],
  ['G-233', '雪鏡', 'E-06', 1], ['G-248', '保溫瓶', 'C-10', 12], ['G-271', '行動電源', 'A-05', 9],
  ['G-290', '腳架', 'D-02', 6], ['G-317', '睡袋', 'F-01', 8], ['G-352', '營燈', 'D-09', 0],
  ['G-389', '雨衣', 'B-04', 17], ['G-417', '頭燈', 'D-07', 37], ['G-431', '背包套', 'B-08', 11],
  ['G-466', '護膝', 'B-12', 3], ['G-502', '折疊椅', 'F-05', 4], ['G-538', '望遠鏡', 'D-11', 7],
  ['G-590', '潛水鏡', 'E-09', 2], ['G-611', '手機防水袋', 'A-07', 25], ['G-647', '暖暖包', 'C-06', 60],
  ['G-683', '登山繩', 'F-08', 5], ['G-705', '相機雨套', 'D-04', 10], ['G-742', '充氣枕', 'C-03', 13],
];
const ASKED = 'G-417';
const BELOW = 3;
const row = ROWS.find(([code]) => code === ASKED);
const files = {
  'gear-lab/server/stock.tsv': `${['code\tname\tshelf\tleft', ...ROWS.map((each) => each.join('\t'))].join('\n')}\n`,
  'truth.json': `${JSON.stringify({
    asked: { code: ASKED, name: row[1], shelf: row[2], left: row[3] },
    below: BELOW,
    low: ROWS.filter((each) => each[3] < BELOW).map(([code, name, , left]) => ({ code, name, left })),
    exactlyAtTheLimit: ROWS.filter((each) => each[3] === BELOW).map(([code]) => code),
    missing: 'G-999',
    codes: ROWS.map(([code]) => code),
    shelves: ROWS.map(([, , shelf]) => shelf),
  }, null, 2)}\n`,
};
let differs = false;
for (const [name, text] of Object.entries(files)) {
  const path = join(seed, name);
  if (process.argv.includes('--check')) {
    const same = existsSync(path) && readFileSync(path, 'utf8') === text;
    console.log(`${same ? 'same' : 'DIFFERENT'}  ${name}`);
    if (!same) differs = true;
  } else {
    writeFileSync(path, text);
    console.log(`wrote ${name} (${text.length} characters)`);
  }
}
console.log(`${ROWS.length} rows | below ${BELOW}: ${ROWS.filter((each) => each[3] < BELOW).map(([code]) => code).join(' ')} | exactly ${BELOW}: ${ROWS.filter((each) => each[3] === BELOW).map(([code]) => code).join(' ')}`);
process.exitCode = differs ? 1 : 0;
