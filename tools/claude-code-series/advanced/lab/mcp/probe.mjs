import { Client } from '@modelcontextprotocol/client';
import { StdioClientTransport } from '@modelcontextprotocol/client/stdio';
import { fileURLToPath } from 'node:url';
const transport=new StdioClientTransport({command:process.execPath,args:[fileURLToPath(new URL('./server.mjs',import.meta.url))],stderr:'pipe'});
const client=new Client({name:'mokaair-probe',version:'1.0.0'});
try {
  await client.connect(transport);
  const tools=await client.listTools();
  const result=await client.callTool({name:'list_tasks',arguments:{limit:2}});
  console.log(JSON.stringify({tools:tools.tools.map(t=>t.name),result},null,2));
} finally { await client.close(); }
