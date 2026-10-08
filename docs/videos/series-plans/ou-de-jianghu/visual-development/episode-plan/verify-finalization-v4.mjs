#!/usr/bin/env node
// Bounded offline v4: correct two prompt contradictions without changing source e001 or v3.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {pathToFileURL,fileURLToPath} from 'node:url';
const root=process.cwd(),here=path.dirname(fileURLToPath(import.meta.url));
const base=path.resolve(process.argv[2]||'');
const presentation=path.resolve(process.argv[3]||'');
const out=path.resolve(process.argv[4]||'');
if(process.argv.length<5||new Set([base,presentation,out]).size!==3)throw Error('Usage: node verify-finalization-v4.mjs <v3> <v3.1> <new-v4>');
if(fs.existsSync(out)&&fs.readdirSync(out).length)throw Error('Output must be absent or empty; never overwrite a prior review');
const sha=b=>createHash('sha256').update(b).digest('hex');
const read=(dir,n)=>JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'));
const json=(n,v)=>fs.writeFileSync(path.join(out,n),JSON.stringify(v,null,2)+'\n');
const oldVideo=fs.readFileSync(path.join(base,'video.json'));
assert.equal(sha(oldVideo),'7f7676d1ce39a6f9dbbdc4cacc5bc8cb39b9979e66e4a906213d2ea4235014df');
const oldHtml=fs.readFileSync(path.join(presentation,'animatic.html'),'utf8');
assert.equal(sha(oldHtml),'6cb27db81797e35d7dc42c62e7c5d71ff6c69d4a9839d93a32e35bb7f0153a0e');
const doc=JSON.parse(oldVideo),old=structuredClone(doc),edits=[];
for(const edit of [
 {id:'a04-s038',from:"Bao's open left palm",to:"Bao's open right palm",reason:'a04-s037 already shows Bao right palm; fix left/right typo without adding a transfer'},
 {id:'a03-s086',from:'head and upper torso stay in the frame with the complete crown.',to:'head and upper torso stay in the frame.',reason:'Uncrowned after a03-s085; remove generic crown clause, preserve explicit without-crown body'}
]){
 const s=doc.scenes.find(s=>s.id===edit.id);assert.equal(s.data.prompt.split(edit.from).length,2);
 const before=s.data.prompt;s.data.prompt=before.replace(edit.from,edit.to);
 edits.push({...edit,before,after:s.data.prompt,kind:'prompt_consistency_correction'});
}
const paths=[];
function diff(a,b,p=''){if(JSON.stringify(a)===JSON.stringify(b))return;if(a&&b&&typeof a==='object'&&typeof b==='object'){for(const k of new Set([...Object.keys(a),...Object.keys(b)]))diff(a[k],b[k],p+'/'+k);}else paths.push(p);}
diff(old,doc);assert.equal(paths.length,2);assert(paths.every(p=>/^\/scenes\/\d+\/data\/prompt$/.test(p)));
const stableProjection=d=>d.scenes.map(s=>({id:s.id,lines:s.lines,action_seconds:s.action_seconds,camera:s.data?.camera,motion:s.data?.motion,source:s.data?.source,visual:s.data?.visual,end_frame:s.data?.end_frame}));
assert.deepEqual(stableProjection(old),stableProjection(doc));
fs.mkdirSync(out,{recursive:true});
for(const n of ['series.json','brief.md','dictionary.json'])if(fs.existsSync(path.join(base,n)))fs.copyFileSync(path.join(base,n),path.join(out,n));
json('video.json',doc);
const oldReceipt=read(base,'proposal-receipt.json'),flags={...oldReceipt.flags,series:read(base,'series.json')};
const {planEpisode,renderMarkdown,renderCsv}=await import(pathToFileURL(path.join(root,'.agents/skills/animation-preproduction/scripts/shot_plan.mjs')));
const plan=planEpisode(doc,flags),previous=read(base,'shot-plan.json');
assert.deepEqual(plan.counts,previous.counts);
assert.deepEqual(plan.totals,previous.totals);
assert.deepEqual(plan.shots.map(s=>[s.id,s.need_s,s.buy_s,s.cost,s.risk.grade]),previous.shots.map(s=>[s.id,s.need_s,s.buy_s,s.cost,s.risk.grade]));
json('shot-plan.json',plan);fs.writeFileSync(path.join(out,'shot-plan.md'),renderMarkdown(plan,'proposal-v4/video.json'));fs.writeFileSync(path.join(out,'shot-plan.csv'),renderCsv(plan));
const camera=read(base,'camera-ledger.json');for(const e of edits)camera.rows.find(s=>s.id===e.id).first_frame=e.after;
json('camera-ledger.json',camera);json('risk-ledger.json',read(base,'risk-ledger.json'));json('proposal-edits.json',[...read(base,'proposal-edits.json'),...edits]);
const receipt={...oldReceipt,version:'v4',created_at:new Date().toISOString(),video_sha256:sha(fs.readFileSync(path.join(out,'video.json'))),parent_video_sha256:sha(oldVideo),builder_sha256:sha(fs.readFileSync(new URL(import.meta.url))),finalization_edits:edits,diff_paths:paths,dialogue_and_duration_unchanged:true,source_files_still_match:Object.entries(oldReceipt.source_sha256).every(([f,h])=>sha(fs.readFileSync(path.join(root,f)))===h)};
assert(receipt.source_files_still_match);json('proposal-receipt.json',receipt);
const results=[];
function run(name,args){const start=new Date().toISOString();const r=spawnSync(process.execPath,args,{cwd:root,encoding:'utf8',windowsHide:true,maxBuffer:50*1024*1024});if(r.error)throw r.error;fs.writeFileSync(path.join(out,name+'.stdout'),r.stdout||'');fs.writeFileSync(path.join(out,name+'.stderr'),r.stderr||'');results.push({name,args:args.map(a=>a.startsWith(out)?'<V4>'+a.slice(out.length):a),exit_code:r.status,started_at:start,finished_at:new Date().toISOString(),stdout_file:name+'.stdout',stderr_file:name+'.stderr'});console.log(name+': exit '+r.status);return r.status;}
const repoHere=path.relative(root,here).split(path.sep).join('/');
assert.equal(run('render',[repoHere+'/render-proposal.mjs',out]),0);
assert.equal(run('budget',[repoHere+'/budget-and-batches.mjs',out]),0);
const budget=read(out,'budget-and-batches.json'),oldBudget=read(base,'budget-and-batches.json');
const withoutBinding=({source_video_sha256,...rest})=>rest;assert.deepEqual(withoutBinding(budget),withoutBinding(oldBudget));
const scenes=read(out,'animatic-scenes.json');assert.deepEqual(scenes,read(base,'animatic-scenes.json'));
fs.copyFileSync(path.join(out,'animatic.html'),path.join(out,'animatic-base.html'));
const frameText=Object.fromEntries(doc.scenes.filter(s=>s.template==='shot').map(s=>[s.id,{first:s.data.prompt,end:s.data.end_frame?.prompt||null}]));
let html=oldHtml.replaceAll('｜v3.1 卡面補充（沿用v3時間）','｜v4 一致性修訂（沿用v3時間）');
const frameToken=/const frameText=.*?;\r?\nfunction frameMarkup/s;
assert(frameToken.test(html));html=html.replace(frameToken,'const frameText='+JSON.stringify(frameText).replace(/</g,'\\u003c')+';\nfunction frameMarkup');
fs.writeFileSync(path.join(out,'animatic.html'),html);json('frame-text.json',frameText);
const cliFlags=['--route','hailuo','--plan','hailuo:max','--hailuo-model','h3','--resolution','2k','--handle','0.5','--clip-takes','2','--expected-takes','1.2,1.5,2','--pilot','a02-s035,a02-s036,a02-s037'];
const video=path.join(out,'video.json');
run('lint',['tools/video/cli.mjs','lint','--file',video,'--json']);
run('craft',['.agents/skills/youtube-video/scripts/drama_craft_check.mjs',video,'--strict','--json']);
run('reading',['.agents/skills/animation-camera/scripts/shot_reading.mjs',video,'--route','hailuo','--strict','--json']);
run('plan-strict',['.agents/skills/animation-preproduction/scripts/shot_plan.mjs',video,'--workdir',out,...cliFlags,'--json','--strict']);
run('ready',['.agents/skills/animation-preproduction/scripts/plan_lock.mjs','--file',video,'--workdir',out,...cliFlags,'--ready','--json']);
assert.equal(results.find(r=>r.name==='lint').exit_code,0);assert.equal(results.find(r=>r.name==='reading').exit_code,0);
const hashes=Object.fromEntries(['video.json','animatic.html','frame-text.json','animatic-scenes.json','shot-plan.json','camera-ledger.json','risk-ledger.json','proposal-edits.json','budget-and-batches.json','proposal-receipt.json'].map(n=>[n,sha(fs.readFileSync(path.join(out,n)))]));
const verification={version:'v4',created_at:new Date().toISOString(),offline_only:true,parent_v3_video_sha256:sha(oldVideo),parent_v31_html_sha256:sha(oldHtml),changes:edits,diff_paths:paths,dialogue_motion_camera_duration_unchanged:true,scene_rows:scenes.length,shot_rows:plan.counts.shots,exact_seconds:scenes.at(-1).end,budget_numerics_and_batches_unchanged:true,plan_counts_risk_cost_timing_unchanged:true,frame_text_count:Object.keys(frameText).length,results,sha256:hashes,no_lock_written:!fs.existsSync(path.join(out,'plan/lock.json')),no_full_length_v4_watch_claimed:true,actual_browser_targeted_review:'pending',parent_v3_unchanged:sha(fs.readFileSync(path.join(base,'video.json')))===sha(oldVideo),parent_v31_unchanged:sha(fs.readFileSync(path.join(presentation,'animatic.html')))===sha(oldHtml),source_files_match:receipt.source_files_still_match,historical_pending_staging:'Existing staging was created with v3; not silently rebound to v4.'};
json('verification.json',verification);
const summary={...verification,external_artifact_directory:'<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261009-v4',source_sha256:oldReceipt.source_sha256,owner_accepted:false,plan_locked:false};
fs.writeFileSync(path.join(here,'finalization-v4-verification.json'),JSON.stringify(summary,null,2)+'\n');
console.log(JSON.stringify({out,video_sha256:hashes['video.json'],html_sha256:hashes['animatic.html'],diff_paths:paths,results:results.map(r=>({name:r.name,exit:r.exit_code})),seconds:verification.exact_seconds,budget_unchanged:true},null,2));
