#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const out=path.resolve(process.argv[2]||'C:/Users/x8120/mokaair-work/videos/ou-de-jianghu-e001/plan/preflight-20261008-v3');
const here=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(out,n),'utf8'));
const receipt=read('proposal-receipt.json'),plan=read('shot-plan.json'),risk=read('risk-ledger.json'),camera=read('camera-ledger.json'),budget=read('budget-and-batches.json'),verification=read('verification.json'),render=read('animatic-render-check.json');
const sha=b=>createHash('sha256').update(b).digest('hex');
const rows=plan.shots.map(s=>{const c=camera.rows.find(c=>c.id===s.id),r=risk.find(r=>r.id===s.id);return {id:s.id,space:c.space,phase:c.phase,station:c.station,axis:c.axis,camera:s.camera,visual:s.visual,source:s.source,need_s:s.need_s,buy_s:s.buy_s,machine_risk:s.risk.grade,human_risk:r.human_grade,reason:r.reason,first_frame:c.first_frame,end_frame:c.end_frame,prompt_sha256:s.web_prompt?.sha256||s.prompt?.sha256||null};});
const summary={schema_version:1,status:'reviewable-proposal-awaiting-concrete-package-decision',version:'v3',source_sha256:receipt.source_sha256,source_unchanged:Object.entries(receipt.source_sha256).every(([f,h])=>sha(fs.readFileSync(f))===h),proposal_video_sha256:receipt.video_sha256,dialogue_and_duration_unchanged:receipt.dialogue_and_duration_unchanged,counts:receipt.counts,original_setups:receipt.original_setups.reduce((n,r)=>n+r.setups,0),proposed_setups:receipt.proposed_setups.reduce((n,r)=>n+r.setups,0),original_machine_c:risk.filter(r=>r.original_machine_c),manual_c:receipt.manual_c,totals:budget.totals,render,checks:verification.results.map(({name,exit_code})=>({name,exit_code})),artifact_sha256:verification.sha256,budget_sha256:sha(fs.readFileSync(path.join(out,'budget-and-batches.json'))),native_lock_written:false,paid_requests_submitted_by_planning_agent:0,external_artifact_directory:'<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261008-v3'};
fs.writeFileSync(path.join(here,'proposal-summary.json'),JSON.stringify(summary,null,2)+'\n');
fs.writeFileSync(path.join(here,'camera-and-risk-ledger.json'),JSON.stringify({version:'v3',source_video_sha256:receipt.video_sha256,spaces:camera.spaces,rows},null,2)+'\n');
fs.writeFileSync(path.join(here,'budget-and-batches.json'),JSON.stringify(budget,null,2)+'\n');
const lines=['# 逐鏡鏡位與風險索引（v3）','','完整首尾狀態與軸線見 [camera-and-risk-ledger.json](camera-and-risk-ledger.json)；正文/每鏡提示雜湊及外部產物指紋見 [proposal-summary.json](proposal-summary.json)。本表不是正式 lock。','','| 鏡號 | 空間／段落 | 主站位 | 類型 | 估剪入秒 | 買秒 | 程式／人工 | 來源切 |','| --- | --- | --- | --- | ---: | ---: | --- | --- |'];
for(const r of rows)lines.push(`| ${r.id} | ${r.space}/${r.phase} | ${r.station} | ${r.visual} | ${r.need_s} | ${r.buy_s||'—'} | ${r.machine_risk}/${r.human_risk} | ${r.source?`${r.source.shot}@${r.source.from_s}s`:'—'} |`);
fs.writeFileSync(path.join(here,'shot-index.md'),lines.join('\n')+'\n');
console.log(JSON.stringify({shots:rows.length,source_unchanged:summary.source_unchanged,summary_sha256:sha(fs.readFileSync(path.join(here,'proposal-summary.json')))},null,2));
