// Offline actual ended-unit audit only; no native production, network or source mutation.
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { isDeepStrictEqual as same } from 'node:util';
import { loadProject, dubsStatus } from '/workspace/travel_scanner_pdf/tools/video/core/state.mjs';
import { speechHash } from '/workspace/travel_scanner_pdf/tools/video/core/timeline.mjs';
const home='/workspace/work/ai-pdf-01',root='/workspace/travel_scanner_pdf',slug='ai-pdf-quotes-to-comparison';
const work=path.join(home,'media',slug),doc=path.join(root,'docs/videos',slug),prefix=path.join(home,'pt-native-state6-qualification-20261027T0327Z');
const read=f=>JSON.parse(fs.readFileSync(f,'utf8')),sha=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex'),exists=f=>fs.existsSync(f);
const save=(f,v)=>fs.writeFileSync(f,JSON.stringify(v,null,2)+'\n',{flag:'wx'});
const files=dir=>exists(dir)?fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(path.join(dir,e.name)):e.isFile()?[path.join(dir,e.name)]:[]):[];
const snapshot=(dir,exclude=[])=>Object.fromEntries(files(dir).sort().filter(f=>!exclude.includes(path.relative(dir,f))).map(f=>[path.relative(dir,f),sha(f)]));
globalThis.fetch=()=>{throw new Error('This actual ended-unit audit is offline; network refused');};
const before=read(prefix+'-before.json'),out=read(prefix+'-actual-outcome.json'),after=read(prefix+'-post-unit-runtime-snapshot.json'),state=read(path.join(work,'auto.json')),site=read(prefix+'-site-after-unit.json');
const pidEnded=[out.native_pid,out.driver_pid].every(pid=>!exists('/proc/'+pid));
const controllers=fs.readdirSync('/proc').filter(n=>/^\d+$/.test(n)&&Number(n)!==process.pid).flatMap(n=>{try{const a=fs.readFileSync('/proc/'+n+'/cmdline','utf8').split('\0').filter(Boolean),exe=path.basename(a[0]??'');return /^(node|python(?:3(?:\.\d+)?)?|ffmpeg|ffprobe)$/.test(exe)&&a.slice(1).some(s=>/ai-pdf-01|whisper_second_opinion/.test(s))?[{pid:Number(n),executable:exe}]:[];}catch{return[];}});
const controls=[home,path.dirname(work),work].flatMap(d=>['LEASE','STOP'].filter(n=>exists(path.join(d,n))).map(n=>path.join(d,n)));
const runtime=snapshot(work,['LEASE']),source=snapshot(doc),core=Object.fromEntries(Object.keys(before.core_and_shared_inputs).map(f=>[f,sha(path.join(root,f))]));
const textDir=path.join(home,'language-text-delivery-20261026T2154Z'),text=snapshot(textDir),marker=path.join(home,'free-caption-preparation-20261026T2144Z/one-use-execution/ONE_USE.json');
const oldCC=read(path.join(home,'free-caption-preparation-20261026T2144Z/one-use-execution/after-final-audit.json')).runtime_files;
const nonauto=x=>Object.fromEntries(Object.entries(x).filter(([f])=>f!=='auto.json'));
const changed=[...new Set([...Object.keys(before.runtime_files),...Object.keys(runtime)])].sort().filter(f=>before.runtime_files[f]!==runtime[f]);
const locales=['en','ja','ko','es','pt','id','vi','th'],project=loadProject({slug,root}),speech=speechHash(project.doc,project.lexicon),status=dubsStatus(project,work,speech);
const maybe=f=>exists(f)?read(f):null,sourceSHA=sha(path.join(doc,'video.json'));
const rows=locales.map(locale=>{
 const idxFile=path.join(doc,'research/translation-reviews',locale+'.meaning-review.json'),idx=read(idxFile),translation=sha(path.join(doc,'i18n',locale+'.json'));
 const boundaries=files(path.join(home,'author-review-boundaries')).filter(f=>new RegExp('^'+locale+'\\.(shorten|reword)\\.round-[12]\\..+\\.json$').test(path.basename(f)));
 const meaning=idx.schema_version===1&&idx.passed===true&&idx.scope==='source-meaning-and-naturalness'&&idx.source_video_sha256===sourceSHA&&idx.translation_sha256===translation&&sha(path.join(doc,idx.report_file))===idx.report_sha256&&boundaries.every(f=>(idx.reviewed_boundaries??[]).some(r=>r.file===path.relative(home,f)&&r.sha256===sha(f)));
 const cache=maybe(path.join(work,'review','check.'+locale+'.json')),flags=maybe(path.join(work,'review','check-flags.'+locale+'.json')),timeline=maybe(path.join(work,'dubs',locale,'timeline.json')),fit=maybe(path.join(work,'dubs',locale,'fit.json'));
 let matching=0;
 for(const[id,row]of Object.entries(cache?.lines??{})){const f=path.join(work,'dubs',locale,'audio',id+'.wav');if(exists(f)&&row.clip===sha(f).slice(0,16))matching++;}
 const checked=Boolean(meaning&&status[locale]?.status==='current'&&!state.languages?.[locale]?.check_stopped&&flags?.speech_hash===speech&&flags?.translation_hash===timeline?.translation_hash&&Array.isArray(flags?.flags)&&flags.flags.length===0&&(fit?.over??[]).length===0&&(fit?.kept??[]).length===0&&matching===101);
 return{locale,translation_sha256:translation,meaning_index_sha256:sha(idxFile),meaning_current:meaning,actual_model_boundary_count:boundaries.length,native_status:status[locale],native_rounds:state.languages?.[locale]??null,actual_flags:flags?.flags??null,raw_matched_primary_checks:matching,actual_checked_voice_ready:checked};
});
const ready=rows.filter(r=>r.actual_checked_voice_ready).map(r=>r.locale);
const journals=files(work).filter(f=>f.includes('/speech-journal/')).map(f=>path.relative(work,f));
const runDir=path.join(work,'run-receipts'),unadopted=fs.readdirSync(runDir,{withFileTypes:true}).filter(e=>e.isFile()&&e.name.endsWith('.json')).map(e=>path.join(runDir,e.name)).filter(f=>!read(f).adopted).map(f=>path.relative(work,f));
const original14=after.original14_protected,archive=path.join(runDir,'archive/4608ed31112bd4b764dbb2da5a5772730eb28d48b7f147edc2b4ae3b7c02e367-d6544532-e2db-4348-9b9d-2f3721dc888f.json');
const primary='346a5bbd4b47884f301a9dfc9b67fe81e1a504232a0f4746e60ddead54d94e3f',qa=read(path.join(work,'review/qa.json'));
const checks={
 actual_driver_and_native_ended:pidEnded,actual_PDF_controllers_absent:controllers.length===0,actual_LEASE_STOP_absent:controls.length===0,
 runtime2350_matches_actual_post_unit_snapshot:Object.keys(runtime).length===2350&&same(runtime,after.runtime_files),
 only_actual_runtime_change_auto:same(changed,['auto.json']),all2349_NONAUTO_match_completed9CC:same(nonauto(runtime),nonauto(oldCC)),
 full_then_current_source514_exact:Object.keys(source).length===514&&same(source,after.source_files)&&same(source,before.full_source_tree_before),
 production9_source_exact:Object.entries(before.source_hashes).every(([f,h])=>sha(path.join(doc,f))===h),
 shared_core20_exact:Object.keys(core).length===20&&same(core,before.core_and_shared_inputs),
 immutable_text28plusmanifest_exact:same(text,before.text_delivery_files_before),consumed_CC_ONE_USE_exact:sha(marker)===before.CC_ONE_USE_sha256,
 original14_exact:Object.keys(original14).length===14&&Object.entries(original14).every(([f,h])=>sha(f)===h),
 protected_primary_checks_thumbnails_CC_exact:Object.entries(before.protected_hashes).every(([f,h])=>sha(path.join(work,f))===h),
 ENJA_failed_caps_exact:['en','ja'].every(l=>same(state.languages[l],before.native_before.languages[l])),
 actual8_meaning_chains_current:rows.every(r=>r.meaning_current),actual7_model_boundaries_bound:rows.reduce((n,r)=>n+r.actual_model_boundary_count,0)===7,
 actual_checked_voices_still_KO_ES:same(ready,['ko','es']),current_unknown_and_unadopted_zero:journals.length===0&&unadopted.length===0,
 terminal_archive836fe_preserved:sha(archive)==='836fe4b1a11afded5d1020f1c2c08fbe9bd417b63d7a9a9c060a56ec3f02051b',
 actual_new_native_block_matches_outcome:out.actual_exit_code===3&&out.actual_native_block_observed&&state.status==='blocked'&&state.blocked_kind==='deferred:dub'&&state.blocked_from_status==='done'&&state.blocked===out.native_blocked_after,
 native_wait_fields_genuinely_absent:['defer_count','defer_shared','deferred_until'].every(k=>!Object.hasOwn(state,k)),
 actual_PT_WAV_ASR_zero:out.PT_primary_WAV_count===0&&out.PT_saved_primary_check_count===0,
 actual_log_bytes_match:sha(prefix+'.log')===out.log_sha256,
 genuine_site_blocked_report_present:site.stage==='blocked'&&(site.checklist??[]).some(r=>r.key==='blocked'&&r.label.includes(state.blocked)),
 genuine_site_final_still_exact_approved:(site.reviews??[]).some(r=>r.gate==='final'&&r.status==='approved'&&r.content_sha256===primary),
 primary_and_existing11QA_still_match:sha(path.join(work,'final.mp4'))===primary&&qa.ok&&qa.final_sha256===primary&&qa.items.length===11&&qa.items.every(r=>r.ok),
 unchanged_native_adapter:sha(path.join(home,'languages.mjs'))==='f8d07607e95c4bed91ea1941f0ab2fac2fd7bbb3005617fe83beb72e668f74bf',
 unchanged_compatible_medium_env:sha('/workspace/work/video-asr-runtime/native-second-asr-environment.compatible.json')==='e9736a50c1188c8c899d0d834822fd3e39f6c73591a53382fb8376bbc31e521d'
};
const audit={recorded_at_utc:new Date().toISOString(),kind:'actual-one-genuine-PT-attempt-natively-blocked-after-NEW-own-failure',slug,ok:Object.values(checks).every(Boolean),checks,actual_exit:out.actual_exit_code,actual_started_at:read(prefix+'-started.json').started_at_utc,actual_ended_at:out.ended_at_utc,native_pid:out.native_pid,driver_pid:out.driver_pid,actual_controllers:controllers,actual_control_paths:controls,actual_native_after:{status:state.status,blocked:state.blocked,blocked_kind:state.blocked_kind,blocked_from_status:state.blocked_from_status,defer_count_field_present:Object.hasOwn(state,'defer_count'),defer_shared_field_present:Object.hasOwn(state,'defer_shared'),deferred_until_field_present:Object.hasOwn(state,'deferred_until'),PT_rounds:state.languages.pt},actual_before_own:6,native_DEFER_LIMIT_unchanged:6,native_block_removed_wait_fields_not_manual_reset:true,no_synthetic_defer7_or_new_due:true,actual_checked_foreign_locales:ready,voice_rows:rows,current_speech_journals:journals,current_top_level_unadopted_model_receipts:unadopted,actual_runtime_changed_paths:changed,actual_outcome_sha256:sha(prefix+'-actual-outcome.json'),actual_log_sha256:sha(prefix+'.log'),current_blocked_runtime_snapshot:{file:prefix+'-post-unit-runtime-snapshot.json',sha256:sha(prefix+'-post-unit-runtime-snapshot.json'),auto_sha256:sha(path.join(work,'auto.json')),runtime_files:Object.keys(runtime).length,dated_source_files:Object.keys(source).length},actual_site_after_unit:{file:prefix+'-site-after-unit.json',sha256:sha(prefix+'-site-after-unit.json'),observed_at_utc:site.observed_at_utc,stage:site.stage,retry_request_id:site.retry_request_id??null,retry_acknowledged_id:site.retry_acknowledged_id??null,dub_retries:site.dub_retries??{},worker_state:site.worker_state},actual_new_owner_retry_request_present:Boolean(site.retry_request_id&&site.retry_request_id!==site.retry_acknowledged_id),no_owner_retry_or_publication_action:true,no_HTTP_code_billing_settlement_or_zero_billing_inference:true,no_new_full_QA_voice_semantic_listening_or_installation_claim:true,next:'Native and real site now genuinely blocked after a new own failure. No due or automatic normal retry remains. Preserve this actual blocked-state snapshot and every failed/unknown/cap/approval/source/text artifact. Resume only through a genuine supported owner retry/recovery reflected by actual site request and normal acknowledgement/guards, after service/current ownership/source/meaning/primary11QA/chat8/quota/unknown checks. Never restore done, recreate/decrease counters, remove skips or invoke ordinary dub while nativeblocked. ENJA ordinary retry/original owner operations/other locale/new movie/full8/publish remain excluded; publishing stays owner.'};
save(prefix+'-post-native-block-audit.json',audit);
if(!audit.ok)throw new Error('Actual stopped-unit audit failed; report saved without changing native/source states');
console.log(JSON.stringify({audit_file:prefix+'-post-native-block-audit.json',audit_sha256:sha(prefix+'-post-native-block-audit.json'),actual_checks_passed:Object.values(checks).filter(Boolean).length,actual_checks_total:Object.keys(checks).length,actual_checked_foreign_locales:ready,native_status:state.status,site_stage:site.stage},null,2));
