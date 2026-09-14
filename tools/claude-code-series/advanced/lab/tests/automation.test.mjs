import test from 'node:test';import assert from 'node:assert/strict';
import {mkdtempSync,rmSync,readFileSync} from 'node:fs';import {tmpdir} from 'node:os';import path from 'node:path';
import {parseResult,lastResult} from '../automation/result.mjs';import {runJob} from '../automation/job.mjs';import {notify} from '../automation/notify.mjs';import {summarize} from '../automation/evaluate.mjs';
test('result parser distinguishes valid data from errors, incomplete streams and malformed output',()=>{
 const good=readFileSync(new URL('../fixtures/result-ok.json',import.meta.url),'utf8');
 assert.deepEqual(parseResult(good).taskIds,['a','b','c']);
 for(const name of ['result-error.json','result-bad-schema.json'])assert.throws(()=>parseResult(readFileSync(new URL('../fixtures/'+name,import.meta.url),'utf8')));
 assert.throws(()=>parseResult('not json'));
 assert.throws(()=>lastResult('{"type":"system"}\n'));
 assert.deepEqual(lastResult('{"type":"system"}\n'+JSON.stringify(JSON.parse(good))).taskIds,['a','b','c']);
 assert.throws(()=>parseResult(JSON.stringify({...JSON.parse(good),structured_output:{summary:'x',taskIds:['a','a']}})));
});
test('repeating a job reuses result, changed input fails and failed attempts can recover',()=>{
 const root=mkdtempSync(path.join(tmpdir(),'mokaair-jobs-'));const input=[{completed:false}];
 try{
  assert.throws(()=>runJob({id:'recover',input,root,failAt:'before-result'}));
  assert.equal(runJob({id:'recover',input,root}).reused,false);
  assert.equal(runJob({id:'recover',input,root}).reused,true);
  assert.throws(()=>runJob({id:'recover',input:[{completed:true}],root}));
  assert.throws(()=>runJob({id:'../bad',input,root}));
  assert.equal(notify({id:'one',status:'completed',secret:'do not log'},root).delivered,true);
  assert.equal(notify({id:'one',status:'completed'},root).duplicate,true);
  assert.doesNotMatch(readFileSync(path.join(root,'one.json'),'utf8'),/secret/);
 }finally{assert.ok(path.basename(root).startsWith('mokaair-jobs-'));rmSync(root,{recursive:true});}
});
test('evaluation includes failed cases, attempts and full time',()=>{
 const rows=JSON.parse(readFileSync(new URL('../fixtures/evaluation.json',import.meta.url),'utf8'));
 assert.deepEqual(summarize(rows)[0],{method:'A',samples:2,passed:1,totalSeconds:80,attempts:4});
});
