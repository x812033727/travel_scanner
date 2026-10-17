import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Read-only verification of an offline editorial package. No network, host, provider, or writes.
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const bytes = (relative) => fs.readFileSync(path.join(here, relative));
const sha = (relative) => hash(bytes(relative));
const json = (relative) => JSON.parse(bytes(relative).toString('utf8'));
const eqSha = (relative, expected) => assert.equal(sha(relative), expected, relative);
const substitute = (base, before, after, offsetExpected = null) => {
  const oldBytes = Buffer.from(before, 'utf8');
  const newBytes = Buffer.from(after, 'utf8');
  const offset = base.indexOf(oldBytes);
  assert.ok(offset >= 0, `missing ${before}`);
  assert.equal(base.indexOf(oldBytes, offset + 1), -1, `not unique ${before}`);
  if (offsetExpected !== null) assert.equal(offset, offsetExpected);
  return Buffer.concat([base.subarray(0, offset), newBytes, base.subarray(offset + oldBytes.length)]);
};

const allFiles = [];
const visit = (directory) => {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const full = path.join(directory, entry.name);
    if (entry.isDirectory()) visit(full);
    else if (entry.isFile()) allFiles.push(path.relative(here, full).replaceAll('\\', '/'));
    else throw new Error(`unexpected link or special file: ${full}`);
  }
};
visit(here);
for (const relative of allFiles.filter((name) => name.endsWith('.json'))) json(relative);
assert.ok(allFiles.every((name) => /\.(?:json|md|mjs)$/.test(name)), 'unexpected binary/media file');
const inventory = json('files.sha256.json');
assert.equal(inventory.status, 'UNREVIEWED_OFFLINE_CANDIDATE');
assert.equal(inventory.self_excluded, 'files.sha256.json');
assert.deepEqual(
  inventory.files.map((row) => row.file).sort(),
  allFiles.filter((name) => name !== 'files.sha256.json').sort(),
  'file inventory is incomplete or stale',
);
for (const row of inventory.files) {
  assert.equal(bytes(row.file).length, row.bytes, `inventory bytes ${row.file}`);
  eqSha(row.file, row.sha256);
}
const manifest = json('manifest.json');
const inverse = json('inverse-diff.json');
const validation = json('validation.json');
const prior = json('prior-two-line/manifest.json');
const priorInverse = json('prior-two-line/inverse-diff.json');
const narrative = json('evidence/round9-narrative.json');
assert.equal(manifest.status, 'UNREVIEWED_OFFLINE_CANDIDATE');
assert.equal(prior.status, 'UNREVIEWED_OFFLINE_CANDIDATE');
assert.equal(narrative.round, 9);
assert.equal(narrative.passed, false);
assert.deepEqual(narrative.failed, ['chapters_link', 'payoffs', 'one_thread']);
assert.deepEqual(manifest.round9_failed, narrative.failed);
eqSha('prior-two-line/manifest.json', manifest.previous_two_line_manifest_sha256);
eqSha('prior-two-line/inverse-diff.json', manifest.previous_two_line_inverse_sha256);
eqSha('prior-two-line/validation.json', prior.validation_file_sha256);
eqSha('prior-two-line/now.json', prior.candidate_chapters_sha256.now);
eqSha('inverse-diff.json', manifest.inverse_file_sha256);
eqSha('validation.json', manifest.validation_file_sha256);
eqSha('visual-warning-audit.md', 'b6e678d3f910e53136dcf54909b0d8937bc4b01421ccd9822defb722038da97c');
eqSha('evidence/round9-narrative.json', manifest.round9_narrative_sha256);
eqSha('evidence/round9-series.json', prior.source_series_sha256);
eqSha('evidence/round9-composed-video.json', prior.source_video_sha256);
eqSha('evidence/round9-brief.md', prior.source_brief_sha256);
eqSha('evidence/round9-lexicon.json', prior.source_lexicon_sha256);
assert.deepEqual(manifest.changes, inverse.steps_in_forward_order);
assert.deepEqual(prior.changes, priorInverse.changes);
assert.deepEqual(manifest.changes.map((change) => change.line_id ?? change.claim_id), ['zc7k', '7asx', 'n1']);

const source = {};
const candidate = {};
for (const key of keys) {
  const sourceRelative = `source/chapters/${key}.json`;
  const candidateRelative = `candidate/chapters/${key}.json`;
  eqSha(sourceRelative, manifest.source_chapters_sha256[key]);
  eqSha(candidateRelative, manifest.candidate_chapters_sha256[key]);
  source[key] = bytes(sourceRelative);
  candidate[key] = bytes(candidateRelative);
}
let origin = source.origin;
let now = source.now;
const [originLine, nowLine, claim] = manifest.changes;
origin = substitute(origin, originLine.before, originLine.after, originLine.byte_offset);
now = substitute(now, nowLine.before, nowLine.after, nowLine.byte_offset);
assert.equal(hash(now), sha('prior-two-line/now.json'));
assert.equal(claim.byte_offset, now.indexOf(Buffer.from(claim.before, 'utf8')));
now = substitute(now, claim.before, claim.after, claim.byte_offset);
assert.ok(origin.equals(candidate.origin));
assert.ok(now.equals(candidate.now));
origin = substitute(origin, originLine.after, originLine.before);
now = substitute(now, claim.after, claim.before);
now = substitute(now, nowLine.after, nowLine.before);
assert.ok(origin.equals(source.origin));
assert.ok(now.equals(source.now));
for (const key of keys.filter((item) => !['origin', 'now'].includes(item))) {
  assert.ok(source[key].equals(candidate[key]), `${key} unexpectedly changed`);
}
const oldNow = json('source/chapters/now.json');
const newNow = json('candidate/chapters/now.json');
const oldClaim = oldNow.claims.find((row) => row.id === 'n1');
const newClaim = newNow.claims.find((row) => row.id === 'n1');
assert.deepEqual(Object.keys(oldClaim), ['id', 'claim', 'scene', 'source', 'fact', 'verdict', 'note']);
assert.equal(newClaim.scene, 'now-01');
assert.equal(newClaim.source, 11);
assert.equal(newClaim.fact, 9);
assert.equal(newClaim.verdict, 'PLAN');
assert.equal(newClaim.note, oldClaim.note);
assert.equal(newClaim.claim, claim.after);
assert.equal(newNow.scenes[0].lines[0].id, '7asx');
assert.equal(newNow.scenes[0].lines[0].text, nowLine.after);

const storyModule = path.join(root, 'tools/video/automation/story.mjs');
const lintModule = path.join(root, 'tools/video/core/lint.mjs');
const timelineModule = path.join(root, 'tools/video/core/timeline.mjs');
assert.equal(hash(fs.readFileSync(storyModule)), validation.renderer.story_module_sha256, 'story renderer drift');
assert.equal(hash(fs.readFileSync(lintModule)), validation.renderer.lint_module_sha256, 'lint renderer drift');
assert.equal(hash(fs.readFileSync(timelineModule)), validation.renderer.timeline_module_sha256, 'timeline renderer drift');
const [{ composeStory, cuteStoryVisualProblems }, { lintVideo }, { estimateTimeline }] = await Promise.all([
  import(pathToFileURL(storyModule)), import(pathToFileURL(lintModule)), import(pathToFileURL(timelineModule)),
]);
const series = json('evidence/round9-series.json');
const archivedVideo = json('evidence/round9-composed-video.json');
const make = (chapters) => composeStory({
  slug: manifest.slug,
  info: series,
  chapters: Object.fromEntries(keys.map((key) => [key, JSON.parse(chapters[key].toString('utf8'))])),
  voice: archivedVideo.voice,
  drama: { music_enabled: Boolean(archivedVideo.music) },
  root,
  videoId: archivedVideo.youtube.video_id ?? null,
});
assert.deepEqual(make(source), archivedVideo);
const preview = json('composed-preview/story-preview.json');
eqSha('composed-preview/story-preview.json', validation.candidate.preview_video_sha256);
assert.deepEqual(make(candidate), preview);
const context = {
  lexicon: json('evidence/round9-lexicon.json'),
  brief: bytes('evidence/round9-brief.md').toString('utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(preview, context);
assert.deepEqual(lint.errors, validation.candidate.lint_errors);
assert.equal(lint.warnings.length, validation.candidate.warning_count);
assert.deepEqual(cuteStoryVisualProblems(preview), validation.candidate.cute_errors);
assert.equal(estimateTimeline(preview).total_frames / 30, validation.candidate.estimated_seconds);
assert.equal(validation.status, 'MECHANICAL_ONLY_NO_NARRATIVE_JUDGE');
assert.equal(manifest.authorizes_pass_or_media, false);
console.log(JSON.stringify({
  status: 'UNREVIEWED_OFFLINE_CANDIDATE', round9_passed: narrative.passed,
  json_files: allFiles.filter((name) => name.endsWith('.json')).length,
  files: allFiles.length, chapters: keys.length, exact_reverse: true,
  lint_errors: lint.errors.length, lint_warnings: lint.warnings.length,
  estimated_seconds: validation.candidate.estimated_seconds,
  media_or_provider_calls: 0,
}, null, 2));
