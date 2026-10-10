// runner: what the seed's tally.mjs cuts short. For one session: every tool call with its input
// and the full text that came back (long ones cut at 40 lines), the entries of permission_denials
// (tool and input only), the system lines other than init (subtype and their keys; for
// permission-shaped ones the text fields), the final reply in full.
// No id is printed; paths are masked. rate_limit_event lines are skipped unread.
// Usage: node extras.mjs <logs> <name> [--json <out.json>]
import { readFileSync, writeFileSync } from 'node:fs';
import { homedir, hostname, userInfo } from 'node:os';
import { join, relative } from 'node:path';

const [logs, name, flag, outFile] = process.argv.slice(2);
const lines = readFileSync(join(logs, `${name}.stream.jsonl`), 'utf8').split('\n').filter(Boolean).flatMap((line) => {
  try { return [JSON.parse(line)]; } catch { return []; }
}).filter((l) => l.type !== 'rate_limit_event');
const init = lines.find((l) => l.type === 'system' && l.subtype === 'init') ?? {};
const result = lines.findLast((l) => l.type === 'result') ?? {};
const cwd = init.cwd ?? '';
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const spell = (p) => [...new Set([p.replaceAll('\\', '\\\\'), p, p.replaceAll('\\', '/'), p.replaceAll('\\', '/').replace(/^([A-Za-z]):/, (m, d) => `/${d.toLowerCase()}`)])];
const mask = (text) => {
  let shown = String(text ?? '');
  for (const s of spell(cwd)) if (s) shown = shown.split(s).join('<lab>');
  for (const s of spell(homedir())) if (s) shown = shown.split(s).join('<home>');
  // Claude Code's own one-line summaries cut a path in the middle: what is left of it is not shown.
  shown = shown.replace(/<home>[^"\s]*…/g, '<a path, cut by Claude Code>…');
  shown = shown.replace(new RegExp(`\\b${esc(userInfo().username)}\\b`, 'gi'), '<user>');
  shown = shown.replace(new RegExp(`\\b${esc(hostname())}\\b`, 'gi'), '<host>');
  return shown.replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, '<uuid>').replace(/toolu_[0-9A-Za-z]{6,}/g, 'toolu_<id>');
};
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((b) => (typeof b === 'string' ? b : b.text ?? textOf(b.content))).join('\n') : '');
const relIn = (input) => {
  const copy = { ...input };
  for (const key of ['file_path', 'path']) {
    if (typeof copy[key] === 'string' && cwd) {
      const r = relative(cwd, copy[key]).replaceAll('\\', '/') || '.';
      copy[key] = r.startsWith('..') || /^[A-Za-z]:|^\//.test(r) ? '(outside the project)' : r;
    }
  }
  return copy;
};
const calls = [];
const byId = new Map();
const says = [];
for (const line of lines) {
  if (line.type === 'assistant') {
    for (const b of line.message?.content ?? []) {
      if (b.type === 'text' && b.text.trim()) says.push({ after: calls.length, text: mask(b.text) });
      if (b.type !== 'tool_use' || byId.has(b.id)) continue;
      const call = { n: calls.length + 1, tool: b.name.startsWith('mcp__') ? 'mcp__(a server)' : b.name, input: b.name.startsWith('mcp__') ? {} : JSON.parse(mask(JSON.stringify(relIn(b.input ?? {})))), is_error: null, text: null };
      calls.push(call); byId.set(b.id, call);
    }
  }
  if (line.type === 'user') {
    for (const b of Array.isArray(line.message?.content) ? line.message.content : []) {
      if (b.type !== 'tool_result') continue;
      const call = byId.get(b.tool_use_id);
      if (!call) continue;
      call.is_error = Boolean(b.is_error);
      call.text = mask(textOf(b.content));
    }
  }
}
const deniedIds = new Map((result.permission_denials ?? []).map((d, at) => [d.tool_use_id, at + 1]));
for (const [id, call] of byId) call.in_permission_denials = deniedIds.has(id);
console.log(`== extras ${name}`);
for (const call of calls) {
  const input = call.tool === 'Bash' ? call.input.command : JSON.stringify(call.input);
  console.log(`call ${call.n} ${call.tool} ${String(input).replaceAll('\n', ' <nl> ').slice(0, 400)}`);
  console.log(`  is_error=${call.is_error} | in permission_denials=${call.in_permission_denials}`);
  const body = (call.text ?? '(no result)').split('\n');
  for (const each of body.slice(0, 40)) console.log(`  | ${each.slice(0, 300)}`);
  if (body.length > 40) console.log(`  | [... ${body.length - 40} more lines cut by the runner]`);
}
console.log(`-- permission_denials on the result line: ${(result.permission_denials ?? []).length}`);
for (const d of result.permission_denials ?? []) {
  const keys = Object.keys(d).sort().join(' ');
  console.log(`  ${String(d.tool_name).startsWith('mcp__') ? 'mcp__(a server)' : d.tool_name} ${mask(JSON.stringify(relIn(d.tool_input ?? {}))).slice(0, 300)} | keys: ${keys}`);
}
console.log('-- system lines other than init');
for (const l of lines.filter((x) => x.type === 'system' && x.subtype !== 'init')) {
  const shown = {};
  for (const [k, v] of Object.entries(l)) {
    if (['uuid', 'session_id', 'tool_use_id', 'type', 'task_id', 'run_id', 'summarizes_uuid', 'output_file'].includes(k)) continue;
    shown[k] = typeof v === 'string' ? mask(v).slice(0, 300) : (v && typeof v === 'object' ? JSON.parse(mask(JSON.stringify(v)).slice(0, 100000)) : v);
  }
  const text = JSON.stringify(shown);
  console.log(`  ${text.slice(0, 600)}${text.length > 600 ? ' [cut]' : ''}`);
}
console.log(`-- what the model wrote between calls (${says.length} text blocks)`);
for (const s of says) console.log(`  [after call ${s.after}] ${s.text.replaceAll('\n', ' <nl> ').slice(0, 500)}`);
console.log(`-- final reply in full (${String(result.result ?? '').length} chars)`);
for (const each of mask(result.result ?? '').split('\n')) console.log(`  | ${each}`);
if (flag === '--json' && outFile) {
  writeFileSync(outFile, `${JSON.stringify({ name, calls: calls.map((c) => ({ n: c.n, tool: c.tool, input: c.input, is_error: c.is_error, in_permission_denials: c.in_permission_denials, result_text: c.text })) }, null, 2)}\n`);
}
