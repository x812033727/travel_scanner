import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { decodeTasks, encodeTasks, archiveTasks } from './core.mjs';
export function runArchive(args) {
  const input=args.shift(); let cutoff, out, apply=false;
  while(args.length) { const option=args.shift(); if(option==='--apply') { if(apply) throw new Error('duplicate-apply'); apply=true; }
    else if(option==='--cutoff' && cutoff===undefined) cutoff=args.shift();
    else if(option==='--out' && out===undefined) out=args.shift();
    else throw new Error('Unknown or duplicate archive option'); }
  if(!input || !cutoff || !out) throw new Error('Usage: node archive.mjs INPUT --cutoff UTC_ISO --out NEWFOLDER [--apply]');
  const backup=readFileSync(input,'utf8'); const tasks=decodeTasks(backup); const result=archiveTasks(tasks,cutoff);
  const summary={cutoff,archivedIds:result.archived.map(task=>task.id),retained:result.retained.length,
    unknownCompleted:result.retained.filter(task=>task.completed && task.completedAt===null).length,applied:apply};
  if(apply) {
    // A fresh output directory contains all outputs. The input is never overwritten.
    mkdirSync(out);
    writeFileSync(join(out,'backup.json'),backup,{flag:'wx'});
    writeFileSync(join(out,'archived.json'),encodeTasks(result.archived),{flag:'wx'});
    writeFileSync(join(out,'retained.json'),encodeTasks(result.retained),{flag:'wx'});
    writeFileSync(join(out,'receipt.json'),JSON.stringify(summary,null,2)+'\n',{flag:'wx'});
  }
  return summary;
}
if(process.argv[1] && import.meta.url===pathToFileURL(process.argv[1]).href) {
  try { console.log(JSON.stringify(runArchive(process.argv.slice(2)),null,2)); }
  catch(error) { console.error(error.message); process.exitCode=1; }
}
