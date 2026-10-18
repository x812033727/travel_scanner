// Runs the note hook (the SessionStart hook that prints three lines) on a made-up event and
// prints exactly what it wrote to stdout, with its size, and what it left in its record.
// No session, no model: only node and a temporary folder.
// Usage: node <seed>/check-note.mjs
import { spawnSync } from 'node:child_process';
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'note-check-'));
const record = join(scratch, 'note.txt');
const event = { hook_event_name: 'SessionStart', source: 'startup', cwd: scratch };
const run = (log) => spawnSync(process.execPath, [join(seed, 'parts', 'note.mjs')], {
  input: JSON.stringify(event), encoding: 'utf8',
  env: { PATH: process.env.PATH, SystemRoot: process.env.SystemRoot ?? '', CLAUDE_PROJECT_DIR: scratch, NOTE_LOG: log },
});

let failed = 0;
const first = run(record);
console.log(`exit ${first.status} | stderr bytes ${first.stderr.length}`);
console.log('stdout, as Claude Code would receive it:');
for (const line of first.stdout.replace(/\n$/, '').split('\n')) console.log(`   | ${line}`);
const body = first.stdout.replace(/\n$/, '');
console.log(`stdout without the final newline: ${body.split('\n').length} lines | ${[...body].length} characters | ${Buffer.byteLength(body)} bytes (UTF-8)`);
const second = run(join(scratch, 'no-such-folder', 'note.txt'));
const lines = existsSync(record) ? readFileSync(record, 'utf8').split('\n').filter(Boolean) : [];
console.log(`the record after two runs (the second could not write one): ${lines.length} line${lines.length === 1 ? '' : 's'}`);
for (const line of lines) console.log(`   ${line}`);
const checks = [
  ['exit 0, nothing on stderr', first.status === 0 && !first.stderr],
  ['three lines on stdout', body.split('\n').length === 3],
  ['one line in the record', lines.length === 1 && lines[0] === 'note said 3 lines'],
  ['it prints the same text when the record cannot be written', second.status === 0 && second.stdout === first.stdout],
];
for (const [label, ok] of checks) { if (!ok) failed += 1; console.log(`${ok ? 'ok  ' : 'FAIL'} ${label}`); }
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
