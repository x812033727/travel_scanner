import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const previous = path.resolve(here, '../A01-round12-candidate');
const round10 = path.resolve(here, '../A01-round10-candidate');
const chaptersInOrder = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const read = (file) => fs.readFileSync(file);
const parse = (file) => JSON.parse(read(file).toString('utf8'));
const json = (value) => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const output = new Map();
const addOutput = (name, value) => output.set(name, json(value));
const priorManifest = parse(path.join(previous, 'manifest.json'));
const delta = parse(path.join(here, 'delta.json'));
assert.equal(priorManifest.status, 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE');
assert.equal(delta.status, 'OFFLINE_EDITORIAL_DELTA_PENDING_INDEPENDENT_REVIEW');
assert.equal(delta.base, 'A01-round12-candidate');
assert.equal(delta.changes.length, 4);
assert.equal(delta.loop_changes.length, 3);
assert.deepEqual(delta.changes.map(({ chapter, scene_id, line_id }) => `${chapter}/${scene_id}/${line_id}`), [
  'hook/hook-03/6h2q', 'origin/origin-r12-01/r12o01', 'origin/origin-06/83ew', 'idea/idea-07b/76ur',
]);
assert.deepEqual(delta.loop_changes.map(({ chapter, setup }) => `${chapter}/${setup}`), [
  'hook/6h2q', 'origin/6h2q', 'idea/b6mn',
]);

const chapters = {};
for (const key of chaptersInOrder) {
  const file = path.join(previous, 'candidate/chapters', `${key}.json`);
  const bytes = read(file);
  assert.equal(sha(bytes), priorManifest.candidate_chapter_sha256[key], `round12 chapter ${key}`);
  chapters[key] = JSON.parse(bytes.toString('utf8'));
  assert.equal(chapters[key].key, key);
}
const seriesBytes = read(path.join(previous, 'candidate/series.json'));
assert.equal(sha(seriesBytes), priorManifest.candidate_series_sha256);
const series = JSON.parse(seriesBytes.toString('utf8'));
const sourceMapBytes = read(path.join(previous, 'source-map.json'));
assert.equal(sha(sourceMapBytes), priorManifest.source_map_sha256);
const sourceMap = JSON.parse(sourceMapBytes.toString('utf8'));
assert.equal(sourceMap.lines.length, 22);

const changedLines = new Set();
for (const change of delta.changes) {
  const chapter = chapters[change.chapter];
  const scene = chapter?.scenes.find((item) => item.id === change.scene_id);
  const line = scene?.lines.find((item) => item.id === change.line_id);
  assert.ok(line, `missing ${change.chapter}/${change.scene_id}/${change.line_id}`);
  assert.equal(line.text, change.old, `source drift at ${change.line_id}`);
  assert.ok(!changedLines.has(change.line_id), `duplicate line ${change.line_id}`);
  assert.ok(change.source_url.startsWith('https://') && change.source_location && change.support);
  const sourceIndex = series.plan.sources.findIndex((item) => item.url === change.source_url);
  assert.ok(sourceIndex >= 0, `source not indexed for ${change.line_id}`);
  changedLines.add(change.line_id);
  line.text = change.new;

  const claims = chapter.claims.filter((item) => item.scene === change.scene_id);
  const claim = claims.find((item) => item.claim === change.old || item.id === `claim-${change.line_id}` ||
    (change.line_id === '83ew' && item.id === 'o20') || (change.line_id === '76ur' && item.id === 'i17'));
  if (change.line_id !== '6h2q') {
    assert.ok(claim, `missing spoken claim ${change.line_id}`);
    assert.equal(claim.source, sourceIndex, `claim source drift at ${change.line_id}`);
    claim.claim = change.new;
    claim.verdict = 'PENDING';
    claim.note = `Round13 isolated narration change; ${change.source_location}. Fresh independent fact/listener/narrative review required; earlier verdict is historical.`;
  } else {
    assert.equal(claim, undefined, 'hook question must not turn a neighboring fact claim into a new claim');
  }

  const prior = sourceMap.lines.find((item) => item.line_id === change.line_id);
  if (prior) {
    assert.equal(prior.text, change.old, `source-map drift at ${change.line_id}`);
    assert.equal(prior.source_index, sourceIndex, `source-map source drift at ${change.line_id}`);
    prior.previous_round12_text = change.old;
    prior.text = change.new;
    prior.source_location = change.source_location;
    prior.verdict = 'PENDING_INDEPENDENT_REVIEW';
    prior.round13_change = true;
  } else {
    sourceMap.lines.push({
      chapter: change.chapter,
      scene_id: change.scene_id,
      line_id: change.line_id,
      previous_round12_text: change.old,
      text: change.new,
      claim_id: claim?.id ?? null,
      source_index: sourceIndex,
      source_url: change.source_url,
      source_location: change.source_location,
      support_type: change.line_id === '6h2q' ? 'source_bound_narrative_question' : 'direct',
      verdict: 'PENDING_INDEPENDENT_REVIEW',
      round13_change: true,
    });
  }
}
assert.equal(changedLines.size, 4);
assert.equal(sourceMap.lines.length, 24);

for (const change of delta.loop_changes) {
  const chapter = chapters[change.chapter];
  const loop = chapter?.loops.find((item) => item.setup === change.setup);
  assert.ok(loop, `missing loop ${change.chapter}/${change.setup}`);
  assert.equal(loop.what, change.old_what, `loop drift ${change.setup}`);
  if (change.old_payoff !== undefined) {
    assert.equal(loop.payoff, change.old_payoff, `payoff drift ${change.setup}`);
    loop.payoff = change.new_payoff;
  }
  loop.what = change.new_what;
}
assert.equal(chapters.idea.loops.find((item) => item.setup === 'b6mn')?.payoff, '76ur');
assert.equal(chapters.origin.loops.find((item) => item.setup === '6h2q')?.payoff, '3zkh');

sourceMap.status = 'PENDING_INDEPENDENT_REVIEW';
sourceMap.base = 'A01-round12-candidate';
sourceMap.notes.push('Round13 changes exactly four spoken lines and three loop descriptions/payoffs. All historical round12 source and review evidence remains immutable; this delta is pending a fresh independent review.');
for (const key of chaptersInOrder) addOutput(`candidate/chapters/${key}.json`, chapters[key]);
output.set('candidate/series.json', seriesBytes);
addOutput('source-map.json', sourceMap);

const [{ composeStory, cuteStoryVisualProblems }, { lintVideo }, { estimateTimeline, spokenUnits }] = await Promise.all([
  import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/lint.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs'))),
]);
const archivedVideo = parse(path.join(round10, 'evidence/round9-composed-video.json'));
const makePreview = (info, allChapters) => composeStory({
  slug: priorManifest.slug,
  info,
  chapters: allChapters,
  voice: archivedVideo.voice,
  drama: { music_enabled: Boolean(archivedVideo.music) },
  root,
  videoId: archivedVideo.youtube.video_id ?? null,
});
const preview = makePreview(series, chapters);
const priorChapters = Object.fromEntries(chaptersInOrder.map((key) => [key, parse(path.join(previous, 'candidate/chapters', `${key}.json`))]));
const priorPreview = makePreview(series, priorChapters);
const context = {
  lexicon: parse(path.join(round10, 'evidence/round9-lexicon.json')),
  brief: read(path.join(round10, 'evidence/round9-brief.md')).toString('utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(preview, context);
const cute = cuteStoryVisualProblems(preview);
const timing = {};
for (const cpm of [250, 300, 320, 340]) {
  const base = estimateTimeline(priorPreview, cpm);
  const current = estimateTimeline(preview, cpm);
  timing[String(cpm)] = {
    round12_seconds: base.total_frames / 30,
    round13_seconds: current.total_frames / 30,
    delta_seconds: (current.total_frames - base.total_frames) / 30,
  };
}
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_UNREVIEWED',
  changed_lines: delta.changes.map(({ chapter, scene_id, line_id, old, new: text }) => ({
    chapter, scene_id, line_id, old, text, spoken_units_delta: spokenUnits(text) - spokenUnits(old),
  })),
  changed_loops: delta.loop_changes.map(({ chapter, setup, new_payoff }) => ({ chapter, setup, payoff: new_payoff ?? null })),
  scene_count: preview.scenes.length,
  line_count: preview.scenes.reduce((sum, scene) => sum + scene.lines.length, 0),
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_warnings: lint.warnings,
  cute_errors: cute,
  estimated_timing_not_tts: timing,
  independent_fact_review: 'NOT_RUN',
  independent_listener_review: 'NOT_RUN',
  narrative_panel: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  generated_images_or_audio: 0,
};
addOutput('validation.json', validation);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  slug: priorManifest.slug,
  base_round12_manifest_sha256: sha(read(path.join(previous, 'manifest.json'))),
  base_chapter_sha256: priorManifest.candidate_chapter_sha256,
  delta_sha256: sha(read(path.join(here, 'delta.json'))),
  candidate_chapter_sha256: Object.fromEntries(chaptersInOrder.map((key) => [key, sha(output.get(`candidate/chapters/${key}.json`))])),
  candidate_series_sha256: sha(output.get('candidate/series.json')),
  source_map_sha256: sha(output.get('source-map.json')),
  validation_sha256: sha(output.get('validation.json')),
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
console.log(JSON.stringify({ action, status: validation.status, scenes: validation.scene_count, lines: validation.line_count,
  seconds_250: timing['250'].round13_seconds, seconds_300: timing['300'].round13_seconds,
  seconds_320: timing['320'].round13_seconds, lint_errors: lint.errors.length,
  lint_warnings: lint.warnings.length, cute_errors: cute.length }));
