// What a session said, for the record and for cards: the text of every result line, and the
// first six lines of the message Claude Code adds to the conversation when a skill of the seed's
// is called (the skill's body). Nobody has to open the raw stream by hand for either.
//
//   node <seed>/runner/said.mjs <logs>/<name>.stream.jsonl      (KIT_DIR may name the plugin folder)
//
// The project folder (the init event's cwd) is printed as <lab> and the plugin folder as
// <plugin>, in every spelling. A message Claude Code added that is not a skill body from one of
// those two folders is a size only: its text is never printed. Rate-limit events are never read.
import { readFileSync } from 'node:fs';

const file = process.argv[2];
const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap((line) => {
  try { return [JSON.parse(line)]; } catch { return []; }
}).filter((line) => line.type !== 'rate_limit_event');
const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((block) => (typeof block === 'string' ? block : block?.text ?? textOf(block?.content) ?? '')).join('\n') : '');
const spellings = (path) => (path ? [...new Set([path, path.replaceAll('\\', '/'), path.replaceAll('/', '\\'), path.replaceAll('\\', '\\\\')])] : []);
const marks = [[String(init.cwd ?? ''), '<lab>'], [String(process.env.KIT_DIR ?? ''), '<plugin>']];
const placed = (text) => {
  let shown = String(text ?? '').replace(/\u001b\[[0-9;]*[A-Za-z]/g, '');
  for (const [path, mark] of marks) for (const each of spellings(path)) shown = shown.split(each).join(mark);
  return shown;
};
const WIDE = 160;

const results = lines.filter((line) => line.type === 'result');
console.log(`-- said.mjs | result lines ${results.length}`);
results.forEach((result, at) => {
  const text = placed(typeof result.result === 'string' ? result.result : '');
  const rows = text ? text.split('\n') : [];
  console.log(`   result ${at + 1}: ${result.subtype} | is_error ${result.is_error ?? '-'} | text ${[...text].length} chars, ${rows.length} lines${rows.length > 60 ? ' (the first 60 shown)' : ''}`);
  for (const row of rows.slice(0, 60)) console.log(`      | ${row.slice(0, WIDE)}`);
});

// Messages on the user side of the main conversation that Claude Code marked synthetic.
const added = lines.filter((line) => line.type === 'user' && !line.parent_tool_use_id && line.isSynthetic);
console.log(`   messages Claude Code added to the main conversation (marked synthetic): ${added.length}`);
added.forEach((line, at) => {
  const content = line.message?.content;
  const text = placed(typeof content === 'string' ? content : textOf((content ?? []).filter((block) => block.type !== 'tool_result')));
  const rows = text.split('\n');
  const ours = /^Base directory for this skill: <(lab|plugin)>/.test(rows[0] ?? '');
  console.log(`   added ${at + 1}: ${[...text].length} chars, ${rows.length} lines | ${ours ? 'a skill body from the project or the plugin; its first six lines:' : 'not shown (not a skill body from the project or the plugin)'}`);
  if (ours) for (const row of rows.slice(0, 6)) console.log(`      | ${row.slice(0, WIDE)}`);
});
