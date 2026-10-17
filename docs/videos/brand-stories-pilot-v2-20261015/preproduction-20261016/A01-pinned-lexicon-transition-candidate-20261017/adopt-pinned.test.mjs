import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import test from 'node:test';
import {fixture} from './synthetic-fixture.mjs';
import {planPinnedTransition} from './transition.mjs';
import {adoptPinnedTransition} from './adopt-pinned.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
const sha=b=>createHash('sha256').update(b).digest('hex');
const json=v=>Buffer.from(JSON.stringify(v)+'\n');
const SLUG='story-rolling-suitcase-v2';
function input(t) {
 const f=fixture(t); const root=path.join(f.parent,'target-docs'),workBase=path.join(f.parent,'target-work');
 fs.mkdirSync(root);fs.mkdirSync(workBase);
 fs.cpSync(path.join(f.beforeRoot,'docs'),path.join(root,'docs'),{recursive:true});
 fs.cpSync(path.join(f.beforeRoot,SLUG),path.join(workBase,SLUG),{recursive:true});
 const pins=JSON.parse(fs.readFileSync(path.join(here,'required-runtime.json')));
 for(const rel of Object.keys(pins)) {const file=path.join(root,rel);fs.mkdirSync(path.dirname(file),{recursive:true});const bytes=Buffer.from('SYNTHETIC_RUNTIME_NOT_EXECUTED '+rel);fs.writeFileSync(file,bytes);pins[rel]=sha(bytes);}
 const p=planPinnedTransition(f.options); const common={schema_version:1,slug:SLUG,plan_sha256:p.plan_sha256,pinned_lexicon_sha256:p.plan.pinned_lexicon_sha256,pinned_head_event_sha256:p.plan.pinned_head_event_sha256,before_source_sha256:p.plan.before_source_sha256,after_source_sha256:p.plan.after_source_sha256};
 const reviewBytes=json({...common,kind:'a01_pinned_historical_lexicon_20261017_review',verdict:'PASS',independent:true,reviewer:'synthetic-reviewer'});
 const receiptBytes=json({...common,kind:'a01_pinned_historical_lexicon_20261017_receipt',operator:'synthetic-operator',owner_approval_ref:'SYNTHETIC_NOT_AUTHORITY',review_sha256:sha(reviewBytes),paid_calls:0,shared_lexicon_writes:0});
 const {snapshotRoot,...options}=f.options;
 return {f,root,workBase,options:{...options,syntheticRuntimePins:pins,root,workBase,beforeRoot:f.beforeRoot,reviewBytes,receiptBytes,expectedPlanSha256:p.plan_sha256,ownerApprovalRef:'SYNTHETIC_NOT_AUTHORITY'}};
}
test('split-volume adoption commits exact sources and retains scoped STOP',t=>{
 const i=input(t);const beforeShared=fs.readFileSync(path.join(i.root,'docs/videos/lexicon.json'));
 const r=adoptPinnedTransition(i.options);
 assert.equal(r.adoption,'COMMITTED_HELD');assert.equal(r.production_status,'HOLD');assert.equal(r.release_allowed,false);
 assert.ok(fs.existsSync(path.join(i.workBase,SLUG,'STOP')));
 assert.deepEqual(fs.readFileSync(path.join(i.root,'docs/videos/lexicon.json')),beforeShared);
 assert.equal(fs.existsSync(path.join(i.root,'docs/videos',SLUG,'story-lexicon/pending.json')),false);
 assert.throws(()=>adoptPinnedTransition(i.options),/ADOPTION_ALREADY_PINNED/);
});
test('interruption at every publication boundary retains STOP and a reader fence',t=>{
 for(const phase of ['work-intent','docs-intent','immutable-files','auto-state','current-pointer','committed-receipt','docs-fence-cleared']) {
  const i=input(t);
  assert.throws(()=>adoptPinnedTransition({...i.options,checkpoint:p=>{if(p===phase)throw Error('synthetic-crash');}}),/synthetic-crash/);
  assert.ok(fs.existsSync(path.join(i.workBase,SLUG,'STOP')));
  const intents=path.join(i.workBase,SLUG,'story/lexicon-intents');
  assert.ok(fs.readdirSync(intents).some(n=>n.endsWith('.json')));
  assert.throws(()=>adoptPinnedTransition(i.options),/ADOPTION_PENDING_TRANSACTION/);
  if(phase==='committed-receipt' || phase==='docs-fence-cleared') {
    const recovered=adoptPinnedTransition({...i.options,recoverCommitted:true});
    assert.equal(recovered.adoption,'RECOVERED_COMMITTED_HELD');assert.equal(recovered.release_allowed,false);
    assert.ok(fs.existsSync(path.join(i.workBase,SLUG,'STOP')));
  } else assert.throws(()=>adoptPinnedTransition({...i.options,recoverCommitted:true}),/ADOPTION_PARTIAL_REQUIRES_REVIEW/);
 }
});
test('wrong deployed runtime and source drift refuse publication',t=>{
 for(const mode of ['runtime','source']) {const i=input(t);
  if(mode==='runtime')fs.appendFileSync(path.join(i.root,'tools/video/core/lexicon-store.mjs'),'// drift');
  else fs.appendFileSync(path.join(i.workBase,SLUG,'auto.json'),' ');
  assert.throws(()=>adoptPinnedTransition(i.options));
  assert.equal(fs.existsSync(path.join(i.root,'docs/videos',SLUG,'story-lexicon/current.json')),false);
 }
});
