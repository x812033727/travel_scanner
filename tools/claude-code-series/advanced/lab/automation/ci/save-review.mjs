import {mkdirSync,writeFileSync} from 'node:fs';
const value=JSON.parse(process.env.REVIEW_JSON??'');
if(!value||typeof value.summary!=='string'||!value.summary.trim()||!Array.isArray(value.findings)||value.findings.some(x=>typeof x!=='string'))throw new Error('Invalid review output');
mkdirSync('run-data',{recursive:true});
writeFileSync('run-data/review.json',JSON.stringify({summary:value.summary,findings:value.findings},null,2)+'\n');
console.log('Saved validated review data. Human review is still required.');
