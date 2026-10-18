// Builds two MADE-UP streams in a temporary folder, in the shape Claude Code 2.1.295 writes
// (system/init, assistant tool_use, system/hook_response, result), and runs tally.mjs on them.
// It checks the parser and the three scoring rules. It is not evidence of anything a model did,
// and the made-up streams are deleted when it ends. No session, no model.
// Usage: node <seed>/check-tally.mjs
import { spawnSync } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'md-lab-tally-'));
const cwd = join(scratch, 'md-lab');
const init = {
  type: 'system', subtype: 'init', cwd, model: 'made-up-model', claude_code_version: '0.0.0',
  permissionMode: 'default', tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write'], mcp_servers: [], plugins: [],
  memory_paths: {},
};
const call = (name, input) => ({ type: 'assistant', message: { content: [{ type: 'tool_use', name, input }] } });
const load = (stdout) => ({ type: 'system', subtype: 'hook_response', hook_event: 'InstructionsLoaded', stdout, exit_code: 0 });
const result = (text) => ({ type: 'result', subtype: 'success', num_turns: 5, permission_denials: [], result: text });

const withFile = [
  init,
  load('session_start Project CLAUDE.md\n'),
  call('Read', { file_path: join(cwd, 'src', 'text.mjs') }),
  call('Edit', { file_path: join(cwd, 'src', 'text.mjs'), old_string: 'a', new_string: 'b' }),
  call('Write', { file_path: join(cwd, 'checks', 'text.check.mjs'), content: '' }),
  call('Edit', { file_path: join(cwd, 'CHANGELOG.md'), old_string: 'a', new_string: 'b' }),
  result('加好了。\n\n**未驗證：測試沒有執行過。**'),
];
const withoutFile = [
  init,
  call('Glob', { pattern: '**/*' }),
  call('Read', { file_path: join(cwd, 'src', 'text.mjs') }),
  call('Edit', { file_path: join(cwd, 'src', 'text.mjs'), old_string: 'a', new_string: 'b' }),
  call('Write', { file_path: join(cwd, 'src', 'text.test.mjs'), content: '' }),
  call('Read', { file_path: join(scratch, 'elsewhere.txt') }),
  result('加好了，測試在 src/text.test.mjs。'),
];
const files = [['made-up-with', withFile], ['made-up-without', withoutFile]].map(([name, lines]) => {
  const file = join(scratch, `${name}.stream.jsonl`);
  writeFileSync(file, `${lines.map((line) => JSON.stringify(line)).join('\n')}\n`);
  return file;
});
const run = spawnSync(process.execPath, [join(here, 'tally.mjs'), ...files], { encoding: 'utf8' });
process.stdout.write(run.stdout);
process.stderr.write(run.stderr);
rmSync(scratch, { recursive: true, force: true });
process.exitCode = run.status ?? 1;
