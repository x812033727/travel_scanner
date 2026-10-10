#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';

const { values } = parseArgs({ options: {
  project: { type: 'string' }, prompt: { type: 'string' }, output: { type: 'string' },
  codex: { type: 'string', default: 'codex' },
} });
if (!values.project || !values.prompt || !values.output) {
  throw new Error('Usage: node record-cli.mjs --project DIR --prompt FILE --output NEW_DIR [--codex EXE]');
}
const project = path.resolve(values.project);
const output = path.resolve(values.output);
if (existsSync(output)) {
  throw new Error('Output already exists. Preserve all partial evidence and choose a new invocation directory.');
}
mkdirSync(path.dirname(output), { recursive: true });
mkdirSync(output); // Atomic reservation: a concurrent invocation cannot share this output.
const prompt = readFileSync(values.prompt, 'utf8');
const args = ['exec', '--sandbox', 'read-only', '--ephemeral', '--json', '--color', 'never',
  '--skip-git-repo-check', '-c', 'approval_policy="never"',
  '-C', project, '--output-last-message', path.join(output, 'answer.md'), '-'];
const started = new Date().toISOString();
const version = spawnSync(values.codex, ['--version'], { encoding: 'utf8', windowsHide: true });
writeFileSync(path.join(output, 'prompt.txt'), prompt);
writeFileSync(path.join(output, 'invocation.json'), JSON.stringify({ args, started, project,
  cli_version: version.stdout?.trim(), node_version: process.version,
  purpose: 'Lesson 01: real read-only project inspection; no implementation or media production',
}, null, 2) + '\n');
const run = spawnSync(values.codex, args, { cwd: project, input: prompt, encoding: 'utf8',
  windowsHide: true, maxBuffer: 64 * 1024 * 1024, timeout: 300000 });
const stdout = run.stdout ?? '';
const stderr = run.stderr ?? '';
writeFileSync(path.join(output, 'events.jsonl'), stdout);
writeFileSync(path.join(output, 'stderr.log'), stderr);
const events = [];
const malformed = [];
for (const [index, line] of stdout.split(/\r?\n/).entries()) {
  if (!line.trim()) continue;
  try { events.push(JSON.parse(line)); } catch { malformed.push(index + 1); }
}
const receipt = { schema_version: 1, started, finished: new Date().toISOString(),
  exit_code: run.status, signal: run.signal, error: run.error?.message ?? null,
  result: run.status === 0 && malformed.length === 0 && events.some(e => e.type === 'turn.completed') ? 'completed' : 'incomplete-preserve-evidence',
  event_count: events.length, malformed_lines: malformed,
  event_types: [...new Set(events.map(e => e.type))],
  prompt_sha256: createHash('sha256').update(prompt).digest('hex'),
  events_sha256: createHash('sha256').update(stdout).digest('hex'),
  stderr_sha256: createHash('sha256').update(stderr).digest('hex'),
  cli_version: version.stdout?.trim(), node_version: process.version,
};
writeFileSync(path.join(output, 'receipt.json'), JSON.stringify(receipt, null, 2) + '\n');
console.log(JSON.stringify(receipt, null, 2));
process.exitCode = receipt.result === 'completed' ? 0 : 1;
