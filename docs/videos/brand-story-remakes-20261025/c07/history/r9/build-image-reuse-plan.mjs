// Pure local request-key rehearsal. This does not invoke Stage.image or a provider.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {resolveLook,keyframeKey} from '../../../../tools/video/core/drama.mjs';
import {shotPrompt} from '../../../../tools/video/media/keyframes.mjs';
import {Stage,imageSelectionVersion} from '../../../../tools/video/media/stages.mjs';

const OUT=path.dirname(fileURLToPath(import.meta.url)),REPO=path.resolve(OUT,'../../../..');
const read=f=>JSON.parse(fs.readFileSync(path.join(OUT,f),'utf8'));
const sha=x=>createHash('sha256').update(x).digest('hex'),fileSha=f=>sha(fs.readFileSync(f));
const doc=read('video.json'),series=read('series.json'),look=resolveLook(doc.look);
assert.deepEqual(doc.characters,[]);
const definitions=[
  ['c7r20104','c7r20301','knife-before-cut-shared-still','A plain knife is held just above a worn sole edge; no detached parts or teardown result are visible.'],
  ['c7h04b1','c7r20607','return-parcel-shared-still','The plain shoebox is closed and its contents are invisible; no new laces, unboxing order or customer likeness is drawn.'],
];
const pairs=definitions.map(([setup,payoff,asset,withheld])=>{
  const a=doc.scenes.find(s=>s.lines.some(l=>l.id===setup));
  const b=doc.scenes.find(s=>s.lines.some(l=>l.id===payoff));
  assert(a&&b);assert.equal(a.data.prompt,b.data.prompt);assert.equal(a.data.camera,b.data.camera);
  const prompt=shotPrompt(a,look,[],1500),payoffPrompt=shotPrompt(b,look,[],1500);
  assert.equal(prompt,payoffPrompt);
  const options={prompt,negative:look.negative??'',references:[],seed:1,size:null};
  const context={status:{image:{provider:'minimax',model:'image-01'}},format:'drama',imageVersion:imageSelectionVersion(series)};
  const key=Stage.prototype.imageKey.call(context,options);
  assert.equal(key,Stage.prototype.imageKey.call(context,{...options,prompt:payoffPrompt}));
  const tuple={provider:'minimax',model:'image-01',prompt,negative:options.negative,width:1920,height:1080,seed:1,references:[]};
  return {
    asset_plan_id:asset,role:'PLANNED_ONE_IDENTICAL_IMAGE_NOT_AN_ACTUAL_ASSET',
    setup_scene_id:a.id,setup_line_id:setup,payoff_scene_id:b.id,payoff_line_id:payoff,
    setup_text:a.lines.find(l=>l.id===setup).text,payoff_text:b.lines.find(l=>l.id===payoff).text,
    prompt:a.data.prompt,setup_prompt_sha256:sha(a.data.prompt),payoff_prompt_sha256:sha(b.data.prompt),prompts_identical:true,
    camera:a.data.camera,cameras_identical:true,cast:[],cast_appearance_prompt:'',cast_identical:true,
    no_result_drawn_in_teaser:withheld,
    source_scope:setup==='c7r20104'?'Authorised repair demonstration is a different boot from either public commenter; shared anonymous illustration is not proof of shared physical identity.':'July public review is not verified and gives no documentary unboxing sequence; this is a neutral conceptual parcel shared at two narration positions.',
    native_same_input_key_rehearsal:{pure_local_functions_only:true,input_tuple:tuple,aspect:'16:9',requested_size:null,nominal_image_size:'1K',image_selection_version:context.imageVersion,seed_offset:0,takes:1,correction_list:[],prompt_budget_chars:1500,base_key:keyframeKey(tuple),native_stage_key:key,setup_and_payoff_keys_identical:true,parameters_are_declared_plan_not_backend_readback:true,no_provider_call:true},
    actual_source_file:null,actual_source_sha256:null,actual_reused_file:null,actual_reused_sha256:null,
    actual_same_asset_verified:false,actual_same_file_sha_verified:false,
  };
});
const files=['tools/video/media/keyframes.mjs','tools/video/media/stages.mjs','tools/video/media/cache.mjs','tools/video/media/prompt-budget.mjs','tools/video/core/drama.mjs','tools/video/media/trim.mjs'];
const cli=(scene)=>['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs','/workspace/work/brand-story-20261025/c07-submission-root','keyframes','--slug',doc.slug,'--workdir','/workspace/work/brand-story-20261025/media','--shot',scene,'--takes','1'];
const plan={
  schema_version:1,revision:'c07-r9',status:'WRITTEN_REUSE_PLAN_PENDING_GENERATION_AND_REAL_FILE_SHA_VERIFICATION',
  not_a_video_schema_extension:true,not_a_keyframes_manifest:true,no_assets_generated:true,actual_same_asset_verified:false,
  candidate_binding:{core_four_sha256:Object.fromEntries(['video.json','script.md','narration-only.json','claims.json'].map(f=>[f,fileSha(path.join(OUT,f))])),claims_md_sha256:fileSha(path.join(OUT,'claims.md')),brief_sha256:fileSha(path.join(OUT,'brief.md')),series_sha256:fileSha(path.join(OUT,'series.json'))},
  rule:{file:'.agents/skills/youtube-video/references/script-writing.md',sha256:fileSha(path.join(REPO,'.agents/skills/youtube-video/references/script-writing.md')),quote:'每一個預告句用回收它的那一章的畫面（同一張圖）'},
  code_readback:{files_sha256:Object.fromEntries(files.map(f=>[f,fileSha(path.join(REPO,f))])),still_alias_field_available:false,clip_source_field_not_applicable:'data.source refers to an earlier clip, not a still alias; no video schema field or keyframes manifest was invented.',native_supported_route:'Official keyframes --shot and the ordinary exact-request cache, with an explicit live-cache byte/SHA check before the teaser invocation.',cache_identity:'Stage.imageKey includes provider/model/composed prompt/negative/reference SHA/seed/dimensions and image-selection version. Camera and cast enter the composed prompt. Scene IDs/output target do not enter the key.',cache_miss_is_not_safe_for_reuse:'Stage.generate can submit a new provider job on a cache miss. Therefore equal planned keys alone are insufficient; a missing, changed or mismatched live cache entry/file stops the pair before the teaser CLI command.',judge_scope:'Each narration scene still needs its own official judge result; request equality does not share or replace either acceptance.'},
  pairs,
  production_handoff:{
    preconditions:[
      'New exact source/visual and fresh narrative reviews, owner outline/script approval, true production admission and whole-film quote are still required. Nothing here starts paid work.',
      'Read actual model/provider/version, size, look, prompt budget, cast/style-reference SHA, correction list and seed from the admitted execution context. Recompute both live Stage.imageKey values using those actual identical inputs; the example tuple above is not backend readback.',
      'Keep the pair in one unchanged project/workdir and serialize its operations. Do not run another writer, retake, cache cleaner or competing generation between preflight and reuse.',
    ],
    per_pair_sequence:pairs.map(p=>({
      asset_plan_id:p.asset_plan_id,
      first:{purpose:'Only after normal admission: generate payoff once, then independently judge that scene.',argv:cli(p.payoff_scene_id),require:'That exact first take must pass and remain selected. Record the real cache key, source file path, bytes/SHA, job and ledger receipt; no retake/correction or second seed.'},
      before_second_command_required:{executed:false,live_cache_read:'Immediately before invoking the teaser, read readCache(projectWorkdir).entries[recomputedLiveKey] and the real entry.file under that workdir.',require_all:['Both recomputed live keys are equal and match the accepted payoff first-take key.','The cache entry exists and its file still exists. Read and SHA256 the actual file bytes; require equality with cache entry.sha256 and the recorded accepted payoff source-file SHA.','Resolve the actual source file path and require it is the very file registered for that accepted payoff request; no substitute, expired entry, unsupported alias or unresolved path.','The source scene still selects that accepted first take; model/version/references/size/seed/correction and cache state have not changed.'],on_any_failure:'STOP BEFORE THE TEASER COMMAND. A cache miss is not permission to generate; restore/reconcile the legitimately accepted shared asset through the normal owner-approved route, never buy a similar second image.'},
      second:{purpose:'Invoke only after the live-cache byte/SHA preflight passes; this must reuse the existing source file.',argv:cli(p.setup_scene_id),require:'Preserve actual reused=true cache/job receipts and apply the teaser scene official judge. If reuse is absent or either scene needs a retake, stop the pair.'},
    })),
    on_any_failure_or_changed_request:'Stop the pair. Do not change only one endpoint, reroll a seed, buy an independently corrected look-alike, use --force/--accept-best, or hand-edit a manifest. If a factual/style correction is necessary, update both ends and repeat the normal exact-bound source/visual and admitted production process within existing account/take caps.',
    actual_verification_required:[
      'Read the real official keyframes manifest only after both scene judges. Require both final selected references to resolve to the identical file, then SHA256 its actual bytes; preserve each actual assignment and verdict.',
      'If either source is trimmed, verify both final selections and assembly inputs use the same derived file and actual SHA. Equality of pre-trim source hashes is insufficient.',
      'Preserve real generation, cache-hit, judge, trim, selected-manifest, assembly and ledger receipts and confirm no duplicate teaser image purchase.',
      'Until those actual checks pass, every file/SHA and actual_same_asset_verified stays null/false. Matching prompt/key or a written plan is not generated-image acceptance or media QA.',
    ],executed:false,
  },provider_calls:0,paid_calls:0,
};
fs.writeFileSync(path.join(OUT,'image-reuse-plan.json'),JSON.stringify(plan,null,2)+'\n');
console.log(JSON.stringify({pairs:pairs.length,keys:pairs.map(p=>p.native_same_input_key_rehearsal.native_stage_key),actual_same_asset_verified:false,paid_calls:0}));
