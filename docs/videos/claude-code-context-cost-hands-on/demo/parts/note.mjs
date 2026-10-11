// 開場提示：session 開始時印三行字，Claude 會讀到。
import { appendFileSync } from 'node:fs';
import { join } from 'node:path';

const root = process.env.CLAUDE_PROJECT_DIR ?? process.cwd();
const log = process.env.NOTE_LOG
  ?? join(root, 'note-record.txt');
const lines = [
  '交班提示（固定文字，示範用）',
  '- 這一輪要出的版本是 1.2.1。',
  '- 沒結束的 job 以 logs/ 的紀錄為準，不要用猜的。',
];
// 寫不了紀錄也照樣印。
const mark = `note said ${lines.length} lines\n`;
try { appendFileSync(log, mark); } catch { /* 略過 */ }
console.log(lines.join('\n'));
