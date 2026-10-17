import test from 'node:test';import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,rmSync,readFileSync,existsSync} from 'node:fs';
import {tmpdir} from 'node:os';import {join} from 'node:path';import {createHash} from 'node:crypto';
import {verifyResult} from '../verify-result.mjs';import {runExec} from '../exec-run.mjs';
import {decodeTasks,weeklyReport} from '../core.mjs';
const source=readFileSync(new URL('../fixtures/tasks.json',import.meta.url),'utf8'),truth=JSON.parse(readFileSync(new URL('../fixtures/truth.json',import.meta.url),'utf8'));
test('dry run supports explicit input/Taipei dates without launching a model',()=>{
  const result=runExec(['--dry-run']);assert.equal(result.modelInvoked,false);assert.equal(result.command[1],'exec');assert.equal(result.schema.additionalProperties,false);
  const next=runExec(['--dry-run','--input','fixtures/tasks.json','--from','2026-10-12','--to','2026-10-18']);
  assert.equal(next.from,'2026-10-12');assert.equal(next.to,'2026-10-18');assert.match(next.command.at(-1),/2026-10-12 through 2026-10-18/);
  assert.throws(()=>runExec(['--dry-run','--from','2026-02-30']));
});
test('synthetic verifier fixtures compute actual receipt dates and reject false truth or changed source',()=>{
  // Explicitly synthetic test inputs; never model execution evidence.
  const project=mkdtempSync(join(tmpdir(),'codex-verify-')),dir=join(project,'run');mkdirSync(dir);
  const inputPath=join(project,'tasks.json'),sourceSha256=createHash('sha256').update(source).digest('hex');writeFileSync(inputPath,source);
  function receipt(from,to){const metadata={input:'tasks.json',inputPath,source,sourceSha256,from,to,timezone:'Asia/Taipei'};
    writeFileSync(join(dir,'input.json'),JSON.stringify(metadata));writeFileSync(join(dir,'status.json'),JSON.stringify({...metadata,state:'exited',exitCode:0,modelInvoked:true}));}
  try {
    receipt('2026-10-05','2026-10-11');writeFileSync(join(dir,'events.jsonl'),'{"type":"turn.started"}\n{"type":"turn.completed"}\n');
    writeFileSync(join(dir,'final.json'),JSON.stringify(truth));assert.deepEqual(verifyResult(dir),truth);
    writeFileSync(join(dir,'final.json'),JSON.stringify({...truth,completedInWeek:3}));assert.throws(()=>verifyResult(dir),/source truth/);
    receipt('2026-10-12','2026-10-18');const next=weeklyReport(decodeTasks(source),'2026-10-12','2026-10-18');assert.equal(next.completedInWeek,0);
    writeFileSync(join(dir,'final.json'),JSON.stringify(next));assert.deepEqual(verifyResult(dir),next);
    writeFileSync(inputPath,source+'\n');assert.throws(()=>verifyResult(dir),/Input changed/);writeFileSync(inputPath,source);
    writeFileSync(join(dir,'status.json'),JSON.stringify({state:'timeout',exitCode:null,modelInvoked:true}));assert.throws(()=>verifyResult(dir));
    receipt('2026-10-12','2026-10-18');writeFileSync(join(dir,'events.jsonl'),'{"type":"turn.started"}\n');assert.throws(()=>verifyResult(dir),/Missing/);
  }finally{rmSync(project,{recursive:true,force:true});}
});
test('missing input keeps a failed receipt, calls no provider and refuses an existing run ID',()=>{
  const project=mkdtempSync(join(tmpdir(),'codex-preflight-')),dir=join(project,'missing-run');
  try {
    assert.throws(()=>runExec(['--run','missing-run','--input','missing.json','--from','2026-10-12','--to','2026-10-18','--codex','unreachable-native-codex'],project),/provider not called/);
    const raw=readFileSync(join(dir,'status.json'),'utf8'),status=JSON.parse(raw);
    assert.equal(status.state,'preflight_failed');assert.equal(status.modelInvoked,false);assert.equal(status.errorCode,'ENOENT');
    assert.equal(status.from,'2026-10-12');assert.equal(status.to,'2026-10-18');assert.equal(status.sourceSha256,null);
    assert.equal(readFileSync(join(dir,'events.jsonl'),'utf8'),'');assert.equal(existsSync(join(dir,'final.json')),false);
    assert.ok(existsSync(join(dir,'input.json')));assert.ok(existsSync(join(dir,'prompt.txt')));
    assert.throws(()=>runExec(['--run','missing-run','--input','missing.json'],project));
    assert.equal(readFileSync(join(dir,'status.json'),'utf8'),raw);
  }finally{rmSync(project,{recursive:true,force:true});}
});
