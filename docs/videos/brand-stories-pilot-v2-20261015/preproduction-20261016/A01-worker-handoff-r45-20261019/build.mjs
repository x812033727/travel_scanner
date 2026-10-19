#!/usr/bin/env node
// Offline, create-only derivation from frozen A01 r45. This does not write a worker state.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const frozen = path.join(path.dirname(here), 'A01-editorial-candidate-20261019-r45');
const expectedFrozenManifest = '4bba4d5b429b6de634c3982aa01027b1d0befd84664aef640d533af0302d05ac';
const action = process.argv[2] ?? '--preview';
assert.ok(['--preview', '--write', '--check'].includes(action), 'use --preview, --write or --check');
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const frozenFile = (name) => fs.readFileSync(path.join(frozen, name));
const frozenJson = (name) => JSON.parse(frozenFile(name));

let repo = here;
while (!fs.existsSync(path.join(repo, 'tools', 'video', 'automation', 'story.mjs'))) {
  const parent = path.dirname(repo);
  assert.notEqual(parent, repo, 'repository root not found');
  repo = parent;
}
const imports = async (name) => import(pathToFileURL(path.join(repo, name)));
const [{ CHAPTER_KEYS, composeStory, readChapterAnswer }, { validateVideo }, { storyProblems }, { lintVideo }, { estimateTimeline }, { cuteStoryVisualProblems }] = await Promise.all([
  imports('tools/video/automation/story.mjs'),
  imports('tools/video/core/schema.mjs'),
  imports('tools/video/core/story.mjs'),
  imports('tools/video/core/lint.mjs'),
  imports('tools/video/core/timeline.mjs'),
  imports('tools/video/automation/story.mjs'),
]);
assert.deepEqual(CHAPTER_KEYS, ['hook', 'origin', 'idea', 'engine', 'turn', 'now']);
assert.equal(sha(frozenFile('manifest.json')), expectedFrozenManifest, 'frozen r45 manifest drift');
const frozenManifest = frozenJson('manifest.json');
for (const [name, expected] of Object.entries(frozenManifest.outputs_sha256 ?? {})) {
  assert.equal(sha(frozenFile(name)), expected, `frozen r45 output drift: ${name}`);
}

const editorial = frozenJson('candidate/video.json');
const editorialSeries = frozenJson('candidate/series.json');
const lexicon = frozenJson('candidate/lexicon.json');
const alignment = frozenJson('source-alignment.json');
const claimLines = frozenFile('candidate/claims.md').toString('utf8').split(/\r?\n/).filter((line) => /^q\d{3}｜/.test(line));
const claimRows = claimLines.map((line) => {
  const fields = line.split('｜');
  assert.equal(fields.length, 6, `malformed claim row: ${line}`);
  const [id, claim, url, checked_on, scene, status] = fields;
  assert.equal(status, 'PENDING', `${id} must remain PENDING`);
  return { id, claim, url, checked_on, scene, status };
});
assert.equal(claimRows.length, 55);
assert.equal(new Set(claimRows.map((row) => row.id)).size, claimRows.length);
assert.equal(alignment.claim_source_rows.length, claimRows.length);
const byClaim = new Map(claimRows.map((row) => [row.id, row]));
const sourceByClaim = new Map(alignment.claim_source_rows.map((row) => [row.id, row]));
const sourceUrls = editorial.sources.map((source) => source.url);
assert.deepEqual(editorialSeries.plan.sources.map((source) => source.url), sourceUrls);
assert.equal(editorialSeries.plan.must_verify.length, sourceUrls.length);

const scenesByKey = new Map(CHAPTER_KEYS.map((key) => [key, []]));
const sceneKey = new Map();
const lineKey = new Map();
const titleByKey = new Map();
let chapterIndex = -1;
for (const scene of editorial.scenes) {
  if (scene.chapter !== undefined) {
    chapterIndex += 1;
    assert.ok(chapterIndex < CHAPTER_KEYS.length, 'too many chapters');
    titleByKey.set(CHAPTER_KEYS[chapterIndex], scene.chapter);
  }
  assert.ok(chapterIndex >= 0, 'scene before first chapter');
  const key = CHAPTER_KEYS[chapterIndex];
  assert.ok(scene.id.startsWith(`${key}-`), `${scene.id} outside ${key}`);
  assert.ok(!sceneKey.has(scene.id), `duplicate scene ${scene.id}`);
  sceneKey.set(scene.id, key);
  scenesByKey.get(key).push(scene);
  for (const line of scene.lines) {
    assert.ok(!lineKey.has(line.id), `duplicate line ${line.id}`);
    lineKey.set(line.id, key);
  }
}
assert.equal(chapterIndex + 1, CHAPTER_KEYS.length);
assert.deepEqual(editorialSeries.plan.chapters.map((entry) => entry.key), CHAPTER_KEYS);
assert.equal(editorial.scenes.length, 51);
assert.equal(lineKey.size, 53);

const indexedClaims = [];
const chapters = {};
for (const key of CHAPTER_KEYS) {
  const sourceScenes = scenesByKey.get(key);
  const scenes = sourceScenes.map(({ id, template, data, lines }) => ({ id, template, data, lines }));
  const rows = [];
  for (const scene of sourceScenes) {
    for (const id of scene.claims ?? []) {
      const original = byClaim.get(id);
      const aligned = sourceByClaim.get(id);
      assert.ok(original && aligned, `missing claim alignment ${id}`);
      assert.equal(original.scene, scene.id, `${id} scene drift`);
      assert.equal(aligned.public_source_index, aligned.plan_source_index, `${id} source index drift`);
      assert.equal(aligned.plan_source_index, aligned.research_source_index, `${id} research index drift`);
      assert.equal(original.url, sourceUrls[aligned.plan_source_index], `${id} URL drift`);
      const matchingFacts = editorialSeries.plan.must_verify.flatMap((fact, index) => fact.sources.includes(aligned.plan_source_index) ? [index] : []);
      assert.equal(matchingFacts.length, 1, `${id} needs one actual must_verify fact`);
      const row = { id, claim: original.claim, scene: scene.id, source: aligned.plan_source_index, fact: matchingFacts[0], verdict: 'PENDING' };
      rows.push(row);
      indexedClaims.push({ ...original, chapter: key, source: row.source, fact: row.fact });
    }
  }
  const loops = editorial.loops.filter((loop) => lineKey.get(loop.payoff) === key);
  const ids = scenes.flatMap((scene) => scene.lines.map((line) => line.id));
  const answer = { title: titleByKey.get(key), scenes, claims: rows, loops };
  const normalized = readChapterAnswer(answer, { key, ids, cast: editorial.characters, sources: sourceUrls.length, facts: editorialSeries.plan.must_verify.length });
  assert.ok(normalized.chapter && !normalized.problem, `${key} reader rejected: ${normalized.problem}`);
  assert.deepEqual(normalized.chapter.scenes, scenes, `${key} worker-normalized scenes changed`);
  assert.deepEqual(normalized.chapter.claims, rows.map(({ claim, scene, source, fact }) => ({ claim, scene, source, fact })), `${key} source/fact normalization changed`);
  assert.deepEqual(normalized.chapter.loops ?? [], loops, `${key} worker-normalized loops changed`);
  chapters[key] = { ...normalized.chapter, claims: rows };
}
assert.equal(indexedClaims.length, claimRows.length);
assert.deepEqual(new Set(indexedClaims.map((row) => row.id)), new Set(claimRows.map((row) => row.id)));

// The approved r45 thumbnail uses a now-chapter shot. This explicit manual choice is accepted by
// composeStory but is outside readChapterAnswer's usual hook-shot selection; see README HOLD.
const approvedThumbnailShot = editorial.thumbnail?.data?.shot;
assert.equal(approvedThumbnailShot, 'now-stow-fail');
assert.equal(sceneKey.get(approvedThumbnailShot), 'now');
chapters.hook.thumbnail_shot = approvedThumbnailShot;

const workerSeries = structuredClone(editorialSeries);
assert.equal(workerSeries.plan.thumbnail.headline, '會滾卻放不下？');
workerSeries.plan.thumbnail.headline = '會滾\n卻放不下？';
const composed = composeStory({ slug: editorial.slug, info: workerSeries, chapters, voice: editorial.voice, root: repo, videoId: editorial.youtube.video_id });
assert.equal(composed.youtube.title, editorial.youtube.title);
assert.equal(composed.thumbnail.data.shot, approvedThumbnailShot);
assert.equal(composed.thumbnail.data.headline.replaceAll('\n', ''), editorial.thumbnail.data.headline);
assert.deepEqual(composed.sources.map((source) => source.url), sourceUrls);
assert.deepEqual(composed.scenes.map((scene) => ({ id: scene.id, chapter: scene.chapter, template: scene.template, data: scene.data, lines: scene.lines, claims: scene.claims ?? [] })),
  editorial.scenes.map((scene) => ({ id: scene.id, chapter: scene.chapter, template: scene.template, data: scene.data, lines: scene.lines, claims: scene.claims ?? [] })), 'scene, narration, prompt or claim-id drift');
const loopOrder = (loops) => new Map(loops.map((loop) => [loop.setup, loop]));
assert.deepEqual([...loopOrder(composed.loops)].sort(([a], [b]) => a.localeCompare(b)), [...loopOrder(editorial.loops)].sort(([a], [b]) => a.localeCompare(b)), 'loop content drift');
assert.deepEqual(validateVideo(composed), [], 'worker-composed video schema errors');
const timeline = estimateTimeline(composed);
const story = storyProblems(composed, workerSeries, timeline);
assert.deepEqual(story.errors, [], 'worker-composed story errors');
const lint = lintVideo(composed, { lexicon, brief: frozenFile('brief.md').toString('utf8'), translations: {}, others: [], series: workerSeries });
assert.deepEqual(lint.errors, [], 'worker-composed lint errors');
const cute = cuteStoryVisualProblems(composed);
assert.deepEqual(cute, [], 'worker-composed cute visual errors');
assert.ok(!lint.warnings.some((warning) => String(warning.message).includes('line break falls inside the word')), 'thumbnail word wrap still fails');

const equal = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const differences = [];
function diff(a, b, location = '') {
  if (equal(a, b)) return;
  if (Array.isArray(a) && Array.isArray(b) && location !== 'loops' && location !== 'youtube.tags') {
    if (a.length !== b.length) differences.push({ path: `${location}.length`, editorial: a.length, worker: b.length });
    for (let index = 0; index < Math.max(a.length, b.length); index++) diff(a[index], b[index], `${location}[${index}]`);
    return;
  }
  if (Array.isArray(a) || Array.isArray(b) || a === null || b === null || typeof a !== 'object' || typeof b !== 'object' || !a || !b) {
    differences.push({ path: location, editorial: a ?? null, worker: b ?? null });
    return;
  }
  for (const key of new Set([...Object.keys(a), ...Object.keys(b)])) diff(a[key], b[key], location ? `${location}.${key}` : key);
}
diff(editorial, composed);
const contentDifferences = differences.filter((entry) => entry.path.startsWith('scenes[') || entry.path === 'loops');
assert.ok(contentDifferences.every((entry) => entry.path === 'loops' || entry.path === 'scenes[50].claims'), 'unexpected scene content drift');
const metadataDifferences = differences.filter((entry) => !contentDifferences.includes(entry));
const delta = {
  status: 'HOLD_OFFLINE_WORKER_RECOMPOSITION',
  frozen_r45_manifest_sha256: expectedFrozenManifest,
  title_exact: composed.youtube.title === editorial.youtube.title,
  thumbnail_shot_exact: composed.thumbnail.data.shot === approvedThumbnailShot,
  thumbnail_headline_same_words_layout_only: composed.thumbnail.data.headline.replaceAll('\n', '') === editorial.thumbnail.data.headline,
  source_urls_exact: equal(composed.sources.map((source) => source.url), sourceUrls),
  scenes_narration_prompts_claim_ids_exact: true,
  loops_same_pairs_order_may_differ: true,
  metadata_differences: metadataDifferences,
  structural_representation_differences: contentDifferences,
  validation: { schema_errors: 0, story_errors: 0, lint_errors: 0, lint_warnings: lint.warnings.length, cute_visual_errors: 0, thumbnail_word_split_warnings: 0 },
};

const readme = `# A01 r45 offline six-chapter worker handoff\n\n` +
  `Status: **HOLD — offline derivation only**. Frozen r45 manifest SHA-256: \`${expectedFrozenManifest}\`. ` +
  `This directory is a create-only decomposition and real current-worker recomposition of the frozen editorial candidate. It is not a host import, official six-chapter worker run, formal verifier/listener result, script-review receipt, auto.json, TTS, or paid media authorization.\n\n` +
  `The six real worker chapter paths are \`story/chapters/{hook,origin,idea,engine,turn,now}.json\`. ` +
  `All 55 claim rows retain the editorial \`PENDING\` marker, exact q-IDs, scene and source indices, and a unique matching must_verify fact index. No row has a formal verifier verdict. ` +
  `Cross-chapter loops reside in the chapter that speaks their payoff. The 53 narrator lines, 51 scene IDs, all visual prompts, claim IDs per scene, six source URLs, voice, lexicon, and title match r45.\n\n` +
  `\`build.mjs --check\` re-runs \`readChapterAnswer\`, \`composeStory\`, \`validateVideo\`, story lint and source-index assertions against frozen r45. ` +
  `\`worker-composed-video.json\` is the actual composer output. \`metadata-delta.json\` lists every JSON difference from editorial r45, including description, tags, source display titles/dates, the intentional headline line break, and any loop-order or empty-field representation drift. No metadata was overwritten after composition.\n\n` +
  `The title and the approved thumbnail shot \`now-stow-fail\` are preserved. The headline words are unchanged but the sibling plan uses \`會滾\\n卻放不下？\` to avoid a word-breaking wrap warning. ` +
  `The thumbnail shot is deliberately stored as \`hook.thumbnail_shot\` even though it belongs to the now chapter: \`composeStory\` accepts a shot anywhere in the merged video, while a normal \`readChapterAnswer\` hook response would not select it. A host wrapper would need to preserve this manual choice.\n\n` +
  `Before any import or paid stage, the owner/worker must resolve the metadata deltas and host wrapper, obtain real six-chapter verifier and listener results, current narrative review and formal pilot script-review receipt, and verify source access and actual TTS duration. The offline PENDING rows and local lint are not those receipts. No \`auto.json\`, \`verify-1.md\`, or formal review JSON is provided.\n`;

const outputs = new Map();
for (const key of CHAPTER_KEYS) outputs.set(`story/chapters/${key}.json`, json(chapters[key]));
outputs.set('series.json', json(workerSeries));
outputs.set('lexicon.json', frozenFile('candidate/lexicon.json'));
outputs.set('brief.md', frozenFile('brief.md'));
outputs.set('claim-map.json', json({ status: 'PENDING', claims: indexedClaims }));
outputs.set('worker-composed-video.json', json(composed));
outputs.set('metadata-delta.json', json(delta));
outputs.set('README.md', Buffer.from(readme));
const manifest = {
  status: 'HOLD_OFFLINE_WORKER_HANDOFF_ONLY',
  frozen_r45_manifest_sha256: expectedFrozenManifest,
  frozen_inputs_sha256: Object.fromEntries(['candidate/video.json', 'candidate/series.json', 'candidate/lexicon.json', 'candidate/claims.md', 'source-alignment.json', 'brief.md'].map((name) => [name, sha(frozenFile(name))])),
  build_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))),
  worker_dependency_sha256: Object.fromEntries(['tools/video/automation/story.mjs', 'tools/video/core/schema.mjs', 'tools/video/core/story.mjs', 'tools/video/core/lint.mjs', 'tools/video/core/timeline.mjs'].map((name) => [name, sha(fs.readFileSync(path.join(repo, name)))])),
  chapters: CHAPTER_KEYS,
  scenes: composed.scenes.length,
  lines: composed.scenes.flatMap((scene) => scene.lines).length,
  claims_pending: indexedClaims.length,
  source_urls: sourceUrls,
  host_import_or_paid_media_authorized: false,
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
};
outputs.set('manifest.json', json(manifest));
for (const [name, bytes] of outputs) {
  const target = path.join(here, name);
  if (action === '--preview') continue;
  if (action === '--write') {
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, bytes, { flag: 'wx' });
  } else {
    assert.ok(fs.readFileSync(target).equals(bytes), `stale output: ${name}`);
  }
}
console.log(JSON.stringify({ action, status: manifest.status, chapters: CHAPTER_KEYS.length, scenes: manifest.scenes,
  lines: manifest.lines, claims_pending: manifest.claims_pending, metadata_differences: metadataDifferences.length,
  structural_representation_differences: contentDifferences.length, lint_errors: lint.errors.length,
  lint_warnings: lint.warnings.length, metadata_paths: metadataDifferences.map((entry) => entry.path),
  structural_paths: contentDifferences.map((entry) => entry.path), manifest_sha256: sha(json(manifest)) }));
