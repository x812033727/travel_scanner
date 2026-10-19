#!/usr/bin/env node
// Offline, create-only derivation from frozen A01 r47. This does not write a worker state.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { compileFunction } from 'node:vm';

const here = path.dirname(fileURLToPath(import.meta.url));
const frozen = path.join(path.dirname(here), 'A01-editorial-candidate-20261019-r47');
const expectedFrozenManifest = '323dc77c5ec678ef38c35204eb7865d46c8ca612b5e82f0a6083ddf70c59a24e';
const previous = path.join(path.dirname(here), 'A01-worker-handoff-r46-canonical-20261019');
const expectedPreviousManifest = '0277e782be1b99b93cff70f51f01a771b4ec9f3b2b36b34c146fadd1a4a11378';
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
const [{ CHAPTER_KEYS, STORY_CHAPTERS, composeStory, readChapterAnswer }, { validateVideo }, { storyProblems }, { lintVideo }, { estimateTimeline }, { cuteStoryVisualProblems }, { hookCadenceProblems, TIGHT_CADENCE }] = await Promise.all([
  imports('tools/video/automation/story.mjs'),
  imports('tools/video/core/schema.mjs'),
  imports('tools/video/core/story.mjs'),
  imports('tools/video/core/lint.mjs'),
  imports('tools/video/core/timeline.mjs'),
  imports('tools/video/automation/story.mjs'),
  imports('tools/video/core/narrative.mjs'),
]);
assert.deepEqual(CHAPTER_KEYS, ['hook', 'origin', 'idea', 'engine', 'turn', 'now']);
assert.equal(sha(fs.readFileSync(path.join(previous, 'manifest.json'))), expectedPreviousManifest, 'original handoff manifest drift');
// Prior r46 handoff is a frozen input only. No prior independent review is assumed or fabricated.
const priorManifest = JSON.parse(fs.readFileSync(path.join(previous, 'manifest.json')));
for (const [name, hash] of Object.entries(priorManifest.outputs_sha256))
  assert.equal(sha(fs.readFileSync(path.join(previous, name))), hash, 'prior canonical output drift ' + name);
// Exercise the actual current non-exported pure helper, not a rewritten numbering algorithm.
// Only its source and its pure isText dependency are compiled; no worker entrypoint is run.
const workerSource = fs.readFileSync(path.join(repo, 'tools/video/automation/story.mjs'), 'utf8');
const numberClaimsSource = workerSource.match(/function numberClaims\(key, rows, previous = \[\]\) \{[\s\S]*?\r?\n\}/)?.[0];
const isTextSource = workerSource.match(/^const isText = .*;$/m)?.[0];
assert.ok(numberClaimsSource && isTextSource, 'current pure numberClaims helper cannot be extracted');
const invokeNumberClaims = compileFunction(`${isTextSource}\n${numberClaimsSource}\nreturn numberClaims(key, rows, previous);`, ['CHAPTER_OF', 'key', 'rows', 'previous']);
const chapterDefinitions = new Map(STORY_CHAPTERS.map((chapter, index) => [chapter.key, { ...chapter, index }]));
const numberClaims = (key, rows, oldRows = []) => invokeNumberClaims(chapterDefinitions, key, rows, oldRows);
assert.equal(sha(frozenFile('manifest.json')), expectedFrozenManifest, 'frozen r47 manifest drift');
const frozenManifest = frozenJson('manifest.json');
for (const [name, expected] of Object.entries(frozenManifest.outputs_sha256 ?? {})) {
  assert.equal(sha(frozenFile(name)), expected, `frozen r47 output drift: ${name}`);
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
assert.equal(claimRows.length, 54);
assert.equal(new Set(claimRows.map((row) => row.id)).size, claimRows.length);
assert.equal(alignment.claim_source_rows.length, claimRows.length);
const byClaim = new Map(claimRows.map((row) => [row.id, row]));
const sourceByClaim = new Map(alignment.claim_source_rows.map((row) => [row.id, row]));
const sourceUrls = editorial.sources.map((source) => source.url);
assert.deepEqual(editorialSeries.plan.sources.map((source) => source.url), sourceUrls);
assert.equal(editorialSeries.plan.must_verify.length, sourceUrls.length);
const semanticMapBytes = fs.readFileSync(path.join(here, 'semantic-fact-map.json'));
const semanticMap = JSON.parse(semanticMapBytes);
const previousSemantic = JSON.parse(fs.readFileSync(path.join(previous, 'semantic-fact-map.json')));
const expectedSemantic = structuredClone(previousSemantic);
delete expectedSemantic.claims.q055;
assert.deepEqual(semanticMap, expectedSemantic, 'retained semantic decisions changed');
const narrationDeltaBytes = frozenFile('narration-delta.json');
assert.equal(sha(narrationDeltaBytes), frozenManifest.authored_narration_delta_sha256);
const narrationChanges = JSON.parse(narrationDeltaBytes).changes;
assert.equal(narrationChanges.length, 6);
assert.equal(semanticMap.status, 'AUTHOR_MAPPING_PENDING_INDEPENDENT_REVIEW');
assert.deepEqual(Object.keys(semanticMap.claims).sort(), [...byClaim.keys()].sort(), 'semantic mapping must explicitly cover exactly all 54 q-IDs');
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
  assert.ok(scene.id.startsWith(`${key}-`) || (key === 'turn' && scene.id === 'now-zipper'), `${scene.id} outside ${key}`);
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
assert.equal(editorial.scenes.length, 50);
assert.equal(lineKey.size, 52);

const indexedClaims = [];
const oldToCanonical = new Map();
const chapters = {};
const sceneIdMap = new Map();
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
  for (const [index, scene] of scenes.entries()) {
    const normalizedScene = normalized.chapter.scenes[index];
    assert.deepEqual({ ...normalizedScene, id: scene.id }, scene, `${key} normalized scene content drift`);
    const expected = scene.id === 'now-zipper' ? 'turn-01' : scene.id;
    assert.equal(normalizedScene.id, expected, 'unexpected actual parser scene ID');
    sceneIdMap.set(scene.id, normalizedScene.id);
  }
  assert.deepEqual(normalized.chapter.claims, rows.map(({ claim, scene, source, fact }) => ({ claim, scene: sceneIdMap.get(scene), source, fact })), `${key} source/fact normalization changed`);
  assert.deepEqual(normalized.chapter.loops ?? [], loops, `${key} worker-normalized loops changed`);
  const canonicalRows = numberClaims(key, rows.map((row) => ({ ...row, scene: sceneIdMap.get(row.scene) })));
  assert.deepEqual(numberClaims(key, canonicalRows), canonicalRows, `${key} canonical IDs not preserved with no previous rows`);
  assert.deepEqual(numberClaims(key, canonicalRows, canonicalRows), canonicalRows, `${key} canonical IDs not preserved with previous rows`);
  for (const [index, row] of canonicalRows.entries()) {
    const original = byClaim.get(rows[index].id);
    const decision = semanticMap.claims[original.id];
    assert.ok(!oldToCanonical.has(original.id), `${original.id} assigned twice`);
    oldToCanonical.set(original.id, row.id);
    indexedClaims.push({ ...original, editorial_id: original.id, id: row.id, chapter: key, source: row.source,
      fact: row.fact, worker_scene: row.scene, fact_reason: decision.reason,
      matched_plan_fact: row.fact === null ? null : editorialSeries.plan.must_verify[row.fact].claim });
  }
  chapters[key] = { ...normalized.chapter, claims: canonicalRows };
}
assert.equal(indexedClaims.length, claimRows.length);
assert.deepEqual(new Set(indexedClaims.map((row) => row.editorial_id)), new Set(claimRows.map((row) => row.id)));
assert.equal(new Set(indexedClaims.map((row) => row.id)).size, 54, 'canonical IDs must remain unique');
assert.equal(oldToCanonical.size, 54);
assert.equal(semanticMap.claims.q003.fact, null, 'review finding q003 must not name fact 2');
assert.equal(semanticMap.claims.q054.fact, null, 'review finding q054 must not name fact 5');

// The selected r47 thumbnail uses a now-chapter shot. This explicit manual choice is accepted by
// composeStory but is outside readChapterAnswer's usual hook-shot selection; see README HOLD.
const approvedThumbnailShot = editorial.thumbnail?.data?.shot;
assert.equal(approvedThumbnailShot, 'now-stow-fail');
assert.equal(sceneKey.get(approvedThumbnailShot), 'now');
chapters.hook.thumbnail_shot = approvedThumbnailShot;

const priorChapters = Object.fromEntries(CHAPTER_KEYS.map((key) => [key, JSON.parse(fs.readFileSync(path.join(previous, 'story/chapters/' + key + '.json')))]));
const previousClaimMap = JSON.parse(fs.readFileSync(path.join(previous, 'claim-id-map.json'))).editorial_to_worker;
const priorChapterDelta = [];
const restoredChapters = structuredClone(chapters);
for (const key of CHAPTER_KEYS) for (const scene of restoredChapters[key].scenes) {
  const change = narrationChanges.find((row) => row.line === scene.lines[0]?.id);
  if (change) { assert.equal(scene.lines[0].text, change.after); scene.lines[0].text = change.before; }
  if (scene.id === 'turn-01') scene.id = 'now-zipper';
}
const zipper = restoredChapters.turn.scenes.pop();
assert.equal(zipper.id, 'now-zipper');
restoredChapters.now.scenes.unshift(zipper);
restoredChapters.now.scenes.splice(-1, 0, priorChapters.now.scenes.find((scene) => scene.id === 'now-answer'));
for (const key of CHAPTER_KEYS) restoredChapters[key].claims = [];
for (const key of CHAPTER_KEYS) for (const row of chapters[key].claims) {
  const editorialId = [...oldToCanonical].find(([, value]) => value === row.id)?.[0];
  const priorId = previousClaimMap[editorialId];
  const oldKey = editorialId === 'q047' ? 'now' : key;
  restoredChapters[oldKey].claims.push({ ...row, id: priorId, scene: row.scene === 'turn-01' ? 'now-zipper' : row.scene });
}
restoredChapters.now.claims.push(priorChapters.now.claims.find((row) => row.id === previousClaimMap.q055));
for (const key of CHAPTER_KEYS) {
  restoredChapters[key].claims.sort((a,b) => Number(a.id.slice(1))-Number(b.id.slice(1)));
  if (Object.hasOwn(priorChapters[key], 'loops')) restoredChapters[key].loops = priorChapters[key].loops;
  else delete restoredChapters[key].loops;
  assert.deepEqual(restoredChapters[key], priorChapters[key], key + ': undeclared canonical content change');
  priorChapterDelta.push({ key, previous_scene_ids: priorChapters[key].scenes.map((s)=>s.id), current_scene_ids: chapters[key].scenes.map((s)=>s.id),
    previous_claim_ids: priorChapters[key].claims.map((c)=>c.id), current_claim_ids: chapters[key].claims.map((c)=>c.id),
    changed_lines: narrationChanges.filter((row)=>lineKey.get(row.line)===key).map((row)=>row.line),
    previous_loops: priorChapters[key].loops ?? [], current_loops: chapters[key].loops ?? [] });
}

const workerSeries = structuredClone(editorialSeries);
assert.equal(workerSeries.plan.thumbnail.headline, '會滾卻放不下？');
workerSeries.plan.thumbnail.headline = '會滾\n卻放不下？';
const composed = composeStory({ slug: editorial.slug, info: workerSeries, chapters, voice: editorial.voice, root: repo, videoId: editorial.youtube.video_id });
assert.equal(composed.youtube.title, editorial.youtube.title);
assert.equal(composed.thumbnail.data.shot, approvedThumbnailShot);
assert.equal(composed.thumbnail.data.headline.replaceAll('\n', ''), editorial.thumbnail.data.headline);
assert.deepEqual(composed.sources.map((source) => source.url), sourceUrls);
assert.deepEqual(composed.scenes.map((scene) => ({ id: scene.id, chapter: scene.chapter, template: scene.template, data: scene.data, lines: scene.lines, claims: scene.claims ?? [] })),
  editorial.scenes.map((scene) => ({ id: sceneIdMap.get(scene.id), chapter: scene.chapter, template: scene.template, data: scene.data, lines: scene.lines, claims: (scene.claims ?? []).map((id) => oldToCanonical.get(id)) })), 'scene, narration, prompt or mapped claim-id drift');
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
assert.deepEqual(TIGHT_CADENCE, { gap: 45, loopsPer10: 8 });
assert.equal(composed.loops.length, 8);
const cadenceChecks = {};
for (const cpm of [250, 275, 300]) {
  const measured = estimateTimeline(composed, cpm);
  const cadence = hookCadenceProblems(composed, measured, TIGHT_CADENCE.gap);
  assert.deepEqual(cadence, [], `worker cadence at ${cpm}`);
  cadenceChecks[cpm] = { cadence_problems: cadence, body_seconds: Number((measured.scenes.find((row) => row.id === 'now-outro').start_frame / 30).toFixed(1)) };
}
const estimatedBandAt275 = cadenceChecks[275].body_seconds >= 420 && cadenceChecks[275].body_seconds <= 480;
// Actual 420–480 second body audio remains required. A low paper estimate is an explicit HOLD, not approval.
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
assert.equal(claimIdDifferences.length, 54, 'all 54 scene claim references must be canonically mapped');
for (const entry of claimIdDifferences) assert.equal(oldToCanonical.get(entry.editorial), entry.worker, `unexpected claim mapping ${entry.path}`);
const sceneIdDifferences = differences.filter((entry) => /^scenes\[\d+\]\.id$/.test(entry.path));
assert.deepEqual(sceneIdDifferences, [{ path: 'scenes[41].id', editorial: 'now-zipper', worker: 'turn-01' }]);
const contentDifferences = differences.filter((entry) => (entry.path.startsWith('scenes[') || entry.path === 'loops') && !claimIdDifferences.includes(entry));
assert.ok(contentDifferences.every((entry) => entry.path === 'loops' || entry.path === 'scenes[49].claims' || entry.path === 'scenes[41].id'), 'unexpected scene content drift');
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
  frozen_r47_manifest_sha256: expectedFrozenManifest,
  title_exact: composed.youtube.title === editorial.youtube.title,
  thumbnail_shot_exact: composed.thumbnail.data.shot === approvedThumbnailShot,
  thumbnail_headline_same_words_layout_only: composed.thumbnail.data.headline.replaceAll('\n', '') === editorial.thumbnail.data.headline,
  source_urls_exact: equal(composed.sources.map((source) => source.url), sourceUrls),
  scenes_narration_prompts_exact_after_scene_id_mapping: true,
  scene_claim_membership_exact_after_id_mapping: true,
  claim_ids_canonicalized_by_actual_worker_helper: true,
  loops_same_pairs_order_may_differ: true,
  metadata_differences: metadataDifferences,
  structural_representation_differences: contentDifferences,
  claim_id_differences: claimIdDifferences,
  prior_canonical_chapter_delta: priorChapterDelta,
  scene_id_map: Object.fromEntries(sceneIdMap),
  canonical_id_migration: Object.entries(previousClaimMap).map(([id, old_id]) => ({ editorial_id: id, previous_worker_id: old_id, current_worker_id: oldToCanonical.get(id) ?? null })),
  target_actual_body_seconds: [420,480], estimated_band_at_275_passed: estimatedBandAt275, actual_tts_duration_not_measured: true, duration_gate_passed: false,
  validation: { schema_errors: 0, story_errors: 0, lint_errors: 0, lint_warnings: lint.warnings.length, cute_visual_errors: 0, thumbnail_word_split_warnings: 0, cadence_checks: cadenceChecks },
};

const readme = fs.readFileSync(path.join(here, 'README.md'), 'utf8');

const factMappingMarkdown = `# A01 r47 authored semantic fact mapping\n\n` +
  `Status: **PENDING independent review**. ${linkedCount} plan-linked claims; ${nullCount} passage-only claims. All 54 remain PENDING. A fact link is a statement relationship, not a source relationship or a verifier verdict.\n\n` +
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
const manifest = {
  status: 'HOLD_OFFLINE_CANONICAL_HANDOFF_PENDING_REVIEW',
  frozen_r47_manifest_sha256: expectedFrozenManifest,
  prior_canonical_manifest_sha256: expectedPreviousManifest,
  frozen_inputs_sha256: Object.fromEntries(['candidate/video.json', 'candidate/series.json', 'candidate/lexicon.json', 'candidate/claims.md', 'source-alignment.json', 'brief.md'].map((name) => [name, sha(frozenFile(name))])),
  build_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))),
  readme_sha256: sha(Buffer.from(readme)),
  authored_semantic_fact_map_sha256: sha(semanticMapBytes),
  number_claims_source_sha256: sha(numberClaimsSource),
  worker_dependency_sha256: Object.fromEntries(['tools/video/automation/story.mjs', 'tools/video/automation/story-prompts.mjs', 'tools/video/core/schema.mjs', 'tools/video/core/story.mjs', 'tools/video/core/lint.mjs', 'tools/video/core/timeline.mjs', 'tools/video/core/narrative.mjs', 'tools/video/core/duration.mjs'].map((name) => [name, sha(fs.readFileSync(path.join(repo, name)))])),
  duration_gate_passed: false, target_actual_body_seconds: [420,480], estimated_band_at_275_passed: estimatedBandAt275,
  chapters: CHAPTER_KEYS,
  scenes: composed.scenes.length,
  lines: composed.scenes.flatMap((scene) => scene.lines).length,
  claims_pending: indexedClaims.length,
  claim_ids_canonicalized: indexedClaims.length,
  claims_plan_linked: linkedCount,
  claims_passage_only: nullCount,
  source_urls: sourceUrls,
  cadence_checks: cadenceChecks,
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
