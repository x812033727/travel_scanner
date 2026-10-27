import fs from 'node:fs';
import { siteClient } from '/workspace/travel_scanner_pdf/tools/video/shorts/site.mjs';
const slug='ai-pdf-quotes-to-comparison';
const out='/workspace/work/ai-pdf-01/pt-native-state6-qualification-20261027T0327Z-site-after-unit.json';
if(fs.existsSync(out))throw new Error('Actual post-unit read already saved; preserve it');
let calls=0;
const api=siteClient({attempts:1,fetch:async(url,options)=>{
 const u=new URL(url);
 if(options.method!=='GET'||u.origin!=='https://mokaair.com'||u.pathname!=='/api/video/reviews/'+slug||u.search||++calls!==1)throw new Error('One exact normal project GET only');
 return fetch(url,{...options,redirect:'error',signal:AbortSignal.timeout(20000)});
}});
const p=await api.project(slug);
if(p?.slug!==slug)throw new Error('Wrong actual project returned');
const result={observed_at_utc:new Date().toISOString(),kind:'actual-normal-project-GET-after-ended-ONE-native-PT-unit',routes:['GET /api/video/reviews/'+slug],slug:p.slug,stage:p.stage,worker_state:p.worker_state,pending:p.pending,checklist:p.checklist,ready_to_upload:p.ready_to_upload,youtube_video_id:p.youtube_video_id,dropped_at:p.dropped_at,retry_request_id:p.retry_request_id,retry_acknowledged_id:p.retry_acknowledged_id,dub_retries:p.dub_retries,dub_retry_blocked:p.dub_retry_blocked,locales_decided_at:p.locales_decided_at,locales:p.locales,reviews:(p.reviews??[]).filter(r=>['final','publish','languages'].includes(r.gate)).map(r=>({id:r.id,gate:r.gate,subject:r.subject??null,status:r.status,content_sha256:r.content_sha256})),no_owner_retry_or_other_mutation:true};
fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify(result,null,2));
