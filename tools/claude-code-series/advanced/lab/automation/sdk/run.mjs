import {query} from '@anthropic-ai/claude-agent-sdk';
import {mkdirSync,readFileSync,writeFileSync,existsSync,renameSync,appendFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {successfulResult,requireResumeState} from './state.mjs';
import path from 'node:path';
const stateDir=path.resolve('run-data');mkdirSync(stateDir,{recursive:true});
const stateFile=path.join(stateDir,'session.json');
const previous=process.argv.includes('--resume') && existsSync(stateFile)?JSON.parse(readFileSync(stateFile,'utf8')):null;
if(process.argv.includes('--resume')&&!previous){console.error('No saved session');process.exit(2);}
if(previous)requireResumeState(previous);
const controller=new AbortController();
const cancel=()=>controller.abort();process.once('SIGINT',cancel);
const timer=setTimeout(cancel,60000);
const prompt=previous?'Reply with the project marker from our last exchange.':process.argv.includes('--cancel-demo')?'The synthetic project marker is MOKAAIR-SDK-94. Write an 800-word fictional story about a tiny robot learning to garden; end with the marker. Do not use tools.':'The synthetic project marker is MOKAAIR-SDK-94. Acknowledge it briefly. Do not use tools.';
const pkg=JSON.parse(readFileSync(new URL('./package.json',import.meta.url),'utf8'));
let state={schemaVersion:1,driverVersion:2,sdkVersion:pkg.dependencies['@anthropic-ai/claude-agent-sdk'],status:'running',sessionId:previous?.sessionId??null,input:prompt,inputSha256:createHash('sha256').update(prompt).digest('hex'),startedAt:new Date().toISOString()};
const save=()=>{state.updatedAt=new Date().toISOString();const temp=stateFile+'.tmp';writeFileSync(temp,JSON.stringify(state,null,2)+'\n');renameSync(temp,stateFile);};
save();
let finishInput;
const inputFinished=new Promise(resolve=>{finishInput=resolve;});
controller.signal.addEventListener('abort',finishInput,{once:true});
async function* input(){
 yield {type:'user',message:{role:'user',content:prompt},parent_tool_use_id:null};
 // Keep input open until completion/cancellation so realtime interruption works.
 await inputFinished;
}
let messages;
try{
 const options={cwd:process.cwd(),tools:[],settingSources:[],mcpServers:{},maxTurns:3,maxBudgetUsd:0.25,abortController:controller,persistSession:true,includePartialMessages:true};
 if(process.env.CLAUDE_BIN)options.pathToClaudeCodeExecutable=process.env.CLAUDE_BIN;
 if(previous)options.resume=previous.sessionId;
 messages=query({prompt:input(),options});
 for await(const message of messages){
  appendFileSync(path.join(stateDir,'events.jsonl'),JSON.stringify({type:message.type,subtype:message.subtype??null,at:new Date().toISOString()})+'\n');
  if(message.type==='system'&&message.subtype==='init'){state.sessionId=message.session_id;save();}
  if(message.type==='stream_event'&&message.event.type==='content_block_delta'&&message.event.delta.type==='text_delta'&&!state.firstOutputAt){state.firstOutputAt=new Date().toISOString();save();console.log('Received first text output; Ctrl+C can cancel this run.');}
  if(message.type==='result'){
   const valid=successfulResult(message);
   state={...state,status:valid?'completed':'failed',result:message.result??null,subtype:message.subtype};
   save();
   finishInput();
  }
 }
 if(state.status==='running')throw new Error('Stream ended without final result');
 if(state.status==='failed')process.exitCode=1;
}catch(error){state={...state,status:controller.signal.aborted?'cancelled':'failed',error:error.message};save();process.exitCode=1;}
finally{finishInput();messages?.close();clearTimeout(timer);controller.signal.removeEventListener('abort',finishInput);process.removeListener('SIGINT',cancel);console.log(JSON.stringify(state,null,2));}
