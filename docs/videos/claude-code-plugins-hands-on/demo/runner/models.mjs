// After every session: which models the stream names, and what the init event lists, as a verdict.
// Usage: node models.mjs <logs>/<name>.stream.jsonl      (KIT_DIR may name the plugin folder)
// Only the seed's own names are printed (ship-kit, release-prep, log-scout) and what Claude Code
// ships; any other plugin, skill, agent or MCP server is a count, never a name or a path.
import { existsSync, readFileSync } from 'node:fs';
import { basename, dirname, join } from 'node:path';

const file = process.argv[2];
const dir = dirname(file);
const name = basename(file).replace(/\.stream\.jsonl$/, '');
const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap((line) => {
  try { return [JSON.parse(line)]; } catch { return []; }
}).filter((line) => line.type !== 'rate_limit_event');
const record = join(dir, `${name}.session.txt`);
const arm = ((existsSync(record) ? readFileSync(record, 'utf8') : '').match(/^# \S+ \| arm (\S+)/) ?? [])[1] ?? '?';
const loads = !['bare', 'origin'].includes(arm);
const kitDir = process.env.KIT_DIR ?? join(dirname(dir), 'ship-kit');
const same = (a, b) => String(a ?? '').replaceAll('\\', '/').replace(/\/$/, '').toLowerCase() === String(b ?? '').replaceAll('\\', '/').replace(/\/$/, '').toLowerCase();

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

const BUILT_IN = new Set(['Explore', 'Plan', 'general-purpose', 'claude', 'statusline-setup', 'claude-code-guide']);
const SHIPPED = new Set(['deep-research', 'design', 'design-sync', 'dataviz', 'artifact-diagramming',
  'artifact-capabilities', 'update-config', 'verify', 'debug', 'code-review', 'simplify', 'batch',
  'fewer-permission-prompts', 'doctor', 'loop', 'schedule', 'claude-api', 'workflow-authoring', 'run',
  'run-skill-generator', 'plugin-authoring', 'claude-in-chrome', 'slides', 'init', 'security-review', 'keybindings-help']);
const names = (list) => (list ?? []).map((each) => (typeof each === 'string' ? each : each.name));
const inits = lines.filter((line) => line.type === 'system' && line.subtype === 'init');
const init = inits[0] ?? {};
const tools = init.tools ?? [];
const builtin = tools.filter((tool) => !String(tool).startsWith('mcp__'));
const plugins = (init.plugins ?? []).map((each) => (typeof each === 'string' ? { name: each } : each));
const own = plugins.filter((each) => String(each.name).startsWith('cc-plugin-'));
const ours = plugins.filter((each) => each.name === 'ship-kit');
const others = plugins.length - own.length - ours.length;
const skills = names(init.skills);
const agents = names(init.agents);
const ourSkills = skills.filter((skill) => /^(ship-kit:)?release-prep$/.test(skill));
const ourAgents = agents.filter((agent) => /^(ship-kit:)?log-scout$/.test(agent));
const otherSkills = skills.filter((skill) => !SHIPPED.has(skill) && !ourSkills.includes(skill)).length;
const otherAgents = agents.filter((agent) => !BUILT_IN.has(agent) && !ourAgents.includes(agent)).length;
const errors = init.plugin_errors ?? [];

console.log(`-- models.mjs ${name} | arm ${arm}`);
console.log(`   init model: ${init.model} | permissionMode: ${init.permissionMode} | apiKeySource: ${init.apiKeySource} | init events: ${inits.length}`);
for (const [label, count] of [...found].sort()) console.log(`   ${label} (x${count})`);
console.log(`   mcp_servers: ${(init.mcp_servers ?? []).length} | mcp tools: ${tools.length - builtin.length} | built-in tools: ${builtin.join(' ') || 'none'}`);
console.log(`   plugins: ${plugins.length} = cc-plugin-* ${own.length} + ship-kit ${ours.length}${ours.length ? ` (path is the seed's plugin folder: ${same(ours[0].path, kitDir) ? 'yes' : 'NO'})` : ''} + any other ${others} | plugin_errors: ${errors.length}`);
console.log(`   skills: ${skills.length} = the seed's ${ourSkills.length} (${ourSkills.join(', ') || 'none'}) + shipped + any other ${otherSkills}`);
console.log(`   agents: ${agents.length} = the seed's ${ourAgents.length} (${ourAgents.join(', ') || 'none'}) + built in + any other ${otherAgents} | slash_commands: ${(init.slash_commands ?? []).length}`);

const modelsNamed = [...found.keys()];
const badModel = modelsNamed.some((key) => !/sonnet|haiku|synthetic/i.test(key));
const badMcp = (init.mcp_servers ?? []).length > 0 || tools.length !== builtin.length;
const wanted = ['Edit', 'Glob', 'Grep', 'Read', 'Skill', 'Write'];
const spawn = builtin.filter((tool) => tool === 'Agent' || tool === 'Task');
const rest = builtin.filter((tool) => tool !== 'Agent' && tool !== 'Task').sort();
const badTools = rest.join(' ') !== wanted.join(' ') || spawn.length === 0;
const badMode = init.permissionMode !== 'default';
const badOthers = others > 0 || otherSkills > 0 || otherAgents > 0;
const badKit = loads ? ours.length !== 1 || !same(ours[0].path, kitDir) || errors.length > 0 : ours.length !== 0;
console.log(`   verdict: ${badModel ? 'STOP: a model that is not sonnet or haiku is named' : 'only sonnet (or haiku) named'}`
  + ` | ${badMcp ? 'STOP: an MCP server or tool is on the init line' : 'no MCP server or tool'}`
  + ` | ${badTools ? 'LOOK: the built-in tools are not Edit Glob Grep Read Skill Write plus Agent or Task' : 'the expected built-in tools'}`
  + ` | ${badMode ? 'STOP: the permission mode is not default' : 'permission mode default'}`
  + ` | ${badOthers ? 'STOP: a plugin, skill or agent that is not the seed\'s or Claude Code\'s own is listed (counts above; names not printed)' : 'nothing listed that is not the seed\'s or Claude Code\'s own'}`
  + ` | ${badKit ? (loads ? 'STOP: this arm loads ship-kit, and it is missing, comes from another folder, or has a load error' : 'STOP: this arm loads no plugin, and ship-kit is listed') : (loads ? 'ship-kit loaded from the seed\'s folder, no load error' : 'no ship-kit, as this arm expects')}`);
