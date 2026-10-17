import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Read-only integrity and pure schema probes. No writer/checker/listener/media stage is invoked.
const dir = path.dirname(fileURLToPath(import.meta.url));
const ix = process.argv.indexOf('--root');
const root = ix >= 0 ? path.resolve(process.argv[ix + 1]) : path.resolve(dir,'../../../../..');
const read = p => fs.readFileSync(path.resolve(root,p));
const json = p => JSON.parse(read(p).toString('utf8'));
const sha = b => createHash('sha256').update(b).digest('hex');
const local = name => JSON.parse(fs.readFileSync(path.join(dir,name),'utf8'));
const pre = 'docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016';
const base = 'docs/videos/brand-stories-pilot-v2-20261015';
const pins = local('source-pins.json').files;
for(const [p,h] of Object.entries(pins)) assert.equal(sha(read(p)),h,`source drift ${p}`);
const plan=local('conversion-plan.json');
const checklist=local('claim-checklist.json');
const impact=local('shot-impact.json');
const ps=json(`${pre}/B18-10min-narration-candidate-v2/paragraphs.json`).paragraphs;
const old=json(`${pre}/B18-storyboard/original-paragraphs.json`);
const board=json(`${pre}/B18-storyboard/storyboard.json`);
const row=json(`${base}/episodes/B18.json`);
const units=s=>s.replace(/[\p{P}\p{S}\p{Z}\s]/gu,'').length;
const checks=[];
const check=(name,fn)=>{fn();checks.push({name,result:'verified'});};
check('all 24 paragraphs exact v2 text/order/chapter/CID',()=>{
 assert.equal(ps.length,24);
 assert.deepEqual(plan.paragraphs.map(p=>[p.id,p.chapter,p.text,p.source_cids]),ps.map(p=>[p.id,p.chapter,p.text,p.source_cids]));
 for(const p of plan.paragraphs)assert.equal(sha(p.text),p.text_sha256);
 // Restrict extraction to exactly six narration sections, not metrics/loops/change tables.
 const md=read(`${pre}/B18-10min-narration-candidate-v2/candidate.md`).toString('utf8');
 const sections=[...md.matchAll(/^## (hook|origin|idea|engine|turn|now)｜[^\r\n]+\r?\n([\s\S]*?)(?=^## |$(?![\s\S]))/gm)];
 assert.equal(sections.length,6);
 const extracted=sections.flatMap(s=>[...s[2].matchAll(/^### (\w+)\r?\n\s*\r?\n> ([^\r\n]+)/gm)].map(m=>({id:m[1],chapter:s[1],text:m[2]})));
 assert.deepEqual(extracted,ps.map(({id,chapter,text})=>({id,chapter,text})));
});
check('9 changed / 15 original-exact paragraphs, units 2294',()=>{
 assert.deepEqual(plan.paragraphs.filter(p=>!p.original_text_equal).map(p=>p.id),['O01','O02','O03','I04','E03','E05','T01','T01a','T03']);
 for(const p of plan.paragraphs){assert.equal(p.original_text_equal,p.text===old.find(o=>o.id===p.id).text);assert.equal(p.candidate_units,units(p.text));}
 assert.equal(ps.reduce((n,p)=>n+units(p.text),0),2294);
 assert.equal(plan.chapters.reduce((n,c)=>n+c.units,0),2294);
});
check('all 103 original shots and original paragraph reconstruction',()=>{
 assert.equal(impact.rows.length,103);
 assert.deepEqual(impact.rows.map(s=>s.id),board.shots.map(s=>s.id));
 for(const s of impact.rows){
  const original=board.shots.find(o=>o.id===s.id);assert.equal(s.original_shot_sha256,sha(JSON.stringify(original)));
  assert.equal(s.original_prompt,original.prompt??null);assert.equal(s.original_camera,original.camera??null);
  assert.deepEqual(s.original_card,original.card??null);assert.deepEqual(s.post_source_overlay,original.post_source_overlay??null);
  for(const r of s.refs){const p=ps.find(p=>p.id===r.paragraph_id);if(r.v2_candidate_start_utf16!==null)assert.equal(p.text.slice(r.v2_candidate_start_utf16,r.v2_candidate_start_utf16+r.text.length),r.text);}
 }
 for(const p of old){const refs=board.shots.flatMap(s=>s.narration_refs.filter(r=>r.paragraph_id===p.id));let end=0;
  for(const r of refs){assert.equal(r.start_utf16,end);end=r.end_utf16;}assert.equal(refs.map(r=>r.text).join(''),p.text);
 }
 for(const p of plan.paragraphs)assert.deepEqual(p.original_shot_ids,board.shots.filter(s=>s.narration_refs.some(r=>r.paragraph_id===p.id)).map(s=>s.id));
});
check('65 proposed claims remain UNCHECKED, source/fact scalar and exact text anchors',()=>{
 assert.equal(checklist.rows.length,65);assert.equal(new Set(checklist.rows.map(c=>c.planning_id)).size,65);
 for(const c of checklist.rows){
  const p=ps.find(p=>p.id===c.paragraph_id);assert.equal(p.text.slice(c.start_utf16,c.end_utf16),c.quote);
  assert.equal(c.verdict,'UNCHECKED');assert.equal(c.native_scene_id,null);
  assert(Number.isInteger(c.source_index_zero_based)&&row.sources[c.source_index_zero_based]);
  assert.equal(row.sources[c.source_index_zero_based].url,c.source_url);
  assert(c.fact_index_zero_based===null||(Number.isInteger(c.fact_index_zero_based)&&row.must_verify[c.fact_index_zero_based]));
  assert(plan.paragraphs.find(p=>p.id===c.paragraph_id).proposed_claim_checklist_ids.includes(c.planning_id));
 }
});
check('all 16 card triples / 9 overlays / 3 hook reuse pairs preserved',()=>{
 assert.equal(plan.card_adapter_plans.length,16);assert.equal(plan.post_source_overlay_plans.length,9);
 for(const c of plan.card_adapter_plans){assert.deepEqual(c.original_card,board.shots.find(s=>s.id===c.shot_id).card);assert.deepEqual(c.proposed_data,{title:c.original_card.text,subtitle:c.original_card.scope,tag:c.original_card.source});}
 assert.deepEqual(plan.hook_visual_reuse,board.hook_visual_reuse);assert.deepEqual(plan.end_visual_reuse,board.end_visual_reuse);
 for(const pair of plan.hook_visual_reuse){const a=board.shots.find(s=>s.id===pair.setup_shot),b=board.shots.find(s=>s.id===pair.recovery_shot);assert.equal(a.prompt,b.prompt);assert.equal(a.camera,b.camera);assert.equal(a.image_asset_key,b.image_asset_key);}
});
check('active row/compiled row unchanged; reviewed hook candidate distinct',()=>{
 const bundle=json(`${base}/stories.json`),hook=json(`${pre}/B18-worker-hook-candidate/B18.json`);
 assert.equal(bundle.stories.find(s=>s.id==='B18').chapters[0].point,row.chapters[0].point);
 assert.notEqual(hook.chapters[0].point,row.chapters[0].point);
});
const {readChapterAnswer,composeStory}=await import(pathToFileURL(path.join(root,'tools/video/automation/story.mjs')).href);
const {TEMPLATE_SPECS}=await import(pathToFileURL(path.join(root,'tools/video/templates/templates.mjs')).href);
const probe={title:'轉換資料型態探針',scenes:[{id:'hook-01',template:'title',data:plan.card_adapter_plans[0].proposed_data,lines:[{id:'abcd',text:'純記憶體探針。'}]}],claims:[]};
const rejection=readChapterAnswer(probe,{key:'hook',ids:['abcd'],sources:4,facts:10});
check('real writer reader rejects native title card',()=>assert.match(rejection.problem,/is a "title"/));
check('all 16 native title card data schemas accept all three fields',()=>{
 for(const c of plan.card_adapter_plans)assert.deepEqual(TEMPLATE_SPECS.title.check(c.proposed_data).filter(Boolean),[]);
});
const composed=composeStory({slug:row.slug,info:{title:row.title,slug:'probe-only',episode:2,target_minutes:10,look:{preset:'cute-mystery'},plan:row,characters:[]},chapters:{hook:{title:probe.title,scenes:probe.scenes,claims:[]}},voice:{},drama:{music_enabled:false},root});
check('real composer preserves native title card data in memory',()=>{
 assert.equal(composed.scenes[0].template,'title');assert.deepEqual(composed.scenes[0].data,probe.scenes[0].data);assert.equal(composed.subtitles.burn_in,false);assert.deepEqual(composed.look,{preset:'cute-mystery'});
});
const shotAnswer={title:'探針',scenes:[{id:'hook-01',template:'shot',data:{prompt:'A single generic person points at an unbranded plate.',camera:'pan right',visual:'still',image_asset_key:'test-key',post_source_overlay:{scope:'test',source:'test'}},lines:[{id:'abcd',text:'純記憶體探針。'}]}],claims:[]};
const parsed=readChapterAnswer(shotAnswer,{key:'hook',ids:['abcd'],sources:4,facts:10});
check('real writer reader drops unsupported asset key and post overlay fields',()=>{
 assert(!parsed.problem);assert(!('image_asset_key' in parsed.chapter.scenes[0].data));assert(!('post_source_overlay' in parsed.chapter.scenes[0].data));
});
check('no production verdict or formal file implied',()=>{
 assert.equal(plan.worker_pass,false);assert.equal(plan.facts_verified_by_this_plan,false);assert.equal(plan.formal_chapters_created,false);
 assert.equal(plan.timing.measured_tts_seconds,null);assert.equal(plan.timing.official_merged_lint_ran,false);
 assert(!fs.existsSync(path.join(dir,'auto.json')));assert(!fs.existsSync(path.join(dir,'chapters')));assert(!fs.existsSync(path.join(dir,'script-review.json')));
});
check('all 30 pinned inputs still byte-exact after checks',()=>{for(const [p,h] of Object.entries(pins))assert.equal(sha(read(p)),h,p);});
const outputs=['README.md','schema-and-adoption.md','conversion-plan.json','claim-checklist.json','shot-impact.json','paragraph-map.md','source-pins.json','verify.mjs'];
const refCounts=impact.rows.flatMap(s=>s.refs).reduce((a,r)=>(a[r.v2_status]=(a[r.v2_status]??0)+1,a),{});
console.log(JSON.stringify({schema_version:1,status:'VERIFIED_LOCAL_PLAN_INTEGRITY_ONLY',checked_at:new Date().toISOString(),node:process.version,
 checks,counts:plan.counts,ref_status_counts:refCounts,source_pins_verified:Object.keys(pins).length,
 changed_paragraph_original_shot_count:impact.rows.filter(s=>s.refs.some(r=>r.paragraph_changed)).length,
 writer_card_probe_problem:rejection.problem,official_full_draft_compose_or_lint:false,media_rendered:false,external_calls:0,model_calls:0,production_access:false,worker_pass:false,
 output_sha256:Object.fromEntries(outputs.map(p=>[p,sha(fs.readFileSync(path.join(dir,p)))]))},null,2));
