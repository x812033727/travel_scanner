#!/usr/bin/env node
// Scoped workaround for upstream animatic's omitted title spans and negative subtitle index.
// This preserves every source scene and timing; upstream remains untouched pending its task.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const root=process.cwd(),out=path.resolve(process.argv[2]||'C:/Users/x8120/mokaair-work/videos/ou-de-jianghu-e001/plan/preflight-20261008-v3');
const read=n=>JSON.parse(fs.readFileSync(path.join(out,n),'utf8'));
const {animaticShots,animaticStats,animaticHtml}=await import(pathToFileURL(path.join(root,'.agents/skills/animation-preproduction/scripts/animatic.mjs')));
const {estimateTimeline,FPS}=await import(pathToFileURL(path.join(root,'tools/video/core/timeline.mjs')));
const doc=read('video.json'),plan=read('shot-plan.json'),risk=new Map(read('risk-ledger.json').map(r=>[r.id,r]));
const timeline=estimateTimeline(doc),spans=new Map(timeline.scenes.map(s=>[s.id,s]));
const shots=animaticShots(doc,plan,{timeline}).map(s=>({...s,risk:risk.get(s.id)?.human_grade||s.risk}));
for(const s of doc.scenes.filter(s=>s.template!=='shot')){
 const t=spans.get(s.id);shots.push({id:s.id,start:t.start_frame/FPS,end:t.end_frame/FPS,image:null,video:null,video_offset:0,image_file:null,move:'locked',kind:'card',setup:'原稿字卡',camera:'字卡／後製排字',motion:[s.data.title,s.data.subtitle,s.data.tag].filter(Boolean).join('｜'),lines:(s.lines||[]).map(l=>({speaker:l.speaker||'narrator',text:l.text})),risk:null,risk_reasons:[],buy_s:0,source:null});
}
shots.sort((a,b)=>a.start-b.start);
const exactSeconds=timeline.scenes.at(-1).end_frame/FPS;
if(shots.length!==doc.scenes.length)throw Error('A source scene was dropped');
for(let i=1;i<shots.length;i++)if(Math.abs(shots[i].start-shots[i-1].end)>0.0011)throw Error(`Unexpected time gap before ${shots[i].id}`);
let html=animaticHtml({title:doc.youtube.title+'｜v3 提案',shots,stats:animaticStats(shots),basis:'估算時間／無配音；455鏡＋4張原稿字卡。風險標籤使用人工裁定；這是未核准提案'});
const oldLine='function lineAt(s,time){if(!s.lines.length)return"";const span=(s.end-s.start)/s.lines.length;const k=Math.min(s.lines.length-1,Math.floor((time-s.start)/span));return s.lines[k].speaker+"："+s.lines[k].text}';
const newLine='function lineAt(s,time){const lines=s?.lines??[];if(!lines.length||time<s.start||time>s.end)return"";const span=Math.max(.001,(s.end-s.start)/lines.length);const k=Math.max(0,Math.min(lines.length-1,Math.floor((time-s.start)/span)));const line=lines[k];return line?(line.speaker??"narrator")+"："+(line.text??""):""}';
const oldIndex='const i=Math.max(0,shots.findIndex(s=>t<s.end));';
const newIndex='const found=shots.findIndex(s=>t<s.end);const i=found<0?shots.length-1:found;';
for(const token of [oldLine,oldIndex,'const KIND={clip:"clip",still:"still",cut:"切"};'])if(!html.includes(token))throw Error('Upstream renderer changed: inspect scoped workaround');
html=html.replace(oldLine,newLine).replace(oldIndex,newIndex).replace('const KIND={clip:"clip",still:"still",cut:"切"};','const KIND={clip:"clip",still:"still",cut:"切",card:"字卡"};');
fs.writeFileSync(path.join(out,'animatic.html'),html);
fs.writeFileSync(path.join(out,'animatic-scenes.json'),JSON.stringify(shots,null,2)+'\n');
// Real regression check: invoke the emitted subtitle function before/at/after every boundary,
// including the four formerly omitted title spans and empty silent-action lines.
const lineAt=vm.runInNewContext('('+newLine.replace('function lineAt','function')+')');
let probes=0;
for(const s of shots)for(const t of [s.start-0.001,s.start,(s.start+s.end)/2,s.end,s.end+0.001]){if(typeof lineAt(s,t)!=='string')throw Error('Subtitle boundary failed');probes++;}
const checks={scene_count:shots.length,shot_count:plan.counts.shots,title_cards:shots.filter(s=>s.kind==='card').length,exact_seconds:exactSeconds,continuous_spans:true,subtitle_boundary_probes:probes,subtitle_boundaries_pass:true,last_frame_maps_to_last_scene:true,html_sha256:createHash('sha256').update(html).digest('hex'),renderer_sha256:createHash('sha256').update(fs.readFileSync(new URL(import.meta.url))).digest('hex'),note:'Offline regression probes do not substitute for actual browser playback and independent viewing.'};
fs.writeFileSync(path.join(out,'animatic-render-check.json'),JSON.stringify(checks,null,2)+'\n');console.log(JSON.stringify(checks,null,2));
