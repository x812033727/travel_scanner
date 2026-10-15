import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';

const event = JSON.parse(readFileSync(0, 'utf8').trim());
if (event.stop_hook_active) process.exit(0);

const run = spawnSync(process.execPath, ['--test'], {
  cwd: process.env.CLAUDE_PROJECT_DIR ?? process.cwd(),
  encoding: 'utf8', timeout: 60_000,
});

if (run.status !== 0) {
  console.error('Tests fail. Fix the code, then finish.');
  console.error(String(run.stdout).slice(-1500));
  process.exitCode = 2;
}
