import { McpServer } from '@modelcontextprotocol/server';
import { StdioServerTransport } from '@modelcontextprotocol/server/stdio';
import { z } from 'zod';
import { listTasks,getTask } from './data.mjs';
const server=new McpServer({name:'mokaair-todo-lab',version:'1.0.0'});
const text = value => ({content:[{type:'text',text:JSON.stringify(value)}]});
server.registerTool('list_tasks',{
  description:'唯讀查詢練習待辦；offset 從 0 開始，每頁最多 20 筆，nextOffset=null 表示結束。',
  inputSchema:z.object({offset:z.number().int().min(0).default(0),limit:z.number().int().min(1).max(20).default(2),completed:z.boolean().optional()}),
  annotations:{readOnlyHint:true}
},async args=>text(listTasks(args)));
server.registerTool('get_task',{
  description:'依 id 查詢一筆練習待辦；找不到時回傳 found=false。',
  inputSchema:z.object({id:z.string().min(1).max(100)}),
  annotations:{readOnlyHint:true}
},async ({id})=>text({found:getTask(id)!==null,item:getTask(id)}));
await server.connect(new StdioServerTransport());
