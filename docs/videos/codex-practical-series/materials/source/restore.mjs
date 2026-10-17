import { readFileSync, writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { decodeTasks } from './core.mjs';
export function runRestore([input,output,...extra]) {
  if(!input || !output || extra.length) throw new Error('Usage: node restore.mjs BACKUP NEWFILE');
  const raw=readFileSync(input,'utf8'); const tasks=decodeTasks(raw);
  writeFileSync(output,raw,{flag:'wx'}); return {restored:tasks.length,output};
}
if(process.argv[1] && import.meta.url===pathToFileURL(process.argv[1]).href) {
  try { console.log(JSON.stringify(runRestore(process.argv.slice(2)))); }
  catch(error) { console.error(error.message); process.exitCode=1; }
}
