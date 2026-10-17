#!/usr/bin/env node
// Rebuild a narrow offline B18 source-binding successor; no host or paid calls.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.resolve(here, '../B18-court-pdf-split-candidate-20261017');
const pilot = path.resolve(here, '../..');
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const parentManifestSha = '87d9ee2fafe2b579dad9dd496391e31d5db585054abf89da380edfd345b959f4';
const sha = (data) => crypto.createHash('sha256').update(data).digest('hex');
const canonical = (data) => JSON.stringify(data, null, 2) + '\n';
const read = (file) => fs.readFileSync(path.join(parent, file));
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
assert.equal(sha(read('sha256.json')), parentManifestSha, 'parent manifest changed');
for (const [file, hash] of Object.entries(JSON.parse(read('sha256.json')).files)) {
  assert.equal(sha(read(file)), hash, 'parent file changed: ' + file);
}

const oldRow = JSON.parse(read('B18.json'));
const activeRow = JSON.parse(fs.readFileSync(path.join(pilot, 'episodes/B18.json')));

const oldSeries = JSON.parse(read('series-adoption.json'));
const oldCoverage = JSON.parse(read('claim-coverage.json'));
const oldChapters = Object.fromEntries(keys.map((key) => [key, JSON.parse(read('remapped-chapters/' + key + '.json'))]));
assert.equal(oldRow.must_verify.length, 10, 'unexpected fact count');
assert.equal(oldCoverage.scene_claims.length, 65, 'unexpected scene claim count');
assert.deepEqual(oldRow.must_verify[4].sources, [3]);
assert.deepEqual(oldSeries.plan.must_verify, oldRow.must_verify);

const oldFact = oldRow.must_verify[4].claim;
const newFact = '法院判決理由認定第579776號實用新案於1972年因存續期間屆滿而消滅；判決並認定此後已有許多與原告無關的企業經營輸送帶壽司店。這只涉及該特定權利，不能推定所有權利同時到期，或其他店只因期滿才出現。';
assert.equal(activeRow.must_verify[4].claim, newFact, 'active B18 fact 4 is not the reviewed successor');
assert.deepEqual({ ...activeRow, must_verify: activeRow.must_verify.map((fact, index) => index === 4 ? { ...fact, claim: oldFact } : fact) }, oldRow, 'active B18 row drifted beyond this reviewed successor');
assert.equal(oldFact, '法院判決理由認定「コンベヤ附調理食台」實用新案第579776號於1962年登錄，1972年因存續期間屆滿而消滅；判決並認定此後已有許多與原告無關的企業經營輸送帶壽司店。這只涉及該特定權利，不能推定所有權利同時到期，或其他店只因期滿才出現。');
const row = structuredClone(oldRow);
row.must_verify[4].claim = newFact;
const series = structuredClone(oldSeries);
series.plan.must_verify[4].claim = newFact;
const chapters = structuredClone(oldChapters);
const byId = Object.fromEntries(keys.flatMap((key) => chapters[key].claims.map((claim) => [claim.id, claim])));
assert.deepEqual([byId.e6.source, byId.e6.fact, byId.e7.source, byId.e7.fact], [2, 4, 3, 4]);
byId.e6.fact = null;
byId.e7.source = 2;
byId.e7.fact = null;
assert.deepEqual(['h7', 't7', 't8'].map((id) => [byId[id].source, byId[id].fact]), [[3, 4], [3, 4], [3, 4]]);
const coverage = structuredClone(oldCoverage);
coverage.status = 'OFFLINE_PROPOSED_READABLE_REGISTRATION_SOURCE_SPLIT_ONLY';
coverage.parent_candidate_manifest_sha256 = parentManifestSha;
coverage.row_to_storyboard_facts[4].scene_claim_ids = ['h7', 't7', 't8'];
for (const id of ['e6', 'e7']) {
  const item = coverage.scene_claims.find((claim) => claim.id === id);
  assert(item, 'missing coverage ' + id);
  item.source_index = 2;
  item.proposed_row_fact_index = null;
  item.coverage = 'direct_scene_source_only';
}

const oldRowRestored = structuredClone(row);
oldRowRestored.must_verify[4].claim = oldFact;
assert.deepEqual(oldRowRestored, oldRow, 'row changed beyond fact 4 wording');
const oldSeriesRestored = structuredClone(series);
oldSeriesRestored.plan.must_verify[4].claim = oldFact;
assert.deepEqual(oldSeriesRestored, oldSeries, 'series changed beyond fact 4 wording');
let scenes = 0, lines = 0, claims = 0;
for (const key of keys) {
  const before = oldChapters[key];
  const after = chapters[key];
  scenes += after.scenes.length;
  lines += after.scenes.flatMap((scene) => scene.lines || []).length;
  claims += after.claims.length;
  assert.deepEqual(after.scenes, before.scenes, key + ': scene/narration drift');
  const restored = structuredClone(after);
  for (const claim of restored.claims) {
    const prior = before.claims.find((item) => item.id === claim.id);
    if (claim.id === 'e6' || claim.id === 'e7') {
      claim.source = prior.source;
      claim.fact = prior.fact;
    }
    assert.equal(claim.verdict, 'UNCHECKED', claim.id + ': verdict changed');
    const mapped = coverage.scene_claims.find((item) => item.id === claim.id);
    assert(mapped, claim.id + ': missing coverage');
    assert.equal(mapped.source_index, after.claims.find((item) => item.id === claim.id).source);
    assert.equal(mapped.proposed_row_fact_index, after.claims.find((item) => item.id === claim.id).fact);
  }
  assert.deepEqual(restored, before, key + ': extra chapter change');
}
assert.deepEqual([scenes, lines, claims], [85, 88, 65]);
assert.deepEqual(coverage.scene_claims.map((claim) => claim.claim), oldCoverage.scene_claims.map((claim) => claim.claim));
assert.deepEqual(coverage.row_to_storyboard_facts[4].row_sources, [3]);
for (const mapping of coverage.row_to_storyboard_facts) {
  assert.deepEqual(mapping.row_sources, row.must_verify[mapping.row_fact_index].sources);
  assert.deepEqual([...mapping.scene_claim_ids].sort(), coverage.scene_claims.filter((claim) => claim.proposed_row_fact_index === mapping.row_fact_index).map((claim) => claim.id).sort());
}

const { STORY_KEYS, storyHash, storyProblems, reviewProblems } = await import(pathToFileURL(path.join(root, 'tools/video/story-plans/plan.mjs')).href);
const story = Object.fromEntries(STORY_KEYS.map((key) => [key, row[key]]));
assert.deepEqual(storyProblems(story, 'B18'), []);
const oldReviewBytes = read('reviews/B18.json');
assert.equal(sha(oldReviewBytes), 'd61ff84d1f91a25787727d625e9c04cbbb31803b95f4658e2eb8669061d19b85', 'parent review drift');
const oldReview = JSON.parse(oldReviewBytes);
assert(reviewProblems(oldReview, story, 'B18').some((problem) => problem.includes('story changed after this review')), 'old review unexpectedly still valid');
const files = new Map([
  ['B18.json', canonical(row)],
  ['series-adoption.json', canonical(series)],
  ['claim-coverage.json', canonical(coverage)],
]);
for (const key of keys) files.set('remapped-chapters/' + key + '.json', canonical(chapters[key]));
files.set('verification.json', canonical({
  schema_version: 1,
  status: 'PASS_OFFLINE_STRUCTURE_ONLY_INDEPENDENT_REVIEW_PENDING',
  parent_candidate_manifest_sha256: parentManifestSha,
  canonical_story_sha256: storyHash(story),
  scene_count: scenes,
  narration_line_count: lines,
  scene_claim_count: claims,
  changed_row_fact_indices: [4],
  changed_scene_metadata_ids: ['e6', 'e7'],
  all_scene_claims_unchecked: true,
  old_row_review_invalid: true,
  independent_review_complete: false,
  import_approved: false,
  paid_calls: 0,
  rendered_video: false,
}));
for (const [name, content] of files) {
  const file = path.join(here, name);
  if (mode === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, content);
  } else {
    assert.equal(fs.readFileSync(file, 'utf8'), content, 'output drift: ' + name);
  }
}
const manifest = { schema_version: 1, parent_candidate_manifest_sha256: parentManifestSha,
  files: Object.fromEntries([...files].map(([name, content]) => [name, sha(content)])),
  README_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  build_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))) };
const manifestFile = path.join(here, 'sha256.json');
if (mode === '--write') fs.writeFileSync(manifestFile, canonical(manifest));
else assert.equal(fs.readFileSync(manifestFile, 'utf8'), canonical(manifest), 'manifest drift');
console.log(JSON.stringify({ status: 'PASS_OFFLINE_CANDIDATE_ONLY', mode, story_sha256: storyHash(story), files: files.size, scenes, lines, claims }));