import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';

// Run from repository root; argument is the parent of ou-de-jianghu-e001.
const mediaRoot = process.argv[2];
if (!mediaRoot) throw new Error('Usage: node handoff/build-manifest.mjs <VIDEO_WORKDIR>');
const base = 'docs/videos/series-plans/ou-de-jianghu/visual-development/';
const digest = value => crypto.createHash('sha256').update(value).digest('hex');
const sha = file => digest(fs.readFileSync(file));
const read = file => JSON.parse(fs.readFileSync(base + file, 'utf8'));
const inventory = read('asset-inventory.json');
for (const source of inventory.source_files) assert.equal(sha(source.path), source.sha256, source.path);
const portraits = read('episode1-portraits/independent-views-receipt.json');
const references = read('animation-reference/media-receipt.json');
const scenes = read('scene-prop-design/media-receipt.json');
const staging = read('import-contract/pending-staging-receipt.json');
const cast = JSON.parse(fs.readFileSync('docs/videos/series-plans/ou-de-jianghu/production/cast.json', 'utf8'));
const shotLooks = cast.characters.map(c => ({ character_id: c.id, shot_looks: c.shot_looks ?? [] }));
const assets = [];
function add(category, key, character, use, version, file, hash, dimensions, receipt, limits = []) {
  const relative = file.replace('<VIDEO_WORKDIR>/', '');
  assert.equal(sha(path.join(mediaRoot, relative)), hash, relative);
  assets.push({ category, key, character_id: character, look_id: character ? 'base' : null,
    use, version, file: '<VIDEO_WORKDIR>/' + relative, sha256: hash, native_dimensions: dimensions,
    receipt, status: 'candidate_for_owner_review', owner_accepted: false, judge: null,
    normal_runtime_integrated: false, animation_verified: false, limitations: limits });
}
for (const a of read('episode1-portraits/media-receipt.json').assets.filter(a => a.display_as_latest)) {
  add('concept', a.id, a.character, 'art_direction', a.version, a.file, a.sha256,
    {width: a.width, height: a.height}, 'episode1-portraits/media-receipt.json');
}
for (const a of portraits.assets.filter(a => a.latest_version)) {
  add('portrait', a.key, a.character_id, a.view, a.version, a.path, a.sha256,
    a.native_dimensions, 'episode1-portraits/independent-views-receipt.json',
    [a.dimension_status, a.aspect_ratio_status]);
}
for (const a of references.entries.filter(a => !a.reused_prior_master)) {
  add('animation_reference', a.key, a.character_id ?? null, a.view,
    Number(a.key.match(/-v(\d+)$/)?.[1] ?? 1), a.file, a.sha256,
    {width: a.width, height: a.height}, 'animation-reference/media-receipt.json', a.limitations);
}
for (const a of scenes.media.filter(a => a.status === 'candidate')) {
  add('scene_or_prop', `${a.id}-v${a.version}`, null, a.kind, a.version,
    'ou-de-jianghu-e001/' + a.file, a.sha256, {width: a.width, height: a.height},
    'scene-prop-design/media-receipt.json', [a.visual_qa]);
}
assert.equal(assets.length, 139);
assert.equal(new Set(assets.map(a => a.sha256)).size, 139);
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
const files = ['asset-inventory.json', 'art-direction/media-receipt.json',
  'episode1-portraits/media-receipt.json',
  'episode1-portraits/independent-views-receipt.json', 'animation-reference/media-receipt.json',
  'animation-reference/prompts.json', 'animation-reference/gallery-verification.json',
  'scene-prop-design/media-receipt.json', 'scene-prop-design/portability-verification.json',
  'episode-plan/proposal-summary.json', 'episode-plan/package-verification.json',
  'episode-plan/presentation-review.json', 'episode-plan/budget-and-batches.json',
  'episode-plan/camera-and-risk-ledger.json', 'episode-plan/preproduction-package-v3.md',
  'import-contract/pending-staging-receipt.json'];
const manifest = {
  schema_version: 1, episode: 'ou-de-jianghu-e001', status: 'preproduction_review_package',
  source_commit: inventory.source_commit, source_files: inventory.source_files,
  accepted_style: '保留目前華麗古裝與細緻人物風格', owner_asset_selection: false,
  plan_locked: false, normal_runtime_integrated: false, paid_animation_started: false,
  counts: {characters: 9, concepts: 9, portraits: 27, new_character_references: 74,
    reused_front_views: 9, character_reference_uses: 83, scene_and_prop_candidates: 29,
    unique_latest_art: 139, character_reference_retained_png_files: 90,
    character_reference_unique_generated_images: 89, character_reference_alias_files: 1},
  characters: characterIds.map(id => ({character_id: id, name: cast.characters.find(c => c.id === id).name,
    look_id: 'base', asset_keys: assets.filter(a => a.character_id === id).map(a => a.key)})),
  assets, reused_references: reuse,
  shot_looks_binding: {source: 'docs/videos/series-plans/ou-de-jianghu/production/cast.json',
    serialization: 'JSON.stringify(characters.map(c => ({character_id:c.id,shot_looks:c.shot_looks??[]})))',
    sha256: digest(JSON.stringify(shotLooks)), named_look_count: 16,
    covered_by_native_look_hash: false, catalogue: shotLooks},
  isolated_pending_import: {receipt: 'import-contract/pending-staging-receipt.json',
    candidate_count: 9, staging_manifest_sha256: staging.staging_manifest_sha256,
    project_sha256: staging.project_sha256, native_look_hash: staging.look_hash,
    fetch_attempts: staging.fetch_attempts, judge: null, owner_accepted: false,
    selection_for_offline_candidate_validation_only: true, normal_runtime_integrated: false},
  bound_files: files.map(file => ({file, sha256: sha(base + file)})),
  remaining_constraints: [
    'All selected artwork remains a review candidate; accepted style is not individual asset adoption.',
    '18 portrait half/full views are below suggested delivery dimensions; originals were not upscaled.',
    'Six-angle sets are 2D/I2V references, not physical turntables or rigged geometry; pose and perspective variations are recorded.',
    'Shen fan dark outer guards in character references versus white jade in canonical scene prop must be reconciled before fan closeups.',
    'Three guestroom paper-window candidates retain a moon outline: spatial proposals only, not window closeup masters.',
    'AI Go-board grids and stones are illustrative; exact 19x19 SVG proposals require adoption for relevant first/last frames.',
    'Scene ledger 10 location rows map to 9 plan space families by combining Qiyun mountain/watchtower.',
    'Scene shot-prop index follows original script; adopted v3 camera/risk ledger governs redesigned actions.',
    'Estimated 1403.533 seconds exceeds the 1380-second upper duration goal; measure TTS and resolve before clips.',
    'Formal script/look/audio/storyboard/plan gates and paid continuous three-shot pilot are future production work.',
    'Later season 14 characters and 16 named look variants stay in their existing task; this package covers episode one.'
  ]
};
fs.writeFileSync(base + 'handoff/asset-manifest.json', JSON.stringify(manifest, null, 2) + '\n');
console.log(JSON.stringify({status:'verified', source_files:inventory.source_files.length,
  unique_latest_art:assets.length, reused_references:reuse.length, bound_files:files.length,
  staging_candidates:9, shot_looks:16}));
