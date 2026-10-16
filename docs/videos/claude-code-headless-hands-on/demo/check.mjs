import { readFileSync } from 'node:fs';

const args = process.argv.slice(2);
const [file, code, inbox = 'inbox.txt'] = args;
const text = readFileSync(inbox, 'utf8').trim();
const want = text.match(/^#\d+/gm) ?? [];
let run = {};
try { run = JSON.parse(readFileSync(file, 'utf8')); } catch {}
const items = run.structured_output?.items ?? [];
const got = items.map((item) => `#${item.id}`);

const ok = code === '0' && run.is_error === false
  && got.sort().join() === want.sort().join();

if (!ok) {
  const kind = run.subtype ?? 'no result';
  const ids = `${got.length}/${want.length}`;
  console.log(`FAILED exit ${code}, ${kind}, ids ${ids}`);
  process.exitCode = 1;
} else {
  for (const item of items) {
    const flag = item.urgent ? 'URGENT' : '-';
    console.log(item.id, item.type, flag);
  }
  const urgent = items.filter((item) => item.urgent).length;
  console.log(`${items.length} items, ${urgent} urgent`);
  process.exitCode = urgent ? 2 : 0;
}
