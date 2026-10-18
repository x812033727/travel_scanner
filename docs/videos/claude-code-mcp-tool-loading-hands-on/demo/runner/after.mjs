// After every session: the init event against what the arm should hold, which models the stream
// names, what was searched for and called, and what the MCP server itself recorded. One verdict.
//
//   node <seed>/runner/after.mjs <logs>/<name>.stream.jsonl
//
// Next to the stream it reads <name>.session.txt (for the arm), <name>.seen.txt (the logging
// hook) and <name>.lab/server/requests.txt (the server's own record).
// Only the seed's own names are printed (the MCP server gear and its forty tools) and the names
// of Claude Code's built-in tools. Any other plugin, skill, agent, MCP server or MCP tool is a
// count, never a name or a path. Rate-limit events are never read.
//
// The verdict has seven parts: the models named, the permission mode, the built-in tools, what
// is listed or called that is not the seed's, the instruction files loaded, the arm's own server
// and tools, and whether a file tool was aimed outside the project. STOP in any part means: do
// not start the next session.
import { existsSync, readFileSync } from 'node:fs';
import { basename, dirname, isAbsolute, join, relative, resolve } from 'node:path';

const file = process.argv[2];
const dir = dirname(file);
const name = basename(file).replace(/\.stream\.jsonl$/, '');
const read = (path) => (existsSync(path) ? readFileSync(path, 'utf8') : null);
const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap((line) => {
  try { return [JSON.parse(line)]; } catch { return []; }
}).filter((line) => line.type !== 'rate_limit_event');
const arm = ((read(join(dir, `${name}.session.txt`)) ?? '').match(/^# \S+ \| arm (\S+)/) ?? [])[1] ?? '?';
// base, off, on: no server. d<N>, u<N>, a<N>: the server with N tools, deferred (the default),
// with tool search off, or in threshold mode. use-d<N>, use-u<N>: the same, with a request that
// calls one tool.
const shape = arm.match(/^(use-)?([dua])(\d+)$/);
const want = shape ? { server: true, count: Number(shape[3]), mode: shape[2], use: Boolean(shape[1]) } : { server: false, count: 0, mode: arm === 'off' ? 'u' : 'd', use: false };
// Whether ToolSearch must be on the init list. An arm named for deferred loading with at least
// one tool must list it; an arm with tool search off must not. Either is a STOP: the arm is not
// in the mode it is named for (managed settings, or a provider variable in the shell, can
// decide that over the arm's own variable). Left open: the server with no tools, threshold mode
// and "on" (nothing says which way they go); in a base without a server its absence is a LOOK.
const searchWant = want.mode === 'u' ? 'no' : want.mode === 'd' && want.server && want.count > 0 ? 'yes' : 'open';
const searchOptional = searchWant !== 'yes' && (want.mode !== 'd' || arm === 'on' || (want.server && want.count === 0));

const BUILT_IN = new Set(['Explore', 'Plan', 'general-purpose', 'claude', 'statusline-setup', 'claude-code-guide']);
const SHIPPED = new Set(['deep-research', 'design', 'design-sync', 'dataviz', 'artifact-diagramming',
  'artifact-capabilities', 'update-config', 'verify', 'debug', 'code-review', 'simplify', 'batch',
  'fewer-permission-prompts', 'doctor', 'loop', 'schedule', 'claude-api', 'workflow-authoring', 'run',
  'run-skill-generator', 'plugin-authoring', 'claude-in-chrome', 'slides', 'init', 'security-review', 'keybindings-help']);
const OUR_TOOL = /^mcp__gear__[a-z_]{6,20}$/;
const names = (list) => (list ?? []).map((each) => (typeof each === 'string' ? each : each.name));
const short = (tool) => String(tool).replace('mcp__gear__', '');

// Models named anywhere in the stream.
const found = new Map();
const walk = (value, key) => {
  if (Array.isArray(value)) { for (const each of value) walk(each, key); return; }
  if (value && typeof value === 'object') {
    for (const [k, v] of Object.entries(value)) {
      if (k === 'modelUsage' && v && typeof v === 'object') {
        for (const model of Object.keys(v)) found.set(`modelUsage key: ${model}`, (found.get(`modelUsage key: ${model}`) ?? 0) + 1);
        continue;
      }
      walk(v, k);
    }
    return;
  }
  if (typeof value === 'string' && key && /^(model|resolvedModel)$/i.test(key)) {
    const label = `${key}: ${value}`;
    found.set(label, (found.get(label) ?? 0) + 1);
  }
};
for (const line of lines) walk(line, null);

// The init event.
const inits = lines.filter((line) => line.type === 'system' && line.subtype === 'init');
const init = inits[0] ?? {};
const tools = init.tools ?? [];
const builtin = tools.filter((tool) => !String(tool).startsWith('mcp__'));
const mcpTools = tools.filter((tool) => String(tool).startsWith('mcp__'));
const ourTools = mcpTools.filter((tool) => OUR_TOOL.test(tool));
const servers = init.mcp_servers ?? [];
const gear = servers.filter((server) => server.name === 'gear');
const plugins = (init.plugins ?? []).map((each) => (typeof each === 'string' ? { name: each } : each));
const own = plugins.filter((each) => String(each.name).startsWith('cc-plugin-'));
const skills = names(init.skills);
const agents = names(init.agents);
const commands = names(init.slash_commands);
const other = {
  plugins: plugins.length - own.length,
  skills: skills.filter((skill) => !SHIPPED.has(skill)).length,
  agents: agents.filter((agent) => !BUILT_IN.has(agent)).length,
  servers: servers.length - gear.length,
  tools: mcpTools.length - ourTools.length,
};

// The logging hook's record.
const seen = (read(join(dir, `${name}.seen.txt`)) ?? '').split('\n').filter(Boolean);
const loads = seen.filter((line) => line.startsWith('InstructionsLoaded'));
const seenCalls = seen.filter((line) => /^(PreToolUse|PermissionRequest) /.test(line));
const seenOutside = seenCalls.filter((line) => line.includes('(outside the project') || line.includes('BLOCKED'));
const seenBlocked = seenCalls.filter((line) => line.includes('BLOCKED')).length;
const kinds = {};
for (const line of seen) kinds[line.split(' ')[0]] = (kinds[line.split(' ')[0]] ?? 0) + 1;

// What the session called, and what came back for a ToolSearch call.
const calls = [];
const done = new Set();
for (const line of lines) {
  if (line.type !== 'assistant') continue;
  for (const block of line.message?.content ?? []) {
    if (block.type !== 'tool_use' || done.has(block.id)) continue;
    done.add(block.id);
    calls.push({ id: block.id, tool: block.name, input: block.input ?? {}, under: Boolean(line.parent_tool_use_id) });
  }
}
const searchIds = new Set(calls.filter((call) => call.tool === 'ToolSearch').map((call) => call.id));
const searches = [];
for (const line of lines) {
  if (line.type !== 'user' || !Array.isArray(line.message?.content)) continue;
  for (const block of line.message.content) {
    if (block.type !== 'tool_result' || !searchIds.has(block.tool_use_id)) continue;
    const inner = Array.isArray(block.content) ? block.content : [];
    const refs = inner.filter((each) => each?.type === 'tool_reference').map((each) => String(each.tool_name ?? '?'));
    const how = line.tool_use_result ?? {};
    searches.push({ id: block.tool_use_id, refs, text: inner.filter((each) => each?.type === 'text').reduce((n, each) => n + String(each.text ?? '').length, 0), matches: Array.isArray(how.matches) ? how.matches.length : '-', total: how.total_deferred_tools ?? '-' });
  }
}
const FILE_TOOLS = new Set(['Read', 'Edit', 'Write', 'NotebookEdit', 'Glob', 'Grep']);
const cwd = String(init.cwd ?? '');
const native = (path) => (process.platform === 'win32' ? String(path).replace(/^\/([A-Za-z])\//, '$1:/') : String(path));
const within = (base, path) => { if (!base) return false; const rel = relative(base, path); return !rel.startsWith('..') && !isAbsolute(rel); };
const outsidePath = (path) => String(path).startsWith('~') || !within(cwd, resolve(cwd, native(path)));
const ROOTED = /^([A-Za-z]:|[\\/]|~|\.\.([\\/]|$))/;
const aimedOutside = (call) => {
  if (!cwd || !FILE_TOOLS.has(call.tool)) return false;
  const path = call.input.file_path ?? call.input.notebook_path ?? call.input.path;
  if (path && outsidePath(path)) return true;
  const glob = call.tool === 'Glob' ? call.input.pattern : call.tool === 'Grep' ? call.input.glob : null;
  return Boolean(glob) && ROOTED.test(String(glob)) && outsidePath(String(glob).split(/[*?[{]/)[0] || '.');
};
const streamOutside = calls.filter(aimedOutside).length;
const gearCalls = calls.filter((call) => OUR_TOOL.test(call.tool));
const otherMcpCalls = calls.filter((call) => String(call.tool).startsWith('mcp__') && !OUR_TOOL.test(call.tool)).length;
const byTool = {};
for (const call of calls) {
  const label = String(call.tool).startsWith('mcp__') ? (OUR_TOOL.test(call.tool) ? call.tool : 'mcp__(a server)') : call.tool;
  byTool[label] = (byTool[label] ?? 0) + 1;
}
const requests = (read(join(dir, `${name}.lab`, 'server', 'requests.txt')) ?? '').split('\n').filter(Boolean);
const asked = (word) => requests.filter((line) => line.includes(` ${word}`)).length;
const startLine = requests.find((line) => / start with \d+ of \d+ tools$/.test(line)) ?? '';
const served = startLine ? Number(startLine.match(/start with (\d+) of/)[1]) : null;
const at = (word) => { const line = requests.find((each) => each.includes(` ${word}`)); return line ? `${line.match(/\+\s*(\d+)ms/)?.[1] ?? '?'} ms` : '-'; };
const results = lines.filter((line) => line.type === 'result');
const denials = results.flatMap((result) => result.permission_denials ?? []);
const gearName = (tool) => (OUR_TOOL.test(tool) ? short(tool) : '(not gear\'s)');
// A query is the model's own words; only the gear tool names in it are kept as they are.
const queryShown = (query) => String(query ?? '').replace(/mcp__(?!gear__)[\w-]+/g, 'mcp__(other)').replaceAll('\n', ' ').slice(0, 70);

console.log(`-- after.mjs ${name} | arm ${arm} | Claude Code ${init.claude_code_version ?? '?'} | init events ${inits.length}`);
console.log(`   init model: ${init.model} | permissionMode: ${init.permissionMode}`);
for (const [label, count] of [...found].sort()) console.log(`   ${label} (x${count})`);
console.log(`   built-in tools (${builtin.length}): ${builtin.join(' ') || 'none'}`);
console.log(`   mcp_servers: ${servers.length} = gear ${gear.length}${gear.length ? ` (${gear.map((server) => server.status).join(', ')})` : ''} + any other ${other.servers}`);
console.log(`   MCP tools on the init event: ${mcpTools.length} = gear's ${ourTools.length} + any other ${other.tools} | this arm's server should hold ${want.count}`);
console.log(`   plugins: ${plugins.length} = cc-plugin-* ${own.length} + any other ${other.plugins} | skills: ${skills.length} = shipped with Claude Code ${skills.length - other.skills} + any other ${other.skills} | agents: ${agents.length} = built in ${agents.length - other.agents} + any other ${other.agents} | slash commands: ${commands.length}`);
console.log(`   counts a base must share with an arm: built-in tools ${builtin.length} | skills ${skills.length} | agents ${agents.length} | slash commands ${commands.length} | plugins ${plugins.length}`);
console.log(`   logging hook's record: ${seen.length} lines | ${Object.entries(kinds).map(([kind, count]) => `${kind} ${count}`).join(', ') || 'none'} | instruction files loaded: ${loads.length}`);
console.log(`   tool calls in the stream: ${calls.length}${calls.length ? ` (${Object.entries(byTool).map(([tool, count]) => `${tool} ${count}`).join(', ')})` : ''} | under Agent calls ${calls.filter((call) => call.under).length}`);
console.log(`   ToolSearch calls: ${searchIds.size}`);
for (const call of calls.filter((each) => each.tool === 'ToolSearch')) {
  const back = searches.find((each) => each.id === call.id);
  console.log(`      query "${queryShown(call.input.query)}" max_results ${call.input.max_results ?? '-'}`);
  if (!back) { console.log('      -> no result line for it in the stream'); continue; }
  const ours = back.refs.filter((tool) => OUR_TOOL.test(tool));
  console.log(`      -> ${back.refs.length} tool references (gear's ${ours.length}: ${ours.map(short).join(', ') || 'none'}; any other ${back.refs.length - ours.length}), ${back.text} chars of text | tool_use_result: matches ${back.matches}, total_deferred_tools ${back.total}`);
}
console.log(`   gear tool calls: ${gearCalls.length}${gearCalls.length ? ` (${gearCalls.map((call) => `${short(call.tool)} ${JSON.stringify(call.input)}`).join(', ')})` : ''} | other MCP calls ${otherMcpCalls}`);
console.log(`   the MCP server's own record: ${requests.length} lines | tools served ${served ?? '-'} | initialize ${asked('initialize')} (at ${at('initialize')}) | tools/list ${asked('tools/list')} (at ${at('tools/list')}) | tools/call ${asked('tools/call')} (first at ${at('tools/call')})`);
console.log(`   file-tool calls aimed outside the project: in the stream ${cwd ? streamOutside : '(no cwd on the init event: not counted)'} | in the logging hook's record ${seenOutside.length} (stopped by it: ${seenBlocked})`);
console.log(`   result lines: ${results.map((result) => `${result.subtype} (${result.num_turns} turns, is_error ${result.is_error ?? '-'})`).join(' | ') || 'none'} | permission_denials ${denials.length}${denials.length ? ` (${denials.map((each) => (String(each.tool_name ?? '').startsWith('mcp__') ? gearName(each.tool_name) : each.tool_name)).join(', ')})` : ''}`);
const subtypes = {};
for (const line of lines) if (line.type === 'system') subtypes[line.subtype] = (subtypes[line.subtype] ?? 0) + 1;
console.log(`   system lines by subtype: ${Object.entries(subtypes).map(([subtype, count]) => `${subtype} ${count}`).join(', ') || 'none'}`);
if (want.use) {
  const said = results.map((result) => (typeof result.result === 'string' ? result.result : '')).join('\n');
  console.log(`   the answer (recorded, not scored): names shelf D-07 ${said.includes('D-07') ? 'yes' : 'no'} | 37 ${/(^|\D)37(\D|$)/.test(said) ? 'yes' : 'no'}`);
}

const modelKeys = [...found.keys()];
const badModel = !modelKeys.length || modelKeys.some((key) => !/sonnet|haiku|synthetic/i.test(key));
// "manual" is the same mode under its other name (the official cli-reference page).
const badMode = !['default', 'manual'].includes(init.permissionMode);
// With tool search off Claude Code drops ToolSearch from the list (the previous video's record
// showed that). Where this arm turns it off, or leaves the choice to Claude Code, it may be
// there or not; in every other arm it must be.
const wanted = ['Edit', 'Glob', 'Grep', 'Read', 'Skill', 'ToolSearch', 'Write'].filter((tool) => !(searchOptional && tool === 'ToolSearch'));
const spawn = builtin.filter((tool) => tool === 'Agent' || tool === 'Task');
const rest = builtin.filter((tool) => tool !== 'Agent' && tool !== 'Task' && !(searchOptional && tool === 'ToolSearch')).sort();
const badTools = rest.join(' ') !== wanted.join(' ') || spawn.length === 0;
const shell = builtin.filter((tool) => /^(Bash|PowerShell)$/i.test(tool)).length;
const badOutside = streamOutside > 0 || seenOutside.length > 0;
const badOthers = Object.values(other).some((count) => count > 0) || otherMcpCalls > 0;
const badLoads = loads.length > 0;
const part = [];
if (want.server !== (gear.length === 1)) part.push(`server gear ${want.server ? 'missing' : 'listed'}`);
if (want.server && gear.length === 1 && gear[0].status !== 'connected') part.push(`server gear is ${gear[0].status}, not connected, when the first request was built`);
if (want.server && served !== want.count) part.push(`the server's own record says it served ${served ?? 'nothing'}, not ${want.count}`);
if (want.server && asked('tools/list') < 1) part.push('the server was never asked for tools/list');
if (!want.server && (requests.length > 0 || ourTools.length > 0)) part.push('an arm without the server has a server record or gear tools');
// Whether deferred tools are listed on the init event is something this video looks at, so for
// a deferred arm the count is only printed above. With tool search off they must all be there.
if (want.server && want.mode === 'u' && ourTools.length !== want.count) part.push(`${ourTools.length} gear tools listed with tool search off, not ${want.count}`);
if (searchWant === 'yes' && !builtin.includes('ToolSearch')) part.push(`arm ${arm} is named for deferred loading and ToolSearch is not on the init list`);
if (searchWant === 'no' && builtin.includes('ToolSearch')) part.push(`arm ${arm} turns tool search off and ToolSearch is on the init list`);
if (want.server && ![0, want.count].includes(ourTools.length)) part.push(`${ourTools.length} gear tools listed, neither 0 nor ${want.count}`);
console.log(`   verdict: ${badModel ? 'STOP: a model that is not sonnet or haiku is named, or none is' : 'only sonnet (or haiku) named'}`
  + ` | ${badMode ? 'STOP: the permission mode is not default' : `permission mode ${init.permissionMode}`}`
  + ` | ${shell ? 'STOP: Bash or PowerShell is among the built-in tools' : badTools ? `LOOK: the built-in tools are not ${wanted.join(' ')} plus Agent or Task` : `the expected built-in tools${searchOptional ? ` (ToolSearch listed: ${builtin.includes('ToolSearch') ? 'yes' : 'no'})` : ''}`}`
  + ` | ${badOthers ? 'STOP: a plugin, skill, agent, MCP server or MCP tool that is not the seed\'s or Claude Code\'s own is listed or was called (counts above; names not printed)' : 'nothing listed or called that is not the seed\'s or Claude Code\'s own'}`
  + ` | ${badLoads ? 'STOP: an instruction file was loaded and this project has none (count above; paths not printed)' : 'no instruction file loaded'}`
  + ` | ${part.length ? `STOP: ${part.join('; ')}` : `the server and tools of arm ${arm} and no other`}`
  + ` | ${badOutside ? 'STOP: a file tool was aimed outside the project (counts above; paths not printed)' : 'no file tool aimed outside the project'}`);
