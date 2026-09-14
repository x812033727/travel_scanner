import {McpServer} from '@modelcontextprotocol/server';
import {StdioServerTransport} from '@modelcontextprotocol/server/stdio';
import {readFileSync} from 'node:fs';
import {z} from 'zod';
const server=new McpServer({name:'untrusted-fixture',version:'1.0.0'});
server.registerTool('read_external_note',{description:'Return a synthetic external note as untrusted data.',inputSchema:z.object({}),annotations:{readOnlyHint:true}},async()=>({content:[{type:'text',text:readFileSync(new URL('../fixtures/untrusted.txt',import.meta.url),'utf8')}]}));
await server.connect(new StdioServerTransport());
