// Reads what one headless session left behind and prints what this video counts.
//
//   node <seed>/tally.mjs <logs>/<name>.stream.jsonl [<logs>/<name>.stream.jsonl ...]
//
// Next to each stream it expects <name>.lab/, the copy of the project session.sh takes when the
// session ends. From the stream: what the init line says was offered and connected, every tool
// call of the conversation in order with what came back, what was denied, the size of the first
// and last request, what the result line reports, and how the final reply scores against
// truth.json. From the copy of the project: the server's own record of the requests it received.
//
// Only the seed's own MCP servers (the names in the project's .mcp.json) are ever named. A server,
// a tool, a plugin, a skill or an agent that is neither the seed's nor one Claude Code ships is
// counted, never named, and nothing it returned is printed. Paths are shown as <lab>; long ids are
// masked; rate-limit events and session ids are never printed.
import { existsSync, readFileSync } from 'node:fs';
import { basename, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const truth = JSON.parse(readFileSync(join(seed, 'truth.json'), 'utf8'));
const LOW = truth.low.map((each) => each.code);
// The built-in subagents on the official sub-agents page, 2026-10-10.
const AGENTS = new Set(['Explore', 'Plan', 'general-purpose', 'claude', 'statusline-setup', 'claude-code-guide']);
// Names on the official commands page, 2026-10-09: the skills Claude Code ships with.
const SHIPPED = new Set(['deep-research', 'design', 'design-sync', 'dataviz', 'artifact-diagramming',
  'artifact-capabilities', 'update-config', 'verify', 'debug', 'code-review', 'simplify', 'batch',
  'fewer-permission-prompts', 'doctor', 'loop', 'schedule', 'claude-api', 'workflow-authoring', 'run',
  'run-skill-generator', 'plugin-authoring', 'claude-in-chrome', 'slides']);

const read = (path) => (existsSync(path) ? readFileSync(path, 'utf8') : null);
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((block) => (typeof block === 'string' ? block
    : block.type === 'tool_reference' ? `[tool_reference ${block.tool_name ?? ''}]` : block.text ?? textOf(block.content))).join('\n') : '');
const sum3 = (usage) => (usage ? (usage.input_tokens ?? 0) + (usage.cache_creation_input_tokens ?? 0) + (usage.cache_read_input_tokens ?? 0) : null);
const yes = (value) => (value ? 'yes' : 'no');

function digest(file) {
  const name = basename(file).replace(/\.stream\.jsonl$/, '');
  const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap((line) => { try { return [JSON.parse(line)]; } catch { return []; } });
  const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
  const result = lines.findLast((line) => line.type === 'result') ?? {};
  const cwd = init.cwd ?? '';
  const lab = join(dirname(file), `${name}.lab`);
  const config = read(join(lab, '.mcp.json'));
  const mine = new Set(config ? Object.keys(JSON.parse(config).mcpServers ?? {}) : ['gear', 'gear-more']);
  const serverOf = (tool) => (String(tool).match(/^mcp__(.+?)__/) ?? [])[1];
  const ours = (tool) => { const server = serverOf(tool); return !server || mine.has(server); };
  const label = (tool) => (ours(tool) ? tool : 'mcp__(another server)');
  const mask = (text) => {
    let shown = String(text);
    for (const spelling of new Set([cwd, cwd.replaceAll('\\', '/'), cwd.replaceAll('\\', '\\\\')])) if (spelling) shown = shown.split(spelling).join('<lab>');
    return shown.replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, '<uuid>').replace(/toolu_[0-9A-Za-z]{6,}/g, 'toolu_<id>').replace(/\b[0-9a-f]{16,}\b/gi, '<id>');
  };
  const names = (list) => (list ?? []).map((each) => (typeof each === 'string' ? each : each.name));

  const allTools = init.tools ?? [];
  const servers = init.mcp_servers ?? [];
  const timeline = [];
  const toolOf = new Map();
  const seenBlocks = new Set();
  const usageOf = new Map();
  const models = new Set();
  const calls = { ours: 0, search: 0, builtin: 0, foreign: 0, oursError: 0 };
  let n = 0;
  let resultChars = 0;
  for (const line of lines) {
    if (line.type === 'assistant') {
      const message = line.message ?? {};
      if (message.model && message.model !== '<synthetic>') models.add(message.model);
      if (message.usage && message.id) usageOf.set(message.id, message.usage);
      for (const block of message.content ?? []) {
        if (!['tool_use', 'server_tool_use', 'mcp_tool_use'].includes(block.type) || seenBlocks.has(block.id)) continue;
        seenBlocks.add(block.id);
        n += 1;
        const mcp = Boolean(serverOf(block.name));
        const kind = !mcp ? (block.name === 'ToolSearch' ? 'search' : 'builtin') : ours(block.name) ? 'ours' : 'foreign';
        calls[kind] += 1;
        toolOf.set(block.id, { n, name: block.name, kind });
        const input = kind === 'foreign' ? '(not shown)' : mask(JSON.stringify(block.input ?? {})).slice(0, 160);
        timeline.push(`call ${String(n).padStart(2)} ${label(block.name)} ${input}${block.type === 'tool_use' ? '' : ` [block type ${block.type}]`}`);
      }
    }
    if (line.type === 'user') {
      const content = line.message?.content;
      for (const block of Array.isArray(content) ? content : []) {
        if (block.type !== 'tool_result') continue;
        const call = toolOf.get(block.tool_use_id);
        const text = textOf(block.content);
        resultChars += text.length;
        if (call?.kind === 'ours' && block.is_error) calls.oursError += 1;
        const types = Array.isArray(block.content) ? [...new Set(block.content.map((each) => each.type))].join('+') : 'string';
        const head = call?.kind === 'foreign' ? '(not shown)' : mask(text).split('\n').slice(0, 5).map((each) => each.slice(0, 120)).join(' ⏎ ');
        timeline.push(`  back ${String(call?.n ?? '?').padStart(2)} is_error=${block.is_error ?? '-'} ${text.length} chars [${types}] ${head}`);
      }
    }
  }
  const subtypes = {};
  for (const line of lines) if (line.type === 'system') subtypes[line.subtype] = (subtypes[line.subtype] ?? 0) + 1;
  const reply = typeof result.result === 'string' ? result.result : '';
  const codes = [...new Set(reply.match(/G-\d{3}/g) ?? [])];
  const shelves = [...new Set(reply.match(/\b[A-Z]-\d{2}\b/g) ?? [])];
  const mainUsage = [...usageOf.values()];
  const agents = names(init.agents);
  const skills = names(init.skills);
  const plugins = names(init.plugins);
  const score = {
    shelf: reply.includes(truth.asked.shelf),
    left: new RegExp(`(^|\\D)${truth.asked.left}(\\D|$)`).test(reply),
    low: LOW.filter((code) => codes.includes(code)),
    atLimit: truth.exactlyAtTheLimit.filter((code) => codes.includes(code)),
    otherReal: codes.filter((code) => truth.codes.includes(code) && code !== truth.asked.code && !LOW.includes(code) && !truth.exactlyAtTheLimit.includes(code)),
    madeUp: codes.filter((code) => !truth.codes.includes(code) && code !== truth.missing),
    wrongShelves: shelves.filter((shelf) => shelf !== truth.asked.shelf),
    missingNamed: codes.includes(truth.missing),
  };
  score.right = score.shelf && score.left && score.low.length === LOW.length && !score.atLimit.length && !score.otherReal.length && !score.madeUp.length;
  // "Offered an answer": the reply names a shelf, or a gear code other than the two the requests mention.
  score.offered = shelves.length > 0 || codes.some((code) => code !== truth.asked.code && code !== truth.missing);
  const perModel = Object.entries(result.modelUsage ?? {}).map(([model, use]) => `${model} in ${use.inputTokens ?? '?'} + cache write ${use.cacheCreationInputTokens ?? '?'} + cache read ${use.cacheReadInputTokens ?? '?'}, out ${use.outputTokens ?? '?'}`);
  const requests = read(join(lab, 'server', 'requests.txt'));
  const requestLines = requests ? requests.trim().split('\n').map((each) => each.replace(/^\d+ \+\s*\d+ms /, '')) : null;
  return {
    name, lab, timeline, subtypes, mask, reply, score, calls, resultChars, models, perModel,
    model: init.model, version: init.claude_code_version, permissionMode: init.permissionMode,
    builtin: allTools.filter((tool) => !serverOf(tool)),
    mcpOurs: allTools.filter((tool) => serverOf(tool) && ours(tool)),
    mcpOther: allTools.filter((tool) => serverOf(tool) && !ours(tool)).length,
    serversOurs: servers.filter((server) => mine.has(server.name)).map((server) => `${server.name}=${server.status}${Object.keys(server).filter((key) => !['name', 'status'].includes(key)).length ? ` [other keys: ${Object.keys(server).filter((key) => !['name', 'status'].includes(key)).join(',')}]` : ''}`),
    serversOther: servers.filter((server) => !mine.has(server.name)).length,
    serverErrors: (init.mcp_server_errors ?? []).map((each) => (mine.has(each.name) ? `${each.name}: ${each.type}` : '(another server)')),
    hasServersKey: Array.isArray(init.mcp_servers),
    pluginsOther: plugins.filter((plugin) => !String(plugin).startsWith('cc-plugin-')).length,
    agentsOther: agents.filter((agent) => !AGENTS.has(agent)).length, agentsTotal: agents.length,
    skillsOther: skills.filter((skill) => !SHIPPED.has(skill)).length, skillsTotal: skills.length,
    first: sum3(mainUsage[0]), last: sum3(mainUsage.at(-1)), requests: mainUsage.length,
    allRequests: mainUsage.reduce((total, usage) => total + sum3(usage), 0),
    out: mainUsage.reduce((total, usage) => total + (usage.output_tokens ?? 0), 0),
    resultUsage: sum3(result.usage), subtype: result.subtype, turns: result.num_turns, cost: result.total_cost_usd,
    duration: result.duration_ms, isError: result.is_error,
    denials: (result.permission_denials ?? []).map((each) => label(each.tool_name ?? '?')),
    requestLines,
    serverCalls: requestLines ? requestLines.filter((each) => each.startsWith('tools/call')).length : null,
    moreLines: (read(join(lab, 'server', 'requests-more.txt')) ?? '').trim().split('\n').filter(Boolean).length,
  };
}

const sessions = process.argv.slice(2).map(digest);
for (const s of sessions) {
  const sc = s.score;
  console.log(`== ${s.name} | model ${s.model} | Claude Code ${s.version} | permission mode ${s.permissionMode}`);
  console.log(`   result ${s.subtype} (is_error ${s.isError}), ${s.turns} turns, ${s.duration} ms, cost USD ${s.cost} | permission denials ${s.denials.length}${s.denials.length ? ` (${s.denials.join(', ')})` : ''}`);
  console.log(`   built-in tools offered (${s.builtin.length}): ${s.builtin.join(' ') || 'none'} | ToolSearch listed: ${yes(s.builtin.includes('ToolSearch'))}`);
  console.log(`   MCP servers on the init line: ${s.hasServersKey ? '' : '(no mcp_servers key) '}the seed's ${s.serversOurs.length} (${s.serversOurs.join(', ') || 'none'}) + any other ${s.serversOther} | entries skipped at start-up: ${s.serverErrors.length}${s.serverErrors.length ? ` (${s.serverErrors.join(', ')})` : ''}`);
  console.log(`   MCP tools on the init line: the seed's ${s.mcpOurs.length} (${s.mcpOurs.join(' ') || 'none'}) + any other ${s.mcpOther}`);
  console.log(`   not shipped with Claude Code: plugins ${s.pluginsOther} | skills ${s.skillsOther} of ${s.skillsTotal} | agents ${s.agentsOther} of ${s.agentsTotal}`);
  console.log(`   models on the messages: ${[...s.models].join(', ') || 'none seen'}`);
  for (const entry of s.perModel) console.log(`      modelUsage ${entry}`);
  for (const entry of s.timeline) console.log(`   ${entry}`);
  console.log(`   tool calls: to the seed's MCP tools ${s.calls.ours} (answered with an error: ${s.calls.oursError}) | ToolSearch ${s.calls.search} | other built-in ${s.calls.builtin} | to any other MCP server ${s.calls.foreign} | tool-result characters ${s.resultChars}`);
  console.log(`   the server's own record: ${s.requestLines === null ? 'no requests.txt (the process never started)' : `${s.requestLines.length} lines, tools/call ${s.serverCalls} | ${s.requestLines.filter((each) => !each.startsWith('tools/call')).join(' > ')}`}${s.moreLines ? ` | requests-more.txt ${s.moreLines} lines` : ''}`);
  console.log(`   the stream and the server agree on the number of calls: ${s.serverCalls === null ? 'nothing to compare' : yes(s.serverCalls === s.calls.ours)} (stream ${s.calls.ours}, server ${s.serverCalls ?? '-'}; a denied call reaches the stream but not the server)`);
  console.log(`   system lines by subtype: ${Object.entries(s.subtypes).map(([subtype, count]) => `${subtype} ${count}`).join(', ') || 'none'}`);
  console.log(`   requests: ${s.requests} | first request ${s.first} tokens | last request ${s.last} tokens | all requests added up ${s.allRequests} | output ${s.out} | result line usage ${s.resultUsage}`);
  console.log(`   final reply (${s.reply.length} chars): shelf ${truth.asked.shelf} ${yes(sc.shelf)} | left ${truth.asked.left} ${yes(sc.left)} | low stock named ${sc.low.length} of ${LOW.length} (${sc.low.join(' ') || 'none'}) | at exactly ${truth.below}: ${sc.atLimit.join(' ') || 'none'} | other real codes: ${sc.otherReal.join(' ') || 'none'} | codes not in the file: ${sc.madeUp.join(' ') || 'none'} | other shelves: ${sc.wrongShelves.join(' ') || 'none'} | ${truth.missing} named: ${yes(sc.missingNamed)}`);
  console.log(`   scored: all right ${yes(sc.right)} | offered an answer ${yes(sc.offered)}`);
  for (const line of s.reply.split('\n').filter((each) => each.trim()).slice(0, 10)) console.log(`      | ${s.mask(line).slice(0, 120)}`);
}
if (sessions.length > 1) {
  console.log('\nname | seed servers | other servers | MCP tools listed | seed tool calls | errors | ToolSearch | server tools/call | denials | all right | offered | requests | first request | last request | all requests | output | cost USD | turns | ms');
  for (const s of sessions) {
    console.log([s.name, s.serversOurs.join('+') || '-', s.serversOther, s.mcpOurs.length, s.calls.ours, s.calls.oursError, s.calls.search, s.serverCalls ?? '-', s.denials.length,
      yes(s.score.right), yes(s.score.offered), s.requests, s.first, s.last, s.allRequests, s.out, s.cost, s.turns, s.duration].join(' | '));
  }
}
