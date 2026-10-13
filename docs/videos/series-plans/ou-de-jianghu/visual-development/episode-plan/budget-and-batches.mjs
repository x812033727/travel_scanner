#!/usr/bin/env node
// Offline arithmetic; does not query an account or submit a provider request.
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const out=path.resolve(process.argv[2]||'C:/Users/x8120/mokaair-work/videos/ou-de-jianghu-e001/plan/preflight-20261008-v3');
const read=n=>JSON.parse(fs.readFileSync(path.join(out,n),'utf8'));
const plan=read('shot-plan.json'),risk=read('risk-ledger.json'),coverage=read('camera-ledger.json'),receipt=read('proposal-receipt.json');
const map=new Map(risk.map(r=>[r.id,r])),round=n=>Math.round(n*10000)/10000;
const rate={checked_on:'2026-10-08',hailuo_max_month_usd:216,hailuo_max_month_credits:27000,h3_2k_credits_per_second:12,
 image_output_1k_or_2k:0.134,image_input_per_reference:0.0011,image_text_per_million:2,judge_budget_per_call:0.01,
 tts_model:'gemini-3.8-flash-tts',tts_input_per_million:0.5,tts_output_per_million:9,audio_tokens_per_second:25,music_per_song:0.08,
 urls:['https://hailuoai.video/zh-Hant/subscribe','https://ai.google.dev/gemini-api/docs/pricing'],
 notes:['Hailuo subscription UI observed Max $216/month and 27000/month; account header 27000 was a one-time visible snapshot, not a future reservation or payment authorization.','H3 12 credits/s is consistent with the current 2250s/27000-credit UI and the 2026-10-04 recorded 5s/60-credit measurement.','Google standard paid rates; image input assumes at most 4 references and 1000 text tokens per image request. Judge $0.01 is repository accounting, not a provider quote.','The repository defaults TTS to gemini-3.8-flash-tts, but the actual server runtime model and account quota have NOT been queried.','Built-in imagegen does not return USD billing. Request counts are a separate envelope, never priced as Gemini API invoices.']};
const pilot=new Set(['a02-s035','a02-s036','a02-s037']);
const spaces=['gate','forge','tower','council','terrace','court','port','room','corridor'];
const used=new Set();
function batch(name,shots){
 const buys=shots.filter(s=>s.visual==='clip'&&!used.has(s.id));
 // Earlier source masters before dependent cuts; within remaining work test the higher risks first.
 buys.sort((a,b)=>Number(Boolean(b.cuts?.length))-Number(Boolean(a.cuts?.length))||'CBA'.indexOf(map.get(a.id).human_grade)-'CBA'.indexOf(map.get(b.id).human_grade));
 buys.forEach(s=>used.add(s.id));
 const one=buys.reduce((n,s)=>n+s.cost.one,0),expected=buys.reduce((n,s)=>n+s.cost.one*map.get(s.id).expected_takes,0),cap=one*2;
 return {name,buys:buys.map(s=>s.id),dependent_cuts:shots.filter(s=>s.visual==='cut').map(s=>({id:s.id,...s.source})),stills:shots.filter(s=>s.visual==='still').map(s=>s.id),one_credits:one,expected_credits:round(expected),cap_credits:cap,expected_plus_10pct:round(expected*1.1),cap_plus_10pct:round(cap*1.1),checkpoint:'實速接完整場，身份/左右/道具/燈光/表演/聲音通過後才開下一場；pilot須站主觀看後放量'};
}
const batches=[batch('00 三鏡小樣',plan.shots.filter(s=>pilot.has(s.id)))];
for(const key of spaces){const ids=new Set(coverage.rows.filter(r=>r.space===key).map(r=>r.id));batches.push(batch(`${key} 場景批`,plan.shots.filter(s=>ids.has(s.id)&&!pilot.has(s.id))));}
if(used.size!==plan.counts.clips)throw Error('A clip is missing or duplicated in the batch plan');
// Two separate monthly allocations; a 10% reserve is held within EACH 27000 envelope.
const periods=[{name:'額度期A',capacity:27000,buys:[],cap:0,expected:0},{name:'額度期B',capacity:27000,buys:[],cap:0,expected:0}];
let period=0;
const byId=new Map(plan.shots.map(s=>[s.id,s]));
for(const b of batches)for(const id of b.buys){const s=byId.get(id);if((periods[period].cap+s.cost.cap)*1.1>27000)period++;
 if(!periods[period])throw Error('Two monthly envelopes insufficient');
 const p=periods[period];p.buys.push(id);p.cap+=s.cost.cap;p.expected+=s.cost.one*map.get(id).expected_takes;
}
for(const p of periods){p.expected=round(p.expected);p.cap_plus_reserve=round(p.cap*1.1);p.expected_plus_reserve=round(p.expected*1.1);p.spare_after_cap_reserve=round(p.capacity-p.cap_plus_reserve);}
const firsts=plan.counts.shots-plan.counts.cuts,ends=plan.shots.filter(s=>s.end_frame_planned).length;
const imageInput=4*rate.image_input_per_reference+1000/1e6*rate.image_text_per_million;
const keyUnit=rate.image_output_1k_or_2k+imageInput+rate.judge_budget_per_call;
const endUnit=rate.image_output_1k_or_2k+imageInput;
const imageMean=1.35; // Editorial allowance, not observed acceptance probability.
const clipExpected=round(batches.reduce((n,b)=>n+b.expected_credits,0));
const clipsOne=plan.totals.clip.one,clipsCap=plan.totals.clip.cap;
const rows=[
 {id:'existing-portraits',unit:'retained asset',quantity:36,one_usd:null,expected_usd:null,cap_usd:null,note:'9 latest concepts + 27 independent views already delivered; retain hashes, no rebuy. Prior imagegen billing unknown.'},
 {id:'animation-reference',unit:'new imagegen request target',quantity:74,one_requests:74,expected_requests:97,cap_requests:148,one_usd:null,expected_usd:null,cap_usd:null,note:'9×5 separate angles + 9 expressions sheets + 9 action sheets + 9 detail sheets + 2 comparison sheets. Existing front full bodies reused. At most 2 requests per asset in this proposal; existing extra versions must be ledgered, not hidden.'},
 {id:'scene-prop-reference',unit:'new imagegen request target',quantity:29,one_requests:29,expected_requests:38,cap_requests:58,one_usd:null,expected_usd:null,cap_usd:null,note:'17 master environments + 2 state views + 7 prop boards + 3 controlled details. Concept art does not count as 450 shot keyframes.'},
 {id:'look-import-judge',unit:'character',quantity:9,one_usd:0.09,expected_usd:0.135,cap_usd:0.18,note:'Proposed only if native import performs one $0.01 budgeted judge per character; actual contract determines calls. No extra image generation charged here.'},
 {id:'look-fallback-reserve',unit:'fallback image',quantity:27,one_usd:0,expected_usd:0,cap_usd:round(54*keyUnit),note:'Ring-fenced optional 9×3×2 fallback if importing existing art is inadequate. No automatic execution or route change.'},
 {id:'keyframe-first',unit:'image+judge',quantity:firsts,one_usd:round(firsts*keyUnit),expected_usd:round(firsts*keyUnit*imageMean),cap_usd:round(firsts*keyUnit*3),note:'1K native pipeline images; 3 take cap. Input budget includes 4 image refs and 1000 text tokens per request. AI image 1K/2K same output rate does not make pipeline output 2K.'},
 {id:'keyframe-end',unit:'image',quantity:ends,one_usd:round(ends*endUnit),expected_usd:round(ends*endUnit*imageMean),cap_usd:round(ends*endUnit*3),note:'s036/s037/Luo-s043 proposed end frames; native tool does not automatically judge these, manual QA mandatory.'},
 {id:'tts',unit:'seconds+input',quantity:1403.533,one_usd:round(1403.533*25*9/1e6+30000*0.5/1e6),expected_usd:round((1403.533*25*9/1e6+30000*0.5/1e6)*1.3),cap_usd:1,note:'Conservative whole timeline as audio ceiling, 30000 input tokens allowance; up to 2 takes per line, $1 hard cap including input, reset/re-price if 2027 rate applies.'},
 {id:'clip-import-judge',unit:'imported clip',quantity:plan.counts.clips,one_usd:round(plan.counts.clips*0.01),expected_usd:round(plan.counts.clips*1.4*0.01),cap_usd:round(plan.counts.clips*2*0.01),note:'Only if --judge used; imported takes ledgered even when rejected. Model-token invoice may differ from $0.01 bookkeeping.'},
 {id:'music',unit:'track',quantity:1,one_usd:0.08,expected_usd:0.08,cap_usd:0.16,note:'Original guqin/xiao low-strings instrumental prompt retained; at most 2 candidates, no extra song scope.'},
 {id:'asr-review',unit:'review allocation',quantity:1,one_usd:0.12,expected_usd:0.24,cap_usd:1,note:'Budget allocation, not a verified current server invoice; keep real ASR/review requirements if production route requires them.'},
 {id:'sfx-and-render',unit:'local work',quantity:1,one_usd:0,expected_usd:0,cap_usd:0,note:'Local render and existing authorized SFX only; new sound service purchases outside scope.'},
];
const api={one:round(rows.reduce((n,r)=>n+(r.one_usd||0),0)),expected:round(rows.reduce((n,r)=>n+(r.expected_usd||0),0)),cap:round(rows.reduce((n,r)=>n+(r.cap_usd||0),0))};
api.expected_plus_10pct=round(api.expected*1.1);api.cap_plus_10pct=round(api.cap*1.1);
const usdPerCredit=216/27000;
const data={version:1,status:'proposal-only-not-spend-authorization',rate,rows,batches,periods,
 totals:{imagegen_new_target:103,imagegen_expected_requests:135,imagegen_request_cap:206,imagegen_usd:null,
  clip_one_credits:clipsOne,clip_expected_credits:clipExpected,clip_cap_credits:clipsCap,clip_expected_plus_10pct:round(clipExpected*1.1),clip_cap_plus_10pct:round(clipsCap*1.1),
  clip_allocated_usd:{one:round(clipsOne*usdPerCredit),expected:round(clipExpected*usdPerCredit),cap:round(clipsCap*usdPerCredit)},api,
  full_prospective_subscription_charge_ceiling:432,known_subscription_plus_api_cap_reserve_usd:round(432+api.cap_plus_10pct),
  note:'Two 27000-credit allocation periods are required. $432 is 2×$216 subscription cost if both periods have to be newly paid, not a checkout or top-up quote. Existing subscription sunk cost/allocation is unknown. Credits do not imply USD cash savings. Built-in imagegen USD and tax are not included in this known subtotal.'},
 assertions:{every_clip_once:used.size===plan.counts.clips,all_period_cap_reserve_within_capacity:periods.every(p=>p.cap_plus_reserve<=p.capacity),manual_c_only_in_pilot:risk.filter(r=>r.human_grade==='C').every(r=>pilot.has(r.id)),source_cut_ranges_within_purchase:plan.shots.filter(s=>s.visual==='cut').every(s=>s.source.from_s+s.need_s<=byId.get(s.source.shot).buy_s),no_source_changed:receipt.source_files_still_match},
 source_video_sha256:receipt.video_sha256};
fs.writeFileSync(path.join(out,'budget-and-batches.json'),JSON.stringify(data,null,2)+'\n');
fs.writeFileSync(path.join(out,'budget-and-batches.sha256'),createHash('sha256').update(fs.readFileSync(path.join(out,'budget-and-batches.json'))).digest('hex')+'\n');
console.log(JSON.stringify({totals:data.totals,periods:periods.map(({buys,...r})=>({...r,clips:buys.length})),assertions:data.assertions},null,2));
if(Object.values(data.assertions).some(x=>!x))process.exitCode=1;
