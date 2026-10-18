// Builds four MADE-UP sessions in a temporary folder (a stream in the shape the official headless
// and Agent SDK pages describe, and the project each would have left) and runs tally.mjs on them.
// It checks the parser and the scoring rule: one session that found the tools through ToolSearch
// and called both, one with no server that made an answer up, one whose call was denied, and one
// that also carried a server that is not the seed's (which must be counted and never named).
// The shape of a ToolSearch call and of its result are guesses from the documentation that the
// first real session confirms or corrects. It is not evidence of anything a model did, and the
// made-up files are deleted when it ends. No session, no model.
// Usage: node <seed>/check-tally.mjs
import { spawnSync } from 'node:child_process';
import { cpSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const truth = JSON.parse(readFileSync(join(here, 'truth.json'), 'utf8'));
const scratch = mkdtempSync(join(tmpdir(), 'gear-lab-tally-'));
const cwd = join(scratch, 'gear-lab');
const GEAR = ['mcp__gear__find_gear', 'mcp__gear__low_stock'];
const init = (tools, servers) => ({
  type: 'system', subtype: 'init', cwd, model: 'made-up-model', claude_code_version: '0.0.0', permissionMode: 'default',
  tools, mcp_servers: servers, plugins: [], skills: ['verify', 'debug'], agents: ['Explore', 'Plan'],
});
let ids = 0;
const usage = (read) => ({ input_tokens: 3, cache_creation_input_tokens: 500, cache_read_input_tokens: read, output_tokens: 10 });
const call = (name, input, read) => { ids += 1; return { type: 'assistant', parent_tool_use_id: null, message: { id: `m${ids}`, model: 'made-up-model', usage: usage(read), content: [{ type: 'tool_use', id: `toolu_madeup${ids}`, name, input }] } }; };
const back = (content, isError) => ({ type: 'user', parent_tool_use_id: null, message: { content: [{ type: 'tool_result', tool_use_id: `toolu_madeup${ids}`, content, ...(isError === undefined ? {} : { is_error: isError }) }] } });
const say = (text, read) => { ids += 1; return { type: 'assistant', parent_tool_use_id: null, message: { id: `m${ids}`, model: 'made-up-model', usage: usage(read), content: [{ type: 'text', text }] } }; };
const result = (text, denials = []) => ({
  type: 'result', subtype: 'success', is_error: false, num_turns: 3, duration_ms: 1, permission_denials: denials, result: text, total_cost_usd: 0,
  usage: { input_tokens: 9, cache_creation_input_tokens: 1500, cache_read_input_tokens: 20000, output_tokens: 90 },
  modelUsage: { 'made-up-model': { inputTokens: 9, outputTokens: 90, cacheReadInputTokens: 20000, cacheCreationInputTokens: 1500 } },
});
const lowText = truth.low.map((each) => `${each.code} ${each.name} 剩 ${each.left}`).join('\n');
const good = `${truth.asked.code} 在貨架 ${truth.asked.shelf}，還剩 ${truth.asked.left} 個。\n低於 ${truth.below} 的：${truth.low.map((each) => each.code).join('、')}`;
const sessions = {
  'made-up-on': {
    requests: ['start', 'initialize asks 2025-11-25', 'notifications/initialized', 'tools/list', 'tools/call find_gear {"code":"G-417"}', 'tools/call low_stock {"below":3}', 'end'],
    stream: [init(['ToolSearch', ...GEAR], [{ name: 'gear', status: 'connected' }]),
      call('ToolSearch', { query: 'select:mcp__gear__find_gear,mcp__gear__low_stock', max_results: 5 }, 6000),
      back(GEAR.map((tool) => ({ type: 'tool_reference', tool_name: tool }))),
      call(GEAR[0], { code: truth.asked.code }, 6400), back([{ type: 'text', text: `${truth.asked.code} ${truth.asked.name}｜貨架 ${truth.asked.shelf}｜剩 ${truth.asked.left}` }], false),
      call(GEAR[1], { below: truth.below }, 6500), back([{ type: 'text', text: lowText }], false),
      say(good, 6700), result(good)],
  },
  'made-up-off': {
    requests: null,
    stream: [init(['ToolSearch'], []), say('made up', 6000), result(`${truth.asked.code} 應該在 B-02，大概還有 5 個。G-001 也快沒了。`)],
  },
  'made-up-denied': {
    requests: ['start', 'initialize asks 2025-11-25', 'notifications/initialized', 'tools/list', 'end'],
    stream: [init(['ToolSearch', ...GEAR], [{ name: 'gear', status: 'connected' }]),
      call(GEAR[0], { code: truth.asked.code }, 6400), back(`made-up denial that names ${cwd}`, true),
      say('made up', 6500), result('我沒有權限使用這個工具。', [{ tool_name: GEAR[0] }])],
  },
  'made-up-foreign': {
    requests: ['start', 'initialize asks 2025-11-25', 'notifications/initialized', 'tools/list', 'end'],
    stream: [init(['ToolSearch', ...GEAR, 'mcp__somebody__private_tool'], [{ name: 'gear', status: 'connected' }, { name: 'somebody', status: 'connected' }]),
      call('mcp__somebody__private_tool', { secret: 'never shown' }, 6400), back('never shown either', false),
      say('made up', 6500), result('made up')],
  },
};
const files = [];
for (const [name, each] of Object.entries(sessions)) {
  const lab = join(scratch, `${name}.lab`);
  mkdirSync(join(lab, 'server'), { recursive: true });
  cpSync(join(here, 'variants', 'mcp.project.json'), join(lab, '.mcp.json'));
  if (each.requests) writeFileSync(join(lab, 'server', 'requests.txt'), each.requests.map((line, at) => `${String(at + 1).padStart(2, '0')} +${String(at * 7).padStart(6)}ms ${line}\n`).join(''));
  const file = join(scratch, `${name}.stream.jsonl`);
  writeFileSync(file, each.stream.map((line) => JSON.stringify(line)).join('\n'));
  files.push(file);
}
const run = spawnSync(process.execPath, [join(here, 'tally.mjs'), ...files], { encoding: 'utf8' });
process.stdout.write(run.stdout);
process.stderr.write(run.stderr);
let failed = run.status !== 0;
if (run.stdout.includes('somebody') || run.stdout.includes('never shown') || run.stdout.includes(scratch)) { console.log('LEAK: a name, a value or a path that must not be printed is in the output'); failed = true; }
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
