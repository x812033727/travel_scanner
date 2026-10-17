#!/usr/bin/env node
// Isolated B18 Route B row10b only. Keep the reviewed T06 without a spoken source name.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const flow = path.resolve(here, '../B18-attribution-flow-candidate-20261017');
const planDir = path.resolve(here, '../B18-fullscript-route-b-plan-20261017');
const priorRowDir = path.resolve(here, '../B18-route-b-row10-candidate-20261017');
const scriptDir = path.resolve(here, '../B18-spoken-source-cadence-candidate-20261017');
const repo = path.resolve(here, '../../../../..');
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
const sha = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (dir, name) => fs.readFileSync(path.join(dir, name));

const pinned = {
  flow_manifest: '8b77652b8263fd33b02a95a3ee1288e85f96d6a847b4b88c2efd488a84ca3754',
  flow_row: 'c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681',
  flow_row_review: '6e06d5ddd1d4d836a105450e15b49fc98203e7ea0a595c7bba1596630fb73dc8',
  route_b_plan: '3b3183525d995950bc9366ecffd82595938817eca09a8a4d6ca95100d1e88985',
  route_b_independent_review: '679c20ceb91cee5b3280eef0df6f0e319705bac3d58398b14c6638d335710a98',
  route_b_review_addendum: 'fcc3ece0b21357027bc2228437d51988349b5732197c90df82f813791b829ee6',
  prior_row10: '73a00f868eb625161cd2a0e9d3692138071b596a3b0c67dfa78d0c6bec3d332f',
  prior_row10_independent_review: '2a14551efc036632da2cef5f46332be9c84560fb651f3dbafe089d460fbc0c96',
  reviewed_fullscript: '7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1',
  reviewed_fullscript_receipt: '603f0a5340b197cc6cbe527991e63bb1629c4f1245e780fdb3981109dea871d4',
};
assert.equal(sha(read(flow, 'sha256.json')), pinned.flow_manifest, 'flow manifest drift');
const flowManifest = JSON.parse(read(flow, 'sha256.json'));
for (const [name, hash] of Object.entries(flowManifest.files))
  assert.equal(sha(read(flow, name)), hash, `flow file drift: ${name}`);
assert.equal(sha(read(flow, 'review-candidate.json')), pinned.flow_row_review, 'flow row review drift');
assert.equal(sha(read(planDir, 'route-b-plan.json')), pinned.route_b_plan, 'Route B plan drift');
assert.equal(sha(read(planDir, 'INDEPENDENT-PLAN-REVIEW.md')), pinned.route_b_independent_review, 'Route B review drift');
assert.equal(sha(read(planDir, 'INDEPENDENT-PLAN-REVIEW-ADDENDUM.md')), pinned.route_b_review_addendum, 'Route B schema addendum drift');
assert.equal(sha(read(priorRowDir, 'B18.json')), pinned.prior_row10, 'prior row10 drift');
assert.equal(sha(read(priorRowDir, 'INDEPENDENT-ROW10-REVIEW.md')), pinned.prior_row10_independent_review, 'prior row10 review drift');
assert.equal(sha(read(scriptDir, 'B18.md')), pinned.reviewed_fullscript, 'reviewed fullscript drift');
assert.equal(sha(read(scriptDir, 'review-candidate.md')), pinned.reviewed_fullscript_receipt, 'fullscript review drift');

const parentBytes = read(flow, 'B18.json');
assert.equal(sha(parentBytes), pinned.flow_row, 'parent row drift');
const parent = JSON.parse(parentBytes);
const plan = JSON.parse(read(planDir, 'route-b-plan.json'));
assert.equal(parent.must_verify.length, 10, 'parent fact count drift');
assert.deepEqual(plan.row_delta.new_review_reviewer_only, [4, 10], 'historical 12-fact plan drift');
const byClaim = new Map(plan.claim_overrides.map((item) => [item.id, item]));
assert.deepEqual([byClaim.get('t3')?.next_fact, byClaim.get('t18')?.next_fact], [10, 11], 'historical claim route drift');
const row = structuredClone(parent);
const chapter = (key) => row.chapters.find((item) => item.key === key);
assert.equal(chapter('hook').point, plan.row_delta.hook_point_before, 'old hook drift');
assert.equal(chapter('turn').point, plan.row_delta.turn_point_before, 'old turn drift');
assert.equal(row.sources[2].supports, plan.row_delta.invention_source_supports_before, 'JIII support drift');
assert.equal(row.sources[3].supports, plan.row_delta.court_source_supports_before, 'court support drift');
chapter('hook').point = plan.row_delta.hook_point_after;
chapter('turn').point = plan.row_delta.turn_point_after;
row.sources[2].supports = plan.row_delta.invention_source_supports_after;
row.sources[3].supports = plan.row_delta.court_source_supports_after;
const factBefore = { 4: parent.must_verify[4].claim };
row.must_verify[4].claim = '法院判決理由記載：1967年獲授權使用餐台及「元禄寿司」標示的訴外元祿，在仙台開直營首店、東京錦糸町開連鎖首店；特定第579776號實用新案於1972年期滿，此後多家公司與本案原告無關地經營輸送帶壽司店。不能說1967年兩店由原告自己開設、所有權利同時期滿或新店只因期滿才出現。';
assert.equal(row.must_verify[9].claim, parent.must_verify[9].claim, 'attributed backroom fact 9 must stay byte-exact');
assert.deepEqual(row.must_verify.map((fact) => fact.sources), parent.must_verify.map((fact) => fact.sources), 'fact source indexes changed');
assert.deepEqual([row.must_verify[4].sources, row.must_verify[9].sources], [[3], [2]], 'fact source route drift');
assert.equal(row.must_verify[4].core, true, 'court core flag drift');
assert.equal(row.must_verify[9].attributed, true, 'JIII attribution flag drift');
assert(row.must_verify[4].claim.includes('1967年') && row.must_verify[4].claim.includes('1972年'));
assert(row.must_verify[9].claim.includes('後場') && !row.must_verify[9].claim.includes('盤色'), 'fact 9 cannot force attribution for T06');
assert(row.sources[2].supports.includes('盤色'), 'JIII source support must retain plate-color evidence');

// Prove the new row differs in only the five named text fields.
const restored = structuredClone(row);
restored.chapters.find((item) => item.key === 'hook').point = plan.row_delta.hook_point_before;
restored.chapters.find((item) => item.key === 'turn').point = plan.row_delta.turn_point_before;
restored.sources[2].supports = plan.row_delta.invention_source_supports_before;
restored.sources[3].supports = plan.row_delta.court_source_supports_before;
restored.must_verify[4].claim = factBefore[4];
assert.deepEqual(restored, parent, 'new row changed beyond five declared text fields');

const { STORY_KEYS, storyHash, storyProblems, reviewProblems } = await import(
  pathToFileURL(path.join(repo, 'tools/video/story-plans/plan.mjs')).href
);
const story = Object.fromEntries(STORY_KEYS.map((key) => [key, row[key]]));
const problems = storyProblems(story, 'B18');
assert.deepEqual(problems, [], `row schema problems: ${problems.join(' | ')}`);
const storySha = storyHash(story);
const oldReview = JSON.parse(read(flow, 'review-candidate.json'));
assert.deepEqual(oldReview.reviewer_only, [4], 'old court reviewer-only list drift');
const oldReviewProblems = reviewProblems(oldReview, story, 'B18');
assert(oldReviewProblems.length > 0, 'old row review unexpectedly validates new row');

const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const chapterFiles = Object.fromEntries(keys.map((key) => {
  const name = `remapped-chapters/${key}.json`;
  return [name, sha(read(flow, name))];
}));
const claims = keys.flatMap((key) => JSON.parse(read(flow, `remapped-chapters/${key}.json`)).claims);
assert.equal(claims.length, 65, 'old scene claim count drift');
assert.equal(new Set(claims.map((item) => item.id)).size, 65, 'old claim ID uniqueness drift');
assert(claims.every((item) => item.verdict === 'UNCHECKED'), 'an existing claim was marked reviewed');
assert(claims.every((item) => item.fact === null || (item.fact >= 0 && item.fact <= 9)), 'old claim fact index drift');
const oldT18 = claims.find((item) => item.id === 't18');
assert.deepEqual([oldT18?.scene, oldT18?.source, oldT18?.fact, oldT18?.verdict],
  ['turn-s092', 1, 7, 'UNCHECKED'], 'old t18 fallback route drift');
const oldClaimsSha = sha(canonical(claims));

const amendment = {
  schema_version: 1,
  status: 'OFFLINE_SUCCESSOR_TO_REVIEWED_DESIGN_HOLD',
  historical_route_b_plan_sha256: pinned.route_b_plan,
  reason: 'Current story-plans schema caps must_verify at 10. Join only the court chronology at fact 4; keep attributed fact 9 limited to backroom routing so reviewed T06 is not forced to speak JIII.',
  old_design_fact_indexes_not_created: [10, 11],
  future_review_reviewer_only: [4],
  claim_fact_route_overrides: [
    { id: 't3', source: 3, historical_plan_fact: 10, successor_fact: 4, reason: 'Court P8 1967 expansion joins court P10 1972 expiry as one limited legal timeline.' },
    {
      id: 't18', source: 2, historical_plan_fact: 11, successor_fact: null,
      target_paragraph: 'T06', target_scene: 'turn-s088',
      future_claim: '發明協會沿革記後來有店用盤色或裝飾區分價位；不得說所有店同時採用。',
      visual_source_card: '公益社團法人發明協會／戰後日本的創新100選「迴轉壽司」沿革',
      pre_verifier_chapter_write_required: { scene: 'turn-s088', source: 2, fact: null, verdict: 'UNCHECKED' },
      post_verifier_persisted_readback_required: { scene: 'turn-s088', source: 2, fact: null, source_card_present: true, source_card_not_spoken: true },
      reason: 'Rewrite and save the turn chapter row before verifier: story.mjs checkedRows falls back to old fact 7 if a verifier-only patch returns null. Then verify the saved null route and native nonspoken source card.',
    },
  ],
  existing_65_scene_claims_changed: false,
  review_required_before_row_adoption: true,
};
for (const change of amendment.claim_fact_route_overrides) {
  const old = byClaim.get(change.id);
  assert.deepEqual([old.next_source, old.next_fact], [change.source, change.historical_plan_fact], `${change.id} historical route drift`);
  if (change.successor_fact === null) {
    assert.deepEqual([change.id, change.source, change.target_paragraph, change.target_scene], ['t18', 2, 'T06', 'turn-s088']);
    assert(plan.paragraph_scene_map.T06.includes(change.target_scene), 'scene-only claim target left T06');
    assert(row.sources[change.source].supports.includes('盤色'), 'scene-only claim lacks source support');
    assert.deepEqual(change.pre_verifier_chapter_write_required,
      { scene: 'turn-s088', source: 2, fact: null, verdict: 'UNCHECKED' }, 't18 must be rewritten before verifier');
    assert.deepEqual(change.post_verifier_persisted_readback_required,
      { scene: 'turn-s088', source: 2, fact: null, source_card_present: true, source_card_not_spoken: true },
      't18 fact-null and source card must be read back after verifier');
  } else {
    assert(row.must_verify[change.successor_fact].sources.includes(change.source), `${change.id} new fact source mismatch`);
  }
}
const delta = {
  schema_version: 1, status: 'FIVE_TEXT_FIELDS_ONLY_HOLD',
  parent_row_sha256: pinned.flow_row,
  changed_paths: [
    'chapters[hook].point', 'chapters[turn].point',
    'must_verify[4].claim',
    'sources[2].supports', 'sources[3].supports',
  ],
  before: {
    hook: plan.row_delta.hook_point_before, turn: plan.row_delta.turn_point_before,
    fact4: factBefore[4],
    source2: plan.row_delta.invention_source_supports_before,
    source3: plan.row_delta.court_source_supports_before,
  },
  after: {
    hook: chapter('hook').point, turn: chapter('turn').point,
    fact4: row.must_verify[4].claim,
    source2: row.sources[2].supports, source3: row.sources[3].supports,
  },
};
const verification = {
  schema_version: 1, status: 'PASS_OFFLINE_ROW_SCHEMA_ONLY_HOLD',
  canonical_story_sha256: storySha,
  row_schema_problems: problems,
  existing_fact_count: row.must_verify.length,
  old_scene_count: keys.reduce((sum, key) => sum + JSON.parse(read(flow, `remapped-chapters/${key}.json`)).scenes.length, 0),
  old_scene_claim_count: claims.length,
  old_scene_claims_sha256: oldClaimsSha,
  old_scene_claims_all_unchecked: true,
  unchanged_parent_chapter_sha256: chapterFiles,
  old_review_problems: oldReviewProblems,
  new_row_independently_source_reviewed: false,
  successor_85_scenes_aligned: false,
  successor_65_scene_claims_reviewed: false,
  t18_pre_verifier_chapter_rewrite_done: false,
  t18_post_verifier_fact_null_readback_done: false,
  t06_nonspoken_source_card_produced_and_qaed: false,
  fullscript_worker_output_matched: false,
  tts_540_to_660_seconds_measured: false,
  media_or_host_calls: 0,
  adoption_approved: false,
};
assert.equal(verification.old_scene_count, 85, 'old scene count drift');
const outputs = new Map([
  ['B18.json', canonical(row)],
  ['routing-amendment.json', canonical(amendment)],
  ['delta.json', canonical(delta)],
  ['verification.json', canonical(verification)],
]);
for (const [name, content] of outputs) {
  const file = path.join(here, name);
  if (mode === '--write') fs.writeFileSync(file, content);
  else assert.equal(fs.readFileSync(file, 'utf8'), content, `output drift: ${name}`);
}
const manifest = {
  schema_version: 1, status: 'OFFLINE_ROW_SCHEMA_ONLY_HOLD', pins: pinned,
  canonical_story_sha256: storySha,
  unchanged_parent_chapter_sha256: chapterFiles,
  files: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  README_sha256: sha(read(here, 'README.md')),
  build_sha256: sha(read(here, 'build.mjs')),
};
if (mode === '--write') fs.writeFileSync(path.join(here, 'sha256.json'), canonical(manifest));
else assert.equal(fs.readFileSync(path.join(here, 'sha256.json'), 'utf8'), canonical(manifest), 'manifest drift');
console.log(JSON.stringify({ status: verification.status, mode, canonical_story_sha256: storySha,
  must_verify: row.must_verify.length, old_scenes: verification.old_scene_count, old_claims: claims.length }));
