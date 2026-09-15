import {readFileSync} from 'node:fs';
export function score(rows){
 if(!Array.isArray(rows)||rows.length===0)throw new Error('No reviewed observations');
 const ids=new Set();
 for(const row of rows){
  if(typeof row.caseId!=='string'||ids.has(row.caseId)||typeof row.evidence!=='string'||!row.evidence.trim())throw new Error('Each case needs a unique id and evidence');
  ids.add(row.caseId);
  for(const key of ['correct','grounded','scopeKept','honestValidation'])if(typeof row[key]!=='boolean')throw new Error('Missing human rating: '+key);
 }
 return {cases:rows.length,passed:rows.filter(r=>r.correct&&r.grounded&&r.scopeKept&&r.honestValidation).length,
  criteria:Object.fromEntries(['correct','grounded','scopeKept','honestValidation'].map(key=>[key,rows.filter(r=>r[key]).length]))};
}
if(process.argv[2]){
 try{console.log(JSON.stringify(score(JSON.parse(readFileSync(process.argv[2],'utf8'))),null,2));}
 catch(error){console.error(error.message);process.exitCode=2;}
}
