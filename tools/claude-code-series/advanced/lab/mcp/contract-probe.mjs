import {Client} from '@modelcontextprotocol/client';
import {StdioClientTransport} from '@modelcontextprotocol/client/stdio';
import {fileURLToPath} from 'node:url';
const client=new Client({name:'contract-probe',version:'1.0.0'});
const transport=new StdioClientTransport({command:process.execPath,args:[fileURLToPath(new URL('./server.mjs',import.meta.url))],stderr:'pipe'});
try{
 await client.connect(transport);
 const call=async(name,args)=>{
  const response=await client.callTool({name,arguments:args});
  if(response.isError)throw new Error(response.content?.[0]?.text??'Tool error');
  return JSON.parse(response.content[0].text);
 };
 const items=[];let offset=0;const seen=new Set();
 do{
  if(seen.has(offset)||seen.size>=20)throw new Error('Invalid or excessive pagination');
  seen.add(offset);
  const page=await call('list_tasks',{offset,limit:2});items.push(...page.items);offset=page.nextOffset;
 }while(offset!==null);
 console.log(JSON.stringify({ids:items.map(x=>x.id),missing:await call('get_task',{id:'missing'}),empty:await call('list_tasks',{offset:100})},null,2));
}finally{await client.close();}
