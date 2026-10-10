// After every session: which models the stream names, and what the init event lists, as counts.
// Usage: node models.mjs <logs>/<name>.stream.jsonl
// Names only the seed's servers (gear, gear-more); anything else is a count.
import { readFileSync } from 'node:fs';

const file = process.argv[2];
const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap((line) => {
  try { return [JSON.parse(line)]; } catch { return []; }
});
const SEED = new Set(['gear', 'gear-more']);
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
  if (typeof value === 'string' && key && /model/i.test(key)) {
    const label = `${key}: ${value}`;
    found.set(label, (found.get(label) ?? 0) + 1);
  }
};
for (const line of lines) {
  if (line.type === 'rate_limit_event') continue;
  walk(line, null);
}
const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
const servers = init.mcp_servers ?? [];
const serverOf = (tool) => (String(tool).match(/^mcp__(.+?)__/) ?? [])[1];
const tools = init.tools ?? [];
const mcpTools = tools.filter((tool) => serverOf(tool));
const types = {};
for (const line of lines) types[line.type] = (types[line.type] ?? 0) + 1;
console.log(`-- models.mjs ${file.split(/[\\/]/).pop()}`);
console.log(`   init model: ${init.model} | apiKeySource: ${init.apiKeySource} | init events: ${lines.filter((l) => l.type === 'system' && l.subtype === 'init').length}`);
for (const [label, count] of [...found].sort()) console.log(`   ${label} (x${count})`);
console.log(`   mcp_servers: ${servers.length} | the seed's: ${servers.filter((s) => SEED.has(s.name)).map((s) => `${s.name}=${s.status}`).join(', ') || 'none'} | not the seed's: ${servers.filter((s) => !SEED.has(s.name)).length}`);
console.log(`   tools: ${tools.length} | built-in: ${tools.filter((t) => !serverOf(t)).join(' ') || 'none'} | mcp tools of the seed's servers: ${mcpTools.filter((t) => SEED.has(serverOf(t))).length} | mcp tools of any other server: ${mcpTools.filter((t) => !SEED.has(serverOf(t))).length}`);
console.log(`   agents: ${(init.agents ?? []).length} | skills: ${(init.skills ?? []).length} | plugins: ${(init.plugins ?? []).length} | slash_commands: ${(init.slash_commands ?? []).length} | memory_paths keys: ${init.memory_paths ? Object.keys(init.memory_paths).length : 'no key'}`);
console.log(`   init keys: ${Object.keys(init).sort().join(' ')}`);
console.log(`   stream line types: ${Object.entries(types).map(([t, c]) => `${t} ${c}`).join(', ')}`);
const names = [...found.keys()].join(' ');
const bad = /opus|fable/i.test(names) || [...found.keys()].some((k) => !/sonnet|haiku|synthetic/i.test(k));
console.log(`   verdict: ${bad ? 'STOP: a model that is not sonnet or haiku is named' : 'only sonnet (or haiku) named'} | ${servers.some((s) => !SEED.has(s.name)) || mcpTools.some((t) => !SEED.has(serverOf(t))) ? 'STOP: something that is not the seed\'s is on the init line' : 'nothing but the seed\'s MCP on the init line'}`);
