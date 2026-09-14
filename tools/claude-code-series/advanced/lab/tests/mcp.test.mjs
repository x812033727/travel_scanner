import test from 'node:test';
import assert from 'node:assert/strict';
import { Client } from '@modelcontextprotocol/client';
import { StdioClientTransport } from '@modelcontextprotocol/client/stdio';
import { fileURLToPath } from 'node:url';
test('actual stdio MCP lists tools, paginates, rejects bad input and returns unknown id',async()=>{
 const client=new Client({name:'test',version:'1.0.0'});
 const transport=new StdioClientTransport({command:process.execPath,args:[fileURLToPath(new URL('../mcp/server.mjs',import.meta.url))],stderr:'pipe'});
 try {
  await client.connect(transport);
  assert.deepEqual((await client.listTools()).tools.map(t=>t.name).sort(),['get_task','list_tasks']);
  const call=async(name,args)=>client.callTool({name,arguments:args});
  const first=JSON.parse((await call('list_tasks',{limit:2})).content[0].text);
  const last=JSON.parse((await call('list_tasks',{offset:first.nextOffset,limit:2})).content[0].text);
  assert.deepEqual([...first.items,...last.items].map(x=>x.id),['a','b','c']);
  assert.equal(last.nextOffset,null);
  assert.equal(JSON.parse((await call('get_task',{id:'missing'})).content[0].text).found,false);
  const missing=JSON.parse((await call('get_task',{id:'missing'})).content[0].text);assert.equal(missing.item,null);
  const empty=JSON.parse((await call('list_tasks',{offset:100})).content[0].text);assert.deepEqual(empty.items,[]);assert.equal(empty.nextOffset,null);
  const active=JSON.parse((await call('list_tasks',{completed:false})).content[0].text);assert.deepEqual(active.items.map(x=>x.id),['a','c']);
  for(const args of [{limit:0},{limit:21},{offset:-1},{completed:'false'}])assert.equal((await call('list_tasks',args)).isError,true);
 } finally {await client.close();}
});
