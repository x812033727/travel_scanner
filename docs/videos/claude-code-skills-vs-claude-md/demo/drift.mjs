// What one headless session changed, measured against the seed, and what the session cost.
// tally.mjs scores the five release steps; this adds what the 2026-10-11 runs need beside it:
// which of the four seed files changed, which files are new, whether the release was carried
// out at all (for a request that did not ask for it), marks that only another procedure would
// leave (a "- [fix]" line, a "## Usage" heading, another procedure's fixed last line), and the
// session's size: requests to the model, tokens, turns, reported cost.
//
//   node <seed>/drift.mjs <logs>/<name>.stream.jsonl [<logs>/<name>.stream.jsonl ...]
//
// Next to each stream it expects <name>.lab/, the copy of the project session-2.sh keeps.
// Paths are printed relative to the project; nothing outside it is named.
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { basename, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = join(dirname(fileURLToPath(import.meta.url)), 'skill-lab');
const SEED_FILES = ['package.json', 'CHANGELOG.md', 'README.md', 'src/units.mjs'];
const OTHER_LAST_LINES = ['補一個測試', '請回報的人確認'];
const NEXT_STEP = /^[\s>*_`-]*下一步[：:]/;

const sha = (path) => (existsSync(path) ? createHash('sha256').update(readFileSync(path)).digest('hex').slice(0, 16) : null);
const walk = (dir, base = dir) => (existsSync(dir) ? readdirSync(dir).flatMap((entry) => {
  const path = join(dir, entry);
  return statSync(path).isDirectory() ? walk(path, base) : [path.slice(base.length + 1).replaceAll('\\', '/')];
}) : []);
const sum = (usage) => (usage ? (usage.input_tokens ?? 0) + (usage.cache_creation_input_tokens ?? 0) + (usage.cache_read_input_tokens ?? 0) : null);

function digest(file) {
  const name = basename(file).replace(/\.stream\.jsonl$/, '');
  const lab = join(dirname(file), `${name}.lab`);
  const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).map((line) => JSON.parse(line));
  const result = lines.findLast((line) => line.type === 'result') ?? {};
  const requests = new Map();
  const skills = [];
  const seen = new Set();
  for (const line of lines) {
    if (line.type !== 'assistant' || line.parent_tool_use_id) continue;
    const id = line.message?.id;
    if (id && !requests.has(id)) requests.set(id, sum(line.message.usage));
    for (const block of line.message?.content ?? []) {
      if (block.type !== 'tool_use' || block.name !== 'Skill' || seen.has(block.id)) continue;
      seen.add(block.id);
      skills.push(String(block.input?.skill ?? block.input?.name ?? block.input?.command ?? '?'));
    }
  }
  const files = walk(lab).filter((path) => !path.startsWith('.claude/') && path !== 'CLAUDE.md').sort();
  const state = Object.fromEntries(SEED_FILES.map((path) => {
    const now = sha(join(lab, path));
    return [path, now === null ? 'deleted' : now === sha(join(seed, path)) ? 'same' : 'changed'];
  }));
  const changelog = existsSync(join(lab, 'CHANGELOG.md')) ? readFileSync(join(lab, 'CHANGELOG.md'), 'utf8').split('\n') : [];
  const readme = existsSync(join(lab, 'README.md')) ? readFileSync(join(lab, 'README.md'), 'utf8').split('\n') : [];
  let version = null;
  try { version = JSON.parse(readFileSync(join(lab, 'package.json'), 'utf8')).version; } catch { version = '(package.json does not parse)'; }
  const reply = typeof result.result === 'string' ? result.result : '';
  const lastLine = reply.split('\n').map((line) => line.trim()).filter(Boolean).at(-1) ?? '';
  const fresh = files.filter((path) => !SEED_FILES.includes(path));
  return {
    name, missing: !existsSync(lab), state, fresh, version, skills, lastLine,
    tagged: changelog.filter((line) => /^\s*-\s*\[/.test(line)).map((line) => line.trim()),
    versionHeading: changelog.some((line) => line.startsWith('## ') && line.includes('0.3.1')),
    usage: readme.some((line) => line.trim() === '## Usage'),
    otherLast: OTHER_LAST_LINES.find((each) => lastLine.includes(each)) ?? null,
    nextStep: NEXT_STEP.test(lastLine),
    released: version !== '0.3.0' || fresh.some((path) => path.startsWith('releases/')),
    requests: [...requests.values()], whole: sum(result.usage), output: result.usage?.output_tokens,
    turns: result.num_turns, cost: result.total_cost_usd, seconds: Math.round((result.duration_ms ?? 0) / 1000),
  };
}

const yes = (value) => (value ? 'yes' : 'no');
const sessions = process.argv.slice(2).map(digest);
for (const s of sessions) {
  console.log(`== ${s.name} | against the seed (${SEED_FILES.join(', ')})`);
  if (s.missing) { console.log('   (no copy of the project next to this stream)'); continue; }
  console.log(`   ${SEED_FILES.map((path) => `${path}: ${s.state[path]}`).join(' | ')}`);
  console.log(`   new files outside .claude: ${s.fresh.join(', ') || 'none'}`);
  console.log(`   package.json version: ${s.version} | CHANGELOG.md has a 0.3.1 heading: ${yes(s.versionHeading)}`);
  console.log(`   the release was carried out (version no longer 0.3.0, or a file under releases/): ${yes(s.released)}`);
  console.log(`   marks of another procedure: CHANGELOG lines starting "- [": ${s.tagged.length}${s.tagged.length ? ` (${s.tagged.join(' / ')})` : ''} | README "## Usage": ${yes(s.usage)} | another procedure's last line: ${s.otherLast ?? 'no'}`);
  console.log(`   Skill calls, in order: ${s.skills.join(', ') || 'none'}`);
  console.log(`   last line of the reply starts with 下一步: ${yes(s.nextStep)}`);
  console.log(`   requests to the model: ${s.requests.length} (input tokens of each: ${s.requests.join(', ')}) | sum ${s.whole}`);
  console.log(`   turns ${s.turns} | output tokens ${s.output} | reported cost USD ${s.cost} | ${s.seconds} s`);
}
if (sessions.length > 1) {
  console.log('\nname | seed files changed | new files | release carried out | "- [" lines | Skill calls | requests | first request | all requests | turns | cost USD');
  for (const s of sessions) {
    if (s.missing) { console.log(`${s.name} | ?`); continue; }
    const changed = SEED_FILES.filter((path) => s.state[path] !== 'same');
    console.log([s.name, changed.join(' ') || 'none', s.fresh.join(' ') || 'none', yes(s.released), s.tagged.length,
      s.skills.join(' ') || 'none', s.requests.length, s.requests[0] ?? '?', s.whole, s.turns, s.cost].join(' | '));
  }
}
