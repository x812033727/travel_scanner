// ROOT MUST READ BEFORE --execute. NEW PT/ID thumbnail.sub-only merge; never replay the consumed all8 headline helper or render/dub here.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
const ROOT='/workspace/travel_scanner_pdf', HOME='/workspace/work/ai-pdf-01', SLUG='ai-pdf-quotes-to-comparison';
const DOC=ROOT+'/docs/videos/'+SLUG, WORK=HOME+'/media/'+SLUG, REV=DOC+'/research/translation-reviews';
const BASE=HOME+'/thumbnail-fit-investigation-20261026', ADMISSION=BASE+'/pt-id-subline-adoption-admission.json';
const ROOT_ADMISSION_SHA='2f66edfe1cc077657ec03760cf7918cb1f1440054d4e7f18fbb1cdf1595c1abc';
const PROPOSAL=BASE+'/root-pt-id-short-subline-proposal.json', PROPOSAL_SHA='3ed57cde8a14bfcefb8252b5576491adbae319d2400c1c52ffd9fbe6c832f5e4';
const REVIEW=BASE+'/pt-id-short-subline-independent-review.json', REVIEW_SHA='656087f62043d44ed6c41d5370da3d0c38f31d555e1e61c72846c91b7f9862a6';
const ALL=['en','ja','ko','es','pt','id','vi','th'], LOCALES=['pt','id'], PREFIX='thumbnail-sublines-pt-id-20261026';
const HISTORY=REV+'/history/'+PREFIX, OUTCOME=HOME+'/pt-id-thumbnail-sublines-reviewed-source-adoption-20261026.json';
const START=HOME+'/pt-id-thumbnail-sublines-reviewed-source-adoption-20261026.started.json';
const SOURCE_OUTCOME=DOC+'/research/language-checkpoints/pt-id-thumbnail-sublines-reviewed-source-adoption-20261026.json';
const sha=b=>createHash('sha256').update(b).digest('hex'), digest=f=>sha(fs.readFileSync(f));
const read=f=>JSON.parse(fs.readFileSync(f,'utf8')), json=x=>JSON.stringify(x,null,2)+'\n';
const trFile=l=>DOC+'/i18n/'+l+'.json', idxFile=l=>REV+'/'+l+'.meaning-review.json';
const compositeRel=l=>'research/translation-reviews/'+l+'.thumbnail-subline-current-source-review-20261026.json';
const proposalRel='research/translation-reviews/'+PREFIX+'.root-proposal.json';
const reviewRel='research/translation-reviews/'+PREFIX+'.independent-metadata-delta-review.json';
const admissionRel='research/translation-reviews/'+PREFIX+'.root-current-source-admission.json';
if (process.argv.length===2 || process.argv[2]==='--help') {
  console.log('ROOT REVIEW FIRST; --execute only. Pinned current source admission; native PT/ID thumbnail.sub-only sheet/merge; preserve all eight voices/source controls. No render, paid request, owner action, approval or voice acceptance.'); process.exit(0);
}
assert.deepEqual(process.argv.slice(2),['--execute']);
let networkAttempts=0;
globalThis.fetch=()=>{ networkAttempts++; throw Error('Offline thumbnail source adoption forbids all fetch/provider requests'); };
const [{main},{acquireProjectLease,leaseHolder},{stopRequested},{loadProject},{dubRequests,translationHash,speechFingerprint}]=await Promise.all([
  import(ROOT+'/tools/video/cli.mjs'), import(ROOT+'/tools/video/core/project-lease.mjs'), import(ROOT+'/tools/video/core/paths.mjs'),
  import(ROOT+'/tools/video/core/state.mjs'), import(ROOT+'/tools/video/dubs/plan.mjs'),
]);
for (const f of [DOC,WORK,BASE]) assert.equal(fs.realpathSync(f),f,'Refuse redirected source/work directory');
for (const f of [ADMISSION,PROPOSAL,REVIEW]) assert(fs.lstatSync(f).isFile()&&!fs.lstatSync(f).isSymbolicLink());
assert.equal(digest(ADMISSION),ROOT_ADMISSION_SHA); assert.equal(digest(PROPOSAL),PROPOSAL_SHA); assert.equal(digest(REVIEW),REVIEW_SHA);
const admission=read(ADMISSION), proposal=read(PROPOSAL), metadataReview=read(REVIEW);
assert.equal(admission.schema_version,1); assert.equal(admission.author,'/root'); assert.equal(admission.slug,SLUG);
assert.deepEqual(admission.locales,LOCALES); assert.deepEqual(Object.keys(admission.translations),LOCALES); assert.deepEqual(Object.keys(admission.protected_translations),ALL);
assert.deepEqual(admission.proposal,{file:PROPOSAL,sha256:PROPOSAL_SHA}); assert.deepEqual(admission.metadata_review,{file:REVIEW,sha256:REVIEW_SHA});
assert.equal(admission.source_video_sha256,'eac88936fbcb0324208d639b75ddad8f045c6bcc3cc8c4f60d89ebc6c65f3e04');
assert.equal(proposal.slug,SLUG); assert.equal(proposal.author,'/root'); assert.equal(proposal.not_adopted,true);
assert.deepEqual(proposal.rows.map(r=>r.locale),LOCALES); assert.deepEqual(metadataReview.locale_reviews.map(r=>r.locale),LOCALES);
assert.equal(metadataReview.slug,SLUG); assert.equal(metadataReview.passed,true); assert.deepEqual(metadataReview.issues,[]);
assert.equal(metadataReview.independent_from_root_proposal_author,true); assert.equal(metadataReview.proposal_sha256,PROPOSAL_SHA);
assert.equal(metadataReview.source_video_sha256,admission.source_video_sha256); assert.deepEqual(metadataReview.reviewed_boundaries,[]);
const project=loadProject({slug:SLUG,root:ROOT}), beforeTr={}, beforeIdx={}, beforeBytes={}, expectedTr={}, expectedIdx={}, protectedIndicesBefore={}, logs=[], applied=[];
for (const l of ALL) { const tb=fs.readFileSync(trFile(l)), t=JSON.parse(tb); assert.equal(sha(tb),admission.protected_translations[l]); assert.equal(Object.keys(t.lines).length,101); assert.deepEqual(project.translations[l],t); beforeTr[l]=t; expectedTr[l]=sha(tb); expectedIdx[l]=digest(idxFile(l)); protectedIndicesBefore[l]=expectedIdx[l]; }
const projection=t=>Object.fromEntries(['title','description','tags','chapters','thumbnail'].map(k=>[k,t[k]]));
function safeReport(rel) {
  assert(typeof rel==='string'&&!path.isAbsolute(rel)); const f=path.resolve(DOC,rel), real=fs.realpathSync(f);
  assert(f.startsWith(DOC+'/')&&real.startsWith(DOC+'/')&&fs.lstatSync(f).isFile()&&!fs.lstatSync(f).isSymbolicLink()); return f;
}
function boundaries(locale,index) {
  assert(Array.isArray(index.reviewed_boundaries));
  for (const row of index.reviewed_boundaries) {
    assert(row.file.startsWith('author-review-boundaries/')&&!row.file.includes('..'));
    assert.equal(digest(path.join(HOME,row.file)),row.sha256,'Prior reviewed boundary changed');
  }
  const dir=HOME+'/author-review-boundaries';
  for (const name of fs.readdirSync(dir).filter(n=>new RegExp('^'+locale+'\\.(shorten|reword)\\.round-[12]\\..+\\.json$').test(n))) {
    const file='author-review-boundaries/'+name, h=digest(HOME+'/'+file);
    assert(index.reviewed_boundaries.some(b=>b.file===file&&b.sha256===h),'Current model boundary lacks actual prior meaning review');
  }
}
for (const [n,l] of LOCALES.entries()) {
  const pin=admission.translations[l], tb=fs.readFileSync(trFile(l)), ib=fs.readFileSync(idxFile(l));
  assert.equal(sha(tb),pin.translation_sha256); assert.equal(sha(ib),pin.meaning_index_sha256);
  const t=JSON.parse(tb), i=JSON.parse(ib), p=proposal.rows[n], m=metadataReview.locale_reviews[n];
  assert.equal(i.schema_version,1); assert.equal(i.slug,SLUG); assert.equal(i.locale,l); assert.equal(i.passed,true);
  assert.equal(i.scope,'source-meaning-and-naturalness'); assert.equal(i.source_video_sha256,admission.source_video_sha256);
  assert.equal(i.translation_sha256,sha(tb)); assert.equal(i.report_file,pin.report_file); assert.equal(i.report_sha256,pin.report_sha256);
  const rf=safeReport(i.report_file), r=read(rf); assert.equal(digest(rf),pin.report_sha256); assert.equal(r.passed,true);
  assert.equal(r.source_video_sha256,admission.source_video_sha256); assert.equal(r.translation_sha256,sha(tb)); boundaries(l,i);
  assert.equal(Object.keys(t.lines).length,101); assert.deepEqual(t.thumbnail,p.before_thumbnail);
  assert.equal(m.passed,true); assert.deepEqual(m.issues,[]); assert.deepEqual(m.before_thumbnail,p.before_thumbnail);
  assert.deepEqual(m.proposed_thumbnail,p.proposed_thumbnail); assert.deepEqual(m.actual_full_metadata_read,projection(t),'Metadata reviewer did not read these exact metadata');
  const restored=structuredClone(p.proposed_thumbnail); restored.sub=t.thumbnail.sub; assert.deepEqual(restored,t.thumbnail);
  assert.equal(p.only_proposed_field,'thumbnail.sub'); assert.equal(p.proposed_thumbnail.sub,({pt:'Imposto + frete',id:'Pajak + ongkir'})[l]); assert(!p.proposed_thumbnail.sub.includes(String.fromCharCode(10))&&!p.proposed_thumbnail.sub.includes(String.fromCharCode(13))&&!/[<>]/.test(p.proposed_thumbnail.sub));
  beforeTr[l]=t; beforeIdx[l]=i; beforeBytes[l]={translation:tb,index:ib}; expectedTr[l]=sha(tb); expectedIdx[l]=sha(ib);
}
const fingerprint=p=>Object.fromEntries(ALL.map(l=>{ const d=dubRequests(p,l); assert.deepEqual(d.missing,[]); return [l,{translation_hash:translationHash(d.script),speech_fingerprint:speechFingerprint(d.requests)}]; }));
const fingerprintsBefore=fingerprint(project);
for (const f of [OUTCOME,START,SOURCE_OUTCOME,HISTORY,BASE+'/pt-id-subline-runtime-before.json',BASE+'/pt-id-subline-runtime-after.json',DOC+'/'+proposalRel,DOC+'/'+reviewRel,DOC+'/'+admissionRel,...LOCALES.map(l=>DOC+'/'+compositeRel(l))]) assert(!fs.existsSync(f),'One-use output exists; inspect, never replay: '+f);
let lease;
try { assert(leaseHolder(WORK)===null,'A project lease exists; do not take it'); assert(!stopRequested(WORK)&&!stopRequested(HOME)); lease=acquireProjectLease(WORK,{owner:'codex-ai-video-pdf-reviewed-PT-ID-thumbnail-sub-only'}); }
catch (error) { throw Error('Metadata adoption refused before writes: '+error.message); } // Never expose a lease record/token.
function guard() {
  lease.verify(); assert(!stopRequested(WORK)&&!stopRequested(HOME),'STOP preserves the stopped project');
  assert.equal(digest(DOC+'/video.json'),admission.source_video_sha256); assert.equal(digest(ADMISSION),ROOT_ADMISSION_SHA);
  assert.equal(digest(PROPOSAL),PROPOSAL_SHA); assert.equal(digest(REVIEW),REVIEW_SHA);
  for (const l of LOCALES) assert.equal(digest(safeReport(admission.translations[l].report_file)),admission.translations[l].report_sha256);
}
function verifySources() { guard(); for (const l of ALL) { assert.equal(digest(trFile(l)),expectedTr[l]); assert.equal(digest(idxFile(l)),expectedIdx[l]); } }
function snapshot() {
  const rows={}; function visit(at) { for (const e of fs.readdirSync(at,{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name))) {
    const f=path.join(at,e.name), rel=path.relative(WORK,f); if (rel==='LEASE') continue;
    assert(!e.isSymbolicLink(),'No symlink in runtime snapshot'); if (e.isDirectory()) visit(f); else { assert(e.isFile()); rows[rel]={sha256:digest(f),size:fs.statSync(f).size}; }
  }} visit(WORK); return rows;
}
const write=(f,b,replace=false)=>{ guard(); fs.writeFileSync(f,b,{flag:replace?'w':'wx',mode:0o600}); };
const native=async args=>{ verifySources(); assert.equal(await main([...args,'--slug',SLUG],{root:ROOT,here:ROOT+'/tools/video',env:{...process.env,VIDEO_WORKDIR:HOME+'/media'},stdout:{write:s=>logs.push(String(s))},stderr:{write:s=>logs.push(String(s))}}),0); guard(); };
const startedAt=new Date().toISOString(); let before=null;
try {
  verifySources(); write(START,json({started_at_utc:startedAt,admission_sha256:ROOT_ADMISSION_SHA,helper_sha256:digest(path.resolve(process.argv[1])),pid:process.pid,scope:'ONE OFFLINE PT/ID thumbnail.sub-ONLY ADOPTION; all8spoken/source controls preserved, not a completed outcome'}));
  before=snapshot(); write(BASE+'/pt-id-subline-runtime-before.json',json(before)); guard(); fs.mkdirSync(HISTORY);
  for (const l of LOCALES) { write(HISTORY+'/'+l+'.prior-translation.json',beforeBytes[l].translation); write(HISTORY+'/'+l+'.prior-meaning-index.json',beforeBytes[l].index); }
  for (const [from,rel] of [[PROPOSAL,proposalRel],[REVIEW,reviewRel],[ADMISSION,admissionRel]]) write(DOC+'/'+rel,fs.readFileSync(from));
  for (const [n,l] of LOCALES.entries()) {
    await native(['i18n-sheet','--locale',l,'--parts','metadata']);
    const sf=WORK+'/i18n/'+l+'.todo.json', sheet=read(sf), saved=structuredClone(sheet), p=proposal.rows[n];
    assert.equal(sheet.slug,SLUG); assert.equal(sheet.locale,l); assert.deepEqual(sheet.parts,['metadata']); assert.deepEqual(sheet.lines,[]);
    assert.deepEqual(sheet.thumbnail.text,beforeTr[l].thumbnail);
    for (const k of ['title','description','tags']) assert.deepEqual(sheet[k].text,beforeTr[l][k]);
    assert.deepEqual(Object.fromEntries(sheet.chapters.map(c=>[c.scene,c.text])),beforeTr[l].chapters);
    sheet.thumbnail.text.sub=p.proposed_thumbnail.sub;
    const restoredSheet=structuredClone(sheet); restoredSheet.thumbnail.text.sub=saved.thumbnail.text.sub; assert.deepEqual(restoredSheet,saved);
    write(sf,json(sheet),true); await native(['i18n-merge','--locale',l]);
    const now=read(trFile(l)), restored=structuredClone(now); restored.thumbnail.sub=beforeTr[l].thumbnail.sub;
    assert.deepEqual(restored,beforeTr[l],'Only selected PT/ID thumbnail.sub may change'); assert.deepEqual(now.thumbnail,p.proposed_thumbnail);
    assert.equal(JSON.stringify(now.lines),JSON.stringify(beforeTr[l].lines),'All101 spoken line records must remain byte-object-exact');
    expectedTr[l]=digest(trFile(l)); applied.push(l); verifySources();
  }
  const after=snapshot(), changed=[...new Set([...Object.keys(before),...Object.keys(after)])].filter(p=>JSON.stringify(before[p])!==JSON.stringify(after[p]));
  const allowed=[...LOCALES.map(l=>'i18n/'+l+'.todo.json'),'state.json']; assert(changed.every(p=>allowed.includes(p)),'Unexpected runtime write: '+changed.join(','));
  const afterProject=loadProject({slug:SLUG,root:ROOT}), fingerprintsAfter=fingerprint(afterProject); assert.deepEqual(fingerprintsAfter,fingerprintsBefore); assert.equal(networkAttempts,0);
  for (const l of ALL) assert.equal(JSON.stringify(afterProject.translations[l].lines),JSON.stringify(beforeTr[l].lines),'All8 locales preserve all101 spoken records');
  const other6=ALL.filter(l=>!LOCALES.includes(l)); for (const l of other6) { assert.equal(digest(trFile(l)),admission.protected_translations[l]); assert.equal(digest(idxFile(l)),protectedIndicesBefore[l]); }
  for (const l of LOCALES) {
    const prior=beforeIdx[l], composite={schema_version:1,slug:SLUG,locale:l,scope:'source-meaning-and-naturalness',passed:true,
      reviewer:'Prior genuine current meaning chain plus independent metadata delta by '+metadataReview.reviewer+'; exact preservation binding by /root',
      source_video_sha256:admission.source_video_sha256,translation_sha256:expectedTr[l],
      prior_current_meaning_index:{file:'research/translation-reviews/history/'+PREFIX+'/'+l+'.prior-meaning-index.json',sha256:sha(beforeBytes[l].index),index:prior},
      prior_translation:{file:'research/translation-reviews/history/'+PREFIX+'/'+l+'.prior-translation.json',sha256:sha(beforeBytes[l].translation)},
      independent_metadata_delta:{report_file:reviewRel,report_sha256:REVIEW_SHA,proposal_file:proposalRel,proposal_sha256:PROPOSAL_SHA,changed_field:'thumbnail.sub',new_spoken_review_claimed:false},
      all101_spoken_records_and_all_other_translation_fields_exact:true,native_dub_fingerprints_unchanged:fingerprintsAfter[l],
      reviewed_boundaries:structuredClone(prior.reviewed_boundaries),future_model_boundary_review_claimed:false,actual_render_fit_audio_voice_or_fullpackage_approval_claimed:false,paid_requests:0};
    const rel=compositeRel(l); write(DOC+'/'+rel,json(composite));
    const index={...prior,reviewer:composite.reviewer,translation_sha256:expectedTr[l],report_file:rel,report_sha256:digest(DOC+'/'+rel)};
    assert.deepEqual(index.reviewed_boundaries,prior.reviewed_boundaries); write(idxFile(l),json(index),true); expectedIdx[l]=digest(idxFile(l)); verifySources();
  }
  const finalRuntime=snapshot(); assert.deepEqual(finalRuntime,after,'Meaning-index-only writes must not affect runtime'); write(BASE+'/pt-id-subline-runtime-after.json',json(finalRuntime));
  const outcome={schema_version:1,slug:SLUG,started_at_utc:startedAt,finished_at_utc:new Date().toISOString(),status:'REVIEWED PT/ID THUMBNAIL SUBLINES ADOPTED / IMAGES NOT RENDERED',
    helper_sha256:digest(path.resolve(process.argv[1])),admission_sha256:ROOT_ADMISSION_SHA,source_video_sha256:admission.source_video_sha256,proposal_sha256:PROPOSAL_SHA,independent_metadata_review_sha256:REVIEW_SHA,
    translations_before:Object.fromEntries(LOCALES.map(l=>[l,admission.translations[l].translation_sha256])),translations_after:Object.fromEntries(LOCALES.map(l=>[l,expectedTr[l]])),meaning_indices_after:Object.fromEntries(LOCALES.map(l=>[l,expectedIdx[l]])),
    all8_translations_before:admission.protected_translations,all8_translations_after:expectedTr,other6_translations_and_indices_byte_exact:true,other6_indices_before:Object.fromEntries(other6.map(l=>[l,protectedIndicesBefore[l]])),other6_indices_after:Object.fromEntries(other6.map(l=>[l,digest(idxFile(l))])),
    runtime_before:{file:BASE+'/pt-id-subline-runtime-before.json',sha256:digest(BASE+'/pt-id-subline-runtime-before.json'),files:Object.keys(before).length},
    runtime_after:{file:BASE+'/pt-id-subline-runtime-after.json',sha256:digest(BASE+'/pt-id-subline-runtime-after.json'),files:Object.keys(after).length},
    actual_runtime_changes:changed,all_other_runtime_files_byte_exact:true,all8_locales_all101_spoken_records_exact:true,selected2_other_metadata_and_other6_whole_sources_exact:true,
    native_fingerprints_before:fingerprintsBefore,native_fingerprints_after:fingerprintsAfter,prior_reviewed_boundaries_preserved:true,native_logs:logs,
    network_attempts:networkAttempts,render_provider_TTS_ASR_owner_approval_publish_requests:0,actual_fit_visual_voice_or_fullpackage_QA_claimed:false,
    next:'Supported native render --thumbnails-only under the actual canonical project lease with all raw/primary guards, then actual full/mobile visual checks; keep the old consumed scratch untouched. Stopped voices/caps/unknowns and real owner choice remain unchanged.'};
  verifySources(); write(OUTCOME,json(outcome)); write(SOURCE_OUTCOME,json(outcome)); console.log(json({outcome:OUTCOME,sha256:digest(OUTCOME),translations_after:Object.fromEntries(LOCALES.map(l=>[l,expectedTr[l]])),voice_pass_claimed:false}));
} catch (error) {
  // Preserve every partial native write. This consumed marker prevents a blind replay; no rollback, reset or false index is created.
  if (fs.existsSync(START)&&!fs.existsSync(OUTCOME)) fs.writeFileSync(OUTCOME,json({slug:SLUG,status:'FAILED / PARTIAL OUTCOME / DO NOT REPLAY',at_utc:new Date().toISOString(),error:error.message,applied_locales:applied,started_marker:START,admission_sha256:ROOT_ADMISSION_SHA,native_logs:logs,network_attempts:networkAttempts,voice_or_fit_approval_claimed:false}),{flag:'wx',mode:0o600});
  throw Error('Metadata-only adoption stopped: '+error.message); // Drop native assertion/lease object properties from terminal output.
} finally { lease.release(); }
