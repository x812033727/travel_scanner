#!/usr/bin/env node
// Read-only check for the isolated B18 Row10b source-review candidate.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const pre = path.dirname(here);
const repo = path.resolve(here, '../../../../..');
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const read = (file) => readFileSync(file);
const pinned = {
  row: '6c2eb6172d0afc6d5c92a91736cf1ad606ea3302d904c749d42d1b74533b14bc',
  story: 'fbcff4985abae065811ff41cb234ac4190fd22cc8129e03f43048d5dd42af665',
  script: '73236441aebc92e804436fd9371a3044a27e5decdd7438905459ef214023768f',
  phase4_manifest: 'efdf3994152db18892d70c35f6ae10ba3f1d4a9076078922a8a988ee0bbd7422',
  phase4_editorial_review: '52172dd22d2a0d349bea7ff7568cbaa2aecef5ab61d2929ad82048df967d745e',
};
const rowFile = path.join(pre, 'B18-route-b-row10b-candidate-20261017/B18.json');
const phase4 = path.join(pre, 'B18-route-b-phase4-candidate-20261017');
assert.equal(sha(read(rowFile)), pinned.row, 'Row10b bytes changed');
assert.equal(sha(read(path.join(phase4, 'B18.md'))), pinned.script, 'Phase4 script changed');
assert.equal(sha(read(path.join(phase4, 'sha256.json'))), pinned.phase4_manifest, 'Phase4 manifest changed');
assert.equal(sha(read(path.join(pre, 'B18-route-b-phase4-full-editorial-review-20261017.md'))), pinned.phase4_editorial_review, 'Phase4 editorial review changed');

const { STORY_KEYS, storyHash, storyProblems, reviewProblems } = await import(
  pathToFileURL(path.join(repo, 'tools/video/story-plans/plan.mjs')).href
);
const row = JSON.parse(read(rowFile));
const story = Object.fromEntries(STORY_KEYS.map((key) => [key, row[key]]));
const review = JSON.parse(read(path.join(here, 'review-candidate.json')));
assert.deepEqual(storyProblems(story, 'B18'), [], 'Row10b schema failed');
assert.equal(storyHash(story), pinned.story, 'Row10b canonical hash changed');
assert.equal(row.sources.length, 6);
assert.equal(row.must_verify.length, 10);
assert.deepEqual(review.reviewer_only, [4]);
assert.equal(review.sources_opened, 6);
assert.deepEqual(reviewProblems(review, story, 'B18'), [], 'review format/hash failed');
assert(row.caveats.length + 2 + review.notes.length <= 800, 'compiled caveats exceed 800');

// This source-only receipt does not assert a media or worker-stage PASS.
console.log(`PASS_OFFLINE_ROW_SOURCE_ONLY_INTEGRATION_HOLD story=${pinned.story} compiled_caveats=${row.caveats.length + 2 + review.notes.length}/800`);
