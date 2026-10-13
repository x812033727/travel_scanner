#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
const base='docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan';
const out=path.resolve(process.argv[2]||'C:/Users/x8120/mokaair-work/videos/ou-de-jianghu-e001/plan/preflight-20261008-v3');
const video=path.join(out,'video.json');
const flags=['--route','hailuo','--plan','hailuo:max','--hailuo-model','h3','--resolution','2k','--handle','0.5','--clip-takes','2','--expected-takes','1.2,1.5,2','--pilot','a02-s035,a02-s036,a02-s037'];
async function run(name,args){
 const start=new Date().toISOString();
 const r=await new Promise((resolve,reject)=>{
  const p=spawn(process.execPath,args,{cwd:process.cwd(),windowsHide:true});let stdout='',stderr='';
  p.stdout.on('data',x=>stdout+=x);p.stderr.on('data',x=>stderr+=x);p.on('error',reject);p.on('close',code=>resolve({code,stdout,stderr}));
 });
 fs.writeFileSync(path.join(out,name+'.stdout'),r.stdout);fs.writeFileSync(path.join(out,name+'.stderr'),r.stderr);
 console.log(`${name}: exit ${r.code}`);
 return {name,args,started_at:start,finished_at:new Date().toISOString(),exit_code:r.code,stdout_file:name+'.stdout',stderr_file:name+'.stderr'};
}
fs.mkdirSync(out,{recursive:true});
const results=[];
results.push(await run('build',[`${base}/build-proposal.mjs`,out]));
if(results[0].exit_code)throw Error('Proposal build failed');
results.push(await run('animatic',['.agents/skills/animation-preproduction/scripts/animatic.mjs','--file',video,'--workdir',out,'--out',path.join(out,'animatic.html'),...flags]));
fs.copyFileSync(path.join(out,'animatic.html'),path.join(out,'animatic-upstream.html'));
results.push(await run('animatic-scoped-render',[`${base}/render-proposal.mjs`,out]));
results.push(...await Promise.all([
run('lint',['tools/video/cli.mjs','lint','--file',video,'--json']),
run('craft',['.agents/skills/youtube-video/scripts/drama_craft_check.mjs',video,'--strict','--json']),
run('reading',['.agents/skills/animation-camera/scripts/shot_reading.mjs',video,'--route','hailuo','--strict','--json']),
run('plan-strict',['.agents/skills/animation-preproduction/scripts/shot_plan.mjs',video,'--workdir',out,...flags,'--json','--strict']),
run('ready',['.agents/skills/animation-preproduction/scripts/plan_lock.mjs','--file',video,'--workdir',out,...flags,'--ready','--json']),
]));
const hashes=Object.fromEntries(['video.json','animatic.html','shot-plan.json','camera-ledger.json','risk-ledger.json','proposal-edits.json'].map(f=>[f,createHash('sha256').update(fs.readFileSync(path.join(out,f))).digest('hex')]));
fs.writeFileSync(path.join(out,'verification.json'),JSON.stringify({created_at:new Date().toISOString(),offline_only:true,no_lock_written:!fs.existsSync(path.join(out,'plan/lock.json')),results,sha256:hashes},null,2)+'\n');
console.log(JSON.stringify({out,results:results.map(r=>({name:r.name,exit:r.exit_code})),sha256:hashes},null,2));
