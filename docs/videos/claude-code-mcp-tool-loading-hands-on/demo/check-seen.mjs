// Runs the project's logging hook on made-up events and prints what it wrote. No session, no
// model. It checks that a name or a path that is not the seed's never reaches the record, and
// that the one thing the hook stops is a file tool aimed outside the project: that call is
// marked BLOCKED and the hook exits 2, every other event exits 0 and prints nothing.
// Usage: node <seed>/check-seen.mjs
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'seen-check-'));
const lab = join(scratch, 'lab');
// What the hook takes for the system's temporary folder, and a made-up folder that is neither
// in it nor in the project.
const temp = join(scratch, 'tmp');
const away = resolve('/made-up/elsewhere');
mkdirSync(lab, { recursive: true });
mkdirSync(temp, { recursive: true });
const record = join(scratch, 'seen.txt');
const pre = (tool, input, extra = {}) => ({ hook_event_name: 'PreToolUse', tool_name: tool, tool_use_id: 'toolu_madeup0001', cwd: lab, tool_input: input, ...extra });
const post = (tool, input, response) => ({ hook_event_name: 'PostToolUse', tool_name: tool, tool_use_id: 'toolu_madeup0002', cwd: lab, tool_input: input, tool_response: response });
const stopped = (event) => ({ event, exit: 2 });
const events = [
  { hook_event_name: 'InstructionsLoaded', cwd: lab, load_reason: 'session_start', memory_type: 'User', file_path: join(away, 'CLAUDE.md') },
  pre('Skill', { skill: 'somebody:private-skill' }),
  pre('Agent', { subagent_type: 'Explore', prompt: 'x'.repeat(120), description: 'made up' }),
  pre('Agent', { subagent_type: 'somebody-elses-agent', prompt: 'x' }),
  pre('ToolSearch', { query: 'select:mcp__gear__find_gear,mcp__somebody__send', max_results: 5 }),
  post('ToolSearch', { query: 'gear shelf', max_results: 5 }, { matches: ['mcp__gear__find_gear'], query: 'gear shelf', total_deferred_tools: 40 }),
  pre('mcp__gear__find_gear', { code: 'G-417' }),
  post('mcp__gear__find_gear', { code: 'G-417' }, [{ type: 'text', text: 'made-up answer' }]),
  pre('mcp__somebody__send', { to: 'nobody' }),
  pre('Read', { file_path: join(lab, 'server', 'stock.tsv') }),
  stopped(pre('Read', { file_path: join(away, 'private.txt') })),
  pre('Glob', { pattern: 'server/*.mjs' }, { agent_id: 'agent-madeup', agent_type: 'somebody-elses-agent' }),
  { hook_event_name: 'PermissionRequest', tool_name: 'Edit', cwd: lab, permission_mode: 'default', tool_input: { file_path: join(lab, 'README.md') }, permission_suggestions: [{ rules: [] }] },
  { hook_event_name: 'PermissionRequest', tool_name: 'mcp__gear__gear_rate', cwd: lab, permission_mode: 'default', tool_input: { code: 'G-417' }, permission_suggestions: [] },
  { hook_event_name: 'PostToolUseFailure', tool_name: 'Edit', tool_use_id: 'toolu_madeup0003', cwd: lab, tool_input: { file_path: join(lab, 'README.md') }, error: `made-up error that names ${lab} and mcp__somebody__send` },
  { hook_event_name: 'SubagentStart', cwd: lab, agent_id: 'agent-madeup', agent_type: 'general-purpose' },
  { hook_event_name: 'SubagentStop', cwd: lab, agent_id: 'agent-madeup', agent_type: 'somebody-elses-agent' },
  { hook_event_name: 'UserPromptExpansion', cwd: lab, expansion_type: 'slash_command', command_name: 'somebody:private-skill', prompt: '/somebody:private-skill' },
  // File tools aimed outside the project are stopped; the same tools inside are not.
  stopped(pre('Write', { file_path: join(away, 'notes.txt'), content: 'x' })),
  stopped(pre('Glob', { pattern: '~/**/*.md' })),
  stopped(pre('Grep', { pattern: 'token', glob: '../**/*.json' })),
  stopped(pre('Read', { file_path: join(temp, 'claude', 'saved-output.txt') })),
  pre('Glob', { pattern: `${lab.replaceAll('\\', '/')}/server/*.tsv` }),
  pre('Grep', { pattern: '/G-4\\d\\d/', glob: '*.tsv', path: 'server' }),
  pre('Glob', { pattern: '**/*.mjs', path: lab }),
  pre('Edit', { file_path: 'README.md' }),
];
let failed = 0;
const exits = [];
events.forEach((each) => {
  const event = each.event ?? each;
  const want = each.exit ?? 0;
  const ran = spawnSync(process.execPath, [join(seed, 'watch', 'seen.mjs')], {
    input: JSON.stringify(event), encoding: 'utf8',
    env: { ...process.env, CLAUDE_PROJECT_DIR: lab, SEEN_LOG: record, TMPDIR: temp, TEMP: temp, TMP: temp },
  });
  exits.push(`exit ${ran.status} | stdout bytes: ${ran.stdout.length} | stderr bytes: ${ran.stderr.length}`);
  const quiet = ran.stdout === '' && (want === 2 ? ran.stderr.length > 0 && !/[\\/]/.test(ran.stderr.replace('logging hook: file tools', '')) : ran.stderr === '');
  if (ran.status !== want || !quiet) { failed += 1; console.log(`FAIL event ${event.hook_event_name} ${event.tool_name ?? ''}: exit ${ran.status}, wanted ${want}`); }
});
const tally = {};
for (const each of exits) tally[each] = (tally[each] ?? 0) + 1;
for (const [each, times] of Object.entries(tally)) console.log(`${times} events: ${each}`);
const text = readFileSync(record, 'utf8');
const rows = text.trimEnd().split('\n');
console.log(`## the record (${rows.length} lines)`);
for (const row of rows) console.log(row);
const check = (ok, what) => { if (!ok) failed += 1; console.log(`${ok ? 'ok  ' : 'FAIL'} ${what}`); };
check(rows.length === events.length, `one line per event (${events.length})`);
check(!/somebody|private-skill|nobody|made-up\/elsewhere|elsewhere/.test(text), 'no skill, agent, server, tool or path that is not the seed\'s is in the record');
check(!text.includes(scratch) && !text.includes(scratch.replaceAll('\\', '/')), 'the project folder is never written out in full');
check(rows.filter((row) => row.endsWith('| BLOCKED')).length === 5, 'five file-tool calls aimed outside the project are BLOCKED');
check(rows.filter((row) => row.includes('(outside the project, in the temp folder)')).length === 1, 'the one in the temp folder says so');
check(rows.some((row) => row.includes('mcp__gear__find_gear {"code":"G-417"}')) && rows.some((row) => row.includes('mcp__(a server)')), 'the seed\'s tool is named, another server\'s is not');
check(rows.some((row) => /ToolSearch query=select:mcp__gear__find_gear,mcp__\(other\) max_results=5/.test(row)), 'a ToolSearch query keeps the seed\'s tool name and hides the other');
check(rows.some((row) => /^PermissionRequest .* mcp__gear__gear_rate .* mode=default/.test(row)), 'a permission request for a gear tool that is not pre-approved is recorded');
check(rows.filter((row) => /^PreToolUse .* (Glob|Grep|Edit|Read) (server|README|\.)/.test(row) && !row.includes('BLOCKED')).length >= 4, 'file tools inside the project are not stopped');
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
