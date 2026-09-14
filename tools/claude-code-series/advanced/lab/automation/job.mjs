import {mkdirSync,existsSync,readFileSync,writeFileSync,renameSync,rmSync} from 'node:fs';
import path from 'node:path';import {createHash,randomUUID} from 'node:crypto';
export function runJob({id,input,root='run-data',failAt}) {
 if(!/^[a-z0-9][a-z0-9-]{0,63}$/.test(id))throw new Error('Invalid job id');
 const directory=path.resolve(root);mkdirSync(directory,{recursive:true});
 const resultFile=path.join(directory,id+'.json'),lock=path.join(directory,id+'.lock');
 const fingerprint=createHash('sha256').update(JSON.stringify(input)).digest('hex');
 if(existsSync(resultFile)) {
  const prior=JSON.parse(readFileSync(resultFile,'utf8'));
  if(prior.fingerprint!==fingerprint)throw new Error('Job id reused for different input');
  return {...prior,reused:true};
 }
 try{mkdirSync(lock);}catch(error){if(error.code==='EEXIST')throw new Error('Job already running; inspect owner before recovering');throw error;}
 const temp=path.join(directory,id+'.'+randomUUID()+'.tmp');
 try {
  writeFileSync(path.join(lock,'owner.json'),JSON.stringify({pid:process.pid,startedAt:new Date().toISOString()}));
  if(existsSync(resultFile)){
   const prior=JSON.parse(readFileSync(resultFile,'utf8'));
   if(prior.fingerprint!==fingerprint)throw new Error('Job id reused for different input');
   return {...prior,reused:true};
  }
  if(failAt==='before-result')throw new Error('Injected failure before result');
  if(!Array.isArray(input)||input.some(x=>!x||typeof x.completed!=='boolean'))throw new Error('Invalid task data');
  const result={id,fingerprint,status:'completed',total:input.length,completed:input.filter(x=>x.completed).length};
  writeFileSync(temp,JSON.stringify(result,null,2)+'\n');
  renameSync(temp,resultFile);
  return {...result,reused:false};
 } finally {
  if(existsSync(temp))rmSync(temp);
  rmSync(path.join(lock,'owner.json'),{force:true});
  rmSync(lock,{recursive:true});
 }
}
