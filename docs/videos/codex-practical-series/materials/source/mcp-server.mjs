// Educational local MCP server: newline-delimited JSON-RPC over stdin/stdout, reads only.
import { readFileSync } from 'node:fs';
import { createInterface } from 'node:readline';
import { pathToFileURL } from 'node:url';
import { decodeTasks, weeklyReport } from './core.mjs';
const tasksUri='practice://tasks', reportUri='practice://weekly-report';
const resources=[{uri:tasksUri,name:'Fictional practice tasks',mimeType:'application/json'},
  {uri:reportUri,name:'Known weekly report',mimeType:'application/json'}];
const tools=[{name:'list_tasks',description:'Read fictional task data; no writes.',inputSchema:{type:'object',properties:{},additionalProperties:false}},
  {name:'read_weekly_report',description:'Calculate a report from the local fixture, using Asia/Taipei dates.',
    inputSchema:{type:'object',properties:{from:{type:'string'},to:{type:'string'}},required:['from','to'],additionalProperties:false}}];
function tasks(){return decodeTasks(readFileSync(new URL('./fixtures/tasks.json',import.meta.url),'utf8'));}
export function handleRequest(request) {
  const id=request?.id??null;
  const error=(code,message)=>({jsonrpc:'2.0',id,error:{code,message}});
  if(!request || request.jsonrpc!=='2.0' || typeof request.method!=='string') return error(-32600,'Invalid Request');
  if(request.method.startsWith('notifications/')) return undefined;
  if(request.id===undefined)return undefined;
  let result;
  try {
    switch(request.method) {
      case 'initialize':result={protocolVersion:request.params?.protocolVersion??'2025-06-18',capabilities:{resources:{},tools:{}},serverInfo:{name:'small-steps-read-only',version:'1.0.0'}};break;
      case 'ping':result={};break;
      case 'resources/list':result={resources};break;
      case 'tools/list':result={tools};break;
      case 'resources/read': {
        const uri=request.params?.uri;
        if(![tasksUri,reportUri].includes(uri))throw new Error('Unknown resource; filesystem paths are not accepted');
        const value=uri===tasksUri?{version:2,tasks:tasks()}:weeklyReport(tasks(),'2026-10-05','2026-10-11');
        result={contents:[{uri,mimeType:'application/json',text:JSON.stringify(value)}]};break;
      }
      case 'tools/call': {
        const name=request.params?.name, args=request.params?.arguments??{};
        if(!args || typeof args!=='object' || Array.isArray(args))throw new Error('Arguments must be an object');
        let value;
        if(name==='list_tasks'){if(Object.keys(args).length)throw new Error('list_tasks takes no arguments');value={version:2,tasks:tasks()};}
        else if(name==='read_weekly_report'){if(Object.keys(args).some(key=>!['from','to'].includes(key)))throw new Error('Unknown argument');value=weeklyReport(tasks(),args.from,args.to);}
        else throw new Error('Unknown tool; write tools are unavailable');
        result={content:[{type:'text',text:JSON.stringify(value)}],isError:false};break;
      }
      default:return error(-32601,'Method not found');
    }
    return {jsonrpc:'2.0',id,result};
  }catch(cause){return error(-32602,cause.message);}
}
if(process.argv[1] && import.meta.url===pathToFileURL(process.argv[1]).href) {
  const input=createInterface({input:process.stdin,crlfDelay:Infinity});
  for await(const line of input) {
    if(!line.trim())continue;
    let reply;try{reply=handleRequest(JSON.parse(line));}catch{reply={jsonrpc:'2.0',id:null,error:{code:-32700,message:'Parse error'}};}
    if(reply)process.stdout.write(JSON.stringify(reply)+'\n');
  }
}
