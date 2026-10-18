// gear-desk：走 stdio 的 MCP 伺服器，不裝任何套件。
// node server/gear.mjs <N>：只提供清單上的前 N 個工具。
import { appendFileSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import { TOOLS } from './tools.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const [head, ...lines] = readFileSync(join(here, 'stock.tsv'),
  'utf8').trim().split('\n').map((line) => line.split('\t'));
const rows = lines.map((cells) => Object.fromEntries(
  head.map((key, at) => [key, cells[at]])));
for (const row of rows) row.zone = row.shelf[0];
const SPEAKS = ['2025-11-25', '2025-06-18', '2025-03-26'];
const TODAY = '2026-10-11'; // 資料檔的日期，不讀系統時間
const started = Date.now();
let seen = 0;

// 啟動時給的數字決定提供幾個工具；沒給就是全部。
const asked = Number(process.argv[2] ?? TOOLS.length);
const count = Number.isInteger(asked) && asked >= 0
  ? Math.min(asked, TOOLS.length) : TOOLS.length;
const OPEN = TOOLS.slice(0, count);

// 收到的每一則訊息，記一行在 server/requests.txt
function note(what) {
  seen += 1;
  const n = String(seen).padStart(2, '0');
  const ms = String(Date.now() - started).padStart(6);
  appendFileSync(join(here, 'requests.txt'),
    `${n} +${ms}ms ${what}\n`);
}

// 交給用戶端的定義：名稱、一句說明、一個參數。
const define = ([name, arg, type, , , description]) => ({
  name,
  description,
  inputSchema: { type: 'object', required: [arg],
    properties: { [arg]: { type } } },
});

const LABEL = { left: '剩', kind: '類別', rate: '日租',
  deposit: '押金', grams: '公克', out: '借出',
  checked: '檢查', shelf: '貨架', zone: '區域',
  name: '名稱', code: '代號' };
const say = (text, isError = false) => (
  { content: [{ type: 'text', text }], isError });
const list = (found, field) => say(found.map((r) => (
  `${r.code} ${r.name} ${LABEL[field]} ${r[field]}`
)).join('\n') || '沒有');
const days = (day) => Math.round(
  (Date.parse(TODAY) - Date.parse(day)) / 86400000);

function call({ name, arguments: args = {} }) {
  const tool = OPEN.find((each) => each[0] === name);
  if (!tool) return say(`沒有這個工具：${name}`, true);
  const [, arg, , op, field] = tool;
  const value = args[arg];
  const [group, target] = field.split('/');
  const one = () => rows.find((r) => r.code === value);
  const some = () => rows.filter((r) => r[group] === value);
  const pick = (sign) => some().sort((a, b) => (
    sign * (Number(a[target]) - Number(b[target]))))[0];
  const single = ['find', 'get', 'week', 'due'].includes(op);
  if (single && !one()) return say(`查無代號：${value}`, true);
  const r = single ? one() : null;
  switch (op) {
    case 'find': return say(
      `${r.code} ${r.name}｜貨架 ${r.shelf}｜剩 ${r.left}`);
    case 'get': return say(
      `${r.code} ${r.name}｜${LABEL[field]} ${r[field]}`);
    case 'week': return say(
      `${r.code} ${r.name}｜七天 ${Number(r.rate) * 7}`);
    case 'due': return say(`${r.code} ${r.name}｜第一天 ${
      Number(r.rate) + Number(r.deposit)}`);
    case 'lt': return list(
      rows.filter((x) => Number(x[field]) < value), field);
    case 'gt': return list(
      rows.filter((x) => Number(x[field]) > value), field);
    case 'before': return list(
      rows.filter((x) => x[field] < value), field);
    case 'after': return list(
      rows.filter((x) => x[field] > value), field);
    case 'eq': return list(some(), field);
    case 'has': return list(rows.filter((x) => (
      x[field].includes(value))), field);
    case 'starts': return list(rows.filter((x) => (
      x[field].startsWith(value))), field);
    case 'count': return say(`${value}：${some().length} 種`);
    case 'sum': return say(`${value}：${LABEL[target]} ${
      some().reduce((n, x) => n + Number(x[target]), 0)}`);
    case 'min': return list([pick(1)].filter(Boolean), target);
    case 'max': return list([pick(-1)].filter(Boolean), target);
    case 'stale': return list(rows.filter((x) => (
      days(x.checked) > value)), field);
    case 'busy': return list(rows.filter((x) => (
      Number(x.out) * 100 > value
        * (Number(x.out) + Number(x.left)))), field);
    default: return say(`沒有這個做法：${op}`, true);
  }
}

function answer({ method, params = {} }) {
  if (method === 'initialize') {
    const want = params.protocolVersion;
    const version = SPEAKS.includes(want) ? want : SPEAKS[0];
    return {
      protocolVersion: version,
      capabilities: { tools: {} },
      serverInfo: { name: 'gear-desk', version: '0.2.0' },
      instructions: '器材租借櫃台庫存：代號、貨架、剩餘數量。',
    };
  }
  if (method === 'ping') return {};
  if (method === 'tools/list') {
    return { tools: OPEN.map(define) };
  }
  if (method === 'tools/call') return call(params);
  return null;
}

function brief({ method, params = {} }) {
  if (method === 'tools/call') {
    const args = JSON.stringify(params.arguments);
    return `${method} ${params.name} ${args}`;
  }
  const meta = params._meta ?? {};
  const want = params.protocolVersion
    ?? meta['io.modelcontextprotocol/protocolVersion'];
  return want ? `${method} asks ${want}` : String(method);
}

note(`start with ${OPEN.length} of ${TOOLS.length} tools`);
const input = createInterface({ input: process.stdin });
input.on('line', (line) => {
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
input.on('close', () => note('end'));
