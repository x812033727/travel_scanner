#!/usr/bin/env node
// Assemble a local candidate only. Never imports or updates active stories.json.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { STORY_KEYS, storyHash, storyProblems, reviewProblems } from '../../../../tools/video/story-plans/plan.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode));
const sha = value => createHash('sha256').update(value).digest('hex');
const canonical = value => `${JSON.stringify(value, null, 2)}\n`;
const read = name => readFileSync(path.join(here, name));
const pins = {
  '../stories.json': 'c02fa490725c169c5cb84c0bf05ae9afa1a0c9bac65d8e17d7c602aafed9871b',
  'B18-route-b-row10c-phase4-candidate-20261017/B18.json': '6c2eb6172d0afc6d5c92a91736cf1ad606ea3302d904c749d42d1b74533b14bc',
  'B18-route-b-row10c-phase4-candidate-20261017/sha256.json': '4222dbc887f3d9caf2e6299f48127f1f373fa58e5cf93a7dc36fcd95216f9e32',
  'B18-route-b-row10c-phase4-candidate-20261017/INDEPENDENT-ROUTE-REVIEW.md': 'dbea4ddcf0d84b8991b1a672e6fbde00b1ef1cb06b1ea7d9b80a67dfabaf29d7',
  'B18-row10b-offline-source-review-20261017/review-candidate.json': 'e0ebf025d25b2d841727da1d219e6a9a864506eb1ccda73b5dc1ea0dc31cd949',
};
for (const [name, hash] of Object.entries(pins)) assert.equal(sha(read(name)), hash, `input drift: ${name}`);
const active = JSON.parse(read('../stories.json'));
assert.equal(active.stories.length, 2);
const row = JSON.parse(read('B18-route-b-row10c-phase4-candidate-20261017/B18.json'));
const review = JSON.parse(read('B18-row10b-offline-source-review-20261017/review-candidate.json'));
const story = Object.fromEntries(STORY_KEYS.map(key => [key, row[key]]));
assert.deepEqual(storyProblems(story, 'B18'), []);
assert.deepEqual(reviewProblems(review, story, 'B18'), []);
assert.equal(storyHash(story), 'fbcff4985abae065811ff41cb234ac4190fd22cc8129e03f43048d5dd42af665');
assert.deepEqual(review.reviewer_only, [4]);
row.must_verify = row.must_verify.map((fact, i) => i === 4 ? { ...fact, reviewer_only: true } : fact);
row.caveats = [row.caveats.trim(), review.notes.trim()].join('\n\n');
assert(row.caveats.length <= 800);
assert.equal(row.slug, 'story-conveyor-belt-sushi-v2');
assert.equal(row.number, 2);
const candidate = structuredClone(active);
candidate.stories[1] = row;
assert.equal(canonical(candidate.stories[0]), canonical(active.stories[0]), 'A01 compiled row changed');
assert.equal(canonical(candidate.series), canonical(active.series), 'series changed');
const name = 'B18-phase4-stories-import-candidate-20261017.json';
const output = canonical(candidate);
const receipt = {
  status: 'OFFLINE_IMPORT_CANDIDATE_ONLY_HOLD',
  inputs: pins,
  output_file: name,
  output_sha256: sha(output),
  a01_compiled_row_unchanged: true,
  series_unchanged: true,
  b18_story_sha256: storyHash(story),
  b18_reviewer_only: [4],
  b18_compiled_caveats_characters: row.caveats.length,
  worker_reference_updated: false,
  phase4_authored_chapters_adopted: false,
  formal_worker_claims_reviewed: false,
  host_imported: false,
  paid_calls: 0,
};
for (const [file, bytes] of [[name, output], ['B18-phase4-import-candidate-receipt-20261017.json', canonical(receipt)]]) {
  if (mode === '--write') writeFileSync(path.join(here, file), bytes);
  else assert.equal(read(file).toString('utf8'), bytes, `candidate drift: ${file}`);
}
console.log(JSON.stringify(receipt));
