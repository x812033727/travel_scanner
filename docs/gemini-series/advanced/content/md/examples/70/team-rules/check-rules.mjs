import {readFileSync,existsSync} from 'node:fs';
import path from 'node:path';
const root=process.cwd(), main=readFileSync('GEMINI.md','utf8');
const references=[...main.matchAll(/^@(.+)$/gm)].map(m=>m[1]);
const errors=[];
for(const ref of references){
  const file=path.resolve(root,ref);
  if(!file.startsWith(root+path.sep)||!existsSync(file)){errors.push('Missing or outside import: '+ref);continue;}
  const text=readFileSync(file,'utf8');
  if(/npm test|pytest/.test(text))errors.push('Conflicting test command: '+ref);
}
if(references.length!==3)errors.push('Expected exactly three shared imports.');
console.log(JSON.stringify({imports:references,errors},null,2));
process.exitCode=errors.length?1:0;
