// A01 only. Resume from the verified 104-link source with one reviewed scene cut.
// Caller verifies the host hold, paid-job quiet state and budget. This driver never enters media.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash,randomUUID} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {readStoryLexicon} from '/opt/mokaair/tools/video/core/story-lexicon.mjs';
import {atomicWrite} from '/opt/mokaair/tools/video/core/paths.mjs';
import {Automation} from '/opt/mokaair/tools/video/automation/flow.mjs';
import {automationClient,RUN_PENDING} from '/opt/mokaair/tools/video/automation/client.mjs';
import {advanceStory} from '/opt/mokaair/tools/video/automation/story.mjs';
import {acquireProjectLease} from '/opt/mokaair/tools/video/core/project-lease.mjs';
import {captureAdoptionSources} from './adopt-pinned.mjs';
import {inspectReviewProgress,checkRound12Manual} from './inspect-review-progress.mjs';
import {assertTurn104,assertOnlyTurnDrop,assertListenerSavedExact,assertVerifierClaimsExact,assertSavedVerifierClaimsExact,assertModelEventScope,assertRound12Tip,retireT19,assertManualAutoChange,scopedStop,retryPendingSameSource} from './review-round12-core.mjs';

const SLUG='story-rolling-suitcase-v2';
const root='/opt/mokaair',workBase='/var/lib/mokaair/video-work';
const workdir=path.join(workBase,SLUG),stop=path.join(workdir,'STOP');
const source104='e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7';
const installReceipt='24110fc8cc1665e9f6830db23e57cde12640c4bd947af3a42a25602528a266fd';
const ownerRef='current-chat/2026-10-17/user-request-complete-production-data-handoff-review-and-A01';
const payload=path.resolve(path.dirname(new URL(import.meta.url).pathname),'../../../../..');
const candidate=path.dirname(new URL(import.meta.url).pathname);
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const need=(condition,code)=>{if(!condition)throw Error(code);};
const json=value=>Buffer.from(JSON.stringify(value,null,2)+'\n');
const exactFile=file=>{const stat=fs.lstatSync(file);need(stat.isFile()&&!stat.isSymbolicLink(),'SOURCE_NOT_REGULAR');return fs.readFileSync(file);};
const hashFile=(file,optional=false)=>optional&&!fs.existsSync(file)?null:sha(exactFile(file));
const chapterFile=workdir+'/story/chapters/turn.json',autoFile=workdir+'/auto.json';
const auditBase=workdir+'/story/recheck-audit',runBase=workdir+'/story/recheck-runs';
const journalDir=workdir+'/run-receipts';
const options={before80Root:payload+'/before80',before81Root:payload+'/before-81',oldLexiconFile:payload+'/old-lexicon.json',reviewBytes:exactFile(payload+'/revision-review.json'),receiptBytes:exactFile(payload+'/revision-owner-record.json')};

function sources(){
 const doc=root+'/docs/videos/'+SLUG;
 return {auto:hashFile(autoFile),video:hashFile(doc+'/video.json'),series:hashFile(doc+'/series.json'),claims:hashFile(doc+'/claims.md'),script:hashFile(doc+'/script.md'),lexicon:readStoryLexicon({slug:SLUG,storyDir:doc,sharedFile:root+'/docs/videos/lexicon.json'}).lexicon_sha256,narrative:hashFile(workdir+'/review/narrative.json'),pilot:hashFile(workdir+'/story/reviews/script-review.json',true),verify:hashFile(doc+'/verify-1.md',true),chapters:Object.fromEntries(['hook','origin','idea','engine','turn','now'].map(key=>[key,hashFile(workdir+'/story/chapters/'+key+'.json')]))};
}
function durable(file,bytes){
 fs.mkdirSync(path.dirname(file),{recursive:true});
 const fd=fs.openSync(file,'wx',0o600);
 try{fs.writeFileSync(fd,bytes);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}
 const dir=fs.openSync(path.dirname(file),'r');try{fs.fsyncSync(dir);}finally{fs.closeSync(dir);}
}
function journalNames(){return fs.existsSync(journalDir)?fs.readdirSync(journalDir).filter(name=>name.endsWith('.json')).sort():[];}
function requireNoJournals(){need(journalNames().length===0,'ACTIVE_OR_UNSETTLED_REQUEST_REQUIRES_REVIEW');}
function requireUnchanged(before,after,keys){for(const key of keys)need(isDeepStrictEqual(before[key],after[key]),'OUTSIDE_SCOPE_SOURCE_CHANGED_'+key);}
function artifacts(){
 const files=[autoFile,...['video.json','series.json','claims.md','script.md','verify-1.md'].map(name=>root+'/docs/videos/'+SLUG+'/'+name),workdir+'/review/narrative.json',...['hook','origin','idea','engine','turn','now'].map(key=>workdir+'/story/chapters/'+key+'.json')];
 return files.filter(file=>fs.existsSync(file)).map(file=>({path:file,sha256:hashFile(file)}));
}
function makeIntent(expected,kind,stopSha){
 const id=new Date().toISOString().replaceAll(':','-')+'-'+randomUUID();
 const dir=runBase+'/'+id;fs.mkdirSync(dir,{recursive:true});
 fs.mkdirSync(dir+'/before');captureAdoptionSources({root,workBase,output:dir+'/before'});
 durable(dir+'/intent.json',json({schema_version:1,slug:SLUG,id,kind,before_source_sha256:expected,owner_approval_ref:ownerRef,stop_sha256:stopSha}));
 return {id,dir};
}
async function commitModelEvent({api,automation,lease,id,dir,before,expected,kind,stage,variant,baselineTurn,beforeTurn}){
 const after=sources(),afterHash=sha(JSON.stringify(after));need(afterHash!==expected,'NO_RECHECK_SOURCE_CHANGE');
 assertModelEventScope(kind,before,after);
 if(kind==='listener_drop')assertListenerSavedExact(JSON.parse(baselineTurn),JSON.parse(exactFile(chapterFile)));
 if(kind==='turn_verifier')assertSavedVerifierClaimsExact(JSON.parse(beforeTurn),JSON.parse(exactFile(chapterFile)));
 lease.verify();need(typeof api.adoptRuns==='function','DURABLE_ADOPTION_REQUIRED');
 await api.adoptRuns(SLUG,{artifacts:artifacts()});
 const names=journalNames();need(names.length===1,'EXACT_ONE_MODEL_JOURNAL_REQUIRED');
 const name=names[0];need(/^[a-f0-9]{64}\.json$/.test(name),'JOURNAL_NAME_INVALID');
 const raw=exactFile(journalDir+'/'+name),record=JSON.parse(raw);
 need(record.request?.slug===SLUG&&record.request?.stage===stage&&record.request?.variant===variant&&record.receipt?.status==='succeeded'&&record.adopted===true,'MODEL_JOURNAL_OUTSIDE_SCOPE');
 const event=auditBase+'/'+id;need(!fs.existsSync(event),'RECHECK_EVENT_COLLISION');
 durable(event+'/'+name,raw);
 const turnEvidence=kind==='listener_drop'||kind==='turn_verifier'?{before_sha256:sha(kind==='listener_drop'?baselineTurn:beforeTurn),after_sha256:hashFile(chapterFile)}:null;
 if(turnEvidence){durable(event+'/before-turn.json',kind==='listener_drop'?baselineTurn:beforeTurn);durable(event+'/after-turn.json',exactFile(chapterFile));}
 const index={schema_version:1,slug:SLUG,result_kind:'saved',install_receipt_sha256:installReceipt,before_source_sha256:expected,after_source_sha256:afterHash,before,after,journals:[{name,stage,variant,status:'succeeded',sha256:sha(raw)}],...(turnEvidence?{turn_evidence:turnEvidence}:{})};
 durable(event+'/index.json',json(index));
 need(hashFile(event+'/'+name)===sha(raw)&&sha(JSON.stringify(sources()))===afterHash,'MODEL_AUDIT_READBACK_FAILED');
 fs.mkdirSync(dir+'/after');captureAdoptionSources({root,workBase,output:dir+'/after'});
 durable(dir+'/committed.json',json({schema_version:1,id,index_sha256:hashFile(event+'/index.json'),source_sha256:afterHash}));
 need(typeof api.settleRuns==='function','DURABLE_SETTLE_REQUIRED');
 await api.settleRuns([...automation.runSlugs]);automation.runSlugs.clear();requireNoJournals();
 return {after,afterHash};
}

function commitManualEvent({lease,id,dir,before,expected,baselineTurn,beforeTurn,beforeAuto,beforeVideo,afterTurn,afterAuto,editorialHash}){
 const after=sources(),afterHash=sha(JSON.stringify(after));need(afterHash!==expected,'NO_MANUAL_SOURCE_CHANGE');
 requireUnchanged(before,after,['series','lexicon','narrative','pilot','verify']);
 for(const key of ['hook','origin','idea','engine','now'])need(before.chapters[key]===after.chapters[key],'OTHER_CHAPTER_CHANGED');
 need(after.chapters.turn===sha(afterTurn)&&before.chapters.turn===sha(beforeTurn)&&before.auto===sha(beforeAuto)&&after.auto===sha(afterAuto),'MANUAL_HASH_MISMATCH');
 need(sha(baselineTurn)==='31157cfd9435d4ff2f94f2506224c21a5e4bd0a1997a788dbd88aa303858a981','BASELINE_104_TURN_DRIFT');
 assertListenerSavedExact(JSON.parse(baselineTurn),JSON.parse(beforeTurn));
 const original=JSON.parse(beforeTurn),cut=JSON.parse(afterTurn);
 need(isDeepStrictEqual(cut,retireT19(original)),'MANUAL_TURN_OUTSIDE_SCOPE');
 assertManualAutoChange(JSON.parse(beforeAuto),JSON.parse(afterAuto));
 lease.verify();requireNoJournals();
 const event=auditBase+'/'+id;need(!fs.existsSync(event),'RECHECK_EVENT_COLLISION');
 const amendment={schema_version:1,slug:SLUG,kind:'retire_t19_after_listener_drop',editorial_review_sha256:editorialHash,owner_approval_ref:ownerRef,removed_scene:'turn-08',removed_line:'6i8x',removed_claim:'t19',before_source_sha256:expected,after_source_sha256:afterHash,baseline_turn_sha256:sha(baselineTurn),before_turn_sha256:sha(beforeTurn),after_turn_sha256:sha(afterTurn),before_auto_sha256:sha(beforeAuto),after_auto_sha256:sha(afterAuto)};
 for(const [name,bytes] of [['baseline-turn.json',baselineTurn],['before-turn.json',beforeTurn],['after-turn.json',afterTurn],['before-auto.json',beforeAuto],['after-auto.json',afterAuto],['manual-amendment.json',json(amendment)]])durable(event+'/'+name,bytes);
 const doc=root+'/docs/videos/'+SLUG;
 const derived=[['series.json',exactFile(doc+'/series.json')],['before-video.json',beforeVideo],['after-video.json',exactFile(doc+'/video.json')],['after-claims.md',exactFile(doc+'/claims.md')],['after-script.md',exactFile(doc+'/script.md')],...['hook','origin','idea','engine','turn','now'].map(key=>['chapter-'+key+'.json',exactFile(workdir+'/story/chapters/'+key+'.json')])];
 const manualDerivatives=Object.fromEntries(derived.map(([name,bytes])=>[name,sha(bytes)]));
 for(const [name,bytes] of derived)durable(event+'/'+name,bytes);
 const index={schema_version:1,slug:SLUG,result_kind:'manual_amendment',install_receipt_sha256:installReceipt,before_source_sha256:expected,after_source_sha256:afterHash,before,after,journals:[],manual_amendment_sha256:hashFile(event+'/manual-amendment.json'),manual_derivatives:manualDerivatives};
 durable(event+'/index.json',json(index));
 checkRound12Manual(workBase,SLUG+'/story/recheck-audit/'+id,index);
 need(sha(JSON.stringify(sources()))===afterHash,'MANUAL_AUDIT_READBACK_FAILED');
 fs.mkdirSync(dir+'/after');captureAdoptionSources({root,workBase,output:dir+'/after'});
 durable(dir+'/committed.json',json({schema_version:1,id,index_sha256:hashFile(event+'/index.json'),source_sha256:afterHash}));
 return {after,afterHash};
}

async function main(){
 const phases={'--listener':0,'--manual':1,'--facts':2,'--panel':3};
 const command=process.argv[2],phaseIndex=phases[command];
 need(process.argv.length===3&&(command==='--preflight'||Number.isInteger(phaseIndex)),'EXPLICIT_PREFLIGHT_OR_ONE_PHASE_REQUIRED');
 need(!fs.existsSync(workBase+'/STOP'),'GLOBAL_STOP_PRESENT');
 need(fs.lstatSync(stop).isFile()&&!fs.lstatSync(stop).isSymbolicLink(),'SCOPED_STOP_REQUIRED');
 const stopGuard=scopedStop(stop),stopBytes=stopGuard.original,stopSha=sha(stopBytes);
 for(const [relative,expected] of Object.entries(JSON.parse(exactFile(candidate+'/required-runtime.json'))))need(hashFile(root+'/'+relative)===expected,'RUNTIME_HASH_DRIFT_'+relative);
 function inspectCandidate(){
  // This writes a bounded copy only under host /tmp. It never acquires or alters A01 LEASE.
  const capture=fs.mkdtempSync(path.join(os.tmpdir(),'a01-round12-preflight-'));
  captureAdoptionSources({root,workBase,output:capture});
  const progress=inspectReviewProgress({...options,base82Root:payload+'/base82',progressRoot:capture});
  assertRound12Tip({links:progress.links,source:progress.source_sha256,events:progress.round12_events,source104,phaseIndex:Number.isInteger(phaseIndex)?phaseIndex:null});
  requireNoJournals();
  const firstRound12=progress.round12_events[0];
  const baselineTurn=progress.links===104?exactFile(chapterFile):exactFile(auditBase+'/'+firstRound12?.id+'/before-turn.json');
  assertTurn104(JSON.parse(baselineTurn));
  const initial=JSON.parse(exactFile(autoFile));
  need(initial.slug===SLUG&&initial.status==='blocked'&&initial.story&&initial.story.chapters?.turn,'REVIEW_BLOCKED_STATE_DRIFT');
  if(progress.links===104)need(initial.blocked_kind==='prompt_fixes:narrative'&&initial.story.narrative?.rounds===11&&initial.story.narrative?.passed===false&&initial.story.narrative_fixes===2&&initial.story.chapters.turn.check_rounds===3&&initial.story.chapters.turn.checked===true&&initial.story.chapters.turn.listened===true&&initial.verified===true&&initial.listener_done===true,'REVIEW_STATE_104_DRIFT');
  need(sha(exactFile(stop))===stopSha,'STOP_CHANGED');
  return {progress,baselineTurn,initial};
 }
 if(command==='--preflight'){
  const {progress}=inspectCandidate();
  console.log(JSON.stringify({event:'A01_ROUND12_PREFLIGHT_PASS',links:progress.links,source_sha256:progress.source_sha256,stop_preserved:true,canonical_lease_acquired:false,temp_capture_written:true,model_calls:0,paid_media_allowed:false}));
  return;
 }
 // A production phase takes A01 LEASE before its own fresh source capture and inspection.
 const lease=acquireProjectLease(workdir,{owner:'a01-round12-reviewed-cut'});
 const restoreStop=()=>stopGuard.restore();
 for(const signal of ['SIGTERM','SIGINT'])process.once(signal,()=>{try{restoreStop();}finally{lease.release();process.exit(128);}});
 try{
  lease.verify();
  const {progress,baselineTurn,initial}=inspectCandidate();
  lease.verify();
  need(sha(JSON.stringify(sources()))===progress.source_sha256,'SOURCE_DRIFT_UNDER_LEASE');
  requireNoJournals();
   const pending=JSON.parse(exactFile(workdir+'/round12-restore-stop.pending.json'));
   need(pending.schema_version===1&&pending.slug===SLUG&&pending.phase===command&&pending.stop_sha256===stopSha&&pending.source_sha256===progress.source_sha256&&pending.host_startup_guard_verified===true,'HOST_RESTORE_GUARD_REQUIRED');
  const fixedNow=new Date();
  const ctx={root,env:process.env,stdout:process.stdout,stderr:process.stderr,now:()=>fixedNow,EXIT:{ok:0,lint:1,usage:2,owner:3,external:4,missing:5,incomplete:6}};
  const api=automationClient(ctx,{attempts:1});const settings=await api.settings();
  need(settings.enabled===true&&settings.durable_stage_runs===true,'DURABLE_AUTOMATION_REQUIRED');
  const automation=new Automation(ctx,api,settings);automation.leases.set(SLUG,lease);automation.runSlugs=new Set();
   const actualStage=automation.stage.bind(automation);let phase=['listener','manual','facts','panel'][phaseIndex],calls=0;
  automation.stage=async(stage,slug,stagePayload,tokens,format,variant,...rest)=>{
   need(slug===SLUG&&format==='drama'&&++calls<=220,'REVIEW_STAGE_BOUND');
   need((phase==='listener'&&stage==='listener'&&variant==='story'&&stagePayload?.chapter?.key==='turn')||(phase==='facts'&&stage==='verifier'&&variant==='story'&&stagePayload?.chapter?.key==='turn')||(phase==='panel'&&stage==='verifier'&&variant==='narrative'),'REVIEW_STAGE_OUTSIDE_SCOPE');
   const answer=await actualStage(stage,slug,stagePayload,tokens,format,variant,...rest);
   if(phase==='listener')assertOnlyTurnDrop(answer);
   if(phase==='facts'){
    need(answer&&typeof answer.patch==='object'&&!Array.isArray(answer.patch)&&Object.keys(answer.patch).length===0&&Array.isArray(answer.drop)&&answer.drop.length===0,'VERIFIER_NARRATION_EDIT_OUTSIDE_SCOPE');
    const current=JSON.parse(exactFile(chapterFile));
    assertVerifierClaimsExact(current,answer);
   }
   return answer;
  };
  async function advanceRetained(state,next){
   const pinned=sha(JSON.stringify(sources()));
   return retryPendingSameSource(()=>advanceStory(automation,state,next),{pendingCode:RUN_PENDING,source:()=>sha(JSON.stringify(sources())),expected:pinned,maxPolls:72,delay:async()=>{console.log('A01 durable receipt pending; polling same request');await new Promise(resolve=>setTimeout(resolve,5000));}});
  }
   let expected=progress.source_sha256;
  lease.verify();need(sha(JSON.stringify(sources()))===progress.source_sha256,'SOURCE_DRIFT_BEFORE_STOP_LIFT');
  need(sha(exactFile(stop))===stopSha,'STOP_CHANGED');stopGuard.remove();
  console.log(JSON.stringify({event:'A01_ROUND12_STARTED',source_sha256:expected,paid_media_allowed:false}));

  // 1. Only the worker's real listener may remove line 6i8x and its now empty shot.
   if(phaseIndex===0){
   lease.verify();need(!fs.existsSync(stop),'NEW_STOP_PRESENT');const before=sources();need(sha(JSON.stringify(before))===expected,'SOURCE_DRIFT_BEFORE_LISTENER');
   const intent=makeIntent(expected,'listener_drop',stopSha);
   initial.story.chapters.turn.listened=false;initial.listener_done=false;
   initial.story.owner_note='獨立編輯複核第 11 輪 one_line／no_recap：turn-08 唯一旁白 6i8x 重複前面安檢拆裝；只 drop 6i8x，不 patch 其他句子。turn-08b 與所有掛鉤保持原樣。';
   const message=await advanceRetained(initial,'verified');
    const saved=JSON.parse(exactFile(chapterFile));assertListenerSavedExact(JSON.parse(baselineTurn),saved);
   need(initial.story.chapters.turn.listened===true&&initial.story.chapters.turn.checked===true&&initial.verified===true&&initial.listener_done===true&&initial.story.narrative.rounds===11,'LISTENER_STATE_OUTSIDE_SCOPE');
    const committed=await commitModelEvent({api,automation,lease,...intent,before,expected,kind:'listener_drop',stage:'listener',variant:'story',baselineTurn});
   expected=committed.afterHash;console.log(JSON.stringify({event:'A01_REAL_LISTENER_DROP_SAVED',message,source_sha256:expected}));
  }

  // 2. Listener keeps old fact rows. Retire only t19, then use the installed relint writer.
   if(phaseIndex===1){
    lease.verify();need(!fs.existsSync(stop),'NEW_STOP_PRESENT');requireNoJournals();
   const before=sources();need(sha(JSON.stringify(before))===expected,'SOURCE_DRIFT_BEFORE_AMENDMENT');
   const intent=makeIntent(expected,'retire_t19',stopSha);
    const beforeTurn=exactFile(chapterFile),beforeAuto=exactFile(autoFile),beforeVideo=exactFile(root+'/docs/videos/'+SLUG+'/video.json');
   const amended=retireT19(JSON.parse(beforeTurn));
   initial.story.chapters.turn.checked=false;initial.verified=false;
   atomicWrite(chapterFile,json(amended));
   const message=await advanceStory(automation,initial,'script passes lint');
   need(typeof message==='string'&&message.includes('passes lint'),'REMERGE_NOT_CLEAN');
   const afterTurn=exactFile(chapterFile),afterAuto=exactFile(autoFile);
    const committed=commitManualEvent({lease,...intent,before,expected,baselineTurn,beforeTurn,beforeAuto,beforeVideo,afterTurn,afterAuto,editorialHash:hashFile(candidate+'/round11-editorial-review.md')});
   expected=committed.afterHash;console.log(JSON.stringify({event:'A01_T19_RETIRED_AND_REMERGED',message,source_sha256:expected}));
  }

  // 3. One real turn verifier; a changed narration or claim identity stops before saving.
   if(phaseIndex===2){
    lease.verify();need(!fs.existsSync(stop),'NEW_STOP_PRESENT');requireNoJournals();
    const before=sources(),beforeTurn=exactFile(chapterFile);need(sha(JSON.stringify(before))===expected,'SOURCE_DRIFT_BEFORE_VERIFIER');
   const intent=makeIntent(expected,'turn_verifier',stopSha);
   const message=await advanceRetained(initial,'verified');
   const turn=JSON.parse(exactFile(chapterFile));need(!turn.scenes.some(scene=>scene.id==='turn-08')&&!turn.claims.some(row=>row.id==='t19'),'RETIRED_SOURCE_REAPPEARED');
   need(initial.story.chapters.turn.check_rounds===4&&initial.story.chapters.turn.checked===true,'VERIFIER_ROUND_DRIFT');
    const committed=await commitModelEvent({api,automation,lease,...intent,before,expected,kind:'turn_verifier',stage:'verifier',variant:'story',beforeTurn});
   expected=committed.afterHash;console.log(JSON.stringify({event:'A01_TURN_VERIFIER_SAVED',message,source_sha256:expected}));
  }

  // 4. The whole-film panel is a new real model answer. The pilot receipt remains a hard stop.
   if(phaseIndex===3){
    lease.verify();need(!fs.existsSync(stop),'NEW_STOP_PRESENT');requireNoJournals();
   const before=sources();need(sha(JSON.stringify(before))===expected,'SOURCE_DRIFT_BEFORE_PANEL');
   const intent=makeIntent(expected,'narrative_panel',stopSha);
   const message=await advanceRetained(initial,'verified');
   need(initial.story.narrative.rounds===12,'NARRATIVE_ROUND_DRIFT');
   need(initial.blocked_kind==='pilot_script_review'||initial.blocked_kind==='prompt_fixes:narrative','PANEL_STOP_GATE_DRIFT');
    const committed=await commitModelEvent({api,automation,lease,...intent,before,expected,kind:'narrative_panel',stage:'verifier',variant:'narrative'});
   expected=committed.afterHash;console.log(JSON.stringify({event:'A01_NARRATIVE_PANEL_SAVED',message,source_sha256:expected,passed:initial.story.narrative.passed,blocked_kind:initial.blocked_kind,paid_media_allowed:false}));
  }
  console.log(JSON.stringify({event:'A01_ROUND12_ENDED',source_sha256:expected,model_call_attempts:calls,narrative:initial.story.narrative,blocked_kind:initial.blocked_kind,paid_media_allowed:false}));
 }finally{restoreStop();lease.release();}
}
await main();
