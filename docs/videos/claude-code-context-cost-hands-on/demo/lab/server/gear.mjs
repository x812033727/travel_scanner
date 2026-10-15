// gear-desk：走 stdio 的 MCP 伺服器，不裝任何套件。
import { appendFileSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const rows = readFileSync(join(here, 'stock.tsv'), 'utf8')
  .trim().split('\n').slice(1).map((line) => line.split('\t'));
const SPEAKS = ['2025-11-25', '2025-06-18', '2025-03-26'];
const started = Date.now();
let seen = 0;

// 收到的每一則訊息，記一行在 server/requests.txt
function note(what) {
  seen += 1;
  const n = String(seen).padStart(2, '0');
  const ms = String(Date.now() - started).padStart(6);
  appendFileSync(join(here, 'requests.txt'),
    `${n} +${ms}ms ${what}\n`);
}

const TOOLS = [{
  name: 'find_gear',
  description: '查一個器材代號放在哪個貨架、還剩幾個。',
  inputSchema: { type: 'object', required: ['code'],
    properties: { code: { type: 'string' } } },
}, {
  name: 'low_stock',
  description: '列出剩餘數量低於 below 的器材。',
  inputSchema: { type: 'object', required: ['below'],
    properties: { below: { type: 'integer' } } },
}];

const say = (text, isError = false) => (
  { content: [{ type: 'text', text }], isError });

function call({ name, arguments: args = {} }) {
  if (name === 'find_gear') {
    const row = rows.find(([id]) => id === args.code);
    if (!row) return say(`查無代號：${args.code}`, true);
    const [code, what, shelf, left] = row;
    return say(`${code} ${what}｜貨架 ${shelf}｜剩 ${left}`);
  }
  if (name === 'low_stock') {
    const low = rows.filter((r) => Number(r[3]) < args.below);
    const list = low.map((r) => `${r[0]} ${r[1]} 剩 ${r[3]}`);
    return say(list.join('\n') || '沒有');
  }
  return say(`沒有這個工具：${name}`, true);
}

function answer({ method, params = {} }) {
  if (method === 'initialize') {
    const asked = params.protocolVersion;
    const version = SPEAKS.includes(asked) ? asked : SPEAKS[0];
    return {
      protocolVersion: version,
      capabilities: { tools: {} },
      serverInfo: { name: 'gear-desk', version: '0.1.0' },
      instructions: '器材租借櫃台庫存：代號、貨架、剩餘數量。',
    };
  }
  if (method === 'ping') return {};
  if (method === 'tools/list') return { tools: TOOLS };
  if (method === 'tools/call') return call(params);
  return null;
}

function brief({ method, params = {} }) {
  if (method === 'tools/call') {
    const args = JSON.stringify(params.arguments);
    return `${method} ${params.name} ${args}`;
  }
  const meta = params._meta ?? {};
  const asked = params.protocolVersion
    ?? meta['io.modelcontextprotocol/protocolVersion'];
  return asked ? `${method} asks ${asked}` : String(method);
}

note('start');
const lines = createInterface({ input: process.stdin });
lines.on('line', (line) => {
  let message;
  try { message = JSON.parse(line); } catch { message = null; }
  if (!message) return note('not JSON');
  note(brief(message));
  if (message.id === undefined) return; // 通知不用回
  const result = answer(message);
  const reply = result ? { result }
    : { error: { code: -32601, message: 'Method not found' } };
  const out = { jsonrpc: '2.0', id: message.id, ...reply };
  process.stdout.write(`${JSON.stringify(out)}\n`);
});
lines.on('close', () => note('end'));
