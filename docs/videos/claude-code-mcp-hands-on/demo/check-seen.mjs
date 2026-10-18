// Feeds the logging hook (hook-log/seen.mjs) twelve MADE-UP events in the shape the hooks reference
// documents, in a temporary project whose .mcp.json names one server, and prints what it logged.
// It checks the logger only: one line per event, nothing on stdout, only the project's own server
// and files named, exit 0. It is not evidence that Claude Code sends any of these events.
// No session, no model.
// Usage: node <seed>/check-seen.mjs
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'gear-lab-seen-'));
const root = join(scratch, 'gear-lab');
mkdirSync(root, { recursive: true });
writeFileSync(join(root, '.mcp.json'), readFileSync(join(here, 'variants', 'mcp.project.json')));
const log = join(scratch, 'seen.txt');
const common = { session_id: 'made-up', cwd: root, permission_mode: 'default' };
const gear = { tool_name: 'mcp__gear__find_gear', tool_input: { code: 'G-417' }, mcp_server: { name: 'gear', source: 'made-up-source' } };
const other = { tool_name: 'mcp__somebody__private_tool', tool_input: { secret: 'never shown' }, mcp_server: { name: 'somebody', source: 'user' } };
const events = [
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'ToolSearch', tool_input: { query: 'select:mcp__gear__find_gear', max_results: 5 } },
  { ...common, hook_event_name: 'PreToolUse', ...gear },
  { ...common, hook_event_name: 'PostToolUse', ...gear, tool_response: [{ type: 'text', text: 'made up' }] },
  { ...common, hook_event_name: 'PostToolUseFailure', ...gear, error: `made-up error that names ${root} and runs on` },
  { ...common, hook_event_name: 'PermissionRequest', ...gear },
  { ...common, hook_event_name: 'PermissionDenied', ...gear, reason: 'made-up reason' },
  { ...common, hook_event_name: 'PreToolUse', ...other },
  { ...common, hook_event_name: 'PostToolUseFailure', ...other, error: 'never shown' },
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'Read', tool_input: { file_path: join(root, 'server', 'stock.tsv') } },
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'Read', tool_input: { file_path: join(scratch, 'elsewhere.txt') } },
  { ...common, hook_event_name: 'InstructionsLoaded', load_reason: 'session_start', memory_type: 'Project', file_path: join(root, 'CLAUDE.md') },
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
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
