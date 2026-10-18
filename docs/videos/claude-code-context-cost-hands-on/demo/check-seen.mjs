// Runs the project's logging hook on made-up events and prints what it wrote. No session, no
// model. It checks that a name or a path that is not the seed's never reaches the record, and
// that the one thing the hook stops is a file tool aimed outside the project and the plugin:
// that call is marked BLOCKED and the hook exits 2, every other event exits 0 and prints nothing.
// Usage: node <seed>/check-seen.mjs
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'seen-check-'));
const lab = join(scratch, 'lab');
const kit = join(scratch, 'ship-kit');
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
  { hook_event_name: 'InstructionsLoaded', cwd: lab, load_reason: 'session_start', memory_type: 'Project', file_path: join(lab, 'CLAUDE.md') },
  { hook_event_name: 'InstructionsLoaded', cwd: lab, load_reason: 'session_start', memory_type: 'User', file_path: join(away, 'CLAUDE.md') },
  pre('Skill', { skill: 'release-prep', args: '1.2.1' }),
  pre('Skill', { skill: 'ship-kit:release-prep', args: '1.2.1' }),
  pre('Skill', { skill: 'somebody:private-skill' }),
  pre('Agent', { subagent_type: 'log-scout', prompt: 'x'.repeat(120), description: 'made up' }),
  pre('Agent', { subagent_type: 'somebody-elses-agent', prompt: 'x' }),
  post('Agent', { subagent_type: 'log-scout', prompt: 'x' }, { status: 'async_launched', note: 'y'.repeat(40) }),
  pre('ToolSearch', { query: 'select:mcp__gear__find_gear,mcp__somebody__send', max_results: 5 }),
  pre('mcp__gear__find_gear', { code: 'G-417' }),
  post('mcp__gear__find_gear', { code: 'G-417' }, [{ type: 'text', text: 'made-up answer' }]),
  pre('mcp__somebody__send', { to: 'nobody' }),
  pre('Read', { file_path: join(lab, '.claude', 'skills', 'release-prep', 'template.md') }),
  pre('Read', { file_path: join(kit, 'skills', 'release-prep', 'template.md') }),
  stopped(pre('Read', { file_path: join(away, 'private.txt') })),
  pre('Edit', { file_path: join(lab, 'package.json') }),
  pre('Glob', { pattern: 'logs/*.log' }, { agent_id: 'agent-madeup', agent_type: 'log-scout' }),
  { hook_event_name: 'PermissionRequest', tool_name: 'Read', cwd: lab, permission_mode: 'default', tool_input: { file_path: join(away, 'private.txt') }, permission_suggestions: [{ rules: [] }] },
  { hook_event_name: 'PostToolUseFailure', tool_name: 'Edit', tool_use_id: 'toolu_madeup0003', cwd: lab, tool_input: { file_path: join(lab, 'src', 'fares.test.mjs') }, error: `made-up error that names ${lab} and mcp__somebody__send` },
  { hook_event_name: 'SubagentStart', cwd: lab, agent_id: 'agent-madeup', agent_type: 'log-scout' },
  { hook_event_name: 'SubagentStop', cwd: lab, agent_id: 'agent-madeup', agent_type: 'somebody-elses-agent' },
  { hook_event_name: 'UserPromptExpansion', cwd: lab, expansion_type: 'slash_command', command_name: 'release-prep', command_source: 'projectSettings', prompt: '/release-prep 1.2.1' },
  // File tools aimed outside the project and the plugin are stopped; the same tools inside are not.
  stopped(pre('Write', { file_path: join(away, 'notes.txt'), content: 'x' })),
  stopped(pre('Glob', { pattern: '~/**/*.md' })),
  stopped(pre('Grep', { pattern: 'token', glob: '../**/*.json' })),
  stopped(pre('Read', { file_path: join(temp, 'claude', 'saved-output.txt') })),
  pre('Glob', { pattern: `${lab.replaceAll('\\', '/')}/logs/*.log` }),
  pre('Grep', { pattern: '/v1\\.2\\.\\d/', glob: '*.md', path: 'src' }),
  pre('Glob', { pattern: '**/*.log', path: lab }),
  pre('Edit', { file_path: 'CHANGELOG.md' }),
];
let failed = 0;
const leaks = [];
for (const each of events) {
  const event = each.event ?? each;
  const want = each.exit ?? 0;
  const out = spawnSync(process.execPath, [join(seed, 'watch', 'seen.mjs')], {
    input: JSON.stringify(event), encoding: 'utf8',
    env: { PATH: process.env.PATH, SystemRoot: process.env.SystemRoot ?? '', TEMP: temp, TMP: temp, TMPDIR: temp, CLAUDE_PROJECT_DIR: lab, SEEN_LOG: record, KIT_DIR: kit },
  });
  if (out.status !== want || out.stdout.length || (want === 0 ? out.stderr.length > 0 : out.stderr.length === 0)) failed += 1;
  if (/made-up|elsewhere|private|notes\.txt|saved-output/.test(out.stderr) || out.stderr.includes(scratch)) leaks.push(event.tool_name);
  console.log(`exit ${out.status} | stdout bytes: ${out.stdout.length} | stderr bytes: ${out.stderr.length}`);
}
const lines = readFileSync(record, 'utf8').split('\n').filter(Boolean);
console.log(`the record (${lines.length} lines):`);
for (const line of lines) console.log(`   ${line}`);
const text = lines.join('\n');
const has = (line) => lines.includes(line);
const checks = [
  ['one line per event; only a blocked call exits 2 and writes to stderr, and nothing goes to stdout', lines.length === events.length && failed === 0],
  ['the made-up names of another skill, agent and MCP server are not in the record', !/somebody|private-skill|send/.test(text)],
  ['no path outside the project is in the record or on stderr', !text.includes(scratch) && !text.includes(scratch.replaceAll('\\', '/')) && !/private\.txt|elsewhere|notes\.txt|saved-output/.test(text) && leaks.length === 0],
  ['the project\'s own CLAUDE.md is named, another one is only (outside the project)', has('InstructionsLoaded session_start Project CLAUDE.md') && has('InstructionsLoaded session_start User (outside the project)')],
  ['the seed\'s names are kept', text.includes('skill=release-prep') && text.includes('skill=ship-kit:release-prep') && text.includes('type=log-scout')],
  ['the seed\'s MCP tool is named with its input, another server\'s is not', text.includes('mcp__gear__find_gear {"code":"G-417"}') && text.includes('mcp__(a server)')],
  ['a ToolSearch query keeps the seed\'s tool and masks the other', text.includes('ToolSearch query=select:mcp__gear__find_gear,mcp__(other)')],
  ['a tool response is a status and a size', text.includes('| status=async_launched response_chars=')],
  ['a call under the agent is marked by=log-scout', text.includes('PreToolUse by=log-scout id=0001 Glob logs/*.log')],
  ['a read and a write outside the project are BLOCKED', has('PreToolUse by=main id=0001 Read (outside the project) | BLOCKED') && has('PreToolUse by=main id=0001 Write (outside the project) | BLOCKED')],
  ['a Glob pattern or a Grep glob that starts at ~ or .. is BLOCKED', has('PreToolUse by=main id=0001 Glob (outside the project) | BLOCKED') && has('PreToolUse by=main id=0001 Grep (outside the project) | BLOCKED')],
  ['a file in the temp folder is BLOCKED and says where', has('PreToolUse by=main id=0001 Read (outside the project, in the temp folder) | BLOCKED')],
  ['five calls were blocked in all, and a permission request for an outside path is recorded but not blocked', lines.filter((line) => line.endsWith('| BLOCKED')).length === 5 && has('PermissionRequest by=main id=---- Read (outside the project) | mode=default suggestions=1')],
  ['inside the project nothing is blocked: a rooted pattern, a regular expression that starts with a slash, the project folder itself, a relative path',
    has('PreToolUse by=main id=0001 Glob <lab>/logs/*.log') && has('PreToolUse by=main id=0001 Grep src') && has('PreToolUse by=main id=0001 Glob .') && has('PreToolUse by=main id=0001 Edit CHANGELOG.md')],
  ['a file in the plugin folder is <plugin>/..., not blocked', has('PreToolUse by=main id=0001 Read <plugin>/skills/release-prep/template.md')],
];
for (const [label, ok] of checks) { if (!ok) failed += 1; console.log(`${ok ? 'ok  ' : 'FAIL'} ${label}`); }
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
