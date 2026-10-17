import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Offline, metadata-only successor. The independently read predecessor stays immutable.
const here = path.dirname(fileURLToPath(import.meta.url));
const base = path.resolve(here, '../B18-precision-reconciliation-candidate-20261017');
const root = path.resolve(here, '../../../../..');
const baseManifestSha = 'cb28ae7bb6aed7a30c639318504e8e11386aee8de1404e9b71b1c372c1e40953';
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (name) => fs.readFileSync(path.join(base, name), 'utf8');
assert.equal(sha(fs.readFileSync(path.join(base, 'sha256.json'))), baseManifestSha, 'parent manifest drift');
for (const [name, expected] of Object.entries(JSON.parse(read('sha256.json')).files)) {
  assert.equal(sha(fs.readFileSync(path.join(base, name))), expected, `parent file drift: ${name}`);
}

const series = JSON.parse(read('series.json'));
const previous = Object.fromEntries(keys.map((key) => [key, JSON.parse(read(`chapters/${key}.json`))]));
const chapters = structuredClone(previous);
const oldClaim = previous.turn.claims.find((row) => row.id === 't6');
const newClaim = chapters.turn.claims.find((row) => row.id === 't6');
assert.deepEqual(oldClaim, {
  id: 't6', claim: '做好的盤子從後場放上直線輸送帶', scene: 'turn-s072',
  source: 2, fact: 12, verdict: 'UNCHECKED',
  note: '發明協會後場到用餐區的直線輸送；無給茶年份。',
});
newClaim.claim = '做好的盤子從後場放上輸送帶';
assert.deepEqual(chapters.turn.scenes, previous.turn.scenes, 'turn narration or visuals drift');
for (const key of keys.filter((key) => key !== 'turn')) assert.deepEqual(chapters[key], previous[key], `chapter drift: ${key}`);
for (const row of chapters.turn.claims.filter((claim) => claim.id !== 't6')) {
  assert.deepEqual(row, previous.turn.claims.find((claim) => claim.id === row.id), `other claim drift: ${row.id}`);
}
assert.equal(chapters.turn.claims.length, previous.turn.claims.length, 'claim count drift');
assert.equal(chapters.turn.scenes.find((row) => row.id === 'turn-s072').lines[0].text, '他們先在後場完成一盤壽司，再把盤子放上輸送帶。');
assert.equal(chapters.turn.scenes.find((row) => row.id === 'turn-s073').lines[0].text, '餐台不再只繞著吧台，而是拉成一條直線。');
assert.equal(chapters.turn.claims.find((row) => row.id === 't11').scene, 'turn-s073');

const allScenes = keys.flatMap((key) => chapters[key].scenes);
const sceneIds = new Set(allScenes.map((row) => row.id));
assert.equal(sceneIds.size, allScenes.length, 'duplicate scene');
const allClaims = keys.flatMap((key) => chapters[key].claims);
assert.equal(new Set(allClaims.map((row) => row.id)).size, allClaims.length, 'duplicate claim');
for (const row of allClaims) {
  assert(sceneIds.has(row.scene), `claim scene missing: ${row.id}`);
  assert(series.plan.sources[row.source], `claim source missing: ${row.id}`);
  if (row.fact !== null && row.fact !== undefined) assert(series.plan.must_verify[row.fact]?.sources.includes(row.source), `fact/source mismatch: ${row.id}`);
  assert.equal(row.verdict, 'UNCHECKED', `unreviewed claim promoted: ${row.id}`);
}

const { composeStory, cuteStoryVisualProblems } = await import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs')).href);
const { loadProject, lintProject } = await import(pathToFileURL(path.join(root, 'tools/video/core/state.mjs')).href);
const { estimateTimeline } = await import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs')).href);
const slug = 'story-conveyor-belt-sushi-v2';
const authored = path.resolve(base, '../B18-authored-chapters-candidate');
const voice = JSON.parse(fs.readFileSync(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'video.json'), 'utf8')).voice;
const beforeDoc = composeStory({ slug, info: series, chapters: previous, voice, drama: { music_enabled: false }, root });
const doc = composeStory({ slug, info: series, chapters, voice, drama: { music_enabled: false }, root });
assert.deepEqual(doc, beforeDoc, 'video content drift');
assert.deepEqual(doc.look, { preset: 'cute-mystery' });
assert.equal(doc.subtitles.burn_in, false);
const cuteErrors = cuteStoryVisualProblems(doc);
assert.deepEqual(cuteErrors, []);
let externalCalls = 0;
globalThis.fetch = () => { externalCalls++; throw new Error('offline candidate must not fetch'); };
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'b18-claim-granularity-'));
assert(/^b18-claim-granularity-[^\\/]+$/.test(path.relative(path.resolve(os.tmpdir()), path.resolve(tmp))), 'unsafe temporary cleanup path');
let lint;
try {
  const shelf = path.join(tmp, 'docs', 'videos');
  const dir = path.join(shelf, slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'video.json'), canonical(doc));
  fs.writeFileSync(path.join(dir, 'series.json'), canonical(series));
  fs.copyFileSync(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'brief.md'), path.join(dir, 'brief.md'));
  fs.copyFileSync(path.join(authored, 'fixtures/lexicon.json'), path.join(shelf, 'lexicon.json'));
  lint = lintProject(loadProject({ slug, root: tmp }));
} finally { fs.rmSync(tmp, { recursive: true, force: true }); }
assert.deepEqual(lint.errors, []);
assert.equal(externalCalls, 0);
const bodySeconds = estimateTimeline(doc).total_frames / 30;
const parentVerification = JSON.parse(read('verification.json'));
assert.equal(bodySeconds, parentVerification.estimated_body_seconds, 'body duration drift');
assert.equal(allScenes.length, parentVerification.scenes, 'scene count drift');
assert.equal(allClaims.length, parentVerification.claims_unchecked, 'claim count drift');
assert.equal(lint.warnings.length, parentVerification.lint_warnings, 'lint warning count drift');

const delta = {
  schema_version: 1, status: 'OFFLINE_CLAIM_GRANULARITY_CORRECTION_ONLY',
  base_manifest_sha256: baseManifestSha,
  claim_rows: [{ id: 't6', before: oldClaim, after: newClaim }],
  unchanged: ['series.json', 'reuse-intent.json', ...keys.filter((key) => key !== 'turn').map((key) => `chapters/${key}.json`), 'all scenes, lines, visuals, loops and other claims in chapters/turn.json'],
  estimated_body_seconds_before: bodySeconds, estimated_body_seconds_after: bodySeconds,
  actual_tts_seconds: null, external_calls: externalCalls,
};
const verification = {
  schema_version: 1, status: 'VERIFIED_OFFLINE_METADATA_STRUCTURE_ONLY_ROW_REVIEW_PENDING',
  scenes: allScenes.length, lines: doc.scenes.flatMap((row) => row.lines).length,
  illustrations: doc.scenes.filter((row) => row.template === 'shot').length,
  cards: doc.scenes.filter((row) => row.template !== 'shot').length,
  claims_unchecked: allClaims.length, estimated_body_seconds: bodySeconds, measured_body_seconds: null,
  lint_errors: lint.errors, lint_warnings: lint.warnings.length,
  lint_warning_kinds: [...new Set(lint.warnings.map((warning) => warning.message.split(':', 1)[0]))],
  cute_errors: cuteErrors, external_calls: externalCalls,
  worker_pass: false, full_story_pass: false, full_source_pass: false, tts_generated: false,
};
const output = new Map([
  ['series.json', read('series.json')],
  ['reuse-intent.json', read('reuse-intent.json')],
  ['delta.json', canonical(delta)], ['verification.json', canonical(verification)],
]);
for (const key of keys) output.set(`chapters/${key}.json`, key === 'turn' ? canonical(chapters.turn) : read(`chapters/${key}.json`));
for (const name of ['series.json', 'reuse-intent.json', ...keys.filter((key) => key !== 'turn').map((key) => `chapters/${key}.json`)]) {
  assert.equal(sha(output.get(name)), sha(read(name)), `unchanged file bytes drift: ${name}`);
}
const hashes = Object.fromEntries([
  ['build.mjs', sha(fs.readFileSync(path.join(here, 'build.mjs')))],
  ['README.md', sha(fs.readFileSync(path.join(here, 'README.md')))],
  ...[...output].map(([name, content]) => [name, sha(content)]),
]);
output.set('sha256.json', canonical({ schema_version: 1, base_manifest_sha256: baseManifestSha, files: hashes }));
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
for (const [name, content] of output) {
  const file = path.join(here, name);
  if (mode === '--write') { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, content); }
  else assert.equal(fs.readFileSync(file, 'utf8'), content, `generated output drift: ${name}`);
}
console.log(JSON.stringify(verification, null, 2));
