// Narrow, pure guards for A01's independently reviewed round-11 narration cut.
import {isDeepStrictEqual} from 'node:util';
import fs from 'node:fs';
import path from 'node:path';

const need=(condition,code)=>{if(!condition)throw Error(code);};
const plain=value=>value!==null&&typeof value==='object'&&!Array.isArray(value);

export function assertTurn104(chapter){
  need(chapter?.key==='turn'&&Array.isArray(chapter.scenes)&&Array.isArray(chapter.claims),'TURN_CHAPTER_INVALID');
  const scene=chapter.scenes.filter(row=>row.id==='turn-08');
  need(scene.length===1&&scene[0].lines?.length===1&&scene[0].lines[0].id==='6i8x','TARGET_SCENE_DRIFT');
  const claim=chapter.claims.filter(row=>row.id==='t19');
  need(claim.length===1&&claim[0].scene==='turn-08','TARGET_CLAIM_DRIFT');
  need(chapter.claims.filter(row=>row.scene==='turn-08').length===1,'OTHER_CLAIM_ON_TARGET_SCENE');
  need(!(chapter.loops??[]).some(loop=>loop.setup==='6i8x'||loop.payoff==='6i8x'),'TARGET_LINE_IS_LOOP_ANCHOR');
  return {scene:scene[0],claim:claim[0]};
}

export function assertOnlyTurnDrop(answer){
  need(plain(answer)&&Object.keys(answer).every(key=>['patch','drop','edits'].includes(key)),'LISTENER_ANSWER_OUTSIDE_SCOPE');
  need(plain(answer.patch)&&Object.keys(answer.patch).length===0,'LISTENER_PATCH_OUTSIDE_SCOPE');
  need(Array.isArray(answer.drop)&&answer.drop.length===1&&answer.drop[0]==='6i8x','LISTENER_DROP_OUTSIDE_SCOPE');
  need(answer.edits===undefined||(Array.isArray(answer.edits)&&answer.edits.length===0),'LISTENER_EDITS_OUTSIDE_SCOPE');
}

export function assertVerifierClaimsExact(before,answer){
  need(Array.isArray(before?.claims)&&Array.isArray(answer?.claims),'VERIFIER_CLAIMS_INVALID');
  const known=new Map(before.claims.map(row=>[row.id,row]));
  need(known.size===before.claims.length,'CURRENT_CLAIM_IDS_DUPLICATED');
  need(answer.claims.length===known.size,'VERIFIER_CLAIM_COUNT_DRIFT');
  const seen=new Set();
  for(let index=0;index<answer.claims.length;index++){
    const row=answer.claims[index];
    need(typeof row?.id==='string'&&!seen.has(row.id)&&known.has(row.id),'VERIFIER_CLAIM_ID_DRIFT');
    need(row.id===before.claims[index].id,'VERIFIER_CLAIM_ORDER_DRIFT');
    seen.add(row.id);
    const prior=known.get(row.id);
    for(const key of ['claim','scene','source','fact'])need(isDeepStrictEqual(row[key],prior[key]),'VERIFIER_CLAIM_IDENTITY_DRIFT');
  }
  need(seen.size===known.size,'VERIFIER_CLAIM_SET_DRIFT');
}

export function assertSavedVerifierClaimsExact(before,after){
  need(before?.key==='turn'&&after?.key==='turn','VERIFIER_SAVED_CHAPTER_INVALID');
  const stable=structuredClone(before);
  const changed=structuredClone(after);
  delete stable.claims;delete changed.claims;delete stable.report;delete changed.report;
  need(isDeepStrictEqual(stable,changed),'VERIFIER_SAVED_CHAPTER_OUTSIDE_SCOPE');
  need(typeof after.report==='string'&&/^### 第 4 輪\n\n[^\s]/u.test(after.report)&&after.report!==before.report,'VERIFIER_SAVED_REPORT_ROUND_DRIFT');
  assertVerifierClaimsExact(before,{claims:after.claims});
  const known=new Map(before.claims.map(row=>[row.id,row]));
  for(const row of after.claims){
    const prior=structuredClone(known.get(row.id));
    const next=structuredClone(row);
    for(const field of ['verdict','note','report']){
      delete prior[field];delete next[field];
    }
    need(isDeepStrictEqual(prior,next),'VERIFIER_SAVED_CLAIM_OUTSIDE_SCOPE');
  }
}

export function assertModelEventScope(kind,before,after){
  need(before&&after,'MODEL_EVENT_SCOPE_MISSING');
  const common=['series','lexicon','pilot'];
  const extra=kind==='listener_drop'?['narrative','verify']:kind==='turn_verifier'?['narrative']:kind==='narrative_panel'?['video','claims','script','verify']:null;
  need(extra!==null,'MODEL_EVENT_KIND_INVALID');
  for(const key of [...common,...extra])need(isDeepStrictEqual(before[key],after[key]),'OUTSIDE_SCOPE_SOURCE_CHANGED_'+key);
  for(const key of ['hook','origin','idea','engine','now'])need(before.chapters[key]===after.chapters[key],'OTHER_CHAPTER_CHANGED_'+key);
  if(kind==='narrative_panel')need(before.chapters.turn===after.chapters.turn,'PANEL_CHANGED_TURN_CHAPTER');
  if(kind==='listener_drop')need(before.chapters.turn!==after.chapters.turn,'LISTENER_TURN_UNCHANGED');
}

export function assertRound12Tip({links,source,events,source104,phaseIndex=null}){
  need(Number.isInteger(links)&&links>=104&&links<=108&&Array.isArray(events),'ROUND12_LINKS_INVALID');
  need(phaseIndex===null||(Number.isInteger(phaseIndex)&&phaseIndex>=0&&phaseIndex<=3&&links===104+phaseIndex),'PHASE_SOURCE_LINK_MISMATCH');
  need(events.length===links-104,'ROUND12_EVENT_COUNT_MISMATCH');
  let tip=source104;
  for(const edge of events){
    need(edge?.before_source_sha256===tip&&typeof edge.after_source_sha256==='string'&&edge.after_source_sha256!==tip,'ROUND12_PREDECESSOR_DRIFT');
    tip=edge.after_source_sha256;
  }
  need(source===tip,'ROUND12_SOURCE_TIP_DRIFT');
}

export function expectedTurnAfterListener(before){
  assertTurn104(before);
  const result=structuredClone(before);
  result.scenes=result.scenes.filter(scene=>scene.id!=='turn-08');
  return result;
}

export function assertListenerSavedExact(before,after){
  need(isDeepStrictEqual(after,expectedTurnAfterListener(before)),'LISTENER_SAVED_OUTSIDE_SCOPE');
}

export function retireT19(afterListener){
  need(afterListener?.key==='turn'&&Array.isArray(afterListener.scenes)&&Array.isArray(afterListener.claims),'TURN_CHAPTER_INVALID');
  need(!afterListener.scenes.some(scene=>scene.id==='turn-08'),'TARGET_SCENE_NOT_DROPPED');
  need(afterListener.claims.filter(row=>row.id==='t19'&&row.scene==='turn-08').length===1,'TARGET_CLAIM_DRIFT');
  need(afterListener.claims.filter(row=>row.scene==='turn-08').length===1,'OTHER_CLAIM_ON_TARGET_SCENE');
  const result=structuredClone(afterListener);
  result.claims=result.claims.filter(row=>row.id!=='t19');
  return result;
}

export function assertManualAutoChange(before,after){
  need(before?.story?.chapters?.turn?.checked===true&&before.verified===true,'AUTO_BEFORE_DRIFT');
  need(after?.story?.chapters?.turn?.checked===false&&after.verified===false,'AUTO_NOT_INVALIDATED');
  const expect=structuredClone(before);
  expect.story.chapters.turn.checked=false;
  expect.verified=false;
  need(isDeepStrictEqual(after,expect),'AUTO_CHANGED_OUTSIDE_SCOPE');
}

export function scopedStop(file){
  const stat=fs.lstatSync(file);
  need(stat.isFile()&&!stat.isSymbolicLink(),'SCOPED_STOP_REQUIRED');
  const original=fs.readFileSync(file);
  let removed=false;
  return {
    original,
    remove(){
      const current=fs.lstatSync(file);
      need(!removed&&current.isFile()&&!current.isSymbolicLink()&&fs.readFileSync(file).equals(original),'STOP_CHANGED');
      fs.unlinkSync(file);removed=true;
    },
    restore(){
      if(!removed)return;
      if(fs.existsSync(file)){const current=fs.lstatSync(file);need(current.isFile()&&!current.isSymbolicLink()&&fs.readFileSync(file).equals(original),'STOP_CHANGED');removed=false;return;}
      const fd=fs.openSync(file,'wx',0o600);
      try{fs.writeFileSync(fd,original);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}
      const dir=fs.openSync(path.dirname(file),'r');
      try{try{fs.fsyncSync(dir);}catch(error){if(process.platform!=='win32'||!['EPERM','EINVAL'].includes(error.code))throw error;}}finally{fs.closeSync(dir);}
      removed=false;
    },
  };
}

export async function retryPendingSameSource(run,{pendingCode,source,expected,maxPolls=24,delay=()=>new Promise(resolve=>setTimeout(resolve,5000))}){
  let pending=0;
  while(true){
    need(source()===expected,'PENDING_REQUEST_SOURCE_CHANGED');
    try{return await run();}
    catch(error){
      if(error.code!==pendingCode||++pending>maxPolls)throw error;
      await delay();
    }
  }
}
