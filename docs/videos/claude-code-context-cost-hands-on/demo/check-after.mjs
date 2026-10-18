// Runs runner/after.mjs, runner/said.mjs, runner/loader-seen.mjs and runner/context-read.mjs on
// made-up records and checks what they say: a clean base arm, an arm with every seed part, the
// plugin arm, the arm with tool search turned off, a session with things that are not the seed's
// (which must say STOP and print none of their names), a session with Bash among its tools, a
// session whose file tool was aimed outside the project, a made-up debug record with names that
// begin like a source word, and a made-up answer to /context.
// No session, no model.
// Usage: node <seed>/check-after.mjs
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'after-check-'));
const lab = join(scratch, 'lab');
const kit = join(scratch, 'ship-kit');
const away = resolve('/made-up/elsewhere');
const TOOLS = ['Task', 'Edit', 'Glob', 'Grep', 'Read', 'Skill', 'ToolSearch', 'Write'];
const SHIPPED = ['debug', 'code-review', 'simplify'];
const BUILT = ['Explore', 'Plan', 'general-purpose'];
const own = [{ name: 'cc-plugin-one', path: '/made/up' }];
const use = { input_tokens: 5, cache_creation_input_tokens: 100, cache_read_input_tokens: 9000, output_tokens: 3 };
const init = (extra) => ({ type: 'system', subtype: 'init', claude_code_version: '0.0.0-made-up', model: 'claude-sonnet-made-up', permissionMode: 'default', cwd: lab,
  tools: TOOLS, mcp_servers: [], skills: SHIPPED, agents: BUILT, slash_commands: SHIPPED, plugins: own, ...extra });
const say = (id, content) => ({ type: 'assistant', parent_tool_use_id: null, message: { id, model: 'claude-sonnet-made-up', usage: use, content } });
const result = (text = '十二個月') => ({ type: 'result', subtype: 'success', is_error: false, num_turns: 1, total_cost_usd: 0.01, usage: use, modelUsage: { 'claude-sonnet-made-up': {} }, result: text });
const gearOn = { tools: [...TOOLS, 'mcp__gear__find_gear', 'mcp__gear__low_stock'], mcp_servers: [{ name: 'gear', status: 'connected' }] };

function put(name, arm, stream, files = {}) {
  writeFileSync(join(scratch, `${name}.stream.jsonl`), `${stream.map((line) => JSON.stringify(line)).join('\n')}\n`);
  writeFileSync(join(scratch, `${name}.session.txt`), `# ${name} | arm ${arm} | start made-up\n`);
  for (const [file, text] of Object.entries(files)) {
    mkdirSync(dirname(join(scratch, file)), { recursive: true });
    writeFileSync(join(scratch, file), text);
  }
}
put('a-base', 'base', [init({}), say('m1', [{ type: 'text', text: '十二個月' }]), result()]);
// The skill body Claude Code adds after a Skill call: a user line marked synthetic whose first
// line is the skill's folder. A second synthetic line that is not a skill body must not be shown.
const body = `Base directory for this skill: ${join(lab, '.claude', 'skills', 'release-prep')}\n\n# 發版準備\n\n1. 改版號。\n2. 改 CHANGELOG。\n3. 改 README。\n4. 寫發版單。\n\nARGUMENTS: 1.2.1`;
put('a-all', 'work', [
  init({ ...gearOn, skills: [...SHIPPED, 'release-prep'], agents: [...BUILT, 'log-scout'], slash_commands: [...SHIPPED, 'release-prep'] }),
  say('m1', [{ type: 'tool_use', id: 't1', name: 'Skill', input: { skill: 'release-prep', args: '1.2.1' } }, { type: 'tool_use', id: 't2', name: 'Agent', input: { subagent_type: 'log-scout', prompt: 'x' } }, { type: 'tool_use', id: 't3', name: 'ToolSearch', input: { query: 'select:mcp__gear__find_gear' } }]),
  { type: 'user', parent_tool_use_id: null, isSynthetic: true, message: { role: 'user', content: [{ type: 'text', text: body }] } },
  { type: 'user', parent_tool_use_id: null, isSynthetic: true, message: { role: 'user', content: [{ type: 'text', text: `a made-up notice that names ${join(away, 'private-output.txt')}\nsecond line` }] } },
  say('m2', [{ type: 'tool_use', id: 't4', name: 'mcp__gear__find_gear', input: { code: 'G-417' } }, { type: 'tool_use', id: 't5', name: 'Edit', input: { file_path: 'package.json' } }, { type: 'tool_use', id: 't6', name: 'Glob', input: { pattern: '**/*.log', path: lab } }]),
  say('m3', [{ type: 'text', text: 'done' }]), result(`改好了，在 ${join(lab, 'package.json')}。\n下一步：跑測試。`),
], {
  'a-all.seen.txt': 'InstructionsLoaded session_start Project CLAUDE.md\nPreToolUse by=main id=0001 Skill skill=release-prep keys=skill,args\nPreToolUse by=main id=0005 Edit package.json\n',
  'a-all.guard.txt': 'guard(project) Edit package.json -> pass | PLUGIN_ROOT unset\n',
  'a-all.lab/server/requests.txt': '01 +     0ms start\n02 +   100ms initialize asks 2025-11-25\n03 +   200ms tools/list\n04 +   300ms tools/call find_gear {"code":"G-417"}\n',
});
// The plugin arm, with the permission mode under its other name.
put('a-plugin', 'plugin', [
  init({ permissionMode: 'manual', skills: [...SHIPPED, 'ship-kit:release-prep'], agents: [...BUILT, 'ship-kit:log-scout'], plugins: [...own, { name: 'ship-kit', path: kit }] }),
  say('m1', [{ type: 'tool_use', id: 't1', name: 'Read', input: { file_path: join(kit, 'skills', 'release-prep', 'template.md') } }]),
  say('m2', [{ type: 'text', text: '十二個月' }]), result(),
]);
// Tool search turned off: ToolSearch is gone from the list, the server's two tools are there.
put('a-upfront', 'upfront', [
  init({ tools: [...TOOLS.filter((tool) => tool !== 'ToolSearch'), 'mcp__gear__find_gear', 'mcp__gear__low_stock'], mcp_servers: [{ name: 'gear', status: 'connected' }] }),
  say('m1', [{ type: 'text', text: '十二個月' }]), result(),
]);
put('a-intruder', 'base', [
  init({ tools: [...TOOLS, 'mcp__secretsrv__peek'], mcp_servers: [{ name: 'secretsrv', status: 'connected' }], skills: [...SHIPPED, 'private-skill-x'], agents: [...BUILT, 'private-agent-y'], plugins: [...own, { name: 'private-plugin-z', path: '/somewhere/private' }] }),
  say('m1', [{ type: 'tool_use', id: 't1', name: 'mcp__secretsrv__peek', input: { what: 'private-thing' } }]), result(),
], { 'a-intruder.seen.txt': 'InstructionsLoaded session_start User (outside the project)\n' });
put('a-bash', 'base', [init({ tools: [...TOOLS, 'Bash'] }), say('m1', [{ type: 'text', text: '十二個月' }]), result()]);
// A write aimed outside the project: the hook's record says BLOCKED, and the stream has the call.
put('a-outside', 'work', [
  init({ ...gearOn, skills: [...SHIPPED, 'release-prep'], agents: [...BUILT, 'log-scout'], slash_commands: [...SHIPPED, 'release-prep'] }),
  say('m1', [{ type: 'tool_use', id: 't1', name: 'Write', input: { file_path: join(away, 'private-notes.txt'), content: 'x' } }, { type: 'tool_use', id: 't2', name: 'Glob', input: { pattern: '~/**/*.md' } }]),
  say('m2', [{ type: 'text', text: 'done' }]), result('done'),
], { 'a-outside.seen.txt': 'InstructionsLoaded session_start Project CLAUDE.md\nPreToolUse by=main id=0001 Write (outside the project) | BLOCKED\nPreToolUse by=main id=0002 Glob (outside the project) | BLOCKED\n' });
put('a-context', 'context', [
  init({ skills: [...SHIPPED, 'release-prep'] }),
  // The line Claude Code writes itself for a local command: no model request is behind it.
  { type: 'assistant', parent_tool_use_id: null, message: { id: 'own1', model: '<synthetic>', usage: { input_tokens: 0, cache_creation_input_tokens: 0, cache_read_input_tokens: 0, output_tokens: 0 }, content: [] } },
  result(`Context Usage\nclaude-sonnet-made-up 12.3k/200k tokens (6%)\nSystem prompt: 4.2k tokens (2.1%)\nMemory files: 151 tokens\n  ${lab}\\CLAUDE.md: 151 tokens\nSkills: 58 tokens\n  release-prep: 58 tokens\n  private-skill-x: 999 tokens\nMCP tools: 1.1k tokens\n  mcp__gear__find_gear (gear): 120 tokens\n  mcp__secretsrv__peek (secretsrv): 77 tokens`),
]);
// A debug record with one real-looking line and names that merely begin like a source word
// ("session", "cli"). The names are made up for this check and are nobody's.
writeFileSync(join(scratch, 'made.debug.txt'), [
  '2026-10-10T00:00:00Z [DEBUG] Loaded 1 unique skills (managed: 0, user: 0, project: 1)',
  '2026-10-10T00:00:00Z [DEBUG] plugin commands by name: Sessionmadeup: 4, climadeup: 2, zeta: 9',
  '2026-10-10T00:00:00Z [DEBUG] mcp config seen at localhost:3845',
].join('\n') + '\n');
writeFileSync(join(scratch, 'made.stderr.txt'), '');

const node = (script, args) => spawnSync(process.execPath, [join(seed, 'runner', script), ...args], { encoding: 'utf8', env: { ...process.env, KIT_DIR: kit } });
const after = (name) => node('after.mjs', [join(scratch, `${name}.stream.jsonl`)]);
const NAMES = ['a-base', 'a-all', 'a-plugin', 'a-upfront', 'a-intruder', 'a-bash', 'a-outside'];
const outs = Object.fromEntries(NAMES.map((name) => [name, after(name)]));
for (const [name, out] of Object.entries(outs)) { process.stdout.write(out.stdout); if (out.stderr) console.log(`[stderr of ${name}] ${out.stderr}`); }
const said = node('said.mjs', [join(scratch, 'a-all.stream.jsonl')]);
process.stdout.write(said.stdout);
if (said.stderr) console.log(`[stderr of said] ${said.stderr}`);
const loader = node('loader-seen.mjs', [join(scratch, 'made.debug.txt'), join(scratch, 'made.stderr.txt')]);
process.stdout.write(loader.stdout);
if (loader.stderr) console.log(`[stderr of loader-seen] ${loader.stderr}`);
const context = node('context-read.mjs', [join(scratch, 'a-context.stream.jsonl')]);
process.stdout.write(context.stdout);
if (context.stderr) console.log(`[stderr of context-read] ${context.stderr}`);

const verdict = (name) => (outs[name].stdout.split('\n').find((line) => line.includes('verdict:')) ?? '');
const stops = (name) => (verdict(name).match(/STOP/g) ?? []).length;
const all = Object.values(outs).map((out) => out.stdout).join('\n') + said.stdout + loader.stdout + context.stdout;
const pairs = loader.stdout.split('\n').find((line) => line.includes('"source: number" pairs')) ?? '';
const checks = [
  ['the verdict has seven parts', verdict('a-base').split(' | ').length === 7],
  ['a clean base arm has no STOP and no LOOK', !/STOP|LOOK/.test(verdict('a-base')) && verdict('a-base').includes('the parts of arm base and no other') && verdict('a-base').endsWith('no file tool aimed outside the project and the plugin')],
  ['an arm with every seed part has no STOP', !/STOP|LOOK/.test(verdict('a-all')) && verdict('a-all').includes('instruction files as this arm holds them (1)')],
  ['its used parts are listed by the seed\'s names', outs['a-all'].stdout.includes('Skill calls 1 (release-prep) | Agent calls 1 (log-scout) | ToolSearch calls 1 | gear tool calls 1 (find_gear {"code":"G-417"})')],
  ['the server\'s and the guard\'s own records are counted', outs['a-all'].stdout.includes('initialize 1 | tools/list 1 | tools/call 1') && outs['a-all'].stdout.includes('the guard\'s record: 1 lines | pass 1, block 0 | Edit and Write calls in the stream 1')],
  ['calls inside the project, by a relative path or the project folder itself, are not counted as outside', outs['a-all'].stdout.includes('in the stream 0 | in the logging hook\'s record 0 (stopped by it: 0; in the temp folder: 0)')],
  ['every result line carries is_error', outs['a-all'].stdout.includes('result lines: success (1 turns, is_error false)')],
  ['the plugin arm is recognised by its prefixed names, a read in the plugin folder is not outside, and mode manual passes',
    !/STOP|LOOK/.test(verdict('a-plugin')) && outs['a-plugin'].stdout.includes('ship-kit 1 (its path is the seed\'s plugin folder: yes)') && verdict('a-plugin').includes('permission mode manual')],
  ['with tool search off, a list without ToolSearch is the expected one', !/STOP|LOOK/.test(verdict('a-upfront')) && verdict('a-upfront').includes('the expected built-in tools (ToolSearch listed: no)')],
  ['things that are not the seed\'s say STOP twice (the lists, the instruction file)', stops('a-intruder') === 2],
  ['and are counted', outs['a-intruder'].stdout.includes('+ any other 1 | MCP tools: 1 = gear\'s 0 + any other 1') && outs['a-intruder'].stdout.includes('outside the project 1')],
  ['Bash among the built-in tools says STOP', stops('a-bash') === 1 && verdict('a-bash').includes('STOP: Bash or PowerShell is among the built-in tools')],
  ['a file tool aimed outside the project says STOP once, counted from the stream and from the hook\'s record',
    stops('a-outside') === 1 && verdict('a-outside').endsWith('STOP: a file tool was aimed outside the project and the plugin (counts above; paths not printed)') && outs['a-outside'].stdout.includes('in the stream 2 | in the logging hook\'s record 2 (stopped by it: 2; in the temp folder: 0)')],
  ['said.mjs prints each result text with the project folder as <lab>', said.stdout.includes('| 改好了，在 <lab>') && said.stdout.includes('| 下一步：跑測試。')],
  ['said.mjs shows six lines of the seed\'s skill body and only the size of any other added message',
    said.stdout.includes('| Base directory for this skill: <lab>') && said.stdout.includes('| 2. 改 CHANGELOG。') && !said.stdout.includes('改 README') && said.stdout.includes('not shown') && !said.stdout.includes('second line')],
  ['loader-seen.mjs prints a listed source word and no name that begins like one', pairs.includes('project: 1 (x1)') && !/sessionmadeup|climadeup|zeta|localhost|: 4|: 2 |3845/i.test(pairs)],
  ['no name or path that is not the seed\'s is printed anywhere', !/secretsrv|private-|\/somewhere|made-up[\\/]elsewhere|Sessionmadeup|climadeup/.test(all) && !all.includes(scratch)],
  ['/context: the seed\'s lines are readable', context.stdout.includes('release-prep: 58 tokens') && context.stdout.includes('<lab>\\CLAUDE.md: 151 tokens') && context.stdout.includes('mcp__gear__find_gear (gear): 120 tokens')],
  ['/context: the other names are masked and counted', context.stdout.includes('___: 999 tokens') && /words masked: [1-9]/.test(context.stdout)],
  ['/context: a line Claude Code wrote itself is not counted as a model request', context.stdout.includes('that carry usage: 0 (0 means')],
];
let failed = 0;
for (const [label, ok] of checks) { if (!ok) failed += 1; console.log(`${ok ? 'ok  ' : 'FAIL'} ${label}`); }
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
