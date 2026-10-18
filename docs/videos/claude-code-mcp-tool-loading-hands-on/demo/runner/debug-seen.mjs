// What the debug record and stderr say about tool search and about loading, as counts and
// numbers only.
// Usage: node debug-seen.mjs <logs>/<name>.debug.txt <logs>/<name>.stderr.txt
// The debug record's format is not documented, so nothing here is scored and no line of it is
// printed whole. Four line shapes the previous video's records showed are read for their
// numbers and for words from a fixed list:
//   [ToolSearch:optimistic] mode=<word>, ENABLE_TOOL_SEARCH=<value>, result=<true|false>
//   Tool search disabled: <reason>
//   Dynamic tool loading: <k>/<n> deferred tools included      (one line per request)
//   ToolSearchTool: selected <tool>, <tool> ...
// A mode, a value or a reason that is not on the list below is printed as "(other)"; a tool name
// that is not the seed's is only counted. Any other line about tool search is a count.
import { existsSync, readFileSync } from 'node:fs';

const [debugFile, stderrFile] = process.argv.slice(2);
const linesOf = (file) => (file && existsSync(file) ? readFileSync(file, 'utf8').split('\n').filter(Boolean) : null);
const debug = linesOf(debugFile);
const stderr = linesOf(stderrFile);
const count = (lines, pattern) => lines.filter((line) => pattern.test(line)).length;
const tally = (list) => { const out = {}; for (const each of list) out[each] = (out[each] ?? 0) + 1; return out; };
const shown = (counts) => Object.entries(counts).map(([key, times]) => `${key} (x${times})`).join(' | ') || 'none';
const MODES = /^[a-z-]{2,12}$/;
const VALUES = /^(undefined|true|false|auto|auto:\d{1,3})$/;
const REASONS = ['no deferred tools available to search', 'ToolSearchTool is not available (may have been disallowed via disallowedTools).'];

if (debug === null) {
  console.log('   debug record: no such file');
} else {
  const about = debug.filter((line) => /tool.?search|deferr|dynamic tool loading/i.test(line));
  const decided = about.flatMap((line) => { const m = line.match(/\[ToolSearch:(\w+)\] mode=([^,\s]+), ENABLE_TOOL_SEARCH=([^,\s]+), result=(\w+)/); return m ? [m] : []; });
  const off = about.flatMap((line) => { const m = line.match(/Tool search disabled: (.*)$/); return m ? [m[1].trim()] : []; });
  const loaded = about.flatMap((line) => { const m = line.match(/Dynamic tool loading: (\d+)\/(\d+) deferred tools included/); return m ? [`${m[1]}/${m[2]}`] : []; });
  const selected = about.flatMap((line) => { const m = line.match(/ToolSearchTool: selected (.*)$/); return m ? [m[1].split(',').map((each) => each.trim()).filter(Boolean)] : []; });
  const known = decided.length + off.length + loaded.length + selected.length;
  console.log(`   debug record: ${debug.length} lines | about tool search or deferred tools: ${about.length} | of them in one of the four shapes read here: ${known} | in any other shape (count only): ${about.length - known}`);
  console.log(`   how tool search was decided: ${shown(tally(decided.map((m) => `mode=${MODES.test(m[2]) ? m[2] : '(other)'}, ENABLE_TOOL_SEARCH=${VALUES.test(m[3]) ? m[3] : '(other)'}, result=${/^(true|false)$/.test(m[4]) ? m[4] : '(other)'}`)))}`);
  console.log(`   "Tool search disabled" lines: ${off.length}${off.length ? ` | ${shown(tally(off.map((reason) => (REASONS.includes(reason) ? `"${reason.slice(0, 40)}"` : '(other)'))))}` : ''}`);
  console.log(`   "Dynamic tool loading: k/n deferred tools included", in order: ${loaded.join(', ') || 'none'}`);
  console.log(`   "ToolSearchTool: selected" lines: ${selected.length}${selected.length ? ` | tools named: ${selected.map((list) => `${list.length} (gear's ${list.filter((tool) => /^mcp__gear__[a-z_]+$/.test(tool)).length})`).join(', ')}` : ''}`);
  const says = [['userSettings', /userSettings/], ['policySettings or managed', /policySettings|managed/i], ['marketplace', /marketplace/i], ['installed_plugins', /installed_plugins/i],
    ['claude.ai or connector', /claude\.ai|claudeai|connector/i], ['MEMORY.md or auto memory', /MEMORY\.md|auto.?memory/i], ['InstructionsLoaded', /InstructionsLoaded/], ['WaitForMcpServers', /WaitForMcpServers/],
    ['tool_reference', /tool_reference/], ['defer_loading', /defer_loading/], ['threshold', /threshold/i]];
  console.log(`   lines that say: ${says.map(([label, pattern]) => `${label} ${count(debug, pattern)}`).join(' | ')}`);
  const quoted = debug.flatMap((line) => line.match(/MCP server "[^"]+"/gi) ?? []);
  console.log(`   MCP server "<name>" mentions: ${quoted.length} | with a name that is not gear: ${quoted.filter((each) => !/"gear"/.test(each)).length} (count only)`);
}
if (stderr === null) console.log('   stderr: no such file');
else console.log(`   stderr: ${stderr.length} lines | that say mcp ${count(stderr, /mcp/i)} | hook ${count(stderr, /hook/i)} | warning ${count(stderr, /warn/i)} | error ${count(stderr, /error/i)}`);
