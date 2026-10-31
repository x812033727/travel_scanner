// Pure Stage.imageKey rehearsal. Does not read credentials, fetch status or call Stage.image.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { resolveLook } from '../../../../tools/video/core/drama.mjs';
import { shotPrompt } from '../../../../tools/video/media/keyframes.mjs';
import { Stage } from '../../../../tools/video/media/stages.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const hash=file=>createHash('sha256').update(fs.readFileSync(path.join(here,file))).digest('hex');
const doc=JSON.parse(fs.readFileSync(path.join(here,'video.json')));
const idx=JSON.parse(fs.readFileSync(path.join(here,'row-index-r1.json')));
const payoff=idx.scenes_by_row.b08;
const teaser=idx.scenes_by_row.h04;
const sceneIds=[...payoff,...teaser];
const look=resolveLook(doc.look);
const status={image:{provider:'minimax',model:'image-01'}};
const mediaBase='/workspace/work/brand-story-20261025/doraemon-audit/author-r4/media';
const runtime='/workspace/work/brand-story-20261025/doraemon-audit/author-r4/free-runtime';
const stage=new Stage({slug:doc.slug,workdir:path.join(mediaBase,doc.slug),options:{},status,stage:'keyframes',imageVersion:1,format:doc.format});
const requests=sceneIds.map(id=>{
  const scene=doc.scenes.find(s=>s.id===id);
  const prompt=shotPrompt(scene,look,[]);
  return {scene_id:id,line_ids:scene.lines.map(l=>l.id),raw_prompt:scene.data.prompt,camera:scene.data.camera,look:doc.look,resolved_look:look,cast:[],correction_list:[],prompt,negative:look.negative,references:[],seed:1,provider:'minimax',model:'image-01',image_selection_version:1,
    keys:[{size:null,dimensions:{width:1920,height:1080},key:stage.imageKey({prompt,negative:look.negative,references:[],seed:1,size:null})},{size:'2K',dimensions:{width:2048,height:1152},key:stage.imageKey({prompt,negative:look.negative,references:[],seed:1,size:'2K'})}]};
});
for(const request of requests){
  if(request.prompt!==requests[0].prompt || request.camera!==requests[0].camera || JSON.stringify(request.keys)!==JSON.stringify(requests[0].keys))throw new Error('Full native request/key equality lost; stop and reconcile.');
}
const core=Object.fromEntries(['video.json','script.md','narration-only.json','claims.json'].map(name=>[name,hash(name)]));
const plan={schema_version:1,revision:'doraemon-r4',role:'AUTHOR_PLAN_NOT_MANIFEST_APPROVAL_OR_CACHE_PROOF',slug:doc.slug,pure_local_stage_imagekey_only:true,backend_settings_read_back:false,live_cache_read:false,actual_same_asset_verified:false,actual_generated_media:0,core_four_sha256:core,
  forward_event_teasers:1,pairs:[{id:'science-magazines-before-story-entry',source_scene_id:payoff[0],source_additional_same_request_scenes:payoff.slice(1),reuse_scene_ids:teaser,requests,all_declared_full_native_keys_equal:true,
    teaser_stops_before_result:'Neutral magazine-opening action; no kingdom, adventure outcome, original character or signature prop is pictured. The story-entry answer is later in c01.',
    actual_source_file:null,actual_source_sha256:null,actual_reused_file:null,actual_reused_sha256:null,actual_same_asset_verified:false,
    ordinary_command_recipe:sceneIds.map((id,i)=>({stage:i===0?'Generate/payoff first only after all admission and review gates':'Require exact live cache hit and accepted actual file SHA BEFORE this command; miss means STOP',argv:['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',runtime,'keyframes','--slug',doc.slug,'--workdir',mediaBase,'--shot',id,'--takes','1']}))}],
  preconditions:['Exact-new-slug US$25 account, all-film quote and protected admission have not been created; no paid step is authorized by this plan.','Independent source/written visual, two fresh native readers, pronunciation, actual voice and owner gates remain pending.','Read actual provider/model/size/image version/seed/references/cast/look/camera/composed prompt/fixes before production. Declared 1K and2K keys are planned alternatives, not live settings. Recompute from final reviewed source and stop on any mismatch.','Generate and accept the first payoff scene with one take. For every other payoff segment and the teaser, require the same live key to point to that accepted file with exact on-disk SHA; cache miss, changed request or file means STOP before any dispatch.'],
  same_asset_acceptance:['Each scene receives its own official judge against its own text; a shared key never transfers a verdict.','Both source/payoff segments and teaser select the same accepted actual file SHA in the official manifest.','After any crop/margin trim, compare the actual selected derived files too; original-source equality alone is insufficient.','Assembly must reference those same selected bytes; reconcile any retake, changed crop, new correction or selection across all ends.','Never hand-edit a manifest, write an alias schema field, buy another similar picture, silently reroll or bypass a failed judge.'],
  original_opening_scene_note:'h02/h03 is the chronological manuscript starting scene, not a second forward event teaser.',paid_calls:0,backend_calls:0,approvals_created:0};
fs.writeFileSync(path.join(here,'image-reuse-plan.json'),JSON.stringify(plan,null,2)+'\n');
console.log(JSON.stringify({requests:requests.length,full_keys_equal:true,key_1k:requests[0].keys[0].key,key_2k:requests[0].keys[1].key,actual_same_asset_verified:false}));
