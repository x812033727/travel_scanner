// Builds three MADE-UP sessions in a temporary folder (a stream in the shape Claude Code 2.1.295
// writes, and the project each would have left) and runs tally.mjs on them. It checks the parser
// and the scoring rules: one session that called the skill and did all five steps, one that had
// no skill and did what a guess would do, one that opened the skill file with Read instead of
// calling the Skill tool. The shape of a Skill tool call's input ({skill, args}) is a guess that
// the first real session confirms or corrects. It is not evidence of anything a model did, and
// the made-up files are deleted when it ends. No session, no model.
// Usage: node <seed>/check-tally.mjs
import { spawnSync } from 'node:child_process';
import { cpSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'skill-lab-tally-'));
const cwd = join(scratch, 'skill-lab');
const shipped = ['verify', 'debug', 'code-review'];
const init = (skills) => ({
  type: 'system', subtype: 'init', cwd, model: 'made-up-model', claude_code_version: '0.0.0',
  permissionMode: 'default', tools: ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Skill'], mcp_servers: [],
  plugins: [{ name: 'cc-plugin-made-up' }], skills, slash_commands: [...skills, 'clear'],
});
let ids = 0;
const call = (name, input, usage) => {
  ids += 1;
  return { type: 'assistant', parent_tool_use_id: null, message: { id: `m${ids}`, usage, content: [{ type: 'tool_use', id: `t${ids}`, name, input }] } };
};
const back = (text) => ({ type: 'user', message: { content: [{ type: 'tool_result', tool_use_id: `t${ids}`, content: text }] } });
const result = (text) => ({
  type: 'result', subtype: 'success', num_turns: 6, permission_denials: [], result: text, total_cost_usd: 0,
  usage: { input_tokens: 12, cache_creation_input_tokens: 3000, cache_read_input_tokens: 20000, output_tokens: 900 },
});
const usage = (write) => ({ input_tokens: 2, cache_creation_input_tokens: write, cache_read_input_tokens: 4427, output_tokens: 10 });
const body = '# 發版準備\n\n只動下面列的檔案，不改 src/。五步照順序做完。';
const template = '# vX.Y.Z\n\n## 這一版改了什麼\n\n## 升級要注意\n\n## 怎麼確認\n';

function project(name, { skill, version, changelog, readme, note }) {
  const lab = join(scratch, `${name}.lab`);
  cpSync(join(here, 'skill-lab'), lab, { recursive: true });
  if (skill) {
    mkdirSync(join(lab, '.claude', 'skills', 'release-prep'), { recursive: true });
    writeFileSync(join(lab, '.claude', 'skills', 'release-prep', 'SKILL.md'), body);
  }
  writeFileSync(join(lab, 'package.json'), `${JSON.stringify({ name: 'unit-kit', version, private: true, type: 'module' }, null, 2)}\n`);
  writeFileSync(join(lab, 'CHANGELOG.md'), changelog);
  writeFileSync(join(lab, 'README.md'), readme);
  if (note) { mkdirSync(join(lab, 'releases')); writeFileSync(join(lab, 'releases', 'v0.3.1.md'), note); }
}
const followed = '# Changelog\n\n## Unreleased\n\n## v0.3.1 (2026-01-01)\n\n- kmToMiles rounds to two decimals.\n\n## v0.3.0 (2026-10-02)\n\n- Add kmToMiles.\n';
const guessed = '# Changelog\n\n## v0.3.1 (2026-01-01)\n\n- kmToMiles rounds to two decimals.\n\n## v0.3.0 (2026-10-02)\n\n- Add kmToMiles.\n';

project('made-up-called', {
  skill: true, version: '0.3.1', changelog: followed, readme: '# unit-kit\n\nLatest release: v0.3.1\n',
  note: '# v0.3.1\n\n## 這一版改了什麼\n\n- rounding\n\n## 升級要注意\n\n無\n\n## 怎麼確認\n\n無\n',
});
project('made-up-no-skill', { skill: false, version: '0.3.1', changelog: guessed, readme: '# unit-kit\n\nLatest release: v0.3.0\n' });
project('made-up-read-only', {
  skill: true, version: '0.3.1', changelog: followed, readme: '# unit-kit\n\nLatest release: v0.3.1\n',
  note: '# v0.3.1\n\n## 這一版改了什麼\n\n## 升級要注意\n',
});

const streams = {
  'made-up-called': [
    init(['release-prep', ...shipped]),
    call('Skill', { skill: 'release-prep', args: '0.3.1' }, usage(1000)), back(`Launching skill: release-prep\n${body}`),
    call('Read', { file_path: join(cwd, '.claude', 'skills', 'release-prep', 'template.md') }), back(template),
    call('Edit', { file_path: join(cwd, 'package.json') }), back('ok'),
    call('Edit', { file_path: join(cwd, 'CHANGELOG.md') }), back('ok'),
    call('Edit', { file_path: join(cwd, 'README.md') }), back('ok'),
    call('Write', { file_path: join(cwd, 'releases', 'v0.3.1.md') }), back('ok'),
    result('四個檔案都改好了。\n\n**下一步：git tag v0.3.1**'),
  ],
  'made-up-no-skill': [
    init([...shipped, 'a-skill-from-somewhere-else']),
    call('Glob', { pattern: '**/*' }, usage(920)), back('package.json'),
    call('Edit', { file_path: join(cwd, 'package.json') }), back('ok'),
    call('Edit', { file_path: join(cwd, 'CHANGELOG.md') }), back('ok'),
    call('Read', { file_path: join(scratch, 'elsewhere.txt') }), back('x'),
    result('版號和 CHANGELOG 都更新了。'),
  ],
  'made-up-read-only': [
    init(['release-prep', ...shipped]),
    call('Glob', { pattern: '**/*' }, usage(960)), back('.claude/skills/release-prep/SKILL.md'),
    call('Read', { file_path: join(cwd, '.claude', 'skills', 'release-prep', 'SKILL.md') }), back(body),
    call('Edit', { file_path: join(cwd, 'package.json') }), back('ok'),
    result('改好了。\n下一步:git tag v0.3.1'),
  ],
};
const files = Object.entries(streams).map(([name, lines]) => {
  const file = join(scratch, `${name}.stream.jsonl`);
  writeFileSync(file, `${lines.map((line) => JSON.stringify(line)).join('\n')}\n`);
  return file;
});
const run = spawnSync(process.execPath, [join(here, 'tally.mjs'), ...files], { encoding: 'utf8' });
process.stdout.write(run.stdout);
process.stderr.write(run.stderr);
rmSync(scratch, { recursive: true, force: true });
process.exitCode = run.status ?? 1;
