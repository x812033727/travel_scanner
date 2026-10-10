// Runs the practice server by hand: copies gear-lab to a temporary folder, starts
// `node server/gear.mjs` there, writes JSON-RPC messages to its stdin one line at a time and
// prints every line it writes back, then prints the requests.txt it kept. The messages are the
// ones the MCP specification describes (the 2026-07-28 probe, then the 2025-11-25 handshake);
// which of them Claude Code really sends is for the first session to show. Then the same for the
// ten-tool server of the "wide" arms, listing only. No session, no model, no network.
// Usage: node <seed>/check-server.mjs
import { spawn } from 'node:child_process';
import { cpSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const seed = dirname(fileURLToPath(import.meta.url));
const scratch = mkdtempSync(join(tmpdir(), 'gear-lab-hand-'));
const lab = join(scratch, 'gear-lab');
cpSync(join(seed, 'gear-lab'), lab, { recursive: true });
cpSync(join(seed, 'variants', 'more.server.mjs'), join(lab, 'server', 'more.mjs'));

const meta = { 'io.modelcontextprotocol/protocolVersion': '2026-07-28', 'io.modelcontextprotocol/clientCapabilities': {} };
const MESSAGES = [
  { jsonrpc: '2.0', id: 'probe', method: 'server/discover', params: { _meta: meta } },
  { jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'by-hand', version: '0' } } },
  { jsonrpc: '2.0', method: 'notifications/initialized' },
  { jsonrpc: '2.0', id: 2, method: 'tools/list' },
  { jsonrpc: '2.0', id: 3, method: 'tools/call', params: { name: 'find_gear', arguments: { code: 'G-417' } } },
  { jsonrpc: '2.0', id: 4, method: 'tools/call', params: { name: 'low_stock', arguments: { below: 3 } } },
  { jsonrpc: '2.0', id: 5, method: 'tools/call', params: { name: 'find_gear', arguments: { code: 'G-999' } } },
  { jsonrpc: '2.0', id: 6, method: 'tools/call', params: { name: 'sell_gear', arguments: {} } },
  { jsonrpc: '2.0', id: 7, method: 'resources/list' },
  { jsonrpc: '2.0', id: 8, method: 'initialize', params: { protocolVersion: '1999-01-01', capabilities: {}, clientInfo: { name: 'by-hand', version: '0' } } },
  'this line is not JSON',
  { jsonrpc: '2.0', id: 9, method: 'ping' },
];

// One message at a time: write it, wait for the reply (or 300 ms for a message that gets none).
async function talk(file, messages, show) {
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
    const line = typeof message === 'string' ? message : JSON.stringify(message);
    const expectsReply = typeof message !== 'string' && message.id !== undefined;
    const reply = new Promise((resolve) => {
      const timer = setTimeout(() => resolve(null), expectsReply ? 3000 : 300);
      waiting.push((got) => { clearTimeout(timer); resolve(got); });
    });
    child.stdin.write(`${line}\n`);
    const got = await reply;
    if (got === null) waiting.shift();
    replies.push(got);
    if (show) {
      console.log(`> ${line}`);
      console.log(got === null ? '  (no reply)' : `< ${got}`);
    }
  }
  child.stdin.end();
  const code = await new Promise((resolve) => child.on('close', resolve));
  return { replies, code, stderr };
}

console.log('## node server/gear.mjs, one message at a time (> sent, < received)');
const main = await talk(join('server', 'gear.mjs'), MESSAGES, true);
console.log(`[server exit ${main.code} after stdin closed | stderr bytes: ${main.stderr.length}]`);
console.log('## server/requests.txt (the +ms column is the time since the server started; it differs every run)');
process.stdout.write(readFileSync(join(lab, 'server', 'requests.txt'), 'utf8'));

const listed = JSON.parse(main.replies[3]).result.tools;
const size = (tools) => JSON.stringify(tools).length;
console.log('## what tools/list hands over');
console.log(`gear: ${listed.length} tools (${listed.map((tool) => tool.name).join(', ')}), ${size(listed)} characters of JSON`);
const more = await talk(join('server', 'more.mjs'), [MESSAGES[1], MESSAGES[2], MESSAGES[3]], false);
const moreTools = JSON.parse(more.replies[2]).result.tools;
console.log(`gear-more: ${moreTools.length} tools (${moreTools.map((tool) => tool.name).join(', ')}), ${size(moreTools)} characters of JSON`);
console.log(`[gear-more exit ${more.code} | requests-more.txt lines: ${readFileSync(join(lab, 'server', 'requests-more.txt'), 'utf8').trim().split('\n').length}]`);
rmSync(scratch, { recursive: true, force: true });
