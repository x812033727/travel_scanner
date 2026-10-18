// Runs the practice MCP server by hand: copies lab/server to a temporary folder, starts
// `node server/gear.mjs` there, writes JSON-RPC messages to its stdin one line at a time and
// prints every line it writes back, then the requests.txt it kept and the size of what
// tools/list hands over (the two tool definitions a client may put in front of the model).
// No session, no model, no network.
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

const MESSAGES = [
  { jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'by-hand', version: '0' } } },
  { jsonrpc: '2.0', method: 'notifications/initialized' },
  { jsonrpc: '2.0', id: 2, method: 'tools/list' },
  { jsonrpc: '2.0', id: 3, method: 'tools/call', params: { name: 'find_gear', arguments: { code: 'G-417' } } },
  { jsonrpc: '2.0', id: 4, method: 'tools/call', params: { name: 'low_stock', arguments: { below: 3 } } },
];

async function talk(file, messages) {
  const child = spawn(process.execPath, [file], { cwd: lab, stdio: ['pipe', 'pipe', 'pipe'] });
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
    console.log(`> ${line}`);
    console.log(got === null ? '  (no reply)' : `< ${got}`);
  }
  child.stdin.end();
  const code = await new Promise((resolve) => child.on('close', resolve));
  return { replies, code, stderr };
}

console.log('## node server/gear.mjs, one message at a time (> sent, < received)');
const main = await talk(join('server', 'gear.mjs'), MESSAGES);
console.log(`[server exit ${main.code} after stdin closed | stderr bytes: ${main.stderr.length}]`);
console.log('## server/requests.txt (the +ms column is the time since the server started; it differs every run)');
process.stdout.write(readFileSync(join(lab, 'server', 'requests.txt'), 'utf8'));
const hello = JSON.parse(main.replies[0]).result;
const tools = JSON.parse(main.replies[2]).result.tools;
const json = JSON.stringify(tools);
console.log('## what the server hands a client before any tool is called');
console.log(`instructions: ${[...hello.instructions].length} characters | tools/list: ${tools.length} tools (${tools.map((tool) => tool.name).join(', ')}), ${[...json].length} characters of JSON, ${Buffer.byteLength(json)} bytes`);
for (const tool of tools) console.log(`   ${tool.name}: description ${[...tool.description].length} characters, input schema ${JSON.stringify(tool.inputSchema).length} characters`);
const answers = [3, 4].map((at) => JSON.parse(main.replies[at]).result.content[0].text);
console.log(`## the two answers: ${answers.map((text) => `${[...text].length} characters`).join(' | ')}`);
const ok = main.code === 0 && tools.length === 2 && answers[0] === 'G-417 頭燈｜貨架 D-07｜剩 37';
console.log(`${ok ? 'ok  ' : 'FAIL'} the server answers the handshake, lists two tools and finds G-417 on shelf D-07 with 37 left`);
rmSync(scratch, { recursive: true, force: true });
process.exitCode = ok ? 0 : 1;
