// Guarded A01 adoption API. No CLI, provider calls, DB reconciliation or STOP removal.
import { createHash, randomUUID } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { acquireProjectLease } from '../../../../../tools/video/core/project-lease.mjs';
import { planPinnedTransition, preparePinnedEvent, verifyPinnedTransition } from './transition.mjs';
const SLUG='story-rolling-suitcase-v2';
const DOC='docs/videos/'+SLUG;
const HERE=path.dirname(fileURLToPath(import.meta.url));
const runtimePins=JSON.parse(fs.readFileSync(path.join(HERE,'required-runtime.json'),'utf8'));
const sha=b=>createHash('sha256').update(b).digest('hex');
const json=v=>Buffer.from(JSON.stringify(v,null,2)+'\n');
function need(ok,code) { if(!ok) { const e=new Error(code); e.code=code; throw e; } }
function safe(root,rel='') {
  need(typeof root==='string' && path.isAbsolute(root) && !root.startsWith('\\\\') && !root.startsWith('//'),'ADOPTION_LOCAL_ROOT_REQUIRED');
  need(!rel || rel.split('/').every(p=>p && p!=='.' && p!=='..' && !/[\\:\x00-\x1f]/.test(p)),'ADOPTION_RELATIVE_PATH_INVALID');
  const resolved=path.resolve(root); let current=path.parse(resolved).root;
  for(const p of path.relative(current,resolved).split(path.sep).filter(Boolean).concat(rel?rel.split('/'):[])) {
    current=path.join(current,p);
    if(fs.existsSync(current)) need(!fs.lstatSync(current).isSymbolicLink(),'ADOPTION_SYMLINK_REFUSED');
  }
  return current;
}
function durable(file,bytes,immutable=true) {
  fs.mkdirSync(path.dirname(file),{recursive:true});
  if(immutable && fs.existsSync(file)) { need(fs.readFileSync(file).equals(bytes),'ADOPTION_IMMUTABLE_COLLISION'); return; }
  const temporary=immutable?file:file+'.'+randomUUID()+'.tmp';
  const fd=fs.openSync(temporary,'wx',0o600);
  try { fs.writeFileSync(fd,bytes); fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
  if(!immutable) fs.renameSync(temporary,file);
  if(process.platform!=='win32') { const d=fs.openSync(path.dirname(file),'r'); try { fs.fsyncSync(d); } finally { fs.closeSync(d); } }
}
function copyRegular(from,to) {
  const stat=fs.lstatSync(from); need(!stat.isSymbolicLink(),'ADOPTION_SYMLINK_REFUSED');
  if(stat.isDirectory()) { fs.mkdirSync(to,{recursive:true}); for(const name of fs.readdirSync(from)) copyRegular(path.join(from,name),path.join(to,name)); }
  else { need(stat.isFile(),'ADOPTION_REGULAR_FILE_REQUIRED'); fs.mkdirSync(path.dirname(to),{recursive:true}); fs.copyFileSync(from,to,fs.constants.COPYFILE_EXCL); }
}
/** Copy only source/audit bytes; never media, credentials, backups or arbitrary work files. */
export function captureAdoptionSources({root,workBase,output}) {
  need(fs.readdirSync(safe(output)).length===0,'ADOPTION_CAPTURE_NOT_EMPTY');
  const copy=(rel,optional=false)=>{
    const from=rel.startsWith('docs/')?safe(root,rel):safe(workBase,rel);
    if(optional && !fs.existsSync(from)) return;
    copyRegular(from,safe(output,rel));
  };
  for(const name of ['video.json','series.json','claims.md','script.md']) copy(DOC+'/'+name);
  copy('docs/videos/lexicon.json'); copy(DOC+'/verify-1.md',true);
  for(const name of ['auto.json','review/narrative.json','story/chapters','story/recheck-audit']) copy(SLUG+'/'+name);
  copy(SLUG+'/story/reviews/script-review.json',true);
  const revisions=safe(workBase,SLUG+'/manual-revisions');
  for(const id of fs.readdirSync(revisions)) copy(SLUG+'/manual-revisions/'+id+'/installation-receipt.json');
  const snapshot=safe(root,DOC+'/story-lexicon');
  if(fs.existsSync(snapshot)) for(const name of ['versions','events','current.json']) {
    if(fs.existsSync(safe(root,DOC+'/story-lexicon/'+name))) copy(DOC+'/story-lexicon/'+name);
  }
  return output;
}
/** Caller owns host deploy locks and verified DB/job/budget preflight. Returns HOLD even after commit. */
export function adoptPinnedTransition({root,workBase,beforeRoot,oldLexiconFile,reviewBytes,receiptBytes,
  expectedPlanSha256,ownerApprovalRef,checkpoint=()=>{},recoverCommitted=false,syntheticRuntimePins,...fixtureOptions}) {
  root=safe(root); workBase=safe(workBase);
  const outside=(child,parent)=>{const r=path.relative(parent,child);return r==='..' || r.startsWith('..'+path.sep) || path.isAbsolute(r);};
  need(outside(root,workBase) && outside(workBase,root),'ADOPTION_SPLIT_ROOTS_REQUIRED');
  const synthetic=Object.keys(fixtureOptions).length>0;
  if(synthetic || syntheticRuntimePins) need(synthetic && !outside(root,os.tmpdir()) && !outside(workBase,os.tmpdir()),'ADOPTION_SYNTHETIC_TARGET_FORBIDDEN');
  const options={...fixtureOptions,snapshotRoot:beforeRoot,oldLexiconFile};
  const prepared=preparePinnedEvent({...options,reviewBytes,receiptBytes});
  need(expectedPlanSha256===prepared.plan_sha256,'ADOPTION_PLAN_PIN_MISMATCH');
  const ownerRecord=JSON.parse(receiptBytes);
  need(typeof ownerApprovalRef==='string' && ownerApprovalRef.trim() && ownerRecord.owner_approval_ref===ownerApprovalRef,'ADOPTION_OWNER_RECORD_MISMATCH');
  for(const [file,pin] of Object.entries(syntheticRuntimePins ?? runtimePins)) need(sha(fs.readFileSync(safe(root,file)))===pin,'ADOPTION_RUNTIME_NOT_DEPLOYED');
  const workdir=safe(workBase,SLUG); const lease=acquireProjectLease(workdir,{owner:'a01-pinned-adoption'});
  let writer;
  try {
    writer=acquireProjectLease(safe(root,'docs/videos/.lexicon-writer'),{owner:'lexicon-writer'});
    const docsPending=safe(root,DOC+'/story-lexicon/pending.json');
    const intentDir=safe(workBase,SLUG+'/story/lexicon-intents');
    if(recoverCommitted) {
      const id=prepared.plan.event_id;
      const workIntent=safe(workBase,SLUG+'/story/lexicon-intents/'+id+'.json');
      const transaction=safe(workBase,SLUG+'/story/lexicon-transactions/'+id+'.json');
      need(fs.existsSync(transaction),'ADOPTION_PARTIAL_REQUIRES_REVIEW');
      const record=JSON.parse(fs.readFileSync(transaction));
      need(record.schema_version===1 && record.id===id && record.status==='committed' && record.plan_sha256===prepared.plan_sha256,'ADOPTION_RECOVERY_RECEIPT_MISMATCH');
      const stop=safe(workBase,SLUG+'/STOP');
      need(fs.existsSync(stop) && sha(fs.readFileSync(stop))===record.stop_sha256,'ADOPTION_RECOVERY_STOP_MISMATCH');
      const intent=json({schema_version:1,id,slug:SLUG,plan_sha256:prepared.plan_sha256,stop_sha256:record.stop_sha256});
      for(const file of [docsPending,workIntent]) if(fs.existsSync(file)) need(fs.readFileSync(file).equals(intent),'ADOPTION_RECOVERY_FENCE_MISMATCH');
      need(!fs.existsSync(intentDir) || fs.readdirSync(intentDir).filter(n=>n.endsWith('.json')).every(n=>n===id+'.json'),'ADOPTION_FOREIGN_INTENT');
      const afterCopy=fs.mkdtempSync(path.join(os.tmpdir(),'a01-adoption-recovery-'));
      captureAdoptionSources({root,workBase,output:afterCopy});
      const result=verifyPinnedTransition({...options,beforeRoot,afterRoot:afterCopy});
      need(result.source_sha256===record.source_sha256,'ADOPTION_RECOVERY_SOURCE_MISMATCH');
      if(fs.existsSync(docsPending)) fs.unlinkSync(docsPending);
      if(fs.existsSync(workIntent)) fs.unlinkSync(workIntent);
      return {...result,adoption:'RECOVERED_COMMITTED_HELD',stop_preserved:true,release_allowed:false};
    }
    need(!fs.existsSync(docsPending) && (!fs.existsSync(intentDir) || !fs.readdirSync(intentDir).some(n=>n.endsWith('.json'))),'ADOPTION_PENDING_TRANSACTION');
    need(!fs.existsSync(safe(root,DOC+'/story-lexicon/current.json')),'ADOPTION_ALREADY_PINNED');
    const stop=safe(workBase,SLUG+'/STOP');
    if(!fs.existsSync(stop)) durable(stop,json({reason:'A01 pinned lexicon adoption; keep held until independent readback and script gates',plan_sha256:prepared.plan_sha256}));
    need(fs.lstatSync(stop).isFile(),'ADOPTION_STOP_NOT_REGULAR');
    const stopHash=sha(fs.readFileSync(stop));
    const beforeCopy=fs.mkdtempSync(path.join(os.tmpdir(),'a01-adoption-before-'));
    captureAdoptionSources({root,workBase,output:beforeCopy});
    if(synthetic) copyRegular(safe(beforeRoot,'A01-LEXICON-E640-OFFLINE-FIXTURE.json'),safe(beforeCopy,'A01-LEXICON-E640-OFFLINE-FIXTURE.json'));
    need(planPinnedTransition({...options,snapshotRoot:beforeCopy}).plan_sha256===prepared.plan_sha256,'ADOPTION_LIVE_SOURCE_DRIFT');
    const id=prepared.plan.event_id;
    const intent=json({schema_version:1,id,slug:SLUG,plan_sha256:prepared.plan_sha256,stop_sha256:stopHash});
    const workIntent=safe(workBase,SLUG+'/story/lexicon-intents/'+id+'.json');
    const transaction=safe(workBase,SLUG+'/story/lexicon-transactions/'+id+'.json');
    need(!fs.existsSync(transaction),'ADOPTION_TRANSACTION_EXISTS');
    durable(workIntent,intent); checkpoint('work-intent');
    durable(docsPending,intent); checkpoint('docs-intent');
    const entries=Object.entries(prepared.files);
    const auto=SLUG+'/auto.json', pointer=DOC+'/story-lexicon/current.json';
    for(const [rel,bytes] of entries.filter(([rel])=>rel!==auto && rel!==pointer)) {
      const target=rel.startsWith('docs/')?safe(root,rel):safe(workBase,rel);
      durable(target,bytes);
    }
    checkpoint('immutable-files');
    // Both fences and scoped STOP remain throughout the two-volume visibility window.
    durable(safe(workBase,auto),prepared.files[auto],false); checkpoint('auto-state');
    durable(safe(root,pointer),prepared.files[pointer]); checkpoint('current-pointer');
    const afterCopy=fs.mkdtempSync(path.join(os.tmpdir(),'a01-adoption-after-'));
    captureAdoptionSources({root,workBase,output:afterCopy});
    const result=verifyPinnedTransition({...options,beforeRoot:beforeCopy,afterRoot:afterCopy});
    need(sha(fs.readFileSync(stop))===stopHash,'ADOPTION_STOP_CHANGED');
    durable(transaction,json({schema_version:1,id,status:'committed',plan_sha256:prepared.plan_sha256,
      source_sha256:result.source_sha256,stop_sha256:stopHash,before_capture:beforeCopy,after_capture:afterCopy}));
    checkpoint('committed-receipt');
    need(fs.readFileSync(docsPending).equals(intent) && fs.readFileSync(workIntent).equals(intent),'ADOPTION_FENCE_CHANGED');
    fs.unlinkSync(docsPending); checkpoint('docs-fence-cleared'); fs.unlinkSync(workIntent);
    return {...result,adoption:'COMMITTED_HELD',before_capture:beforeCopy,after_capture:afterCopy,stop_preserved:true,release_allowed:false};
  } finally { writer?.release(); lease.release(); }
}
