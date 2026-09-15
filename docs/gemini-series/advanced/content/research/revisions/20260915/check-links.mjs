import assert from 'node:assert/strict';
import { mkdtempSync, cpSync, copyFileSync, readFileSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkPacks } from '../../../../../../../tools/gemini-series.mjs';
import { draftCatalogue } from '../../../../platform/release-contract.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../../../..');
// Keep the separate temporary check workspace; never add reference packs to the deliverable.
const workspace = mkdtempSync(path.join(os.tmpdir(), 'gemini-revision-check-'));
cpSync(path.join(here, 'output'), workspace, { recursive: true });
const series = draftCatalogue(root);
const slugs = series.articles.filter(a => [57].includes(a.number)).map(a => a.slug);
const references = series.articles.filter(a => [56, 58].includes(a.number)).map(a => a.slug);
for (const slug of references) {
  const rel = path.join('apps/api/app/guides/content', slug + '.json');
  copyFileSync(path.join(root, rel), path.join(workspace, rel));
  assert.deepEqual(readFileSync(path.join(root, rel)), readFileSync(path.join(workspace, rel)));
}
const result = checkPacks(series, workspace, { phase: 'advanced', slugs });
assert.deepEqual(result.errors, []);
const report = { status: 'passed', revisedSlugs: slugs, unchangedReferenceSlugs: references, published: false };
writeFileSync(path.join(here, 'link-check.json'), JSON.stringify(report, null, 2) + '\n');
console.log('Lesson 57 revised pack: catalogue, body length, assets and internal links passed.');
