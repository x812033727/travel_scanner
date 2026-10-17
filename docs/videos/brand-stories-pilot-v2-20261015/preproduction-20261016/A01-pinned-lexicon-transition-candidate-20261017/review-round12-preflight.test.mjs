// Runs the actual driver --preflight branch against a private fixture. A mocked
// lease acquisition mutates LEASE, making a misplaced call observable.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath,pathToFileURL} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const repo=path.resolve(here,'../../../../..');
const snapshot=process.env.A01_SNAPSHOT104_ROOT;
if(!snapshot)throw Error('Set A01_SNAPSHOT104_ROOT to the verified snapshot-104 root');
const slug='story-rolling-suitcase-v2';
const source104='e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7';

test('--preflight never creates or renames the canonical A01 LEASE',()=>{
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'a01-preflight-lease-'));
 try{
  const root=path.join(temp,'runtime'),workBase=path.join(temp,'work'),workdir=path.join(workBase,slug);
  const candidate=path.join(temp,'candidate'),payload=path.join(temp,'payload'),childTemp=path.join(temp,'tmp');
  for(const dir of [root,workdir,candidate,payload,childTemp,path.join(workdir,'story/chapters'),path.join(workdir,'run-receipts')])fs.mkdirSync(dir,{recursive:true});
  fs.copyFileSync(path.join(snapshot,slug,'auto.json'),path.join(workdir,'auto.json'));
  fs.copyFileSync(path.join(snapshot,slug,'story/chapters/turn.json'),path.join(workdir,'story/chapters/turn.json'));
  fs.writeFileSync(path.join(workdir,'STOP'),'A01 STOP retained\n');
  const lease=path.join(workdir,'LEASE'),old=Buffer.from('dead holder is evidence, not a file to rename\n');
  fs.writeFileSync(lease,old);
  fs.writeFileSync(path.join(candidate,'required-runtime.json'),'{}\n');
  fs.writeFileSync(path.join(payload,'revision-review.json'),'{}\n');
  fs.writeFileSync(path.join(payload,'revision-owner-record.json'),'{}\n');
  const mock=`import fs from 'node:fs';import path from 'node:path';
export const readStoryLexicon=()=>{throw Error('NO_SOURCE_READ_EXPECTED')};
export const atomicWrite=()=>{throw Error('NO_WRITE_EXPECTED')};
export class Automation{constructor(){throw Error('NO_AUTOMATION_EXPECTED')}}
export const RUN_PENDING='video_ai_run_pending';
export const automationClient=()=>{throw Error('NO_CLIENT_EXPECTED')};
export const advanceStory=()=>{throw Error('NO_MODEL_EXPECTED')};
export function acquireProjectLease(workdir){fs.renameSync(path.join(workdir,'LEASE'),path.join(workdir,'LEASE.dead.json'));fs.writeFileSync(path.join(workdir,'LEASE'),'bad new holder');throw Error('LEASE_ACQUIRED_IN_PREFLIGHT')}
export function captureAdoptionSources({output}){if(!fs.statSync(output).isDirectory())throw Error('BAD_TEMP_CAPTURE')}
export const inspectReviewProgress=()=>({links:104,source_sha256:'${source104}',round12_events:[]});
export const checkRound12Manual=()=>{throw Error('NO_MANUAL_EVENT_EXPECTED')};
`;
  fs.writeFileSync(path.join(candidate,'preflight-mocks.mjs'),mock);
  let driver=fs.readFileSync(path.join(here,'review-round12-104.mjs'),'utf8');
  const imports=[
   "'/opt/mokaair/tools/video/core/story-lexicon.mjs'",
   "'/opt/mokaair/tools/video/core/paths.mjs'",
   "'/opt/mokaair/tools/video/automation/flow.mjs'",
   "'/opt/mokaair/tools/video/automation/client.mjs'",
   "'/opt/mokaair/tools/video/automation/story.mjs'",
   "'/opt/mokaair/tools/video/core/project-lease.mjs'",
   "'./adopt-pinned.mjs'",
   "'./inspect-review-progress.mjs'",
  ];
  for(const target of imports){assert.ok(driver.includes(target),`import ${target}`);driver=driver.replace(target,"'./preflight-mocks.mjs'");}
  const core="'./review-round12-core.mjs'";
  assert.ok(driver.includes(core));driver=driver.replace(core,JSON.stringify(pathToFileURL(path.join(here,'review-round12-core.mjs')).href));
  const roots="const root='/opt/mokaair',workBase='/var/lib/mokaair/video-work';";
  assert.ok(driver.includes(roots));driver=driver.replace(roots,`const root=${JSON.stringify(root)},workBase=${JSON.stringify(workBase)};`);
  const paths=/const payload=path\.resolve\(path\.dirname\(new URL\(import\.meta\.url\)\.pathname\),'\.\.\/\.\.\/\.\.\/\.\.\/\.\.'\);\s*const candidate=path\.dirname\(new URL\(import\.meta\.url\)\.pathname\);/;
  assert.match(driver,paths);driver=driver.replace(paths,`const payload=${JSON.stringify(payload)};const candidate=${JSON.stringify(candidate)};`);
  const runnable=path.join(candidate,'preflight-fixture.mjs');fs.writeFileSync(runnable,driver);
  const run=spawnSync(process.execPath,[runnable,'--preflight'],{cwd:repo,env:{...process.env,TEMP:childTemp,TMP:childTemp,TMPDIR:childTemp},encoding:'utf8',timeout:15000});
  assert.equal(run.status,0,run.stderr||run.stdout);
  const result=JSON.parse(run.stdout.trim().split(/\r?\n/).at(-1));
  assert.equal(result.event,'A01_ROUND12_PREFLIGHT_PASS');
  assert.equal(result.canonical_lease_acquired,false);
  assert.equal(result.temp_capture_written,true);
  assert.deepEqual(fs.readFileSync(lease),old);
  assert.equal(fs.existsSync(path.join(workdir,'LEASE.dead.json')),false);
  assert.equal(fs.readFileSync(path.join(workdir,'STOP'),'utf8'),'A01 STOP retained\n');
 }finally{
  assert.equal(path.resolve(path.dirname(temp)),path.resolve(os.tmpdir()));
  assert.ok(path.basename(temp).startsWith('a01-preflight-lease-'));
  fs.rmSync(temp,{recursive:true,force:true});
 }
});
