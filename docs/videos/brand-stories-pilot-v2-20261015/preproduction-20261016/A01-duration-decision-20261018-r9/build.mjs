// A01-only duration decision over frozen r8. This script never touches production.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r8 = path.resolve(here, '../A01-story-depth-candidate-20261018-r8');
const pilot = path.resolve(here, '../..');
const expected = {
  r8_manifest: '3475e820d22df7f9d8fd850764d450f17630a2dcdd390949f9147d03062c42b8',
  pilot_series: 'b2cdb40dd5c6b9e7723ae76fd5fb9992ca66fc0baebabc4ae0f5caabdb38502b',
  b18_episode: 'c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681',
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const readR8 = (name) => fs.readFileSync(path.join(r8, name));
const candidateNames = ['video.json', 'series.json', 'lexicon.json', 'script.md', 'claims.md'];

const r8ManifestBytes = readR8('manifest.json');
assert.equal(sha(r8ManifestBytes), expected.r8_manifest, 'r8 manifest drift');
const r8Manifest = JSON.parse(r8ManifestBytes);
assert.equal(r8Manifest.status, 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE');
for (const name of candidateNames) {
  assert.equal(sha(readR8('candidate/' + name)), r8Manifest.outputs_sha256['candidate/' + name], 'r8 candidate drift ' + name);
}
for (const name of ['source-map.json', 'validation.json']) {
  assert.equal(sha(readR8(name)), r8Manifest.outputs_sha256[name], 'r8 metadata drift ' + name);
}
assert.equal(sha(readR8('README.md')), r8Manifest.readme_sha256, 'r8 README drift');
assert.equal(sha(fs.readFileSync(path.join(pilot, 'series.json'))), expected.pilot_series, 'shared pilot series drift');
assert.equal(sha(fs.readFileSync(path.join(pilot, 'episodes/B18.json'))), expected.b18_episode, 'B18 plan drift');

const previous = JSON.parse(readR8('candidate/video.json'));
const video = structuredClone(previous);
assert.equal(video.slug, 'story-rolling-suitcase-v2');
assert.deepEqual(video.target_minutes, [9, 11], 'r8 duration changed');
video.target_minutes = [7, 8];
assert.deepEqual({ ...video, target_minutes: previous.target_minutes }, previous, 'only A01 duration may change');
const series = JSON.parse(readR8('candidate/series.json'));
assert.equal(series.target_minutes, 10, 'pilot series must remain ten minutes');

const [{ screenplay }, { estimateTimeline }, { lintVideo }, { cuteStoryVisualProblems }] = await Promise.all([
  'tools/video/core/screenplay.mjs',
  'tools/video/core/timeline.mjs',
  'tools/video/core/lint.mjs',
  'tools/video/automation/story.mjs',
].map((file) => import(pathToFileURL(path.join(repo, file)))));
assert.equal(screenplay(video), readR8('candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'duration must not change narration');
const lintContext = {
  lexicon: JSON.parse(readR8('candidate/lexicon.json')),
  brief: fs.readFileSync(path.join(here, '../A01-story-depth-candidate-20261018-r4/base/brief.md'), 'utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(video, lintContext);
const lintAt300 = lintVideo(video, { ...lintContext, cpm: 300 });
const cute = cuteStoryVisualProblems(video);
assert.equal(lint.errors.length, 0, 'video lint errors');
assert.equal(cute.length, 0, 'cute illustration errors');
const timing = Object.fromEntries([250, 275, 300].map((cpm) => {
  const before = estimateTimeline(previous, cpm).total_frames / 30;
  const after = estimateTimeline(video, cpm).total_frames / 30;
  assert.equal(after, before, 'duration metadata must not change scene timing');
  const expectedSeconds = JSON.parse(readR8('validation.json')).estimated_timing_not_tts[cpm].candidate_seconds;
  assert.equal(Number(after.toFixed(1)), expectedSeconds, 'r8 timing drift');
  return [cpm, Number(after.toFixed(1))];
}));

const validation = {
  status: 'OFFLINE_DURATION_ONLY_HOLD_UNREVIEWED',
  owner_decision: '2026-10-18 A01 only, compact 7–8 minute narrated body',
  slug: video.slug,
  body_target_seconds: [420, 480],
  separate_bookends_seconds_planned: { intro: 5, outro: 21 },
  final_cut_seconds_if_bookends_match_plan: [446, 506],
  estimated_body_seconds_not_tts: timing,
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_errors_at_300_cpm: lintAt300.errors,
  cute_visual_errors: cute,
  narrative_lint_at_default_250_cpm: 'RAN_ON_518_5_SECOND_ESTIMATE_NOT_MEASURED_7_TO_8_MINUTE_CUT',
  narrative_lint_at_300_cpm: 'NOT_RUN_CURRENT_RUNTIME_REQUIRES_EIGHT_MINUTES',
  package_source_index_integrity: 'P1_HOLD_INHERITED_R8_UNRELATED_AND_MISSING_SOURCES',
  source_fact_visual_listener_review: 'NOT_RUN_FOR_R9',
  measured_tts_body_and_cut: 'NOT_RUN',
  host_worker_duration_gate: 'UNCHANGED_540_TO_660_REQUIRES_SEPARATE_A01_ONLY_CHANGE',
  host_import_or_paid_media: 'NOT_RUN',
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ...candidateNames.filter((name) => name !== 'video.json').map((name) => ['candidate/' + name, readR8('candidate/' + name)]),
  ['validation.json', json(validation)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_DURATION_ONLY',
  slug: video.slug,
  derives_from_r8_manifest_sha256: expected.r8_manifest,
  source_snapshot: r8Manifest.source_snapshot,
  preserved_sha256: { 'pilot/series.json': expected.pilot_series, 'pilot/episodes/B18.json': expected.b18_episode },
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  changed_fields: ['candidate/video.json:target_minutes'],
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));

const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r9');
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), 'missing output ' + name);
    assert.ok(fs.readFileSync(file).equals(bytes), 'stale output ' + name);
  }
}
console.log(JSON.stringify({ action, status: validation.status, slug: video.slug, target_minutes: video.target_minutes, pilot_target: series.target_minutes, body_seconds_at_300_cpm: timing[300], lint_errors: lint.errors.length, cute_errors: cute.length }));
