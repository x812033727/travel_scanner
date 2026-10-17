import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const at=process.argv.indexOf('--repo'),repo=at>=0?path.resolve(process.argv[at+1]):path.resolve(dir,'../../../../..');
const sha=b=>createHash('sha256').update(b).digest('hex');
const fh=f=>sha(fs.readFileSync(f));
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const local=p=>read(path.join(dir,p));
let externalCalls=0;globalThis.fetch=()=>{externalCalls++;throw new Error('No network in offline verification');};
const checks=[],check=(name,fn)=>{fn();checks.push({name,result:'verified'});};
const pins=local('input-pins.json');
check('43 input files and exact lexicon fixture',()=>{
 assert.equal(Object.keys(pins.files).length,43);for(const [p,h]of Object.entries(pins.files))assert.equal(fh(path.join(repo,p)),h,p);
 assert.equal(fh(path.join(dir,pins.lexicon.file)),pins.lexicon.sha256);
});
const initial=local('output-pins.json');
check('all initial generated files match their frozen output hashes',()=>{for(const [p,h]of Object.entries(initial.files))assert.equal(fh(path.join(dir,p)),h,p);});
const m=local('mapping.json'),e=local('compose-lint-evidence.json'),keys=['hook','origin','idea','engine','turn','now'];
const chapters=Object.fromEntries(keys.map(k=>[k,local(`chapters/${k}.json`)]));
const original=read(path.join(repo,'docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-10min-narration-candidate-v2/paragraphs.json')).paragraphs;
const flattened=keys.flatMap(k=>chapters[k].scenes.flatMap(s=>s.lines.map(l=>({scene:s.id,...l}))));
check('24 paragraphs and 99 native lines reconstruct exactly in order',()=>{
 assert.deepEqual(m.paragraphs,original);assert.equal(flattened.length,99);
 assert.deepEqual(flattened.map(l=>[l.id,l.scene,l.text]),m.lines.map(l=>[l.line_id,l.scene_id,l.text]));
 assert.equal(flattened.map(l=>l.text).join(''),original.map(p=>p.text).join(''));
 for(const p of original){const rows=m.lines.filter(l=>l.paragraph_id===p.id);let offset=0;for(const l of rows){assert.equal(l.start_utf16,offset);assert.equal(p.text.slice(l.start_utf16,l.end_utf16),l.text);offset=l.end_utf16;}assert.equal(offset,p.text.length);}
 assert.equal(new Set(flattened.map(l=>l.id)).size,99);
});
check('all 65 claims UNCHECKED with single-scene verbatim scope and scalar source/fact',()=>{
 const claims=keys.flatMap(k=>chapters[k].claims);assert.equal(claims.length,65);assert.equal(m.claims.length,65);
 for(const c of m.claims){const n=claims.find(x=>x.id===c.claim_id);assert.deepEqual(n,c.native);assert.equal(n.verdict,'UNCHECKED');assert.equal(c.all_scene_ids.length,1);assert.equal(c.all_scene_ids[0],n.scene);
  const scene=keys.flatMap(k=>chapters[k].scenes).find(s=>s.id===n.scene);assert(scene.lines.map(l=>l.text).join('').includes(n.claim));
  assert(Number.isInteger(n.source)&&n.source>=0&&n.source<=2);assert(n.fact===null||Number.isInteger(n.fact));
 }
 assert.deepEqual(m.claims.filter(c=>c.fact_boundary_adjustment).map(c=>c.claim_id),['i2','i8']);
 assert(m.claims.filter(c=>c.fact_boundary_adjustment).every(c=>c.native.fact===null));
});
const docroot=path.join(dir,'synthetic/docroot'),slug='story-conveyor-belt-sushi-v2';
const mod=p=>import(pathToFileURL(path.join(repo,p)).href);
const {composeStory,cuteStoryVisualProblems}=await mod('tools/video/automation/story.mjs');
const {loadProject,lintProject}=await mod('tools/video/core/state.mjs');
const {screenplay}=await mod('tools/video/core/screenplay.mjs');
const {estimateTimeline}=await mod('tools/video/core/timeline.mjs');
const {TEMPLATE_SPECS,slideHtml,visibleText}=await mod('tools/video/templates/templates.mjs');
const project=loadProject({slug,root:docroot}),doc=project.doc;
const lint=lintProject(project),cute=cuteStoryVisualProblems(doc);
check('official compose equals canonical video and script; CC off burn-in',()=>{
 const merged=composeStory({slug,info:local('series.json'),chapters,voice:doc.voice,drama:{music_enabled:false},root:docroot});assert.deepEqual(merged,doc);
 assert.equal(fs.readFileSync(path.join(docroot,'docs/videos',slug,'script.md'),'utf8'),screenplay(doc));assert.equal(doc.subtitles.burn_in,false);assert.deepEqual(doc.look,{preset:'cute-mystery'});
});
check('official lint/cute 0 errors; preserve exact recorded warnings and estimate',()=>{
 assert.deepEqual(lint,e.lint);assert.deepEqual(lint.errors,[]);assert.deepEqual(cute,[]);assert.equal(estimateTimeline(doc).total_frames/30,e.estimated_body_seconds);
});
check('96 actual scenes: 77 illustrations, 19 cards; physical ratio and card runs',()=>{
 assert.equal(doc.scenes.length,96);assert.equal(doc.scenes.filter(s=>s.template==='shot').length,77);assert.equal(doc.scenes.filter(s=>s.template==='title').length,19);
 let max=0,run=0;for(const s of doc.scenes){run=s.template==='shot'?0:run+1;max=Math.max(max,run);if(s.template==='shot')assert(!('image_asset_key'in s.data)&&!('post_source_overlay'in s.data)&&!('source'in s.data));}
 assert.equal(max,2);assert(77/96>=0.7);
});
check('all 16 original cards plus nine overlay scopes are really present in native HTML',()=>{
 assert.equal(m.cards.filter(c=>c.original_card).length,16);assert.equal(m.source_overlays.length,9);
 const texts=new Map();for(const c of m.cards){assert.deepEqual(TEMPLATE_SPECS.title.check(c.data).filter(Boolean),[]);const txt=visibleText(slideHtml({id:c.scene_id,template:'title',data:c.data,lines:[]},{first:true,reveal:0,previousReveal:0}));texts.set(c.scene_id,txt);
  for(const value of Object.values(c.data))assert(value.split('\n').every(part=>txt.includes(part)));if(c.original_card){assert(txt.includes(c.original_card.text));assert(txt.includes(c.original_card.scope));}
 }
 for(const o of m.source_overlays)assert(texts.get(o.native_card_scene_id).includes(o.original_overlay.scope));
});
check('11 complete line loops and three unchanged hook/payoff image requests',()=>{
 const order=new Map(flattened.map((l,i)=>[l.id,i]));assert.equal(doc.loops.length,11);assert.equal(new Set(doc.loops.map(l=>l.setup)).size,11);
 for(const l of doc.loops)assert(order.has(l.setup)&&order.has(l.payoff)&&order.get(l.setup)<order.get(l.payoff));
 for(const p of m.image_reuse){const a=doc.scenes.find(s=>s.id===p.setup_scene_id),b=doc.scenes.find(s=>s.id===p.payoff_scene_id);assert.equal(a.data.prompt,b.data.prompt);assert.equal(a.data.camera,b.data.camera);}
});
check('all runtime plan facts/sources/metadata remain exact compiled references',()=>{
 const info=local('series.json'),row=local('worker-row-reference.json');
 assert.deepEqual(info.plan,Object.fromEntries(Object.entries(row).filter(([k])=>!['number','title','logline','slug'].includes(k))));
 const bundle=read(path.join(repo,'docs/videos/brand-stories-pilot-v2-20261015/stories.json'));assert.deepEqual(row,bundle.stories.find(s=>s.id==='B18'));
});
check('no worker approval, paid files, or external calls',()=>{
 const work=path.join(dir,'synthetic/work',slug),docs=path.join(docroot,'docs/videos',slug);
 for(const p of ['auto.json','approvals.json','review/narrative.json','story/reviews/script-review.json','audio','final.mp4','keyframes'])assert(!fs.existsSync(path.join(work,p)));
 assert(!fs.existsSync(path.join(docs,'verify-1.md')));assert.equal(externalCalls,0);assert.equal(e.worker_pass,false);
});
check('all original pinned sources remain unchanged after official checks',()=>{for(const [p,h]of Object.entries(pins.files))assert.equal(fh(path.join(repo,p)),h,p);});
console.log(JSON.stringify({schema_version:1,status:'VERIFIED_OFFLINE_CANDIDATE_STRUCTURE_ONLY',checks,paragraphs:24,lines:99,scenes:96,claims_unchecked:65,lint_errors:lint.errors,cute_errors:cute,warnings:lint.warnings.length,estimated_body_seconds:e.estimated_body_seconds,measured_body_seconds:null,source_files_unchanged:43,external_calls:externalCalls,worker_pass:false,
 chapter_sha256:Object.fromEntries(keys.map(k=>[k,fh(path.join(dir,'chapters',`${k}.json`))])),mapping_sha256:fh(path.join(dir,'mapping.json')),compose_evidence_sha256:fh(path.join(dir,'compose-lint-evidence.json'))},null,2));
