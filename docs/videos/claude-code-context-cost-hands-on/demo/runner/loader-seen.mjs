// What the debug record and stderr say about loading, as counts only.
// Usage: node loader-seen.mjs <logs>/<name>.debug.txt <logs>/<name>.stderr.txt
// The debug record's format is not documented, so nothing here is scored and no line of it is
// printed: a line that names a seed part can name something else too. Every figure is a count;
// the only words taken from the record are a fixed list of source words ("user: 0", "project: 1").
import { existsSync, readFileSync } from 'node:fs';

const [debugFile, stderrFile] = process.argv.slice(2);
const linesOf = (file) => (file && existsSync(file) ? readFileSync(file, 'utf8').split('\n').filter(Boolean) : null);
const debug = linesOf(debugFile);
const stderr = linesOf(stderrFile);
const count = (lines, pattern) => lines.filter((line) => pattern.test(line)).length;

if (debug === null) {
  console.log('   debug record: no such file');
} else {
  const seeds = [['CLAUDE.md', /CLAUDE\.md/], ['release-prep', /release-prep/], ['log-scout', /log-scout/], ['gear (as a word)', /(^|[^A-Za-z0-9_-])gear([^A-Za-z0-9_-]|$)/],
    ['guard.mjs', /guard\.mjs/], ['note.mjs', /note\.mjs/], ['seen.mjs', /seen\.mjs/], ['ship-kit', /ship-kit/]];
  console.log(`   debug record: ${debug.length} lines | lines that name the seed's parts: ${seeds.map(([label, pattern]) => `${label} ${count(debug, pattern)}`).join(' | ')}`);
  const pairs = {};
  for (const line of debug.filter((each) => /skill|agent|plugin|hook|memory|CLAUDE\.md|mcp/i.test(each))) {
    // Only the listed source words, alone or with "s" or "Settings" after them. Any other word
    // that merely begins with one of them (a name) is not a source and is never printed.
    for (const pair of line.match(/\b(managed|policy|user|project|local|plugin|built-?in|bundled|flag|cli|inline|session|enterprise|dynamic)(?:s|Settings)?: ?\d+/gi) ?? []) pairs[pair] = (pairs[pair] ?? 0) + 1;
  }
  console.log(`   "source: number" pairs on lines about skills, agents, plugins, hooks, memory or MCP: ${Object.entries(pairs).map(([pair, times]) => `${pair} (x${times})`).join(' | ') || 'none'}`);
  const says = [['userSettings', /userSettings/], ['policySettings or managed', /policySettings|managed/i], ['marketplace', /marketplace/i], ['installed_plugins', /installed_plugins/i],
    ['synced', /synced/i], ['claude.ai or connector', /claude\.ai|claudeai|connector/i], ['advisor', /advisor/i], ['trust', /trust/i], ['tool search', /tool.?search/i],
    ['deferred', /deferr/i], ['MEMORY.md or auto memory', /MEMORY\.md|auto.?memory/i], ['SessionStart', /SessionStart/], ['InstructionsLoaded', /InstructionsLoaded/]];
  console.log(`   lines that say: ${says.map(([label, pattern]) => `${label} ${count(debug, pattern)}`).join(' | ')}`);
  const quoted = debug.flatMap((line) => line.match(/MCP server "[^"]+"/gi) ?? []);
  console.log(`   MCP server "<name>" mentions: ${quoted.length} | with a name that is not gear: ${quoted.filter((each) => !/"gear"/.test(each)).length} (count only)`);
  const ids = new Set(debug.flatMap((line) => line.match(/[a-z0-9][a-z0-9._-]*@(inline|skills-dir|synced|[a-z0-9][a-z0-9._-]*)/gi) ?? []).filter((id) => !id.startsWith('ship-kit@') && !/@\d/.test(id)));
  console.log(`   plugin ids of the form name@origin that are not ship-kit's, distinct: ${ids.size} (count only; Claude Code reads its own install records whether or not anything is loaded)`);
}
if (stderr === null) console.log('   stderr: no such file');
else console.log(`   stderr: ${stderr.length} lines | that say plugin ${count(stderr, /plugin/i)} | trust ${count(stderr, /trust/i)} | hook ${count(stderr, /hook/i)} | mcp ${count(stderr, /mcp/i)} | warning ${count(stderr, /warn/i)}`);
