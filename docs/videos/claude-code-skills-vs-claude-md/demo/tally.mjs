// Reads what one headless session left behind and prints what this video counts.
//
//   node <seed>/tally.mjs <logs>/<name>.stream.jsonl [<logs>/<name>.stream.jsonl ...]
//
// Next to each stream it expects <name>.lab/, the copy of the project session.sh takes when the
// session ends. From the stream: what was offered, which skills the session started with, every
// tool call in order, whether the Skill tool was called and for which skill, where the skill's
// text shows up, the size of the first request, and the reply's last line. From the copy of the
// project: the five steps of the release-prep procedure.
//
// Nothing outside the project is printed: paths are relative to the session's cwd or shown as
// "(outside the project)", and a skill or plugin that is neither the project's nor one Claude
// Code ships is only counted, never named.
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { basename, dirname, isAbsolute, join, posix, win32 } from 'node:path';

const VERSION = '0.3.1';
// Names on the official commands page, 2026-10-09: what Claude Code ships with.
const SHIPPED = new Set(['deep-research', 'design', 'design-sync', 'dataviz', 'artifact-diagramming',
  'artifact-capabilities', 'update-config', 'verify', 'debug', 'code-review', 'simplify', 'batch',
  'fewer-permission-prompts', 'doctor', 'loop', 'schedule', 'claude-api', 'workflow-authoring', 'run',
  'run-skill-generator', 'plugin-authoring', 'claude-in-chrome', 'slides']);
const BODY_MARK = '五步照順序做完';
const TEMPLATE_MARK = '升級要注意';
const HEADINGS = ['## 這一版改了什麼', '## 升級要注意', '## 怎麼確認'];
const NEXT_STEP = /^[\s>*_`-]*下一步[：:]/;

function relativeTo(cwd, file) {
  if (typeof file !== 'string' || !file) return '';
  const tool = /^[A-Za-z]:[\\/]/.test(cwd) ? win32 : posix;
  if (!tool.isAbsolute(file)) return file.replaceAll('\\', '/');
  const rel = tool.relative(cwd, file);
  if (!rel) return '.';
  if (rel.startsWith('..') || tool.isAbsolute(rel) || isAbsolute(rel)) return '(outside the project)';
  return rel.replaceAll('\\', '/');
}

const walk = (dir, base = dir) => (existsSync(dir) ? readdirSync(dir).flatMap((entry) => {
  const path = join(dir, entry);
  return statSync(path).isDirectory() ? walk(path, base) : [path.slice(base.length + 1).replaceAll('\\', '/')];
}) : []);
const read = (path) => (existsSync(path) ? readFileSync(path, 'utf8') : null);
const sha = (text) => createHash('sha256').update(text).digest('hex').slice(0, 16);
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((block) => (typeof block === 'string' ? block : block.text ?? textOf(block.content) ?? '')).join('\n') : '');

function disk(lab) {
  if (!existsSync(lab)) return { missing: true };
  const mine = existsSync(join(lab, '.claude', 'skills')) ? readdirSync(join(lab, '.claude', 'skills')) : [];
  let version = null;
  try { version = JSON.parse(read(join(lab, 'package.json'))).version; } catch { version = '(package.json does not parse)'; }
  const log = (read(join(lab, 'CHANGELOG.md')) ?? '').split('\n').map((line) => line.trimEnd());
  const unreleased = log.indexOf('## Unreleased');
  const heading = log.findIndex((line) => new RegExp(`^## v${VERSION.replaceAll('.', '\\.')} \\(\\d{4}-\\d{2}-\\d{2}\\)$`).test(line));
  const anyHeading = log.find((line) => line.startsWith('## ') && line.includes(VERSION)) ?? '(none)';
  const between = unreleased >= 0 && heading > unreleased ? log.slice(unreleased + 1, heading) : [];
  const next = log.findIndex((line, at) => at > heading && line.startsWith('## '));
  const after = heading >= 0 ? log.slice(heading + 1, next < 0 ? log.length : next) : [];
  const readme = (read(join(lab, 'README.md')) ?? '').split('\n').map((line) => line.trim());
  const releaseLine = readme.find((line) => line.startsWith('Latest release:')) ?? '(no such line)';
  const note = read(join(lab, 'releases', `v${VERSION}.md`));
  const noteLines = (note ?? '').split('\n').map((line) => line.trimEnd());
  const src = read(join(lab, 'src', 'units.mjs'));
  return {
    mine, version, anyHeading, releaseLine,
    files: walk(lab).filter((path) => !path.startsWith('.claude/')).sort(),
    f1: version === VERSION,
    f2Heading: heading >= 0,
    f2Kept: unreleased >= 0 && heading > unreleased,
    f2Moved: heading >= 0 && unreleased >= 0 && !between.some((line) => line.startsWith('- ')) && after.some((line) => line.startsWith('- ')),
    f3: readme.includes(`Latest release: v${VERSION}`),
    f4File: note !== null,
    f4Headings: HEADINGS.filter((each) => noteLines.includes(each)).length,
    srcHash: src === null ? '(deleted)' : sha(src),
  };
}

function digest(file) {
  const name = basename(file).replace(/\.stream\.jsonl$/, '');
  const lines = readFileSync(file, 'utf8').split('\n').filter(Boolean).map((line) => JSON.parse(line));
  const init = lines.find((line) => line.type === 'system' && line.subtype === 'init') ?? {};
  const result = lines.findLast((line) => line.type === 'result') ?? {};
  const cwd = init.cwd ?? '';
  const d = disk(join(dirname(file), `${name}.lab`));
  const mine = new Set(d.mine ?? []);
  const label = (skill) => (mine.has(skill) || SHIPPED.has(skill) ? skill : '(another skill)');

  const started = (init.skills ?? []).map((each) => (typeof each === 'string' ? each : each.name));
  const commands = (init.slash_commands ?? []).map((each) => (typeof each === 'string' ? each : each.name));
  const plugins = (init.plugins ?? []).map((each) => (typeof each === 'string' ? each : each.name));

  const timeline = [];
  const written = new Set();
  const skillCalls = [];
  const opened = [];
  const toolOf = new Map();
  const where = { body: new Set(), template: new Set() };
  const seenMessages = new Set();
  let calls = 0;
  let first = null;
  for (const line of lines) {
    if (line.type === 'assistant') {
      const usage = line.message?.usage;
      if (!first && usage) first = usage;
      if (line.parent_tool_use_id) continue;
      for (const block of line.message?.content ?? []) {
        if (block.type !== 'tool_use' || seenMessages.has(block.id)) continue;
        seenMessages.add(block.id);
        calls += 1;
        const input = block.input ?? {};
        toolOf.set(block.id, `${block.name} (call ${calls})`);
        if (block.name === 'Skill') {
          const skill = String(input.skill ?? input.name ?? input.command ?? '').replace(/^\//, '');
          const args = String(input.args ?? input.arguments ?? '').split('\n')[0].slice(0, 40);
          skillCalls.push({ at: calls, skill, keys: Object.keys(input).join(',') });
          timeline.push(`call ${String(calls).padStart(2)} Skill ${label(skill)}${args ? ` args="${args}"` : ''} [input keys: ${Object.keys(input).join(',')}]`);
          continue;
        }
        const target = relativeTo(cwd, input.file_path ?? input.path ?? '');
        const detail = target || input.pattern || input.command || '';
        timeline.push(`call ${String(calls).padStart(2)} ${block.name} ${String(detail).split('\n')[0].slice(0, 90)}`);
        if ((block.name === 'Write' || block.name === 'Edit') && target) written.add(target);
        if (target.startsWith('.claude/skills/') || /(^|\/)CLAUDE(\.local)?\.md$/.test(target)) opened.push(`${block.name} ${target}`);
      }
    }
    if (line.type === 'user') {
      const content = line.message?.content;
      const blocks = Array.isArray(content) ? content : [{ type: 'text', text: textOf(content) }];
      for (const block of blocks) {
        const text = textOf(block.content ?? block.text ?? block);
        const place = block.type === 'tool_result' ? `the result of ${toolOf.get(block.tool_use_id) ?? 'a tool call'}`
          : `a user message${line.isSynthetic || line.isMeta ? ' (added by Claude Code)' : ''}`;
        if (text.includes(BODY_MARK)) where.body.add(place);
        if (text.includes(TEMPLATE_MARK)) where.template.add(place);
      }
    }
  }
  const reply = typeof result.result === 'string' ? result.result : '';
  const lastLine = reply.split('\n').map((line) => line.trim()).filter(Boolean).at(-1) ?? '';
  const firstTotal = first ? (first.input_tokens ?? 0) + (first.cache_creation_input_tokens ?? 0) + (first.cache_read_input_tokens ?? 0) : null;
  const total = result.usage ? (result.usage.input_tokens ?? 0) + (result.usage.cache_creation_input_tokens ?? 0) + (result.usage.cache_read_input_tokens ?? 0) : null;
  const target = skillCalls.find((call) => call.skill === 'release-prep');
  return {
    name, d, lastLine, timeline, opened, where, first, firstTotal, total,
    model: init.model, version: init.claude_code_version, permissionMode: init.permissionMode,
    tools: (init.tools ?? []).filter((tool) => !tool.startsWith('mcp__')),
    mcpTools: (init.tools ?? []).filter((tool) => tool.startsWith('mcp__')).length,
    mcpServers: (init.mcp_servers ?? []).length,
    pluginsShipped: plugins.filter((plugin) => String(plugin).startsWith('cc-plugin-')),
    pluginsOther: plugins.filter((plugin) => !String(plugin).startsWith('cc-plugin-')).length,
    skillsTotal: started.length,
    skillsMine: started.filter((skill) => mine.has(skill)),
    skillsShipped: started.filter((skill) => !mine.has(skill) && SHIPPED.has(skill)).length,
    skillsOther: started.filter((skill) => !mine.has(skill) && !SHIPPED.has(skill)).length,
    commandsMine: commands.filter((command) => mine.has(command)),
    subtype: result.subtype, turns: result.num_turns, denials: (result.permission_denials ?? []).length,
    cost: result.total_cost_usd, outputTokens: result.usage?.output_tokens,
    written: [...written], skillCalls,
    invoked: Boolean(target), invokedAt: target?.at,
    otherSkills: skillCalls.filter((call) => call.skill !== 'release-prep').map((call) => label(call.skill)),
    f5: NEXT_STEP.test(lastLine) && lastLine.includes(`git tag v${VERSION}`),
  };
}

const yes = (value) => (value ? 'yes' : 'no');
const list = (values) => [...values].join('; ') || 'nowhere';
const sessions = process.argv.slice(2).map(digest);
for (const s of sessions) {
  const d = s.d;
  console.log(`== ${s.name} | model ${s.model} | Claude Code ${s.version} | permission mode ${s.permissionMode}`);
  console.log(`   result ${s.subtype}, ${s.turns} turns, ${s.denials} permission denials, cost USD ${s.cost}, output tokens ${s.outputTokens}`);
  console.log(`   built-in tools offered (${s.tools.length}): ${s.tools.join(' ')}`);
  console.log(`   MCP servers ${s.mcpServers}, MCP tools ${s.mcpTools} | plugins shipped with Claude Code: ${s.pluginsShipped.length}, other plugins: ${s.pluginsOther}`);
  console.log(`   skills the session started with: ${s.skillsTotal} = the project's ${s.skillsMine.length} (${s.skillsMine.join(', ') || 'none'}) + shipped with Claude Code ${s.skillsShipped} + anything else ${s.skillsOther}`);
  console.log(`   the project's skills among the slash commands: ${s.commandsMine.join(', ') || 'none'}`);
  for (const entry of s.timeline) console.log(`   ${entry}`);
  console.log(`   Skill tool called for release-prep: ${yes(s.invoked)}${s.invoked ? ` (call ${s.invokedAt})` : ''} | other Skill calls: ${s.otherSkills.join(', ') || 'none'}`);
  console.log(`   skill or instruction files opened with a tool: ${s.opened.join('; ') || 'none'}`);
  console.log(`   the procedure's text appears in: ${list(s.where.body)}`);
  console.log(`   the template's text appears in: ${list(s.where.template)}`);
  console.log(`   first request: input ${s.first?.input_tokens} + cache write ${s.first?.cache_creation_input_tokens} + cache read ${s.first?.cache_read_input_tokens} = ${s.firstTotal} tokens | whole session: ${s.total}`);
  console.log(`   files written: ${s.written.join(', ') || 'none'}`);
  console.log(`   last line of the reply: ${s.lastLine}`);
  if (d.missing) { console.log('   (no copy of the project next to this stream: the five steps cannot be scored)'); continue; }
  console.log(`   files in the project afterwards: ${d.files.join(' ')}`);
  console.log(`   F1 package.json version is ${VERSION}: ${yes(d.f1)} (it is ${d.version})`);
  console.log(`   F2 CHANGELOG.md: dated heading ${yes(d.f2Heading)} (${d.anyHeading}), Unreleased kept above it ${yes(d.f2Kept)}, items moved under it ${yes(d.f2Moved)} -> ${yes(d.f2Heading && d.f2Kept && d.f2Moved)}`);
  console.log(`   F3 README.md says Latest release: v${VERSION}: ${yes(d.f3)} (${d.releaseLine})`);
  console.log(`   F4 releases/v${VERSION}.md: file ${yes(d.f4File)}, template headings ${d.f4Headings} of 3 -> ${yes(d.f4File && d.f4Headings === 3)}`);
  console.log(`   F5 last line starts with 下一步： and has git tag v${VERSION}: ${yes(s.f5)}`);
  console.log(`   not scored: src/units.mjs sha256[0:16] ${d.srcHash}`);
}
if (sessions.length > 1) {
  console.log('\nname | Skill called | F1 version | F2 changelog | F3 readme | F4 release note | F5 last line | SKILL.md opened with a tool | first request tokens | turns');
  for (const s of sessions) {
    const d = s.d;
    const cells = d.missing ? ['?', '?', '?', '?'] : [yes(d.f1), yes(d.f2Heading && d.f2Kept && d.f2Moved), yes(d.f3), yes(d.f4File && d.f4Headings === 3)];
    console.log([s.name, yes(s.invoked), ...cells, yes(s.f5), yes(s.opened.some((each) => each.endsWith("SKILL.md"))), s.firstTotal, s.turns].join(' | '));
  }
}
