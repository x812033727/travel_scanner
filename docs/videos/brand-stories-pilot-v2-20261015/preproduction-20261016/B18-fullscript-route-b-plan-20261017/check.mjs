#!/usr/bin/env node
// Read-only validation of a staged design, not a story/scene adoption builder.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const flow = resolve(here, '../B18-attribution-flow-candidate-20261017');
const fullscript = resolve(here, '../B18-spoken-source-cadence-candidate-20261017');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const initials = ['H', 'O', 'I', 'E', 'T', 'N'];
const read = (file) => readFileSync(file);
const shaBytes = (bytes) => createHash('sha256').update(bytes).digest('hex');
const sha = (file) => shaBytes(read(file));
const canonical = (obj) => JSON.stringify(obj, null, 2) + '\n';
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'usage: node check.mjs --write|--check');

const pins = {
  flow_manifest: '8b77652b8263fd33b02a95a3ee1288e85f96d6a847b4b88c2efd488a84ca3754',
  row: 'c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681',
  row_review: '6e06d5ddd1d4d836a105450e15b49fc98203e7ea0a595c7bba1596630fb73dc8',
  reviewed_script: '7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1',
  reviewed_script_receipt: '603f0a5340b197cc6cbe527991e63bb1629c4f1245e780fdb3981109dea871d4',
};
assert.equal(sha(join(flow, 'sha256.json')), pins.flow_manifest, 'flow manifest drift');
assert.equal(sha(join(flow, 'B18.json')), pins.row, 'flow row drift');
assert.equal(sha(join(flow, 'review-candidate.json')), pins.row_review, 'row review drift');
assert.equal(sha(join(fullscript, 'B18.md')), pins.reviewed_script, 'reviewed script drift');
assert.equal(sha(join(fullscript, 'review-candidate.md')), pins.reviewed_script_receipt, 'review receipt drift');
const flowManifest = JSON.parse(read(join(flow, 'sha256.json')));
for (const [name, expected] of Object.entries(flowManifest.files))
  assert.equal(sha(join(flow, name)), expected, `flow source drift: ${name}`);
const row = JSON.parse(read(join(flow, 'B18.json')));
const rowReview = JSON.parse(read(join(flow, 'review-candidate.json')));
assert.equal(rowReview.story_sha256, 'd0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648');
assert.equal(rowReview.verdict, 'pass');
assert.deepEqual(rowReview.reviewer_only, [4]);
const chapters = Object.fromEntries(keys.map((key) => [key, JSON.parse(read(join(flow, 'remapped-chapters', `${key}.json`)))]));
const oldSceneIds = keys.flatMap((key) => chapters[key].scenes.map((scene) => scene.id));
const oldLines = keys.flatMap((key) => chapters[key].scenes.flatMap((scene) => scene.lines));
const oldClaims = keys.flatMap((key) => chapters[key].claims);
assert.deepEqual([oldSceneIds.length, oldLines.length, oldClaims.length], [85, 88, 65]);
assert.equal(new Set(oldSceneIds).size, 85, 'duplicate scene ID');
assert.equal(new Set(oldClaims.map((claim) => claim.id)).size, 65, 'duplicate claim ID');
assert(oldClaims.every((claim) => claim.verdict === 'UNCHECKED'), 'a claim received an unexpected verdict');

const script = read(join(fullscript, 'B18.md')).toString();
const paragraphs = [...script.matchAll(/^> (.+)$/gm)].map((match) => match[1]);
const paragraphIds = [...script.matchAll(/^\*\*製作註 ([HOIETN]\d\d)（不朗讀）\*\*/gm)].map((match) => match[1]);
assert.equal(paragraphs.length, 25);
assert.equal(paragraphIds.length, 25);
assert.equal(new Set(paragraphIds).size, 25);
const oldVisible = oldLines.reduce((sum, line) => sum + [...line.text].length, 0);
const newVisible = paragraphs.reduce((sum, text) => sum + [...text].length, 0);
assert.equal(oldVisible, 2264, 'parent spoken character count drift');
assert.equal(newVisible, 3007, 'reviewed spoken character count drift');

const plan = JSON.parse(read(join(here, 'route-b-plan.json')));
assert.equal(plan.schema_version, 1);
assert.equal(plan.status, 'STAGED_DESIGN_HOLD');
assert.deepEqual(plan.pins, pins);
assert.equal(row.must_verify.length, 10, 'parent row facts drift');
assert.equal(row.chapters[0].key, 'hook');
assert.equal(row.chapters[4].key, 'turn');
assert.equal(plan.row_delta.hook_point_before, row.chapters[0].point);
assert.equal(plan.row_delta.turn_point_before, row.chapters[4].point);
assert.equal(plan.row_delta.invention_source_supports_before, row.sources[2].supports);
assert.equal(plan.row_delta.court_source_supports_before, row.sources[3].supports);
assert.deepEqual(plan.row_delta.add_facts.map((fact) => fact.sources), [[3], [2]]);
assert.match(plan.row_delta.add_facts[0].claim, /1967|一九六七/);
assert.match(plan.row_delta.add_facts[1].claim, /盤色|裝飾/);
assert.match(plan.row_delta.invention_source_supports_after, /盤色|裝飾/);
assert.match(plan.row_delta.court_source_supports_after, /L476.?495/);
assert.match(plan.row_delta.hook_point_after, /後場/);
assert.match(plan.row_delta.turn_point_after, /1967|一九六七/);
assert.deepEqual(plan.row_delta.new_review_reviewer_only, [4, 10]);
const futureFacts = [...row.must_verify, ...plan.row_delta.add_facts];
assert.match(paragraphs[1], /後場/);
assert(!paragraphs[1].includes('權利後來到期'));
assert.match(paragraphs[16], /一九六七年/); // T01 is paragraph 17, zero-indexed.

// Every paragraph owns a consecutive span in the proposed chapter order; all 85
// original scene IDs remain accounted for. This permits declared scene reordering,
// but it does not pretend the scene objects or claim rows have been rewritten.
assert.deepEqual(Object.keys(plan.paragraph_scene_map), paragraphIds);
const sceneCoverage = [];
const proposedSceneOrder = [];
for (let i = 0; i < keys.length; i++) {
  const key = keys[i];
  const ids = paragraphIds.filter((id) => id.startsWith(initials[i]));
  const assigned = ids.flatMap((id) => plan.paragraph_scene_map[id]);
  const original = chapters[key].scenes.map((scene) => scene.id);
  assert.equal(assigned.length, original.length, `${key}: scene count drift`);
  assert.deepEqual([...assigned].sort(), [...original].sort(), `${key}: scene mapping is not a permutation`);
  for (const id of ids) assert(plan.paragraph_scene_map[id].length > 0, `no scenes mapped to ${id}`);
  sceneCoverage.push(...assigned.map((id, index) => ({ id, paragraph: ids.find((note) => plan.paragraph_scene_map[note].includes(id)),
    before_position: original.indexOf(id), proposed_position: index, action: 'rewrite_and_recheck' })));
  proposedSceneOrder.push(...assigned);
}
assert.equal(sceneCoverage.length, 85);
const proposedParagraphOfScene = new Map(sceneCoverage.map((entry) => [entry.id, entry.paragraph]));
const oldSceneById = new Map(keys.flatMap((key) => chapters[key].scenes.map((scene) => [scene.id, scene])));
const shots = proposedSceneOrder.filter((id) => oldSceneById.get(id).template === 'shot').length;
let cardRun = 0;
let maxCardRun = 0;
for (const id of proposedSceneOrder) {
  cardRun = oldSceneById.get(id).template === 'shot' ? 0 : cardRun + 1;
  maxCardRun = Math.max(maxCardRun, cardRun);
}
assert.equal(shots, 66, 'historical shot count drift');
assert(shots * 100 >= proposedSceneOrder.length * 70, 'proposed scene order falls below illustrated ratio');
assert(maxCardRun <= 3, 'proposed scene order has too many consecutive cards');

const knownClaimIds = new Set(oldClaims.map((claim) => claim.id));
const overrideIds = plan.claim_overrides.map((entry) => entry.id);
assert.equal(new Set(overrideIds).size, overrideIds.length, 'duplicate claim override');
for (const entry of plan.claim_overrides) {
  assert(knownClaimIds.has(entry.id), `unknown claim override: ${entry.id}`);
  assert(['rewrite', 'remap', 'reorder', 'expand_source'].includes(entry.action), `unknown claim action: ${entry.id}`);
  assert(typeof entry.reason === 'string' && entry.reason.length >= 10, `claim ${entry.id} needs a reason`);
  assert(paragraphIds.includes(entry.target_paragraph), `claim ${entry.id} missing paragraph destination`);
  const before = oldClaims.find((claim) => claim.id === entry.id);
  const targetScene = entry.target_scene ?? before.scene;
  assert.equal(proposedParagraphOfScene.get(targetScene), entry.target_paragraph,
    `claim ${entry.id} destination does not belong to ${entry.target_paragraph}`);
  if (targetScene !== before.scene) assert.equal(entry.action, 'remap', `claim ${entry.id} moves scene without remap action`);
  if (entry.next_source !== undefined) assert(row.sources[entry.next_source], `claim ${entry.id} bad source`);
  if (entry.next_fact !== undefined) assert(Number.isInteger(entry.next_fact) && entry.next_fact >= 0 && entry.next_fact <= 11, `claim ${entry.id} bad fact`);
  if (entry.next_fact !== undefined && entry.next_source !== undefined)
    assert(futureFacts[entry.next_fact].sources.includes(entry.next_source), `claim ${entry.id} future fact/source mismatch`);
}
for (const id of ['h4', 'h6', 'h7', 'i1', 'i5', 'i6', 'i7', 'e6', 'e8', 'e9', 't2', 't3', 't7', 't15', 't18', 'n2', 'n7'])
  assert(overrideIds.includes(id), `known mismatch lacks a disposition: ${id}`);
const overrides = new Map(plan.claim_overrides.map((entry) => [entry.id, entry]));
const claimCoverage = oldClaims.map((claim) => ({
  id: claim.id, before_scene: claim.scene, before_source: claim.source, before_fact: claim.fact,
  verdict: claim.verdict, disposition: overrides.get(claim.id)?.action ?? 'retain_with_formal_recheck',
  target_paragraph: overrides.get(claim.id)?.target_paragraph ?? proposedParagraphOfScene.get(claim.scene),
  target_scene: overrides.get(claim.id)?.target_scene ?? claim.scene,
  ...(overrides.get(claim.id)?.next_source !== undefined ? { proposed_source: overrides.get(claim.id).next_source } : {}),
  ...(overrides.get(claim.id)?.next_fact !== undefined ? { proposed_fact: overrides.get(claim.id).next_fact } : {}),
}));
assert.equal(claimCoverage.length, 65);
assert(claimCoverage.every((claim) => claim.verdict === 'UNCHECKED'));

const report = {
  schema_version: 1, status: 'PASS_STAGED_DESIGN_ONLY_HOLD',
  pins, parent_story_sha256: 'd0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648',
  reviewed_script_paragraphs: paragraphs.length,
  parent_scenes: oldSceneIds.length, parent_lines: oldLines.length,
  historical_shots: shots, proposed_order_max_card_run: maxCardRun,
  old_voiced_visible_characters: oldVisible, reviewed_voiced_visible_characters: newVisible,
  extra_voiced_visible_characters_to_align: newVisible - oldVisible,
  old_scene_claims: oldClaims.length, all_old_claims_unchecked: true,
  proposed_row_review_complete: false, proposed_chapter_rewrite_complete: false,
  actual_worker_six_chapter_review_complete: false, tts_measured: false,
  paid_calls: 0, import_approved: false, rendered_video: false,
  paragraph_scene_coverage: sceneCoverage, original_claim_dispositions: claimCoverage,
};
const reportPath = join(here, 'verification.json');
if (mode === '--write') writeFileSync(reportPath, canonical(report));
else assert.equal(read(reportPath).toString(), canonical(report), 'verification readback drift');
const manifest = {
  schema_version: 1, status: 'STAGED_DESIGN_HOLD', pins,
  files: {
    'README.md': sha(join(here, 'README.md')),
    'route-b-plan.json': sha(join(here, 'route-b-plan.json')),
    'check.mjs': sha(join(here, 'check.mjs')),
    'verification.json': shaBytes(canonical(report)),
  },
};
const manifestPath = join(here, 'sha256.json');
if (mode === '--write') writeFileSync(manifestPath, canonical(manifest));
else assert.equal(read(manifestPath).toString(), canonical(manifest), 'manifest readback drift');
console.log(JSON.stringify({ status: report.status, scenes: oldSceneIds.length, claims: oldClaims.length,
  voiced_char_delta: newVisible - oldVisible, mode }));
