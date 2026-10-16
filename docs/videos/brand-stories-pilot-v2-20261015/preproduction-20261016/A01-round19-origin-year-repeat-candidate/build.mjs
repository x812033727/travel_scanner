import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const base = path.resolve(here, '../A01-round18-n14-provenance-candidate');
const round10 = path.resolve(here, '../A01-round10-candidate');
const chapterKeys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const read = (file) => fs.readFileSync(file);
const parse = (file) => JSON.parse(read(file).toString('utf8'));
const json = (value) => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const output = new Map();

const baseManifestBytes = read(path.join(base, 'manifest.json'));
const baseManifest = JSON.parse(baseManifestBytes.toString('utf8'));
const deltaBytes = read(path.join(here, 'delta.json'));
const delta = JSON.parse(deltaBytes.toString('utf8'));
assert.equal(delta.status, 'OFFLINE_NARRATION_DELTA_PENDING_INDEPENDENT_REVIEW');
assert.equal(delta.base, 'A01-round18-n14-provenance-candidate');
assert.equal(sha(baseManifestBytes), delta.base_manifest_sha256, 'frozen round18 manifest drift');
assert.equal(baseManifest.status, 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE');
assert.deepEqual([delta.chapter, delta.scene_id, delta.line_id, delta.claim_id],
  ['origin', 'origin-01', 'zc7k', 'o22']);

const chapters = {};
for (const key of chapterKeys) {
  const name = `candidate/chapters/${key}.json`;
  const bytes = read(path.join(base, name));
  assert.equal(sha(bytes), baseManifest.candidate_chapter_sha256[key], `round18 ${name} drift`);
  chapters[key] = JSON.parse(bytes.toString('utf8'));
  assert.equal(chapters[key].key, key);
  if (key !== 'origin') output.set(name, bytes);
}
const origin = chapters.origin;
const oldOrigin = structuredClone(origin);
const scene = origin.scenes.find(({ id }) => id === delta.scene_id);
assert.ok(scene);
const line = scene.lines.find(({ id }) => id === delta.line_id);
const claim = origin.claims.find(({ id }) => id === delta.claim_id);
assert.ok(line && claim);
assert.equal(line.text, delta.old);
assert.equal(claim.claim, delta.old);
assert.equal(claim.scene, delta.scene_id);
assert.equal(claim.source, 8);
assert.equal(claim.fact, 5);
assert.equal(claim.verdict, 'PENDING');
const preceding = origin.scenes.find(({ id }) => id === 'origin-r12-01')?.lines.find(({ id }) => id === 'r12o01');
assert.ok(preceding);
assert.equal(preceding.text, '1928 年出發前，安妮塔問：人為什麼得像馱馬一樣搬行李？這是溫尼特卡歷史學會引述她遊記的話。');
line.text = delta.new;
claim.claim = delta.new;
const originWithOldValues = structuredClone(origin);
originWithOldValues.scenes.find(({ id }) => id === delta.scene_id).lines.find(({ id }) => id === delta.line_id).text = delta.old;
originWithOldValues.claims.find(({ id }) => id === delta.claim_id).claim = delta.old;
assert.deepEqual(originWithOldValues, oldOrigin, 'unrelated origin fields drift');
output.set('candidate/chapters/origin.json', json(origin));

const seriesBytes = read(path.join(base, 'candidate/series.json'));
assert.equal(sha(seriesBytes), baseManifest.candidate_series_sha256, 'round18 series drift');
const series = JSON.parse(seriesBytes.toString('utf8'));
assert.match(series.plan.chapters.find(({ key }) => key === 'origin').point, /1928 年出發前/);
assert.match(series.plan.must_verify[5].claim, /1928 年/);
assert.match(series.plan.sources[8].supports, /1928/);
output.set('candidate/series.json', seriesBytes);

const baseMapBytes = read(path.join(base, 'source-map.json'));
assert.equal(sha(baseMapBytes), baseManifest.source_map_sha256, 'round18 source map drift');
const sourceMap = JSON.parse(baseMapBytes.toString('utf8'));
assert.equal(sourceMap.lines.length, 27);
const oldMap = structuredClone(sourceMap);
const row = sourceMap.lines.find(({ line_id }) => line_id === delta.line_id);
assert.ok(row);
assert.deepEqual([row.chapter, row.scene_id, row.claim_id], [delta.chapter, delta.scene_id, delta.claim_id]);
assert.equal(row.text, delta.old);
assert.equal(row.source_index, 8);
assert.equal(row.fact_index, 5);
assert.equal(row.verdict, 'PENDING_INDEPENDENT_REVIEW');
row.text = delta.new;
const mapWithOldValue = structuredClone(sourceMap);
mapWithOldValue.lines.find(({ line_id }) => line_id === delta.line_id).text = delta.old;
assert.deepEqual(mapWithOldValue, oldMap, 'unrelated source map fields drift');
for (const active of sourceMap.lines) {
  const actual = chapters[active.chapter].scenes.find(({ id }) => id === active.scene_id)
    ?.lines.find(({ id }) => id === active.line_id)?.text;
  assert.equal(actual, active.text, `active map narration drift ${active.line_id}`);
}
output.set('source-map.json', json(sourceMap));

const [{ composeStory, cuteStoryVisualProblems }, { lintVideo }, { estimateTimeline, spokenUnits }] = await Promise.all([
  import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/lint.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs'))),
]);
const archivedVideo = parse(path.join(round10, 'evidence/round9-composed-video.json'));
const makePreview = (info, allChapters) => composeStory({
  slug: baseManifest.slug,
  info,
  chapters: allChapters,
  voice: archivedVideo.voice,
  drama: { music_enabled: Boolean(archivedVideo.music) },
  root,
  videoId: archivedVideo.youtube.video_id ?? null,
});
const preview = makePreview(series, chapters);
const baseChapters = Object.fromEntries(chapterKeys.map((key) => [key, parse(path.join(base, 'candidate/chapters', `${key}.json`))]));
const basePreview = makePreview(series, baseChapters);
const narration = (video) => video.scenes.flatMap((item) => item.lines.map((spoken) => ({
  scene_id: item.id, line_id: spoken.id, text: spoken.text,
})));
const lines = narration(preview);
const baseLines = narration(basePreview);
assert.equal(preview.scenes.length, 79);
assert.equal(lines.length, 108);
assert.deepEqual(lines.map(({ scene_id, line_id }) => [scene_id, line_id]),
  baseLines.map(({ scene_id, line_id }) => [scene_id, line_id]));
assert.deepEqual(lines.filter(({ line_id }) => line_id !== delta.line_id),
  baseLines.filter(({ line_id }) => line_id !== delta.line_id), 'unrelated narration drift');
assert.equal(sha(json(baseLines)), baseManifest.narration_sha256, 'round18 narration drift');
assert.equal(lines.find(({ line_id }) => line_id === delta.line_id).text, delta.new);
const context = {
  lexicon: parse(path.join(round10, 'evidence/round9-lexicon.json')),
  brief: read(path.join(round10, 'evidence/round9-brief.md')).toString('utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(preview, context);
const cute = cuteStoryVisualProblems(preview);
const timing = Object.fromEntries([250, 300, 320, 340].map((cpm) => [String(cpm), {
  round18_seconds: estimateTimeline(basePreview, cpm).total_frames / 30,
  round19_seconds: estimateTimeline(preview, cpm).total_frames / 30,
}]));
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_FULL_REVIEW',
  base_round18_manifest_sha256: delta.base_manifest_sha256,
  changed_lines: [{
    chapter: delta.chapter,
    scene_id: delta.scene_id,
    line_id: delta.line_id,
    old: delta.old,
    text: delta.new,
    spoken_units_delta: spokenUnits(delta.new) - spokenUnits(delta.old),
  }],
  changed_active_source_rows: [delta.line_id],
  preserved_1928_factual_pins: true,
  scene_count: preview.scenes.length,
  line_count: lines.length,
  narration_sha256: sha(json(lines)),
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_warnings: lint.warnings,
  cute_errors: cute,
  estimated_timing_not_tts: timing,
  independent_full_script_review: 'NOT_RUN_FOR_ROUND19',
  genuine_narrative_panel: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  generated_images_or_audio: 0,
};
output.set('validation.json', json(validation));
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  slug: baseManifest.slug,
  base_round18_manifest_sha256: delta.base_manifest_sha256,
  base_chapter_sha256: baseManifest.candidate_chapter_sha256,
  base_series_sha256: baseManifest.candidate_series_sha256,
  base_source_map_sha256: baseManifest.source_map_sha256,
  delta_sha256: sha(deltaBytes),
  candidate_chapter_sha256: Object.fromEntries(chapterKeys.map((key) => [key, sha(output.get(`candidate/chapters/${key}.json`))])),
  candidate_series_sha256: sha(output.get('candidate/series.json')),
  source_map_sha256: sha(output.get('source-map.json')),
  validation_sha256: sha(output.get('validation.json')),
  narration_sha256: validation.narration_sha256,
  inherited_round9_narrative_passed: false,
  authorizes_host_install_or_paid_media: false,
};
output.set('manifest.json', json(manifest));

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
  lines: validation.line_count, changed_spoken_lines: 1, changed_active_source_rows: 1,
  lint_errors: lint.errors.length, lint_warnings: lint.warnings.length,
  cute_errors: cute.length, estimated_seconds_not_tts: timing }));
