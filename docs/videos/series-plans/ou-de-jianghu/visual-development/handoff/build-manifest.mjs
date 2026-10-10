import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';

// Run from repository root; argument is the parent of ou-de-jianghu-e001.
const mediaRoot = process.argv[2];
const check = process.argv.includes('--check');
if (!mediaRoot) throw new Error('Usage: node handoff/build-manifest.mjs <VIDEO_WORKDIR> [--check]');
const base = 'docs/videos/series-plans/ou-de-jianghu/visual-development/';
const digest = value => crypto.createHash('sha256').update(value).digest('hex');
const sha = file => digest(fs.readFileSync(file));
const read = file => JSON.parse(fs.readFileSync(base + file, 'utf8'));
const inventory = read('asset-inventory.json');
assert.equal(inventory.source_files.length,12);
for (const source of inventory.source_files) assert.equal(sha(source.path), source.sha256, source.path);
const portraits = read('episode1-portraits/finalized-views-receipt.json');
const references = read('animation-reference/finalized-media-receipt.json');
const scenes = read('scene-prop-design/media-receipt.json');
const staging = read('import-contract/pending-staging-receipt.json');
const mapping = read('handoff/finalization-20261009.json');
const v4 = read('episode-plan/finalization-v4-verification.json');
const cold = read('scene-prop-design/cold-state-spec.json');
const fanReview = read('animation-reference/fan-independent-final-review.json');
const mouthReview = read('animation-reference/mouth-independent-review.json');
assert.equal(mapping.working_video.sha256, 'cb341b457f28e5139cff6f0528722d2a0facebf8cfea90423aec572ed71ebd17');
assert.equal(mapping.shots.length, 455);
assert.equal(mapping.validation.cold_master_input_count, 0);
assert.equal(mapping.validation.all_asset_final_bindings_pending, true);
assert.deepEqual(mapping.fan_reference_policy.masters.map(x=>x.candidate_key),['shen-guihe-construction-details-v3','personal-prop-states-v3']);
assert.equal(sha(mapping.working_video.file.replace('<VIDEO_WORKDIR>', mediaRoot)), mapping.working_video.sha256);
for (const source of mapping.reference_snapshot_sources) assert.equal(sha(source.file), source.sha256, `Rebuild finalization mapping first: ${source.file}`);
for (const receipt of [portraits, references]) for (const source of receipt.source_files) assert.equal(sha(source.path), source.sha256, source.path);
const cast = JSON.parse(fs.readFileSync('docs/videos/series-plans/ou-de-jianghu/production/cast.json', 'utf8'));
const shotLooks = cast.characters.map(c => ({ character_id: c.id, shot_looks: c.shot_looks ?? [] }));
const assets = [];
function add(category, key, character, use, version, file, hash, dimensions, receipt, limits = []) {
  const relative = file.replace('<VIDEO_WORKDIR>/', '');
  const bytes = fs.readFileSync(path.join(mediaRoot, relative));
  assert.equal(digest(bytes), hash, relative);
  assert.equal(bytes.subarray(0,8).toString('hex'), '89504e470d0a1a0a', relative);
  assert.equal(bytes.readUInt32BE(16), dimensions.width, relative);
  assert.equal(bytes.readUInt32BE(20), dimensions.height, relative);
  assets.push({ category, key, character_id: character, look_id: character ? 'base' : null,
    use, version, file: '<VIDEO_WORKDIR>/' + relative, sha256: hash, native_dimensions: dimensions,
    receipt, status: 'candidate_for_owner_review', owner_accepted: false, judge: null,
    normal_runtime_integrated: false, animation_verified: false, limitations: limits });
}
for (const a of portraits.concepts) {
  add('concept', a.id, a.character, 'art_direction', a.version, a.file, a.sha256,
    {width: a.width, height: a.height}, 'episode1-portraits/finalized-views-receipt.json');
}
for (const a of portraits.assets) {
  add('portrait', a.key, a.character_id, a.view, a.version, a.path, a.sha256,
    a.native_dimensions, 'episode1-portraits/finalized-views-receipt.json',
    [a.dimension_status, a.aspect_ratio_status, a.reference_use_disposition].filter(Boolean));
}
for (const a of references.entries.filter(a => !a.reused_prior_master)) {
  add('animation_reference', a.key, a.character_id ?? null, a.view,
    Number(a.key.match(/-v(\d+)$/)?.[1] ?? 1), a.file, a.sha256,
    {width: a.width, height: a.height}, 'animation-reference/finalized-media-receipt.json', a.limitations);
}
for (const a of scenes.media.filter(a => a.status === 'candidate' && !a.id.startsWith('chess-guestroom-cold'))) {
  add('scene_or_prop', `${a.id}-v${a.version}`, null, a.kind, a.version,
    'ou-de-jianghu-e001/' + a.file, a.sha256, {width: a.width, height: a.height},
    'scene-prop-design/media-receipt.json', [a.visual_qa]);
}
assert.equal(assets.length, 146);
assert.equal(new Set(assets.map(a => a.sha256)).size, 146);
assert.equal(new Set(assets.map(a => a.key)).size, 146);
for (const [category,count] of Object.entries({concept:9,portrait:27,animation_reference:82,scene_or_prop:28})) assert.equal(assets.filter(a=>a.category===category).length,count,category);
assert.equal(assets.filter(a=>a.use==='mouth-shapes').length,8);
assert.equal(assets.some(a=>a.key.startsWith('chess-guestroom-cold')),false);
assert.equal(cold.images_rendered,false);
assert.equal(assets.find(a=>a.key==='chess-guestroom-master-v4')?.sha256,cold.base.sha256);
for(const reviewed of fanReview.media)assert.equal(assets.find(a=>a.key===reviewed.key)?.sha256,reviewed.sha256,`Final fan review differs from selected image ${reviewed.key}`);
for(const reviewed of mouthReview.assets)assert.equal(assets.find(a=>a.key===reviewed.selected_key)?.sha256,reviewed.sha256,`Mouth review differs from selected image ${reviewed.selected_key}`);
assert.equal(mouthReview.assets.length,8);
for(const master of mapping.fan_reference_policy.masters)assert.equal(assets.find(a=>a.key===master.candidate_key)?.sha256,master.sha256);
const characterIds = [...new Set(portraits.assets.map(a => a.character_id))];
assert.equal(characterIds.length, 9);
assert.equal(shotLooks.reduce((n,c) => n+c.shot_looks.length, 0), 16);
const reuse = references.entries.filter(a => a.reused_prior_master).map(a => {
  const portrait = assets.find(p => p.key === a.key && p.sha256 === a.sha256);
  assert.ok(portrait, `Missing reused portrait: ${a.key}`);
  return {key: a.key, character_id: a.character_id, use: 'front', sha256: a.sha256};
});
assert.equal(reuse.length, 9);
assert.equal(sha(staging.staging_manifest.replace('<VIDEO_WORKDIR>', mediaRoot)), staging.staging_manifest_sha256);
assert.equal(sha(staging.project.replace('<VIDEO_WORKDIR>', mediaRoot)), staging.project_sha256);
assert.notEqual(staging.project_sha256, mapping.working_video.sha256);
assert.equal(staging.candidates.length,9);
const historicalCandidates=staging.candidates.map(candidate=>{
  assert.equal(sha(candidate.original.replace('<VIDEO_WORKDIR>',mediaRoot)),candidate.sha256,candidate.original);
  const current=assets.find(a=>a.category==='portrait'&&a.use==='full-body'&&a.character_id===candidate.character_id);
  return {...candidate,status:'historical_v3_isolated_pending_candidate',current_selected_portrait_key:current.key,same_pixels_as_current_portrait:current.sha256===candidate.sha256,current_v4_binding:false,normal_runtime_integrated:false};
});
const files = ['asset-inventory.json', 'art-direction/media-receipt.json',
  'episode1-portraits/media-receipt.json',
  'episode1-portraits/independent-views-receipt.json', 'animation-reference/media-receipt.json',
  'animation-reference/prompts.json', 'animation-reference/gallery-verification.json',
  'scene-prop-design/media-receipt.json', 'scene-prop-design/portability-verification.json',
  'episode-plan/proposal-summary.json', 'episode-plan/package-verification.json',
  'episode-plan/presentation-review.json', 'episode-plan/budget-and-batches.json',
  'episode-plan/camera-and-risk-ledger.json', 'episode-plan/preproduction-package-v3.md',
  'import-contract/pending-staging-receipt.json',
  'episode1-portraits/finalized-views-receipt.json',
  'animation-reference/finalized-media-receipt.json', 'animation-reference/finalization-20261009.json',
  'animation-reference/mouth-independent-review.json', 'animation-reference/fan-independent-final-review.json',
  'animation-reference/gallery-verification-20261009.json',
  'animation-reference/verify-final-gallery.mjs',
  'scene-prop-design/go-layout-decision.json', 'scene-prop-design/cold-state-spec.json',
  'episode-plan/finalization-v4-verification.json', 'episode-plan/finalization-v4.md',
  'handoff/finalization-20261009.json', 'handoff/finalization-20261009.md'];
const manifest = {
  schema_version: 2, episode: 'ou-de-jianghu-e001', status: 'preproduction_review_package',date_local:'2026-10-09',
  source_commit:execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(), inventory_source_commit:inventory.source_commit, source_files: inventory.source_files,
  builder:{file:base+'handoff/build-manifest.mjs',sha256:sha(base+'handoff/build-manifest.mjs'),commit_is_context_only:true},
  accepted_style: '保留目前華麗古裝與細緻人物風格', owner_asset_selection: false,
  plan_locked: false, normal_runtime_integrated: false, paid_animation_started: false,
  counts: {characters: 9, concepts: 9, portraits: 27, new_character_references: 82,
    reused_front_views: 9, character_reference_uses: 91, static_mouth_sheets:8,scene_and_prop_candidates: 28,
    unique_latest_art: 146},
  reference_history_counts_from_receipt:references.counts,
  characters: characterIds.map(id => ({character_id: id, name: cast.characters.find(c => c.id === id).name,
    look_id: 'base', asset_keys: assets.filter(a => a.character_id === id).map(a => a.key)})),
  assets, reused_references: reuse,
  current_proposal:{version:'v4',...mapping.working_video,shot_count:455,change_count:2,dialogue_motion_camera_duration_unchanged:v4.dialogue_motion_camera_duration_unchanged,budget_numerics_and_batches_unchanged:v4.budget_numerics_and_batches_unchanged,formal_runtime_binding:false,owner_accepted:false,p7_accepted:false},
  resolution_disposition:{native_portrait_pngs_verified:27,editorial_targets_not_import_gates:true,below_editorial_target:portraits.assets.filter(a=>a.dimension_status==='native_below_target').length,upscaled:false,use:'native identity and costume reference candidates for future first-frame creation',future_actual_shot_contract: 'Choose a supported route and read back actual first-frame pixels; current drama keyframes default is 1K, H3 first-frame I2V excludes simultaneous reference_images.'},
  static_mouth_reference:{count:8,source:'animation-reference/finalized-media-receipt.json',timed_phonemes:false,lip_sync_verified:false,not_a_full_headwear_master:true,silent_yin_wusheng_excluded:true},
  fan_reference_policy:mapping.fan_reference_policy,
  cold_room:{independent_cold_master_selected:false,all_cold_versions_not_for_input:true,derived_clean_master:cold.base,derived_shots:cold.shots.map(s=>s.shot_id),state_spec:'scene-prop-design/cold-state-spec.json',rendered:false},
  shot_looks_binding: {source: 'docs/videos/series-plans/ou-de-jianghu/production/cast.json',
    serialization: 'JSON.stringify(characters.map(c => ({character_id:c.id,shot_looks:c.shot_looks??[]})))',
    sha256: digest(JSON.stringify(shotLooks)), named_look_count: 16,
    covered_by_native_look_hash: false, catalogue: shotLooks},
  isolated_pending_import: {receipt: 'import-contract/pending-staging-receipt.json',
    status:'historical_v3_only_not_current_v4_import',project:staging.project,current_v4_binding:false,
    candidate_count: 9, staging_manifest_sha256: staging.staging_manifest_sha256,
    project_sha256: staging.project_sha256, native_look_hash: staging.look_hash,
    fetch_attempts: staging.fetch_attempts, judge: null, owner_accepted: false,
    selection_for_offline_candidate_validation_only: true, normal_runtime_integrated: false,candidates:historicalCandidates},
  bound_files: files.map(file => ({file, sha256: sha(base + file)})),
  remaining_constraints: [
    'All selected artwork remains a review candidate; accepted style is not individual asset adoption.',
    '18 portrait half/full views remain below editorial 1600/2048 targets; current native PNGs are valid identity/costume references, not rendered first frames. No upscaling is claimed.',
    'Six-angle sets are 2D/I2V references, not physical turntables or rigged geometry; pose and perspective variations are recorded.',
    'Only shen-guihe-construction-details-v3 and personal-prop-states-v3 govern fan anatomy: white jade, white paper, no tassel/chain/charm. Pose/concept/color images may retain tiny hand-adjacent marks and are not fan topology evidence; no global pixel-consistency claim.',
    'The independent cold-room masters are retired/not-for-input; future cold first frames derive from clean master-v4 and the unrendered state spec.',
    'AI Go-board grids and stones are illustrative; six exact 19x19 subset states preserve original 16 then 17 coordinates and must guide future first/last frames.',
    'Scene ledger 10 location rows map to 9 plan space families by combining Qiyun mountain/watchtower.',
    'Scene shot-prop index follows original script; current v4 proposal and reference mapping govern redesigned actions, without owner adoption being implied.',
    'Eight static mouth sheets do not establish phoneme mapping, TTS timing or lipsync QA.',
    'Nine old isolated imports are historical v3-bound pending records. The latest Shen fullbody has not been imported, chosen or approved for runtime.',
    'Estimated 1403.533 seconds exceeds the 1380-second upper duration goal; measure TTS and resolve before clips.',
    'Formal script/look/audio/storyboard/plan gates and paid continuous three-shot pilot are future production work.',
    'Later season 14 characters and 16 named look variants stay in their existing task; this package covers episode one.'
  ]
};
const serialized=JSON.stringify(manifest,null,2)+'\n';
if(check)assert.equal(fs.readFileSync(base+'handoff/asset-manifest.json','utf8'),serialized,'Manifest differs; rebuild against the finalized receipts');
else fs.writeFileSync(base + 'handoff/asset-manifest.json', serialized);
console.log(JSON.stringify({status:'verified', source_files:inventory.source_files.length,
  unique_latest_art:assets.length, reused_references:reuse.length, bound_files:files.length,
  staging_candidates:9, shot_looks:16}));
