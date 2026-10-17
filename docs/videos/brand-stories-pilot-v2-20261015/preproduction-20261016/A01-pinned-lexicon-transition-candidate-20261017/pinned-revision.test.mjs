import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import {hostFixture} from '../A01-e640-round20-offline-bridge-20261017/synthetic-fixture.mjs';
import {planPinnedTransition,preparePinnedEvent} from './transition.mjs';
import {planOfflineRevision,prepareOfflineRevision,verify82Fixture,OFFLINE_PINS} from './pinned-revision-plan.mjs';
const SLUG='story-rolling-suitcase-v2';
const sha=b=>createHash('sha256').update(b).digest('hex');const json=v=>Buffer.from(JSON.stringify(v)+'\n');
function fixture(t) {
 const f=hostFixture(t),before81Root=path.join(f.parent,'pinned-81'),after82Root=path.join(f.parent,'pinned-82');
 const baseline={snapshotRoot:f.before80Root,oldLexiconFile:f.options.oldLexiconFile,pins:f.pins80,expectedOldSha:f.options.expectedOldSha,expectedNewSha:f.options.expectedNewSha};
 const p=planPinnedTransition(baseline);const common={schema_version:1,slug:SLUG,plan_sha256:p.plan_sha256,pinned_lexicon_sha256:p.plan.pinned_lexicon_sha256,pinned_head_event_sha256:p.plan.pinned_head_event_sha256,before_source_sha256:p.plan.before_source_sha256,after_source_sha256:p.plan.after_source_sha256};
 const reviewBytes=json({...common,kind:'a01_pinned_historical_lexicon_20261017_review',verdict:'PASS',independent:true,reviewer:'synthetic-reviewer'});
 const receiptBytes=json({...common,kind:'a01_pinned_historical_lexicon_20261017_receipt',operator:'synthetic-operator',owner_approval_ref:'SYNTHETIC_NOT_AUTHORITY',review_sha256:sha(reviewBytes),paid_calls:0,shared_lexicon_writes:0});
 const prepared81=preparePinnedEvent({...baseline,reviewBytes,receiptBytes});fs.cpSync(f.before80Root,before81Root,{recursive:true});
 for(const [rel,bytes] of Object.entries(prepared81.files))f.write(before81Root,rel,bytes);
 const options={before80Root:f.before80Root,before81Root,after82Root,oldLexiconFile:baseline.oldLexiconFile,pins80:f.pins80,expectedOldSha:baseline.expectedOldSha,expectedNewSha:baseline.expectedNewSha};
 const proposed=planOfflineRevision(options),p82=proposed.plan;
 const common82={schema_version:1,slug:SLUG,plan_sha256:proposed.plan_sha256,round22_manifest_sha256:OFFLINE_PINS.round22_manifest_sha256,before_source_sha256:p82.previous_81_pins.source_composite_sha256,after_source_sha256:p82.after_source_composite_sha256};
 options.reviewBytes=json({...common82,kind:'a01_round22_existing_story_independent_review',verdict:'PASS',independent:true,reviewer:'synthetic-new-editor'});
 options.receiptBytes=json({...common82,kind:'a01_round22_existing_story_revision_receipt',event_id:OFFLINE_PINS.event_id,review_sha256:sha(options.reviewBytes),paid_calls:0,auto_retry:false,operator:'synthetic-operator',owner_approval_ref:'SYNTHETIC_NOT_AUTHORITY'});
 const p82prepared=prepareOfflineRevision(options);fs.cpSync(before81Root,after82Root,{recursive:true});
 for(const [rel,bytes] of Object.entries({...p82prepared.replacements,...p82prepared.files}))f.write(after82Root,rel,bytes);
 return {f,options,proposed};
}
test('pinned chapter revision preserves pronunciation version, history and narrative failure',t=>{
 const {options,proposed}=fixture(t);const result=verify82Fixture(options);
 assert.equal(result.integrity,'LOCAL_82_EVENT_TRANSITION_PASS');assert.equal(result.paid_work_allowed,false);assert.equal(result.production_status,'HOLD');
 assert.equal(proposed.plan.before_source_hashes.lexicon,proposed.plan.after_source_hashes.lexicon);
 const before=JSON.parse(fs.readFileSync(path.join(options.before81Root,SLUG,'auto.json'))),after=JSON.parse(fs.readFileSync(path.join(options.after82Root,SLUG,'auto.json')));
 assert.equal(after.story.lexicon_sha256,before.story.lexicon_sha256);assert.equal(after.story.lexicon_head_event_sha256,before.story.lexicon_head_event_sha256);
 assert.deepEqual(after.story.narrative,before.story.narrative);assert.equal(after.story.narrative_fixes,before.story.narrative_fixes);
 assert.equal(after.verified,false);assert.equal(after.listener_done,false);
});
test('82 readback rejects an added snapshot file and shared dictionary change',t=>{
 for(const mode of ['snapshot','shared']) {
  const {f,options}=fixture(t);
  f.write(options.after82Root,mode==='snapshot'?'docs/videos/'+SLUG+'/story-lexicon/extra.json':'docs/videos/lexicon.json',json({changed:true}));
  assert.throws(()=>verify82Fixture(options),/PINNED_SNAPSHOT_CHANGED|SHARED_LEXICON_CHANGED/);
 }
});
