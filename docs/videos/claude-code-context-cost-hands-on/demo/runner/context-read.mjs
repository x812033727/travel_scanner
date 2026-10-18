// What a session answered to "/context", with every word that is not on an allow list masked.
//
//   node <seed>/runner/context-read.mjs <logs>/<name>.stream.jsonl
//
// Nobody knows before the first run what /context prints without a terminal, or whether it
// prints at all. Whatever text the stream holds (the result line, any text Claude Code or the
// model wrote) is shown line by line, but a word is kept only when it is a number, a
// punctuation mark, one of the seed's own names, or one of the plain words below. Anything
// else, including every name and path that is not the seed's, becomes ___ . The count of masked
// words is printed, so a reader can tell how much is hidden without seeing it.
import { readFileSync } from 'node:fs';

const file = process.argv[2];
const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).flatMap((line) => {
  try { return [JSON.parse(line)]; } catch { return []; }
}).filter((line) => line.type !== 'rate_limit_event');
const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((block) => (typeof block === 'string' ? block : block?.text ?? textOf(block?.content) ?? '')).join('\n') : '');

const ALLOW = new Set(`a an and are as at available be before by can cannot category claude code command commands compact
context conversation count current custom deferred each empty estimate estimated for free from has in input interactive is isn't
it large left limit loaded local main max memory message messages mode model no none not of on only or output percent
percentage plugin plugins project prompt remaining reserved session size skill skills source space suggestions system
terminal the this to token tokens tool tools total unknown usage used user using when window with without agent agents
autocompact auto-compact buffer builtin built-in bundled file files hook hooks mcp server servers thinking
claude.md release-prep log-scout gear find_gear low_stock mcp__gear__find_gear mcp__gear__low_stock ship-kit
read edit write glob grep task toolsearch sonnet claude-sonnet-5-5 fare-sync`.split(/\s+/));
const cwd = String(init.cwd ?? '');
const spellings = cwd ? [...new Set([cwd, cwd.replaceAll('\\', '/'), cwd.replaceAll('/', '\\'), cwd.replaceAll('\\', '\\\\')])] : [];
let masked = 0;
const distinct = new Set();
const keep = (word) => {
  if (/^<lab>/.test(word)) return word;
  const bare = word.replace(/^[^\p{L}\p{N}<]+|[^\p{L}\p{N}>]+$/gu, '');
  if (!bare || /^[\d.,%:+\-~≈/()kKmM]+$/.test(bare) || ALLOW.has(bare.toLowerCase())) return word;
  masked += 1;
  distinct.add(bare.toLowerCase());
  return word.replace(bare, '___');
};
const show = (text) => {
  let shown = String(text ?? '').replace(/\u001b\[[0-9;]*[A-Za-z]/g, '');
  for (const each of spellings) shown = shown.split(each).join('<lab>');
  return shown.split('\n').map((line) => line.split(/(\s+)/).map((part) => (/^\s*$/.test(part) ? part : keep(part))).join('').slice(0, 160));
};

const results = lines.filter((line) => line.type === 'result');
const said = [];
for (const line of lines) {
  if (line.type === 'assistant' && !line.parent_tool_use_id) {
    for (const block of line.message?.content ?? []) if (block.type === 'text' && block.text) said.push(['assistant text', block.text]);
  } else if (line.type === 'user' && !line.parent_tool_use_id) {
    const content = line.message?.content;
    const text = typeof content === 'string' ? content : textOf((content ?? []).filter((block) => block.type !== 'tool_result'));
    if (text.trim()) said.push([`user-side text${line.isSynthetic ? ' (marked synthetic)' : ''}`, text]);
  } else if (line.type === 'system' && line.subtype !== 'init' && !/^hook_/.test(String(line.subtype))) {
    const text = [line.content, line.text, line.output, line.message].filter((each) => typeof each === 'string').join('\n');
    if (text.trim()) said.push([`system line (${line.subtype})`, text]);
  }
}
// An assistant line Claude Code wrote itself (model "<synthetic>", or a usage of zero) has no
// model request behind it, so it is not counted: ctx-cost.mjs reads it the same way.
const inputSide = (usage) => (usage?.input_tokens ?? 0) + (usage?.cache_creation_input_tokens ?? 0) + (usage?.cache_read_input_tokens ?? 0);
const requests = new Set(lines.filter((line) => line.type === 'assistant' && !line.parent_tool_use_id && line.message?.usage
  && line.message.model !== '<synthetic>' && inputSide(line.message.usage) > 0).map((line) => line.message.id));
const types = {};
for (const line of lines) { const key = line.type === 'system' ? `system/${line.subtype}` : line.type; types[key] = (types[key] ?? 0) + 1; }
console.log(`-- context-read.mjs | stream lines by type: ${Object.entries(types).map(([type, count]) => `${type} ${count}`).join(', ')}`);
console.log(`   requests of the main conversation that carry usage: ${requests.size} (0 means no model request was sent for this command)`);
results.forEach((result, at) => {
  console.log(`   result line ${at + 1}: ${result.subtype} | is_error ${result.is_error} | turns ${result.num_turns} | cost USD ${result.total_cost_usd} | result text ${String(result.result ?? '').length} chars, ${String(result.result ?? '').split('\n').length} lines`);
  for (const line of show(result.result).slice(0, 80)) console.log(`      | ${line}`);
});
for (const [label, text] of said) {
  console.log(`   ${label}: ${text.length} chars`);
  for (const line of show(text).slice(0, 60)) console.log(`      | ${line}`);
}
console.log(`   words masked: ${masked} | distinct ${distinct.size} (not printed)`);
