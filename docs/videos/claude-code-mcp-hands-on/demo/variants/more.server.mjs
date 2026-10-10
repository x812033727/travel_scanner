// gear-more: ten more tools for the same counter, there only to be listed. The "wide" arms
// connect it next to gear to see what tools nobody calls cost. Every call answers with an error;
// nothing is read or written except requests-more.txt in this folder. No dependencies.
import { appendFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const SPEAKS = ['2025-11-25', '2025-06-18', '2025-03-26'];
const started = Date.now();
let seen = 0;
const note = (what) => {
  seen += 1;
  appendFileSync(join(here, 'requests-more.txt'),
    `${String(seen).padStart(2, '0')} +${String(Date.now() - started).padStart(6)}ms ${what}\n`);
};
const text = { type: 'string' };
const whole = { type: 'integer' };
const tool = (name, description, properties) => ({
  name, description, inputSchema: { type: 'object', required: Object.keys(properties), properties },
});
const TOOLS = [
  tool('reserve_gear', '替一位客人保留一件器材，從取件日保留到歸還日。', { code: text, customer: text, from: text, until: text }),
  tool('cancel_reservation', '取消一筆保留，並把數量加回庫存。', { reservation: text, reason: text }),
  tool('check_out', '客人取件：把一筆保留改成出租中，記下押金。', { reservation: text, deposit: whole }),
  tool('check_in', '客人歸還：記下歸還時的狀況，需要清潔或維修就標記。', { reservation: text, condition: text }),
  tool('list_reservations', '列出某一天要取件或要歸還的保留。', { day: text, kind: text }),
  tool('move_shelf', '把一個器材代號搬到另一個貨架。', { code: text, shelf: text }),
  tool('adjust_stock', '盤點後修正一個器材代號的剩餘數量，並寫下原因。', { code: text, left: whole, reason: text }),
  tool('price_quote', '依器材代號與租借天數算出租金與押金。', { code: text, days: whole }),
  tool('repair_ticket', '替一件器材開一張維修單，維修期間不出租。', { code: text, problem: text }),
  tool('daily_summary', '某一天的出租、歸還、逾期與缺貨的件數。', { day: text }),
];

function answer({ method, params = {} }) {
  if (method === 'initialize') {
    const asked = params.protocolVersion;
    return {
      protocolVersion: SPEAKS.includes(asked) ? asked : SPEAKS[0],
      capabilities: { tools: {} },
      serverInfo: { name: 'gear-more', version: '0.1.0' },
      instructions: '器材租借櫃台的保留、取件、歸還、搬貨架、盤點與報價。',
    };
  }
  if (method === 'ping') return {};
  if (method === 'tools/list') return { tools: TOOLS };
  if (method === 'tools/call') {
    return { content: [{ type: 'text', text: '這個工具只是擺著的，沒有接任何東西。' }], isError: true };
  }
  return null;
}

note('start');
const lines = createInterface({ input: process.stdin });
lines.on('line', (line) => {
  let message;
  try { message = JSON.parse(line); } catch { return note('not JSON'); }
  note(message.method === 'tools/call' ? `tools/call ${message.params?.name}` : String(message.method));
  if (message.id === undefined) return;
  const result = answer(message);
  const reply = result ? { result } : { error: { code: -32601, message: 'Method not found' } };
  process.stdout.write(`${JSON.stringify({ jsonrpc: '2.0', id: message.id, ...reply })}\n`);
});
lines.on('close', () => note('end'));
