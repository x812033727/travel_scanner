import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const media=path.resolve(process.argv[2]||'');
if(!process.argv[2])throw Error('Pass episode media directory; add --check to verify the recorded decision.');
const base='docs/videos/series-plans/ou-de-jianghu/visual-development/';
const read=f=>JSON.parse(fs.readFileSync(f,'utf8'));
const sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const expected={
  'handoff/asset-manifest.json':'cbda063982c38b4135745e798659e51c88a1e529b53da5b2a810cbe68af9f540',
  'handoff/finalization-20261009.json':'bbcf9dbfc630ff3dc8e9d06a465324b7d8a908381bad09b3d7079322b794d490',
  'episode-plan/budget-and-batches.json':'2592cb5e0c6c3f41e4b3a4a774beac9a604490c02ebc4fcaf6903db691d1e0c2'
};
for(const [f,h]of Object.entries(expected))assert.equal(sha(base+f),h,f);
const manifest=read(base+'handoff/asset-manifest.json');
assert.equal(manifest.assets.length,146);
for(const s of manifest.source_files)assert.equal(sha(s.path),s.sha256,s.path);
for(const a of manifest.assets){const f=path.join(media,a.file.replace('<VIDEO_WORKDIR>/ou-de-jianghu-e001/',''));assert.equal(sha(f),a.sha256,a.key);}
const video=path.join(media,'plan/preflight-20261009-v4/video.json');
assert.equal(sha(video),'cb341b457f28e5139cff6f0528722d2a0facebf8cfea90423aec572ed71ebd17');
const v4Budget=path.join(media,'plan/preflight-20261009-v4/budget-and-batches.json');
assert.equal(sha(v4Budget),'f62d04c4bbc99825d847a8818e1a0229e335f21f77f16598626e1d24741199a2');
const budget=read(v4Budget),originalBudget=read(base+'episode-plan/budget-and-batches.json');
assert.equal(budget.source_video_sha256,sha(video));
for(const key of ['totals','periods','rows','batches'])assert.deepEqual(budget[key],originalBudget[key],key+' changed between v3 and v4');
const lockPath=path.join(media,'plan/lock.json'),lock=read(lockPath);
assert.equal(lock.route,'hailuo');assert.equal(lock.plan,'hailuo:max');assert.equal(lock.hailuo_model,'h3');
assert.equal(lock.resolution,'2k');assert.equal(lock.web_assist,'off');assert.equal(lock.clip_takes,2);
assert.equal(Object.keys(lock.shots).length,455);
assert.deepEqual(lock.pilot,['a02-s035','a02-s036','a02-s037']);
const reply='採用素材與 v4，按此點數上限鎖定 plan';
assert.equal(lock.note,reply);
const file=base+'handoff/adoption-decision-20261009.json';
const external=path.join(media,'adoption/20261009/owner-adoption.json');
const {owner_accepted: historicalFanOwnerFlag,...fanPolicy}=manifest.fan_reference_policy;
const decision={schema_version:1,episode:'ou-de-jianghu-e001',
  decision_recorded_at_utc:'2026-10-08T17:39:40Z',recorded_at_utc:'2026-10-08T17:48:07.518Z',
  receipt_corrected_at_utc:'2026-10-08T17:50:42Z',
  receipt_corrections:'Separate decision capture from receipt creation; bind unchanged v4 budget; label the copied pre-adoption fan owner flag as historical. Initial receipt preserved outside Git; no scope, media or lock change.',
  status:'owner_adopted_reference_package_and_hailuo_plan_locked',
  user_decision:{route_reply:'使用hailuoai',
    question:'已確認使用 Hailuo AI。是否正式採用這 146 張素材與 v4，先鎖定 Hailuo 點數計畫：本期最多使用現有點數 26,980.8 點（含預留），首批三鏡上限 316.8 點包含在內；第二期有額度才續做，不購點、不續訂、不扣 API 費用？目前 Mokaair 判圖關閉，look 會如實保留待處理，本輪先完成 plan 鎖定。',
    answer:reply,authorization_source:'direct human reply in this task'},
  accepted_scope:{episode_one_only:true,asset_count:146,working_video_version:'v4',
    reference_uses_only:true,existing_use_limits_retained:true,footage_or_lipsync_accepted:false},
  spending_limits:{provider:'hailuo-web',existing_entitlement_only:true,
    current_period_cap_including_reserve_credits:26980.8,pilot_cap_including_reserve_credits:316.8,
    pilot_is_included_in_period_cap:true,second_period_cap_including_reserve_credits:21753.6,
    second_period_condition:'Proceed only when that period actually has available entitlement; no purchase or renewal authorized.',
    total_two_period_cap_including_reserve_credits:48734.4,
    topup_authorized:false,subscription_purchase_or_renewal_authorized:false,api_spend_authorized_usd:0,
    historical_cash_proposal_usd:677.4817,historical_cash_proposal_approved:false,
    native_lock_cash_estimates_authorize_payment:false,
    enforcement:'Native plan totals do not enforce this manual two-period envelope. Check actual available credits, receipts, batch membership and remaining cap before each submission; stop at the cap. Pilot acceptance is required before expanding.'},
  bound_files:Object.entries(expected).map(([f,h])=>({file:base+f,sha256:h})),
  working_budget:{file:'<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261009-v4/budget-and-batches.json',sha256:sha(v4Budget),
    source_video_sha256:budget.source_video_sha256,rows_batches_periods_and_totals_unchanged_from_bound_repo_v3_budget:true},
  working_video:{file:'<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261009-v4/video.json',sha256:sha(video)},
  native_plan_lock:{file:'<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/lock.json',sha256:sha(lockPath),created_at:lock.created_at,
    route:lock.route,plan:lock.plan,hailuo_model:lock.hailuo_model,resolution:lock.resolution,web_assist:lock.web_assist,
    clip_takes:lock.clip_takes,hashes:lock.hashes,shot_count:Object.keys(lock.shots).length,pilot:lock.pilot,
    machine_totals:lock.totals,manual_budget_precedence:'Use the bound manual budget and this narrower owner spending authorization. Machine risk expectations and historic subscription price are not new spending authority.'},
  assets:manifest.assets.map(a=>({key:a.key,category:a.category,character_id:a.character_id,use:a.use,
    file:a.file,sha256:a.sha256,owner_accepted_for_reference_use:true,limitations:a.limitations})),
  retained_policies:{fan:{...fanPolicy,historical_source_owner_accepted:historicalFanOwnerFlag,owner_accepted_for_reference_use:true},mouth:manifest.static_mouth_reference,
    cold_room:manifest.cold_room,native_size:manifest.resolution_disposition},
  gate_state_at_lock:{plan_locked:true,look_approved:false,script_v4_approved:false,audio_approved:false,
    storyboard_approved:false,ready_to_submit_clips:false,
    look_blocker:'True judge is required. Mokaair drama is disabled and this decision authorizes no API spending.',
    script_note:'v4 screenplay includes changed silent-action descriptions; canonical script approval must not stand in for v4.',
    implementation_note:'Normal workdir holds the lock and imported pending candidates; every production operation must continue using the v4 file until a separately coordinated canonical adoption occurs.'},
  paid_actions_in_this_turn:{api_requests:0,hailuo_generation_requests:0,purchased_credits:0,renewals:0},
  source_files:manifest.source_files};
if(process.argv.includes('--check')){assert.deepEqual(read(file),decision,'Adoption receipt drifted');assert.deepEqual(read(external),decision,'External adoption receipt drifted');}
else if(process.argv.includes('--correct-initial-receipt')){
  const initial='ae0fa507c3b5ffe2c84968b4acc037a637cbd3f0fe030114fd025a898bb34a3e';
  assert.equal(sha(file),initial);assert.equal(sha(external),initial);
  fs.writeFileSync(path.join(media,'adoption/20261009/owner-adoption-initial-before-receipt-corrections.json'),fs.readFileSync(external),{flag:'wx'});
  fs.writeFileSync(file,JSON.stringify(decision,null,2)+'\n');fs.writeFileSync(external,JSON.stringify(decision,null,2)+'\n');
}
else{assert.ok(!fs.existsSync(file),'Refuse overwriting a recorded adoption');fs.writeFileSync(file,JSON.stringify(decision,null,2)+'\n');
  fs.writeFileSync(external,JSON.stringify(decision,null,2)+'\n',{flag:'wx'});}
console.log(JSON.stringify({accepted_assets:146,locked_shots:455,plan_lock_sha256:sha(lockPath),adoption_sha256:sha(file),look_approved:false,api_spend_authorized_usd:0}));
