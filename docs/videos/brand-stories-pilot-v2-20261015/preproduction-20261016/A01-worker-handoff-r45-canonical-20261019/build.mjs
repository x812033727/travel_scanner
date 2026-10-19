#!/usr/bin/env node
// Offline, create-only derivation from frozen A01 r45. This does not write a worker state.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { compileFunction } from 'node:vm';

const here = path.dirname(fileURLToPath(import.meta.url));
const frozen = path.join(path.dirname(here), 'A01-editorial-candidate-20261019-r45');
const expectedFrozenManifest = '896615541683e620eb6e79468d8d304f146ad932700a7f044d5a1eb9784888f6';
const previous = path.join(path.dirname(here), 'A01-worker-handoff-r45-20261019');
const expectedPreviousManifest = '7ba60fd949319420444a3236eec1180f02543a4f8d406e89b089f34b722f5fdf';
const expectedPreviousReview = 'a4b1144e48144b78b016c7353dd56f7f9b9298de24ee4386fba2022598d64c27';
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
const [{ CHAPTER_KEYS, STORY_CHAPTERS, composeStory, readChapterAnswer }, { validateVideo }, { storyProblems }, { lintVideo }, { estimateTimeline }, { cuteStoryVisualProblems }] = await Promise.all([
  imports('tools/video/automation/story.mjs'),
  imports('tools/video/core/schema.mjs'),
  imports('tools/video/core/story.mjs'),
  imports('tools/video/core/lint.mjs'),
  imports('tools/video/core/timeline.mjs'),
  imports('tools/video/automation/story.mjs'),
]);
assert.deepEqual(CHAPTER_KEYS, ['hook', 'origin', 'idea', 'engine', 'turn', 'now']);
assert.equal(sha(fs.readFileSync(path.join(previous, 'manifest.json'))), expectedPreviousManifest, 'original handoff manifest drift');
assert.equal(sha(fs.readFileSync(path.join(previous, 'independent-handoff-review.md'))), expectedPreviousReview, 'original independent review drift');
// Exercise the actual current non-exported pure helper, not a rewritten numbering algorithm.
// Only its source and its pure isText dependency are compiled; no worker entrypoint is run.
const workerSource = fs.readFileSync(path.join(repo, 'tools/video/automation/story.mjs'), 'utf8');
const numberClaimsSource = workerSource.match(/function numberClaims\(key, rows, previous = \[\]\) \{[\s\S]*?\r?\n\}/)?.[0];
const isTextSource = workerSource.match(/^const isText = .*;$/m)?.[0];
assert.ok(numberClaimsSource && isTextSource, 'current pure numberClaims helper cannot be extracted');
const invokeNumberClaims = compileFunction(`${isTextSource}\n${numberClaimsSource}\nreturn numberClaims(key, rows, previous);`, ['CHAPTER_OF', 'key', 'rows', 'previous']);
const chapterDefinitions = new Map(STORY_CHAPTERS.map((chapter, index) => [chapter.key, { ...chapter, index }]));
const numberClaims = (key, rows, oldRows = []) => invokeNumberClaims(chapterDefinitions, key, rows, oldRows);
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
const semanticMapBytes = fs.readFileSync(path.join(here, 'semantic-fact-map.json'));
const semanticMap = JSON.parse(semanticMapBytes);
assert.equal(semanticMap.status, 'AUTHOR_MAPPING_PENDING_INDEPENDENT_REVIEW');
assert.deepEqual(Object.keys(semanticMap.claims).sort(), [...byClaim.keys()].sort(), 'semantic mapping must explicitly cover exactly all 55 q-IDs');
for (const [id, decision] of Object.entries(semanticMap.claims)) {
  assert.ok(decision.fact === null || (Number.isInteger(decision.fact) && editorialSeries.plan.must_verify[decision.fact]), `${id} has invalid fact decision`);
  assert.ok(typeof decision.reason === 'string' && decision.reason.trim(), `${id} needs a semantic rationale`);
}

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
const oldToCanonical = new Map();
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
      const decision = semanticMap.claims[id];
      // This assertion checks a referenced fact's source consistency only. The explicit authored
      // semantic map, not source equality, decides whether this claim actually tells that fact.
      if (decision.fact !== null) assert.ok(editorialSeries.plan.must_verify[decision.fact].sources.includes(aligned.plan_source_index), `${id} fact/source inconsistency`);
      const row = { id, claim: original.claim, scene: scene.id, source: aligned.plan_source_index, fact: decision.fact, verdict: 'PENDING' };
      rows.push(row);
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
  const canonicalRows = numberClaims(key, rows);
  assert.deepEqual(numberClaims(key, canonicalRows), canonicalRows, `${key} canonical IDs not preserved with no previous rows`);
  assert.deepEqual(numberClaims(key, canonicalRows, canonicalRows), canonicalRows, `${key} canonical IDs not preserved with previous rows`);
  for (const [index, row] of canonicalRows.entries()) {
    const original = byClaim.get(rows[index].id);
    const decision = semanticMap.claims[original.id];
    assert.ok(!oldToCanonical.has(original.id), `${original.id} assigned twice`);
    oldToCanonical.set(original.id, row.id);
    indexedClaims.push({ ...original, editorial_id: original.id, id: row.id, chapter: key, source: row.source,
      fact: row.fact, fact_reason: decision.reason,
      matched_plan_fact: row.fact === null ? null : editorialSeries.plan.must_verify[row.fact].claim });
  }
  chapters[key] = { ...normalized.chapter, claims: canonicalRows };
}
assert.equal(indexedClaims.length, claimRows.length);
assert.deepEqual(new Set(indexedClaims.map((row) => row.editorial_id)), new Set(claimRows.map((row) => row.id)));
assert.equal(new Set(indexedClaims.map((row) => row.id)).size, 55, 'canonical IDs must remain unique');
assert.equal(oldToCanonical.size, 55);
assert.equal(semanticMap.claims.q003.fact, null, 'review finding q003 must not name fact 2');
assert.equal(semanticMap.claims.q054.fact, null, 'review finding q054 must not name fact 5');

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
  editorial.scenes.map((scene) => ({ id: scene.id, chapter: scene.chapter, template: scene.template, data: scene.data, lines: scene.lines, claims: (scene.claims ?? []).map((id) => oldToCanonical.get(id)) })), 'scene, narration, prompt or mapped claim-id drift');
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
const claimIdDifferences = differences.filter((entry) => /^scenes\[\d+\]\.claims\[\d+\]$/.test(entry.path));
assert.equal(claimIdDifferences.length, 55, 'all 55 scene claim references must be canonically mapped');
for (const entry of claimIdDifferences) assert.equal(oldToCanonical.get(entry.editorial), entry.worker, `unexpected claim mapping ${entry.path}`);
const contentDifferences = differences.filter((entry) => (entry.path.startsWith('scenes[') || entry.path === 'loops') && !claimIdDifferences.includes(entry));
assert.ok(contentDifferences.every((entry) => entry.path === 'loops' || entry.path === 'scenes[50].claims'), 'unexpected scene content drift');
const metadataDifferences = differences.filter((entry) => !contentDifferences.includes(entry) && !claimIdDifferences.includes(entry));
const linkedCount = indexedClaims.filter((row) => row.fact !== null).length;
const nullCount = indexedClaims.length - linkedCount;
const chapterCounts = CHAPTER_KEYS.map((key) => ({
  key, prefix: chapterDefinitions.get(key).prefix,
  scenes: chapters[key].scenes.length, lines: chapters[key].scenes.flatMap((scene) => scene.lines).length,
  claims: chapters[key].claims.length, loops: (chapters[key].loops ?? []).length,
  fact_linked: chapters[key].claims.filter((row) => row.fact !== null).length,
  fact_null: chapters[key].claims.filter((row) => row.fact === null).length,
}));
const delta = {
  status: 'HOLD_OFFLINE_CANONICAL_WORKER_RECOMPOSITION',
  frozen_r45_manifest_sha256: expectedFrozenManifest,
  title_exact: composed.youtube.title === editorial.youtube.title,
  thumbnail_shot_exact: composed.thumbnail.data.shot === approvedThumbnailShot,
  thumbnail_headline_same_words_layout_only: composed.thumbnail.data.headline.replaceAll('\n', '') === editorial.thumbnail.data.headline,
  source_urls_exact: equal(composed.sources.map((source) => source.url), sourceUrls),
  scenes_narration_prompts_exact: true,
  scene_claim_membership_exact_after_id_mapping: true,
  claim_ids_canonicalized_by_actual_worker_helper: true,
  loops_same_pairs_order_may_differ: true,
  metadata_differences: metadataDifferences,
  structural_representation_differences: contentDifferences,
  claim_id_differences: claimIdDifferences,
  validation: { schema_errors: 0, story_errors: 0, lint_errors: 0, lint_warnings: lint.warnings.length, cute_visual_errors: 0, thumbnail_word_split_warnings: 0 },
};

const readme = `# A01 r45 canonical offline six-chapter handoff\n\n` +
  `Status: **HOLD — authored correction awaiting independent review**. Frozen editorial r45 manifest: \`${expectedFrozenManifest}\`. ` +
  `This successor retains the original handoff content (current portable manifest \`${expectedPreviousManifest}\`) and its independent CHANGES REQUESTED report. The report still reviews the original raw manifest; that manifest is preserved verbatim in ../portability-20261019/historical-manifests/A01-worker-handoff-r45-20261019.json. Only packaging hash references changed; the original handoff chapters and composed content are byte-identical. The original handoff is superseded as an adoption input and retained only as evidence; this successor still awaits independent review. This directory is local, create-only derivation, not a host import, official worker run, approval, or paid-media authorization.\n\n` +
  `## What changed\n\n` +
  `1. \`semantic-fact-map.json\` explicitly decides the fact index for every editorial q-ID and explains why. ${linkedCount} rows reference a plan fact with matching factual content; ${nullCount} use \`fact: null\` and retain their original source for passage verification. Sharing a source never assigns a fact. Claims with substantive details beyond a plan summary conservatively stay null. The semantic decisions need independent review; the build only verifies coverage and structural consistency. All 55 verdicts remain \`PENDING\`.\n` +
  `2. The actual current worker's \`numberClaims\` source and \`STORY_CHAPTERS\` produce chapter-prefixed IDs. \`claim-id-map.json\` and \`claim-map.json\` trace every q001–q055 row to its canonical ID. The build calls that same helper again with empty and populated previous rows and proves it preserves every canonical ID. No numbering algorithm was separately reimplemented. This does not promise IDs survive a future writer rewrite or dropped/added claim.\n\n` +
  `## Preserved content and actual recomposition\n\n` +
  `The six chapter files are \`story/chapters/{hook,origin,idea,engine,turn,now}.json\`. The 53 narration lines, 51 scene IDs, all image prompts, eight setup/payoff pairs, six public source URLs, voice, characters, lexicon, title, and selected thumbnail are unchanged from r45. Scene claims use the mapped canonical IDs with exactly the same membership. Cross-chapter loops live in their payoff chapter.\n\n` +
  `\`build.mjs --check\` runs current \`readChapterAnswer\`, the actual pure \`numberClaims\` helper, \`composeStory\`, schema, story, cute-visual and lint checks. It verifies all frozen and generated hashes. \`worker-composed-video.json\` is the unmodified composer output. \`metadata-delta.json\` lists the 55 ID substitutions, 12 metadata deltas and two representation deltas. The metadata deltas retain the original documented description/tags/source-title/date differences and the headline newline. They still need an explicit publication decision; older source dates are not fresh checks.\n\n` +
  `## Manual-wrapper conditions\n\n` +
  `- The approved thumbnail is \`now-stow-fail\`, intentionally stored in \`hook.thumbnail_shot\`. \`composeStory\` accepts it from the merged scene set; the hook writer parser rejects it because it is in the now chapter. A wrapper must preserve and reassert this manual selection after parsing.\n` +
  `- \`readChapterAnswer\` strips claim IDs/verdicts; this derivation explicitly restores canonical PENDING rows after parsing. In the real \`checkChapter\` / \`checkedRows\` path, canonical IDs are preserved only when the verifier returns each existing row's input ID unchanged and the row survives. Missing, unknown or duplicate IDs, added/dropped claims, or a writer-parser rewrite do not have that guarantee. The helper test checks preservation under the unchanged-ID contract; it does not run a verifier. New formal receipts must bind the actual resulting script and IDs, not reuse this offline mapping as an approval.\n` +
  `- No \`auto.json\`, \`verify-1.md\`, checked/listened state, approval or formal script-review JSON is created. Copying chapter files alone does not set the live worker's \`written\` count and can trigger a rewrite on retry. The wrapper must reconcile live admission/runtime state under the existing gates. The inherited plan's \`series.hands_off\` value is not permission to enable automation.\n` +
  `- The owner adopted the Rollaboard direction. The inherited old ALTERNATE_PROPOSAL caveat is historical text; the newer series note records the adoption. A later adoption wrapper should make effective state explicit while preserving old evidence.\n` +
  `- Before import or paid stages: independent review of this corrected mapping, approved wrapper and fresh host evidence, real six-chapter verifier/listener results, current narrative review and pilot script-review receipt, source access and real TTS duration remain required. All production/media gates stay HOLD; this package performs no host or network operation.\n`;

const factMappingMarkdown = `# A01 r45 authored semantic fact mapping\n\n` +
  `Status: **PENDING independent review**. ${linkedCount} plan-linked claims; ${nullCount} passage-only claims. All 55 remain PENDING. A fact link is a statement relationship, not a source relationship or a verifier verdict.\n\n` +
  `## Frozen plan facts\n\n| Index | must_verify statement | Source indices |\n| --- | --- | --- |\n` +
  editorialSeries.plan.must_verify.map((fact, index) => `| ${index} | ${fact.claim} | ${fact.sources.join(', ')} |`).join('\n') +
  `\n\n## Claim decisions\n\n| Editorial ID | Worker ID | Chapter | Source | Fact | Authored rationale |\n| --- | --- | --- | ---: | --- | --- |\n` +
  indexedClaims.map((row) => `| ${row.editorial_id} | ${row.id} | ${row.chapter} | ${row.source} | ${row.fact === null ? 'null' : row.fact} | ${row.fact_reason} |`).join('\n') + '\n';

const outputs = new Map();
for (const key of CHAPTER_KEYS) outputs.set(`story/chapters/${key}.json`, json(chapters[key]));
outputs.set('series.json', json(workerSeries));
outputs.set('lexicon.json', frozenFile('candidate/lexicon.json'));
outputs.set('brief.md', frozenFile('brief.md'));
outputs.set('claim-map.json', json({ status: 'PENDING', claims: indexedClaims }));
outputs.set('claim-id-map.json', json({ status: 'PENDING', editorial_to_worker: Object.fromEntries(oldToCanonical),
  worker_to_editorial: Object.fromEntries([...oldToCanonical].map(([oldId, canonicalId]) => [canonicalId, oldId])),
  number_claims_source_sha256: sha(numberClaimsSource), canonical_ids_preserved_by_current_helper: true, chapters: chapterCounts }));
outputs.set('fact-mapping.md', Buffer.from(factMappingMarkdown));
outputs.set('worker-composed-video.json', json(composed));
outputs.set('metadata-delta.json', json(delta));
outputs.set('README.md', Buffer.from(readme));
const manifest = {
  status: 'HOLD_OFFLINE_CANONICAL_HANDOFF_PENDING_REVIEW',
  frozen_r45_manifest_sha256: expectedFrozenManifest,
  original_handoff_manifest_sha256: expectedPreviousManifest,
  original_independent_review_sha256: expectedPreviousReview,
  frozen_inputs_sha256: Object.fromEntries(['candidate/video.json', 'candidate/series.json', 'candidate/lexicon.json', 'candidate/claims.md', 'source-alignment.json', 'brief.md'].map((name) => [name, sha(frozenFile(name))])),
  build_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))),
  authored_semantic_fact_map_sha256: sha(semanticMapBytes),
  number_claims_source_sha256: sha(numberClaimsSource),
  worker_dependency_sha256: Object.fromEntries(['tools/video/automation/story.mjs', 'tools/video/automation/story-prompts.mjs', 'tools/video/core/schema.mjs', 'tools/video/core/story.mjs', 'tools/video/core/lint.mjs', 'tools/video/core/timeline.mjs'].map((name) => [name, sha(fs.readFileSync(path.join(repo, name)))])),
  chapters: CHAPTER_KEYS,
  scenes: composed.scenes.length,
  lines: composed.scenes.flatMap((scene) => scene.lines).length,
  claims_pending: indexedClaims.length,
  claim_ids_canonicalized: indexedClaims.length,
  claims_plan_linked: linkedCount,
  claims_passage_only: nullCount,
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
  canonical_claim_ids: oldToCanonical.size, claims_plan_linked: linkedCount, claims_passage_only: nullCount,
  structural_representation_differences: contentDifferences.length, lint_errors: lint.errors.length,
  lint_warnings: lint.warnings.length, metadata_paths: metadataDifferences.map((entry) => entry.path),
  structural_paths: contentDifferences.map((entry) => entry.path), manifest_sha256: sha(json(manifest)) }));
