import {readFileSync} from 'node:fs';
export function summarize(rows) {
 if(!rows.length)throw new Error('No samples');
 const methods=[...new Set(rows.map(row=>row.method))];
 return methods.map(method=>{
 const group=rows.filter(row=>row.method===method);
 if(group.some(row=>!Number.isFinite(row.seconds)||row.seconds<0||!Number.isInteger(row.attempts)||row.attempts<1||typeof row.passed!=='boolean'))throw new Error('Invalid observation');
 return {method,samples:group.length,passed:group.filter(row=>row.passed).length,totalSeconds:group.reduce((s,r)=>s+r.seconds,0),attempts:group.reduce((s,r)=>s+r.attempts,0)};
 });
}
if(process.argv[2])console.log(JSON.stringify(summarize(JSON.parse(readFileSync(process.argv[2],'utf8'))),null,2));
