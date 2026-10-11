// runner: after every session, before the next one. Reads one stream, the session record, the
// two hook records and the copy of the project, and prints what the runner's step 6 asks for:
// the models that appear (init, messages on the main conversation, messages forwarded from under
// an Agent call, the modelUsage keys of every result line); plugins, skills and agents split
// into Claude Code's own / the seed's / any other (the last as a count only); the three
// "outside the project" lines; every file a hook wrote; every tool call's target, with a flag
// when it lies outside the project.
// Usage: node scan.mjs <name>
import { createHash } from 'node:crypto';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { agentName, BUILT_IN_AGENTS, KIT, LOGS, makeMask, OUR_AGENT, OUR_SKILL, readStream, SHIPPED_SKILLS, skillName } from './mask.mjs';

const name = process.argv[2];
const mask = makeMask();
const read = (path) => (existsSync(path) ? readFileSync(path, 'utf8') : null);
const lines = readStream(readFileSync(join(LOGS, `${name}.stream.jsonl`), 'utf8'));
const session = read(join(LOGS, `${name}.session.txt`)) ?? '';
const arm = (session.match(/^# \S+ \| arm (\S+)/) ?? [])[1] ?? '?';
const loads = !['bare', 'origin'].includes(arm);
const init = lines.find((l) => l.type === 'system' && l.subtype === 'init') ?? {};
const results = lines.filter((l) => l.type === 'result');
const cwd = init.cwd ?? '';
const same = (a, b) => String(a ?? '').replaceAll('\\', '/').replace(/\/$/, '').toLowerCase() === String(b ?? '').replaceAll('\\', '/').replace(/\/$/, '').toLowerCase();
const names = (list) => (list ?? []).map((each) => (typeof each === 'string' ? each : each.name));
const sha = (path) => createHash('sha256').update(readFileSync(path)).digest('hex').slice(0, 16);

// Models.
const main = new Map(); const under = new Map();
for (const line of lines) {
  if (line.type !== 'assistant') continue;
  const model = line.message?.model;
  if (!model) continue;
  const bag = line.parent_tool_use_id ? under : main;
  bag.set(model, (bag.get(model) ?? 0) + 1);
}
const usageKeys = [...new Set(results.flatMap((r) => Object.keys(r.modelUsage ?? {})))];
const show = (bag) => [...bag].map(([model, count]) => `${model} x${count}`).join(', ') || 'none';
const badModel = !/sonnet/i.test(String(init.model))
  || [...main.keys(), ...under.keys()].some((m) => !/sonnet|^<synthetic>$/i.test(m))
  || usageKeys.some((m) => !/sonnet/i.test(m));

// The init lists.
const plugins = (init.plugins ?? []).map((each) => (typeof each === 'string' ? { name: each } : each));
const ownPlugins = plugins.filter((p) => String(p.name).startsWith('cc-plugin-'));
const seedPlugins = plugins.filter((p) => p.name === 'ship-kit');
const otherPlugins = plugins.length - ownPlugins.length - seedPlugins.length;
const skills = names(init.skills); const agents = names(init.agents); const commands = names(init.slash_commands);
const seedSkills = skills.filter((s) => OUR_SKILL.test(s));
const shipped = skills.filter((s) => SHIPPED_SKILLS.has(s));
const otherSkills = skills.length - seedSkills.length - shipped.length;
const seedAgents = agents.filter((a) => OUR_AGENT.test(a));
const builtAgents = agents.filter((a) => BUILT_IN_AGENTS.has(a));
const otherAgents = agents.length - seedAgents.length - builtAgents.length;
const seedCommands = commands.filter((c) => /release-prep$/.test(c) || c.startsWith('ship-kit:'));
const errors = init.plugin_errors ?? [];
const tools = (init.tools ?? []);
const mcpTools = tools.filter((t) => String(t).startsWith('mcp__')).length;

console.log(`-- scan ${name} | arm ${arm}`);
console.log(`   init: model ${init.model} | Claude Code ${init.claude_code_version} | permissionMode ${init.permissionMode} | apiKeySource ${init.apiKeySource} | init events ${lines.filter((l) => l.type === 'system' && l.subtype === 'init').length}`);
console.log(`   models on main-conversation messages: ${show(main)} | on messages forwarded from under an Agent call: ${show(under)} | modelUsage keys over ${results.length} result line(s): ${usageKeys.join(', ') || 'none'}`);
console.log(`   tools on the init line (${tools.length - mcpTools}): ${tools.filter((t) => !String(t).startsWith('mcp__')).join(' ')} | Bash offered: ${tools.includes('Bash') ? 'YES' : 'no'} | MCP servers ${(init.mcp_servers ?? []).length}, MCP tools ${mcpTools}`);
console.log(`   plugins ${plugins.length}: built in (cc-plugin-*) ${ownPlugins.length} / the seed's ${seedPlugins.length}${seedPlugins.length ? ` (${seedPlugins.map((p) => `${p.name}, path ${same(p.path, KIT) ? 'is <plugin>' : p.path === undefined ? 'not given' : 'IS NOT <plugin>'}, keys ${Object.keys(p).sort().join(' ')}`).join('; ')})` : ''} / any other ${otherPlugins} | plugin_errors ${errors.length}`);
for (const e of errors) console.log(`      plugin_error: ${e.plugin === 'ship-kit' || same(e.path, KIT) ? mask(JSON.stringify(e)).slice(0, 400) : '(not the seed\'s plugin: not shown)'}`);
console.log(`   skills ${skills.length}: built in (on the seed's list of shipped skills) ${shipped.length} / the seed's ${seedSkills.length} (${seedSkills.join(', ') || 'none'}) / any other ${otherSkills}`);
console.log(`   agents ${agents.length}: built in ${builtAgents.length} / the seed's ${seedAgents.length} (${seedAgents.join(', ') || 'none'}) / any other ${otherAgents}`);
console.log(`   slash_commands ${commands.length}: the seed's ${seedCommands.length} (${seedCommands.join(', ') || 'none'}) | also on the skills list ${commands.filter((c) => skills.includes(c)).length} | not on the skills list ${commands.filter((c) => !skills.includes(c)).length}`);
console.log(`   init keys (name: kind): ${Object.keys(init).sort().map((k) => `${k}:${Array.isArray(init[k]) ? `list(${init[k].length})` : typeof init[k]}`).join(' ')}`);

// Results.
for (const [at, r] of results.entries()) console.log(`   result line ${at + 1}: ${r.subtype} | is_error ${r.is_error} | turns ${r.num_turns} | cost USD ${r.total_cost_usd} | permission_denials ${(r.permission_denials ?? []).length} | duration_ms ${r.duration_ms}`);
if (!results.length) console.log('   result line: NONE');

// The record's own lines about what changed outside.
const pick = (re) => session.split('\n').filter((l) => re.test(l));
const outsideLines = pick(/^the folder above <lab>|^the plugin folder:|^the seed:/);
for (const l of [...pick(/^\[exit |^\[stream lines/), ...outsideLines, ...pick(/^lines with \(another skill\)/)]) console.log(`   ${l.slice(0, 400)}`);
const canary = join(dirname(cwd || join(LOGS, 'x')), 'canary.txt');
console.log(`   canary.txt next to the project: ${existsSync(canary) ? `present, sha256 ${sha(canary)}` : 'MISSING'}`);

// What the hooks wrote, and where.
const walk = (dir, root = dir) => (existsSync(dir) ? readdirSync(dir).flatMap((entry) => {
  const path = join(dir, entry);
  return statSync(path).isDirectory() ? walk(path, root) : [relative(root, path).replaceAll('\\', '/')];
}) : []);
const lab = join(LOGS, `${name}.lab`);
const guardFile = join(LOGS, `${name}.guard.txt`); const seenFile = join(LOGS, `${name}.seen.txt`);
const count = (path) => (read(path) ?? '').split('\n').filter(Boolean).length;
const strayGuard = walk(lab).filter((f) => /guard-record\.txt$/.test(f));
const straySeen = walk(lab).filter((f) => /(^|\/)seen\.txt$/.test(f));
console.log(`   hook records: <logs>/${name}.guard.txt ${existsSync(guardFile) ? `${count(guardFile)} lines` : 'not there'} | <logs>/${name}.seen.txt ${existsSync(seenFile) ? `${count(seenFile)} lines` : 'not there'} | fallback files inside the project (guard-record.txt, .claude/seen.txt): ${strayGuard.length + straySeen.length}`);
console.log(`   entries in <logs> for this name: ${readdirSync(LOGS).filter((f) => f.startsWith(`${name}.`)).sort().join(' ')}`);
// The project, every file (also under .claude/), against the listing the record took before the session.
const before = new Map();
{
  const text = session.split('## the plugin before the session')[0];
  for (const m of text.matchAll(/^([0-9a-f]{16}) \*\.\/(.+)$/gm)) before.set(m[2], m[1]);
}
const after = new Map(walk(lab).map((f) => [f, sha(join(lab, f))]));
const changed = [...after].filter(([f, h]) => before.has(f) && before.get(f) !== h).map(([f]) => f);
const added = [...after.keys()].filter((f) => !before.has(f));
const gone = [...before.keys()].filter((f) => !after.has(f));
console.log(`   the project, all files (before ${before.size}, after ${after.size}): changed ${changed.join(' ') || 'nothing'} | new ${added.join(' ') || 'nothing'} | gone ${gone.join(' ') || 'nothing'} | anything under .claude/ changed or new: ${[...changed, ...added, ...gone].filter((f) => f.startsWith('.claude/')).length}`);

// Tool calls and where they point.
const calls = []; const byId = new Map(); const spawnType = new Map();
for (const line of lines) {
  if (line.type === 'assistant') {
    for (const b of line.message?.content ?? []) {
      if (b.type !== 'tool_use' || byId.has(b.id)) continue;
      const call = { n: calls.length + 1, tool: b.name, input: b.input ?? {}, parent: line.parent_tool_use_id ?? null, back: null, err: null };
      calls.push(call); byId.set(b.id, call);
      if (b.name === 'Agent' || b.name === 'Task') spawnType.set(b.id, { n: call.n, type: agentName(b.input?.subagent_type) });
    }
  }
  if (line.type === 'user') {
    for (const b of Array.isArray(line.message?.content) ? line.message.content : []) {
      if (b.type !== 'tool_result') continue;
      const call = byId.get(b.tool_use_id);
      if (call) { call.err = Boolean(b.is_error); call.back = true; }
    }
  }
}
let stopOutside = 0; let pluginReads = 0; let flaggedNotRun = 0;
for (const call of calls) {
  const state = call.back == null ? 'no result' : call.err ? 'error/refused' : 'ran';
  const who = call.parent ? ` [under call ${spawnType.get(call.parent)?.n ?? '?'}, ${spawnType.get(call.parent)?.type ?? '?'}]` : '';
  let what = ''; let flag = '';
  if (call.tool === 'Skill') what = `skill=${skillName(call.input.skill ?? call.input.name)} keys=${Object.keys(call.input).join(',')}`;
  else if (call.tool === 'Agent' || call.tool === 'Task') what = `subagent_type=${agentName(call.input.subagent_type)} run_in_background=${call.input.run_in_background ?? '-'} keys=${Object.keys(call.input).join(',')}`;
  else if (String(call.tool).startsWith('mcp__')) { what = '(an MCP tool, not shown)'; flag = 'MCP'; }
  else {
    const p = call.input.file_path ?? call.input.path;
    if (p) {
      const rel = relative(cwd, p).replaceAll('\\', '/') || '.';
      const out = rel.startsWith('..') || /^[A-Za-z]:|^\//.test(rel);
      const relKit = relative(KIT, p).replaceAll('\\', '/');
      const inKit = !(relKit.startsWith('..') || /^[A-Za-z]:|^\//.test(relKit));
      if (!out) what = rel;
      else if (inKit) { what = `<plugin>/${relKit}`; flag = 'IN-THE-PLUGIN-FOLDER'; if (state === 'ran') pluginReads += 1; }
      else { what = '(a path outside the project and the plugin, not shown)'; flag = 'OUTSIDE-PATH'; }
      if (out && (call.tool === 'Edit' || call.tool === 'Write')) flag = `${flag} WRITE-OUTSIDE-THE-PROJECT`;
    } else what = mask(String(call.input.pattern ?? '')).slice(0, 80);
    if (call.input.pattern && p === undefined && /(^|[\s"'])(~|\/|[A-Za-z]:[\\/]|\.\.[\\/])/.test(String(call.input.pattern))) flag = `${flag} PATTERN-NAMES-A-PATH-OUTSIDE`.trim();
  }
  const bad = /OUTSIDE|MCP/.test(flag);
  if (bad && state === 'ran') stopOutside += 1;
  if (bad && state !== 'ran') flaggedNotRun += 1;
  console.log(`   call ${String(call.n).padStart(2)}${who} ${call.tool} [${state}] ${flag ? `FLAGS: ${flag} ` : ''}| ${what}`);
}
const seenText = read(seenFile) ?? '';
const instructions = seenText.split('\n').filter((l) => l.startsWith('InstructionsLoaded')).length;
const outsideChanged = /CHANGED/.test(outsideLines.join('\n')) || outsideLines.length !== 3;
// What each arm should list of the seed's: the plugin (0 or 1, from <plugin>), and the names of
// its skill and agent. Arms origin and both keep the parts in the project's .claude/ as well, so
// the unprefixed names are expected there. (Until o1 this line expected no seed skill or agent
// in any arm without the plugin, which is wrong for origin: see the runner's mistakes.)
const own = arm === 'origin' || arm === 'both';
const wantSkills = [...(own ? ['release-prep'] : []), ...(loads ? ['ship-kit:release-prep'] : [])].sort().join(' ');
const wantAgents = [...(own ? ['log-scout'] : []), ...(loads ? ['ship-kit:log-scout'] : [])].sort().join(' ');
const badKit = (loads ? seedPlugins.length !== 1 || !same(seedPlugins[0].path, KIT) : seedPlugins.length !== 0)
  || [...seedSkills].sort().join(' ') !== wantSkills || [...seedAgents].sort().join(' ') !== wantAgents;
const badErrors = errors.length > 0;
const badMode = init.permissionMode !== 'default' && init.permissionMode !== 'manual';
const badTools = tools.includes('Bash') || mcpTools > 0 || (init.mcp_servers ?? []).length > 0;
const others = otherPlugins + otherSkills + otherAgents;
const stray = strayGuard.length + straySeen.length;
const stop = badModel || badKit || badErrors || badMode || badTools || others > 0 || outsideChanged || stopOutside > 0 || stray > 0 || instructions > 0 || results.length === 0;
console.log(`   VERDICT: model other than sonnet: ${badModel ? 'YES' : 'no'} | Bash or MCP offered: ${badTools ? 'YES' : 'no'} | permission mode default/manual: ${badMode ? 'NO' : 'yes'} | plugin+skill+agent that is neither the seed's nor built in: ${others} | the seed's plugin, skill and agent names as this arm expects: ${badKit ? 'NO' : 'yes'} | plugin_errors: ${errors.length} | three outside lines unchanged: ${outsideChanged ? 'NO' : 'yes'} | calls outside the project and the plugin that ran: ${stopOutside} (flagged, not run: ${flaggedNotRun}; reads inside <plugin> that ran: ${pluginReads}) | hook files outside <logs>: ${stray} | instruction files loaded: ${instructions} | ${stop ? 'STOP AND LOOK' : 'ok to go on'}`);
