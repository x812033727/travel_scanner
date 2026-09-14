import test from 'node:test';import assert from 'node:assert/strict';
import {mkdtempSync,rmSync,cpSync,readFileSync,writeFileSync,readdirSync,existsSync} from 'node:fs';
import {tmpdir} from 'node:os';import path from 'node:path';import {spawnSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
const source=fileURLToPath(new URL('../',import.meta.url));
function exercise(run){
 const root=mkdtempSync(path.join(tmpdir(),'mokaair-cli-state-'));
 try{
  for(const dir of ['automation','fixtures'])cpSync(path.join(source,dir),path.join(root,dir),{recursive:true,filter:p=>!p.split(path.sep).some(x=>['node_modules','run-data'].includes(x))});
  const command=(file,args=[],extra={})=>spawnSync(process.execPath,[file,...args],{cwd:root,encoding:'utf8',timeout:5000,windowsHide:true,env:{...process.env,NODE_TEST_CONTEXT:undefined,...extra}});
  return run(root,command);
 }finally{assert.ok(path.basename(root).startsWith('mokaair-cli-state-'));rmSync(root,{recursive:true});}
}
test('CLI persists separate failed, recovered and reused attempts',()=>exercise((root,run)=>{
 const state=()=>JSON.parse(readFileSync(path.join(root,'run-data/run-state.json'),'utf8'));
 assert.equal(run('automation/run-job.mjs',['recover','fail']).status,1);
 assert.equal(state().status,'failed');
 assert.equal(run('automation/run-job.mjs',['recover']).status,0);
 assert.equal(state().status,'completed');assert.equal(state().reused,false);
 assert.equal(run('automation/run-job.mjs',['recover']).status,0);assert.equal(state().reused,true);
 const attempts=readdirSync(path.join(root,'run-data/attempts')).filter(f=>f.endsWith('.json')).map(f=>JSON.parse(readFileSync(path.join(root,'run-data/attempts',f),'utf8')));
 assert.equal(new Set(attempts.map(x=>x.attemptId)).size,3);assert.equal(attempts.filter(x=>x.status==='failed').length,1);
 assert.equal(attempts.filter(x=>x.status==='completed').length,2);
}));
test('CSV export quotes data and review artifact drops unknown fields and rejects invalid output',()=>exercise((root,run)=>{
 writeFileSync(path.join(root,'fixtures/csv.json'),JSON.stringify([{method:'=1+1',case:'quote,"換行\n',seconds:1,attempts:1,passed:false}]));
 assert.equal(run('automation/export-evaluation.mjs',['fixtures/csv.json']).status,0);
 const csv=readFileSync(path.join(root,'run-data/evaluation.csv'),'utf8');
 assert.match(csv,/"'=1\+1"/);assert.ok(csv.includes('"quote,""換行\n"'));
 const valid=run('automation/ci/save-review.mjs',[],{REVIEW_JSON:JSON.stringify({summary:'待人工核對',findings:['固定案例'],privateToken:'discard'})});
 assert.equal(valid.status,0,valid.stderr);
 const artifact=path.join(root,'run-data/review.json');const before=readFileSync(artifact,'utf8');
 assert.deepEqual(JSON.parse(before),{summary:'待人工核對',findings:['固定案例']});
 assert.equal(run('automation/ci/save-review.mjs',[],{REVIEW_JSON:'{"summary":" ","findings":[]}'}).status,1);
 assert.equal(readFileSync(artifact,'utf8'),before);
 assert.equal(existsSync(path.join(root,'privateToken')),false);
}));
test('cancellation handler preserves attempt state without writing a completed job',()=>exercise((root,run)=>{
 const result=run('--input-type=module',['-e',"setTimeout(()=>process.emit('SIGINT'),250);process.argv=['node','run-job','cancel','pause'];await import('./automation/run-job.mjs');"]);
 assert.equal(result.status,130,result.stderr);
 const state=JSON.parse(readFileSync(path.join(root,'run-data/run-state.json'),'utf8'));
 assert.equal(state.status,'cancelled');assert.equal(existsSync(path.join(root,'run-data/cancel.json')),false);
}));
