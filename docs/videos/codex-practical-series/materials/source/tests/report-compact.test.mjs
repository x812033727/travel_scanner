import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
const root=fileURLToPath(new URL('..',import.meta.url));
const args=['report.mjs','fixtures/tasks.json','--from','2026-10-05','--to','2026-10-11'];
function run(extra=[]) {const env={...process.env};delete env.NODE_TEST_CONTEXT;return spawnSync(process.execPath,[...args,...extra],{cwd:root,env,encoding:'utf8'});}
test('compact CLI is exactly one JSON line with unchanged values and source',()=>{
  const source=readFileSync(join(root,'fixtures/tasks.json'));
  const pretty=run(),compact=run(['--compact']);
  assert.equal(pretty.status,0,pretty.stderr);assert.equal(compact.status,0,compact.stderr);
  assert.ok(pretty.stdout.trim().split('\n').length>1);
  assert.equal(compact.stdout.split('\n').length,2);assert.ok(compact.stdout.endsWith('\n'));
  const truth=JSON.parse(readFileSync(join(root,'fixtures/truth.json'),'utf8'));
  assert.deepEqual(JSON.parse(pretty.stdout),truth);assert.deepEqual(JSON.parse(compact.stdout),truth);
  assert.deepEqual(readFileSync(join(root,'fixtures/tasks.json')),source);
  assert.equal(run(['--compact','--compact']).status,1);
  assert.equal(run(['--compact','false']).status,1);
});
test('compact --out keeps one-line format and refuses existing output',()=>{
  const scratch=mkdtempSync(join(tmpdir(),'small-steps-compact-'));
  try {const output=join(scratch,'report.json');const first=run(['--compact','--out',output]);
    assert.equal(first.status,0,first.stderr);assert.equal(readFileSync(output,'utf8'),first.stdout);
    assert.equal(run(['--compact','--out',output]).status,1);
    assert.equal(readFileSync(output,'utf8'),first.stdout);
  }finally{rmSync(scratch,{recursive:true,force:true});}
});
