// Guarded existing-chapter revision; STOP remains and no provider/job calls are made.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash,randomUUID} from 'node:crypto';
import {acquireProjectLease} from '../../../../../tools/video/core/project-lease.mjs';
import {captureAdoptionSources} from './adopt-pinned.mjs';
import {prepareOfflineRevision,planOfflineRevision,verify82Fixture} from './pinned-revision-plan.mjs';
const SLUG='story-rolling-suitcase-v2',DOC='docs/videos/'+SLUG;
const sha=b=>createHash('sha256').update(b).digest('hex');
const json=v=>Buffer.from(JSON.stringify(v,null,2)+'\n');
const pins=JSON.parse(fs.readFileSync(new URL('./required-runtime.json',import.meta.url)));
function need(ok,code){if(!ok)throw Error(code);}
function safe(root,rel=''){
 need(path.isAbsolute(root)&&!root.startsWith('\\\\')&&!root.startsWith('//'),'REVISION_LOCAL_ROOT_REQUIRED');
 need(!rel||rel.split('/').every(p=>p&&p!=='.'&&p!=='..'&&!/[\\:\x00-\x1f]/.test(p)),'REVISION_RELATIVE_PATH_INVALID');
 let current=path.parse(path.resolve(root)).root;
 for(const part of path.relative(current,path.resolve(root)).split(path.sep).filter(Boolean).concat(rel?rel.split('/'):[])){
  current=path.join(current,part);let stat;
  try{stat=fs.lstatSync(current);}catch(error){if(error.code!=='ENOENT')throw error;}
  if(stat)need(!stat.isSymbolicLink(),'REVISION_SYMLINK_REFUSED');
 }return current;
}
function durable(file,bytes,immutable=true){
 fs.mkdirSync(path.dirname(file),{recursive:true});
 if(immutable&&fs.existsSync(file)){need(fs.readFileSync(file).equals(bytes),'REVISION_IMMUTABLE_COLLISION');return;}
 const temp=immutable?file:file+'.'+randomUUID()+'.tmp';const fd=fs.openSync(temp,'wx',0o600);
 try{fs.writeFileSync(fd,bytes);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}
 if(!immutable)fs.renameSync(temp,file);
 if(process.platform!=='win32'){const d=fs.openSync(path.dirname(file),'r');try{fs.fsyncSync(d);}finally{fs.closeSync(d);}}
}
export function adoptExistingRevision({root,workBase,expectedPlanSha256,ownerApprovalRef,checkpoint=()=>{},recoverCommitted=false,...options}){
 root=safe(root);workBase=safe(workBase);
 const outside=(a,b)=>{const r=path.relative(b,a);return r==='..'||r.startsWith('..'+path.sep)||path.isAbsolute(r);};
 need(outside(root,workBase)&&outside(workBase,root),'REVISION_SPLIT_ROOTS_REQUIRED');
 // This production adapter accepts only the real historical baseline; fixture overrides stay offline.
 need(!['pins80','expectedOldSha','expectedNewSha'].some(k=>Object.hasOwn(options,k)),'REVISION_FIXTURE_OVERRIDE_REFUSED');
 const prepared=prepareOfflineRevision(options);
 need(prepared.plan_sha256===expectedPlanSha256,'REVISION_PLAN_PIN_MISMATCH');
 const receipt=JSON.parse(options.receiptBytes);
 need(typeof ownerApprovalRef==='string'&&ownerApprovalRef.trim()&&receipt.owner_approval_ref===ownerApprovalRef,'REVISION_OWNER_RECORD_MISMATCH');
 for(const [rel,pin] of Object.entries(pins))need(sha(fs.readFileSync(safe(root,rel)))===pin,'REVISION_RUNTIME_NOT_DEPLOYED');
 const lease=acquireProjectLease(safe(workBase,SLUG),{owner:'a01-round22-adoption'});let writer;
 try{
  writer=acquireProjectLease(safe(root,'docs/videos/.lexicon-writer'),{owner:'lexicon-writer'});
  const id=prepared.plan.event_id;
  const stop=safe(workBase,SLUG+'/STOP');need(fs.lstatSync(stop).isFile(),'REVISION_STOP_REQUIRED');
  const stopHash=sha(fs.readFileSync(stop));
  const pending=safe(root,DOC+'/story-lexicon/pending.json');
  const intentDir=safe(workBase,SLUG+'/story/lexicon-intents');
  const intentFile=safe(workBase,SLUG+'/story/lexicon-intents/'+id+'.json');
  const transaction=safe(workBase,SLUG+'/story/lexicon-transactions/'+id+'.json');
  const intent=json({schema_version:1,id,slug:SLUG,plan_sha256:expectedPlanSha256,stop_sha256:stopHash});
  const capture=()=>{const output=fs.mkdtempSync(path.join(os.tmpdir(),'a01-revision-capture-'));captureAdoptionSources({root,workBase,output});return output;};
  if(recoverCommitted){
   need(fs.existsSync(transaction),'REVISION_PARTIAL_REQUIRES_REVIEW');
   const record=JSON.parse(fs.readFileSync(transaction));
   need(record.schema_version===1&&record.id===id&&record.status==='committed'&&record.plan_sha256===expectedPlanSha256&&record.stop_sha256===stopHash,'REVISION_RECOVERY_RECEIPT_MISMATCH');
   need(!fs.existsSync(intentDir)||fs.readdirSync(intentDir).filter(n=>n.endsWith('.json')).every(n=>n===id+'.json'),'REVISION_FOREIGN_INTENT');
   for(const file of [pending,intentFile])if(fs.existsSync(file))need(fs.readFileSync(file).equals(intent),'REVISION_RECOVERY_FENCE_MISMATCH');
   const after=capture();const result=verify82Fixture({...options,after82Root:after});
   need(record.source_sha256===result.new_pins.source_composite_sha256,'REVISION_RECOVERY_SOURCE_MISMATCH');
   for(const file of [pending,intentFile])if(fs.existsSync(file))fs.unlinkSync(file);
   return {...result,adoption:'RECOVERED_COMMITTED_HELD',after_capture:after,stop_preserved:true,release_allowed:false};
  }
  need(!fs.existsSync(pending)&&(!fs.existsSync(intentDir)||!fs.readdirSync(intentDir).some(n=>n.endsWith('.json'))),'REVISION_PENDING_TRANSACTION');
  need(!fs.existsSync(transaction),'REVISION_TRANSACTION_EXISTS');
  const before=capture();need(planOfflineRevision({...options,before81Root:before}).plan_sha256===expectedPlanSha256,'REVISION_LIVE_SOURCE_DRIFT');
  durable(intentFile,intent);checkpoint('work-intent');durable(pending,intent);checkpoint('docs-intent');
  for(const [rel,bytes] of Object.entries(prepared.files))durable(safe(workBase,rel),bytes);
  checkpoint('immutable-files');
  const auto=SLUG+'/auto.json';
  for(const [rel,bytes] of Object.entries(prepared.replacements).filter(([rel])=>rel!==auto))durable(rel.startsWith('docs/')?safe(root,rel):safe(workBase,rel),bytes,false);
  checkpoint('chapter-sources');durable(safe(workBase,auto),prepared.replacements[auto],false);checkpoint('auto-state');
  const after=capture();const result=verify82Fixture({...options,before81Root:before,after82Root:after});
  need(sha(fs.readFileSync(stop))===stopHash,'REVISION_STOP_CHANGED');
  durable(transaction,json({schema_version:1,id,status:'committed',plan_sha256:expectedPlanSha256,source_sha256:result.new_pins.source_composite_sha256,stop_sha256:stopHash,before_capture:before,after_capture:after}));checkpoint('committed-receipt');
  need(fs.readFileSync(pending).equals(intent)&&fs.readFileSync(intentFile).equals(intent),'REVISION_FENCE_CHANGED');
  fs.unlinkSync(pending);checkpoint('docs-fence-cleared');fs.unlinkSync(intentFile);
  return {...result,adoption:'COMMITTED_HELD',before_capture:before,after_capture:after,stop_preserved:true,release_allowed:false};
 }finally{writer?.release();lease.release();}
}
