// Runs ctx-cost.mjs on made-up streams and checks every figure it prints. No session, no model:
// the streams are written here, in the shape earlier videos' records showed (one init event,
// assistant lines that repeat a message id when tools run in parallel, lines under an Agent
// call, a message marked synthetic, an Agent call put in the background whose report arrives as
// a task notification, an Agent call that ran in the foreground whose report is in its tool
// result and is repeated as a task notification, hook responses, the other system subtypes a
// working session carries, a line Claude Code wrote itself, and a rate-limit event that must
// never be read).
// Usage: node <seed>/check-ctx-cost.mjs
import { spawnSync } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'ctx-cost-check-'));
const usage = (input, write, read) => ({ input_tokens: input, cache_creation_input_tokens: write, cache_read_input_tokens: read, output_tokens: 1 });
const init = (extra = {}) => ({
  type: 'system', subtype: 'init', claude_code_version: '0.0.0-made-up', model: 'made-up-model', permissionMode: 'default',
  tools: ['Read', 'Edit', 'ToolSearch'], mcp_servers: [], skills: ['one', 'two', 'private-skill-x'], agents: ['Explore', 'private-agent-y'],
  slash_commands: ['one', 'two'], plugins: [{ name: 'private-plugin-z', path: '/nowhere' }], ...extra,
});
const say = (id, use, content, parent = null, model = 'made-up-model') => ({ type: 'assistant', parent_tool_use_id: parent, message: { id, model, usage: use, content } });
const back = (content, extra = {}, parent = null) => ({ type: 'user', parent_tool_use_id: parent, message: { role: 'user', content }, ...extra });
const sys = (subtype, extra = {}) => ({ type: 'system', subtype, ...extra });
const result = (use, cost, extra = {}) => ({ type: 'result', subtype: 'success', num_turns: 1, total_cost_usd: cost, usage: use, modelUsage: { 'made-up-model': {} }, result: 'ok', ...extra });
const limit = { type: 'rate_limit_event', rate_limit_info: { note: 'this line must never be read', utilization: 0.99 } };
const one = (use) => [init(), limit, say('m1', use, [{ type: 'text', text: '十二個月' }]), result(use, 0.01)];

// A working session: a skill call and an Agent call in one response (the Agent call goes to the
// background and its report arrives later as a task notification), then a tool of an MCP server.
const work = [
  init({ tools: ['Read', 'Edit', 'ToolSearch', 'mcp__secretsrv__peek'], mcp_servers: [{ name: 'secretsrv', status: 'connected' }] }),
  limit,
  say('w1', usage(6, 494, 9000), [{ type: 'thinking', thinking: '...' }, { type: 'tool_use', id: 't1', name: 'Skill', input: { skill: 'one' } }]),
  say('w1', usage(6, 494, 9000), [{ type: 'tool_use', id: 't2', name: 'Agent', input: { subagent_type: 'private-agent-y', prompt: 'x'.repeat(50) } }]),
  sys('hook_started', { hook_name: 'PreToolUse:Skill' }),
  sys('hook_response', { hook_name: 'PreToolUse:Skill', exit_code: 0, outcome: 'success', stdout: '', stderr: '' }),
  sys('hook_started', { hook_name: 'SubagentStart:private-agent-y' }),
  sys('hook_response', { hook_name: 'SubagentStart:private-agent-y', exit_code: 0, outcome: 'success', stdout: 'hello', stderr: '' }),
  back([{ type: 'tool_result', tool_use_id: 't1', content: 'Launching skill: one' }]),
  back([{ type: 'text', text: 'B'.repeat(600) }], { isSynthetic: true }),
  back([{ type: 'tool_result', tool_use_id: 't2', content: [{ type: 'text', text: 'A'.repeat(1028) }] }], { tool_use_result: { isAsync: true, status: 'async_launched' } }),
  sys('task_started', { tool_use_id: 't2' }), sys('background_tasks_changed'),
  say('s1', usage(3, 2997, 0), [{ type: 'text', text: 'in the subagent' }], 't2'),
  say('w2', usage(8, 1492, 9500), [{ type: 'tool_use', id: 't3', name: 'mcp__secretsrv__peek', input: {} }]),
  back([{ type: 'tool_result', tool_use_id: 't3', is_error: true, content: 'E'.repeat(40) }]),
  sys('task_progress', { tool_use_id: 't2' }), sys('task_progress', { tool_use_id: 't2' }), sys('task_updated', { tool_use_id: 't2' }),
  sys('task_notification', { tool_use_id: 't2', status: 'completed', summary: 'N'.repeat(62) }),
  sys('task_summary'), sys('task_summary'), sys('post_turn_summary'), sys('thinking_tokens', { tokens: 5 }), sys('background_tasks_changed'),
  say('w3', usage(5, 495, 11000), [{ type: 'text', text: 'T'.repeat(100) }]),
  result(usage(19, 2481, 29500), 0.05),
  result(usage(5, 495, 11000), 0.06),
];
// An Agent call that ran in the foreground, as the subagents video's records describe one: the
// tool result holds the report (1,266 characters, 658 of them the report), and the stream also
// carries a task notification whose summary is the same report. Here the notification comes
// before the tool result, the harder order.
const report = 'R'.repeat(658);
const fore = [
  init({ tools: ['Read', 'Agent'] }),
  say('f1', usage(5, 100, 9000), [{ type: 'tool_use', id: 'a1', name: 'Agent', input: { subagent_type: 'private-agent-y', prompt: 'p' } }]),
  sys('task_started', { tool_use_id: 'a1' }),
  say('g1', usage(2, 1110, 3048), [{ type: 'text', text: report }], 'a1'),
  sys('task_notification', { tool_use_id: 'a1', status: 'completed', summary: report }),
  back([{ type: 'tool_result', tool_use_id: 'a1', content: [{ type: 'text', text: 'F'.repeat(1266 - 658) + report }] }], { tool_use_result: { status: 'completed' } }),
  say('f2', usage(5, 600, 9105), [{ type: 'text', text: 'done' }]),
  result(usage(10, 700, 18105), 0.1),
];
// A line Claude Code wrote itself (model "<synthetic>", usage all zero), then a real request.
const own = [
  init(),
  say('x0', usage(0, 0, 0), [{ type: 'text', text: 'a notice written by Claude Code' }], null, '<synthetic>'),
  say('x1', usage(5, 100, 9000), [{ type: 'text', text: 'twelve' }]),
  result(usage(5, 100, 9000), 0.01, { is_error: true }),
];
const streams = {
  'made-base': one(usage(10, 9000, 0)),
  'made-base2': one(usage(10, 0, 9003)),
  'made-part': one(usage(4, 120, 9000)),
  'made-work': work,
};
const more = {
  'made-fore': fore,
  'made-own': own,
  'made-same': one(usage(10, 9000, 0)),
  'made-same2': one(usage(10, 0, 9000)),
  'made-near': one(usage(4, 8, 9000)),
};
const put = (name, lines) => {
  const path = join(scratch, `${name}.stream.jsonl`);
  writeFileSync(path, `${lines.map((line) => JSON.stringify(line)).join('\n')}\nthis line is not JSON\n`);
  return path;
};
const paths = Object.entries(streams).map(([name, lines]) => put(name, lines));
const extra = Object.fromEntries(Object.entries(more).map(([name, lines]) => [name, put(name, lines)]));
// What Windows PowerShell 5.1 writes for `claude -p ... > with.jsonl`: UTF-16LE with a BOM.
const wide = join(scratch, 'made-utf16.jsonl');
writeFileSync(wide, Buffer.concat([Buffer.from([0xff, 0xfe]), Buffer.from(`${streams['made-part'].map((line) => JSON.stringify(line)).join('\r\n')}\r\n`, 'utf16le')]));

const run = (files, flags) => spawnSync(process.execPath, [join(seed, 'ctx-cost.mjs'), ...files, ...flags], { encoding: 'utf8' });
const plain = run(paths, ['--base', 'made-base,made-base2']);
const named = run(paths, ['--base', 'made-base', '--names', '--quiet']);
const shapes = run([extra['made-fore'], extra['made-own']], []);
const detail = run([paths[3]], ['--system']);
const same = [extra['made-same'], extra['made-same2'], extra['made-near']];
const floored = run(same, ['--base', 'made-same,made-same2', '--floor', '11', '--quiet']);
const bare = run(same, ['--base', 'made-same,made-same2', '--quiet']);
const utf16 = run([wide], []);
process.stdout.write(plain.stdout);
console.log('--- the same four streams with --base made-base --names --quiet ---');
process.stdout.write(named.stdout);
console.log('--- a foreground Agent call, and a line Claude Code wrote itself ---');
process.stdout.write(shapes.stdout);
console.log('--- made-work again with --system: the other system lines by subtype ---');
{
  // Only the lists: each "other system lines" line and the lines it wraps onto.
  const all = detail.stdout.split('\n');
  all.forEach((line, at) => {
    if (!line.includes('other system lines')) return;
    console.log(line);
    for (let next = at + 1; next < all.length && all[next].startsWith('         '); next += 1) console.log(all[next]);
  });
}
console.log('--- two equal base runs and a run 2 away, with --floor 11 --quiet, then without --floor ---');
process.stdout.write(floored.stdout);
process.stdout.write(bare.stdout);
console.log('--- a stream saved as UTF-16 ---');
process.stdout.write(utf16.stdout);
console.log(`[exit ${utf16.status}]`);

const out = plain.stdout;
const every = [plain, shapes, detail, floored, bare, utf16].map((each) => each.stdout).join('\n');
const tooWide = every.split('\n').filter((line) => line.length > 78 && !line.startsWith('base:'));
const checks = [
  ['exit 0 and nothing on stderr', [plain, named, shapes, detail, floored, bare].every((each) => each.status === 0 && !each.stderr)],
  ['the three usage fields are added up: 10 + 9,000 + 0 = 9,010', out.includes('request 1: 10 + 9,000 + 0 = 9,010')],
  ['the same total from another split: 10 + 0 + 9,003 = 9,013', out.includes('request 1: 10 + 0 + 9,003 = 9,013')],
  ['two base runs give a mean and a spread', out.includes('base: made-base, made-base2 | first request 9,010, 9,013 | mean 9,011.5 | spread 3')],
  ['a difference is taken from the mean of the base', out.includes('made-part | 1 | 9,124 = 4 + 120 + 9,000 | +112.5 |')],
  ['a message id repeated for parallel tool calls counts once: three requests', out.includes('first 9,500 | last 11,500 | grew +2,000 over 3 requests')],
  ['growth is printed per request', out.includes('= 11,000 (+1,500)') && out.includes('= 11,500 (+500)')],
  ['what Claude wrote before the next request', out.includes('-- after request 1: Claude wrote 0 chars of text, 2 tool calls') && out.includes('tool calls: Skill, Agent (inputs 112 chars)')],
  ['tool results as character counts, one a line', out.includes('tool result Skill: 20 chars') && out.includes('tool result Agent: 1,028 chars (launched in the background)')],
  ['a message marked synthetic is listed with its size', out.includes('added by Claude Code (synthetic): 600 chars')],
  ['a background report is listed as a task notification with its size', out.includes('task notification: 62 chars')],
  ['a foreground report is listed once: in the Agent tool result, not again as a notification',
    shapes.stdout.includes('tool result Agent: 1,266 chars (the report is in it)') && shapes.stdout.includes('task notification: same report as in the Agent tool result') && !/task notification: \d/.test(shapes.stdout)],
  ['hook output is counted, and a name that is not a tool is hidden', out.includes('hooks ran, main and under Agent: 2 | with output: 1') && out.includes('SubagentStart:(a name) exit 0: stdout 5, stderr 0 chars')],
  ['an errored MCP result is shown without the server name', out.includes('tool result mcp__(a server): 40 chars (error)')],
  ['requests under an Agent call are kept apart', out.includes('under Agent calls: 1 request of their own | largest input side 3,000')],
  ['other system lines are one count, and --system lists them by subtype', out.includes('other system lines: 4') && out.includes('other system lines: 8') && detail.stdout.includes('other system lines (8): task_progress 2, task_updated 1, task_summary 2,')],
  ['both result lines are printed', out.includes('result 2: success')],
  ['a line Claude Code wrote itself is not request 1', shapes.stdout.includes('lines Claude Code wrote itself (no request behind them): 1') && shapes.stdout.includes('request 1: 5 + 100 + 9,000 = 9,105') && !shapes.stdout.includes('0 + 0 + 0')],
  ['a result line that is an error says so', shapes.stdout.includes('result 1: success (is_error)')],
  ['no name of a skill, agent, server or plugin without --names', !/secretsrv|private-/.test(every)],
  ['the rate-limit event is never printed', !/utilization|never be read|rate_limit/.test(every + named.stdout)],
  ['--names prints them, --quiet keeps only the table', named.stdout.startsWith('base: made-base |') && !named.stdout.includes('== made-work')],
  ['one base run says there is no spread', named.stdout.includes('one run, no spread')],
  ['two equal base runs and --floor 11: a run 2 away is inside the bar', floored.stdout.includes('| spread 0') && floored.stdout.includes('bar: 11 (the larger of the spread and --floor 11)') && floored.stdout.includes('made-near | 1 | 9,012 = 4 + 8 + 9,000 | +2 (inside the bar) |')],
  ['without --floor the same run would be printed as a difference', bare.stdout.includes('made-near | 1 | 9,012 = 4 + 8 + 9,000 | +2 |')],
  ['a UTF-16 file is named as one, and the exit code is 2', utf16.status === 2 && utf16.stdout.includes('this file is UTF-16, not UTF-8') && !utf16.stdout.includes('--verbose')],
  ['no line a card may quote is wider than 78 columns', tooWide.length === 0],
];
let failed = 0;
for (const [label, ok] of checks) { if (!ok) failed += 1; console.log(`${ok ? 'ok  ' : 'FAIL'} ${label}`); }
if (tooWide.length) for (const line of tooWide) console.log(`     too wide (${line.length}): ${line}`);
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
