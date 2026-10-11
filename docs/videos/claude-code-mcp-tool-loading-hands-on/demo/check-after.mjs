// Runs the three after-session readers (runner/after.mjs, runner/debug-seen.mjs, runner/said.mjs)
// and the rule script (runner/ladder.mjs) on made-up records and checks what they print.
// No session, no model: every stream, hook record, server record and debug record is written
// here, in the shape the previous video's records showed. The names that must never be printed
// are made up too (private-*, secretsrv).
// Usage: node <seed>/check-after.mjs
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'after-check-'));
const logs = join(scratch, 'logs');
const ladderLogs = join(scratch, 'ladder');
mkdirSync(logs); mkdirSync(ladderLogs);
const cwd = join(scratch, 'lab');
const SHIPPED = ['init', 'debug', 'loop'];
const BUILT = ['Task', 'Edit', 'Glob', 'Grep', 'Read', 'Skill', 'ToolSearch', 'Write'];
const gearTools = (count) => ['find_gear', 'low_stock', 'gear_kind', 'gear_rate', 'gear_deposit', 'gear_weight', 'gear_out', 'gear_checked', 'shelf_items', 'kind_items']
  .concat(Array.from({ length: 30 }, (_, at) => `made_tool_${'abcdefghijklmnopqrstuvwxyzabcd'[at]}`)).slice(0, count).map((tool) => `mcp__gear__${tool}`);
const usage = (input, write, read) => ({ input_tokens: input, cache_creation_input_tokens: write, cache_read_input_tokens: read, output_tokens: 1 });
const init = (extra = {}) => ({ type: 'system', subtype: 'init', claude_code_version: '0.0.0-made-up', model: 'claude-sonnet-made-up', permissionMode: 'default', cwd,
  tools: BUILT, mcp_servers: [], skills: SHIPPED, agents: ['Explore', 'Plan'], slash_commands: ['init', 'debug', 'loop', 'help'], plugins: [{ name: 'cc-plugin-made-up', path: '/nowhere' }], ...extra });
const say = (id, use, content) => ({ type: 'assistant', parent_tool_use_id: null, message: { id, model: 'claude-sonnet-made-up', usage: use, content } });
const back = (content, extra = {}) => ({ type: 'user', parent_tool_use_id: null, message: { role: 'user', content }, ...extra });
const result = (text, extra = {}) => ({ type: 'result', subtype: 'success', is_error: false, num_turns: 1, total_cost_usd: 0.01, usage: usage(1, 1, 1), modelUsage: { 'claude-sonnet-made-up': {} }, result: text, permission_denials: [], ...extra });
const limit = { type: 'rate_limit_event', rate_limit_info: { note: 'this line must never be read' } };
const withServer = (count, listed = count, status = 'connected', tools = BUILT) => init({ tools: [...tools, ...gearTools(listed)], mcp_servers: [{ name: 'gear', status }] });
const served = (count, more = []) => [`01 +     0ms start with ${count} of 40 tools`, '02 +     9ms initialize asks 2025-11-25', '03 +    11ms notifications/initialized', '04 +    15ms tools/list', ...more, '99 +  3000ms end'];

function put(dir, name, arm, stream, { seen = [], requests = null, debug = null, ended = true } = {}) {
  writeFileSync(join(dir, `${name}.stream.jsonl`), `${stream.map((line) => JSON.stringify(line)).join('\n')}\n`);
  writeFileSync(join(dir, `${name}.session.txt`), `# ${name} | arm ${arm} | start 2026-01-01T00:00:00Z\n${ended ? `# ${name} | end 2026-01-01T00:01:00Z\n` : ''}`);
  writeFileSync(join(dir, `${name}.seen.txt`), seen.length ? `${seen.join('\n')}\n` : '');
  if (requests) { mkdirSync(join(dir, `${name}.lab`, 'server'), { recursive: true }); writeFileSync(join(dir, `${name}.lab`, 'server', 'requests.txt'), `${requests.join('\n')}\n`); }
  if (debug) writeFileSync(join(dir, `${name}.debug.txt`), `${debug.join('\n')}\n`);
  writeFileSync(join(dir, `${name}.stderr.txt`), '');
}
const one = (first, use) => [first, limit, say('m1', use, [{ type: 'text', text: '十二個月' }]), result('一年有十二個月。')];
const noBuiltSearch = BUILT.filter((tool) => tool !== 'ToolSearch');
const refs = ['mcp__gear__find_gear'];
const used = [
  withServer(40), limit,
  say('k1', usage(2, 400, 9690), [{ type: 'tool_use', id: 's1', name: 'ToolSearch', input: { query: 'select:mcp__gear__find_gear', max_results: 5 } }]),
  back([{ type: 'tool_result', tool_use_id: 's1', content: refs.map((tool) => ({ type: 'tool_reference', tool_name: tool })) }], { tool_use_result: { matches: refs, query: 'select:mcp__gear__find_gear', total_deferred_tools: 40 } }),
  say('k2', usage(2, 310, 10090), [{ type: 'tool_use', id: 'c1', name: 'mcp__gear__find_gear', input: { code: 'G-417' } }]),
  back([{ type: 'tool_result', tool_use_id: 'c1', content: [{ type: 'text', text: 'G-417 頭燈｜貨架 D-07｜剩 37' }] }]),
  say('k3', usage(2, 80, 10400), [{ type: 'text', text: 'D-07，剩 37 個。' }]),
  result('G-417 在貨架 D-07，還剩 37 個。', { num_turns: 3 }),
];
const debugUsed = [
  '2026-01-01T00:00:00.000Z [DEBUG] [ToolSearch:optimistic] mode=tst, ENABLE_TOOL_SEARCH=undefined, result=true',
  '2026-01-01T00:00:01.000Z [DEBUG] Dynamic tool loading: 0/40 deferred tools included',
  '2026-01-01T00:00:02.000Z [DEBUG] ToolSearchTool: selected mcp__gear__find_gear',
  '2026-01-01T00:00:03.000Z [DEBUG] Dynamic tool loading: 1/40 deferred tools included',
  '2026-01-01T00:00:04.000Z [DEBUG] Dynamic tool loading: 1/40 deferred tools included',
  '2026-01-01T00:00:05.000Z [DEBUG] Tool search disabled: a made-up reason that names private-plugin-z',
  '2026-01-01T00:00:06.000Z [DEBUG] a made-up line about tool search in another shape, naming secretsrv',
  '2026-01-01T00:00:07.000Z [DEBUG] MCP server "gear" connected', '2026-01-01T00:00:08.000Z [DEBUG] MCP server "secretsrv" connected',
];
const away = resolve('/made-up/elsewhere/private.txt');
put(logs, 'c-base', 'base', one(init(), usage(2, 9010, 0)), { debug: ['x [DEBUG] [ToolSearch:optimistic] mode=tst, ENABLE_TOOL_SEARCH=undefined, result=true', 'x [DEBUG] Tool search disabled: no deferred tools available to search'] });
put(logs, 'c-d10', 'd10', one(withServer(10), usage(2, 770, 9010)), { requests: served(10) });
put(logs, 'c-u10', 'u10', one({ ...withServer(10, 10, 'connected', noBuiltSearch), permissionMode: 'manual' }, usage(2, 10258, 0)), { requests: served(10) });
put(logs, 'c-off', 'off', one(init({ tools: noBuiltSearch }), usage(2, 9010, 0)));
put(logs, 'c-use', 'use-d40', used, { requests: served(40, ['05 +  6100ms tools/call find_gear {"code":"G-417"}']), debug: debugUsed,
  seen: ['PreToolUse by=main id=0001 ToolSearch query=select:mcp__gear__find_gear max_results=5', 'PreToolUse by=main id=0002 mcp__gear__find_gear {"code":"G-417"}'] });
put(logs, 'c-mixed', 'd10', one(init({ tools: [...BUILT, ...gearTools(10), 'mcp__secretsrv__peek'], mcp_servers: [{ name: 'gear', status: 'connected' }, { name: 'secretsrv', status: 'connected' }],
  skills: [...SHIPPED, 'private-skill-x'], agents: ['Explore', 'private-agent-y'], plugins: [{ name: 'private-plugin-z' }] }), usage(2, 900, 9010)),
{ requests: served(10), seen: ['InstructionsLoaded session_start User (outside the project)'] });
put(logs, 'c-shell', 'base', one(init({ tools: [...BUILT, 'Bash'] }), usage(2, 9010, 0)));
put(logs, 'c-out', 'base', [init(), say('o1', usage(2, 9010, 0), [{ type: 'tool_use', id: 'r1', name: 'Read', input: { file_path: away } }]), result('x')],
  { seen: ['PreToolUse by=main id=0001 Read (outside the project) | BLOCKED'] });
put(logs, 'c-pending', 'd10', one(withServer(10, 0, 'pending'), usage(2, 100, 9010)), { requests: served(10) });
put(logs, 'c-wrong', 'd10', one(withServer(10, 2), usage(2, 100, 9010)), { requests: served(2) });
put(logs, 'c-listed0', 'd10', one(withServer(10, 0), usage(2, 100, 9010)), { requests: served(10) });
// An arm that is not in the mode it is named for, and the server with no tools.
put(logs, 'c-dplain', 'd10', one(withServer(10, 10, 'connected', noBuiltSearch), usage(2, 100, 9010)), { requests: served(10) });
put(logs, 'c-usearch', 'u10', one(withServer(10), usage(2, 100, 9010)), { requests: served(10) });
put(logs, 'c-offsearch', 'off', one(init(), usage(2, 9010, 0)));
put(logs, 'c-d0', 'd0', one(withServer(0, 0, 'connected', noBuiltSearch), usage(2, 30, 9010)), { requests: served(0) });

const run = (script, ...args) => spawnSync(process.execPath, [join(seed, 'runner', script), ...args], { encoding: 'utf8' });
const after = Object.fromEntries(['c-base', 'c-d10', 'c-u10', 'c-off', 'c-use', 'c-mixed', 'c-shell', 'c-out', 'c-pending', 'c-wrong', 'c-listed0', 'c-dplain', 'c-usearch', 'c-offsearch', 'c-d0'].map((name) => [name, run('after.mjs', join(logs, `${name}.stream.jsonl`))]));
const verdict = (name) => after[name].stdout.split('\n').find((line) => line.includes('verdict:')) ?? '';
const stops = (name) => (verdict(name).match(/STOP/g) ?? []).length;
for (const name of ['c-use', 'c-mixed']) { console.log(`--- after.mjs ${name} ---`); process.stdout.write(after[name].stdout.split('\n').map((line) => line.slice(0, 330)).join('\n')); }
console.log('--- the verdict of every made-up case, cut at 150 columns ---');
for (const name of Object.keys(after)) console.log(`${name}: STOP x${stops(name)} |${verdict(name).replace('   verdict:', '').slice(0, 150)}`);
const debug = run('debug-seen.mjs', join(logs, 'c-use.debug.txt'), join(logs, 'c-use.stderr.txt'));
const debugBase = run('debug-seen.mjs', join(logs, 'c-base.debug.txt'), join(logs, 'c-base.stderr.txt'));
console.log('--- debug-seen.mjs on the made-up debug record of c-use, then of c-base (first three lines) ---');
process.stdout.write(debug.stdout);
process.stdout.write(`${debugBase.stdout.split('\n').slice(0, 3).join('\n')}\n`);
const said = run('said.mjs', join(logs, 'c-use.stream.jsonl'));
console.log('--- said.mjs c-use ---');
process.stdout.write(said.stdout);

// The rule script, on made-up sets of runs. Every number here is invented to exercise a rule;
// none is an expectation.
const extraSkill = () => init({ skills: [...SHIPPED, 'slides'], slash_commands: ['init', 'debug', 'loop', 'help', 'slides'] });
const steps = (list, firstLine) => [firstLine, ...list.map((total, at) => say(`s${at}`, usage(2, total - 2, 0), [{ type: 'text', text: 'x' }])), result('x')];
function scenario(label, build, ...flags) {
  const dir = join(scratch, `ladder-${label}`);
  mkdirSync(dir);
  const first = (name, arm, total, extra = {}) => put(dir, name, arm, one(extra.init ?? init(), usage(2, total - 2, 0)), extra);
  const rungs = (rows) => { for (const [n, d, u] of rows) { first(`d${n}`, `d${n}`, d, { init: withServer(n) }); first(`u${n}`, `u${n}`, u, { init: withServer(n, n, 'connected', noBuiltSearch) }); } };
  build(first, rungs, dir);
  return run('ladder.mjs', dir, ...flags);
}
// The bases the previous video's record would give: a warm-up that lists one more skill.
const common = (first) => { first('w0', 'base', 11270, { init: extraSkill() }); first('z1', 'base', 11190); first('z2', 'base', 11186); first('zf', 'off', 11188, { init: init({ tools: noBuiltSearch }) }); };

// Round numbers, the two sessions that call a tool, and a record that was interrupted.
const roundSet = (first, rungs, dir) => {
  first('w0', 'base', 9100, { init: extraSkill() });
  first('z1', 'base', 9010); first('z2', 'base', 9014);
  first('zf', 'off', 9012, { init: init({ tools: noBuiltSearch }) });
  rungs([[2, 9700, 9260], [10, 9780, 10260], [40, 10080, 14010]]);
  put(dir, 'kd', 'use-d40', steps([10090, 10400, 10480], withServer(40)));
  put(dir, 'ku', 'use-u40', steps([14020, 14100], withServer(40, 40, 'connected', noBuiltSearch)));
  put(dir, 'broken', 'd10', one(withServer(10), usage(2, 5000, 0)), { ended: false });
};
const ladder = scenario('round', roundSet, '--skip', 'broken');
const clash = scenario('clash', roundSet);
// A: each arm exactly in proportion to the characters the server hands over (0.9 a character of
// names over a fixed 676 when deferred, 0.83 a character of tools/list up front).
const A = scenario('A', (first, rungs) => { common(first); rungs([[2, 11901, 11439], [10, 12061, 12411], [40, 12715, 16170]]); });
// A2: the same, with every run moved by 5 the worse way (inside what reruns have differed by).
const A2 = scenario('A2', (first, rungs) => { common(first); rungs([[2, 11896, 11434], [10, 12066, 12416], [40, 12710, 16165]]); });
// B: an exact line in the number of tools (12 a tool deferred, 125 up front), each run moved
// by 5. The same cost for every tool is not in proportion to characters that differ by tool.
const B = scenario('B', (first, rungs) => { common(first); rungs([[2, 11907, 11433], [10, 12013, 12443], [40, 12363, 16183]]); });
// C: the server with no tools is in the folder too. C2: the same with d0 on the deferred line.
const withZero = (zero) => (first, rungs) => { common(first); first('d0', 'd0', zero, { init: withServer(0) }); rungs([[2, 11901, 11438], [10, 11997, 12438], [40, 12357, 16188]]); };
const C = scenario('C', withZero(11218));
const C2 = scenario('C2', withZero(11879));
// D: up front smaller at 2, cannot tell at 10, deferred smaller at 40.
const D = scenario('D', (first, rungs) => { common(first); rungs([[2, 11901, 11438], [10, 12000, 11995], [40, 12400, 16000]]); });
// E: one arm of the ladder lists one more skill than every base run.
const E = scenario('E', (first, rungs) => { common(first); rungs([[2, 11901, 11438], [40, 12400, 16188]]); first('d10', 'd10', 12080, { init: { ...withServer(10), skills: [...SHIPPED, 'slides'] } }); first('u10', 'u10', 12438, { init: withServer(10, 10, 'connected', noBuiltSearch) }); });
// G: the first base run lists the extra skill, as the warm-up does; the second does not.
const G = scenario('G', (first, rungs) => { first('w0', 'base', 11270, { init: extraSkill() }); first('z1', 'base', 11270, { init: extraSkill() }); first('z2', 'base', 11186); first('zf', 'off', 11188, { init: init({ tools: noBuiltSearch }) }); rungs([[2, 11901, 11438], [10, 12000, 12438], [40, 12400, 16188]]); });
console.log('--- ladder.mjs on a made-up set of twelve runs with round numbers ---');
process.stdout.write(ladder.stdout);
console.log(`--- the same set without --skip: exit ${clash.status} ---`);
process.stdout.write(clash.stderr);
const only = (ran, pattern) => ran.stdout.split('\n').filter((line) => pattern.test(line)).join('\n');
console.log('--- A: in proportion to the characters; A2: the same with 5 of run-to-run difference; B: the same cost for every tool ---');
for (const [label, ran] of [['A', A], ['A2', A2], ['B', B]]) console.log(only(ran, /a straight line|more tools/).split('\n').map((line) => `${label}: ${line}`).join('\n'));
console.log('--- C: with the server with no tools in the folder (every line from its section on); C2: only its section ---');
process.stdout.write(`${C.stdout.slice(C.stdout.indexOf('== the ladder'))}`);
console.log(only(C2, /d0|no tools/));
console.log('--- D: a rung that cannot tell between two that point opposite ways ---');
process.stdout.write(D.stdout.slice(D.stdout.indexOf('== where deferred')));
console.log('--- E: an arm whose counts match no base run ---');
console.log(only(E, /^10 \||match no base|deferred (2|10) ->|turn-over/));
console.log('--- G: one of the two base runs lists the extra skill ---');
console.log(only(G, /^bar|^warm-up|^tool search off|^2 \|/));

const L = ladder.stdout;
const scenarios = [ladder, A, A2, B, C, C2, D, E, G];
const every = [...Object.values(after), debug, debugBase, said, ...scenarios, clash].map((each) => each.stdout + each.stderr).join('\n');
const checks = [
  ['every reader exits 0 with nothing on stderr', [...Object.values(after), debug, debugBase, said, ...scenarios].every((each) => each.status === 0 && !each.stderr)],
  ['clean cases have no STOP: base, d10, u10 (mode manual, no ToolSearch), off, use-d40', ['c-base', 'c-d10', 'c-u10', 'c-off', 'c-use'].every((name) => stops(name) === 0)],
  ['with tool search off the verdict says whether ToolSearch is listed', verdict('c-u10').includes('(ToolSearch listed: no)') && verdict('c-u10').includes('permission mode manual')],
  ['a deferred arm that lists none of its tools on the init event is not a STOP, and the count is printed', stops('c-listed0') === 0 && after['c-listed0'].stdout.includes("MCP tools on the init event: 0 = gear's 0 + any other 0 | this arm's server should hold 10")],
  ['an arm named for deferred loading without ToolSearch on the init list: STOP', stops('c-dplain') === 1 && verdict('c-dplain').includes('is named for deferred loading and ToolSearch is not on the init list')],
  ['an arm with tool search off that lists ToolSearch: STOP, with a server and without', stops('c-usearch') === 1 && stops('c-offsearch') === 1 && verdict('c-offsearch').includes('turns tool search off and ToolSearch is on the init list')],
  ['the server with no tools is no STOP whether or not ToolSearch is listed', stops('c-d0') === 0 && verdict('c-d0').includes('(ToolSearch listed: no)')],
  ['another plugin, skill, agent, server and tool, and a loaded instruction file: two STOPs', stops('c-mixed') === 2 && after['c-mixed'].stdout.includes('+ any other 1')],
  ['Bash among the built-in tools: STOP', stops('c-shell') === 1 && verdict('c-shell').includes('STOP: Bash or PowerShell')],
  ['a file tool aimed outside the project: STOP, counted in the stream and in the hook record', stops('c-out') === 1 && after['c-out'].stdout.includes('in the stream 1 | in the logging hook\'s record 1 (stopped by it: 1)')],
  ['a server that is still pending when the first request is built: STOP', stops('c-pending') === 1 && verdict('c-pending').includes('is pending, not connected')],
  ['a server that served another number of tools than the arm says: STOP', stops('c-wrong') === 1 && verdict('c-wrong').includes('served 2, not 10')],
  ['a ToolSearch call is printed with its references and the two numbers of its result', after['c-use'].stdout.includes('-> 1 tool references (gear\'s 1: find_gear; any other 0), 0 chars of text | tool_use_result: matches 1, total_deferred_tools 40')],
  ['the server\'s own record is counted, with when it was asked', after['c-use'].stdout.includes('tools served 40 | initialize 1 (at 9 ms) | tools/list 1 (at 15 ms) | tools/call 1 (first at 6100 ms)')],
  ['the answer of a use arm is recorded as yes or no', after['c-use'].stdout.includes('names shelf D-07 yes | 37 yes')],
  ['the debug record gives the k/n of every request in order', debug.stdout.includes('in order: 0/40, 1/40, 1/40')],
  ['a debug record without a k/n line says none', debugBase.stdout.includes('in order: none')],
  ['how tool search was decided is read from a fixed vocabulary', debug.stdout.includes('mode=tst, ENABLE_TOOL_SEARCH=undefined, result=true (x1)') && debugBase.stdout.includes('"no deferred tools available to search" (x1)')],
  ['a reason or a line in another shape is a count, not text', debug.stdout.includes('(other) (x1)') && debug.stdout.includes('in any other shape (count only): 1')],
  ['said.mjs prints the result text', said.stdout.includes('| G-417 在貨架 D-07，還剩 37 個。')],
  ['no made-up private name is printed by any reader', !/private-|secretsrv|never be read|elsewhere/.test(every)],
  ['ladder: the warm-up is shown and not used', L.includes('warm-up w0: first request 9,100') && L.includes('shown, never used') && L.includes('warm-up: no base run has its counts; against each, for the record: z1 +90, z2 +86')],
  ['ladder: the bar is the larger of the base runs\' difference and the floor', L.includes('bar: 11 (the larger of |z1 - z2| = 4 and the floor 11)')],
  ['ladder: tool search off without a server against the default base runs that share its counts', L.includes('tool search off, no server, minus the default base: +0 (cannot tell: inside 11) (against z1, z2) | built-in tools 7 against 8')],
  ['ladder: each arm minus the base with the same counts', L.includes('2 | 9,700, +688 | 9,260, +248 | +440') && L.includes('40 | 10,080, +1,068 | 14,010, +4,998 | -3,930')],
  ['ladder: the up-front arms against the default base, the way the previous video measured', L.includes('how the previous video measured it): 2 +248 | 10 +1,248 | 40 +4,998')],
  ['ladder: per tool between rungs, beside the characters a tool', L.includes('deferred 2 -> 10: +80 for 8 more tools = +10 a tool | names 22.3 characters a tool') && L.includes('up front 10 -> 40: +3,750 for 30 more tools = +125 a tool | tools/list 151 characters a tool')],
  ['ladder: the line is drawn in characters and the tolerance carries the leverage (55.9 and 53.6 at bar 11)', L.includes('through N = 2 and 10 (41 and 219) puts N = 40 (946) at 10,107; it came out 10,080 (-26.7; within 55.9, in proportion to the characters)') && L.includes('(-118.5; more than 53.6 off the line)')],
  ['ladder: each line at N = 0 over its base, and their difference once', L.includes('deferred: the same line at N = 0 (0 characters) is 9,682, +669.6 over its base') && L.includes('up front: the same line at N = 0 (2 characters) is 9,004, -8.2 over its base') && L.includes('the deferred line at N = 0 minus the up-front line at N = 0: +677.8')],
  ['A: arms in exact proportion to the characters are in line, both modes', (A.stdout.match(/in proportion to the characters\)/g) ?? []).length === 2 && !A.stdout.includes('off the line')],
  ['A2: the same arms moved by 5 each, the worse way, are still in line', A2.stdout.includes('(-50.3; within 55.9, in proportion to the characters)') && A2.stdout.includes('(-49.9; within 53.6, in proportion to the characters)')],
  ['B: the same cost for every tool is off the character line, and the per-tool figures show it', B.stdout.includes('(-82.9; more than 55.9 off the line)') && B.stdout.includes('(-167.2; more than 53.6 off the line)') && B.stdout.includes('= +126.3 a tool') && B.stdout.includes('= +124.7 a tool')],
  ['C: the server with no tools is never a rung and never part of a line', !/^0 \|/m.test(C.stdout) && !C.stdout.includes('0 -> 2') && !C.stdout.includes('through N = 0') && C.stdout.includes('through N = 2 and 10 (41 and 219) puts N = 40')],
  ['C: d0 is printed on its own: minus base, and against each line at N = 0', C.stdout.includes('server with no tools, minus base: +30') && C.stdout.includes('the deferred line at N = 0 (calculation) minus d0 (run): +660.9 (more than 13.5: d0 is off the deferred line)') && C.stdout.includes('the up-front line at N = 0 (calculation) minus d0 (run): -36.2 (more than 13.8: d0 is off the up-front line)')],
  ['C2: a d0 that is where the deferred line says is named as on the line', C2.stdout.includes('minus d0 (run): -0.1 (within 13.5: d0 sits on the deferred line)')],
  ['ladder: where the order turns over between two rungs', L.includes('N = 2: up front is smaller (+440)') && L.includes('N = 10: deferred is smaller (-480)') && L.includes('at about 5.8 tools')],
  ['D: a rung that cannot tell between two opposite ones is where it turns over, with no calculation', D.stdout.includes('N = 10: cannot tell (+5)') && D.stdout.includes('the order turns over at about N = 10') && !D.stdout.includes('on a straight line between')],
  ['E: an arm whose counts match no base run gets no figure and is listed for a rerun', E.stdout.includes('10 | 12,080, no base run with the same counts |') && E.stdout.includes('arms whose counts match no base run (rerun under a new name, then --skip the old one): d10')],
  ['G: only the base run with the same counts is used, for the off base and for the warm-up', G.stdout.includes('(against z2)') && G.stdout.includes('warm-up minus the base runs with the same counts (z1): +0') && G.stdout.includes('bar: 11 (the floor') && G.stdout.includes('2 | 11,901, +715 |')],
  ['ladder: the two sessions that call a tool', L.includes('use-d40 | 3 | 10,090, 10,400, 10,480 | +390 | 30,970 | +10') && L.includes('use-u40 | 2 | 14,020, 14,100 | +80 | 28,120 | +10') && L.includes('last request -3,620 | all requests added up +2,850 | requests 3 against 2')],
  ['ladder: an interrupted record is not read, and two streams with one arm are refused', clash.status === 2 && clash.stderr.includes('two streams have the arm d10')],
];
let failed = 0;
for (const [label, ok] of checks) { if (!ok) failed += 1; console.log(`${ok ? 'ok  ' : 'FAIL'} ${label}`); }
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
