// Offline phase probe. The copied modules must match the staged production bytes.
// No real model, account, host, or network call is possible in this harness.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {assertTurn104,assertOnlyTurnDrop,assertListenerSavedExact,assertVerifierClaimsExact,assertSavedVerifierClaimsExact,assertModelEventScope,assertRound12Tip,retireT19,assertManualAutoChange,scopedStop,retryPendingSameSource} from './review-round12-core.mjs';

const snapshot=process.env.A01_SNAPSHOT104_ROOT;
const donor=process.env.A01_PINNED_RUNTIME_ROOT;
if(!snapshot&&!donor)test('round-12 pinned donor checks', {skip:'external snapshot and pinned runtime are unavailable'},()=>{});
else{
if(!snapshot||!donor)throw Error('Set both A01_SNAPSHOT104_ROOT and A01_PINNED_RUNTIME_ROOT');
const slug='story-rolling-suitcase-v2';
const source104='e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7';
const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../../../../..');
const required=JSON.parse(fs.readFileSync(new URL('./required-runtime.json',import.meta.url)));
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const json=value=>Buffer.from(JSON.stringify(value,null,2)+'\n');
const hashFile=file=>fs.existsSync(file)?sha(fs.readFileSync(file)):null;
const read=file=>JSON.parse(fs.readFileSync(file));

function sandbox(){
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'a01-round12-donor-'));
 const root=path.join(temp,'runtime'),workBase=path.join(temp,'work');
 fs.mkdirSync(root,{recursive:true});fs.mkdirSync(workBase);
 fs.cpSync(path.join(donor,'tools/video'),path.join(root,'tools/video'),{recursive:true});
 fs.symlinkSync(path.join(repo,'node_modules'),path.join(root,'node_modules'),'junction');
 fs.cpSync(path.join(snapshot,'docs'),path.join(root,'docs'),{recursive:true});
 fs.cpSync(path.join(snapshot,slug),path.join(workBase,slug),{recursive:true});
 fs.writeFileSync(path.join(workBase,slug,'STOP'),'offline guard\n');
 fs.mkdirSync(path.join(workBase,slug,'run-receipts'),{recursive:true});
 for(const [rel,wanted] of Object.entries(required))assert.equal(hashFile(path.join(root,rel)),wanted,`pinned runtime ${rel}`);
 const workdir=path.join(workBase,slug),doc=path.join(root,'docs/videos',slug);
 return {temp,root,workBase,workdir,doc,stop:path.join(workdir,'STOP'),turn:path.join(workdir,'story/chapters/turn.json')};
}

async function setup(){
 const box=sandbox();
 const [{Automation},{advanceStory,storyBrief},{readStoryLexicon}]=await Promise.all([
  import(pathToFileURL(path.join(box.root,'tools/video/automation/flow.mjs'))),
  import(pathToFileURL(path.join(box.root,'tools/video/automation/story.mjs'))),
  import(pathToFileURL(path.join(box.root,'tools/video/core/story-lexicon.mjs'))),
 ]);
 const series=read(path.join(box.doc,'series.json'));
 fs.writeFileSync(path.join(box.doc,'brief.md'),storyBrief({episode:{title:series.title,logline:series.logline},plan:series.plan,cast:series.characters??[],look:series.look}));
 const originalVideo=read(path.join(box.doc,'video.json'));
 const settings={enabled:true,durable_stage_runs:true,drama:{drama_voice:originalVideo.voice,music_enabled:Boolean(originalVideo.music),drama_max_verify_rounds:4}};
 let mode='normal',stageCalls=[],keys=new Map(),adopted=0,settled=0;
 const requestFile=key=>path.join(box.workdir,'run-receipts',key+'.json');
 const api={
  async run(stage,requestedSlug,instructions,payload,maxTokens,format,variant){
   assert.equal(requestedSlug,slug);assert.equal(format,'drama');assert.ok(instructions.length>0);assert.ok(maxTokens>0);
   const request={stage,slug:requestedSlug,variant,payload};
   const key=sha(JSON.stringify(request));
   const identity=stage+':'+variant;
   if(keys.has(identity))assert.equal(key,keys.get(identity),'a pending stage must reuse its request key');
   else keys.set(identity,key);
   stageCalls.push({stage,variant,key});
   const file=requestFile(key);fs.mkdirSync(path.dirname(file),{recursive:true});
   const record=fs.existsSync(file)?read(file):{request_key:key,request,receipt:{status:'running'}};
   fs.writeFileSync(file,json(record));
   if(mode==='pending'&&stageCalls.filter(row=>row.key===key).length===1)throw Object.assign(Error('pending'),{code:'video_ai_run_pending'});
   if(mode==='uncertain'){
    record.receipt.status='uncertain';fs.writeFileSync(file,json(record));
    throw Object.assign(Error('uncertain'),{code:'video_ai_run_uncertain'});
   }
   let answer;
   if(stage==='listener'&&variant==='story')answer={patch:{},drop:['6i8x']};
   else if(stage==='verifier'&&variant==='story')answer={patch:{},drop:[],claims:read(box.turn).claims.map(row=>({...row,verdict:row.verdict==='UNCHECKED'?'CONFIRMED':row.verdict??'CONFIRMED'})),report:'離線固定回答：逐列核對，來源與事實欄位保持原樣。'};
   else if(stage==='verifier'&&variant==='narrative'){
    const line=read(path.join(box.doc,'video.json')).scenes.flatMap(scene=>scene.lines??[])[0];
    const prior=read(path.join(box.workdir,'review/narrative.json'));
    answer={answers:prior.answers.map(row=>({id:row.id,yes:true,evidence:`[${line.id}] ${line.text}`}))};
   }else throw Error('UNEXPECTED_STAGE_'+identity);
   record.receipt.status='succeeded';record.receipt.answer=answer;fs.writeFileSync(file,json(record));
   return {model:'offline-deterministic',input_tokens:1,output_tokens:1,usage:{tokens:2,token_budget:100},text:JSON.stringify(answer)};
  },
  async adoptRuns(_,proof){
   const names=fs.readdirSync(path.join(box.workdir,'run-receipts'));
   assert.equal(names.length,1);
   for(const artifact of proof.artifacts)assert.equal(hashFile(artifact.path),artifact.sha256);
   const file=path.join(box.workdir,'run-receipts',names[0]),record=read(file);
   assert.equal(record.receipt.status,'succeeded');record.adopted=true;fs.writeFileSync(file,json(record));adopted++;
  },
  async settleRuns(){
   const names=fs.readdirSync(path.join(box.workdir,'run-receipts'));
   assert.equal(names.length,1);assert.equal(read(path.join(box.workdir,'run-receipts',names[0])).adopted,true);
   fs.unlinkSync(path.join(box.workdir,'run-receipts',names[0]));settled++;
  },
 };
 const ctx={root:box.root,env:{VIDEO_WORKDIR:box.workBase},now:()=>new Date('2026-10-17T08:00:00.000Z'),stdout:{write(){}},stderr:{write(){}},fetch:async()=>({ok:false,status:404,text:async()=>''}),sleep:async()=>{},EXIT:{ok:0,lint:1,usage:2,owner:3,external:4,missing:5,incomplete:6}};
 const automation=new Automation(ctx,api,settings);
 automation.leases.set(slug,{verify(){}});automation.runSlugs=new Set();automation.reference=()=>({script_writing:'offline pinned stage test'});
 automation.reportBlocked=async()=>true;
 const actualStage=automation.stage.bind(automation);
 automation.stage=async(stage,requestedSlug,payload,tokens,format,variant,...rest)=>{
  const answer=await actualStage(stage,requestedSlug,payload,tokens,format,variant,...rest);
  if(stage==='listener')assertOnlyTurnDrop(answer);
  if(stage==='verifier'&&variant==='story'){
   assert.deepEqual(answer.patch,{});assert.deepEqual(answer.drop,[]);
   assertVerifierClaimsExact(read(box.turn),answer);
  }
  return answer;
 };
 function sources(){
  const chapterDir=path.join(box.workdir,'story/chapters');
  return {auto:hashFile(path.join(box.workdir,'auto.json')),video:hashFile(path.join(box.doc,'video.json')),series:hashFile(path.join(box.doc,'series.json')),claims:hashFile(path.join(box.doc,'claims.md')),script:hashFile(path.join(box.doc,'script.md')),lexicon:readStoryLexicon({slug,storyDir:box.doc,sharedFile:path.join(box.root,'docs/videos/lexicon.json')}).lexicon_sha256,narrative:hashFile(path.join(box.workdir,'review/narrative.json')),pilot:hashFile(path.join(box.workdir,'story/reviews/script-review.json')),verify:hashFile(path.join(box.doc,'verify-1.md')),chapters:Object.fromEntries(['hook','origin','idea','engine','turn','now'].map(key=>[key,hashFile(path.join(chapterDir,key+'.json'))]))};
 }
 const source=()=>sha(JSON.stringify(sources()));
 function guard(run){
  const stopped=scopedStop(box.stop),original=fs.readFileSync(box.stop);stopped.remove();
  return Promise.resolve().then(run).finally(()=>{stopped.restore();assert.deepEqual(fs.readFileSync(box.stop),original);});
 }
 function journal(){const names=fs.readdirSync(path.join(box.workdir,'run-receipts'));assert.equal(names.length,1);return path.join(box.workdir,'run-receipts',names[0]);}
 async function commit(kind,before,beforeTurn){
  const after=sources();assertModelEventScope(kind,before,after);
  if(kind==='listener_drop')assertListenerSavedExact(readFromBytes(beforeTurn),read(box.turn));
  if(kind==='turn_verifier')assertSavedVerifierClaimsExact(readFromBytes(beforeTurn),read(box.turn));
  const file=journal();assert.equal(read(file).receipt.status,'succeeded');
  const artifacts=[box.turn,path.join(box.workdir,'auto.json'),path.join(box.doc,'video.json')].map(file=>({path:file,sha256:hashFile(file)}));
  await api.adoptRuns(slug,{artifacts});
  const next=source();assert.notEqual(next,sha(JSON.stringify(before)));
  await api.settleRuns([slug]);automation.runSlugs.clear();
  return next;
 }
 return {box,api,automation,advanceStory,sources,source,guard,commit,journal,get mode(){return mode},set mode(value){mode=value},get stageCalls(){return stageCalls},get adopted(){return adopted},get settled(){return settled}};
}
const readFromBytes=bytes=>JSON.parse(bytes);

test('pinned production story/flow/lexicon hashes run four persisted round-12 phases without media',async()=>{
 const h=await setup();
 try{
  const {box,automation,advanceStory}=h;
  const baseline=fs.readFileSync(box.turn),state=read(path.join(box.workdir,'auto.json'));
  assertTurn104(readFromBytes(baseline));assert.equal(h.source(),source104);
  const edges=[];
  const append=(before,after)=>{edges.push({before_source_sha256:before,after_source_sha256:after});assertRound12Tip({links:104+edges.length,source:after,events:edges,source104});};
  let before=h.source();
  await h.guard(async()=>{
   const tuple=h.sources();state.story.chapters.turn.listened=false;state.listener_done=false;
   state.story.owner_note='僅刪 turn-08 的 6i8x';
   h.mode='pending';
   const message=await retryPendingSameSource(()=>advanceStory(automation,state,'verified'),{pendingCode:'video_ai_run_pending',source:h.source,expected:before,maxPolls:2,delay:async()=>{}});
   assert.match(message,/heard/);assert.equal(state.story.chapters.turn.listened,true);
   assertListenerSavedExact(readFromBytes(baseline),read(box.turn));
   await h.commit('listener_drop',tuple,baseline);
  });
  append(before,h.source());assert.equal(h.stageCalls.filter(row=>row.stage==='listener').length,2);
  assert.equal(new Set(h.stageCalls.filter(row=>row.stage==='listener').map(row=>row.key)).size,1);
  before=h.source();
  await h.guard(async()=>{
   const beforeAuto=read(path.join(box.workdir,'auto.json'));
   const cut=read(box.turn);fs.writeFileSync(box.turn,json(retireT19(cut)));
   state.story.chapters.turn.checked=false;state.verified=false;
   const message=await advanceStory(automation,state,'script passes lint');
   assert.match(message,/passes lint/);assertManualAutoChange(beforeAuto,read(path.join(box.workdir,'auto.json')));
   assert.equal(read(box.turn).claims.some(row=>row.id==='t19'),false);
   assert.equal(fs.readdirSync(path.join(box.workdir,'run-receipts')).length,0);
  });
  append(before,h.source());
  before=h.source();
  await h.guard(async()=>{
   const tuple=h.sources(),prior=fs.readFileSync(box.turn);h.mode='pending';
   const message=await retryPendingSameSource(()=>advanceStory(automation,state,'verified'),{pendingCode:'video_ai_run_pending',source:h.source,expected:before,maxPolls:2,delay:async()=>{}});assert.match(message,/checked \(round 4\)/);
   assert.equal(state.story.chapters.turn.check_rounds,4);
   assert.match(read(box.turn).report,/^### 第 4 輪\n\n/);
   await h.commit('turn_verifier',tuple,prior);
  });
  append(before,h.source());
  before=h.source();
  await h.guard(async()=>{
   const tuple=h.sources();
   const message=await retryPendingSameSource(()=>advanceStory(automation,state,'verified'),{pendingCode:'video_ai_run_pending',source:h.source,expected:before,maxPolls:2,delay:async()=>{}});
   assert.equal(state.story.narrative.rounds,12);
   assert.ok(['pilot_script_review','prompt_fixes:narrative'].includes(state.blocked_kind));
   assert.match(message,/blocked|panel/);
   await h.commit('narrative_panel',tuple);
  });
  append(before,h.source());
  assert.equal(h.adopted,3);assert.equal(h.settled,3);
  assert.deepEqual(h.stageCalls.map(row=>row.stage+':'+row.variant),['listener:story','listener:story','verifier:story','verifier:story','verifier:narrative','verifier:narrative']);
  assert.equal(fs.readdirSync(path.join(box.workdir,'run-receipts')).length,0);
  assert.equal(fs.existsSync(path.join(box.workdir,'story/reviews/script-review.json')),false);
  console.log(JSON.stringify({event:'A01_PINNED_DONOR_FOUR_PHASE_PASS',links:108,source_sha256:h.source(),stage_calls:h.stageCalls.length,unique_request_keys:new Set(h.stageCalls.map(row=>row.key)).size,adopted:h.adopted,settled:h.settled,blocked_kind:state.blocked_kind}));
 }finally{fs.rmSync(h.box.temp,{recursive:true,force:true});}
});

test('pinned donor uncertain listener leaves journal, no adopted link, and restores STOP',async()=>{
 const h=await setup();
 try{
  const before=h.source(),state=read(path.join(h.box.workdir,'auto.json'));
  assert.equal(before,source104);h.mode='uncertain';state.story.chapters.turn.listened=false;state.listener_done=false;
  await assert.rejects(()=>h.guard(()=>h.advanceStory(h.automation,state,'verified')),/uncertain/);
  assert.equal(h.source(),before);assert.equal(read(h.journal()).receipt.status,'uncertain');
  assert.equal(h.adopted,0);assert.equal(h.settled,0);
  assert.equal(fs.existsSync(h.box.stop),true);
  console.log(JSON.stringify({event:'A01_PINNED_DONOR_UNCERTAIN_HELD',source_sha256:h.source(),journal_status:'uncertain',adopted:h.adopted}));
 }finally{fs.rmSync(h.box.temp,{recursive:true,force:true});}
});

async function prepareForUncertain(h,target){
 const {box,automation,advanceStory}=h,state=read(path.join(box.workdir,'auto.json'));
 const baseline=fs.readFileSync(box.turn);
 await h.guard(async()=>{
  const tuple=h.sources();state.story.chapters.turn.listened=false;state.listener_done=false;
  state.story.owner_note='僅刪 turn-08 的 6i8x';
  await advanceStory(automation,state,'verified');await h.commit('listener_drop',tuple,baseline);
 });
 await h.guard(async()=>{
  fs.writeFileSync(box.turn,json(retireT19(read(box.turn))));
  state.story.chapters.turn.checked=false;state.verified=false;
  assert.match(await advanceStory(automation,state,'script passes lint'),/passes lint/);
 });
 if(target==='panel')await h.guard(async()=>{
  const tuple=h.sources(),prior=fs.readFileSync(box.turn);
  await advanceStory(automation,state,'verified');await h.commit('turn_verifier',tuple,prior);
 });
 return state;
}

for(const target of ['facts','panel'])test(`pinned donor uncertain ${target} holds prior tip, journal, and STOP`,async()=>{
 const h=await setup();
 try{
  const state=await prepareForUncertain(h,target),before=h.source(),previousAdoptions=h.adopted;
  h.mode='uncertain';
  await assert.rejects(()=>h.guard(()=>h.advanceStory(h.automation,state,'verified')),/uncertain/);
  assert.equal(h.source(),before);assert.equal(read(h.journal()).receipt.status,'uncertain');
  assert.equal(h.adopted,previousAdoptions);assert.equal(h.settled,previousAdoptions);
  assert.equal(fs.existsSync(h.box.stop),true);
  console.log(JSON.stringify({event:'A01_PINNED_DONOR_UNCERTAIN_HELD',phase:target,source_sha256:before,journal_status:'uncertain',adopted:h.adopted}));
 }finally{fs.rmSync(h.box.temp,{recursive:true,force:true});}
});
}
