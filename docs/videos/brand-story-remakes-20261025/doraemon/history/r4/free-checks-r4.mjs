// Ordinary lint and TTS dry-run, using exact copied immutable dictionary bytes.
// No dictionary initializer, fresh native payload/reader, credentials or network.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { main } from '../../../../tools/video/cli.mjs';
import { writeScreenplay } from '../../../../tools/video/core/screenplay.mjs';
import { loadProject } from '../../../../tools/video/core/state.mjs';
import { planRequests } from '../../../../tools/video/tts/requests.mjs';
import { speechHash } from '../../../../tools/video/core/timeline.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const audit='/workspace/work/brand-story-20261025/doraemon-audit/author-r4';
const root=path.join(audit,'free-runtime');
const workdir=path.join(audit,'media');
const taskHome=path.join(audit,'empty-credential-context');
const slug='story-adapt-doraemon-after-fujiko-remake-20261025';
const shelf=path.join(root,'docs/videos');
const target=path.join(shelf,slug);
const oldShelf=path.join(here,'history/r3/runtime-state/docs/videos');
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
fs.mkdirSync(target,{recursive:true});fs.mkdirSync(taskHome,{recursive:true});
const copies=[];
function copyExact(from,to){
  fs.mkdirSync(path.dirname(to),{recursive:true});
  const bytes=fs.readFileSync(from);
  if(fs.existsSync(to)&&!fs.readFileSync(to).equals(bytes))throw new Error('Existing immutable dictionary copy differs; stop.');
  if(!fs.existsSync(to))fs.writeFileSync(to,bytes);
  copies.push({source:from,target:to,sha256:hash(bytes)});
}
copyExact(path.join(oldShelf,'lexicon.json'),path.join(shelf,'lexicon.json'));
function copyTree(from,to){for(const e of fs.readdirSync(from,{withFileTypes:true}))e.isDirectory()?copyTree(path.join(from,e.name),path.join(to,e.name)):copyExact(path.join(from,e.name),path.join(to,e.name));}
copyTree(path.join(oldShelf,slug,'story-lexicon'),path.join(target,'story-lexicon'));
for(const name of ['video.json','brief.md','series.json','claims.md'])fs.copyFileSync(path.join(here,name),path.join(target,name));
if(fs.existsSync(path.join(target,'verify-1.md')))throw new Error('R2 verify must not appear in R3 runtime.');
const doc=JSON.parse(fs.readFileSync(path.join(target,'video.json')));
const canonical=writeScreenplay(target,doc);
let networkAttempts=0;
const run=async args=>{
 let stdout='',stderr='';
 const code=await main(args,{root,home:taskHome,env:{},stdout:{write:s=>{stdout+=s;}},stderr:{write:s=>{stderr+=s;}},fetch:async()=>{networkAttempts++;throw new Error('No network authorized for free author checks.');}});
 return {argv:args,exit_code:code,stdout,stderr};
};
const lint=await run(['lint','--slug',slug,'--json']);
fs.writeFileSync(path.join(here,'native-author-lint-r4.json'),lint.stdout);
fs.writeFileSync(path.join(audit,'ordinary-lint-r4.stderr.txt'),lint.stderr);
if(lint.exit_code!==0)throw new Error(`Ordinary lint failed: ${lint.exit_code}; receipt preserved.`);
const planned=await run(['tts','--slug',slug,'--workdir',workdir,'--dry-run']);
fs.writeFileSync(path.join(audit,'ordinary-free-planner-r4.txt'),planned.stdout+planned.stderr);
if(planned.exit_code!==0)throw new Error(`Ordinary dry-run failed: ${planned.exit_code}; receipt preserved.`);
const project=loadProject({root,slug});
const requests=planRequests(project.doc,project.lexicon);
fs.writeFileSync(path.join(audit,'speech-request-plan-r4.json'),JSON.stringify(requests,null,2)+'\n');
const proof={role:'ORDINARY_FREE_AUTHOR_CHECKS_NOT_FRESH_NATIVE_OR_AUDIO',lint_exit_code:lint.exit_code,planner_exit_code:planned.exit_code,planner_argv:planned.argv,requests:requests.length,speech_hash:speechHash(project.doc,project.lexicon),network_attempts:networkAttempts,credential_context:'empty same-task ctx.home and env; no default credentials inspected',dictionary_initialized:false,dictionary_copies:copies,canonical_script_sha256:hash(fs.readFileSync(canonical)),fresh_native_inputs_prepared:0,fresh_native_readers_run:0,actual_native_rounds_total:2,paid_calls:0};
fs.writeFileSync(path.join(audit,'free-checks-r4.json'),JSON.stringify(proof,null,2)+'\n');
console.log(JSON.stringify({lint_exit_code:lint.exit_code,planner_exit_code:planned.exit_code,requests:requests.length,network_attempts:networkAttempts,dictionary_initialized:false}));
