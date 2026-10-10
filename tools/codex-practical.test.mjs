// npm run test:tools discovers this bridge; standalone learner tests are also runnable directly.
import './codex-practical/labs.test.mjs';
import test from 'node:test';
import assert from 'node:assert/strict';
import { checkCurriculum } from './codex-practical/course.mjs';
import { mkdtempSync, readFileSync, writeFileSync, rmSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

test('Codex course supplies all independent lesson and surface specifications', () => {
  const result = checkCurriculum();
  assert.deepEqual(result.errors, []);
  assert.equal(result.lessons, 18);
  assert.equal(result.episodes, 36);
});

test('CLI recorder refuses partial pre-existing evidence before any provider invocation', () => {
  const output = mkdtempSync(path.join(tmpdir(),'codex-partial-evidence-'));
  assert.equal(path.dirname(path.resolve(output)),path.resolve(tmpdir()));
  try {
    writeFileSync(path.join(output,'invocation.json'),'KEEP-PARTIAL');
    const env = {...process.env}; delete env.NODE_TEST_CONTEXT;
    const result = spawnSync(process.execPath,[fileURLToPath(new URL('./codex-practical/record-cli.mjs',import.meta.url)),
      '--project',output,'--prompt',path.join(output,'nonexistent-prompt'), '--output',output,'--codex','never-invoke-provider'],
      {encoding:'utf8',env,windowsHide:true});
    assert.equal(result.status,1);
    assert.match(result.stderr,/Output already exists/);
    assert.equal(readFileSync(path.join(output,'invocation.json'),'utf8'),'KEEP-PARTIAL');
  } finally { rmSync(output,{recursive:true,force:true}); }
});

test('package builder rejects a misleading dot-dot directory inside the checkout before writing', () => {
  const repo = fileURLToPath(new URL('..',import.meta.url));
  const output = path.join(repo,'..lesson-build-guard');
  assert.equal(existsSync(output),false);
  const env = {...process.env}; delete env.NODE_TEST_CONTEXT;
  const result = spawnSync(process.execPath,[fileURLToPath(new URL('./codex-practical/course.mjs',import.meta.url)),
    'build','--output',output,'--python','never-invoke-python'],{encoding:'utf8',env,windowsHide:true});
  assert.equal(result.status,1);
  assert.match(result.stderr,/must be outside the Git checkout/);
  assert.equal(existsSync(output),false);
});
