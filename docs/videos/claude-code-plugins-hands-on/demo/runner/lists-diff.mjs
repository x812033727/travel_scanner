// runner: compares the init lists of two sessions without printing any name that is not the
// seed's or on the seed's lists of what Claude Code ships. For each list (plugins, skills, agents,
// slash_commands, tools): how many entries only the first has, only the second has, and which of
// those are the seed's or shipped; anything else is a count.
// Usage: node lists-diff.mjs <nameA> <nameB>
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { BUILT_IN_AGENTS, LOGS, readStream, SHIPPED_SKILLS } from './mask.mjs';

const [a, b] = process.argv.slice(2);
const initOf = (name) => readStream(readFileSync(join(LOGS, `${name}.stream.jsonl`), 'utf8')).find((l) => l.type === 'system' && l.subtype === 'init') ?? {};
const names = (list) => (list ?? []).map((each) => (typeof each === 'string' ? each : each.name));
const known = (name) => /^(ship-kit:)?(release-prep|log-scout)$/.test(name) || name === 'ship-kit' || SHIPPED_SKILLS.has(name) || BUILT_IN_AGENTS.has(name) || /^cc-plugin-/.test(name);
const A = initOf(a); const B = initOf(b);
for (const key of ['plugins', 'skills', 'agents', 'slash_commands', 'terminal_slash_commands', 'tools', 'capabilities']) {
  const la = names(A[key]); const lb = names(B[key]);
  const onlyA = la.filter((x) => !lb.includes(x)); const onlyB = lb.filter((x) => !la.includes(x));
  const show = (list) => `${list.length}${list.length ? ` (${list.map((x) => (known(String(x)) ? x : null)).filter(Boolean).join(', ') || 'none shown'}; not the seed's and not on the shipped lists: ${list.filter((x) => !known(String(x))).length})` : ''}`;
  console.log(`${key}: ${a} ${la.length}, ${b} ${lb.length} | only in ${a}: ${show(onlyA)} | only in ${b}: ${show(onlyB)}`);
}
