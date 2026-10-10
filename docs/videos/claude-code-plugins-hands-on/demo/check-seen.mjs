// Runs the project's logging hook on made-up events and prints what it wrote. No session, no
// model. It also checks that a name or a path that is not the seed's never reaches the record.
// Usage: node <seed>/check-seen.mjs
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'seen-check-'));
const lab = join(scratch, 'lab');
const kit = join(scratch, 'ship-kit');
mkdirSync(lab, { recursive: true });
const record = join(scratch, 'seen.txt');
const pre = (tool, input, extra = {}) => ({ hook_event_name: 'PreToolUse', tool_name: tool, tool_use_id: 'toolu_madeup0001', cwd: lab, tool_input: input, ...extra });
const events = [
  pre('Skill', { skill: 'ship-kit:release-prep', args: '1.2.1' }),
  pre('Skill', { skill: 'release-prep', args: '0.4.1' }),
  pre('Skill', { skill: 'somebody:private-skill' }),
  pre('Agent', { subagent_type: 'ship-kit:log-scout', prompt: 'x'.repeat(120), description: 'made up' }),
  pre('Agent', { subagent_type: 'somebody-elses-agent', prompt: 'x' }),
  pre('Read', { file_path: join(kit, 'skills', 'release-prep', 'template.md') }),
  pre('Read', { file_path: join(scratch, 'elsewhere', 'private.txt') }),
  pre('Edit', { file_path: join(lab, 'package.json') }),
  pre('Glob', { pattern: 'logs/*.log' }, { agent_id: 'agent-madeup', agent_type: 'ship-kit:log-scout' }),
  pre('mcp__somebody__send', { to: 'nobody' }),
  { hook_event_name: 'PermissionRequest', tool_name: 'Read', cwd: lab, permission_mode: 'default', tool_input: { file_path: join(kit, 'skills', 'release-prep', 'template.md') }, permission_suggestions: [{ rules: [{ toolName: 'Read', ruleContent: '//made/up/**' }] }] },
  { hook_event_name: 'PostToolUseFailure', tool_name: 'Edit', tool_use_id: 'toolu_madeup0002', cwd: lab, tool_input: { file_path: join(lab, 'src', 'fares.test.mjs') }, error: `made-up error that names ${lab} and ${kit}` },
  { hook_event_name: 'PostToolUse', tool_name: 'Agent', tool_use_id: 'toolu_madeup0003', cwd: lab, tool_input: { subagent_type: 'log-scout', prompt: 'x' }, tool_response: { status: 'completed' } },
  { hook_event_name: 'SubagentStart', cwd: lab, agent_id: 'agent-madeup', agent_type: 'ship-kit:log-scout' },
  { hook_event_name: 'SubagentStop', cwd: lab, agent_id: 'agent-madeup', agent_type: 'somebody-elses-agent' },
  { hook_event_name: 'UserPromptExpansion', cwd: lab, expansion_type: 'slash_command', command_name: 'ship-kit:release-prep', command_source: 'plugin', prompt: '/ship-kit:release-prep 1.2.1' },
  { hook_event_name: 'InstructionsLoaded', cwd: lab, load_reason: 'session_start', memory_type: 'User', file_path: join(scratch, 'elsewhere', 'CLAUDE.md') },
];
let failed = 0;
for (const event of events) {
  const out = spawnSync(process.execPath, [join(seed, 'watch', 'seen.mjs')], {
    input: JSON.stringify(event), encoding: 'utf8',
    env: { PATH: process.env.PATH, SystemRoot: process.env.SystemRoot ?? '', CLAUDE_PROJECT_DIR: lab, SEEN_LOG: record, KIT_DIR: kit },
  });
  if (out.status !== 0 || out.stdout.length || out.stderr.length) failed += 1;
  console.log(`exit ${out.status} | stdout bytes: ${out.stdout.length} | stderr bytes: ${out.stderr.length}`);
}
const lines = readFileSync(record, 'utf8').split('\n').filter(Boolean);
console.log(`the record (${lines.length} lines):`);
for (const line of lines) console.log(`   ${line}`);
const text = lines.join('\n');
const checks = [
  ['one line per event', lines.length === events.length],
  ['the made-up names of another skill, agent and MCP server are not in the record', !/somebody|private-skill|send/.test(text)],
  ['no path of the scratch folder is in the record', !text.includes(scratch) && !text.includes(scratch.replaceAll('\\', '/')) && !/private\.txt|elsewhere/.test(text)],
  ['a file in the plugin is shown as <plugin>/...', text.includes('Read <plugin>/skills/release-prep/template.md')],
  ['the seed\'s names are kept', text.includes('skill=ship-kit:release-prep') && text.includes('skill=release-prep') && text.includes('type=ship-kit:log-scout')],
  ['a call under the plugin\'s agent is marked by=ship-kit:log-scout', text.includes('PreToolUse by=ship-kit:log-scout id=0001 Glob logs/*.log')],
];
for (const [label, ok] of checks) { if (!ok) failed += 1; console.log(`${ok ? 'ok  ' : 'FAIL'} ${label}`); }
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
