// Source-only projections using the official narrative functions. No review answer is created.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { STORY_VOICE_STYLE } from '../../../../tools/video/automation/register.mjs';
import { estimateTimeline, spokenUnits } from '../../../../tools/video/core/timeline.mjs';
import { panelPayload, panelRulesSha256 } from '../../../../tools/video/core/narrative.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
const read=name=>JSON.parse(fs.readFileSync(path.join(here,name),'utf8'));
const write=(name,value)=>fs.writeFileSync(path.join(here,name),JSON.stringify(value,null,2)+'\n');
const doc=read('video.json');
doc.voice.style=STORY_VOICE_STYLE;
write('video.json',doc);
const payload=panelPayload(doc,estimateTimeline(doc));
write('panel-payload.json',payload);
write('panel-contract.json',{panel_rules_sha256:panelRulesSha256(doc),payload_sha256:createHash('sha256').update(fs.readFileSync(path.join(here,'panel-payload.json'))).digest('hex'),estimated_timestamps_only:true,review_status:'NOT_SUBMITTED',author_wrote_no_answers:true});
const narr=read('narration-only.json');
const chapters=[];
for(const s of doc.scenes){if(s.chapter)chapters.push({name:s.chapter,scenes:0,lines:0,units:0,viewer:0,reaction:0});const c=chapters.at(-1);c.scenes++;for(const l of s.lines??[]){c.lines++;c.units+=spokenUnits(l.say??l.text);c.viewer+=(l.text.match(/你/g)??[]).length;c.reaction+=(l.text.match(/我/g)??[]).length;}}
const bodyScenes=doc.scenes.filter(s=>!['title','chapter','outro'].includes(s.template));
let run=0,maxRun=0;for(const s of bodyScenes){run=s.template==='shot'?0:run+1;maxRun=Math.max(maxRun,run);}
const notes=read('author-notes.json');
Object.assign(notes,{narration_characters_with_punctuation:narr.reduce((a,r)=>a+r.text.length,0),narration_han_characters:narr.reduce((a,r)=>a+(r.text.match(/[\u4e00-\u9fff]/g)??[]).length,0),spoken_units:narr.reduce((a,r)=>a+spokenUnits(r.text),0),opening_spoken_units:chapters[0].units,body_spoken_units:chapters.slice(1).reduce((a,c)=>a+c.units,0),estimate_narration_seconds_at_4_5:narr.reduce((a,r)=>a+spokenUnits(r.text),0)/4.5,scenes:doc.scenes.length,lines:narr.length,body_scenes:bodyScenes.length,body_shots:bodyScenes.filter(s=>s.template==='shot').length,body_cards:bodyScenes.filter(s=>s.template!=='shot').length,planned_body_image_ratio:bodyScenes.filter(s=>s.template==='shot').length/bodyScenes.length,max_consecutive_cards:maxRun,loops:doc.loops.length,chapter_counts:chapters,preserved_compatible_prompt_count:read('reuse-eligibility.json').filter(r=>r.prompt_verbatim).length});
write('author-notes.json',notes);
const files=['video.json','script.md','claims.md','claims.json','narration-only.json','panel-payload.json','series.json','brief.md','source-anchors.json','source-catalog.json','reuse-eligibility.json','build-candidate.py','build-panel.mjs','author-notes.json','source-snapshot-manifest.json'];
for (const name of [`author-delta-r${notes.author_revision}.json`,`lint-r${notes.author_revision}-author.json`]) if (fs.existsSync(path.join(here,name))) files.push(name);
const hashes=Object.fromEntries(files.map(name=>[name,createHash('sha256').update(fs.readFileSync(path.join(here,name))).digest('hex')]));
write('candidate-freeze.json',{schema_version:1,author_revision:notes.author_revision??1,slug:doc.slug,status:'FROZEN_AUTHOR_CANDIDATE_PENDING_INDEPENDENT_REVIEW',sha256:hashes,spoken_units:notes.spoken_units,body_spoken_units:notes.body_spoken_units,measured_audio_seconds:null,unknown_historical_claims_included:0,paid_calls:0,backend_writes:0,approvals_created:0});
console.log(JSON.stringify({sha256:hashes,spoken_units:notes.spoken_units,body_spoken_units:notes.body_spoken_units,chapters,scenes:notes.scenes,lines:notes.lines,ratio:notes.planned_body_image_ratio,loops:notes.loops},null,2));
