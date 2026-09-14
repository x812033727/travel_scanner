import test from 'node:test';import assert from 'node:assert/strict';
import {mkdtempSync,writeFileSync,mkdirSync,readFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';import path from 'node:path';import {fileURLToPath} from 'node:url';import {spawnSync} from 'node:child_process';
const root=mkdtempSync(path.join(tmpdir(),'mokaair-hooks-'));
const run=(file,event)=>spawnSync(process.execPath,[fileURLToPath(new URL('../hooks/'+file+'.mjs',import.meta.url))],{input:typeof event==='string'?event:JSON.stringify({cwd:root,...event}),encoding:'utf8',windowsHide:true,timeout:20000});
test('guard rejects protected/outside writes and allows a normal fixture',()=>{
 try {
  for(const file_path of ['private/key.txt','../outside.txt'])assert.equal(JSON.parse(run('protect',{hook_event_name:'PreToolUse',tool_name:'Write',tool_input:{file_path}}).stdout).hookSpecificOutput.permissionDecision,'deny');
  assert.equal(run('protect',{hook_event_name:'PreToolUse',tool_name:'Edit',tool_input:{file_path:'fixtures/tasks.json'}}).stdout,'');
  assert.equal(run('protect','invalid').status,2);
  assert.equal(run('audit','\ufeff'+JSON.stringify({cwd:root,hook_event_name:'PostToolUse',tool_name:'Edit'})+'\r\n').status,0);
 }finally{}
});
test('formatter is scoped and idempotent and preserves JSON string whitespace',()=>{
 mkdirSync(path.join(root,'fixtures'));const file=path.join(root,'fixtures/tasks.json');
 writeFileSync(file,'{"title":"two  spaces  "}');
 const event={hook_event_name:'PostToolUse',tool_input:{file_path:file}};
 assert.equal(run('format-json',event).stdout,'');
 const formatted=readFileSync(file,'utf8');assert.equal(JSON.parse(formatted).title,'two  spaces  ');
 run('format-json',event);assert.equal(readFileSync(file,'utf8'),formatted);
 writeFileSync(file,'not json');assert.match(run('format-json',event).stdout,/JSON formatting failed/);
});
test('audit omits raw tool input and repeated Stop terminates',()=>{
 run('audit',{hook_event_name:'PostToolUse',tool_name:'Edit',tool_input:{secret:'FAKE-DO-NOT-LOG'}});
 assert.doesNotMatch(readFileSync(path.join(root,'run-data/events.jsonl'),'utf8'),/FAKE-DO-NOT-LOG/);
 assert.equal(run('quality',{hook_event_name:'Stop',stop_hook_active:true}).stdout,'');
 assert.equal(JSON.parse(run('quality',{hook_event_name:'Stop',stop_hook_active:false}).stdout).decision,'block');
});
process.on('exit',()=>{assert.ok(path.basename(root).startsWith('mokaair-hooks-'));rmSync(root,{recursive:true,force:true});});
