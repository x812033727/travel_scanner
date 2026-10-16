#!/usr/bin/env node
// Offline-only successor: remove three unsupported brewery names from B18 worker input.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.resolve(here, '../B18-worker-input-adoption-candidate-20261017');
const root = path.resolve(here, '../../../../..');
const pilot = path.resolve(here, '../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const parentManifestSha = '56d6602b844a5daa055c7a176ad7db739d5ee29150c22eacb89110006071c05a';
const parentReviewSha = 'bbb3782c57ec05c4ba0c58dfb766343e67f4ef4f890c051ed93c8552dd1508a1';
const unwanted = ['朝日啤酒', 'アサヒビール', 'Asahi'];
const sha = (data) => crypto.createHash('sha256').update(data).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (name) => fs.readFileSync(path.join(parent, name));

const parentManifestBytes = read('sha256.json');
assert.equal(sha(parentManifestBytes), parentManifestSha, 'reviewed parent manifest drift');
for (const [name, expected] of Object.entries(JSON.parse(parentManifestBytes).files)) {
  assert.equal(sha(read(name)), expected, `reviewed parent file drift: ${name}`);
}
assert.equal(sha(read('independent-review-20261017.md')), parentReviewSha, 'independent review drift');
const oldRow = JSON.parse(read('B18.json'));
const oldSeries = JSON.parse(read('series-adoption.json'));
const oldCoverage = JSON.parse(read('claim-coverage.json'));
const oldChapters = Object.fromEntries(keys.map((key) => [key, JSON.parse(read(`remapped-chapters/${key}.json`))]));
assert.deepEqual(oldRow.names.slice(10, 13), unwanted, 'unsupported names moved in parent row');
assert.deepEqual(oldSeries.names.slice(10, 13), unwanted, 'unsupported names moved in parent series');
assert.deepEqual(oldSeries.plan.names.slice(10, 13), unwanted, 'unsupported names moved in parent plan');
assert.equal(oldCoverage.scene_claims.length, 65);

const trim = (names) => names.filter((name) => !unwanted.includes(name));
const row = { ...oldRow, names: trim(oldRow.names) };
const series = { ...oldSeries, names: trim(oldSeries.names), plan: { ...oldSeries.plan, names: trim(oldSeries.plan.names) } };
assert.equal(row.names.length, oldRow.names.length - 3);
assert.equal(series.names.length, oldSeries.names.length - 3);
assert.deepEqual(series.plan.names, row.names);
assert.deepEqual({ ...row, names: oldRow.names }, oldRow, 'row changed beyond names');
assert.deepEqual({ ...series, names: oldSeries.names, plan: { ...series.plan, names: oldSeries.plan.names } }, oldSeries, 'series changed beyond names');
assert.deepEqual(row.sources, oldRow.sources);
assert.deepEqual(row.must_verify, oldRow.must_verify);
assert.deepEqual(series.plan.sources, oldSeries.plan.sources);
assert.deepEqual(series.plan.must_verify, oldSeries.plan.must_verify);
assert.equal(row.caveats, oldRow.caveats, 'source/readability caveat changed');
assert.equal(series.plan.caveats, oldSeries.plan.caveats, 'series caveat changed');
for (const key of keys) {
  assert.equal(sha(canonical(oldChapters[key])), sha(read(`remapped-chapters/${key}.json`)), `${key} serialization changed`);
  for (const claim of oldChapters[key].claims) assert.equal(claim.verdict, 'UNCHECKED', `${claim.id} verdict changed`);
}

const { STORY_KEYS, storyProblems, storyHash, reviewProblems } = await import(pathToFileURL(path.join(root, 'tools/video/story-plans/plan.mjs')).href);
const source = Object.fromEntries(STORY_KEYS.map((key) => [key, row[key]]));
const problems = storyProblems(source, 'B18');
assert.deepEqual(problems, []);
const previousReview = JSON.parse(fs.readFileSync(path.join(pilot, 'episodes/reviews/B18.json'), 'utf8'));
const staleReviewProblems = reviewProblems(previousReview, source, 'B18');
assert(staleReviewProblems.some((problem) => problem.includes('story changed after this review')));
assert.notEqual(storyHash(source), previousReview.story_sha256);
assert.notEqual(storyHash(source), storyHash(Object.fromEntries(STORY_KEYS.map((key) => [key, oldRow[key]]))));

let externalCalls = 0;
globalThis.fetch = () => { externalCalls++; throw new Error('offline candidate must not fetch'); };
const { composeStory, cuteStoryVisualProblems } = await import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs')).href);
const authored = path.resolve(here, '../B18-authored-chapters-candidate');
const voice = JSON.parse(fs.readFileSync(path.join(authored, 'synthetic/docroot/docs/videos/story-conveyor-belt-sushi-v2/video.json'), 'utf8')).voice;
const oldVideo = composeStory({ slug: row.slug, info: oldSeries, chapters: oldChapters, voice, drama: { music_enabled: false }, root });
const newVideo = composeStory({ slug: row.slug, info: series, chapters: oldChapters, voice, drama: { music_enabled: false }, root });
assert.deepEqual(newVideo, oldVideo, 'name removal changed composed video');
assert.deepEqual(cuteStoryVisualProblems(newVideo), []);
assert.equal(externalCalls, 0);

const outputs = new Map([
  ['B18.json', canonical(row)],
  ['series-adoption.json', canonical(series)],
  ['claim-coverage.json', read('claim-coverage.json').toString('utf8')],
]);
for (const key of keys) outputs.set(`remapped-chapters/${key}.json`, read(`remapped-chapters/${key}.json`).toString('utf8'));
const delta = {
  schema_version: 1, status: 'OFFLINE_UNSUPPORTED_NAME_REMOVAL_ONLY',
  parent_manifest_sha256: parentManifestSha, parent_independent_review_sha256: parentReviewSha,
  removed_names: unwanted,
  changed_json_paths: ['B18.json:/names', 'series-adoption.json:/names', 'series-adoption.json:/plan/names'],
  unchanged: ['sources', 'must_verify', 'chapters', 'caveats', 'claim-coverage.json', 'all six remapped-chapters', 'narration', 'scenes', 'claim/source/fact bindings'],
  composed_video_identical: true, external_calls: externalCalls,
};
outputs.set('delta.json', canonical(delta));
const verification = {
  schema_version: 1, status: 'OFFLINE_EXACT_DELTA_INDEPENDENT_REVIEW_PENDING',
  parent_manifest_sha256: parentManifestSha, parent_independent_review_sha256: parentReviewSha,
  row_sha256: sha(outputs.get('B18.json')), canonical_story_sha256: storyHash(source),
  series_adoption_sha256: sha(outputs.get('series-adoption.json')),
  coverage_sha256: sha(outputs.get('claim-coverage.json')),
  remapped_chapter_sha256: Object.fromEntries(keys.map((key) => [key, sha(outputs.get(`remapped-chapters/${key}.json`))])),
  removed_names: unwanted, row_sources_unchanged: true, row_must_verify_unchanged: true,
  scene_claims_unchecked: oldCoverage.scene_claims.length, storyboard_chapters_unchanged: true,
  composed_video_identical: true, cute_story_visual_problems: 0,
  old_review_problems: staleReviewProblems, story_problems: problems,
  source_readability_caveat_retained: true, external_calls: externalCalls,
  independent_delta_review_pass: false, worker_pass: false, import_approved: false, host_written: false, paid_calls: 0,
};
outputs.set('verification.json', canonical(verification));
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
for (const [name, content] of outputs) {
  const target = path.join(here, name);
  if (mode === '--write') { fs.mkdirSync(path.dirname(target), { recursive: true }); fs.writeFileSync(target, content); }
  else assert.equal(fs.readFileSync(target, 'utf8'), content, `successor file drift: ${name}`);
}
console.log(canonical(verification));
