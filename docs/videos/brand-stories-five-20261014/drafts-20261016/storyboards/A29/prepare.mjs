import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const repo=process.env.PREP_REPO_ROOT||process.cwd();
const sourceRelative='docs/videos/brand-stories-five-20261014/drafts-20261016/source-refresh-and-outline-A29.md';
const source=path.join(repo,sourceRelative);
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const raw=fs.readFileSync(source);assert.equal(hash(raw),'9d8d6ea834c526d3f6e5b452f01545a74c87873948c8392a1bc4bb8954056c11');
const full=raw.toString('utf8');
const spoken=full.split('## 二、六章完整旁白候選')[1].split('## 三、主張與原件索引')[0];
const units=s=>[...s.replace(/[\p{P}\p{S}\s]/gu,'')].length;
const chapters={H:'hook',O:'origin',I:'idea',E:'engine',T:'turn',N:'now'};
const paragraphs=[...spoken.matchAll(/^\| ((?:H|O|I|E|T|N)\d+[a-z]?) \| ([^|]+) \| ([^|]+) \|$/gm)].map(m=>({id:m[1],chapter:chapters[m[1][0]],text:m[2].trim(),claim_label:m[3].trim(),source_cids:[...m[3].matchAll(/C\d+[a-z]?/g)].map(x=>x[0]),units:units(m[2].trim())}));
assert.equal(paragraphs.length,65);assert.equal(new Set(paragraphs.map(p=>p.id)).size,65);assert.equal(paragraphs.reduce((sum,p)=>sum+p.units,0),2201);
const segmented=[];
for(const chapter of Object.values(chapters)){
 const ps=paragraphs.filter(p=>p.chapter===chapter),stream=ps.map(p=>p.text).join('');let offset=0;const ranges=ps.map(p=>{const r={...p,start:offset,end:offset+p.text.length};offset=r.end;return r;});
 const cuts=[0,...[...stream.matchAll(/[，。；：？！]/g)].map(m=>m.index+1)];if(cuts.at(-1)!==stream.length)cuts.push(stream.length);
 const ends=new Set(ranges.map(r=>r.end));const dp=new Array(cuts.length).fill(Infinity),prev=new Array(cuts.length).fill(-1);dp[0]=0;
 for(let j=1;j<cuts.length;j++){for(let i=0;i<j;i++){const n=units(stream.slice(cuts[i],cuts[j]));if(n<12||n>35)continue;const cross=ranges.filter(r=>r.start<cuts[j]&&r.end>cuts[i]).length-1;const cost=(n-26)**2/24+cross*2+(ends.has(cuts[j])?0:0.3);if(dp[i]+cost<dp[j]){dp[j]=dp[i]+cost;prev[j]=i;}}}
 assert.ok(Number.isFinite(dp.at(-1)),chapter);let j=cuts.length-1,parts=[];while(j>0){const i=prev[j];parts.unshift([cuts[i],cuts[j]]);j=i;}
 for(const [start,end]of parts){const refs=ranges.filter(r=>r.start<end&&r.end>start).map(r=>{const a=Math.max(start,r.start)-r.start,b=Math.min(end,r.end)-r.start;return{paragraph_id:r.id,start_utf16:a,end_utf16:b,text:r.text.slice(a,b),source_cids:r.source_cids};});const text=refs.map(r=>r.text).join('');segmented.push({id:'A29-S'+String(segmented.length+1).padStart(3,'0'),chapter,narration_refs:refs,text,units:units(text),estimated_spoken_seconds:{at_250_cpm:units(text)*60/250,at_230_cpm:units(text)*60/230},source_cids:[...new Set(refs.flatMap(r=>r.source_cids))]});}
}
assert.deepEqual(segmented.flatMap(s=>s.narration_refs).reduce((a,r)=>{a[r.paragraph_id]=(a[r.paragraph_id]??'')+r.text;return a;},{}),Object.fromEntries(paragraphs.map(p=>[p.id,p.text])));
const result={status:'EDITORIAL_STORYBOARD_PREPARATION_ONLY',source:{base:'repository_root',file:sourceRelative,sha256:hash(raw),section:'二、六章完整旁白候選 only; exclude claims, loops and notes'},paragraphs,shots:segmented};
fs.writeFileSync(path.join(dir,'narration-segments.json'),JSON.stringify(result,null,2)+'\n');
console.log(segmented.map(s=>`${s.id} ${s.chapter} [${s.narration_refs.map(r=>r.paragraph_id).join('+')}] ${s.units} ${s.text}`).join('\n'));
console.log(JSON.stringify({paragraphs:paragraphs.length,shots:segmented.length,units:segmented.reduce((n,s)=>n+s.units,0)}));
