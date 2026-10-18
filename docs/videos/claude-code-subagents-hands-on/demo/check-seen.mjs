// Feeds the logging hook (agent-log/seen.mjs) eleven MADE-UP events in the shape the hooks
// reference documents, in a temporary project that has one agent file, and prints what it logged.
// It checks the logger only: one line per event, nothing on stdout, only the project's own agent
// and files and the built-in agents named, exit 0. It is not evidence that Claude Code sends any
// of these events. No session, no model.
// Usage: node <seed>/check-seen.mjs
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'log-lab-seen-'));
const root = join(scratch, 'log-lab');
mkdirSync(join(root, '.claude', 'agents'), { recursive: true });
writeFileSync(join(root, '.claude', 'agents', 'log-scout.md'), '---\nname: log-scout\ndescription: made up\n---\n');
const log = join(scratch, 'seen.log');
const common = { session_id: 'made-up', cwd: root, permission_mode: 'default' };
const inside = { agent_id: 'made-up-agent-id', agent_type: 'log-scout' };
const events = [
  { ...common, hook_event_name: 'InstructionsLoaded', load_reason: 'session_start', memory_type: 'Project', file_path: join(root, 'CLAUDE.md') },
  { ...common, hook_event_name: 'InstructionsLoaded', load_reason: 'session_start', memory_type: 'User', file_path: join(scratch, 'elsewhere', 'CLAUDE.md') },
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'Agent', tool_input: { description: 'made up', prompt: 'made-up task', subagent_type: 'log-scout' } },
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'Agent', tool_input: { description: 'made up', prompt: '【trip-queue】 made up', subagent_type: 'somebody-elses-agent', model: 'opus', run_in_background: true } },
  { ...common, hook_event_name: 'SubagentStart', ...inside },
  { ...common, ...inside, hook_event_name: 'PreToolUse', tool_name: 'Read', tool_input: { file_path: join(root, 'logs', 'queue-2026-10-01.log') } },
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'Read', tool_input: { file_path: join(root, 'README.md') } },
  { ...common, agent_id: 'made-up-other-id', agent_type: 'somebody-elses-agent', hook_event_name: 'PreToolUse', tool_name: 'Read', tool_input: { file_path: join(scratch, 'elsewhere.txt') } },
  { ...common, hook_event_name: 'PostToolUse', tool_name: 'Agent', tool_input: { subagent_type: 'log-scout' }, tool_response: { status: 'completed', agentId: 'made-up-agent-id', content: [], resolvedModel: 'made-up-model', totalTokens: 12450, totalDurationMs: 48211, totalToolUseCount: 7, usage: {} } },
  { ...common, hook_event_name: 'SubagentStop', ...inside, stop_hook_active: false, last_assistant_message: '【trip-queue】\nJ0000｜made-up.log｜1\n共 1 筆' },
  { ...common, hook_event_name: 'SubagentStop', agent_id: 'made-up-internal', agent_type: '', stop_hook_active: false, last_assistant_message: 'made up' },
];
let failed = false;
for (const event of events) {
  const run = spawnSync(process.execPath, [join(here, 'agent-log', 'seen.mjs')], {
    input: JSON.stringify(event), encoding: 'utf8',
    env: { ...process.env, CLAUDE_PROJECT_DIR: root, SEEN_LOG: log },
  });
  console.log(`exit ${run.status} | stdout bytes: ${run.stdout.length} | stderr bytes: ${run.stderr.length}`);
  if (run.status !== 0 || run.stdout.length || run.stderr.length) failed = true;
}
console.log('--- the log file');
process.stdout.write(readFileSync(log, 'utf8'));
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
