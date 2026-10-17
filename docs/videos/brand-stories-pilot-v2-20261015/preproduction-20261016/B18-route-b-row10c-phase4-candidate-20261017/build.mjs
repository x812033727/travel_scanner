#!/usr/bin/env node
// Isolated B18 Row10c: identical Row10b plan, reconciled with Phase4's audible T06 source.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const flow = path.resolve(here, '../B18-attribution-flow-candidate-20261017');
const planDir = path.resolve(here, '../B18-fullscript-route-b-plan-20261017');
const priorRowDir = path.resolve(here, '../B18-route-b-row10-candidate-20261017');
const row10bDir = path.resolve(here, '../B18-route-b-row10b-candidate-20261017');
const phase4Dir = path.resolve(here, '../B18-route-b-phase4-candidate-20261017');
const phase4ReviewDir = path.resolve(here, '..');
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
  row10b_row: '6c2eb6172d0afc6d5c92a91736cf1ad606ea3302d904c749d42d1b74533b14bc',
  phase4_manifest: 'efdf3994152db18892d70c35f6ae10ba3f1d4a9076078922a8a988ee0bbd7422',
  phase4_fullscript_review: '52172dd22d2a0d349bea7ff7568cbaa2aecef5ab61d2929ad82048df967d745e',
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
assert.equal(sha(read(row10bDir, 'B18.json')), pinned.row10b_row, 'Row10b row drift');
assert.equal(sha(read(phase4Dir, 'sha256.json')), pinned.phase4_manifest, 'Phase4 manifest drift');
const phase4Manifest = JSON.parse(read(phase4Dir, 'sha256.json'));
for (const [name, hash] of Object.entries({ ...phase4Manifest.inputs, ...phase4Manifest.outputs }))
  assert.equal(sha(read(phase4Dir, name)), hash, `Phase4 file drift: ${name}`);
assert.equal(sha(read(phase4ReviewDir, 'B18-route-b-phase4-full-editorial-review-20261017.md')),
  pinned.phase4_fullscript_review, 'Phase4 fullscript review drift');
assert.equal(phase4Manifest.pins.row10b, pinned.row10b_row, 'Phase4 reviewed a different row');

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
assert.equal(canonical(row), read(row10bDir, 'B18.json').toString('utf8'), 'Row10c must not edit Row10b plan bytes');

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
const phase4Chapters = Object.fromEntries(keys.map((key) =>
  [key, JSON.parse(read(phase4Dir, `remapped-chapters/${key}.json`))]));
const phase4Scenes = keys.flatMap((key) => phase4Chapters[key].scenes);
const phase4Claims = keys.flatMap((key) => phase4Chapters[key].claims);
assert.equal(phase4Scenes.length, 95, 'Phase4 scene count drift');
assert.equal(phase4Scenes.filter((scene) => scene.template === 'shot').length, 94, 'Phase4 shot count drift');
assert.equal(phase4Scenes.at(-1)?.template, 'outro', 'Phase4 terminal outro drift');
assert.equal(phase4Claims.length, 65, 'Phase4 claim count drift');
assert(phase4Claims.every((claim) => claim.verdict === 'UNCHECKED'), 'Phase4 claim was marked checked');
const phase4T18 = phase4Claims.find((claim) => claim.id === 't18');
assert.deepEqual([phase4T18?.scene, phase4T18?.source, phase4T18?.fact, phase4T18?.verdict],
  ['turn-s088', 2, null, 'UNCHECKED'], 'Phase4 t18 route drift');
const phase4T06Scene = phase4Chapters.turn.scenes.find((scene) => scene.id === 'turn-s088');
const audibleT06 = phase4T06Scene?.lines.map((line) => line.text).join('') ?? '';
assert.equal(phase4T06Scene?.template, 'shot', 'Phase4 T06 is no longer an illustration');
assert(audibleT06.includes('發明協會的沿革') && audibleT06.includes('盤子的顏色或裝飾區分價位'),
  'Phase4 T06 audible attribution or pricing drift');
assert.equal(row.sources[2].url,
  'https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii',
  'JIII source URL drift');

const amendment = {
  schema_version: 1,
  status: 'OFFLINE_PHASE4_AUDIBLE_ATTRIBUTION_ROUTE_HOLD',
  historical_route_b_plan_sha256: pinned.route_b_plan,
  phase4_manifest_sha256: pinned.phase4_manifest,
  reason: 'Current story-plans schema caps must_verify at 10. Keep attributed fact 9 limited to backroom routing; Phase4 T06 audibly names JIII, and its extra pricing claim stays source 2/fact null.',
  old_design_fact_indexes_not_created: [10, 11],
  future_review_reviewer_only: [4],
  claim_fact_route_overrides: [
    { id: 't3', source: 3, historical_plan_fact: 10, successor_fact: 4, reason: 'Court P8 1967 expansion joins court P10 1972 expiry as one limited legal timeline.' },
    {
      id: 't18', source: 2, historical_plan_fact: 11, successor_fact: null,
      target_paragraph: 'T06', target_scene: 'turn-s088',
      future_claim: '發明協會沿革記後來有店用盤色或裝飾區分價位；不得說所有店同時採用。',
      pre_verifier_chapter_write_required: { scene: 'turn-s088', source: 2, fact: null, verdict: 'UNCHECKED' },
      post_verifier_persisted_readback_required: { scene: 'turn-s088', source: 2, fact: null, audible_attribution: '發明協會的沿革' },
      final_description_source_url_required: row.sources[2].url,
      reason: 'Rewrite and save the turn chapter row before verifier: story.mjs checkedRows falls back to old fact 7 if a verifier-only patch returns null. Read back the saved null route and audible attribution; check the full source URL in the final description separately.',
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
      { scene: 'turn-s088', source: 2, fact: null, audible_attribution: '發明協會的沿革' },
      't18 fact-null and audible attribution must be read back after verifier');
    assert(audibleT06.includes(change.post_verifier_persisted_readback_required.audible_attribution),
      'Phase4 T06 no longer speaks source attribution');
    assert.equal(change.final_description_source_url_required, row.sources[2].url,
      'final description must link the full JIII source URL');
  } else {
    assert(row.must_verify[change.successor_fact].sources.includes(change.source), `${change.id} new fact source mismatch`);
  }
}
const delta = {
  schema_version: 1, status: 'ROW_BYTES_UNCHANGED_ROUTING_ONLY_HOLD',
  row10b_sha256: pinned.row10b_row,
  row10c_sha256: sha(canonical(row)),
  row_changed_paths: [],
  prior_routing_amendment_sha256: sha(read(row10bDir, 'routing-amendment.json')),
  phase4_manifest_sha256: pinned.phase4_manifest,
  routing_changes: [
    'pin the exact Phase4 T06 script, scenes and independent fullscript review',
    'replace obsolete nonspoken source-card requirement with audible JIII attribution in turn-s088',
    'require full JIII source URL in final video description',
    'retain t18 source 2/fact null before verifier and in persisted readback after verifier',
  ],
};
const verification = {
  schema_version: 1, status: 'PASS_OFFLINE_ROW_PHASE4_ROUTE_SHAPE_ONLY_HOLD',
  canonical_story_sha256: storySha,
  row_bytes_same_as_row10b: true,
  row_schema_problems: problems,
  existing_fact_count: row.must_verify.length,
  old_scene_count: keys.reduce((sum, key) => sum + JSON.parse(read(flow, `remapped-chapters/${key}.json`)).scenes.length, 0),
  old_scene_claim_count: claims.length,
  old_scene_claims_sha256: oldClaimsSha,
  old_scene_claims_all_unchecked: true,
  unchanged_parent_chapter_sha256: chapterFiles,
  old_review_problems: oldReviewProblems,
  row10c_route_independently_reviewed: false,
  phase4_scene_count: phase4Scenes.length,
  phase4_shot_count: phase4Scenes.filter((scene) => scene.template === 'shot').length,
  phase4_scene_claim_count: phase4Claims.length,
  phase4_scene_claims_all_unchecked: true,
  phase4_t06_audible_attribution_offline: true,
  formal_worker_chapters_matched: false,
  formal_65_scene_claims_reviewed: false,
  t18_pre_verifier_chapter_rewrite_done: false,
  t18_post_verifier_fact_null_readback_done: false,
  final_description_source_url_present: false,
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
  schema_version: 1, status: 'OFFLINE_ROW_PHASE4_ROUTE_ONLY_HOLD', pins: pinned,
  canonical_story_sha256: storySha,
  unchanged_parent_chapter_sha256: chapterFiles,
  files: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  README_sha256: sha(read(here, 'README.md')),
  RECONCILIATION_HOLD_sha256: sha(read(here, 'RECONCILIATION-HOLD.md')),
  build_sha256: sha(read(here, 'build.mjs')),
};
if (mode === '--write') fs.writeFileSync(path.join(here, 'sha256.json'), canonical(manifest));
else assert.equal(fs.readFileSync(path.join(here, 'sha256.json'), 'utf8'), canonical(manifest), 'manifest drift');
console.log(JSON.stringify({ status: verification.status, mode, canonical_story_sha256: storySha,
  must_verify: row.must_verify.length, phase4_scenes: phase4Scenes.length, phase4_claims: phase4Claims.length }));
