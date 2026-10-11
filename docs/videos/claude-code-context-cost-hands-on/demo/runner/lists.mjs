// Runner: the init lists of every session, split three ways (Claude Code's own / the seed's /
// any other), and which of Claude Code's own shipped skills and slash commands differ between
// sessions. Only names on the seed's list of shipped skills, built-in agents and the seed's own
// parts are ever printed; anything else is a count.
//   node lists.mjs <logs> <name> [<name> ...]
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const [logs, ...names] = process.argv.slice(2);
const BUILT_IN = new Set(['Explore', 'Plan', 'general-purpose', 'claude', 'statusline-setup', 'claude-code-guide']);
const SHIPPED = new Set(['deep-research', 'design', 'design-sync', 'dataviz', 'artifact-diagramming',
  'artifact-capabilities', 'update-config', 'verify', 'debug', 'code-review', 'simplify', 'batch',
  'fewer-permission-prompts', 'doctor', 'loop', 'schedule', 'claude-api', 'workflow-authoring', 'run',
  'run-skill-generator', 'plugin-authoring', 'claude-in-chrome', 'slides', 'init', 'security-review', 'keybindings-help']);
const OUR_SKILL = /^(ship-kit:)?release-prep$/;
const OUR_AGENT = /^(ship-kit:)?log-scout$/;
const namesOf = (list) => (list ?? []).map((each) => (typeof each === 'string' ? each : each.name));
const rows = names.map((name) => {
  const init = readFileSync(join(logs, `${name}.stream.jsonl`), 'utf8').split('\n').filter(Boolean).flatMap((line) => {
    try { return [JSON.parse(line)]; } catch { return []; }
  }).find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
  const skills = namesOf(init.skills);
  const agents = namesOf(init.agents);
  const plugins = namesOf(init.plugins);
  const tools = init.tools ?? [];
  const servers = namesOf(init.mcp_servers);
  const commands = namesOf(init.slash_commands);
  return { name, skills, agents, plugins, tools, servers, commands };
});
console.log('name | built-in tools | MCP servers gear/other | MCP tools gear/other | plugins own/seed/other | skills shipped/seed/other | agents built-in/seed/other | slash commands');
for (const r of rows) {
  const mcp = r.tools.filter((tool) => tool.startsWith('mcp__'));
  const gearTools = mcp.filter((tool) => /^mcp__gear__(find_gear|low_stock)$/.test(tool)).length;
  const own = r.plugins.filter((p) => String(p).startsWith('cc-plugin-')).length;
  const kit = r.plugins.filter((p) => p === 'ship-kit').length;
  const shipped = r.skills.filter((s) => SHIPPED.has(s)).length;
  const ourS = r.skills.filter((s) => OUR_SKILL.test(s)).length;
  const builtin = r.agents.filter((a) => BUILT_IN.has(a)).length;
  const ourA = r.agents.filter((a) => OUR_AGENT.test(a)).length;
  const gear = r.servers.filter((s) => s === 'gear').length;
  console.log(`${r.name} | ${r.tools.length - mcp.length} | ${gear}/${r.servers.length - gear} | ${gearTools}/${mcp.length - gearTools} | ${own}/${kit}/${r.plugins.length - own - kit} | ${shipped}/${ourS}/${r.skills.length - shipped - ourS} | ${builtin}/${ourA}/${r.agents.length - builtin - ourA} | ${r.commands.length}`);
}
// Shipped skills that are not in every session.
const all = new Set(rows.flatMap((r) => r.skills.filter((s) => SHIPPED.has(s))));
const uneven = [...all].filter((skill) => !rows.every((r) => r.skills.includes(skill)));
console.log(`shipped skills listed in some sessions and not in others: ${uneven.length}`);
for (const skill of uneven) console.log(`   ${skill}: listed in ${rows.filter((r) => r.skills.includes(skill)).map((r) => r.name).join(' ') || 'none'} | not in ${rows.filter((r) => !r.skills.includes(skill)).map((r) => r.name).join(' ') || 'none'}`);
// Slash commands that are not in every session: names only when they are a shipped skill or the seed's.
const allC = new Set(rows.flatMap((r) => r.commands));
const unevenC = [...allC].filter((c) => !rows.every((r) => r.commands.includes(c)));
console.log(`slash commands listed in some sessions and not in others: ${unevenC.length}${unevenC.length ? ` (${unevenC.map((c) => (SHIPPED.has(c) || /(^|:)release-prep$/.test(c) ? c : '(not on the shipped list: name not printed)')).join(', ')})` : ''}`);
