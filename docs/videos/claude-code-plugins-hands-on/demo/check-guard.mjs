// Runs the guard on made-up hook events, in both places it can live: a project's
// .claude/hooks/ and a plugin's scripts/. No session, no model: only node and a temporary folder.
// Usage: node <seed>/check-guard.mjs
import { spawnSync } from 'node:child_process';
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'guard-check-'));
const project = join(scratch, 'project');
const plugin = join(scratch, 'plugin');
mkdirSync(join(project, '.claude', 'hooks'), { recursive: true });
mkdirSync(join(project, 'src'), { recursive: true });
mkdirSync(join(plugin, 'scripts'), { recursive: true });
cpSync(join(seed, 'parts', 'guard.mjs'), join(project, '.claude', 'hooks', 'guard.mjs'));
cpSync(join(seed, 'parts', 'guard.mjs'), join(plugin, 'scripts', 'guard.mjs'));
writeFileSync(join(project, 'src', 'fares.test.mjs'), '// an existing test\n');
writeFileSync(join(project, 'package.json'), '{}\n');
const record = join(scratch, 'guard.txt');
const forward = (path) => path.replaceAll('\\', '/');

let failed = 0;
function run(label, { script, target, tool = 'Edit', env = {}, want, log = record }) {
  const event = { hook_event_name: 'PreToolUse', tool_name: tool, cwd: project, tool_input: { file_path: join(project, target) } };
  const out = spawnSync(process.execPath, [script], {
    input: JSON.stringify(event), encoding: 'utf8',
    env: { PATH: process.env.PATH, SystemRoot: process.env.SystemRoot ?? '', CLAUDE_PROJECT_DIR: project, GUARD_LOG: log, ...env },
  });
  const ok = out.status === want;
  if (!ok) failed += 1;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${label}: exit ${out.status} (want ${want}) | stdout bytes ${out.stdout.length} | stderr lines ${out.stderr.split('\n').filter(Boolean).length}`);
  for (const line of out.stderr.split('\n').filter(Boolean)) console.log(`       stderr | ${line}`);
}

const inProject = join(project, '.claude', 'hooks', 'guard.mjs');
const inPlugin = join(plugin, 'scripts', 'guard.mjs');
// The path arrives as Claude Code is documented to substitute it on Windows: forward slashes.
const asPlugin = { script: forward(inPlugin), env: { CLAUDE_PLUGIN_ROOT: forward(plugin) } };
run('project copy, Edit of the existing test', { script: forward(inProject), target: 'src/fares.test.mjs', want: 2 });
run('project copy, Edit of package.json', { script: forward(inProject), target: 'package.json', want: 0 });
run('plugin copy, Edit of the existing test', { ...asPlugin, target: 'src/fares.test.mjs', want: 2 });
run('plugin copy, Edit of package.json', { ...asPlugin, target: 'package.json', want: 0 });
run('plugin copy, Write of a test that does not exist yet', { ...asPlugin, target: 'src/new.test.mjs', tool: 'Write', want: 0 });
run('plugin copy, plugin root given with backslashes', { script: inPlugin.replaceAll('/', '\\'), env: { CLAUDE_PLUGIN_ROOT: plugin.replaceAll('/', '\\') }, target: 'package.json', want: 0 });
run('plugin copy, the record cannot be written', { ...asPlugin, target: 'src/fares.test.mjs', want: 2, log: join(scratch, 'no-such-folder', 'guard.txt') });

console.log('the record the seven runs left (six lines: the last run could not write one):');
const lines = existsSync(record) ? readFileSync(record, 'utf8').split('\n').filter(Boolean) : [];
for (const line of lines) console.log(`   ${line}`);
const want = [
  'guard(project) Edit fares.test.mjs -> block | PLUGIN_ROOT unset',
  'guard(project) Edit package.json -> pass | PLUGIN_ROOT unset',
  'guard(plugin) Edit fares.test.mjs -> block | PLUGIN_ROOT slash',
  'guard(plugin) Edit package.json -> pass | PLUGIN_ROOT slash',
  'guard(plugin) Write new.test.mjs -> pass | PLUGIN_ROOT slash',
];
const sixth = 'guard(plugin) Edit package.json -> pass | PLUGIN_ROOT backslash';
const same = lines.length === 6 && want.every((line, at) => lines[at] === line) && lines[5] === sixth;
console.log(`${same ? 'ok  ' : 'FAIL'} the record is the six expected lines (the sixth was given the plugin root with backslashes)`);
if (!same) failed += 1;
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
