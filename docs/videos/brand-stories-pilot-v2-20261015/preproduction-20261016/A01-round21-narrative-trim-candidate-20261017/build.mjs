import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath,pathToFileURL} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url)),base=path.resolve(here,'../A01-round20-i17-fact-index-candidate'),root=path.resolve(here,'../../../../..');
const keys=['hook','origin','idea','engine','turn','now'];const sha=b=>createHash('sha256').update(b).digest('hex');
const read=f=>fs.readFileSync(f),parse=f=>JSON.parse(read(f));const json=v=>Buffer.from(JSON.stringify(v,null,2)+'\n');
const manifestBytes=read(path.join(base,'manifest.json')),m=JSON.parse(manifestBytes);
assert.equal(sha(manifestBytes),'4d701779891e1076c3729788cc82165901d71140bfbd77c07fa9b1c060b32549');
const output=new Map(),chapters={};
for(const key of keys){const bytes=read(path.join(base,'candidate/chapters/'+key+'.json'));assert.equal(sha(bytes),m.candidate_chapter_sha256[key]);chapters[key]=JSON.parse(bytes);output.set('candidate/chapters/'+key+'.json',bytes);}
const line=chapters.engine.scenes.find(s=>s.id==='engine-r12-04').lines.find(l=>l.id==='r12e04');
const old=line.text;assert.equal(old,'在 Sadow 專利的示例裡，兩組輪子裝在箱蓋底，另兩組在箱身底；合起來，四組輪子都在箱底。');
const replacement='在 Sadow 專利的示例裡，兩組輪子裝在箱蓋底，另兩組在箱身底。';
let changed=0;function trim(value){if(Array.isArray(value))return value.map(trim);if(value && typeof value==='object')return Object.fromEntries(Object.entries(value).map(([k,v])=>[k,trim(v)]));if(value===old){changed++;return replacement;}return value;}
chapters.engine=trim(chapters.engine);output.set('candidate/chapters/engine.json',json(chapters.engine));
const seriesBytes=read(path.join(base,'candidate/series.json'));assert.equal(sha(seriesBytes),m.candidate_series_sha256);const series=JSON.parse(seriesBytes);output.set('candidate/series.json',seriesBytes);
const mapBytes=read(path.join(base,'source-map.json'));assert.equal(sha(mapBytes),m.source_map_sha256);const sourceMap=JSON.parse(mapBytes);const rows=sourceMap.lines.filter(r=>r.line_id==='r12e04');assert.equal(rows.length,1);assert.equal(rows[0].text,old);rows[0].text=replacement;output.set('source-map.json',json(sourceMap));
const [{composeStory,cuteStoryVisualProblems},{lintVideo}]=await Promise.all([import(pathToFileURL(path.join(root,'tools/video/automation/story.mjs'))),import(pathToFileURL(path.join(root,'tools/video/core/lint.mjs')))]);
const evidence=path.resolve(here,'../A01-round10-candidate/evidence');const archived=parse(path.join(evidence,'round9-composed-video.json'));
const make=chs=>composeStory({slug:m.slug,info:series,chapters:chs,voice:archived.voice,drama:{music_enabled:Boolean(archived.music)},root,videoId:archived.youtube.video_id??null});
const preview=make(chapters),baseChapters=Object.fromEntries(keys.map(k=>[k,parse(path.join(base,'candidate/chapters/'+k+'.json'))]));
const lines=v=>v.scenes.flatMap(s=>s.lines.map(l=>({scene_id:s.id,line_id:l.id,text:l.text})));const before=lines(make(baseChapters)),after=lines(preview);
assert.equal(sha(json(before)),m.narration_sha256);assert.equal(preview.scenes.length,79);assert.equal(after.length,108);
assert.deepEqual(before.filter(l=>l.line_id!=='r12e04'),after.filter(l=>l.line_id!=='r12e04'));assert.deepEqual(before.map(l=>[l.scene_id,l.line_id]),after.map(l=>[l.scene_id,l.line_id]));
const lint=lintVideo(preview,{lexicon:parse(path.join(evidence,'round9-lexicon.json')),brief:read(path.join(evidence,'round9-brief.md')).toString('utf8'),translations:{},others:[],series});const cute=cuteStoryVisualProblems(preview);assert.deepEqual(lint.errors,[]);assert.deepEqual(cute,[]);
const delta={base_manifest_sha256:sha(manifestBytes),chapter:'engine',scene_id:'engine-r12-04',line_id:'r12e04',old,text:replacement,reason:'remove repeated four-wheels-at-bottom clause; retain new wheel-group allocation detail',changed_spoken_lines:1,changed_source_rows:1,other_chapter_bytes_unchanged:true,host_or_paid_authorized:false};output.set('delta.json',json(delta));
const validation={status:'OFFLINE_MECHANICAL_ONLY_HOLD_FULL_REVIEW',scene_count:79,line_count:108,narration_sha256:sha(json(after)),lint_errors:lint.errors,lint_warning_count:lint.warnings.length,lint_warnings:lint.warnings,cute_errors:cute,independent_full_script_review:'NOT_RUN_FOR_ROUND21',genuine_narrative_panel:'NOT_RUN',script_review_receipt:'NOT_ISSUED',generated_images_or_audio:0};output.set('validation.json',json(validation));
const manifest={status:'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',slug:m.slug,base_round20_manifest_sha256:sha(manifestBytes),delta_sha256:sha(output.get('delta.json')),candidate_chapter_sha256:Object.fromEntries(keys.map(k=>[k,sha(output.get('candidate/chapters/'+k+'.json'))])),candidate_series_sha256:sha(seriesBytes),source_map_sha256:sha(output.get('source-map.json')),validation_sha256:sha(output.get('validation.json')),narration_sha256:validation.narration_sha256,changed_spoken_lines:1,changed_active_source_rows:1,active_source_rows:sourceMap.lines.length,inherited_round9_narrative_passed:false,authorizes_host_install_or_paid_media:false};output.set('manifest.json',json(manifest));
const action=process.argv[2];assert.ok(['--write','--check'].includes(action));for(const [name,bytes]of output){const file=path.join(here,name);if(action==='--write'){fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,bytes);}else assert.ok(read(file).equals(bytes),'stale '+name);}
console.log(JSON.stringify({action,manifest_sha256:sha(output.get('manifest.json')),narration_sha256:manifest.narration_sha256,scenes:79,lines:108,lint_errors:lint.errors.length,cute_errors:cute.length,status:'HOLD'}));
