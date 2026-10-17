#!/usr/bin/env node
// Deterministic offline B18 citation-pointer successor. Never writes the parent or active inputs.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.resolve(here, '../B18-readable-registration-candidate-20261017');
const pilot = path.resolve(here, '../..');
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const parentManifestSha = '1838bc925f6647776803129c177c286ac0493f8a0aaeee8ecc1aae8d02364044';
const expectedStorySha = 'da692f3833f3d5448e3ec7603f0549a4f9b1afe2828c00aa8ee657618584a5e1';
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');

const sha = (data) => crypto.createHash('sha256').update(data).digest('hex');
const canonical = (data) => JSON.stringify(data, null, 2) + '\n';
const readParent = (name) => fs.readFileSync(path.join(parent, name));
const parentManifestBytes = readParent('sha256.json');
assert.equal(sha(parentManifestBytes), parentManifestSha, 'parent manifest changed');
const parentManifest = JSON.parse(parentManifestBytes);
for (const [name, hash] of Object.entries(parentManifest.files)) {
  assert.equal(sha(readParent(name)), hash, 'parent file changed: ' + name);
}
assert.equal(sha(readParent('README.md')), parentManifest.README_sha256, 'parent README changed');
assert.equal(sha(readParent('build.mjs')), parentManifest.build_sha256, 'parent builder changed');

const rowBytes = readParent('B18.json');
const reviewBytes = readParent('reviews/B18.json');
const seriesBytes = readParent('series-adoption.json');
const row = JSON.parse(rowBytes);
const review = JSON.parse(reviewBytes);
const series = JSON.parse(seriesBytes);
assert.deepEqual(series.plan.must_verify, row.must_verify, 'series and row fact lists differ');
assert.equal(row.must_verify.length, 10, 'unexpected B18 fact count');
assert.equal(row.sources[0].url, 'https://j-net21.smrj.go.jp/special/expo1970/20231113.html');
assert.deepEqual(row.must_verify[4].sources, [3], 'court-only fact changed');
assert.equal(sha(fs.readFileSync(path.join(pilot, 'episodes/B18.json'))), sha(rowBytes), 'active row drifted');
assert.equal(sha(fs.readFileSync(path.join(pilot, 'episodes/reviews/B18.json'))), sha(reviewBytes), 'active review drifted');

const beforeChapters = Object.fromEntries(keys.map((key) => [key, JSON.parse(readParent(`remapped-chapters/${key}.json`))]));
const chapters = structuredClone(beforeChapters);
const beforeCoverage = JSON.parse(readParent('claim-coverage.json'));
const coverage = structuredClone(beforeCoverage);
assert.equal(beforeCoverage.scene_claims.length, 65, 'unexpected coverage count');
const changes = [
  { id: 'e1', chapter: 'engine', scene: 'engine-s041', before: 1, after: 0, fact: 0 },
  { id: 'h5', chapter: 'hook', scene: 'hook-s004', before: 2, after: 0, fact: 3 },
  { id: 'i1', chapter: 'idea', scene: 'idea-s024', before: 2, after: 0, fact: 3 },
  { id: 'i5', chapter: 'idea', scene: 'idea-s031', before: 2, after: 0, fact: 3 },
];
for (const change of changes) {
  const found = keys.flatMap((key) => chapters[key].claims.map((claim) => ({ key, claim })))
    .filter(({ claim }) => claim.id === change.id);
  assert.equal(found.length, 1, `claim ${change.id} is not unique`);
  const [{ key, claim }] = found;
  assert.equal(key, change.chapter, `${change.id}: chapter changed`);
  assert.equal(claim.scene, change.scene, `${change.id}: scene changed`);
  assert.equal(claim.source, change.before, `${change.id}: old source changed`);
  assert.equal(claim.fact, change.fact, `${change.id}: fact changed`);
  assert.equal(claim.verdict, 'UNCHECKED', `${change.id}: verdict changed`);
  assert(row.must_verify[claim.fact].sources.includes(change.after), `${change.id}: new source outside row fact`);
  claim.source = change.after;

  const matches = coverage.scene_claims.filter((item) => item.id === change.id);
  assert.equal(matches.length, 1, `${change.id}: coverage is not unique`);
  assert.equal(matches[0].source_index, change.before, `${change.id}: old coverage changed`);
  assert.equal(matches[0].proposed_row_fact_index, change.fact, `${change.id}: coverage fact changed`);
  matches[0].source_index = change.after;
}
coverage.status = 'OFFLINE_PROPOSED_FOUR_SCENE_SOURCE_POINTERS_ONLY';
coverage.parent_candidate_manifest_sha256 = parentManifestSha;

let scenes = 0;
let lines = 0;
let claims = 0;
const allIds = new Set();
for (const key of keys) {
  const before = beforeChapters[key];
  const after = chapters[key];
  scenes += after.scenes.length;
  lines += after.scenes.flatMap((scene) => scene.lines || []).length;
  claims += after.claims.length;
  assert.deepEqual(after.scenes, before.scenes, `${key}: scene/narration drift`);
  const restored = structuredClone(after);
  for (const claim of restored.claims) {
    assert(!allIds.has(claim.id), `${claim.id}: duplicate claim`);
    allIds.add(claim.id);
    assert.equal(claim.verdict, 'UNCHECKED', `${claim.id}: verdict changed`);
    assert(claim.source >= 0 && claim.source < row.sources.length, `${claim.id}: invalid source index`);
    if (claim.fact !== null) {
      assert(claim.fact >= 0 && claim.fact < row.must_verify.length, `${claim.id}: invalid fact index`);
      assert(row.must_verify[claim.fact].sources.includes(claim.source), `${claim.id}: source not in fact`);
    }
    const mapped = coverage.scene_claims.find((item) => item.id === claim.id);
    assert(mapped, `${claim.id}: missing coverage`);
    assert.equal(mapped.source_index, claim.source, `${claim.id}: coverage source mismatch`);
    assert.equal(mapped.proposed_row_fact_index, claim.fact, `${claim.id}: coverage fact mismatch`);
    const patch = changes.find((item) => item.id === claim.id);
    if (patch) claim.source = patch.before;
  }
  assert.deepEqual(restored, before, `${key}: extra chapter change`);
}
assert.deepEqual([scenes, lines, claims], [85, 88, 65], 'episode shape changed');
assert.deepEqual([...allIds].sort(), beforeCoverage.scene_claims.map((claim) => claim.id).sort());
const restoredCoverage = structuredClone(coverage);
restoredCoverage.status = beforeCoverage.status;
restoredCoverage.parent_candidate_manifest_sha256 = beforeCoverage.parent_candidate_manifest_sha256;
for (const change of changes) {
  restoredCoverage.scene_claims.find((item) => item.id === change.id).source_index = change.before;
}
assert.deepEqual(restoredCoverage, beforeCoverage, 'coverage changed beyond four sources and lineage');
for (const mapping of coverage.row_to_storyboard_facts) {
  assert.deepEqual(mapping.row_sources, row.must_verify[mapping.row_fact_index].sources);
  assert.deepEqual([...mapping.scene_claim_ids].sort(), coverage.scene_claims
    .filter((claim) => claim.proposed_row_fact_index === mapping.row_fact_index)
    .map((claim) => claim.id).sort());
}
for (const id of ['h7', 't7', 't8']) {
  const claim = keys.flatMap((key) => chapters[key].claims).find((item) => item.id === id);
  assert.deepEqual([claim.source, claim.fact], [3, 4], `${id}: court mapping changed`);
}
for (const id of ['e6', 'e7']) {
  const claim = keys.flatMap((key) => chapters[key].claims).find((item) => item.id === id);
  assert.deepEqual([claim.source, claim.fact], [2, null], `${id}: readable registration mapping changed`);
}

const { STORY_KEYS, storyHash, storyProblems, reviewProblems } = await import(
  pathToFileURL(path.join(root, 'tools/video/story-plans/plan.mjs')).href
);
const story = Object.fromEntries(STORY_KEYS.map((key) => [key, row[key]]));
assert.equal(storyHash(story), expectedStorySha, 'canonical row story changed');
assert.deepEqual(storyProblems(story, 'B18'), [], 'row validation failed');
assert.deepEqual(reviewProblems(review, story, 'B18'), [], 'existing row review no longer matches row');

const files = new Map([
  ['B18.json', rowBytes],
  ['reviews/B18.json', reviewBytes],
  ['series-adoption.json', seriesBytes],
  ['claim-coverage.json', canonical(coverage)],
]);
for (const key of keys) {
  const name = `remapped-chapters/${key}.json`;
  files.set(name, ['hook', 'idea', 'engine'].includes(key)
    ? canonical(chapters[key]) : readParent(name));
}
const changedFiles = ['claim-coverage.json', 'remapped-chapters/engine.json',
  'remapped-chapters/hook.json', 'remapped-chapters/idea.json'];
const fileDelta = Object.fromEntries(changedFiles.map((name) => [name, {
  before_sha256: sha(readParent(name)), after_sha256: sha(files.get(name)),
}]));
for (const name of ['B18.json', 'reviews/B18.json', 'series-adoption.json',
  'remapped-chapters/origin.json', 'remapped-chapters/turn.json', 'remapped-chapters/now.json']) {
  assert.equal(sha(files.get(name)), sha(readParent(name)), `${name}: unchanged file drifted`);
}
files.set('delta.json', canonical({
  schema_version: 1,
  status: 'OFFLINE_FOUR_SOURCE_POINTERS_ONLY',
  parent_candidate_manifest_sha256: parentManifestSha,
  changes: changes.map(({ id, chapter, scene, before, after, fact }) => ({
    id, chapter, scene, before_source_index: before, after_source_index: after,
    unchanged_row_fact_index: fact, unchanged_verdict: 'UNCHECKED',
  })),
  changed_files: fileDelta,
  row_sha256_before: sha(rowBytes), row_sha256_after: sha(files.get('B18.json')),
  review_sha256_before: sha(reviewBytes), review_sha256_after: sha(files.get('reviews/B18.json')),
  canonical_story_sha256_before: expectedStorySha,
  canonical_story_sha256_after: storyHash(story),
}));
files.set('verification.json', canonical({
  schema_version: 1,
  status: 'PASS_OFFLINE_STRUCTURE_ONLY',
  parent_candidate_manifest_sha256: parentManifestSha,
  canonical_story_sha256: storyHash(story),
  scene_count: scenes, narration_line_count: lines, scene_claim_count: claims,
  changed_scene_source_ids: changes.map((change) => change.id),
  unchanged_row_and_review: true,
  row_review_hash_valid: true,
  all_scene_claims_unchecked: true,
  independent_new_source_review_complete: false,
  formal_worker_verifier_complete: false,
  import_approved: false,
  paid_calls: 0,
  rendered_video: false,
}));

for (const [name, content] of files) {
  const target = path.join(here, name);
  if (mode === '--write') {
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, content);
  } else {
    assert.equal(sha(fs.readFileSync(target)), sha(content), `output drift: ${name}`);
  }
}
const manifest = {
  schema_version: 1,
  parent_candidate_manifest_sha256: parentManifestSha,
  files: Object.fromEntries([...files].map(([name, content]) => [name, sha(content)])),
  README_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  build_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))),
};
const manifestFile = path.join(here, 'sha256.json');
if (mode === '--write') fs.writeFileSync(manifestFile, canonical(manifest));
else assert.equal(fs.readFileSync(manifestFile, 'utf8'), canonical(manifest), 'manifest drift');
console.log(JSON.stringify({
  status: 'PASS_OFFLINE_CANDIDATE_ONLY', mode, story_sha256: storyHash(story),
  changed_scene_source_ids: changes.map((change) => change.id),
  scenes, lines, claims, files: files.size,
}));
