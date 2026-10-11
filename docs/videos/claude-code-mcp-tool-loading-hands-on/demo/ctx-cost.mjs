// Reads saved Claude Code streams and prints what each request of the main conversation carried.
//
//   claude -p "..." --output-format stream-json --verbose > one.jsonl
//   node ctx-cost.mjs one.jsonl [two.jsonl ...] [--base name[,name]] [--floor n]
//                     [--names] [--system] [--quiet]
//
// For every stream: the first request's input side (input + cache write + cache read, the three
// usage fields the API reports), every later request and how much it grew, and what arrived in
// between (tool results, messages Claude Code added, notices), each as a character count. A
// ToolSearch result is a list of tool references with no text: it is printed as that many
// references, not as characters.
// With two or more streams: one row per stream and the difference of each first request from
// the base. --base names the stream(s) to subtract (default: the first file); with two or more
// base streams the base is their mean and their spread is printed. A difference no larger than
// the spread is marked. --floor n sets the least a difference must exceed to count: the bar is
// the larger of the spread and n, which matters when two base runs happen to come out equal.
//
// It calls no model and reads nothing but the files it is given. Names of skills, agents, MCP
// servers and plugins are counted, not printed, unless --names is passed. System lines that are
// neither hooks nor task notices are a count; --system lists them by subtype. Rate-limit events
// are never read. Per-request output tokens are not used: the official cost-tracking page calls
// the per-step figure a placeholder, so output is taken from the result line only.
//
// Save the stream from Git Bash or a macOS or Linux terminal: Windows PowerShell's > writes
// UTF-16, which this script names and does not read.
import { readFileSync } from 'node:fs';
import { basename } from 'node:path';

const args = process.argv.slice(2);
const VALUED = ['--base', '--floor'];
const flag = (name) => args.includes(name);
const option = (name) => { const at = args.indexOf(name); return at >= 0 ? args[at + 1] : null; };
const files = args.filter((arg, at) => !arg.startsWith('--') && !VALUED.includes(args[at - 1]));
const showNames = flag('--names');
const showSystem = flag('--system');
const quiet = flag('--quiet');
const floor = Number(option('--floor') ?? 0);
if (!files.length || !Number.isFinite(floor) || floor < 0) {
  console.error('usage: node ctx-cost.mjs <stream.jsonl> [more.jsonl ...] [--base name[,name]] [--floor n] [--names] [--system] [--quiet]');
  process.exit(2);
}

const WIDTH = 78;
const num = (value) => Number(value ?? 0).toLocaleString('en-US');
const signed = (value) => `${value >= 0 ? '+' : '-'}${num(Math.abs(Math.round(value * 10) / 10))}`;
const side = (usage) => ({
  input: usage?.input_tokens ?? 0,
  write: usage?.cache_creation_input_tokens ?? 0,
  read: usage?.cache_read_input_tokens ?? 0,
});
const sum = (s) => s.input + s.write + s.read;
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((block) => (typeof block === 'string' ? block : block?.text ?? textOf(block?.content) ?? '')).join('\n')
    : content && typeof content === 'object' ? (content.text ?? '') : '');
const isMcp = (tool) => String(tool).startsWith('mcp__');
const isSpawn = (tool) => tool === 'Agent' || tool === 'Task';
const toolLabel = (tool) => (isMcp(tool) && !showNames ? 'mcp__(a server)' : String(tool));
// A hook's name is "Event" or "Event:what". For tool events the second half is a tool name; for
// any other event it can be an agent or a command name, which is only shown with --names.
const hookLabel = (value) => {
  const [event, ...rest] = String(value ?? '?').split(':');
  if (!rest.length || showNames) return String(value ?? '?');
  const what = rest.join(':');
  if (/^(Pre|Post)ToolUse|^PermissionRequest/.test(event)) return `${event}:${toolLabel(what)}`;
  return event === 'SessionStart' && /^(startup|resume|clear|compact|fork)$/.test(what) ? `${event}:${what}` : `${event}:(a name)`;
};
const nameOf = (file) => basename(file).replace(/\.stream\.jsonl$|\.jsonl$|\.json$/, '');
const tally = (list) => { const out = {}; for (const each of list) out[each] = (out[each] ?? 0) + 1; return out; };
const listed = (counts) => Object.entries(counts).map(([key, count]) => (count > 1 ? `${key} x${count}` : key));
// A list that would pass 78 columns goes on as many lines as it needs.
function wrapped(indent, head, items, tail = '') {
  const lines = [];
  let line = `${indent}${head}`;
  items.forEach((item, at) => {
    const piece = `${item}${at < items.length - 1 ? ',' : tail}`;
    if (line.length + 1 + piece.length > WIDTH && line.length > indent.length + head.length) {
      lines.push(line);
      line = `${indent}   ${piece}`;
    } else line += ` ${piece}`;
  });
  lines.push(line);
  return lines;
}

function read(file) {
  const name = nameOf(file);
  const bytes = readFileSync(file);
  const utf16 = (bytes[0] === 0xff && bytes[1] === 0xfe) || (bytes[0] === 0xfe && bytes[1] === 0xff) || bytes.subarray(0, 4096).includes(0);
  const lines = utf16 ? [] : bytes.toString('utf8').replace(/^﻿/, '').split('\n').filter(Boolean).flatMap((line) => {
    try { return [JSON.parse(line)]; } catch { return []; }
  }).filter((line) => line.type !== 'rate_limit_event');
  const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
  const results = lines.filter((line) => line.type === 'result');
  const requests = [];           // main conversation, one per API response
  const byId = new Map();
  const toolOf = new Map();      // tool_use_id -> tool name
  const spawned = new Map();     // tool_use_id of an Agent call -> 'background' or 'foreground'
  const under = new Map();       // subagent requests: message id -> usage
  let own = 0;                   // assistant lines Claude Code wrote itself: no request behind them
  let current = null;            // what arrived since the last main request
  const fresh = () => ({ results: [], added: [], notices: [], hooks: [], other: {} });
  let pending = fresh();
  for (const line of lines) {
    const parent = line.parent_tool_use_id ?? null;
    if (line.type === 'assistant') {
      const message = line.message ?? {};
      if (parent) { if (message.id && message.usage) under.set(message.id, message.usage); continue; }
      if (!message.id || !message.usage) continue;
      // A notice Claude Code writes itself (a limit, an API error) is an assistant line with the
      // model "<synthetic>" and a usage of zero: it is not a request.
      if (message.model === '<synthetic>' || sum(side(message.usage)) === 0) { if (!byId.has(message.id)) own += 1; byId.set(message.id, null); continue; }
      if (!byId.has(message.id)) {
        current = { id: message.id, model: message.model, usage: side(message.usage), before: pending, calls: [], text: 0, thinking: 0 };
        pending = fresh();
        byId.set(message.id, current);
        requests.push(current);
      }
      const request = byId.get(message.id);
      for (const block of message.content ?? []) {
        if (block.type === 'tool_use') {
          toolOf.set(block.id, block.name);
          request.calls.push({ tool: block.name, chars: JSON.stringify(block.input ?? {}).length });
        } else if (block.type === 'text') request.text += String(block.text ?? '').length;
        else if (block.type === 'thinking' || block.type === 'redacted_thinking') request.thinking += 1;
      }
      continue;
    }
    if (line.type === 'user' && !parent) {
      const content = line.message?.content;
      const blocks = Array.isArray(content) ? content : [{ type: 'text', text: textOf(content) }];
      for (const block of blocks) {
        if (block.type === 'tool_result') {
          const tool = toolOf.get(block.tool_use_id) ?? '?';
          // An Agent call that was put in the background answers at once with a launch note
          // (isAsync true) and reports later; one that ran in the foreground answers with the
          // report itself (status completed, no isAsync).
          const how = line.tool_use_result ?? {};
          if (isSpawn(tool)) spawned.set(block.tool_use_id, how.isAsync === true || how.status === 'async_launched' ? 'background' : 'foreground');
          // A ToolSearch result holds no text: it is a list of tool_reference blocks, each naming
          // one deferred tool whose definition is loaded from then on. They are counted as
          // references; only the blocks that carry text count as characters.
          const inner = Array.isArray(block.content) ? block.content : [];
          const refs = inner.filter((each) => each?.type === 'tool_reference').map((each) => String(each.tool_name ?? '?'));
          const chars = refs.length ? textOf(inner.filter((each) => each?.type !== 'tool_reference')).length : textOf(block.content).length;
          pending.results.push({ id: block.tool_use_id, tool, chars, refs, error: Boolean(block.is_error) });
        } else {
          const chars = textOf(block.text ?? block.content ?? block).length;
          if (chars) pending.added.push({ chars, synthetic: Boolean(line.isSynthetic) });
        }
      }
      continue;
    }
    if (line.type === 'system' && line.subtype !== 'init') {
      if (line.subtype === 'task_notification') {
        pending.notices.push({ id: line.tool_use_id ?? null, chars: String(line.summary ?? line.result ?? '').length });
      } else if (line.subtype === 'hook_response') {
        const out = String(line.stdout ?? '').length;
        const err = String(line.stderr ?? '').length;
        pending.hooks.push({ name: hookLabel(line.hook_name ?? line.hook_event), code: line.exit_code, out, err });
      } else pending.other[line.subtype] = (pending.other[line.subtype] ?? 0) + 1;
    }
  }
  const servers = init.mcp_servers ?? [];
  const tools = init.tools ?? [];
  const last = results.at(-1) ?? {};
  return {
    name, utf16, init, requests, own, spawned, trailing: pending, under: [...under.values()].map((usage) => sum(side(usage))),
    lists: {
      'built-in tools': tools.filter((tool) => !isMcp(tool)).length,
      'MCP tools': tools.filter(isMcp).length,
      'MCP servers': servers.length,
      skills: (init.skills ?? []).length,
      agents: (init.agents ?? []).length,
      'slash commands': (init.slash_commands ?? []).length,
      plugins: (init.plugins ?? []).length,
    },
    servers: tally(servers.map((server) => server.status ?? '?')),
    results, last,
    models: [...new Set(requests.map((request) => request.model).filter(Boolean))],
  };
}

// What arrived after one request and before the next, one item a line.
function between(before, spawned, indent) {
  const parts = [];
  for (const each of before.results) {
    const how = spawned.get(each.id);
    const note = each.error ? ' (error)' : how === 'background' ? ' (launched in the background)' : how === 'foreground' ? ' (the report is in it)' : '';
    if (each.refs?.length) {
      const n = each.refs.length;
      parts.push(`${indent}tool result ${toolLabel(each.tool)}: ${n} tool reference${n === 1 ? '' : 's'}, ${num(each.chars)} chars of text${note}`);
      if (showNames) parts.push(...wrapped(indent, '   referenced (--names):', each.refs));
    } else parts.push(`${indent}tool result ${toolLabel(each.tool)}: ${num(each.chars)} chars${note}`);
  }
  for (const each of before.added) parts.push(`${indent}added by Claude Code${each.synthetic ? ' (synthetic)' : ''}: ${num(each.chars)} chars`);
  // A foreground Agent call's report is already in its tool result; the stream repeats it as a
  // task notification, which is not a second arrival.
  for (const each of before.notices) {
    parts.push(spawned.get(each.id) === 'foreground'
      ? `${indent}task notification: same report as in the Agent tool result`
      : `${indent}task notification: ${num(each.chars)} chars`);
  }
  if (before.hooks.length) {
    const said = before.hooks.filter((hook) => hook.out + hook.err > 0);
    parts.push(`${indent}hooks ran, main and under Agent: ${before.hooks.length} | with output: ${said.length}`);
    for (const hook of said) parts.push(`${indent}   ${hook.name} exit ${hook.code}: stdout ${num(hook.out)}, stderr ${num(hook.err)} chars`);
  }
  const other = Object.entries(before.other);
  if (other.length) {
    const total = other.reduce((n, [, count]) => n + count, 0);
    if (showSystem) parts.push(...wrapped(indent, `other system lines (${total}):`, other.map(([subtype, count]) => `${subtype} ${count}`)));
    else parts.push(`${indent}other system lines: ${total}`);
  }
  return parts;
}

// Every line a card may quote stays inside 78 columns: three numbers and their sum.
function show(s) {
  const init = s.init;
  const l = s.lists;
  if (s.utf16) {
    console.log(`== ${s.name}`);
    console.log('   this file is UTF-16, not UTF-8 (Windows PowerShell\'s > saves that).');
    console.log('   Save the stream again from Git Bash, or a macOS or Linux terminal.');
    return;
  }
  console.log(`== ${s.name} | Claude Code ${init.claude_code_version ?? '?'} | ${init.model ?? '?'} | mode ${init.permissionMode ?? '?'}`);
  console.log(`   init: built-in tools ${l['built-in tools']} | MCP servers ${l['MCP servers']}${l['MCP servers'] ? ` (${listed(s.servers).join(', ')})` : ''}, tools ${l['MCP tools']}`);
  console.log(`         skills ${l.skills} | agents ${l.agents} | slash commands ${l['slash commands']} | plugins ${l.plugins}`);
  if (showNames) {
    const names = (list) => (list ?? []).map((each) => (typeof each === 'string' ? each : each.name)).join(', ') || 'none';
    for (const key of ['tools', 'mcp_servers', 'skills', 'agents', 'plugins']) console.log(`   ${key} (--names): ${names(init[key])}`);
  }
  if (s.own) console.log(`   lines Claude Code wrote itself (no request behind them): ${s.own}`);
  if (!s.requests.length) { console.log('   no request of the main conversation carries usage (was it made with --verbose?)'); return; }
  console.log('   each request: input + cache write + cache read = input side');
  s.requests.forEach((request, at) => {
    const u = request.usage;
    const total = sum(u);
    const parts = between(request.before, s.spawned, '      ');
    if (at) {
      const prior = s.requests[at - 1];
      console.log(`   -- after request ${at}: Claude wrote ${num(prior.text)} chars of text, ${prior.calls.length} tool call${prior.calls.length === 1 ? '' : 's'}`);
      if (prior.calls.length) {
        const inputs = ` (inputs ${num(prior.calls.reduce((n, call) => n + call.chars, 0))} chars)`;
        for (const line of wrapped('      ', 'tool calls:', listed(tally(prior.calls.map((call) => toolLabel(call.tool)))), inputs)) console.log(line);
      }
    } else if (parts.length) console.log('   -- before request 1:');
    for (const part of parts) console.log(part);
    console.log(`   request ${at + 1}: ${num(u.input)} + ${num(u.write)} + ${num(u.read)} = ${num(total)}${at ? ` (${signed(total - sum(s.requests[at - 1].usage))})` : ''}`);
  });
  const first = sum(s.requests[0].usage);
  const final = sum(s.requests.at(-1).usage);
  console.log(`   first ${num(first)} | last ${num(final)} | grew ${signed(final - first)} over ${s.requests.length} request${s.requests.length > 1 ? 's' : ''}`);
  if (s.requests.length > 1) console.log(`   all ${s.requests.length} requests' input sides added up: ${num(s.requests.reduce((n, request) => n + sum(request.usage), 0))}`);
  const tail = between(s.trailing, s.spawned, '      ');
  if (tail.length) { console.log('   -- after the last request:'); for (const part of tail) console.log(part); }
  if (s.under.length) console.log(`   under Agent calls: ${s.under.length} request${s.under.length > 1 ? 's' : ''} of their own | largest input side ${num(Math.max(...s.under))}`);
  s.results.forEach((result, at) => {
    const u = result.usage ?? {};
    const models = Object.keys(result.modelUsage ?? {});
    console.log(`   result ${at + 1}: ${result.subtype}${result.is_error ? ' (is_error)' : ''} | turns ${result.num_turns} | cost USD ${result.total_cost_usd ?? '?'}`);
    console.log(`      usage ${num(u.input_tokens)} + ${num(u.cache_creation_input_tokens)} + ${num(u.cache_read_input_tokens)}, output ${num(u.output_tokens)} | models in modelUsage: ${models.length}${showNames ? ` (${models.join(', ')})` : ''}`);
  });
}

const streams = files.map(read);
for (const s of streams) if (!quiet || s.utf16) show(s);
if (streams.some((s) => s.utf16)) process.exitCode = 2;

if (streams.length > 1) {
  const wanted = (option('--base') ?? streams[0].name).split(',');
  const base = streams.filter((s) => wanted.includes(s.name) && s.requests.length);
  if (!base.length) { console.error(`--base: no stream named ${wanted.join(', ')} with a request in it`); process.exit(2); }
  const firsts = base.map((s) => sum(s.requests[0].usage));
  const mean = firsts.reduce((a, b) => a + b, 0) / firsts.length;
  const spread = Math.max(...firsts) - Math.min(...firsts);
  const bar = Math.max(spread, floor);
  if (!quiet) console.log('');
  console.log(`base: ${base.map((s) => s.name).join(', ')} | first request ${firsts.map(num).join(', ')}${base.length > 1 ? ` | mean ${num(Math.round(mean * 10) / 10)} | spread ${num(spread)}` : ' | one run, no spread'}`);
  if (floor > 0) console.log(`bar: ${num(bar)} (the larger of the spread and --floor ${num(floor)})`);
  console.log('name | requests | first = input + write + read | minus base | last | grew');
  for (const s of streams) {
    if (s.utf16) { console.log(`${s.name} | not read: the file is UTF-16`); continue; }
    if (!s.requests.length) { console.log(`${s.name} | 0 | - | - | - | -`); continue; }
    const u = s.requests[0].usage;
    const first = sum(u);
    const final = sum(s.requests.at(-1).usage);
    const diff = first - mean;
    const inside = (base.length > 1 || floor > 0) && Math.abs(diff) <= bar;
    const note = wanted.includes(s.name) ? '(base)' : inside ? `${signed(diff)} (inside the ${floor > 0 ? 'bar' : 'spread'})` : signed(diff);
    console.log(`${s.name} | ${s.requests.length} | ${num(first)} = ${num(u.input)} + ${num(u.write)} + ${num(u.read)} | ${note} | ${num(final)} | ${signed(final - first)}`);
  }
}
