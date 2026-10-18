// What a session said, for the record and for cards: the text of every result line. Nobody has
// to open the raw stream by hand for it.
//
//   node <seed>/runner/said.mjs <logs>/<name>.stream.jsonl
//
// The project folder (the init event's cwd) is printed as <lab>, in every spelling. A message
// Claude Code added to the conversation is a size only: its text is never printed. Rate-limit
// events are never read.
import { readFileSync } from 'node:fs';

const file = process.argv[2];
const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap((line) => {
  try { return [JSON.parse(line)]; } catch { return []; }
}).filter((line) => line.type !== 'rate_limit_event');
const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((block) => (typeof block === 'string' ? block : block?.text ?? textOf(block?.content) ?? '')).join('\n') : '');
const spellings = (path) => (path ? [...new Set([path, path.replaceAll('\\', '/'), path.replaceAll('/', '\\'), path.replaceAll('\\', '\\\\')])] : []);
const placed = (text) => {
  let shown = String(text ?? '').replace(/\u001b\[[0-9;]*[A-Za-z]/g, '');
  for (const each of spellings(String(init.cwd ?? ''))) shown = shown.split(each).join('<lab>');
  return shown;
};
const WIDE = 160;

const results = lines.filter((line) => line.type === 'result');
console.log(`-- said.mjs | result lines ${results.length}`);
results.forEach((result, at) => {
  const text = placed(typeof result.result === 'string' ? result.result : '');
  const rows = text ? text.split('\n') : [];
  console.log(`   result ${at + 1}: ${result.subtype} | is_error ${result.is_error ?? '-'} | text ${[...text].length} chars, ${rows.length} lines${rows.length > 20 ? ' (the first 20 shown)' : ''}`);
  for (const row of rows.slice(0, 20)) console.log(`      | ${row.slice(0, WIDE)}`);
});
const added = lines.filter((line) => line.type === 'user' && !line.parent_tool_use_id && line.isSynthetic);
console.log(`   messages Claude Code added to the main conversation (marked synthetic): ${added.length}${added.length ? ` | chars ${added.map((line) => [...textOf(line.message?.content)].length).join(', ')} (text not shown)` : ''}`);
