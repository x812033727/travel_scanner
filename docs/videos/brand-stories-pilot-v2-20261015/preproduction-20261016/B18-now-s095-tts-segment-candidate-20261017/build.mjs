import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Offline editorial correction. This does not install a chapter or synthesize audio.
const here = path.dirname(fileURLToPath(import.meta.url));
const base = path.resolve(here, '../B18-visual-card-reuse-integration-candidate-20261017');
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const baseManifestSha = 'd950454ac96598ec59c1391731e4e0c0f9eae54c702123b4d9b3b3afb1675d1f';
const sourceUrl = 'https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html';
const oldFirst = '二〇二一年，日本機械學會把一台一九八五年製造、當時仍在元祿壽司堺東店使用的輸送機';
const newFirst = '二〇二一年，日本機械學會認定第一百一十二號機械遺產。';
const newPunctuationLine = '其中一台輸送機製於一九八五年，當時仍在元祿壽司堺東店使用。';
const oldSecond = '列為第一百一十二號機械遺產；一起被認定的，還有早期那種叫「魚鱗板」的轉彎板片。';
const newSecond = '元祿產業保存的早期「魚鱗板」輸送板片，也一起獲得認定。';
const sha = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (file) => fs.readFileSync(file, 'utf8');

assert.equal(sha(fs.readFileSync(path.join(base, 'sha256.json'))), baseManifestSha, 'base manifest drift');
const baseManifest = JSON.parse(read(path.join(base, 'sha256.json'))).files;
for (const [name, expected] of Object.entries(baseManifest)) {
  assert.equal(sha(fs.readFileSync(path.join(base, name))), expected, `base file drift: ${name}`);
}
const series = JSON.parse(read(path.join(base, 'series.json')));
const previous = Object.fromEntries(keys.map((key) => [key, JSON.parse(read(path.join(base, 'chapters', `${key}.json`)))]));
const chapters = structuredClone(previous);
const now = chapters.now;
const firstScene = now.scenes.find((scene) => scene.id === 'now-s095');
const secondScene = now.scenes.find((scene) => scene.id === 'now-s096');
assert.equal(firstScene?.template, 'title');
assert.equal(secondScene?.template, 'shot');
assert.deepEqual(firstScene.lines, [
  { id: 'bb7022f4', text: oldFirst },
  { id: '8b88e002', text: '，' },
]);
assert.deepEqual(secondScene.lines, [{ id: '1585ea8b', text: oldSecond }]);
assert.deepEqual(now.claims.filter((claim) => claim.id === 'n4').map((claim) => claim.scene), ['now-s096']);
firstScene.lines = [
  { id: 'bb7022f4', text: newFirst },
  { id: '8b88e002', text: newPunctuationLine },
];
secondScene.lines = [{ id: '1585ea8b', text: newSecond }];
now.claims.find((claim) => claim.id === 'n4').scene = 'now-s095';
const reverse = structuredClone(now);
reverse.scenes.find((scene) => scene.id === 'now-s095').lines = previous.now.scenes.find((scene) => scene.id === 'now-s095').lines;
reverse.scenes.find((scene) => scene.id === 'now-s096').lines = previous.now.scenes.find((scene) => scene.id === 'now-s096').lines;
reverse.claims.find((claim) => claim.id === 'n4').scene = 'now-s096';
assert.deepEqual(reverse, previous.now, 'changes escaped the two lines and n4 scene binding');
for (const key of keys.filter((key) => key !== 'now')) assert.deepEqual(chapters[key], previous[key]);

const { composeStory, cuteStoryVisualProblems } = await import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs')).href);
const { loadProject, lintProject } = await import(pathToFileURL(path.join(root, 'tools/video/core/state.mjs')).href);
const { estimateTimeline } = await import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs')).href);
const authored = path.resolve(base, '../B18-authored-chapters-candidate');
const slug = 'story-conveyor-belt-sushi-v2';
const voice = JSON.parse(read(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'video.json'))).voice;
const beforeDoc = composeStory({ slug, info: series, chapters: previous, voice, drama: { music_enabled: false }, root });
const doc = composeStory({ slug, info: series, chapters, voice, drama: { music_enabled: false }, root });
const expectedDoc = structuredClone(beforeDoc);
expectedDoc.scenes.find((scene) => scene.id === 'now-s095').lines = firstScene.lines;
expectedDoc.scenes.find((scene) => scene.id === 'now-s096').lines = [{ id: '1585ea8b', text: newSecond }];
expectedDoc.scenes.find((scene) => scene.id === 'now-s095').claims.push('n4');
expectedDoc.scenes.find((scene) => scene.id === 'now-s096').claims = ['n5'];
assert.deepEqual(doc, expectedDoc, 'composed output changed outside the two reviewed spoken lines');
const punctuationOnly = doc.scenes.flatMap((scene) => scene.lines.map((line) => ({ scene: scene.id, ...line })))
  .filter((line) => /^[\p{P}\p{S}\s]+$/u.test(line.text));
assert.deepEqual(punctuationOnly, [], 'standalone punctuation segment remains');
assert([newFirst, newPunctuationLine, newSecond].every((text) => text.endsWith('。')), 'each narration unit needs a complete sentence');
assert.deepEqual(doc.scenes.find((scene) => scene.id === 'now-s095').lines.map((line) => line.id), ['bb7022f4', '8b88e002']);
assert.deepEqual(doc.look, { preset: 'cute-mystery' });
assert.equal(doc.subtitles.burn_in, false);
assert.equal(doc.scenes.length, 90);
assert.equal(doc.scenes.filter((scene) => scene.template === 'shot').length, 71);
assert.deepEqual(cuteStoryVisualProblems(doc), []);
const claims = keys.flatMap((key) => chapters[key].claims);
assert.equal(claims.length, 65);
assert(claims.every((claim) => claim.verdict === 'UNCHECKED'));
assert.equal(claims.find((claim) => claim.id === 'n4').source, 1);
assert.equal(claims.find((claim) => claim.id === 'n4').fact, 8);

let externalCalls = 0;
globalThis.fetch = () => { externalCalls++; throw new Error('offline candidate must not fetch'); };
let lint;
let lintBefore;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'b18-tts-segment-'));
try {
  const shelf = path.join(tmp, 'docs', 'videos');
  const dir = path.join(shelf, slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'video.json'), canonical(beforeDoc));
  fs.writeFileSync(path.join(dir, 'series.json'), canonical(series));
  fs.copyFileSync(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'brief.md'), path.join(dir, 'brief.md'));
  fs.copyFileSync(path.join(authored, 'fixtures/lexicon.json'), path.join(shelf, 'lexicon.json'));
  lintBefore = lintProject(loadProject({ slug, root: tmp }));
  fs.writeFileSync(path.join(dir, 'video.json'), canonical(doc));
  lint = lintProject(loadProject({ slug, root: tmp }));
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
assert.deepEqual(lint.errors, []);
assert.equal(externalCalls, 0);
assert.equal(lintBefore.warnings.length, 22, 'baseline lint warning count drift');
const warningKind = (warning) => warning.message.split(':', 1)[0];
const baselineWarningKinds = new Set(lintBefore.warnings.map(warningKind));
const newWarningKinds = [...new Set(lint.warnings.map(warningKind))]
  .filter((kind) => !baselineWarningKinds.has(kind));
const lines = doc.scenes.flatMap((scene) => scene.lines);
assert.equal(lines.length, 93);
const estimatedBodySeconds = estimateTimeline(doc).total_frames / 30;
const delta = {
  schema_version: 1,
  status: 'OFFLINE_TTS_SEGMENT_DELTA_ONLY',
  base_manifest_sha256: baseManifestSha,
  source_url: sourceUrl,
  scene_changes: [
    { scene: 'now-s095', line_id: 'bb7022f4', before: oldFirst, after: newFirst },
    { scene: 'now-s095', line_id: '8b88e002', before: '，', after: newPunctuationLine },
    { scene: 'now-s096', line_id: '1585ea8b', before: oldSecond, after: newSecond },
  ],
  claim_binding_changes: [{ claim_id: 'n4', field: 'scene', before: 'now-s096', after: 'now-s095' }],
  prompt_changes: 0,
  card_changes: 0,
  other_narration_changes: 0,
};
const verification = {
  schema_version: 1,
  status: 'VERIFIED_OFFLINE_SEGMENT_STRUCTURE_ONLY',
  scenes: doc.scenes.length,
  lines: lines.length,
  illustrations: 71,
  cards: 19,
  claims_unchecked: claims.length,
  punctuation_only_lines: punctuationOnly.length,
  now_s095_complete_sentences: 2,
  now_s096_complete_sentence: true,
  rewritten_punctuation_line_id: '8b88e002',
  estimated_body_seconds: estimatedBodySeconds,
  measured_body_seconds: null,
  lint_errors: lint.errors,
  cute_errors: [],
  lint_warnings: lint.warnings.length,
  baseline_lint_warnings: lintBefore.warnings.length,
  new_lint_warning_kinds: newWarningKinds,
  external_calls: externalCalls,
  worker_pass: false,
  tts_generated: false,
  full_story_pass: false,
  full_source_pass: false,
};
const output = new Map([
  ['series.json', read(path.join(base, 'series.json'))],
  ['reuse-intent.json', read(path.join(base, 'reuse-intent.json'))],
  ['delta.json', canonical(delta)],
  ['verification.json', canonical(verification)],
]);
for (const key of keys) output.set(`chapters/${key}.json`, key === 'now' ? canonical(chapters[key]) : read(path.join(base, 'chapters', `${key}.json`)));
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
  if (mode === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, content);
  } else assert.equal(read(file), content, `generated output drift: ${name}`);
}
console.log(JSON.stringify({ status: verification.status, scenes: verification.scenes,
  lines: verification.lines, punctuation_only_lines: 0, lint_errors: 0, cute_errors: 0,
  lint_warnings: verification.lint_warnings, external_calls: 0 }, null, 2));
