import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const base = path.resolve(here, '../A01-round14-source-bound-loop-candidate');
const round10 = path.resolve(here, '../A01-round10-candidate');
const chaptersInOrder = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const read = (file) => fs.readFileSync(file);
const parse = (file) => JSON.parse(read(file).toString('utf8'));
const json = (value) => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const output = new Map();
const addOutput = (name, bytes) => output.set(name, bytes);
const baseManifestBytes = read(path.join(base, 'manifest.json'));
const baseManifest = JSON.parse(baseManifestBytes.toString('utf8'));
const delta = parse(path.join(here, 'delta.json'));

assert.equal(delta.status, 'OFFLINE_PLAN_DELTA_PENDING_FULL_REVIEW');
assert.equal(delta.base, 'A01-round14-source-bound-loop-candidate');
assert.equal(baseManifest.status, 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE');
assert.equal(sha(baseManifestBytes), delta.base_manifest_sha256, 'frozen round14 manifest drift');
assert.equal(delta.series_plan_changes.length, 1);
assert.equal(delta.series_plan_changes[0].chapter, 'origin');
assert.deepEqual(delta.series_plan_changes[0].script_sequence, [
  'origin-r12-01/r12o01', 'origin-03/csdd', 'origin-03/9ij6',
  'origin-01/zc7k', 'origin-01b/6b28',
]);

const chapters = {};
for (const key of chaptersInOrder) {
  const file = path.join(base, 'candidate/chapters', `${key}.json`);
  const bytes = read(file);
  assert.equal(sha(bytes), baseManifest.candidate_chapter_sha256[key], `round14 chapter ${key} drift`);
  chapters[key] = JSON.parse(bytes.toString('utf8'));
  assert.equal(chapters[key].key, key);
  addOutput(`candidate/chapters/${key}.json`, bytes);
}
const originSequence = chapters.origin.scenes.flatMap((scene) => scene.lines.map((line) => ({
  id: `${scene.id}/${line.id}`, text: line.text,
}))).slice(0, 5);
assert.deepEqual(originSequence.map(({ id }) => id), delta.series_plan_changes[0].script_sequence);
assert.match(originSequence[0].text, /1928 年出發前/);
assert.match(originSequence[3].text, /1928 年.*出發/);

const baseSeriesBytes = read(path.join(base, 'candidate/series.json'));
assert.equal(sha(baseSeriesBytes), baseManifest.candidate_series_sha256, 'round14 series drift');
const baseSeries = JSON.parse(baseSeriesBytes.toString('utf8'));
const series = structuredClone(baseSeries);
const change = delta.series_plan_changes[0];
const originPoint = series.plan.chapters.find((chapter) => chapter.key === change.chapter);
assert.ok(originPoint, 'missing origin plan');
assert.equal(originPoint.point.split(change.old_fragment).length, 2, 'origin plan fragment drift');
originPoint.point = originPoint.point.replace(change.old_fragment, change.new_fragment);
assert.ok(originPoint.point.includes(change.new_fragment));
assert.ok(!originPoint.point.includes(change.old_fragment));
const baseExceptPoint = structuredClone(baseSeries);
baseExceptPoint.plan.chapters.find((chapter) => chapter.key === change.chapter).point = originPoint.point;
assert.deepEqual(series, baseExceptPoint, 'unexpected series change');
addOutput('candidate/series.json', json(series));

for (const name of ['source-map.json', 'validation.json']) {
  const bytes = read(path.join(base, name));
  const expected = name === 'source-map.json' ? baseManifest.source_map_sha256 : baseManifest.validation_sha256;
  assert.equal(sha(bytes), expected, `round14 ${name} drift`);
}
const sourceMapBytes = read(path.join(base, 'source-map.json'));
addOutput('source-map.json', sourceMapBytes);

const [{ composeStory, cuteStoryVisualProblems }, { lintVideo }, { estimateTimeline }] = await Promise.all([
  import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/lint.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs'))),
]);
const archivedVideo = parse(path.join(round10, 'evidence/round9-composed-video.json'));
const makePreview = (info) => composeStory({
  slug: baseManifest.slug,
  info,
  chapters,
  voice: archivedVideo.voice,
  drama: { music_enabled: Boolean(archivedVideo.music) },
  root,
  videoId: archivedVideo.youtube.video_id ?? null,
});
const preview = makePreview(series);
const basePreview = makePreview(baseSeries);
assert.deepEqual(preview.scenes, basePreview.scenes, 'plan delta changed scenes');
assert.deepEqual(preview.claims, basePreview.claims, 'plan delta changed claims');
const narration = preview.scenes.flatMap((scene) => scene.lines.map((line) => ({
  scene_id: scene.id, line_id: line.id, text: line.text,
})));
const baseNarration = basePreview.scenes.flatMap((scene) => scene.lines.map((line) => ({
  scene_id: scene.id, line_id: line.id, text: line.text,
})));
assert.deepEqual(narration, baseNarration, 'plan delta changed narration');
const context = {
  lexicon: parse(path.join(round10, 'evidence/round9-lexicon.json')),
  brief: read(path.join(round10, 'evidence/round9-brief.md')).toString('utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(preview, context);
const cute = cuteStoryVisualProblems(preview);
const timing = Object.fromEntries([250, 300, 320, 340].map((cpm) => {
  const current = estimateTimeline(preview, cpm).total_frames / 30;
  const prior = estimateTimeline(basePreview, cpm).total_frames / 30;
  assert.equal(current, prior, `plan delta changed ${cpm} CPM estimate`);
  return [String(cpm), current];
}));
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_FULL_REVIEW',
  base_round14_manifest_sha256: delta.base_manifest_sha256,
  changed_series_plan_fragments: delta.series_plan_changes.map(({ chapter, old_fragment, new_fragment, script_sequence }) => ({
    chapter, old_fragment, new_fragment, script_sequence,
  })),
  changed_spoken_lines: 0,
  changed_scenes: 0,
  changed_claims_or_loops: 0,
  scene_count: preview.scenes.length,
  line_count: narration.length,
  narration_sha256: sha(json(narration)),
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_warnings: lint.warnings,
  cute_errors: cute,
  estimated_timing_not_tts: timing,
  independent_full_script_review: 'NOT_RUN',
  genuine_narrative_panel: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  generated_images_or_audio: 0,
};
addOutput('validation.json', json(validation));
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  slug: baseManifest.slug,
  base_round14_manifest_sha256: delta.base_manifest_sha256,
  base_chapter_sha256: baseManifest.candidate_chapter_sha256,
  base_series_sha256: baseManifest.candidate_series_sha256,
  base_source_map_sha256: baseManifest.source_map_sha256,
  delta_sha256: sha(read(path.join(here, 'delta.json'))),
  series_plan_allowlist: ['origin.point'],
  series_plan_fragment_count: 1,
  candidate_chapter_sha256: Object.fromEntries(chaptersInOrder.map((key) => [key, sha(output.get(`candidate/chapters/${key}.json`))])),
  candidate_series_sha256: sha(output.get('candidate/series.json')),
  source_map_sha256: sha(output.get('source-map.json')),
  validation_sha256: sha(output.get('validation.json')),
  narration_sha256: validation.narration_sha256,
  inherited_round9_narrative_passed: false,
  authorizes_host_install_or_paid_media: false,
};
addOutput('manifest.json', json(manifest));

const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of output) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(`${here}${path.sep}`), `unsafe output path ${name}`);
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), `missing generated ${name}`);
    assert.ok(read(file).equals(bytes), `stale generated ${name}`);
  }
}
assert.equal(lint.errors.length, 0, `lint errors: ${JSON.stringify(lint.errors)}`);
assert.equal(cute.length, 0, `cute visual errors: ${JSON.stringify(cute)}`);
console.log(JSON.stringify({ action, status: validation.status, scenes: validation.scene_count,
  lines: validation.line_count, changed_spoken_lines: 0, lint_errors: lint.errors.length,
  lint_warnings: lint.warnings.length, cute_errors: cute.length, estimated_seconds_not_tts: timing }));
