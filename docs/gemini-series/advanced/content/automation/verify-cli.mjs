/** Version-pinned offline integration with the installed CLI, not model simulation evidence. */
import assert from 'node:assert/strict';
import {mkdtempSync, mkdirSync, readFileSync, writeFileSync, readdirSync, renameSync, rmSync, symlinkSync, unlinkSync} from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const cli = path.resolve(process.argv[2] || '');
const python = path.resolve(process.argv[3] || '');
assert.equal(JSON.parse(readFileSync(path.join(cli, 'package.json'), 'utf8')).version, '0.59.0');
const temporary = mkdtempSync(path.join(os.tmpdir(), 'gemini-automation-lab-'));
const isolated = path.join(temporary, 'home');
const results = {};
const record = (n, value) => (results[n] ??= []).push(value);
const put = (file, data) => {mkdirSync(path.dirname(file), {recursive:true}); writeFileSync(file, typeof data === 'string' ? data : JSON.stringify(data, null, 2) + '\n');};
function copy(from, to) {
  mkdirSync(to, {recursive:true});
  for (const item of readdirSync(from, {withFileTypes:true})) {
    assert.ok(!item.isSymbolicLink());
    if (item.isDirectory()) copy(path.join(from,item.name),path.join(to,item.name));
    else writeFileSync(path.join(to,item.name),readFileSync(path.join(from,item.name)));
  }
}
process.env.GEMINI_CLI_HOME = isolated;
process.env.GEMINI_CLI_SYSTEM_SETTINGS_PATH = path.join(temporary,'system.json');
process.env.GEMINI_CLI_SYSTEM_DEFAULTS_PATH = path.join(temporary,'defaults.json');
for (const key of Object.keys(process.env)) if (/GEMINI_API_KEY|GOOGLE_API_KEY|GOOGLE_APPLICATION_CREDENTIALS|GOOGLE_GENAI_USE_VERTEXAI/.test(key)) delete process.env[key];
globalThis.fetch = async () => {throw new Error('No cloud access in this offline verification.');};
put(path.join(isolated,'.gemini/settings.json'),{telemetry:{enabled:false}});
put(process.env.GEMINI_CLI_SYSTEM_SETTINGS_PATH,{});
put(process.env.GEMINI_CLI_SYSTEM_DEFAULTS_PATH,{});
try {
  for (const number of [75,76,77]) copy(path.join(here,'examples',String(number)),path.join(temporary,String(number)));
  const core = await import(pathToFileURL(path.join(cli,'bundle/chunk-YSBB75DZ.js')));
  const catalog = path.join(temporary,'75');
  const workspace = {getDirectories:()=>[catalog], onDirectoriesChanged:()=>()=>{}};
  const mcpConfig = {isTrustedFolder:()=>true, sanitizationConfig:{}, emitMcpDiagnostic:()=>{}};
  const server = {command:python,args:['-X','utf8',path.join(catalog,'server.py')],cwd:catalog,timeout:10000};
  const client = await core.connectToMcpServer('0.59.0','lesson-catalog',server,false,workspace,mcpConfig);
  try {
    const listed = await client.listTools();
    assert.deepEqual(listed.tools.map(t=>t.name),['lookup_product']);
    record(75,{case:'discovery',tools:listed.tools.map(t=>t.name),inputSchema:listed.tools[0].inputSchema});
    for (const [sku,expectedError,found] of [['SKU-001',false,true],['SKU-999',false,false],['../private.txt',true,null],[42,true,null],['SKU-003',false,true]]) {
      const response = await client.callTool({name:'lookup_product',arguments:{sku}});
      assert.equal(Boolean(response.isError),expectedError);
      if (!expectedError) assert.equal(response.structuredContent.found,found);
      record(75,{case:'query',sku,isError:Boolean(response.isError),structuredContent:response.structuredContent ?? null});
    }
  } finally { await client.close(); }
  await assert.rejects(()=>client.callTool({name:'lookup_product',arguments:{sku:'SKU-001'}}));
  record(75,{case:'closed-connection',queryRejected:true,notEquivalentToCliDisable:true});
  await assert.rejects(()=>core.connectToMcpServer('0.59.0','untrusted',server,false,workspace,{...mcpConfig,isTrustedFolder:()=>false}),/not trusted/);
  record(75,{case:'untrusted-workspace',connectionRejected:true});
  await assert.rejects(()=>core.connectToMcpServer('0.59.0','missing-server',{...server,args:['-X','utf8','missing-server.py'],timeout:1500},false,workspace,mcpConfig));
  record(75,{case:'startup-failure',connectionRejected:true});
  await assert.rejects(()=>core.connectToMcpServer('0.59.0','no-handshake',{...server,args:['-c','import time; time.sleep(5)'],timeout:300},false,workspace,mcpConfig));
  record(75,{case:'handshake-timeout',connectionRejected:true});

  const hookRoot = path.join(temporary,'76');
  const runner = new core.HookRunner({isTrustedFolder:()=>true,storage:{getPlansDir:()=>path.join(temporary,'plans')},sanitizationConfig:{}});
  const aggregator = new core.HookAggregator();
  const base = {cwd:hookRoot,session_id:'authored-local-fixture',transcript_path:'',hook_event_name:'BeforeTool',tool_name:'write_file',tool_input:{file_path:'docs/example.md',content:'# 題目\n\n## 來源\n本機樣本'}};
  // Only fixed, reviewed paths are quoted into this shell command. No model input is interpolated.
  const quote = value => `'${value.replaceAll("'", "''")}'`;
  const prefix = process.platform === 'win32' ? '& ' : '';
  const command = `${prefix}${quote(process.execPath)} ./quality-gate.mjs`;
  async function hookCase(name, input, commandOverride, expected, timeout=10000) {
    const hook = {name,type:core.HookType.Command,source:core.ConfigSource.Project,command:commandOverride || command,timeout};
    const result = await runner.executeHook(hook,core.HookEventName.BeforeTool,input);
    const aggregate = aggregator.aggregateResults([result],core.HookEventName.BeforeTool);
    const blocked = aggregate.finalOutput?.getBlockingError().blocked ?? false;
    assert.equal(blocked,expected,name);
    if (name === 'valid' || name === 'valid-absolute-path') {
      assert.equal(result.success,true,name);
      assert.equal(aggregate.finalOutput?.decision,'allow',name);
    }
    record(76,{case:name,runnerSuccess:result.success,exitCode:result.exitCode ?? null,blocked,decision:aggregate.finalOutput?.decision ?? null,reason:aggregate.finalOutput?.getEffectiveReason() ?? '',error:result.error ? String(result.error.message).replaceAll(temporary,'<temporary>') : null});
  }
  await hookCase('valid',base,null,false);
  await hookCase('valid-absolute-path',{...base,tool_input:{...base.tool_input,file_path:path.join(hookRoot,'docs/example.md')}},null,false);
  await hookCase('missing-sources',{...base,tool_input:{...base.tool_input,content:'# 題目'}},null,true);
  await hookCase('outside-scope',{...base,tool_input:{...base.tool_input,file_path:'../private.md'}},null,true);
  await hookCase('unfinished-todo',{...base,tool_input:{...base.tool_input,content:'# 題目\nTODO\n## 來源'}},null,true);
  const docs = path.join(hookRoot,'docs');
  const savedDocs = path.join(hookRoot,'saved-docs');
  const outsideDocs = path.join(temporary,'outside-docs');
  mkdirSync(outsideDocs);
  renameSync(docs,savedDocs);
  try {
    symlinkSync(outsideDocs,docs,process.platform === 'win32' ? 'junction' : 'dir');
    await hookCase('linked-docs-directory',base,null,true);
  } finally {
    // Remove only the temporary directory link; keep its target untouched.
    unlinkSync(docs);
    renameSync(savedDocs,docs);
  }
  for (const [name,source,expected,timeout] of [
    ['exit-one',"process.stderr.write('authored warning'); process.exitCode=1;",false,10000],
    ['exit-two',"process.stderr.write('authored block'); process.exitCode=2;",true,10000],
    ['invalid-stdout',"console.log('not-json');",false,10000],
    ['timeout',"setTimeout(()=>{},10000);",false,1200]]) {
    put(path.join(hookRoot,'case.mjs'),source);
    await hookCase(name,base,`${prefix}${quote(process.execPath)} ./case.mjs`,expected,timeout);
  }
  const registry = new core.HookRegistry({});
  registry.registerHook({name:'switchable',type:core.HookType.Command,command},core.HookEventName.BeforeTool,{source:core.ConfigSource.Project,matcher:'^write_file$'});
  const planner = new core.HookPlanner(registry);
  assert.ok(planner.createExecutionPlan(core.HookEventName.BeforeTool,{toolName:'write_file'}));
  registry.setHookEnabled('switchable',false);
  assert.equal(planner.createExecutionPlan(core.HookEventName.BeforeTool,{toolName:'write_file'}),null);
  record(76,{case:'disabled',executionPlan:null,verified:'actual registry and planner'});

  const agentRoot=path.join(temporary,'77/review-project/.gemini/agents');
  for (const file of ['code-reviewer.md','docs-reviewer.md']) {
    const [agent]=await core.parseAgentMarkdown(path.join(agentRoot,file));
    assert.deepEqual(agent.tools,['read_file','grep_search']);
    assert.equal(agent.model,'inherit');
    assert.equal(agent.max_turns,4);
    record(77,{case:'agent-definition',name:agent.name,tools:agent.tools,model:agent.model,maxTurns:agent.max_turns});
  }
  await assert.rejects(()=>core.parseAgentMarkdown('bad.md','# No frontmatter'));
  record(77,{case:'missing-frontmatter',rejected:true});
  const policyDir=path.join(temporary,'policies');
  put(path.join(policyDir,'no-tools.toml'),readFileSync(path.join(here,'examples/78/no-tools.toml'),'utf8'));
  const policies=await core.loadPoliciesFromToml([policyDir],()=>2);
  assert.equal(policies.errors.length,0);
  const engine=new core.PolicyEngine({rules:policies.rules});
  for (const name of ['read_file','write_file','run_shell_command','mcp_lesson-catalog_lookup_product']) {
    const decision=await engine.check({name,args:{}});
    assert.equal(decision.decision,'deny');
    record(78,{case:'no-tools-policy',tool:name,decision:decision.decision});
  }
  const report={checkedAt:new Date().toISOString(),cli:'0.59.0',node:process.version,platform:process.platform,mcpPythonSdk:'2.2.0',cloudCalls:0,
    method:'actual CLI MCP connection, hook runner/aggregator/planner and agent parser; authored inputs',results,
    pending:['interactive /mcp disable and model tool selection','full model-to-tool hook flow','actual subagent responses and concurrency','real headless model calls','GitHub hosted workflow execution']};
  put(path.join(here,'verification/local-cli.json'),report);
  console.log(JSON.stringify(Object.fromEntries(Object.entries(results).map(([n,rows])=>[n,rows.length]))));
} catch (error) {
  console.error('Verification failed before cleanup:', error);
  throw error;
} finally {
  assert.ok(temporary.startsWith(path.resolve(os.tmpdir())+path.sep));
  rmSync(temporary,{recursive:true,force:true,maxRetries:8,retryDelay:250});
}
