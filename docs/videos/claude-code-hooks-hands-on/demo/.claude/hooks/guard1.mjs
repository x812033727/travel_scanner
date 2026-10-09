import { existsSync, readFileSync } from 'node:fs';

const event = JSON.parse(readFileSync(0, 'utf8').trim());
const file = String(event.tool_input?.file_path ?? '');

if (/\.test\.[cm]?js$/.test(file) && existsSync(file)) {
  console.error('This test already exists: do not change it.');
  console.error('Fix the code instead. New tests are fine.');
  process.exitCode = 1;
}
