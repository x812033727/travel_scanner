// After every session: which models the stream names, and what the init event lists, as counts.
// Usage: node models.mjs <logs>/<name>.stream.jsonl
// No MCP server, tool, plugin, skill or agent is named; anything that is not Claude Code's own is a count.
import { readFileSync } from 'node:fs';

const file = process.argv[2];
const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap((line) => {
  try { return [JSON.parse(line)]; } catch { return []; }
});
const found = new Map();
const walk = (value, key) => {
  if (Array.isArray(value)) { for (const each of value) walk(each, key); return; }
  if (value && typeof value === 'object') {
    for (const [k, v] of Object.entries(value)) {
      if (k === 'modelUsage' && v && typeof v === 'object') {
        for (const name of Object.keys(v)) found.set(`modelUsage key: ${name}`, (found.get(`modelUsage key: ${name}`) ?? 0) + 1);
        continue;
      }
      walk(v, k);
    }
    return;
  }
  if (typeof value === 'string' && key && /^model$/i.test(key)) {
    const label = `${key}: ${value}`;
    found.set(label, (found.get(label) ?? 0) + 1);
  }
};
for (const line of lines) {
  if (line.type === 'rate_limit_event') continue;
  walk(line, null);
}
const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
const tools = init.tools ?? [];
const WANTED = ['Bash', 'Edit', 'Glob', 'Grep', 'Read', 'Write'];
const builtin = tools.filter((tool) => !String(tool).startsWith('mcp__'));
const types = {};
for (const line of lines) types[line.type] = (types[line.type] ?? 0) + 1;
console.log(`-- models.mjs ${file.split(/[\\/]/).pop()}`);
console.log(`   init model: ${init.model} | permissionMode: ${init.permissionMode} | apiKeySource: ${init.apiKeySource} | init events: ${lines.filter((l) => l.type === 'system' && l.subtype === 'init').length}`);
for (const [label, count] of [...found].sort()) console.log(`   ${label} (x${count})`);
console.log(`   mcp_servers: ${(init.mcp_servers ?? []).length} | mcp tools: ${tools.length - builtin.length} | built-in tools: ${builtin.join(' ') || 'none'}`);
console.log(`   agents: ${(init.agents ?? []).length} | skills: ${(init.skills ?? []).length} | plugins: ${(init.plugins ?? []).length} | slash_commands: ${(init.slash_commands ?? []).length}`);
console.log(`   stream line types: ${Object.entries(types).map(([t, c]) => `${t} ${c}`).join(', ')}`);
const names = [...found.keys()];
const badModel = names.some((k) => !/sonnet|haiku|synthetic/i.test(k));
const badMcp = (init.mcp_servers ?? []).length > 0 || tools.length !== builtin.length;
const badTools = [...builtin].sort().join(' ') !== WANTED.join(' ');
const badMode = init.permissionMode !== 'default';
console.log(`   verdict: ${badModel ? 'STOP: a model that is not sonnet or haiku is named' : 'only sonnet (or haiku) named'} | ${badMcp ? 'STOP: an MCP server or tool is on the init line' : 'no MCP server or tool on the init line'} | ${badTools ? 'LOOK: the built-in tools are not exactly Bash Edit Glob Grep Read Write' : 'the six built-in tools, no other'} | ${badMode ? 'STOP: the permission mode is not default' : 'permission mode default'}`);
