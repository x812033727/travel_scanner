// Runs tally.mjs and runner/models.mjs on three made-up sessions and checks what they print.
// No session, no model. The streams are written here by hand, in the shape the earlier videos'
// run logs recorded for Claude Code 2.1.295 (a Skill call followed by a "Base directory for this
// skill" message, an Agent call whose report arrives as a task_notification, hook_response
// lines). They are not the record of any session.
// Usage: node <seed>/check-tally.mjs
import { spawnSync } from 'node:child_process';
import { cpSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'tally-check-'));
const logs = join(scratch, 'run', 'logs');
const kit = join(scratch, 'run', 'ship-kit');
const cwd = join(scratch, 'run', 'lab');
mkdirSync(logs, { recursive: true });

function lab(name, change) {
  const dir = join(logs, `${name}.lab`);
  cpSync(join(seed, 'lab-b'), dir, { recursive: true });
  mkdirSync(join(dir, 'logs'), { recursive: true });
  cpSync(join(seed, 'placed', 'b.fares-test.mjs.txt'), join(dir, 'src', 'fares.test.mjs'));
  cpSync(join(seed, 'placed', 'b.jobs-1.txt'), join(dir, 'logs', 'sync-2026-10-08.log'));
  cpSync(join(seed, 'placed', 'b.jobs-2.txt'), join(dir, 'logs', 'sync-2026-10-09.log'));
  change(dir);
}
const released = (withNote) => (dir) => {
  writeFileSync(join(dir, 'package.json'), readFileSync(join(dir, 'package.json'), 'utf8').replace('1.2.0', '1.2.1'));
  writeFileSync(join(dir, 'CHANGELOG.md'), readFileSync(join(dir, 'CHANGELOG.md'), 'utf8').replace('## Unreleased\n\n', '## Unreleased\n\n## v1.2.1 (2026-10-10)\n\n'));
  writeFileSync(join(dir, 'README.md'), readFileSync(join(dir, 'README.md'), 'utf8').replace('v1.2.0', 'v1.2.1'));
  if (!withNote) return;
  mkdirSync(join(dir, 'releases'));
  writeFileSync(join(dir, 'releases', 'v1.2.1.md'), '# v1.2.1\n\n## 這一版改了什麼\n\n- made up\n\n## 升級要注意\n\n無\n\n## 怎麼確認\n\nmade up\n');
};

const usage = (n) => ({ input_tokens: 10, cache_creation_input_tokens: n, cache_read_input_tokens: 0, output_tokens: 5 });
const say = (id, blocks, extra = {}) => ({ type: 'assistant', message: { id, model: 'claude-sonnet-5-5', usage: usage(extra.tokens ?? 9000), content: blocks }, parent_tool_use_id: extra.parent ?? null });
const use = (id, tool, input) => ({ type: 'tool_use', id, name: tool, input });
const back = (id, text, extra = {}) => ({ type: 'user', message: { content: [{ type: 'tool_result', tool_use_id: id, content: text, is_error: extra.error ?? false }] }, parent_tool_use_id: extra.parent ?? null, tool_use_result: extra.meta });
const hookLine = (hook, code) => ({ type: 'system', subtype: 'hook_response', hook_name: hook, hook_event: hook.split(':')[0], exit_code: code, outcome: code ? 'error' : 'success' });
const init = (extra) => ({ type: 'system', subtype: 'init', cwd, model: 'claude-sonnet-5-5', claude_code_version: '0.0.0-made-up', permissionMode: 'default',
  tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Skill', 'Task'], mcp_servers: [], slash_commands: ['init', 'loop', ...(extra.commands ?? [])],
  plugins: [{ name: 'cc-plugin-one', path: 'made-up' }, { name: 'cc-plugin-two', path: 'made-up' }, ...(extra.plugins ?? [])],
  skills: ['init', 'loop', ...(extra.skills ?? [])], agents: ['Explore', 'general-purpose', ...(extra.agents ?? [])], ...(extra.errors ? { plugin_errors: extra.errors } : {}) });
const done = (text) => ({ type: 'result', subtype: 'success', num_turns: 3, total_cost_usd: 0.01, result: text, usage: usage(9000), modelUsage: { 'claude-sonnet-5-5': {} }, permission_denials: [] });
const report = 'J2103｜sync-2026-10-08.log｜8\nJ2204｜sync-2026-10-09.log｜11\n共 2 筆';
const write = (name, arm, lines, seen, guard) => {
  writeFileSync(join(logs, `${name}.session.txt`), `# ${name} | arm ${arm} | start made-up\n`);
  writeFileSync(join(logs, `${name}.stream.jsonl`), `${lines.map((line) => JSON.stringify(line)).join('\n')}\n`);
  writeFileSync(join(logs, `${name}.seen.txt`), seen.length ? `${seen.join('\n')}\n` : '');
  if (guard.length) writeFileSync(join(logs, `${name}.guard.txt`), `${guard.join('\n')}\n`);
};

// 1. The plugin loaded, all three parts used.
lab('made-kit', released(true));
write('made-kit', 'kit', [
  init({ plugins: [{ name: 'ship-kit', path: kit }], skills: ['ship-kit:release-prep'], agents: ['ship-kit:log-scout'], commands: ['ship-kit:release-prep'] }),
  say('m1', [use('toolu_made0001', 'Agent', { subagent_type: 'ship-kit:log-scout', prompt: 'check logs/', description: 'made up' })], { tokens: 9100 }),
  back('toolu_made0001', 'Async agent launched (made up)', { meta: { isAsync: true, status: 'async_launched' } }),
  say('s1', [use('toolu_made0101', 'Glob', { pattern: 'logs/*.log' })], { parent: 'toolu_made0001' }),
  back('toolu_made0101', 'logs/sync-2026-10-08.log', { parent: 'toolu_made0001' }),
  say('m2', [use('toolu_made0002', 'Skill', { skill: 'ship-kit:release-prep', args: '1.2.1' })]),
  back('toolu_made0002', 'Launching skill: ship-kit:release-prep'),
  { type: 'user', isSynthetic: true, message: { content: [{ type: 'text', text: `Base directory for this skill: ${join(kit, 'skills', 'release-prep')}\n\n# made up` }] } },
  say('m3', [use('toolu_made0003', 'Read', { file_path: join(kit, 'skills', 'release-prep', 'template.md') })]),
  back('toolu_made0003', '# vX.Y.Z'),
  say('m4', [use('toolu_made0004', 'Edit', { file_path: join(cwd, 'package.json') })]), hookLine('PreToolUse:Edit', 0), back('toolu_made0004', 'updated'),
  say('m5', [use('toolu_made0005', 'Edit', { file_path: join(cwd, 'CHANGELOG.md') })]), hookLine('PreToolUse:Edit', 0), back('toolu_made0005', 'updated'),
  say('m6', [use('toolu_made0006', 'Edit', { file_path: join(cwd, 'README.md') })]), hookLine('PreToolUse:Edit', 0), back('toolu_made0006', 'updated'),
  say('m7', [use('toolu_made0007', 'Write', { file_path: join(cwd, 'releases', 'v1.2.1.md') })]), hookLine('PreToolUse:Write', 0), back('toolu_made0007', 'created'),
  done('made-up reply\n下一步：git tag v1.2.1'),
  { type: 'system', subtype: 'task_notification', tool_use_id: 'toolu_made0001', status: 'completed', summary: report },
  say('m8', [{ type: 'text', text: 'made up' }]),
  done('J2103 and J2204 never finished.'),
], ['PreToolUse by=main id=0001 Agent type=ship-kit:log-scout background=- prompt_chars=11', 'PreToolUse by=main id=0002 Skill skill=ship-kit:release-prep keys=skill,args'],
['guard(plugin) Edit package.json -> pass | PLUGIN_ROOT slash', 'guard(plugin) Edit CHANGELOG.md -> pass | PLUGIN_ROOT slash', 'guard(plugin) Edit README.md -> pass | PLUGIN_ROOT slash', 'guard(plugin) Write v1.2.1.md -> pass | PLUGIN_ROOT slash']);

// 2. No plugin: the obvious three steps, nothing of the seed's.
lab('made-bare', released(false));
write('made-bare', 'bare', [
  init({}),
  say('m1', [use('toolu_made1001', 'Glob', { pattern: 'logs/*' })], { tokens: 9000 }), back('toolu_made1001', 'logs/sync-2026-10-08.log'),
  say('m2', [use('toolu_made1002', 'Edit', { file_path: join(cwd, 'package.json') })]), back('toolu_made1002', 'updated'),
  say('m3', [use('toolu_made1003', 'Edit', { file_path: join(cwd, 'CHANGELOG.md') })]), back('toolu_made1003', 'updated'),
  say('m4', [use('toolu_made1004', 'Edit', { file_path: join(cwd, 'README.md') })]), back('toolu_made1004', 'updated'),
  done('made-up reply. J2103 and J2204 never finished. There is no agent called log-scout.'),
], ['PreToolUse by=main id=1001 Glob logs/*'], []);

// 3. Somebody else's plugin, skill and agent on the init line; a hook stops an edit; a read is asked about.
lab('made-other', () => {});
write('made-other', 'guard', [
  init({ plugins: [{ name: 'ship-kit', path: kit }, { name: 'somebody-private', path: 'X:/private/place' }], skills: ['ship-kit:release-prep', 'somebody-private:thing'],
    agents: ['ship-kit:log-scout', 'private-agent'], errors: [{ plugin: 'somebody-private', type: 'made-up-type', message: 'secret path X:/private/place' }] }),
  say('m1', [use('toolu_made2001', 'Edit', { file_path: join(cwd, 'src', 'fares.test.mjs') })]), hookLine('PreToolUse:Edit', 2),
  back('toolu_made2001', 'PreToolUse:Edit hook error: [node made-up]: This test already exists: do not change it.\nFix the code instead. New tests are fine.\nThis hook comes from the ship-kit plugin.', { error: true }),
  say('m2', [use('toolu_made2002', 'Read', { file_path: join(scratch, 'elsewhere', 'private.txt') })]),
  back('toolu_made2002', 'Claude requested permissions to read from a made-up place, but you haven\'t granted it yet.', { error: true }),
  done('made-up reply'),
], ['PreToolUse by=main id=2001 Edit src/fares.test.mjs', 'PreToolUse by=main id=2002 Read (outside the project)', 'PermissionRequest by=main id=---- Read (outside the project) | mode=default suggestions=1'],
['guard(plugin) Edit fares.test.mjs -> block | PLUGIN_ROOT slash']);

const streams = ['made-kit', 'made-bare', 'made-other'].map((name) => join(logs, `${name}.stream.jsonl`));
const env = { PATH: process.env.PATH, SystemRoot: process.env.SystemRoot ?? '', USERPROFILE: process.env.USERPROFILE ?? '', HOME: process.env.HOME ?? '' };
const tally = spawnSync(process.execPath, [join(seed, 'tally.mjs'), ...streams], { encoding: 'utf8', env });
const hide = (text) => text.split(scratch).join('<scratch>').split(scratch.replaceAll('\\', '/')).join('<scratch>');
console.log(hide(tally.stdout).split('\n').map((line) => line.slice(0, 230)).join('\n'));
if (tally.stderr) console.log(`tally stderr: ${hide(tally.stderr).slice(0, 600)}`);
const verdicts = streams.map((stream) => spawnSync(process.execPath, [join(seed, 'runner', 'models.mjs'), stream], { encoding: 'utf8', env }).stdout);
for (const verdict of verdicts) console.log(hide(verdict).split('\n').map((line) => line.slice(0, 400)).join('\n'));

const out = tally.stdout;
const section = (name) => out.split('== ').find((part) => part.startsWith(name)) ?? '';
const checks = [
  ['made-kit: all three parts yes', /scored: plugin on the init line yes \| skill listed yes, used yes, effect yes \| agent listed yes, used yes, effect yes \| hook: one guard line per Edit or Write yes \| all three parts yes/.test(section('made-kit'))],
  ['made-kit: the Skill call and its base directory are in the plugin', section('made-kit').includes('as "ship-kit:release-prep"') && section('made-kit').includes('<plugin>/skills/release-prep')],
  ['made-kit: the report is read from the task_notification', section('made-kit').includes('unfinished jobs named 2 of 2') && section('made-kit').includes('yes, N = 2')],
  ['made-kit: F5 is found on the first of two result lines', section('made-kit').includes('git tag v1.2.1: yes')],
  ['made-bare: plugin no, F1 to F3 yes, F4 no, all three no', /plugin on the init line no/.test(section('made-bare')) && /F1 package\.json yes .* F2 CHANGELOG yes \| F3 README yes \| F4 releases\/v1\.2\.1\.md no/.test(section('made-bare')) && /all three parts no/.test(section('made-bare'))],
  ['made-other: the other plugin, skill and agent are counted', section('made-other').includes('any other 1  <- STOP') && section('made-other').includes('plugin_errors on the init line: 1')],
  ['made-other: none of their names, paths or messages is printed', !/somebody-private|private-agent|X:\/private|secret path|private\.txt/.test(out + verdicts.join(''))],
  ['made-other: the edit is "stopped by a hook" and the text names the plugin', section('made-other').includes('-> stopped by a hook | the text names the ship-kit plugin')],
  ['made-other: the read is "refused: asked"', section('made-other').includes('-> refused: asked')],
  ['made-other: the existing test file is unchanged', section('made-other').includes('the existing test file is unchanged: yes')],
  ['models.mjs: made-kit passes, made-other says STOP', /ship-kit loaded from the seed's folder, no load error/.test(verdicts[0]) && !/STOP/.test(verdicts[0]) && /STOP: a plugin, skill or agent that is not the seed's/.test(verdicts[2])],
  ['models.mjs: made-bare expects no ship-kit', /no ship-kit, as this arm expects/.test(verdicts[1]) && !/STOP/.test(verdicts[1])],
];
let failed = 0;
for (const [label, ok] of checks) { if (!ok) failed += 1; console.log(`${ok ? 'ok  ' : 'FAIL'} ${label}`); }
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed || tally.status ? 1 : 0;
