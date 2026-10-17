// A01 only: run the installed worker's real chapter checks and panel; never media or approval.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash,randomUUID} from 'node:crypto';
import {readStoryLexicon} from '/opt/mokaair/tools/video/core/story-lexicon.mjs';
import {Automation} from '/opt/mokaair/tools/video/automation/flow.mjs';
import {automationClient,RUN_PENDING} from '/opt/mokaair/tools/video/automation/client.mjs';
import {advanceStory,readChapterAnswer} from '/opt/mokaair/tools/video/automation/story.mjs';
import {acquireProjectLease} from '/opt/mokaair/tools/video/core/project-lease.mjs';
import {captureAdoptionSources} from './adopt-pinned.mjs';
import {inspectReviewProgress} from './inspect-review-progress.mjs';
import {isDeepStrictEqual} from 'node:util';
const SLUG='story-rolling-suitcase-v2',root='/opt/mokaair',workBase='/var/lib/mokaair/video-work';
const workdir=path.join(workBase,SLUG),stop=path.join(workdir,'STOP');
const sha=b=>createHash('sha256').update(b).digest('hex');
function need(v,c){if(!v)throw Error(c);}
const payload=path.resolve(path.dirname(new URL(import.meta.url).pathname),'../../../../..');
const options={before80Root:payload+'/before80',before81Root:payload+'/before-81',oldLexiconFile:payload+'/old-lexicon.json',reviewBytes:fs.readFileSync(payload+'/revision-review.json'),receiptBytes:fs.readFileSync(payload+'/revision-owner-record.json')};
need(!fs.existsSync(workBase+'/STOP'),'GLOBAL_STOP_PRESENT');
need(fs.lstatSync(stop).isFile()&&!fs.lstatSync(stop).isSymbolicLink(),'SCOPED_STOP_REQUIRED');
need(process.argv.length===3&&['--preflight','--run'].includes(process.argv[2]),'EXPLICIT_PREFLIGHT_OR_RUN_REQUIRED');
const stopBytes=fs.readFileSync(stop),stopSha=sha(stopBytes);
const lease=acquireProjectLease(workdir,{owner:'a01-bounded-real-review'});
let removed=false;
function restoreStop(){if(!removed)return;if(fs.existsSync(stop)){need(fs.readFileSync(stop).equals(stopBytes),'STOP_CHANGED');return;}const fd=fs.openSync(stop,'wx',0o600);try{fs.writeFileSync(fd,stopBytes);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}removed=false;}
for(const signal of ['SIGTERM','SIGINT'])process.once(signal,()=>{try{restoreStop();}finally{lease.release();process.exit(128);}});
try{
 const capture=fs.mkdtempSync(path.join(os.tmpdir(),'a01-pre-real-review-'));captureAdoptionSources({root,workBase,output:capture});
 const progress=inspectReviewProgress({...options,base82Root:payload+'/base82',progressRoot:capture});need(progress.links===97&&progress.source_sha256==='1628c8b6e948289e48d1dadc14a8e06b7066f3c3c704f780e909f98cedc4c376','REVIEW_SOURCE_DRIFT');const initial={new_pins:{source_composite_sha256:progress.source_sha256,install_receipt_sha256:'24110fc8cc1665e9f6830db23e57cde12640c4bd947af3a42a25602528a266fd'}};
 if(process.argv[2]==='--preflight'){console.log(JSON.stringify({event:'A01_REVIEW_PREFLIGHT_PASS',source_sha256:initial.new_pins.source_composite_sha256,stop_preserved:true,paid_calls:0}));}else{
 const ctx={root,env:process.env,stdout:process.stdout,stderr:process.stderr,now:()=>new Date(),EXIT:{ok:0,lint:1,usage:2,owner:3,external:4,missing:5,incomplete:6}};
 const api=automationClient(ctx,{attempts:1});const settings=await api.settings();need(settings.enabled===true,'AUTOMATION_DISABLED');need(settings.durable_stage_runs===true,'DURABLE_STAGE_RUNS_REQUIRED');
 const automation=new Automation(ctx,api,settings);automation.leases.set(SLUG,lease);automation.runSlugs=new Set();
 let didBlock=false;const actualBlock=automation.block.bind(automation);automation.block=async(...args)=>{didBlock=true;return actualBlock(...args);};
 let writerCalls=0;let calls=0;const actualStage=automation.stage.bind(automation);
 automation.stage=async(stage,slug,payload,tokens,format,variant,...rest)=>{
  need(slug===SLUG&&format==='drama'&&((variant==='story'&&['verifier','listener'].includes(stage))||(stage==='verifier'&&variant==='narrative')||(stage==='writer'&&variant==='story'&&payload.chapter?.key==='now')),'REVIEW_STAGE_OUTSIDE_SCOPE');
  need(++calls<=120,'REVIEW_CALL_BOUND');
  if(stage!=='writer')return actualStage(stage,slug,payload,tokens,format,variant,...rest);
  need(++writerCalls<=13,'WRITER_POLL_BOUND');
  const current=JSON.parse(fs.readFileSync(workdir+'/story/chapters/now.json'));const expected=structuredClone(current);
  const line=expected.scenes.find(s=>s.id==='now-01')?.lines.find(l=>l.id==='7asx');
  need(line?.text==='還有位置。1997 年，Samsonite 發表了平衡四輪直立箱，箱子從往後拉，變成站著推。','WRITER_SOURCE_LINE_DRIFT');
  line.text='還有位置。1997 年，Samsonite 發表了平衡四輪直立箱，箱子能站著推。';
  const narrowed={...payload,lint_errors:[...payload.lint_errors,'本次只修 now-01/7asx 的單鏡長度。請把這一句精確改成「'+line.text+'」。其他所有場景、ID、文字、提示詞、鏡頭、章名、loops 都原樣保留；不加新詞條。']};
  const answer=await actualStage(stage,slug,narrowed,tokens,format,variant,...rest);
  const info=JSON.parse(fs.readFileSync(root+'/docs/videos/'+SLUG+'/series.json'));
  const read=readChapterAnswer(answer,{key:'now',ids:current.scenes.flatMap(s=>s.lines.map(l=>l.id)),cast:info.characters??[],sources:info.plan.sources.length,facts:info.plan.must_verify.length});
  need(!read.problem&&!read.noMore&&isDeepStrictEqual(read.chapter.scenes,expected.scenes)&&read.chapter.title===current.title&&isDeepStrictEqual(read.chapter.loops??[],current.loops??[]),'WRITER_EDIT_OUTSIDE_APPROVED_LINE');
  need(Object.keys(read.lexicon??{}).length===0,'WRITER_LEXICON_ADDITIONS_REFUSED');
  return answer;
 };
 const state=JSON.parse(fs.readFileSync(workdir+'/auto.json'));
 need(state.slug===SLUG&&state.status==='blocked'&&state.blocked_kind==='prompt_fixes:narrative','REVIEW_STATE_DRIFT');
 need(sha(fs.readFileSync(stop))===stopSha,'STOP_CHANGED');fs.unlinkSync(stop);removed=true;
 console.log(JSON.stringify({event:'A01_REVIEW_BATCH_STARTED',initial_source:initial.new_pins.source_composite_sha256,paid_media_allowed:false}));
 const durable=(file,bytes)=>{fs.mkdirSync(path.dirname(file),{recursive:true});const fd=fs.openSync(file,'wx',0o600);try{fs.writeFileSync(fd,bytes);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}const d=fs.openSync(path.dirname(file),'r');try{fs.fsyncSync(d);}finally{fs.closeSync(d);}};
 const json=v=>Buffer.from(JSON.stringify(v,null,2)+'\n');
 const hashFile=(file,optional=false)=>{if(optional&&!fs.existsSync(file))return null;need(fs.lstatSync(file).isFile()&&!fs.lstatSync(file).isSymbolicLink(),'SOURCE_NOT_REGULAR');return sha(fs.readFileSync(file));};
 const sources=()=>({auto:hashFile(workdir+'/auto.json'),video:hashFile(root+'/docs/videos/'+SLUG+'/video.json'),series:hashFile(root+'/docs/videos/'+SLUG+'/series.json'),claims:hashFile(root+'/docs/videos/'+SLUG+'/claims.md'),script:hashFile(root+'/docs/videos/'+SLUG+'/script.md'),lexicon:readStoryLexicon({slug:SLUG,storyDir:root+'/docs/videos/'+SLUG,sharedFile:root+'/docs/videos/lexicon.json'}).lexicon_sha256,narrative:hashFile(workdir+'/review/narrative.json'),pilot:hashFile(workdir+'/story/reviews/script-review.json',true),verify:hashFile(root+'/docs/videos/'+SLUG+'/verify-1.md',true),chapters:Object.fromEntries(['hook','origin','idea','engine','turn','now'].map(k=>[k,hashFile(workdir+'/story/chapters/'+k+'.json')]))});
 const journalDir=workdir+'/run-receipts';
 const journals=()=>fs.existsSync(journalDir)?fs.readdirSync(journalDir).filter(n=>n.endsWith('.json')):[];
 need(journals().length===0,'EXISTING_ACTIVE_RUN_RECEIPT_REQUIRES_REVIEW');
 let expected=initial.new_pins.source_composite_sha256;
 for(let unit=0;unit<8;unit++){
  lease.verify();need(!fs.existsSync(stop),'NEW_STOP_PRESENT');
  const before=sources();need(sha(JSON.stringify(before))===expected,'RECHECK_SOURCE_CHAIN_DRIFT');
  const id=new Date().toISOString().replaceAll(':','-')+'-'+randomUUID();
  const runDir=workdir+'/story/recheck-runs/'+id;fs.mkdirSync(runDir,{recursive:true});
  const beforeCapture=runDir+'/before';fs.mkdirSync(beforeCapture);captureAdoptionSources({root,workBase,output:beforeCapture});
  durable(runDir+'/intent.json',json({schema_version:1,slug:SLUG,id,before_source_sha256:expected,owner_approval_ref:'current-chat/2026-10-17/user-request-complete-production-data-handoff-review-and-A01',stop_sha256:stopSha}));
  let message,polls=0;
  while(true){
   try{const fixes=state.story.chapters.now.lint_fixes;message=await advanceStory(automation,state,'verified');if(state.story.chapters.now.lint_fixes>fixes){state.story.chapters.now.checked=false;state.story.chapters.now.listened=false;state.verified=false;state.listener_done=false;automation.persist(state);}break;}
   catch(error){if(error.code===RUN_PENDING&&++polls<=12){console.log('A01 durable receipt pending; polling retained request');await new Promise(r=>setTimeout(r,5000));continue;}throw error;}
  }
  const after=sources(),afterHash=sha(JSON.stringify(after));need(afterHash!==expected,'NO_RECHECK_SOURCE_CHANGE');
  lease.verify();
  const artifacts=[workdir+'/auto.json',...['video.json','series.json','claims.md','script.md','verify-1.md'].map(n=>root+'/docs/videos/'+SLUG+'/'+n),workdir+'/review/narrative.json',...['hook','origin','idea','engine','turn','now'].map(k=>workdir+'/story/chapters/'+k+'.json')].filter(file=>fs.existsSync(file)).map(file=>({path:file,sha256:hashFile(file)}));
  need(typeof api.adoptRuns==='function','DURABLE_ADOPTION_REQUIRED');await api.adoptRuns(SLUG,{artifacts});
  const event=workdir+'/story/recheck-audit/'+id;need(!fs.existsSync(event),'RECHECK_EVENT_COLLISION');
  const rows=[];
  for(const name of journals()){
   need(/^[a-f0-9]{64}\.json$/.test(name),'INVALID_JOURNAL_NAME');const file=journalDir+'/'+name;
   need(fs.lstatSync(file).isFile()&&!fs.lstatSync(file).isSymbolicLink(),'JOURNAL_NOT_REGULAR');
   const bytes=fs.readFileSync(file),record=JSON.parse(bytes);
   need(record.request?.slug===SLUG&&record.receipt?.status==='succeeded'&&record.adopted===true,'UNCONSUMED_OR_UNCERTAIN_JOURNAL');
   need((record.request.variant==='story'&&['verifier','listener'].includes(record.request.stage))||(record.request.stage==='verifier'&&record.request.variant==='narrative')||(record.request.stage==='writer'&&record.request.variant==='story'&&record.request.payload?.chapter?.key==='now'),'JOURNAL_OUTSIDE_SCOPE');
   durable(event+'/'+name,bytes);rows.push({name,stage:record.request.stage,variant:record.request.variant,status:record.receipt.status,sha256:sha(bytes)});
  }
  need(rows.length>0,'RECHECK_HAS_NO_MODEL_JOURNAL');
  const index={schema_version:1,slug:SLUG,result_kind:'saved',install_receipt_sha256:initial.new_pins.install_receipt_sha256,before_source_sha256:expected,after_source_sha256:afterHash,before,after,journals:rows};
  durable(event+'/index.json',json(index));
  for(const row of rows)need(hashFile(event+'/'+row.name)===row.sha256,'AUDIT_JOURNAL_READBACK_FAILED');
  need(sha(JSON.stringify(sources()))===afterHash,'AUDIT_SOURCE_READBACK_FAILED');
  const afterCapture=runDir+'/after';fs.mkdirSync(afterCapture);captureAdoptionSources({root,workBase,output:afterCapture});
  durable(runDir+'/committed.json',json({schema_version:1,id,index_sha256:hashFile(event+'/index.json'),source_sha256:afterHash}));
  await api.settleRuns?.([...automation.runSlugs]);automation.runSlugs.clear();expected=afterHash;
  console.log(JSON.stringify({unit:unit+1,event_id:id,message,calls,source_sha256:expected,checked:Object.values(state.story.chapters).filter(c=>c.checked).length,listened:Object.values(state.story.chapters).filter(c=>c.listened).length,narrative:state.story.narrative}));
  if(didBlock||automation.halted||automation.skipped.has(SLUG)||state.story.narrative?.passed===true||!message)break;
  need(Object.values(state.story.chapters).every(c=>!c.lint?.length),'REVIEW_LINT_REQUIRES_REWRITE');
 }
 console.log(JSON.stringify({event:'A01_REVIEW_BATCH_ENDED',calls,verified:state.verified,listener_done:state.listener_done,narrative:state.story.narrative,blocked_kind:state.blocked_kind,paid_media_allowed:false}));
 }
}finally{restoreStop();lease.release();}
