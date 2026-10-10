// runner: what the seed's tally.mjs cuts short. For one session: every tool call with its input
// and the text that came back (long ones cut at 40 lines), who issued it (the main conversation or
// a subagent), the "Base directory for this skill" message, the entries of permission_denials,
// the stream's system lines other than init (hook_started / hook_response and the rest; ids and
// time stamps dropped), what the model wrote between calls, and every result line's reply in
// full. No id is printed; paths are masked; a skill or agent that is not the seed's or built in
// is written "(another skill)" / "(another agent)". rate_limit_event lines are dropped unread.
// Usage: node extras.mjs <name> [--json <out.json>]
import { readFileSync, writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { agentName, KIT, LOGS, makeMask, readStream, skillName } from './mask.mjs';

const [name, flag, outFile] = process.argv.slice(2);
const lines = readStream(readFileSync(join(LOGS, `${name}.stream.jsonl`), 'utf8'));
const init = lines.find((l) => l.type === 'system' && l.subtype === 'init') ?? {};
const results = lines.filter((l) => l.type === 'result');
const cwd = init.cwd ?? '';
const mask = makeMask();
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((b) => (typeof b === 'string' ? b : b.text ?? textOf(b.content))).join('\n') : '');
const inside = (base, p) => { const r = relative(base, p).replaceAll('\\', '/') || '.'; return r.startsWith('..') || /^[A-Za-z]:|^\//.test(r) ? null : r; };
const relIn = (tool, input) => {
  const copy = { ...input };
  for (const key of ['file_path', 'path']) {
    if (typeof copy[key] === 'string' && cwd) {
      const here = inside(cwd, copy[key]); const there = inside(KIT, copy[key]);
      copy[key] = here !== null ? here : there !== null ? `<plugin>/${there}` : '(outside the project)';
    }
  }
  if (tool === 'Skill') { if ('skill' in copy) copy.skill = skillName(copy.skill); if ('name' in copy) copy.name = skillName(copy.name); }
  if (tool === 'Agent' || tool === 'Task') { if ('subagent_type' in copy) copy.subagent_type = agentName(copy.subagent_type); }
  return copy;
};
const calls = []; const byId = new Map(); const says = []; const baseDirs = []; const synthetic = [];
for (const line of lines) {
  const parent = line.parent_tool_use_id ?? null;
  if (line.type === 'assistant') {
    for (const b of line.message?.content ?? []) {
      if (b.type === 'text' && b.text.trim()) says.push({ after: calls.length, under: parent ? byId.get(parent)?.n ?? '?' : null, text: mask(b.text) });
      if (b.type !== 'tool_use' || byId.has(b.id)) continue;
      const mcp = b.name.startsWith('mcp__');
      const call = { n: calls.length + 1, under: parent ? byId.get(parent)?.n ?? '?' : null, tool: mcp ? 'mcp__(a server)' : b.name, input: mcp ? {} : JSON.parse(mask(JSON.stringify(relIn(b.name, b.input ?? {})))), is_error: null, text: null, meta: null };
      calls.push(call); byId.set(b.id, call);
    }
  }
  if (line.type === 'user') {
    const content = line.message?.content;
    const blocks = Array.isArray(content) ? content : [{ type: 'text', text: textOf(content) }];
    for (const b of blocks) {
      if (b.type !== 'tool_result') {
        const text = textOf(b.content ?? b.text ?? b);
        const at = text.indexOf('Base directory for this skill:');
        if (at >= 0) baseDirs.push(mask(text.slice(at).split('\n')[0]));
        if (text.trim()) synthetic.push({ after: calls.length, under: parent ? byId.get(parent)?.n ?? '?' : null, isSynthetic: Boolean(line.isSynthetic), chars: text.length, head: mask(text).split('\n').filter((l) => l.trim()).slice(0, 6) });
        continue;
      }
      const call = byId.get(b.tool_use_id);
      if (!call) continue;
      call.is_error = Boolean(b.is_error);
      call.text = call.tool.startsWith('mcp__') ? '(not shown)' : mask(textOf(b.content));
      const meta = line.tool_use_result;
      if (meta && typeof meta === 'object' && !Array.isArray(meta)) call.meta = Object.fromEntries(Object.entries(meta).filter(([k, v]) => ['status', 'isAsync', 'success', 'commandName', 'allowedTools', 'type'].includes(k) && typeof v !== 'object').map(([k, v]) => [k, typeof v === 'string' ? mask(v) : v]));
    }
  }
}
const denied = new Set(results.flatMap((r) => r.permission_denials ?? []).map((d) => d.tool_use_id));
for (const [id, call] of byId) call.in_permission_denials = denied.has(id);
console.log(`== extras ${name}`);
for (const call of calls) {
  console.log(`call ${call.n}${call.under ? ` [under call ${call.under}]` : ''} ${call.tool} ${JSON.stringify(call.input).replaceAll('\\n', ' <nl> ').slice(0, 700)}`);
  console.log(`  is_error=${call.is_error} | in permission_denials=${call.in_permission_denials}${call.meta && Object.keys(call.meta).length ? ` | tool_use_result: ${JSON.stringify(call.meta)}` : ''}`);
  const body = (call.text ?? '(no result)').split('\n');
  for (const each of body.slice(0, 40)) console.log(`  | ${each.slice(0, 300)}`);
  if (body.length > 40) console.log(`  | [... ${body.length - 40} more lines cut by the runner]`);
}
console.log(`-- "Base directory for this skill" lines: ${baseDirs.length}`);
for (const each of baseDirs) console.log(`  ${each}`);
console.log(`-- user-side text messages that are not tool results: ${synthetic.length}`);
for (const s of synthetic) {
  console.log(`  [after call ${s.after}${s.under ? `, under call ${s.under}` : ''}] isSynthetic=${s.isSynthetic} ${s.chars} chars; first lines:`);
  for (const each of s.head) console.log(`    | ${each.slice(0, 200)}`);
}
console.log(`-- permission_denials over the result lines: ${results.flatMap((r) => r.permission_denials ?? []).length}`);
for (const d of results.flatMap((r) => r.permission_denials ?? [])) {
  const mcp = String(d.tool_name).startsWith('mcp__');
  console.log(`  ${mcp ? 'mcp__(a server)' : d.tool_name} ${mcp ? '' : mask(JSON.stringify(relIn(d.tool_name, d.tool_input ?? {}))).slice(0, 300)} | keys: ${Object.keys(d).sort().join(' ')}`);
}
const DROP = /(^|_)(id|uuid)$|^uuid$|^session_id$|^type$|^output_file$|^timestamp$|^cwd$|^transcript_path$/i;
const system = lines.filter((x) => x.type === 'system' && x.subtype !== 'init');
const tidy = (value, depth = 0) => {
  if (typeof value === 'string') return mask(value).slice(0, 300);
  if (Array.isArray(value)) return value.slice(0, 12).map((v) => tidy(v, depth + 1));
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).filter(([k]) => !DROP.test(k)).map(([k, v]) => [k, tidy(v, depth + 1)]));
  return value;
};
// The repeated block: a hook_started line, and a hook_response line with exit code 0 and nothing
// on output, stdout or stderr. Those are counted by hook name; every other system line is printed.
const quiet = (l) => l.subtype === 'hook_started' || l.subtype === 'thinking_tokens'
  || (l.subtype === 'hook_response' && l.exit_code === 0 && !l.output && !l.stdout && !l.stderr);
const counted = {};
for (const l of system.filter(quiet)) { const key = l.subtype === 'thinking_tokens' ? 'thinking_tokens' : `${l.subtype} ${l.hook_name}`; counted[key] = (counted[key] ?? 0) + 1; }
console.log(`-- system lines other than init: ${system.length}. Trimmed here: ${system.filter(quiet).length} lines that are hook_started, thinking_tokens, or a hook_response with exit code 0 and empty output, stdout and stderr (outcome "success"); counted by hook name:`);
console.log(`  ${Object.entries(counted).map(([key, n]) => `${key} x${n}`).join(' | ') || 'none'}`);
console.log(`  keys on a hook_response line: ${[...new Set(system.filter((l) => l.subtype === 'hook_response').flatMap((l) => Object.keys(l)))].sort().join(' ') || '-'}`);
console.log('  every other system line, in order (ids and time stamps dropped; long text cut at 300):');
for (const l of system.filter((each) => !quiet(each))) {
  const text = JSON.stringify(tidy(l));
  console.log(`  ${text.slice(0, 1200)}${text.length > 1200 ? ' [cut]' : ''}`);
}
console.log(`-- what the model wrote between calls (${says.length} text blocks)`);
for (const s of says) console.log(`  [after call ${s.after}${s.under ? `, under call ${s.under}` : ''}] ${s.text.replaceAll('\n', ' <nl> ').slice(0, 600)}`);
for (const [at, r] of results.entries()) {
  console.log(`-- result line ${at + 1} of ${results.length}: ${r.subtype}, reply in full (${String(r.result ?? '').length} chars)`);
  for (const each of mask(r.result ?? '').split('\n')) console.log(`  | ${each}`);
}
// The main conversation's requests: input side and output tokens (the measurement the brief asks for).
const usage = new Map();
for (const line of lines) if (line.type === 'assistant' && !line.parent_tool_use_id && line.message?.id && line.message?.usage) usage.set(line.message.id, line.message.usage);
console.log(`-- main conversation, per request (input_tokens + cache_creation + cache_read = input side):`);
let at = 0;
for (const u of usage.values()) { at += 1; console.log(`  request ${at}: ${u.input_tokens ?? 0} + ${u.cache_creation_input_tokens ?? 0} + ${u.cache_read_input_tokens ?? 0} = ${(u.input_tokens ?? 0) + (u.cache_creation_input_tokens ?? 0) + (u.cache_read_input_tokens ?? 0)}`); }
if (flag === '--json' && outFile) {
  writeFileSync(outFile, `${JSON.stringify({ name, calls: calls.map((c) => ({ n: c.n, under_call: c.under, tool: c.tool, input: c.input, is_error: c.is_error, in_permission_denials: c.in_permission_denials, result_text: c.text })) }, null, 2)}\n`);
}
