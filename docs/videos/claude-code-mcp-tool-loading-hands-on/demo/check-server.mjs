// Runs the practice MCP server by hand and measures what it hands a client. It copies lab/server
// to a temporary folder, starts `node server/gear.mjs <N>` there for N = 0, 2, 10 and 40, writes
// JSON-RPC messages to its stdin one line at a time, and prints: the size of each tools/list
// answer (the definitions a client may put in front of the model), the size of every single
// definition, the size of the names alone, and one call of every tool.
// No session, no model, no network. Sizes are characters (code points) and UTF-8 bytes of the
// JSON the server wrote; nothing here is a token count.
// Usage: node <seed>/check-server.mjs
import { spawn } from 'node:child_process';
import { cpSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'gear-hand-'));
const lab = join(scratch, 'lab');
cpSync(join(seed, 'lab'), lab, { recursive: true });
const chars = (text) => [...text].length;
const bytes = (text) => Buffer.byteLength(text);
let failed = 0;
const check = (ok, what) => { if (!ok) failed += 1; console.log(`${ok ? 'ok  ' : 'FAIL'} ${what}`); };

async function talk(count, messages, echo) {
  const child = spawn(process.execPath, [join('server', 'gear.mjs'), ...(count === null ? [] : [String(count)])], { cwd: lab, stdio: ['pipe', 'pipe', 'pipe'] });
  let buffer = '';
  let stderr = '';
  const waiting = [];
  child.stdout.setEncoding('utf8').on('data', (chunk) => {
    buffer += chunk;
    let at;
    while ((at = buffer.indexOf('\n')) >= 0) {
      const line = buffer.slice(0, at);
      buffer = buffer.slice(at + 1);
      (waiting.shift() ?? (() => {}))(line);
    }
  });
  child.stderr.setEncoding('utf8').on('data', (chunk) => { stderr += chunk; });
  const replies = [];
  for (const message of messages) {
    const line = JSON.stringify(message);
    const expectsReply = message.id !== undefined;
    const reply = new Promise((resolve) => {
      const timer = setTimeout(() => resolve(null), expectsReply ? 3000 : 300);
      waiting.push((got) => { clearTimeout(timer); resolve(got); });
    });
    child.stdin.write(`${line}\n`);
    const got = await reply;
    if (got === null) waiting.shift();
    replies.push(got);
    if (echo) { console.log(`> ${line}`); console.log(got === null ? '  (no reply)' : `< ${got.length > 300 ? `${got.slice(0, 300)} ... (${got.length} characters)` : got}`); }
  }
  child.stdin.end();
  const code = await new Promise((resolve) => child.on('close', resolve));
  return { replies, code, stderr };
}

const HELLO = [
  { jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'by-hand', version: '0' } } },
  { jsonrpc: '2.0', method: 'notifications/initialized' },
  { jsonrpc: '2.0', id: 2, method: 'tools/list' },
];

console.log('## node server/gear.mjs 2, one message at a time (> sent, < received)');
const two = await talk(2, [...HELLO,
  { jsonrpc: '2.0', id: 3, method: 'tools/call', params: { name: 'find_gear', arguments: { code: 'G-417' } } },
  { jsonrpc: '2.0', id: 4, method: 'tools/call', params: { name: 'low_stock', arguments: { below: 3 } } },
  { jsonrpc: '2.0', id: 5, method: 'tools/call', params: { name: 'gear_kind', arguments: { code: 'G-417' } } },
], true);
console.log(`[server exit ${two.code} after stdin closed | stderr bytes: ${two.stderr.length}]`);
console.log('## server/requests.txt of that run (the +ms column is the time since the server started; it differs every run)');
process.stdout.write(readFileSync(join(lab, 'server', 'requests.txt'), 'utf8'));
const hello = JSON.parse(two.replies[0]).result;
const answer = JSON.parse(two.replies[3]).result.content[0].text;
const third = JSON.parse(two.replies[5]).result;

console.log('## what the server hands a client before any tool is called, for each N');
console.log(`instructions: ${chars(hello.instructions)} characters, ${bytes(hello.instructions)} bytes (the same for every N)`);
console.log('N  | tools/list JSON: characters, bytes | per definition: least, most, mean characters | names with the mcp__gear__ prefix: characters');
const lists = {};
for (const count of [0, 2, 10, 40]) {
  const run = await talk(count, HELLO, false);
  const tools = JSON.parse(run.replies[2]).result.tools;
  lists[count] = tools;
  const json = JSON.stringify(tools);
  const each = tools.map((tool) => chars(JSON.stringify(tool)));
  const names = tools.map((tool) => `mcp__gear__${tool.name}`).join('\n');
  const mean = each.length ? Math.round((each.reduce((a, b) => a + b, 0) / each.length) * 10) / 10 : 0;
  console.log(`${String(count).padEnd(2)} | ${tools.length} tools: ${chars(json)}, ${bytes(json)} | ${each.length ? `${Math.min(...each)}, ${Math.max(...each)}, ${mean}` : '-'} | ${chars(names)}`);
}
const all = await talk(null, HELLO, false);
const everything = JSON.parse(all.replies[2]).result.tools;
console.log(`(no number given: ${everything.length} tools)`);

console.log('## every definition, as the server writes it (characters of its JSON | of its description | name)');
lists[40].forEach((tool, at) => console.log(`${String(at + 1).padStart(2)} ${String(chars(JSON.stringify(tool))).padStart(4)} ${String(chars(tool.description)).padStart(3)}  ${tool.name}`));
const slice = (from, to) => { const part = lists[40].slice(from, to).map((tool) => chars(JSON.stringify(tool))); return `${part.reduce((a, b) => a + b, 0)} characters over ${part.length} definitions, mean ${Math.round((part.reduce((a, b) => a + b, 0) / part.length) * 10) / 10}`; };
console.log(`definitions 1-2: ${slice(0, 2)} | 3-10: ${slice(2, 10)} | 11-40: ${slice(10, 40)}`);

// One call of every tool, with an argument that fits its type, against the server with all forty.
const SAMPLE = { code: 'G-417', below: 5, above: 20, shelf: 'D-07', kind: '露營', day: '2026-09-01', zone: 'D', text: '袋', prefix: 'G-4', days: 60, share: 50 };
const calls = lists[40].map((tool, at) => {
  const arg = tool.inputSchema.required[0];
  return { jsonrpc: '2.0', id: 100 + at, method: 'tools/call', params: { name: tool.name, arguments: { [arg]: SAMPLE[arg] } } };
});
const called = await talk(40, [...HELLO, ...calls], false);
const results = called.replies.slice(3).map((reply) => (reply ? JSON.parse(reply).result : null));
const sizes = results.map((result) => (result ? chars(result.content[0].text) : -1));
console.log(`## one call of each of the forty tools: answered ${results.filter(Boolean).length} | isError ${results.filter((result) => result?.isError).length} | answers of 2 characters or fewer (nothing found): ${sizes.filter((size) => size >= 0 && size <= 2).length} | characters least ${Math.min(...sizes)}, most ${Math.max(...sizes)}`);

const sameOrder = (a, b) => a.every((tool, at) => JSON.stringify(tool) === JSON.stringify(b[at]));
check(two.code === 0 && lists[2].length === 2 && answer === 'G-417 頭燈｜貨架 D-07｜剩 37', 'with 2 the server answers the handshake, lists two tools and finds G-417 on shelf D-07 with 37 left');
check(chars(JSON.stringify(lists[2])) === 302 && chars(hello.instructions) === 20, 'its two definitions and its instructions are the size the previous video measured (302 and 20 characters)');
check(third.isError === true, 'a tool beyond the first N is refused by the server itself (gear_kind with N = 2)');
check(lists[0].length === 0 && lists[10].length === 10 && lists[40].length === 40 && everything.length === 40, 'N = 0, 10, 40 and no number list 0, 10, 40 and 40 tools');
check(sameOrder(lists[2], lists[10]) && sameOrder(lists[10], lists[40]), 'a larger N only adds definitions after the ones a smaller N lists');
check(new Set(lists[40].map((tool) => tool.name)).size === 40 && lists[40].every((tool) => /^[a-z_]{6,20}$/.test(tool.name)), 'forty different names, lower-case letters and underscores');
check(lists[40].every((tool) => Object.keys(tool.inputSchema.properties).length === 1), 'every tool takes exactly one argument');
check(results.every((result) => result && !result.isError), 'every tool answers its sample call without an error');
// The rule script asks "is it a straight line" in these characters: its constants must be today's.
const measured = { up: {}, names: {} };
for (const count of [0, 2, 10, 40]) {
  measured.up[count] = chars(JSON.stringify(lists[count]));
  measured.names[count] = chars(lists[count].map((tool) => `mcp__gear__${tool.name}`).join('\n'));
}
const constants = (readFileSync(join(seed, 'runner', 'ladder.mjs'), 'utf8').match(/^const CHARS = (\{.*\});$/m) ?? [])[1];
check(constants === JSON.stringify(measured), `runner/ladder.mjs holds these sizes as its constants (${JSON.stringify(measured)})`);
rmSync(scratch, { recursive: true, force: true });
process.exitCode = failed ? 1 : 0;
