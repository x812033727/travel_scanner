// Reads what one headless session left behind and prints what this video counts.
//
//   node <seed>/tally.mjs <logs>/<name>.stream.jsonl [<logs>/<name>.stream.jsonl ...]
//
// Next to each stream it expects <name>.session.txt (for the arm), <name>.lab/ (the copy of the
// project session.sh takes when the session ends), <name>.seen.txt (the project's logging hook)
// and <name>.guard.txt (what the guard wrote). The plugin folder is KIT_DIR, or ship-kit next to
// the records folder.
//
// For each of the three parts it reports three things, fixed before any session ran:
//   listed   the init event names it (and under which name)
//   used     the stream holds the call (Skill, Agent) or the guard's own record holds a line
//   effect   the project's files or the subagent's report show what it did
//
// How one tool call is labelled:
//   ran               its tool result is not marked as an error
//   stopped by a hook marked as an error and the text says a hook stopped it
//   refused: asked    marked as an error, and the logging hook saw a PermissionRequest for it
//   refused: other    marked as an error, listed as denied or reading like a refusal, no request seen
//   ran, failed       marked as an error, none of the above
//   no result         the stream holds no tool result for it
//
// Only the seed's own names are printed: the plugin ship-kit, the skill release-prep, the agent
// log-scout, and what Claude Code ships. Any other plugin, skill, agent or MCP tool is a count.
// Paths are shown as <lab>, <plugin> or <home>; long ids are masked; rate-limit events are never read.
import { createHash } from 'node:crypto';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { homedir } from 'node:os';
import { basename, dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const truth = JSON.parse(readFileSync(join(seed, 'truth.json'), 'utf8'));
const PLUGIN = 'ship-kit';
const ARMS = {
  bare: { project: 'b', own: false, kit: false }, kit: { project: 'b', own: false, kit: true },
  origin: { project: 'a', own: true, kit: false }, both: { project: 'a', own: true, kit: true },
  guard: { project: 'b', own: false, kit: true }, stale: { project: 'b', own: false, kit: true },
  strict: { project: 'b', own: false, kit: true }, slash: { project: 'b', own: false, kit: true },
  short: { project: 'b', own: false, kit: true },
};
// The built-in subagents on the official sub-agents page, and the skills on the commands page.
const BUILT_IN = new Set(['Explore', 'Plan', 'general-purpose', 'claude', 'statusline-setup', 'claude-code-guide']);
const SHIPPED = new Set(['deep-research', 'design', 'design-sync', 'dataviz', 'artifact-diagramming',
  'artifact-capabilities', 'update-config', 'verify', 'debug', 'code-review', 'simplify', 'batch',
  'fewer-permission-prompts', 'doctor', 'loop', 'schedule', 'claude-api', 'workflow-authoring', 'run',
  'run-skill-generator', 'plugin-authoring', 'claude-in-chrome', 'slides', 'init', 'security-review', 'keybindings-help']);
const OUR_SKILL = /^(ship-kit:)?release-prep$/;
const OUR_AGENT = /^(ship-kit:)?log-scout$/;
const SPAWN = new Set(['Agent', 'Task']);
const HEADINGS = ['## 這一版改了什麼', '## 升級要注意', '## 怎麼確認'];
const NEXT_STEP = /^[\s>*_`-]*下一步[：:]/;
const COUNT_LINE = /^[\s>*_`|-]*共\s*(\d+)\s*筆/;

const read = (path) => (existsSync(path) ? readFileSync(path, 'utf8') : null);
const sha = (path) => createHash('sha256').update(readFileSync(path)).digest('hex').slice(0, 16);
const walk = (dir, root = dir) => (existsSync(dir) ? readdirSync(dir).flatMap((entry) => {
  const path = join(dir, entry);
  if (statSync(path).isDirectory()) return entry === '.claude' ? [] : walk(path, root);
  return [relative(root, path).replaceAll('\\', '/')];
}) : []);
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((block) => (typeof block === 'string' ? block : block.text ?? textOf(block.content) ?? '')).join('\n') : '');
const yes = (value) => (value ? 'yes' : 'no');
const names = (list) => (list ?? []).map((each) => (typeof each === 'string' ? each : each.name));
const sum3 = (usage) => (usage ? (usage.input_tokens ?? 0) + (usage.cache_creation_input_tokens ?? 0) + (usage.cache_read_input_tokens ?? 0) : null);
// Every way one folder is written in a stream: C:\\a\\b (inside JSON text), C:\a\b, C:/a/b, either case of the drive letter.
const spellings = (path) => {
  if (!path) return [];
  const forward = path.replaceAll('\\', '/');
  const drives = /^[A-Za-z]:/.test(forward) ? [forward[0].toUpperCase() + forward.slice(1), forward[0].toLowerCase() + forward.slice(1)] : [forward];
  return [...new Set(drives.flatMap((each) => [each.replaceAll('/', '\\\\'), each.replaceAll('/', '\\'), each]))];
};
const same = (a, b) => String(a ?? '').replaceAll('\\', '/').replace(/\/$/, '').toLowerCase() === String(b ?? '').replaceAll('\\', '/').replace(/\/$/, '').toLowerCase();

// The project as session.sh builds it: lab-a or lab-b plus the files it places.
function baseline(project) {
  const dir = join(seed, `lab-${project}`);
  const files = new Map(walk(dir).map((file) => [file, sha(join(dir, file))]));
  const t = truth[project];
  files.set(t.test, sha(join(seed, 'placed', project === 'a' ? 'a.queue-test.mjs.txt' : 'b.fares-test.mjs.txt')));
  t.logs.forEach((log, at) => files.set(`logs/${log}`, sha(join(seed, 'placed', `${project}.jobs-${at + 1}.txt`))));
  return files;
}

function disk(lab, project) {
  if (!existsSync(lab)) return { missing: true };
  const t = truth[project];
  const version = t.release;
  let found = null;
  try { found = JSON.parse(read(join(lab, 'package.json'))).version; } catch { found = '(package.json does not parse)'; }
  const log = (read(join(lab, 'CHANGELOG.md')) ?? '').split('\n').map((line) => line.trimEnd());
  const unreleased = log.indexOf('## Unreleased');
  const heading = log.findIndex((line) => new RegExp(`^## v${version.replaceAll('.', '\\.')} \\(\\d{4}-\\d{2}-\\d{2}\\)$`).test(line));
  const between = unreleased >= 0 && heading > unreleased ? log.slice(unreleased + 1, heading) : [];
  const next = log.findIndex((line, at) => at > heading && line.startsWith('## '));
  const after = heading >= 0 ? log.slice(heading + 1, next < 0 ? log.length : next) : [];
  const readme = (read(join(lab, 'README.md')) ?? '').split('\n').map((line) => line.trim());
  const note = read(join(lab, 'releases', `v${version}.md`));
  const noteLines = (note ?? '').split('\n').map((line) => line.trimEnd());
  const base = baseline(project);
  const now = new Map(walk(lab).map((file) => [file, sha(join(lab, file))]));
  return {
    version, found,
    f1: found === version,
    f2: heading >= 0 && unreleased >= 0 && heading > unreleased && !between.some((line) => line.startsWith('- ')) && after.some((line) => line.startsWith('- ')),
    f3: readme.includes(`Latest release: v${version}`),
    f4File: note !== null,
    f4Headings: HEADINGS.filter((each) => noteLines.includes(each)).length,
    changed: [...now].filter(([file, sum]) => base.has(file) && base.get(file) !== sum).map(([file]) => file),
    added: [...now.keys()].filter((file) => !base.has(file)),
    gone: [...base.keys()].filter((file) => !now.has(file)),
    testSame: now.get(t.test) === base.get(t.test),
  };
}

function digest(file) {
  const name = basename(file).replace(/\.stream\.jsonl$/, '');
  const dir = dirname(file);
  const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap((line) => { try { return [JSON.parse(line)]; } catch { return []; } })
    .filter((line) => line.type !== 'rate_limit_event');
  const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
  const results = lines.filter((line) => line.type === 'result');
  const result = results.at(-1) ?? {};
  const session = read(join(dir, `${name}.session.txt`)) ?? '';
  const arm = (session.match(/^# \S+ \| arm (\S+)/) ?? [])[1] ?? '?';
  const spec = ARMS[arm] ?? { project: 'b', own: false, kit: false };
  const t = truth[spec.project];
  const cwd = init.cwd ?? '';
  const kitDir = process.env.KIT_DIR ?? join(dirname(dir), PLUGIN);
  const home = homedir();
  const mask = (text) => {
    let shown = String(text ?? '');
    for (const [path, mark] of [[cwd, '<lab>'], [kitDir, '<plugin>'], [home, '<home>']]) for (const each of spellings(path)) shown = shown.split(each).join(mark);
    return shown.split(basename(home)).join('<user>')
      .replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, '<uuid>')
      .replace(/toolu_[0-9A-Za-z]{6,}/g, 'toolu_<id>').replace(/agent-[0-9a-f]{6,}/g, 'agent-<id>');
  };
  const place = (path) => {
    if (!path) return '';
    const shown = mask(path).replaceAll('\\', '/').replace(/^<lab>\/?/, '') || '.';
    if (shown.startsWith('<plugin>')) return shown;
    return /^<home>|^[A-Za-z]:|^\//.test(shown) ? '(outside the project)' : shown;
  };
  const isMcp = (tool) => String(tool).startsWith('mcp__');
  const skillName = (value) => { const skill = String(value ?? '').replace(/^\//, ''); return OUR_SKILL.test(skill) || SHIPPED.has(skill) ? skill : '(another skill)'; };
  const agentName = (value) => (!value ? '(no type given)' : OUR_AGENT.test(value) || BUILT_IN.has(value) ? value : '(another agent)');

  // The init event.
  const plugins = (init.plugins ?? []).map((each) => (typeof each === 'string' ? { name: each } : each));
  const ours = plugins.filter((each) => each.name === PLUGIN);
  const skills = names(init.skills);
  const agents = names(init.agents);
  const commands = names(init.slash_commands);
  const errors = (init.plugin_errors ?? []).map((each) => (each.plugin === PLUGIN || same(each.path, kitDir)
    ? `${each.type}: ${mask(each.message).slice(0, 200)}` : `${each.type}: (not the seed's plugin: message not shown)`));

  // The logging hook's record: which calls got as far as a permission request.
  const seen = (read(join(dir, `${name}.seen.txt`)) ?? '').split('\n').filter(Boolean);
  const asked = new Set();
  const pending = [];
  for (const line of seen) {
    const [kind, , id, tool, ...rest] = line.split(' ');
    const what = rest.join(' ').split(' | ')[0];
    if (kind === 'PreToolUse') pending.push({ tool, id: String(id).replace('id=', ''), what });
    if (kind === 'PermissionRequest') {
      const match = pending.findLast((each) => each.tool === tool && each.what === what && !asked.has(each.id));
      if (match) asked.add(match.id);
    }
  }
  const kinds = {};
  for (const line of seen) kinds[line.split(' ')[0]] = (kinds[line.split(' ')[0]] ?? 0) + 1;

  // The guard's own record.
  const guard = (read(join(dir, `${name}.guard.txt`)) ?? '').split('\n').filter(Boolean);
  const guardBy = { plugin: 0, project: 0 };
  const guardSays = { pass: 0, block: 0 };
  const shapes = new Set();
  for (const line of guard) {
    const where = (line.match(/^guard\((\w+)\)/) ?? [])[1];
    if (where in guardBy) guardBy[where] += 1;
    const says = (line.match(/-> (\w+)/) ?? [])[1];
    if (says in guardSays) guardSays[says] += 1;
    shapes.add((line.split(' | ')[1] ?? '').trim());
  }

  // The stream.
  const deniedIds = new Set(results.flatMap((each) => each.permission_denials ?? []).map((each) => each.tool_use_id).filter(Boolean));
  const calls = [];
  const byId = new Map();
  const spawns = new Map();
  const models = { main: new Set(), under: new Set() };
  const usage = new Map();
  const notes = [];
  let baseDirs = [];
  for (const line of lines) {
    const parent = line.parent_tool_use_id ?? null;
    if (line.type === 'assistant') {
      const message = line.message ?? {};
      if (message.model && message.model !== '<synthetic>') (parent ? models.under : models.main).add(message.model);
      if (!parent && message.usage && message.id) usage.set(message.id, message.usage);
      for (const block of message.content ?? []) {
        if (block.type !== 'tool_use' || byId.has(block.id)) continue;
        const input = block.input ?? {};
        const call = { n: calls.length + 1, id: block.id, under: parent ? (spawns.get(parent)?.type ?? '(an Agent call)') : null, tool: isMcp(block.name) ? 'mcp__(a server)' : block.name, label: 'no result', text: '' };
        if (block.name === 'Skill') {
          call.skill = String(input.skill ?? input.name ?? '').replace(/^\//, '');
          call.target = `skill=${skillName(call.skill)}${input.args ? ` args="${String(input.args).split('\n')[0].slice(0, 40)}"` : ''}`;
        } else if (SPAWN.has(block.name)) {
          call.type = agentName(input.subagent_type);
          call.target = `type=${call.type} run_in_background=${input.run_in_background ?? '-'} prompt ${String(input.prompt ?? '').length} chars`;
          spawns.set(block.id, { n: call.n, type: call.type, raw: String(input.subagent_type ?? ''), report: null, how: '-', tools: {} });
        } else if (isMcp(block.name)) {
          call.target = '(not shown)';
        } else {
          call.target = place(input.file_path ?? input.path) || mask(String(input.pattern ?? '').slice(0, 60));
        }
        if (parent && spawns.has(parent)) spawns.get(parent).tools[block.name] = (spawns.get(parent).tools[block.name] ?? 0) + 1;
        calls.push(call);
        byId.set(block.id, call);
      }
    }
    if (line.type === 'user') {
      const content = line.message?.content;
      const blocks = Array.isArray(content) ? content : [{ type: 'text', text: textOf(content) }];
      for (const block of blocks) {
        const text = textOf(block.content ?? block.text ?? block);
        if (block.type !== 'tool_result') {
          const at = text.indexOf('Base directory for this skill:');
          if (at >= 0) baseDirs.push(place(text.slice(at + 30).split('\n')[0].trim()));
          continue;
        }
        const call = byId.get(block.tool_use_id);
        if (!call) continue;
        call.text = call.tool.startsWith('mcp__') ? '(not shown)' : mask(text);
        call.isError = Boolean(block.is_error);
        const hook = /hook (blocking )?error|hook comes from/i.test(text);
        const wasAsked = asked.has(String(block.tool_use_id).slice(-4));
        const refusal = deniedIds.has(block.tool_use_id) || /permission|haven't granted|requires approval|denied/i.test(text.slice(0, 400));
        call.label = !block.is_error ? 'ran' : hook ? 'stopped by a hook' : wasAsked ? 'refused: asked' : refusal ? 'refused: other' : 'ran, failed';
        call.namesPlugin = text.includes(`${PLUGIN} plugin`);
        const spawn = spawns.get(block.tool_use_id);
        if (spawn) { spawn.report = text; spawn.how = line.tool_use_result?.isAsync ? 'background' : 'foreground'; }
      }
    }
    if (line.type === 'system' && line.subtype === 'task_notification' && spawns.has(line.tool_use_id)) {
      const spawn = spawns.get(line.tool_use_id);
      spawn.report = String(line.summary ?? line.result ?? '');
      spawn.how = 'background (report came as a task_notification)';
    }
    if (line.type === 'system' && line.subtype !== 'init') notes.push(line);
  }
  for (const spawn of spawns.values()) {
    const report = spawn.report ?? '';
    spawn.found = t.unfinished.filter((job) => report.includes(job.id)).length;
    spawn.wrong = t.finished.filter((id) => report.includes(id)).length;
    const count = report.split('\n').map((each) => each.match(COUNT_LINE)).find(Boolean);
    spawn.count = count ? Number(count[1]) : null;
  }
  const subtypes = {};
  for (const line of notes) subtypes[line.subtype] = (subtypes[line.subtype] ?? 0) + 1;
  const hookLines = notes.filter((line) => line.subtype === 'hook_response');
  const hookSeen = {};
  for (const line of hookLines) {
    const key = `${line.hook_name} exit ${line.exit_code} ${line.outcome}`;
    hookSeen[key] = (hookSeen[key] ?? 0) + 1;
  }
  const hookKeys = [...new Set(hookLines.flatMap((line) => Object.keys(line)))].sort();

  const d = disk(join(dir, `${name}.lab`), spec.project);
  const replies = results.map((each) => (typeof each.result === 'string' ? each.result : ''));
  const lastLines = replies.map((reply) => reply.split('\n').map((line) => line.trim()).filter(Boolean).at(-1) ?? '');
  const f5 = lastLines.some((line) => NEXT_STEP.test(line) && line.includes(`git tag v${t.release}`));
  const allReplies = replies.join('\n');
  const mainUsage = [...usage.values()].map(sum3);
  const edits = calls.filter((call) => call.tool === 'Edit' || call.tool === 'Write');
  const skillCalls = calls.filter((call) => call.tool === 'Skill' && OUR_SKILL.test(call.skill ?? ''));
  const ourSpawns = [...spawns.values()].filter((spawn) => OUR_AGENT.test(spawn.raw));
  const reported = ourSpawns.find((spawn) => spawn.found === t.unfinished.length && spawn.count === t.unfinished.length);
  const guardHere = spec.own && !spec.kit ? guardBy.project : guardBy.plugin;
  const parts = {
    plugin: ours.length === 1 && plugins.filter((each) => each.name !== PLUGIN && !String(each.name).startsWith('cc-plugin-')).length === 0,
    skillListed: skills.some((skill) => OUR_SKILL.test(skill)),
    skillUsed: skillCalls.length > 0,
    skillEffect: Boolean(d.f4File && d.f4Headings === 3),
    agentListed: agents.some((agent) => OUR_AGENT.test(agent)),
    agentUsed: ourSpawns.length > 0,
    agentEffect: Boolean(reported),
    hookUsed: guardHere > 0 && guardHere === edits.length,
  };
  return {
    name, arm, spec, t, d, calls, parts, mask, seenLines: seen.length, kinds, guard, guardBy, guardSays, shapes, edits, subtypes, hookSeen, hookKeys, baseDirs,
    model: init.model, version: init.claude_code_version, permissionMode: init.permissionMode, initKeys: Object.keys(init).sort(),
    builtin: (init.tools ?? []).filter((tool) => !isMcp(tool)), mcpTools: (init.tools ?? []).filter(isMcp).length, servers: (init.mcp_servers ?? []).length,
    pluginsOwn: plugins.filter((each) => String(each.name).startsWith('cc-plugin-')).length, pluginsOurs: ours.length,
    pluginPath: ours.length ? (same(ours[0].path, kitDir) ? 'is <plugin>' : ours[0].path === undefined ? 'no path given' : 'IS NOT <plugin>') : '-',
    pluginsOther: plugins.filter((each) => each.name !== PLUGIN && !String(each.name).startsWith('cc-plugin-')).length, errors,
    skillsOurs: skills.filter((skill) => OUR_SKILL.test(skill)), skillsShipped: skills.filter((skill) => SHIPPED.has(skill)).length,
    skillsOther: skills.filter((skill) => !OUR_SKILL.test(skill) && !SHIPPED.has(skill)).length, skillsTotal: skills.length,
    agentsOurs: agents.filter((agent) => OUR_AGENT.test(agent)), agentsBuiltIn: agents.filter((agent) => BUILT_IN.has(agent)).length,
    agentsOther: agents.filter((agent) => !OUR_AGENT.test(agent) && !BUILT_IN.has(agent)).length, agentsTotal: agents.length,
    commandsOurs: commands.filter((command) => /release-prep$/.test(command) || command.startsWith(`${PLUGIN}:`)), commandsTotal: commands.length,
    models, modelUsage: [...new Set(results.flatMap((each) => Object.keys(each.modelUsage ?? {})))],
    results: results.map((each, at) => `${each.subtype} (${each.num_turns} turns, last line: ${mask(lastLines[at]).slice(0, 60)})`),
    cost: result.total_cost_usd, denials: results.flatMap((each) => each.permission_denials ?? []).map((each) => (isMcp(each.tool_name) ? 'mcp__(a server)' : each.tool_name ?? '?')),
    spawns: [...spawns.values()], skillCalls, f5, mainUsage, first: mainUsage[0] ?? null,
    idsInReply: t.unfinished.filter((job) => allReplies.includes(job.id)).length,
    reply: replies.at(-1) ?? '',
  };
}

const sessions = process.argv.slice(2).map(digest);
for (const s of sessions) {
  const d = s.d;
  console.log(`== ${s.name} | arm ${s.arm} (project ${s.spec.project}, parts in .claude/: ${yes(s.spec.own)}, plugin loaded: ${yes(s.spec.kit)}) | model ${s.model} | Claude Code ${s.version} | permission mode ${s.permissionMode}`);
  console.log(`   result lines: ${s.results.join(' | ') || 'none'} | cost USD ${s.cost}`);
  console.log(`   built-in tools offered (${s.builtin.length}): ${s.builtin.join(' ') || 'none'} | MCP servers ${s.servers}, MCP tools ${s.mcpTools}`);
  console.log(`   plugins on the init line: Claude Code's own (cc-plugin-*) ${s.pluginsOwn} | ${PLUGIN} ${s.pluginsOurs} (its path ${s.pluginPath}) | any other ${s.pluginsOther}${s.pluginsOther ? '  <- STOP: not the seed\'s (count only)' : ''}`);
  console.log(`   plugin_errors on the init line: ${s.errors.length}${s.errors.length ? ` -> ${s.errors.join(' || ')}` : ''}`);
  console.log(`   skills: ${s.skillsTotal} = the seed's ${s.skillsOurs.length} (${s.skillsOurs.join(', ') || 'none'}) + shipped with Claude Code ${s.skillsShipped} + any other ${s.skillsOther}${s.skillsOther ? '  <- STOP (count only)' : ''}`);
  console.log(`   agents: ${s.agentsTotal} = the seed's ${s.agentsOurs.length} (${s.agentsOurs.join(', ') || 'none'}) + built in ${s.agentsBuiltIn} + any other ${s.agentsOther}${s.agentsOther ? '  <- STOP (count only)' : ''}`);
  console.log(`   slash commands: ${s.commandsTotal}, of them the seed's: ${s.commandsOurs.join(', ') || 'none'}`);
  console.log(`   init keys: ${s.initKeys.join(' ')}`);
  console.log(`   models on the main conversation: ${[...s.models.main].join(', ') || 'none seen'} | under Agent calls: ${[...s.models.under].join(', ') || 'none seen'} | modelUsage keys: ${s.modelUsage.join(', ') || 'none'}`);
  for (const call of s.calls) {
    console.log(`   call ${String(call.n).padStart(2)}${call.under ? ` [under ${call.under}]` : ''} ${call.tool} ${String(call.target ?? '').replaceAll('\n', ' ⏎ ').slice(0, 130)}`);
    const most = call.label === 'stopped by a hook' ? 10 : 2;
    console.log(`        -> ${call.label}${call.namesPlugin ? ` | the text names the ${PLUGIN} plugin` : ''} | ${call.text.split('\n').filter((each) => each.trim()).slice(0, most).map((each) => each.slice(0, 150)).join(' ⏎ ')}`);
  }
  const labels = {};
  for (const call of s.calls) labels[call.label] = (labels[call.label] ?? 0) + 1;
  console.log(`   calls: ${s.calls.length} | ${Object.entries(labels).map(([label, count]) => `${label} ${count}`).join(' | ') || 'none'} | permission_denials on the result lines: ${s.denials.length}${s.denials.length ? ` (${s.denials.join(', ')})` : ''}`);
  console.log(`   Skill calls for the seed's skill: ${s.skillCalls.length}${s.skillCalls.length ? ` (${s.skillCalls.map((call) => `call ${call.n} as "${call.skill}"`).join(', ')})` : ''} | "Base directory for this skill" messages: ${s.baseDirs.join(' ; ') || 'none'}`);
  for (const spawn of s.spawns) {
    console.log(`   Agent call ${spawn.n}: type ${spawn.type} | ran in the ${spawn.how} | tools under it: ${Object.entries(spawn.tools).map(([tool, count]) => `${tool} ${count}`).join(', ') || 'none seen'}`);
    console.log(`      its report: ${spawn.report === null ? 'none seen' : `${spawn.report.length} chars | unfinished jobs named ${spawn.found} of ${s.t.unfinished.length} | finished jobs also named in it ${spawn.wrong} | a line "共 N 筆": ${spawn.count === null ? 'no' : `yes, N = ${spawn.count}`}`}`);
    for (const line of (spawn.report ?? '').split('\n').filter((each) => each.trim()).slice(0, 10)) console.log(`      | ${s.mask(line).slice(0, 120)}`);
  }
  console.log(`   system lines by subtype: ${Object.entries(s.subtypes).map(([subtype, count]) => `${subtype} ${count}`).join(', ') || 'none'}`);
  console.log(`   hook_response lines: ${Object.entries(s.hookSeen).map(([key, count]) => `${key} x${count}`).join(' | ') || 'none'} | keys on them: ${s.hookKeys.join(' ') || '-'}`);
  console.log(`   logging hook's record: ${s.seenLines} lines | ${Object.entries(s.kinds).map(([kind, count]) => `${kind} ${count}`).join(', ') || 'none'}`);
  console.log(`   guard's record: ${s.guard.length} lines | from the plugin ${s.guardBy.plugin}, from the project ${s.guardBy.project} | pass ${s.guardSays.pass}, block ${s.guardSays.block} | ${[...s.shapes].join(' ; ') || '-'} | Edit and Write calls in the stream: ${s.edits.length}`);
  console.log(`   main conversation, each request's input side: ${s.mainUsage.join(', ') || 'none'} | first request ${s.first}`);
  if (d.missing) { console.log('   (no copy of the project next to this stream: the files cannot be checked)'); continue; }
  console.log(`   the project afterwards: changed ${d.changed.join(' ') || 'nothing'} | new ${d.added.join(' ') || 'nothing'} | gone ${d.gone.join(' ') || 'nothing'} | the existing test file is unchanged: ${yes(d.testSame)}`);
  console.log(`   release steps for v${d.version}: F1 package.json ${yes(d.f1)} (${d.found}) | F2 CHANGELOG ${yes(d.f2)} | F3 README ${yes(d.f3)} | F4 releases/v${d.version}.md ${yes(d.f4File)} with ${d.f4Headings} of 3 template headings | F5 a reply ends with 下一步 and git tag v${d.version}: ${yes(s.f5)}`);
  console.log(`   unfinished jobs named in the replies: ${s.idsInReply} of ${s.t.unfinished.length}`);
  const p = s.parts;
  console.log(`   scored: plugin on the init line ${yes(p.plugin)} | skill listed ${yes(p.skillListed)}, used ${yes(p.skillUsed)}, effect ${yes(p.skillEffect)} | agent listed ${yes(p.agentListed)}, used ${yes(p.agentUsed)}, effect ${yes(p.agentEffect)} | hook: one guard line per Edit or Write ${yes(p.hookUsed)} | all three parts ${yes(p.skillListed && p.skillUsed && p.skillEffect && p.agentListed && p.agentUsed && p.agentEffect && p.hookUsed)}`);
  console.log(`   final reply (${s.reply.length} chars), first 10 lines:`);
  for (const line of s.reply.split('\n').filter((each) => each.trim()).slice(0, 10)) console.log(`      | ${s.mask(line).slice(0, 140)}`);
}
if (sessions.length > 1) {
  console.log('\nname | arm | plugin listed | other plugins | skill listed as | Skill call as | F4 | F5 | agent listed as | Agent call as | report ok | guard lines plugin/project | Edit+Write | all three | first request | cost USD');
  for (const s of sessions) {
    const p = s.parts;
    console.log([s.name, s.arm, yes(p.plugin), s.pluginsOther, s.skillsOurs.join('+') || '-', s.skillCalls.map((call) => call.skill).join('+') || '-',
      yes(p.skillEffect), yes(s.f5), s.agentsOurs.join('+') || '-', s.spawns.map((spawn) => spawn.type).join('+') || '-', yes(p.agentEffect),
      `${s.guardBy.plugin}/${s.guardBy.project}`, s.edits.length,
      yes(p.skillListed && p.skillUsed && p.skillEffect && p.agentListed && p.agentUsed && p.agentEffect && p.hookUsed), s.first, s.cost].join(' | '));
  }
}
