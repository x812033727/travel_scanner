import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { COMMON, ROOT, SLUGS, compile, hash, loadSource } from './build.mjs';
import { documentProblem, retentionProblem, verdictPasses } from '../../../../tools/video/automation/series.mjs';

const text = v => typeof v === 'string' && v.trim().length > 0;
const cliffTypes = new Set(['danger','reveal','choice','reversal','emotion']);
const beatOrder = ['opening','first_half','midpoint','second_half','ending'];
const stateKeys = ['time','knowledge','character_state','evidence','carry_forward'];
export function validateSource(source, expectedSlug=source?.series?.slug) {
  const errors=[];
  const check=(ok,msg)=>{if(!ok) errors.push(msg);};
  try {
    const series={...source.series,...COMMON,chapters:4};
    check(series.slug===expectedSlug,'series slug does not match directory');
    check(/^[a-z0-9][a-z0-9-]{1,39}$/.test(series.slug),'invalid series slug');
    for(const k of ['title','premise','note']) check(text(series[k]),`missing series.${k}`);
    check(series.title.length<=200,'title exceeds 200 characters');
    check(series.premise.length<=4000,'premise exceeds API limit');
    check(series.note.length<=2000,'note exceeds API limit');
    check(series.genre!=='xianxia-bonds','all five plans must enable retention rules');
    check(series.tone===(series.lead==='dual-male'?'dual-male-leads-subtext':'no-romance'),'unexpected emotional tone');
    check(source.chapters.length===4,'expected four chapters');
    const episodes=source.chapters.flatMap(c=>c.episodes);
    check(episodes.length===40,'expected 40 episodes');
    check(episodes.every((e,i)=>e.number===i+1),'episodes must remain in order 1–40');
    const cast=new Set(source.setting.characters.map(c=>c.id));
    const locations=new Set(source.setting.locations.map(l=>l.id));
    const mysteries=new Map(source.setting.mysteries.map(m=>[m.id,m]));
    check(cast.size===source.setting.characters.length,'duplicate cast id');
    check(locations.size===source.setting.locations.length,'duplicate location id');
    check(mysteries.size===source.setting.mysteries.length,'duplicate mystery id');
    check(mysteries.size>=8 && mysteries.size<=12,'expected 8–12 mysteries');
    for(const c of source.setting.characters){
      for(const k of ['id','name','role','appearance','personality','want','fear','secret','speech']) check(text(c[k]),`cast ${c.id}: missing ${k}`);
      check(c.appearance.length<=800,`cast ${c.id}: appearance too long`);
      check(c.voice.provider==='gemini' && text(c.voice.name) && text(c.voice.style),`cast ${c.id}: voice proposal missing`);
      for(const r of c.relationships) check(cast.has(r.with) && text(r.kind),`cast ${c.id}: unknown relationship ${r.with}`);
    }
    const hooks=new Set();
    const titles=new Set();
    for(let i=0;i<episodes.length;i++){
      const e=episodes[i],prefix=`episode ${e.number}: `;
      for(const k of ['title','logline','hook','conflict','turn','theme']) check(text(e[k]),prefix+`missing ${k}`);
      check(!hooks.has(e.hook),prefix+'repeated hook'); hooks.add(e.hook);
      check(!titles.has(e.title),prefix+'repeated title'); titles.add(e.title);
      // At 250 characters/min this is an estimate, never a measured spoken duration.
      const spoken=[...e.hook.replace(/[\p{P}\p{Z}\s]/gu,'')].length;
      check(spoken/250*60<=8,prefix+'hook estimate exceeds 8 seconds');
      check(cliffTypes.has(e.cliffhanger?.type) && text(e.cliffhanger?.text),prefix+'invalid ending');
      if(i) check(e.cliffhanger.type!==episodes[i-1].cliffhanger.type,prefix+'same ending type as previous episode (including chapter boundary)');
      if(e.number%10===0) check(['reveal','reversal'].includes(e.cliffhanger.type),prefix+'chapter must close with reveal/reversal');
      check(new Set(e.tension).size>1,prefix+'flat tension');
      check(e.characters.length>=2 && e.characters.length<=4,prefix+'cast outside 2–4');
      check(e.locations.length>=1 && e.locations.length<=2,prefix+'locations outside 1–2');
      check(new Set(e.characters).size===e.characters.length,prefix+'duplicate character');
      for(const id of e.characters) check(cast.has(id),prefix+`unknown character ${id}`);
      for(const id of e.locations) check(locations.has(id),prefix+`unknown location ${id}`);
      for(const k of stateKeys) check(text(e.state?.[k]),prefix+`missing continuity ${k}`);
      check(e.closed_ending===(e.number===40),prefix+'closure must be reserved for finale');
      check(e.satisfaction.length>=2,prefix+'needs two payoffs');
      const first=e.satisfaction[0];
      check(Number.isFinite(first?.planned_seconds) && first.planned_seconds>=0 && first.planned_seconds<=30,prefix+'first reward must be planned within 30 seconds');
      let previousSeconds=-1,previousBeat=-1;
      for(const b of e.satisfaction){
        check(text(b.text) && b.text.length>=8,prefix+'reward needs a concrete action');
        check(Number.isFinite(b.planned_seconds) && b.planned_seconds>previousSeconds && b.planned_seconds<180,prefix+'reward timestamps unordered/outside episode');
        check(beatOrder.indexOf(b.beat)>=previousBeat,prefix+'reward beats unordered');
        previousSeconds=b.planned_seconds;previousBeat=beatOrder.indexOf(b.beat);
      }
      for(const id of e.setups){check(mysteries.has(id),prefix+`unknown setup ${id}`);if(mysteries.has(id)){const m=mysteries.get(id);check(m.planted===e.number||m.advanced.includes(e.number),prefix+`setup schedule differs for ${id}`);}}
      for(const id of e.payoffs){
        const m=mysteries.get(id); check(Boolean(m),prefix+`unknown payoff ${id}`);
        if(m){check(e.number>=m.planted,prefix+`payoff before planting ${id}`);check(e.number>=m.revealed||m.advanced.includes(e.number),prefix+`partial payoff not in advance schedule ${id}`);}
      }
    }
    for(const m of mysteries.values()){
      check(text(m.question)&&text(m.answer),`mystery ${m.id}: missing question/answer`);
      check(Number.isInteger(m.planted)&&Number.isInteger(m.revealed)&&m.planted>=1&&m.planted<m.revealed&&m.revealed<=40,`mystery ${m.id}: invalid chronology`);
      check(m.reserved===false,`mystery ${m.id}: cannot reserve for sequel`);
      check(new Set(m.advanced).size===m.advanced.length,`mystery ${m.id}: duplicate advances`);
      for(const n of m.advanced)check(Number.isInteger(n)&&n>=m.planted&&n<=40,`mystery ${m.id}: invalid advance`);
      check(episodes.find(e=>e.number===m.planted)?.setups.includes(m.id),`mystery ${m.id}: missing actual planting`);
      check(episodes.find(e=>e.number===m.revealed)?.payoffs.includes(m.id),`mystery ${m.id}: missing actual resolution`);
    }
    const files=compile(source);
    for(const kind of ['setting','outline']){const p=documentProblem(kind,JSON.parse(files[`${kind}.json`]),{series});if(p)errors.push(`production ${kind}: ${p}`);}
    for(let n=1;n<=4;n++){
      const c=source.chapters[n-1];
      check(c.number===n && c.episodes.length===10,`chapter ${n}: invalid range`);
      for(const k of ['title','theme','start_state','end_state','turn','stakes','question'])check(text(c[k]),`chapter ${n}: missing ${k}`);
      const p=documentProblem('chapter',JSON.parse(files[`chapter-0${n}.json`]),{series,chapter_number:n});if(p)errors.push(`production chapter ${n}: ${p}`);
    }
    const retention=retentionProblem(series,episodes);if(retention)errors.push(`cross-chapter retention: ${retention}`);
    const p=source.packaging;
    check(p.titles.length===3&&new Set(p.titles).size===3,'need three distinct title candidates');
    for(const title of p.titles)check(text(title)&&title.length<=100&&!/[<>]/.test(title),'invalid YouTube title');
    check(text(p.description)&&text(p.pinned_comment),'description/comment missing');
    check(p.tags.join(',').length<=500,'tags exceed 500 characters');
    for (const tag of ['漫劇','AI漫劇','一口氣看完']) check(p.tags.includes(tag),`missing required tag: ${tag}`);
    check(p.thumbnail_variants.length===3,'need three thumbnail compositions');
    for(const v of p.thumbnail_variants)check(text(v.headline)&&[...v.headline].length<=12&&v.episode>=1&&v.episode<=3&&text(v.scene)&&text(v.composition)&&text(v.promise),'invalid thumbnail or reference outside first three episodes');
    check(source.continuity_notes.length>=3,'cross-episode continuity guidance missing');
  }catch(error){errors.push(`invalid source shape: ${error.message}`);}
  return errors;
}

export async function validateFiles(slug,source) {
  const errors=[];
  for(const [name,expected] of Object.entries(compile(source))){
    try{const actual=await fs.readFile(path.join(ROOT,slug,name),'utf8');if(actual!==expected)errors.push(`${name}: missing/stale generated file`);}catch{errors.push(`${name}: cannot read`);}
  }
  return errors;
}

export function validateReview(review,source){
  const errors=[];
  if(!review || typeof review!=='object' || Array.isArray(review))return ['review: invalid receipt'];
  if(review.slug!==source.series.slug)errors.push('review: wrong series');
  if(review.source_sha256!==hash(source))errors.push('review: stale source hash');
  if(!text(review.reviewer)||!text(review.author)||review.reviewer===review.author)errors.push('review: independent reviewer required');
  if(review.evidence_type!=='independent-editorial-review')errors.push('review: wrong evidence type');
  if(!text(review.scope)||!text(review.limitations))errors.push('review: scope/limitations missing');
  if(!Array.isArray(review.open_findings)||review.open_findings.length)errors.push('review: unresolved findings');
  const names=['setting','outline','chapter-01','chapter-02','chapter-03','chapter-04'];
  if(Object.keys(review.documents??{}).sort().join('|')!==names.sort().join('|'))errors.push('review: expected six document verdicts');
  for(const name of names){
    const verdict=review.documents?.[name];
    if(!verdict || !Array.isArray(verdict.problems) || !Array.isArray(verdict.similar_works) || !text(verdict.notes) || !verdictPasses(verdict,name.startsWith('chapter')?'chapter':name))errors.push(`review: ${name} did not pass`);
  }
  return errors;
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const args=process.argv.slice(2),sourceOnly=args.includes('--source-only'),writeReport=args.includes('--write-report'),requireReviews=args.includes('--require-reviews');
  const selected=args.filter(a=>!a.startsWith('--'));
  const results=[];
  for(const slug of selected.length?selected:SLUGS){
    try{const source=await loadSource(slug);const errors=[...validateSource(source,slug),...(sourceOnly?[]:await validateFiles(slug,source))];if(requireReviews){try{const review=JSON.parse(await fs.readFile(path.join(ROOT,'reviews',`${slug}.json`),'utf8'));errors.push(...validateReview(review,source));}catch(e){errors.push(`review: ${e.message}`);}}results.push({slug,title:source.series.title,source_sha256:hash(source),episodes:source.chapters.flatMap(c=>c.episodes).length,documents:6,errors});}
    catch(e){results.push({slug,errors:[e.message]});}
  }
  const report={scope:'offline-production-plans',media_or_retention_measured:false,backend_created:false,source_only:sourceOnly,independent_review_required:requireReviews,ok:results.every(r=>r.errors.length===0),series:results};
  if(writeReport)await fs.writeFile(path.join(ROOT,'validation-report.json'),JSON.stringify(report,null,2)+'\n','utf8');
  console.log(JSON.stringify(report,null,2));
  if(!report.ok)process.exitCode=1;
}
