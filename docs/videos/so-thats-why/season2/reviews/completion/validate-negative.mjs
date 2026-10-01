import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import cp from 'node:child_process';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
// Mutations run in an isolated temporary copy, never in the checkout.
const out=path.dirname(fileURLToPath(import.meta.url));
const repo=path.resolve(out,'../../../../../..');
const fixture=fs.mkdtempSync(path.join(os.tmpdir(),'sothatswhy-completion-negative-'));
const reportPath=process.argv.find(a=>a.startsWith('--report='))?.slice(9);
const base=path.join(fixture,'docs/videos/so-thats-why/season2');
for(const rel of ['docs/videos/so-thats-why','docs/videos/story-plans/brand-stories-100','docs/videos/ai-term-context-window','docs/videos/ai-term-token','docs/ai-video-season-01'])fs.cpSync(path.join(repo,rel),path.join(fixture,rel),{recursive:true});
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
let backups;
const abs=p=>path.resolve(base,p);
const edit=(p,fn)=>{const a=abs(p);if(!backups.has(a))backups.set(a,fs.readFileSync(a));fs.writeFileSync(a,fn(fs.readFileSync(a,'utf8')));};
const jedit=(p,fn)=>edit(p,t=>{const d=JSON.parse(t);fn(d);return JSON.stringify(d,null,2)+'\n';});
const rebind=id=>{const p=id+'.md',r='reviews/completion/'+id+'.json';const old=JSON.parse(fs.readFileSync(abs(r))).package_sha256,newHash=sha(fs.readFileSync(abs(p)));
edit('reviews/completion/'+id+'.md',t=>t.replace(new RegExp(old,'gi'),newHash));
jedit(r,d=>{d.package_sha256=newHash;d.report_sha256=sha(fs.readFileSync(abs(d.report)));});};
const run=batch=>cp.spawnSync(process.execPath,[path.join(base,'validate.mjs'),'--batch='+batch],{encoding:'utf8'});
const cases=[
 ['package-drift',()=>edit('T27.md',t=>t+'\nChanged package.\n'),'stale review'],
 ['report-drift',()=>edit('reviews/completion/T27.md',t=>t+'\nChanged report.\n'),'stale review'],
 ['bundle-drift',()=>jedit('completion-packaging.json',d=>d.episodes[0].target_seconds=999),'bundle differs'],
 ['original-inventory-drift',()=>jedit('../season2-topics.json',d=>d.episodes[0].title+='改'),'original topic inventory changed'],
 ['original-row-title-drift',()=>jedit('dispositions.json',d=>d.episodes[0].original_title+='改'),'original title, check and verdict'],
 ['unresolved-disposition',()=>jedit('dispositions.json',d=>d.episodes[0].status='pending'),'unresolved disposition'],
 ['self-review',()=>jedit('reviews/completion/T27.json',d=>d.reviewer_agent=d.author_agent),'independent text review'],
 ['fabricated-rejected-package',()=>jedit('dispositions.json',d=>d.episodes.find(r=>r.id==='B30').package='B30.md'),'fabricated production package'],
 ['unknown-duplicate-record',()=>jedit('dispositions.json',d=>d.episodes.find(r=>r.id==='B30').duplicate_of[0].record_id='ZZ99'),'duplicate record ID not found'],
 ['duplicate-source-hash-drift',()=>jedit('dispositions.json',d=>d.episodes.find(r=>r.id==='B30').duplicate_of[0].source_sha256='0'.repeat(64)),'duplicate source changed'],
 ['preserved-artifact-drift',()=>edit('B26.md',t=>t+'\nChanged preserved package.\n'),'preservation: changed B26.md'],
 ['missing-plain-science-prompt',()=>{edit('S50.md',t=>{let removed=false;return t.split('\n').map(line=>{if(!removed&&line.startsWith('| P1／')){const cells=line.split('|');cells[cells.length-2]=' ';removed=true;return cells.join('|');}return line;}).join('\n');});rebind('S50');},'six chapter, ten Short and two thumbnail prompts required'],
 ['wrong-prompt-group-with-total-18',()=>{edit('S50.md',t=>{const line=t.split('\n').find(l=>l.startsWith('| P1／'));return t.replace(line+'\n','').replace('### Short 1','### Short 1\n\n'+line);});rebind('S50');},'six chapter, ten Short and two thumbnail prompts required'],
 ['crlf-new-package',()=>{edit('T27.md',t=>t.replaceAll('\n','\r\n'));rebind('T27');},'LF text with a single final newline required'],
 ['consecutive-ending-punctuation',()=>{edit('T27.md',t=>{let i=0;return t.replace(/```text\r?\n([\s\S]*?)\r?\n```/g,(m)=>i++===2?'```text\n'+('甲'.repeat(39)+'！？').repeat(5)+'\n```':m);});rebind('T27');},'sentence exceeds 40 characters'],
 ['metadata-title-limit',()=>{edit('T27.md',t=>t.replace(/```json\r?\n([\s\S]*?)\r?\n```/,(_m,j)=>{const d=JSON.parse(j);d.localizations.en.title='X'.repeat(101);return '```json\n'+JSON.stringify(d,null,2)+'\n```';}));rebind('T27');},'title length must be 1..100'],
 ['wrong-totals',()=>jedit('dispositions.json',d=>d.totals.adopted=100),'totals differ'],
 ['duplicate-proposed-order',()=>jedit('dispositions.json',d=>d.proposed_order[1].id=d.proposed_order[0].id),'proposed order must contain'],
 ['unsupported-publication-claim',()=>jedit('dispositions.json',d=>d.published=true),'must remain unaccepted'],
 ['selection-drift',()=>edit('reviews/completion/travel-selection.md',t=>t+'\nChanged selection.\n'),'disposition report must bind current selection'],
 ['missing-pillar-review',()=>jedit('dispositions.json',d=>d.pillar_reviews.pop()),'four pillar reviews required'],
 ['unknown-batch',()=>{},'unknown batch']
];
const baseline=run('completion');if(baseline.status!==0)throw Error('Fixture baseline failed: '+baseline.stdout+baseline.stderr);
const results=[];
for(const[name,mutate,expected]of cases){backups=new Map();try{mutate();const r=run(name==='unknown-batch'?'made-up':'completion'),output=r.stdout+r.stderr;const pass=r.status!==0&&output.includes(expected);results.push({name,pass,exit_code:r.status,expected});if(!pass)throw Error(name+' unexpectedly passed or failed for a different reason: '+output);}finally{for(const[a,b]of backups)fs.writeFileSync(a,b);}}
const final=run('completion');if(final.status!==0)throw Error('Fixture restoration failed');
const report={checked_on:'2026-10-01',scope:'TEXT_ONLY',fixture,baseline_pass:true,restored_baseline_pass:true,negative_cases:results};
if(reportPath)fs.writeFileSync(path.resolve(reportPath),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({baseline:'PASS',negative_cases:results.length,rejected:results.filter(r=>r.pass).length,restored_baseline:'PASS'}));
