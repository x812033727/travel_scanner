#!/usr/bin/env node
// Offline two-line successor to the B18 attributed-narration candidate.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.resolve(here, '../B18-attributed-narration-candidate-20261017');
const pilot = path.resolve(here, '../..');
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
const sha = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => JSON.stringify(value, null, 2) + '\n';
const readParent = (name) => fs.readFileSync(path.join(parent, name));

const parentManifestSha = '7f39a6b95a8233ff4cc32986588c71431886987c75a5d4cd9764c1bf1910753f';
const parentReviewSha = '67c2f823fcf15bdfa3a9babc650d461154f7ab5f5b3fdb28d95057bb57642f5c';
const manifestBytes = readParent('sha256.json');
assert.equal(sha(manifestBytes), parentManifestSha, 'parent manifest drift');
const parentManifest = JSON.parse(manifestBytes);
for (const [name, expected] of Object.entries(parentManifest.files))
  assert.equal(sha(readParent(name)), expected, `parent output drift: ${name}`);
assert.equal(sha(readParent('README.md')), parentManifest.README_sha256, 'parent README drift');
assert.equal(sha(readParent('build.mjs')), parentManifest.build_sha256, 'parent builder drift');
assert.equal(sha(readParent('INDEPENDENT-ATTRIBUTION-REVIEW.md')), parentReviewSha, 'parent review drift');

const rowBytes = readParent('B18.json');
assert.equal(sha(rowBytes), 'c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681', 'parent row drift');
const row = JSON.parse(rowBytes);
const seriesBytes = readParent('series-adoption.json');
const coverageBytes = readParent('claim-coverage.json');
const parentChapters = Object.fromEntries(keys.map((key) => [key, JSON.parse(readParent(`remapped-chapters/${key}.json`))]));
const chapters = structuredClone(parentChapters);
const parentMap = JSON.parse(readParent('attribution-map.json'));
const attributionMap = structuredClone(parentMap);
const edits = [
  {
    chapter: 'idea', scene: 'idea-s032', claim: 'i6', line: '3f5899d2', source: 0, fact: 3,
    before: 'J-Net21 說，這種板子後來叫「魚鱗板」。原本會把盤子擠掉的地方，終於有了能走的路。',
    after: '同一篇報導把這種板子叫作「魚鱗板」。原本會把盤子擠掉的地方，終於有了能走的路。',
  },
  {
    chapter: 'idea', scene: 'idea-s033', claim: 'i7', line: '464491bc', source: 0, fact: 3,
    before: 'J-Net21 記載，從工廠參觀到試作機完成，前後約十年。',
    after: '報導還記載，從工廠參觀到試作機完成，前後約十年。',
  },
];

const ideaScenes = chapters.idea.scenes;
const i5 = ideaScenes.find((scene) => scene.id === 'idea-s031');
const i6 = ideaScenes.find((scene) => scene.id === 'idea-s032');
const i7 = ideaScenes.find((scene) => scene.id === 'idea-s033');
assert.deepEqual([ideaScenes.indexOf(i6), ideaScenes.indexOf(i7)],
  [ideaScenes.indexOf(i5) + 1, ideaScenes.indexOf(i5) + 2], 'source antecedent scenes are not consecutive');
assert.match(i5.lines[0].text, /^依 J-Net21 的記載，/, 'i5 source antecedent drift');
assert.equal(row.must_verify[3].attributed, true, 'attributed fact drift');
assert.deepEqual(row.must_verify[3].sources, [0, 2], 'fact 3 source route drift');
for (const edit of edits) {
  const scene = chapters[edit.chapter].scenes.find((item) => item.id === edit.scene);
  const line = scene?.lines?.find((item) => item.id === edit.line);
  const claim = chapters[edit.chapter].claims.find((item) => item.id === edit.claim);
  assert.equal(line?.text, edit.before, `parent narration drift: ${edit.claim}`);
  assert(!line.say, `spoken override hides edited text: ${edit.claim}`);
  assert.deepEqual([claim?.scene, claim?.source, claim?.fact, claim?.verdict],
    [edit.scene, edit.source, edit.fact, 'UNCHECKED'], `claim route drift: ${edit.claim}`);
  line.text = edit.after;
  const mapEntry = attributionMap.changed_narration.find((item) => item.claim === edit.claim);
  assert.equal(mapEntry?.after, edit.before, `parent attribution map drift: ${edit.claim}`);
  mapEntry.after = edit.after;
}
assert.match(i6.lines[0].text, /^同一篇報導/, 'i6 source handoff drift');
assert.match(i7.lines[0].text, /^報導還記載/, 'i7 source handoff drift');

// Reverse only the two declared edits and prove every other parent byte/object is unchanged.
const restoredChapters = structuredClone(chapters);
for (const edit of edits)
  restoredChapters[edit.chapter].scenes.find((scene) => scene.id === edit.scene)
    .lines.find((line) => line.id === edit.line).text = edit.before;
assert.deepEqual(restoredChapters, parentChapters, 'chapters changed beyond i6/i7');
const restoredMap = structuredClone(attributionMap);
for (const edit of edits)
  restoredMap.changed_narration.find((item) => item.claim === edit.claim).after = edit.before;
assert.deepEqual(restoredMap, parentMap, 'attribution map changed beyond i6/i7');

let scenes = 0;
let lines = 0;
let claims = 0;
const claimIds = new Set();
const coverage = JSON.parse(coverageBytes);
for (const key of keys) {
  const chapter = chapters[key];
  scenes += chapter.scenes.length;
  lines += chapter.scenes.flatMap((scene) => scene.lines || []).length;
  claims += chapter.claims.length;
  assert.deepEqual(chapter.claims, parentChapters[key].claims, `claim/source/fact changed: ${key}`);
  for (const claim of chapter.claims) {
    assert(!claimIds.has(claim.id), `duplicate claim ${claim.id}`);
    claimIds.add(claim.id);
    assert.equal(claim.verdict, 'UNCHECKED', `claim verdict drift: ${claim.id}`);
    assert(claim.source >= 0 && claim.source < row.sources.length, `source range: ${claim.id}`);
    if (claim.fact !== null)
      assert(row.must_verify[claim.fact].sources.includes(claim.source), `fact source mismatch: ${claim.id}`);
    const mapped = coverage.scene_claims.find((item) => item.id === claim.id);
    assert.deepEqual([mapped?.claim, mapped?.source_index, mapped?.proposed_row_fact_index],
      [claim.claim, claim.source, claim.fact], `coverage mismatch: ${claim.id}`);
  }
}
assert.deepEqual([scenes, lines, claims], [85, 88, 65], 'episode shape drift');
assert.deepEqual([...claimIds].sort(), coverage.scene_claims.map((item) => item.id).sort());
for (const id of ['h7', 't7', 't8']) {
  const claim = keys.flatMap((key) => chapters[key].claims).find((item) => item.id === id);
  assert.deepEqual([claim?.source, claim?.fact], [3, 4], `court route drift: ${id}`);
}
for (const id of ['e6', 'e7']) {
  const claim = keys.flatMap((key) => chapters[key].claims).find((item) => item.id === id);
  assert.deepEqual([claim?.source, claim?.fact], [2, null], `registration route drift: ${id}`);
}
const activeReview = JSON.parse(fs.readFileSync(path.join(pilot, 'episodes/reviews/B18.json')));
assert.deepEqual(activeReview.reviewer_only, [4], 'court reviewer-only requirement drift');

const { STORY_KEYS, storyHash, storyProblems, reviewProblems } = await import(
  pathToFileURL(path.join(root, 'tools/video/story-plans/plan.mjs')).href
);
const story = Object.fromEntries(STORY_KEYS.map((key) => [key, row[key]]));
const storySha = storyHash(story);
assert.equal(storySha, 'd0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648', 'story hash drift');
assert.deepEqual(storyProblems(story, 'B18'), [], 'candidate story invalid');
const staleProblems = reviewProblems(activeReview, story, 'B18');
assert(staleProblems.length > 0, 'old active review unexpectedly validates candidate');

const files = new Map([
  ['B18.json', rowBytes],
  ['series-adoption.json', seriesBytes],
  ['claim-coverage.json', coverageBytes],
  ['attribution-map.json', canonical(attributionMap)],
  ['flow-map.json', canonical({
    schema_version: 1, status: 'OFFLINE_PROPOSED_HOLD', parent_candidate_manifest_sha256: parentManifestSha,
    parent_independent_review_sha256: parentReviewSha, changed_narration: edits,
    unchanged_row_sha256: sha(rowBytes), canonical_story_sha256: storySha,
    fullscript_I03_I04_alignment_and_independent_review_required: true,
  })],
  ['fullscript-impact.json', readParent('fullscript-impact.json')],
]);
for (const key of keys) {
  const name = `remapped-chapters/${key}.json`;
  files.set(name, key === 'idea' ? canonical(chapters.idea) : readParent(name));
}
const sourceNames = ['B18.json', 'series-adoption.json', 'claim-coverage.json',
  ...keys.map((key) => `remapped-chapters/${key}.json`)];
const delta = Object.fromEntries(sourceNames.map((name) => [name, {
  before_sha256: sha(readParent(name)), after_sha256: sha(files.get(name)),
  changed: sha(readParent(name)) !== sha(files.get(name)),
}]));
assert.deepEqual(sourceNames.filter((name) => delta[name].changed), ['remapped-chapters/idea.json'],
  'changed source files exceed idea chapter');
files.set('delta.json', canonical({
  schema_version: 1, status: 'OFFLINE_TWO_LINE_FLOW_HOLD', parent_candidate_manifest_sha256: parentManifestSha,
  named_changes: edits, source_files: delta, canonical_story_sha256: storySha,
  old_active_review_valid_for_candidate: false,
}));
files.set('verification.json', canonical({
  schema_version: 1, status: 'PASS_OFFLINE_STRUCTURE_ONLY_HOLD',
  scenes, narration_lines: lines, scene_claims: claims, all_scene_claims_unchecked: true,
  unchanged_row_and_claim_source_fact_routes: true, court_reviewer_only_required_in_new_review: true,
  canonical_story_sha256: storySha, stale_row_review_problems: staleProblems,
  independent_new_review_complete: false, fullscript_reconciled_and_reviewed: false,
  tts_tested: false, paid_calls: 0, rendered_video: false, import_approved: false,
}));

for (const [name, content] of files) {
  const target = path.join(here, name);
  if (mode === '--write') {
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, content);
  } else {
    assert.equal(fs.readFileSync(target, 'utf8'), content.toString(), `output drift: ${name}`);
  }
}
const manifest = {
  schema_version: 1, parent_candidate_manifest_sha256: parentManifestSha,
  parent_independent_review_sha256: parentReviewSha,
  files: Object.fromEntries([...files].map(([name, content]) => [name, sha(content)])),
  README_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  build_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))),
};
const manifestPath = path.join(here, 'sha256.json');
if (mode === '--write') fs.writeFileSync(manifestPath, canonical(manifest));
else assert.equal(fs.readFileSync(manifestPath, 'utf8'), canonical(manifest), 'manifest drift');
console.log(JSON.stringify({ status: 'PASS_OFFLINE_CANDIDATE_HOLD', mode, story_sha256: storySha,
  scenes, lines, claims, source_files_changed: sourceNames.filter((name) => delta[name].changed) }));
