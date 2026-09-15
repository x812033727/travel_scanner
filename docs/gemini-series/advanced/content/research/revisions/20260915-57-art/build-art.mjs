import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import sharp from 'sharp';

const here = path.dirname(fileURLToPath(import.meta.url));
const previous = path.join(here, '../20260915');
const relative = 'output/apps/web/public/guides/notebooklm-source-versioning/diagram-1.svg';
const review = JSON.parse(readFileSync(path.join(previous, 'review.json'), 'utf8'));
const hash = data => createHash('sha256').update(data).digest('hex');
const source = readFileSync(path.join(previous, relative));
assert.equal(hash(source), review.files.find(f => f.path === relative).sha256);
const oldFooter = '文件已查；真實同步與回答待驗';
const newFooter = '手動同步與引用已驗；保留舊產出';
assert.equal(source.toString().split(oldFooter).length, 2);
const revised = source.toString().replace(oldFooter, newFooter);
const output = path.join(here, relative);
mkdirSync(path.dirname(output), { recursive: true });
writeFileSync(output, revised);
const visual = path.join(here, 'visual');
mkdirSync(visual, { recursive: true });
for (const [name, width] of [['diagram-desktop.png', 1600], ['diagram-mobile.png', 360]]) {
  await sharp(output).resize({ width }).png().toFile(path.join(visual, name));
}
assert.deepEqual(source, readFileSync(path.join(previous, relative)));
const files = [relative, 'visual/diagram-desktop.png', 'visual/diagram-mobile.png'];
writeFileSync(path.join(here, 'review.json'), JSON.stringify({
  date: '2026-09-15',
  scope: 'Lesson 57 diagram footer only; apply after the full 20260915 revision.',
  previousRevisionUnchanged: true,
  previousDiagramSha256: hash(source),
  previousReceiptSha256: hash(readFileSync(path.join(previous, 'review.json'))),
  footer: newFooter,
  visualReview: 'See visual-review.json; rendering alone does not prove readability.',
  published: false,
  files: files.map(file => ({ path: file, sha256: hash(readFileSync(path.join(here, file))) })),
}, null, 2) + '\n');
console.log('Built isolated lesson 57 footer overlay; previous revision unchanged.');
