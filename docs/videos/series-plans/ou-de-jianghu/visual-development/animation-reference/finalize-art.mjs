import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { inspectLookPng } from '../../../../../../tools/video/media/look.mjs';

const media = path.resolve(process.argv[2] || '');
if (!process.argv[2]) throw Error('Pass the episode media directory');
const base = 'docs/videos/series-plans/ou-de-jianghu/visual-development/';
const dir = path.join(media, 'final-art/20261009');
const read = f => JSON.parse(fs.readFileSync(f, 'utf8'));
const digest = b => crypto.createHash('sha256').update(b).digest('hex');
const sha = f => digest(fs.readFileSync(f));
const portable = f => '<VIDEO_WORKDIR>/ou-de-jianghu-e001/' + path.relative(media, f).replaceAll('\\', '/');
const inventory = read(base + 'asset-inventory.json');
for (const s of inventory.source_files) assert.equal(sha(s.path), s.sha256, s.path);
const rootOutputs = read(path.join(dir, 'outputs-root.json'));
const mouthOutputs = read(path.join(dir, 'mouth-study-outputs.json'));
const mouthPrompts = read(path.join(dir, 'mouth-study-prompts.json')).entries;
const all = [...rootOutputs, ...mouthOutputs];
assert.equal(rootOutputs.length, 18);
assert.equal(mouthOutputs.length, 9);
const records = all.map(a => {
  const bytes = fs.readFileSync(a.file), dims = inspectLookPng(bytes);
  assert.equal(digest(bytes), sha(a.original), 'Original bytes must be preserved: ' + a.key);
  const p = a.prompt ? a : mouthPrompts.find(p => p.key === a.key);
  assert.ok(p?.prompt, a.key);
  const refs = p.target ? [{file:p.target,role:'edit_target'}] : p.references ?? [p.reference];
  const ref = refs[0].file;
  const keyStem = a.key.replace(/-v\d+$/, '');
  const selected = !all.some(b => b.key.replace(/-v\d+$/, '') === keyStem && Number(b.key.match(/-v(\d+)$/)[1]) > Number(a.key.match(/-v(\d+)$/)[1]));
  return {key:a.key, logical_key:keyStem, version:Number(a.key.match(/-v(\d+)$/)[1]),
    file:portable(a.file), sha256:digest(bytes), bytes:bytes.length,
    width:dims.width, height:dims.height, original_bytes_preserved:true,
    original:'<IMAGEGEN_ORIGINAL>/' + path.basename(path.dirname(a.original)) + '/' + path.basename(a.original),
    prompt:p.prompt, prompt_sha256:digest(p.prompt), reference:{file:portable(ref),sha256:sha(ref)},
    references:refs.map(r=>({role:r.role??'identity_reference',file:portable(r.file),sha256:sha(r.file)})),
    provider:'builtin_imagegen', exact_model:null, billing_usd:null, selected,
    status:selected?'editorial_preferred_pending_owner_adoption':'superseded_candidate',
    fan_attachment_limit:['shen-guihe-concept-v5','shen-guihe-right-profile-v3','shen-guihe-left-three-quarter-v3'].includes(a.key)?'Uncertain small pendant/line at fist; identity and costume use only, prohibited as fan construction master.':null,
    owner_accepted:false, judge:null, animation_verified:false};
});
assert.equal(records.filter(r => r.selected).length, 19);
const selected = new Map(records.filter(r => r.selected).map(r => [r.logical_key,r]));
const fanPolicy = {
  detail_master:'shen-guihe-construction-details-v3',prop_master:'personal-prop-states-v3',
  geometry:'White paper, white jade guards/ribs, tiny silver pivot; no fan-mounted string, chain or tassel.',
  other_views:'Identity, costume, pose and palette only. Small ambiguous fist-side pendants/lines in some pose or concept views must not define fan construction.',
  first_frame_rule:'Use the two clear prop/detail masters for fan construction; reject a first frame that adds fan-mounted ornaments.'
};
const oldPortraits = read(base + 'episode1-portraits/independent-views-receipt.json');
const portraits = structuredClone(oldPortraits.assets.filter(a => a.latest_version));
for (const a of portraits) {
  const r = selected.get(a.key.replace(/-v\d+$/, ''));
  if (r) Object.assign(a, {key:r.key,version:r.version,path:r.file,sha256:r.sha256,bytes:r.bytes,
    native_dimensions:{width:r.width,height:r.height,long_edge:Math.max(r.width,r.height),aspect_ratio:r.width/r.height},
    revision_of:a.key, references:r.references, prompt_sha256:r.prompt_sha256,
    prompt_source:'animation-reference/finalization-20261009.json',prompt_key:r.key,
    original_generated_filename:path.basename(r.original), review_status:'visually_reviewed_fan_material_correction'});
  a.reference_use_disposition = 'Original size retained for identity/costume reference; not a rendered shot or final delivery.';
}
const concepts = structuredClone(read(base+'episode1-portraits/media-receipt.json').assets.filter(a=>a.display_as_latest));
for(const a of concepts){const r=selected.get(a.id.replace(/-v\d+$/,''));if(r)Object.assign(a,{id:r.key,version:r.version,
  revision_of:a.id,file:r.file.replace('<VIDEO_WORKDIR>/',''),sha256:r.sha256,bytes:r.bytes,width:r.width,height:r.height});}
const portraitReceipt={schema_version:1,date_local:'2026-10-09',source_files:inventory.source_files,
  historical_receipts:['independent-views-receipt.json','media-receipt.json'],
  status:'editorial_preferred_reference_set_pending_owner_adoption',owner_accepted:false,runtime_integrated:false,fan_use_policy:fanPolicy,
  counts:{characters:9,portraits:27,concepts:9,revised_portraits:2,revised_concepts:1},assets:portraits,concepts,
  dimension_disposition:'18 half/full portraits remain below the old 1600/2048 editorial suggestions. Their native dimensions are accepted by the editor for identity and costume reference only; no owner size waiver, upscaling or final-shot acceptance is asserted.'};
fs.writeFileSync(base+'episode1-portraits/finalized-views-receipt.json',JSON.stringify(portraitReceipt,null,2)+'\n');

const oldReference = read(base+'animation-reference/media-receipt.json');
const entries = structuredClone(oldReference.entries);
for (const a of entries) {
  const r=selected.get(a.key.replace(/-v\d+$/,''));
  if(r)Object.assign(a,{revision_of:a.key,key:r.key,file:r.file.replace('<VIDEO_WORKDIR>/',''),sha256:r.sha256,
    bytes:r.bytes,width:r.width,height:r.height,version:r.version,original_bytes_preserved:true});
}
for(const r of records.filter(r=>r.selected&&r.key.includes('-mouth-shapes-'))){
  entries.push({key:r.key,character_id:r.key.split('-mouth-shapes-')[0],view:'mouth-shapes',version:r.version,
    file:r.file.replace('<VIDEO_WORKDIR>/',''),sha256:r.sha256,bytes:r.bytes,width:r.width,height:r.height,
    reused_prior_master:false,status:r.status,owner_accepted:false,judge:null,rigged:false,
    limitations:['Six static mouth studies: closed, slight part, A, E/I, O, U. Not timed phonemes or validated lip-sync.','Some crowns/hat edges are cropped; use the separate headshot/crown master for headwear.']});
}
assert.equal(entries.length,91);
assert.equal(entries.filter(e=>e.view==='mouth-shapes').length,8);
assert.equal(entries.filter(e=>e.character_id==='yin-wusheng'&&e.view==='mouth-shapes').length,0);
const ar={...oldReference,date_local:'2026-10-09',historical_receipt:'media-receipt.json',
  retained_originals:oldReference.retained_originals.map(r=>({...r,selected_in_20261008_receipt:r.selected,selected:entries.some(e=>!e.reused_prior_master&&e.key===r.key)})),
  status:'editorial_preferred_reference_set_pending_owner_adoption',entries,fan_use_policy:fanPolicy,
  counts:{characters:9,new_selected_png:82,reused_front_png:9,total_reference_uses:91,mouth_study_sheets:8,
    all_new_png_including_history:112,unique_generated_images:111,alias_files:1},
  finalization_history:records.filter(r=>!/-full-body-|-three-quarter-halfbody-|-concept-/.test(r.key)).map(r=>({key:r.key,file:r.file,sha256:r.sha256,selected:r.selected})),
  finalization_receipt:'finalization-20261009.json',
  limitations:['Native reference sizes are preserved, with an explicit identity/costume-use disposition; these are not final frame delivery sizes.',
    'Pose and perspective vary slightly; these are 2D references, not an orthographic rig.',
    'Mouth sheets are static acting references and do not establish lip-sync.',
    'Individual owner adoption and actual runtime look/judge remain pending.']};
fs.writeFileSync(base+'animation-reference/finalized-media-receipt.json',JSON.stringify(ar,null,2)+'\n');
const finalization={schema_version:1,date_local:'2026-10-09',source_files:inventory.source_files,
  generated_images:records.length,selected_new_images:19,fan_corrections:11,fan_attempts:18,mouth_generated:9,mouth_selected:8,
  editorial_decision:'Use white-jade guards/ribs, white paper, tiny silver pivot, no fan-mounted cord/tassel; preserve blue ornaments at the waist.',
    owner_accepted:false,paid_animation_started:false,fan_use_policy:fanPolicy,records};
fs.writeFileSync(base+'animation-reference/finalization-20261009.json',JSON.stringify(finalization,null,2)+'\n');
fs.writeFileSync(path.join(dir,'character-finalization.json'),JSON.stringify(finalization,null,2)+'\n');
console.log(JSON.stringify({sources:12,png_checked:records.length,selected:19,portraits:27,concepts:9,character_reference_uses:91}));
