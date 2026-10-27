// ROOT REVIEW FIRST. Fill only the exact hash of the genuine post-adoption admission.
// One native canonical render; no scratch-copy adoption, provider calls, voice or publishing.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
const ROOT_ADMISSION_SHA = '771a5d71c9d6e4474fd4c85f03046f7720a1c3957630c841297d095f854d09bc';
const ROOT='/workspace/travel_scanner_pdf', HOME='/workspace/work/ai-pdf-01', SLUG='ai-pdf-quotes-to-comparison';
const WORK=HOME+'/media/'+SLUG, DOC=ROOT+'/docs/videos/'+SLUG;
const ADMISSION=HOME+'/thumbnail-fit-investigation-20261026/native-render-admission.json';
const OUT=HOME+'/localized-thumbnail-native-adoption-20261026';
const LOCALES=['en','ja','ko','es','pt','id','vi','th'];
const SOURCE='eac88936fbcb0324208d639b75ddad8f045c6bcc3cc8c4f60d89ebc6c65f3e04';
const FINAL='346a5bbd4b47884f301a9dfc9b67fe81e1a504232a0f4746e60ddead54d94e3f';
const hash=b=>createHash('sha256').update(b).digest('hex'), sha=p=>hash(fs.readFileSync(p));
const read=p=>JSON.parse(fs.readFileSync(p,'utf8')), json=j=>JSON.stringify(j,null,2)+'\n';
const hex=s=>typeof s==='string'&&/^[a-f0-9]{64}$/.test(s);
if (process.argv.length===2 || process.argv[2]==='--help') { console.log('ROOT REVIEW FIRST: fill ROOT_ADMISSION_SHA; --execute performs ONE guarded native render --thumbnails-only.'); process.exit(0); }
assert.deepEqual(process.argv.slice(2),['--execute']); assert(hex(ROOT_ADMISSION_SHA),'Root must pin the real post-adoption admission first');
const networkAttempts=[];
globalThis.fetch=(...args)=>{networkAttempts.push({argument_type:typeof args[0]});throw Error('Canonical thumbnail-only render forbids Node fetch/provider requests');};
process.env.PLAYWRIGHT_BROWSERS_PATH ??= '/workspace/work/ai-animation-01/browsers';
const [{main},{openRenderer},{localizedThumbnails},{renderPlan,themeHash},{loadProject},{acquireProjectLease,leaseHolder},{stopRequested},{approvalState},{localizedThumbnailHash,thumbnailStatus},{visualHash},{THUMB_SIZE},{thumbnailChecks,imageSize}]=await Promise.all([
 import(ROOT+'/tools/video/cli.mjs'),import(ROOT+'/tools/video/render/browser.mjs'),import(ROOT+'/tools/video/render/cli.mjs'),import(ROOT+'/tools/video/render/plan.mjs'),import(ROOT+'/tools/video/core/state.mjs'),import(ROOT+'/tools/video/core/project-lease.mjs'),import(ROOT+'/tools/video/core/paths.mjs'),import(ROOT+'/tools/video/core/approvals.mjs'),import(ROOT+'/tools/video/core/translations.mjs'),import(ROOT+'/tools/video/core/timeline.mjs'),import(ROOT+'/tools/video/templates/templates.mjs'),import(ROOT+'/tools/video/qa/thumbnail.mjs')
]);
function file(p) { const s=fs.lstatSync(p);assert(s.isFile()&&!s.isSymbolicLink(),'Expected regular file: '+p);return {sha256:sha(p),bytes:s.size}; }
function tree(dir) { const rows={};const walk=p=>{for(const e of fs.readdirSync(p,{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name))){const f=path.join(p,e.name),r=path.relative(dir,f).split(path.sep).join('/');if(dir===WORK&&r==='LEASE')continue;assert(!e.isSymbolicLink(),'Symlink in protected tree: '+f);if(e.isDirectory())walk(f);else rows[r]=file(f);}};walk(dir);return rows; }
assert.equal(sha(ADMISSION),ROOT_ADMISSION_SHA);const admission=read(ADMISSION);
assert.equal(admission.schema_version,1);assert.equal(admission.slug,SLUG);assert.equal(admission.source_video_sha256,SOURCE);
for(const name of ['translation_sha256','meaning_index_sha256']) { assert.deepEqual(Object.keys(admission[name]??{}).sort(),[...LOCALES].sort());LOCALES.forEach(l=>assert(hex(admission[name][l]))); }
assert.equal(admission.approved_final_sha256,FINAL);assert(hex(admission.primary_qa_sha256));
const adoption=admission.metadata_adoption_receipt;assert(adoption&&hex(adoption.sha256));
assert(path.isAbsolute(adoption.file)&&path.resolve(adoption.file)===adoption.file&&adoption.file.startsWith(HOME+'/'),'Adoption receipt must be the exact external film file');
assert.equal(fs.realpathSync(adoption.file),adoption.file,'Adoption receipt cannot use symlink aliases');
const pins={'video.json':admission.source_video_sha256,...Object.fromEntries(LOCALES.map(l=>['i18n/'+l+'.json',admission.translation_sha256[l]])),...Object.fromEntries(LOCALES.map(l=>['research/translation-reviews/'+l+'.meaning-review.json',admission.meaning_index_sha256[l]]))};
function sourceSnapshot() { return Object.fromEntries(Object.keys(pins).map(r=>[r,file(DOC+'/'+r)])); }
function verifyPins() {
 assert.equal(sha(ADMISSION),ROOT_ADMISSION_SHA);assert.equal(file(adoption.file).sha256,adoption.sha256);assert.equal(sha(WORK+'/review/qa.json'),admission.primary_qa_sha256);
 for(const [r,h] of Object.entries(pins))assert.equal(file(DOC+'/'+r).sha256,h,'Changed source/index pin: '+r);
 for(const l of LOCALES){const i=read(DOC+'/research/translation-reviews/'+l+'.meaning-review.json');assert.equal(i.passed,true);assert.equal(i.scope,'source-meaning-and-naturalness');assert.equal(i.source_video_sha256,admission.source_video_sha256);assert.equal(i.translation_sha256,admission.translation_sha256[l]);const rp=path.resolve(DOC,i.report_file??'');assert(rp.startsWith(DOC+'/')&&fs.realpathSync(rp).startsWith(DOC+'/'));assert.equal(file(rp).sha256,i.report_sha256);}
 const qa=read(WORK+'/review/qa.json');assert.equal(qa.ok,true);assert.equal(qa.final_sha256,FINAL);assert.equal(qa.items?.length,11);assert(qa.items.every(r=>r.ok===true));
}
assert.equal(fs.realpathSync(WORK),WORK);assert.equal(fs.realpathSync(DOC),DOC);assert(!fs.existsSync(OUT),'Consumed one-use output exists; never overwrite or replay');
assert.equal(leaseHolder(WORK),null,'Project has a holder; leave it untouched');assert(!stopRequested(WORK));verifyPins();
const lease=acquireProjectLease(WORK,{owner:'codex-ai-video-pdf-reviewed-localized-thumbnails-native-render'});
let admitted=false,before=null,sourceBefore=null,nativeCode=null,errorMessage=null,after=null,sourceAfter=null,logFd=null,journalFd=null;
const started=new Date().toISOString(),captures=[],qaResults=[];let project=null,oldManifest=null,oldState=null;
const strip=m=>{const x={...m};delete x.thumbnail_locales;delete x.thumbnail_locale_gaps;return x;};
const write=(name,data)=>fs.writeFileSync(OUT+'/'+name,data,{flag:'wx',mode:0o600});
const verify=()=>{lease.verify();assert(!stopRequested(WORK),'STOP holds canonical thumbnail render');verifyPins();};
try {
 verify();const approved=await approvalState({gate:'final',docDir:DOC,workdir:WORK});assert.equal(approved.status,'approved');assert.equal(approved.sha256,FINAL);assert.equal(sha(WORK+'/final.mp4'),FINAL);
 fs.mkdirSync(OUT);admitted=true;write('ONE_USE_ADMISSION.json',json({started_at_utc:started,pid:process.pid,helper_sha256:sha(process.argv[1]),admission_sha256:ROOT_ADMISSION_SHA,workdir:WORK,canonical_native_thumbnail_render_only:true,visual_review_pending:true}));
 logFd=fs.openSync(OUT+'/native-render.log','wx',0o600);journalFd=fs.openSync(OUT+'/actual-capture-journal.jsonl','wx',0o600);fs.mkdirSync(OUT+'/diagnostic-captures');
 before=tree(WORK);sourceBefore=sourceSnapshot();write('runtime.before.json',json(before));write('source-pins.before.json',json(sourceBefore));oldManifest=read(WORK+'/frames/manifest.json');oldState=read(WORK+'/state.json');
 project=loadProject({slug:SLUG,root:ROOT});assert.equal(oldManifest.visual_hash,visualHash(project.doc));assert(project.doc.thumbnail&&!project.doc.thumbnail.variants&&!project.doc.thumbnail.data.capture&&!project.doc.thumbnail.data.shot,'Review any non-stock/variant dependency separately');
 assert(LOCALES.every(l=>thumbnailStatus(project.doc,project.translations[l])==='current'));
 const plan=renderPlan(project.doc,themeHash(),ROOT,{translations:project.translations,workdir:WORK});const localized=localizedThumbnails(plan);
 assert.equal(localized.drawable.length,8);assert.deepEqual(Object.keys(localized.gaps),[]);assert.deepEqual(localized.drawable.map(x=>x.locale).sort(),[...LOCALES].sort());
 const byKey=new Map(localized.drawable.map(x=>[x.key,x]));assert.equal(byKey.size,8);
 const wrappedRenderer=async options=>{
  verify();assert.equal(options.root,ROOT);assert.equal(options.workdir,WORK);const native=await openRenderer(options);
  return {capture:async(key,html,opts)=>{
   verify();const own=byKey.get(key);assert(own&&own.html===html,'Refuse body/primary/unknown capture');assert.equal(opts.type,'jpeg');assert.equal(opts.quality,90);assert.equal(opts.transition??false,false);assert.deepEqual(opts.size,THUMB_SIZE);assert(!captures.some(r=>r.locale===own.locale),'Duplicate locale capture');
   const result=await native.capture(key,html,opts);assert(Buffer.isBuffer(result.still));assert(Array.isArray(result.problems));assert.equal(result.frames.length,0);
   const row={locale:own.locale,native_key:key,native_thumbnail_hash:own.hash,html_sha256:hash(html),actual_jpeg_sha256:hash(result.still),bytes:result.still.length,actual_image_size:imageSize(result.still),native_viewport:opts.size,native_layout_font_image_brand_problems:[...result.problems]};
   const qa=thumbnailChecks({bytes:result.still,headline:project.translations[own.locale].thumbnail.headline,title:project.translations[own.locale].title,locale:own.locale});qaResults.push({locale:own.locale,...qa});
   captures.push(row);fs.writeSync(journalFd,JSON.stringify({...row,native_thumbnail_qa:qa})+'\n');fs.fsyncSync(journalFd);write('diagnostic-captures/'+own.locale+'.NOT_VISUALLY_REVIEWED.jpg',result.still);
   verify();return result; // Preserve actual capture first; verify immediately before native canonical JPEG write.
  },sheet:async()=>{throw Error('Contact sheet/body/primary render is forbidden');},close:async()=>{await native.close();verify();}};
 };
 const output={write:s=>{fs.writeSync(logFd,String(s));fs.fsyncSync(logFd);process.stdout.write(s);}};
 verify();nativeCode=await main(['render','--slug',SLUG,'--thumbnails-only'],{root:ROOT,here:ROOT+'/tools/video',env:{...process.env,VIDEO_WORKDIR:HOME+'/media'},stdout:output,stderr:output,openRenderer:wrappedRenderer});verify();
 assert.equal(nativeCode,0,'Actual native render failed');const manifest=read(WORK+'/frames/manifest.json');assert.deepEqual(strip(manifest),strip(oldManifest),'Primary/body manifest changed');
 assert.deepEqual(Object.keys(manifest.thumbnail_locales??{}).sort(),[...LOCALES].sort());assert.deepEqual(Object.keys(manifest.thumbnail_locale_gaps??{}),[]);assert.equal(captures.length,8);
 for(const l of LOCALES){const row=captures.find(r=>r.locale===l),m=manifest.thumbnail_locales[l];assert.equal(m.file,'thumbnails/'+l+'.jpg');assert.equal(m.hash,localizedThumbnailHash(project.doc,project.translations[l]));const bytes=fs.readFileSync(WORK+'/'+m.file);assert.equal(hash(bytes),row.actual_jpeg_sha256);assert.deepEqual(row.actual_image_size,{format:'jpeg',height:720,width:1280});assert(bytes.length<=2*1024*1024);assert.deepEqual(row.native_layout_font_image_brand_problems,[]);const qa=qaResults.find(r=>r.locale===l);assert.equal(qa.ok,true,l+' failed native phone/thumbnail QA: '+qa.detail);}
 const state=read(WORK+'/state.json');assert.equal(state.runs.length,oldState.runs.length+1);assert.deepEqual(state.runs.slice(0,-1),oldState.runs);assert.deepEqual({...state,runs:[]},{...oldState,runs:[]});const run=state.runs.at(-1);assert.equal(run.stage,'render');assert.equal(run.thumbnails_only,true);assert.deepEqual([...run.drawn].sort(),[...LOCALES].sort());
 assert.equal(networkAttempts.length,0,'Node/provider fetch was attempted');verify();
} catch(error) { errorMessage=String(error.message);process.exitCode=1;console.error('Native thumbnail-only guard stopped: '+errorMessage); }
finally {
 try { if(admitted){
  try{after=tree(WORK);sourceAfter=sourceSnapshot();write('runtime.after.json',json(after));write('source-pins.after.json',json(sourceAfter));if(sourceBefore)assert.deepEqual(sourceAfter,sourceBefore,'Source/index pins changed');if(before){const changes=[...new Set([...Object.keys(before),...Object.keys(after)])].filter(r=>JSON.stringify(before[r])!==JSON.stringify(after[r]));const allowed=new Set(['frames/manifest.json','state.json',...LOCALES.map(l=>'thumbnails/'+l+'.jpg')]);assert(changes.every(r=>allowed.has(r)),'Unexpected protected runtime changes: '+changes.filter(r=>!allowed.has(r)).join(','));if(oldManifest)assert.deepEqual(strip(read(WORK+'/frames/manifest.json')),strip(oldManifest),'Primary/body manifest changed');const oldState=before['state.json'];assert(oldState,'Expected existing native state.json');}}
  catch(e){errorMessage=[errorMessage,String(e.message)].filter(Boolean).join('; ');process.exitCode=1;}
  const changed=before&&after?[...new Set([...Object.keys(before),...Object.keys(after)])].filter(r=>JSON.stringify(before[r])!==JSON.stringify(after[r])):null;
  write('actual-captures.json',json(captures));write('actual-thumbnail-qa.json',json(qaResults));write('actual-outcome.json',json({schema_version:1,slug:SLUG,started_at_utc:started,ended_at_utc:new Date().toISOString(),admission_sha256:ROOT_ADMISSION_SHA,native_command:['render','--slug',SLUG,'--thumbnails-only'],native_exit_code:nativeCode,guard_passed:errorMessage===null,error:errorMessage,changed_runtime_paths:changed,all_other_runtime_files_byte_exact:before!==null&&after!==null&&changed.every(r=>new Set(['frames/manifest.json','state.json',...LOCALES.map(l=>'thumbnails/'+l+'.jpg')]).has(r)),source_pins_unchanged:sourceBefore!==null&&sourceAfter!==null&&JSON.stringify(sourceBefore)===JSON.stringify(sourceAfter),actual_captures:captures,native_thumbnail_qa:qaResults,actual_geometry_scope:'Native1280x720 viewport and actual JPEG dimensions plus unchanged native layout/font/image/brand problem reports; no computed-browser-font-size claim',phone_rule_scope:'Unchanged native thumbnailChecks minimum24px at320px, an estimate distinct from required actual visual inspection',node_network_attempts:networkAttempts,visual_review_pending:true,body_or_primary_redrawn:false,voice_or_full8package_approval_claimed:false,owner_action_upload_or_publication:false,next:'Actually inspect all8 canonical JPEGs at full and mobile size before calling visual QA passed. Preserve any failed native/code/fit/QA result and consumed output; never replay this one-use directory or adopt diagnostic copies manually.'}));
 }} finally { try { if(logFd!==null)fs.closeSync(logFd);if(journalFd!==null)fs.closeSync(journalFd); } finally { lease.release(); } }
}
