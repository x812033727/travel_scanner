// Reads what one headless session left behind and prints what this video counts.
//
//   node <seed>/tally.mjs <logs>/<name>.stream.jsonl [<logs>/<name>.stream.jsonl ...]
//
// Next to each stream it expects <name>.lab/, the copy of the project session.sh takes when the
// session ends. From the stream: what was offered, which agents the session started with, every
// tool call of the main conversation in order, every Agent call and what ran under it, how many
// characters of tool results landed in the main conversation and how many stayed under an Agent
// call, the size of the main conversation's first and last request, what the result line reports,
// and which of the planted job ids the final reply names. From the copy of the project: whether
// REPORT.md exists and whether the logs are untouched.
//
// Nothing outside the project is printed: paths are relative to the session's cwd or shown as
// "(outside the project)"; an agent, skill or plugin that is neither the project's nor one Claude
// Code ships is only counted, never named; long hexadecimal ids are masked; rate-limit events and
// session ids are never printed.
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { basename, dirname, isAbsolute, join, posix, win32 } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const truth = JSON.parse(readFileSync(join(seed, 'truth.json'), 'utf8'));
const UNFINISHED = truth.unfinished.map((job) => job.id);
const NEXT_FILE = truth.finishedInTheNextFile.map((job) => job.id);
// The built-in subagents on the official sub-agents page, 2026-10-10.
const BUILT_IN = new Set(['Explore', 'Plan', 'general-purpose', 'claude', 'statusline-setup', 'claude-code-guide']);
// Names on the official commands page, 2026-10-09: the skills Claude Code ships with.
const SHIPPED = new Set(['deep-research', 'design', 'design-sync', 'dataviz', 'artifact-diagramming',
  'artifact-capabilities', 'update-config', 'verify', 'debug', 'code-review', 'simplify', 'batch',
  'fewer-permission-prompts', 'doctor', 'loop', 'schedule', 'claude-api', 'workflow-authoring', 'run',
  'run-skill-generator', 'plugin-authoring', 'claude-in-chrome', 'slides']);
const SPAWN = new Set(['Agent', 'Task']);
const MARK = '【trip-queue】';
const COUNT_LINE = /^[\s>*_`-]*共\s*\d+\s*筆/;

function relativeTo(cwd, file) {
  if (typeof file !== 'string' || !file) return '';
  const tool = /^[A-Za-z]:[\\/]/.test(cwd) ? win32 : posix;
  if (!tool.isAbsolute(file)) return file.replaceAll('\\', '/');
  const rel = tool.relative(cwd, file);
  if (!rel) return '.';
  if (rel.startsWith('..') || tool.isAbsolute(rel) || isAbsolute(rel)) return '(outside the project)';
  return rel.replaceAll('\\', '/');
}

const walk = (dir, base = dir) => (existsSync(dir) ? readdirSync(dir).flatMap((entry) => {
  const path = join(dir, entry);
  return statSync(path).isDirectory() ? walk(path, base) : [path.slice(base.length + 1).replaceAll('\\', '/')];
}) : []);
const read = (path) => (existsSync(path) ? readFileSync(path, 'utf8') : null);
const sha = (text) => createHash('sha256').update(text).digest('hex').slice(0, 16);
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((block) => (typeof block === 'string' ? block : block.text ?? textOf(block.content) ?? '')).join('\n') : '');
const ids = (text) => [...new Set(String(text).match(/J\d{4}/g) ?? [])];
const sum3 = (usage) => (usage ? (usage.input_tokens ?? 0) + (usage.cache_creation_input_tokens ?? 0) + (usage.cache_read_input_tokens ?? 0) : null);

function disk(lab) {
  if (!existsSync(lab)) return { missing: true };
  const agentDir = join(lab, '.claude', 'agents');
  const mine = (existsSync(agentDir) ? readdirSync(agentDir) : []).map((file) => {
    const name = (read(join(agentDir, file)) ?? '').split('\n').find((line) => line.startsWith('name:'));
    return name ? name.slice(5).trim() : null;
  }).filter(Boolean);
  const report = read(join(lab, 'REPORT.md'));
  const logs = walk(join(seed, 'log-lab', 'logs'));
  const changed = logs.filter((name) => read(join(lab, 'logs', name)) !== read(join(seed, 'log-lab', 'logs', name)));
  return {
    mine,
    files: walk(lab).filter((path) => !path.startsWith('.claude/')).sort(),
    hasClaudeMd: existsSync(join(lab, 'CLAUDE.md')),
    report: report === null ? null : { lines: report.replace(/\n$/, '').split('\n').length, found: UNFINISHED.filter((id) => report.includes(id)).length, sha: sha(report) },
    logsChanged: changed.length,
  };
}

function digest(file) {
  const name = basename(file).replace(/\.stream\.jsonl$/, '');
  const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).map((line) => JSON.parse(line));
  const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
  const result = lines.findLast((line) => line.type === 'result') ?? {};
  const cwd = init.cwd ?? '';
  const d = disk(join(dirname(file), `${name}.lab`));
  const mine = new Set(d.mine ?? []);
  const agentLabel = (type) => (!type ? '(no type given)' : mine.has(type) || BUILT_IN.has(type) ? type : '(another agent)');
  const mask = (text) => {
    let shown = String(text);
    for (const spelling of new Set([cwd, cwd.replaceAll('\\', '/'), cwd.replaceAll('\\', '\\\\')])) if (spelling) shown = shown.split(spelling).join('<lab>');
    return shown.replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, '<uuid>').replace(/\b[0-9a-f]{12,}\b/gi, '<id>');
  };

  const names = (list) => (list ?? []).map((each) => (typeof each === 'string' ? each : each.name));
  const agents = init.agents === undefined ? null : names(init.agents);
  const skills = names(init.skills);
  const plugins = names(init.plugins);

  const timeline = [];
  const spawns = new Map(); // Agent tool_use id -> what was asked and what ran under it
  const toolOf = new Map();
  const seenBlocks = new Set();
  const usageOf = new Map(); // main conversation: message id -> usage, in order
  const subUsage = new Map();
  const models = { main: new Set(), under: new Set() };
  const chars = { mainOther: 0, mainAgent: 0, under: 0 };
  const notes = { count: 0, chars: 0, found: 0 };
  const writers = [];
  let calls = 0;
  for (const line of lines) {
    const parent = line.parent_tool_use_id ?? null;
    const under = parent ? spawns.get(parent) : null;
    if (line.type === 'assistant') {
      const message = line.message ?? {};
      if (message.model && message.model !== '<synthetic>') (parent ? models.under : models.main).add(message.model);
      if (message.usage && message.id) (parent ? subUsage : usageOf).set(message.id, message.usage);
      for (const block of message.content ?? []) {
        if (parent && block.type === 'text' && under) under.textBlocks += 1;
        if (block.type !== 'tool_use' || seenBlocks.has(block.id)) continue;
        seenBlocks.add(block.id);
        const input = block.input ?? {};
        const target = relativeTo(cwd, input.file_path ?? input.path ?? '');
        const detail = String(target || input.pattern || '').split('\n')[0].slice(0, 80);
        if ((block.name === 'Write' || block.name === 'Edit') && target) writers.push({ target, by: parent ? (under?.type ?? '(under an unknown call)') : 'main' });
        if (parent) {
          toolOf.set(block.id, `${block.name} (under an Agent call)`);
          if (under) { under.tools[block.name] = (under.tools[block.name] ?? 0) + 1; under.calls.push(`${block.name} ${detail}`); }
          continue;
        }
        calls += 1;
        toolOf.set(block.id, `${block.name} (call ${calls})`);
        if (SPAWN.has(block.name)) {
          const prompt = String(input.prompt ?? '');
          const spawn = {
            at: calls, tool: block.name, type: agentLabel(input.subagent_type), keys: Object.keys(input).join(','),
            model: input.model ?? '-', background: input.run_in_background ?? '-', named: input.name === undefined ? 'no' : 'yes',
            promptChars: prompt.length, markInPrompt: prompt.includes(MARK), tools: {}, calls: [], textBlocks: 0,
            firstUser: null, resultChars: 0, report: null,
          };
          spawns.set(block.id, spawn);
          timeline.push(`call ${String(calls).padStart(2)} ${block.name} type=${spawn.type} [input keys: ${spawn.keys}] model=${spawn.model} run_in_background=${spawn.background} name given=${spawn.named} prompt ${spawn.promptChars} chars`);
        } else {
          timeline.push(`call ${String(calls).padStart(2)} ${block.name} ${detail}`);
        }
      }
    }
    if (line.type === 'user') {
      const content = line.message?.content;
      const blocks = Array.isArray(content) ? content : [{ type: 'text', text: textOf(content) }];
      for (const block of blocks) {
        const text = textOf(block.content ?? block.text ?? block);
        if (block.type === 'tool_result') {
          if (parent) { chars.under += text.length; if (under) under.resultChars += text.length; continue; }
          const spawn = spawns.get(block.tool_use_id);
          if (spawn) { chars.mainAgent += text.length; spawn.report = text; } else chars.mainOther += text.length;
        } else if (parent) {
          if (under && under.firstUser === null) under.firstUser = text.length;
        } else {
          notes.count += 1; notes.chars += text.length;
          notes.found = Math.max(notes.found, UNFINISHED.filter((id) => text.includes(id)).length);
        }
      }
    }
  }
  const subtypes = {};
  for (const line of lines) if (line.type === 'system') subtypes[line.subtype] = (subtypes[line.subtype] ?? 0) + 1;
  const reply = typeof result.result === 'string' ? result.result : '';
  const named = ids(reply);
  const mainUsage = [...usageOf.values()];
  const perModel = Object.entries(result.modelUsage ?? {}).map(([model, use]) => `${model} in ${use.inputTokens ?? '?'} + cache write ${use.cacheCreationInputTokens ?? '?'} + cache read ${use.cacheReadInputTokens ?? '?'}, out ${use.outputTokens ?? '?'}`);
  const treeTotal = Object.values(result.modelUsage ?? {}).reduce((total, use) => total + (use.inputTokens ?? 0) + (use.cacheCreationInputTokens ?? 0) + (use.cacheReadInputTokens ?? 0), 0);
  const tools = (init.tools ?? []).filter((tool) => !tool.startsWith('mcp__'));
  return {
    name, d, timeline, spawns: [...spawns.values()], chars, notes, subtypes, mask, reply,
    model: init.model, version: init.claude_code_version, permissionMode: init.permissionMode,
    tools, spawnTool: tools.filter((tool) => SPAWN.has(tool)).join('+') || 'none',
    mcpTools: (init.tools ?? []).filter((tool) => tool.startsWith('mcp__')).length,
    mcpServers: (init.mcp_servers ?? []).length,
    pluginsOther: plugins.filter((plugin) => !String(plugin).startsWith('cc-plugin-')).length,
    agents,
    agentsMine: (agents ?? []).filter((agent) => mine.has(agent)),
    agentsBuiltIn: (agents ?? []).filter((agent) => !mine.has(agent) && BUILT_IN.has(agent)),
    agentsOther: (agents ?? []).filter((agent) => !mine.has(agent) && !BUILT_IN.has(agent)).length,
    skillsOther: skills.filter((skill) => !SHIPPED.has(skill)).length, skillsTotal: skills.length,
    models, writers,
    first: sum3(mainUsage[0]), last: sum3(mainUsage.at(-1)), mainRequests: mainUsage.length,
    mainSum: mainUsage.reduce((total, usage) => total + sum3(usage), 0),
    subRequests: subUsage.size, subSum: [...subUsage.values()].reduce((total, usage) => total + sum3(usage), 0),
    resultUsage: sum3(result.usage), resultOut: result.usage?.output_tokens, perModel, treeTotal,
    subtype: result.subtype, turns: result.num_turns, cost: result.total_cost_usd,
    denials: (result.permission_denials ?? []).map((each) => each.tool_name ?? '?'),
    found: UNFINISHED.filter((id) => named.includes(id)),
    nextFile: NEXT_FILE.filter((id) => named.includes(id)),
    others: named.filter((id) => !UNFINISHED.includes(id) && !NEXT_FILE.includes(id)),
    markInReply: reply.includes(MARK),
  };
}

const yes = (value) => (value ? 'yes' : 'no');
const sessions = process.argv.slice(2).map(digest);
for (const s of sessions) {
  const d = s.d;
  const mine = s.spawns.filter((spawn) => (d.mine ?? []).includes(spawn.type));
  console.log(`== ${s.name} | model ${s.model} | Claude Code ${s.version} | permission mode ${s.permissionMode}`);
  console.log(`   result ${s.subtype}, ${s.turns} turns, permission denials ${s.denials.length}${s.denials.length ? ` (${s.denials.join(', ')})` : ''}, cost USD ${s.cost}`);
  console.log(`   built-in tools offered (${s.tools.length}): ${s.tools.join(' ')} | the tool that starts a subagent is listed as: ${s.spawnTool}`);
  console.log(`   MCP servers ${s.mcpServers}, MCP tools ${s.mcpTools} | plugins not shipped with Claude Code: ${s.pluginsOther} | skills ${s.skillsTotal}, of them not shipped with Claude Code: ${s.skillsOther}`);
  if (s.agents === null) console.log('   agents the session started with: (the init line has no agents list)');
  else console.log(`   agents the session started with: ${s.agents.length} = the project's ${s.agentsMine.length} (${s.agentsMine.join(', ') || 'none'}) + built in ${s.agentsBuiltIn.length} (${s.agentsBuiltIn.join(', ') || 'none'}) + anything else ${s.agentsOther}`);
  console.log(`   models on the main conversation's messages: ${[...s.models.main].join(', ') || 'none seen'} | on messages under an Agent call: ${[...s.models.under].join(', ') || 'none seen'}`);
  for (const entry of s.timeline) console.log(`   ${entry}`);
  console.log(`   subagent started: ${yes(s.spawns.length)} (${s.spawns.length} call${s.spawns.length === 1 ? '' : 's'}) | to a project agent: ${yes(mine.length)}${mine.length ? ` (${[...new Set(mine.map((spawn) => spawn.type))].join(', ')}, first at call ${mine[0].at})` : ''} | to others: ${s.spawns.filter((spawn) => !mine.includes(spawn)).map((spawn) => spawn.type).join(', ') || 'none'}`);
  for (const spawn of s.spawns) {
    const tools = Object.entries(spawn.tools).map(([tool, count]) => `${tool} ${count}`).join(', ') || 'none seen';
    console.log(`   under call ${spawn.at} (${spawn.type}): tool calls ${tools} | tool results ${spawn.resultChars} chars | first message under it ${spawn.firstUser === null ? 'none seen' : `${spawn.firstUser} chars`} | text blocks ${spawn.textBlocks} | marker in the prompt it was given: ${yes(spawn.markInPrompt)}`);
    for (const call of spawn.calls) console.log(`      ${call}`);
    if (spawn.report === null) { console.log('      what came back to the main conversation: no tool result seen for this call'); continue; }
    const report = spawn.report.split('\n');
    const countLine = report.find((line) => COUNT_LINE.test(line));
    console.log(`      what came back to the main conversation: ${spawn.report.length} chars, ${report.length} lines | planted ids in it ${UNFINISHED.filter((id) => spawn.report.includes(id)).length} of ${UNFINISHED.length} | a line "共 N 筆": ${countLine ? `yes (${countLine.trim().slice(0, 40)})` : 'no'} | marker ${MARK}: ${yes(spawn.report.includes(MARK))}`);
    for (const line of report.slice(0, 24)) console.log(`      | ${s.mask(line).slice(0, 110)}`);
    if (report.length > 24) console.log(`      | (${report.length - 24} more lines)`);
  }
  console.log(`   tool-result characters: in the main conversation ${s.chars.mainOther + s.chars.mainAgent} (from Agent calls ${s.chars.mainAgent}, from its own tools ${s.chars.mainOther}) | under Agent calls ${s.chars.under}`);
  console.log(`   main-conversation user messages that are not tool results: ${s.notes.count} (${s.notes.chars} chars, planted ids in the fullest one ${s.notes.found})`);
  console.log(`   system lines by subtype: ${Object.entries(s.subtypes).map(([subtype, count]) => `${subtype} ${count}`).join(', ') || 'none'}`);
  console.log(`   main conversation: ${s.mainRequests} requests | first request ${s.first} tokens | last request ${s.last} tokens | all its requests added up ${s.mainSum}`);
  console.log(`   messages under Agent calls that carry usage: ${s.subRequests} (added up ${s.subSum})`);
  console.log(`   result line: usage ${s.resultUsage} input-side tokens, ${s.resultOut} output | modelUsage added up ${s.treeTotal} input-side tokens`);
  for (const entry of s.perModel) console.log(`      modelUsage ${entry}`);
  console.log(`   final reply: planted unfinished jobs named ${s.found.length} of ${UNFINISHED.length} (${s.found.join(' ') || 'none'}) | jobs that finish in the next file named: ${s.nextFile.join(' ') || 'none'} | other job ids named: ${s.others.length}${s.others.length ? ` (${s.others.slice(0, 12).join(' ')})` : ''} | marker ${MARK}: ${yes(s.markInReply)}`);
  for (const line of s.reply.split('\n').filter((each) => [...s.nextFile, ...s.others.slice(0, 6)].some((id) => each.includes(id))).slice(0, 8)) console.log(`      | ${s.mask(line).slice(0, 110)}`);
  if (d.missing) { console.log('   (no copy of the project next to this stream: the files cannot be checked)'); continue; }
  const wrote = s.writers.filter((each) => each.target === 'REPORT.md').map((each) => each.by);
  console.log(`   files in the project afterwards: ${d.files.join(' ')}`);
  console.log(`   REPORT.md: ${d.report ? `exists, ${d.report.lines} lines, planted ids in it ${d.report.found} of ${UNFINISHED.length}` : 'does not exist'} | written by: ${wrote.join(', ') || 'no Write or Edit call seen'} | other files written: ${s.writers.filter((each) => each.target !== 'REPORT.md').map((each) => `${each.target} by ${each.by}`).join(', ') || 'none'}`);
  console.log(`   log files that differ from the seed: ${d.logsChanged} | CLAUDE.md in the project: ${yes(d.hasClaudeMd)}`);
}
if (sessions.length > 1) {
  console.log('\nname | subagent started | to the project agent | planted ids in the reply | next-file ids named | other ids named | main: tool-result chars | under Agent: tool-result chars | main first request | main last request | result usage | modelUsage total | cost USD | turns');
  for (const s of sessions) {
    const mine = s.spawns.filter((spawn) => (s.d.mine ?? []).includes(spawn.type));
    console.log([s.name, yes(s.spawns.length), yes(mine.length), `${s.found.length}/${UNFINISHED.length}`, s.nextFile.length, s.others.length,
      s.chars.mainOther + s.chars.mainAgent, s.chars.under, s.first, s.last, s.resultUsage, s.treeTotal, s.cost, s.turns].join(' | '));
  }
}
