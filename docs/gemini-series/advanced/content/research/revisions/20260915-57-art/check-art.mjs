import assert from 'node:assert/strict';
import { mkdtempSync, cpSync, copyFileSync, readFileSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkPacks } from '../../../../../../../tools/gemini-series.mjs';
import { draftCatalogue } from '../../../../platform/release-contract.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../../../..');
const workspace = mkdtempSync(path.join(os.tmpdir(), 'gemini57-art-check-'));
cpSync(path.join(here, '../20260915/output'), workspace, { recursive: true });
cpSync(path.join(here, 'output'), workspace, { recursive: true });
const series = draftCatalogue(root);
const references = series.articles.filter(a => [56, 58].includes(a.number)).map(a => a.slug);
for (const slug of references) {
  const rel = path.join('apps/api/app/guides/content', slug + '.json');
  copyFileSync(path.join(root, rel), path.join(workspace, rel));
  assert.deepEqual(readFileSync(path.join(root, rel)), readFileSync(path.join(workspace, rel)));
}
const result = checkPacks(series, workspace, { phase: 'advanced', slugs: ['notebooklm-source-versioning'] });
assert.deepEqual(result.errors, []);
writeFileSync(path.join(here, 'link-check.json'), JSON.stringify({
  status: 'passed', scope: 'Full lesson 57 candidate with isolated SVG overlay applied', published: false,
}, null, 2) + '\n');
console.log('Lesson 57 full pack with diagram overlay passed asset, content and link checks.');
