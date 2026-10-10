// runner: what the debug record and stderr of each session say about permission rules, as counts
// only. A rule-shaped string is Tool(...) for a built-in tool name; this video's own rules are
// bare tool names passed with --allowedTools (no parentheses), so every rule-shaped string is
// counted as "other" and none is printed. A count above zero is a reason to look, not a finding:
// a tool call written the same way is counted too.
// Usage: node rules-count.mjs <name> [<name> ...]
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { LOGS } from './mask.mjs';

const shaped = /\b(?:Bash|PowerShell|Read|Edit|Write|Glob|Grep|WebFetch|WebSearch|Agent|Task|Skill|NotebookEdit|mcp__[A-Za-z0-9_-]+)\([^()\n]{1,160}\)/g;
for (const name of process.argv.slice(2)) {
  const out = [];
  for (const [label, file] of [['debug', `${name}.debug.txt`], ['stderr', `${name}.stderr.txt`]]) {
    const path = join(LOGS, file);
    const text = existsSync(path) ? readFileSync(path, 'utf8') : '';
    const lines = text.split('\n');
    const count = (re) => lines.filter((l) => re.test(l)).length;
    const found = text.match(shaped) ?? [];
    const byTool = {};
    for (const each of found) { const tool = each.split('(')[0].replace(/^mcp__.*/, 'mcp__(a server)'); byTool[tool] = (byTool[tool] ?? 0) + 1; }
    out.push(`${label}: ${lines.filter(Boolean).length} lines | rule-shaped strings ${found.length}${found.length ? ` (${Object.entries(byTool).map(([t, n]) => `${t} ${n}`).join(', ')})` : ''} | lines saying "permission" ${count(/permission/i)}, "allowedTools" or "cliArg" or "flagSettings" ${count(/allowedTools|cliArg|flagSettings/)}, "userSettings" ${count(/userSettings|user settings/i)}, "projectSettings" ${count(/projectSettings/)}, "localSettings" ${count(/localSettings/)}, "policySettings" or "managed" ${count(/policySettings|managed/i)}, "Ignoring" ${count(/Ignoring \d+ /)}, "trust" ${count(/trust/i)}`);
  }
  console.log(`${name} | ${out.join(' || ')}`);
}
