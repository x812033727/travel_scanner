// Read-only verifier for actual review edges appended after the verified 82-event source.
import fs from 'node:fs';import path from 'node:path';import {createHash} from 'node:crypto';import {isDeepStrictEqual} from 'node:util';
import {verify82Fixture} from './pinned-revision-plan.mjs';import {readStoryLexicon} from './snapshot-format.mjs';
import {assertListenerSavedExact,assertSavedVerifierClaimsExact,assertModelEventScope,assertRound12Tip,retireT19,assertManualAutoChange} from './review-round12-core.mjs';
import {composeStory} from '../../../../../tools/video/automation/story.mjs';
import {screenplay} from '../../../../../tools/video/core/screenplay.mjs';
import {normalizeRun,sourceHash,validateRunReceipt,canonicalJson} from '../../../../../tools/video/automation/run-receipts.mjs';
const SLUG='story-rolling-suitcase-v2',DOC='docs/videos/'+SLUG,KEYS=['hook','origin','idea','engine','turn','now'];
const ROUND12_SOURCE104='e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7';
const sha=b=>createHash('sha256').update(b).digest('hex');const need=(v,c)=>{if(!v)throw Error(c);};
function at(root,rel){need(path.isAbsolute(root)&&!root.startsWith('\\\\')&&!root.startsWith('//'),'LOCAL_ROOT_REQUIRED');need(rel.split('/').every(p=>p&&p!=='.'&&p!=='..'&&!/[\\:\x00-\x1f]/.test(p)),'UNSAFE_PATH');let file=path.resolve(root);for(const p of rel.split('/')){file=path.join(file,p);if(fs.existsSync(file))need(!fs.lstatSync(file).isSymbolicLink(),'SYMLINK_REFUSED');}return file;}
const bytes=(root,rel)=>{const file=at(root,rel);need(fs.lstatSync(file).isFile(),'REGULAR_FILE_REQUIRED');return fs.readFileSync(file);};
const hash=(root,rel,optional=false)=>optional&&!fs.existsSync(at(root,rel))?null:sha(bytes(root,rel));
const json=value=>Buffer.from(JSON.stringify(value,null,2)+'\n');
function claimsMarkdown(info,chapters){
 const out=[`# 主張表：${info.title}`,'','企劃的必查事實在匯入前已由第二個人對過來源；這張表是逐章撰稿與查核的紀錄。',''];
 for(const key of KEYS){
  const chapter=chapters[key];out.push(`## ${chapter.title}（${key}）`,'');
  for(const row of chapter.claims??[]){
   const source=Number.isInteger(row.source)?info.plan.sources[row.source]:null;
   out.push([row.id,row.claim,source?.url??'',source?.checked??'',row.scene,row.verdict??'待查'].map(cell=>String(cell).replace(/[|｜\n]/g,'／')).join('｜'));
  }
  out.push('');
 }
 return Buffer.from(out.join('\n'));
}
export function manualDerivativeBytes({series,chapters,beforeVideo,root}){
 const info=JSON.parse(series),prior=JSON.parse(beforeVideo);
 const parsed=Object.fromEntries(KEYS.map(key=>[key,JSON.parse(chapters[key])]));
 const build=(items)=>composeStory({slug:SLUG,info,chapters:items,voice:prior.voice,drama:{music_enabled:Boolean(prior.music)},root,videoId:prior.youtube?.video_id??null});
 const previous={...parsed,turn:JSON.parse(chapters.beforeTurn)};
 need(isDeepStrictEqual(prior,build(previous)),'MANUAL_BEFORE_VIDEO_NOT_COMPOSED');
 const video=build(parsed);
 return {'after-video.json':json(video),'after-claims.md':claimsMarkdown(info,parsed),'after-script.md':Buffer.from(screenplay(video))};
}
function files(root){const result=[];function walk(rel){for(const e of fs.readdirSync(rel?at(root,rel):root,{withFileTypes:true})){need(!e.isSymbolicLink(),'SYMLINK_REFUSED');const p=rel?rel+'/'+e.name:e.name;if(e.isDirectory())walk(p);else{need(e.isFile(),'REGULAR_FILE_REQUIRED');result.push(p);}}}walk('');return result.sort();}
function sources(root){return {auto:hash(root,SLUG+'/auto.json'),video:hash(root,DOC+'/video.json'),series:hash(root,DOC+'/series.json'),claims:hash(root,DOC+'/claims.md'),script:hash(root,DOC+'/script.md'),lexicon:readStoryLexicon({slug:SLUG,storyDir:at(root,DOC),sharedFile:at(root,'docs/videos/lexicon.json')}).lexicon_sha256,narrative:hash(root,SLUG+'/review/narrative.json'),pilot:hash(root,SLUG+'/story/reviews/script-review.json',true),verify:hash(root,DOC+'/verify-1.md',true),chapters:Object.fromEntries(KEYS.map(k=>[k,hash(root,SLUG+'/story/chapters/'+k+'.json')]))};}
export function checkRound12Manual(root,rel,index){
 const derivativeNames=['series.json','before-video.json','after-video.json','after-claims.md','after-script.md',...KEYS.map(key=>'chapter-'+key+'.json')];
 const names=['index.json','manual-amendment.json','baseline-turn.json','before-turn.json','after-turn.json','before-auto.json','after-auto.json',...derivativeNames];
 need(fs.readdirSync(at(root,rel)).sort().join('|')===names.sort().join('|'),'MANUAL_EVENT_EXTRA_FILE');
 need(Array.isArray(index.journals)&&index.journals.length===0,'MANUAL_EVENT_HAS_MODEL_JOURNAL');
 const receiptBytes=bytes(root,rel+'/manual-amendment.json'),receipt=JSON.parse(receiptBytes);
 need(index.manual_amendment_sha256===sha(receiptBytes),'MANUAL_RECEIPT_HASH_INVALID');
 need(receipt.schema_version===1&&receipt.slug===SLUG&&receipt.kind==='retire_t19_after_listener_drop'&&receipt.owner_approval_ref==='current-chat/2026-10-17/user-request-complete-production-data-handoff-review-and-A01'&&receipt.removed_scene==='turn-08'&&receipt.removed_line==='6i8x'&&receipt.removed_claim==='t19','MANUAL_RECEIPT_SCOPE_INVALID');
 need(receipt.editorial_review_sha256===sha(fs.readFileSync(new URL('./round11-editorial-review.md',import.meta.url))),'EDITORIAL_REVIEW_HASH_INVALID');
 need(receipt.before_source_sha256===index.before_source_sha256&&receipt.after_source_sha256===index.after_source_sha256,'MANUAL_SOURCE_EDGE_INVALID');
 const baseline=bytes(root,rel+'/baseline-turn.json'),beforeTurn=bytes(root,rel+'/before-turn.json'),afterTurn=bytes(root,rel+'/after-turn.json');
 const beforeAuto=bytes(root,rel+'/before-auto.json'),afterAuto=bytes(root,rel+'/after-auto.json');
 need(sha(baseline)==='31157cfd9435d4ff2f94f2506224c21a5e4bd0a1997a788dbd88aa303858a981'&&sha(baseline)===receipt.baseline_turn_sha256,'BASELINE_104_TURN_INVALID');
 need(index.before.chapters.turn===sha(beforeTurn)&&index.after.chapters.turn===sha(afterTurn)&&index.before.auto===sha(beforeAuto)&&index.after.auto===sha(afterAuto),'MANUAL_SOURCE_FILE_HASH_INVALID');
 need(receipt.before_turn_sha256===sha(beforeTurn)&&receipt.after_turn_sha256===sha(afterTurn)&&receipt.before_auto_sha256===sha(beforeAuto)&&receipt.after_auto_sha256===sha(afterAuto),'MANUAL_RECEIPT_FILE_HASH_INVALID');
 assertListenerSavedExact(JSON.parse(baseline),JSON.parse(beforeTurn));
 need(isDeepStrictEqual(JSON.parse(afterTurn),retireT19(JSON.parse(beforeTurn))),'MANUAL_TURN_OUTSIDE_SCOPE');
 assertManualAutoChange(JSON.parse(beforeAuto),JSON.parse(afterAuto));
 for(const key of ['series','lexicon','narrative','pilot','verify'])need(isDeepStrictEqual(index.before[key],index.after[key]),'MANUAL_UNRELATED_SOURCE_CHANGED');
 for(const key of KEYS.filter(key=>key!=='turn'))need(index.before.chapters[key]===index.after.chapters[key],'MANUAL_OTHER_CHAPTER_CHANGED');
 need(index.before.video===index.manual_derivatives?.['before-video.json']&&index.after.video===index.manual_derivatives?.['after-video.json']&&index.after.series===index.manual_derivatives?.['series.json']&&index.after.claims===index.manual_derivatives?.['after-claims.md']&&index.after.script===index.manual_derivatives?.['after-script.md'],'MANUAL_DERIVATIVE_SOURCE_HASH_INVALID');
 for(const name of derivativeNames)need(index.manual_derivatives[name]===hash(root,rel+'/'+name),'MANUAL_DERIVATIVE_EVIDENCE_HASH_INVALID');
 const chapters=Object.fromEntries(KEYS.map(key=>[key,bytes(root,rel+'/chapter-'+key+'.json')]));
 for(const key of KEYS)need(sha(chapters[key])===index.after.chapters[key],'MANUAL_CHAPTER_EVIDENCE_HASH_INVALID');
 need(sha(chapters.turn)===sha(afterTurn),'MANUAL_TURN_EVIDENCE_MISMATCH');
 const expected=manualDerivativeBytes({series:bytes(root,rel+'/series.json'),chapters:{...chapters,beforeTurn},beforeVideo:bytes(root,rel+'/before-video.json'),root});
 for(const [name,wanted] of Object.entries(expected))need(bytes(root,rel+'/'+name).equals(wanted),'MANUAL_DERIVATIVE_RECOMPOSE_MISMATCH_'+name);
}
export function checkRound12Model(root,rel,index,kind){
 assertModelEventScope(kind,index.before,index.after);
 const hasTurn=kind==='listener_drop'||kind==='turn_verifier';
 need(hasTurn===Boolean(index.turn_evidence),'ROUND12_TURN_EVIDENCE_MISSING_OR_EXTRA');
 if(!hasTurn)return;
 const before=bytes(root,rel+'/before-turn.json'),after=bytes(root,rel+'/after-turn.json');
 need(index.turn_evidence.before_sha256===sha(before)&&index.turn_evidence.after_sha256===sha(after),'ROUND12_TURN_EVIDENCE_HASH_INVALID');
 need(index.before.chapters.turn===sha(before)&&index.after.chapters.turn===sha(after),'ROUND12_TURN_SOURCE_MISMATCH');
 if(kind==='listener_drop')assertListenerSavedExact(JSON.parse(before),JSON.parse(after));
 else assertSavedVerifierClaimsExact(JSON.parse(before),JSON.parse(after));
}
export function inspectReviewProgress({base82Root,progressRoot,...options}){
 const verified=verify82Fixture({...options,after82Root:base82Root});const old=files(base82Root),current=files(progressRoot);
 const mutable=new Set([SLUG+'/auto.json',DOC+'/video.json',DOC+'/claims.md',DOC+'/script.md',DOC+'/verify-1.md','docs/videos/lexicon.json',SLUG+'/review/narrative.json',...KEYS.map(k=>SLUG+'/story/chapters/'+k+'.json')]);
 for(const rel of old){need(current.includes(rel),'BASELINE_FILE_MISSING');if(!mutable.has(rel))need(hash(base82Root,rel)===hash(progressRoot,rel),'HISTORICAL_BYTES_CHANGED');}
 const audit=SLUG+'/story/recheck-audit';const priorIds=fs.readdirSync(at(base82Root,audit));const ids=fs.readdirSync(at(progressRoot,audit)).filter(id=>!priorIds.includes(id));
 need(ids.every(id=>/^[A-Za-z0-9._-]+$/.test(id)),'UNSAFE_EVENT_ID');
 const added=current.filter(rel=>!old.includes(rel));need(added.every(rel=>ids.some(id=>rel.startsWith(audit+'/'+id+'/'))),'UNEXPECTED_ADDED_FILE');
 const events=ids.map(id=>{const rel=audit+'/'+id;const index=JSON.parse(bytes(progressRoot,rel+'/index.json'));need(index.schema_version===1&&index.slug===SLUG&&['saved','manual_amendment'].includes(index.result_kind)&&index.install_receipt_sha256===verified.new_pins.install_receipt_sha256,'RECHECK_INDEX_INVALID');need(sha(JSON.stringify(index.before))===index.before_source_sha256&&sha(JSON.stringify(index.after))===index.after_source_sha256&&index.before_source_sha256!==index.after_source_sha256,'SOURCE_EDGE_INVALID');need(Array.isArray(index.journals)&&(index.result_kind==='manual_amendment'||index.journals.length>0),'REAL_JOURNALS_REQUIRED');const names=new Set();for(const row of index.journals){need(/^[a-f0-9]{64}\.json$/.test(row.name)&&!names.has(row.name),'JOURNAL_NAME_INVALID');names.add(row.name);const raw=bytes(progressRoot,rel+'/'+row.name);need(sha(raw)===row.sha256,'JOURNAL_HASH_INVALID');const record=JSON.parse(raw);need(record.schema_version===1&&/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i.test(record.request_key??'')&&record.request?.format==='drama'&&typeof record.site==='string','JOURNAL_IDENTITY_INVALID');let site;try{site=new URL(record.site);}catch{throw Error('JOURNAL_SITE_INVALID');}need(['http:','https:'].includes(site.protocol)&&!site.username&&!site.password&&!site.search&&!site.hash,'JOURNAL_SITE_INVALID');need(record.request?.slug===SLUG&&record.adopted===true&&record.receipt?.status==='succeeded'&&row.status==='succeeded'&&row.stage===record.request.stage&&row.variant===record.request.variant,'JOURNAL_NOT_ADOPTED_SUCCESS');need((row.variant==='story'&&['verifier','listener'].includes(row.stage))||(row.variant==='narrative'&&row.stage==='verifier')||(row.variant==='story'&&row.stage==='writer'&&record.request.payload?.chapter?.key==='now'&&Array.isArray(record.request.payload?.lint_errors)&&record.request.payload.lint_errors.some(e=>e.includes('now-01'))),'JOURNAL_SCOPE_INVALID');need(record.source_hash===sourceHash(normalizeRun(record.request))&&row.name===record.source_hash+'.json'&&canonicalJson(record.request)===canonicalJson(normalizeRun(record.request)),'JOURNAL_REQUEST_HASH_INVALID');validateRunReceipt(record.receipt,record);need(record.receipt_hash===sha(canonicalJson(record.receipt)),'JOURNAL_RECEIPT_HASH_INVALID');need(Array.isArray(record.adoption?.artifacts)&&record.adoption.artifacts.length>0,'ADOPTION_PROOFS_MISSING');
 const proofMap=new Map([['/var/lib/mokaair/video-work/'+SLUG+'/auto.json',index.after.auto],...['video','series','claims','script','verify'].map(k=>['/opt/mokaair/'+DOC+'/'+(k==='verify'?'verify-1.md':k+(['video','series'].includes(k)?'.json':'.md')),index.after[k]]),['/var/lib/mokaair/video-work/'+SLUG+'/review/narrative.json',index.after.narrative],...KEYS.map(k=>['/var/lib/mokaair/video-work/'+SLUG+'/story/chapters/'+k+'.json',index.after.chapters[k]])].filter(([,value])=>value!==null));
 need(record.adoption.artifacts.length===proofMap.size,'ADOPTION_PROOF_COUNT_INVALID');const proofNames=new Set();for(const proof of record.adoption.artifacts){need(typeof proof.path==='string'&&!proofNames.has(proof.path)&&proofMap.has(proof.path)&&/^[a-f0-9]{64}$/.test(proof.sha256)&&proof.sha256===proofMap.get(proof.path),'ADOPTION_PROOF_SOURCE_MISMATCH');proofNames.add(proof.path);}}
 if(index.result_kind==='manual_amendment')checkRound12Manual(progressRoot,rel,index);else need(fs.readdirSync(at(progressRoot,rel)).sort().join('|')===[...names,'index.json',...(index.turn_evidence?['before-turn.json','after-turn.json']:[])].sort().join('|'),'EXTRA_EVENT_FILE');return {id,index,index_sha256:hash(progressRoot,rel+'/index.json')};});
 let source=verified.new_pins.source_composite_sha256,tuple=JSON.parse(bytes(base82Root,audit+'/round22-existing-revision-d7c321dfb9871511/index.json')).after;const visited=new Set(),visitedSources=new Set([source]);let round12Step=0;const round12Edges=[];
 for(let n=0;n<events.length;n++){const next=events.filter(e=>e.index.before_source_sha256===source&&JSON.stringify(e.index.before)===JSON.stringify(tuple));need(next.length===1&&!visited.has(next[0].id),'RECHECK_CHAIN_FORK_OR_GAP');const event=next[0];
  if(source===ROUND12_SOURCE104||round12Step){
   round12Step++;round12Edges.push({id:event.id,before_source_sha256:event.index.before_source_sha256,after_source_sha256:event.index.after_source_sha256});
   const row=event.index.journals?.[0],request=row?JSON.parse(bytes(progressRoot,audit+'/'+event.id+'/'+row.name)).request:null;
   const valid=[
    event.index.result_kind==='saved'&&event.index.journals?.length===1&&row?.stage==='listener'&&row?.variant==='story'&&request?.payload?.chapter?.key==='turn',
    event.index.result_kind==='manual_amendment'&&event.index.journals?.length===0,
    event.index.result_kind==='saved'&&event.index.journals?.length===1&&row?.stage==='verifier'&&row?.variant==='story'&&request?.payload?.chapter?.key==='turn',
    event.index.result_kind==='saved'&&event.index.journals?.length===1&&row?.stage==='verifier'&&row?.variant==='narrative',
   ];
   need(round12Step<=4&&valid[round12Step-1],'ROUND12_SEQUENCE_OR_SCOPE_INVALID');
   if(round12Step!==2)checkRound12Model(progressRoot,audit+'/'+event.id,event.index,['listener_drop',null,'turn_verifier','narrative_panel'][round12Step-1]);
  }
  need(!visitedSources.has(event.index.after_source_sha256),'RECHECK_SOURCE_CYCLE');visited.add(event.id);source=event.index.after_source_sha256;visitedSources.add(source);tuple=event.index.after;}
 assertRound12Tip({links:82+events.length,source,events:round12Edges,source104:ROUND12_SOURCE104});
 const actual=sources(progressRoot);need(JSON.stringify(actual)===JSON.stringify(tuple)&&sha(JSON.stringify(actual))===source,'CURRENT_SOURCE_NOT_AT_TIP');
 return {schema_version:1,integrity:'ACTUAL_REVIEW_PROGRESS_CHAIN_PASS',links:82+events.length,source_sha256:source,round12_events:round12Edges,new_events:events.map(({id,index,index_sha256})=>({id,index_sha256,journals:index.journals})),production_status:'HOLD',paid_work_allowed:false};
}
