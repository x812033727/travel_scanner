// After every session: the init event against what the arm should hold, which models the stream
// names, which instruction files were loaded, and which parts the session used. One verdict line.
//
//   node <seed>/runner/after.mjs <logs>/<name>.stream.jsonl      (KIT_DIR may name the plugin folder)
//
// Next to the stream it reads <name>.session.txt (for the arm), <name>.seen.txt (the logging
// hook), <name>.guard.txt, <name>.note.txt and <name>.lab/server/requests.txt.
// Only the seed's own names are printed (the plugin ship-kit, the skill release-prep, the agent
// log-scout, the MCP server gear and its two tools) and the names of Claude Code's built-in
// tools. Any other plugin, skill, agent, MCP server or MCP tool is a count, never a name or a
// path. Rate-limit events are never read.
//
// The verdict has seven parts: the models named, the permission mode, the built-in tools, what
// is listed or called that is not the seed's, the instruction files loaded, the arm's own parts,
// and whether a file tool was aimed outside the project and the plugin. STOP in any part means:
// do not start the next session.
import { createHash } from 'node:crypto';
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
const every = { memory: true, skill: true, agent: true, mcp: true, hook: 'guard', plugin: false };
const none = { memory: false, skill: false, agent: false, mcp: false, hook: null, plugin: false };
const ARMS = {
  base: none, memory: { ...none, memory: true }, skill: { ...none, skill: true }, agent: { ...none, agent: true },
  mcp: { ...none, mcp: true }, hook: { ...none, hook: 'guard' }, note: { ...none, hook: 'note' }, plugin: { ...none, plugin: true },
  all: every, work: every, context: every, slash: every, safe: every, upfront: { ...none, mcp: true },
};
const want = ARMS[arm] ?? none;
const kitDir = process.env.KIT_DIR ?? join(dirname(dir), 'ship-kit');
const same = (a, b) => String(a ?? '').replaceAll('\\', '/').replace(/\/$/, '').toLowerCase() === String(b ?? '').replaceAll('\\', '/').replace(/\/$/, '').toLowerCase();
const yes = (value) => (value ? 'yes' : 'no');

// The built-in subagents on the official sub-agents page, and the skills Claude Code ships
// (the official commands page, read 2026-10-10, plus the ones earlier videos' records showed).
const BUILT_IN = new Set(['Explore', 'Plan', 'general-purpose', 'claude', 'statusline-setup', 'claude-code-guide']);
const SHIPPED = new Set(['deep-research', 'design', 'design-sync', 'dataviz', 'artifact-diagramming',
  'artifact-capabilities', 'update-config', 'verify', 'debug', 'code-review', 'simplify', 'batch',
  'fewer-permission-prompts', 'doctor', 'loop', 'schedule', 'claude-api', 'workflow-authoring', 'run',
  'run-skill-generator', 'plugin-authoring', 'claude-in-chrome', 'slides', 'init', 'security-review', 'keybindings-help']);
const OUR_SKILL = /^(ship-kit:)?release-prep$/;
const OUR_AGENT = /^(ship-kit:)?log-scout$/;
const OUR_TOOL = /^mcp__gear__(find_gear|low_stock)$/;
const names = (list) => (list ?? []).map((each) => (typeof each === 'string' ? each : each.name));

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
const kit = plugins.filter((each) => each.name === 'ship-kit');
const skills = names(init.skills);
const agents = names(init.agents);
const commands = names(init.slash_commands);
const ourSkills = skills.filter((skill) => OUR_SKILL.test(skill));
const ourAgents = agents.filter((agent) => OUR_AGENT.test(agent));
const other = {
  plugins: plugins.length - own.length - kit.length,
  skills: skills.filter((skill) => !SHIPPED.has(skill) && !OUR_SKILL.test(skill)).length,
  agents: agents.filter((agent) => !BUILT_IN.has(agent) && !OUR_AGENT.test(agent)).length,
  servers: servers.length - gear.length,
  tools: mcpTools.length - ourTools.length,
};
const errors = init.plugin_errors ?? [];

// The logging hook's record.
const seen = (read(join(dir, `${name}.seen.txt`)) ?? '').split('\n').filter(Boolean);
const loads = seen.filter((line) => line.startsWith('InstructionsLoaded'));
const ownMemory = loads.filter((line) => /\sCLAUDE\.md$/.test(line)).length;
const outsideLoads = loads.filter((line) => line.includes('(outside the project')).length;
// File tools aimed outside the project and the plugin, counted twice over: from the logging
// hook's record (it writes "(outside the project...)" and stops the call with BLOCKED), and from
// the stream's own tool calls, so the count does not rest on the hook having run.
const seenCalls = seen.filter((line) => /^(PreToolUse|PermissionRequest) /.test(line));
const seenOutside = seenCalls.filter((line) => line.includes('(outside the project') || line.includes('BLOCKED'));
const seenBlocked = seenCalls.filter((line) => line.includes('BLOCKED')).length;
const seenTemp = seenOutside.filter((line) => line.includes('in the temp folder')).length;
const kinds = {};
for (const line of seen) kinds[line.split(' ')[0]] = (kinds[line.split(' ')[0]] ?? 0) + 1;

// What the session used.
const calls = [];
const done = new Set();
for (const line of lines) {
  if (line.type !== 'assistant') continue;
  for (const block of line.message?.content ?? []) {
    if (block.type !== 'tool_use' || done.has(block.id)) continue;
    done.add(block.id);
    calls.push({ tool: block.name, input: block.input ?? {}, under: Boolean(line.parent_tool_use_id) });
  }
}
const main = calls.filter((call) => !call.under);
const FILE_TOOLS = new Set(['Read', 'Edit', 'Write', 'NotebookEdit', 'Glob', 'Grep']);
const cwd = String(init.cwd ?? '');
const native = (path) => (process.platform === 'win32' ? String(path).replace(/^\/([A-Za-z])\//, '$1:/') : String(path));
const within = (base, path) => { if (!base) return false; const rel = relative(base, path); return !rel.startsWith('..') && !isAbsolute(rel); };
const outsidePath = (path) => {
  if (String(path).startsWith('~')) return true;
  const full = resolve(cwd, native(path));
  return !(within(cwd, full) || within(kitDir, full));
};
const ROOTED = /^([A-Za-z]:|[\\/]|~|\.\.([\\/]|$))/;
const aimedOutside = (call) => {
  if (!cwd || !FILE_TOOLS.has(call.tool)) return false;
  const path = call.input.file_path ?? call.input.notebook_path ?? call.input.path;
  if (path && outsidePath(path)) return true;
  const glob = call.tool === 'Glob' ? call.input.pattern : call.tool === 'Grep' ? call.input.glob : null;
  return Boolean(glob) && ROOTED.test(String(glob)) && outsidePath(String(glob).split(/[*?[{]/)[0] || '.');
};
const streamOutside = calls.filter(aimedOutside).length;
const skillCalls = main.filter((call) => call.tool === 'Skill').map((call) => String(call.input.skill ?? call.input.name ?? '').replace(/^\//, ''));
const agentCalls = main.filter((call) => call.tool === 'Agent' || call.tool === 'Task').map((call) => String(call.input.subagent_type ?? ''));
const gearCalls = main.filter((call) => OUR_TOOL.test(call.tool));
const otherMcpCalls = calls.filter((call) => String(call.tool).startsWith('mcp__') && !OUR_TOOL.test(call.tool)).length;
const searches = main.filter((call) => call.tool === 'ToolSearch').length;
const byTool = {};
for (const call of calls) {
  const label = String(call.tool).startsWith('mcp__') ? (OUR_TOOL.test(call.tool) ? call.tool : 'mcp__(a server)') : call.tool;
  byTool[label] = (byTool[label] ?? 0) + 1;
}
const guard = (read(join(dir, `${name}.guard.txt`)) ?? '').split('\n').filter(Boolean);
const note = (read(join(dir, `${name}.note.txt`)) ?? '').split('\n').filter(Boolean);
const requests = (read(join(dir, `${name}.lab`, 'server', 'requests.txt')) ?? '').split('\n').filter(Boolean);
const asked = (word) => requests.filter((line) => line.includes(` ${word}`)).length;
const startHooks = lines.filter((line) => line.type === 'system' && line.subtype === 'hook_response' && /^SessionStart/.test(String(line.hook_name ?? line.hook_event ?? '')));
const results = lines.filter((line) => line.type === 'result');

console.log(`-- after.mjs ${name} | arm ${arm} | Claude Code ${init.claude_code_version ?? '?'} | init events ${inits.length}`);
console.log(`   init model: ${init.model} | permissionMode: ${init.permissionMode}`);
for (const [label, count] of [...found].sort()) console.log(`   ${label} (x${count})`);
console.log(`   built-in tools (${builtin.length}): ${builtin.join(' ') || 'none'}`);
console.log(`   mcp_servers: ${servers.length} = gear ${gear.length}${gear.length ? ` (${gear.map((server) => server.status).join(', ')})` : ''} + any other ${other.servers} | MCP tools: ${mcpTools.length} = gear's ${ourTools.length}${ourTools.length ? ` (${ourTools.join(', ')})` : ''} + any other ${other.tools}`);
console.log(`   plugins: ${plugins.length} = cc-plugin-* ${own.length} + ship-kit ${kit.length}${kit.length ? ` (its path is the seed's plugin folder: ${same(kit[0].path, kitDir) ? 'yes' : 'NO'})` : ''} + any other ${other.plugins} | plugin_errors: ${errors.length}`);
console.log(`   skills: ${skills.length} = the seed's ${ourSkills.length} (${ourSkills.join(', ') || 'none'}) + shipped with Claude Code ${skills.filter((skill) => SHIPPED.has(skill)).length} + any other ${other.skills}`);
console.log(`   agents: ${agents.length} = the seed's ${ourAgents.length} (${ourAgents.join(', ') || 'none'}) + built in ${agents.filter((agent) => BUILT_IN.has(agent)).length} + any other ${other.agents}`);
console.log(`   slash commands: ${commands.length}, of them the seed's: ${commands.filter((command) => /release-prep$/.test(command)).join(', ') || 'none'}`);
console.log(`   init keys: ${Object.keys(init).sort().join(' ')}`);
console.log(`   logging hook's record: ${seen.length} lines | ${Object.entries(kinds).map(([kind, count]) => `${kind} ${count}`).join(', ') || 'none'}`);
console.log(`   instruction files loaded: ${loads.length} | the project's own CLAUDE.md ${ownMemory} | outside the project ${outsideLoads} | any other inside the project ${loads.length - ownMemory - outsideLoads}`);
console.log(`   tool calls in the stream: ${calls.length}${calls.length ? ` (${Object.entries(byTool).map(([tool, count]) => `${tool} ${count}`).join(', ')})` : ''} | under Agent calls ${calls.filter((call) => call.under).length}`);
console.log(`   parts used: Skill calls ${skillCalls.length}${skillCalls.length ? ` (${skillCalls.map((skill) => (OUR_SKILL.test(skill) || SHIPPED.has(skill) ? skill : '(another skill)')).join(', ')})` : ''} | Agent calls ${agentCalls.length}${agentCalls.length ? ` (${agentCalls.map((type) => (OUR_AGENT.test(type) || BUILT_IN.has(type) ? type : type ? '(another agent)' : '(no type)')).join(', ')})` : ''} | ToolSearch calls ${searches} | gear tool calls ${gearCalls.length}${gearCalls.length ? ` (${gearCalls.map((call) => `${call.tool.replace('mcp__gear__', '')} ${JSON.stringify(call.input)}`).join(', ')})` : ''} | other MCP calls ${otherMcpCalls}`);
console.log(`   the MCP server's own record: ${requests.length} lines | initialize ${asked('initialize')} | tools/list ${asked('tools/list')} | tools/call ${asked('tools/call')}`);
console.log(`   the guard's record: ${guard.length} lines | pass ${guard.filter((line) => line.includes('-> pass')).length}, block ${guard.filter((line) => line.includes('-> block')).length} | Edit and Write calls in the stream ${calls.filter((call) => call.tool === 'Edit' || call.tool === 'Write').length}`);
console.log(`   the note hook's record: ${note.length} lines | SessionStart hook responses in the stream: ${startHooks.length}${startHooks.length ? ` (stdout ${startHooks.map((line) => String(line.stdout ?? '').length).join(', ')} chars)` : ''}`);
console.log(`   file-tool calls aimed outside the project and the plugin: in the stream ${cwd ? streamOutside : '(no cwd on the init event: not counted)'} | in the logging hook's record ${seenOutside.length} (stopped by it: ${seenBlocked}; in the temp folder: ${seenTemp})`);
console.log(`   result lines: ${results.map((result) => `${result.subtype} (${result.num_turns} turns, is_error ${result.is_error ?? '-'})`).join(' | ') || 'none'} | permission_denials ${results.flatMap((result) => result.permission_denials ?? []).length}`);
const subtypes = {};
for (const line of lines) if (line.type === 'system') subtypes[line.subtype] = (subtypes[line.subtype] ?? 0) + 1;
console.log(`   system lines by subtype: ${Object.entries(subtypes).map(([subtype, count]) => `${subtype} ${count}`).join(', ') || 'none'}`);
if (arm === 'work' || arm === 'slash') {
  // What the working session left behind. Recorded as yes or no; none of it is scored, and no
  // line of a reply is printed here.
  const lab = join(dir, `${name}.lab`);
  const text = (path) => read(join(lab, path)) ?? '';
  let version = '(package.json does not parse)';
  try { version = JSON.parse(text('package.json')).version; } catch { /* keep the note */ }
  const note = text('releases/v1.2.1.md').split('\n').map((line) => line.trimEnd());
  const heads = ['## 這一版改了什麼', '## 升級要注意', '## 怎麼確認'].filter((heading) => note.includes(heading)).length;
  const replies = results.map((result) => (typeof result.result === 'string' ? result.result : ''));
  const said = replies.join('\n');
  const last = replies.map((reply) => reply.split('\n').map((line) => line.trim()).filter(Boolean).at(-1) ?? '');
  const test = existsSync(join(lab, 'src', 'fares.test.mjs')) ? createHash('sha256').update(readFileSync(join(lab, 'src', 'fares.test.mjs'))).digest('hex').slice(0, 16) : 'gone';
  console.log(`   the work itself (recorded, not scored): package.json version ${version} | README names v1.2.1 ${yes(/Latest release: v1\.2\.1/.test(text('README.md')))} | CHANGELOG has a v1.2.1 heading ${yes(/^## v1\.2\.1 \(/m.test(text('CHANGELOG.md')))} | releases/v1.2.1.md has ${heads} of 3 template headings`);
  console.log(`      replies name J2103 ${yes(said.includes('J2103'))}, J2204 ${yes(said.includes('J2204'))}, shelf D-07 ${yes(said.includes('D-07'))}, 37 ${yes(/(^|\D)37(\D|$)/.test(said))} | a reply's last line starts with 下一步 ${yes(last.some((line) => /^[\s>*_\`-]*下一步/.test(line)))}, with 未驗證 ${yes(last.some((line) => /^[\s>*_\`-]*未驗證/.test(line)))} | the existing test file is unchanged ${yes(test === '6aa2fe229839400c')}`);
}

const modelKeys = [...found.keys()];
const badModel = !modelKeys.length || modelKeys.some((key) => !/sonnet|haiku|synthetic/i.test(key));
// "manual" is the same mode under its other name (the official cli-reference page).
const badMode = !['default', 'manual'].includes(init.permissionMode);
// With tool search turned off (arm upfront) Claude Code drops ToolSearch from the list: the MCP
// video's record showed that. In that arm it may be there or not; everywhere else it must be.
const optional = arm === 'upfront' ? ['ToolSearch'] : [];
const wanted = ['Edit', 'Glob', 'Grep', 'Read', 'Skill', 'ToolSearch', 'Write'].filter((tool) => !optional.includes(tool));
const spawn = builtin.filter((tool) => tool === 'Agent' || tool === 'Task');
const rest = builtin.filter((tool) => tool !== 'Agent' && tool !== 'Task' && !optional.includes(tool)).sort();
const badTools = rest.join(' ') !== wanted.join(' ') || spawn.length === 0;
const shell = builtin.filter((tool) => /^(Bash|PowerShell)$/i.test(tool)).length;
const badOutside = streamOutside > 0 || seenOutside.length > 0;
const badOthers = Object.values(other).some((count) => count > 0) || otherMcpCalls > 0;
const badLoads = outsideLoads > 0 || (loads.length - ownMemory - outsideLoads) > 0 || (want.memory ? ownMemory < 1 : ownMemory > 0);
const part = [];
if (want.skill !== ourSkills.includes('release-prep')) part.push(`skill release-prep ${want.skill ? 'missing' : 'listed'}`);
if (want.agent !== ourAgents.includes('log-scout')) part.push(`agent log-scout ${want.agent ? 'missing' : 'listed'}`);
if (want.mcp !== (gear.length === 1)) part.push(`server gear ${want.mcp ? 'missing' : 'listed'}`);
if (want.mcp && gear.length === 1 && !['connected', 'pending'].includes(gear[0].status)) part.push(`server gear is ${gear[0].status}`);
if (want.plugin !== (kit.length === 1)) part.push(`plugin ship-kit ${want.plugin ? 'missing' : 'listed'}`);
if (want.plugin && kit.length === 1 && (!same(kit[0].path, kitDir) || errors.length)) part.push('plugin ship-kit comes from another folder or has a load error');
if (want.plugin !== ourSkills.includes('ship-kit:release-prep')) part.push(`skill ship-kit:release-prep ${want.plugin ? 'missing' : 'listed'}`);
if (want.plugin !== ourAgents.includes('ship-kit:log-scout')) part.push(`agent ship-kit:log-scout ${want.plugin ? 'missing' : 'listed'}`);
if ((want.hook === 'note') !== (note.length > 0)) part.push(`note hook ${want.hook === 'note' ? 'left no record' : 'left a record'}`);
if (want.hook !== 'guard' && guard.length > 0) part.push('the guard left a record in an arm without it');
if (arm === 'safe') part.length = 0; // --safe-mode turns the parts off on purpose: read the lists above
console.log(`   verdict: ${badModel ? 'STOP: a model that is not sonnet or haiku is named, or none is' : 'only sonnet (or haiku) named'}`
  + ` | ${badMode ? 'STOP: the permission mode is not default' : `permission mode ${init.permissionMode}`}`
  + ` | ${shell ? 'STOP: Bash or PowerShell is among the built-in tools' : badTools ? `LOOK: the built-in tools are not ${wanted.join(' ')} plus Agent or Task` : `the expected built-in tools${optional.length ? ` (ToolSearch listed: ${builtin.includes('ToolSearch') ? 'yes' : 'no'})` : ''}`}`
  + ` | ${badOthers ? 'STOP: a plugin, skill, agent, MCP server or MCP tool that is not the seed\'s or Claude Code\'s own is listed or was called (counts above; names not printed)' : 'nothing listed or called that is not the seed\'s or Claude Code\'s own'}`
  + ` | ${badLoads ? 'STOP: the instruction files loaded are not what this arm holds (counts above; paths not printed)' : `instruction files as this arm holds them (${ownMemory})`}`
  + ` | ${part.length ? `STOP: ${part.join('; ')}` : `the parts of arm ${arm} and no other`}`
  + ` | ${badOutside ? 'STOP: a file tool was aimed outside the project and the plugin (counts above; paths not printed)' : 'no file tool aimed outside the project and the plugin'}`);
