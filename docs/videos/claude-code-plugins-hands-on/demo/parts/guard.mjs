// 守門：已經存在的測試檔不能改。每被呼叫一次，留一行紀錄。
import { appendFileSync, existsSync } from 'node:fs';
import { readFileSync } from 'node:fs';
import { basename, join } from 'node:path';

const event = JSON.parse(readFileSync(0, 'utf8').trim());
const file = String(event.tool_input?.file_path ?? '');
const stop = /\.test\.[cm]?js$/.test(file) && existsSync(file);

// 紀錄：這支腳本放在哪裡、外掛根目錄的變數長什麼樣。
const home = import.meta.url.includes('/.claude/hooks/')
  ? 'project' : 'plugin';
const kit = process.env.CLAUDE_PLUGIN_ROOT;
const shape = !kit ? 'unset'
  : kit.includes('\\') ? 'backslash' : 'slash';
const root = process.env.CLAUDE_PROJECT_DIR ?? event.cwd;
const log = process.env.GUARD_LOG
  ?? join(root, 'guard-record.txt');
const what = `${event.tool_name} ${basename(file)}`;
const line = `guard(${home}) ${what}`
  + ` -> ${stop ? 'block' : 'pass'} | PLUGIN_ROOT ${shape}\n`;
// 寫不了紀錄也照樣守門。
try { appendFileSync(log, line); } catch { /* 略過 */ }

if (stop) {
  console.error('This test already exists: do not change it.');
  console.error('Fix the code instead. New tests are fine.');
  process.exitCode = 2;
}
