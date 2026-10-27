import fs from 'node:fs';
import { isDeepStrictEqual as same } from 'node:util';
import { siteClient } from '/workspace/travel_scanner_pdf/tools/video/shorts/site.mjs';
const out='/workspace/work/ai-pdf-01/pt-native-state6-qualification-20261027T0327Z-projects-before-paid.json';
if(fs.existsSync(out))throw new Error('This exact pre-entry GET receipt already exists; never overwrite or repeat it');
const slugs=['ai-editable-explainer-animation','ai-pdf-quotes-to-comparison'],routes=[],seen=new Set();
const api=siteClient({attempts:1,fetch:async(url,options)=>{
 const u=new URL(url);
 if(options.method!=='GET'||u.origin!=='https://mokaair.com'||u.search||!slugs.some(s=>u.pathname==='/api/video/reviews/'+s)||seen.has(u.pathname))throw new Error('Only one exact normal GET per named project');
 seen.add(u.pathname);routes.push('GET '+u.pathname);
 return fetch(url,{...options,redirect:'error',signal:AbortSignal.timeout(20000)});
}});
const records=[];
for(const slug of slugs){
 const p=await api.project(slug),final=p?.reviews?.find(r=>r.gate==='final'&&(r.subject??null)===null);
 const wanted=Object.fromEntries(['en','ja','ko','es','pt','id','vi','th'].map(l=>[l,{metadata:true,captions:true,dub:true}]));
 const sha=slug==='ai-editable-explainer-animation'?'ead26bf5740e1a47499a7bf406c5820bd4b84fd31495d367c1dd83f551a5b521':'346a5bbd4b47884f301a9dfc9b67fe81e1a504232a0f4746e60ddead54d94e3f';
 if(p?.slug!==slug||p.dropped_at||final?.status!=='approved'||final.content_sha256!==sha||!same(p.dub_retries??{},{}))throw new Error('Actual project/final/retry guard changed: '+slug);
 if(p.retry_request_id&&p.retry_request_id!==p.retry_acknowledged_id)throw new Error('A true pending retry exists: '+slug);
 if(slug==='ai-editable-explainer-animation'&&p.worker_state!=='unavailable')throw new Error('Original actual worker state changed');
 if(slug==='ai-pdf-quotes-to-comparison'&&!((p.locales_decided_at==null&&Object.keys(p.locales??{}).length===0)||same(p.locales,wanted)))throw new Error('Actual PDF owner language choice changed');
 records.push({observed_at_utc:new Date().toISOString(),slug,stage:p.stage,worker_state:p.worker_state,ready_to_upload:p.ready_to_upload,youtube_video_id:p.youtube_video_id,dropped_at:p.dropped_at,locales_decided_at:p.locales_decided_at,locales:p.locales,dub_retries:p.dub_retries,retry_request_id:p.retry_request_id,retry_acknowledged_id:p.retry_acknowledged_id,dub_retry_blocked:p.dub_retry_blocked,final:{id:final.id,status:final.status,content_sha256:final.content_sha256}});
}
const result={recorded_at_utc:new Date().toISOString(),kind:'actual-exact-normal-both-project-GET-before-one-PT-unit',routes,records,no_owner_or_paid_or_project_mutation:true};
fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify(result,null,2));
