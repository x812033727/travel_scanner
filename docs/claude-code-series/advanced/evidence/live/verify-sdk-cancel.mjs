import {createRequire} from 'node:module';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {mkdtempSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import path from 'node:path';

const root=fileURLToPath(new URL('../../../../../',import.meta.url));
const sdkRequire=createRequire(path.join(root,'tools/claude-code-series/advanced/lab/automation/sdk/package.json'));
const {query}=await import(pathToFileURL(sdkRequire.resolve('@anthropic-ai/claude-agent-sdk')).href);
const controller=new AbortController();
const directory=mkdtempSync(path.join(tmpdir(),'mokaair-sdk-cancel-'));
const report={started_at:new Date().toISOString(),scope:'Cancel a real SDK stream on its first output text delta; no tool execution',sdk_version:'0.3.270',initialized:false,received_text_delta:false,aborted:false,completed:false};
const options={cwd:directory,tools:[],settingSources:[],mcpServers:{},maxTurns:3,maxBudgetUsd:0.25,abortController:controller,persistSession:false,includePartialMessages:true};
if(process.env.CLAUDE_BIN)options.pathToClaudeCodeExecutable=process.env.CLAUDE_BIN;
async function* input(){
  yield {type:'user',message:{role:'user',content:'Write an 800-word fictional story about a tiny robot that learns to garden. Begin the story directly, without an introduction. End with MOKAAIR-SDK-CANCEL-94-COMPLETED. Do not use tools.'},parent_tool_use_id:null};
  if(!controller.signal.aborted)await new Promise(resolve=>controller.signal.addEventListener('abort',resolve,{once:true}));
}
const stream=query({prompt:input(),options});
const deadline=setTimeout(()=>controller.abort(),20000);
try{
  for await(const message of stream){
    if(message.type==='system'&&message.subtype==='init'){
      report.initialized=true;
      report.session_id=message.session_id;
    }
    if(message.type==='stream_event'&&message.event.type==='content_block_delta'&&message.event.delta.type==='text_delta'&&!controller.signal.aborted){
      report.received_text_delta=true;
      report.first_delta=message.event.delta.text;
      report.abort_requested_at=new Date().toISOString();
      controller.abort();
    }
    if(message.type==='result'){
      report.result_subtype=message.subtype;
      report.result=message.result??null;
      report.normal_success=message.subtype==='success'&&!message.is_error&&Boolean(message.result)&&!/(interrupted|aborted)/i.test(message.result);
      report.completed=message.subtype==='success'&&Boolean(message.result?.includes('MOKAAIR-SDK-CANCEL-94-COMPLETED'));
    }
  }
}catch(error){
  report.error_name=error.name;
  report.error=error.message;
}finally{
  clearTimeout(deadline);
  stream.close();
  report.aborted=controller.signal.aborted;
  report.passed=report.initialized&&report.received_text_delta&&report.aborted&&!report.completed&&!report.normal_success&&/abort/i.test(report.error??'');
  report.finished_at=new Date().toISOString();
  writeFileSync(new URL('./sdk-cancel.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report));
}
process.exitCode=report.passed?0:1;
