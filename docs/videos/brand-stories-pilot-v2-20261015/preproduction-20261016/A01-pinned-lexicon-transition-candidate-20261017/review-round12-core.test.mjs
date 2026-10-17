import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {assertTurn104,assertOnlyTurnDrop,assertListenerSavedExact,assertVerifierClaimsExact,assertSavedVerifierClaimsExact,assertModelEventScope,assertRound12Tip,expectedTurnAfterListener,retireT19,assertManualAutoChange,scopedStop,retryPendingSameSource} from './review-round12-core.mjs';
import {checkRound12Manual,checkRound12Model,manualDerivativeBytes} from './inspect-review-progress.mjs';
import {lintProject,loadProject} from '../../../../../tools/video/core/state.mjs';
import {writeScreenplay} from '../../../../../tools/video/core/screenplay.mjs';
import {storyBrief,composeStory} from '../../../../../tools/video/automation/story.mjs';

const snapshot=process.env.A01_SNAPSHOT104_ROOT;
if(!snapshot)throw Error('Set A01_SNAPSHOT104_ROOT to the verified snapshot-104 root');
const slug='story-rolling-suitcase-v2';
const original=JSON.parse(fs.readFileSync(path.join(snapshot,slug,'story/chapters/turn.json')));
const auto=JSON.parse(fs.readFileSync(path.join(snapshot,slug,'auto.json')));
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const json=value=>Buffer.from(JSON.stringify(value,null,2)+'\n');

test('actual 104 chapter has exactly the reviewed target',()=>{
 const target=assertTurn104(original);
 assert.equal(target.scene.lines[0].text,'照這篇報導的說法，他動手改造的起點，就是前面那些旅客拆裝的麻煩。');
 assert.equal(target.claim.id,'t19');
});

test('only an empty patch and one exact drop are admitted',()=>{
 assertOnlyTurnDrop({patch:{},drop:['6i8x'],edits:[]});
 for(const answer of [{patch:{x:'change'},drop:['6i8x']},{patch:{},drop:['6i8x','b7mz']},{patch:{},drop:[]},{patch:{},drop:['6i8x'],lexicon:{evil:'x'}},{patch:{},drop:['6i8x'],edits:[{id:'6i8x',text:'hidden edit'}]}])assert.throws(()=>assertOnlyTurnDrop(answer));
});

test('verifier claim IDs retain exact unique order and saved core fields',()=>{
 const chapter=retireT19(expectedTurnAfterListener(original));
 const reply={claims:chapter.claims.map(row=>({...row,verdict:'CONFIRMED'}))};
 const saved={...chapter,report:'### 第 4 輪\n\n第四輪查核報告',claims:reply.claims};
 assertVerifierClaimsExact(chapter,reply);
 assertSavedVerifierClaimsExact(chapter,saved);
 const duplicate=structuredClone(reply);duplicate.claims[1].id=duplicate.claims[0].id;
 assert.throws(()=>assertVerifierClaimsExact(chapter,duplicate),/VERIFIER_CLAIM_ID_DRIFT/);
 const reordered=structuredClone(reply);[reordered.claims[0],reordered.claims[1]]=[reordered.claims[1],reordered.claims[0]];
 assert.throws(()=>assertVerifierClaimsExact(chapter,reordered),/VERIFIER_CLAIM_ORDER_DRIFT/);
 const tampered=structuredClone(reply);tampered.claims[0].scene='other';
 assert.throws(()=>assertSavedVerifierClaimsExact(chapter,{...saved,claims:tampered.claims}),/VERIFIER_CLAIM_IDENTITY_DRIFT/);
 const extra=structuredClone(reply);extra.claims[0].unsafe='x';
 assert.throws(()=>assertSavedVerifierClaimsExact(chapter,{...saved,claims:extra.claims}),/VERIFIER_SAVED_CLAIM_OUTSIDE_SCOPE/);
 assert.throws(()=>assertSavedVerifierClaimsExact(chapter,{...saved,report:'### 第 3 輪\n\n舊報告'}),/VERIFIER_SAVED_REPORT_ROUND_DRIFT/);
 assert.throws(()=>assertSavedVerifierClaimsExact(chapter,{...saved,title:'篡改'}),/VERIFIER_SAVED_CHAPTER_OUTSIDE_SCOPE/);
});

test('model audit scope rejects other chapters before any adoption',()=>{
 const before={series:'s',lexicon:'l',narrative:'n',pilot:null,verify:'v',video:'video',claims:'claims',script:'script',chapters:{hook:'h',origin:'o',idea:'i',engine:'e',turn:'t',now:'w'}};
 const after={...before,chapters:{...before.chapters,turn:'changed'}};
 assertModelEventScope('listener_drop',before,after);
 assert.throws(()=>assertModelEventScope('listener_drop',before,{...after,chapters:{...after.chapters,now:'tampered'}}),/OTHER_CHAPTER_CHANGED_now/);
 assertModelEventScope('narrative_panel',before,{...before,narrative:'round-12'});
 for(const key of ['video','claims','script','verify'])assert.throws(()=>assertModelEventScope('narrative_panel',before,{...before,narrative:'round-12',[key]:'tampered'}),/OUTSIDE_SCOPE_SOURCE_CHANGED_/);
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'a01-round12-scope-'));
 try{
  const rel='event';fs.mkdirSync(path.join(tmp,rel));
  const beforeTurn=json(original),afterTurn=json(expectedTurnAfterListener(original));
  fs.writeFileSync(path.join(tmp,rel,'before-turn.json'),beforeTurn);fs.writeFileSync(path.join(tmp,rel,'after-turn.json'),afterTurn);
  const index={before:{...before,chapters:{...before.chapters,turn:sha(beforeTurn)}},after:{...after,chapters:{...after.chapters,turn:sha(afterTurn)}},turn_evidence:{before_sha256:sha(beforeTurn),after_sha256:sha(afterTurn)}};
  checkRound12Model(tmp,rel,index,'listener_drop');
  index.after.chapters.now='tampered';
  assert.throws(()=>checkRound12Model(tmp,rel,index,'listener_drop'),/OTHER_CHAPTER_CHANGED_now/);
 }finally{fs.rmSync(tmp,{recursive:true,force:true});}
});

test('every round-12 phase pins the exact 104 source and previous event tip',()=>{
 const source104='e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7';
 assertRound12Tip({links:104,source:source104,events:[],source104,phaseIndex:0});
 assert.throws(()=>assertRound12Tip({links:104,source:'wrong',events:[],source104,phaseIndex:0}),/ROUND12_SOURCE_TIP_DRIFT/);
 const edges=[{before_source_sha256:source104,after_source_sha256:'105'},{before_source_sha256:'105',after_source_sha256:'106'}];
 assertRound12Tip({links:106,source:'106',events:edges,source104,phaseIndex:2});
 assert.throws(()=>assertRound12Tip({links:106,source:'106',events:[edges[0],{...edges[1],before_source_sha256:'other'}],source104,phaseIndex:2}),/ROUND12_PREDECESSOR_DRIFT/);
 assert.throws(()=>assertRound12Tip({links:106,source:'106',events:edges,source104,phaseIndex:1}),/PHASE_SOURCE_LINK_MISMATCH/);
});

test('listener result must preserve every other byte-level JSON field',()=>{
 const cut=expectedTurnAfterListener(original);
 assertListenerSavedExact(original,cut);
 assert.equal(cut.scenes.length,original.scenes.length-1);
 assert.equal(cut.claims.length,original.claims.length);
 assert.throws(()=>assertListenerSavedExact(original,{...cut,title:'changed'}));
});

test('manual amendment removes only t19 and invalidates only factual flags',()=>{
 const cut=expectedTurnAfterListener(original);
 const fixed=retireT19(cut);
 assert.equal(fixed.claims.length,original.claims.length-1);
 assert.equal(fixed.claims.some(row=>row.id==='t19'),false);
 const next=structuredClone(auto);next.story.chapters.turn.checked=false;next.verified=false;
 assertManualAutoChange(auto,next);
 next.story.narrative_fixes=0;
 assert.throws(()=>assertManualAutoChange(auto,next));
});

test('manual audit verifier accepts the exact 104 cut and rejects a broadened claim edit',()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'a01-round12-audit-'));
 try{
  const event=path.join(tmp,'event');fs.mkdirSync(event);
  const baseline=fs.readFileSync(path.join(snapshot,slug,'story/chapters/turn.json'));
  const beforeTurn=json(expectedTurnAfterListener(original));
  const afterTurn=json(retireT19(JSON.parse(beforeTurn)));
  const beforeAuto=json(auto),after=structuredClone(auto);after.story.chapters.turn.checked=false;after.verified=false;
  const afterAuto=json(after);
  const keys=['hook','origin','idea','engine','turn','now'];
  const chapterBytes=Object.fromEntries(keys.map(key=>[key,key==='turn'?afterTurn:fs.readFileSync(path.join(snapshot,slug,'story/chapters',key+'.json'))]));
  const series=fs.readFileSync(path.join(snapshot,'docs/videos',slug,'series.json'));
  const previousVideo=JSON.parse(fs.readFileSync(path.join(snapshot,'docs/videos',slug,'video.json')));
  const priorChapters=Object.fromEntries(keys.map(key=>[key,JSON.parse(key==='turn'?beforeTurn:chapterBytes[key])]));
  const beforeVideo=json(composeStory({slug,info:JSON.parse(series),chapters:priorChapters,voice:previousVideo.voice,drama:{music_enabled:Boolean(previousVideo.music)},root:snapshot,videoId:previousVideo.youtube?.video_id??null}));
  const derived=manualDerivativeBytes({series,chapters:{...chapterBytes,beforeTurn},beforeVideo,root:snapshot});
  const evidence={'series.json':series,'before-video.json':beforeVideo,...derived,...Object.fromEntries(keys.map(key=>['chapter-'+key+'.json',chapterBytes[key]]))};
  const chapters=Object.fromEntries(keys.map(key=>[key,key==='turn'?sha(beforeTurn):sha(chapterBytes[key])]));
  const before={auto:sha(beforeAuto),video:sha(beforeVideo),claims:'prior',script:'prior',series:sha(series),lexicon:'same',narrative:'same',pilot:null,verify:'same',chapters};
  const later={...before,auto:sha(afterAuto),video:sha(derived['after-video.json']),claims:sha(derived['after-claims.md']),script:sha(derived['after-script.md']),chapters:{...chapters,turn:sha(afterTurn)}};
  const index={before,after:later,before_source_sha256:sha(JSON.stringify(before)),after_source_sha256:sha(JSON.stringify(later)),journals:[]};
  const amendment={schema_version:1,slug,kind:'retire_t19_after_listener_drop',editorial_review_sha256:sha(fs.readFileSync(new URL('./round11-editorial-review.md',import.meta.url))),owner_approval_ref:'current-chat/2026-10-17/user-request-complete-production-data-handoff-review-and-A01',removed_scene:'turn-08',removed_line:'6i8x',removed_claim:'t19',before_source_sha256:index.before_source_sha256,after_source_sha256:index.after_source_sha256,baseline_turn_sha256:sha(baseline),before_turn_sha256:sha(beforeTurn),after_turn_sha256:sha(afterTurn),before_auto_sha256:sha(beforeAuto),after_auto_sha256:sha(afterAuto)};
  index.manual_derivatives=Object.fromEntries(Object.entries(evidence).map(([name,bytes])=>[name,sha(bytes)]));
  for(const [name,bytes] of [['baseline-turn.json',baseline],['before-turn.json',beforeTurn],['after-turn.json',afterTurn],['before-auto.json',beforeAuto],['after-auto.json',afterAuto],['manual-amendment.json',json(amendment)],...Object.entries(evidence),['index.json',json(index)]])fs.writeFileSync(path.join(event,name),bytes);
  index.manual_amendment_sha256=sha(fs.readFileSync(path.join(event,'manual-amendment.json')));
  checkRound12Manual(tmp,'event',index);
  const bad=structuredClone(JSON.parse(afterTurn));bad.title='changed';fs.writeFileSync(path.join(event,'after-turn.json'),json(bad));
  assert.throws(()=>checkRound12Manual(tmp,'event',index));
  fs.writeFileSync(path.join(event,'after-turn.json'),afterTurn);
  const wrong=Buffer.from(derived['after-video.json'].toString().replace('"category": "story"','"category": "drama"'));
  fs.writeFileSync(path.join(event,'after-video.json'),wrong);index.manual_derivatives['after-video.json']=sha(wrong);index.after.video=sha(wrong);
  index.after_source_sha256=sha(JSON.stringify(index.after));amendment.after_source_sha256=index.after_source_sha256;
  fs.writeFileSync(path.join(event,'manual-amendment.json'),json(amendment));index.manual_amendment_sha256=sha(json(amendment));
  assert.throws(()=>checkRound12Manual(tmp,'event',index),/MANUAL_DERIVATIVE_RECOMPOSE_MISMATCH_after-video.json/);
 }finally{fs.rmSync(tmp,{recursive:true,force:true});}
});

test('pending poll retains the same source and refuses a changed request source',async()=>{
 const pendingCode='video_ai_run_pending',key='one-durable-key';let calls=0,source='pinned';
 const result=await retryPendingSameSource(async()=>{
  calls++;assert.equal(key,'one-durable-key');
  if(calls<3)throw Object.assign(new Error('pending'),{code:pendingCode});
  return 'saved';
 },{pendingCode,source:()=>source,expected:'pinned',maxPolls:3,delay:async()=>{}});
 assert.equal(result,'saved');assert.equal(calls,3);
 await assert.rejects(()=>retryPendingSameSource(async()=>{source='changed';throw Object.assign(new Error('pending'),{code:pendingCode});},{pendingCode,source:()=>source,expected:'pinned',maxPolls:2,delay:async()=>{}}),/PENDING_REQUEST_SOURCE_CHANGED/);
});

test('scoped STOP is restored byte for byte after a simulated failure',()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'a01-round12-stop-'));
 try{
  const file=path.join(tmp,'STOP'),content=Buffer.from('A01 reviewed STOP\n');fs.writeFileSync(file,content);
  const guard=scopedStop(file);
  assert.throws(()=>{try{guard.remove();assert.equal(fs.existsSync(file),false);throw Error('simulated failure');}finally{guard.restore();}},/simulated failure/);
  assert.deepEqual(fs.readFileSync(file),content);
 }finally{fs.rmSync(tmp,{recursive:true,force:true});}
});

test('installed lint path allows the transient orphan t19 after the listener cut',()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'a01-round12-lint-'));
 try{
  fs.cpSync(path.join(snapshot,'docs'),path.join(tmp,'docs'),{recursive:true});
  const dir=path.join(tmp,'docs/videos',slug);
  const series=JSON.parse(fs.readFileSync(path.join(dir,'series.json')));
  fs.writeFileSync(path.join(dir,'brief.md'),storyBrief({episode:{title:series.title,logline:series.logline},plan:series.plan,cast:series.characters??[],look:series.look}));
  const videoFile=path.join(dir,'video.json');
  const video=JSON.parse(fs.readFileSync(videoFile));
  video.scenes=video.scenes.filter(scene=>scene.id!=='turn-08');
  fs.writeFileSync(videoFile,JSON.stringify(video,null,2)+'\n');
  writeScreenplay(dir,video);
  const withOrphan=lintProject(loadProject({slug,root:tmp}));
  console.log(JSON.stringify({event:'A01_ROUND12_LINT_PROBE',with_orphan_errors:withOrphan.errors.map(row=>row.message)}));
  assert.deepEqual(withOrphan.errors,[]);
 }finally{fs.rmSync(tmp,{recursive:true,force:true});}
});
