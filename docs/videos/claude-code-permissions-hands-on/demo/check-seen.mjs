// Feeds the logging hook (hook-log/seen.mjs) twelve MADE-UP events in the shape the hooks reference
// documents, and prints what it logged. It checks the logger only: one line per event, nothing on
// stdout (so it returns no decision), no path outside the project, no MCP tool named, exit 0.
// It is not evidence that Claude Code sends any of these events. No session, no model.
// Usage: node <seed>/check-seen.mjs
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'fare-lab-seen-'));
const root = join(scratch, 'fare-lab');
mkdirSync(root, { recursive: true });
const log = join(scratch, 'seen.txt');
const common = { session_id: 'made-up', cwd: root, permission_mode: 'default' };
const bash = { tool_name: 'Bash', tool_input: { command: 'bash scripts/deploy.sh', description: 'made up' } };
const edit = { tool_name: 'Edit', tool_input: { file_path: join(root, 'data', 'rates.csv'), old_string: 'a', new_string: 'b' } };
const other = { tool_name: 'mcp__somebody__private_tool', tool_input: { secret: 'never shown' } };
const events = [
  { ...common, hook_event_name: 'PreToolUse', ...bash, tool_use_id: 'toolu_madeup0001' },
  { ...common, hook_event_name: 'PermissionRequest', ...bash, permission_suggestions: [{ type: 'addRules', rules: [{ toolName: 'Bash', ruleContent: 'bash scripts/deploy.sh' }], behavior: 'allow', destination: 'localSettings' }] },
  { ...common, hook_event_name: 'PostToolUseFailure', ...bash, tool_use_id: 'toolu_madeup0001', error: `made-up error that names ${root} and runs on` },
  { ...common, hook_event_name: 'PreToolUse', ...edit, tool_use_id: 'toolu_madeup0002' },
  { ...common, hook_event_name: 'PostToolUse', ...edit, tool_use_id: 'toolu_madeup0002', tool_response: { made: 'up' } },
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'Read', tool_input: { file_path: join(root, '.env') }, tool_use_id: 'toolu_madeup0003' },
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'Read', tool_input: { file_path: join(scratch, 'elsewhere.txt') }, tool_use_id: 'toolu_madeup0004' },
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'Grep', tool_input: { pattern: 'API_BASE', path: root }, tool_use_id: 'toolu_madeup0005' },
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'Glob', tool_input: { pattern: '**/.env*' }, tool_use_id: 'toolu_madeup0006' },
  { ...common, hook_event_name: 'PermissionDenied', ...bash, tool_use_id: 'toolu_madeup0007', reason: 'made-up reason' },
  { ...common, hook_event_name: 'PreToolUse', ...other, tool_use_id: 'toolu_madeup0008' },
  { ...common, hook_event_name: 'InstructionsLoaded', load_reason: 'session_start', memory_type: 'User', file_path: join(scratch, 'elsewhere', 'CLAUDE.md') },
];
let failed = false;
for (const event of events) {
  const run = spawnSync(process.execPath, [join(here, 'hook-log', 'seen.mjs')], {
    input: JSON.stringify(event), encoding: 'utf8',
    env: { ...process.env, CLAUDE_PROJECT_DIR: root, SEEN_LOG: log },
  });
  console.log(`exit ${run.status} | stdout bytes: ${run.stdout.length} | stderr bytes: ${run.stderr.length}`);
  if (run.status !== 0 || run.stdout.length || run.stderr.length) failed = true;
}
console.log('--- the record');
const text = readFileSync(log, 'utf8');
process.stdout.write(text);
if (text.includes('somebody') || text.includes('never shown') || text.includes(scratch)) { console.log('LEAK: a name, a value or a path that must not be recorded is in the record'); failed = true; }
if (text.trim().split('\n').length !== events.length) { console.log('WRONG: not one line per event'); failed = true; }
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
