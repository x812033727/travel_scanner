import {readFileSync} from 'node:fs';
import {join,dirname,resolve,relative,isAbsolute} from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {decodeTasks,weeklyReport} from './core.mjs';
export function verifyResult(directory) {
  const status=JSON.parse(readFileSync(join(directory,'status.json'),'utf8'));
  if(status.state!=='exited'||status.exitCode!==0||status.modelInvoked!==true)throw new Error('Process did not exit successfully');
  const metadata=JSON.parse(readFileSync(join(directory,'input.json'),'utf8'));
  const project=dirname(resolve(directory));
  if(typeof metadata.input!=='string')throw new Error('Input changed or unexpected scope');
  const path=resolve(project,metadata.input),scope=relative(project,path);
  if(!scope||scope==='..'||scope.startsWith('..\\')||scope.startsWith('../')||isAbsolute(scope)||metadata.inputPath!==path)throw new Error('Input changed or unexpected scope');
  for(const key of ['input','inputPath','from','to','timezone','sourceSha256'])if(status[key]!==metadata[key])throw new Error('Receipt parameters do not match input');
  if(metadata.timezone!=='Asia/Taipei')throw new Error('Unexpected report timezone');
  const raw=readFileSync(path,'utf8'),hash=createHash('sha256').update(raw).digest('hex');
  if(metadata.source!==raw||metadata.sourceSha256!==hash)throw new Error('Input changed or unexpected scope');
  const truth=weeklyReport(decodeTasks(raw),metadata.from,metadata.to);
  const events=readFileSync(join(directory,'events.jsonl'),'utf8').replace(/^\uFEFF/,'').split(/\r?\n/).filter(line=>line.trim()).map(JSON.parse);
  const types=events.map(event=>event.type);
  if(types.filter(type=>type==='turn.started').length!==1||types.filter(type=>type==='turn.completed').length!==1
      ||types.indexOf('turn.started')>types.indexOf('turn.completed')||types.includes('turn.failed')||types.includes('error'))throw new Error('Missing, failed or ambiguous turn');
  const result=JSON.parse(readFileSync(join(directory,'final.json'),'utf8').replace(/^\uFEFF/,''));
  if(!result||Array.isArray(result)||Object.keys(result).length!==Object.keys(truth).length
      ||Object.entries(truth).some(([key,value])=>result[key]!==value))throw new Error('Report does not match source truth');
  return result;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
  try{if(process.argv.length!==3)throw new Error('Usage: node verify-result.mjs RUNFOLDER');console.log(JSON.stringify(verifyResult(process.argv[2]),null,2));}
  catch(error){console.error(error.message);process.exitCode=1;}
}
