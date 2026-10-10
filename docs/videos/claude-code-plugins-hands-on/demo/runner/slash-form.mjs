// runner: in which spelling the plugin folder appears in one session's stream, place by place.
// The folder itself is never printed: each occurrence is reported as "backslash", "slash",
// "double backslash" or "posix (/c/...)", with the drive letter's case, and the text right after
// it (masked).
// Usage: node slash-form.mjs <name>
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { KIT, LOGS, makeMask, readStream } from './mask.mjs';

const name = process.argv[2];
const mask = makeMask();
const lines = readStream(readFileSync(join(LOGS, `${name}.stream.jsonl`), 'utf8'));
const fwd = KIT.replaceAll('\\', '/');
const forms = [];
for (const [drive, label] of [[fwd[0].toUpperCase(), 'upper'], [fwd[0].toLowerCase(), 'lower']]) {
  const base = drive + fwd.slice(1);
  forms.push([base.replaceAll('/', '\\\\'), `double backslash, drive letter ${label} case`]);
  forms.push([base.replaceAll('/', '\\'), `backslash, drive letter ${label} case`]);
  forms.push([base, `slash, drive letter ${label} case`]);
}
forms.push([`/${fwd[0].toLowerCase()}${fwd.slice(2)}`, 'posix (/c/...)']);
const formOf = (text) => {
  const out = [];
  const source = String(text ?? '');
  for (const [spelling, label] of forms) {
    let at = source.indexOf(spelling);
    while (at >= 0) {
      const after = source.slice(at + spelling.length, at + spelling.length + 36).split(/[\s"'\])]/)[0];
      out.push(`${label}, followed by "${mask(after)}"`);
      at = source.indexOf(spelling, at + spelling.length);
    }
  }
  return out;
};
const textOf = (content) => (typeof content === 'string' ? content
  : Array.isArray(content) ? content.map((b) => (typeof b === 'string' ? b : b.text ?? textOf(b.content))).join('\n') : '');
const seen = new Map();
const report = (label, text) => {
  for (const form of formOf(text)) {
    const key = `${label}: ${form}`;
    seen.set(key, (seen.get(key) ?? 0) + 1);
  }
};
const init = lines.find((l) => l.type === 'system' && l.subtype === 'init') ?? {};
const plug = (init.plugins ?? []).find((p) => p.name === 'ship-kit');
if (plug) report('init plugins[].path', plug.path);
for (const line of lines) {
  if (line.type === 'user') {
    const content = line.message?.content;
    const blocks = Array.isArray(content) ? content : [{ type: 'text', text: textOf(content) }];
    for (const b of blocks) {
      const text = textOf(b.content ?? b.text ?? b);
      if (b.type === 'tool_result') report(b.is_error ? 'a tool result marked as an error' : 'a tool result', text);
      else report('a user-side text message (the skill\'s body)', text);
    }
  }
  if (line.type === 'assistant') for (const b of line.message?.content ?? []) if (b.type === 'tool_use') report(`a ${b.name} call's input`, Object.values(b.input ?? {}).filter((v) => typeof v === 'string').join('\n'));
  if (line.type === 'system' && line.subtype === 'hook_response') report(`hook_response ${line.hook_name} exit ${line.exit_code}`, `${line.output ?? ''}\n${line.stderr ?? ''}\n${line.stdout ?? ''}`);
}
console.log(`-- the plugin folder's spelling in ${name} (each distinct place and spelling, with how many times)`);
for (const [key, times] of seen) console.log(`   ${key} (x${times})`);
if (!seen.size) console.log('   (the plugin folder is not written anywhere in the places looked at)');
if (plug) console.log(`   init plugins[] entry for ship-kit, other fields: version ${JSON.stringify(plug.version)} | source ${mask(JSON.stringify(plug.source))}`);
