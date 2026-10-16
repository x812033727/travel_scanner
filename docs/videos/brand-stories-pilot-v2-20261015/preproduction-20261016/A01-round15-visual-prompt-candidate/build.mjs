import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const base = path.resolve(here, '../A01-round14-source-bound-loop-candidate');
const round10 = path.resolve(here, '../A01-round10-candidate');
const chapterKeys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const expectedChanges = [
  'hook/hook-01', 'hook/hook-03',
  'origin/origin-06', 'origin/origin-13', 'origin/origin-15',
  'engine/engine-r12-04', 'turn/turn-12',
];
const expectedLongStills = [
  'hook-07', 'origin-r12-01', 'origin-03', 'origin-13', 'origin-14', 'origin-15',
  'idea-02', 'idea-06', 'idea-08', 'idea-10', 'idea-13',
  'turn-01', 'turn-09', 'turn-12', 'turn-15', 'now-01',
];
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const read = (file) => fs.readFileSync(file);
const parse = (file) => JSON.parse(read(file).toString('utf8'));
const encode = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const outputs = new Map();
const put = (name, bytes) => outputs.set(name, bytes);
const baseManifestBytes = read(path.join(base, 'manifest.json'));
const baseManifest = JSON.parse(baseManifestBytes.toString('utf8'));
const deltaBytes = read(path.join(here, 'delta.json'));
const delta = JSON.parse(deltaBytes.toString('utf8'));

assert.equal(baseManifest.status, 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE');
assert.equal(delta.status, 'OFFLINE_VISUAL_PROMPT_DELTA_PENDING_INDEPENDENT_REVIEW');
assert.equal(delta.base, 'A01-round14-source-bound-loop-candidate');
assert.equal(hash(baseManifestBytes), delta.base_manifest_sha256, 'frozen round14 manifest drift');
assert.deepEqual(delta.changes.map((change) => change.chapter + '/' + change.scene_id), expectedChanges);
assert.equal(delta.changes.length, new Set(expectedChanges).size);

const originalChapters = {};
const chapters = {};
for (const key of chapterKeys) {
  const chapterBytes = read(path.join(base, 'candidate/chapters', key + '.json'));
  assert.equal(hash(chapterBytes), baseManifest.candidate_chapter_sha256[key], 'round14 chapter drift: ' + key);
  originalChapters[key] = JSON.parse(chapterBytes.toString('utf8'));
  chapters[key] = structuredClone(originalChapters[key]);
  assert.equal(chapters[key].key, key);
}
const seriesBytes = read(path.join(base, 'candidate/series.json'));
const sourceMapBytes = read(path.join(base, 'source-map.json'));
assert.equal(hash(seriesBytes), baseManifest.candidate_series_sha256, 'round14 series drift');
assert.equal(hash(sourceMapBytes), baseManifest.source_map_sha256, 'round14 source-map drift');
const series = JSON.parse(seriesBytes.toString('utf8'));
assert.deepEqual(series.look, { preset: 'cute-mystery' });
assert.equal(series.image_model, 'image-01');
put('candidate/series.json', seriesBytes);
put('source-map.json', sourceMapBytes);

for (const change of delta.changes) {
  assert.ok(change.reason && change.new && change.old);
  const scene = chapters[change.chapter]?.scenes.find((item) => item.id === change.scene_id);
  assert.ok(scene, 'missing scene ' + change.scene_id);
  assert.equal(scene.template, 'shot', 'only shot prompts may change');
  assert.equal(scene.data.prompt, change.old, 'prompt drift at ' + change.scene_id);
  scene.data.prompt = change.new;
}

const chapterHashes = {};
const lineHashes = {};
const claimHashes = {};
for (const key of chapterKeys) {
  const before = originalChapters[key];
  const after = chapters[key];
  const beforeExceptPrompts = structuredClone(before);
  const afterExceptPrompts = structuredClone(after);
  for (const chapter of [beforeExceptPrompts, afterExceptPrompts]) {
    for (const scene of chapter.scenes) if (scene.template === 'shot') delete scene.data.prompt;
  }
  assert.deepEqual(afterExceptPrompts, beforeExceptPrompts, 'non-prompt change in ' + key);
  const lines = (chapter) => chapter.scenes.flatMap((scene) => scene.lines.map((line) => ({
    scene_id: scene.id, line_id: line.id, text: line.text,
  })));
  assert.deepEqual(lines(after), lines(before), 'narration drift in ' + key);
  assert.deepEqual(after.claims, before.claims, 'claim drift in ' + key);
  const candidateBytes = encode(after);
  put('candidate/chapters/' + key + '.json', candidateBytes);
  chapterHashes[key] = hash(candidateBytes);
  lineHashes[key] = hash(encode(lines(after)));
  claimHashes[key] = hash(encode(after.claims));
}

const [{ composeStory, cuteStoryVisualProblems }, { resolveLook, shotAppearancePrompt, shotCast },
  { lintVideo }, { estimateTimeline }, { composeShotPrompt, IMAGE_PROMPT_LIMITS, imageModelVendor }] = await Promise.all([
  import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/drama.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/lint.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/media/prompt-budget.mjs'))),
]);
const archivedVideo = parse(path.join(round10, 'evidence/round9-composed-video.json'));
const makePreview = (allChapters) => composeStory({
  slug: baseManifest.slug,
  info: series,
  chapters: allChapters,
  voice: archivedVideo.voice,
  drama: { music_enabled: Boolean(archivedVideo.music) },
  root,
  videoId: archivedVideo.youtube.video_id ?? null,
});
const preview = makePreview(chapters);
const basePreview = makePreview(originalChapters);
assert.equal(preview.scenes.length, basePreview.scenes.length);
assert.deepEqual(preview.scenes.map((scene) => [scene.id, scene.template, scene.lines]),
  basePreview.scenes.map((scene) => [scene.id, scene.template, scene.lines]),
  'scene boundaries or spoken lines changed');
assert.equal(imageModelVendor(series.image_model), 'minimax');
const resolvedLook = resolveLook(series.look);
const effectivePrompts = delta.changes.map((change) => {
  const scene = preview.scenes.find((item) => item.id === change.scene_id);
  assert.ok(scene, 'composed scene missing: ' + change.scene_id);
  const cast = shotCast(preview, scene);
  if (scene.id === 'hook-03') assert.deepEqual(cast.map((character) => character.id), ['traveler-heavy']);
  if (scene.id === 'turn-12') assert.deepEqual(cast.map((character) => character.id), ['traveler-upright']);
  const result = composeShotPrompt({
    prompt: scene.data.prompt,
    look: resolvedLook,
    camera: scene.data.camera,
    cast: shotAppearancePrompt(cast),
    limit: IMAGE_PROMPT_LIMITS.minimax,
  });
  assert.equal(result.cutChars, 0, 'MiniMax would truncate prompt: ' + scene.id);
  assert.equal(result.droppedFixes, 0);
  assert.ok(result.prompt.length < IMAGE_PROMPT_LIMITS.minimax, 'MiniMax prompt limit: ' + scene.id);
  return {
    scene_id: scene.id,
    cast_ids: cast.map((character) => character.id),
    characters_appended: cast.map((character) => character.appearance),
    prompt: result.prompt,
    chars: result.prompt.length,
    sha256: hash(Buffer.from(result.prompt)),
  };
});
put('effective-prompts.json', encode({
  status: 'OFFLINE_ASSEMBLED_PROMPT_CHECK_NOT_IMAGE_QA',
  model: series.image_model,
  max_chars_exclusive: IMAGE_PROMPT_LIMITS.minimax,
  prompts: effectivePrompts,
}));
const sourceMap = JSON.parse(sourceMapBytes.toString('utf8'));
const expectedSourcePins = [
  ['hook', 'hook-01', 'h1', 'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469'],
  ['hook', 'hook-03', 'h8', 'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469'],
  ['origin', 'origin-06', 'o20', 'https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/'],
  ['origin', 'origin-13', 'o11', 'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469'],
  ['origin', 'origin-15', 'o14', 'https://patents.google.com/patent/US3653474A/en'],
  ['engine', 'engine-r12-04', 'claim-r12e04', 'https://patents.google.com/patent/US3653474A/en'],
  ['turn', 'turn-12', 't12', 'https://travelpro.com/pages/our-history'],
  ['turn', 'turn-12', 't13', 'https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage'],
];
const sourcePins = expectedSourcePins.map(([chapter, sceneId, claimId, url]) => {
  const claim = chapters[chapter].claims.find((item) => item.id === claimId && item.scene === sceneId);
  assert.ok(claim, 'source-pinned claim missing: ' + claimId);
  assert.equal(series.plan.sources[claim.source]?.url, url, 'source pin drift: ' + claimId);
  return { scene_id: sceneId, claim_id: claimId, source_index: claim.source, source_url: url,
    verdict_inherited: claim.verdict };
});
for (const line of sourceMap.lines.filter((item) => item.scene_id === 'origin-06' ||
  item.scene_id === 'engine-r12-04' || item.scene_id === 'turn-12')) {
  assert.equal(series.plan.sources[line.source_index]?.url, line.source_url,
    'source-map plan URL drift: ' + line.line_id);
}
const context = {
  lexicon: parse(path.join(round10, 'evidence/round9-lexicon.json')),
  brief: read(path.join(round10, 'evidence/round9-brief.md')).toString('utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(preview, context);
const cuteErrors = cuteStoryVisualProblems(preview);
const estimates = {};
for (const cpm of [250, 300, 320]) {
  const timeline = estimateTimeline(preview, cpm);
  const baseTimeline = estimateTimeline(basePreview, cpm);
  assert.equal(timeline.total_frames, baseTimeline.total_frames, 'prompt change affected duration');
  estimates[String(cpm)] = timeline.total_frames / 30;
  if (cpm === 250) {
    const longStills = timeline.scenes
      .filter((scene) => scene.template === 'shot' && (scene.end_frame - scene.start_frame) / 30 > 10)
      .map((scene) => ({ id: scene.id, estimated_seconds: Math.round((scene.end_frame - scene.start_frame) / 30 * 100) / 100 }));
    assert.deepEqual(longStills.map((scene) => scene.id), expectedLongStills,
      '250 CPM long-still cohort changed');
    estimates.long_stills_over_10_seconds_at_250 = longStills;
  }
}
const validation = {
  status: 'OFFLINE_PROMPT_ONLY_PENDING_INDEPENDENT_VISUAL_REVIEW',
  changed_scene_ids: delta.changes.map((change) => change.scene_id),
  scene_count: preview.scenes.length,
  spoken_line_count: preview.scenes.reduce((sum, scene) => sum + scene.lines.length, 0),
  line_sha256_by_chapter: lineHashes,
  claims_sha256_by_chapter: claimHashes,
  series_sha256_unchanged: hash(seriesBytes),
  source_map_sha256_unchanged: hash(sourceMapBytes),
  effective_prompt_sha256: hash(outputs.get('effective-prompts.json')),
  effective_prompt_minimax_limit: IMAGE_PROMPT_LIMITS.minimax,
  effective_prompt_char_counts: effectivePrompts.map((item) => ({
    scene_id: item.scene_id, cast_ids: item.cast_ids, chars: item.chars,
  })),
  source_pins: sourcePins,
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_warnings: lint.warnings,
  cute_story_visual_errors: cuteErrors,
  estimated_timing_not_tts: estimates,
  independent_visual_source_review: 'NOT_RUN',
  three_shot_pilot: 'PLAN_ONLY_NOT_GENERATED',
  generated_images_audio_or_video: 0,
  script_review_receipt: 'NOT_ISSUED',
};
put('validation.json', encode(validation));
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_VISUAL_CANDIDATE',
  slug: baseManifest.slug,
  base_round14_manifest_sha256: hash(baseManifestBytes),
  base_chapter_sha256: baseManifest.candidate_chapter_sha256,
  base_series_sha256: baseManifest.candidate_series_sha256,
  base_source_map_sha256: baseManifest.source_map_sha256,
  delta_sha256: hash(deltaBytes),
  readme_sha256: hash(read(path.join(here, 'README.md'))),
  pilot_plan_sha256: hash(read(path.join(here, 'THREE-SHOT-PILOT.md'))),
  candidate_chapter_sha256: chapterHashes,
  candidate_series_sha256: hash(outputs.get('candidate/series.json')),
  source_map_sha256: hash(outputs.get('source-map.json')),
  effective_prompts_sha256: hash(outputs.get('effective-prompts.json')),
  validation_sha256: hash(outputs.get('validation.json')),
  narration_or_claim_changes: 0,
  approved_or_deployed: false,
  authorizes_host_install_or_paid_media: false,
};
put('manifest.json', encode(manifest));

const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'unsafe output path: ' + name);
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), 'missing generated file: ' + name);
    assert.ok(read(file).equals(bytes), 'stale generated file: ' + name);
  }
}
assert.equal(lint.errors.length, 0, 'video lint errors');
assert.equal(cuteErrors.length, 0, 'cute story visual errors');
console.log(JSON.stringify({
  action, status: validation.status, scenes: validation.scene_count,
  lines: validation.spoken_line_count, prompt_changes: delta.changes.length,
  lint_errors: lint.errors.length, lint_warnings: lint.warnings.length,
  cute_errors: cuteErrors.length,
  long_stills_over_10_seconds_at_250: estimates.long_stills_over_10_seconds_at_250.length,
}));
