// runner: the small result files a card may quote, written into <runner>/out/results/ (and from
// there copied to demo/results/). Everything is masked the same way as the run log; the hook
// records get "id=cN" in place of the last four characters of a tool-call id.
// Usage: node results.mjs <name> [<name> ...]
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { BUILT_IN_AGENTS, KIT, LOGS, makeMask, OUR_AGENT, OUR_SKILL, readStream, RUNNER, SHIPPED_SKILLS } from './mask.mjs';

const out = join(RUNNER, 'out', 'results');
mkdirSync(out, { recursive: true });
const mask = makeMask();
const read = (path) => (existsSync(path) ? readFileSync(path, 'utf8') : null);
const put = (file, text) => writeFileSync(join(out, file), text.endsWith('\n') ? text : `${text}\n`);
const ordinal = (text) => {
  const order = new Map();
  return text.replace(/ id=(\S{4}) /g, (whole, id) => {
    if (id === '----') return whole;
    if (!order.has(id)) order.set(id, order.size + 1);
    return ` id=c${order.get(id)} `;
  });
};
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((b) => (typeof b === 'string' ? b : b.text ?? textOf(b.content))).join('\n') : '');
const names = (list) => (list ?? []).map((each) => (typeof each === 'string' ? each : each.name));
const same = (a, b) => String(a ?? '').replaceAll('\\', '/').replace(/\/$/, '').toLowerCase() === String(b ?? '').replaceAll('\\', '/').replace(/\/$/, '').toLowerCase();

const listRows = ['name | arm | plugins: built in / the seed\'s / other | skills: built in / the seed\'s / other | agents: built in / the seed\'s / other | slash commands | the seed\'s names on the lists (plugins; skills; agents; slash commands) | plugin_errors'];
const tokenRows = ['name | arm | input side of each request of the main conversation (input + cache write + cache read) | first request'];
const firsts = {};
for (const name of process.argv.slice(2)) {
  const lines = readStream(readFileSync(join(LOGS, `${name}.stream.jsonl`), 'utf8'));
  const session = read(join(LOGS, `${name}.session.txt`)) ?? '';
  const arm = (session.match(/^# \S+ \| arm (\S+)/) ?? [])[1] ?? '?';
  const init = lines.find((l) => l.type === 'system' && l.subtype === 'init') ?? {};
  const results = lines.filter((l) => l.type === 'result');

  // The two hook records.
  const seen = read(join(LOGS, `${name}.seen.txt`));
  if (seen !== null) put(`${name}.seen.txt`, ordinal(mask(seen)));
  const guard = read(join(LOGS, `${name}.guard.txt`));
  if (guard !== null) put(`${name}.guard.txt`, mask(guard));

  // Every result line's reply.
  put(`${name}.reply.md`, results.map((r, at) => `${results.length > 1 ? `<!-- result line ${at + 1} of ${results.length} -->\n` : ''}${mask(r.result ?? '')}`).join('\n\n'));

  // The subagent's report (it arrives as a task_notification) and the Agent call that asked for it.
  const spawn = new Map();
  for (const line of lines) {
    if (line.type === 'assistant') for (const b of line.message?.content ?? []) if (b.type === 'tool_use' && (b.name === 'Agent' || b.name === 'Task')) spawn.set(b.id, b.input ?? {});
    if (line.type === 'system' && line.subtype === 'task_notification' && spawn.has(line.tool_use_id)) {
      const input = spawn.get(line.tool_use_id);
      const type = OUR_AGENT.test(String(input.subagent_type)) || BUILT_IN_AGENTS.has(String(input.subagent_type)) ? input.subagent_type : '(another agent)';
      put(`${name}.agent-report.txt`, `# ${name}: the Agent call's subagent_type was "${type}"; this is the summary of the task_notification that came back (status ${line.status})\n${mask(String(line.summary ?? line.result ?? ''))}`);
    }
  }

  // A tool result that is an error: a hook's block or a refused read.
  const calls = new Map();
  for (const line of lines) {
    if (line.type === 'assistant') for (const b of line.message?.content ?? []) if (b.type === 'tool_use') calls.set(b.id, b);
    if (line.type !== 'user') continue;
    for (const b of Array.isArray(line.message?.content) ? line.message.content : []) {
      if (b.type !== 'tool_result' || !b.is_error) continue;
      const call = calls.get(b.tool_use_id);
      const text = mask(textOf(b.content));
      if (/hook/i.test(text)) put(`${name}.blocked-edit.txt`, `# ${name}: the tool result of the ${call?.name} call on src/fares.test.mjs (is_error true), word for word; the plugin folder is written <plugin>\n${text}`);
      else put(`${name}.refused-read.txt`, `# ${name}: the tool result of the ${call?.name} call (is_error true), word for word; the plugin folder is written <plugin>\n${text}`);
    }
  }
  const denied = lines.filter((l) => l.type === 'system' && l.subtype === 'permission_denied');
  if (denied.length) {
    const file = join(out, `${name}.refused-read.txt`);
    const extra = denied.map((d) => `# the stream's permission_denied line: tool_name ${d.tool_name} | decision_reason_type ${d.decision_reason_type} | decision_reason ${d.decision_reason}`).join('\n');
    const asked = (seen ?? '').split('\n').filter((l) => l.startsWith('PermissionRequest')).map((l) => `# the logging hook's line: ${ordinal(mask(l))}`).join('\n');
    writeFileSync(file, `${read(file) ?? ''}${extra}\n${asked}\n`);
  }
  // A hook_response line that is not exit code 0.
  const failed = lines.filter((l) => l.type === 'system' && l.subtype === 'hook_response' && l.exit_code !== 0);
  if (failed.length) put(`${name}.hook-response.txt`, failed.map((l) => `# ${name}: a hook_response line of the stream (--include-hook-events): hook_name ${l.hook_name} | exit_code ${l.exit_code} | outcome ${l.outcome} | stdout ${JSON.stringify(l.stdout ?? '')}\n# its stderr, word for word (the project folder is written <lab>):\n${mask(String(l.stderr ?? '')).replaceAll('\r', '')}`).join('\n'));
  // The slash expansion.
  const expansion = (seen ?? '').split('\n').filter((l) => l.startsWith('UserPromptExpansion'));
  if (expansion.length) put(`${name}.expansion.txt`, `# ${name}: what the project's logging hook wrote for the UserPromptExpansion event\n${expansion.join('\n')}`);

  // Files the session left that a card may show.
  const lab = join(LOGS, `${name}.lab`);
  for (const version of ['1.2.1', '0.4.1']) {
    const note = read(join(lab, 'releases', `v${version}.md`));
    if (note !== null) put(`${name}.release-v${version}.md`, note);
  }
  if (arm === 'stale' || arm === 'guard') {
    const test = read(join(lab, 'src', 'fares.test.mjs'));
    if (test !== null) put(`${name}.fares-test-after.mjs.txt`, test);
  }

  // The init lists, as counts and the seed's own names.
  const plugins = (init.plugins ?? []).map((each) => (typeof each === 'string' ? { name: each } : each));
  const own = plugins.filter((p) => String(p.name).startsWith('cc-plugin-')).length;
  const seedP = plugins.filter((p) => p.name === 'ship-kit');
  const skills = names(init.skills); const agents = names(init.agents); const commands = names(init.slash_commands);
  const seedS = skills.filter((s) => OUR_SKILL.test(s)); const shipped = skills.filter((s) => SHIPPED_SKILLS.has(s)).length;
  const seedA = agents.filter((a) => OUR_AGENT.test(a)); const built = agents.filter((a) => BUILT_IN_AGENTS.has(a)).length;
  const seedC = commands.filter((c) => /release-prep$/.test(c) || c.startsWith('ship-kit:'));
  listRows.push([name, arm, `${plugins.length}: ${own} / ${seedP.length} / ${plugins.length - own - seedP.length}`,
    `${skills.length}: ${shipped} / ${seedS.length} / ${skills.length - shipped - seedS.length}`,
    `${agents.length}: ${built} / ${seedA.length} / ${agents.length - built - seedA.length}`, commands.length,
    `${seedP.map((p) => `${p.name} (source ${p.source}, version ${p.version}, path ${same(p.path, KIT) ? '<plugin>' : 'NOT <plugin>'})`).join(', ') || '-'}; ${seedS.join(', ') || '-'}; ${seedA.join(', ') || '-'}; ${seedC.join(', ') || '-'}`,
    (init.plugin_errors ?? []).length].join(' | '));

  // The main conversation's requests.
  const usage = new Map();
  for (const line of lines) if (line.type === 'assistant' && !line.parent_tool_use_id && line.message?.id && line.message?.usage) usage.set(line.message.id, line.message.usage);
  const sums = [...usage.values()].map((u) => (u.input_tokens ?? 0) + (u.cache_creation_input_tokens ?? 0) + (u.cache_read_input_tokens ?? 0));
  tokenRows.push([name, arm, sums.join(', '), sums[0] ?? '-'].join(' | '));
  (firsts[arm] ??= []).push(sums[0]);
}
put('init-lists.txt', listRows.join('\n'));
const stat = (list) => (list?.length ? `${list.join(', ')} | min ${Math.min(...list)}, max ${Math.max(...list)}, mean ${(list.reduce((a, b) => a + b, 0) / list.length).toFixed(1)}` : '-');
const kit = firsts.kit ?? []; const bare = firsts.bare ?? [];
const mean = (list) => list.reduce((a, b) => a + b, 0) / list.length;
tokenRows.push('', `first request, arm kit (plugin loaded, ship-b.txt): ${stat(kit)}`, `first request, arm bare (no plugin, ship-b.txt): ${stat(bare)}`);
if (kit.length && bare.length) tokenRows.push(`difference of the two means: ${(mean(kit) - mean(bare)).toFixed(1)} | smallest pairwise difference ${Math.min(...kit) - Math.max(...bare)}, largest ${Math.max(...kit) - Math.min(...bare)} | widest spread inside one arm: ${Math.max(Math.max(...kit) - Math.min(...kit), Math.max(...bare) - Math.min(...bare))}`);
put('first-request.txt', tokenRows.join('\n'));
console.log(listRows.join('\n'));
console.log(tokenRows.join('\n'));
