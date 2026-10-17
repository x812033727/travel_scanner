import {mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import {join,resolve,basename,relative,isAbsolute} from 'node:path';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {decodeTasks,weeklyReport} from './core.mjs';
import {verifyResult} from './verify-result.mjs';
const root=fileURLToPath(new URL('.',import.meta.url));
export const schema={type:'object',properties:{revision:{type:'string'},timezone:{type:'string'},weekStart:{type:'string'},weekEnd:{type:'string'},
  total:{type:'integer',minimum:0},completedInWeek:{type:'integer',minimum:0},pending:{type:'integer',minimum:0},unknownCompleted:{type:'integer',minimum:0}},
  required:['revision','timezone','weekStart','weekEnd','total','completedInWeek','pending','unknownCompleted'],additionalProperties:false};
export function execArguments(args) {
  const result={input:'fixtures/tasks.json',from:'2026-10-05',to:'2026-10-11',binary:process.env.CODEX_BINARY_PATH||'codex',dryRun:false};
  const seen=new Set();
  for(let i=0;i<args.length;i++){
    const flag=args[i];
    if(seen.has(flag))throw new Error('Duplicate option');seen.add(flag);
    if(flag==='--dry-run'){result.dryRun=true;continue;}
    const key={'--run':'run','--codex':'binary','--input':'input','--from':'from','--to':'to'}[flag];
    const value=args[++i];
    if(!key||!value||value.startsWith('--'))throw new Error('Usage: node exec-run.mjs (--dry-run OR --run NEWFOLDER) [--input FILE] [--from DATE --to DATE] [--codex NATIVE_BINARY]');
    result[key]=value;
  }
  if(result.dryRun===Boolean(result.run))throw new Error('Choose --dry-run or --run NEWFOLDER');
  if(result.run&&(basename(result.run)!==result.run||['.','..'].includes(result.run)))throw new Error('Use a new folder name, not a path');
  if(/\.(cmd|bat)$/i.test(result.binary))throw new Error('Pass a native codex executable with --codex; shell wrappers are not executed');
  return result;
}
function inputPath(projectRoot,input){
  const path=resolve(projectRoot,input),scope=relative(projectRoot,path);
  if(!scope||scope==='..'||scope.startsWith('..\\')||scope.startsWith('../')||isAbsolute(scope))throw new Error('Input must stay inside this practice project');
  return path;
}
function promptFor(options){return 'Read only '+options.input+'. Return the weekly report for inclusive Asia/Taipei dates '+options.from+' through '+options.to+'. UTC completion timestamps convert to +08:00 for calendar boundaries. Use revision weekly-report-v2, timezone Asia/Taipei, weekStart, weekEnd, total, completedInWeek, pending, unknownCompleted. Unknown completion dates stay unknown. Do not edit input or use external services.';}
function argv(directory,prompt,projectRoot){return ['exec','--sandbox','read-only','--skip-git-repo-check','--ephemeral','--json','--color','never','-C',projectRoot,'--output-schema',join(directory,'schema.json'),'-o',join(directory,'final.json'),prompt];}
export function runExec(args,projectRoot=root) {
  const options=execArguments(args),project=resolve(projectRoot),prompt=promptFor(options);
  if(options.dryRun){inputPath(project,options.input);weeklyReport([],options.from,options.to);
    return {modelInvoked:false,input:options.input,from:options.from,to:options.to,timezone:'Asia/Taipei',command:[options.binary,...argv('RUN',prompt,project)],schema};}
  const directory=resolve(project,options.run);mkdirSync(directory);
  const startedAt=new Date().toISOString();
  const metadata={input:options.input,inputPath:null,from:options.from,to:options.to,timezone:'Asia/Taipei',source:null,sourceSha256:null};
  const status={schemaVersion:1,state:'preflighting',modelInvoked:false,input:options.input,inputPath:null,from:options.from,to:options.to,
    timezone:'Asia/Taipei',sourceSha256:null,startedAt,nodeVersion:process.version};
  const write=(name,value)=>writeFileSync(join(directory,name),value,{flag:'wx'});
  const saveStatus=value=>writeFileSync(join(directory,'status.json'),JSON.stringify(value,null,2)+'\n');
  write('schema.json',JSON.stringify(schema,null,2)+'\n');write('prompt.txt',prompt+'\n');saveStatus(status);
  try {
    metadata.inputPath=inputPath(project,options.input);status.inputPath=metadata.inputPath;
    metadata.source=readFileSync(metadata.inputPath,'utf8');
    metadata.sourceSha256=createHash('sha256').update(metadata.source).digest('hex');status.sourceSha256=metadata.sourceSha256;
    weeklyReport(decodeTasks(metadata.source),options.from,options.to);
  }catch(error){
    write('input.json',JSON.stringify(metadata,null,2)+'\n');write('events.jsonl','');write('stderr.log',error.message+'\n');
    saveStatus({...status,state:'preflight_failed',finishedAt:new Date().toISOString(),exitCode:null,errorCode:error.code||null,error:error.message});
    throw new Error('Preflight failed; provider not called; see '+options.run+'/status.json');
  }
  write('input.json',JSON.stringify(metadata,null,2)+'\n');
  const command=argv(directory,prompt,project);saveStatus({...status,state:'running',modelInvoked:true,command});
  const result=spawnSync(options.binary,command,{cwd:project,encoding:'utf8',timeout:120000,maxBuffer:16*1024*1024,shell:false});
  write('events.jsonl',result.stdout||'');write('stderr.log',result.stderr||String(result.error||''));
  const state=result.error?(result.error.code==='ETIMEDOUT'?'timeout':'launch_failed'):'exited';
  saveStatus({...status,state,modelInvoked:true,command,finishedAt:new Date().toISOString(),exitCode:result.status,signal:result.signal||null,errorCode:result.error?.code||null});
  return verifyResult(directory);
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
  try{console.log(JSON.stringify(runExec(process.argv.slice(2)),null,2));}catch(error){console.error(error.message);process.exitCode=1;}
}
