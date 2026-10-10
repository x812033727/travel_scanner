import test from 'node:test';import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';import {spawnSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
import {handleRequest} from '../mcp-server.mjs';
const rpc=(method,params={})=>handleRequest({jsonrpc:'2.0',id:1,method,params});
test('local MCP lists whitelisted resources/tools and computes known truth',()=>{
  assert.equal(rpc('initialize',{protocolVersion:'2025-06-18'}).result.protocolVersion,'2025-06-18');
  assert.deepEqual(rpc('tools/list').result.tools.map(tool=>tool.name),['list_tasks','read_weekly_report']);
  assert.deepEqual(rpc('resources/list').result.resources.map(resource=>resource.uri),['practice://tasks','practice://weekly-report']);
  const report=JSON.parse(rpc('tools/call',{name:'read_weekly_report',arguments:{from:'2026-10-05',to:'2026-10-11'}}).result.content[0].text);
  assert.equal(report.total,5);assert.equal(report.completedInWeek,2);
  assert.equal(JSON.parse(rpc('resources/read',{uri:'practice://tasks'}).result.contents[0].text).tasks.length,5);
});
test('MCP refuses writes/path escape/additional args and leaves fixture unchanged',()=>{
  const path=new URL('../fixtures/tasks.json',import.meta.url),before=readFileSync(path,'utf8');
  for(const request of [['tools/call',{name:'write_task',arguments:{id:'bad'}}],['resources/read',{uri:'../../secret'}],
    ['tools/call',{name:'list_tasks',arguments:{path:'elsewhere'}}],['tools/call',{name:'read_weekly_report',arguments:{from:'bad',to:'bad'}}]])assert.ok(rpc(...request).error);
  assert.equal(readFileSync(path,'utf8'),before);
  assert.equal(handleRequest({jsonrpc:'2.0',method:'notifications/initialized'}),undefined);
});
test('real stdio framing returns JSON only, handles malformed input, and exits on EOF',()=>{
  const request={jsonrpc:'2.0',id:7,method:'tools/call',params:{name:'list_tasks',arguments:{}}};
  const run=spawnSync(process.execPath,[fileURLToPath(new URL('../mcp-server.mjs',import.meta.url))],
    {input:JSON.stringify(request)+'\n{bad\n',encoding:'utf8',timeout:5000});
  assert.equal(run.status,0);const lines=run.stdout.trim().split('\n').map(JSON.parse);
  assert.equal(lines[0].id,7);assert.equal(lines[1].error.code,-32700);assert.equal(run.stderr,'');
});
