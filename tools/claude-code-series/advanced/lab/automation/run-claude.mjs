import {spawn} from 'node:child_process';import {readFileSync} from 'node:fs';
import {parseResult} from './result.mjs';
const schema=readFileSync(new URL('./schema.json',import.meta.url),'utf8');
const input=readFileSync(new URL('../fixtures/tasks.json',import.meta.url),'utf8');
const args=['-p','--output-format','json','--json-schema',schema,'--max-budget-usd','0.25','--no-session-persistence','--tools','','--strict-mcp-config','--mcp-config','{"mcpServers":{}}'];
const child=spawn(process.env.CLAUDE_BIN??'claude',args,{windowsHide:true,stdio:['pipe','pipe','pipe']});
let output='',diagnostic='',timedOut=false;
const timer=setTimeout(()=>{timedOut=true;child.kill();},90000);
child.stdout.on('data',chunk=>{output+=chunk;if(output.length>1000000)child.kill();});
child.stderr.on('data',chunk=>{diagnostic=(diagnostic+chunk).slice(-4000);});
child.on('error',error=>{clearTimeout(timer);console.error(error.message);process.exitCode=1;});
child.on('close',code=>{
 clearTimeout(timer);
 try{if(timedOut)throw new Error('Claude timeout');if(code!==0)throw new Error('Claude failed: '+diagnostic);
 console.log(JSON.stringify(parseResult(output),null,2));}
 catch(error){console.error(error.message);process.exitCode=1;}
});
child.stdin.end('Summarize the following synthetic todo data in Traditional Chinese. Return all unique task IDs. Do not call tools.\n'+input);
