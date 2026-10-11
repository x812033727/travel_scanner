// Reads the stream-json output of `claude -p --output-format stream-json --verbose` and prints,
// per session: what was offered, the order of tool calls and instruction-file loads, the files
// written, the reply's last line, and the three checks this video counts. Paths are printed
// relative to the session's cwd; anything outside it prints as "(outside the project)".
// Usage: node <seed>/tally.mjs <name>.stream.jsonl [<name>.stream.jsonl ...]
import { readFileSync } from 'node:fs';
import { basename, isAbsolute, win32, posix } from 'node:path';

const TEAM = /^checks\/[^/]+\.check\.mjs$/;
const LOCAL = /^src\/[^/]+\.test\.mjs$/;
const TEST_LIKE = /(\.check|\.test|\.spec)\.[cm]?js$|^(tests?|__tests__|spec|checks)\//;
const UNVERIFIED = /^[\s>*_`-]*未驗證[：:]/;

function relativeTo(cwd, file) {
  if (typeof file !== 'string' || !file) return '';
  const tool = /^[A-Za-z]:[\\/]/.test(cwd) ? win32 : posix;
  if (!tool.isAbsolute(file)) return file.replaceAll('\\', '/');
  const rel = tool.relative(cwd, file);
  if (!rel || rel.startsWith('..') || tool.isAbsolute(rel) || isAbsolute(rel)) return '(outside the project)';
  return rel.replaceAll('\\', '/');
}

function digest(file) {
  const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).map((line) => JSON.parse(line));
  const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
  const result = lines.findLast((line) => line.type === 'result') ?? {};
  const cwd = init.cwd ?? '';
  const timeline = [];
  const written = new Set();
  const readInstructions = [];
  let calls = 0;
  for (const line of lines) {
    if (line.type === 'system' && line.subtype === 'hook_response' && line.hook_event === 'InstructionsLoaded') {
      timeline.push(`load  ${String(line.stdout ?? '').trim()} [hook exit ${line.exit_code}]`);
    }
    if (line.type !== 'assistant') continue;
    for (const block of line.message?.content ?? []) {
      if (block.type !== 'tool_use') continue;
      calls += 1;
      const input = block.input ?? {};
      const target = relativeTo(cwd, input.file_path ?? input.path ?? '');
      const detail = target || input.pattern || input.command || '';
      timeline.push(`call ${String(calls).padStart(2)} ${block.name} ${String(detail).split('\n')[0].slice(0, 90)}`);
      if ((block.name === 'Write' || block.name === 'Edit') && target) written.add(target);
      if (/(^|\/)CLAUDE(\.local)?\.md$|^\.claude\/rules\//.test(target)) readInstructions.push(`${block.name} ${target}`);
    }
  }
  const reply = typeof result.result === 'string' ? result.result : '';
  const lastLine = reply.split('\n').map((line) => line.trim()).filter(Boolean).at(-1) ?? '';
  const tests = [...written].filter((path) => TEST_LIKE.test(path));
  return {
    name: basename(file).replace(/\.stream\.jsonl$/, ''),
    model: init.model, version: init.claude_code_version, permissionMode: init.permissionMode,
    tools: (init.tools ?? []).filter((tool) => !tool.startsWith('mcp__')),
    mcpTools: (init.tools ?? []).filter((tool) => tool.startsWith('mcp__')).length,
    mcpServers: (init.mcp_servers ?? []).length,
    plugins: (init.plugins ?? []).map((plugin) => (typeof plugin === 'string' ? plugin : plugin.name)),
    memoryPathKeys: Object.keys(init.memory_paths ?? {}),
    subtype: result.subtype, turns: result.num_turns, denials: (result.permission_denials ?? []).length,
    timeline, written: [...written], tests, readInstructions, lastLine,
    l1Team: tests.some((path) => TEAM.test(path)), l1Local: tests.some((path) => LOCAL.test(path)),
    l1Other: tests.filter((path) => !TEAM.test(path) && !LOCAL.test(path)),
    l2: written.has('CHANGELOG.md'), l3: UNVERIFIED.test(lastLine),
  };
}

const yes = (value) => (value ? 'yes' : 'no');
const sessions = process.argv.slice(2).map(digest);
for (const s of sessions) {
  console.log(`== ${s.name} | model ${s.model} | Claude Code ${s.version} | permission mode ${s.permissionMode}`);
  console.log(`   result ${s.subtype}, ${s.turns} turns, ${s.denials} permission denials`);
  console.log(`   built-in tools offered (${s.tools.length}): ${s.tools.join(' ')}`);
  console.log(`   MCP servers ${s.mcpServers}, MCP tools ${s.mcpTools} | plugins: ${s.plugins.join(', ') || 'none'} | memory_paths keys: ${s.memoryPathKeys.join(', ') || 'none'}`);
  for (const entry of s.timeline) console.log(`   ${entry}`);
  console.log(`   files written: ${s.written.join(', ') || 'none'}`);
  console.log(`   opened an instruction file with a tool: ${s.readInstructions.join('; ') || 'no'}`);
  console.log(`   last line of the reply: ${s.lastLine}`);
  console.log(`   L1 test file: ${s.tests.join(', ') || 'none'} -> checks/<module>.check.mjs ${yes(s.l1Team)}, src/<module>.test.mjs ${yes(s.l1Local)}${s.l1Other.length ? `, elsewhere ${s.l1Other.join(', ')}` : ''}`);
  console.log(`   L2 CHANGELOG.md written: ${yes(s.l2)}`);
  console.log(`   L3 last line starts with 未驗證：: ${yes(s.l3)}`);
}
if (sessions.length > 1) {
  console.log('\nname | test file | L1 team | L1 local | L2 changelog | L3 last line | opened instruction file | turns');
  for (const s of sessions) {
    console.log([s.name, s.tests.join(' + ') || 'none', yes(s.l1Team), yes(s.l1Local), yes(s.l2), yes(s.l3), yes(s.readInstructions.length), s.turns].join(' | '));
  }
}
