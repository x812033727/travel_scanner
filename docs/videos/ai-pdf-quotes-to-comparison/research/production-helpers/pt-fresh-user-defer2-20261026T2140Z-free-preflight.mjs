// ONE root-authorized nonpaid preflight. Never sends non-GET or writes canonical source/media.
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';
import { acquireProjectLease } from '/workspace/travel_scanner_pdf/tools/video/core/project-lease.mjs';
import { siteClient } from '/workspace/travel_scanner_pdf/tools/video/shorts/site.mjs';
import { main, EXIT } from '/workspace/travel_scanner_pdf/tools/video/cli.mjs';
const home='/workspace/work/ai-pdf-01', root='/workspace/travel_scanner_pdf', slug='ai-pdf-quotes-to-comparison';
const work=path.join(home,'media',slug), doc=path.join(root,'docs/videos',slug), original='/workspace/work/ai-animation-01/media/ai-editable-explainer-animation';
const prefix=path.join(home,'pt-fresh-user-defer2-20261026T2140Z');
const read=f=>JSON.parse(fs.readFileSync(f)), sha=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const insist=(v,m)=>{if(!v)throw new Error(m);};
const save=(suffix,value)=>fs.writeFileSync(prefix+suffix,JSON.stringify(value,null,2)+'\n',{flag:'wx'});
function files(dir){return fs.existsSync(dir)?fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(path.join(dir,e.name)):e.isFile()?[path.join(dir,e.name)]:[]):[];}
function snapshot(){return Object.fromEntries(files(work).filter(f=>path.relative(work,f)!=='LEASE').sort().map(f=>[path.relative(work,f),sha(f)]));}
function producers(){return fs.readdirSync('/proc').filter(n=>/^\d+$/.test(n)&&Number(n)!==process.pid).flatMap(n=>{try{const args=fs.readFileSync(`/proc/${n}/cmdline`,'utf8').split('\0').filter(Boolean);return /^(node|python(?:3(?:\.\d+)?)?)$/.test(path.basename(args[0]??''))&&args.some(a=>/ai-pdf-01|ai-animation-01|whisper_second_opinion/.test(a))?[{pid:Number(n),executable:path.basename(args[0]),arguments:args.slice(1)}]:[];}catch{return[];}});}
function controls(){insist(producers().length===0,'Another actual producer/Whisper controller is live');for(const base of [work,original,path.dirname(work),path.dirname(original),home,'/workspace/work/ai-animation-01'])for(const n of ['LEASE','STOP'])insist(!fs.existsSync(path.join(base,n)),`${n} exists at ${base}`);}
const rawFetch=globalThis.fetch;
const routes=[];
globalThis.fetch=async(input,init={})=>{const url=new URL(typeof input==='string'?input:input.url);const method=init.method??(typeof input==='object'?input.method:'GET')??'GET';insist(method==='GET'&&url.origin==='https://mokaair.com'&&['/api/video/reviews/ai-editable-explainer-animation','/api/video/reviews/ai-pdf-quotes-to-comparison','/api/video/speech/status'].includes(url.pathname)&&!url.search,'Preflight allows only exact three nonpaid GET routes');routes.push(`GET ${url.pathname}`);return rawFetch(input,{...init,redirect:'error',signal:AbortSignal.timeout(30000)});};
let lease;
let before;
let beforeSources;
let result;
try{
  controls();
  const guard=read(prefix+'-original-task.json');
  insist(guard.owner==='codex-ai-video'&&guard.actual_task_blob==='0ecde69a42861d4f672a0be1105fb2b209829246'&&Date.now()-Date.parse(guard.latest_checkpoint)>7200000,'Original task recent/changed or not established');
  insist(Date.now()-Date.parse(guard.observed_at_utc)<600000,'Original task check stale');
  const state=read(path.join(work,'auto.json'));
  insist(state.status==='done'&&!state.tidied_at&&state.defer_count===2&&state.deferred_until==='2026-10-26T21:05:02.168Z'&&Date.parse(state.deferred_until)<Date.now(),'Preserved native defer2/current eligibility differs');
  insist(isDeepStrictEqual(state.languages.pt,{shorten:0,retakes:0,reword:0,check_stopped:true}),'PT existing native limits differ');
  const journals=files(work).filter(f=>f.includes('/speech-journal/'));
  const runDir=path.join(work,'run-receipts');
  const outstanding=fs.existsSync(runDir)?fs.readdirSync(runDir,{withFileTypes:true}).filter(e=>e.isFile()&&e.name.endsWith('.json')).map(e=>path.join(runDir,e.name)).filter(f=>!read(f).adopted):[];
  const archive=path.join(runDir,'archive/4608ed31112bd4b764dbb2da5a5772730eb28d48b7f147edc2b4ae3b7c02e367-d6544532-e2db-4348-9b9d-2f3721dc888f.json');
  insist(sha(archive)==='836fe4b1a11afded5d1020f1c2c08fbe9bd417b63d7a9a9c060a56ec3f02051b'&&read(archive).receipt?.status==='succeeded'&&read(archive).owner_retry?.reason==='inputs changed; the saved run is terminal','Immutable first-writer archive differs; preserve and inspect');
  insist(journals.length===0&&outstanding.length===0,'Existing unknown or unadopted durable receipt must be reconciled, never resent');
  const primary='346a5bbd4b47884f301a9dfc9b67fe81e1a504232a0f4746e60ddead54d94e3f';
  insist(sha(path.join(work,'final.mp4'))===primary,'Actual primary bytes changed');
  const qa=read(path.join(work,'review/qa.json'));
  insist(qa.ok&&qa.final_sha256===primary&&qa.items?.length===11&&qa.items.every(r=>r.ok),'Matching real11QA missing');
  const locales=['en','ja','ko','es','pt','id','vi','th'];
  const wanted=Object.fromEntries(locales.map(l=>[l,{metadata:true,captions:true,dub:true}]));
  const choice=read(path.join(work,'languages.json')),auth=read(path.join(home,'local-language-authorization.json'));
  insist(isDeepStrictEqual(choice.locales,wanted)&&auth.source==='user-chat-authorization'&&auth.final_sha256===primary&&isDeepStrictEqual(auth.locales,wanted)&&auth.local_choice_recorded_at===choice.decided_at&&auth.plan_sha256===sha(path.join(doc,'production-plan.json')),'Local exact8 authorization not current');
  const source=sha(path.join(doc,'video.json'));
  insist(source==='eac88936fbcb0324208d639b75ddad8f045c6bcc3cc8c4f60d89ebc6c65f3e04','Chinese source differs');
  const indices=locales.map(locale=>{const indexFile=path.join(doc,'research/translation-reviews',`${locale}.meaning-review.json`),i=read(indexFile),translation=sha(path.join(doc,'i18n',locale+'.json'));insist(i.schema_version===1&&i.passed&&i.scope==='source-meaning-and-naturalness'&&i.source_video_sha256===source&&i.translation_sha256===translation&&sha(path.join(doc,i.report_file))===i.report_sha256,`${locale} actual meaning chain stale`);for(const f of files(path.join(home,'author-review-boundaries')).filter(f=>new RegExp(`^${locale}\\.(shorten|reword)\\.round-[12]\\..+\\.json$`).test(path.basename(f))))insist((i.reviewed_boundaries??[]).some(b=>b.file===path.relative(home,f)&&b.sha256===sha(f)),`${locale} actual native answer not reviewed`);return{locale,index_sha256:sha(indexFile),translation_sha256:translation,report_sha256:i.report_sha256};});
  const ptReportFile=path.join(doc,'research/translation-reviews/baseline-preflights/pt-exact-current-full-independent-review-20261026.json'),ptReport=read(ptReportFile),ptBaseline=path.join(doc,'research/translation-reviews/baseline-preflights/pt-exact-current-baseline-20261026.json');
  insist(ptReport.passed&&ptReport.source_video_sha256===source&&ptReport.translation_sha256===indices.find(i=>i.locale==='pt').translation_sha256&&sha(ptBaseline)===ptReport.baseline_sha256&&ptReport.coverage.all101_current_spoken_pairs_actually_read&&ptReport.coverage.all62_complete_scene_card_contexts_actually_read,'Prior real exact-current PT101-pair review/baseline is not current');
  before=snapshot();beforeSources=Object.fromEntries([path.join(doc,'video.json'),...locales.map(l=>path.join(doc,'i18n',l+'.json'))].map(f=>[path.relative(doc,f),sha(f)]));
  save('-before-free.json',{observed_at_utc:new Date().toISOString(),runtime_files:before,source_files:beforeSources,native_auto:state,current_indices:indices,unknown_journal_files:journals.length,unadopted_durable_receipts:outstanding.length,PT_actual_prior_full_review_sha256:sha(ptReportFile),original_task_guard_sha256:sha(prefix+'-original-task.json')});
  lease=acquireProjectLease(work,{owner:'codex-ai-video-pdf-free-preflight'});lease.verify();
  const api=siteClient({attempts:1});
  const orig=await api.project('ai-editable-explainer-animation'),pdf=await api.project(slug);
  const fr=pdf?.reviews?.find(r=>r.gate==='final'&&(r.subject??null)===null),or=orig?.reviews?.find(r=>r.gate==='final'&&(r.subject??null)===null);
  insist(orig&&!orig.dropped_at&&or?.status==='approved'&&or.content_sha256==='ead26bf5740e1a47499a7bf406c5820bd4b84fd31495d367c1dd83f551a5b521'&&isDeepStrictEqual(orig.dub_retries??{},{})&&orig.worker_state==='unavailable','Original remote/retry state differs');
  insist(pdf&&!pdf.dropped_at&&fr?.status==='approved'&&fr.content_sha256===primary&&isDeepStrictEqual(pdf.dub_retries??{},{}),'PDF real exact primary not approved/current retry exists');
  insist(pdf.locales_decided_at==null&&Object.keys(pdf.locales??{}).length===0||isDeepStrictEqual(pdf.locales,wanted),'Different real owner language choice');
  let log='';const capture={write:s=>{log+=s;return true;}};
  const exit=await main(['dub','--slug',slug,'--locale','pt','--dry-run'],{root,env:{...process.env,VIDEO_WORKDIR:path.join(home,'media')},stdout:capture,stderr:capture});
  fs.writeFileSync(prefix+'-dry-run.log',log,{flag:'wx'});
  const req=log.match(/pt: (\d+) requests, (\d+) to synthesize; about (\d+) billable characters now/),remaining=log.match(/(\d+) characters left this month/),over=log.match(/(\d+) would not fit even at/);
  insist(exit===EXIT.ok&&req&&remaining&&over&&Number(req[2])===95&&Number(req[3])===6112&&Number(remaining[1])>=Number(req[3])&&log.includes('Gemini ready')&&!log.includes('lines have no current translation'),'Actual PT dryrun/quota failed; inspect retained log');
  lease.verify();insist(isDeepStrictEqual(before,snapshot()),'Canonical runtime changed during free preflight');
  insist(isDeepStrictEqual(beforeSources,Object.fromEntries(Object.keys(beforeSources).map(p=>[p,sha(path.join(doc,p))]))),'Source changed during preflight');
  result={observed_at_utc:new Date().toISOString(),kind:'one-fresh-user-nonpaid-PT-preflight-preserving-defer2',routes,original_final:{id:or.id,status:or.status,sha256:or.content_sha256},original_retries:orig.dub_retries??{},original_worker_state:orig.worker_state,original_LEASE_STOP_controller_absent:true,PDF_final:{id:fr.id,status:fr.status,sha256:fr.content_sha256},matching_QA11:true,PDF_locales_decided_at:pdf.locales_decided_at,PDF_retries:pdf.dub_retries??{},actual_dry_run_exit:exit,estimated_new_requests:Number(req[2]),estimated_billable_characters:Number(req[3]),monthly_characters_remaining_at_read:Number(remaining[1]),estimated_over_windows_preserved:Number(over[1]),Gemini_configured_ready_is_not_actual_synthesis_availability:true,no_billing_inference:true,project_runtime_byte_exact:true,protected_runtime_file_count:Object.keys(before).length,source9_byte_exact:true,current_indices:indices,PT_actual_prior_full_review_sha256:sha(ptReportFile),native_defer_count:state.defer_count,native_deferred_until:state.deferred_until,native_PT_rounds:state.languages.pt,native_auto_defer_caps_exact:true,journal_files:journals.length,unadopted_model_receipts:outstanding.length,prior_false_positive_guard_failure:prefix.replace('T2140Z','T2138Z')+'-free-preflight-failure.json',immutable_archived_first_writer_sha256:sha(archive),native_current_run_receipt_scan_is_top_level:true,no_paid_operation_performed:true,source_task_Git_not_written:true,dry_run_log_sha256:sha(prefix+'-dry-run.log'),helper_sha256:sha(prefix+'-free-preflight.mjs')};
  save('-free-preflight.json',result);
}catch(error){save('-free-preflight-failure.json',{recorded_at_utc:new Date().toISOString(),message:error.message,no_paid_operation_performed:true,source_task_Git_not_written:true});console.error(error.message);process.exitCode=1;}
finally{lease?.release();globalThis.fetch=rawFetch;if(before){const after=snapshot();const exact=isDeepStrictEqual(before,after);const released=!fs.existsSync(path.join(work,'LEASE'));save('-released-free-preflight.json',{recorded_at_utc:new Date().toISOString(),runtime_file_count:Object.keys(after).length,project_runtime_byte_exact:exact,LEASE_STOP_absent:released&&!fs.existsSync(path.join(work,'STOP')),no_paid_operation_performed:true,source_task_Git_not_written:true});if(!exact||!released)process.exitCode=1;}}
if(result)console.log(JSON.stringify({prefix,...result},null,2));
