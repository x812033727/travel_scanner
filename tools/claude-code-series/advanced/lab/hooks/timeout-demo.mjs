import {spawnSync} from 'node:child_process';
const start=Date.now();
const result=spawnSync(process.execPath,['-e','setInterval(()=>{},1000)'],{encoding:'utf8',timeout:300,windowsHide:true});
const expected=result.error?.code==='ETIMEDOUT'&&result.status!==0;
console.log(JSON.stringify({expectedTimeout:expected,error:result.error?.code,status:result.status,signal:result.signal,elapsedMs:Date.now()-start}));
if(!expected)process.exitCode=1;
