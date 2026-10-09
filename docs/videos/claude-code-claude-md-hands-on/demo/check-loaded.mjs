// Feeds four made-up InstructionsLoaded events to load-log/loaded.mjs, the way Claude Code
// would on stdin, and prints what the logger wrote. No session, no model.
// Usage (from any folder): node <seed>/check-loaded.mjs
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const script = join(here, 'load-log', 'loaded.mjs');
const scratch = mkdtempSync(join(tmpdir(), 'md-lab-'));
const project = join(scratch, 'md-lab');
const log = join(scratch, 'loaded.log');
const elsewhere = resolve(scratch, '..', 'somewhere-else', 'CLAUDE.md');

const events = [
  { load_reason: 'session_start', memory_type: 'Project', file_path: join(project, 'CLAUDE.md') },
  { load_reason: 'session_start', memory_type: 'Local', file_path: join(project, 'CLAUDE.local.md') },
  {
    load_reason: 'nested_traversal', memory_type: 'Project',
    file_path: join(project, 'docs', 'CLAUDE.md'), trigger_file_path: join(project, 'docs', 'use.md'),
  },
  { load_reason: 'session_start', memory_type: 'User', file_path: elsewhere },
];

for (const event of events) {
  const input = JSON.stringify({ hook_event_name: 'InstructionsLoaded', cwd: project, ...event });
  const run = spawnSync(process.execPath, [script], {
    input, encoding: 'utf8', env: { ...process.env, CLAUDE_PROJECT_DIR: project, LOAD_LOG: log },
  });
  console.log(`exit ${run.status} | stdout: ${run.stdout.trim()}${run.stderr ? ` | stderr: ${run.stderr.trim()}` : ''}`);
}
console.log('--- the log file');
console.log(readFileSync(log, 'utf8').trim());
rmSync(scratch, { recursive: true, force: true });
