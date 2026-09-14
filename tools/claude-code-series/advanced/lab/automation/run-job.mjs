import {readFileSync,mkdirSync,writeFileSync,renameSync} from 'node:fs';import {randomUUID} from 'node:crypto';import {runJob} from './job.mjs';
const [id='daily-demo',mode]=process.argv.slice(2);
const attemptId=randomUUID();mkdirSync('run-data/attempts',{recursive:true});
const state={attemptId,jobId:id,pid:process.pid,startedAt:new Date().toISOString(),status:'running'};
const save=()=>{
 state.updatedAt=new Date().toISOString();
 for(const file of [`run-data/attempts/${attemptId}.json`,'run-data/run-state.json']){const temp=file+'.'+attemptId+'.tmp';writeFileSync(temp,JSON.stringify(state,null,2)+'\n');renameSync(temp,file);}
};
save();
process.once('SIGINT',()=>{state.status='cancelled';save();process.exit(130);});
try{
 if(mode==='pause')await new Promise(resolve=>setTimeout(resolve,10000));
 const input=JSON.parse(readFileSync('fixtures/tasks.json','utf8'));
 const result=runJob({id,input,failAt:mode==='fail'?'before-result':undefined});
 state.status='completed';state.reused=result.reused;save();console.log(JSON.stringify(result,null,2));
}catch(error){state.status='failed';state.error=error.message;save();console.error(error.message);process.exitCode=1;}
