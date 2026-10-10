// What the debug record and stderr of one session say about permission rules, without printing
// any rule that is not the seed's: a rule-shaped string, Tool(...), is printed only when it is
// one of the rules in the seed's rules file; every other one is counted. A tool call written the
// same way (for example a Bash call with its command) also counts as "other", so a number above
// zero there is a reason to look, not a finding.
// Usage: node rules-seen.mjs <rules.json> <debug.txt> <stderr.txt>
import { existsSync, readFileSync } from 'node:fs';

const [rulesFile, debugFile, stderrFile] = process.argv.slice(2);
const permissions = JSON.parse(readFileSync(rulesFile, 'utf8')).permissions ?? {};
const mine = new Set(['allow', 'ask', 'deny'].flatMap((list) => permissions[list] ?? []));
const read = (file) => (file && existsSync(file) ? readFileSync(file, 'utf8') : '');
const shaped = /\b(?:Bash|PowerShell|Read|Edit|Write|Glob|Grep|WebFetch|WebSearch|Agent|Skill|NotebookEdit|mcp__[A-Za-z0-9_-]+)\([^()\n]{1,120}\)/g;

for (const [label, text] of [['debug record', read(debugFile)], ['stderr', read(stderrFile)]]) {
  const lines = text.split('\n');
  const found = text.match(shaped) ?? [];
  const seeds = new Map();
  let other = 0;
  for (const each of found) {
    if (mine.has(each)) seeds.set(each, (seeds.get(each) ?? 0) + 1);
    else other += 1;
  }
  const count = (pattern) => lines.filter((line) => pattern.test(line)).length;
  console.log(`${label}: ${lines.length} lines | mentioning "permission": ${count(/permission/i)} | "trust": ${count(/trust/i)} | "userSettings" or "user settings": ${count(/user ?settings/i)} | "policySettings" or "managed": ${count(/policy ?settings|managed/i)} | "flagSettings" or "cliArg": ${count(/flag ?settings|cliArg/i)}`);
  console.log(`  rule-shaped strings: the seed's own ${[...seeds.values()].reduce((a, b) => a + b, 0)} | any other ${other} (count only)`);
  for (const [rule, times] of [...seeds].sort()) console.log(`    ${rule} x${times}`);
  const ignoring = lines.filter((line) => /Ignoring \d+ permissions\./.test(line));
  console.log(`  lines that say a permissions entry was ignored: ${ignoring.length}`);
  for (const line of ignoring.slice(0, 3)) console.log(`    ${line.replace(/^\S+Z? ?\[[A-Z]+\] ?/, '').slice(0, 240)}`);
}
