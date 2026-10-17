import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const base = path.resolve(here, '../A01-round16-origin-plan-alignment-candidate');
const round10 = path.resolve(here, '../A01-round10-candidate');
const chapterKeys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const read = (file) => fs.readFileSync(file);
const parse = (file) => JSON.parse(read(file).toString('utf8'));
const json = (value) => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const output = new Map();
const addOutput = (name, value) => output.set(name, json(value));
const baseManifestBytes = read(path.join(base, 'manifest.json'));
const baseManifest = JSON.parse(baseManifestBytes.toString('utf8'));
const delta = parse(path.join(here, 'delta.json'));
assert.equal(baseManifest.status, 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE');
assert.equal(delta.status, 'OFFLINE_SOURCE_BOUND_DELTA_PENDING_INDEPENDENT_REVIEW');
assert.equal(delta.base, 'A01-round16-origin-plan-alignment-candidate');
assert.equal(sha(baseManifestBytes), delta.base_manifest_sha256, 'frozen round16 manifest drift');
assert.deepEqual(delta.line_changes.map(({ line_id }) => line_id), ['r12o03', '4prs', 'r12e07']);
assert.deepEqual(delta.prompt_changes.map(({ scene_id }) => scene_id), ['origin-r12-03', 'engine-r12-07']);
assert.deepEqual(delta.series_plan_changes.map(({ chapter }) => chapter), ['origin', 'engine']);
assert.deepEqual(delta.source_matrix_additions.map(({ line_id }) => line_id), ['9ij6', 'tszs']);
assert.equal(delta.claim_source_changes.length, 1);
assert.equal(delta.claim_source_changes[0].claim_id, 'n14');

const chapters = {};
for (const key of chapterKeys) {
  const file = path.join(base, 'candidate/chapters', `${key}.json`);
  const bytes = read(file);
  assert.equal(sha(bytes), baseManifest.candidate_chapter_sha256[key], `round16 chapter ${key} drift`);
  chapters[key] = JSON.parse(bytes.toString('utf8'));
  assert.equal(chapters[key].key, key);
}
const sceneFor = (chapter, sceneId) => {
  const scene = chapters[chapter]?.scenes.find(({ id }) => id === sceneId);
  assert.ok(scene, `missing ${chapter}/${sceneId}`);
  return scene;
};
const lineFor = (chapter, sceneId, lineId) => {
  const line = sceneFor(chapter, sceneId).lines.find(({ id }) => id === lineId);
  assert.ok(line, `missing ${chapter}/${sceneId}/${lineId}`);
  return line;
};
const claimFor = (chapter, claimId) => {
  const claim = chapters[chapter]?.claims.find(({ id }) => id === claimId);
  assert.ok(claim, `missing ${chapter} claim ${claimId}`);
  return claim;
};
for (const change of delta.line_changes) {
  const line = lineFor(change.chapter, change.scene_id, change.line_id);
  const claim = claimFor(change.chapter, change.claim_id);
  assert.equal(line.text, change.old, `base narration drift ${change.line_id}`);
  assert.equal(claim.claim, change.old, `base claim drift ${change.claim_id}`);
  assert.equal(claim.scene, change.scene_id);
  line.text = change.new;
  claim.claim = change.new;
  claim.verdict = 'PENDING';
  claim.note = `Round17 source-bound narrowing; ${change.source_location}. Exact revised claim needs fresh independent verifier/listener/full-script review; prior verdict is historical.`;
}
for (const change of delta.prompt_changes) {
  const scene = sceneFor(change.chapter, change.scene_id);
  assert.equal(scene.data.prompt, change.old, `base visual drift ${change.scene_id}`);
  scene.data.prompt = change.new;
}

const baseSeriesBytes = read(path.join(base, 'candidate/series.json'));
assert.equal(sha(baseSeriesBytes), baseManifest.candidate_series_sha256, 'round16 series drift');
const series = JSON.parse(baseSeriesBytes.toString('utf8'));
for (const change of delta.series_plan_changes) {
  const chapter = series.plan.chapters.find(({ key }) => key === change.chapter);
  assert.ok(chapter, `missing plan ${change.chapter}`);
  assert.equal(chapter.point.split(change.old_fragment).length, 2, `plan fragment drift ${change.chapter}`);
  chapter.point = chapter.point.replace(change.old_fragment, change.new_fragment);
}
const sourceChange = delta.series_source_supports_change;
assert.equal(sourceChange.source_index, 8);
const source = series.plan.sources[sourceChange.source_index];
assert.equal(source.url, 'https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/');
assert.equal(source.supports.split(sourceChange.old_fragment).length, 2, 'WHS supports drift');
source.supports = source.supports.replace(sourceChange.old_fragment, sourceChange.new_fragment);
const newFactIndex = series.plan.must_verify.length;
assert.equal(newFactIndex, 14, 'must_verify numbering drift');
assert.equal(delta.must_verify_append.sources.length, 1);
assert.equal(delta.must_verify_append.sources[0], 8);
series.plan.must_verify.push(delta.must_verify_append);
const museumClaim = claimFor('origin', 'o20');
assert.equal(museumClaim.fact, null, 'museum fact already bound');
museumClaim.fact = newFactIndex;
museumClaim.verdict = 'PENDING';
museumClaim.note += ` Round17 plan adds must_verify[${newFactIndex}] for the museum item and uncertain identity; not a verifier PASS.`;
for (const change of delta.claim_source_changes) {
  const claim = claimFor(change.chapter, change.claim_id);
  assert.equal(claim.source, change.old_source, `claim source drift ${change.claim_id}`);
  claim.source = change.new_source;
  claim.verdict = 'PENDING';
  claim.note = `Round17 source scope: ${change.reason} Original round11 NOT FOUND and later pending rebound remain historical; fresh independent review required.`;
}
for (const key of chapterKeys) addOutput(`candidate/chapters/${key}.json`, chapters[key]);
addOutput('candidate/series.json', series);

const baseMapBytes = read(path.join(base, 'source-map.json'));
assert.equal(sha(baseMapBytes), baseManifest.source_map_sha256, 'round16 source map drift');
const sourceMap = JSON.parse(baseMapBytes.toString('utf8'));
assert.equal(sourceMap.lines.length, 25);
for (const change of delta.line_changes) {
  const row = sourceMap.lines.find(({ line_id }) => line_id === change.line_id);
  assert.ok(row, `missing map ${change.line_id}`);
  assert.equal(row.chapter, change.chapter);
  assert.equal(row.scene_id, change.scene_id);
  assert.equal(row.claim_id, change.claim_id);
  assert.equal(row.text, change.old, `source map drift ${change.line_id}`);
  row.previous_round16_text = change.old;
  row.text = change.new;
  row.source_location = change.source_location;
  row.support_type = change.support_type;
  row.verdict = 'PENDING_INDEPENDENT_REVIEW';
  row.round17_change = true;
  if (delta.prompt_changes.some(({ scene_id }) => scene_id === change.scene_id)) row.visual_prompt_changed = true;
}
const museumRow = sourceMap.lines.find(({ line_id }) => line_id === '83ew');
assert.ok(museumRow && museumRow.fact_index === null && museumRow.claim_id === 'o20');
museumRow.fact_index = newFactIndex;
museumRow.round17_fact_binding = true;
for (const addition of delta.source_matrix_additions) {
  assert.ok(!sourceMap.lines.some(({ line_id }) => line_id === addition.line_id), `duplicate map ${addition.line_id}`);
  const line = lineFor(addition.chapter, addition.scene_id, addition.line_id);
  const claim = claimFor(addition.chapter, addition.claim_id);
  assert.equal(claim.scene, addition.scene_id);
  assert.equal(claim.source, addition.source_index, `source scope ${addition.line_id}`);
  assert.equal(claim.fact, addition.fact_index, `fact scope ${addition.line_id}`);
  sourceMap.lines.push({
    ...addition,
    text: line.text,
    source_url: Number.isInteger(addition.source_index) ? series.plan.sources[addition.source_index].url : null,
    verdict: 'PENDING_INDEPENDENT_REVIEW',
    round17_addition: true,
  });
}
assert.equal(sourceMap.lines.length, 27);
assert.equal(new Set(sourceMap.lines.map(({ line_id }) => line_id)).size, 27);
for (const row of sourceMap.lines) {
  assert.equal(lineFor(row.chapter, row.scene_id, row.line_id).text, row.text, `map text drift ${row.line_id}`);
}
sourceMap.status = 'PENDING_INDEPENDENT_REVIEW';
sourceMap.base = delta.base;
sourceMap.notes.push('Round17 narrows three spoken claims to the original archive/patent scope, adjusts two illustrative prompts, adds a museum-object fact to the plan, records both lines of the family-case claim and the final general physics statement, and leaves all prior verifier/NOT FOUND history intact. This is offline pending evidence, not a script-review receipt.');
addOutput('source-map.json', sourceMap);

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
const basePreview = makePreview(parse(path.join(base, 'candidate/series.json')), baseChapters);
const narration = (video) => video.scenes.flatMap((scene) => scene.lines.map((line) => ({
  scene_id: scene.id, line_id: line.id, text: line.text,
})));
const lines = narration(preview);
const baseLines = narration(basePreview);
assert.equal(preview.scenes.length, basePreview.scenes.length);
assert.deepEqual(lines.map(({ scene_id, line_id }) => [scene_id, line_id]), baseLines.map(({ scene_id, line_id }) => [scene_id, line_id]));
assert.deepEqual(lines.filter((line) => !delta.line_changes.some(({ line_id }) => line_id === line.line_id)),
  baseLines.filter((line) => !delta.line_changes.some(({ line_id }) => line_id === line.line_id)));
const context = {
  lexicon: parse(path.join(round10, 'evidence/round9-lexicon.json')),
  brief: read(path.join(round10, 'evidence/round9-brief.md')).toString('utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(preview, context);
const cute = cuteStoryVisualProblems(preview);
const timing = Object.fromEntries([250, 300, 320, 340].map((cpm) => [String(cpm), {
  round16_seconds: estimateTimeline(basePreview, cpm).total_frames / 30,
  round17_seconds: estimateTimeline(preview, cpm).total_frames / 30,
}]));
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_FULL_REVIEW',
  base_round16_manifest_sha256: delta.base_manifest_sha256,
  changed_lines: delta.line_changes.map(({ chapter, scene_id, line_id, old, new: text }) => ({
    chapter, scene_id, line_id, old, text, spoken_units_delta: spokenUnits(text) - spokenUnits(old),
  })),
  changed_visual_prompts: delta.prompt_changes.map(({ chapter, scene_id }) => ({ chapter, scene_id })),
  added_source_matrix_lines: delta.source_matrix_additions.map(({ line_id }) => line_id),
  added_must_verify_index: newFactIndex,
  scene_count: preview.scenes.length,
  line_count: lines.length,
  narration_sha256: sha(json(lines)),
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
addOutput('validation.json', validation);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  slug: baseManifest.slug,
  base_round16_manifest_sha256: delta.base_manifest_sha256,
  base_chapter_sha256: baseManifest.candidate_chapter_sha256,
  base_series_sha256: baseManifest.candidate_series_sha256,
  base_source_map_sha256: baseManifest.source_map_sha256,
  delta_sha256: sha(read(path.join(here, 'delta.json'))),
  candidate_chapter_sha256: Object.fromEntries(chapterKeys.map((key) => [key, sha(output.get(`candidate/chapters/${key}.json`))])),
  candidate_series_sha256: sha(output.get('candidate/series.json')),
  source_map_sha256: sha(output.get('source-map.json')),
  validation_sha256: sha(output.get('validation.json')),
  narration_sha256: validation.narration_sha256,
  inherited_round9_narrative_passed: false,
  authorizes_host_install_or_paid_media: false,
};
addOutput('manifest.json', manifest);

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
  lines: validation.line_count, changed_spoken_lines: delta.line_changes.length,
  lint_errors: lint.errors.length, lint_warnings: lint.warnings.length,
  cute_errors: cute.length, estimated_seconds_not_tts: timing }));
