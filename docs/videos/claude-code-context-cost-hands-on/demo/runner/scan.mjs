// Runner's check after every session (not in the brief). Counts and the seed's own names only.
//   node scan.mjs <logs> <name>
// Prints: where each model name appears (init, main-conversation messages, messages forwarded
// from under an Agent call, modelUsage keys of every result line); the files the run left in
// <logs> under this name; the inherited-variable line of the record as a count and a digest
// (names are never printed); what changed in the project against the listing in the record.
import { createHash } from 'node:crypto';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const [logs, name] = process.argv.slice(2);
const stream = readFileSync(join(logs, `${name}.stream.jsonl`), 'utf8').split('\n').filter(Boolean).flatMap((line) => {
  try { return [JSON.parse(line)]; } catch { return []; }
}).filter((line) => line.type !== 'rate_limit_event');
const tally = new Map();
const add = (label) => tally.set(label, (tally.get(label) ?? 0) + 1);
const seenIds = new Set();
for (const line of stream) {
  if (line.type === 'system' && line.subtype === 'init') add(`init model: ${line.model}`);
  if (line.type === 'assistant') {
    const id = line.message?.id;
    const where = line.parent_tool_use_id ? 'under an Agent call' : 'main conversation';
    if (id && seenIds.has(id)) continue;
    if (id) seenIds.add(id);
    add(`assistant message, ${where}: ${line.message?.model}`);
  }
  if (line.type === 'result') for (const key of Object.keys(line.modelUsage ?? {})) add(`result modelUsage key: ${key}`);
}
console.log(`== scan ${name}`);
for (const [label, count] of [...tally].sort()) console.log(`   ${label} (x${count})`);
const other = [...tally.keys()].filter((label) => !/claude-sonnet-|<synthetic>/.test(label.split(': ').at(-1)));
console.log(`   model names that are not a sonnet: ${other.length}`);

const record = readFileSync(join(logs, `${name}.session.txt`), 'utf8').split('\n');
const vars = record.find((line) => line.startsWith('## variables this shell hands the session')) ?? '';
const [, list = '', removed = ''] = vars.match(/shell\): (.*)\| of them removed for the session:(.*)$/) ?? [];
const namesList = list.trim().split(/\s+/).filter(Boolean);
console.log(`   inherited variables named in the record: ${namesList.length} | digest of the names ${createHash('sha256').update(namesList.join(' ')).digest('hex').slice(0, 12)} | of the script's five removed: ${removed.trim() === 'none' ? 0 : removed.trim().split(/\s+/).filter(Boolean).length}`);

const files = readdirSync(logs).filter((entry) => entry.startsWith(`${name}.`)).sort();
console.log(`   in <logs> under this name: ${files.map((entry) => { const s = statSync(join(logs, entry)); return s.isDirectory() ? `${entry}/` : `${entry} (${s.size} B)`; }).join(', ')}`);

// The project as the session left it against the listing taken before it.
const walk = (dir) => (existsSync(dir) ? readdirSync(dir).flatMap((entry) => { const path = join(dir, entry); return statSync(path).isDirectory() ? walk(path) : [path]; }) : []);
const lab = join(logs, `${name}.lab`);
const after = new Map(walk(lab).map((path) => [`./${relative(lab, path).replaceAll('\\', '/')}`, createHash('sha256').update(readFileSync(path)).digest('hex').slice(0, 16)]));
const before = new Map();
let inHashes = false;
for (const line of record) {
  if (line.startsWith('$ sha256sum')) { inHashes = before.size === 0; continue; }
  if (line.startsWith('## ')) inHashes = false;
  const match = inHashes && line.match(/^([0-9a-f]{16}) \*(\.\/.*)$/);
  if (match) before.set(match[2], match[1]);
}
const added = [...after.keys()].filter((path) => !before.has(path));
const gone = [...before.keys()].filter((path) => !after.has(path));
const changed = [...after.keys()].filter((path) => before.has(path) && before.get(path) !== after.get(path));
console.log(`   project files before ${before.size}, after ${after.size} | added: ${added.join(' ') || 'none'} | removed: ${gone.join(' ') || 'none'} | changed: ${changed.join(' ') || 'none'}`);
