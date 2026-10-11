// Feeds the logging hook (skill-log/seen.mjs) six MADE-UP events in the shape the hooks reference
// documents, in a temporary project that has one skill folder, and prints what it logged.
// It checks the logger only: that it writes one line per event, prints nothing to stdout, names
// only the project's own skills and files, and exits 0. It is not evidence that Claude Code
// sends any of these events. No session, no model.
// Usage: node <seed>/check-seen.mjs
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'skill-lab-seen-'));
const root = join(scratch, 'skill-lab');
mkdirSync(join(root, '.claude', 'skills', 'release-prep'), { recursive: true });
const log = join(scratch, 'seen.log');
const common = { session_id: 'made-up', cwd: root, permission_mode: 'default' };
const events = [
  { ...common, hook_event_name: 'InstructionsLoaded', load_reason: 'session_start', memory_type: 'Project', file_path: join(root, 'CLAUDE.md') },
  { ...common, hook_event_name: 'InstructionsLoaded', load_reason: 'session_start', memory_type: 'User', file_path: join(scratch, 'elsewhere', 'CLAUDE.md') },
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'Skill', tool_input: { skill: 'release-prep', args: '0.3.1' } },
  { ...common, hook_event_name: 'PreToolUse', tool_name: 'Skill', tool_input: { skill: 'somebody-elses-skill' } },
  { ...common, hook_event_name: 'UserPromptExpansion', expansion_type: 'slash_command', command_name: 'release-prep', command_args: '0.3.1', command_source: 'made-up-source', prompt: '/release-prep 0.3.1' },
  { ...common, hook_event_name: 'UserPromptExpansion', expansion_type: 'slash_command', command_name: 'somebody-elses-skill', command_args: '', command_source: 'made-up-source', prompt: '/somebody-elses-skill' },
];
let failed = false;
for (const event of events) {
  const run = spawnSync(process.execPath, [join(here, 'skill-log', 'seen.mjs')], {
    input: JSON.stringify(event), encoding: 'utf8',
    env: { ...process.env, CLAUDE_PROJECT_DIR: root, SKILL_LOG: log },
  });
  console.log(`exit ${run.status} | stdout bytes: ${run.stdout.length} | stderr bytes: ${run.stderr.length}`);
  if (run.status !== 0 || run.stdout.length || run.stderr.length) failed = true;
}
console.log('--- the log file');
process.stdout.write(readFileSync(log, 'utf8'));
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
